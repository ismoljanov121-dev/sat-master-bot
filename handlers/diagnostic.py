"""
SAT AI Bot - Diagnostic Quiz Handler (Father Mode v6.0 / Production-Ready)
Interactive high-yield Digital SAT Math diagnostic engine.
Features:
- Strict HTML escaping of math formulas, topic labels, and user inputs
- Dual-layer message rendering with automatic plain-text fallback on entity errors
- Bulletproof try...finally callback acknowledgments (zero spinning/frozen buttons)
- Persistent session storage in db.local_cache with in-memory caching
- Graceful error recovery and 'message is not modified' suppression
"""

import html
import json
import logging
import os
import re
from typing import Any

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)

from config import WEBAPP_URL
from database import db
from handlers.score_surgery import generate_surgery_report

logger = logging.getLogger("DiagnosticHandler")

router = Router()

# Load questions from JSON
QUESTIONS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "questions.json")
try:
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        QUESTIONS: list[dict[str, Any]] = json.load(f)
except Exception as e:
    logger.critical(f"Failed to load questions from {QUESTIONS_FILE}: {e}")
    QUESTIONS = []

# In-memory session cache backed by database local cache
USER_SESSIONS: dict[int, dict[str, Any]] = {}


def get_user_session(user_id: int, fallback_idx: int = 0) -> dict[str, Any]:
    """Retrieves the user's active diagnostic session from memory or persistent storage."""
    str_id = str(user_id)
    if user_id in USER_SESSIONS:
        return USER_SESSIONS[user_id]

    active_sessions = db.local_cache.setdefault("diagnostic_sessions", {})
    if str_id in active_sessions and isinstance(active_sessions[str_id], dict):
        USER_SESSIONS[user_id] = active_sessions[str_id]
        return active_sessions[str_id]

    new_session: dict[str, Any] = {
        "current_idx": fallback_idx,
        "correct": 0,
        "incorrect_items": [],
        "answered_indices": []
    }
    USER_SESSIONS[user_id] = new_session
    active_sessions[str_id] = new_session
    return new_session


def save_user_session(user_id: int, session: dict[str, Any]) -> None:
    """Saves session state into memory and persistent cache."""
    str_id = str(user_id)
    USER_SESSIONS[user_id] = session
    try:
        active_sessions = db.local_cache.setdefault("diagnostic_sessions", {})
        active_sessions[str_id] = session
        db._save_local_db()
    except Exception as e:
        logger.warning(f"Error persisting diagnostic session for {user_id}: {e}")


def clear_user_session(user_id: int) -> None:
    """Clears user session from memory and database."""
    str_id = str(user_id)
    USER_SESSIONS.pop(user_id, None)
    try:
        active_sessions = db.local_cache.setdefault("diagnostic_sessions", {})
        active_sessions.pop(str_id, None)
        db._save_local_db()
    except Exception as e:
        logger.warning(f"Error clearing diagnostic session for {user_id}: {e}")


async def safe_answer_callback(callback: CallbackQuery, text: str | None = None, show_alert: bool = False) -> None:
    """Answers a callback query safely without raising unhandled exceptions."""
    try:
        await callback.answer(text=text, show_alert=show_alert)
    except Exception as e:
        logger.debug(f"Ignored callback.answer failure: {e}")


async def safe_edit_message(
    callback: CallbackQuery,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None
) -> bool:
    """
    Edits a Telegram message safely using HTML parse_mode.
    If Telegram Bot API rejects the entities, automatically falls back to plain text.
    Silently ignores 'message is not modified' errors.
    """
    if not callback.message:
        return False

    try:
        await callback.message.edit_text(text, reply_markup=reply_markup, parse_mode="HTML")
        return True
    except TelegramBadRequest as e:
        err_msg = str(e).lower()
        if "message is not modified" in err_msg:
            return True
        logger.warning(f"HTML entity error in edit_message ({e}), initiating plain-text fallback...")
        try:
            # Strip all HTML tags and unescape entities for plain-text display
            plain_text = re.sub(r"<[^>]+>", "", text)
            plain_text = html.unescape(plain_text)
            await callback.message.edit_text(plain_text, reply_markup=reply_markup, parse_mode=None)
            return True
        except Exception as fallback_err:
            logger.error(f"Plain text fallback edit failed: {fallback_err}")
            return False
    except Exception as e:
        logger.error(f"Unexpected error in safe_edit_message: {e}")
        return False


