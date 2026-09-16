"""
Unit and Integration Tests for Student Flow:
- Honest Score Surgery & Diagnostic Tahlil
- Error Notebook (Xatolar Daftari) Persistence & Spaced-repetition Resolution
- Student Feedback Collection
- Exam Templates (Daily 10m & Pilot Mock) & Pacing Metrics
- Test Questions API Endpoint
- 3 P0 Paths in /start Navigation
"""

import asyncio
import os
import unittest
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from bot import setup_web_app
from database import db
from handlers.score_surgery import generate_surgery_report
from handlers.start import get_main_menu_keyboard
from services.exam_service import EXAM_TEMPLATES, exam_engine


class TestStudentFlow(unittest.TestCase):
    def setUp(self):
        self.user_id = 99881122
        # Clean test user from database cache
        str_id = str(self.user_id)
        if "error_notebook" in db.local_cache and str_id in db.local_cache["error_notebook"]:
            db.local_cache["error_notebook"].pop(str_id, None)

    # --- 1. Honest Score Surgery ---
    def test_score_surgery_honest_metrics(self):
        user_name = "Azizbek"
        total_q = 7
        correct_q = 5
        incorrect_items = [
            {"topic": "Linear Equations", "points_lost": 20},
            {"topic": "Quadratic & Parabola", "points_lost": 20}
        ]

        report = generate_surgery_report(user_name, total_q, correct_q, incorrect_items)

        # Must include accuracy percentage (71%)
        self.assertIn("71%", report)
        self.assertIn("5 / 7 ta to'g'ri", report)
        self.assertIn("Linear Equations", report)
        self.assertIn("Quadratic &amp; Parabola", report)

        # Must NOT contain misleading 800 score claims or 1-day promises
        self.assertNotIn("/ 800", report)
        self.assertNotIn("1 KUNDA +", report)
        self.assertNotIn("Taxminiy Math Ballingiz", report)

        # Must have educational advice and disclaimer
        self.assertIn("FOYDALI TAVSIYALAR", report)
        self.assertIn("rasmiy SAT balli emas", report)

    # --- 2. Error Notebook CRUD & Resolution ---
    def test_error_notebook_workflow(self):
        async def run_flow():
            # Initially no mistakes
            count = db.get_unresolved_mistakes_count(self.user_id)
            self.assertEqual(count, 0)

            # Record a mistake
            await db.record_mistake(
                user_id=self.user_id,
                question_id="test_q1",
                section="math",
                domain="Heart of Algebra",
                question_text="If 2x + 4 = 10, what is x?",
                correct_answer="C",
                user_answer="A",
                explanation="2x = 6 => x = 3",
                hack="Desmos 2x + 4 = 10 chizing"
            )

            # Check unresolved mistakes
            unresolved = db.get_user_mistakes(self.user_id, resolved_filter=False)
            self.assertEqual(len(unresolved), 1)
            self.assertEqual(unresolved[0]["question_id"], "test_q1")
            self.assertFalse(unresolved[0]["resolved"])
            self.assertEqual(db.get_unresolved_mistakes_count(self.user_id), 1)

            # Record another mistake
            await db.record_mistake(
                user_id=self.user_id,
                question_id="test_q2",
                section="reading",
                domain="Craft and Structure",
                question_text="Sample reading question stem...",
                correct_answer="B",
                user_answer="D",
                explanation="Sample explanation"
            )
            self.assertEqual(db.get_unresolved_mistakes_count(self.user_id), 2)

            # Resolve first mistake
            resolved_ok = await db.resolve_mistake(self.user_id, "test_q1")
            self.assertTrue(resolved_ok)
            self.assertEqual(db.get_unresolved_mistakes_count(self.user_id), 1)

            # Verify resolved mistake filter
            resolved_list = db.get_user_mistakes(self.user_id, resolved_filter=True)
            self.assertEqual(len(resolved_list), 1)
            self.assertEqual(resolved_list[0]["question_id"], "test_q1")
            self.assertTrue(resolved_list[0]["resolved"])
            self.assertIsNotNone(resolved_list[0]["resolved_at"])

        asyncio.run(run_flow())

    # --- 3. Student Feedback Storage ---
    def test_student_feedback_collection(self):
        async def run_feedback():
            initial_count = len(db.get_all_feedback())
            entry = await db.save_student_feedback(
                user_id=self.user_id,
                username="test_student",
                full_name="Test Student",
                feedback_text="Mini App test runner interfeysi juda qulay bo'libdi!",
                category="ui_praise"
            )
            self.assertIn("id", entry)
            self.assertEqual(entry["user_id"], self.user_id)
            self.assertEqual(len(db.get_all_feedback()), initial_count + 1)

        asyncio.run(run_feedback())

    # --- 4. Exam Service Templates & Pacing ---
    def test_exam_templates_and_pacing(self):
        # Verify daily_10m exists and has honest quotas
        self.assertIn("daily_10m", EXAM_TEMPLATES)
        self.assertEqual(EXAM_TEMPLATES["daily_10m"]["duration_seconds"], 600)
        self.assertEqual(sum(EXAM_TEMPLATES["daily_10m"]["section_quotas"].values()), 6)
        self.assertFalse(EXAM_TEMPLATES["daily_10m"]["is_official"])

        # Verify pilot_mock exists
        self.assertIn("pilot_mock", EXAM_TEMPLATES)
        self.assertEqual(EXAM_TEMPLATES["pilot_mock"]["duration_seconds"], 1500)
        self.assertEqual(sum(EXAM_TEMPLATES["pilot_mock"]["section_quotas"].values()), 18)
        self.assertFalse(EXAM_TEMPLATES["pilot_mock"]["is_official"])

        # Create attempt and verify pacing calculation in finalize_score
        attempt = exam_engine.create_attempt(user_id=self.user_id, template_name="daily_10m")
        self.assertEqual(len(attempt["questions"]), 6)

        # Submit all answers
        for idx in range(len(attempt["questions"])):
            target_q = attempt["questions"][idx]
            exam_engine.submit_answer(attempt, idx, target_q["correct"], expected_nonce=attempt["nonce"])

        score = attempt.get("score", {})
        self.assertEqual(score["correct_count"], 6)
        self.assertEqual(score["accuracy_percentage"], 100)
        self.assertIn("avg_seconds_per_question", score)
        self.assertIn("total_time_seconds", score)

    # --- 5. Main Menu Keyboard 3 P0 Paths ---
    def test_start_menu_keyboard_paths(self):
        # Clean user (0 mistakes)
        kb = get_main_menu_keyboard(self.user_id)
        btn_texts = [b.text for row in kb.inline_keyboard for b in row]

        # Must have the 3 clear paths:
        self.assertTrue(any("Darajamni bilish" in t for t in btn_texts))
        self.assertTrue(any("Bugungi 10 daqiqalik mashq" in t for t in btn_texts))
        self.assertTrue(any("Xatolarim daftari" in t for t in btn_texts))

        # Test with 3 unresolved mistakes -> badge should display (3)
        async def mock_mistakes():
            for i in range(3):
                await db.record_mistake(
                    user_id=self.user_id,
                    question_id=f"m_{i}",
                    section="math",
                    domain="Algebra",
                    question_text=f"Sample {i}",
                    correct_answer="A",
                    user_answer="B",
                    explanation="exp"
                )
        asyncio.run(mock_mistakes())

        kb_with_mistakes = get_main_menu_keyboard(self.user_id)
        btn_texts_m = [b.text for row in kb_with_mistakes.inline_keyboard for b in row]
        self.assertTrue(any("Xatolarim daftari (3)" in t for t in btn_texts_m))


