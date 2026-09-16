"""
EduTest Pro - Master Runner (Aiogram 3.x + aiohttp Web & API Server)
Integrates:
- Bot Routers: start, diagnostic, practice, exam, admin, stats, referral
- Versioned WebApp API (/api/v1/auth/validate, /api/v1/user/progress, /api/v1/user/attention-event)
- Official Telegram WebApp initData HMAC-SHA256 authentication
- Graceful shutdown and resilient error recovery
"""

import asyncio
from datetime import datetime
import json
import logging
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiohttp import web

from config import (
    BACKUP_CHANNEL,
    BOT_NAME,
    BOT_TOKEN,
    BRAND_NAME,
    CENTER_NAME,
    PORT,
)
from database import db
from handlers.admin import router as admin_router
from handlers.diagnostic import router as diag_router
from handlers.exam import router as exam_router
from handlers.feedback import router as feedback_router
from handlers.mistakes import router as mistakes_router
from handlers.practice import router as practice_router
from handlers.referral import router as referral_router
from handlers.start import router as start_router
from handlers.stats import router as stats_router
from services.auth_service import validate_telegram_init_data
from services.backup_service import backup_scheduler_loop

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("EduTestPro")

WEBAPP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "webapp")


# --- 1. HTTP & API HANDLERS (aiohttp) ---
async def health_handler(request: web.Request) -> web.Response:
    """Health check endpoint for Render.com, cron monitors, and uptime checks."""
    return web.json_response({
        "status": "ok",
        "bot": "active",
        "service": BOT_NAME,
        "brand": BRAND_NAME,
        "center": CENTER_NAME
    })


async def webapp_handler(request: web.Request) -> web.Response:
    """Serves the interactive EduTest Pro Study Tracker WebApp."""
    index_file = os.path.join(WEBAPP_DIR, "index.html")
    if os.path.exists(index_file):
        return web.FileResponse(index_file)
    return web.Response(text="WebApp index.html not found", status=404)


async def api_auth_validate(request: web.Request) -> web.Response:
    """
    POST /api/v1/auth/validate
    Validates Telegram WebApp initData HMAC-SHA256 signature.
    """
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"status": "error", "message": "Noto'g'ri JSON payload"}, status=400)

    init_data = data.get("initData", "")
    is_valid, user_data, msg = validate_telegram_init_data(init_data)

    if not is_valid:
        return web.json_response({
            "status": "error",
            "authenticated": False,
            "message": msg
        }, status=401)

    return web.json_response({
        "status": "ok",
        "authenticated": True,
        "user": user_data,
        "message": msg
    })


async def api_user_progress_get(request: web.Request) -> web.Response:
    """
    GET /api/v1/user/progress
    Retrieves synchronized student tasks, errors, and settings.
    Requires 'X-Telegram-Init-Data' header or query parameter 'initData'.
    """
    init_data = request.headers.get("X-Telegram-Init-Data") or request.query.get("initData", "")
    is_valid, user_data, msg = validate_telegram_init_data(init_data)

    if not is_valid or not user_data:
        return web.json_response({"status": "error", "message": "Ruxsatsiz kirish: initData tasdiqlanmadi"}, status=401)

    user_id = user_data.get("id")
    if not user_id:
        return web.json_response({"status": "error", "message": "User ID topilmadi"}, status=400)

    saved_data = db.get_webapp_user_data(user_id) or {"tasks": [], "errors": [], "settings": {}}
    return web.json_response({
        "status": "ok",
        "user_id": user_id,
        "data": saved_data
    })


ALLOWED_ATTENTION_EVENTS = {"tab_hidden", "tab_visible", "window_blur", "window_focus"}


