"""
EduTest Pro - Handlers Integration Test Suite
Tests:
1. Admin access control (rejection for non-admins on command and callback)
2. Admin CSV export upload to Telegram (no undefined TASHKENT_TZ, document sent)
3. Admin recent results with section breakdown and session filtering
4. Diagnostic test callback idempotency (double-clicks guarded)
5. Exam engine callback answer idempotency, nonce check, and index check
6. Group mock session common deadline clamping
"""

import asyncio
import os
import sys
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aiogram.types import CallbackQuery, Chat, Message, User
from database import db, get_utc_now_str
from handlers.admin import (
    cb_admin_export_csv,
    cb_admin_recent_results,
    check_admin_access,
    cmd_admin,
)
from handlers.diagnostic import USER_SESSIONS, handle_answer
from handlers.exam import cb_select_answer, get_exam_question_keyboard
from services.exam_service import exam_engine


class TestHandlersIntegration(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.admin_id = 777111
        self.student_id = 888222
        # Ensure clean isolated state in local_cache for test users
        db.local_cache["users"] = {}
        db.local_cache["exam_attempts"] = {}
        db.local_cache["exam_sessions"] = {}
        db.local_cache["diagnostic_sessions"] = {}

        db.local_cache["users"][str(self.admin_id)] = {
            "user_id": self.admin_id,
            "full_name": "Admin Marstif",
            "username": "admin_marstif"
        }
        db.local_cache["users"][str(self.student_id)] = {
            "user_id": self.student_id,
            "full_name": "Student Kamron",
            "username": "kamron_sat"
        }

    # --- 1. Admin Access Control Rejection ---
    async def test_admin_access_rejection_for_non_admin(self):
        with patch("config.ADMIN_IDS", [self.admin_id]):
            # 1. Non-admin message
            fake_message = Message.model_construct(
                message_id=1,
                date=datetime.now(),
                chat=Chat.model_construct(id=self.student_id, type="private"),
                from_user=User.model_construct(id=self.student_id, is_bot=False, first_name="Kamron")
            )
            fake_message.__dict__["answer"] = AsyncMock()

            has_access_msg = await check_admin_access(fake_message)
            self.assertFalse(has_access_msg)
            fake_message.answer.assert_called_once()
            self.assertIn("taqiqlandi", fake_message.answer.call_args[0][0].lower())

            # 2. Non-admin callback
            fake_callback = CallbackQuery.model_construct(
                id="cb1",
                from_user=User.model_construct(id=self.student_id, is_bot=False, first_name="Kamron"),
                chat_instance="ci"
            )
            fake_callback.__dict__["answer"] = AsyncMock()

            has_access_cb = await check_admin_access(fake_callback)
            self.assertFalse(has_access_cb)
            fake_callback.answer.assert_called_once()
            self.assertIn("faqat administratorlar", fake_callback.answer.call_args[0][0].lower())

    # --- 2. Admin CSV Export Fix (Undefined TASHKENT_TZ resolved) ---
    async def test_admin_csv_export_sends_document(self):
        with patch("config.ADMIN_IDS", [self.admin_id]):
            # Seed an attempt
            db.local_cache["exam_attempts"]["att_csv_test"] = {
                "attempt_id": "att_csv_test",
                "user_id": self.student_id,
                "title": "EduTest Pro Demo Mock",
                "template_name": "demo_mock",
                "start_time": get_utc_now_str(),
                "status": "submitted",
                "score": {
                    "total_questions": 12,
                    "correct_count": 10,
                    "accuracy_percentage": 83,
                    "by_section": {
                        "math": {"total": 4, "correct": 4},
                        "reading": {"total": 4, "correct": 3},
                        "writing": {"total": 4, "correct": 3}
                    }
                }
            }

            fake_bot = MagicMock()
            fake_bot.send_document = AsyncMock()

            fake_message = Message.model_construct(
                message_id=2,
                date=datetime.now(),
                chat=Chat.model_construct(id=self.admin_id, type="private")
            )
            fake_message.__dict__["_bot"] = fake_bot

            fake_callback = CallbackQuery.model_construct(
                id="cb2",
                from_user=User.model_construct(id=self.admin_id, is_bot=False, first_name="Admin"),
                chat_instance="ci",
                message=fake_message
            )
            fake_callback.__dict__["answer"] = AsyncMock()

            # Calling cb_admin_export_csv must NOT raise NameError: TASHKENT_TZ
            await cb_admin_export_csv(fake_callback)

            fake_bot.send_document.assert_called_once()
            call_kwargs = fake_bot.send_document.call_args[1]
            self.assertEqual(call_kwargs["chat_id"], self.admin_id)
            doc = call_kwargs["document"]
            self.assertTrue(doc.filename.startswith("edutest_pro_results_"))
            self.assertTrue(doc.filename.endswith(".csv"))
            fake_callback.answer.assert_called_with("✅ CSV hisoboti yuborildi!")

    # --- 3. Admin Recent Results with Section Breakdown & Session Filter ---
    async def test_admin_recent_results_and_session_filter(self):
        with patch("config.ADMIN_IDS", [self.admin_id]):
            sess_id = "sess_filter_101"
            db.local_cache["exam_sessions"][sess_id] = {
                "session_id": sess_id,
                "code": "MARS88",
                "title": "EduTest Pro Demo Mock",
                "status": "active"
            }
            db.local_cache["exam_attempts"]["att_filt_1"] = {
                "attempt_id": "att_filt_1",
                "user_id": self.student_id,
                "session_id": sess_id,
                "template_name": "demo_mock",
                "start_time": get_utc_now_str(),
                "status": "submitted",
                "score": {
                    "total_questions": 12,
                    "correct_count": 11,
                    "accuracy_percentage": 92,
                    "by_section": {
                        "math": {"total": 4, "correct": 4},
                        "reading": {"total": 4, "correct": 4},
                        "writing": {"total": 4, "correct": 3}
                    },
                    "weaknesses": [{"domain": "Standard English Conventions", "errors": 1}]
                }
            }

            fake_callback = MagicMock()
            fake_callback.from_user.id = self.admin_id
            fake_callback.data = f"adm:sess_filter:{sess_id}"
            fake_callback.message.edit_text = AsyncMock()
            fake_callback.answer = AsyncMock()

            await cb_admin_recent_results(fake_callback)

            fake_callback.message.edit_text.assert_called_once()
            call_text = fake_callback.message.edit_text.call_args[0][0]
            self.assertIn("MARS88", call_text)
            self.assertIn("Student Kamron", call_text)
            self.assertIn("92%", call_text)
            self.assertIn("M: 4/4", call_text)
            self.assertIn("Standard English Conventions", call_text)

    # --- 4. Diagnostic Callback Idempotency ---
    async def test_diagnostic_double_click_idempotency(self):
        mock_questions = [
            {
                "id": "d1",
                "question": "Q1?",
                "options": [{"key": "A", "text": "1"}],
                "correct": "A",
                "topic": "Algebra",
                "trap": "Trap explanation",
                "explanation": "Classical solution"
            }
        ]
        with patch("handlers.diagnostic.QUESTIONS", mock_questions):
            USER_SESSIONS.pop(self.student_id, None)
            diag_session = {
                "current_idx": 0,
                "correct": 0,
                "incorrect_items": [],
                "answered_indices": []
            }
            db.local_cache["diagnostic_sessions"][str(self.student_id)] = diag_session

            fake_callback = MagicMock()
            fake_callback.from_user.id = self.student_id
            fake_callback.data = "ans_0_A"
            fake_callback.message.edit_text = AsyncMock()
            fake_callback.answer = AsyncMock()

            # First click
            await handle_answer(fake_callback)
            session_after_1 = db.local_cache["diagnostic_sessions"][str(self.student_id)]
            self.assertEqual(session_after_1["correct"], 1)
            self.assertIn(0, session_after_1["answered_indices"])

            # Second click on same question
            await handle_answer(fake_callback)
            session_after_2 = db.local_cache["diagnostic_sessions"][str(self.student_id)]
            self.assertEqual(session_after_2["correct"], 1, "Double click must not increment diagnostic score")

    # --- 5. Exam Engine Nonce Check & Callback Idempotency ---
    async def test_exam_nonce_check_and_answer_idempotency(self):
        attempt = exam_engine.create_attempt(user_id=self.student_id, template_name="demo_mock")
        nonce = attempt["nonce"]
        db.local_cache["exam_attempts"] = {attempt["attempt_id"]: attempt}

        # Case A: Mismatched nonce is rejected
        fake_cb_bad_nonce = MagicMock()
        fake_cb_bad_nonce.from_user.id = self.student_id
        fake_cb_bad_nonce.data = f"ex:a:wrong9:0:A"
        fake_cb_bad_nonce.answer = AsyncMock()
        fake_cb_bad_nonce.message.edit_text = AsyncMock()

        await cb_select_answer(fake_cb_bad_nonce)
        fake_cb_bad_nonce.answer.assert_called_with("⛔ Ushbu savol eski yoki boshqa imtihon sessiyasiga tegishli.", show_alert=True)
        self.assertEqual(len(attempt["answers"]), 0)

        # Case B: Valid nonce answer records successfully
        target_q = attempt["questions"][0]
        correct_key = target_q["correct"]

        fake_cb_valid = MagicMock()
        fake_cb_valid.from_user.id = self.student_id
        fake_cb_valid.data = f"ex:a:{nonce}:0:{correct_key}"
        fake_cb_valid.answer = AsyncMock()
        fake_cb_valid.message.edit_text = AsyncMock()

        await cb_select_answer(fake_cb_valid)
        self.assertEqual(len(attempt["answers"]), 1)
        self.assertEqual(attempt["current_idx"], 1)

        # Case C: Re-answering question index 0 is idempotent
        fake_cb_repeat = MagicMock()
        fake_cb_repeat.from_user.id = self.student_id
        fake_cb_repeat.data = f"ex:a:{nonce}:0:{correct_key}"
        fake_cb_repeat.answer = AsyncMock()
        fake_cb_repeat.message.edit_text = AsyncMock()

        await cb_select_answer(fake_cb_repeat)
        fake_cb_repeat.answer.assert_called_with("ℹ️ Ushbu savolga allaqachon javob berilgan.")
        self.assertEqual(len(attempt["answers"]), 1)

    # --- 6. Group Mock Session Common Deadline Clamping ---
    def test_group_session_common_deadline(self):
        now_utc = datetime.now(timezone.utc)
        # Session closes in 5 minutes (earlier than the 12-minute template duration)
        sess_deadline = (now_utc + timedelta(minutes=5)).isoformat()

        attempt = exam_engine.create_attempt(
            user_id=self.student_id,
            template_name="demo_mock",
            session_id="sess_group_1",
            session_deadline=sess_deadline
        )

        attempt_deadline = datetime.fromisoformat(attempt["deadline"])
        if attempt_deadline.tzinfo is None:
            attempt_deadline = attempt_deadline.replace(tzinfo=timezone.utc)

        # Attempt deadline should be bounded by session deadline (<= 5 min 5 sec)
        diff_seconds = (attempt_deadline - now_utc).total_seconds()
        self.assertLessEqual(diff_seconds, 305, "Student deadline must be clamped to session deadline")


if __name__ == "__main__":
    unittest.main()
