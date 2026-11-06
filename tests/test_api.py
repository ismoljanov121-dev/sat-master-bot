import os
from unittest.mock import AsyncMock, patch

import config
from database import db, shift_day, today
from services import cards, writing_ai
from services.content import content
from tests.helpers import ApiTestCase, init_data

ADMIN = 1000
GOOD_ESSAY = "word " * 120


def mock_items(mock_id: str, route: dict, answer) -> list[dict]:
    items = []
    for ids in content.mock_modules(mock_id, route).values():
        for question_id in ids:
            items.append({"q": question_id, "a": answer(content.bank[question_id]), "t": 60})
    return items


def right_answer(question: dict) -> str:
    return question["cor"] if question["type"] == "mcq" else question["ans"][0]


def wrong_answer(question: dict) -> str:
    if question["type"] == "spr":
        return "999999"
    return "A" if question["cor"] != "A" else "B"


class AuthTest(ApiTestCase):
    async def test_requests_without_valid_init_data_are_refused(self):
        response = await self.client.get("/api/v1/bootstrap")
        self.assertEqual(response.status, 401)
        response = await self.client.get("/api/v1/bootstrap", headers={"X-Telegram-Init-Data": "user=1&hash=abc"})
        self.assertEqual(response.status, 401)

    async def test_first_request_creates_the_user(self):
        data = await self.call("GET", "/api/v1/bootstrap", user=7, expect=200)
        self.assertEqual(data["me"]["id"], 7)
        self.assertFalse(data["me"]["onboarded"])
        self.assertFalse(data["staff"])
        self.assertEqual(await db.fetchval("SELECT COUNT(*) FROM users"), 1)


class ProfileTest(ApiTestCase):
    async def test_valid_goals_are_saved_and_bad_ones_ignored(self):
        data = await self.call("POST", "/api/v1/profile", body={
            "focus": "both", "target_sat": 1450, "target_ielts": 7.5, "exam_date": "2027-03-14",
            "daily_minutes": 45, "reminder_hour": 20, "reminders_on": False, "onboarded": True,
        }, expect=200)
        self.assertEqual(data["me"]["target_sat"], 1450)
        self.assertEqual(data["me"]["reminder_hour"], 20)
        self.assertFalse(data["me"]["reminders_on"])
        self.assertTrue(data["me"]["onboarded"])

        data = await self.call("POST", "/api/v1/profile", body={"target_sat": 9000, "reminder_hour": 40, "focus": "x"}, expect=200)
        self.assertEqual(data["me"]["target_sat"], 1450)
        self.assertEqual(data["me"]["reminder_hour"], 20)
        self.assertEqual(data["me"]["focus"], "both")


