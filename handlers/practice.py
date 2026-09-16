"""
EduTest Pro - Infinite Practice Engine (Math, Reading, Writing)
Provides endless practice with authentic Digital SAT questions,
topic (domain) & difficulty filters, instant feedback, Desmos strategies,
SAT grammar strategies, and streak tracking.
"""

import html
import logging
import re
from typing import Any

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from database import db
from services.question_service import qs

logger = logging.getLogger("PracticeHandler")

router = Router()

# ==================== USER FILTER STATE ====================

def get_user_filters(user_id: int) -> dict[str, str]:
    """Gets or initializes user practice filters."""
    db.local_cache.setdefault("practice_filters", {})
    return db.local_cache["practice_filters"].setdefault(str(user_id), {
        "section": "mixed",
        "difficulty": "all",
        "domain": "all"
    })

def set_user_filter(user_id: int, key: str, value: str):
    """Sets a specific filter parameter for the user."""
    filters = get_user_filters(user_id)
    filters[key] = value
    db._save_local_db()

def reset_user_filters(user_id: int):
    """Resets all filters to default (mixed, all, all)."""
    db.local_cache.setdefault("practice_filters", {})
    db.local_cache["practice_filters"][str(user_id)] = {
        "section": "mixed",
        "difficulty": "all",
        "domain": "all"
    }
    db._save_local_db()

# ==================== KEYBOARDS ====================

