"""
User records: first contact, goals, streaks and referral rewards.
"""

import re
from typing import Any

from database import day_diff, db, now_ts, shift_day, today

PROFILE_FIELDS = (
    "focus", "target_sat", "target_ielts", "exam_date",
    "daily_minutes", "reminder_hour", "reminders_on", "onboarded",
)
FOCUS_VALUES = ("sat", "ielts", "both")


async def get_user(user_id: int) -> dict[str, Any] | None:
    return await db.fetchrow("SELECT * FROM users WHERE id = ?", user_id)


async def touch_user(
    tg_user: dict[str, Any],
    *,
    source: str = "",
    referred_by: int | None = None,
    bot_started: bool = False,
) -> tuple[dict[str, Any], bool]:
    """Creates or refreshes a user from Telegram data. Returns (row, is_new)."""
    user_id = int(tg_user["id"])
    existing = await get_user(user_id)
    now = now_ts()
    first_name = str(tg_user.get("first_name") or "")[:128]
    username = str(tg_user.get("username") or "")[:64]
    language = str(tg_user.get("language_code") or "")[:12]

    if existing is None:
        if referred_by == user_id:
            referred_by = None
        await db.execute(
            """INSERT INTO users (id, first_name, username, language_code, created_at, last_seen_at,
                                  source, referred_by, bot_started)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT (id) DO NOTHING""",
            user_id, first_name, username, language, now, now, source[:64], referred_by, int(bot_started),
        )
        return await get_user(user_id), True

    await db.execute(
        """UPDATE users SET first_name = ?, username = ?, language_code = ?, last_seen_at = ?,
                            bot_started = ?, blocked = ?
           WHERE id = ?""",
        first_name, username, language, now,
        1 if bot_started else existing["bot_started"],
        0 if bot_started else existing["blocked"],
        user_id,
    )
    return await get_user(user_id), False


def clean_profile(payload: dict[str, Any]) -> dict[str, Any]:
    """Keeps only valid goal settings. Unknown or malformed fields are dropped."""
    clean: dict[str, Any] = {}
    if payload.get("focus") in FOCUS_VALUES:
        clean["focus"] = payload["focus"]
    if "target_sat" in payload:
        value = payload["target_sat"]
        if value is None:
            clean["target_sat"] = None
        elif isinstance(value, int) and 400 <= value <= 1600:
            clean["target_sat"] = value
    if "target_ielts" in payload:
        value = payload["target_ielts"]
        if value is None:
            clean["target_ielts"] = None
        elif isinstance(value, (int, float)) and 4 <= value <= 9:
            clean["target_ielts"] = float(value)
    if "exam_date" in payload:
        value = payload["exam_date"]
        if value is None or value == "":
            clean["exam_date"] = None
        elif isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            clean["exam_date"] = value
    if isinstance(payload.get("daily_minutes"), int) and 10 <= payload["daily_minutes"] <= 180:
        clean["daily_minutes"] = payload["daily_minutes"]
    if isinstance(payload.get("reminder_hour"), int) and 0 <= payload["reminder_hour"] <= 23:
        clean["reminder_hour"] = payload["reminder_hour"]
    if isinstance(payload.get("reminders_on"), bool):
        clean["reminders_on"] = int(payload["reminders_on"])
    if isinstance(payload.get("onboarded"), bool):
        clean["onboarded"] = int(payload["onboarded"])
    return clean


async def update_profile(user_id: int, fields: dict[str, Any]) -> dict[str, Any]:
    names = [name for name in PROFILE_FIELDS if name in fields]
    if names:
        assignments = ", ".join(f"{name} = ?" for name in names)
        await db.execute(
            f"UPDATE users SET {assignments} WHERE id = ?",
            *[fields[name] for name in names], user_id,
        )
    return await get_user(user_id)


async def mark_active(user_id: int) -> int | None:
    """Records study activity today and returns the referrer to reward, if this is the first time."""
    row = await get_user(user_id)
    if row is None:
        return None
    day = today()
    if row["last_active_day"] != day:
        yesterday = shift_day(day, -1)
        streak = row["streak"] + 1 if row["last_active_day"] == yesterday else 1
        await db.execute(
            "UPDATE users SET streak = ?, best_streak = ?, last_active_day = ? WHERE id = ?",
            streak, max(streak, row["best_streak"]), day, user_id,
        )
    if row["referred_by"] and not row["referral_rewarded"]:
        await db.execute("UPDATE users SET referral_rewarded = 1 WHERE id = ?", user_id)
        await db.execute("UPDATE users SET ai_bonus = ai_bonus + 1 WHERE id = ?", row["referred_by"])
        return row["referred_by"]
    return None


def current_streak(row: dict[str, Any]) -> int:
    """A streak survives until the end of the day after the last activity."""
    last = row.get("last_active_day")
    if not last or day_diff(today(), last) > 1:
        return 0
    return row["streak"]


async def referral_count(user_id: int) -> tuple[int, int]:
    """Returns (people who joined, people who started studying)."""
    joined = await db.fetchval("SELECT COUNT(*) FROM users WHERE referred_by = ?", user_id)
    active = await db.fetchval(
        "SELECT COUNT(*) FROM users WHERE referred_by = ? AND referral_rewarded = 1", user_id
    )
    return int(joined or 0), int(active or 0)


async def record_event(user_id: int, name: str, meta: str = "") -> None:
    await db.execute(
        "INSERT INTO events (user_id, name, meta, day, created_at) VALUES (?, ?, ?, ?, ?)",
        user_id, name[:48], meta[:120], today(), now_ts(),
    )
