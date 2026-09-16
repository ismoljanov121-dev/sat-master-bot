"""
EduTest Pro - Exam Service Engine
Manages ExamSession, Attempt State Machine, Deterministic Shuffling,
Timeout Enforcement, and Section/Domain Score Aggregation.
"""

import logging
import random
import string
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from config import CENTER_NAME
from services.question_service import qs

logger = logging.getLogger("ExamService")

# Tashkent Timezone (UTC+5) for reporting
TASHKENT_TZ = timezone(timedelta(hours=5))

# --- Exam Template Definitions ---
EXAM_TEMPLATES: dict[str, dict[str, Any]] = {
    "daily_10m": {
        "name": "daily_10m",
        "title": "Bugungi 10 daqiqalik mashq",
        "description": "6 ta savol / 10 daqiqa (2 Math, 2 Reading, 2 Writing)",
        "duration_seconds": 10 * 60,
        "section_quotas": {
            "reading": 2,
            "writing": 2,
            "math": 2
        },
        "is_official": False,
        "disclaimer": "Mustaqil Digital SAT mashqi. Bluebook formatidan ilhomlangan mustaqil tayyorgarlik vositasi."
    },
    "pilot_mock": {
        "name": "pilot_mock",
        "title": "Digital SAT Pilot Mock",
        "description": "18 ta savol / 25 daqiqa (6 Math, 6 Reading, 6 Writing)",
        "duration_seconds": 25 * 60,
        "section_quotas": {
            "reading": 6,
            "writing": 6,
            "math": 6
        },
        "is_official": False,
        "disclaimer": "Mustaqil Digital SAT Pilot Mock sinovi. Bluebook formatidan ilhomlangan mustaqil tayyorgarlik vositasi."
    },
    "demo_mock": {
        "name": "demo_mock",
        "title": "EduTest Digital SAT Mini Mock",
        "description": "12 ta savol / 15 daqiqa (4 Math, 4 Reading, 4 Writing)",
        "duration_seconds": 15 * 60,
        "section_quotas": {
            "math": 4,
            "reading": 4,
            "writing": 4
        },
        "is_official": False,
        "disclaimer": "Mustaqil Digital SAT mashqi. Bluebook formatidan ilhomlangan mustaqil tayyorgarlik vositasi."
    }
}


def check_template_pool_sufficiency(template_name: str) -> tuple[bool, str, dict[str, dict[str, int]]]:
    """
    Validates if the question bank contains enough verified questions for the template.
    Returns: (is_sufficient, message, stats_dict)
    """
    template = EXAM_TEMPLATES.get(template_name)
    if not template:
        return False, f"Noma'lum imtihon shabloni: {template_name}", {}

    quotas = template["section_quotas"]
    stats: dict[str, dict[str, int]] = {}
    is_sufficient = True
    missing_details = []

    for sec, required_count in quotas.items():
        available_questions = qs.get_questions_by_section(sec)
        avail_count = len(available_questions)
        stats[sec] = {"required": required_count, "available": avail_count}
        if avail_count < required_count:
            is_sufficient = False
            missing_details.append(f"{sec.title()}: talab {required_count} ta, mavjud {avail_count} ta")

    if not is_sufficient:
        msg = (
            "⚠️ <b>Savollar bazasi to'liq emas:</b>\n"
            + "\n".join(f"• {d}" for d in missing_details)
            + "\n\n<i>Halol sifat standarti: Baza sun'iy soxtalashtirilmaydi. "
            "Demo uchun 'Demo Mock (12 savol)' tavsiya etiladi.</i>"
        )
        return False, msg, stats

    return True, "Savollar bazasi to'liq va yetarli.", stats


