import asyncio
import logging
from datetime import datetime
from typing import Any, Optional

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from config import TIMEZONE, WEBAPP_URL
from database import TZ, db, shift_day, today
from services import plan, review, users
from services.channel import (  # noqa: F401  the channel helpers stay importable from here
    FOOTER, POLL_EXPLANATION_LIMIT, POLL_OPTION_LIMIT, POLL_QUESTION_LIMIT, SLOTS, channel_quiz_candidates,
    next_item, plain_text, post_slot, practice_button, short_explanation,
)
from services.content import content  # noqa: F401

logger = logging.getLogger(__name__)

SEND_DELAY_SECONDS = 0.05
INACTIVE_AFTER_DAYS = 14


async def post_channel_slot(bot: Bot, slot: int):
    """One of the four daily channel slots, ten posts a day in all (see SLOTS in services/channel.py)."""
    await post_slot(bot, slot)


def open_app_button(label: str = "📱 Mini App'ni ochish") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=label, web_app=WebAppInfo(url=WEBAPP_URL))]])


async def _deliver(bot: Bot, user_id: int, text: str) -> bool:
    try:
        await bot.send_message(user_id, text, parse_mode="HTML", reply_markup=open_app_button())
        return True
    except TelegramForbiddenError:
        await db.execute("UPDATE users SET blocked = 1 WHERE id = ?", user_id)
    except TelegramRetryAfter as e:
        await asyncio.sleep(e.retry_after)
    except Exception as e:
        logger.warning("Could not message user: %s", type(e).__name__)
    return False


def reminder_text(user: dict[str, Any], due: int, tasks: int) -> str:
    name = user["first_name"] or "Do'stim"
    streak = users.current_streak(user)
    lines = [f"⏰ <b>{name}, bugungi mashq vaqti keldi.</b>\n"]
    if streak:
        lines.append(f"🔥 {streak} kunlik seriyangiz bor, uni uzmang.")
    if due:
        lines.append(f"🔁 Takrorlash uchun {due} ta savol kutmoqda.")
    if tasks:
        lines.append(f"📋 Bugungi rejada {tasks} ta vazifa bor.")
    return "\n".join(lines)


async def send_reminders(bot: Bot, hour: Optional[int] = None):
    """Runs hourly and messages people whose chosen hour it is and who have not studied yet today."""
    hour = datetime.now(TZ).hour if hour is None else hour
    day = today()
    active_since = shift_day(day, -INACTIVE_AFTER_DAYS)
    rows = await db.fetch(
        """SELECT * FROM users
           WHERE reminders_on = 1 AND blocked = 0 AND bot_started = 1 AND onboarded = 1 AND reminder_hour = ?
             AND (last_active_day IS NULL OR last_active_day < ?)
             AND (last_active_day IS NULL OR last_active_day >= ?)
             AND (last_reminded_day IS NULL OR last_reminded_day < ?)""",
        hour, day, active_since, day,
    )
    sent = 0
    for user in rows:
        due = await review.due_count(user["id"])
        today_plan = await plan.today_plan(user)
        await db.execute("UPDATE users SET last_reminded_day = ? WHERE id = ?", day, user["id"])
        sent += await _deliver(bot, user["id"], reminder_text(user, due, today_plan["total"] - today_plan["done"]))
        await asyncio.sleep(SEND_DELAY_SECONDS)
    if rows:
        logger.info("Reminders sent: %s of %s", sent, len(rows))


async def send_weekly_reports(bot: Bot):
    active_since = shift_day(today(), -INACTIVE_AFTER_DAYS)
    rows = await db.fetch(
        "SELECT * FROM users WHERE blocked = 0 AND bot_started = 1 AND last_active_day >= ?", active_since
    )
    for user in rows:
        report = await plan.weekly_report(user)
        await _deliver(bot, user["id"], plan.weekly_report_text(report))
        await asyncio.sleep(SEND_DELAY_SECONDS)


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    """Configures scheduled posts and messages in Asia/Tashkent timezone."""
    scheduler = AsyncIOScheduler(
        timezone=TIMEZONE,
        job_defaults={"misfire_grace_time": 3600, "coalesce": True, "max_instances": 1},
    )

    # Channel: four slots a day, ten posts in all (08:00, 13:00, 18:00 and 21:00 Tashkent).
    for slot, (hour, minute, _kinds) in enumerate(SLOTS):
        scheduler.add_job(post_channel_slot, CronTrigger(hour=hour, minute=minute, timezone=TIMEZONE),
                          args=[bot, slot], id=f"channel_slot_{slot}")

    # Every hour: study reminders. Sunday 18:00: weekly reports.
    scheduler.add_job(send_reminders, CronTrigger(minute=5, timezone=TIMEZONE), args=[bot])
    scheduler.add_job(send_weekly_reports, CronTrigger(day_of_week="sun", hour=18, minute=0, timezone=TIMEZONE), args=[bot])

    return scheduler
