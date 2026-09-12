"""
SAT Master AI - Automated 30-Minute Cloud Backup Service
Dumps database state (MongoDB + Local Fallback) and sends JSON archive to Telegram Backup Channel.
"""

import asyncio
import logging
import json
from datetime import datetime, timezone, timedelta
from typing import Optional
from aiogram import Bot
from aiogram.types import BufferedInputFile
from config import BACKUP_CHANNEL
from database import db

logger = logging.getLogger("BackupService")

# Tashkent Timezone (UTC+5)
TASHKENT_TZ = timezone(timedelta(hours=5))

async def export_full_database_state() -> dict:
    """Exports complete snapshot of users and quiz results."""
    export_data = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "timestamp_tashkent": datetime.now(TASHKENT_TZ).strftime("%Y-%m-%d %H:%M:%S"),
        "total_users": 0,
        "total_quizzes": 0,
        "users": {},
        "quizzes": []
    }

    # Fetch from MongoDB if active
    if db.is_mongo_active and db.db:
        try:
            users_cursor = db.db.users.find({}, {"_id": 0})
            users_list = await users_cursor.to_list(length=10000)
            for u in users_list:
                export_data["users"][str(u.get("user_id"))] = u

            quizzes_cursor = db.db.quiz_results.find({}, {"_id": 0})
            export_data["quizzes"] = await quizzes_cursor.to_list(length=10000)

            export_data["total_users"] = len(export_data["users"])
            export_data["total_quizzes"] = len(export_data["quizzes"])
            export_data["source"] = "MongoDB Atlas (Primary Cloud)"
            return export_data
        except Exception as e:
            logger.error(f"Error reading from MongoDB during backup: {e}")

    # Fallback to local cache
    local_data = db.local_cache
    export_data["users"] = local_data.get("users", {})
    export_data["quizzes"] = local_data.get("quizzes", [])
    export_data["total_users"] = len(export_data["users"])
    export_data["total_quizzes"] = len(export_data["quizzes"])
    export_data["source"] = "Local Cache (Failover)"
    return export_data

async def perform_backup(bot: Bot, manual: bool = False) -> bool:
    """Executes single backup operation and uploads JSON dump to backup channel."""
    try:
        data = await export_full_database_state()
        now_str = datetime.now(TASHKENT_TZ).strftime("%Y%m%d_%H%M%S")
        filename = f"sat_master_backup_{now_str}.json"

        json_bytes = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
        doc_file = BufferedInputFile(json_bytes, filename=filename)

        prefix = "⚡ [QO'LDA CHAQIRILGAN ZAXIRA]" if manual else "⏰ [30 MINUTLIK AVTOMATIK ZAXIRA]"
        caption = (
            f"💾 <b>SAT MASTER AI — CLOUD BACKUP</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏷️ <b>Turi:</b> {prefix}\n"
            f"📅 <b>Vaqt:</b> {data['timestamp_tashkent']} (Toshkent)\n"
            f"👥 <b>Jami o'quvchilar:</b> {data['total_users']}\n"
            f"📊 <b>Topshirilgan testlar:</b> {data['total_quizzes']}\n"
            f"🗄️ <b>Manba:</b> {data['source']}\n"
            f"✅ <i>Holat: 100% Sinxronlangan va Xavfsiz saqlandi</i>"
        )

        await bot.send_document(
            chat_id=BACKUP_CHANNEL,
            document=doc_file,
            caption=caption,
            parse_mode="HTML"
        )
        logger.info(f"✅ Backup successfully sent to {BACKUP_CHANNEL} ({filename})")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to perform backup to {BACKUP_CHANNEL}: {e}")
        return False

async def backup_scheduler_loop(bot: Bot, interval_seconds: int = 1800):
    """Periodic background loop that runs every 30 minutes (1800 seconds)."""
    logger.info(f"🚀 Backup Scheduler started! Target: {BACKUP_CHANNEL}, Interval: {interval_seconds}s")
    
    # Run initial backup 10 seconds after bot boot
    await asyncio.sleep(10)
    await perform_backup(bot, manual=False)

    while True:
        try:
            await asyncio.sleep(interval_seconds)
            await perform_backup(bot, manual=False)
        except asyncio.CancelledError:
            logger.info("Backup scheduler stopped.")
            break
        except Exception as e:
            logger.error(f"Unexpected error in backup scheduler loop: {e}")
            await asyncio.sleep(60)  # wait 1 min before retrying if error occurs