class TestTestQuestionsApi(AioHTTPTestCase):
    async def get_application(self):
        return setup_web_app()

    @unittest_run_loop
    async def test_get_daily_questions(self):
        resp = await self.client.get("/api/v1/test/questions?mode=daily_10m")
        self.assertEqual(resp.status, 200)
        data = await resp.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["mode"], "daily_10m")
        self.assertEqual(len(data["questions"]), 6)

    @unittest_run_loop
    async def test_get_pilot_mock_questions(self):
        resp = await self.client.get("/api/v1/test/questions?mode=pilot_mock")
        self.assertEqual(resp.status, 200)
        data = await resp.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["mode"], "pilot_mock")
        self.assertEqual(len(data["questions"]), 18)

    @unittest_run_loop
    async def test_get_diagnostic_questions(self):
        resp = await self.client.get("/api/v1/test/questions?mode=diagnostic")
        self.assertEqual(resp.status, 200)
        data = await resp.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["mode"], "diagnostic")
        self.assertEqual(len(data["questions"]), 7)

    @unittest_run_loop
    async def test_get_full_mock_questions(self):
        resp = await self.client.get("/api/v1/test/questions?mode=full_mock")
        self.assertEqual(resp.status, 200)
        data = await resp.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["mode"], "full_mock")
        self.assertEqual(len(data["questions"]), 98)
        self.assertEqual(data["duration_seconds"], 134 * 60)


if __name__ == "__main__":
    unittest.main()
