import json
import os
from pathlib import Path
from unittest.mock import AsyncMock, patch

import config
from database import db, now_ts, shift_day, today
from services import attempts, cards, review, sessions, writing_ai
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

    async def test_the_server_picks_the_second_module(self):
        items = mock_items("sat_mock_1", {"rw": "easy", "math": "easy"}, wrong_answer)
        report = (await self.call("POST", "/api/v1/attempts", body={
            "kind": "sat_mock", "ref": "sat_mock_1", "route": {"rw": "hard", "math": "hard"}, "items": items,
        }, expect=201))["report"]
        self.assertEqual(report["route"], {"rw": "easy", "math": "easy"})

    async def test_questions_seen_in_practice_do_not_count_towards_the_score(self):
        familiar = content.mocks["sat_mock_1"]["rw"]["m1"][:10]
        await self.call("POST", "/api/v1/attempts", user=2, body={
            "kind": "practice", "mode": "domain", "items": [{"q": qid, "a": right_answer(content.bank[qid])} for qid in familiar],
        }, expect=201)
        fresh = (await self.submit(right_answer, user=1))["report"]
        exposed = (await self.submit(right_answer, user=2))["report"]
        self.assertEqual(fresh["exposure"], {"seen": 0, "total": 98, "clean": True})
        self.assertEqual(exposed["exposure"], {"seen": 10, "total": 98, "clean": True})
        self.assertEqual(exposed["sections"]["rw"]["correct"], 54)
        self.assertLess(exposed["sections"]["rw"]["score"], fresh["sections"]["rw"]["score"] + 1)
        self.assertGreater(exposed["sections"]["rw"]["spread"], fresh["sections"]["rw"]["spread"] - 1)

    async def test_a_retake_keeps_all_answers_and_warns(self):
        await self.submit(right_answer)
        report = (await self.submit(right_answer))["report"]
        self.assertEqual(report["exposure"], {"seen": 98, "total": 98, "clean": False})
        self.assertGreaterEqual(report["score"], 1500)

    async def test_mock_list_counts_familiar_questions(self):
        question_id = content.mocks["sat_mock_3"]["math"]["m1"][0]
        await self.call("POST", "/api/v1/attempts", body={
            "kind": "practice", "mode": "domain", "items": [{"q": question_id, "a": "A"}],
        }, expect=201)
        seen = (await self.call("GET", "/api/v1/mocks", expect=200))["seen"]
        self.assertEqual(seen, {"sat_mock_1": 0, "sat_mock_2": 0, "sat_mock_3": 1, "sat_mock_4": 0})

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

    async def test_algebra_practice_does_not_reach_a_mock(self):
        for _ in range(10):
            ids = (await self.call("GET", "/api/v1/practice?section=m&domain=Algebra&count=10", expect=200))["ids"]
            self.assertTrue(all(content.bank[qid].get("free") for qid in ids))
            await self.practice(ids, right_answer)

    async def test_practice_never_shows_the_next_mock_or_a_sealed_exam(self):
        off_limits = content.mock_questions["sat_mock_1"] | content.sealed_questions
        for _ in range(12):
            ids = (await self.call("GET", "/api/v1/practice?section=rw&domain=Information and Ideas&count=10", expect=200))["ids"]
            self.assertTrue(ids)
            self.assertFalse(set(ids) & off_limits)
            await self.practice(ids, right_answer, ref="Information and Ideas")

    async def test_the_furthest_mock_is_opened_first(self):
        ids = (await self.call("GET", "/api/v1/practice?section=rw&domain=Information and Ideas&count=10", expect=200))["ids"]
        self.assertLessEqual({content.mock_of.get(qid) for qid in ids}, {None, "sat_mock_4"})

    async def test_protection_moves_on_after_a_mock(self):
        route = {"rw": "hard", "math": "hard"}
        await self.call("POST", "/api/v1/attempts", body={
            "kind": "sat_mock", "ref": "sat_mock_1", "route": route, "items": mock_items("sat_mock_1", route, right_answer),
        }, expect=201)
        ids = (await self.call("GET", "/api/v1/practice?section=rw&domain=Information and Ideas&count=20", expect=200))["ids"]
        self.assertFalse(set(ids) & content.mock_questions["sat_mock_2"])
        self.assertTrue(set(ids) & content.mock_questions["sat_mock_1"])

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

    async def test_task_1_feedback_receives_the_data_the_student_saw(self):
        with patch.object(writing_ai, "_call_gemini", AsyncMock(return_value=(FAKE_FEEDBACK, "gemini-test"))) as call:
            await self.submit(prompt_id="w1_03", status=201)
        self.assertIn("Technology 18%", call.await_args.args[4])

    async def test_task_2_feedback_has_no_visual(self):
        with patch.object(writing_ai, "_call_gemini", AsyncMock(return_value=(FAKE_FEEDBACK, "gemini-test"))) as call:
            await self.submit(status=201)
        self.assertEqual(call.await_args.args[4], "")

    def test_every_visual_can_be_described(self):
        for prompt in content.writing["task1"]:
            with self.subTest(prompt=prompt["id"]):
                self.assertGreater(len(writing_ai.describe_visual(prompt["visual"])), 40)

    def test_described_data_keeps_the_figures(self):
        line = writing_ai.describe_visual(content.writing_by_id["w1_22"]["visual"])
        self.assertIn("51+: 22, 38, 54, 68", line)
        flow = writing_ai.describe_visual(content.writing_by_id["w1_08"]["visual"])
        self.assertIn("Then, for Black tea", flow)
        place = writing_ai.describe_visual(content.writing_by_id["w1_05"]["visual"])
        self.assertIn("clock tower is unchanged", place)

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
        self.assertFalse(joined["session"]["secure"])
        self.assertFalse(joined["started"])

        await self.call("POST", f"/api/v1/sessions/{session['code']}/start", user=5, body={"name": "Aziza Karimova"}, expect=200)
        route = {"rw": "hard", "math": "hard"}
        await self.call("POST", "/api/v1/attempts", user=5, body={
            "kind": "sat_mock", "ref": "sat_mock_2", "route": route, "session": session["code"],
            "items": mock_items("sat_mock_2", route, right_answer),
        }, expect=201)

        results = await self.call("GET", f"/api/v1/teacher/sessions/{session['code']}", user=ADMIN, expect=200)
        self.assertEqual(results["count"], 1)
        self.assertEqual(results["students"][0]["correct"], 98)
        self.assertEqual(results["students"][0]["name"], "Aziza Karimova")
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

    async def join_and_start(self, session, user=5, name="Ali Valiyev"):
        await self.call("POST", "/api/v1/sessions/join", user=user, body={"code": session["code"]}, expect=200)
        return await self.call("POST", f"/api/v1/sessions/{session['code']}/start", user=user, body={"name": name}, expect=200)

    async def submit_exam(self, session, user=5, answer=right_answer, ref="sat_mock_2", expect=201):
        route = {"rw": "hard", "math": "hard"}
        return await self.call("POST", "/api/v1/attempts", user=user, body={
            "kind": "sat_mock", "ref": ref, "route": route, "session": session["code"], "items": mock_items(ref, route, answer),
        }, expect=expect)

    async def test_a_name_is_needed_to_start(self):
        await self.call("GET", "/api/v1/bootstrap", user=ADMIN, expect=200)
        session = await self.create_session()
        data = await self.call("POST", f"/api/v1/sessions/{session['code']}/start", user=5, body={"name": "  A "}, expect=400)
        self.assertEqual(data["error"], "name_required")
        await self.join_and_start(session, name="  Ali   Valiyev ")
        self.assertEqual((await sessions.get_entry(session["code"], 5))["full_name"], "Ali Valiyev")

    async def test_the_last_name_is_offered_next_time(self):
        await self.call("GET", "/api/v1/bootstrap", user=ADMIN, expect=200)
        first, second = await self.create_session(), await self.create_session()
        await self.join_and_start(first, name="Ali Valiyev")
        joined = await self.call("POST", "/api/v1/sessions/join", user=5, body={"code": second["code"]}, expect=200)
        self.assertEqual(joined["name"], "Ali Valiyev")

    async def test_only_the_first_result_counts(self):
        await self.call("GET", "/api/v1/bootstrap", user=ADMIN, expect=200)
        session = await self.create_session()
        await self.join_and_start(session)
        first = await self.submit_exam(session, answer=wrong_answer)
        second = await self.submit_exam(session, answer=right_answer)
        self.assertEqual(second["id"], first["id"])
        self.assertEqual(second["report"]["score"], first["report"]["score"])
        self.assertEqual(await db.fetchval("SELECT COUNT(*) FROM attempts WHERE session_code = ?", session["code"]), 1)
        again = await self.call("POST", f"/api/v1/sessions/{session['code']}/start", user=5, body={}, expect=200)
        self.assertEqual(again["done"], first["id"])
        joined = await self.call("POST", "/api/v1/sessions/join", user=5, body={"code": session["code"]}, expect=200)
        self.assertEqual(joined["done"], first["id"])

    async def test_a_different_exam_cannot_use_the_code(self):
        await self.call("GET", "/api/v1/bootstrap", user=ADMIN, expect=200)
        session = await self.create_session()
        await self.join_and_start(session)
        await self.submit_exam(session, ref="sat_mock_3")
        results = await self.call("GET", f"/api/v1/teacher/sessions/{session['code']}", user=ADMIN, expect=200)
        self.assertEqual(results["count"], 0)

    async def test_the_teacher_sees_who_is_still_working(self):
        await self.call("GET", "/api/v1/bootstrap", user=ADMIN, expect=200)
        session = await self.create_session()
        await self.join_and_start(session, user=5, name="Ali Valiyev")
        await self.join_and_start(session, user=6, name="Zarina Oripova")
        await self.submit_exam(session, user=5)
        results = await self.call("GET", f"/api/v1/teacher/sessions/{session['code']}", user=ADMIN, expect=200)
        self.assertEqual((results["count"], results["active"]), (1, 1))
        self.assertEqual([(s["name"], s["active"]) for s in results["students"]], [("Ali Valiyev", False), ("Zarina Oripova", True)])

    async def test_a_started_student_can_finish_after_the_exam_closes(self):
        await self.call("GET", "/api/v1/bootstrap", user=ADMIN, expect=200)
        session = await self.create_session()
        await self.join_and_start(session)
        await self.call("POST", f"/api/v1/teacher/sessions/{session['code']}/close", user=ADMIN, expect=200)
        await self.submit_exam(session)
        results = await self.call("GET", f"/api/v1/teacher/sessions/{session['code']}", user=ADMIN, expect=200)
        self.assertEqual(results["count"], 1)
        await self.call("POST", f"/api/v1/sessions/{session['code']}/start", user=6, body={"name": "Yangi O'quvchi"}, expect=404)

    async def test_time_comes_from_the_server_and_late_work_is_marked(self):
        await self.call("GET", "/api/v1/bootstrap", user=ADMIN, expect=200)
        session = await self.create_session()
        ticket = await self.join_and_start(session)
        self.assertGreater(ticket["seconds_left"], 143 * 60)
        await db.execute("UPDATE session_entries SET deadline_at = ? WHERE user_id = 5", now_ts() - sessions.GRACE_SECONDS - 60)
        again = await self.call("POST", f"/api/v1/sessions/{session['code']}/start", user=5, body={}, expect=200)
        self.assertEqual(again["seconds_left"], 0)
        await self.submit_exam(session)
        results = await self.call("GET", f"/api/v1/teacher/sessions/{session['code']}", user=ADMIN, expect=200)
        self.assertTrue(results["students"][0]["late"])
        data = (await centers_csv(session["code"])).decode("utf-8")
        self.assertIn("Kech topshirdi", data)

    async def test_export_needs_the_bot(self):
        await self.call("GET", "/api/v1/bootstrap", user=ADMIN, expect=200)
        session = await self.create_session()
        with patch.dict(self.client.server.app._state, {"bot": None}):
            await self.call("POST", f"/api/v1/teacher/sessions/{session['code']}/export", user=ADMIN, expect=503)