def prepare_shuffled_questions(template_name: str, seed: int) -> list[dict[str, Any]]:
    """
    Selects questions according to quotas and performs deterministic shuffling
    of questions and options with correct answer key remapping.
    """
    template = EXAM_TEMPLATES.get(template_name, EXAM_TEMPLATES["demo_mock"])
    quotas = template["section_quotas"]
    rng = random.Random(seed)

    selected_raw: list[dict[str, Any]] = []
    for sec, count in quotas.items():
        pool = qs.get_questions_by_section(sec)
        if not pool:
            continue
        # Deterministically sample questions
        shuffled_pool = list(pool)
        rng.shuffle(shuffled_pool)
        selected_raw.extend(shuffled_pool[:count])

    # Shuffle the overall question order across sections
    rng.shuffle(selected_raw)

    prepared: list[dict[str, Any]] = []
    for q in selected_raw:
        orig_options = q.get("options", [])
        orig_correct = str(q.get("correct", "")).strip().upper()

        # Find original correct text
        correct_text = ""
        for opt in orig_options:
            if str(opt.get("key", "")).strip().upper() == orig_correct:
                correct_text = opt.get("text", "")
                break

        # Shuffle options copy
        shuffled_options_raw = list(orig_options)
        rng.shuffle(shuffled_options_raw)

        # Reassign keys A, B, C, D
        new_options: list[dict[str, str]] = []
        new_correct_key = "A"
        keys_pool = ["A", "B", "C", "D"]

        for idx, opt in enumerate(shuffled_options_raw):
            assigned_key = keys_pool[idx] if idx < len(keys_pool) else str(idx)
            new_options.append({
                "key": assigned_key,
                "text": opt.get("text", "")
            })
            if opt.get("text", "") == correct_text:
                new_correct_key = assigned_key

        prepared_q = {
            "id": q.get("id"),
            "section": q.get("section", "math"),
            "domain": q.get("domain", "General"),
            "difficulty": q.get("difficulty", "Medium"),
            "passage": q.get("passage"),
            "question": q.get("question", ""),
            "options": new_options,
            "correct": new_correct_key,
            "explanation": q.get("explanation", ""),
            "strategy_or_hack": q.get("strategy_or_hack", "")
        }
        prepared.append(prepared_q)

    return prepared


