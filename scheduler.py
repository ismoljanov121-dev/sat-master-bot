import asyncio
import logging
import random
import re
from datetime import datetime
from typing import Any, Optional

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from config import BOT_USERNAME, CHANNEL_ID, TIMEZONE, WEBAPP_URL
from content_bank import IELTS_TIPS, IELTS_VOCAB_PACKS
from database import TZ, db, now_ts, shift_day, today
from services import analytics, plan, review, users
from services.content import content

logger = logging.getLogger(__name__)

POLL_QUESTION_LIMIT = 300
POLL_OPTION_LIMIT = 100
POLL_EXPLANATION_LIMIT = 200
PASSAGE_LIMIT = 900
SEND_DELAY_SECONDS = 0.05
INACTIVE_AFTER_DAYS = 14
FOOTER = f"\n\n━━━━━━━━━━━━━━━━━━━━\n🤖 <b>Bepul IELTS va SAT mashq testlari:</b> @{BOT_USERNAME}"

_PLAIN_SYMBOLS = (
    (r"\cdot", "·"), (r"\le", "≤"), (r"\ge", "≥"), (r"\ne", "≠"), (r"\pm", "±"), (r"\pi", "π"), (r"\theta", "θ"),
    (r"\times", "×"), (r"\div", "÷"), (r"\left", ""), (r"\right", ""), ("^{2}", "²"), ("^{3}", "³"), (r"^{\circ}", "°"),
)


def plain_text(text: str) -> Optional[str]:
    """Turns LaTeX into text Telegram can show in a poll. Returns None if a formula is too complex for that."""
    def formula(match: re.Match) -> str:
        value = match.group(1)
        value = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"\1/\2", value)
        value = re.sub(r"\\sqrt\{([^{}]+)\}", r"√(\1)", value)
        for source, target in _PLAIN_SYMBOLS:
            value = value.replace(source, target)
        value = re.sub(r"_\{(\d+)\}", r"\1", value)
        return value.replace("{,}", ",").strip()

    result = re.sub(r"\\\((.+?)\\\)", formula, text, flags=re.S)
    return None if "\\" in result or "{" in result or "^" in result else result


def short_explanation(text: str) -> str:
    plain = plain_text(text) or ""
    if len(plain) <= POLL_EXPLANATION_LIMIT:
        return plain
    cut = plain[:POLL_EXPLANATION_LIMIT]
    sentence_end = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
    return cut[: sentence_end + 1] if sentence_end > 60 else cut[: POLL_EXPLANATION_LIMIT - 1] + "…"


def channel_quiz_candidates() -> list[dict[str, Any]]:
    """MCQ questions no mock uses, so the channel never gives away a mock."""
    candidates = []
    for question in content.bank.values():
        if not question.get("free") or question["type"] != "mcq" or "fig" in question:
            continue
        stem = plain_text(question["q"])
        options = [plain_text(option) for option in question["opts"]]
        passage = plain_text(question.get("pas", "")) if question.get("pas") else ""
        if stem is None or passage is None or None in options:
            continue
        if len(stem) > POLL_QUESTION_LIMIT - 20 or len(passage) > PASSAGE_LIMIT:
            continue
        if any(len(option) > POLL_OPTION_LIMIT for option in options):
            continue
        candidates.append({"id": question["id"], "sec": question["sec"], "dom": question["dom"], "stem": stem,
                           "passage": passage, "options": options, "correct": "ABCD".index(question["cor"])})
    return candidates


async def next_item(kind: str, item_ids: list[str]) -> str:
    """Picks an item not posted yet. When all have been used, the cycle starts over."""
    rows = await db.fetch("SELECT item_id FROM channel_log WHERE kind = ?", kind)
    used = {row["item_id"] for row in rows}
    fresh = [item_id for item_id in item_ids if item_id not in used]
    if not fresh:
        await db.execute("DELETE FROM channel_log WHERE kind = ?", kind)
        fresh = list(item_ids)
    choice = random.choice(fresh)
    await db.execute(
        "INSERT INTO channel_log (kind, item_id, posted_at) VALUES (?, ?, ?) ON CONFLICT (kind, item_id) DO NOTHING",
        kind, choice, now_ts(),
    )
    return choice


def practice_button(source: str, label: str = "📱 Ko'proq mashq qilish") -> InlineKeyboardMarkup:
    url = f"https://t.me/{BOT_USERNAME}?start=ch_{source}"
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=label, url=url)]])