def get_practice_hub_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Returns main navigation keyboard for Practice Mode with active filter badges."""
    filters = get_user_filters(user_id)
    sec = filters.get("section", "mixed")
    diff = filters.get("difficulty", "all")
    dom = filters.get("domain", "all")

    sec_label = {
        "mixed": "🎲 Mixed (Aralash)",
        "math": "🧮 Math (Matematika)",
        "reading": "📖 Reading (O'qish)",
        "writing": "✍️ Writing (Grammatika)"
    }.get(sec, "🎲 Mixed")

    diff_label = {
        "all": "⚪ Barchasi",
        "easy": "🟢 Oson (Easy)",
        "medium": "🟡 O'rtacha (Med)",
        "hard": "🔴 Qiyin (Hard)"
    }.get(diff.lower(), "⚪ Barchasi")

    dom_label = "⚪ Barcha Mavzular" if dom == "all" else f"📂 {dom.title()[:14]}.."

    buttons = [
        [
            InlineKeyboardButton(text="🚀 Mashqni Boshlash", callback_data="prac_start_active")
        ],
        [
            InlineKeyboardButton(text=f"Bo'lim: {sec_label}", callback_data="prac_menu_sec")
        ],
        [
            InlineKeyboardButton(text=f"Qiyinlik: {diff_label}", callback_data="prac_menu_diff"),
            InlineKeyboardButton(text=f"Mavzu: {dom_label}", callback_data="prac_menu_dom")
        ],
        [
            InlineKeyboardButton(text="🔄 Filtrlarni Tozalash", callback_data="prac_reset_filters"),
            InlineKeyboardButton(text="⬅️ Asosiy Menyu", callback_data="back_to_menu")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_section_selector_keyboard() -> InlineKeyboardMarkup:
    """Submenu to pick Section."""
    buttons = [
        [InlineKeyboardButton(text="🎲 Mixed (Barcha Bo'limlar)", callback_data="prac_set_sec_mixed")],
        [
            InlineKeyboardButton(text="🧮 Digital SAT Math", callback_data="prac_set_sec_math"),
            InlineKeyboardButton(text="📖 Digital SAT Reading", callback_data="prac_set_sec_reading")
        ],
        [InlineKeyboardButton(text="✍️ Digital SAT Writing & Grammar", callback_data="prac_set_sec_writing")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="practice_hub")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_difficulty_selector_keyboard() -> InlineKeyboardMarkup:
    """Submenu to pick Difficulty."""
    buttons = [
        [InlineKeyboardButton(text="⚪ Barcha Qiyinliklar (All)", callback_data="prac_set_diff_all")],
        [InlineKeyboardButton(text="🟢 Oson (Easy)", callback_data="prac_set_diff_easy")],
        [InlineKeyboardButton(text="🟡 O'rtacha (Medium)", callback_data="prac_set_diff_medium")],
        [InlineKeyboardButton(text="🔴 Qiyin (Hard)", callback_data="prac_set_diff_hard")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="practice_hub")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_domain_selector_keyboard(section: str) -> InlineKeyboardMarkup:
    """Submenu to pick SAT Domain based on the active section."""
    buttons = []
    sec = section.lower()

    if sec in ("math", "mixed"):
        buttons.extend([
            [InlineKeyboardButton(text="📐 Algebra (Linear Equations & Systems)", callback_data="prac_set_dom_algebra")],
            [InlineKeyboardButton(text="📈 Advanced Math (Quadratics & Vertex)", callback_data="prac_set_dom_advanced")],
            [InlineKeyboardButton(text="📊 Problem Solving (Percentages & Stats)", callback_data="prac_set_dom_problem")],
            [InlineKeyboardButton(text="📏 Geometry & Trig (Circles & Triangles)", callback_data="prac_set_dom_geometry")]
        ])
    elif sec == "reading":
        buttons.extend([
            [InlineKeyboardButton(text="🔤 Words in Context (Craft & Structure)", callback_data="prac_set_dom_words")],
            [InlineKeyboardButton(text="📖 Central Ideas & Details", callback_data="prac_set_dom_ideas")],
            [InlineKeyboardButton(text="🔍 Command of Evidence & Inferences", callback_data="prac_set_dom_evidence")]
        ])
    elif sec == "writing":
        buttons.extend([
            [InlineKeyboardButton(text="✒️ Boundaries & Punctuation", callback_data="prac_set_dom_boundaries")],
            [InlineKeyboardButton(text="📝 Form, Structure & Modifiers", callback_data="prac_set_dom_structure")],
            [InlineKeyboardButton(text="🔄 Transitions & Connectors", callback_data="prac_set_dom_transitions")],
            [InlineKeyboardButton(text="📑 Rhetorical Synthesis (Notes)", callback_data="prac_set_dom_rhetorical")]
        ])

    buttons.append([InlineKeyboardButton(text="⚪ Barcha Mavzular (All Topics)", callback_data="prac_set_dom_all")])
    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="practice_hub")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_practice_question_keyboard(q_data: dict[str, Any], section: str) -> InlineKeyboardMarkup:
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


def get_post_answer_keyboard(q_data: dict[str, Any], section: str) -> InlineKeyboardMarkup:
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


async def safe_edit_practice(callback: CallbackQuery, text: str, reply_markup: InlineKeyboardMarkup | None = None):
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


async def render_question_view(callback: CallbackQuery, q_data: dict[str, Any], section: str):
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
    
    domain = html.escape(str(q_data.get("domain", "General")))
    difficulty = html.escape(str(q_data.get("difficulty", "Medium")))
    passage = q_data.get("passage")
    question_text = html.escape(str(q_data.get("question", "")))
    
    lines = [
        f"<b>{header_title}</b>",
        "━━━━━━━━━━━━━━━━━━━━━━",
        f"📂 <b>Mavzu:</b> {domain}",
        f"📊 <b>Qiyinlik:</b> {difficulty} | 🔥 <b>Ketma-ketlik:</b> {streak} ta",
        "━━━━━━━━━━━━━━━━━━━━━━\n"
    ]
    
    if passage:
        clean_passage = html.escape(str(passage))
        lines.append(f"📄 <b>Matn (Passage / Notes):</b>\n<i>{clean_passage}</i>\n")
        
    lines.append(f"❓ <b>Savol:</b>\n{question_text}\n")
    lines.append("👇 <b>Variantlar:</b>")
    
    for opt in q_data.get("options", []):
        opt_key = html.escape(opt.get("key", ""))
        opt_text = html.escape(opt.get("text", ""))
        lines.append(f"<b>{opt_key})</b> {opt_text}")

    full_text = "\n".join(lines)
    kb = get_practice_question_keyboard(q_data, section)
    await safe_edit_practice(callback, full_text, reply_markup=kb)


# ==================== ENTRY POINTS & MENUS ====================

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

    filters = get_user_filters(user_id)
    sec_badge = filters.get("section", "mixed").upper()
    diff_badge = filters.get("difficulty", "all").capitalize()
    dom_badge = filters.get("domain", "all")

    hub_text = (
        f"📚 <b>CHEKSIZ DIGITAL SAT MASHQ BAZASI</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Assalomu alaykum, <b>{user_name}</b>!\n"
        f"Bu yerda siz Digital SAT imtihoni savollarini mavzu va qiyinlik bo'yicha saralab mashq qilishingiz mumkin.\n\n"
        f"📊 <b>Sizning Natijalaringiz:</b>\n"
        f"• 📝 Jami yechilgan: <b>{total} ta</b>\n"
        f"• 🎯 To'g'ri javoblar: <b>{correct} ta</b> (Aniqlik: <b>{accuracy}%</b>)\n"
        f"• 🔥 Hozirgi ketma-ketlik: <b>{streak} ta</b> (Rekord: {best_streak})\n\n"
        f"⚙️ <b>Faol Filtrlar:</b>\n"
        f"• Bo'lim: <code>{sec_badge}</code> | Qiyinlik: <code>{diff_badge}</code>\n"
        f"• Mavzu: <code>{dom_badge}</code>\n\n"
        f"👇 <i>Mashqni boshlash uchun '🚀 Mashqni Boshlash' tugmasini bosing yoki filtrlarni moslang:</i>"
    )
    await message.answer(hub_text, reply_markup=get_practice_hub_keyboard(user_id), parse_mode="HTML")


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

        filters = get_user_filters(user_id)
        sec_badge = filters.get("section", "mixed").upper()
        diff_badge = filters.get("difficulty", "all").capitalize()
        dom_badge = filters.get("domain", "all")

        hub_text = (
            f"📚 <b>CHEKSIZ DIGITAL SAT MASHQ BAZASI</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Assalomu alaykum, <b>{user_name}</b>!\n\n"
            f"📊 <b>Sizning Natijalaringiz:</b>\n"
            f"• 📝 Jami yechilgan: <b>{total} ta</b>\n"
            f"• 🎯 To'g'ri javoblar: <b>{correct} ta</b> (Aniqlik: <b>{accuracy}%</b>)\n"
            f"• 🔥 Hozirgi ketma-ketlik: <b>{streak} ta</b> (Rekord: {best_streak})\n\n"
            f"⚙️ <b>Faol Filtrlar:</b>\n"
            f"• Bo'lim: <code>{sec_badge}</code> | Qiyinlik: <code>{diff_badge}</code>\n"
            f"• Mavzu: <code>{dom_badge}</code>\n\n"
            f"👇 <i>Mashqni boshlash yoki filtrlarni sozlash:</i>"
        )
        await safe_edit_practice(callback, hub_text, reply_markup=get_practice_hub_keyboard(user_id))
    finally:
        try:
            await callback.answer()
        except Exception:
            pass


# ==================== FILTER SUBMENUS ====================

@router.callback_query(F.data == "prac_menu_sec")
async def cb_menu_sec(callback: CallbackQuery):
    """Opens section selector menu."""
    text = (
        f"🔀 <b>BO'LIMNI TANLANG</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Qaysi yo'nalish bo'yicha mashq qilmoqchisiz?\n"
        f"• <b>Math</b>: Algebra, Advanced Math, Geometriya, Desmos\n"
        f"• <b>Reading</b>: Words in Context, Central Ideas, Evidence\n"
        f"• <b>Writing</b>: Punctuation, Grammar, Transitions, Synthesis\n"
        f"• <b>Mixed</b>: Barcha bo'limlardan aralash"
    )
    await safe_edit_practice(callback, text, reply_markup=get_section_selector_keyboard())
    await callback.answer()


@router.callback_query(F.data == "prac_menu_diff")
async def cb_menu_diff(callback: CallbackQuery):
    """Opens difficulty selector menu."""
    text = (
        f"🎯 <b>QIYINLIK DARAJASINI TANLANG</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"• <b>🟢 Oson (Easy)</b>: Asosiy fundamental qoidalar va tushunchalar\n"
        f"• <b>🟡 O'rtacha (Medium)</b>: Standart SAT darajasidagi savollar\n"
        f"• <b>🔴 Qiyin (Hard)</b>: Hard Module 2 (700-800 ballik) nozik savollar\n"
        f"• <b>⚪ Barchasi</b>: Aralash murakkablik"
    )
    await safe_edit_practice(callback, text, reply_markup=get_difficulty_selector_keyboard())
    await callback.answer()


@router.callback_query(F.data == "prac_menu_dom")
async def cb_menu_dom(callback: CallbackQuery):
    """Opens domain selector menu based on active section."""
    user_id = callback.from_user.id
    filters = get_user_filters(user_id)
    sec = filters.get("section", "mixed")

    text = (
        f"📂 <b>SAT MAVZUSINI (DOMAIN) TANLANG</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Tanlangan bo'lim: <b>{sec.upper()}</b>\n"
        f"O'zingiz kuchaytirmoqchi bo'lgan aniq zaif mavzuni belgilang:"
    )
    await safe_edit_practice(callback, text, reply_markup=get_domain_selector_keyboard(sec))
    await callback.answer()


@router.callback_query(F.data.startswith("prac_set_sec_"))
async def cb_set_section(callback: CallbackQuery):
    """Updates selected section filter."""
    user_id = callback.from_user.id
    val = callback.data.replace("prac_set_sec_", "").strip()
    set_user_filter(user_id, "section", val)
    # Reset domain when section changes
    set_user_filter(user_id, "domain", "all")
    await cb_practice_hub(callback)


@router.callback_query(F.data.startswith("prac_set_diff_"))
async def cb_set_difficulty(callback: CallbackQuery):
    """Updates selected difficulty filter."""
    user_id = callback.from_user.id
    val = callback.data.replace("prac_set_diff_", "").strip()
    set_user_filter(user_id, "difficulty", val)
    await cb_practice_hub(callback)


@router.callback_query(F.data.startswith("prac_set_dom_"))
async def cb_set_domain(callback: CallbackQuery):
    """Updates selected domain filter."""
    user_id = callback.from_user.id
    raw = callback.data.replace("prac_set_dom_", "").strip()
    domain_map = {
        "algebra": "Algebra",
        "advanced": "Advanced Math",
        "problem": "Problem Solving",
        "geometry": "Geometry",
        "words": "Words in Context",
        "ideas": "Central Ideas",
        "evidence": "Command of Evidence",
        "boundaries": "Boundaries",
        "structure": "Form, Structure",
        "transitions": "Transitions",
        "rhetorical": "Rhetorical Synthesis",
        "all": "all"
    }
    val = domain_map.get(raw, "all")
    set_user_filter(user_id, "domain", val)
    await cb_practice_hub(callback)


@router.callback_query(F.data == "prac_reset_filters")
async def cb_reset_filters(callback: CallbackQuery):
    """Resets all filters to default."""
    user_id = callback.from_user.id
    reset_user_filters(user_id)
    await cb_practice_hub(callback)


# ==================== QUESTION DELIVERY & ANSWERING ====================

@router.callback_query(F.data.in_(["prac_start_active", "prac_next_active"]))
async def cb_start_active_practice(callback: CallbackQuery):
    """Starts or continues practice using active user filters."""
    try:
        user_id = callback.from_user.id
        filters = get_user_filters(user_id)
        sec = filters.get("section", "mixed")
        diff = filters.get("difficulty", "all")
        dom = filters.get("domain", "all")
        
        answered_ids = db.get_answered_question_ids(user_id)
        q_data = qs.get_next_filtered_question(answered_ids, section=sec, domain=dom, difficulty=diff)
        
        db.local_cache.setdefault("practice_sessions", {})
        db.local_cache["practice_sessions"][str(user_id)] = {
            "question_id": q_data["id"],
            "section": sec,
            "q_data": q_data
        }
        db._save_local_db()

        await render_question_view(callback, q_data, sec)
    finally:
        try:
            await callback.answer()
        except Exception:
            pass


@router.callback_query(F.data.startswith("prac_start_"))
async def cb_start_practice_section(callback: CallbackQuery):
    """Shortcut: starts practice in a specific section and sets filter."""
    try:
        user_id = callback.from_user.id
        section = callback.data.replace("prac_start_", "").strip()
        set_user_filter(user_id, "section", section)
        
        filters = get_user_filters(user_id)
        diff = filters.get("difficulty", "all")
        dom = filters.get("domain", "all")

        answered_ids = db.get_answered_question_ids(user_id)
        q_data = qs.get_next_filtered_question(answered_ids, section=section, domain=dom, difficulty=diff)
        
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
    """Loads next question adhering to active user filters."""
    try:
        user_id = callback.from_user.id
        raw_sec = callback.data.replace("prac_next_", "").strip()
        
        filters = get_user_filters(user_id)
        sec = raw_sec if raw_sec not in ("active", "") else filters.get("section", "mixed")
        diff = filters.get("difficulty", "all")
        dom = filters.get("domain", "all")

        answered_ids = db.get_answered_question_ids(user_id)
        q_data = qs.get_next_filtered_question(answered_ids, section=sec, domain=dom, difficulty=diff)
        
        db.local_cache.setdefault("practice_sessions", {})
        db.local_cache["practice_sessions"][str(user_id)] = {
            "question_id": q_data["id"],
            "section": sec,
            "q_data": q_data
        }
        db._save_local_db()

        await render_question_view(callback, q_data, sec)
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
        
        if not is_correct:
            try:
                await db.record_mistake(
                    user_id=user_id,
                    question_id=str(q_data.get("id", "")),
                    section=str(q_data.get("section", "math")),
                    domain=str(q_data.get("domain", "General")),
                    question_text=str(q_data.get("question", "")),
                    correct_answer=correct_key,
                    user_answer=selected_key,
                    explanation=str(q_data.get("explanation", "")),
                    hack=str(q_data.get("strategy_or_hack", "")),
                    options=q_data.get("options", []),
                    passage=q_data.get("passage"),
                    source="practice"
                )
            except Exception as rec_err:
                logger.warning(f"Failed to record practice mistake: {rec_err}")
        else:
            try:
                await db.resolve_mistake(user_id, str(q_data.get("id", "")))
            except Exception:
                pass

        stats = db.get_user_practice_stats(user_id)
        streak = stats.get("current_streak", 0)
        
        if is_correct:
            status_badge = f"🎉 <b>BARAKALLA, TO'G'RI JAVOB! (+1 ball)</b>\\n🔥 Hozirgi ketma-ketlik: <b>{streak} ta</b>"
        else:
            status_badge = f"❌ <b>NOTO'G'RI JAVOB!</b>\\nSiz tanladingiz: <b>{selected_key}</b> | To'g'ri javob: <b>{correct_key}</b>"

        explanation = html.escape(str(q_data.get("explanation", "Tushuntirish mavjud emas.")))
        
        text = (
            f"{status_badge}\\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\\n"
            f"💡 <b>Tushuntirish (Explanation):</b>\\n"
            f"{explanation}\\n\\n"
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

        hack_text = html.escape(str(q_data.get("strategy_or_hack", "Ushbu savol uchun hiyla qo'shilmagan.")))
        q_sec = q_data.get("section", "math").lower()
        title = "⚡ <b>DESMOS CHEATCODE & HACK</b>" if q_sec == "math" else "🎯 <b>DIGITAL SAT STRATEGIYASI & QOIDASI</b>"

        text = (
            f"{title}\\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\\n"
            f"{hack_text}\\n\\n"
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
