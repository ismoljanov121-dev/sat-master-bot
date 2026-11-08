from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import config
from services import centers, subscription, users
from tests.helpers import ApiTestCase, DatabaseTestCase

ADMIN = 1000


def member(status: str, **extra) -> SimpleNamespace:
    return SimpleNamespace(status=status, **extra)


def channel(answer) -> SimpleNamespace:
    return SimpleNamespace(get_chat_member=AsyncMock(return_value=answer))


class MembershipTest(DatabaseTestCase):
    async def test_statuses(self):
        cases = (("member", True), ("administrator", True), ("creator", True), ("left", False), ("kicked", False))
        for status, expected in cases:
            self.assertEqual(await subscription.is_member(channel(member(status)), 5, fresh=True), expected, status)
        self.assertTrue(await subscription.is_member(channel(member("restricted", is_member=True)), 5, fresh=True))
        self.assertFalse(await subscription.is_member(channel(member("restricted", is_member=False)), 5, fresh=True))

    async def test_answers_are_cached_and_a_fresh_check_asks_again(self):
        bot = channel(member("member"))
        self.assertTrue(await subscription.is_member(bot, 5))
        self.assertTrue(await subscription.is_member(bot, 5))
        self.assertEqual(bot.get_chat_member.await_count, 1)
        await subscription.is_member(bot, 5, fresh=True)
        self.assertEqual(bot.get_chat_member.await_count, 2)

    async def test_a_failed_check_lets_the_user_in(self):
        bot = SimpleNamespace(get_chat_member=AsyncMock(side_effect=RuntimeError("member list is inaccessible")))
        with self.assertLogs("services.subscription", level="ERROR") as logs:
            self.assertTrue(await subscription.may_use(bot, 5))
        self.assertIn("member list is inaccessible", logs.output[0])

    async def test_admins_are_never_checked(self):
        bot = channel(member("left"))
        self.assertTrue(await subscription.may_use(bot, ADMIN))
        bot.get_chat_member.assert_not_awaited()

    async def test_teachers_skip_the_channel(self):
        await users.touch_user({"id": ADMIN, "first_name": "Admin"})
        center = await centers.create_center("Marstif", ADMIN)
        await centers.join_as_teacher(center["teacher_code"], 9)
        bot = channel(member("left"))
        self.assertTrue(await subscription.may_use(bot, 9))
        self.assertFalse(await subscription.may_use(bot, 10))

    async def test_the_switch_turns_the_requirement_off(self):
        bot = channel(member("left"))
        with patch.object(config, "REQUIRE_SUBSCRIPTION", False):
            self.assertTrue(await subscription.may_use(bot, 5))
        bot.get_chat_member.assert_not_awaited()


class MiniAppGateTest(ApiTestCase):
    async def test_outsider_is_refused_with_the_channel_link(self):
        self.bot.outsiders.add(7)
        data = await self.call("GET", "/api/v1/bootstrap", user=7, expect=403)
        self.assertEqual(data, {"error": "not_subscribed", "channel": config.CHANNEL_URL})
        self.assertIsNone(await users.get_user(7))

    async def test_members_and_admins_get_in(self):
        await self.call("GET", "/api/v1/bootstrap", user=8, expect=200)
        self.bot.outsiders.add(ADMIN)
        await self.call("GET", "/api/v1/bootstrap", user=ADMIN, expect=200)

    async def test_joining_opens_the_app(self):
        self.bot.outsiders.add(7)
        await self.call("GET", "/api/v1/bootstrap", user=7, expect=403)
        self.bot.outsiders.discard(7)
        subscription.forget(7)
        await self.call("GET", "/api/v1/bootstrap", user=7, expect=200)