def validate_progress_schema(payload: dict) -> tuple[bool, str]:
    """Validates user progress payload against strict schema rules."""
    if not isinstance(payload, dict):
        return False, "Payload lug'at (object) ko'rinishida bo'lishi shart"

    # Tasks validation
    tasks = payload.get("tasks")
    if tasks is not None:
        if not isinstance(tasks, list):
            return False, "tasks massiv bo'lishi shart"
        if len(tasks) > 100:
            return False, "tasks soni 100 tadan oshmasligi kerak"
        for t in tasks:
            if not isinstance(t, dict):
                return False, "Har bir task obyekt bo'lishi shart"
            subj = t.get("subject", "")
            if not isinstance(subj, str) or len(subj) > 100:
                return False, "Task subject matn bo'lishi va 100 belgidan oshmasligi kerak"
            dur = t.get("duration")
            if dur is not None:
                if not isinstance(dur, (int, float)) or not (1 <= dur <= 600):
                    return False, "Task duration 1 dan 600 daqiqagacha bo'lishi kerak"
            d_str = t.get("date")
            if d_str is not None:
                if not isinstance(d_str, str) or len(d_str) != 10:
                    return False, "Task date formati YYYY-MM-DD bo'lishi kerak"
                try:
                    datetime.strptime(d_str, "%Y-%m-%d")
                except ValueError:
                    return False, "Task date formati YYYY-MM-DD bo'lishi kerak"

    # Errors validation
    errors = payload.get("errors")
    if errors is not None:
        if not isinstance(errors, list):
            return False, "errors massiv bo'lishi shart"
        if len(errors) > 100:
            return False, "errors soni 100 tadan oshmasligi kerak"
        for err in errors:
            if not isinstance(err, dict):
                return False, "Har bir error obyekt bo'lishi shart"
            sol = err.get("solution")
            if sol is not None and isinstance(sol, str) and sol.strip():
                if not (sol.startswith("https://") or sol.startswith("http://")):
                    return False, "Xatolik yechimi havolasi http(s):// bilan boshlanishi kerak"

    # Settings validation
    settings = payload.get("settings")
    if settings is not None:
        if not isinstance(settings, dict):
            return False, "settings lug'at bo'lishi shart"
        if len(settings) > 20:
            return False, "settings kalitlari soni 20 tadan oshmasligi kerak"

    return True, "Valid"


async def api_user_progress_post(request: web.Request) -> web.Response:
    """
    POST /api/v1/user/progress
    Persists student tasks, error log entries, and settings to backend.
    Enforces strict schema validation. Allows empty arrays to clear data.
    """
    init_data = request.headers.get("X-Telegram-Init-Data")
    try:
        payload = await request.json()
    except Exception:
        return web.json_response({"status": "error", "message": "Noto'g'ri JSON formati"}, status=400)

    if not init_data and isinstance(payload, dict):
        init_data = payload.get("initData", "")

    is_valid, user_data, msg = validate_telegram_init_data(init_data or "")
    if not is_valid or not user_data:
        return web.json_response({"status": "error", "message": "Ruxsatsiz kirish: initData tasdiqlanmadi"}, status=401)

    user_id = user_data.get("id")
    if not user_id or not isinstance(user_id, int) or user_id <= 0:
        return web.json_response({"status": "error", "message": "Yaroqsiz user ID"}, status=400)

    # Validate size
    payload_str = json.dumps(payload)
    if len(payload_str.encode("utf-8")) > 102400:  # 100 KB limit
        return web.json_response({"status": "error", "message": "Payload hajmi 100 KB dan oshmasligi kerak"}, status=413)

    is_valid_schema, schema_err = validate_progress_schema(payload)
    if not is_valid_schema:
        return web.json_response({"status": "error", "message": schema_err}, status=400)

    await db.save_webapp_user_data(user_id, payload)
    return web.json_response({
        "status": "ok",
        "message": "Ma'lumotlar server bilan muvaffaqiyatli sinxronlandi."
    })