class ExamEngine:
    """Server-authoritative state manager for exam sessions and attempts."""

    @staticmethod
    def generate_join_code(prefix: str = "MARS", existing_codes: set[str] | None = None) -> str:
        """Generates an alphanumeric 6-character clean join code (e.g., MARS7K) guaranteeing uniqueness."""
        chars = string.ascii_uppercase + string.digits
        for _ in range(200):
            suffix = "".join(random.choices(chars, k=2))
            code = f"{prefix[:4].upper()}{suffix}"
            if existing_codes is None or code not in existing_codes:
                return code
        return f"{prefix[:4].upper()}{uuid.uuid4().hex[:2].upper()}"

    @staticmethod
    def create_attempt(
        user_id: int,
        template_name: str = "demo_mock",
        session_id: str | None = None,
        custom_seed: int | None = None,
        session_deadline: str | None = None
    ) -> dict[str, Any]:
        """Creates an authoritative exam attempt with strict server-side deadline and attempt nonce."""
        template = EXAM_TEMPLATES.get(template_name, EXAM_TEMPLATES["demo_mock"])
        duration = template["duration_seconds"]

        now_utc = datetime.now(timezone.utc)
        deadline_utc = now_utc + timedelta(seconds=duration)
        if session_deadline:
            try:
                s_dl = datetime.fromisoformat(session_deadline)
                if s_dl.tzinfo is None:
                    s_dl = s_dl.replace(tzinfo=timezone.utc)
                if s_dl < deadline_utc:
                    deadline_utc = s_dl
            except Exception as e:
                logger.warning(f"Failed to parse session_deadline {session_deadline}: {e}")

        seed = custom_seed if custom_seed is not None else int(now_utc.timestamp() * 1000) ^ user_id
        questions = prepare_shuffled_questions(template_name, seed)

        attempt_id = f"att_{uuid.uuid4().hex[:8]}"
        nonce = uuid.uuid4().hex[:6]

        attempt_data = {
            "attempt_id": attempt_id,
            "nonce": nonce,
            "user_id": user_id,
            "session_id": session_id,
            "template_name": template_name,
            "title": template["title"],
            "seed": seed,
            "total_questions": len(questions),
            "current_idx": 0,
            "questions": questions,
            "answers": {},  # str(idx) -> {"qid": str, "selected": str, "is_correct": bool, "answered_at": str}
            "start_time": now_utc.isoformat(),
            "deadline": deadline_utc.isoformat(),
            "status": "active",
            "score": None
        }
        return attempt_data

    @staticmethod
    def is_attempt_expired(attempt: dict[str, Any]) -> bool:
        """Checks if server deadline has passed."""
        if attempt.get("status") in ("submitted", "cancelled", "expired"):
            return True
        try:
            deadline = datetime.fromisoformat(attempt["deadline"])
            if deadline.tzinfo is None:
                deadline = deadline.replace(tzinfo=timezone.utc)
            now_utc = datetime.now(timezone.utc)
            return now_utc > deadline
        except Exception as e:
            logger.error(f"Error parsing deadline: {e}")
            return False

    @staticmethod
    def submit_answer(
        attempt: dict[str, Any],
        q_idx: int,
        selected_key: str,
        expected_nonce: str | None = None
    ) -> tuple[str, dict[str, Any]]:
        """
        Submits an answer with idempotency, nonce validation, and server deadline enforcement.
        Returns: (status_code, updated_attempt)
        status_codes: 'recorded', 'already_answered', 'expired', 'invalid_index', 'invalid_nonce'
        """
        if expected_nonce and attempt.get("nonce") != expected_nonce:
            return "invalid_nonce", attempt

        if ExamEngine.is_attempt_expired(attempt):
            attempt["status"] = "expired"
            ExamEngine.finalize_score(attempt)
            return "expired", attempt

        questions = attempt.get("questions", [])
        if q_idx < 0 or q_idx >= len(questions):
            return "invalid_index", attempt

        str_idx = str(q_idx)
        answers = attempt.setdefault("answers", {})

        # Idempotency check: if this question index was already answered,
        # ignore repeated taps to prevent double counting.
        if str_idx in answers:
            return "already_answered", attempt

        if q_idx != attempt.get("current_idx"):
            return "invalid_index", attempt

        target_q = questions[q_idx]
        correct_key = target_q.get("correct", "").strip().upper()
        selected_norm = selected_key.strip().upper()
        is_correct = (selected_norm == correct_key)

        answers[str_idx] = {
            "qid": target_q.get("id"),
            "section": target_q.get("section", "math"),
            "domain": target_q.get("domain", "General"),
            "selected": selected_norm,
            "correct": correct_key,
            "is_correct": is_correct,
            "answered_at": datetime.now(timezone.utc).isoformat()
        }

        # Advance current_idx
        if q_idx + 1 < len(questions):
            attempt["current_idx"] = q_idx + 1
        else:
            attempt["current_idx"] = q_idx

        # If all questions answered, finalize
        if len(answers) >= len(questions):
            attempt["status"] = "submitted"
            ExamEngine.finalize_score(attempt)
            return "recorded", attempt

        return "recorded", attempt

    @staticmethod
    def finalize_score(attempt: dict[str, Any]) -> dict[str, Any]:
        """Calculates section breakdown, accuracy percentage, and identifies weak domains."""
        questions = attempt.get("questions", [])
        answers = attempt.get("answers", {})
        total_q = len(questions)

        correct_count = 0
        by_section: dict[str, dict[str, int]] = {
            "math": {"total": 0, "correct": 0},
            "reading": {"total": 0, "correct": 0},
            "writing": {"total": 0, "correct": 0}
        }
        domain_errors: dict[str, int] = {}

        for idx, q in enumerate(questions):
            sec = q.get("section", "math").lower()
            domain = q.get("domain", "General")
            if sec not in by_section:
                by_section[sec] = {"total": 0, "correct": 0}
            by_section[sec]["total"] += 1

            ans_entry = answers.get(str(idx))
            if ans_entry and ans_entry.get("is_correct"):
                correct_count += 1
                by_section[sec]["correct"] += 1
            else:
                domain_errors[domain] = domain_errors.get(domain, 0) + 1

        accuracy = round((correct_count / total_q) * 100) if total_q > 0 else 0

        # Calculate pacing / time spent
        total_time_seconds = 0
        try:
            start_iso = attempt.get("start_time")
            if start_iso:
                start_dt = datetime.fromisoformat(start_iso)
                if start_dt.tzinfo is None:
                    start_dt = start_dt.replace(tzinfo=timezone.utc)
                total_time_seconds = max(int((datetime.now(timezone.utc) - start_dt).total_seconds()), 1)
        except Exception:
            total_time_seconds = 0

        avg_sec_per_q = round(total_time_seconds / len(answers), 1) if answers else 0.0

        # Sort weak domains
        sorted_weaknesses = [
            {"domain": dom, "errors": count}
            for dom, count in sorted(domain_errors.items(), key=lambda x: x[1], reverse=True)
            if count > 0
        ]

        attempt["score"] = {
            "total_questions": total_q,
            "answered_questions": len(answers),
            "correct_count": correct_count,
            "accuracy_percentage": accuracy,
            "total_time_seconds": total_time_seconds,
            "avg_seconds_per_question": avg_sec_per_q,
            "by_section": by_section,
            "weaknesses": sorted_weaknesses[:3],
            "submitted_at": datetime.now(timezone.utc).isoformat()
        }
        return attempt["score"]


exam_engine = ExamEngine()
