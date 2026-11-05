import re
import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import CommandStart, Command
from aiogram.enums import ChatMemberStatus

from config import CHANNEL_ID, CHANNEL_URL, ADMIN_ID

logger = logging.getLogger(__name__)
router = Router()

# Mini App URL (hosted on Render or local tunnel)
MINI_APP_URL = "https://sat-master-bot.onrender.com/miniapp"

async def is_user_subscribed(bot: Bot, user_id: int) -> bool:
    """Check whether a user is subscribed to the mandatory channel."""
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in [
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.CREATOR
        ]
    except Exception:
        return False

def get_join_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Kanalga a'zo bo'lish (@ieltssat_daily)", url=CHANNEL_URL)],
        [InlineKeyboardButton(text="✅ A'zo bo'ldim — Barcha materiallarni ochish", callback_data="check_sub")]
    ])

def get_materials_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Ball Hisoblagich (Mini App)", web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton(text="📚 Cambridge IELTS 1–19 To'plami", callback_data="dl_ielts")],
        [InlineKeyboardButton(text="🎯 Official SAT Bluebook 1–6 Testlari", callback_data="dl_sat")],
        [InlineKeyboardButton(text="💎 Band 9 Akademik Lug'at & Kollokatsiyalar", callback_data="dl_vocab")],
        [InlineKeyboardButton(text="⚡ SAT Math 800 & Desmos Sirlari", callback_data="dl_desmos")],
        [InlineKeyboardButton(text="📢 Rasmiy Kanalga O'tish", url=CHANNEL_URL)]
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
            "Ushbu bot orqali O'zbekistondagi eng nufuzli universitetlarga kirish va grant yutish "
            "uchun kerak bo'ladigan barcha rasmiy materiallarni <b>mutlaqo bepul</b> yuklab olishingiz mumkin.\n\n"
            "📖 <b>Bazadagi materiallar:</b>\n"
            "• Cambridge IELTS 1–19 (Barcha PDF kitoblar va Listening MP3lar)\n"
            "• Digital SAT Bluebook 1–6 rasmiy testlari va yechimlari\n"
            "• Band 9 namunaviy insholar va kollokatsiyalar\n"
            "• SAT Math 800 formulalar va Desmos xaklari\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🔒 <i>Fayllarni yuklab olish faqat kanalimiz a'zolari uchun ochiq.</i>\n\n"
            "👉 Pastdagi tugma orqali <b>@ieltssat_daily</b> kanaliga a'zo bo'ling va <b>'A'zo bo'ldim'</b> tugmasini bosing:"
        )
        await message.answer(text, reply_markup=get_join_keyboard(), parse_mode="HTML")
        return

    text = (
        f"👋 <b>Xush kelibsiz, {message.from_user.first_name}!</b>\n\n"
        "🎉 Sizga <b>IELTS & SAT O'quv Bazasi</b>ga to'liq ruxsat berildi.\n\n"
        "Kerakli bo'limni tanlang yoki <b>Mini App</b> orqali o'z balingizni hisoblang:"
    )
    await message.answer(text, reply_markup=get_materials_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "check_sub")
async def callback_check_sub(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    subscribed = await is_user_subscribed(bot, user_id)

    if subscribed:
        await callback.message.edit_text(
            "✅ <b>Obuna tasdiqlandi!</b> Barcha IELTS va SAT materiallari ochiq.\n\n"
            "O'zingizga kerakli manbani tanlang:",
            reply_markup=get_materials_keyboard(),
            parse_mode="HTML"
        )
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

# =========================================================================
# 🔄 SMART GROUP RECREATOR & CONTENT CURATOR
# =========================================================================
# When added to discussion groups, the bot detects high-value educational
# questions, vocabulary, and tips, rewrites them with official channel branding,
# and prepares or publishes them.

KEYWORDS = ["ielts", "sat", "reading", "writing", "speaking", "listening", "vocab", "collocation", "task 1", "task 2", "bluebook", "desmos"]

@router.message(F.chat.type.in_(["group", "supergroup"]))
async def group_content_listener(message: Message, bot: Bot):
    """Listens to study & discussion groups and curates educational content."""
    text = message.text or message.caption or ""
    if len(text) < 40:
        return

    text_lower = text.lower()
    matches = [k for k in KEYWORDS if re.search(r'\b' + re.escape(k) + r'\b', text_lower)]
    
    # If the message contains high-value study content
    if len(matches) >= 2:
        logger.info(f"Detected educational content in group {message.chat.title} (keywords: {matches})")
        
        # Clean and recreate post for your channel
        recreated_post = (
            "💡 <b>Kanal O'quvchilari Uchun Maxsus Savol / Tavsiya</b> 🎯\n\n"
            f"{text.strip()}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📚 <b>Bepul Cambridge IELTS 1–19 va SAT Bluebook bazasi:</b> @ieltssat_dailybot\n"
            "📢 <b>Rasmiy kanalimiz:</b> @ieltssat_daily"
        )

        # Notify admin or queue post
        if ADMIN_ID:
            try:
                await bot.send_message(
                    chat_id=ADMIN_ID,
                    text=f"📥 <b>Guruhdan yangi post tavsiyasi topildi ({message.chat.title}):</b>\n\n{recreated_post}",
                    parse_mode="HTML"
                )
            except Exception:
                pass