async def api_attention_event_post(request: web.Request) -> web.Response:
    """
    POST /api/v1/user/attention-event
    Honest anti-cheat boundary: logs focus/visibility changes as an attention signal,
    without drawing definitive cheating conclusions. Requires authentication and valid schema.
    """
    init_data = request.headers.get("X-Telegram-Init-Data")
    try:
        body = await request.json()
    except Exception:
        return web.json_response({"status": "error", "message": "Noto'g'ri JSON formati"}, status=400)

    if not init_data and isinstance(body, dict):
        init_data = body.get("initData", "")

    is_valid, user_data, msg = validate_telegram_init_data(init_data or "")
    if not is_valid or not user_data:
        return web.json_response({"status": "error", "message": "Ruxsatsiz kirish: initData tasdiqlanmadi"}, status=401)

    user_id = user_data.get("id")
    if not user_id or not isinstance(user_id, int) or user_id <= 0:
        return web.json_response({"status": "error", "message": "Yaroqsiz user ID"}, status=400)

    if not isinstance(body, dict):
        return web.json_response({"status": "error", "message": "Body lug'at bo'lishi shart"}, status=400)

    event_type = body.get("event")
    if event_type not in ALLOWED_ATTENTION_EVENTS:
        return web.json_response({
            "status": "error",
            "message": f"Yaroqsiz event turi: {event_type}. Ruxsat etilganlar: {list(ALLOWED_ATTENTION_EVENTS)}"
        }, status=400)

    await db.save_attention_event(user_id, body)
    logger.info(f"Attention event logged to database: user_id={user_id}, event={event_type}")

    return web.json_response({
        "status": "ok",
        "recorded": True,
        "event": event_type,
        "note": "Attention signal DB ga qayd etildi (dalil emas, xizmat signali)"
    })


async def api_test_questions_get(request: web.Request) -> web.Response:
    """
    GET /api/v1/test/questions?mode=daily_10m|pilot_mock|diagnostic
    Returns structured questions for mobile Mini App interactive testing.
    """
    mode = request.query.get("mode", "daily_10m")
    if mode == "diagnostic":
        from handlers.diagnostic import QUESTIONS
        return web.json_response({
            "status": "ok",
            "mode": mode,
            "title": "Digital SAT Diagnostika (Math)",
            "duration_seconds": 15 * 60,
            "questions": QUESTIONS
        })

    from services.exam_service import EXAM_TEMPLATES, prepare_shuffled_questions
    tpl = EXAM_TEMPLATES.get(mode, EXAM_TEMPLATES["daily_10m"])
    seed = int(datetime.now().timestamp() * 1000)
    questions = prepare_shuffled_questions(mode, seed)
    return web.json_response({
        "status": "ok",
        "mode": mode,
        "title": tpl.get("title"),
        "description": tpl.get("description"),
        "duration_seconds": tpl.get("duration_seconds"),
        "questions": questions
    })


def setup_web_app() -> web.Application:
    """Constructs the unified aiohttp web application with API routes and 256KB request limit."""
    app = web.Application(client_max_size=256 * 1024)
    # CORS options
    app.router.add_get("/", health_handler)
    app.router.add_get("/health", health_handler)
    app.router.add_get("/webapp", webapp_handler)

    # Versioned API
    app.router.add_post("/api/v1/auth/validate", api_auth_validate)
    app.router.add_get("/api/v1/user/progress", api_user_progress_get)
    app.router.add_post("/api/v1/user/progress", api_user_progress_post)
    app.router.add_post("/api/v1/user/attention-event", api_attention_event_post)
    app.router.add_get("/api/v1/test/questions", api_test_questions_get)

    if os.path.exists(WEBAPP_DIR):
        app.router.add_static("/static/", path=WEBAPP_DIR, name="static")

    return app


