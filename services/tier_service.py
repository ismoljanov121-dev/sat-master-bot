"""
EduTest Pro - Tier & Subscription Service
Manages FREE and PRO entitlements, daily question allowances (50/day Free, 150/day Pro),
weekly full mock exam quotas (1/week Free, unlimited Pro), fair-use limits,
and Beta Early-Access mode.
"""

from datetime import datetime, timezone
import logging
from typing import Any

from config import (
    FREE_DAILY_QUESTIONS_LIMIT,
    FREE_WEEKLY_MOCKS_LIMIT,
    PAYMENTS_ENABLED,
    PRO_BETA_MODE,
    PRO_DAILY_FAIR_USE_LIMIT,
)
from database import TASHKENT_TZ, db, get_tashkent_now_str

logger = logging.getLogger("TierService")

# Official Telegram Stars (XTR) Pricing Reference (Inactive when PAYMENTS_ENABLED=False)
TIER_PLANS: dict[str, dict[str, Any]] = {
    "pro_1m": {
        "id": "pro_1m",
        "title": "👑 1 Oylik PRO (Intensiv)",
        "description": "30 kun to'liq mock imtihonlar, shaxsiy reja, 'Xatomni tuzat' va chuqur tahlil",
        "stars": 250,
        "days": 30,
        "label": "1 Oy — 250 ⭐",
        "badge": "PRO 1M"
    },
    "pro_3m": {
        "id": "pro_3m",
        "title": "🏆 3 Oylik PRO (SAT Mavsumi)",
        "description": "90 kun to'liq tayyorgarlik kursi. Rasmiy imtihongacha barcha ilg'or imkoniyatlar",
        "stars": 600,
        "days": 90,
        "label": "3 Oy — 600 ⭐",
        "badge": "PRO 3M"
    },
    "pro_7d": {
        "id": "pro_7d",
        "title": "⚡ 7 Kunlik PRO (Sprint)",
        "description": "7 kunlik intensiv takrorlash: to'liq mocklar va zaif mavzular bo'yicha tezkor mashq",
        "stars": 75,
        "days": 7,
        "label": "7 Kun — 75 ⭐",
        "badge": "PRO 7D"
    }
}


def get_today_date_str() -> str:
    """Returns today's date in Tashkent timezone (YYYY-MM-DD)."""
    return datetime.now(TASHKENT_TZ).strftime("%Y-%m-%d")


def is_user_pro(user_id: int) -> bool:
    """
    Checks if user is entitled to PRO features.
    During launch/beta phase (PRO_BETA_MODE=True), ALL users are granted PRO features for free.
    When beta ends, checks active paid subscription in database.
    """
    if PRO_BETA_MODE:
        return True

    sub = db.get_user_subscription(user_id)
    if not sub:
        return False

    if not sub.get("is_active", False):
        return False

    expires_iso = sub.get("expires_at")
    if not expires_iso:
        return False

    try:
        exp_dt = datetime.fromisoformat(expires_iso)
        if exp_dt.tzinfo is None:
            exp_dt = exp_dt.replace(tzinfo=timezone.utc)
        return exp_dt > datetime.now(timezone.utc)
    except Exception as e:
        logger.error(f"Error parsing subscription expiration date for user {user_id}: {e}")
        return False


def get_user_tier(user_id: int) -> dict[str, Any]:
    """
    Returns complete user tier metadata.
    """
    if PRO_BETA_MODE:
        return {
            "tier": "pro_beta",
            "tier_label": "👑 PRO (Beta)",
            "badge": "PRO BETA",
            "is_pro": True,
            "is_beta": True,
            "plan_id": "pro_beta",
            "expires_at": "Beta davomida bepul",
            "daily_limit": PRO_DAILY_FAIR_USE_LIMIT,
            "weekly_mock_limit": 999,
            "fair_use_active": True,
            "payments_enabled": PAYMENTS_ENABLED
        }

    pro = is_user_pro(user_id)
    sub = db.get_user_subscription(user_id)

    if pro and sub:
        exp_raw = sub.get("expires_at")
        try:
            exp_dt = datetime.fromisoformat(exp_raw)
            if exp_dt.tzinfo is None:
                exp_dt = exp_dt.replace(tzinfo=timezone.utc)
            tashkent_exp = exp_dt.astimezone(TASHKENT_TZ).strftime("%Y-%m-%d %H:%M")
        except Exception:
            tashkent_exp = exp_raw[:16] if exp_raw else "Faol"

        return {
            "tier": "pro",
            "tier_label": "👑 PRO",
            "badge": "PRO",
            "is_pro": True,
            "is_beta": False,
            "plan_id": sub.get("plan_id", "pro_1m"),
            "expires_at": tashkent_exp,
            "daily_limit": PRO_DAILY_FAIR_USE_LIMIT,
            "weekly_mock_limit": 999,
            "fair_use_active": True,
            "payments_enabled": PAYMENTS_ENABLED
        }

    return {
        "tier": "free",
        "tier_label": "🆓 FREE",
        "badge": "FREE",
        "is_pro": False,
        "is_beta": False,
        "plan_id": "free",
        "expires_at": None,
        "daily_limit": FREE_DAILY_QUESTIONS_LIMIT,
        "weekly_mock_limit": FREE_WEEKLY_MOCKS_LIMIT,
        "fair_use_active": False,
        "payments_enabled": PAYMENTS_ENABLED
    }


