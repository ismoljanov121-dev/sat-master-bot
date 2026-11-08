import asyncio
import html
import logging
import re
import unittest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch

from aiogram import Bot, Dispatcher
from aiogram.client.session.base import BaseSession
from aiogram.methods import AnswerCallbackQuery, EditMessageText, GetChatMember, SendMessage, SendVideo
from aiogram.types import CallbackQuery, Chat, ChatMemberLeft, ChatMemberMember, Message, Update, User, Video
from aiohttp import ClientSession

import bot as bot_module
from config import BOT_TOKEN, CHANNEL_URL
from database import asyncpg_url, db
from handlers import router
from scheduler import setup_scheduler
from services import alerts, centers, promo, users
from tests.helpers import DatabaseTestCase

ADMIN = 1000


class FakeSession(BaseSession):
    """Answers Bot API calls locally, so updates can run through the real routers."""

    def __init__(self):
        super().__init__()
        self.requests = []
        self.subscribed = False
        self.channel_error = False

    async def close(self):
        pass

    async def make_request(self, bot, method, timeout=None):
        self.requests.append(method)
        if isinstance(method, GetChatMember):
            if self.channel_error:
                raise RuntimeError("channel unavailable")
            user = User(id=method.user_id, is_bot=False, first_name="Ali")
            return ChatMemberMember(user=user) if self.subscribed else ChatMemberLeft(user=user)
        if isinstance(method, (SendMessage, EditMessageText)):
            return Message(message_id=99, date=datetime.now(timezone.utc), chat=Chat(id=method.chat_id or 1, type="private"), text=method.text)
        if isinstance(method, SendVideo):
            return Message(message_id=99, date=datetime.now(timezone.utc), chat=Chat(id=method.chat_id, type="private"), caption=method.caption)
        if isinstance(method, AnswerCallbackQuery):
            return True
        return True

    async def stream_content(self, *args, **kwargs):
        yield b""


