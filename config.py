"""
IELTS & SAT Daily - Centralized Configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "").strip()
BOT_USERNAME: str = os.getenv("BOT_USERNAME", "ieltssat_dailybot").strip().lstrip("@")
CHANNEL_ID: str = os.getenv("CHANNEL_ID", "@ieltssat_daily").strip()
CHANNEL_URL: str = os.getenv("CHANNEL_URL", "https://t.me/ieltssat_daily").strip()
ADMIN_ID: int = int(os.getenv("ADMIN_ID", "0"))
TIMEZONE: str = os.getenv("TIMEZONE", "Asia/Tashkent").strip()
WEBAPP_URL: str = os.getenv("WEBAPP_URL", "https://sat-master-bot.onrender.com/webapp").strip()
PORT: int = int(os.getenv("PORT", "8080"))
MONGO_URI: str = os.getenv("MONGO_URI", "").strip()
