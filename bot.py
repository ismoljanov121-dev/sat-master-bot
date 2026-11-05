import os
import asyncio
import logging
from pathlib import Path
from aiohttp import web, ClientSession, ClientTimeout
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import TelegramNetworkError, TelegramServerError

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

@web.middleware
async def response_headers(request, handler):
    response = await handler(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    if request.path in ("/webapp", "/miniapp"):
        response.headers["Cache-Control"] = "no-cache"
    return response

async def setup_web_app():
    app = web.Application(middlewares=[response_headers])
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)
    app.router.add_get("/webapp", serve_webapp)
    app.router.add_get("/miniapp", serve_webapp)
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

async def self_ping_loop():
    """Keeps Render Free Tier 100% awake 24/7 by pinging public URL every 8 minutes."""
    render_url = os.getenv("RENDER_EXTERNAL_URL", "https://sat-master-bot.onrender.com")
    health_url = f"{render_url.rstrip('/')}/health"
    await asyncio.sleep(45)  # Wait 45 seconds after initial startup
    while True:
        try:
            timeout = ClientTimeout(total=20)
            async with ClientSession(timeout=timeout) as session:
                async with session.get(health_url) as resp:
                    logger.info(f"Keep-alive self-ping: status {resp.status} for {health_url}")
        except Exception as e:
            logger.warning(f"Keep-alive self-ping warning: {e}")
        await asyncio.sleep(8 * 60)  # Ping every 8 minutes (Render sleeps after 15 minutes)

async def run_polling(dp, bot):
    """Aiogram ishlash paytida o'zi qayta ulanadi, boshlanishdagi getMe xatosini esa shu yerda ushlaymiz."""
    delay = 5
    while True:
        try:
            await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), close_bot_session=False)
            return
        except (TelegramNetworkError, TelegramServerError, asyncio.TimeoutError) as e:
            logger.warning(f"Telegram unavailable at startup: {e}. Retrying in {delay}s")
            await asyncio.sleep(delay)
            delay = min(delay * 2, 60)

async def main():
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        logger.error("BOT_TOKEN is missing! Please configure BOT_TOKEN.")
        return

    web_runner = await start_web_server()
    ping_task = asyncio.create_task(self_ping_loop())

    bot = DefaultBotProperties(parse_mode=ParseMode.HTML)
    bot = Bot(token=BOT_TOKEN, default=bot)
    dp = Dispatcher()
    dp.include_router(router)

    scheduler = setup_scheduler(bot)
    scheduler.start()
    logger.info("Scheduler started successfully for Asia/Tashkent daily posts.")

    try:
        logger.info("Bot is polling for updates...")
        await run_polling(dp, bot)
    finally:
        ping_task.cancel()
        scheduler.shutdown()
        await web_runner.cleanup()
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
