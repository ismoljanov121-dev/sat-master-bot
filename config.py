"""
EduTest Pro - Centralized Configuration
Brand, Academy Context, Admin Authorization, and Server Settings
"""

import os

from dotenv import load_dotenv

load_dotenv()

# --- Core Brand & Center Information ---
BRAND_NAME: str = os.getenv("BRAND_NAME", "EduTest Pro").strip()
BOT_NAME: str = os.getenv("BOT_NAME", "EduTest Pro | Mock & Exam System").strip()
CENTER_NAME: str = os.getenv("CENTER_NAME", "Mustaqil Digital SAT Tayyorgarlik").strip()
MENTOR_NAME: str = os.getenv("MENTOR_NAME", "SAT Mentor").strip()

# --- Telegram Bot Token & Username ---
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "").strip()
BOT_USERNAME: str = os.getenv("BOT_USERNAME", "SAT_helper123_bot").strip().lstrip("@")

# --- Administrator IDs ---
def _parse_admin_ids(raw_value: str) -> list[int]:
    """Parses comma-separated or space-separated Telegram IDs safely."""
    ids: list[int] = []
    if not raw_value:
        return ids
    normalized = raw_value.replace(";", ",").replace(" ", ",")
    for token in normalized.split(","):
        cleaned = token.strip()
        if cleaned.isdigit():
            ids.append(int(cleaned))
    return ids

ADMIN_IDS: list[int] = _parse_admin_ids(os.getenv("ADMIN_IDS", ""))

def is_admin(user_id: int) -> bool:
    """Checks if the given Telegram user ID has administrator privileges."""
    return user_id in ADMIN_IDS

# --- WebApp & Server Settings ---
WEBAPP_URL: str = os.getenv("WEBAPP_URL", "http://127.0.0.1:8080/webapp").strip()
PORT: int = int(os.getenv("PORT", "8080"))

# --- 24/7 Backup Channel (Optional, disabled if empty) ---
BACKUP_CHANNEL: str = os.getenv("BACKUP_CHANNEL", "").strip()

# --- Database Storage Paths ---
BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
LOCAL_DB_FILE: str = os.path.join(BASE_DIR, "users_db.json")
MONGO_URI: str = os.getenv("MONGO_URI", "").strip()

# --- Tier, Limits & Beta Configuration ---
FREE_DAILY_QUESTIONS_LIMIT: int = int(os.getenv("FREE_DAILY_QUESTIONS_LIMIT", "50"))
FREE_WEEKLY_MOCKS_LIMIT: int = int(os.getenv("FREE_WEEKLY_MOCKS_LIMIT", "1"))
PRO_DAILY_FAIR_USE_LIMIT: int = int(os.getenv("PRO_DAILY_FAIR_USE_LIMIT", "150"))

# Launch & Beta Strategy:
# PAYMENTS_ENABLED is False: No live invoices sent, no surprise charges.
# PRO_BETA_MODE is True: Pro features are freely unlocked for all early adopters during beta.
PAYMENTS_ENABLED: bool = os.getenv("PAYMENTS_ENABLED", "False").lower() in ("true", "1")
PRO_BETA_MODE: bool = os.getenv("PRO_BETA_MODE", "True").lower() in ("true", "1")


