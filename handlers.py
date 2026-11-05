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
        [InlineKeyboardButton(text="📚 Cambridge IELTS 1–19 To'plami", callback_data="dl_ielts")],
        [InlineKeyboardButton(text="🎯 Official SAT Bluebook 1–6 Testlari", callback_data="dl_sat")],
        [InlineKeyboardButton(text="💎 Band 9 Akademik Lug'at & Kollokatsiyalar", callback_data="dl_vocab")],
        [InlineKeyboardButton(text="⚡ SAT Math 800 & Desmos Sirlari", callback_data="dl_desmos")]
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
            "🎓 <b>IELTS 8.5 & SAT 1500+ Rasmiy O'quv Bazasiga Xush Kelibsiz!</b>\n\n"
            "Ushbu bot orqali nufuzli universitetlarga kirish va grant yutish "
            "uchun kerak bo'ladigan barcha rasmiy materiallarni <b>bepul</b> olishingiz mumkin.\n\n"
            "📖 <b>Bazadagi materiallar:</b>\n"
            "• <b>Full SAT Mock Tizimi:</b> 42 ta test savollari (Math & Reading) tahlillari bilan\n"
            "• <b>IELTS Listening & Reading:</b> 40 tadan to'liq mock test savollari\n"
            "• <b>IELTS Writing Bank:</b> 42 ta mavzu va Band 9 shablonlari\n"
            "• Cambridge IELTS 1–19 PDF va MP3 to'plami\n"
            "• Digital SAT Bluebook 1–6 rasmiy testlari\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🔒 <i>Fayllarni yuklab olish va mock testlarni ishlash faqat kanalimiz a'zolari uchun ochiq.</i>\n\n"
            "👉 Pastdagi tugma orqali <b>@ieltssat_daily</b> kanaliga a'zo bo'ling va <b>'A'zo bo'ldim'</b> tugmasini bosing:"
        )
        await message.answer(text, reply_markup=get_join_inline_keyboard(), parse_mode="HTML")
        await message.answer("👇 Pastki doimiy menyudan ham foydalanishingiz mumkin:", reply_markup=get_main_reply_keyboard())
        return

    text = (
        f"👋 <b>Xush kelibsiz, {html.escape(message.from_user.first_name)}!</b>\n\n"
        "🎉 Sizga <b>IELTS & SAT O'quv Bazasi va Mock Tizimi</b>ga to'liq ruxsat berildi.\n\n"
        "Quyidagi tugmalar orqali Mini App’ni ochishingiz yoki materiallarni yuklab olishingiz mumkin:"
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
        "🎯 <b>IELTS & SAT Full Mock Tizimi</b>\n\n"
        "Mini App ichida quyidagi kengaytirilgan bo'limlar tayyor:\n\n"
        "• <b>Digital SAT Full Mock:</b> 42 ta savol (21 Reading/Writing + 21 Math) timer va College Board tahlillari bilan\n"
        "• <b>IELTS Listening Full Mock:</b> 40 ta savol (Section 1–4) audio pleyer va tapescript bilan\n"
        "• <b>IELTS Reading Full Mock:</b> 40 ta savol (Passage 1–3) T/F/NG va tushuntirishlar bilan\n"
        "• <b>IELTS Writing Bank:</b> 42 ta Task 1 va Task 2 mavzulari Band 9 shablonlari bilan\n"
        "• <b>Score & Grant Predictor:</b> Universitetlar grantini hisoblash kalkulyatori\n\n"
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
        "📢 <b>IELTS 8.5 & SAT 1500+ Rasmiy O'quv Kanali:</b>\n\n"
        "👉 @ieltssat_daily\n\n"
        "Kanalda har kuni:\n"
        "• 09:00 — Band 9 & SAT 1500+ Lug'at\n"
        "• 14:00 — Interaktiv Quiz-Viktorina\n"
        "• 20:00 — Cambridge / Bluebook Tahlillari va Maslahatlar"
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
        "📚 <b>Cambridge IELTS 1–19 To'liq Mega-To'plami</b>\n\n"
        "Paket tarkibi:\n"
        "• 1-kitobdan 19-kitobgacha bo'lgan rasmiy testlar (PDF)\n"
        "• Barcha Listening audio fayllari (MP3) va matnlari (Tapescripts)\n"
        "• Rasmiy javoblar kaliti va namunaviy insholar\n\n"
        "📂 Fayllar rasmiy kanalimiz arxiviga joylangan. Quyidagi tugma orqali yuklab oling:"
    )
    await callback.message.edit_text(
        text,
        reply_markup=get_channel_action_button("Kanal orqali Cambridge 1–19 yuklash"),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "dl_sat")
async def callback_dl_sat(callback: CallbackQuery):
    await callback.answer()
    text = (
        "🎯 <b>Official Digital SAT Bluebook 1–6 Testlari</b>\n\n"
        "Paket tarkibi:\n"
        "• College Board rasmiy Module 1 & Module 2 Math va Reading savollari\n"
        "• Har bir savolning bosqichma-bosqich tushuntirilgan yechimlari\n"
        "• Qiyin darajadagi tenglamalar va funksiyalar tahlili\n\n"
        "📂 Testlar kanalimiz arxiviga joylangan. Quyidagi tugma orqali oching:"
    )
    await callback.message.edit_text(
        text,
        reply_markup=get_channel_action_button("Kanal orqali SAT testlarini ochish"),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "dl_vocab")
async def callback_dl_vocab(callback: CallbackQuery):
    await callback.answer()
    text = (
        "💎 <b>Band 9 & SAT 1500+ Akademik Lug'at Jadvali</b>\n\n"
        "Paket tarkibi:\n"
        "• Insho va Speaking uchun 500+ yuqori darajadagi kollokatsiyalar\n"
        "• Mavzular bo'yicha saralangan so'zlar (Technology, Education, Environment)\n"
        "• O'zbekcha izohlari va kontekstdagi misollari bilan\n\n"
        "📂 Lug'at fayli kanalimizda saqlanadi. Quyidagi tugma orqali oling:"
    )
    await callback.message.edit_text(
        text,
        reply_markup=get_channel_action_button("Lug'at jadvalini yuklab olish"),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "dl_desmos")
async def callback_dl_desmos(callback: CallbackQuery):
    await callback.answer()
    text = (
        "⚡ <b>SAT Math 800: Desmos Sirlari & Formulalar</b>\n\n"
        "Paket tarkibi:\n"
        "• Desmos kalkulyatorida savollarni 15 soniyada yechish usullari\n"
        "• Geometriya va algebra uchun eng muhim formulalar varaqasi\n\n"
        "📂 Qo'llanma kanalimizda saqlanadi. Quyidagi tugma orqali oling:"
    )
    await callback.message.edit_text(
        text,
        reply_markup=get_channel_action_button("Desmos qo'llanmasini olish"),
        parse_mode="HTML"
    )

@router.message(F.chat.type == "private")
async def msg_private_fallback(message: Message):
    text = (
        "👋 <b>IELTS & SAT O'quv Bazasiga Xush Kelibsiz!</b>\n\n"
        "Pastdagi doimiy menyu tugmalari orqali Mini App'ni ochishingiz, "
        "mock test topshirishingiz yoki bepul kitoblarni yuklab olishingiz mumkin."
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
            "📚 <b>Bepul Cambridge IELTS 1–19 va SAT Bluebook bazasi:</b> @ieltssat_dailybot\n"
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
