"""
EduTest Pro - Tier and Telegram Stars Payment Test Suite
Tests:
1. Free Tier defaults (10 questions/day limit, full explanations, basic analytics)
2. Free Tier error notebook (unlimited mistake reviews)
3. Pro Tier privileges (150 questions/day fair-use, full mock exam access)
4. Subscription activation and expiration fallback to Free without data loss
5. Telegram Stars payment idempotency (duplicate telegram_charge_id rejected)
6. Practice API endpoint tier enforcement (403 on limit reached, 200 on mistakes review)
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
from services.tier_service import (
    FREE_DAILY_QUESTIONS_LIMIT,
    FREE_WEEKLY_MOCKS_LIMIT,
    PRO_DAILY_FAIR_USE_LIMIT,
    TIER_PLANS,
    can_answer_practice_question,
    can_take_full_mock,
    get_daily_question_status,
    get_user_tier,
    is_user_pro,
    record_question_attempt,
)


class TestTierServiceUnit(unittest.TestCase):
    def setUp(self):
        self.saved_cache = copy.deepcopy(db.local_cache)

    def tearDown(self):
        db.local_cache = self.saved_cache
        db._save_local_db_sync()

    @patch("services.tier_service.PRO_BETA_MODE", False)
    def test_default_free_tier(self):
        user_id = 999111
        self.assertFalse(is_user_pro(user_id))
        tier_info = get_user_tier(user_id)
        self.assertEqual(tier_info["tier"], "free")
        self.assertFalse(tier_info["is_pro"])

        status = get_daily_question_status(user_id)
        self.assertEqual(status["answered_today"], 0)
        self.assertEqual(status["daily_limit"], FREE_DAILY_QUESTIONS_LIMIT)
        self.assertEqual(status["remaining_today"], FREE_DAILY_QUESTIONS_LIMIT)
        self.assertFalse(status["is_pro"])

    @patch("services.tier_service.PRO_BETA_MODE", False)
    def test_free_daily_limit_enforcement(self):
        user_id = 999222
        # Practice 50 questions
        for i in range(FREE_DAILY_QUESTIONS_LIMIT):
            allowed, msg = can_answer_practice_question(user_id, is_mistake_practice=False)
            self.assertTrue(allowed, f"Question {i+1} should be allowed")
            asyncio.run(record_question_attempt(user_id))

        # 51st question should be blocked for new practice
        allowed, msg = can_answer_practice_question(user_id, is_mistake_practice=False)
        self.assertFalse(allowed)
        self.assertIn("limitingiz to'ldi", msg)

        # Verify status
        status = get_daily_question_status(user_id)
        self.assertEqual(status["answered_today"], FREE_DAILY_QUESTIONS_LIMIT)
        self.assertEqual(status["remaining_today"], 0)
        self.assertTrue(status["is_limit_reached"])

    @patch("services.tier_service.PRO_BETA_MODE", False)
    def test_error_notebook_unlimited_for_free_users(self):
        user_id = 999333
        # Exceed daily limit
        for _ in range(55):
            asyncio.run(record_question_attempt(user_id))

        # Regular question blocked
        allowed, _ = can_answer_practice_question(user_id, is_mistake_practice=False)
        self.assertFalse(allowed)

        # Mistake review ALWAYS allowed for Free users
        allowed, msg = can_answer_practice_question(user_id, is_mistake_practice=True)
        self.assertTrue(allowed, "Mistake review should never be blocked")
        self.assertIn("Xatolar ustida mashq har doim cheklovsiz", msg)

    @patch("services.tier_service.PRO_BETA_MODE", False)
    def test_pro_subscription_and_privileges(self):
        user_id = 999444
        # Initially Free: 1 weekly mock allowed
        self.assertFalse(is_user_pro(user_id))
        can_mock, _ = can_take_full_mock(user_id)
        self.assertTrue(can_mock)
        # Consume the 1 weekly mock
        asyncio.run(db.increment_weekly_mocks(user_id))
        can_mock2, _ = can_take_full_mock(user_id)
        self.assertFalse(can_mock2)

        # Grant 1 Month Pro
        asyncio.run(db.add_user_subscription(
            user_id=user_id,
            plan_id="pro_1m",
            duration_days=30,
            stars_paid=250,
            telegram_charge_id="test_charge_1001"
        ))

        self.assertTrue(is_user_pro(user_id))
        self.assertEqual(get_user_tier(user_id)["tier"], "pro")
        can_mock_pro, _ = can_take_full_mock(user_id)
        self.assertTrue(can_mock_pro)

        status = get_daily_question_status(user_id)
        self.assertTrue(status["is_pro"])
        self.assertEqual(status["daily_limit"], PRO_DAILY_FAIR_USE_LIMIT)
        self.assertEqual(status["remaining_today"], PRO_DAILY_FAIR_USE_LIMIT)

    @patch("services.tier_service.PRO_BETA_MODE", False)
    def test_subscription_expiry_fallback(self):
        user_id = 999555
        # Grant expired subscription
        past_date = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
        db.local_cache.setdefault("subscriptions", {})[str(user_id)] = {
            "user_id": user_id,
            "plan_id": "pro_7d",
            "is_active": True,
            "started_at": (datetime.now(timezone.utc) - timedelta(days=8)).isoformat(),
            "expires_at": past_date,
            "stars_paid": 75,
            "latest_charge_id": "expired_charge_1"
        }
        db._save_local_db_sync()

        # Expiration recognized immediately
        self.assertFalse(is_user_pro(user_id))
        self.assertEqual(get_user_tier(user_id)["tier"], "free")

        # Check that subscription record is preserved (never deleted)
        sub = db.get_user_subscription(user_id)
        self.assertIsNotNone(sub)
        self.assertEqual(sub["plan_id"], "pro_7d")

    def test_payment_charge_id_idempotency(self):
        charge_id = "uniq_charge_9988"
        self.assertFalse(db.has_payment_charge_id(charge_id))

        asyncio.run(db.record_payment(
            user_id=777,
            plan_id="pro_1m",
            stars_amount=250,
            telegram_charge_id=charge_id
        ))
        self.assertTrue(db.has_payment_charge_id(charge_id))


class TestTierAndPaymentApi(AioHTTPTestCase):
    async def get_application(self) -> web.Application:
        return setup_web_app()

    def setUp(self):
        self.saved_cache = copy.deepcopy(db.local_cache)
        super().setUp()

    def tearDown(self):
        db.local_cache = self.saved_cache
        db._save_local_db_sync()
        super().tearDown()

    @patch("services.tier_service.PRO_BETA_MODE", False)
    async def test_today_summary_includes_tier(self):
        user_id = 1234567
        resp = await self.client.get(
            "/api/v1/practice/today-summary",
            headers={"X-Dev-User-Id": str(user_id)}
        )
        self.assertEqual(resp.status, 200)
        body = await resp.json()
        self.assertEqual(body["status"], "ok")
        self.assertEqual(body["tier"]["tier"], "free")
        self.assertIn("daily_usage", body)
        self.assertEqual(body["daily_usage"]["answered_today"], 0)
        self.assertEqual(body["daily_usage"]["daily_limit"], FREE_DAILY_QUESTIONS_LIMIT)

    async def test_today_summary_pro_beta_mode(self):
        user_id = 1234568
        resp = await self.client.get(
            "/api/v1/practice/today-summary",
            headers={"X-Dev-User-Id": str(user_id)}
        )
        self.assertEqual(resp.status, 200)
        body = await resp.json()
        self.assertEqual(body["status"], "ok")
        self.assertEqual(body["tier"]["tier"], "pro_beta")
        self.assertTrue(body["tier"]["is_pro"])
        self.assertTrue(body["tier"]["is_beta"])
        self.assertEqual(body["daily_usage"]["daily_limit"], PRO_DAILY_FAIR_USE_LIMIT)

    @patch("services.tier_service.PRO_BETA_MODE", False)
    async def test_practice_questions_blocked_when_limit_reached(self):
        user_id = 7654321

        # Exhaust 50 questions
        for _ in range(FREE_DAILY_QUESTIONS_LIMIT):
            await record_question_attempt(user_id)

        # Attempt to get normal practice questions -> 403 Forbidden
        resp = await self.client.get(
            "/api/v1/practice/questions?mode=daily_10m",
            headers={"X-Dev-User-Id": str(user_id)}
        )
        self.assertEqual(resp.status, 403)
        body = await resp.json()
        self.assertEqual(body["status"], "limit_reached")
        self.assertEqual(body["tier"]["tier"], "free")

        # Attempt to get mistake review questions -> Allowed (200 OK)
        resp2 = await self.client.get(
            "/api/v1/practice/questions?mode=mistakes",
            headers={"X-Dev-User-Id": str(user_id)}
        )
        self.assertEqual(resp2.status, 200)
        body2 = await resp2.json()
        self.assertEqual(body2["status"], "ok")


if __name__ == "__main__":
    unittest.main()
