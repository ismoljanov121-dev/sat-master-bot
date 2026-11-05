import random
import logging
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from config import CHANNEL_ID, TIMEZONE
from content_bank import IELTS_VOCAB_PACKS, SAT_QUIZZES, IELTS_TIPS

logger = logging.getLogger(__name__)

async def post_daily_vocab_pack(bot: Bot):
    """09:00 AM Daily 10-Word Band 8.5+ Power Pack."""
    pack = random.choice(IELTS_VOCAB_PACKS)
    
    lines = [
        f"📖 <b>IELTS Band 8.5+ Kunlik 10 ta So'z To'plami</b>",
        f"🏷 <b>Mavzu</b>: {pack['topic']}\n"
    ]
    for i, w in enumerate(pack['words'], start=1):
        lines.append(f"<b>{i}. {w['w']}</b> — {w['m']}\n   🔗 <i>Kollokatsiya:</i> <code>{w['c']}</code>")

    lines.append("\n━━━━━━━━━━━━━━━━━━━━")
    lines.append("🤖 <b>To'liq IELTS 1–19 va SAT Bluebook bazasi:</b> @ieltssat_dailybot")

    text = "\n".join(lines)
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode="HTML")
        logger.info("Successfully posted 10-word vocabulary pack.")
    except Exception as e:
        logger.error(f"Error posting vocabulary pack: {e}")

async def post_daily_sat_quiz(bot: Bot):
    """02:00 PM Daily Interactive SAT Question of the Day."""
    item = random.choice(SAT_QUIZZES)
    prompt = f"🎯 [Question of the Day] {item['type']}\n\n{item['question']}"
    
    try:
        await bot.send_poll(
            chat_id=CHANNEL_ID,
            question=prompt[:300],
            options=item['options'],
            type="quiz",
            correct_option_id=item['correct_option_id'],
            explanation=item['explanation'][:200],
            is_anonymous=True
        )
        logger.info("Successfully posted daily SAT quiz poll.")
    except Exception as e:
        logger.error(f"Error posting daily SAT quiz: {e}")

async def post_daily_tip(bot: Bot):
    """08:00 PM Daily Strategy Tip."""
    item = random.choice(IELTS_TIPS)
    text = (
        f"💡 <b>Imtihon Strategiyasi: {item['title']}</b>\n\n"
        f"{item['body']}\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🤖 <b>Bepul Cambridge kitoblarini olish:</b> @ieltssat_dailybot"
    )
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode="HTML")
        logger.info("Successfully posted daily strategy tip.")
    except Exception as e:
        logger.error(f"Error posting daily strategy tip: {e}")

def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    """Configures scheduled daily posts in Asia/Tashkent timezone."""
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

    return scheduler