class MockAttemptTest(ApiTestCase):
    route = {"rw": "hard", "math": "hard"}

    async def submit(self, answer, user=1, route=None):
        route = route or self.route
        return await self.call("POST", "/api/v1/attempts", user=user, body={
            "kind": "sat_mock", "ref": "sat_mock_1", "route": route,
            "items": mock_items("sat_mock_1", route, answer),
        }, expect=201)

    async def test_server_grades_the_attempt(self):
        data = await self.submit(right_answer)
        report = data["report"]
        self.assertEqual(report["sections"]["rw"]["correct"], 54)
        self.assertEqual(report["sections"]["math"]["correct"], 44)
        self.assertGreaterEqual(report["score"], 1500)
        self.assertLessEqual(report["low"], report["score"])
        self.assertEqual(data["me"]["streak"], 1)

    async def test_a_client_cannot_claim_a_better_score(self):
        route = self.route
        items = mock_items("sat_mock_1", route, wrong_answer)
        data = await self.call("POST", "/api/v1/attempts", body={
            "kind": "sat_mock", "ref": "sat_mock_1", "route": route, "items": items,
            "score": 1600, "correct": 98,
        }, expect=201)
        self.assertLess(data["report"]["score"], 800)

    async def test_report_has_domains_pacing_and_steps(self):
        report = (await self.submit(wrong_answer))["report"]
        self.assertEqual(len(report["domains"]), 8)
        self.assertEqual(sum(d["total"] for d in report["domains"]), 98)
        self.assertEqual(report["pacing"]["avg_s"], 60)
        self.assertTrue(report["steps"])
        self.assertIn("practice", {step["action"]["type"] for step in report["steps"]})

    async def test_previous_score_is_reported(self):
        first = await self.submit(wrong_answer)
        second = await self.submit(right_answer)
        self.assertEqual(second["report"]["previous"], first["report"]["score"])

    async def test_unknown_mock_is_rejected(self):
        await self.call("POST", "/api/v1/attempts", body={"kind": "sat_mock", "ref": "nope", "route": self.route}, expect=400)
        await self.call("POST", "/api/v1/attempts", body={"kind": "sat_mock", "ref": "sat_mock_1", "route": {"rw": "x"}}, expect=400)

    async def test_attempts_are_private(self):
        attempt_id = (await self.submit(right_answer, user=1))["id"]
        await self.call("GET", f"/api/v1/attempts/{attempt_id}", user=2, expect=404)
        data = await self.call("GET", f"/api/v1/attempts/{attempt_id}", user=1, expect=200)
        self.assertEqual(len(data["answers"]), 98)
        listing = await self.call("GET", "/api/v1/attempts", user=1, expect=200)
        self.assertEqual(listing["attempts"][0]["id"], attempt_id)

    async def test_skipped_mock_questions_are_not_counted_as_mistakes(self):
        await self.call("POST", "/api/v1/attempts", body={
            "kind": "sat_mock", "ref": "sat_mock_1", "route": self.route, "items": [],
        }, expect=201)
        notebook = await self.call("GET", "/api/v1/notebook", expect=200)
        self.assertEqual(notebook["items"], [])


class PracticeTest(ApiTestCase):
    async def practice(self, question_ids, answer, mode="domain", ref="Algebra"):
        return await self.call("POST", "/api/v1/attempts", body={
            "kind": "practice", "mode": mode, "ref": ref,
            "items": [{"q": qid, "a": answer(content.bank[qid]), "t": 30} for qid in question_ids],
        }, expect=201)

    async def test_filters_and_unseen_questions_first(self):
        first = (await self.call("GET", "/api/v1/practice?section=m&domain=Algebra&count=10", expect=200))["ids"]
        self.assertEqual(len(first), 10)
        self.assertEqual({content.bank[qid]["dom"] for qid in first}, {"Algebra"})
        await self.practice(first, right_answer)
        second = (await self.call("GET", "/api/v1/practice?section=m&domain=Algebra&count=10", expect=200))["ids"]
        self.assertFalse(set(first) & set(second))

    async def test_mock_questions_are_used_last(self):
        ids = (await self.call("GET", "/api/v1/practice?section=m&domain=Geometry and Trigonometry&count=5", expect=200))["ids"]
        self.assertTrue(all(content.bank[qid].get("free") for qid in ids))

    async def test_spaced_repetition_schedule(self):
        question_id = next(iter(content.bank))
        await self.practice([question_id], wrong_answer)

        notebook = await self.call("GET", "/api/v1/notebook", expect=200)
        self.assertEqual(notebook["due"], [])
        self.assertEqual(notebook["items"][0]["due"], shift_day(today(), 1))

        await db.execute("UPDATE review_items SET due_day = ?", today())
        notebook = await self.call("GET", "/api/v1/notebook", expect=200)
        self.assertEqual(notebook["due"], [question_id])

        for expected_days in (3, 7):
            await self.practice([question_id], right_answer, mode="review", ref="")
            notebook = await self.call("GET", "/api/v1/notebook", expect=200)
            self.assertEqual(notebook["items"][0]["due"], shift_day(today(), expected_days))

        await self.practice([question_id], right_answer, mode="review", ref="")
        notebook = await self.call("GET", "/api/v1/notebook", expect=200)
        self.assertEqual(notebook["items"], [])
        self.assertEqual(notebook["resolved"], 1)

    async def test_a_wrong_review_starts_over(self):
        question_id = next(iter(content.bank))
        await self.practice([question_id], wrong_answer)
        await self.practice([question_id], right_answer, mode="review", ref="")
        await self.practice([question_id], wrong_answer, mode="review", ref="")
        item = (await self.call("GET", "/api/v1/notebook", expect=200))["items"][0]
        self.assertEqual(item["box"], 0)
        self.assertEqual(item["wrong"], 2)

    async def test_diagnostic_covers_every_domain(self):
        ids = (await self.call("GET", "/api/v1/diagnostic", expect=200))["ids"]
        self.assertEqual(len(ids), 16)
        self.assertEqual(len({content.bank[qid]["dom"] for qid in ids}), 8)
        report = (await self.practice(ids, right_answer, mode="diagnostic", ref=""))["report"]
        self.assertEqual(report["kind"], "diagnostic")
        boot = await self.call("GET", "/api/v1/bootstrap", expect=200)
        self.assertTrue(boot["summary"]["diagnostic_done"])

    async def test_unknown_questions_are_ignored(self):
        await self.call("POST", "/api/v1/attempts", body={
            "kind": "practice", "mode": "domain", "items": [{"q": "nope", "a": "A"}],
        }, expect=400)


