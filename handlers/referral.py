"""
EduTest Pro - Referral and Virality Engine
Enables students to invite classmates and earn rewards (VIP Desmos Strategiyalari, Hard Module 2).
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

router = Router()

def get_referral_keyboard(user_id: int) -> InlineKeyboardMarkup:
    ref_link = f"https://t.me/edutest_pro_bot?start=ref_{user_id}"
    share_url = f"https://t.me/share/url?url={ref_link}&text=Digital%20SAT%201500%2B%20uchun%20AI%20Rentgen%20va%20Desmos%20hiylalari!%20Tekin%20sinab%20ko'r:"
    
    buttons = [
        [InlineKeyboardButton(text="🚀 Telegramda Do'stlarga Ulashish", url=share_url)],
        [InlineKeyboardButton(text="⬅️ Asosiy Menyu", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@router.message(Command("referral"))
async def cmd_referral(message: Message):
    user_id = message.from_user.id
    user_name = html.escape(message.from_user.first_name or "Abituriyent")
    
    user_data = db.local_cache.get("users", {}).get(str(user_id), {})
    ref_count = user_data.get("referrals_count", 0)
    ref_link = f"https://t.me/edutest_pro_bot?start=ref_{user_id}"

    text = (
        f"👥 <b>DO'STLARNI TAKLIF QILING VA VIP IMKONIYATLARNI OCHING!</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Sizning referal havolangiz:\n"
        f"👉 <code>{ref_link}</code> <i>(nusxalash uchun ustiga bosing)</i>\n\n"
        f"📊 <b>Siz taklif qilgan do'stlar:</b> <b>{ref_count} ta</b>\n\n"
        f"🎁 <b>BEPUL VIP BONUslar:</b>\n"
        f"• <b>1 ta do'st:</b> Digital SAT Desmos Top-10 Shpargalka (PDF)\n"
        f"• <b>3 ta do'st:</b> Hard Module 2 (750-800 ball) maxfiy savollari\n"
        f"• <b>5 ta do'st:</b> To'liq 60 kunlik VIP Tracker & Video Tahlillar!\n\n"
        f"💡 <i>Do'stlaringiz bilan ulashing va birgalikda 1500+ oling!</i>"
    )

    await message.answer(text, reply_markup=get_referral_keyboard(user_id), parse_mode="HTML")

@router.callback_query(F.data == "referral_menu")
async def cb_referral(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        user_data = db.local_cache.get("users", {}).get(str(user_id), {})
        ref_count = user_data.get("referrals_count", 0)
        ref_link = f"https://t.me/edutest_pro_bot?start=ref_{user_id}"

        text = (
            f"👥 <b>DO'STLARNI TAKLIF QILING VA VIP IMKONIYATLARNI OCHING!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Sizning referal havolangiz:\n"
            f"👉 <code>{ref_link}</code> <i>(nusxalash uchun ustiga bosing)</i>\n\n"
            f"📊 <b>Siz taklif qilgan do'stlar:</b> <b>{ref_count} ta</b>\n\n"
            f"🎁 <b>BEPUL VIP BONUslar:</b>\n"
            f"• <b>1 ta do'st:</b> Digital SAT Desmos Top-10 Shpargalka (PDF)\n"
            f"• <b>3 ta do'st:</b> Hard Module 2 (750-800 ball) maxfiy savollari\n"
            f"• <b>5 ta do'st:</b> To'liq 60 kunlik VIP Tracker & Video Tahlillar!\n\n"
            f"💡 <i>Do'stlaringiz bilan ulashing va birgalikda 1500+ oling!</i>"
        )

        try:
            await callback.message.edit_text(text, reply_markup=get_referral_keyboard(user_id), parse_mode="HTML")
        except Exception:
            pass
    finally:
        try:
            await callback.answer()
        except Exception:
            pass
