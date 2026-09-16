"""
EduTest Pro - Student Feedback & Suggestions Handler
Enables students to submit feedback, report tricky questions, and suggest improvements.
"""

import html
import logging
from typing import Any

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import ADMIN_IDS
from database import db

logger = logging.getLogger("FeedbackHandler")

router = Router()


class FeedbackState(StatesGroup):
    waiting_for_feedback = State()


def get_feedback_prompt_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="fb_cancel")],
        [InlineKeyboardButton(text="⬅️ Bosh Menyu", callback_data="back_to_menu")]
    ])


@router.message(Command("feedback"))
@router.message(Command("taklif"))
async def cmd_feedback(message: Message, state: FSMContext):
    await state.set_state(FeedbackState.waiting_for_feedback)
    text = (
        "💬 <b>TAKLIF VA FIKRLAR (STUDENT FEEDBACK)</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Biz sizning fikringizni juda qadrlaymiz! Iltimos, quyidagilardan birini yozib qoldiring:\n\n"
        "• Bot yoki Mini App'da qaysi imkoniyat sizga eng ko'p yoqdi?\n"
        "• Qaysi savolda noaniqlik yoki xato uchratdingiz?\n"
        "• SAT tayyorgarligingiz uchun yana qanday yangi funksiya qo'shishimizni xohlaysiz?\n\n"
        "✍️ <i>Fikringizni bitta xabar ko'rinishida yozib yuboring:</i>"
    )
    await message.answer(text, reply_markup=get_feedback_prompt_keyboard(), parse_mode="HTML")


@router.callback_query(F.data == "send_feedback_prompt")
async def cb_feedback_prompt(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FeedbackState.waiting_for_feedback)
    text = (
        "💬 <b>TAKLIF VA FIKRLAR (STUDENT FEEDBACK)</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Biz sizning fikringizni juda qadrlaymiz! Iltimos, quyidagilardan birini yozib qoldiring:\n\n"
        "• Bot yoki Mini App'da qaysi imkoniyat sizga eng ko'p yoqdi?\n"
        "• Qaysi savolda noaniqlik yoki xato uchratdingiz?\n"
        "• SAT tayyorgarligingiz uchun yana qanday yangi funksiya qo'shishimizni xohlaysiz?\n\n"
        "✍️ <i>Fikringizni bitta xabar ko'rinishida yozib yuboring:</i>"
    )
    try:
        await callback.message.edit_text(text, reply_markup=get_feedback_prompt_keyboard(), parse_mode="HTML")
    except Exception:
        await callback.message.answer(text, reply_markup=get_feedback_prompt_keyboard(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "fb_cancel")
async def cb_feedback_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    text = "Taklif yuborish bekor qilindi."
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Bosh Menyu", callback_data="back_to_menu")]
    ])
    try:
        await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    except Exception:
        pass
    await callback.answer()


@router.message(FeedbackState.waiting_for_feedback)
async def process_feedback_message(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    full_name = message.from_user.full_name or ""
    feedback_text = message.text or message.caption or ""

    if not feedback_text.strip():
        await message.answer("Iltimos, matnli taklif yoki fikr yozing:")
        return

    # Save to database
    entry = await db.save_student_feedback(
        user_id=user_id,
        username=username,
        full_name=full_name,
        feedback_text=feedback_text
    )

    await state.clear()

    # Thank user
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Bosh Menyu", callback_data="back_to_menu")]
    ])
    safe_user_name = html.escape(full_name or "Do'stim")
    reply_text = (
        f"🙏 <b>Katta rahmat, {safe_user_name}!</b>\n\n"
        "Sizning taklifingiz muvaffaqiyatli qabul qilindi. "
        "Biz har bir fikrni diqqat bilan o'rganib, tizimni siz uchun yanada foydali va qulay qilamiz!\n\n"
        "<i>SAT tayyorgarligingizda ulkan zafarlar tilaymiz! 🚀</i>"
    )
    await message.answer(reply_text, reply_markup=kb, parse_mode="HTML")

    # Notify admins if any
    for admin_id in ADMIN_IDS:
        try:
            admin_notice = (
                "📬 <b>YANGI FOYDALANUVCHI TAKLIFI</b>\n"
                f"👤 <b>Kimdan:</b> {html.escape(full_name)} (@{html.escape(username)})\n"
                f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📝 <b>Matn:</b>\n{html.escape(feedback_text)}"
            )
            await message.bot.send_message(chat_id=admin_id, text=admin_notice, parse_mode="HTML")
        except Exception as e:
            logger.warning(f"Could not notify admin {admin_id}: {e}")
