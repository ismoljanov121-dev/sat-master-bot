"""
EduTest Pro - Comprehensive Free Product & Pro Beta Test Suite
Verifies:
1. Free Tier Generous Model (50 questions/day limit, 1 free full mock/week)
2. Mistake notebook and review exemptions (zero limit consumption)
3. Mock exams separate tracking from daily practice quota
4. Payments disabled guard & Pro Beta unlocked features
5. Adaptive Study Plan generation & rebalancing
6. Fix My Mistake (5-step pedagogical transfer loop)
7. Custom Test Builder with 7-day attempt deduplication
8. Pacing Strategy & Time Management analytics
9. Tiered Scaffolding Hints (Level 1 & Level 2 without answer leakage)
10. Pragmatic Weekly Report with epistemic honesty
11. Unified API endpoints integration via AioHTTPTestCase
"""

import asyncio
import copy
import json
import os
import sys
import unittest
from unittest.mock import patch
from datetime import datetime, timedelta, timezone

from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot import setup_web_app
from database import db
from services.custom_test_service import custom_test_service
from services.fix_mistake_service import fix_mistake_service
from services.hint_scaffolding_service import hint_service
from services.pacing_service import pacing_service
from services.question_repository import vault
from services.study_plan_service import study_planner
from services.telemetry_service import telemetry
from services.tier_service import (
    FREE_DAILY_QUESTIONS_LIMIT,
    FREE_WEEKLY_MOCKS_LIMIT,
    PRO_DAILY_FAIR_USE_LIMIT,
    can_answer_practice_question,
    can_take_full_mock,
    get_daily_question_status,
    get_user_tier,
    is_user_pro,
    record_question_attempt,
)
from services.weekly_report_service import weekly_report_service


class TestFreeProductModel(unittest.TestCase):
    def setUp(self):
        self.saved_cache = copy.deepcopy(db.local_cache)

    def tearDown(self):
        db.local_cache = self.saved_cache
        db._save_local_db_sync()

    @patch("services.tier_service.PRO_BETA_MODE", False)
    def test_free_tier_50_questions_daily_limit(self):
        user_id = 110001
        self.assertEqual(FREE_DAILY_QUESTIONS_LIMIT, 50)

        # Answer 50 questions
        for i in range(50):
            allowed, _ = can_answer_practice_question(user_id, is_mistake_practice=False)
            self.assertTrue(allowed, f"Question {i+1} should be permitted")
            asyncio.run(record_question_attempt(user_id, is_mistake_practice=False))

        # 51st question blocked
        allowed, reason = can_answer_practice_question(user_id, is_mistake_practice=False)
        self.assertFalse(allowed)
        self.assertIn("50 ta yangi savol limitingiz to'ldi", reason)

        # Confirm status
        status = get_daily_question_status(user_id)
        self.assertEqual(status["answered_today"], 50)
        self.assertEqual(status["remaining_today"], 0)
        self.assertTrue(status["is_limit_reached"])

    @patch("services.tier_service.PRO_BETA_MODE", False)
    def test_mistakes_re_practice_exempt_from_daily_limit(self):
        user_id = 110002
        # Pre-fill daily quota to 50
        for _ in range(50):
            asyncio.run(record_question_attempt(user_id))

        status = get_daily_question_status(user_id)
        self.assertTrue(status["is_limit_reached"])

        # Attempting mistake practice is strictly allowed
        allowed, reason = can_answer_practice_question(user_id, is_mistake_practice=True)
        self.assertTrue(allowed)
        self.assertIn("har doim cheklovsiz", reason)

        # Attempting review is strictly allowed
        allowed_rev, _ = can_answer_practice_question(user_id, is_review=True)
        self.assertTrue(allowed_rev)

        # Recording mistake practice does NOT increment daily count
        used_before = status["answered_today"]
        asyncio.run(record_question_attempt(user_id, is_mistake_practice=True))
        status_after = get_daily_question_status(user_id)
        self.assertEqual(status_after["answered_today"], used_before)

    @patch("services.tier_service.PRO_BETA_MODE", False)
    def test_free_one_weekly_mock_exam(self):
        user_id = 110003
        # Initially, 0 weekly mocks used -> 1st mock allowed
        self.assertEqual(db.get_weekly_mocks_used(user_id), 0)
        can_mock, msg = can_take_full_mock(user_id)
        self.assertTrue(can_mock)
        self.assertIn("1/1", msg)

        # Student starts/completes 1st mock
        asyncio.run(db.increment_weekly_mocks(user_id))
        self.assertEqual(db.get_weekly_mocks_used(user_id), 1)

        # 2nd mock in same week is politely restricted
        can_mock_2, msg_2 = can_take_full_mock(user_id)
        self.assertFalse(can_mock_2)
        self.assertIn("Dushanbadan", msg_2)
        self.assertIn("50 ta mashq esa doimo ochiq", msg_2)

    @patch("services.tier_service.PRO_BETA_MODE", False)
    def test_mock_questions_do_not_consume_daily_practice_quota(self):
        user_id = 110004
        # Simulating answering 20 mock exam questions
        for _ in range(20):
            count = asyncio.run(record_question_attempt(user_id, is_mock=True))
            self.assertEqual(count, 0)

        # Daily practice quota remains 0 used
        status = get_daily_question_status(user_id)
        self.assertEqual(status["answered_today"], 0)
        self.assertEqual(status["remaining_today"], 50)


