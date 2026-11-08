"""
Mini App REST API under /api/v1. Every route needs a valid Telegram initData header.
"""

import json
import logging
import random
import time
from collections import defaultdict, deque
from typing import Any, Optional

from aiogram.types import BufferedInputFile
from aiohttp import web

import config
from services import attempts, cards, centers, plan, review, subscription, users, writing_ai
from services.auth_service import validate_telegram_init_data
from services.content import SAT_DOMAINS, content

logger = logging.getLogger(__name__)
routes = web.RouteTableDef()

RATE_LIMIT = 120
RATE_WINDOW_SECONDS = 60
_requests: dict[int, deque] = defaultdict(deque)


def ok(data: Any = None, status: int = 200) -> web.Response:
    return web.json_response(data if data is not None else {}, status=status, dumps=lambda v: json.dumps(v, ensure_ascii=False))


def fail(code: str, status: int = 400) -> web.Response:
    return web.json_response({"error": code}, status=status)


def _allowed(user_id: int) -> bool:
    now = time.monotonic()
    window = _requests[user_id]
    while window and now - window[0] > RATE_WINDOW_SECONDS:
        window.popleft()
    if len(window) >= RATE_LIMIT:
        return False
    window.append(now)
    return True


@web.middleware
async def api_middleware(request: web.Request, handler):
    if not request.path.startswith("/api/"):
        return await handler(request)
    valid, tg_user, _ = validate_telegram_init_data(request.headers.get("X-Telegram-Init-Data", ""), request.app["bot_token"])
    if not valid:
        return fail("unauthorized", 401)
    user_id = tg_user["id"]
    if not _allowed(user_id):
        return fail("rate_limited", 429)
    if not await subscription.may_use(request.app.get("bot"), user_id):
        return web.json_response({"error": "not_subscribed", "channel": config.CHANNEL_URL}, status=403)
    user = await users.get_user(user_id)
    if user is None:
        user, _ = await users.touch_user(tg_user)
    request["tg_user"] = tg_user
    request["user"] = user
    try:
        return await handler(request)
    except attempts.AttemptError as e:
        return fail(str(e))
    except web.HTTPException:
        raise
    except Exception:
        logger.exception("API error on %s", request.path)
        return fail("server_error", 500)


async def read_json(request: web.Request) -> dict[str, Any]:
    try:
        body = await request.json()
    except ValueError:
        raise web.HTTPBadRequest(text='{"error":"bad_json"}', content_type="application/json")
    if not isinstance(body, dict):
        raise web.HTTPBadRequest(text='{"error":"bad_json"}', content_type="application/json")
    return body


def public_user(row: dict[str, Any]) -> dict[str, Any]:
    keys = ("id", "first_name", "focus", "target_sat", "target_ielts", "exam_date", "daily_minutes", "reminder_hour", "best_streak")
    return {
        **{key: row[key] for key in keys},
        "onboarded": bool(row["onboarded"]), "reminders_on": bool(row["reminders_on"]), "streak": users.current_streak(row),
    }


async def _referral_info(user: dict[str, Any]) -> dict[str, Any]:
    joined, active = await users.referral_count(user["id"])
    return {
        "link": f"https://t.me/{config.BOT_USERNAME}?start=ref_{user['id']}",
        "joined": joined, "active": active, "bonus": user["ai_bonus"],
    }


@routes.get("/api/v1/bootstrap")
async def bootstrap(request: web.Request) -> web.Response:
    user, _ = await users.touch_user(request["tg_user"])
    user_id = user["id"]
    return ok({
        "me": public_user(user),
        "plan": await plan.today_plan(user),
        "summary": await attempts.summary(user_id),
        "mastery": await attempts.mastery(user_id),
        "week": await attempts.week_activity(user_id),
        "due": await review.due_count(user_id),
        "ai": {
            "enabled": bool(config.GEMINI_API_KEY),
            "remaining": await writing_ai.remaining_today(user),
            "limit": config.AI_DAILY_LIMIT + user["ai_bonus"],
        },
        "referral": await _referral_info(user),
        "staff": await centers.is_staff(user_id),
        "admin": centers.is_admin(user_id),
        "desmos_key": config.DESMOS_API_KEY,
        "bot_username": config.BOT_USERNAME,
    })


@routes.post("/api/v1/profile")
async def update_profile(request: web.Request) -> web.Response:
    user = await users.update_profile(request["user"]["id"], users.clean_profile(await read_json(request)))
    return ok({"me": public_user(user), "plan": await plan.today_plan(user)})


