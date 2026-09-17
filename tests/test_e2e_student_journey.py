"""
EduTest Pro - End-to-End Student Practice Journey Test Suite
Validates the complete 5-step learning flow:
1. Bugun (Today Hub): Summary, streak, micro-goal target, mistake counters.
2. Mashq (Practice): Question delivery with strict zero-leakage anti-cheat guarantee.
3. Javob Izohi (Instant Explanation): Real-time server-side answer check, Uzbek explanation, Desmos hack.
4. Xatolarim (Error Notebook): Auto-recording wrong answers, re-practice, and resolution.
5. Natijalar (Results & Analytics): Idempotent submission, honest mastery stats, pacing, and bot-webapp sync.
"""

import hashlib
import hmac
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from urllib.parse import urlencode

from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot import setup_web_app
from config import BOT_TOKEN
from database import db


def create_signed_init_data(user_obj: dict | None, bot_token: str, auth_date: int | None = None) -> str:
    """Helper to generate authentic Telegram WebApp initData string."""
    date_val = auth_date if auth_date is not None else int(datetime.now(timezone.utc).timestamp())
    params: dict[str, str] = {
        "auth_date": str(date_val),
        "query_id": "AAHdF6IQAAAAAN0XohD74h-X",
    }
    if user_obj is not None:
        params["user"] = json.dumps(user_obj)

    sorted_pairs = [f"{k}={v}" for k, v in sorted(params.items())]
    data_check_string = "\n".join(sorted_pairs)

    secret_key = hmac.new(b"WebAppData", bot_token.encode("utf-8"), hashlib.sha256).digest()
    computed_hash = hmac.new(secret_key, data_check_string.encode("utf-8"), hashlib.sha256).hexdigest()

    return f"{urlencode(params)}&hash={computed_hash}"


