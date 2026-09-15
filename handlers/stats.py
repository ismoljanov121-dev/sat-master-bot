"""
SAT Master AI - User Statistics & Admin Backup Triggers
"""

import html

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from database import db
from services.backup_service import perform_backup

router = Router()

@router.message(Command("stats"))
async def cmd_stats(message: Message):
    user_id = message.from_user.id
    user_name = html.escape(message.from_user.first_name or "Abituriyent")
    
    user_data = db.local_cache.get("users", {}).get(str(user_id), {})
    quizzes_taken = user_data.get("quizzes_taken", 0)
    last_score = user_data.get("last_score", "Topshirilmagan")
    streak = user_data.get("streak", 0)
    ref_count = user_data.get("referrals_count", 0)

    text = (
        f"📊 <b>SHAXSIY STATISTIKA VA NATIJALAR</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>Abituriyent:</b> {user_name}\n"
        f"🔥 <b>Intizom ketma-ketligi:</b> {streak} kun\n"
        f"📝 <b>Yechilgan testlar:</b> {quizzes_taken} ta\n"
        f"🎯 <b>So'nggi Math balli:</b> {last_score} / 800\n"
        f"👥 <b>Taklif qilingan do'stlar:</b> {ref_count} ta\n\n"
        f"💡 <i>Natijangizni oshirish uchun har kuni kamida 1 ta test topshiring!</i>"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔬 Yangi Rentgen Test ➡️", callback_data="start_diagnostic")],
        [InlineKeyboardButton(text="⬅️ Asosiy Menyu", callback_data="back_to_menu")]
    ])
    await message.answer(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data == "my_stats")
async def cb_stats(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        user_name = html.escape(callback.from_user.first_name or "Abituriyent")
        
        user_data = db.local_cache.get("users", {}).get(str(user_id), {})
        quizzes_taken = user_data.get("quizzes_taken", 0)
        last_score = user_data.get("last_score", "Topshirilmagan")
        streak = user_data.get("streak", 0)
        ref_count = user_data.get("referrals_count", 0)

        text = (
            f"📊 <b>SHAXSIY STATISTIKA VA NATIJALAR</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 <b>Abituriyent:</b> {user_name}\n"
            f"🔥 <b>Intizom ketma-ketligi:</b> {streak} kun\n"
            f"📝 <b>Yechilgan testlar:</b> {quizzes_taken} ta\n"
            f"🎯 <b>So'nggi Math balli:</b> {last_score} / 800\n"
            f"👥 <b>Taklif qilingan do'stlar:</b> {ref_count} ta\n\n"
            f"💡 <i>Natijangizni oshirish uchun har kuni kamida 1 ta test topshiring!</i>"
        )

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔬 Yangi Rentgen Test ➡️", callback_data="start_diagnostic")],
            [InlineKeyboardButton(text="⬅️ Asosiy Menyu", callback_data="back_to_menu")]
        ])
        try:
            await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
        except Exception:
            pass
    finally:
        try:
            await callback.answer()
        except Exception:
            pass

from config import BACKUP_CHANNEL, is_admin


@router.message(Command("backup"))
async def cmd_manual_backup(message: Message):
    """Allows manual trigger of cloud backup to backup channel (Admin only)."""
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("⛔ <b>Kirish taqiqlandi!</b> Ushbu buyruq faqat administratorlar uchun.", parse_mode="HTML")
        return

    status_msg = await message.answer("⏳ <i>Zaxira nusxasi olinmoqda va yuklanmoqda...</i>", parse_mode="HTML")
    success = await perform_backup(message.bot, manual=True)
    target = BACKUP_CHANNEL if BACKUP_CHANNEL else "Lokal fayl"
    if success:
        await status_msg.edit_text(f"✅ <b>Zaxira nusxasi ({target}) ga muvaffaqiyatli jo'natildi!</b>", parse_mode="HTML")
    else:
        await status_msg.edit_text("❌ <b>Zaxiralashda xatolik yuz berdi yoki kanal sozlanmagan.</b>", parse_mode="HTML")

