"""
Learning centers: teachers, group exam sessions with join codes, results and CSV export.
"""

import csv
import io
import json
import secrets
import uuid
from typing import Any, Optional

from config import ADMIN_IDS
from database import db, now_ts
from services import sessions
from services.content import content

CODE_ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"


def _code(length: int) -> str:
    return "".join(secrets.choice(CODE_ALPHABET) for _ in range(length))


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


async def create_center(name: str, created_by: int) -> dict[str, Any]:
    center_id = uuid.uuid4().hex
    teacher_code = _code(10)
    now = now_ts()
    await db.execute(
        "INSERT INTO centers (id, name, teacher_code, created_by, created_at) VALUES (?, ?, ?, ?, ?)",
        center_id, name.strip()[:80], teacher_code, created_by, now,
    )
    await db.execute(
        "INSERT INTO center_members (center_id, user_id, role, joined_at) VALUES (?, ?, 'teacher', ?)",
        center_id, created_by, now,
    )
    return await db.fetchrow("SELECT * FROM centers WHERE id = ?", center_id)


async def list_centers() -> list[dict[str, Any]]:
    return await db.fetch(
        """SELECT centers.*, (SELECT COUNT(*) FROM center_members m WHERE m.center_id = centers.id AND m.role = 'student') AS students
           FROM centers ORDER BY created_at DESC"""
    )


async def join_as_teacher(teacher_code: str, user_id: int) -> Optional[dict[str, Any]]:
    center = await db.fetchrow("SELECT * FROM centers WHERE teacher_code = ?", teacher_code.strip().upper())
    if center is None:
        return None
    await db.execute(
        """INSERT INTO center_members (center_id, user_id, role, joined_at) VALUES (?, ?, 'teacher', ?)
           ON CONFLICT (center_id, user_id) DO UPDATE SET role = 'teacher'""",
        center["id"], user_id, now_ts(),
    )
    return center


async def teacher_center_ids(user_id: int) -> list[str]:
    rows = await db.fetch("SELECT center_id FROM center_members WHERE user_id = ? AND role = 'teacher'", user_id)
    return [row["center_id"] for row in rows]


async def is_staff(user_id: int) -> bool:
    return is_admin(user_id) or bool(await teacher_center_ids(user_id))


def exam_catalog() -> list[dict[str, Any]]:
    """Exams a teacher can assign to a session, the ones with server-side keys first."""
    items = [{"kind": "sat_mock", "ref": mock["id"], "title": mock["title"]} for mock in content.mocks.values()]
    items += [{"kind": "ielts_reading", "ref": str(n), "title": f"IELTS Reading: {t['title']}"} for n, t in content.reading.items()]
    items += [{"kind": "ielts_listening", "ref": str(n), "title": f"IELTS Listening: {t['title']}"} for n, t in content.listening.items()]
    for item in items:
        item["secure"] = sessions.is_sealed(item["kind"], item["ref"])
    return sorted(items, key=lambda item: not item["secure"])