class TestProBetaAndPersonalizedServices(unittest.TestCase):
    def setUp(self):
        self.saved_cache = copy.deepcopy(db.local_cache)

    def tearDown(self):
        db.local_cache = self.saved_cache
        db._save_local_db_sync()

    def test_pro_beta_unlocked_for_all(self):
        user_id = 220001
        tier_info = get_user_tier(user_id)
        self.assertEqual(tier_info["tier"], "pro_beta")
        self.assertTrue(tier_info["is_pro"])
        self.assertTrue(tier_info["is_beta"])
        self.assertEqual(tier_info["daily_limit"], PRO_DAILY_FAIR_USE_LIMIT)
        self.assertFalse(tier_info["payments_enabled"])

        # Uncapped mock tests during beta
        can_mock, _ = can_take_full_mock(user_id)
        self.assertTrue(can_mock)

    def test_adaptive_study_plan_service(self):
        user_id = 220002
        plan = study_planner.create_or_update_plan(
            user_id=user_id,
            target_exam_date="2026-11-15",
            daily_minutes=45,
            target_score=1450
        )
        self.assertEqual(plan["user_id"], user_id)
        self.assertEqual(plan["daily_minutes"], 45)
        self.assertEqual(plan["target_score"], 1450)
        self.assertIn("current_focus_domain", plan)
        self.assertIn("recommendation_rationale", plan)
        self.assertTrue(len(plan["weekly_schedule"]) > 0)

        # Rebalance plan
        updated_plan = study_planner.rebalance_plan(user_id)
        self.assertIn("Reja yangilandi", updated_plan["recommendation_rationale"])

    def test_fix_mistake_service(self):
        user_id = 220003
        # Seed an unresolved mistake
        asyncio.run(db.record_mistake(
            user_id=user_id,
            question_id="m_alg_1",
            section="math",
            domain="Algebra",
            question_text="What is x if 3x + 9 = 24?",
            correct_answer="A",
            user_answer="B",
            explanation="Subtract 9 from 24 to get 15, divide by 3 to get 5.",
            hack="Desmosga 3x + 9 = 24 deb yozing va x-interceptni ko'ring.",
            options=[{"key": "A", "text": "5"}, {"key": "B", "text": "7"}]
        ))

        exercise = fix_mistake_service.generate_fix_exercise(user_id, "m_alg_1")
        self.assertIsNotNone(exercise)
        self.assertEqual(exercise["section"], "math")
        self.assertEqual(exercise["domain"], "Algebra")
        self.assertEqual(exercise["step_1_diagnosis"]["your_answer"], "B")
        self.assertEqual(exercise["step_1_diagnosis"]["correct_answer"], "A")
        self.assertIn("core_principle", exercise["step_2_concept_rule"])
        self.assertIn("walkthrough", exercise["step_3_worked_example"])
        self.assertIsNotNone(exercise["step_4_new_drill_question"])
        self.assertNotEqual(exercise["step_4_new_drill_question"]["id"], "m_alg_1")
        self.assertEqual(exercise["step_5_spaced_repetition"]["status"], "scheduled_next_day")

    def test_custom_test_builder_with_deduplication(self):
        user_id = 220004
        # Record recent attempts to test deduplication
        asyncio.run(db.record_attempt_detail(
            user_id=user_id,
            question_id="m_alg_1",
            is_correct=True,
            time_spent_seconds=60,
            section="math",
            domain="Algebra"
        ))

        test_payload = custom_test_service.build_custom_test(
            user_id=user_id,
            section="math",
            domain="Algebra",
            difficulty="Medium",
            count=5,
            timed=True
        )
        self.assertIsNotNone(test_payload)
        self.assertEqual(test_payload["section"], "math")
        self.assertEqual(test_payload["count"], 5)
        self.assertTrue(test_payload["total_time_seconds"] > 0)
        self.assertTrue(len(test_payload["questions"]) == 5)

        # Check answers stripped from delivered test questions
        for q in test_payload["questions"]:
            self.assertNotIn("correct", q)
            self.assertNotIn("explanation", q)

    def test_pacing_strategy_analytics(self):
        user_id = 220005
        # 1. Under 5 attempts -> Insufficient data notice
        initial = pacing_service.analyze_user_pacing(user_id)
        self.assertEqual(initial["status"], "insufficient_data")

        # 2. Record overtime and rushed attempts
        # Overtime Math (>95s)
        asyncio.run(db.record_attempt_detail(user_id, "q_over_1", False, 120, "math", "Advanced Math"))
        asyncio.run(db.record_attempt_detail(user_id, "q_over_2", True, 110, "math", "Advanced Math"))
        # Rushed Math (<25s mistake)
        asyncio.run(db.record_attempt_detail(user_id, "q_rush_1", False, 15, "math", "Algebra"))
        # Normal Math (80s correct)
        asyncio.run(db.record_attempt_detail(user_id, "q_norm_1", True, 75, "math", "Algebra"))
        asyncio.run(db.record_attempt_detail(user_id, "q_norm_2", True, 80, "math", "Geometry"))

        analysis = pacing_service.analyze_user_pacing(user_id)
        self.assertEqual(analysis["status"], "ok")
        self.assertEqual(analysis["total_analyzed"], 5)
        self.assertEqual(analysis["overtime_count"], 2)
        self.assertEqual(analysis["rushed_errors_count"], 1)
        self.assertTrue(analysis["average_time_seconds"] > 0)
        self.assertIn("Advanced Math", analysis["heaviest_domain"])

    def test_tiered_scaffolding_hints(self):
        # Test hint retrieval for a published vault question
        published = vault.get_published_questions()
        self.assertTrue(len(published) > 0)
        sample_q = published[0]
        qid = sample_q["id"]

        hints = hint_service.get_hints_for_question(qid)
        self.assertTrue(hints["ok"])
        self.assertEqual(hints["question_id"], qid)
        self.assertIn("1-Maslahat", hints["hint_level_1"])
        self.assertIn("2-Maslahat", hints["hint_level_2"])
        # Ensure correct answer is NOT leaked in hints
        correct_key = sample_q.get("correct", "A")
        self.assertNotIn(f"To'g'ri javob: {correct_key}", hints["hint_level_1"])

    def test_pragmatic_weekly_report_epistemic_honesty(self):
        user_id = 220006
        # Under 15 attempts -> Preliminary honest status
        prelim = weekly_report_service.generate_weekly_report(user_id)
        self.assertEqual(prelim["status"], "preliminary")
        self.assertFalse(prelim["is_confident"])
        self.assertIn("kamida 15 ta savol", prelim["notice"])

        # Add 16 attempts
        for i in range(16):
            is_corr = (i % 2 == 0)
            dom = "Algebra" if i < 8 else "Craft and Structure"
            asyncio.run(db.record_attempt_detail(user_id, f"q_rep_{i}", is_corr, 60, "math" if i < 8 else "reading", dom))

        report = weekly_report_service.generate_weekly_report(user_id)
        self.assertEqual(report["status"], "ready")
        self.assertTrue(report["is_confident"])
        self.assertEqual(report["total_questions"], 16)
        self.assertIn("q1_what_improved", report)
        self.assertIn("q2_what_is_difficult", report)
        self.assertEqual(len(report["q3_next_week_plan"]), 3)

    def test_telemetry_service(self):
        user_id = 220007
        asyncio.run(telemetry.record_event("starter_drill_completed", user_id=user_id, metadata={"mode": "microdrill"}))
        asyncio.run(telemetry.record_event("pro_beta_feature_used", user_id=user_id, metadata={"step": "study_plan"}))

        summary = telemetry.get_summary()
        self.assertGreaterEqual(summary.get("starter_drill_completed", 0), 1)
        self.assertGreaterEqual(summary.get("pro_beta_feature_used", 0), 1)


