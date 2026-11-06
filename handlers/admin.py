"""
Admin and learning-center commands. Group exams themselves are managed in the Mini App's center panel.
"""

import html

from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message, WebAppInfo

from config import BOT_USERNAME, WEBAPP_URL
from scheduler import send_broadcast
from services import analytics, centers, users

router = Router()
_sending: set[int] = set()


def admin_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏫 Markaz panelini ochish", web_app=WebAppInfo(url=f"{WEBAPP_URL}?tab=center"))],
        [InlineKeyboardButton(text="🔄 Yangilash", callback_data="adm:refresh")],
        [InlineKeyboardButton(text="📈 Manbalar va voronka", callback_data="adm:report")],
        [InlineKeyboardButton(text="📣 Xabar yuborish", callback_data="adm:broadcast")],
        [InlineKeyboardButton(text="📋 Markazlar ro'yxati", callback_data="adm:centers")],
    ])


async def dashboard_text() -> str:
    stats = await centers.platform_stats()
    storage = "Postgres" if stats["storage"] == "postgres" else "SQLite (deploy'da o'chadi, DATABASE_URL qo'shing)"
    return (
        "📊 <b>Boshqaruv paneli</b>\n\n"
        f"👥 Foydalanuvchilar: <b>{stats['users']}</b> (botni boshlagan: {stats['started']})\n"
        f"🟢 Bugun faol: <b>{stats['active_today']}</b>, 7 kunda: <b>{stats['active_week']}</b>\n"
        f"📝 Bugungi urinishlar: <b>{stats['attempts_today']}</b>\n"
        f"🎯 Jami SAT mock: <b>{stats['mocks']}</b>\n"
        f"✍️ Bugungi AI tekshiruvlar: <b>{stats['essays_today']}</b>\n"
        f"💾 Saqlash: {storage}\n\n"
        "Yangi markaz: <code>/center_add Markaz nomi</code>"
    )


@router.message(F.chat.type == "private", Command("admin"))
async def cmd_admin(message: Message):
    user_id = message.from_user.id
    if centers.is_admin(user_id):
        await message.answer(await dashboard_text(), reply_markup=admin_keyboard(), parse_mode="HTML")
    elif await centers.is_staff(user_id):
        await message.answer(
            "🏫 Guruh imtihonlarini Markaz panelida boshqaring:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[admin_keyboard().inline_keyboard[0]]),
        )
    else:
        await message.answer("Bu buyruq faqat administrator va o'qituvchilar uchun.")


@router.callback_query(F.data == "adm:refresh")
async def cb_refresh(callback: CallbackQuery):
    if not centers.is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q", show_alert=True)
        return
    await callback.answer("Yangilandi")
    text = await dashboard_text()
    if text != callback.message.html_text:
        await callback.message.edit_text(text, reply_markup=admin_keyboard(), parse_mode="HTML")


@router.callback_query(F.data == "adm:report")
async def cb_report(callback: CallbackQuery):
    if not centers.is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q", show_alert=True)
        return
    await callback.answer()
    await callback.message.answer(await analytics.report_text(), parse_mode="HTML")


async def broadcast_help() -> str:
    lines = [
        "📣 <b>Xabar yuborish</b>\n",
        "1. Xabarni shu chatga yozing yoki rasm bilan tayyorlang.",
        "2. Unga javob (reply) sifatida <code>/broadcast segment</code> yozing.",
        "3. Bot sonini ko'rsatadi, siz tasdiqlaysiz.\n",
        "<b>Segmentlar</b> (eslatmalarni o'chirganlar kirmaydi):",
    ]
    for name, label in analytics.SEGMENT_NAMES.items():
        lines.append(f"• <code>{name}</code>: {label} ({await analytics.segment_size(name)})")
    return "\n".join(lines)


@router.callback_query(F.data == "adm:broadcast")
async def cb_broadcast_help(callback: CallbackQuery):
    if not centers.is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q", show_alert=True)
        return
    await callback.answer()
    await callback.message.answer(await broadcast_help(), parse_mode="HTML")


@router.message(F.chat.type == "private", Command("broadcast"))
async def cmd_broadcast(message: Message, command: CommandObject):
    if not centers.is_admin(message.from_user.id):
        return
    segment = analytics.find_segment(command.args)
    if segment is None or message.reply_to_message is None:
        await message.answer(await broadcast_help(), parse_mode="HTML")
        return
    source_id = message.reply_to_message.message_id
    count = await analytics.segment_size(segment)
    await message.answer(
        f"Javob berilgan xabar <b>{count}</b> kishiga yuboriladi: {analytics.SEGMENT_NAMES[segment]}.\n\n"
        "Yuborilgan xabarni qaytarib bo'lmaydi.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"✅ {count} kishiga yuborish", callback_data=f"bc:{segment}:{source_id}")],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="bc:cancel")],
        ]),
    )


@router.callback_query(F.data == "bc:cancel")
async def cb_broadcast_cancel(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Bekor qilindi.")


@router.callback_query(F.data.startswith("bc:"))
async def cb_broadcast_send(callback: CallbackQuery, bot: Bot):
    if not centers.is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q", show_alert=True)
        return
    _, segment, source_id = callback.data.split(":")
    key = int(source_id)
    if key in _sending or analytics.find_segment(segment) is None:
        await callback.answer("Bu xabar allaqachon yuborilmoqda.", show_alert=True)
        return
    _sending.add(key)
    await callback.answer("Yuborish boshlandi")
    await callback.message.edit_text("⏳ Yuborilmoqda...")
    sent, total = await send_broadcast(bot, segment, callback.message.chat.id, key)
    await users.record_event(callback.from_user.id, "broadcast", f"{segment}:{sent}/{total}")
    await callback.message.edit_text(f"✅ Yuborildi: {sent} / {total}")


def teacher_link(center: dict) -> str:
    return f"https://t.me/{BOT_USERNAME}?start=teacher_{center['teacher_code']}"


@router.callback_query(F.data == "adm:centers")
async def cb_centers(callback: CallbackQuery):
    if not centers.is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q", show_alert=True)
        return
    await callback.answer()
    rows = await centers.list_centers()
    if not rows:
        await callback.message.answer("Hali markaz yo'q. Qo'shish: <code>/center_add Markaz nomi</code>", parse_mode="HTML")
        return
    lines = ["🏫 <b>Markazlar</b>\n"]
    for row in rows:
        lines.append(f"<b>{html.escape(row['name'])}</b>: {row['students']} o'quvchi\n{teacher_link(row)}\n")
    await callback.message.answer("\n".join(lines), parse_mode="HTML", disable_web_page_preview=True)


@router.message(F.chat.type == "private", Command("center_add"))
async def cmd_center_add(message: Message, command: CommandObject):
    if not centers.is_admin(message.from_user.id):
        return
    name = (command.args or "").strip()
    if not name:
        await message.answer("Foydalanish: <code>/center_add Markaz nomi</code>", parse_mode="HTML")
        return
    center = await centers.create_center(name, message.from_user.id)
    await message.answer(
        f"✅ <b>{html.escape(center['name'])}</b> markazi yaratildi.\n\n"
        f"O'qituvchilar uchun taklif havolasi:\n{teacher_link(center)}",
        parse_mode="HTML", disable_web_page_preview=True,
    )
