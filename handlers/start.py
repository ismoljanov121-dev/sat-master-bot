"""
EduTest Pro - Start Command, Referrals, and Primary Dashboard
"""

import html
import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)

from config import BRAND_NAME, CENTER_NAME, WEBAPP_URL, is_admin
from database import db

logger = logging.getLogger("StartHandler")

router = Router()

def get_main_menu_keyboard(user_id: int | None = None) -> InlineKeyboardMarkup:
    """Creates the primary navigation dashboard for the user with 3 clear P0 paths."""
    unresolved_count = db.get_unresolved_mistakes_count(user_id) if user_id else 0
    mistakes_btn_text = f"❌ 3. Xatolarim daftari ({unresolved_count})" if unresolved_count > 0 else "❌ 3. Xatolarim daftari"

    buttons = [
        # --- 3 Clear P0 Paths ---
        [
            InlineKeyboardButton(
                text="🎯 1. Darajamni bilish (7 savol - Bepul)",
                callback_data="start_diagnostic"
            )
        ],
        [
            InlineKeyboardButton(
                text="⏱️ 2. Bugungi 10 daqiqalik mashq",
                callback_data="ex_start:daily_10m"
            )
        ],
        [
            InlineKeyboardButton(
                text=mistakes_btn_text,
                callback_data="notebook_menu"
            )
        ],
        # --- Secondary Features ---
        [
            InlineKeyboardButton(
                text="📱 Mini Appda Test Topshirish & Tracker",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ],
        [
            InlineKeyboardButton(
                text="📝 Mock Imtihon Markazi",
                callback_data="exam_hub"
            ),
            InlineKeyboardButton(
                text="📚 SAT Mashq Bazasi",
                callback_data="practice_hub"
            )
        ],
        [
            InlineKeyboardButton(
                text="⚡ Desmos Strategiyalari",
                callback_data="desmos_catalog"
            ),
            InlineKeyboardButton(
                text="📊 Mening Natijam",
                callback_data="my_stats"
            )
        ],
        [
            InlineKeyboardButton(
                text="💬 Fikr va Taklif (Feedback)",
                callback_data="send_feedback_prompt"
            ),
            InlineKeyboardButton(
                text="👥 Do'stlarni Taklif Qilish",
                callback_data="referral_menu"
            )
        ]
    ]

    if user_id and is_admin(user_id):
        buttons.append([
            InlineKeyboardButton(
                text="⚙️ Administrator Paneli",
                callback_data="admin_panel_open"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject = None):
    try:
        user_id = message.from_user.id
        user_name = html.escape(message.from_user.first_name or "Do'stim")
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
            f"Xush kelibsiz! Bu <b>{BRAND_NAME}</b> — Digital SAT imtihoniga mustaqil tayyorlanish "
            "uchun mo'ljallangan intellektual platforma (bepul pilot versiyasi).\n\n"
            "🎯 <b>SIZ UCHUN 3 TA ASOSIY YO'L:</b>\n"
            "1️⃣ <b>🎯 Darajamni bilish:</b> 7 ta nozik savol orqali bilim darajangiz va zaif mavzularni bepul aniqlang.\n"
            "2️⃣ <b>⏱️ Bugungi 10 daqiqalik mashq:</b> Kunlik odatga aylanadigan tezkor 6 savollik mikro-mashq.\n"
            "3️⃣ <b>❌ Xatolarim daftari:</b> Ilgari xato qilgan savollaringizni to'liq o'zlashtirguncha qayta mashq qiling.\n\n"
            "📱 Shuningdek, <b>Mini App</b> orqali mobil telefonda qulay test topshirishingiz mumkin.\n\n"
            "👇 <i>Quyidagi 3 ta asosiy yo'ldan birini tanlang:</i>"
        )
        await message.answer(welcome_text, reply_markup=get_main_menu_keyboard(user_id), parse_mode="HTML")
    except Exception as e:
        logger.error(f"Critical error in cmd_start: {e}")
        try:
            await message.answer(
                "Assalomu alaykum! Xush kelibsiz! Tizim yangilandi, xizmatlaringizdan foydalanishingiz mumkin.",
                reply_markup=get_main_menu_keyboard()
            )
        except Exception:
            pass

DESMOS_HUB_TEXT = (
    "⚡ <b>DIGITAL SAT DESMOS STRATEGIYALARI</b>\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n"
    "<i>Formula yodlamang — Desmos imkoniyatlaridan maksimal foydalaning!</i>\n\n"
    "1️⃣ <b>Tenglamalar Sistemasi</b> ➔ Kesishgan nuqta = Yechim\n"
    "2️⃣ <b>Parabola & Vertex</b> ➔ Cho'qqi (h, k) da k = Max/Min\n"
    "3️⃣ <b>Aylana Radiusi & Markazi</b> ➔ Tenglamani to'g'ridan-to'g'ri chizish\n"
    "4️⃣ <b>Jadval & Regression</b> ➔ <code>y₁ ~ mx₁ + b</code> bilan formulani topish\n"
    "5️⃣ <b>Tengsizliklar Sohasi</b> ➔ Rangli soha = To'g'ri javob\n"
    "6️⃣ <b>Slayder & Constants</b> ➔ k ga slayder berib moslash\n\n"
    "👇 <i>Aniq misol va formulani ko'rish uchun tanlang:</i>"
)

def get_desmos_hub_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="1️⃣ Tenglamalar Sistemasi", callback_data="desmos_c_sys"),
            InlineKeyboardButton(text="2️⃣ Parabola & Vertex", callback_data="desmos_c_quad")
        ],
        [
            InlineKeyboardButton(text="3️⃣ Aylana Radiusi", callback_data="desmos_c_circle"),
            InlineKeyboardButton(text="4️⃣ Jadval & Regression", callback_data="desmos_c_reg")
        ],
        [
            InlineKeyboardButton(text="5️⃣ Tengsizliklar Sohasi", callback_data="desmos_c_ineq"),
            InlineKeyboardButton(text="6️⃣ Slayder & Constants", callback_data="desmos_c_sliders")
        ],
        [
            InlineKeyboardButton(text="🔬 O'z bilimimda sinab ko'rish ➡️", callback_data="start_diagnostic")
        ],
        [
            InlineKeyboardButton(text="⬅️ Asosiy Menyu", callback_data="back_to_menu")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

DESMOS_CARDS = {
    "sys": (
        "⚡ <b>DESMOS CHEATCODE #1: TENGLAMALAR SISTEMASI</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "📌 <b>QOIDASI:</b>\n"
        "• Kesishish nuqtasi = Yechim (x, y)\n"
        "• 2 ta chiziq parallel ➔ 0 ta yechim (No solution)\n"
        "• Chiziqlar ustma-ust ➔ Cheksiz yechim (Infinite)\n\n"
        "⌨️ <b>DESMOSGA YOZILISHI:</b>\n"
        "1-qator: <code>2x - 3y = 8</code>\n"
        "2-qator: <code>4x + y = 2</code>\n"
        "🎯 Bosing: Kesishgan nuqtada (1, -2) chiqadi ➔ x=1, y=-2!\n\n"
        "⏱️ <i>Qo'lda: 1.5 daqiqa | Desmosda: 4 soniya!</i>"
    ),
    "quad": (
        "⚡ <b>DESMOS CHEATCODE #2: PARABOLA & VERTEX (MAX/MIN)</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "📌 <b>QOIDASI:</b>\n"
        "• Parabolaning eng baland/past cho'qqisi = Vertex (h, k)\n"
        "• Maksimal/Minimal qiymat = har doim <b>y</b> koordinatasi!\n\n"
        "⌨️ <b>DESMOSGA YOZILISHI:</b>\n"
        "1-qator: <code>y = -2(x - 5)² + 18</code>\n"
        "🎯 Cho'qqi nuqtani bosing: <b>(5, 18)</b> chiqadi.\n"
        "Maksimal qiymat: <b>18</b>!\n\n"
        "⏱️ <i>Qo'lda: 2 daqiqa | Desmosda: 3 soniya!</i>"
    ),
    "circle": (
        "⚡ <b>DESMOS CHEATCODE #3: AYLANA RADIUSI & MARKAZI</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "📌 <b>QOIDASI:</b>\n"
        "• Qavslarga ajratish va to'la kvadrat qilish shart emas!\n\n"
        "⌨️ <b>DESMOSGA YOZILISHI:</b>\n"
        "1-qator: <code>x² + y² - 6x + 8y - 11 = 0</code>\n"
        "🎯 Aylana chiziladi. Markazni bosing: <b>(3, -4)</b>.\n"
        "Eng chetki nuqtani bosing: <b>(3, 2)</b>.\n"
        "Radius: 2 - (-4) = <b>6</b>!\n\n"
        "⏱️ <i>Qo'lda: 3 daqiqa | Desmosda: 8 soniya!</i>"
    ),
    "reg": (
        "⚡ <b>DESMOS CHEATCODE #4: JADVAL & REGRESSION</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "📌 <b>QOIDASI:</b>\n"
        "• Jadval berilib formula so'ralsa, qo'lda tenglama tuzmang!\n\n"
        "⌨️ <b>DESMOSGA YOZILISHI:</b>\n"
        "1️⃣ <b>+</b> tugmasini bosib <b>Table</b> (jadval) qo'shing va x₁, y₁ larni kiriting.\n"
        "2️⃣ Chiziqli bo'lsa: <code>y₁ ~ mx₁ + b</code>\n"
        "3️⃣ Kvadrat bo'lsa: <code>y₁ ~ ax₁² + bx₁ + c</code>\n"
        "🎯 Desmos <b>m</b>, <b>b</b> yoki <b>a</b> larni 1 soniyada chiqarib beradi!\n\n"
        "⏱️ <i>Qo'lda: 3 daqiqa | Desmosda: 10 soniya!</i>"
    ),
    "ineq": (
        "⚡ <b>DESMOS CHEATCODE #5: TENGSIZLIKLAR SOHASI</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "📌 <b>QOIDASI:</b>\n"
        "• Qaysi nuqta yechim ekanini tekshirish uchun ko'z bilan ko'ring!\n\n"
        "⌨️ <b>DESMOSGA YOZILISHI:</b>\n"
        "1-qator: <code>y > 2x + 1</code>\n"
        "2-qator: <code>y <= -x + 5</code>\n"
        "🎯 Ikkala rangli soha ustma-ust tushgan joy = Yechimlar sohasi! Variantdagi nuqtani kiritib tekshiring.\n\n"
        "⏱️ <i>Qo'lda: 1.5 daqiqa | Desmosda: 5 soniya!</i>"
    ),
    "sliders": (
        "⚡ <b>DESMOS CHEATCODE #6: SLAYDER & CONSTANTS</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "📌 <b>QOIDASI:</b>\n"
        "• Tenglamada k, c, a kabi noaniq parametrlar berilsa:\n\n"
        "⌨️ <b>DESMOSGA YOZILISHI:</b>\n"
        "1-qator: <code>y = 3x² + kx + 12</code>\n"
        "2-qator: <b>'add slider: k'</b> ni bosing.\n"
        "🎯 Slayderni suring yoki variantdagi sonlarni yozing. Grafik savol shartiga qachon mos tushsa, o'sha son to'g'ri!\n\n"
        "⏱️ <i>Qo'lda: 2 daqiqa | Desmosda: 5 soniya!</i>"
    )
}

@router.message(Command("desmos"))
async def cmd_desmos(message: Message):
    await message.answer(DESMOS_HUB_TEXT, reply_markup=get_desmos_hub_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "desmos_catalog")
async def desmos_catalog(callback: CallbackQuery):
    try:
        try:
            await callback.message.edit_text(DESMOS_HUB_TEXT, reply_markup=get_desmos_hub_keyboard(), parse_mode="HTML")
        except Exception:
            pass
    finally:
        try:
            await callback.answer()
        except Exception:
            pass

@router.callback_query(F.data.startswith("desmos_c_"))
async def cb_desmos_detail(callback: CallbackQuery):
    try:
        key = callback.data.replace("desmos_c_", "").strip()
        text = DESMOS_CARDS.get(key, DESMOS_HUB_TEXT)
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🧮 Shu mavzuda mashq qilish ➡️", callback_data="prac_start_math")],
            [InlineKeyboardButton(text="⬅️ Barcha Hiylalar", callback_data="desmos_catalog")],
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

@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        welcome_text = (
            f"⚡ <b>{BRAND_NAME} — ASOSIY BOSHQARUV MENYUSI</b>\n\n"
            "Kerakli bo'limni tanlang:"
        )
        try:
            await callback.message.edit_text(welcome_text, reply_markup=get_main_menu_keyboard(user_id), parse_mode="HTML")
        except Exception:
            pass
    finally:
        try:
            await callback.answer()
        except Exception:
            pass

@router.callback_query(F.data == "admin_panel_open")
async def cb_open_admin_panel(callback: CallbackQuery):
    """Direct button trigger to open admin panel if authorized."""
    user_id = callback.from_user.id
    if not is_admin(user_id):
        await callback.answer("⛔ Ushbu bo'lim faqat administratorlar uchun.", show_alert=True)
        return

    from handlers.admin import format_admin_dashboard_text, get_admin_main_keyboard
    try:
        text = format_admin_dashboard_text()
        await callback.message.edit_text(text, reply_markup=get_admin_main_keyboard(), parse_mode="HTML")
    finally:
        try:
            await callback.answer()
        except Exception:
            pass


@router.message(Command("webapp"))
@router.message(Command("rejim"))
async def cmd_webapp(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Shaxsiy Rejim & Trackerni Ochish", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton(text="⬅️ Asosiy Menyu", callback_data="back_to_menu")]
    ])
    text = (
        "📱 <b>SHAXSIY REJIM & 60 KUNLIK INTIZOM TRACKERI</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Ushbu interaktiv Mini App orqali siz:\n"
        "• 🤖 <b>AI Generator:</b> O'zingizga mos ideal kun tartibini avtomatik tuzasiz.\n"
        "• ✨ <b>Tayyor Andozalar:</b> SAT 1500+ Standart, Gap Year yoki Maktab rejimlaridan foydalanasiz.\n"
        "• 📊 <b>Mentorga Hisobot:</b> Kunlik o'qish foizini 1-tugmada o'qituvchingizga yuborasiz.\n"
        "• ❌ <b>Error Log:</b> Xatolarni daftarga qayd qilib, Desmos bilan yechishni o'rganasiz.\n\n"
        "👇 <i>Pastdagi tugmani bosing va ilovani ishga tushiring:</i>"
    )
    await message.answer(text, reply_markup=kb, parse_mode="HTML")
