"""
Daily study plan and the weekly summary, both derived from what the student actually did.
"""

from datetime import datetime
from typing import Any

from database import day_diff, db, shift_day, today
from services import attempts, review, users

WEEKDAY_SKILL = {0: "reading", 1: "writing", 2: "listening", 3: "reading", 4: "writing", 5: "listening", 6: "reading"}
SKILL_TASKS = {
    "reading": ("IELTS Reading", "Bitta matn ustida ishlang", 20, {"type": "reading"}, "ielts_reading"),
    "listening": ("IELTS Listening", "Bitta bo'limni tinglang", 15, {"type": "listening"}, "ielts_listening"),
    "writing": ("IELTS Writing", "Bitta inshoni yozib tekshiring", 40, {"type": "writing"}, "writing"),
}
MOCK_INTERVAL_DAYS = 7


def _task(task_id: str, title: str, detail: str, minutes: int, action: dict[str, Any], done: bool) -> dict[str, Any]:
    return {"id": task_id, "title": title, "detail": detail, "minutes": minutes, "action": action, "done": done}


async def today_plan(user: dict[str, Any]) -> dict[str, Any]:
    user_id = user["id"]
    day = today()
    focus = user["focus"] or "sat"
    budget = user["daily_minutes"]
    done = await attempts.kinds_done_today(user_id)
    due = await review.due_count(user_id)
    overview = await attempts.summary(user_id)
    writing_today = await db.fetchval(
        "SELECT COUNT(*) FROM writing_submissions WHERE user_id = ? AND day = ?", user_id, day
    )
    if writing_today:
        done.add("writing")

    tasks: list[dict[str, Any]] = []
    studies_sat = focus in ("sat", "both")
    studies_ielts = focus in ("ielts", "both")

    if studies_sat and not overview["diagnostic_done"]:
        tasks.append(_task("diagnostic", "Diagnostika", "Zaif mavzularingizni aniqlaymiz", 15, {"type": "diagnostic"}, False))

    if due or "practice:review" in done:
        count = min(due, 10)
        tasks.append(_task(
            "review", "Xatolarni takrorlash",
            f"{count} ta savol vaqti keldi" if count else "Bugungi takrorlash bajarildi",
            max(5, count), {"type": "review"}, due == 0,
        ))

    if studies_sat and overview["diagnostic_done"]:
        weak = await attempts.weak_domains(user_id)
        first = weak[0]
        tasks.append(_task(
            "practice", f"{first['domain']}", "10 savollik mashq", 12,
            {"type": "practice", "section": first["section"], "domain": first["domain"]},
            f"practice:{first['domain']}" in done,
        ))
        if budget >= 45:
            other = next((d for d in weak if d["section"] != first["section"]), weak[1])
            tasks.append(_task(
                "practice2", f"{other['domain']}", "10 savollik mashq", 12,
                {"type": "practice", "section": other["section"], "domain": other["domain"]},
                f"practice:{other['domain']}" in done,
            ))

        latest = overview["latest"]["sat_mock"]
        days_since = day_diff(day, latest["day"]) if latest else None
        weekend = datetime.strptime(day, "%Y-%m-%d").weekday() >= 5
        if (days_since is None or days_since >= MOCK_INTERVAL_DAYS) and weekend:
            tasks.append(_task("mock", "To'liq SAT mock", "Haftalik nazorat imtihoni", 134, {"type": "mock"}, "sat_mock" in done))

    if studies_ielts:
        skill = WEEKDAY_SKILL[datetime.strptime(day, "%Y-%m-%d").weekday()]
        title, detail, minutes, action, done_key = SKILL_TASKS[skill]
        tasks.append(_task(f"ielts_{skill}", title, detail, minutes, action, done_key in done))

    days_left = None
    if user["exam_date"]:
        days_left = day_diff(user["exam_date"], day)
    return {
        "tasks": tasks, "done": sum(task["done"] for task in tasks), "total": len(tasks),
        "days_left": days_left, "minutes": sum(task["minutes"] for task in tasks if not task["done"]),
    }


async def weekly_report(user: dict[str, Any]) -> dict[str, Any]:
    user_id = user["id"]
    start = shift_day(today(), -6)
    previous_start = shift_day(start, -7)
    rows = await db.fetch(
        """SELECT domain, section, is_correct, attempts.day AS day FROM answers
           JOIN attempts ON attempts.id = answers.attempt_id
           WHERE answers.user_id = ? AND attempts.day >= ? AND section IN ('rw', 'm')""",
        user_id, previous_start,
    )
    this_week = [row for row in rows if row["day"] >= start]
    last_week = [row for row in rows if row["day"] < start]

    def accuracy(items: list[dict[str, Any]]) -> int | None:
        return round(100 * sum(row["is_correct"] for row in items) / len(items)) if items else None

    per_domain: dict[str, list[dict[str, Any]]] = {}
    for row in this_week:
        per_domain.setdefault(row["domain"], []).append(row)
    ranked = sorted(
        ((accuracy(items), name) for name, items in per_domain.items() if len(items) >= 3),
        key=lambda pair: pair[0],
    )
    active_days = await db.fetchval(
        "SELECT COUNT(DISTINCT day) FROM attempts WHERE user_id = ? AND day >= ?", user_id, start
    )
    return {
        "questions": len(this_week), "accuracy": accuracy(this_week), "previous_accuracy": accuracy(last_week),
        "active_days": int(active_days or 0), "streak": users.current_streak(user),
        "best": ranked[-1] if ranked else None, "worst": ranked[0] if ranked else None,
        "due": await review.due_count(user_id),
    }


def weekly_report_text(report: dict[str, Any]) -> str:
    lines = ["📊 <b>Haftalik hisobotingiz</b>\n"]
    if not report["questions"]:
        lines.append("Bu hafta savol ishlanmadi. Bugun 10 daqiqadan boshlab ko'ring.")
        return "\n".join(lines)
    lines.append(f"• Ishlangan savollar: <b>{report['questions']}</b>")
    lines.append(f"• Aniqlik: <b>{report['accuracy']}%</b>")
    if report["previous_accuracy"] is not None:
        delta = report["accuracy"] - report["previous_accuracy"]
        lines.append(f"• O'tgan haftaga nisbatan: <b>{delta:+d}%</b>")
    lines.append(f"• Faol kunlar: <b>{report['active_days']} / 7</b>")
    if report["streak"]:
        lines.append(f"• Ketma-ket kunlar: <b>{report['streak']}</b>")
    if report["best"] and report["worst"] and report["best"] != report["worst"]:
        lines.append(f"\n💪 Eng yaxshi mavzu: {report['best'][1]} ({report['best'][0]}%)")
        lines.append(f"🎯 E'tibor bering: {report['worst'][1]} ({report['worst'][0]}%)")
    if report["due"]:
        lines.append(f"\nTakrorlash uchun {report['due']} ta savol kutmoqda.")
    return "\n".join(lines)