async def post_daily_vocab_pack(bot: Bot):
    """09:00 AM Daily 10-Word Band 8.5+ Power Pack."""
    choice = await next_item("vocab", [str(i) for i in range(len(IELTS_VOCAB_PACKS))])
    pack = IELTS_VOCAB_PACKS[int(choice)]

    lines = [
        "📖 <b>IELTS Band 8.5+ Kunlik 10 ta So'z To'plami</b>",
        f"🏷 <b>Mavzu</b>: {pack['topic']}\n"
    ]
    for i, w in enumerate(pack['words'], start=1):
        lines.append(f"<b>{i}. {w['w']}</b> — {w['m']}\n   🔗 <i>Kollokatsiya:</i> <code>{w['c']}</code>")

    try:
        await bot.send_message(chat_id=CHANNEL_ID, text="\n".join(lines) + FOOTER, parse_mode="HTML",
                               reply_markup=practice_button("vocab"))
        logger.info("Successfully posted 10-word vocabulary pack.")
    except Exception as e:
        logger.error(f"Error posting vocabulary pack: {e}")


async def post_daily_sat_quiz(bot: Bot):
    """02:00 PM Daily Interactive SAT Question of the Day."""
    candidates = channel_quiz_candidates()
    if not candidates:
        logger.warning("No channel quiz question fits Telegram poll limits.")
        return
    by_id = {item["id"]: item for item in candidates}
    item = by_id[await next_item("quiz", list(by_id))]
    label = "SAT Math" if item["sec"] == "m" else "SAT Reading & Writing"
    prompt = f"🎯 {label}\n\n{item['stem']}"

    try:
        if item["passage"]:
            await bot.send_message(chat_id=CHANNEL_ID, text=f"📄 <b>Kunning savoli: matn</b>\n\n{item['passage']}", parse_mode="HTML")
        await bot.send_poll(
            chat_id=CHANNEL_ID,
            question=prompt[:POLL_QUESTION_LIMIT],
            options=item["options"],
            type="quiz",
            correct_option_id=item["correct"],
            explanation=short_explanation(content.notes[item["id"]]["exp"]) or None,
            is_anonymous=True,
            reply_markup=practice_button("quiz"),
        )
        logger.info("Successfully posted daily SAT quiz poll.")
    except Exception as e:
        logger.error(f"Error posting daily SAT quiz: {e}")


async def post_daily_tip(bot: Bot):
    """08:00 PM Daily Strategy Tip."""
    choice = await next_item("tip", [str(i) for i in range(len(IELTS_TIPS))])
    item = IELTS_TIPS[int(choice)]
    text = f"💡 <b>Imtihon Strategiyasi: {item['title']}</b>\n\n{item['body']}{FOOTER}"
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode="HTML", reply_markup=practice_button("tip"))
        logger.info("Successfully posted daily strategy tip.")
    except Exception as e:
        logger.error(f"Error posting daily strategy tip: {e}")


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


async def send_broadcast(bot: Bot, segment: str, from_chat_id: int, message_id: int) -> tuple[int, int]:
    """Copies the admin's message to everyone in a segment. Returns how many got it, out of how many."""
    recipients = await analytics.segment_users(segment)
    sent = 0
    for user_id in recipients:
        for retry in (True, False):
            try:
                await bot.copy_message(chat_id=user_id, from_chat_id=from_chat_id, message_id=message_id)
                sent += 1
            except TelegramForbiddenError:
                await db.execute("UPDATE users SET blocked = 1 WHERE id = ?", user_id)
            except TelegramRetryAfter as e:
                await asyncio.sleep(e.retry_after)
                if retry:
                    continue
            except Exception as e:
                logger.warning("Could not send a broadcast: %s", type(e).__name__)
            break
        await asyncio.sleep(SEND_DELAY_SECONDS)
    logger.info("Broadcast to %s: %s of %s", segment, sent, len(recipients))
    return sent, len(recipients)


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    """Configures scheduled posts and messages in Asia/Tashkent timezone."""
    scheduler = AsyncIOScheduler(
        timezone=TIMEZONE,
        job_defaults={"misfire_grace_time": 3600, "coalesce": True, "max_instances": 1},
    )

    # 09:00 AM Tashkent: 10-Word Vocabulary Pack
    scheduler.add_job(post_daily_vocab_pack, CronTrigger(hour=9, minute=0, timezone=TIMEZONE), args=[bot])

    # 14:00 PM Tashkent: Interactive SAT Quiz Poll
    scheduler.add_job(post_daily_sat_quiz, CronTrigger(hour=14, minute=0, timezone=TIMEZONE), args=[bot])

    # 20:00 PM Tashkent: Evening Strategy Tip
    scheduler.add_job(post_daily_tip, CronTrigger(hour=20, minute=0, timezone=TIMEZONE), args=[bot])

    # Every hour: study reminders. Sunday 18:00: weekly reports.
    scheduler.add_job(send_reminders, CronTrigger(minute=5, timezone=TIMEZONE), args=[bot])
    scheduler.add_job(send_weekly_reports, CronTrigger(day_of_week="sun", hour=18, minute=0, timezone=TIMEZONE), args=[bot])

    return scheduler
