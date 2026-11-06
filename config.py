"""
IELTS & SAT Daily - Centralized Configuration
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


def _int_env(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, "").strip() or default)
    except ValueError:
        return default


def _id_set(*names: str) -> frozenset[int]:
    ids = set()
    for name in names:
        for part in os.getenv(name, "").replace(";", ",").split(","):
            part = part.strip()
            if part.lstrip("-").isdigit() and int(part) != 0:
                ids.add(int(part))
    return frozenset(ids)


BOT_TOKEN: str = os.getenv("BOT_TOKEN", "").strip()
BOT_USERNAME: str = os.getenv("BOT_USERNAME", "ieltssat_dailybot").strip().lstrip("@")
CHANNEL_ID: str = os.getenv("CHANNEL_ID", "@ieltssat_daily").strip()
CHANNEL_URL: str = os.getenv("CHANNEL_URL", "https://t.me/ieltssat_daily").strip()
TIMEZONE: str = os.getenv("TIMEZONE", "Asia/Tashkent").strip()
WEBAPP_URL: str = os.getenv("WEBAPP_URL", "https://sat-master-bot.onrender.com/webapp").strip()
PORT: int = _int_env("PORT", 8080)

# Both spellings are accepted: ADMIN_ID came first, ADMIN_IDS allows several people.
ADMIN_IDS: frozenset[int] = _id_set("ADMIN_IDS", "ADMIN_ID")

# Postgres URL. Without it the bot uses a local SQLite file, which Render wipes on every deploy.
DATABASE_URL: str = os.getenv("DATABASE_URL", "").strip()
SQLITE_PATH: str = os.getenv("SQLITE_PATH", str(BASE_DIR / "data" / "app.db")).strip()

GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "").strip()
# Tried in order. Free-tier models are often busy, so a second and third choice matter.
GEMINI_MODELS: list[str] = [
    name.strip()
    for name in os.getenv("GEMINI_MODELS", "gemini-3.5-flash,gemini-3-flash-preview,gemini-3.5-flash-lite").split(",")
    if name.strip()
]
AI_DAILY_LIMIT: int = _int_env("AI_DAILY_LIMIT", 3)
AI_GLOBAL_DAILY_LIMIT: int = _int_env("AI_GLOBAL_DAILY_LIMIT", 200)

DESMOS_API_KEY: str = os.getenv("DESMOS_API_KEY", "").strip()
SENTRY_DSN: str = os.getenv("SENTRY_DSN", "").strip()
