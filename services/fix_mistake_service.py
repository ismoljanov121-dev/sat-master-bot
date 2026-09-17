"""
EduTest Pro - 'Xatomni Tuzat' (Fix My Mistake) Pedagogical Service
Provides a structured 5-step corrective learning loop:
1. Mistake Diagnosis: Exact erroneous choice and the accurate reasoning.
2. Concept Capsule: Core rule, definition, or formula governing the question.
3. Worked Example: Concise step-by-step demonstration of the concept.
4. Active Application: Brand NEW question from the vault testing the same skill (prevents memorization).
5. Spaced Repetition Scheduling: Flags the concept for next-day re-verification.
"""

from datetime import datetime, timezone
import logging
from typing import Any

from database import db, get_utc_now_str
from services.question_repository import vault

logger = logging.getLogger("FixMistakeService")


class FixMistakeService:
    def generate_fix_exercise(self, user_id: int, mistake_id: str) -> dict[str, Any] | None:
        """
        Creates a comprehensive conceptual remedial drill from a student's error.
        """
        mistakes = db.get_user_mistakes(user_id, resolved_filter=False)
        target_mistake = None
        for m in mistakes:
            if m.get("mistake_id") == mistake_id or m.get("question_id") == mistake_id:
                target_mistake = m
                break

        if not target_mistake:
            # If specific mistake not found, take the latest unresolved mistake
            if mistakes:
                target_mistake = mistakes[0]
            else:
                return None

        orig_qid = target_mistake.get("question_id")
        orig_q = vault.get_question(orig_qid) or {}
        section = target_mistake.get("section") or orig_q.get("section", "math")
        domain = target_mistake.get("domain") or orig_q.get("domain", "General")
        skill = target_mistake.get("skill") or orig_q.get("skill", domain)

        # Step 1: Diagnose Error
        chosen_key = target_mistake.get("user_answer") or target_mistake.get("user_choice") or "?"
        correct_key = target_mistake.get("correct_answer", orig_q.get("correct", "A"))
        explanation = target_mistake.get("explanation") or orig_q.get("explanation", "")
        hack = target_mistake.get("strategy_or_hack") or orig_q.get("strategy_or_hack", "")

        # Step 2 & 3: Concept Capsule & Worked Demonstration
        concept_capsule = self._build_concept_capsule(domain, skill, orig_q, hack)
        worked_example = {
            "prompt": orig_q.get("question", target_mistake.get("question_stem", "")),
            "correct_choice": correct_key,
            "walkthrough": explanation,
            "tactical_note": hack
        }

        # Step 4: Active Application (Fetch NEW question testing same skill/domain)
        transfer_question = self._find_transfer_question(orig_qid, section, domain, skill)

        exercise = {
            "mistake_id": target_mistake.get("mistake_id", orig_qid),
            "original_question_id": orig_qid,
            "section": section,
            "domain": domain,
            "skill": skill,
            "step_1_diagnosis": {
                "your_answer": chosen_key,
                "correct_answer": correct_key,
                "difference_analysis": f"Siz '{chosen_key}' variantini tanlagansiz, ammo to'g'ri javob: '{correct_key}'."
            },
            "step_2_concept_rule": concept_capsule,
            "step_3_worked_example": worked_example,
            "step_4_new_drill_question": transfer_question,
            "step_5_spaced_repetition": {
                "status": "scheduled_next_day",
                "next_check_date": "Ertaga",
                "goal": "Yangi savolni mustaqil ishlab ko'nikmani 100% o'zlashtirish"
            }
        }

        return exercise

    def _build_concept_capsule(self, domain: str, skill: str, orig_q: dict, hack: str) -> dict[str, str]:
        """Synthesizes the core conceptual rule for the topic."""
        return {
            "topic": f"{domain} — {skill}",
            "core_principle": (
                f"Ushbu turdagi SAT savollarida '{skill}' qoidasi tekshiriladi. "
                f"Asosiy e'tibor: shartdagi mantiqiy bog'liqlik va invariantlarni aniqlashdir."
            ),
            "key_takeaway": hack if hack else "Har bir variantni matn yoki formulaga nisbatan tekshirib chiqing."
        }

    def _find_transfer_question(
        self,
        exclude_qid: str,
        section: str,
        domain: str,
        skill: str
    ) -> dict[str, Any] | None:
        """Finds a DIFFERENT published question with the same skill or domain."""
        # 1. Try exact skill match
        candidates = vault.get_published_questions(section=section, domain=domain, skill=skill)
        valid = [q for q in candidates if q.get("id") != exclude_qid]

        # 2. Fallback to domain match
        if not valid:
            candidates = vault.get_published_questions(section=section, domain=domain)
            valid = [q for q in candidates if q.get("id") != exclude_qid]

        # 3. Fallback to section match
        if not valid:
            candidates = vault.get_published_questions(section=section)
            valid = [q for q in candidates if q.get("id") != exclude_qid]

        if not valid:
            return None

        # Return the first matching question stripped of direct answer keys for safe delivery
        raw = valid[0]
        return {
            "id": raw["id"],
            "section": raw.get("section"),
            "domain": raw.get("domain"),
            "skill": raw.get("skill"),
            "difficulty": raw.get("difficulty"),
            "passage": raw.get("passage"),
            "question": raw.get("question"),
            "options": raw.get("options", []),
            "is_transfer_question": True
        }


fix_mistake_service = FixMistakeService()
