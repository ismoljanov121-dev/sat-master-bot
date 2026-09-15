"""
EduTest Pro - Telegram WebApp Authentication & Security Service
Implements official Telegram WebApp HMAC-SHA256 initData validation,
replay attack mitigation via auth_date window, and payload sanitization.
"""

import hashlib
import hmac
import json
import logging
from datetime import datetime, timezone
from typing import Any
from urllib.parse import parse_qsl

from config import BOT_TOKEN

logger = logging.getLogger("AuthService")

# Maximum acceptable age for initData (24 hours = 86400 seconds)
MAX_AUTH_AGE_SECONDS = 86400
# Clock skew allowance (5 minutes = 300 seconds)
MAX_FUTURE_SKEW_SECONDS = 300


def validate_telegram_init_data(
    init_data_raw: str,
    bot_token: str | None = None
) -> tuple[bool, dict[str, Any] | None, str]:
    """
    Validates Telegram WebApp initData string using HMAC-SHA256.
    
    Steps:
    1. Parse query string key-values.
    2. Extract and pop 'hash'.
    3. Construct data_check_string by sorting keys and joining with newline.
    4. Compute secret_key = HMAC_SHA256("WebAppData", bot_token).
    5. Compute signature = HMAC_SHA256(secret_key, data_check_string).
    6. Verify signature and check auth_date expiration.
    
    Returns: (is_valid, user_data_dict, error_or_success_message)
    """
    token = bot_token or BOT_TOKEN
    if not token:
        return False, None, "BOT_TOKEN mavjud emas"

    if not init_data_raw or not isinstance(init_data_raw, str):
        return False, None, "Bo'sh yoki noto'g'ri initData"

    try:
        # Parse query string into dictionary
        parsed_items = dict(parse_qsl(init_data_raw, keep_blank_values=True))
        received_hash = parsed_items.pop("hash", None)

        if not received_hash:
            return False, None, "initData ichida 'hash' imzosi topilmadi"

        # Build data check string sorted by key
        sorted_pairs = [f"{k}={v}" for k, v in sorted(parsed_items.items())]
        data_check_string = "\n".join(sorted_pairs)

        # Official Telegram WebApp secret key derivation
        secret_key = hmac.new(b"WebAppData", token.encode("utf-8"), hashlib.sha256).digest()
        computed_hash = hmac.new(
            secret_key,
            data_check_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        # Constant-time comparison
        if not hmac.compare_digest(computed_hash.lower(), received_hash.lower()):
            return False, None, "Noto'g'ri kriptografik imzo (Invalid hash)"

        # Validate auth_date freshness
        auth_date_raw = parsed_items.get("auth_date")
        if not auth_date_raw:
            return False, None, "auth_date topilmadi"

        try:
            auth_timestamp = int(auth_date_raw)
        except ValueError:
            return False, None, "auth_date formati noto'g'ri"

        now_timestamp = int(datetime.now(timezone.utc).timestamp())
        age_seconds = now_timestamp - auth_timestamp

        if age_seconds > MAX_AUTH_AGE_SECONDS:
            return False, None, f"Avtorizatsiya muddati o'tgan ({age_seconds} soniya > {MAX_AUTH_AGE_SECONDS})"

        if age_seconds < -MAX_FUTURE_SKEW_SECONDS:
            return False, None, "auth_date kelajak vaqtida berilgan (Soat nomuvofiqligi)"

        # Parse user payload
        user_json_str = parsed_items.get("user")
        user_data: dict[str, Any] = {}
        if user_json_str:
            try:
                user_data = json.loads(user_json_str)
            except Exception as e:
                logger.warning(f"Could not parse 'user' JSON: {e}")
                return False, None, "User ma'lumotlari JSON formatida emas"

        return True, user_data, "Muvaffaqiyatli autentifikatsiya qilindi"

    except Exception as e:
        logger.error(f"Unexpected error in validate_telegram_init_data: {e}")
        return False, None, f"Tekshirishda xatolik: {e!s}"
