"""
Local preview of the Mini App without Telegram. Prints a URL with signed test user data.

Usage: python scripts/dev_server.py [port] [user_id]
"""
import asyncio
import hashlib
import hmac
import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import quote, urlencode

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("BOT_TOKEN", "123456:LOCAL_PREVIEW")
os.environ.setdefault("SQLITE_PATH", str(Path(__file__).resolve().parent.parent / "data" / "app.db"))

from aiohttp import web  # noqa: E402

from bot import create_web_app  # noqa: E402
from config import BOT_TOKEN  # noqa: E402
from database import db  # noqa: E402

THEMES = {
    "light": {"bg_color": "#ffffff", "secondary_bg_color": "#f1f2f6", "section_bg_color": "#ffffff", "text_color": "#14181f",
              "hint_color": "#6d7685", "button_color": "#2f6fed", "button_text_color": "#ffffff"},
    "dark": {"bg_color": "#17212b", "secondary_bg_color": "#0e1621", "section_bg_color": "#17212b", "text_color": "#f5f5f5",
             "hint_color": "#708499", "button_color": "#5288c1", "button_text_color": "#ffffff"},
}


def signed_init_data(user_id: int) -> str:
    fields = {
        "auth_date": str(int(time.time())), "query_id": "LOCAL",
        "user": json.dumps({"id": user_id, "first_name": "Sinov", "language_code": "uz"}),
    }
    check = "\n".join(f"{key}={value}" for key, value in sorted(fields.items()))
    secret = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
    fields["hash"] = hmac.new(secret, check.encode(), hashlib.sha256).hexdigest()
    return urlencode(fields)


async def main(port: int, user_id: int) -> None:
    await db.connect()
    runner = web.AppRunner(create_web_app())
    await runner.setup()
    await web.TCPSite(runner, "127.0.0.1", port).start()
    for name, theme in THEMES.items():
        fragment = urlencode({
            "tgWebAppData": signed_init_data(user_id), "tgWebAppVersion": "8.0", "tgWebAppPlatform": "tdesktop",
            "tgWebAppThemeParams": json.dumps(theme),
        }, quote_via=quote)
        print(f"{name} http://127.0.0.1:{port}/webapp#{fragment}", flush=True)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main(int(sys.argv[1]) if len(sys.argv) > 1 else 8099, int(sys.argv[2]) if len(sys.argv) > 2 else 1000))
