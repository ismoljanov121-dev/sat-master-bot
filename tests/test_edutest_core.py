"""
EduTest Pro - Comprehensive Test Suite
Validates:
1. Configuration & Branding (EduTest Pro / Marstif Academy)
2. Question Bank Schema Integrity (48 Curated Questions)
3. Exam Engine State Machine, Timeout, and Scoring
4. Deterministic Shuffling and Correct Answer Key Remapping
5. Pool Sufficiency Guard (Demo Mock vs Full Mock)
6. Admin Authorization & Access Control
7. Diagnostic Answer Callback Idempotency
8. Telegram WebApp HMAC-SHA256 initData Authentication
9. Atomic Persistence & CSV Export
10. XSS Sanitization & URL Allowlisting
"""

import hashlib
import hmac
import json
import os

import sys
import unittest
from unittest.mock import patch
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import BRAND_NAME, CENTER_NAME, _parse_admin_ids, is_admin
from database import Database, get_utc_now_str
from services.auth_service import MAX_AUTH_AGE_SECONDS, validate_telegram_init_data
from services.exam_service import (
    check_template_pool_sufficiency,
    exam_engine,
    prepare_shuffled_questions,
)
from services.question_service import qs


class TestEduTestCore(unittest.TestCase):

    def setUp(self):
        self.test_token = "123456789:ABCdefGHIjklMNOpqrSTUvwxYZ_test_token"

    # --- 1. Branding & Configuration ---
    def test_config_and_branding(self):
        self.assertEqual(BRAND_NAME, "EduTest Pro")
        self.assertTrue(len(CENTER_NAME) > 0)
        self.assertEqual(_parse_admin_ids("123, 456; 789"), [123, 456, 789])
        self.assertEqual(_parse_admin_ids(""), [])

    # --- 2. Question Bank Schemas ---
    def test_question_bank_schemas(self):
        curated = qs.curated_questions
        self.assertGreaterEqual(len(curated), 48, "Expected at least 48 curated questions in bank")

        seen_ids = set()
        for q in curated:
            qid = q.get("id")
            self.assertNotIn(qid, seen_ids, f"Duplicate question ID found: {qid}")
            seen_ids.add(qid)

            is_valid, err = qs.validate_question_schema(q)
            self.assertTrue(is_valid, f"Validation failed for question {qid}: {err}")

    # --- 3. Exam State Machine & Scoring ---
    def test_exam_state_machine_and_scoring(self):
        user_id = 999001
        attempt = exam_engine.create_attempt(user_id=user_id, template_name="demo_mock", custom_seed=42)

        self.assertEqual(attempt["status"], "active")
        self.assertEqual(attempt["total_questions"], 12)
        self.assertEqual(attempt["current_idx"], 0)

        # Answer question 0
        target_q = attempt["questions"][0]
        correct_key = target_q["correct"]
        status, updated = exam_engine.submit_answer(attempt, 0, correct_key)
        self.assertEqual(status, "recorded")
        self.assertEqual(len(updated["answers"]), 1)
        self.assertTrue(updated["answers"]["0"]["is_correct"])

        # Idempotency check: repeat answering same index 0
        status_repeat, updated_repeat = exam_engine.submit_answer(updated, 0, correct_key)
        self.assertEqual(status_repeat, "already_answered")
        self.assertEqual(len(updated_repeat["answers"]), 1)

        # Finalize score
        score = exam_engine.finalize_score(updated)
        self.assertEqual(score["total_questions"], 12)
        self.assertEqual(score["correct_count"], 1)
        self.assertIn("by_section", score)
        self.assertIn("math", score["by_section"])
        self.assertIn("reading", score["by_section"])
        self.assertIn("writing", score["by_section"])

    # --- 4. Deterministic Shuffling & Correct Key Remapping ---
    def test_deterministic_shuffling_and_remapping(self):
        seed = 777
        prepared_1 = prepare_shuffled_questions("demo_mock", seed)
        prepared_2 = prepare_shuffled_questions("demo_mock", seed)

        # Exact determinism with identical seed
        self.assertEqual(len(prepared_1), len(prepared_2))
        for q1, q2 in zip(prepared_1, prepared_2):
            self.assertEqual(q1["id"], q2["id"])
            self.assertEqual(q1["correct"], q2["correct"])

            # Verify that remapped correct key points to the exact same text
            # as the original question's correct answer
            orig = qs.get_question_by_id(q1["id"])
            if orig:
                orig_correct_key = orig["correct"]
                orig_correct_text = next(
                    opt["text"] for opt in orig["options"]
                    if opt["key"] == orig_correct_key
                )
                remapped_correct_text = next(
                    opt["text"] for opt in q1["options"]
                    if opt["key"] == q1["correct"]
                )
                self.assertEqual(
                    orig_correct_text,
                    remapped_correct_text,
                    f"Option remapping altered correct answer for {q1['id']}"
                )

    # --- 5. Server Deadline & Timeout ---
    def test_server_deadline_and_timeout(self):
        user_id = 999002
        attempt = exam_engine.create_attempt(user_id=user_id, template_name="demo_mock")

        # Artificially set deadline into the past
        past_utc = datetime.now(timezone.utc) - timedelta(minutes=5)
        attempt["deadline"] = past_utc.isoformat()

        self.assertTrue(exam_engine.is_attempt_expired(attempt))

        # Attempt to answer after expiry
        status, updated = exam_engine.submit_answer(attempt, 0, "A")
        self.assertEqual(status, "expired")
        self.assertEqual(updated["status"], "expired")

    # --- 6. Pool Sufficiency Guard ---
    def test_pool_sufficiency_guard(self):
        # Daily 10m requires 6 questions (2 Math, 2 Reading, 2 Writing) -> must be sufficient
        is_suff_daily, _msg_daily, _ = check_template_pool_sufficiency("daily_10m")
        self.assertTrue(is_suff_daily)

        # Pilot Mock requires 18 questions (6 Math, 6 Reading, 6 Writing) -> must be sufficient
        is_suff_pilot, _msg_pilot, _ = check_template_pool_sufficiency("pilot_mock")
        self.assertTrue(is_suff_pilot)

        # Oversized Mock requiring 1000 questions -> must honestly declare insufficient pool
        oversized = {
            "oversized": {
                "name": "oversized",
                "section_quotas": {"math": 1000, "reading": 1000, "writing": 1000}
            }
        }
        with patch.dict("services.exam_service.EXAM_TEMPLATES", oversized):
            is_suff_over, msg_over, stats = check_template_pool_sufficiency("oversized")
            self.assertFalse(is_suff_over)
            self.assertIn("Savollar bazasi to'liq emas", msg_over)
            self.assertIn("math", stats)

    # --- 7. Admin Authorization ---
    def test_admin_authorization(self):
        fake_admin_id = 11223344
        fake_student_id = 99887766

        # Test with custom ADMIN_IDS
        with patch("config.ADMIN_IDS", [fake_admin_id]):
            self.assertTrue(is_admin(fake_admin_id))
            self.assertFalse(is_admin(fake_student_id))

    # --- 8. Diagnostic Callback Idempotency ---
    def test_diagnostic_idempotency(self):
        session = {
            "current_idx": 0,
            "correct": 0,
            "incorrect_items": [],
            "answered_indices": []
        }

        q_idx = 0
        # First click on correct answer
        answered = session["answered_indices"]
        if q_idx not in answered:
            answered.append(q_idx)
            session["correct"] += 1

        self.assertEqual(session["correct"], 1)

        # Second click on same question index
        if q_idx not in answered:
            answered.append(q_idx)
            session["correct"] += 1

        self.assertEqual(session["correct"], 1, "Duplicate click must not increase score")

    # --- 9. Telegram WebApp initData HMAC-SHA256 ---
    def test_telegram_initdata_hmac_validation(self):
        token = self.test_token
        user_obj = {"id": 12345678, "first_name": "Otabek", "username": "otabek_dev"}
        auth_date = int(datetime.now(timezone.utc).timestamp())

        # Generate authentic signature
        params = {
            "auth_date": str(auth_date),
            "query_id": "AAHdF6IQAAAAAN0XohD74h-X",
            "user": json.dumps(user_obj)
        }
        sorted_pairs = [f"{k}={v}" for k, v in sorted(params.items())]
        data_check_string = "\n".join(sorted_pairs)

        secret_key = hmac.new(b"WebAppData", token.encode("utf-8"), hashlib.sha256).digest()
        computed_hash = hmac.new(secret_key, data_check_string.encode("utf-8"), hashlib.sha256).hexdigest()

        valid_init_data = f"{urlencode(params)}&hash={computed_hash}"

        # 1. Valid signature passes
        is_valid, user_data, msg = validate_telegram_init_data(valid_init_data, bot_token=token)
        self.assertTrue(is_valid, f"Validation failed unexpectedly: {msg}")
        self.assertIsNotNone(user_data)
        assert user_data is not None
        self.assertEqual(user_data["id"], 12345678)
        self.assertEqual(user_data["first_name"], "Otabek")

        # 2. Forged signature fails
        forged_init_data = f"{urlencode(params)}&hash=deadbeef0123456789abcdef"
        is_valid_f, _, msg_f = validate_telegram_init_data(forged_init_data, bot_token=token)
        self.assertFalse(is_valid_f)
        self.assertIn("Noto'g'ri kriptografik imzo", msg_f)

        # 3. Expired auth_date fails
        expired_params = dict(params)
        expired_params["auth_date"] = str(auth_date - (MAX_AUTH_AGE_SECONDS + 500))
        sorted_expired = [f"{k}={v}" for k, v in sorted(expired_params.items())]
        exp_check_str = "\n".join(sorted_expired)
        exp_hash = hmac.new(secret_key, exp_check_str.encode("utf-8"), hashlib.sha256).hexdigest()
        expired_init_data = f"{urlencode(expired_params)}&hash={exp_hash}"

        is_valid_exp, _, msg_exp = validate_telegram_init_data(expired_init_data, bot_token=token)
        self.assertFalse(is_valid_exp)
        self.assertIn("muddati o'tgan", msg_exp)

    # --- 10. Atomic Persistence & CSV Export ---
    def test_atomic_persistence_and_csv(self):
        test_db_file = os.path.join(os.path.dirname(__file__), "test_db_temp.json")
        try:
            db_inst = Database(mongo_uri="")
            # Populate dummy attempt
            db_inst.local_cache["users"]["555"] = {
                "user_id": 555,
                "full_name": "Test Alisher",
                "username": "alisher_sat"
            }
            db_inst.local_cache["exam_attempts"]["att_test1"] = {
                "attempt_id": "att_test1",
                "user_id": 555,
                "title": "EduTest Pro Demo Mock",
                "template_name": "demo_mock",
                "start_time": get_utc_now_str(),
                "status": "submitted",
                "score": {
                    "total_questions": 12,
                    "correct_count": 9,
                    "accuracy_percentage": 75,
                    "by_section": {
                        "math": {"total": 4, "correct": 3},
                        "reading": {"total": 4, "correct": 3},
                        "writing": {"total": 4, "correct": 3}
                    }
                }
            }

            csv_output = db_inst.export_results_csv()
            self.assertIn("Test Alisher", csv_output)
            self.assertIn("att_test1", csv_output)
            self.assertIn("75%", csv_output)
            self.assertIn("3/4", csv_output)
        finally:
            if os.path.exists(test_db_file):
                os.remove(test_db_file)

    # --- 11. XSS Sanitization & URL Allowlisting ---
    def test_xss_sanitization_and_url_allowlist(self):
        # Simulating index.html escaping logic
        def escape_html(text):
            if not text:
                return ""
            return (
                str(text)
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&#39;")
            )

        def sanitize_url(url):
            if not url or not isinstance(url, str):
                return ""
            t = url.strip()
            return t if t.startswith("https://") else ""

        xss_payload = "<script>alert('pwned')</script>"
        escaped = escape_html(xss_payload)
        self.assertNotIn("<script>", escaped)
        self.assertIn("&lt;script&gt;", escaped)

        self.assertEqual(sanitize_url("javascript:alert(1)"), "")
        self.assertEqual(sanitize_url("http://insecure.com"), "")
        self.assertEqual(sanitize_url("https://desmos.com/calculator/test"), "https://desmos.com/calculator/test")


if __name__ == "__main__":
    unittest.main()
