import html
import re
import logging
from aiogram import Router, F, Bot
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo
)
from aiogram.filters import CommandStart, Command
from aiogram.enums import ChatMemberStatus

from config import CHANNEL_ID, CHANNEL_URL, ADMIN_ID, WEBAPP_URL

logger = logging.getLogger(__name__)
router = Router()

def get_main_reply_keyboard() -> ReplyKeyboardMarkup:
    """Doimiy pastki klaviatura menyusi (klaviatura ustida/yonida doim ko'rinib turadi)."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Ballni Hisoblash & Mock (Mini App)", web_app=WebAppInfo(url=WEBAPP_URL))],
            [
                KeyboardButton(text="🎯 Mock Testlar (SAT & IELTS)"),
                KeyboardButton(text="📚 Bepul Materiallar")
            ],
            [
                KeyboardButton(text="📢 Rasmiy Kanal (@ieltssat_daily)")
            ]
        ],
        resize_keyboard=True,
        is_persistent=True
    )

async def is_user_subscribed(bot: Bot, user_id: int) -> bool:
    """Foydalanuvchi kanalga a'zo ekanligini tekshirish."""
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in [
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.CREATOR
        ]
    except Exception:
        return False

def get_join_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Kanalga a'zo bo'lish (@ieltssat_daily)", url=CHANNEL_URL)],
        [InlineKeyboardButton(text="✅ A'zo bo'ldim — Barcha materiallarni ochish", callback_data="check_sub")]
    ])

def get_materials_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 IELTS Tayyorgarlik Materiallari", callback_data="dl_ielts")],
        [InlineKeyboardButton(text="🎯 Digital SAT Tayyorgarlik Materiallari", callback_data="dl_sat")],
        [InlineKeyboardButton(text="💎 Akademik Lug'at & Kollokatsiyalar", callback_data="dl_vocab")],
        [InlineKeyboardButton(text="⚡ SAT Math Maslahatlari", callback_data="dl_desmos")]
    ])

def get_channel_action_button(label: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📥 {label}", url=CHANNEL_URL)],
        [InlineKeyboardButton(text="🔙 Bosh menyuga qaytish", callback_data="check_sub")]
    ])

@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    user_id = message.from_user.id
    subscribed = await is_user_subscribed(bot, user_id)

    if not subscribed:
        text = (
            "🎓 <b>IELTS 8.5 & SAT 1500+ O'quv Bazasiga Xush Kelibsiz!</b>\n\n"
            "Ushbu bot orqali SAT va IELTS imtihonlariga tayyorgarlik uchun "
            "mashq testlari va materiallarni <b>bepul</b> olishingiz mumkin.\n\n"
            "📖 <b>Bazadagi materiallar:</b>\n"
            "• <b>Digital SAT Mock:</b> 98 savollik testlar (54 RW + 44 Math) tahlillari bilan\n"
            "• <b>IELTS Listening & Reading:</b> 40 savollik mashq testlari\n"
            "• <b>IELTS Writing Bank:</b> Task 1 va Task 2 mavzulari, reja va foydali iboralar bilan\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🔒 <i>Materiallar va mock testlar faqat kanalimiz a'zolari uchun ochiq.</i>\n\n"
            "👉 Pastdagi tugma orqali <b>@ieltssat_daily</b> kanaliga a'zo bo'ling va <b>'A'zo bo'ldim'</b> tugmasini bosing:"
        )
        await message.answer(text, reply_markup=get_join_inline_keyboard(), parse_mode="HTML")
        await message.answer("👇 Pastki doimiy menyudan ham foydalanishingiz mumkin:", reply_markup=get_main_reply_keyboard())
        return

    text = (
        f"👋 <b>Xush kelibsiz, {html.escape(message.from_user.first_name)}!</b>\n\n"
        "🎉 Sizga <b>IELTS & SAT O'quv Bazasi va Mock Tizimi</b>ga to'liq ruxsat berildi.\n\n"
        "Quyidagi tugmalar orqali Mini App’ni ochishingiz yoki materiallar bo'limiga o'tishingiz mumkin:"
    )
    await message.answer(text, reply_markup=get_main_reply_keyboard(), parse_mode="HTML")
    await message.answer("📚 <b>O'quv materiallari bo'limlari:</b>", reply_markup=get_materials_inline_keyboard(), parse_mode="HTML")

