"""
Channel membership check. Students must join the channel before they use the bot and the Mini App.

Answers are cached for a short time. When Telegram cannot answer, the user is let in and the admins get an alert,
because a broken check must not lock every student out.
"""

import logging
import time
from typing import Any, Optional

from aiogram.enums import ChatMemberStatus

import config
from services import centers

logger = logging.getLogger(__name__)

MEMBER_TTL_SECONDS = 600
# Short, so a student who has just joined gets in on the next tap.
OUTSIDER_TTL_SECONDS = 5
FAILURE_TTL_SECONDS = 60
MAX_CACHED_USERS = 50_000
MEMBER_STATUSES = {ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER}

_cache: dict[int, tuple[bool, float]] = {}


def forget(user_id: Optional[int] = None) -> None:
    """Drops cached answers for one user, or for everyone."""
    if user_id is None:
        _cache.clear()
    else:
        _cache.pop(user_id, None)


def _remember(user_id: int, joined: bool, ttl: float) -> bool:
    if len(_cache) >= MAX_CACHED_USERS:
        _cache.clear()
    _cache[user_id] = (joined, time.monotonic() + ttl)
    return joined


async def is_member(bot: Any, user_id: int, *, fresh: bool = False) -> bool:
    """True when the user is in the channel. Also True when the check is off or Telegram cannot answer."""
    if not config.REQUIRE_SUBSCRIPTION or bot is None:
        return True
    cached = _cache.get(user_id)
    if cached is not None and not fresh and cached[1] > time.monotonic():
        return cached[0]
    try:
        member = await bot.get_chat_member(config.CHANNEL_ID, user_id)
    except Exception as e:
        logger.error("Channel membership check failed, letting the user in: %s: %s", type(e).__name__, str(e)[:200])
        return _remember(user_id, True, FAILURE_TTL_SECONDS)
    status = member.status
    joined = status in MEMBER_STATUSES or (status == ChatMemberStatus.RESTRICTED and bool(getattr(member, "is_member", False)))
    return _remember(user_id, joined, MEMBER_TTL_SECONDS if joined else OUTSIDER_TTL_SECONDS)


async def may_use(bot: Any, user_id: int, *, fresh: bool = False) -> bool:
    """Admins and teachers skip the requirement. Everyone else must be in the channel."""
    if not config.REQUIRE_SUBSCRIPTION or centers.is_admin(user_id):
        return True
    if await is_member(bot, user_id, fresh=fresh):
        return True
    return await centers.is_staff(user_id)
