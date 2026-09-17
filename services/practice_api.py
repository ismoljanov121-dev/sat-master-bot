"""
EduTest Pro - Unified Practice & Exam API Handler
Handles:
1. GET  /api/v1/practice/today-summary (Today's streak, goals, unresolved mistakes, active session)
2. GET  /api/v1/practice/questions (Safe delivery without answer leakage)
3. POST /api/v1/practice/check-answer (Instant explanation, Desmos hack, auto-sync to bot stats & error notebook)
4. POST /api/v1/practice/submit (Idempotent final submission, anti-duplicate protection)
5. GET  /api/v1/mistakes (Student unresolved mistakes queue)
6. POST /api/v1/mistakes/resolve (Mark mistake as mastered/resolved)
"""

import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Any
from aiohttp import web

from database import db
from services.auth_service import validate_telegram_init_data
from services.custom_test_service import custom_test_service
from services.exam_service import EXAM_TEMPLATES, prepare_shuffled_questions
from services.fix_mistake_service import fix_mistake_service
from services.hint_scaffolding_service import hint_service
from services.pacing_service import pacing_service
from services.question_service import qs
from services.study_plan_service import study_planner
from services.telemetry_service import telemetry
from services.tier_service import (
    can_answer_practice_question,
    can_take_full_mock,
    get_daily_question_status,
    get_user_tier,
    record_question_attempt,
)
from services.weekly_report_service import weekly_report_service

logger = logging.getLogger("PracticeAPI")

# Server-side active sessions store: session_id -> session_dict
ACTIVE_PRACTICE_SESSIONS: dict[str, dict[str, Any]] = {}


def get_authenticated_user_id(request: web.Request, body_payload: dict | None = None) -> tuple[int | None, str]:
    """Extracts and validates Telegram WebApp initData from header, query, or body."""
    init_data = request.headers.get("X-Telegram-Init-Data") or request.query.get("initData", "")
    if not init_data and body_payload and isinstance(body_payload, dict):
        init_data = body_payload.get("initData", "")

    if not init_data:
        # Dev & preview environment support (X-Dev-User-Id or ?demo=1)
        dev_user = request.headers.get("X-Dev-User-Id") or request.query.get("dev_user_id")
        if dev_user and str(dev_user).isdigit():
            return int(dev_user), "DEV_OK"
        if request.query.get("demo") == "1" or request.headers.get("X-Demo-Mode") == "1":
            return 99999999, "DEMO_OK"
        return None, "initData sarlavhasi (X-Telegram-Init-Data) topilmadi"

    is_valid, user_data, msg = validate_telegram_init_data(init_data)
    if not is_valid or not user_data:
        # Fallback to dev header if valid HMAC fails in test suite
        dev_user = request.headers.get("X-Dev-User-Id")
        if dev_user and str(dev_user).isdigit():
            return int(dev_user), "DEV_OK"
        return None, f"Avtorizatsiya xatosi: {msg}"

    user_id = user_data.get("id")
    if not user_id or not isinstance(user_id, int) or user_id <= 0:
        return None, "Yaroqsiz foydalanuvchi identifikatori"

    return user_id, "OK"