class PlanTest(ApiTestCase):
    async def test_new_student_starts_with_the_diagnostic(self):
        await self.call("POST", "/api/v1/profile", body={"focus": "sat", "onboarded": True}, expect=200)
        plan = (await self.call("GET", "/api/v1/bootstrap", expect=200))["plan"]
        self.assertEqual(plan["tasks"][0]["action"]["type"], "diagnostic")

    async def test_due_reviews_and_weak_domain_appear(self):
        await self.call("POST", "/api/v1/profile", body={"focus": "sat", "exam_date": shift_day(today(), 30)}, expect=200)
        ids = (await self.call("GET", "/api/v1/diagnostic", expect=200))["ids"]
        await self.call("POST", "/api/v1/attempts", body={
            "kind": "practice", "mode": "diagnostic",
            "items": [{"q": qid, "a": wrong_answer(content.bank[qid]) if content.bank[qid]["sec"] == "m" else right_answer(content.bank[qid])} for qid in ids],
        }, expect=201)
        await db.execute("UPDATE review_items SET due_day = ?", today())
        plan = (await self.call("GET", "/api/v1/bootstrap", expect=200))["plan"]
        kinds = {task["action"]["type"] for task in plan["tasks"]}
        self.assertIn("review", kinds)
        practice = next(task for task in plan["tasks"] if task["action"]["type"] == "practice")
        self.assertEqual(practice["action"]["section"], "m")
        self.assertEqual(plan["days_left"], 30)


class IeltsAttemptTest(ApiTestCase):
    async def test_reading_is_graded_on_the_server(self):
        test = content.reading[1]
        answers = {str(q["num"]): q["ans"] for q in test["questions"]}
        data = await self.call("POST", "/api/v1/attempts", body={"kind": "ielts_reading", "ref": 1, "answers": answers}, expect=201)
        self.assertEqual(data["report"]["correct"], 40)
        self.assertEqual(data["report"]["band"], 9)

    async def test_listening_counts_blank_answers_as_wrong(self):
        data = await self.call("POST", "/api/v1/attempts", body={"kind": "ielts_listening", "ref": 1, "answers": {}}, expect=201)
        self.assertEqual(data["report"]["correct"], 0)
        self.assertEqual(len(data["report"]["wrong"]), 40)

    async def test_unknown_test(self):
        await self.call("POST", "/api/v1/attempts", body={"kind": "ielts_reading", "ref": 99, "answers": {}}, expect=400)


