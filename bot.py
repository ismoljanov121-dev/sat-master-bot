import asyncio
import hashlib
import logging
import os
import re
import time
import warnings
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramNetworkError, TelegramServerError
from aiohttp import ClientSession, ClientTimeout, web

import webapi
from config import ADMIN_IDS, BOT_TOKEN, PORT, SENTRY_DSN
from database import db
from handlers import router
from scheduler import setup_scheduler
from services import alerts, cards, review

# String keys are fine for this small app, and the warning would only fill the logs.
warnings.filterwarnings("ignore", category=web.NotAppKeyWarning)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ielts_sat_bot")

WEBAPP_DIR = Path(__file__).parent / "webapp"
INDEX_FILE = WEBAPP_DIR / "index.html"
ASSET_LINK = re.compile(r'/static/([\w./-]+)\?v=dev')
VERSION = os.getenv("RENDER_GIT_COMMIT", "dev")[:7]
STARTED_AT = time.time()


def asset_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:10]


def build_index() -> str:
    """Stamps each asset link with a content hash, so browsers can cache assets forever."""
    html = INDEX_FILE.read_text(encoding="utf-8")
    html = ASSET_LINK.sub(lambda m: f"/static/{m.group(1)}?v={asset_hash(WEBAPP_DIR / m.group(1))}", html)
    data_files = {path.name: asset_hash(path) for path in sorted((WEBAPP_DIR / "data").glob("*.json"))}
    return html.replace("__DATA_VERSIONS__", repr(data_files))


async def home(request):
    return web.Response(text="IELTS & SAT Daily Bot is running.")


async def health_check(request):
    """Keep-alive and uptime target. Answers 503 when the bot is not really working."""
    polling = request.app["runtime"].get("polling_task")
    polling_alive = polling is None or not polling.done()
    database_alive = await db.ping()
    healthy = polling_alive and database_alive
    return web.json_response(
        {
            "status": "ok" if healthy else "degraded", "version": VERSION, "storage": db.kind,
            "database": database_alive, "polling": polling_alive, "uptime_s": int(time.time() - STARTED_AT),
        },
        status=200 if healthy else 503,
    )


async def serve_webapp(request):
    return web.Response(text=request.app["index_html"], content_type="text/html")


async def serve_card(request):
    attempt_id, signature = request.match_info["attempt"], request.match_info["signature"]
    if not cards.verify(attempt_id, signature, request.app["bot_token"]):
        raise web.HTTPNotFound()
    image = await cards.render_card(attempt_id)
    if image is None:
        raise web.HTTPNotFound()
    return web.Response(body=image, content_type="image/png", headers={"Cache-Control": "public, max-age=86400"})


@web.middleware
async def response_headers(request, handler):
    response = await handler(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    if request.path in ("/webapp", "/miniapp"):
        response.headers["Cache-Control"] = "no-cache"
    elif request.path.startswith("/static/"):
        versioned = "v" in request.query
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable" if versioned else "no-cache"
    elif request.path.startswith("/audio/"):
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    return response


def create_web_app(bot: Bot | None = None, bot_token: str = BOT_TOKEN) -> web.Application:
    app = web.Application(middlewares=[response_headers, webapi.api_middleware], client_max_size=512 * 1024)
    app["bot"] = bot
    app["bot_token"] = bot_token
    app["runtime"] = {}
    app["index_html"] = build_index()
    app.add_routes(webapi.routes)
    app.router.add_get("/", home)
    app.router.add_get("/health", health_check)
    app.router.add_get("/webapp", serve_webapp)
    app.router.add_get("/miniapp", serve_webapp)
    app.router.add_get(r"/card/{attempt:[0-9a-f]{32}}-{signature:[0-9a-f]{20}}.png", serve_card)
    app.router.add_static("/static", WEBAPP_DIR)
    audio_dir = WEBAPP_DIR / "audio"
    if audio_dir.exists():
        app.router.add_static("/audio", audio_dir)
    return app


async def start_web_server(app: web.Application) -> web.AppRunner:
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logger.info(f"Web server listening on 0.0.0.0:{PORT}")
    return runner


async def self_ping_loop():
    """Keeps Render Free Tier awake by pinging the public URL every 8 minutes."""
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

    if SENTRY_DSN:
        import sentry_sdk

        sentry_sdk.init(dsn=SENTRY_DSN, release=VERSION)

    await db.connect()
    await review.forget_sealed_questions()
    if db.kind == "sqlite":
        logger.warning("DATABASE_URL is not set: progress is stored in a local file and is lost on each deploy.")

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)
    alerts.install(bot, ADMIN_IDS)

    app = create_web_app(bot)
    web_runner = await start_web_server(app)
    ping_task = asyncio.create_task(self_ping_loop())

    scheduler = setup_scheduler(bot)
    scheduler.start()
    logger.info("Scheduler started successfully for Asia/Tashkent daily posts.")

    polling_task = asyncio.create_task(run_polling(dp, bot))
    app["runtime"]["polling_task"] = polling_task
    try:
        logger.info("Bot is polling for updates...")
        await polling_task
    finally:
        ping_task.cancel()
        scheduler.shutdown()
        await web_runner.cleanup()
        await bot.session.close()
        await db.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