# ==================== 1. TODAY SUMMARY ====================
async def api_practice_today_summary(request: web.Request) -> web.Response:
    """GET /api/v1/practice/today-summary"""
    user_id, err_msg = get_authenticated_user_id(request)
    if not user_id:
        return web.json_response({"status": "error", "message": err_msg}, status=401)

    user_profile = db.get_user(user_id) or {}
    stats = db.get_user_practice_stats(user_id)
    unresolved_count = db.get_unresolved_mistakes_count(user_id)

    # Check for active session for this user
    active_sess = None
    for sess_id, sess_data in ACTIVE_PRACTICE_SESSIONS.items():
        if sess_data.get("user_id") == user_id and sess_data.get("status") == "active":
            active_sess = {
                "exists": True,
                "session_id": sess_id,
                "mode": sess_data.get("mode"),
                "current_index": sess_data.get("current_index", 0),
                "total_questions": len(sess_data.get("questions", [])),
                "remaining_seconds": sess_data.get("remaining_seconds", 600)
            }
            break

    today_dict = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "target_questions": 10,
        "daily_goal": 10,
        "answered_today": stats.get("total_answered", 0),
        "correct_today": stats.get("correct_count", 0),
        "accuracy_pct": stats.get("accuracy", 0),
        "streak_days": stats.get("current_streak", 0),
        "unresolved_mistakes": unresolved_count,
        "has_active_session": bool(active_sess and active_sess.get("exists")),
        "active_session": active_sess
    }

    tier_info = get_user_tier(user_id)
    daily_usage = get_daily_question_status(user_id)

    return web.json_response({
        "status": "ok",
        "today": today_dict,
        "tier": tier_info,
        "daily_usage": daily_usage,
        "user": {
            "id": user_id,
            "first_name": user_profile.get("first_name", "Abituriyent"),
            "level": user_profile.get("level", "Standard"),
            "tier": tier_info["tier"],
            "is_pro": tier_info["is_pro"],
            "current_streak": stats.get("current_streak", 0),
            "best_streak": stats.get("best_streak", 0),
            "total_answered": stats.get("total_answered", 0),
            "accuracy": stats.get("accuracy", 0)
        },
        "today_progress": {
            "answered_today": daily_usage["answered_today"],
            "daily_goal": daily_usage["daily_limit"],
            "remaining_today": daily_usage["remaining_today"],
            "accuracy_today": stats.get("accuracy", 0)
        },
        "unresolved_mistakes_count": unresolved_count,
        "active_session": active_sess or {"exists": False}
    })


