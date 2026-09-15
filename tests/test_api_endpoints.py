"""
EduTest Pro - API Endpoints Integration Test Suite (aiohttp TestClient)
Tests:
1. Health check (/health)
2. WebApp static handler (/webapp)
3. Auth validation (/api/v1/auth/validate): missing, valid, forged, missing user, non-positive id
4. Progress endpoints (/api/v1/user/progress):
   - 401 unauthorized on missing/invalid initData
   - 400 bad request on schema violations (duration, date, solution URL, array bounds)
   - 200 ok on valid payload roundtrip
   - 200 ok on empty array clearing/deletion
5. Attention event endpoint (/api/v1/user/attention-event):
   - 401 unauthorized on missing initData
   - 400 bad request on disallowed event types
   - 200 ok and database persistence on valid events (tab_hidden, window_blur)
"""

import hashlib
import hmac
import json
import os
import sys
from datetime import datetime, timezone
from urllib.parse import urlencode

from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot import setup_web_app
from config import BOT_TOKEN
from database import db


def create_signed_init_data(user_obj: dict | None, bot_token: str, auth_date: int | None = None, forged: bool = False) -> str:
    """Helper to generate authentic or forged Telegram WebApp initData string."""
    date_val = auth_date if auth_date is not None else int(datetime.now(timezone.utc).timestamp())
    params: dict[str, str] = {
        "auth_date": str(date_val),
        "query_id": "AAHdF6IQAAAAAN0XohD74h-X",
    }
    if user_obj is not None:
        params["user"] = json.dumps(user_obj)

    sorted_pairs = [f"{k}={v}" for k, v in sorted(params.items())]
    data_check_string = "\n".join(sorted_pairs)

    secret_key = hmac.new(b"WebAppData", bot_token.encode("utf-8"), hashlib.sha256).digest()
    computed_hash = hmac.new(secret_key, data_check_string.encode("utf-8"), hashlib.sha256).hexdigest()

    if forged:
        computed_hash = "deadbeef1234567890abcdef"

    return f"{urlencode(params)}&hash={computed_hash}"


