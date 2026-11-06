"""
What the admin needs to decide what to build next: where students come from, where they drop off, and who to
write to. Reminders and broadcasts both respect a student who turned messages off.
"""

import html
from datetime import datetime
from typing import Any, Optional

from database import TZ, day_diff, db, now_ts, shift_day, today

DAY_SECONDS = 86400
FUNNEL_DAYS = 30
RETURN_WINDOW_DAYS = 37
RETURN_AFTER_DAYS = 7
INACTIVE_DAYS = 14

CHANNEL_LABELS = {"ch_vocab": "Kanal: lug'at", "ch_quiz": "Kanal: quiz", "ch_tip": "Kanal: strategiya"}
SEGMENT_NAMES = {
    "hammasi": "Hamma", "faol": "7 kunda faol", "nofaol": "14 kundan beri faol emas", "boshlamagan": "Hali mashq qilmagan",
    "sat": "SAT tanlaganlar", "ielts": "IELTS tanlaganlar",
}
REACHABLE = "bot_started = 1 AND blocked = 0 AND reminders_on = 1"


def source_label(source: str) -> str:
    """Deep links carry codes, so raw sources are folded into the channels a person can act on."""
    if not source:
        return "To'g'ridan-to'g'ri"
    if source == "referral":
        return "Do'st taklifi"
    if source.startswith("s_"):
        return "Guruh imtihoni"
    if source.startswith("teacher_"):
        return "O'qituvchi havolasi"
    return CHANNEL_LABELS.get(source, source)


async def funnel(days: int = FUNNEL_DAYS) -> dict[str, Any]:
    """New students of the last days, step by step, in total and per source."""
    rows = await db.fetch(
        """SELECT source, COUNT(*) AS users, SUM(onboarded) AS onboarded,
                  SUM(CASE WHEN last_active_day IS NULL THEN 0 ELSE 1 END) AS studied,
                  SUM(CASE WHEN last_active_day >= ? THEN 1 ELSE 0 END) AS active
           FROM users WHERE created_at >= ? GROUP BY source""",
        shift_day(today(), -6), now_ts() - days * DAY_SECONDS,
    )
    steps = ("users", "onboarded", "studied", "active")
    sources: dict[str, dict[str, int]] = {}
    for row in rows:
        entry = sources.setdefault(source_label(row["source"]), dict.fromkeys(steps, 0))
        for step in steps:
            entry[step] += int(row[step] or 0)
    ranked = sorted(sources.items(), key=lambda item: -item[1]["users"])
    return {"days": days, "total": {step: sum(item[step] for item in sources.values()) for step in steps}, "sources": ranked}


async def week_return() -> dict[str, int]:
    """Of the students who joined one to five weeks ago, how many still studied a week or more after joining."""
    now = now_ts()
    rows = await db.fetch(
        "SELECT created_at, last_active_day FROM users WHERE created_at >= ? AND created_at <= ?",
        now - RETURN_WINDOW_DAYS * DAY_SECONDS, now - RETURN_AFTER_DAYS * DAY_SECONDS,
    )
    returned = 0
    for row in rows:
        joined = datetime.fromtimestamp(row["created_at"], TZ).strftime("%Y-%m-%d")
        returned += bool(row["last_active_day"]) and day_diff(row["last_active_day"], joined) >= RETURN_AFTER_DAYS
    return {"users": len(rows), "returned": returned}


async def recent_events(limit: int = 12) -> list[dict[str, Any]]:
    return await db.fetch(
        """SELECT name, COUNT(*) AS total, COUNT(DISTINCT user_id) AS people FROM events
           WHERE day >= ? GROUP BY name ORDER BY total DESC LIMIT ?""",
        shift_day(today(), -6), limit,
    )


def _share(part: int, whole: int) -> str:
    return f"{round(100 * part / whole)}%" if whole else "0%"


async def report_text() -> str:
    data = await funnel()
    total = data["total"]
    back = await week_return()
    lines = [
        f"📈 <b>Oxirgi {data['days']} kun</b>\n",
        f"👥 Yangi: <b>{total['users']}</b>",
        f"🎯 Maqsad belgilagan: <b>{total['onboarded']}</b> ({_share(total['onboarded'], total['users'])})",
        f"✏️ Mashq boshlagan: <b>{total['studied']}</b> ({_share(total['studied'], total['users'])})",
        f"🟢 7 kunda faol: <b>{total['active']}</b> ({_share(total['active'], total['users'])})",
        f"🔁 Bir haftadan keyin qaytgan: <b>{back['returned']}</b> / {back['users']} ({_share(back['returned'], back['users'])})",
    ]
    if data["sources"]:
        lines.append("\n<b>Manbalar</b> (keldi → mashq boshladi)")
        lines += [
            f"• {html.escape(name)}: {entry['users']} → {entry['studied']} ({_share(entry['studied'], entry['users'])})"
            for name, entry in data["sources"][:10]
        ]
    events = await recent_events()
    if events:
        lines.append("\n<b>7 kunlik hodisalar</b> (necha marta / necha kishi)")
        lines += [f"• {html.escape(row['name'])}: {int(row['total'])} / {int(row['people'])}" for row in events]
    return "\n".join(lines)


def _segment_filter(segment: str) -> tuple[str, tuple]:
    day = today()
    filters: dict[str, tuple[str, tuple]] = {
        "hammasi": ("", ()),
        "faol": (" AND last_active_day >= ?", (shift_day(day, -6),)),
        "nofaol": (" AND last_active_day < ?", (shift_day(day, -INACTIVE_DAYS),)),
        "boshlamagan": (" AND last_active_day IS NULL", ()),
        "sat": (" AND focus IN ('sat', 'both')", ()),
        "ielts": (" AND focus IN ('ielts', 'both')", ()),
    }
    return filters[segment]


async def segment_size(segment: str) -> int:
    where, args = _segment_filter(segment)
    return int(await db.fetchval(f"SELECT COUNT(*) FROM users WHERE {REACHABLE}{where}", *args) or 0)


async def segment_users(segment: str) -> list[int]:
    where, args = _segment_filter(segment)
    return [row["id"] for row in await db.fetch(f"SELECT id FROM users WHERE {REACHABLE}{where}", *args)]


def find_segment(name: Optional[str]) -> Optional[str]:
    value = (name or "").strip().lower()
    return value if value in SEGMENT_NAMES else None
