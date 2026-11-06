"""
Stores finished tests and builds their reports. Every attempt is graded here, whatever the client showed.
"""

import json
import uuid
from collections import defaultdict
from typing import Any, Optional

from database import db, now_ts, shift_day, today
from services import review, scoring, users
from services.content import DOMAIN_NAMES, SAT_DOMAINS, content

TARGET_SECONDS = {"rw": 71, "m": 95}
RUSHED_SECONDS = 15
MAX_ITEM_SECONDS = 3600
MAX_PRACTICE_ITEMS = 60
SECTION_NAMES = {"rw": "Reading & Writing", "m": "Math"}
IELTS_TYPE_NAMES = {
    "tfng": "True / False / Not Given", "ynng": "Yes / No / Not Given", "mcq": "Multiple choice",
    "form": "Gap fill", "heading": "Matching headings", "match": "Matching information", "summary": "Summary completion",
}


class AttemptError(ValueError):
    pass


def _clean_answer(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()[:64]


def _clean_seconds(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return 0
    return int(min(MAX_ITEM_SECONDS, max(0, value)))


def _question_row(question: dict[str, Any], module: str, item: dict[str, Any]) -> dict[str, Any]:
    chosen = _clean_answer(item.get("a"))
    return {
        "question_id": question["id"], "section": question["sec"], "domain": question["dom"],
        "skill": question.get("skill", ""), "difficulty": question["dif"], "module": module, "chosen": chosen,
        "correct": bool(chosen) and scoring.sat_answer_correct(question, chosen),
        "time_s": _clean_seconds(item.get("t")), "type": question["type"],
    }


def _breakdown(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, int]]:
    table: dict[str, dict[str, int]] = defaultdict(lambda: {"correct": 0, "total": 0})
    for row in rows:
        table[row[key]]["total"] += 1
        table[row[key]]["correct"] += int(row["correct"])
    return dict(table)


def domain_report(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    table = _breakdown(rows, "domain")
    report = []
    for section, domains in SAT_DOMAINS.items():
        for domain in domains:
            if domain in table:
                report.append({"section": section, "domain": domain, **table[domain]})
    return report


def pacing_report(rows: list[dict[str, Any]]) -> dict[str, Any]:
    timed = [row for row in rows if row["time_s"] > 0]
    if not timed:
        return {"avg_s": 0, "slow": 0, "rushed": 0, "tip": ""}
    slow = [row for row in timed if row["time_s"] > TARGET_SECONDS[row["section"]] * 1.5]
    rushed = [row for row in timed if row["time_s"] < RUSHED_SECONDS and row["chosen"] and not row["correct"]]
    if len(rushed) > len(slow):
        tip = f"{len(rushed)} ta savolda shoshilib xato qilindi. Savol shartini oxirigacha o'qishga odatlaning."
    elif len(slow) >= 3:
        tip = f"{len(slow)} ta savolga juda ko'p vaqt ketdi. Javob ko'rinmasa, belgilab, keyingisiga o'ting."
    else:
        tip = "Vaqt taqsimoti yaxshi."
    return {
        "avg_s": round(sum(row["time_s"] for row in timed) / len(timed)),
        "slow": len(slow), "rushed": len(rushed), "tip": tip,
    }


def next_steps(domains: list[dict[str, Any]], pacing: dict[str, Any]) -> list[dict[str, Any]]:
    """Up to three concrete actions, weakest domains first."""
    weak = sorted(
        (d for d in domains if d["total"] and d["correct"] / d["total"] < 0.75),
        key=lambda d: d["correct"] / d["total"],
    )
    steps = [
        {"text": f"{DOMAIN_NAMES[d['domain']]}: 10 savollik mashq",
         "action": {"type": "practice", "section": d["section"], "domain": d["domain"]}}
        for d in weak[:2]
    ]
    steps.append({"text": "Xatolar daftarini takrorlash", "action": {"type": "review"}})
    return steps[:3]


async def _previous_score(user_id: int, kind: str) -> Optional[float]:
    return await db.fetchval(
        "SELECT score FROM attempts WHERE user_id = ? AND kind = ? ORDER BY created_at DESC LIMIT 1", user_id, kind
    )


async def _store(
    user_id: int, kind: str, ref: str, title: str, rows: list[dict[str, Any]], report: dict[str, Any], *,
    correct: int, total: int, score: Optional[float] = None, low: Optional[float] = None,
    high: Optional[float] = None, duration_s: int = 0, session_code: Optional[str] = None,
    review_mode: bool = False,
) -> tuple[str, Optional[int]]:
    attempt_id = uuid.uuid4().hex
    now, day = now_ts(), today()
    async with db.transaction():
        await db.execute(
            """INSERT INTO attempts (id, user_id, kind, ref, title, session_code, correct, total, score, score_low,
                                     score_high, duration_s, report, created_at, day)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            attempt_id, user_id, kind, ref, title, session_code, correct, total,
            None if score is None else float(score), None if low is None else float(low),
            None if high is None else float(high), duration_s, json.dumps(report, ensure_ascii=False), now, day,
        )
        await db.executemany(
            """INSERT INTO answers (attempt_id, user_id, question_id, section, domain, skill, difficulty, module,
                                    chosen, is_correct, time_s, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [(attempt_id, user_id, row["question_id"], row["section"], row["domain"], row["skill"], row["difficulty"],
              row["module"], row["chosen"], int(row["correct"]), row["time_s"], now) for row in rows],
        )
        sat_rows = [row for row in rows if row["question_id"] in content.bank]
        # An unanswered mock question is not a mistake to study. In review, every answer counts.
        await review.apply_results(user_id, [
            (row["question_id"], row["correct"], row["chosen"])
            for row in sat_rows if row["chosen"] or review_mode
        ])
    rewarded_referrer = await users.mark_active(user_id)
    return attempt_id, rewarded_referrer


async def submit_sat_mock(user_id: int, payload: dict[str, Any], session_code: Optional[str]) -> dict[str, Any]:
    mock_id = payload.get("ref")
    route = payload.get("route") or {}
    if mock_id not in content.mocks or route.get("rw") not in ("easy", "hard") or route.get("math") not in ("easy", "hard"):
        raise AttemptError("unknown_mock")

    items = {item.get("q"): item for item in payload.get("items", []) if isinstance(item, dict)}
    rows = []
    for module, ids in content.mock_modules(mock_id, route).items():
        for question_id in ids:
            rows.append(_question_row(content.bank[question_id], module, items.get(question_id, {})))

    sections = {}
    for key, section in (("rw", "rw"), ("math", "m")):
        part = [row for row in rows if row["section"] == section]
        estimate = scoring.section_score([(row["difficulty"], row["type"], row["correct"]) for row in part])
        sections[key] = {
            **estimate, "correct": sum(row["correct"] for row in part), "total": len(part), "route": route[key],
        }
    total = scoring.total_score(sections["rw"], sections["math"])
    domains = domain_report(rows)
    pacing = pacing_report(rows)
    difficulty = _breakdown(rows, "difficulty")
    previous = await _previous_score(user_id, "sat_mock")
    title = content.mocks[mock_id]["title"]
    correct = sum(row["correct"] for row in rows)

    report = {
        "kind": "sat_mock", "title": title, **total, "sections": sections, "domains": domains,
        "difficulty": difficulty, "pacing": pacing, "steps": next_steps(domains, pacing),
        "previous": previous, "ref": mock_id, "route": route,
    }
    attempt_id, referrer = await _store(
        user_id, "sat_mock", mock_id, title, rows, report, correct=correct, total=len(rows),
        score=total["score"], low=total["low"], high=total["high"],
        duration_s=sum(row["time_s"] for row in rows), session_code=session_code,
    )
    return {"id": attempt_id, "report": report, "referrer": referrer}


async def submit_practice(user_id: int, payload: dict[str, Any]) -> dict[str, Any]:
    mode = payload.get("mode")
    if mode not in ("domain", "review", "diagnostic"):
        raise AttemptError("unknown_mode")
    raw_items = [item for item in payload.get("items", []) if isinstance(item, dict)][:MAX_PRACTICE_ITEMS]
    rows = [_question_row(content.bank[item["q"]], mode, item) for item in raw_items if item.get("q") in content.bank]
    if not rows:
        raise AttemptError("empty")

    correct = sum(row["correct"] for row in rows)
    domains = domain_report(rows)
    pacing = pacing_report(rows)
    kind = "diagnostic" if mode == "diagnostic" else "practice"
    label = str(payload.get("ref") or "")[:80]
    title = {"domain": f"Mashq: {label}" if label else "Mashq", "review": "Xatolarni takrorlash", "diagnostic": "Diagnostika"}[mode]
    report = {
        "kind": kind, "mode": mode, "title": title, "correct": correct, "total": len(rows),
        "domains": domains, "pacing": pacing, "steps": next_steps(domains, pacing),
    }
    attempt_id, referrer = await _store(
        user_id, kind, mode if not label else label, title, rows, report, correct=correct, total=len(rows),
        duration_s=sum(row["time_s"] for row in rows), review_mode=mode == "review",
    )
    return {"id": attempt_id, "report": report, "referrer": referrer}


async def submit_ielts(user_id: int, payload: dict[str, Any], session_code: Optional[str]) -> dict[str, Any]:
    kind = payload.get("kind")
    tests, table = (
        (content.reading, scoring.READING_BANDS) if kind == "ielts_reading" else (content.listening, scoring.LISTENING_BANDS)
    )
    test = tests.get(payload.get("ref"))
    if test is None:
        raise AttemptError("unknown_test")
    answers = payload.get("answers") if isinstance(payload.get("answers"), dict) else {}
    section = "ielts_r" if kind == "ielts_reading" else "ielts_l"

    rows = []
    for question in test["questions"]:
        chosen = _clean_answer(answers.get(str(question["num"])))
        rows.append({
            "question_id": f"{section}{test['num']}_{question['num']}", "section": section, "domain": question["type"],
            "skill": "", "difficulty": "", "module": "", "chosen": chosen,
            "correct": scoring.ielts_answer_correct(question, chosen), "time_s": 0, "type": question["type"],
        })
    correct = sum(row["correct"] for row in rows)
    band = scoring.ielts_band(correct, table)
    by_type = [
        {"type": name, "label": IELTS_TYPE_NAMES.get(name, name), **value}
        for name, value in _breakdown(rows, "domain").items()
    ]
    previous = await _previous_score(user_id, kind)
    report = {
        "kind": kind, "title": test["title"], "band": band, "correct": correct, "total": len(rows),
        "types": by_type, "previous": previous, "ref": test["num"],
        "wrong": [question["num"] for question, row in zip(test["questions"], rows) if not row["correct"]],
    }
    attempt_id, referrer = await _store(
        user_id, kind, str(test["num"]), test["title"], rows, report, correct=correct, total=len(rows),
        score=band, duration_s=_clean_seconds(payload.get("duration_s")) if payload.get("duration_s") else 0,
        session_code=session_code,
    )
    return {"id": attempt_id, "report": report, "referrer": referrer}


def _public_attempt(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row["id"], "kind": row["kind"], "ref": row["ref"], "title": row["title"], "correct": row["correct"],
        "total": row["total"], "score": row["score"], "low": row["score_low"], "high": row["score_high"],
        "day": row["day"], "at": row["created_at"], "session": row["session_code"],
    }


async def list_attempts(user_id: int, limit: int = 40) -> list[dict[str, Any]]:
    rows = await db.fetch(
        "SELECT * FROM attempts WHERE user_id = ? ORDER BY created_at DESC LIMIT ?", user_id, limit
    )
    return [_public_attempt(row) for row in rows]


async def get_attempt(user_id: int, attempt_id: str) -> Optional[dict[str, Any]]:
    row = await db.fetchrow("SELECT * FROM attempts WHERE id = ? AND user_id = ?", attempt_id, user_id)
    if row is None:
        return None
    answers = await db.fetch(
        "SELECT question_id, module, chosen, is_correct, time_s FROM answers WHERE attempt_id = ?", attempt_id
    )
    return {**_public_attempt(row), "report": json.loads(row["report"]), "answers": answers}


async def mastery(user_id: int, recent: int = 400) -> list[dict[str, Any]]:
    """Accuracy per SAT domain over the latest answers. Domains with no data are listed with total 0."""
    rows = await db.fetch(
        """SELECT section, domain, is_correct AS correct FROM answers
           WHERE user_id = ? AND section IN ('rw', 'm') ORDER BY created_at DESC LIMIT ?""",
        user_id, recent,
    )
    table = _breakdown(rows, "domain")
    return [
        {"section": section, "domain": domain, **table.get(domain, {"correct": 0, "total": 0})}
        for section, domains in SAT_DOMAINS.items() for domain in domains
    ]


async def weak_domains(user_id: int, section: Optional[str] = None) -> list[dict[str, Any]]:
    """Weakest first. Smoothing keeps two lucky answers from outranking a domain with real data."""
    def key(item: dict[str, Any]) -> float:
        return (item["correct"] + 1.4) / (item["total"] + 2)

    domains = await mastery(user_id)
    if section:
        domains = [d for d in domains if d["section"] == section]
    return sorted(domains, key=key)


async def summary(user_id: int) -> dict[str, Any]:
    totals = await db.fetchrow(
        """SELECT COUNT(*) AS answered, COALESCE(SUM(is_correct), 0) AS correct FROM answers
           WHERE user_id = ? AND section IN ('rw', 'm')""",
        user_id,
    )
    latest = {}
    for kind in ("sat_mock", "ielts_reading", "ielts_listening"):
        row = await db.fetchrow(
            "SELECT * FROM attempts WHERE user_id = ? AND kind = ? ORDER BY created_at DESC LIMIT 1", user_id, kind
        )
        latest[kind] = _public_attempt(row) if row else None
    has_diagnostic = await db.fetchval("SELECT COUNT(*) FROM attempts WHERE user_id = ? AND kind = 'diagnostic'", user_id)
    return {
        "answered": int(totals["answered"]), "correct": int(totals["correct"] or 0),
        "latest": latest, "diagnostic_done": bool(has_diagnostic),
    }


async def kinds_done_today(user_id: int) -> set[str]:
    rows = await db.fetch("SELECT kind, ref FROM attempts WHERE user_id = ? AND day = ?", user_id, today())
    done = {row["kind"] for row in rows}
    done.update(f"{row['kind']}:{row['ref']}" for row in rows)
    return done


async def week_activity(user_id: int) -> list[dict[str, Any]]:
    start = shift_day(today(), -6)
    rows = await db.fetch(
        "SELECT day, COUNT(*) AS tests, SUM(total) AS questions FROM attempts WHERE user_id = ? AND day >= ? GROUP BY day",
        user_id, start,
    )
    by_day = {row["day"]: row for row in rows}
    return [
        {"day": day, "tests": int(by_day[day]["tests"]) if day in by_day else 0}
        for day in (shift_day(start, offset) for offset in range(7))
    ]
