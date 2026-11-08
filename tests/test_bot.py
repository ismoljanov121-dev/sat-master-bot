from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from aiogram.exceptions import TelegramForbiddenError

import scheduler
from content_bank import IELTS_TIPS, IELTS_VOCAB_PACKS
from database import db, shift_day, today
from handlers import admin, menu
from services import centers, channel, plan, users
from tests.helpers import DatabaseTestCase


def fake_message(user_id: int = 5, first_name: str = "Ali") -> SimpleNamespace:
    user = SimpleNamespace(id=user_id, first_name=first_name, model_dump=lambda: {"id": user_id, "first_name": first_name})
    return SimpleNamespace(from_user=user, answer=AsyncMock())


class StartTest(DatabaseTestCase):
    async def start(self, args=None, user_id=5):
        message = fake_message(user_id)
        bot = SimpleNamespace(get_chat_member=AsyncMock(return_value=SimpleNamespace(status="member")))
        await menu.cmd_start(message, bot, SimpleNamespace(args=args))
        return message

    async def test_start_records_the_user(self):
        await self.start()
        row = await users.get_user(5)
        self.assertEqual(row["bot_started"], 1)

    async def test_referral_link(self):
        await self.start("ref_77")
        row = await users.get_user(5)
        self.assertEqual(row["referred_by"], 77)
        self.assertEqual(row["source"], "referral")

    async def test_channel_source_is_kept(self):
        await self.start("ch_quiz")
        self.assertEqual((await users.get_user(5))["source"], "ch_quiz")

    async def test_teacher_invite(self):
        await users.touch_user({"id": 1000, "first_name": "Admin"})
        center = await centers.create_center("Marstif", 1000)
        message = await self.start(f"teacher_{center['teacher_code']}")
        self.assertIn("Marstif", message.answer.await_args.args[0])
        self.assertTrue(await centers.is_staff(5))

    async def test_wrong_teacher_invite(self):
        message = await self.start("teacher_NOPE")
        self.assertIn("noto'g'ri", message.answer.await_args.args[0])
        self.assertFalse(await centers.is_staff(5))

    async def test_session_code_from_mock_command(self):
        await users.touch_user({"id": 1000, "first_name": "Admin"})
        session = await centers.create_session(1000, "sat_mock", "sat_mock_1")
        message = fake_message()
        await users.touch_user({"id": 5, "first_name": "Ali"})
        await menu.cmd_menu(message, SimpleNamespace(command="mock", args=session["code"]))
        markup = message.answer.await_args.kwargs["reply_markup"]
        self.assertIn(session["code"], markup.inline_keyboard[0][0].web_app.url)

    async def test_mock_command_with_a_bad_code(self):
        message = fake_message()
        await menu.cmd_menu(message, SimpleNamespace(command="mock", args="ZZZZZZ"))
        self.assertIn("topilmadi", message.answer.await_args.args[0])


class AdminTest(DatabaseTestCase):
    async def test_only_admins_see_stats(self):
        message = fake_message(5)
        await admin.cmd_admin(message)
        self.assertIn("faqat", message.answer.await_args.args[0])

        message = fake_message(1000)
        await admin.cmd_admin(message)
        self.assertIn("Foydalanuvchilar", message.answer.await_args.args[0])

    async def test_center_add_is_admin_only(self):
        message = fake_message(5)
        await admin.cmd_center_add(message, SimpleNamespace(args="Yashirin"))
        message.answer.assert_not_awaited()

        message = fake_message(1000)
        await admin.cmd_center_add(message, SimpleNamespace(args="Marstif Academy"))
        self.assertIn("start=teacher_", message.answer.await_args.args[0])
        self.assertEqual(len(await centers.list_centers()), 1)