def get_daily_question_status(user_id: int) -> dict[str, Any]:
    """
    Calculates current daily question usage against the user's tier limit.
    """
    tier_info = get_user_tier(user_id)
    today_str = get_today_date_str()
    used_today = db.get_daily_usage(user_id, today_str)
    limit = tier_info["daily_limit"]
    remaining = max(0, limit - used_today)

    return {
        "date": today_str,
        "answered_today": used_today,
        "daily_limit": limit,
        "remaining_today": remaining,
        "is_limit_reached": used_today >= limit,
        "tier": tier_info["tier"],
        "is_pro": tier_info["is_pro"],
        "is_beta": tier_info.get("is_beta", False),
        "weekly_mocks_used": db.get_weekly_mocks_used(user_id),
        "weekly_mocks_limit": tier_info.get("weekly_mock_limit", FREE_WEEKLY_MOCKS_LIMIT)
    }


def can_answer_practice_question(
    user_id: int,
    is_mistake_practice: bool = False,
    is_review: bool = False
) -> tuple[bool, str]:
    """
    Verifies whether the user is allowed to receive/answer another practice question.
    - Practicing mistakes or re-practicing previously solved questions is ALWAYS UNLIMITED and free.
    - Free tier has a generous 50 new questions/day limit.
    - Pro tier has a 150 questions/day fair use limit to prevent automated scraping.
    """
    if is_mistake_practice or is_review:
        return True, "Xatolar ustida mashq har doim cheklovsiz."

    status = get_daily_question_status(user_id)
    if not status["is_limit_reached"]:
        return True, "Ruxsat berildi."

    if not status["is_pro"]:
        return False, (
            f"Bugungi bepul {FREE_DAILY_QUESTIONS_LIMIT} ta yangi savol limitingiz to'ldi. 🎯\n"
            f"Xatolaringiz ustida 'Xatolarim' bo'limida cheklovsiz ishlashingiz "
            f"yoki ertaga yangi savollar bilan davom etishingiz mumkin!"
        )

    return False, (
        f"Bugungi {PRO_DAILY_FAIR_USE_LIMIT} ta savollik xavfsiz mashq chegarasiga yetdingiz (Fair Use). "
        f"Miyangizga dam bering va ertaga yangi kuch bilan davom eting! 🌟"
    )


async def record_question_attempt(
    user_id: int,
    is_mistake_practice: bool = False,
    is_review: bool = False,
    is_mock: bool = False
) -> int:
    """
    Increments daily usage counter for new practice questions.
    Mistakes, re-reviews, and mock exam questions DO NOT consume the daily practice limit.
    """
    if is_mistake_practice or is_review:
        return 0

    if is_mock:
        # Mock exams have their own separate weekly tracking
        return 0

    today_str = get_today_date_str()
    new_count = await db.increment_daily_usage(user_id, today_str, 1)
    return new_count


def can_take_full_mock(user_id: int) -> tuple[bool, str]:
    """
    Checks if user is entitled to start a full-length mock exam.
    - In PRO / PRO_BETA: Unlimited full mocks.
    - In FREE: 1 free full mock exam per calendar week.
    """
    if is_user_pro(user_id):
        return True, "To'liq mock testlar ochiq (PRO / Beta)."

    used_this_week = db.get_weekly_mocks_used(user_id)
    if used_this_week < FREE_WEEKLY_MOCKS_LIMIT:
        return True, f"Haftalik bepul mock imtihon ruxsati ({used_this_week + 1}/{FREE_WEEKLY_MOCKS_LIMIT})."

    return False, (
        f"Bu haftalik bepul {FREE_WEEKLY_MOCKS_LIMIT} ta to'liq mock imtihonidan foydalandingiz. "
        f"Yangi haftada (Dushanbadan) yana bitta bepul to'liq mock ochiladi. "
        f"Diagnostika va kunlik 50 ta mashq esa doimo ochiq!"
    )


def can_access_weak_topic_plan(user_id: int) -> tuple[bool, str]:
    """
    Checks if user can access Adaptive Weak Domain Drills & Surgery.
    In PRO_BETA_MODE, freely open to all students.
    """
    if is_user_pro(user_id):
        return True, "Shaxsiy reja tasdiqlandi (PRO / Beta)."
    return False, "Kuchsiz mavzular bo'yicha shaxsiy reja PRO a'zolarga taqdim etiladi."


def get_available_plans() -> dict[str, dict[str, Any]]:
    """Returns available Telegram Stars subscription plans."""
    return TIER_PLANS

