import hashlib
import hmac
import json
import time
import unittest
from types import SimpleNamespace
from urllib.parse import urlencode

from aiohttp.test_utils import TestClient, TestServer

from bot import create_web_app
from config import BOT_TOKEN
from database import SCHEMA, db
from services import subscription

TABLES = [statement.split()[5] for statement in SCHEMA if statement.startswith("CREATE TABLE")]


def init_data(user_id: int, first_name: str = "Ali", age_seconds: int = 0, token: str = BOT_TOKEN) -> str:
    fields = {
        "auth_date": str(int(time.time()) - age_seconds),
        "query_id": "AAH",
        "user": json.dumps({"id": user_id, "first_name": first_name, "language_code": "uz"}),
    }
    check = "\n".join(f"{key}={value}" for key, value in sorted(fields.items()))
    secret = hmac.new(b"WebAppData", token.encode(), hashlib.sha256).digest()
    fields["hash"] = hmac.new(secret, check.encode(), hashlib.sha256).hexdigest()
    return urlencode(fields)


class DatabaseTestCase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        subscription.forget()
        await db.connect()
        for table in TABLES:
            await db.execute(f"DELETE FROM {table}")

    async def asyncTearDown(self):
        await db.close()


class FakeBot:
    """Records what the app tried to send through Telegram."""

    def __init__(self):
        self.messages = []
        self.documents = []
        # Users who have not joined the channel. Everyone else is a member.
        self.outsiders = set()

    async def get_chat_member(self, chat_id, user_id):
        return SimpleNamespace(status="left" if user_id in self.outsiders else "member")

    async def send_message(self, chat_id, text, **kwargs):
        self.messages.append((chat_id, text))

    async def send_document(self, chat_id, document, **kwargs):
        self.documents.append((chat_id, document))


class ApiTestCase(DatabaseTestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.bot = FakeBot()
        self.client = TestClient(TestServer(create_web_app(self.bot)))
        await self.client.start_server()

    async def asyncTearDown(self):
        await self.client.close()
        await super().asyncTearDown()

    async def call(self, method: str, path: str, user: int = 1, body=None, expect: int | None = None):
        headers = {"X-Telegram-Init-Data": init_data(user)}
        response = await self.client.request(method, path, headers=headers, json=body)
        data = await response.json()
        if expect is not None:
            self.assertEqual(response.status, expect, data)
        return data