@router.message(F.chat.type == "private", Command("menu"))
@router.message(F.chat.type == "private", Command("mock"))
async def cmd_menu(message: Message):
    text = (
        "🎯 <b>IELTS 8.5 & SAT 1500+ Asosiy Menyu:</b>\n\n"
        "Pastdagi doimiy tugmalar orqali xohlagan bo'limni tanlashingiz mumkin:"
    )
    await message.answer(text, reply_markup=get_main_reply_keyboard(), parse_mode="HTML")

@router.message(F.chat.type == "private", F.text.contains("Mock"))
async def msg_mock_hub(message: Message):
    text = (
        "🎯 <b>IELTS & SAT Mock Tizimi</b>\n\n"
        "Mini App ichida quyidagi kengaytirilgan bo'limlar tayyor:\n\n"
        "• <b>Digital SAT Mock:</b> 98 ta savol (54 Reading & Writing + 44 Math), taymer va tahlillar bilan\n"
        "• <b>IELTS Listening:</b> 40 ta savol (Section 1–4) va tapescript bilan\n"
        "• <b>IELTS Reading:</b> 40 ta savol (Passage 1–3), T/F/NG va tushuntirishlar bilan\n"
        "• <b>IELTS Writing Bank:</b> Task 1 va Task 2 mavzulari, reja va foydali iboralar bilan\n"
        "• <b>Ball Predictor:</b> SAT va IELTS ballari bo'yicha taxminiy profil bahosi\n\n"
        "👇 <b>Quyidagi tugma orqali to'liq Mini App’ni oching:</b>"
    )
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Mini App’da Mock Testlarni Ochish", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    await message.answer(text, reply_markup=inline_kb, parse_mode="HTML")

@router.message(F.chat.type == "private", F.text.contains("Bepul Materiallar"))
async def msg_materials(message: Message):
    text = (
        "📚 <b>IELTS & SAT Bepul O'quv Materiallari</b>\n\n"
        "O'zingizga kerakli bo'limni tanlang:"
    )
    await message.answer(text, reply_markup=get_materials_inline_keyboard(), parse_mode="HTML")

@router.message(F.chat.type == "private", F.text.contains("Rasmiy Kanal"))
async def msg_channel(message: Message):
    text = (
        "📢 <b>IELTS 8.5 & SAT 1500+ O'quv Kanali:</b>\n\n"
        "👉 @ieltssat_daily\n\n"
        "Kanalda har kuni:\n"
        "• 09:00 — Akademik Lug'at\n"
        "• 14:00 — Interaktiv Quiz-Viktorina\n"
        "• 20:00 — Imtihon Strategiyalari"
    )
    await message.answer(text, reply_markup=get_main_reply_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "check_sub")