def get_question_keyboard(q_idx: int) -> InlineKeyboardMarkup:
    """Builds inline keyboard with options A, B, C, D."""
    if not QUESTIONS or q_idx >= len(QUESTIONS):
        return InlineKeyboardMarkup(inline_keyboard=[])

    q = QUESTIONS[q_idx]
    buttons: list[list[InlineKeyboardButton]] = []
    row: list[InlineKeyboardButton] = []
    for opt in q.get("options", []):
        opt_key = str(opt.get("key", "")).strip()
        opt_text = str(opt.get("text", "")).strip()
        btn = InlineKeyboardButton(
            text=f"{opt_key}) {opt_text}",
            callback_data=f"ans_{q_idx}_{opt_key}"
        )
        row.append(btn)
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_after_answer_keyboard(q_idx: int, is_last: bool) -> InlineKeyboardMarkup:
    """Builds navigation and Desmos hack buttons after answering."""
    buttons: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text="⚡ Desmos Hack (10s yechim)", callback_data=f"hack_{q_idx}")],
    ]
    if not is_last:
        buttons.append([InlineKeyboardButton(text="Keyingi savol ➡️", callback_data=f"next_{q_idx + 1}")])
    else:
        buttons.append([InlineKeyboardButton(text="🔬 Rentgen Xulosasini Olish ➡️", callback_data="finish_quiz")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_hack_keyboard(q_idx: int, is_last: bool) -> InlineKeyboardMarkup:
    """Builds navigation after viewing Desmos cheatcode."""
    buttons: list[list[InlineKeyboardButton]] = []
    if not is_last:
        buttons.append([InlineKeyboardButton(text="Keyingi savol ➡️", callback_data=f"next_{q_idx + 1}")])
    else:
        buttons.append([InlineKeyboardButton(text="🔬 Rentgen Xulosasini Olish ➡️", callback_data="finish_quiz")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def format_question_text(q_idx: int, total: int, q: dict[str, Any]) -> str:
    """Builds question view with safe escaping and visual progress indicator."""
    topic = html.escape(str(q.get("topic", "Math")))
    question = html.escape(str(q.get("question", "")))
    progress = "▰" * (q_idx + 1) + "▱" * max(0, total - q_idx - 1)

    return (
        f"📝 <b>SAVOL {q_idx + 1} / {total}</b>\n"
        f"<i>{progress}</i>\n"
        f"🏷️ <i>Mavzu: {topic}</i>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"<b>{question}</b>\n\n"
        f"<i>To'g'ri javob variantini tanlang:</i>"
    )


def format_answer_result(is_correct: bool, correct_key: str, trap: str, explanation: str) -> str:
    """Builds answer explanation view with safe HTML escaping."""
    if is_correct:
        res_header = "✅ <b>BARAKALLA! JAVOB TO'G'RI!</b>\n"
    else:
        res_header = f"❌ <b>XATO! To'g'ri javob: {html.escape(correct_key)}</b>\n"

    esc_trap = html.escape(trap)
    esc_exp = html.escape(explanation)
    return (
        f"{res_header}"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ <b>Tuzoq tahlili:</b> {esc_trap}\n\n"
        f"📖 <b>Klassik yechim:</b> {esc_exp}"
    )


def format_hack_text(desmos_hack: str) -> str:
    """Builds Desmos hack view with safe HTML escaping."""
    esc_hack = html.escape(desmos_hack)
    return (
        f"🚀 <b>DESMOS CHEATCODE &amp; HACK</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{esc_hack}\n\n"
        f"💡 <i>Ushbu usul bilan formulalarni eslash shart emas!</i>"
    )


async def send_question(callback: CallbackQuery, q_idx: int) -> None:
    """Sends question at index q_idx to the user."""
    total = len(QUESTIONS)
    if total == 0:
        await safe_edit_message(callback, "❌ <i>Savollar bazasi topilmadi.</i>")
        return

    if q_idx >= total:
        await finish_quiz(callback)
        return

    q = QUESTIONS[q_idx]
    text = format_question_text(q_idx, total, q)
    kb = get_question_keyboard(q_idx)
    await safe_edit_message(callback, text=text, reply_markup=kb)


@router.message(Command("diagnostic"))
async def cmd_diagnostic(message: Message) -> None:
    """Initializes diagnostic test from slash command."""
    user_id = message.from_user.id
    total = len(QUESTIONS)
    if total == 0:
        await message.answer("❌ <i>Savollar bazasi yuklanmagan.</i>")
        return

    session = {
        "current_idx": 0,
        "correct": 0,
        "incorrect_items": [],
        "answered_indices": []
    }
    save_user_session(user_id, session)

    q = QUESTIONS[0]
    text = format_question_text(0, total, q)
    kb = get_question_keyboard(0)

    try:
        await message.answer(text, reply_markup=kb, parse_mode="HTML")
    except Exception as e:
        logger.warning(f"Failed to send HTML question via message: {e}")
        plain = re.sub(r"<[^>]+>", "", text)
        await message.answer(plain, reply_markup=kb, parse_mode=None)


@router.callback_query(F.data == "start_diagnostic")
async def start_quiz(callback: CallbackQuery) -> None:
    """Starts or restarts the diagnostic quiz from inline button."""
    try:
        user_id = callback.from_user.id
        session = {
            "current_idx": 0,
            "correct": 0,
            "incorrect_items": [],
            "answered_indices": []
        }
        save_user_session(user_id, session)
        await send_question(callback, q_idx=0)
    finally:
        await safe_answer_callback(callback)


@router.callback_query(F.data.startswith("ans_"))
async def handle_answer(callback: CallbackQuery) -> None:
    """Evaluates the selected answer option and reveals explanation with idempotency."""
    try:
        user_id = callback.from_user.id
        data_parts = (callback.data or "").split("_")
        if len(data_parts) < 3:
            logger.error(f"Malformed answer callback data: {callback.data}")
            return

        q_idx = int(data_parts[1])
        selected_key = data_parts[2].upper()

        if q_idx >= len(QUESTIONS):
            logger.error(f"Question index out of bounds: {q_idx}")
            return

        session = get_user_session(user_id, fallback_idx=q_idx)
        q = QUESTIONS[q_idx]

        correct_key = str(q.get("correct", "")).strip().upper()
        is_correct = (selected_key == correct_key)
        is_last = (q_idx == len(QUESTIONS) - 1)

        # Idempotency guard: only record score change if not already answered
        answered_indices = session.setdefault("answered_indices", [])
        if q_idx not in answered_indices:
            answered_indices.append(q_idx)
            if is_correct:
                session["correct"] = session.get("correct", 0) + 1
            else:
                session.setdefault("incorrect_items", []).append(q)

        session["current_idx"] = q_idx
        save_user_session(user_id, session)

        res_body = format_answer_result(
            is_correct=is_correct,
            correct_key=correct_key,
            trap=str(q.get("trap", "")),
            explanation=str(q.get("explanation", ""))
        )
        kb = get_after_answer_keyboard(q_idx, is_last)
        await safe_edit_message(callback, text=res_body, reply_markup=kb)
    finally:
        await safe_answer_callback(callback)


@router.callback_query(F.data.startswith("hack_"))
async def show_desmos_hack(callback: CallbackQuery) -> None:
    """Displays the 10-second Desmos cheatcode for the question."""
    try:
        data_parts = (callback.data or "").split("_")
        if len(data_parts) < 2:
            return

        q_idx = int(data_parts[1])
        if q_idx >= len(QUESTIONS):
            return

        q = QUESTIONS[q_idx]
        is_last = (q_idx == len(QUESTIONS) - 1)

        hack_text = format_hack_text(str(q.get("desmos_hack", "")))
        kb = get_hack_keyboard(q_idx, is_last)
        await safe_edit_message(callback, text=hack_text, reply_markup=kb)
    finally:
        await safe_answer_callback(callback)


@router.callback_query(F.data.startswith("next_"))
async def next_question(callback: CallbackQuery) -> None:
    """Navigates to the next question."""
    try:
        data_parts = (callback.data or "").split("_")
        if len(data_parts) < 2:
            return

        q_idx = int(data_parts[1])
        await send_question(callback, q_idx)
    finally:
        await safe_answer_callback(callback)


@router.callback_query(F.data == "finish_quiz")
async def finish_quiz(callback: CallbackQuery) -> None:
    """Generates the final surgical diagnosis report and saves to DB."""
    try:
        user_id = callback.from_user.id
        session = get_user_session(user_id)
        user_name = callback.from_user.full_name or callback.from_user.first_name or "Abituriyent"

        incorrect_items = session.get("incorrect_items", [])
        correct_count = session.get("correct", 0)
        total_questions = len(QUESTIONS)

        points_lost = sum(item.get("points_lost", 20) for item in incorrect_items)
        estimated_score = max(800 - points_lost, 400)
        weaknesses = [str(item.get("topic", "General")) for item in incorrect_items]

        # Save to Database (MongoDB Atlas + local cache)
        try:
            await db.save_quiz_result(
                user_id=user_id,
                score=estimated_score,
                correct=correct_count,
                total=total_questions,
                weaknesses=weaknesses
            )
        except Exception as db_err:
            logger.error(f"Error saving quiz result to DB: {db_err}")

        # Generate surgery report
        report = generate_surgery_report(
            user_name=user_name,
            total_q=total_questions,
            correct_q=correct_count,
            incorrect_items=incorrect_items
        )

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Testni Qayta Topshirish", callback_data="start_diagnostic")],
            [
                InlineKeyboardButton(text="⚡ Desmos Hiylalari", callback_data="desmos_catalog"),
                InlineKeyboardButton(text="📊 Mening Natijam", callback_data="my_stats")
            ],
            [
                InlineKeyboardButton(text="📱 Shaxsiy Rejim & 60 Kunlik Tracker (Web App)", web_app=WebAppInfo(url=WEBAPP_URL))
            ],
            [
                InlineKeyboardButton(text="👥 Do'stlarni Taklif Qilish (VIP)", callback_data="referral_menu"),
                InlineKeyboardButton(text="⬅️ Asosiy Menyu", callback_data="back_to_menu")
            ]
        ])

        await safe_edit_message(callback, text=report, reply_markup=kb)

        # Clear session after successful completion
        clear_user_session(user_id)
    finally:
        await safe_answer_callback(callback)
