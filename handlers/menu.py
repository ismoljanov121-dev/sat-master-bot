import html
import re
import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware, Router, F, Bot
from aiogram.enums import ChatType
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    TelegramObject,
    WebAppInfo
)
from aiogram.filters import CommandObject, CommandStart, Command

from config import ADMIN_IDS, CHANNEL_URL, WEBAPP_URL
from services import centers, subscription, users
from services.promo import channel_handle

logger = logging.getLogger(__name__)
router = Router()

CHECK_PREFIX = "check_sub"
CHANNEL = channel_handle()
NOT_JOINED_ALERT = f"❌ Siz hali {CHANNEL} kanaliga a'zo bo'lmadingiz! Iltimos, avval kanalga obuna bo'ling."
GATE_TEXT = (
    f"🔒 <b>Avval {CHANNEL} kanaliga obuna bo'ling.</b>\n\n"
    "Bot va Mini App kanal a'zolari uchun bepul. Obuna bo'lgach, <b>«✅ A'zo bo'ldim»</b> tugmasini bosing."
)
WELCOME_LOCKED = (
    "🎓 <b>IELTS va SAT O'quv Bazasiga Xush Kelibsiz!</b>\n\n"
    "Bu bot orqali SAT va IELTS imtihonlariga <b>bepul</b> tayyorlanasiz.\n\n"
    "📖 <b>Nimalar bor:</b>\n"
    "• <b>Digital SAT Mock:</b> adaptiv, 98 savollik testlar va batafsil hisobot\n"
    "• <b>Qisqa mashqlar:</b> mavzu bo'yicha 10 savol va xatolar daftari\n"
    "• <b>IELTS Listening va Reading:</b> 40 savollik testlar\n"
    "• <b>AI Writing:</b> inshongizni yozing va taxminiy band oling\n\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    f"🔒 Botdan foydalanish uchun <b>{CHANNEL}</b> kanaliga obuna bo'ling. "
    "Kanalda har kuni so'zlar, savollar va strategiyalar chiqadi.\n\n"
    "Obuna bo'lgach, <b>«✅ A'zo bo'ldim»</b> tugmasini bosing 👇"
)


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

def get_join_inline_keyboard(payload: str = "") -> InlineKeyboardMarkup:
    """The check button carries what the student asked for, such as an exam code, so it opens after joining."""
    check = f"{CHECK_PREFIX}:{payload}" if payload else CHECK_PREFIX
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📢 Kanalga a'zo bo'lish ({CHANNEL})", url=CHANNEL_URL)],
        [InlineKeyboardButton(text="✅ A'zo bo'ldim — Barcha materiallarni ochish", callback_data=check[:64])]
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
        [InlineKeyboardButton(text="🔙 Bosh menyuga qaytish", callback_data=CHECK_PREFIX)]
    ])

def session_button(code: str, title: str) -> InlineKeyboardMarkup:
    url = f"{WEBAPP_URL}?session={code}"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"🚀 {title[:40]}", web_app=WebAppInfo(url=url))]
    ])


def pending_payload(message: Message) -> str:
    """An exam code typed before joining the channel, as /mock CODE."""
    match = re.match(r"/mock(?:@\w+)?\s+(\S+)", message.text or "")
    return f"s_{match.group(1)[:16]}" if match else ""


