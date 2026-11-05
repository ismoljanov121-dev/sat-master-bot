import os
import asyncio
import logging
from pathlib import Path
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from handlers import router
from scheduler import setup_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ielts_sat_bot")

WEBAPP_DIR = Path(__file__).parent / "webapp"

async def health_check(request):
    """Keep-alive endpoint for cron-job.org / Render."""
    return web.Response(text="IELTS & SAT Daily Bot is running healthy! 🚀", status=200)

async def serve_webapp(request):
    """Serves the clean IELTS & SAT Score Predictor Telegram Mini App."""
    index_file = WEBAPP_DIR / "index.html"
    if index_file.exists():
        return web.FileResponse(index_file)
    return web.Response(text="Mini App file not found", status=404)

async def setup_web_app():
    app = web.Application()
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)
    app.router.add_get("/webapp", serve_webapp)
    app.router.add_get("/miniapp", serve_webapp)
    if WEBAPP_DIR.exists():
        app.router.add_static("/static", WEBAPP_DIR)
    return app

async def start_web_server():
    port = int(os.getenv("PORT", 8080))
    app = await setup_web_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"Health-check & Mini App web server listening on 0.0.0.0:{port}")
    return runner

async def main():
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        logger.error("BOT_TOKEN is missing! Please configure BOT_TOKEN.")
        return

    web_runner = await start_web_server()

    bot = DefaultBotProperties(parse_mode=ParseMode.HTML)
    bot = Bot(token=BOT_TOKEN, default=bot)
    dp = Dispatcher()
    dp.include_router(router)

    scheduler = setup_scheduler(bot)
    scheduler.start()
    logger.info("Scheduler started successfully for Asia/Tashkent daily posts.")

    try:
        logger.info("Bot is polling for updates...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        scheduler.shutdown()
        await web_runner.cleanup()
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