async def _session_code(body: dict[str, Any]) -> Optional[str]:
    code = body.get("session")
    if not isinstance(code, str) or not code:
        return None
    session = await centers.get_session(code)
    return session["code"] if session and session["status"] == "open" else None


async def _notify_referrer(request: web.Request, referrer: Optional[int]) -> None:
    bot = request.app.get("bot")
    if not referrer or bot is None:
        return
    try:
        await bot.send_message(
            referrer, "🎁 Taklif qilgan do'stingiz mashqni boshladi. Sizga <b>+1 AI Writing tekshiruvi</b> qo'shildi."
        )
    except Exception as e:
        logger.info("Could not notify referrer %s: %s", referrer, type(e).__name__)


@routes.post("/api/v1/attempts")
async def submit_attempt(request: web.Request) -> web.Response:
    user = request["user"]
    body = await read_json(request)
    kind = body.get("kind")
    if kind == "sat_mock":
        result = await attempts.submit_sat_mock(user["id"], body, await _session_code(body))
    elif kind == "practice":
        result = await attempts.submit_practice(user["id"], body)
    elif kind in ("ielts_reading", "ielts_listening"):
        result = await attempts.submit_ielts(user["id"], body, await _session_code(body))
    else:
        return fail("unknown_kind")
    await _notify_referrer(request, result.pop("referrer"))
    fresh = await users.get_user(user["id"])
    return ok({**result, "me": public_user(fresh), "due": await review.due_count(user["id"])}, status=201)


@routes.get("/api/v1/attempts")
async def list_attempts(request: web.Request) -> web.Response:
    return ok({"attempts": await attempts.list_attempts(request["user"]["id"])})


@routes.get("/api/v1/attempts/{attempt_id}")
async def get_attempt(request: web.Request) -> web.Response:
    found = await attempts.get_attempt(request["user"]["id"], request.match_info["attempt_id"])
    return ok(found) if found else fail("not_found", 404)


@routes.get("/api/v1/practice")
async def practice_set(request: web.Request) -> web.Response:
    query = request.query
    section = query.get("section") if query.get("section") in SAT_DOMAINS else None
    domain = query.get("domain") or None
    difficulty = query.get("difficulty") if query.get("difficulty") in ("Easy", "Medium", "Hard") else None
    try:
        count = min(30, max(1, int(query.get("count", 10))))
    except ValueError:
        count = 10
    return ok({"ids": await review.pick_questions(request["user"]["id"], section, domain, difficulty, count)})


@routes.get("/api/v1/diagnostic")
async def diagnostic_set(request: web.Request) -> web.Response:
    user_id = request["user"]["id"]
    ids: list[str] = []
    for section, domains in SAT_DOMAINS.items():
        for domain in domains:
            ids += await review.pick_questions(user_id, section, domain, "Medium", 1)
            ids += await review.pick_questions(user_id, section, domain, random.choice(("Easy", "Hard")), 1)
    return ok({"ids": ids})


@routes.get("/api/v1/notebook")
async def notebook(request: web.Request) -> web.Response:
    return ok(await review.notebook(request["user"]["id"]))


@routes.post("/api/v1/writing")
async def evaluate_writing(request: web.Request) -> web.Response:
    user = request["user"]
    body = await read_json(request)
    prompt = content.writing_by_id.get(body.get("prompt_id"))
    if prompt is None or not isinstance(body.get("text"), str):
        return fail("bad_request")
    task = 1 if prompt["id"].startswith("w1") else 2
    minutes = body.get("minutes") if isinstance(body.get("minutes"), int) else 0
    try:
        result = await writing_ai.evaluate(user, task, prompt["prompt"], prompt["id"], body["text"], minutes)
    except writing_ai.WritingError as e:
        return fail(e.code, 429 if e.code in ("limit_reached", "ai_busy") else 400)
    await users.mark_active(user["id"])
    fresh = await users.get_user(user["id"])
    return ok({**result, "remaining": await writing_ai.remaining_today(fresh), "me": public_user(fresh)}, status=201)


@routes.get("/api/v1/writing")
async def writing_history(request: web.Request) -> web.Response:
    user = request["user"]
    return ok({"items": await writing_ai.history(user["id"]), "remaining": await writing_ai.remaining_today(user)})


@routes.get("/api/v1/writing/{submission_id}")
async def writing_detail(request: web.Request) -> web.Response:
    found = await writing_ai.get_submission(request["user"]["id"], request.match_info["submission_id"])
    return ok(found) if found else fail("not_found", 404)


