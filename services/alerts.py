"""
Sends ERROR-level logs to the admins on Telegram, so a failure does not go unnoticed.
"""

import asyncio
import html
import logging
import time

from aiogram import Bot

COOLDOWN_SECONDS = 300
MAX_TEXT = 900


class TelegramAlertHandler(logging.Handler):
    def __init__(self, bot: Bot, admin_ids: frozenset[int]):
        super().__init__(level=logging.ERROR)
        self.bot = bot
        self.admin_ids = admin_ids
        self.last_sent: dict[str, float] = {}

    def emit(self, record: logging.LogRecord) -> None:
        # Our own failure to reach Telegram must not trigger another alert.
        if record.name.startswith(("aiogram", "aiohttp", __name__)):
            return
        key = f"{record.name}:{record.lineno}"
        now = time.monotonic()
        if now - self.last_sent.get(key, -COOLDOWN_SECONDS) < COOLDOWN_SECONDS:
            return
        self.last_sent[key] = now
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return
        text = self.format(record)[-MAX_TEXT:]
        loop.create_task(self._send(f"🚨 <b>Botda xatolik</b>\n<code>{html.escape(text)}</code>"))

    async def _send(self, text: str) -> None:
        for admin_id in self.admin_ids:
            try:
                await self.bot.send_message(admin_id, text)
            except Exception as e:
                logging.getLogger(__name__).info("Alert not delivered: %s", type(e).__name__)


def install(bot: Bot, admin_ids: frozenset[int]) -> None:
    if admin_ids:
        logging.getLogger().addHandler(TelegramAlertHandler(bot, admin_ids))
