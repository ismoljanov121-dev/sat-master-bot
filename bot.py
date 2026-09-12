"""
SAT AI Bot - Master Runner (Aiogram 3.x + aiohttp Web Server for Render & cron-job.org)
"""

import asyncio
import logging
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand

from config import BOT_TOKEN, WEBAPP_URL, BACKUP_CHANNEL
from database import db
from handlers.start import router as start_router
from handlers.diagnostic import router as diag_router
from handlers.referral import router as referral_router
from handlers.stats import router as stats_router
from services.backup_service import backup_scheduler_loop

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("SATAIBot")

WEBAPP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "webapp")

# --- 1. HEALTH CHECK & WEBAPP WEB SERVER (Render.com Keep-Alive) ---
async def health_handler(request):
    """Health check endpoint for Render.com and cron-job.org ping."""
    return web.json_response({
        "status": "ok",
        "bot": "active",
        "service": "SAT Master AI Bot"
    })

async def webapp_handler(request):
    """Serves the 60-day SAT Tracker WebApp directly from the server."""
    index_file = os.path.join(WEBAPP_DIR, "index.html")
    if os.path.exists(index_file):
        return web.FileResponse(index_file)
    return web.Response(text="WebApp index.html not found", status=404)

def setup_web_app():
    app = web.Application()
    app.router.add_get("/", health_handler)
    app.router.add_get("/health", health_handler)
    app.router.add_get("/webapp", webapp_handler)
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

    # Register routers
    dp.include_router(start_router)
    dp.include_router(diag_router)
    dp.include_router(referral_router)
    dp.include_router(stats_router)

    # Set commands menu
    commands = [
        BotCommand(command="start", description="Bosh menyu va AI Rentgen"),
        BotCommand(command="webapp", description="Shaxsiy rejim & 60 kunlik tracker"),
        BotCommand(command="diagnostic", description="Rentgen Test (Math)"),
        BotCommand(command="desmos", description="Desmos Cheatcodes"),
        BotCommand(command="referral", description="Do'stlarni taklif qilish"),
        BotCommand(command="stats", description="Mening natijalarim"),
        BotCommand(command="backup", description="Bulutli zaxira (Admin)")
    ]
    await bot.set_my_commands(commands)

    # Launch 30-Minute Automatic Backup Scheduler Loop to @acacafagag
    asyncio.create_task(backup_scheduler_loop(bot, interval_seconds=1800))

    # Automatically set Bot Name, Bio (Short Description), and Welcome Description
    try:
        await bot.set_my_name(name="SAT Master AI")
        await bot.set_my_short_description(
            short_description="⚡ Digital SAT 1500+ AI Rentgen Diagnostika & Desmos Hiylalari. 5 daqiqada ballingizni oshiring!"
        )
        await bot.set_my_description(
            description=(
                "Digital SAT'dan 1500+ ololmayapsizmi? 🎯\n\n"
                "Muammo bilimsizlikda emas — qaysi mavzuda ball yo'qotayotganingizni va Desmos hiylalarini bilmasligingizda!\n\n"
                "BIZNING BOT NIMA BERADI?\n"
                "🔬 AI Rentgen: 5 daqiqada qaysi mavzu sening 80-100 ballingni o'g'irlayotganini ko'rsatib beradi.\n"
                "⚡ Desmos Hacks: Math savollarini formulalarsiz, 10 soniyada yechish yo'llari.\n"
                "📱 60 Kunlik SAT Tracker: SAT 1500 va IELTS 8.0 uchun dars jadvali WebApp'i.\n\n"
                "👇 'Start' tugmasini bosing va o'z bilimingizni bepul rentgen qiling!"
            )
        )
        logger.info("✅ Bot name, bio and description automatically synchronized!")
    except Exception as e:
        logger.warning(f"Could not auto-sync profile details: {e}")

    me = await bot.get_me()
    print("\n" + "=" * 50)
    print(f"🚀 SAT MASTER AI BOT ISHGA TUSHDI!")
    print(f"🤖 Bot: @{me.username} ({me.full_name})")
    print("=" * 50 + "\n")

    # Start Web Server on PORT for Render.com
    port = int(os.getenv("PORT", "8080"))
    app = setup_web_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🌐 Render Web Server & /health listening on port {port}")

    # Run bot polling
    try:
        await dp.start_polling(bot)
    finally:
        await runner.cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
