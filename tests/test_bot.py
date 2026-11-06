from types import SimpleNamespace
from unittest.mock import AsyncMock

from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter

import scheduler
from content_bank import IELTS_TIPS, IELTS_VOCAB_PACKS
from database import db, shift_day, today
from handlers import admin, menu
from services import analytics, centers, plan, users
from tests.helpers import DatabaseTestCase


def fake_message(user_id: int = 5, first_name: str = "Ali") -> SimpleNamespace:
    user = SimpleNamespace(id=user_id, first_name=first_name, model_dump=lambda: {"id": user_id, "first_name": first_name})
    return SimpleNamespace(from_user=user, answer=AsyncMock())


class StartTest(DatabaseTestCase):
    async def start(self, args=None, user_id=5):
        message = fake_message(user_id)
        bot = SimpleNamespace(get_chat_member=AsyncMock(side_effect=Exception("no channel")))
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


class AnalyticsTest(DatabaseTestCase):
    async def add_user(self, user_id: int, source: str = "", **fields):
        await users.touch_user({"id": user_id, "first_name": "Ali"}, source=source, bot_started=True)
        for name, value in fields.items():
            await db.execute(f"UPDATE users SET {name} = ? WHERE id = ?", value, user_id)

    def test_sources_are_folded_into_readable_channels(self):
        self.assertEqual(analytics.source_label(""), "To'g'ridan-to'g'ri")
        self.assertEqual(analytics.source_label("ch_quiz"), "Kanal: quiz")
        self.assertEqual(analytics.source_label("referral"), "Do'st taklifi")
        self.assertEqual(analytics.source_label("s_ABC123"), "Guruh imtihoni")
        self.assertEqual(analytics.source_label("teacher_XYZ"), "O'qituvchi havolasi")
        self.assertEqual(analytics.source_label("instagram"), "instagram")

    async def test_funnel_counts_every_step_per_source(self):
        await self.add_user(1, "ch_quiz", onboarded=1, last_active_day=today())
        await self.add_user(2, "ch_quiz", onboarded=1)
        await self.add_user(3, "s_ABC")
        await self.add_user(4, "s_DEF", last_active_day=shift_day(today(), -20))
        data = await analytics.funnel()
        self.assertEqual(data["total"], {"users": 4, "onboarded": 2, "studied": 2, "active": 1})
        sources = dict(data["sources"])
        self.assertEqual(sources["Kanal: quiz"], {"users": 2, "onboarded": 2, "studied": 1, "active": 1})
        self.assertEqual(sources["Guruh imtihoni"]["users"], 2)

    async def test_return_counts_study_a_week_after_joining(self):
        joined = analytics.now_ts() - 20 * analytics.DAY_SECONDS
        await self.add_user(1, created_at=joined, last_active_day=today())
        await self.add_user(2, created_at=joined, last_active_day=shift_day(today(), -19))
        await self.add_user(3, created_at=joined)
        await self.add_user(4)
        self.assertEqual(await analytics.week_return(), {"users": 3, "returned": 1})

    async def test_report_escapes_sources_from_deep_links(self):
        await self.add_user(1, "<b>x")
        await users.record_event(1, "app_open")
        text = await analytics.report_text()
        self.assertIn("&lt;b&gt;x", text)
        self.assertIn("app_open", text)

    async def test_report_on_an_empty_database(self):
        self.assertIn("Yangi", await analytics.report_text())

    async def test_segments_leave_out_people_who_cannot_or_do_not_want_messages(self):
        await self.add_user(1, focus="sat", last_active_day=today())
        await self.add_user(2, focus="ielts", last_active_day=shift_day(today(), -30))
        await self.add_user(3, focus="both")
        await self.add_user(4, reminders_on=0)
        await self.add_user(5, blocked=1)
        await users.touch_user({"id": 6, "first_name": "Ali"})
        self.assertEqual(sorted(await analytics.segment_users("hammasi")), [1, 2, 3])
        self.assertEqual(await analytics.segment_users("faol"), [1])
        self.assertEqual(await analytics.segment_users("nofaol"), [2])
        self.assertEqual(await analytics.segment_users("boshlamagan"), [3])
        self.assertEqual(sorted(await analytics.segment_users("sat")), [1, 3])
        self.assertEqual(sorted(await analytics.segment_users("ielts")), [2, 3])
        self.assertEqual(await analytics.segment_size("hammasi"), 3)


