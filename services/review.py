"""
Mistake notebook with spaced repetition, and question picking for practice sets.

A wrong answer comes back after 1 day. Correct reviews move it to 3 days, then 7 days, then it is resolved.
"""

import random
from typing import Any, Optional

from database import db, now_ts, shift_day, today
from services.content import content

INTERVALS = (1, 3, 7)


async def apply_results(user_id: int, results: list[tuple[str, bool, str]]) -> None:
    """Updates the notebook from (question_id, correct, chosen) rows."""
    if not results:
        return
    ids = [row[0] for row in results]
    marks = ", ".join("?" for _ in ids)
    existing = {
        row["question_id"]: row
        for row in await db.fetch(
            f"SELECT * FROM review_items WHERE user_id = ? AND question_id IN ({marks})", user_id, *ids
        )
    }
    day, now = today(), now_ts()
    updates = []
    for question_id, correct, chosen in results:
        row = existing.get(question_id)
        if correct:
            if row is None or row["resolved"]:
                continue
            box = row["box"] + 1
            resolved = int(box >= len(INTERVALS))
            due = day if resolved else shift_day(day, INTERVALS[box])
            updates.append((user_id, question_id, box, due, row["wrong_count"], resolved, chosen, now))
        else:
            wrong_count = row["wrong_count"] + 1 if row else 1
            updates.append((user_id, question_id, 0, shift_day(day, INTERVALS[0]), wrong_count, 0, chosen, now))
    await db.executemany(
        """INSERT INTO review_items (user_id, question_id, box, due_day, wrong_count, resolved, last_chosen, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT (user_id, question_id) DO UPDATE SET
               box = excluded.box, due_day = excluded.due_day, wrong_count = excluded.wrong_count,
               resolved = excluded.resolved, last_chosen = excluded.last_chosen, updated_at = excluded.updated_at""",
        updates,
    )


async def due_count(user_id: int) -> int:
    value = await db.fetchval(
        "SELECT COUNT(*) FROM review_items WHERE user_id = ? AND resolved = 0 AND due_day <= ?", user_id, today()
    )
    return int(value or 0)


async def notebook(user_id: int) -> dict[str, Any]:
    rows = await db.fetch(
        """SELECT question_id, box, due_day, wrong_count, last_chosen, resolved FROM review_items
           WHERE user_id = ? ORDER BY resolved, due_day, wrong_count DESC""",
        user_id,
    )
    day = today()
    open_rows = [row for row in rows if not row["resolved"] and row["question_id"] in content.bank]
    return {
        "due": [row["question_id"] for row in open_rows if row["due_day"] <= day],
        "items": [
            {"q": row["question_id"], "box": row["box"], "due": row["due_day"],
             "wrong": row["wrong_count"], "chosen": row["last_chosen"]}
            for row in open_rows
        ],
        "resolved": sum(1 for row in rows if row["resolved"]),
    }


async def pick_questions(
    user_id: int,
    section: Optional[str] = None,
    domain: Optional[str] = None,
    difficulty: Optional[str] = None,
    count: int = 10,
) -> list[str]:
    """Unseen questions come first, and among those the ones no mock uses, so mocks stay fresh."""
    rows = await db.fetch(
        "SELECT question_id, MAX(created_at) AS last_seen FROM answers WHERE user_id = ? GROUP BY question_id", user_id
    )
    seen = {row["question_id"]: row["last_seen"] for row in rows}
    pool = [
        q for q in content.bank.values()
        if (section is None or q["sec"] == section)
        and (domain is None or q["dom"] == domain)
        and (difficulty is None or q["dif"] == difficulty)
    ]
    random.shuffle(pool)
    pool.sort(key=lambda q: (q["id"] in seen, 0 if q.get("free") else 1, seen.get(q["id"], 0)))
    return [q["id"] for q in pool[:count]]
