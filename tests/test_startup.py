import asyncio
import logging
import unittest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch

from aiogram import Bot, Dispatcher
from aiogram.client.session.base import BaseSession
from aiogram.methods import AnswerCallbackQuery, EditMessageText, GetChatMember, SendMessage
from aiogram.types import CallbackQuery, Chat, ChatMemberMember, Message, Update, User
from aiohttp import ClientSession

import bot as bot_module
from config import BOT_TOKEN
from database import db
from handlers import router
from scheduler import setup_scheduler
from services import alerts, centers, users
from tests.helpers import DatabaseTestCase

ADMIN = 1000


class FakeSession(BaseSession):
    """Answers Bot API calls locally, so updates can run through the real routers."""

    def __init__(self):
        super().__init__()
        self.requests = []
        self.subscribed = False

    async def close(self):
        pass

    async def make_request(self, bot, method, timeout=None):
        self.requests.append(method)
        if isinstance(method, GetChatMember):
            if not self.subscribed:
                raise RuntimeError("channel unavailable")
            return ChatMemberMember(user=User(id=method.user_id, is_bot=False, first_name="Ali"))
        if isinstance(method, (SendMessage, EditMessageText)):
            return Message(message_id=99, date=datetime.now(timezone.utc), chat=Chat(id=method.chat_id or 1, type="private"), text=method.text)
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
        return [request.text for request in self.session.requests if isinstance(request, (SendMessage, EditMessageText))]


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
        await users.touch_user({"id": ADMIN, "first_name": "Admin"})
        session = await centers.create_session(ADMIN, "sat_mock", "sat_mock_1")
        replies = await self.send(f"/mock {session['code']}")
        self.assertIn(session["title"], replies[0])

    async def test_plain_menu_commands(self):
        self.assertIn("Asosiy Menyu", (await self.send("/menu"))[0])
        self.assertIn("Asosiy Menyu", (await self.send("/mock"))[0])

    async def test_keyboard_buttons(self):
        self.assertIn("Mock Tizimi", (await self.send("🎯 Mock Testlar (SAT & IELTS)"))[0])
        self.assertIn("Materiallari", (await self.send("📚 Bepul Materiallar"))[0])
        self.assertIn("Kanali", (await self.send("📢 Rasmiy Kanal (@ieltssat_daily)"))[0])

    async def test_admin_commands_are_not_swallowed_by_the_menu(self):
        replies = await self.send("/admin", user_id=ADMIN)
        self.assertIn("Boshqaruv paneli", replies[0])
        replies = await self.send("/center_add Marstif Academy", user_id=ADMIN)
        self.assertIn("start=teacher_", replies[0])

    async def test_students_are_refused_admin_commands(self):
        self.assertIn("faqat", (await self.send("/admin"))[0])
        self.assertEqual(await self.send("/center_add Yashirin"), [])

    async def test_unknown_private_text_gets_the_fallback(self):
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


class StartupTest(unittest.IsolatedAsyncioTestCase):
    async def test_every_update_type_in_use_is_requested(self):
        dp = Dispatcher()
        router._parent_router = None
        dp.include_router(router)
        self.assertLessEqual({"message", "callback_query"}, set(dp.resolve_used_update_types()))

    def test_scheduler_has_all_jobs(self):
        scheduler = setup_scheduler(object())
        names = {job.func.__name__ for job in scheduler.get_jobs()}
        self.assertEqual(names, {"post_daily_vocab_pack", "post_daily_sat_quiz", "post_daily_tip", "send_reminders", "send_weekly_reports"})

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