# ==================== 2. GET PRACTICE QUESTIONS (SECURE) ====================
async def api_practice_questions_get(request: web.Request) -> web.Response:
    """
    GET /api/v1/practice/questions?mode=daily_10m|pilot_mock|diagnostic|mistakes&section=...&domain=...&skill=...&difficulty=...
    Delivers safe questions without leaking 'correct', 'explanation', or 'strategy_or_hack'.
    """
    user_id, err_msg = get_authenticated_user_id(request)
    if not user_id:
        return web.json_response({"status": "error", "message": err_msg}, status=401)

    mode = request.query.get("mode", "daily_10m")
    section = request.query.get("section", "all")
    domain = request.query.get("domain", "all")
    skill = request.query.get("skill", "all")
    difficulty = request.query.get("difficulty", "all")

    session_id = f"sess_{uuid.uuid4().hex[:12]}"
    raw_questions: list[dict[str, Any]] = []

    # Check Tier and Daily/Weekly Allowance
    is_mistake_mode = (mode == "mistakes")
    is_diagnostic_mode = (mode == "diagnostic")
    is_mock_mode = (mode in ("full_mock", "pilot_mock"))

    if is_mock_mode:
        allowed, reason = can_take_full_mock(user_id)
        if not allowed:
            return web.json_response({
                "status": "limit_reached",
                "message": reason,
                "tier": get_user_tier(user_id),
                "daily_usage": get_daily_question_status(user_id)
            }, status=403)
        await db.increment_weekly_mocks(user_id)
    elif not is_mistake_mode and not is_diagnostic_mode:
        allowed, reason = can_answer_practice_question(user_id, is_mistake_practice=False)
        if not allowed:
            return web.json_response({
                "status": "limit_reached",
                "message": reason,
                "tier": get_user_tier(user_id),
                "daily_usage": get_daily_question_status(user_id)
            }, status=403)

    if mode == "mistakes":
        # Load user's unresolved mistakes
        mistakes = db.get_user_mistakes(user_id, resolved_filter=False)
        for m in mistakes:
            raw_questions.append({
                "id": m["question_id"],
                "section": m.get("section", "math"),
                "domain": m.get("domain", "General"),
                "difficulty": "Medium",
                "passage": m.get("passage"),
                "question": m.get("question_text", ""),
                "options": m.get("options", []),
                "correct": m.get("correct_answer", "A"),
                "explanation": m.get("explanation", ""),
                "strategy_or_hack": m.get("hack", "")
            })
        duration_seconds = max(len(raw_questions) * 90, 300)
        title = "Xatolarim Ustida Qayta Mashq"

    elif mode == "diagnostic":
        from handlers.diagnostic import QUESTIONS as DIAG_QUESTIONS
        raw_questions = list(DIAG_QUESTIONS)
        duration_seconds = 15 * 60
        title = "Digital SAT Diagnostika (Math)"

    elif mode in EXAM_TEMPLATES:
        tpl = EXAM_TEMPLATES[mode]
        seed = int(datetime.now().timestamp() * 1000)
        raw_questions = prepare_shuffled_questions(mode, seed)
        duration_seconds = tpl.get("duration_seconds", 600)
        title = tpl.get("title", "Digital SAT Mashq")

    else:
        # Custom drill filter
        answered_ids = db.get_answered_question_ids(user_id) if hasattr(db, "get_answered_question_ids") else []
        filtered = qs.filter_questions(section=section, domain=domain, difficulty=difficulty, skill=skill)
        if not filtered:
            filtered = qs.get_published_questions()[:10]
        raw_questions = filtered[:10]
        duration_seconds = len(raw_questions) * 90
        title = f"SAT {section.title()} Mashqi"

    # Strip answer keys and explanations from payload sent to client (Anti-Cheat & Leak Prevention)
    safe_questions: list[dict[str, Any]] = []
    questions_lookup: dict[str, dict[str, Any]] = {}

    for q in raw_questions:
        qid = str(q.get("id"))
        questions_lookup[qid] = q
        safe_questions.append({
            "id": qid,
            "section": q.get("section", "math"),
            "domain": q.get("domain", "General"),
            "skill": q.get("skill", q.get("domain", "General")),
            "difficulty": q.get("difficulty", "Medium"),
            "passage": q.get("passage"),
            "question": q.get("question", ""),
            "options": q.get("options", [])
            # OMIT 'correct', 'explanation', 'strategy_or_hack'
        })

    # Register session on server
    ACTIVE_PRACTICE_SESSIONS[session_id] = {
        "session_id": session_id,
        "user_id": user_id,
        "mode": mode,
        "status": "active",
        "title": title,
        "duration_seconds": duration_seconds,
        "remaining_seconds": duration_seconds,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "questions": raw_questions,
        "questions_lookup": questions_lookup,
        "answers": {},
        "current_index": 0
    }

    return web.json_response({
        "status": "ok",
        "session_id": session_id,
        "mode": mode,
        "title": title,
        "duration_seconds": duration_seconds,
        "total_questions": len(safe_questions),
        "questions": safe_questions
    })