FAKE_FEEDBACK = {
    "on_topic": True,
    "task": {"band": 6, "comment": "Yaxshi"}, "coherence": {"band": 6.5, "comment": "Yaxshi"},
    "lexical": {"band": 6, "comment": "O'rtacha"}, "grammar": {"band": 5.5, "comment": "Xatolar bor"},
    "summary": "Umumiy xulosa", "strengths": ["Tuzilma"],
    "mistakes": [{"quote": "I am agree", "fix": "I agree", "why": "Fe'l"}],
    "improved_paragraph": "A better paragraph.", "next_steps": ["Mashq qiling"],
}


class WritingTest(ApiTestCase):
    def setUp(self):
        key = patch.object(config, "GEMINI_API_KEY", "test-key")
        key.start()
        self.addCleanup(key.stop)

    async def submit(self, text=GOOD_ESSAY, status=None, prompt_id="w2_01", user=1):
        return await self.call("POST", "/api/v1/writing", user=user, body={"prompt_id": prompt_id, "text": text, "minutes": 40}, expect=status)

    async def test_feedback_is_saved_and_the_band_is_computed(self):
        with patch.object(writing_ai, "_call_gemini", AsyncMock(return_value=(FAKE_FEEDBACK, "gemini-test"))):
            data = await self.submit(status=201)
        self.assertEqual(data["band"], 6.0)
        self.assertEqual(data["remaining"], config.AI_DAILY_LIMIT - 1)
        self.assertEqual(data["me"]["streak"], 1)
        history = await self.call("GET", "/api/v1/writing", expect=200)
        self.assertEqual(len(history["items"]), 1)
        detail = await self.call("GET", f"/api/v1/writing/{data['id']}", expect=200)
        self.assertEqual(detail["criteria"]["grammar"]["band"], 5.5)
        await self.call("GET", f"/api/v1/writing/{data['id']}", user=2, expect=404)

    async def test_daily_limit(self):
        with patch.object(writing_ai, "_call_gemini", AsyncMock(return_value=(FAKE_FEEDBACK, "gemini-test"))) as call:
            for _ in range(config.AI_DAILY_LIMIT):
                await self.submit(status=201)
            data = await self.submit(status=429)
        self.assertEqual(data["error"], "limit_reached")
        self.assertEqual(call.await_count, config.AI_DAILY_LIMIT)

    async def test_length_limits_do_not_spend_a_check(self):
        with patch.object(writing_ai, "_call_gemini", AsyncMock(return_value=(FAKE_FEEDBACK, "gemini-test"))) as call:
            self.assertEqual((await self.submit("too short", status=400))["error"], "too_short")
            self.assertEqual((await self.submit("word " * 900, status=400))["error"], "too_long")
        call.assert_not_awaited()

    async def test_failure_does_not_spend_a_check(self):
        with patch.object(writing_ai, "_call_gemini", AsyncMock(side_effect=writing_ai.WritingError("ai_busy"))):
            self.assertEqual((await self.submit(status=429))["error"], "ai_busy")
        data = await self.call("GET", "/api/v1/writing", expect=200)
        self.assertEqual(data["remaining"], config.AI_DAILY_LIMIT)

    async def test_prompt_must_be_ours(self):
        await self.submit(prompt_id="made_up", status=400)

    async def test_disabled_without_a_key(self):
        with patch.object(config, "GEMINI_API_KEY", ""):
            self.assertEqual((await self.submit(status=400))["error"], "ai_disabled")

    def test_bands_are_clamped_and_rounded(self):
        cleaned = writing_ai.clean_feedback({**FAKE_FEEDBACK, "task": {"band": 12, "comment": ""}, "grammar": {"band": 6.3, "comment": ""}}, 2)
        self.assertEqual(cleaned["criteria"]["task"]["band"], 9.0)
        self.assertEqual(cleaned["criteria"]["grammar"]["band"], 6.5)
        self.assertEqual(writing_ai.overall_band([6, 6, 6, 6.5]), 6.0)
        self.assertEqual(writing_ai.overall_band([6.5, 6.5, 6.5, 6]), 6.5)


