"""
SAT Master AI - Start Command, Referrals, and Primary Dashboard
"""

from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from config import WEBAPP_URL
from database import db
import logging

logger = logging.getLogger("StartHandler")

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
            ),
            InlineKeyboardButton(
                text="📊 Mening Natijam",
                callback_data="my_stats"
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
                text="👥 Do'stlarni Taklif Qilish (VIP)",
                callback_data="referral_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject = None):
    try:
        user_id = message.from_user.id
        user_name = message.from_user.first_name or "Do'stim"
        username = message.from_user.username or ""

        # Check for referral parameter: /start ref_123456
        referred_by = None
        args = command.args if command else None
        if args and args.startswith("ref_"):
            try:
                ref_id_str = args.replace("ref_", "").strip()
                if ref_id_str.isdigit() and int(ref_id_str) != user_id:
                    referred_by = int(ref_id_str)
                    ref_str_id = str(referred_by)
                    if "users" in db.local_cache and ref_str_id in db.local_cache["users"]:
                        db.local_cache["users"][ref_str_id]["referrals_count"] = (
                            db.local_cache["users"][ref_str_id].get("referrals_count", 0) + 1
                        )
                        db._save_local_db()
                        try:
                            await message.bot.send_message(
                                chat_id=referred_by,
                                text=f"🎉 <b>Yangi do'stingiz qo'shildi!</b>\n{user_name} sizning referal havolangiz orqali botga kirdi. Referal ballaringiz soni oshdi!",
                                parse_mode="HTML"
                            )
                        except Exception:
                            pass
            except Exception as e:
                logger.warning(f"Referral parsing error: {e}")

        # Save to database
        try:
            await db.save_user(
                user_id=user_id,
                username=username,
                full_name=message.from_user.full_name,
                referred_by=referred_by
            )
        except Exception as e:
            logger.error(f"Error in save_user: {e}")

        welcome_text = (
            f"Assalomu alaykum, <b>{user_name}</b>! ⚡\n\n"
            f"Xush kelibsiz! Bu <b>SAT Master AI</b> — Digital SAT 1500+ ball olishingiz uchun "
            f"shaxsiy <b>AI Rentgen Diagnostika</b> va <b>Desmos Hiylalari</b> tizimi.\n\n"
            f"🎯 <b>BIZNING IMKONIYATLAR:</b>\n"
            f"• 🔬 <b>AI Rentgen:</b> 5-7 ta nozik savol orqali qaysi mavzu sening 80-100 ballingni o'g'irlayotganini aniqlaydi.\n"
            f"• ⚡ <b>Desmos Hacks:</b> Digital SAT Math savollarini formulalarsiz, 10 soniyada yechish sirlari.\n"
            f"• 📱 <b>60 Kunlik Kundalik:</b> SAT 1500 va IELTS 8.0 uchun to'liq intizom WebApp'i.\n"
            f"• 👥 <b>VIP Bonuslar:</b> Do'stlaringizni taklif qilib, Hard Module 2 testlarini bepul oching!\n\n"
            f"👇 <i>Hozir o'z bilimingizni rentgen qilish uchun quyidagi tugmani bosing:</i>"
        )
        await message.answer(welcome_text, reply_markup=get_main_menu_keyboard(), parse_mode="HTML")
    except Exception as e:
        logger.error(f"Critical error in cmd_start: {e}")
        try:
            await message.answer(
                "Assalomu alaykum! Xush kelibsiz! Tizim yangilandi, xizmatlaringizdan foydalanishingiz mumkin.",
                reply_markup=get_main_menu_keyboard()
            )
        except Exception:
            pass

DESMOS_CATALOG_TEXT = (
    "⚡ <b>DIGITAL SAT DESMOS TOP-8 CHEATCODES</b>\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n"
    "1. <b>Tenglamalar Sistemasi:</b> Ikkita tenglamani ketma-ket yozing. Kesishgan nuqtalarni bosing — yechimlar darhol ko'rinadi!\n\n"
    "2. <b>No-solution / Infinitely Many:</b> Ikkala chiziq ustma-ust tushsa (cheksiz yechim), parallel bo'lsa (yechim yo'q).\n\n"
    "3. <b>Regression (Statistika):</b> y₁ ~ mx₁ + b yoki y₁ ~ ax₁² + bx₁ + c formulasi bilan istalgan jadval qonuniyatini 3 soniyada toping!\n\n"
    "4. <b>Aylana Tenglamasi:</b> x² + y² + Ax + By + C = 0 ni to'g'ridan-to'g'ri tashlang, markaz va radiusni Desmos o'zi hisoblab beradi.\n\n"
    "5. <b>Tengsizliklar (Inequalities):</b> y > 2x + 1 ni yozing — Desmos sohani bo'yab beradi, so'ralgan nuqta sohada bormi-yo'qligi darhol ma'lum bo'ladi!\n\n"
    "6. <b>Constants & Sliders:</b> ax² + bx + c = 0 da a, b, c ga slayder qo'shing va savol shartiga mos keltiring!\n\n"
    "7. <b>Equivalent Expressions:</b> Asl ifodani 1-qatorga, variantlarni 2-qatorga yozing. Qaysi grafik ustma-ust tushsa, o'sha to'g'ri!\n\n"
    "8. <b>Vertex & Min/Max:</b> Parabolaning eng baland/past cho'qqisini sichqoncha bilan bosing — y qiymati maksimal/minimal qiymatdir!"
)

@router.message(Command("desmos"))
async def cmd_desmos(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔬 O'z bilimimda sinab ko'rish ➡️", callback_data="start_diagnostic")],
        [InlineKeyboardButton(text="⬅️ Asosiy menyu", callback_data="back_to_menu")]
    ])
    await message.answer(DESMOS_CATALOG_TEXT, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data == "desmos_catalog")
async def desmos_catalog(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔬 O'z bilimimda sinab ko'rish ➡️", callback_data="start_diagnostic")],
        [InlineKeyboardButton(text="⬅️ Asosiy menyu", callback_data="back_to_menu")]
    ])
    await callback.message.edit_text(DESMOS_CATALOG_TEXT, reply_markup=kb, parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    welcome_text = (
        "⚡ <b>ASOSIY BOSHQARUV MENYUSI</b>\n\n"
        "Kerakli bo'limni tanlang:"
    )
    await callback.message.edit_text(welcome_text, reply_markup=get_main_menu_keyboard(), parse_mode="HTML")
    await callback.answer()