async def callback_check_sub(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    subscribed = await is_user_subscribed(bot, user_id)

    if subscribed:
        await callback.answer()
        await callback.message.edit_text(
            "✅ <b>Obuna tasdiqlandi!</b> Barcha IELTS va SAT materiallari hamda Mock tizimi ochiq.\n\n"
            "O'zingizga kerakli manbani tanlang:",
            reply_markup=get_materials_inline_keyboard(),
            parse_mode="HTML"
        )
        await callback.message.answer("📱 Pastki menyu faollashtirildi:", reply_markup=get_main_reply_keyboard())
    else:
        await callback.answer(
            "❌ Siz hali @ieltssat_daily kanaliga a'zo bo'lmadingiz! Iltimos, avval kanalga obuna bo'ling.",
            show_alert=True
        )

@router.callback_query(F.data == "dl_ielts")
async def callback_dl_ielts(callback: CallbackQuery):
    await callback.answer()
    text = (
        "📚 <b>IELTS Tayyorgarlik Materiallari</b>\n\n"
        "Bu yerda nimalar bor:\n"
        "• Mini App'da Listening va Reading mashq testlari\n"
        "• Writing Bank: Task 1 va Task 2 mavzulari va rejalari\n"
        "• Kanalda kunlik lug'at va imtihon strategiyalari\n\n"
        "📂 Kanal postlarini quyidagi tugma orqali ko'ring:"
    )
    await callback.message.edit_text(
        text,
        reply_markup=get_channel_action_button("Kanalni ochish"),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "dl_sat")
async def callback_dl_sat(callback: CallbackQuery):
    await callback.answer()
    text = (
        "🎯 <b>Digital SAT Tayyorgarlik Materiallari</b>\n\n"
        "Bu yerda nimalar bor:\n"
        "• Mini App'da 98 savollik mock testlar (RW va Math)\n"
        "• Har bir savolning izohi va strategiyasi\n"
        "• Kanalda kunlik SAT savoli\n\n"
        "📂 Kanal postlarini quyidagi tugma orqali ko'ring:"
    )
    await callback.message.edit_text(
        text,
        reply_markup=get_channel_action_button("Kanalni ochish"),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "dl_vocab")
async def callback_dl_vocab(callback: CallbackQuery):
    await callback.answer()
    text = (
        "💎 <b>Akademik Lug'at va Kollokatsiyalar</b>\n\n"
        "Kanalda har kuni 09:00 da:\n"
        "• Mavzu bo'yicha 10 ta akademik so'z\n"
        "• O'zbekcha izoh va kollokatsiya\n\n"
        "📂 Kanal postlarini quyidagi tugma orqali ko'ring:"
    )
    await callback.message.edit_text(
        text,
        reply_markup=get_channel_action_button("Kanalni ochish"),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "dl_desmos")
async def callback_dl_desmos(callback: CallbackQuery):
    await callback.answer()
    text = (
        "⚡ <b>SAT Math Maslahatlari</b>\n\n"
        "Kanalda:\n"
        "• Har kuni 14:00 da SAT savoli va yechimi\n"
        "• Har kuni 20:00 da imtihon strategiyasi\n\n"
        "📂 Kanal postlarini quyidagi tugma orqali ko'ring:"
    )
    await callback.message.edit_text(
        text,
        reply_markup=get_channel_action_button("Kanalni ochish"),
        parse_mode="HTML"
    )

@router.message(F.chat.type == "private")
async def msg_private_fallback(message: Message):
    text = (
        "👋 <b>IELTS & SAT O'quv Bazasiga Xush Kelibsiz!</b>\n\n"
        "Pastdagi doimiy menyu tugmalari orqali Mini App'ni ochishingiz, "
        "mock test topshirishingiz yoki materiallar bo'limiga o'tishingiz mumkin."
    )
    await message.answer(text, reply_markup=get_main_reply_keyboard(), parse_mode="HTML")

KEYWORDS = ["ielts", "sat", "reading", "writing", "speaking", "listening", "vocab", "collocation", "task 1", "task 2", "bluebook", "desmos"]

@router.message(F.chat.type.in_(["group", "supergroup"]))
async def group_content_listener(message: Message, bot: Bot):
    text = message.text or message.caption or ""
    if len(text) < 40:
        return

    text_lower = text.lower()
    matches = [k for k in KEYWORDS if re.search(r'\b' + re.escape(k) + r'\b', text_lower)]
    
    if len(matches) >= 2:
        logger.info(f"Guruhdan savol/fayl topildi: {message.chat.title}")
        recreated_post = (
            "💡 <b>Kanal O'quvchilari Uchun Maxsus Savol / Tavsiya</b> 🎯\n\n"
            f"{html.escape(text.strip()[:3000])}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📚 <b>Bepul IELTS va SAT mashq testlari:</b> @ieltssat_dailybot\n"
            "📢 <b>Rasmiy kanalimiz:</b> @ieltssat_daily"
        )
        if ADMIN_ID:
            try:
                await bot.send_message(
                    chat_id=ADMIN_ID,
                    text=f"📥 <b>Guruhdan yangi post tavsiyasi ({html.escape(message.chat.title or '')}):</b>\n\n{recreated_post}",
                    parse_mode="HTML"
                )
            except Exception:
                pass