async def create_session(created_by: int, kind: str, ref: str, title: str = "") -> dict[str, Any]:
    exam = next((item for item in exam_catalog() if item["kind"] == kind and item["ref"] == ref), None)
    if exam is None:
        raise ValueError("unknown_exam")
    center_ids = await teacher_center_ids(created_by)
    center_id = center_ids[0] if center_ids else None
    for _ in range(8):
        code = _code(6)
        if await db.fetchval("SELECT COUNT(*) FROM exam_sessions WHERE code = ?", code) == 0:
            break
    await db.execute(
        """INSERT INTO exam_sessions (code, center_id, created_by, title, kind, ref, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        code, center_id, created_by, (title.strip() or exam["title"])[:100], kind, ref, now_ts(),
    )
    return await get_session(code)


async def get_session(code: str) -> Optional[dict[str, Any]]:
    return await db.fetchrow("SELECT * FROM exam_sessions WHERE code = ?", code.strip().upper())


async def can_manage(user_id: int, session: dict[str, Any]) -> bool:
    if is_admin(user_id) or session["created_by"] == user_id:
        return True
    return session["center_id"] in await teacher_center_ids(user_id)


async def join_session(user_id: int, code: str) -> Optional[dict[str, Any]]:
    session = await get_session(code)
    if session is None or session["status"] != "open":
        return None
    if session["center_id"]:
        await db.execute(
            """INSERT INTO center_members (center_id, user_id, role, joined_at) VALUES (?, ?, 'student', ?)
               ON CONFLICT (center_id, user_id) DO NOTHING""",
            session["center_id"], user_id, now_ts(),
        )
    return session


async def close_session(code: str) -> None:
    await db.execute("UPDATE exam_sessions SET status = 'closed', closed_at = ? WHERE code = ?", now_ts(), code)


async def list_sessions(user_id: int, limit: int = 30) -> list[dict[str, Any]]:
    if is_admin(user_id):
        rows = await db.fetch("SELECT * FROM exam_sessions ORDER BY created_at DESC LIMIT ?", limit)
    else:
        center_ids = await teacher_center_ids(user_id)
        marks = ", ".join("?" for _ in center_ids) or "''"
        rows = await db.fetch(
            f"""SELECT * FROM exam_sessions WHERE created_by = ? OR center_id IN ({marks})
                ORDER BY created_at DESC LIMIT ?""",
            user_id, *center_ids, limit,
        )
    for row in rows:
        row["results"] = int(await db.fetchval("SELECT COUNT(*) FROM attempts WHERE session_code = ?", row["code"]) or 0)
    return rows


async def session_results(code: str) -> dict[str, Any]:
    entries = {
        row["user_id"]: row
        for row in await db.fetch(
            """SELECT session_entries.*, users.first_name, users.username FROM session_entries
               JOIN users ON users.id = session_entries.user_id WHERE code = ?""",
            code,
        )
    }
    rows = await db.fetch(
        """SELECT attempts.*, users.first_name, users.username FROM attempts
           JOIN users ON users.id = attempts.user_id
           WHERE session_code = ? ORDER BY created_at""",
        code,
    )
    # Older exams could hold several attempts per student. Only the first one counts.
    first_attempts = {}
    for row in rows:
        first_attempts.setdefault(row["user_id"], row)

    students = []
    domains: dict[str, dict[str, int]] = {}
    for user_id, row in first_attempts.items():
        report = json.loads(row["report"])
        entry = entries.get(user_id)
        seconds = entry["finished_at"] - entry["started_at"] if entry and entry["finished_at"] else row["duration_s"]
        students.append({
            "name": (entry and entry["full_name"]) or row["first_name"] or "—", "username": row["username"],
            "correct": row["correct"], "total": row["total"], "score": row["score"], "low": row["score_low"],
            "high": row["score_high"], "at": row["created_at"], "minutes": round(seconds / 60),
            "late": bool(entry and entry["late"]), "active": False,
            "seen": report.get("exposure", {}).get("seen", 0),
        })
        for part in report.get("domains", []):
            topic = domains.setdefault(part["domain"], {"correct": 0, "total": 0})
            topic["correct"] += part["correct"]
            topic["total"] += part["total"]
    students.sort(key=lambda student: (student["score"] is None, -(student["score"] or 0), student["at"]))
    for user_id, entry in entries.items():
        if user_id not in first_attempts:
            students.append({
                "name": entry["full_name"] or entry["first_name"] or "—", "username": entry["username"], "correct": None,
                "total": None, "score": None, "low": None, "high": None, "at": entry["started_at"],
                "minutes": round((now_ts() - entry["started_at"]) / 60), "late": False, "active": True, "seen": 0,
            })
    topics = sorted(
        ({"domain": name, **value} for name, value in domains.items()),
        key=lambda item: item["correct"] / item["total"] if item["total"] else 1,
    )
    scores = [student["score"] for student in students if student["score"] is not None]
    return {
        "students": students, "topics": topics, "count": len(first_attempts),
        "active": sum(student["active"] for student in students),
        "average": round(sum(scores) / len(scores), 1) if scores else None,
    }


async def session_csv(code: str) -> bytes:
    data = await session_results(code)
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["O'quvchi", "Username", "To'g'ri", "Jami", "Ball", "Oraliq", "Daqiqa", "Holat"])
    for student in data["students"]:
        if student["active"]:
            continue
        spread = f"{student['low']:.0f}-{student['high']:.0f}" if student["low"] is not None else ""
        score = "" if student["score"] is None else student["score"]
        writer.writerow([
            _safe_cell(student["name"]), _safe_cell(student["username"]), student["correct"], student["total"],
            score, spread, student["minutes"], "Kech topshirdi" if student["late"] else "Topshirdi",
        ])
    # The BOM makes Excel read Uzbek letters correctly.
    return ("﻿" + buffer.getvalue()).encode("utf-8")


def _safe_cell(value: str) -> str:
    """Stops spreadsheet programs from running a name that starts like a formula."""
    text = str(value or "")
    return "'" + text if text[:1] in ("=", "+", "-", "@") else text


async def platform_stats() -> dict[str, Any]:
    from database import shift_day, today

    day = today()
    return {
        "users": int(await db.fetchval("SELECT COUNT(*) FROM users") or 0),
        "started": int(await db.fetchval("SELECT COUNT(*) FROM users WHERE bot_started = 1") or 0),
        "active_today": int(await db.fetchval("SELECT COUNT(*) FROM users WHERE last_active_day = ?", day) or 0),
        "active_week": int(await db.fetchval(
            "SELECT COUNT(*) FROM users WHERE last_active_day >= ?", shift_day(day, -6)) or 0),
        "attempts_today": int(await db.fetchval("SELECT COUNT(*) FROM attempts WHERE day = ?", day) or 0),
        "mocks": int(await db.fetchval("SELECT COUNT(*) FROM attempts WHERE kind = 'sat_mock'") or 0),
        "essays_today": int(await db.fetchval("SELECT COUNT(*) FROM writing_submissions WHERE day = ?", day) or 0),
        "storage": db.kind,
    }
