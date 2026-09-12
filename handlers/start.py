"""
SAT AI Bot - Start Command and Navigation Handler
"""

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from config import WEBAPP_URL

router = Router()

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Creates the primary navigation dashboard for the user."""
    buttons = [
        [
            InlineKeyboardButton(
                text="🔬 AI Rentgen Diagnostika (5 daqiqa)",
                callback_data="start_diagnostic"
            )
        ],
        [
            InlineKeyboardButton(
                text="⚡ Desmos Hiylalari & Cheatcodes",
                callback_data="desmos_catalog"
            )
        ],
        [
            InlineKeyboardButton(
                text="📱 60 Kunlik Kundalik (Web App)",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ],
        [
            InlineKeyboardButton(
                text="🤖 AI Ustozdan Yordam So'rash",
                callback_data="ask_ai_info"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_name = message.from_user.first_name or "Do'stim"
    welcome_text = (
        f"Assalomu alaykum, <b>{user_name}</b>! ⚡\n\n"
        f"Xush kelibsiz! Bu <b>SAT Master AI</b> — Digital SAT 1500+ ball olishingiz uchun "
        f"shaxsiy <b>AI Rentgen Diagnostika</b> va <b>Desmos Hiylalari</b> tizimi.\n\n"
        f"🎯 <b>BIZ NIMA BERAMIZ?</b>\n"
        f"• 🔬 <b>AI Rentgen:</b> 5 ta nozik savol orqali qaysi mavzu sening 80-100 ballingni o'g'irlayotganini aniqlaydi.\n"
        f"• ⚡ <b>Desmos Hacks:</b> Digital SAT Math savollarini formulalarsiz, 10 soniyada yechish yo'li.\n"
        f"• 📱 <b>60 Kunlik Kundalik:</b> Digital SAT 1500 va IELTS 8.0 uchun to'liq intizom WebApp'i.\n\n"
        f"👇 <i>Hozir o'z bilimingizni rentgen qilish uchun quyidagi tugmani bosing:</i>"
    )
    await message.answer(welcome_text, reply_markup=get_main_menu_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "desmos_catalog")
async def desmos_catalog(callback: CallbackQuery):
    text = (
        "⚡ <b>DIGITAL SAT DESMOS TOP-5 CHEATCODES</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "1. <b>Tenglamalar Sistemasi:</b> Ikkita tenglamani ketma-ket yozing. Kesishgan nuqtalarni sichqoncha bilan bosing — yechimlar darhol ko'rinadi!\n\n"
        "2. <b>No-solution / Infinitely Many:</b> Ikkala chiziq ustma-ust tushsa (cheksiz), parallel bo'lsa (yechim yo'q).\n\n"
        "3. <b>Regression (Statistika):</b> y₁ ~ mx₁ + b yoki y₁ ~ ax₁² + bx₁ + c formulasi bilan istalgan jadval qonuniyatini 3 soniyada toping!\n\n"
        "4. <b>Aylana Tenglamasi:</b> x² + y² + Ax + By + C = 0 ni to'g'ridan-to'g'ri tashlang, markaz va radiusni Desmos o'zi hisoblab beradi.\n\n"
        "5. <b>Tengsizliklar (Inequalities):</b> y > 2x + 1 ni yozing — Desmos sohani bo'yab beradi, so'ralgan nuqta sohada bormi-yo'qligi darhol ma'lum bo'ladi!"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔬 O'z bilimimda sinab ko'rish ➡️", callback_data="start_diagnostic")],
        [InlineKeyboardButton(text="⬅️ Asosiy menyu", callback_data="back_to_menu")]
    ])
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "ask_ai_info")
async def ask_ai_info(callback: CallbackQuery):
    text = (
        "🤖 <b>AI USTOZ BILAN ISHLASH</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Siz istalgan SAT yoki IELTS savolini (matn yoki rasm shaklida) botga yuborishingiz mumkin.\n\n"
        "AI unga:\n"
        "1. Nega standart usul sekin ekanini tushuntiradi.\n"
        "2. Desmos orqali 10 soniyada yechish yo'lini ko'rsatadi.\n"
        "3. Imtihonda tushishi mumkin bo'lgan tuzoqlarni ochib beradi.\n\n"
        "💬 <i>Hozir xohlagan savolingizni yuborib ko'ring!</i>"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Asosiy menyu", callback_data="back_to_menu")]
    ])
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "open_webapp_info")
async def webapp_info(callback: CallbackQuery):
    text = (
        "📱 <b>60 KUNLIK SAT & IELTS KUNDALIGI</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Ushbu kundalik orqali siz:\n"
        "• Har kuni 5 soat toza SAT darsi\n"
        "• 7.5 soat uyqu tartibi\n"
        "• Sport va o'zlashtirish foizini kuzatib borasiz.\n\n"
        "Quyidagi tugma orqali WebApp ni ochishingiz mumkin:"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 WebApp ni Ochish", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton(text="⬅️ Asosiy menyu", callback_data="back_to_menu")]
    ])
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    welcome_text = (
        "⚡ <b>ASOSIY BOSHQARUV MENYUSI</b>\n\n"
        "Kerakli bo'limni tanlang:"
    )
    await callback.message.edit_text(welcome_text, reply_markup=get_main_menu_keyboard(), parse_mode="HTML")
    await callback.answer()