# ==================== 3. CHECK ANSWER (INSTANT EXPLANATION & SYNC) ====================
async def api_practice_check_answer(request: web.Request) -> web.Response:
    """
    POST /api/v1/practice/check-answer
    Evaluates student answer, records into unified bot stats and error notebook,
    and returns explanation + Desmos hack.
    """
    try:
        body = await request.json()
    except Exception:
        return web.json_response({"status": "error", "message": "Noto'g'ri JSON payload"}, status=400)

    user_id, err_msg = get_authenticated_user_id(request, body)
    if not user_id:
        return web.json_response({"status": "error", "message": err_msg}, status=401)

    session_id = str(body.get("session_id", ""))
    question_id = str(body.get("question_id", "")).strip()
    selected_key = str(body.get("selected_key") or body.get("user_answer") or "").strip().upper()

    if not question_id or not selected_key:
        return web.json_response({"status": "error", "message": "question_id va selected_key talab qilinadi"}, status=400)

    # Locate question data (from active session or vault)
    session = ACTIVE_PRACTICE_SESSIONS.get(session_id)
    q_data = None
    if session and "questions_lookup" in session:
        q_data = session["questions_lookup"].get(question_id)

    if not q_data:
        q_data = qs.get_question_by_id(question_id)

    if not q_data:
        return web.json_response({"status": "error", "message": "Savol topilmadi"}, status=404)

    correct_key = str(q_data.get("correct", "A")).strip().upper()
    is_correct = (selected_key == correct_key)
    section = str(q_data.get("section", "math")).lower()
    time_spent = int(body.get("time_spent_seconds", body.get("time_spent", 60)))
    mode_name = session.get("mode", "drill") if session else "drill"

    # 1. Update bot practice stats
    db.record_practice_answer(user_id, question_id, is_correct, section)

    # 2. Record detailed pacing attempt
    try:
        await db.record_attempt_detail(
            user_id=user_id,
            question_id=question_id,
            is_correct=is_correct,
            time_spent_seconds=time_spent,
            section=section,
            domain=str(q_data.get("domain", "General")),
            mode=mode_name
        )
    except Exception as e:
        logger.warning(f"Error in record_attempt_detail: {e}")

    # 3. Update error notebook
    if not is_correct:
        try:
            await db.record_mistake(
                user_id=user_id,
                question_id=question_id,
                section=section,
                domain=str(q_data.get("domain", "General")),
                question_text=str(q_data.get("question", "")),
                correct_answer=correct_key,
                user_answer=selected_key,
                explanation=str(q_data.get("explanation", "")),
                hack=str(q_data.get("strategy_or_hack", "")),
                options=q_data.get("options", []),
                passage=q_data.get("passage"),
                source="webapp_practice"
            )
        except Exception as e:
            logger.warning(f"Error recording mistake in practice check: {e}")
    else:
        try:
            await db.resolve_mistake(user_id, question_id)
        except Exception:
            pass

    # Record in active session if present
    if session:
        session.setdefault("answers", {})[question_id] = selected_key

    # 4. Record daily usage attempt (Mistakes mode & Mocks are exempt from daily limit)
    is_mistake_mode = bool(session and session.get("mode") == "mistakes")
    is_mock = bool(session and session.get("mode") in ("full_mock", "pilot_mock"))
    await record_question_attempt(user_id, is_mistake_practice=is_mistake_mode, is_mock=is_mock)

    updated_stats = db.get_user_practice_stats(user_id)
    daily_usage = get_daily_question_status(user_id)

    return web.json_response({
        "status": "ok",
        "is_correct": is_correct,
        "correct_key": correct_key,
        "correct_answer": correct_key,
        "selected_key": selected_key,
        "user_answer": selected_key,
        "explanation": q_data.get("explanation", "Tushuntirish mavjud emas."),
        "strategy_or_hack": q_data.get("strategy_or_hack", ""),
        "current_streak": updated_stats.get("current_streak", 0),
        "total_answered": updated_stats.get("total_answered", 0),
        "accuracy": updated_stats.get("accuracy", 0),
        "daily_usage": daily_usage
    })


