"""
EduTest Pro - Student Error Notebook (Xatolarim Daftari)
Tracks every missed or skipped question across Diagnostic, Practice, and Mock tests.
Enables targeted spaced-repetition re-testing until mastery.
"""

import html
import logging
import re
from typing import Any

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from database import db
from services.question_service import qs

logger = logging.getLogger("MistakesHandler")

router = Router()


def get_notebook_main_keyboard(has_unresolved: bool) -> InlineKeyboardMarkup:
    buttons = []
    if has_unresolved:
        buttons.append([
            InlineKeyboardButton(
                text="🔄 Xatolar ustida qayta mashq",
                callback_data="nb_practice"
            )
        ])
    buttons.append([
        InlineKeyboardButton(
            text="📋 Xatolar ro'yxati",
            callback_data="nb_list:0"
        )
    ])
    buttons.append([
        InlineKeyboardButton(
            text="🗑️ Daftarni tozalash",
            callback_data="nb_clear_confirm"
        ),
        InlineKeyboardButton(
            text="⬅️ Asosiy Menyu",
            callback_data="back_to_menu"
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def safe_edit(callback: CallbackQuery, text: str, reply_markup: InlineKeyboardMarkup | None = None) -> None:
    try:
        await callback.message.edit_text(text, reply_markup=reply_markup, parse_mode="HTML")
    except TelegramBadRequest as e:
        if "message is not modified" in str(e).lower():
            return
        plain_text = re.sub(r"<[^>]+>", "", text)
        try:
            await callback.message.edit_text(plain_text, reply_markup=reply_markup)
        except Exception:
            pass
    except Exception as e:
        logger.error(f"Error in safe_edit mistakes: {e}")


def format_notebook_dashboard_text(user_id: int) -> tuple[str, bool]:
    all_mistakes = db.get_user_mistakes(user_id, resolved_filter=None)
    unresolved = [m for m in all_mistakes if not m.get("resolved")]
    resolved = [m for m in all_mistakes if m.get("resolved")]

    total_count = len(all_mistakes)
    unresolved_count = len(unresolved)
    resolved_count = len(resolved)

    sec_stats = {"math": 0, "reading": 0, "writing": 0}
    for m in unresolved:
        s = str(m.get("section", "math")).lower()
        if s in sec_stats:
            sec_stats[s] += 1

    lines = [
        "❌ <b>XATOLARIM DAFTARI (ERROR NOTEBOOK)</b>",
        "━━━━━━━━━━━━━━━━━━━━━━",
        "Bu yerda siz diagnostika, mashq yoki mock testlarda xato qilgan "
        "barcha savollaringiz jamlangan. Maqsad — har bir xatoni o'rganib, uni yechishni o'zlashtirish.\n",
        "📊 <b>Umumiy holat:</b>",
        f"• 🔴 Hal qilinmagan xatolar: <b>{unresolved_count} ta</b>",
        f"• 🟢 O'zlashtirilgan xatolar: <b>{resolved_count} ta</b>",
        f"• 📁 Jami qayd etilgan: <b>{total_count} ta</b>\n",
        "📂 <b>Faol xatolar bo'limlar bo'yicha:</b>",
        f"• 🧮 Math: <b>{sec_stats['math']} ta</b>",
        f"• 📖 Reading: <b>{sec_stats['reading']} ta</b>",
        f"• ✍️ Writing: <b>{sec_stats['writing']} ta</b>\n"
    ]

    if unresolved_count > 0:
        lines.append("👇 <i>'Xatolar ustida qayta mashq' tugmasini bosing va noaniq mavzularni to'liq o'zlashtiring:</i>")
    else:
        lines.append("🌟 <b>Hozircha barcha xatolaringiz o'zlashtirilgan yoki daftaringiz bo'sh!</b>")

    return "\n".join(lines), (unresolved_count > 0)


@router.message(Command("mistakes"))
@router.message(Command("xatolar"))
async def cmd_mistakes(message: Message):
    user_id = message.from_user.id
    text, has_unresolved = format_notebook_dashboard_text(user_id)
    await message.answer(text, reply_markup=get_notebook_main_keyboard(has_unresolved), parse_mode="HTML")


@router.callback_query(F.data == "notebook_menu")
async def cb_notebook_menu(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        text, has_unresolved = format_notebook_dashboard_text(user_id)
        await safe_edit(callback, text, get_notebook_main_keyboard(has_unresolved))
    finally:
        try:
            await callback.answer()
        except Exception:
            pass


@router.callback_query(F.data == "nb_practice")
async def cb_start_mistake_practice(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        unresolved = db.get_user_mistakes(user_id, resolved_filter=False)

        if not unresolved:
            text = (
                "🎉 <b>Ajoyib natija!</b>\n\n"
                "Siz barcha xatolaringizni muvaffaqiyatli bartaraf etdingiz. "
                "Hozirda hal qilinmagan xatolar qolmadi!"
            )
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Xatolar Daftari", callback_data="notebook_menu")],
                [InlineKeyboardButton(text="🎯 Asosiy Menyu", callback_data="back_to_menu")]
            ])
            await safe_edit(callback, text, kb)
            return

        target_item = unresolved[0]
        qid = target_item.get("question_id", "")
        options = target_item.get("options") or []

        if not options:
            full_q = qs.get_question_by_id(qid)
            if full_q:
                options = full_q.get("options", [])

        sec = html.escape(str(target_item.get("section", "math")).upper())
        domain = html.escape(str(target_item.get("domain", "General")))
        q_text = html.escape(str(target_item.get("question_text", "")))
        passage = target_item.get("passage")

        lines = [
            f"🔄 <b>XATOLAR USTIDA MASHQ (1/{len(unresolved)})</b>",
            f"📂 <b>Bo'lim:</b> {sec} | <b>Mavzu:</b> {domain}",
            "━━━━━━━━━━━━━━━━━━━━━━\n"
        ]
        if passage:
            lines.append(f"📄 <b>Matn:</b>\n<i>{html.escape(str(passage))}</i>\n")

        lines.append(f"<b>{q_text}</b>\n")
        lines.append("👇 <i>To'g'ri javob variantini tanlang:</i>")

        buttons = []
        row1, row2 = [], []
        for opt in options:
            k = opt.get("key", "")
            t = opt.get("text", "")
            btn = InlineKeyboardButton(text=f"{k}) {t[:28]}", callback_data=f"nb_a:{qid}:{k}")
            if k in ("A", "B"):
                row1.append(btn)
            else:
                row2.append(btn)

        if row1:
            buttons.append(row1)
        if row2:
            buttons.append(row2)

        buttons.append([
            InlineKeyboardButton(text="💡 Tushuntirishni ko'rish", callback_data=f"nb_view:{qid}"),
            InlineKeyboardButton(text="⬅️ Daftarga qaytish", callback_data="notebook_menu")
        ])

        await safe_edit(callback, "\n".join(lines), InlineKeyboardMarkup(inline_keyboard=buttons))
    finally:
        try:
            await callback.answer()
        except Exception:
            pass


@router.callback_query(F.data.startswith("nb_a:"))
async def cb_answer_mistake_practice(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        parts = callback.data.split(":")
        if len(parts) < 3:
            return

        qid = parts[1]
        selected_key = parts[2].upper()

        unresolved = db.get_user_mistakes(user_id, resolved_filter=False)
        target = next((m for m in unresolved if str(m.get("question_id")) == qid), None)

        if not target:
            await callback.answer("Ushbu savol allaqachon hal qilingan!", show_alert=True)
            text, has_unresolved = format_notebook_dashboard_text(user_id)
            await safe_edit(callback, text, get_notebook_main_keyboard(has_unresolved))
            return

        correct_key = str(target.get("correct_answer", "A")).strip().upper()
        is_correct = (selected_key == correct_key)

        explanation = html.escape(str(target.get("explanation", "Tushuntirish berilmagan.")))
        hack = html.escape(str(target.get("hack", "")))

        if is_correct:
            await db.resolve_mistake(user_id, qid)
            status_text = (
                "🎉 <b>BARAKALLA! XATO BARTARAF ETILDI!</b>\n"
                f"Siz to'g'ri javob berdingiz: <b>{selected_key}</b>.\n"
                "Ushbu savol muvaffaqiyatli 'O'zlashtirilgan' deb belgilandi."
            )
        else:
            status_text = (
                "❌ <b>QAYTA XATO BO'LDI</b>\n"
                f"Siz tanladingiz: <b>{selected_key}</b> | To'g'ri javob: <b>{correct_key}</b>\n"
                "Savol daftarda faol qoladi. Yechim tahlilini diqqat bilan o'rganing:"
            )

        report_lines = [
            status_text,
            "━━━━━━━━━━━━━━━━━━━━━━",
            f"💡 <b>Tushuntirish:</b>\n{explanation}\n"
        ]
        if hack:
            report_lines.append(f"⚡ <b>Desmos / Strategik hiyla:</b>\n{hack}\n")

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Keyingi xato ➡️", callback_data="nb_practice")],
            [InlineKeyboardButton(text="⬅️ Xatolar Daftari", callback_data="notebook_menu")]
        ])
        await safe_edit(callback, "\n".join(report_lines), kb)
    finally:
        try:
            await callback.answer()
        except Exception:
            pass


@router.callback_query(F.data.startswith("nb_list:"))
async def cb_list_mistakes(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        page = int(callback.data.split(":")[1])
        all_mistakes = db.get_user_mistakes(user_id, resolved_filter=None)

        if not all_mistakes:
            text = (
                "📂 <b>XATOLAR RO'YXATI BO'SH</b>\n\n"
                "Sizda hozircha birorta ham qayd etilgan xato yo'q. "
                "Diagnostika yoki mashqlarni yechish orqali bilimlaringizni sinab ko'ring."
            )
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Daftarga Qaytish", callback_data="notebook_menu")]
            ])
            await safe_edit(callback, text, kb)
            return

        page_size = 5
        total_pages = (len(all_mistakes) + page_size - 1) // page_size
        page = max(0, min(page, total_pages - 1))
        page_items = all_mistakes[page * page_size : (page + 1) * page_size]

        lines = [
            f"📋 <b>QAYD ETILGAN XATOLAR ({page + 1}/{total_pages}-sahifa)</b>",
            "━━━━━━━━━━━━━━━━━━━━━━"
        ]

        buttons = []
        for idx, item in enumerate(page_items):
            qid = item.get("question_id", "")
            sec = str(item.get("section", "math")).upper()
            dom = item.get("domain", "General")
            resolved = item.get("resolved", False)
            status_icon = "🟢" if resolved else "🔴"
            q_short = (item.get("question_text") or "")[:45]

            lines.append(f"{idx + 1}. {status_icon} <b>[{sec}]</b> {dom}: <i>{html.escape(q_short)}...</i>")
            buttons.append([
                InlineKeyboardButton(
                    text=f"{status_icon} {idx + 1}-savol tahlili",
                    callback_data=f"nb_view:{qid}"
                )
            ])

        nav_row = []
        if page > 0:
            nav_row.append(InlineKeyboardButton(text="◀️ Oldingi", callback_data=f"nb_list:{page - 1}"))
        if page + 1 < total_pages:
            nav_row.append(InlineKeyboardButton(text="Keyingi ▶️", callback_data=f"nb_list:{page + 1}"))

        if nav_row:
            buttons.append(nav_row)

        buttons.append([InlineKeyboardButton(text="⬅️ Daftarga Qaytish", callback_data="notebook_menu")])

        await safe_edit(callback, "\n".join(lines), InlineKeyboardMarkup(inline_keyboard=buttons))
    finally:
        try:
            await callback.answer()
        except Exception:
            pass


@router.callback_query(F.data.startswith("nb_view:"))
async def cb_view_single_mistake(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        qid = callback.data.replace("nb_view:", "").strip()
        all_mistakes = db.get_user_mistakes(user_id, resolved_filter=None)
        item = next((m for m in all_mistakes if str(m.get("question_id")) == qid), None)

        if not item:
            await callback.answer("Savol topilmadi.", show_alert=True)
            return

        sec = html.escape(str(item.get("section", "math")).upper())
        dom = html.escape(str(item.get("domain", "General")))
        q_text = html.escape(str(item.get("question_text", "")))
        corr = html.escape(str(item.get("correct_answer", "")))
        user_ans = html.escape(str(item.get("user_answer", "-")))
        exp = html.escape(str(item.get("explanation", "Tushuntirish yo'q.")))
        hack = html.escape(str(item.get("hack", "")))
        resolved = item.get("resolved", False)

        lines = [
            f"🔍 <b>SAVOL TAHLILI [{sec} - {dom}]</b>",
            f"Holati: {'🟢 O\'zlashtirilgan' if resolved else '🔴 Faol xato'}",
            "━━━━━━━━━━━━━━━━━━━━━━\n",
            f"<b>Savol:</b>\n{q_text}\n",
            f"❌ <b>Sizning javobingiz:</b> {user_ans}",
            f"✅ <b>To'g'ri javob:</b> {corr}\n",
            f"💡 <b>Tushuntirish:</b>\n{exp}\n"
        ]
        if hack:
            lines.append(f"⚡ <b>Desmos / Strategiya:</b>\n{hack}\n")

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Ro'yxatga Qaytish", callback_data="nb_list:0")],
            [InlineKeyboardButton(text="⬅️ Xatolar Daftari", callback_data="notebook_menu")]
        ])
        await safe_edit(callback, "\n".join(lines), kb)
    finally:
        try:
            await callback.answer()
        except Exception:
            pass


@router.callback_query(F.data == "nb_clear_confirm")
async def cb_clear_notebook_confirm(callback: CallbackQuery):
    text = (
        "⚠️ <b>DIQQAT: Xatolar daftarini tozalashni xohlaysizmi?</b>\n\n"
        "Barcha qayd etilgan xatolar tarixingiz o'chiriladi. "
        "Ushbu amalni ortga qaytarib bo'lmaydi."
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗑️ Ha, tozalansin", callback_data="nb_clear_exec")],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="notebook_menu")]
    ])
    await safe_edit(callback, text, kb)
    await callback.answer()


@router.callback_query(F.data == "nb_clear_exec")
async def cb_clear_notebook_exec(callback: CallbackQuery):
    user_id = callback.from_user.id
    str_id = str(user_id)
    if "error_notebook" in db.local_cache and str_id in db.local_cache["error_notebook"]:
        db.local_cache["error_notebook"][str_id] = {}
        await db._atomic_save_local()

    text = "✅ <b>Xatolar daftari muvaffaqiyatli tozalandi!</b>"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Asosiy Menyu", callback_data="back_to_menu")]
    ])
    await safe_edit(callback, text, kb)
    await callback.answer("Tozalandi", show_alert=True)