def _session_info(session: dict[str, Any]) -> dict[str, Any]:
    keys = ("code", "title", "kind", "ref", "status", "created_at")
    return {key: session[key] for key in keys}


@routes.post("/api/v1/sessions/join")
async def join_session(request: web.Request) -> web.Response:
    body = await read_json(request)
    code = body.get("code")
    if not isinstance(code, str) or not code.strip():
        return fail("bad_request")
    session = await centers.join_session(request["user"]["id"], code)
    return ok({"session": _session_info(session)}) if session else fail("session_not_found", 404)


async def _staff_or_403(request: web.Request) -> Optional[web.Response]:
    if not await centers.is_staff(request["user"]["id"]):
        return fail("forbidden", 403)
    return None


async def _managed_session(request: web.Request) -> tuple[Optional[dict[str, Any]], Optional[web.Response]]:
    session = await centers.get_session(request.match_info["code"])
    if session is None:
        return None, fail("not_found", 404)
    if not await centers.can_manage(request["user"]["id"], session):
        return None, fail("forbidden", 403)
    return session, None


@routes.get("/api/v1/teacher")
async def teacher_home(request: web.Request) -> web.Response:
    denied = await _staff_or_403(request)
    if denied:
        return denied
    user_id = request["user"]["id"]
    sessions = await centers.list_sessions(user_id)
    return ok({
        "sessions": [{**_session_info(row), "results": row["results"]} for row in sessions],
        "catalog": centers.exam_catalog(),
        "stats": await centers.platform_stats() if centers.is_admin(user_id) else None,
    })


@routes.post("/api/v1/teacher/join")
async def teacher_join(request: web.Request) -> web.Response:
    body = await read_json(request)
    center = await centers.join_as_teacher(str(body.get("code") or ""), request["user"]["id"])
    return ok({"center": center["name"]}) if center else fail("not_found", 404)


@routes.post("/api/v1/teacher/sessions")
async def teacher_create_session(request: web.Request) -> web.Response:
    denied = await _staff_or_403(request)
    if denied:
        return denied
    body = await read_json(request)
    try:
        session = await centers.create_session(
            request["user"]["id"], str(body.get("kind") or ""), str(body.get("ref") or ""), str(body.get("title") or "")
        )
    except ValueError as e:
        return fail(str(e))
    return ok({"session": _session_info(session)}, status=201)


@routes.get("/api/v1/teacher/sessions/{code}")
async def teacher_session(request: web.Request) -> web.Response:
    session, denied = await _managed_session(request)
    if denied:
        return denied
    return ok({"session": _session_info(session), **await centers.session_results(session["code"])})


@routes.post("/api/v1/teacher/sessions/{code}/close")
async def teacher_close_session(request: web.Request) -> web.Response:
    session, denied = await _managed_session(request)
    if denied:
        return denied
    await centers.close_session(session["code"])
    return ok()


@routes.post("/api/v1/teacher/sessions/{code}/export")
async def teacher_export(request: web.Request) -> web.Response:
    session, denied = await _managed_session(request)
    if denied:
        return denied
    bot = request.app.get("bot")
    if bot is None:
        return fail("bot_unavailable", 503)
    data = await centers.session_csv(session["code"])
    await bot.send_document(
        request["user"]["id"], BufferedInputFile(data, filename=f"natijalar_{session['code']}.csv"),
        caption=f"📄 {session['title']} natijalari",
    )
    return ok({"sent": True})


@routes.post("/api/v1/share")
async def share_result(request: web.Request) -> web.Response:
    body = await read_json(request)
    attempt = await attempts.get_attempt(request["user"]["id"], str(body.get("attempt") or ""))
    if attempt is None:
        return fail("not_found", 404)
    base_url = config.WEBAPP_URL.rsplit("/", 1)[0]
    link = f"https://t.me/{config.BOT_USERNAME}?start=ref_{request['user']['id']}"
    return ok({
        "image": f"{base_url}{cards.card_path(attempt['id'], request.app['bot_token'])}",
        "link": link, "text": cards.share_text(attempt),
    })


@routes.post("/api/v1/events")
async def record_event(request: web.Request) -> web.Response:
    body = await read_json(request)
    name = body.get("name")
    if isinstance(name, str) and name:
        await users.record_event(request["user"]["id"], name, str(body.get("meta") or ""))
    return ok()
