"""
Admin and learning-center commands. Group exams themselves are managed in the Mini App's center panel.
"""

import html

from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message, WebAppInfo

from config import BOT_USERNAME, WEBAPP_URL
from services import centers, promo

router = Router()


def admin_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏫 Markaz panelini ochish", web_app=WebAppInfo(url=f"{WEBAPP_URL}?tab=center"))],
        [InlineKeyboardButton(text="🔄 Yangilash", callback_data="adm:refresh")],
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
        f"📣 Reklama tugmasidan kelganlar: <b>{stats['promo']}</b>\n"
        f"💾 Saqlash: {storage}\n\n"
        "Yangi markaz: <code>/center_add Markaz nomi</code>\n"
        "Reklama posti: <code>/reklama</code>"
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


@router.message(F.chat.type == "private", Command("reklama"))
async def cmd_promo(message: Message):
    """An admin sends a video captioned /reklama and gets back the advert post, ready to forward."""
    if not centers.is_admin(message.from_user.id):
        return
    if message.video:
        await message.answer_video(
            message.video.file_id, caption=promo.CAPTION, reply_markup=promo.keyboard(), parse_mode="HTML",
            supports_streaming=True,
        )
        return
    if message.animation:
        await message.answer_animation(
            message.animation.file_id, caption=promo.CAPTION, reply_markup=promo.keyboard(), parse_mode="HTML",
        )
        return
    await message.answer(promo.HELP, parse_mode="HTML")
    await message.answer(promo.CAPTION, reply_markup=promo.keyboard(), parse_mode="HTML", disable_web_page_preview=True)


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
