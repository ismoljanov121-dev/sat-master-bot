"""
SAT Master AI - Infinite Practice Engine (Math, Reading, Writing)
Provides endless practice with authentic Digital SAT questions,
instant feedback, Desmos hacks, SAT grammar strategies, and streak tracking.
"""

import html
import re
import logging
from typing import Dict, Any, Optional
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database import db
from services.question_service import qs

logger = logging.getLogger("PracticeHandler")

router = Router()

def get_practice_hub_keyboard() -> InlineKeyboardMarkup:
    """Returns main navigation keyboard for Practice Mode."""
    buttons = [
        [
            InlineKeyboardButton(text="🎲 Cheksiz Tasodifiy Rejim (Mixed)", callback_data="prac_start_mixed")
        ],
        [
            InlineKeyboardButton(text="🧮 Digital SAT Math (Desmos Hack)", callback_data="prac_start_math"),
            InlineKeyboardButton(text="📖 Digital SAT Reading", callback_data="prac_start_reading")
        ],
        [
            InlineKeyboardButton(text="✍️ Digital SAT Writing & Grammar", callback_data="prac_start_writing")
        ],
        [
            InlineKeyboardButton(text="⬅️ Asosiy Menyu", callback_data="back_to_menu")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_practice_question_keyboard(q_data: Dict[str, Any], section: str) -> InlineKeyboardMarkup:
    """Builds inline keyboard for selecting answer options A, B, C, D."""
    buttons = []
    options = q_data.get("options", [])
    
    row1 = []
    row2 = []
    for opt in options:
        opt_text = opt.get('text', '')
        btn = InlineKeyboardButton(
            text=f"{opt['key']}) {opt_text[:25]}",
            callback_data=f"prac_ans_{opt['key']}"
        )
        if opt['key'] in ("A", "B"):
            row1.append(btn)
        else:
            row2.append(btn)
    
    if row1:
        buttons.append(row1)
    if row2:
        buttons.append(row2)

    buttons.append([
        InlineKeyboardButton(text="⏭️ O'tkazib yuborish (Skip)", callback_data=f"prac_next_{section}"),
        InlineKeyboardButton(text="⬅️ Mashq Menyusi", callback_data="practice_hub")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_post_answer_keyboard(q_data: Dict[str, Any], section: str) -> InlineKeyboardMarkup:
    """Builds keyboard after answering with Hack/Rule button and Next Question button."""
    q_sec = q_data.get("section", "math").lower()
    hack_label = "⚡ Desmos Hackni Ko'rish" if q_sec == "math" else "🎯 SAT Qoidasi & Taktikasi"
    
    buttons = [
        [
            InlineKeyboardButton(text=hack_label, callback_data=f"prac_hack_{q_data.get('id')}")
        ],
        [
            InlineKeyboardButton(text="Keyingi Savol ➡️", callback_data=f"prac_next_{section}"),
            InlineKeyboardButton(text="⬅️ Mashq Menyusi", callback_data="practice_hub")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def safe_edit_practice(callback: CallbackQuery, text: str, reply_markup: Optional[InlineKeyboardMarkup] = None):
    """Safely edits message with plain-text fallback on entity parser error."""
    try:
        await callback.message.edit_text(text, reply_markup=reply_markup, parse_mode="HTML")
    except Exception as e:
        logger.warning(f"HTML error in practice edit, falling back to plain text: {e}")
        try:
            clean_text = re.sub(r"<[^>]+>", "", text)
            await callback.message.edit_text(clean_text, reply_markup=reply_markup)
        except Exception as inner_e:
            logger.error(f"Fallback edit failed in practice: {inner_e}")

async def render_question_view(callback: CallbackQuery, q_data: Dict[str, Any], section: str):
    """Formats and renders a Digital SAT practice question."""
    user_id = callback.from_user.id
    stats = db.get_user_practice_stats(user_id)
    streak = stats.get("current_streak", 0)
    
    sec_titles = {
        "math": "🧮 DIGITAL SAT MATH",
        "reading": "📖 DIGITAL SAT READING",
        "writing": "✍️ DIGITAL SAT WRITING & GRAMMAR",
        "mixed": "🎲 CHEKSIZ SAT MASHQ"
    }
    header_title = sec_titles.get(section.lower(), "🎯 DIGITAL SAT MASHQ")
    
    domain = html.escape(q_data.get("domain", "General"))
    difficulty = html.escape(q_data.get("difficulty", "Medium"))
    passage = q_data.get("passage")
    question_text = html.escape(q_data.get("question", ""))
    
    lines = [
        f"<b>{header_title}</b>",
        "━━━━━━━━━━━━━━━━━━━━━━",
        f"📂 <b>Mavzu:</b> {domain}",
        f"📊 <b>Qiyinlik:</b> {difficulty} | 🔥 <b>Ketma-ketlik:</b> {streak} ta",
        "━━━━━━━━━━━━━━━━━━━━━━\n"
    ]
    
    if passage:
        clean_passage = html.escape(passage)
        lines.append(f"📄 <b>Matn (Passage):</b>\n<i>{clean_passage}</i>\n")
        
    lines.append(f"❓ <b>Savol:</b>\n{question_text}\n")
    lines.append("👇 <b>Variantlar:</b>")
    
    for opt in q_data.get("options", []):
        opt_key = html.escape(opt["key"])
        opt_text = html.escape(opt["text"])
        lines.append(f"<b>{opt_key})</b> {opt_text}")

    full_text = "\n".join(lines)
    kb = get_practice_question_keyboard(q_data, section)
    await safe_edit_practice(callback, full_text, reply_markup=kb)

@router.message(Command("practice"))
async def cmd_practice(message: Message):
    """Entry point via /practice command."""
    user_id = message.from_user.id
    user_name = html.escape(message.from_user.first_name or "Abituriyent")
    stats = db.get_user_practice_stats(user_id)
    
    total = stats.get("total_answered", 0)
    correct = stats.get("correct_count", 0)
    accuracy = stats.get("accuracy", 0)
    streak = stats.get("current_streak", 0)
    best_streak = stats.get("best_streak", 0)

    hub_text = (
        f"📚 <b>CHEKSIZ DIGITAL SAT MASHQ BAZASI</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Assalomu alaykum, <b>{user_name}</b>!\n"
        f"Bu yerda siz Digital SAT imtihonida tushadigan haqiqiy savollar ustida cheksiz mashq qilishingiz mumkin.\n\n"
        f"📊 <b>Sizning Natijalaringiz:</b>\n"
        f"• 📝 Jami yechilgan: <b>{total} ta</b>\n"
        f"• 🎯 To'g'ri javoblar: <b>{correct} ta</b>\n"
        f"• 📈 Umumiy aniqlik: <b>{accuracy}%</b>\n"
        f"• 🔥 Hozirgi ketma-ketlik: <b>{streak} ta</b> (Rekord: {best_streak})\n\n"
        f"👇 <i>Mashq qilish uchun kerakli bo'limni tanlang:</i>"
    )
    await message.answer(hub_text, reply_markup=get_practice_hub_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "practice_hub")
async def cb_practice_hub(callback: CallbackQuery):
    """Callback returning to the Practice Mode Hub."""
    try:
        user_id = callback.from_user.id
        user_name = html.escape(callback.from_user.first_name or "Abituriyent")
        stats = db.get_user_practice_stats(user_id)
        
        total = stats.get("total_answered", 0)
        correct = stats.get("correct_count", 0)
        accuracy = stats.get("accuracy", 0)
        streak = stats.get("current_streak", 0)
        best_streak = stats.get("best_streak", 0)

        hub_text = (
            f"📚 <b>CHEKSIZ DIGITAL SAT MASHQ BAZASI</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Assalomu alaykum, <b>{user_name}</b>!\n\n"
            f"📊 <b>Sizning Natijalaringiz:</b>\n"
            f"• 📝 Jami yechilgan: <b>{total} ta</b>\n"
            f"• 🎯 To'g'ri javoblar: <b>{correct} ta</b>\n"
            f"• 📈 Umumiy aniqlik: <b>{accuracy}%</b>\n"
            f"• 🔥 Hozirgi ketma-ketlik: <b>{streak} ta</b> (Rekord: {best_streak})\n\n"
            f"👇 <i>Mashq qilish uchun kerakli bo'limni tanlang:</i>"
        )
        await safe_edit_practice(callback, hub_text, reply_markup=get_practice_hub_keyboard())
    finally:
        try:
            await callback.answer()
        except Exception:
            pass

@router.callback_query(F.data.startswith("prac_start_"))
async def cb_start_practice_section(callback: CallbackQuery):
    """Starts practice in a specific section: mixed, math, reading, writing."""
    try:
        user_id = callback.from_user.id
        section = callback.data.replace("prac_start_", "").strip()
        
        answered_ids = db.get_answered_question_ids(user_id)
        q_data = qs.get_next_question(answered_ids, section=section)
        
        db.local_cache.setdefault("practice_sessions", {})
        db.local_cache["practice_sessions"][str(user_id)] = {
            "question_id": q_data["id"],
            "section": section,
            "q_data": q_data
        }
        db._save_local_db()

        await render_question_view(callback, q_data, section)
    finally:
        try:
            await callback.answer()
        except Exception:
            pass

@router.callback_query(F.data.startswith("prac_next_"))
async def cb_next_practice_question(callback: CallbackQuery):
    """Loads the next question in the active section."""
    try:
        user_id = callback.from_user.id
        section = callback.data.replace("prac_next_", "").strip()
        
        answered_ids = db.get_answered_question_ids(user_id)
        q_data = qs.get_next_question(answered_ids, section=section)
        
        db.local_cache.setdefault("practice_sessions", {})
        db.local_cache["practice_sessions"][str(user_id)] = {
            "question_id": q_data["id"],
            "section": section,
            "q_data": q_data
        }
        db._save_local_db()

        await render_question_view(callback, q_data, section)
    finally:
        try:
            await callback.answer()
        except Exception:
            pass

@router.callback_query(F.data.startswith("prac_ans_"))
async def cb_answer_practice(callback: CallbackQuery):
    """Evaluates the user's selected answer, records statistics, and presents explanation."""
    try:
        user_id = callback.from_user.id
        selected_key = callback.data.replace("prac_ans_", "").strip()
        
        session = db.local_cache.get("practice_sessions", {}).get(str(user_id))
        if not session or "q_data" not in session:
            await callback.answer("Savol ma'lumotlari yangilandi. Iltimos, yangi savolni boshlang.")
            return

        q_data = session["q_data"]
        section = session.get("section", "mixed")
        correct_key = q_data.get("correct", "A")
        is_correct = (selected_key.upper() == correct_key.upper())

        # Record in database
        db.record_practice_answer(user_id, q_data.get("id", ""), is_correct, q_data.get("section", "math"))
        
        stats = db.get_user_practice_stats(user_id)
        streak = stats.get("current_streak", 0)
        
        if is_correct:
            status_badge = f"🎉 <b>BARAKALLA, TO'G'RI JAVOB! (+1 ball)</b>\n🔥 Hozirgi ketma-ketlik: <b>{streak} ta</b>"
        else:
            status_badge = f"❌ <b>NOTO'G'RI JAVOB!</b>\nSiz tanladingiz: <b>{selected_key}</b> | To'g'ri javob: <b>{correct_key}</b>"

        explanation = html.escape(q_data.get("explanation", "Tushuntirish mavjud emas."))
        
        text = (
            f"{status_badge}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💡 <b>Tushuntirish (Explanation):</b>\n"
            f"{explanation}\n\n"
            f"👇 <i>Pastdagi tugmalar orqali ushbu savolning maxfiy Desmos/SAT hiylasini ko'ring yoki keyingisiga o'ting:</i>"
        )
        
        kb = get_post_answer_keyboard(q_data, section)
        await safe_edit_practice(callback, text, reply_markup=kb)
    finally:
        try:
            await callback.answer()
        except Exception:
            pass

@router.callback_query(F.data.startswith("prac_hack_"))
async def cb_show_hack(callback: CallbackQuery):
    """Displays the Desmos Hack or SAT Strategy for the active question."""
    try:
        user_id = callback.from_user.id
        qid = callback.data.replace("prac_hack_", "").strip()
        
        session = db.local_cache.get("practice_sessions", {}).get(str(user_id), {})
        q_data = session.get("q_data")
        section = session.get("section", "mixed")
        
        if not q_data or str(q_data.get("id")) != qid:
            q_data = qs.get_question_by_id(qid)

        if not q_data:
            await callback.answer("Hiyla ma'lumoti topilmadi.")
            return

        hack_text = html.escape(q_data.get("strategy_or_hack", "Ushbu savol uchun hiyla qo'shilmagan."))
        q_sec = q_data.get("section", "math").lower()
        title = "⚡ <b>DESMOS CHEATCODE & HACK</b>" if q_sec == "math" else "🎯 <b>DIGITAL SAT STRATEGIYASI & QOIDASI</b>"

        text = (
            f"{title}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{hack_text}\n\n"
            f"💡 <i>Ushbu usul sizga imtihonda qimmatli 1-2 daqiqa vaqtni tejashga yordam beradi!</i>"
        )

        buttons = [
            [InlineKeyboardButton(text="Keyingi Savol ➡️", callback_data=f"prac_next_{section}")],
            [InlineKeyboardButton(text="⬅️ Mashq Menyusi", callback_data="practice_hub")]
        ]
        await safe_edit_practice(callback, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    finally:
        try:
            await callback.answer()
        except Exception:
            pass
