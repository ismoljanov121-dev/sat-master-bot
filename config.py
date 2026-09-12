"""
SAT AI Bot - Configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

# Admin IDs for reports (optional)
ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()]

# WebApp URL (Render hosted URL with fallback)
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://sat-master-bot.onrender.com/webapp").strip()

# 24/7 Backup Channel (Defaults to @acacafagag)
BACKUP_CHANNEL = os.getenv("BACKUP_CHANNEL", "@acacafagag").strip()