class RouterTestCase(DatabaseTestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.session = FakeSession()
        self.bot = Bot(token=BOT_TOKEN, session=self.session)
        self.dp = Dispatcher()
        # A router can belong to one dispatcher only, and every test builds a new one.
        router._parent_router = None
        self.dp.include_router(router)
        self.update_id = 0

    def message(self, text: str, user_id: int = 5, chat_type: str = "private") -> Update:
        self.update_id += 1
        user = User(id=user_id, is_bot=False, first_name="Ali", username="ali")
        chat = Chat(id=user_id if chat_type == "private" else -100, type=chat_type, title=None if chat_type == "private" else "Guruh")
        return Update(update_id=self.update_id, message=Message(
            message_id=self.update_id, date=datetime.now(timezone.utc), chat=chat, from_user=user, text=text,
        ))

    async def send(self, text: str, **kwargs) -> list[str]:
        self.session.requests.clear()
        await self.dp.feed_update(self.bot, self.message(text, **kwargs))
        return self.replies()

    def replies(self) -> list[str]:
        return [request.text for request in self.session.requests if isinstance(request, (SendMessage, EditMessageText))]

    def sent(self, method_type) -> list:
        return [request for request in self.session.requests if isinstance(request, method_type)]

    async def press(self, data: str, user_id: int = 5) -> None:
        self.session.requests.clear()
        self.update_id += 1
        user = User(id=user_id, is_bot=False, first_name="Ali")
        source = Message(message_id=1, date=datetime.now(timezone.utc), chat=Chat(id=user_id, type="private"), text="x")
        await self.dp.feed_update(self.bot, Update(update_id=self.update_id, callback_query=CallbackQuery(
            id="1", from_user=user, chat_instance="c", data=data, message=source,
        )))


class RoutingTest(RouterTestCase):
    async def test_start_runs_through_the_router(self):
        replies = await self.send("/start")
        self.assertIn("Xush Kelibsiz", replies[0])
        self.assertEqual((await users.get_user(5))["bot_started"], 1)

    async def test_subscribed_user_gets_the_main_menu(self):
        self.session.subscribed = True
        replies = await self.send("/start")
        self.assertIn("Xush kelibsiz, Ali", replies[0])

    async def test_start_with_referral(self):
        await self.send("/start ref_77")
        self.assertEqual((await users.get_user(5))["referred_by"], 77)

    async def test_mock_command_with_a_code(self):
        self.session.subscribed = True
        await users.touch_user({"id": ADMIN, "first_name": "Admin"})
        session = await centers.create_session(ADMIN, "sat_mock", "sat_mock_1")
        replies = await self.send(f"/mock {session['code']}")
        self.assertIn(session["title"], replies[0])

    async def test_plain_menu_commands(self):
        self.session.subscribed = True
        self.assertIn("Asosiy Menyu", (await self.send("/menu"))[0])
        self.assertIn("Asosiy Menyu", (await self.send("/mock"))[0])

    async def test_keyboard_buttons(self):
        self.session.subscribed = True
        self.assertIn("Mock Tizimi", (await self.send("🎯 Mock Testlar (SAT & IELTS)"))[0])
        self.assertIn("Materiallari", (await self.send("📚 Bepul Materiallar"))[0])
        channel = (await self.send("📢 Rasmiy Kanal (@ieltssat_daily)"))[0]
        self.assertIn("Kanali", channel)
        # The times the channel really posts at, see SLOTS in services/channel.py.
        for slot in ("08:00", "13:00", "18:00", "21:00"):
            self.assertIn(slot, channel)

    async def test_admin_commands_are_not_swallowed_by_the_menu(self):
        replies = await self.send("/admin", user_id=ADMIN)
        self.assertIn("Boshqaruv paneli", replies[0])
        replies = await self.send("/center_add Marstif Academy", user_id=ADMIN)
        self.assertIn("start=teacher_", replies[0])

    async def test_students_are_refused_admin_commands(self):
        self.assertIn("faqat", (await self.send("/admin"))[0])
        self.assertEqual(await self.send("/center_add Yashirin"), [])

    async def test_unknown_private_text_gets_the_fallback(self):
        self.session.subscribed = True
        self.assertIn("Xush Kelibsiz", (await self.send("salom"))[0])

    async def test_group_message_with_keywords_goes_to_admins(self):
        text = "IELTS reading va writing bo'yicha foydali maslahatlar va SAT tayyorgarlik rejasi shu yerda yozilgan"
        replies = await self.send(text, chat_type="supergroup")
        self.assertEqual(len(replies), 1)
        self.assertEqual(self.session.requests[0].chat_id, ADMIN)

    async def test_channel_check_button(self):
        self.update_id += 1
        user = User(id=5, is_bot=False, first_name="Ali")
        source = Message(message_id=1, date=datetime.now(timezone.utc), chat=Chat(id=5, type="private"), text="x")
        update = Update(update_id=self.update_id, callback_query=CallbackQuery(
            id="1", from_user=user, chat_instance="c", data="check_sub", message=source,
        ))
        await self.dp.feed_update(self.bot, update)
        answers = [request for request in self.session.requests if isinstance(request, AnswerCallbackQuery)]
        self.assertTrue(answers[0].show_alert)


class ChannelGateTest(RouterTestCase):
    async def test_outsider_start_shows_only_the_join_prompt(self):
        replies = await self.send("/start")
        self.assertEqual(len(replies), 1)
        self.assertIn("obuna bo'ling", replies[0])
        keyboard = self.sent(SendMessage)[0].reply_markup.inline_keyboard
        self.assertEqual(keyboard[0][0].url, CHANNEL_URL)
        self.assertEqual(keyboard[1][0].callback_data, "check_sub")

    async def test_outsider_menu_is_gated(self):
        replies = await self.send("📚 Bepul Materiallar")
        self.assertIn("Avval", replies[0])
        self.assertNotIn("Materiallari", replies[0])

    async def test_outsider_buttons_are_gated(self):
        await self.press("dl_sat")
        self.assertTrue(self.sent(AnswerCallbackQuery)[0].show_alert)
        self.assertEqual(self.sent(EditMessageText), [])

    async def test_exam_code_waits_on_the_check_button(self):
        await users.touch_user({"id": ADMIN, "first_name": "Admin"})
        session = await centers.create_session(ADMIN, "sat_mock", "sat_mock_1")
        await self.send(f"/mock {session['code']}")
        keyboard = self.sent(SendMessage)[0].reply_markup.inline_keyboard
        self.assertEqual(keyboard[1][0].callback_data, f"check_sub:s_{session['code']}")

        self.session.subscribed = True
        await self.press(f"check_sub:s_{session['code']}")
        self.assertIn(session["title"], self.replies()[0])
        self.assertIn(session["code"], self.sent(SendMessage)[0].reply_markup.inline_keyboard[0][0].web_app.url)

    async def test_start_link_with_an_exam_code_keeps_it_too(self):
        await users.touch_user({"id": ADMIN, "first_name": "Admin"})
        session = await centers.create_session(ADMIN, "sat_mock", "sat_mock_1")
        await self.send(f"/start s_{session['code']}")
        keyboard = self.sent(SendMessage)[0].reply_markup.inline_keyboard
        self.assertEqual(keyboard[1][0].callback_data, f"check_sub:s_{session['code']}")

    async def test_check_button_refuses_until_joined_then_opens_the_menu(self):
        await self.press("check_sub")
        self.assertTrue(self.sent(AnswerCallbackQuery)[0].show_alert)
        self.session.subscribed = True
        await self.press("check_sub")
        self.assertIn("Obuna tasdiqlandi", self.replies()[0])

    async def test_failed_check_lets_students_in(self):
        self.session.channel_error = True
        with self.assertLogs("services.subscription", level="ERROR"):
            replies = await self.send("📚 Bepul Materiallar")
        self.assertIn("Materiallari", replies[0])

    async def test_admins_and_teachers_skip_the_channel(self):
        self.assertIn("Materiallari", (await self.send("📚 Bepul Materiallar", user_id=ADMIN))[0])
        await users.touch_user({"id": ADMIN, "first_name": "Admin"})
        center = await centers.create_center("Marstif", ADMIN)
        await centers.join_as_teacher(center["teacher_code"], 7)
        self.assertIn("Materiallari", (await self.send("📚 Bepul Materiallar", user_id=7))[0])

    async def test_advert_link_records_where_the_user_came_from(self):
        await self.send("/start promo")
        self.assertEqual((await users.get_user(5))["source"], "promo")


class PromoPostTest(RouterTestCase):
    def video_message(self, caption: str, user_id: int = ADMIN) -> Update:
        self.update_id += 1
        user = User(id=user_id, is_bot=False, first_name="Admin")
        return Update(update_id=self.update_id, message=Message(
            message_id=self.update_id, date=datetime.now(timezone.utc), chat=Chat(id=user_id, type="private"),
            from_user=user, caption=caption,
            video=Video(file_id="promo-video", file_unique_id="u1", width=1080, height=1920, duration=24),
        ))

    async def test_video_comes_back_as_a_ready_post(self):
        self.session.requests.clear()
        await self.dp.feed_update(self.bot, self.video_message("/reklama"))
        videos = self.sent(SendVideo)
        self.assertEqual(len(videos), 1)
        self.assertEqual(videos[0].video, "promo-video")
        self.assertEqual(videos[0].caption, promo.CAPTION)
        buttons = [row[0] for row in videos[0].reply_markup.inline_keyboard]
        self.assertTrue(buttons[0].url.endswith("?start=promo"))
        self.assertEqual(buttons[1].url, CHANNEL_URL)

    async def test_command_alone_explains_and_sends_the_text_post(self):
        replies = await self.send("/reklama", user_id=ADMIN)
        self.assertIn("/reklama", replies[0])
        self.assertEqual(replies[1], promo.CAPTION)

    async def test_students_cannot_make_posts(self):
        self.session.requests.clear()
        await self.dp.feed_update(self.bot, self.video_message("/reklama", user_id=5))
        self.assertEqual(self.sent(SendVideo), [])
        self.assertEqual(self.replies(), [])

    async def test_dashboard_counts_people_from_the_advert(self):
        await users.touch_user({"id": 42, "first_name": "Vali"}, source="promo")
        replies = await self.send("/admin", user_id=ADMIN)
        self.assertIn("Reklama tugmasidan kelganlar: <b>1</b>", replies[0])

    def test_caption_fits_the_telegram_limit(self):
        visible = html.unescape(re.sub(r"<[^>]+>", "", promo.CAPTION))
        self.assertLessEqual(len(visible.encode("utf-16-le")) // 2, promo.CAPTION_LIMIT)


class StartupTest(unittest.IsolatedAsyncioTestCase):
    async def test_every_update_type_in_use_is_requested(self):
        dp = Dispatcher()
        router._parent_router = None
        dp.include_router(router)
        self.assertLessEqual({"message", "callback_query"}, set(dp.resolve_used_update_types()))

    def test_scheduler_has_all_jobs(self):
        scheduler = setup_scheduler(object())
        jobs = scheduler.get_jobs()
        self.assertEqual({job.func.__name__ for job in jobs}, {"post_channel_slot", "send_reminders", "send_weekly_reports"})
        slots = [job for job in jobs if job.func.__name__ == "post_channel_slot"]
        self.assertEqual(sorted(job.args[1] for job in slots), [0, 1, 2, 3])

    async def test_main_starts_serves_and_stops_cleanly(self):
        seen = {}

        async def fake_polling(dp, bot):
            async with ClientSession() as session:
                async with session.get("http://127.0.0.1:18999/health") as response:
                    seen["health"] = response.status
                    seen["body"] = await response.json()
                async with session.get("http://127.0.0.1:18999/webapp") as response:
                    seen["webapp"] = response.status

        router._parent_router = None
        with patch.object(bot_module, "PORT", 18999), patch.object(bot_module, "run_polling", fake_polling), \
                patch.object(bot_module, "self_ping_loop", AsyncMock()):
            await bot_module.main()

        self.assertEqual(seen["health"], 200)
        self.assertEqual(seen["body"]["status"], "ok")
        self.assertEqual(seen["webapp"], 200)
        self.assertFalse(await db.ping())


class ConnectionUrlTest(unittest.TestCase):
    def test_libpq_options_are_removed_and_the_rest_kept(self):
        url = "postgresql://user:p%40ss@host.neon.tech/db?sslmode=require&channel_binding=require"
        self.assertEqual(asyncpg_url(url), "postgresql://user:p%40ss@host.neon.tech/db?sslmode=require")

    def test_plain_urls_stay_the_same(self):
        self.assertEqual(asyncpg_url("postgres://u:p@localhost:5432/db"), "postgres://u:p@localhost:5432/db")


class AlertTest(unittest.IsolatedAsyncioTestCase):
    async def test_errors_reach_admins_once_per_cooldown(self):
        fake_bot = AsyncMock()
        handler = alerts.TelegramAlertHandler(fake_bot, frozenset({ADMIN}))
        logger = logging.getLogger("tests.alert_sample")
        logger.addHandler(handler)
        logger.propagate = False
        try:
            for _ in range(3):
                logger.error("database is down")
            await asyncio.sleep(0)
            await asyncio.sleep(0)
        finally:
            logger.removeHandler(handler)
        self.assertEqual(fake_bot.send_message.await_count, 1)
        self.assertIn("database is down", fake_bot.send_message.await_args.args[1])