class BroadcastTest(DatabaseTestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        admin._sending.clear()
        for user_id in (1, 2, 3):
            await users.touch_user({"id": user_id, "first_name": "Ali"}, bot_started=True)

    async def test_it_needs_a_reply_and_a_known_segment(self):
        message = fake_message(1000)
        message.reply_to_message = None
        await admin.cmd_broadcast(message, SimpleNamespace(args="hammasi"))
        self.assertIn("Segmentlar", message.answer.await_args.args[0])

        message = fake_message(1000)
        message.reply_to_message = SimpleNamespace(message_id=7)
        await admin.cmd_broadcast(message, SimpleNamespace(args="yoq"))
        self.assertIn("Segmentlar", message.answer.await_args.args[0])

    async def test_nothing_goes_out_before_the_admin_confirms(self):
        message = fake_message(1000)
        message.reply_to_message = SimpleNamespace(message_id=7)
        await admin.cmd_broadcast(message, SimpleNamespace(args="hammasi"))
        markup = message.answer.await_args.kwargs["reply_markup"]
        self.assertEqual(markup.inline_keyboard[0][0].callback_data, "bc:hammasi:7")
        self.assertIn("3", message.answer.await_args.args[0])

    async def test_students_cannot_broadcast(self):
        message = fake_message(5)
        message.reply_to_message = SimpleNamespace(message_id=7)
        await admin.cmd_broadcast(message, SimpleNamespace(args="hammasi"))
        message.answer.assert_not_awaited()

        callback = SimpleNamespace(from_user=SimpleNamespace(id=5), data="bc:hammasi:7", answer=AsyncMock())
        bot = SimpleNamespace(copy_message=AsyncMock())
        await admin.cb_broadcast_send(callback, bot)
        bot.copy_message.assert_not_awaited()

    async def confirm(self, bot):
        chat = SimpleNamespace(id=1000)
        callback = SimpleNamespace(
            from_user=SimpleNamespace(id=1000), data="bc:hammasi:7", answer=AsyncMock(),
            message=SimpleNamespace(chat=chat, edit_text=AsyncMock()),
        )
        await admin.cb_broadcast_send(callback, bot)
        return callback

    async def test_confirmed_message_is_copied_to_the_segment(self):
        bot = SimpleNamespace(copy_message=AsyncMock())
        callback = await self.confirm(bot)
        self.assertEqual(sorted(call.kwargs["chat_id"] for call in bot.copy_message.await_args_list), [1, 2, 3])
        self.assertEqual(bot.copy_message.await_args.kwargs["message_id"], 7)
        self.assertIn("3 / 3", callback.message.edit_text.await_args.args[0])
        self.assertEqual(await db.fetchval("SELECT meta FROM events WHERE name = 'broadcast'"), "hammasi:3/3")

    async def test_a_second_tap_does_not_send_twice(self):
        bot = SimpleNamespace(copy_message=AsyncMock())
        await self.confirm(bot)
        await self.confirm(bot)
        self.assertEqual(bot.copy_message.await_count, 3)

    async def test_blocked_users_are_marked_and_the_rest_still_get_it(self):
        error = TelegramForbiddenError(method=SimpleNamespace(), message="blocked")
        bot = SimpleNamespace(copy_message=AsyncMock(side_effect=[error, None, None]))
        sent, total = await scheduler.send_broadcast(bot, "hammasi", 1000, 7)
        self.assertEqual((sent, total), (2, 3))
        self.assertEqual(await db.fetchval("SELECT COUNT(*) FROM users WHERE blocked = 1"), 1)

    async def test_a_rate_limit_waits_and_tries_again(self):
        error = TelegramRetryAfter(method=SimpleNamespace(), message="slow", retry_after=0)
        bot = SimpleNamespace(copy_message=AsyncMock(side_effect=[error, None, None, None]))
        sent, total = await scheduler.send_broadcast(bot, "hammasi", 1000, 7)
        self.assertEqual((sent, total), (3, 3))


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
        await scheduler.post_daily_vocab_pack(bot)
        await scheduler.post_daily_tip(bot)
        await scheduler.post_daily_sat_quiz(bot)
        self.assertEqual(bot.send_poll.await_count, 1)
        self.assertGreaterEqual(bot.send_message.await_count, 2)

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