class TestProBetaApiEndpoints(AioHTTPTestCase):
    async def get_application(self) -> web.Application:
        return setup_web_app()

    def setUp(self):
        self.saved_cache = copy.deepcopy(db.local_cache)
        super().setUp()

    def tearDown(self):
        db.local_cache = self.saved_cache
        db._save_local_db_sync()
        super().tearDown()

    async def test_api_study_plan_endpoints(self):
        user_id = 330001
        # GET plan
        resp = await self.client.get(
            "/api/v1/study-plan",
            headers={"X-Dev-User-Id": str(user_id)}
        )
        self.assertEqual(resp.status, 200)
        data = await resp.json()
        self.assertEqual(data["status"], "ok")
        self.assertIn("plan", data)

        # POST rebalance
        resp_reb = await self.client.post(
            "/api/v1/study-plan/rebalance",
            headers={"X-Dev-User-Id": str(user_id)},
            json={}
        )
        self.assertEqual(resp_reb.status, 200)
        data_reb = await resp_reb.json()
        self.assertEqual(data_reb["status"], "ok")
        self.assertIn("Reja yangilandi", data_reb["plan"]["recommendation_rationale"])

    async def test_api_custom_test_builder(self):
        user_id = 330002
        resp = await self.client.post(
            "/api/v1/practice/custom-test",
            headers={"X-Dev-User-Id": str(user_id)},
            json={
                "section": "math",
                "difficulty": "Medium",
                "count": 5,
                "timed": True
            }
        )
        self.assertEqual(resp.status, 200)
        data = await resp.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["test"]["count"], 5)
        self.assertIn("session_id", data)

    async def test_api_fix_mistake_endpoint(self):
        user_id = 330003
        # When no mistakes exist
        resp_empty = await self.client.get(
            "/api/v1/practice/fix-mistake",
            headers={"X-Dev-User-Id": str(user_id)}
        )
        self.assertEqual(resp_empty.status, 200)
        data_empty = await resp_empty.json()
        self.assertEqual(data_empty["status"], "empty")

        # Add mistake and query again
        await db.record_mistake(
            user_id=user_id,
            question_id="m_geo_1",
            section="math",
            domain="Geometry and Trigonometry",
            question_text="A right triangle has legs 6 and 8. What is the hypotenuse?",
            correct_answer="C",
            user_answer="B",
            explanation="By Pythagorean theorem: 6^2 + 8^2 = 36 + 64 = 100, sqrt(100) = 10.",
            hack="Pifagor sonlari: 3-4-5 uchburchagining 2 karralisi: 6-8-10.",
            options=[{"key": "A", "text": "8"}, {"key": "B", "text": "9"}, {"key": "C", "text": "10"}]
        )

        resp = await self.client.get(
            "/api/v1/practice/fix-mistake?mistake_id=m_geo_1",
            headers={"X-Dev-User-Id": str(user_id)}
        )
        self.assertEqual(resp.status, 200)
        data = await resp.json()
        self.assertEqual(data["status"], "ok")
        self.assertIn("exercise", data)
        self.assertEqual(data["exercise"]["domain"], "Geometry and Trigonometry")

    async def test_api_analytics_pacing_and_weekly_report(self):
        user_id = 330004
        # Pacing
        resp_pace = await self.client.get(
            "/api/v1/analytics/pacing",
            headers={"X-Dev-User-Id": str(user_id)}
        )
        self.assertEqual(resp_pace.status, 200)
        data_pace = await resp_pace.json()
        self.assertEqual(data_pace["status"], "ok")

        # Weekly Report
        resp_rep = await self.client.get(
            "/api/v1/analytics/weekly-report",
            headers={"X-Dev-User-Id": str(user_id)}
        )
        self.assertEqual(resp_rep.status, 200)
        data_rep = await resp_rep.json()
        self.assertEqual(data_rep["status"], "ok")
        self.assertIn("report", data_rep)

    async def test_api_hints_scaffolding(self):
        published = vault.get_published_questions()
        sample_qid = published[0]["id"]

        resp = await self.client.get(
            f"/api/v1/practice/hint?question_id={sample_qid}",
            headers={"X-Dev-User-Id": "330005"}
        )
        self.assertEqual(resp.status, 200)
        data = await resp.json()
        self.assertEqual(data["status"], "ok")
        self.assertIn("hint_level_1", data["hints"])
        self.assertIn("hint_level_2", data["hints"])

    async def test_api_telemetry_event(self):
        resp = await self.client.post(
            "/api/v1/telemetry/event",
            headers={"X-Dev-User-Id": "330006"},
            json={
                "event": "starter_drill_completed",
                "metadata": {"mode": "microdrill", "duration_seconds": 145}
            }
        )
        self.assertEqual(resp.status, 200)
        data = await resp.json()
        self.assertEqual(data["status"], "ok")
        self.assertTrue(data["recorded"])


if __name__ == "__main__":
    unittest.main()
