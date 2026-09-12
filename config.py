"""
SAT AI Bot - Configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

# Admin IDs for reports (optional)
ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()]

# WebApp URL (optional public URL, can be local or ngrok or GitHub Pages)
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://bird-for-accessory-sender.trycloudflare.com")