class TestE2EStudentJourney(AioHTTPTestCase):

    async def get_application(self) -> web.Application:
        return setup_web_app()

    def setUp(self):
        super().setUp()
        self.user_id = 99881122
        self.user_obj = {
            "id": self.user_id,
            "first_name": "Azizbek",
            "last_name": "Rahimov",
            "username": "aziz_sat"
        }
        self.valid_init_data = create_signed_init_data(self.user_obj, BOT_TOKEN)
        self.auth_headers = {
            "Content-Type": "application/json",
            "X-Telegram-Init-Data": self.valid_init_data
        }

        # Initialize student profile in database with clean test isolation
        str_id = str(self.user_id)
        db.local_cache.setdefault("users", {})[str_id] = {
            "user_id": self.user_id,
            "username": "aziz_sat",
            "full_name": "Azizbek Rahimov",
            "level": "Advanced",
            "role": "student"
        }
        db.local_cache.setdefault("error_notebook", {})[str_id] = {}
        db.local_cache.setdefault("practice_stats", {})[str_id] = {
            "total_answered": 0,
            "correct_count": 0,
            "current_streak": 0,
            "best_streak": 0,
            "by_section": {
                "math": {"total": 0, "correct": 0},
                "reading": {"total": 0, "correct": 0},
                "writing": {"total": 0, "correct": 0}
            },
            "answered_ids": []
        }

    # =========================================================================
    # STEP 1: BUGUN (TODAY SUMMARY)
    # =========================================================================
    async def test_01_today_summary_flow(self):
        """Verifies initial student state: streak, 10-question daily target, zero mistakes."""
        resp = await self.client.get("/api/v1/practice/today-summary", headers=self.auth_headers)
        self.assertEqual(resp.status, 200)

        data = await resp.json()
        self.assertEqual(data["status"], "ok")
        self.assertIn("today", data)

        today = data["today"]
        self.assertEqual(today["target_questions"], 10)
        self.assertEqual(today["unresolved_mistakes"], 0)
        self.assertIn("streak_days", today)
        self.assertFalse(today["has_active_session"])

    # =========================================================================
    # STEP 2: MASHQ (PRACTICE QUESTIONS & ZERO-LEAKAGE AUDIT)
    # =========================================================================
    async def test_02_practice_questions_zero_leakage(self):
        """
        Verifies safe delivery of practice questions:
        Strictly guarantees 'correct', 'explanation', and 'strategy_or_hack' are stripped.
        """
        resp = await self.client.get("/api/v1/practice/questions?mode=daily_10m", headers=self.auth_headers)
        self.assertEqual(resp.status, 200)

        data = await resp.json()
        self.assertEqual(data["status"], "ok")
        self.assertIn("session_id", data)
        self.assertTrue(data["session_id"].startswith("sess_"))

        questions = data["questions"]
        self.assertGreaterEqual(len(questions), 4)

        # STRICT ANTI-CHEAT AUDIT: None of the questions must expose answers or hacks!
        for q in questions:
            self.assertIn("id", q)
            self.assertIn("question", q)
            self.assertIn("options", q)
            self.assertNotIn("correct", q, f"CRITICAL LEAK: Question {q.get('id')} leaked 'correct'!")
            self.assertNotIn("explanation", q, f"CRITICAL LEAK: Question {q.get('id')} leaked 'explanation'!")
            self.assertNotIn("strategy_or_hack", q, f"CRITICAL LEAK: Question {q.get('id')} leaked 'strategy_or_hack'!")

    # =========================================================================
    # STEP 3: JAVOB IZOHI (INSTANT EXPLANATION & AUTO-RECORD WRONG ANSWER)
    # =========================================================================
    async def test_03_instant_check_answer_and_mistake_recording(self):
        """
        Submits an answer:
        1. Checks server-side validation and dual explanation return.
        2. Intentionally wrong answer must automatically record into error_notebook.
        """
        # 1. Start a session
        q_resp = await self.client.get("/api/v1/practice/questions?mode=daily_10m", headers=self.auth_headers)
        q_data = await q_resp.json()
        session_id = q_data["session_id"]
        q0 = q_data["questions"][0]
        qid = q0["id"]

        # 2. Check answer with deliberate choice "Z" (wrong answer)
        check_payload = {
            "session_id": session_id,
            "question_id": qid,
            "user_answer": "Z",
            "time_spent_seconds": 25
        }
        check_resp = await self.client.post("/api/v1/practice/check-answer", headers=self.auth_headers, json=check_payload)
        self.assertEqual(check_resp.status, 200)

        result = await check_resp.json()
        self.assertEqual(result["status"], "ok")
        self.assertFalse(result["is_correct"])
        self.assertIn("correct_answer", result)
        self.assertTrue(len(result.get("explanation", "")) > 0, "Uzbek explanation must be provided")

        # 3. Verify that the mistake was automatically saved into error_notebook
        mistakes = db.get_user_mistakes(self.user_id, resolved_filter=False)
        self.assertTrue(any(str(m.get("question_id")) == str(qid) for m in mistakes),
                        "Incorrect answer was not queued into error notebook!")

    # =========================================================================
    # STEP 4: XATOLARIM (ERROR NOTEBOOK RETRIEVAL & ONE-CLICK RESOLVE)
    # =========================================================================
    async def test_04_error_notebook_and_resolve(self):
        """
        Tests:
        1. Fetching unresolved mistakes queue via GET /api/v1/mistakes.
        2. Resolving a mistake via POST /api/v1/mistakes/resolve.
        """
        # Ensure a mistake exists
        await db.record_mistake(
            user_id=self.user_id,
            question_id="test_q_geom_101",
            section="math",
            domain="Geometry",
            question_text="In circle O, what is radius r?",
            options=[{"key": "A", "text": "5"}, {"key": "B", "text": "10"}],
            user_answer="A",
            correct_answer="B",
            explanation="Radius equals diameter divided by 2.",
            hack="Desmos circle equation: (x-h)^2 + (y-k)^2 = r^2"
        )

        # 1. Fetch mistakes
        m_resp = await self.client.get("/api/v1/mistakes?resolved=0", headers=self.auth_headers)
        self.assertEqual(m_resp.status, 200)
        m_data = await m_resp.json()
        self.assertEqual(m_data["status"], "ok")
        self.assertGreaterEqual(m_data["count"], 1)

        # 2. Resolve the mistake
        res_payload = {"question_id": "test_q_geom_101"}
        res_resp = await self.client.post("/api/v1/mistakes/resolve", headers=self.auth_headers, json=res_payload)
        self.assertEqual(res_resp.status, 200)
        res_data = await res_resp.json()
        self.assertEqual(res_data["status"], "ok")
        self.assertTrue(res_data["resolved"])

        # 3. Verify it is no longer in unresolved list
        m_after = await self.client.get("/api/v1/mistakes?resolved=0", headers=self.auth_headers)
        m_after_data = await m_after.json()
        self.assertFalse(any(str(m.get("question_id")) == "test_q_geom_101" for m in m_after_data["mistakes"]))

    # =========================================================================
    # STEP 5: NATIJALAR (IDEMPOTENT SUBMISSION & BOT-WEBAPP SYNC)
    # =========================================================================
    async def test_05_idempotent_submit_and_stats_synchronization(self):
        """
        Tests:
        1. Final exam submission via POST /api/v1/practice/submit.
        2. Idempotency protection against duplicate network requests.
        3. Synchronization with bot practice stats and streak.
        """
        # 1. Start a clean session
        q_resp = await self.client.get("/api/v1/practice/questions?mode=daily_10m", headers=self.auth_headers)
        q_data = await q_resp.json()
        session_id = q_data["session_id"]
        questions = q_data["questions"]

        # 2. Prepare answers dictionary with correct answers
        from services.practice_api import ACTIVE_PRACTICE_SESSIONS
        sess_data = ACTIVE_PRACTICE_SESSIONS.get(session_id)
        answers = {}
        for q in sess_data["questions"]:
            answers[q["id"]] = q.get("correct", "A")

        idempotency_key = f"idemp_{uuid.uuid4().hex}"
        submit_payload = {
            "session_id": session_id,
            "idempotency_key": idempotency_key,
            "answers": answers,
            "total_time_spent": 140
        }

        # First submission
        sub_resp1 = await self.client.post("/api/v1/practice/submit", headers=self.auth_headers, json=submit_payload)
        self.assertEqual(sub_resp1.status, 200)
        res1 = await sub_resp1.json()
        self.assertEqual(res1["status"], "ok")
        self.assertIn("results", res1)

        first_stats = res1["results"]
        self.assertEqual(first_stats["total_questions"], len(questions))
        self.assertIn("accuracy_pct", first_stats)
        self.assertIn("avg_time_per_question_seconds", first_stats)
        self.assertIn("domain_breakdown", first_stats)

        # 3. IDEMPOTENCY CHECK: Send the exact same submission request again
        sub_resp2 = await self.client.post("/api/v1/practice/submit", headers=self.auth_headers, json=submit_payload)
        self.assertEqual(sub_resp2.status, 200)
        res2 = await sub_resp2.json()
        self.assertTrue(res2.get("idempotent", False), "Duplicate request should return idempotent cached response")
        self.assertEqual(res2["results"]["accuracy_pct"], first_stats["accuracy_pct"])

        # 4. BOT SYNCHRONIZATION CHECK: Telegram bot practice stats must reflect the session
        bot_stats = db.get_user_practice_stats(self.user_id)
        self.assertGreaterEqual(bot_stats.get("total_answered", 0), len(questions))
        self.assertGreaterEqual(bot_stats.get("current_streak", 0), 1)
