"""
Group exam entries: who is taking the exam, when their time runs out, and the one result that counts.

Sealed exams reach students through this module without answer keys. The server routes the adaptive second
module itself, so the phone never needs a key.
"""

import json
from typing import Any, Optional

from database import db, now_ts
from services.content import content

# The SAT clock includes the ten-minute break between the two sections.
EXAM_SECONDS = {"sat_mock": (134 + 10) * 60, "ielts_reading": 60 * 60, "ielts_listening": 40 * 60}
GRACE_SECONDS = 180
NAME_MIN = 3
NAME_MAX = 80
KEY_FIELDS = ("cor", "ans", "alts", "expl")


class SessionError(ValueError):
    def __init__(self, code: str, status: int = 400):
        super().__init__(code)
        self.code = code
        self.status = status


def is_sealed(kind: str, ref: Any) -> bool:
    if kind == "sat_mock":
        return ref in content.sealed_mocks
    return kind == "ielts_reading" and str(ref).isdigit() and int(ref) in content.sealed_reading


def without_keys(item: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in item.items() if key not in KEY_FIELDS}


def sealed_paper(session: dict[str, Any]) -> Optional[dict[str, Any]]:
    """Everything a student needs to answer a sealed exam, and nothing that gives the answers away."""
    if not is_sealed(session["kind"], session["ref"]):
        return None
    if session["kind"] == "sat_mock":
        mock = content.mocks[session["ref"]]
        questions = {qid: without_keys(content.bank[qid]) for qid in content.mock_questions[mock["id"]]}
        return {"mock": mock, "questions": questions}
    test = content.reading[int(session["ref"])]
    return {"test": {**test, "questions": [without_keys(question) for question in test["questions"]]}}


def clean_name(value: Any) -> str:
    return " ".join(str(value or "").split())[:NAME_MAX]


async def get_entry(code: str, user_id: int) -> Optional[dict[str, Any]]:
    return await db.fetchrow("SELECT * FROM session_entries WHERE code = ? AND user_id = ?", code, user_id)


async def last_name(user_id: int) -> str:
    """The name the student gave last time, so they type it only once."""
    name = await db.fetchval(
        "SELECT full_name FROM session_entries WHERE user_id = ? AND full_name <> '' ORDER BY started_at DESC LIMIT 1", user_id
    )
    return name or ""


async def _create_entry(session: dict[str, Any], user_id: int, name: str) -> dict[str, Any]:
    now = now_ts()
    await db.execute(
        """INSERT INTO session_entries (code, user_id, full_name, started_at, deadline_at) VALUES (?, ?, ?, ?, ?)
           ON CONFLICT (code, user_id) DO NOTHING""",
        session["code"], user_id, name, now, now + EXAM_SECONDS[session["kind"]],
    )
    return await get_entry(session["code"], user_id)


async def start(session: dict[str, Any], user_id: int, name: Any) -> dict[str, Any]:
    """Starts the clock once. Coming back later, even after the exam closed, continues the same entry."""
    entry = await get_entry(session["code"], user_id)
    if entry is not None:
        return entry
    if session["status"] != "open":
        raise SessionError("session_closed", 404)
    full_name = clean_name(name)
    if len(full_name) < NAME_MIN:
        raise SessionError("name_required")
    return await _create_entry(session, user_id, full_name)


def seconds_left(entry: dict[str, Any]) -> int:
    return max(0, entry["deadline_at"] - now_ts())


async def lock_module(entry: dict[str, Any], section: str, route: str, items: dict[str, dict[str, Any]]) -> None:
    """Keeps the routed module's answers on the server, so a finished module cannot be changed later."""
    state = json.loads(entry["state"])
    state.setdefault("route", {})[section] = route
    state.setdefault("answers", {}).update(items)
    await db.execute(
        "UPDATE session_entries SET state = ? WHERE code = ? AND user_id = ?",
        json.dumps(state, ensure_ascii=False), entry["code"], entry["user_id"],
    )


async def claim(session: dict[str, Any], user_id: int, attempt_id: str) -> bool:
    """Runs inside the attempt's transaction. False means another submit got there first, so this one rolls back."""
    entry = await get_entry(session["code"], user_id) or await _create_entry(session, user_id, "")
    now = now_ts()
    await db.execute(
        """UPDATE session_entries SET attempt_id = ?, finished_at = ?, late = ?
           WHERE code = ? AND user_id = ? AND attempt_id IS NULL""",
        attempt_id, now, int(now > entry["deadline_at"] + GRACE_SECONDS), session["code"], user_id,
    )
    return (await get_entry(session["code"], user_id))["attempt_id"] == attempt_id