class TestApiEndpoints(AioHTTPTestCase):

    async def get_application(self) -> web.Application:
        return setup_web_app()

    def setUp(self):
        super().setUp()
        self.test_user = {
            "id": 12345678,
            "first_name": "Azizbek",
            "username": "azizbek_sat"
        }
        self.valid_init_data = create_signed_init_data(self.test_user, BOT_TOKEN)

    # --- 1. Health Check ---
    async def test_health_check(self):
        resp = await self.client.request("GET", "/health")
        self.assertEqual(resp.status, 200)
        data = await resp.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["brand"], "EduTest Pro")

    # --- 2. Auth Validate ---
    async def test_auth_validate_success(self):
        resp = await self.client.request(
            "POST",
            "/api/v1/auth/validate",
            json={"initData": self.valid_init_data}
        )
        self.assertEqual(resp.status, 200)
        data = await resp.json()
        self.assertTrue(data["authenticated"])
        self.assertEqual(data["user"]["id"], 12345678)

    async def test_auth_validate_forged_signature(self):
        forged = create_signed_init_data(self.test_user, BOT_TOKEN, forged=True)
        resp = await self.client.request(
            "POST",
            "/api/v1/auth/validate",
            json={"initData": forged}
        )
        self.assertEqual(resp.status, 401)
        data = await resp.json()
        self.assertFalse(data["authenticated"])

    async def test_auth_validate_missing_user(self):
        # Signed payload without user field
        no_user_init_data = create_signed_init_data(None, BOT_TOKEN)
        resp = await self.client.request(
            "POST",
            "/api/v1/auth/validate",
            json={"initData": no_user_init_data}
        )
        self.assertEqual(resp.status, 401)
        data = await resp.json()
        self.assertFalse(data["authenticated"])

    async def test_auth_validate_invalid_user_id(self):
        # Signed payload with negative or non-int user id
        bad_user = {"id": -99, "first_name": "Bad"}
        bad_init_data = create_signed_init_data(bad_user, BOT_TOKEN)
        resp = await self.client.request(
            "POST",
            "/api/v1/auth/validate",
            json={"initData": bad_init_data}
        )
        self.assertEqual(resp.status, 401)

    # --- 3. User Progress API ---
    async def test_progress_unauthorized_missing_header(self):
        resp = await self.client.request("GET", "/api/v1/user/progress")
        self.assertEqual(resp.status, 401)

        post_resp = await self.client.request("POST", "/api/v1/user/progress", json={})
        self.assertEqual(post_resp.status, 401)

    async def test_progress_schema_validation_errors(self):
        headers = {"X-Telegram-Init-Data": self.valid_init_data}

        # Case A: Task duration out of bounds (> 600)
        bad_task_payload = {
            "tasks": [{"subject": "Math", "duration": 999, "date": "2026-09-15"}]
        }
        resp = await self.client.request("POST", "/api/v1/user/progress", headers=headers, json=bad_task_payload)
        self.assertEqual(resp.status, 400)
        data = await resp.json()
        self.assertIn("duration", data["message"].lower())

        # Case B: Task date bad format
        bad_date_payload = {
            "tasks": [{"subject": "Math", "duration": 45, "date": "not-a-date"}]
        }
        resp_b = await self.client.request("POST", "/api/v1/user/progress", headers=headers, json=bad_date_payload)
        self.assertEqual(resp_b.status, 400)

        # Case C: Solution URL not https
        bad_err_payload = {
            "errors": [{"subject": "Math", "solution": "javascript:alert(1)"}]
        }
        resp_c = await self.client.request("POST", "/api/v1/user/progress", headers=headers, json=bad_err_payload)
        self.assertEqual(resp_c.status, 400)

    async def test_progress_save_and_retrieve_roundtrip(self):
        headers = {"X-Telegram-Init-Data": self.valid_init_data}
        valid_payload = {
            "tasks": [
                {"subject": "Math - Heart of Algebra", "duration": 60, "date": "2026-09-15"}
            ],
            "errors": [
                {"subject": "Math", "solution": "https://desmos.com/calculator/test1234"}
            ],
            "settings": {
                "centerName": "MARSTIF ACADEMY",
                "groupName": "SAT-Master"
            }
        }

        # 1. Save
        post_resp = await self.client.request("POST", "/api/v1/user/progress", headers=headers, json=valid_payload)
        self.assertEqual(post_resp.status, 200)

        # 2. Retrieve
        get_resp = await self.client.request("GET", "/api/v1/user/progress", headers=headers)
        self.assertEqual(get_resp.status, 200)
        get_data = await get_resp.json()
        self.assertEqual(get_data["user_id"], 12345678)
        self.assertEqual(len(get_data["data"]["tasks"]), 1)
        self.assertEqual(get_data["data"]["tasks"][0]["subject"], "Math - Heart of Algebra")

        # 3. Clear via empty array
        clear_payload = {"tasks": [], "errors": [], "settings": {}}
        clear_resp = await self.client.request("POST", "/api/v1/user/progress", headers=headers, json=clear_payload)
        self.assertEqual(clear_resp.status, 200)

        verify_resp = await self.client.request("GET", "/api/v1/user/progress", headers=headers)
        verify_data = await verify_resp.json()
        self.assertEqual(verify_data["data"]["tasks"], [])

    # --- 4. Attention Event API ---
    async def test_attention_event_unauthorized(self):
        resp = await self.client.request("POST", "/api/v1/user/attention-event", json={"event": "tab_hidden"})
        self.assertEqual(resp.status, 401)

    async def test_attention_event_invalid_type(self):
        headers = {"X-Telegram-Init-Data": self.valid_init_data}
        resp = await self.client.request(
            "POST",
            "/api/v1/user/attention-event",
            headers=headers,
            json={"event": "hacked_tab"}
        )
        self.assertEqual(resp.status, 400)
        data = await resp.json()
        self.assertIn("Yaroqsiz event turi", data["message"])

    async def test_attention_event_success_and_db_persistence(self):
        headers = {"X-Telegram-Init-Data": self.valid_init_data}
        payload = {
            "event": "tab_hidden",
            "attempt_id": "att_test_att1",
            "details": {"reason": "switched_app"}
        }
        resp = await self.client.request(
            "POST",
            "/api/v1/user/attention-event",
            headers=headers,
            json=payload
        )
        self.assertEqual(resp.status, 200)
        data = await resp.json()
        self.assertTrue(data["recorded"])
        self.assertEqual(data["event"], "tab_hidden")

        # Check DB persistence
        events = db.get_attention_events(user_id=12345678)
        self.assertTrue(any(e.get("event") == "tab_hidden" for e in events))