class CenterTest(ApiTestCase):
    async def create_session(self, user=ADMIN):
        return (await self.call("POST", "/api/v1/teacher/sessions", user=user, body={"kind": "sat_mock", "ref": "sat_mock_2"}, expect=201))["session"]

    async def test_students_cannot_use_the_panel(self):
        await self.call("GET", "/api/v1/teacher", user=5, expect=403)
        await self.call("POST", "/api/v1/teacher/sessions", user=5, body={"kind": "sat_mock", "ref": "sat_mock_1"}, expect=403)

    async def test_session_flow(self):
        await self.call("GET", "/api/v1/bootstrap", user=ADMIN, expect=200)
        session = await self.create_session()
        self.assertEqual(len(session["code"]), 6)

        joined = await self.call("POST", "/api/v1/sessions/join", user=5, body={"code": session["code"].lower()}, expect=200)
        self.assertEqual(joined["session"]["ref"], "sat_mock_2")

        route = {"rw": "easy", "math": "easy"}
        await self.call("POST", "/api/v1/attempts", user=5, body={
            "kind": "sat_mock", "ref": "sat_mock_2", "route": route, "session": session["code"],
            "items": mock_items("sat_mock_2", route, right_answer),
        }, expect=201)

        results = await self.call("GET", f"/api/v1/teacher/sessions/{session['code']}", user=ADMIN, expect=200)
        self.assertEqual(results["count"], 1)
        self.assertEqual(results["students"][0]["correct"], 98)
        self.assertTrue(results["topics"])

        await self.call("POST", f"/api/v1/teacher/sessions/{session['code']}/export", user=ADMIN, expect=200)
        self.assertEqual(self.bot.documents[0][0], ADMIN)

        await self.call("POST", f"/api/v1/teacher/sessions/{session['code']}/close", user=ADMIN, expect=200)
        await self.call("POST", "/api/v1/sessions/join", user=6, body={"code": session["code"]}, expect=404)

    async def test_teacher_invite_and_isolation(self):
        from services import centers

        await self.call("GET", "/api/v1/bootstrap", user=11, expect=200)
        await self.call("GET", "/api/v1/bootstrap", user=12, expect=200)
        first = await centers.create_center("A Markaz", 11)
        second = await centers.create_center("B Markaz", 12)
        session = await self.create_session(user=11)
        self.assertEqual((await self.call("GET", "/api/v1/bootstrap", user=11))["staff"], True)
        await self.call("GET", f"/api/v1/teacher/sessions/{session['code']}", user=12, expect=403)

        await self.call("GET", "/api/v1/bootstrap", user=13, expect=200)
        await self.call("POST", "/api/v1/teacher/join", user=13, body={"code": first["teacher_code"]}, expect=200)
        await self.call("GET", f"/api/v1/teacher/sessions/{session['code']}", user=13, expect=200)
        await self.call("POST", "/api/v1/teacher/join", user=14, body={"code": "WRONG"}, expect=404)
        self.assertNotEqual(first["id"], second["id"])

    async def test_csv_neutralises_formula_names(self):
        from services import centers

        await self.call("GET", "/api/v1/bootstrap", user=ADMIN, expect=200)
        session = await self.create_session()
        headers = {"X-Telegram-Init-Data": init_data(21, first_name="=HYPERLINK(1)")}
        await self.client.get("/api/v1/bootstrap", headers=headers)
        await self.call("POST", "/api/v1/attempts", user=21, body={
            "kind": "sat_mock", "ref": "sat_mock_2", "route": {"rw": "easy", "math": "easy"}, "session": session["code"], "items": [],
        })
        data = (await centers.session_csv(session["code"])).decode("utf-8")
        self.assertIn("'=", data)

    async def test_export_needs_the_bot(self):
        await self.call("GET", "/api/v1/bootstrap", user=ADMIN, expect=200)
        session = await self.create_session()
        with patch.dict(self.client.server.app._state, {"bot": None}):
            await self.call("POST", f"/api/v1/teacher/sessions/{session['code']}/export", user=ADMIN, expect=503)


