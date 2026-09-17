"""
EduTest Pro - Custom Test Builder Service
Enables students to configure custom practice sets by:
- Section (Math, Reading, Writing, Mixed)
- Domain and specific Skill
- Difficulty (Easy, Medium, Hard, All)
- Question Count (5, 10, 15, 20)
- Timer Mode (SAT Pacing vs Untimed Study)
Includes smart deduplication: prioritizing questions unattempted in the last 7 days.
"""

import random
import uuid
import logging
from typing import Any

from database import db
from services.question_repository import vault

logger = logging.getLogger("CustomTestService")


class CustomTestService:
    def build_custom_test(
        self,
        user_id: int,
        section: str = "all",
        domain: str = "all",
        skill: str = "all",
        difficulty: str = "All",
        count: int = 10,
        timed: bool = True
    ) -> dict[str, Any]:
        """
        Builds a customized test session ensuring fresh, unattempted questions where possible.
        """
        count = max(3, min(25, int(count)))

        # Fetch candidate questions from vault
        candidates = vault.get_published_questions(
            section=None if section in ("all", "mixed") else section,
            domain=None if domain == "all" else domain,
            skill=None if skill == "all" else skill,
            difficulty=None if difficulty == "All" else difficulty
        )

        if not candidates:
            # Fallback to broader section if narrow filter yielded 0 questions
            candidates = vault.get_published_questions(
                section=None if section in ("all", "mixed") else section
            )

        if not candidates:
            candidates = vault.get_published_questions()

        # Deduplication against last 7 days attempts
        recent_qids = db.get_user_recent_attempted_qids(user_id, days=7)
        unattempted = [q for q in candidates if q.get("id") not in recent_qids]

        if len(unattempted) >= count:
            selected_raw = random.sample(unattempted, count)
        else:
            # Take all unattempted, fill remaining with oldest attempted
            selected_raw = list(unattempted)
            remaining_needed = count - len(selected_raw)
            attempted = [q for q in candidates if q.get("id") in recent_qids]
            random.shuffle(attempted)
            selected_raw.extend(attempted[:remaining_needed])

        # If still less than count, duplicate pool with shuffle
        if len(selected_raw) < count and candidates:
            while len(selected_raw) < count:
                selected_raw.append(random.choice(candidates))

        # Format questions safely for test delivery (strip answers)
        safe_questions = []
        for idx, q in enumerate(selected_raw):
            safe_questions.append({
                "index": idx + 1,
                "id": q["id"],
                "section": q.get("section"),
                "domain": q.get("domain"),
                "skill": q.get("skill"),
                "difficulty": q.get("difficulty"),
                "passage": q.get("passage"),
                "question": q.get("question"),
                "options": q.get("options", []),
                "time_limit_seconds": 90 if q.get("section") == "math" else 75
            })

        # Calculate time budget
        total_seconds = sum(q["time_limit_seconds"] for q in safe_questions) if timed else 0
        session_id = f"custom_{uuid.uuid4().hex[:12]}"

        test_payload = {
            "session_id": session_id,
            "user_id": user_id,
            "mode": "custom_drill",
            "section": section,
            "domain": domain,
            "skill": skill,
            "difficulty": difficulty,
            "count": len(safe_questions),
            "timed": timed,
            "total_time_seconds": total_seconds,
            "questions": safe_questions,
            "fresh_question_ratio": f"{len(unattempted)}/{len(safe_questions)}"
        }

        return test_payload


custom_test_service = CustomTestService()