class ChannelTest(DatabaseTestCase):
    def test_latex_becomes_poll_text(self):
        self.assertEqual(scheduler.plain_text(r"If \(x^{2}=9\) and \(\frac{1}{2}\)"), "If x²=9 and 1/2")
        self.assertEqual(scheduler.plain_text(r"\(\sqrt{16}\le 5\)"), "√(16)≤ 5")
        self.assertIsNone(scheduler.plain_text(r"\(x^{\frac{1}{2}}\)"))

    def test_candidates_fit_telegram_limits_and_skip_mock_questions(self):
        candidates = scheduler.channel_quiz_candidates()
        self.assertGreaterEqual(len(candidates), 30)
        for item in candidates:
            self.assertTrue(scheduler.content.bank[item["id"]].get("free"))
            self.assertLessEqual(len(item["stem"]) + 20, scheduler.POLL_QUESTION_LIMIT)
            self.assertTrue(all(len(option) <= scheduler.POLL_OPTION_LIMIT for option in item["options"]))

    def test_explanations_fit_the_poll_limit(self):
        for item in scheduler.channel_quiz_candidates():
            self.assertLessEqual(len(scheduler.short_explanation(scheduler.content.notes[item["id"]]["exp"])), scheduler.POLL_EXPLANATION_LIMIT)

    async def test_items_do_not_repeat_until_all_were_used(self):
        items = ["a", "b", "c"]
        first_round = [await scheduler.next_item("test", items) for _ in items]
        self.assertEqual(sorted(first_round), items)
        self.assertIn(await scheduler.next_item("test", items), items)
        self.assertEqual(await db.fetchval("SELECT COUNT(*) FROM channel_log WHERE kind = 'test'"), 1)

    async def test_daily_posts_reach_the_channel(self):
        bot = SimpleNamespace(send_message=AsyncMock(), send_poll=AsyncMock())
        with patch.object(channel, "POST_GAP_SECONDS", 0):
            for slot in range(len(scheduler.SLOTS)):
                await scheduler.post_channel_slot(bot, slot)
        self.assertGreaterEqual(bot.send_poll.await_count, 4)
        self.assertGreaterEqual(bot.send_message.await_count, 6)

    def test_channel_has_enough_content(self):
        self.assertGreaterEqual(len(IELTS_VOCAB_PACKS), 20)
        self.assertGreaterEqual(len(IELTS_TIPS), 30)
        for pack in IELTS_VOCAB_PACKS:
            self.assertEqual(len(pack["words"]), 10)


class ReminderTest(DatabaseTestCase):
    async def add_user(self, user_id: int, **fields):
        await users.touch_user({"id": user_id, "first_name": "Ali"}, bot_started=True)
        values = {"onboarded": 1, "reminder_hour": 19, "last_active_day": shift_day(today(), -1), **fields}
        for name, value in values.items():
            await db.execute(f"UPDATE users SET {name} = ? WHERE id = ?", value, user_id)

    async def test_who_gets_a_reminder(self):
        await self.add_user(1)
        await self.add_user(2, reminder_hour=8)
        await self.add_user(3, last_active_day=today())
        await self.add_user(4, reminders_on=0)
        await self.add_user(5, blocked=1)
        await self.add_user(6, onboarded=0)
        await self.add_user(7, last_active_day=shift_day(today(), -30))
        bot = SimpleNamespace(send_message=AsyncMock())
        await scheduler.send_reminders(bot, hour=19)
        self.assertEqual([call.args[0] for call in bot.send_message.await_args_list], [1])

    async def test_one_reminder_per_day(self):
        await self.add_user(1)
        bot = SimpleNamespace(send_message=AsyncMock())
        await scheduler.send_reminders(bot, hour=19)
        await scheduler.send_reminders(bot, hour=19)
        self.assertEqual(bot.send_message.await_count, 1)

    async def test_blocked_bot_stops_future_reminders(self):
        await self.add_user(1)
        error = TelegramForbiddenError(method=SimpleNamespace(), message="blocked")
        await scheduler.send_reminders(SimpleNamespace(send_message=AsyncMock(side_effect=error)), hour=19)
        self.assertEqual((await users.get_user(1))["blocked"], 1)

    async def test_streak_rules(self):
        await users.touch_user({"id": 1, "first_name": "Ali"})
        await db.execute("UPDATE users SET streak = 4, best_streak = 4, last_active_day = ? WHERE id = 1", shift_day(today(), -1))
        await users.mark_active(1)
        row = await users.get_user(1)
        self.assertEqual((row["streak"], row["best_streak"]), (5, 5))
        await users.mark_active(1)
        self.assertEqual((await users.get_user(1))["streak"], 5)
        await db.execute("UPDATE users SET last_active_day = ? WHERE id = 1", shift_day(today(), -3))
        self.assertEqual(users.current_streak(await users.get_user(1)), 0)
        await users.mark_active(1)
        self.assertEqual((await users.get_user(1))["streak"], 1)

    async def test_weekly_report_text(self):
        await users.touch_user({"id": 1, "first_name": "Ali"})
        empty = await plan.weekly_report(await users.get_user(1))
        self.assertIn("ishlanmadi", plan.weekly_report_text(empty))