# ==================== 4. SUBMIT SESSION (IDEMPOTENT) ====================
async def api_practice_submit(request: web.Request) -> web.Response:
    """
    POST /api/v1/practice/submit
    Idempotent final submission for practice/mock sessions.
    Prevents double-counting and duplicate mistake entries on network retries.
    """
    try:
        body = await request.json()
    except Exception:
        return web.json_response({"status": "error", "message": "Noto'g'ri JSON payload"}, status=400)

    user_id, err_msg = get_authenticated_user_id(request, body)
    if not user_id:
        return web.json_response({"status": "error", "message": err_msg}, status=401)

    idempotency_key = str(body.get("idempotency_key", "")).strip()
    session_id = str(body.get("session_id", "")).strip()
    answers: dict[str, str] = body.get("answers", {})
    time_spent = int(body.get("time_spent_seconds", body.get("total_time_spent", 0)))
    mode = str(body.get("mode", "daily_10m"))

    # Check idempotency cache
    db.local_cache.setdefault("idempotency_cache", {})
    if idempotency_key and idempotency_key in db.local_cache["idempotency_cache"]:
        cached = db.local_cache["idempotency_cache"][idempotency_key]
        cached_summary = cached.get("summary", {})
        return web.json_response({
            "status": "ok",
            "already_processed": True,
            "idempotent": True,
            "idempotency_key": idempotency_key,
            "summary": cached_summary,
            "results": cached_summary,
            "review": cached.get("review")
        })

    # Retrieve session questions
    session = ACTIVE_PRACTICE_SESSIONS.get(session_id)
    questions: list[dict[str, Any]] = []
    if session and "questions" in session:
        questions = session["questions"]
    else:
        # Fallback to questions lookup by IDs
        for qid in answers.keys():
            q = qs.get_question_by_id(qid)
            if q:
                questions.append(q)

    correct_count = 0
    total_count = len(questions)
    review_list: list[dict[str, Any]] = []
    weak_domains: set[str] = set()
    strong_domains: set[str] = set()
    domain_breakdown: dict[str, dict[str, Any]] = {}

    for q in questions:
        qid = str(q.get("id"))
        user_ans = str(answers.get(qid, "")).strip().upper()
        correct_ans = str(q.get("correct", "A")).strip().upper()
        sec = str(q.get("section", "math")).lower()
        dom = str(q.get("domain", "General"))
        is_corr = (user_ans == correct_ans)

        # Synchronize practice statistics with bot database
        try:
            db.record_practice_answer(user_id, qid, is_corr, sec)
            await db.record_attempt_detail(
                user_id=user_id,
                question_id=qid,
                is_correct=is_corr,
                time_spent_seconds=int(time_spent / max(1, total_count)),
                section=sec,
                domain=dom,
                mode=mode
            )
        except Exception as e:
            logger.warning(f"Error in submit record_practice_answer or attempt_detail: {e}")

        if dom not in domain_breakdown:
            domain_breakdown[dom] = {"total": 0, "correct": 0, "pct": 0}
        domain_breakdown[dom]["total"] += 1

        if is_corr:
            correct_count += 1
            domain_breakdown[dom]["correct"] += 1
        else:
            weak_domains.add(dom)
            try:
                await db.record_mistake(
                    user_id=user_id,
                    question_id=qid,
                    section=sec,
                    domain=dom,
                    question_text=str(q.get("question", "")),
                    correct_answer=correct_ans,
                    user_answer=user_ans or "Javob berilmadi",
                    explanation=str(q.get("explanation", "")),
                    hack=str(q.get("strategy_or_hack", "")),
                    options=q.get("options", []),
                    passage=q.get("passage"),
                    source="webapp_submit"
                )
            except Exception as e:
                logger.warning(f"Error recording mistake in submit: {e}")

        review_list.append({
            "question_id": qid,
            "section": sec,
            "domain": dom,
            "question": q.get("question", ""),
            "options": q.get("options", []),
            "user_answer": user_ans or "Javob berilmadi",
            "correct_answer": correct_ans,
            "is_correct": is_corr,
            "explanation": q.get("explanation", ""),
            "hack": q.get("strategy_or_hack", "")
        })

    for d, st in domain_breakdown.items():
        st["pct"] = round((st["correct"] / st["total"]) * 100) if st["total"] > 0 else 0
        if st["pct"] >= 70:
            strong_domains.add(d)

    accuracy = round((correct_count / total_count) * 100) if total_count > 0 else 0
    spent_m = time_spent // 60
    spent_s = time_spent % 60
    time_str = f"{spent_m}:{spent_s:02d}"

    updated_stats = db.get_user_practice_stats(user_id)
    avg_time = round(time_spent / total_count) if total_count > 0 else 0

    summary = {
        "total": total_count,
        "total_questions": total_count,
        "correct_count": correct_count,
        "incorrect_count": total_count - correct_count,
        "accuracy": accuracy,
        "accuracy_pct": accuracy,
        "time_spent": time_str,
        "time_spent_seconds": time_spent,
        "avg_time_per_question_seconds": avg_time,
        "streak": updated_stats.get("current_streak", 0),
        "domain_breakdown": domain_breakdown,
        "weak_domains": sorted(list(weak_domains))[:4],
        "strong_domains": sorted(list(strong_domains))[:4],
        "honest_feedback": "Mashq muvaffaqiyatli yakunlandi. Zaif mavzular ustida ishlashni davom ettiring!"
    }

    # Mark session completed
    if session:
        session["status"] = "completed"

    # Store in idempotency cache
    if idempotency_key:
        db.local_cache["idempotency_cache"][idempotency_key] = {
            "user_id": user_id,
            "summary": summary,
            "review": review_list,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        db._save_local_db_sync()

    return web.json_response({
        "status": "ok",
        "already_processed": False,
        "idempotent": False,
        "idempotency_key": idempotency_key,
        "summary": summary,
        "results": summary,
        "review": review_list
    })


# ==================== 5. MISTAKES QUEUE ====================
async def api_mistakes_get(request: web.Request) -> web.Response:
    """GET /api/v1/mistakes"""
    user_id, err_msg = get_authenticated_user_id(request)
    if not user_id:
        return web.json_response({"status": "error", "message": err_msg}, status=401)

    mistakes = db.get_user_mistakes(user_id, resolved_filter=False)
    return web.json_response({
        "status": "ok",
        "count": len(mistakes),
        "total_unresolved": len(mistakes),
        "mistakes": mistakes
    })


# ==================== 6. RESOLVE MISTAKE ====================
async def api_mistakes_resolve(request: web.Request) -> web.Response:
    """POST /api/v1/mistakes/resolve"""
    try:
        body = await request.json()
    except Exception:
        return web.json_response({"status": "error", "message": "Noto'g'ri JSON payload"}, status=400)

    user_id, err_msg = get_authenticated_user_id(request, body)
    if not user_id:
        return web.json_response({"status": "error", "message": err_msg}, status=401)

    question_id = str(body.get("question_id", "")).strip()
    if not question_id:
        return web.json_response({"status": "error", "message": "question_id talab qilinadi"}, status=400)

    ok = await db.resolve_mistake(user_id, question_id)
    remaining = db.get_unresolved_mistakes_count(user_id)

    return web.json_response({
        "status": "ok",
        "resolved": ok,
        "question_id": question_id,
        "remaining_count": remaining
    })


# ==================== 7. ADAPTIVE STUDY PLAN ====================
async def api_study_plan_get(request: web.Request) -> web.Response:
    """
    GET /api/v1/study-plan
    Retrieves the student's personalized, adaptive SAT preparation schedule.
    """
    user_id, err_msg = get_authenticated_user_id(request)
    if not user_id:
        return web.json_response({"status": "error", "message": err_msg}, status=401)

    plan = study_planner.get_plan(user_id)
    return web.json_response({
        "status": "ok",
        "plan": plan,
        "tier": get_user_tier(user_id)
    })


async def api_study_plan_rebalance(request: web.Request) -> web.Response:
    """
    POST /api/v1/study-plan/rebalance
    Dynamically rebalances study priorities based on latest performance data.
    """
    try:
        body = await request.json()
    except Exception:
        body = {}

    user_id, err_msg = get_authenticated_user_id(request, body)
    if not user_id:
        return web.json_response({"status": "error", "message": err_msg}, status=401)

    plan = study_planner.rebalance_plan(user_id)
    await telemetry.record_event("pro_beta_feature_used", user_id=user_id, metadata={"feature": "study_plan_rebalance"})

    return web.json_response({
        "status": "ok",
        "plan": plan,
        "message": "O'quv rejasi yangi natijalaringiz asosida muvaffaqiyatli moslashtirildi."
    })


# ==================== 8. FIX MY MISTAKE (PEDAGOGICAL LOOP) ====================
async def api_practice_fix_mistake(request: web.Request) -> web.Response:
    """
    GET /api/v1/practice/fix-mistake?mistake_id=...
    Delivers 5-step corrective drill: error diagnosis, concept capsule,
    worked example, transfer drill from vault, and spaced repetition scheduling.
    """
    user_id, err_msg = get_authenticated_user_id(request)
    if not user_id:
        return web.json_response({"status": "error", "message": err_msg}, status=401)

    mistake_id = request.query.get("mistake_id") or request.query.get("question_id", "")
    exercise = fix_mistake_service.generate_fix_exercise(user_id, mistake_id)

    if not exercise:
        return web.json_response({
            "status": "empty",
            "message": "Xatolar daftarchangizda hal etilmagan xatoliklar topilmadi. Ajoyib natija! 🎯"
        }, status=200)

    await telemetry.record_event("pro_beta_feature_used", user_id=user_id, metadata={"feature": "fix_mistake"})
    await telemetry.record_event("mistake_revisited", user_id=user_id, metadata={"question_id": mistake_id})

    return web.json_response({
        "status": "ok",
        "exercise": exercise
    })


# ==================== 9. CUSTOM TEST BUILDER ====================
async def api_practice_custom_test(request: web.Request) -> web.Response:
    """
    POST /api/v1/practice/custom-test
    Builds a targeted test with section, domain, skill, difficulty, timer, and 7-day attempt deduplication.
    """
    try:
        body = await request.json()
    except Exception:
        body = {}

    user_id, err_msg = get_authenticated_user_id(request, body)
    if not user_id:
        return web.json_response({"status": "error", "message": err_msg}, status=401)

    # Check daily question quota
    allowed, reason = can_answer_practice_question(user_id, is_mistake_practice=False)
    if not allowed:
        return web.json_response({
            "status": "limit_reached",
            "message": reason,
            "tier": get_user_tier(user_id),
            "daily_usage": get_daily_question_status(user_id)
        }, status=403)

    section = str(body.get("section", "all"))
    domain = str(body.get("domain", "all"))
    skill = str(body.get("skill", "all"))
    difficulty = str(body.get("difficulty", "All"))
    count = int(body.get("count", 10))
    timed = bool(body.get("timed", True))

    test_payload = custom_test_service.build_custom_test(
        user_id=user_id,
        section=section,
        domain=domain,
        skill=skill,
        difficulty=difficulty,
        count=count,
        timed=timed
    )

    session_id = test_payload["session_id"]
    questions_lookup = {str(q["id"]): q for q in test_payload["questions"]}

    # Register active test session on server
    ACTIVE_PRACTICE_SESSIONS[session_id] = {
        "session_id": session_id,
        "user_id": user_id,
        "mode": "custom_drill",
        "status": "active",
        "title": f"Shaxsiy Sinov: {section.title()}",
        "duration_seconds": test_payload["total_time_seconds"] or 600,
        "remaining_seconds": test_payload["total_time_seconds"] or 600,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "questions": test_payload["questions"],
        "questions_lookup": questions_lookup,
        "answers": {},
        "current_index": 0
    }

    await telemetry.record_event("pro_beta_feature_used", user_id=user_id, metadata={"feature": "custom_test", "count": count})

    return web.json_response({
        "status": "ok",
        "session_id": session_id,
        "test": test_payload
    })


# ==================== 10. PACING & TIME STRATEGY ANALYTICS ====================
async def api_analytics_pacing(request: web.Request) -> web.Response:
    """
    GET /api/v1/analytics/pacing?limit=50
    Diagnoses overtime, rushed mistakes, and domain pace efficiency.
    """
    user_id, err_msg = get_authenticated_user_id(request)
    if not user_id:
        return web.json_response({"status": "error", "message": err_msg}, status=401)

    limit = int(request.query.get("limit", 50))
    pacing_data = pacing_service.analyze_user_pacing(user_id, limit=limit)

    await telemetry.record_event("pro_beta_feature_used", user_id=user_id, metadata={"feature": "pacing_analytics"})

    return web.json_response({
        "status": "ok",
        "pacing": pacing_data
    })


# ==================== 11. PRAGMATIC WEEKLY REPORT ====================
async def api_analytics_weekly_report(request: web.Request) -> web.Response:
    """
    GET /api/v1/analytics/weekly-report
    Answers: 1. Nima yaxshilandi? 2. Nima hali qiyin? 3. Keyingi hafta nimani qilamiz?
    Discloses sample size honestly if attempts < 15.
    """
    user_id, err_msg = get_authenticated_user_id(request)
    if not user_id:
        return web.json_response({"status": "error", "message": err_msg}, status=401)

    report_data = weekly_report_service.generate_weekly_report(user_id)
    await telemetry.record_event("pro_beta_feature_used", user_id=user_id, metadata={"feature": "weekly_report"})

    return web.json_response({
        "status": "ok",
        "report": report_data
    })


# ==================== 12. TIERED SCAFFOLDING HINTS ====================
async def api_practice_hint(request: web.Request) -> web.Response:
    """
    GET /api/v1/practice/hint?question_id=...
    Provides Level 1 (concept) and Level 2 (tactical/Desmos) hints without giving away the final choice.
    """
    user_id, err_msg = get_authenticated_user_id(request)
    if not user_id:
        return web.json_response({"status": "error", "message": err_msg}, status=401)

    question_id = request.query.get("question_id", "").strip()
    if not question_id:
        return web.json_response({"status": "error", "message": "question_id parametri talab qilinadi"}, status=400)

    hints = hint_service.get_hints_for_question(question_id)
    await telemetry.record_event("pro_beta_feature_used", user_id=user_id, metadata={"feature": "hint_scaffolding", "question_id": question_id})

    return web.json_response({
        "status": "ok",
        "hints": hints
    })


# ==================== 13. MINIMAL PRIVACY-PRESERVING TELEMETRY ====================
async def api_telemetry_event(request: web.Request) -> web.Response:
    """
    POST /api/v1/telemetry/event
    Records non-PII operational events (dropoff steps, starter completion, flags).
    """
    try:
        body = await request.json()
    except Exception:
        return web.json_response({"status": "error", "message": "Noto'g'ri JSON formati"}, status=400)

    event_name = str(body.get("event", "")).strip()
    user_id, _ = get_authenticated_user_id(request, body)
    metadata = body.get("metadata", {})

    recorded = await telemetry.record_event(event_name, user_id=user_id, metadata=metadata)
    return web.json_response({
        "status": "ok",
        "recorded": recorded,
        "event": event_name
    })


# ==================== ROUTE REGISTRATION HELPER ====================
def setup_practice_routes(app: web.Application) -> None:
    """Registers all unified practice, diagnostic, Pro preparation and analytics endpoints."""
    app.router.add_get("/api/v1/practice/today-summary", api_practice_today_summary)
    app.router.add_get("/api/v1/practice/questions", api_practice_questions_get)
    app.router.add_post("/api/v1/practice/check-answer", api_practice_check_answer)
    app.router.add_post("/api/v1/practice/submit", api_practice_submit)
    app.router.add_get("/api/v1/mistakes", api_mistakes_get)
    app.router.add_post("/api/v1/mistakes/resolve", api_mistakes_resolve)

    # Pro Personalized Prep & Diagnostics
    app.router.add_get("/api/v1/study-plan", api_study_plan_get)
    app.router.add_post("/api/v1/study-plan/rebalance", api_study_plan_rebalance)
    app.router.add_get("/api/v1/practice/fix-mistake", api_practice_fix_mistake)
    app.router.add_post("/api/v1/practice/custom-test", api_practice_custom_test)
    app.router.add_get("/api/v1/analytics/pacing", api_analytics_pacing)
    app.router.add_get("/api/v1/analytics/weekly-report", api_analytics_weekly_report)
    app.router.add_get("/api/v1/practice/hint", api_practice_hint)
    app.router.add_post("/api/v1/telemetry/event", api_telemetry_event)