class ChannelGate(BaseMiddleware):
    """Students must join the channel before using the menu. /start and the check button handle it themselves."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        chat = data.get("event_chat")
        if user is None or chat is None or chat.type != ChatType.PRIVATE:
            return await handler(event, data)
        if isinstance(event, Message) and (event.text or "").startswith("/start"):
            return await handler(event, data)
        if isinstance(event, CallbackQuery) and (event.data or "").startswith(CHECK_PREFIX):
            return await handler(event, data)
        if await subscription.may_use(data["bot"], user.id):
            return await handler(event, data)
        if isinstance(event, CallbackQuery):
            await event.answer(NOT_JOINED_ALERT, show_alert=True)
        elif isinstance(event, Message):
            await event.answer(GATE_TEXT, reply_markup=get_join_inline_keyboard(pending_payload(event)), parse_mode="HTML")
        return None


router.message.middleware(ChannelGate())
router.callback_query.middleware(ChannelGate())


async def answer_session(message: Message, code: str, user_id: int | None = None) -> None:
    session = await centers.join_session(user_id or message.from_user.id, code)
    if session is None:
        await message.answer("❌ Bu kod topilmadi yoki imtihon yopilgan. Kodni o'qituvchingizdan tekshiring.")
        return
    await message.answer(
        f"🏫 <b>{html.escape(session['title'])}</b>\n\nImtihonni boshlash uchun pastdagi tugmani bosing.",
        reply_markup=session_button(session["code"], session["title"]),
        parse_mode="HTML",
    )


def parse_start(args: str) -> tuple[str, int | None]:
    """Splits a deep link into its source label and the referrer, if any."""
    if args.startswith("ref_") and args[4:].isdigit():
        return "referral", int(args[4:])
    return args[:64], None


@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot, command: CommandObject):
    args = (command.args or "").strip()
    source, referrer = parse_start(args)
    await users.touch_user(message.from_user.model_dump(), source=source, referred_by=referrer, bot_started=True)

    if args.startswith("teacher_"):
        center = await centers.join_as_teacher(args[8:], message.from_user.id)
        if center is None:
            await message.answer("❌ Taklif havolasi eskirgan yoki noto'g'ri.")
        else:
            await message.answer(
                f"✅ Siz <b>{html.escape(center['name'])}</b> markazining o'qituvchisi sifatida qo'shildingiz.\n\n"
                "Mini App'dagi Profil bo'limida Markaz paneli paydo bo'ldi.",
                reply_markup=get_main_reply_keyboard(), parse_mode="HTML",
            )
        return

    user_id = message.from_user.id
    if not await subscription.may_use(bot, user_id):
        payload = args if args.startswith("s_") else ""
        await message.answer(WELCOME_LOCKED, reply_markup=get_join_inline_keyboard(payload), parse_mode="HTML")
        return

    if args.startswith("s_"):
        await answer_session(message, args[2:])
        return

    text = (
        f"👋 <b>Xush kelibsiz, {html.escape(message.from_user.first_name)}!</b>\n\n"
        "Mini App'da bugungi rejangiz, mock testlar, mashqlar va natijalaringiz bor.\n\n"
        "Quyidagi tugmalar orqali Mini App'ni ochishingiz yoki materiallar bo'limiga o'tishingiz mumkin:"
    )
    await message.answer(text, reply_markup=get_main_reply_keyboard(), parse_mode="HTML")
    await message.answer("📚 <b>O'quv materiallari bo'limlari:</b>", reply_markup=get_materials_inline_keyboard(), parse_mode="HTML")

@router.message(F.chat.type == "private", Command("menu"))
@router.message(F.chat.type == "private", Command("mock"))
async def cmd_menu(message: Message, command: CommandObject):
    if command.command == "mock" and command.args:
        await answer_session(message, command.args)
        return
    text = (
        "🎯 <b>IELTS va SAT Asosiy Menyu:</b>\n\n"
        "Pastdagi doimiy tugmalar orqali xohlagan bo'limni tanlashingiz mumkin:"
    )
    await message.answer(text, reply_markup=get_main_reply_keyboard(), parse_mode="HTML")

@router.message(F.chat.type == "private", F.text.contains("Mock"))
async def msg_mock_hub(message: Message):
    text = (
        "🎯 <b>IELTS & SAT Mock Tizimi</b>\n\n"
        "Mini App ichida quyidagi bo'limlar tayyor:\n\n"
        "• <b>Digital SAT Mock:</b> 98 ta savol (54 Reading & Writing + 44 Math), adaptiv 2-modul va batafsil hisobot\n"
        "• <b>Qisqa mashqlar:</b> mavzu bo'yicha 10 savol, xatolar daftari va takrorlash\n"
        "• <b>IELTS Listening:</b> 40 ta savol (Section 1–4), audio va tapescript bilan\n"
        "• <b>IELTS Reading:</b> 40 ta savol, to'liq uzunlikdagi testlar bilan\n"
        "• <b>IELTS Writing:</b> 46 ta mavzu va AI tekshiruvi\n\n"
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
        "📢 <b>IELTS va SAT O'quv Kanali:</b>\n\n"
        f"👉 {CHANNEL}\n\n"
        "Kanalda har kuni 10 ta post:\n"
        "• 08:00 — SAT va IELTS so'zlari, maslahat\n"
        "• 13:00 — SAT savoli va so'z testi\n"
        "• 18:00 — SAT Math, ibora va IELTS testi\n"
        "• 21:00 — IELTS Speaking savoli va qo'shimcha post"
    )
    await message.answer(text, reply_markup=get_main_reply_keyboard(), parse_mode="HTML")

@router.callback_query(F.data.startswith(CHECK_PREFIX))
async def callback_check_sub(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    payload = (callback.data or "")[len(CHECK_PREFIX):].lstrip(":")
    if not await subscription.may_use(bot, user_id, fresh=True):
        await callback.answer(NOT_JOINED_ALERT, show_alert=True)
        return

    await callback.answer()
    if payload.startswith("s_") and callback.message is not None:
        await answer_session(callback.message, payload[2:], user_id=user_id)
        return
    await callback.message.edit_text(
        "✅ <b>Obuna tasdiqlandi!</b> Barcha IELTS va SAT materiallari hamda Mock tizimi ochiq.\n\n"
        "O'zingizga kerakli manbani tanlang:",
        reply_markup=get_materials_inline_keyboard(),
        parse_mode="HTML"
    )
    await callback.message.answer("📱 Pastki menyu faollashtirildi:", reply_markup=get_main_reply_keyboard())

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
        "Kanalda har kuni:\n"
        "• 08:00 da SAT va IELTS so'zlari: o'zbekcha ma'nosi, misol va sinonimlari bilan\n"
        "• 13:00 da so'z testi\n"
        "• 18:00 da ibora yoki kollokatsiya\n\n"
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
        "Kanalda har kuni:\n"
        "• 13:00 da SAT savoli test shaklida\n"
        "• 18:00 da SAT Math savoli, javobi va izohi bilan\n"
        "• 08:00 da imtihon maslahati\n\n"
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
        for admin_id in ADMIN_IDS:
            try:
                await bot.send_message(
                    chat_id=admin_id,
                    text=f"📥 <b>Guruhdan yangi post tavsiyasi ({html.escape(message.chat.title or '')}):</b>\n\n{recreated_post}",
                    parse_mode="HTML"
                )
            except Exception:
                pass