async def centers_csv(code: str) -> bytes:
    from services import centers

    return await centers.session_csv(code)


class SealedExamTest(ApiTestCase):
    async def sealed_session(self, kind="sat_mock", ref="sat_mock_5"):
        await self.call("GET", "/api/v1/bootstrap", user=ADMIN, expect=200)
        return (await self.call("POST", "/api/v1/teacher/sessions", user=ADMIN, body={"kind": kind, "ref": ref}, expect=201))["session"]

    async def start(self, session, user=5):
        await self.call("POST", "/api/v1/sessions/join", user=user, body={"code": session["code"]}, expect=200)
        return await self.call("POST", f"/api/v1/sessions/{session['code']}/start", user=user, body={"name": "Ali Valiyev"}, expect=200)

    def first_module(self, section, answer):
        ids = content.mocks["sat_mock_5"][section]["m1"]
        return [{"q": qid, "a": answer(content.bank[qid]), "t": 30} for qid in ids]

    async def route(self, session, section, answer, user=5):
        body = {"section": section, "items": self.first_module(section, answer)}
        return (await self.call("POST", f"/api/v1/sessions/{session['code']}/route", user=user, body=body, expect=200))["route"]

    async def finish(self, session, answer=right_answer, user=5, expect=201):
        route = {"rw": "hard", "math": "hard"}
        return await self.call("POST", "/api/v1/attempts", user=user, body={
            "kind": "sat_mock", "ref": "sat_mock_5", "route": route, "session": session["code"],
            "items": mock_items("sat_mock_5", route, answer),
        }, expect=expect)

    def test_sealed_exams_are_not_in_the_public_files(self):
        data_dir = Path(__file__).resolve().parent.parent / "webapp" / "data"
        bank = {q["id"] for q in json.loads((data_dir / "sat_bank.json").read_text(encoding="utf-8"))}
        notes = set(json.loads((data_dir / "sat_notes.json").read_text(encoding="utf-8")))
        mocks = {m["id"] for m in json.loads((data_dir / "sat_mocks.json").read_text(encoding="utf-8"))}
        reading = {t["num"] for t in json.loads((data_dir / "ielts.json").read_text(encoding="utf-8"))["reading"]}
        self.assertTrue(content.sealed_questions)
        self.assertFalse(bank & content.sealed_questions)
        self.assertFalse(notes & content.sealed_questions)
        self.assertFalse(mocks & content.sealed_mocks)
        self.assertFalse(reading & content.sealed_reading)

    async def test_the_server_does_not_serve_the_sealed_file(self):
        for path in ("/static/../data/sealed_exams.json", "/static/%2e%2e/data/sealed_exams.json", "/data/sealed_exams.json"):
            response = await self.client.get(path)
            self.assertIn(response.status, (403, 404), path)

    async def test_the_paper_has_no_keys(self):
        ticket = await self.start(await self.sealed_session())
        exam = ticket["exam"]
        self.assertEqual(len(exam["questions"]), len(content.mock_questions["sat_mock_5"]))
        text = json.dumps(exam["questions"])
        self.assertNotIn('"cor"', text)
        self.assertNotIn('"ans"', text)
        self.assertNotIn('"exp"', text)

    async def test_the_second_module_is_chosen_by_the_server_and_stays_chosen(self):
        session = await self.sealed_session()
        await self.start(session)
        self.assertEqual(await self.route(session, "rw", wrong_answer), "easy")
        self.assertEqual(await self.route(session, "rw", right_answer), "easy")
        self.assertEqual(await self.route(session, "math", right_answer), "hard")

    async def test_finished_modules_cannot_be_changed(self):
        session = await self.sealed_session()
        await self.start(session)
        await self.route(session, "rw", wrong_answer)
        await self.route(session, "math", wrong_answer)
        report = (await self.finish(session, answer=right_answer))["report"]
        self.assertEqual(report["route"], {"rw": "easy", "math": "easy"})
        rw_first = len(content.mocks["sat_mock_5"]["rw"]["m1"])
        self.assertLessEqual(report["sections"]["rw"]["correct"], 54 - rw_first)

    async def test_a_sealed_mock_needs_a_session(self):
        await self.finish({"code": ""}, expect=400)

    async def test_sealed_questions_stay_out_of_the_notebook(self):
        session = await self.sealed_session()
        await self.start(session)
        await self.finish(session, answer=wrong_answer)
        self.assertEqual((await self.call("GET", "/api/v1/notebook", user=5, expect=200))["items"], [])

    async def test_old_notebooks_forget_questions_that_became_sealed(self):
        sealed_id = next(iter(content.sealed_questions))
        await db.execute(
            """INSERT INTO review_items (user_id, question_id, due_day, updated_at) VALUES (5, ?, ?, 1)""", sealed_id, today(),
        )
        await review.forget_sealed_questions()
        self.assertEqual(await db.fetchval("SELECT COUNT(*) FROM review_items"), 0)

    async def test_review_opens_when_the_exam_closes(self):
        session = await self.sealed_session()
        await self.start(session)
        attempt_id = (await self.finish(session))["id"]
        self.assertTrue((await self.call("GET", f"/api/v1/attempts/{attempt_id}", user=5, expect=200))["locked"])
        await self.call("GET", f"/api/v1/attempts/{attempt_id}/review", user=5, expect=403)

        await self.call("POST", f"/api/v1/teacher/sessions/{session['code']}/close", user=ADMIN, expect=200)
        self.assertFalse((await self.call("GET", f"/api/v1/attempts/{attempt_id}", user=5, expect=200))["locked"])
        pack = await self.call("GET", f"/api/v1/attempts/{attempt_id}/review", user=5, expect=200)
        self.assertEqual(len(pack["questions"]), 98)
        self.assertTrue(all(qid in pack["notes"] for qid in pack["questions"]))
        await self.call("GET", f"/api/v1/attempts/{attempt_id}/review", user=6, expect=404)

    async def test_sealed_reading(self):
        session = await self.sealed_session("ielts_reading", "4")
        self.assertTrue(session["secure"])
        ticket = await self.start(session)
        questions = ticket["exam"]["test"]["questions"]
        self.assertEqual(len(questions), 40)
        self.assertFalse({"ans", "alts", "expl"} & {key for question in questions for key in question})
        answers = {str(q["num"]): q["ans"] for q in content.reading[4]["questions"]}
        await self.call("POST", "/api/v1/attempts", user=6, body={"kind": "ielts_reading", "ref": 4, "answers": answers}, expect=400)
        data = await self.call("POST", "/api/v1/attempts", user=5, body={
            "kind": "ielts_reading", "ref": 4, "answers": answers, "session": session["code"],
        }, expect=201)
        self.assertEqual(data["report"]["correct"], 40)

    async def test_the_catalog_lists_sealed_exams_first(self):
        await self.call("GET", "/api/v1/bootstrap", user=ADMIN, expect=200)
        catalog = (await self.call("GET", "/api/v1/teacher", user=ADMIN, expect=200))["catalog"]
        self.assertEqual([item["secure"] for item in catalog[:2]], [True, True])
        self.assertFalse(catalog[-1]["secure"])

    def test_module_route_uses_the_threshold(self):
        ids = content.mocks["sat_mock_1"]["rw"]["m1"]
        half = {qid: {"a": right_answer(content.bank[qid])} for qid in ids[:15]}
        self.assertEqual(attempts.module_route("sat_mock_1", "rw", half), "hard")
        self.assertEqual(attempts.module_route("sat_mock_1", "rw", {}), "easy")


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


class EventTest(ApiTestCase):
    async def test_known_events_are_stored_and_others_ignored(self):
        await self.call("POST", "/api/v1/events", body={"name": "app_open"}, expect=200)
        await self.call("POST", "/api/v1/events", body={"name": "made_up"}, expect=200)
        await self.call("POST", "/api/v1/events", body={"name": ["app_open"]}, expect=200)
        self.assertEqual(await db.fetchval("SELECT COUNT(*) FROM events"), 1)


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
