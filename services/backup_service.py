"""
EduTest Pro - Automated Cloud Backup Service
Dumps database state (MongoDB + Atomic Local Cache) and sends JSON archive to Telegram Backup Channel.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta, timezone

from aiogram import Bot
from aiogram.types import BufferedInputFile

from config import BACKUP_CHANNEL, BRAND_NAME, CENTER_NAME
from database import db

logger = logging.getLogger("BackupService")

# Tashkent Timezone (UTC+5)
TASHKENT_TZ = timezone(timedelta(hours=5))

async def export_full_database_state() -> dict:
    """Exports complete snapshot of users, exams, quizzes, webapp data, and attention events."""
    export_data = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "timestamp_tashkent": datetime.now(TASHKENT_TZ).strftime("%Y-%m-%d %H:%M:%S"),
        "total_users": 0,
        "total_quizzes": 0,
        "total_exams": 0,
        "users": {},
        "quizzes": [],
        "exam_sessions": {},
        "exam_attempts": {},
        "webapp_data": {},
        "attention_events": []
    }

    # Fetch from MongoDB if active
    if db.is_mongo_active and (db.db is not None):
        try:
            users_cursor = db.db.users.find({}, {"_id": 0})
            users_list = await users_cursor.to_list(length=10000)
            for u in users_list:
                export_data["users"][str(u.get("user_id"))] = u

            quizzes_cursor = db.db.quiz_results.find({}, {"_id": 0})
            export_data["quizzes"] = await quizzes_cursor.to_list(length=10000)

            sessions_cursor = db.db.exam_sessions.find({}, {"_id": 0})
            sessions_list = await sessions_cursor.to_list(length=10000)
            for s in sessions_list:
                export_data["exam_sessions"][s.get("session_id")] = s

            attempts_cursor = db.db.exam_attempts.find({}, {"_id": 0})
            attempts_list = await attempts_cursor.to_list(length=10000)
            for a in attempts_list:
                export_data["exam_attempts"][a.get("attempt_id")] = a

            webapp_cursor = db.db.webapp_data.find({}, {"_id": 0})
            webapp_list = await webapp_cursor.to_list(length=10000)
            for w in webapp_list:
                export_data["webapp_data"][str(w.get("user_id"))] = w

            att_cursor = db.db.attention_events.find({}, {"_id": 0})
            export_data["attention_events"] = await att_cursor.to_list(length=10000)

            export_data["total_users"] = len(export_data["users"])
            export_data["total_quizzes"] = len(export_data["quizzes"])
            export_data["total_exams"] = len(export_data["exam_attempts"])
            export_data["source"] = "MongoDB Atlas (Primary Cloud)"
            return export_data
        except Exception as e:
            logger.error(f"Error reading from MongoDB during backup: {e}")

    # Fallback to local cache
    local_data = db.local_cache
    export_data["users"] = local_data.get("users", {})
    export_data["quizzes"] = local_data.get("quizzes", [])
    export_data["exam_sessions"] = local_data.get("exam_sessions", {})
    export_data["exam_attempts"] = local_data.get("exam_attempts", {})
    export_data["webapp_data"] = local_data.get("webapp_data", {})
    export_data["attention_events"] = local_data.get("attention_events", [])
    export_data["total_users"] = len(export_data["users"])
    export_data["total_quizzes"] = len(export_data["quizzes"])
    export_data["total_exams"] = len(export_data["exam_attempts"])
    export_data["source"] = "Atomic Local Storage (Failover & Durable)"
    return export_data


async def restore_database_from_snapshot(snapshot: dict) -> bool:
    """Restores database state from a verified snapshot dictionary."""
    try:
        keys = ["users", "quizzes", "exam_sessions", "exam_attempts", "webapp_data", "attention_events"]
        for k in keys:
            if k in snapshot:
                db.local_cache[k] = snapshot[k]
        await db._atomic_save_local()
        return True
    except Exception as e:
        logger.error(f"Error restoring database snapshot: {e}")
        return False

async def perform_backup(bot: Bot, manual: bool = False) -> bool:
    """Executes single backup operation and uploads JSON dump to backup channel."""
    if not BACKUP_CHANNEL:
        logger.info("Backup skipped: BACKUP_CHANNEL is not configured.")
        return False

    try:
        data = await export_full_database_state()
        now_str = datetime.now(TASHKENT_TZ).strftime("%Y%m%d_%H%M%S")
        filename = f"edutest_pro_backup_{now_str}.json"

        json_bytes = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
        doc_file = BufferedInputFile(json_bytes, filename=filename)

        prefix = "⚡ [QO'LDA CHAQIRILGAN ZAXIRA]" if manual else "⏰ [30 MINUTLIK AVTOMATIK ZAXIRA]"
        caption = (
            f"💾 <b>{BRAND_NAME} — TIZIM ZAXIRASI</b>\n"
            f"🏛️ <b>Markaz:</b> {CENTER_NAME}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏷️ <b>Turi:</b> {prefix}\n"
            f"📅 <b>Vaqt:</b> {data['timestamp_tashkent']} (Toshkent)\n"
            f"👥 <b>Jami o'quvchilar:</b> {data['total_users']}\n"
            f"📝 <b>Mock imtihonlar:</b> {data.get('total_exams', 0)}\n"
            f"🗄️ <b>Manba:</b> {data['source']}\n"
            f"✅ <i>Holat: Xavfsiz saqlandi</i>"
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
    if not BACKUP_CHANNEL:
        logger.info("Backup scheduler dormant: BACKUP_CHANNEL not configured.")
        return

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
            await asyncio.sleep(60)