class ReferralTest(ApiTestCase):
    async def test_reward_comes_after_the_friend_studies(self):
        from services import users

        await users.touch_user({"id": 1, "first_name": "A"}, bot_started=True)
        await users.touch_user({"id": 2, "first_name": "B"}, referred_by=1, bot_started=True)
        boot = await self.call("GET", "/api/v1/bootstrap", user=1, expect=200)
        self.assertEqual(boot["referral"]["joined"], 1)
        self.assertEqual(boot["referral"]["bonus"], 0)

        question_id = next(iter(content.bank))
        for _ in range(2):
            await self.call("POST", "/api/v1/attempts", user=2, body={
                "kind": "practice", "mode": "domain", "items": [{"q": question_id, "a": "A"}],
            }, expect=201)
        boot = await self.call("GET", "/api/v1/bootstrap", user=1, expect=200)
        self.assertEqual(boot["referral"]["active"], 1)
        self.assertEqual(boot["referral"]["bonus"], 1)
        self.assertEqual(boot["ai"]["limit"], config.AI_DAILY_LIMIT + 1)
        self.assertEqual(len(self.bot.messages), 1)

    async def test_nobody_can_refer_themselves(self):
        from services import users

        row, _ = await users.touch_user({"id": 3, "first_name": "A"}, referred_by=3)
        self.assertIsNone(row["referred_by"])


class WebTest(ApiTestCase):
    async def test_ci_runs_on_the_database_it_asked_for(self):
        expected = "postgres" if os.environ.get("TEST_DATABASE_URL") else "sqlite"
        self.assertEqual(db.kind, expected)

    async def test_health_reports_storage_and_version(self):
        response = await self.client.get("/health")
        data = await response.json()
        self.assertEqual(response.status, 200)
        self.assertEqual(data["status"], "ok")
        self.assertIn(data["storage"], ("sqlite", "postgres"))

    async def test_health_fails_when_polling_stopped(self):
        import asyncio

        task = asyncio.create_task(asyncio.sleep(0))
        await task
        self.client.server.app["runtime"]["polling_task"] = task
        response = await self.client.get("/health")
        self.assertEqual(response.status, 503)

    async def test_mini_app_links_assets_by_content_hash(self):
        response = await self.client.get("/webapp")
        html = await response.text()
        self.assertEqual(response.status, 200)
        self.assertNotIn("?v=dev", html)
        self.assertEqual(response.headers["Cache-Control"], "no-cache")

    async def test_versioned_assets_are_cached_forever(self):
        response = await self.client.get("/static/data/sat_mocks.json?v=1")
        self.assertEqual(response.status, 200)
        self.assertIn("immutable", response.headers["Cache-Control"])

    async def test_share_card_needs_a_valid_signature(self):
        question_id = next(iter(content.bank))
        await self.call("GET", "/api/v1/bootstrap", user=1, expect=200)
        attempt = await self.call("POST", "/api/v1/attempts", body={
            "kind": "practice", "mode": "domain", "items": [{"q": question_id, "a": "A"}],
        }, expect=201)
        share = await self.call("POST", "/api/v1/share", body={"attempt": attempt["id"]}, expect=200)
        self.assertIn("start=ref_1", share["link"])
        response = await self.client.get(cards.card_path(attempt["id"], config.BOT_TOKEN))
        self.assertEqual(response.status, 200)
        self.assertEqual(response.headers["Content-Type"], "image/png")
        forged = await self.client.get(f"/card/{attempt['id']}-{'0' * 20}.png")
        self.assertEqual(forged.status, 404)