# --- 2. MAIN ORCHESTRATOR ---
async def main():
    if not BOT_TOKEN or "YOUR_TOKEN" in BOT_TOKEN:
        print("\n" + "!" * 60)
        print("DIQQAT: BOT_TOKEN aniqlanmadi!")
        print("Iltimos, .env fayliga BOT_TOKEN=... ni kiriting.")
        print("!" * 60 + "\n")
        return

    # Connect Database
    await db.connect()

    # Initialize Bot
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Register Routers
    dp.include_router(start_router)
    dp.include_router(mistakes_router)
    dp.include_router(feedback_router)
    dp.include_router(exam_router)
    dp.include_router(admin_router)
    dp.include_router(diag_router)
    dp.include_router(practice_router)
    dp.include_router(referral_router)
    dp.include_router(stats_router)

    # Set commands menu
    commands = [
        BotCommand(command="start", description="Bosh menyu va 3 asosiy yo'l"),
        BotCommand(command="mock", description="Mock Imtihon Markazi"),
        BotCommand(command="practice", description="Cheksiz SAT Mashq Bazasi"),
        BotCommand(command="mistakes", description="Xatolarim daftari"),
        BotCommand(command="feedback", description="Taklif va fikr bildirish"),
        BotCommand(command="admin", description="Administrator Paneli"),
        BotCommand(command="webapp", description="O'quvchi Kabineti & Test Runner"),
        BotCommand(command="diagnostic", description="Diagnostika Testi (Math)"),
        BotCommand(command="desmos", description="Desmos Strategiyalari"),
        BotCommand(command="stats", description="Mening Natijalarim"),
        BotCommand(command="referral", description="Do'stlarni Taklif Qilish"),
        BotCommand(command="backup", description="Tizim Zaxirasi (Admin)")
    ]
    try:
        await bot.set_my_commands(commands)
    except Exception as e:
        logger.warning(f"Could not set bot commands: {e}")

    # Launch Automatic Backup Scheduler Loop if BACKUP_CHANNEL is set
    backup_task = None
    if BACKUP_CHANNEL:
        backup_task = asyncio.create_task(backup_scheduler_loop(bot, interval_seconds=1800))
    else:
        logger.info("ℹ️ BACKUP_CHANNEL sozlanmagan. Avtomatik kanal zaxirasi o'chirilgan.")

    # Synchronize Bot Profile Metadata
    try:
        await bot.set_my_name(name=BOT_NAME)
        await bot.set_my_short_description(
            short_description=f"🎯 {CENTER_NAME} uchun Digital SAT Diagnostika, Mock Imtihon va Desmos strategiyalari."
        )
        await bot.set_my_description(
            description=(
                f"Assalomu alaykum! Bu {BRAND_NAME} — {CENTER_NAME} uchun mo'ljallangan "
                f"zamonaviy diagnostika, mock imtihon va o'quv nazorati tizimi.\n\n"
                f"IMKONIYATLAR:\n"
                f"🔬 Diagnostika: 7 ta nozik savol orqali bilim darajasi va zaif mavzular tahlili.\n"
                f"📝 Mock Imtihon: Server vaqt nazorati ostida deterministik mock testlari.\n"
                f"📚 SAT Mashq Bazasi: Math, Reading va Writing bo'yicha cheksiz mashqlar.\n"
                f"⚡ Desmos Strategiyalari: Digital SAT Math savollarini tezkor yechish usullari.\n"
                f"📱 O'quvchi Kabineti: 60 kunlik intizomli dars jadvali WebApp'i.\n\n"
                f"👇 'Start' tugmasini bosing va tizimdan foydalanishni boshlang!"
            )
        )
        logger.info("✅ Bot name, bio and description successfully synchronized!")
    except Exception as e:
        logger.warning(f"Could not auto-sync profile details: {e}")

    try:
        me = await bot.get_me()
        print("\n" + "=" * 50)
        print(f"🚀 {BRAND_NAME} TIZIMI ISHGA TUSHDI!")
        print(f"🤖 Bot: @{me.username} ({me.full_name})")
        print(f"🏛️ Markaz: {CENTER_NAME}")
        print("=" * 50 + "\n")
    except Exception as e:
        logger.warning(f"Could not fetch bot identity: {e}")

    # Start Web & API Server
    app = setup_web_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"🌐 Web Server & /api/v1/ listening on port {PORT}")

    # Run bot polling with clean shutdown
    try:
        await dp.start_polling(bot)
    finally:
        logger.info("Initiating graceful shutdown...")
        if backup_task and not backup_task.done():
            backup_task.cancel()
        await runner.cleanup()
        await bot.session.close()
        await db.close()
        logger.info("Shutdown completed cleanly.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot execution terminated.")
