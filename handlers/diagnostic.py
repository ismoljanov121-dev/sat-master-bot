"""
SAT AI Bot - Diagnostic Quiz Handler
Interactive 5-question high-yield Digital SAT Math diagnostic.
"""

import json
import os
from typing import Dict, List
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from handlers.score_surgery import generate_surgery_report

router = Router()

# Load questions
QUESTIONS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "questions.json")
with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
    QUESTIONS: List[Dict] = json.load(f)

# In-memory user quiz sessions
# {user_id: {"current_idx": 0, "correct": 0, "incorrect_items": []}}
USER_SESSIONS: Dict[int, Dict] = {}

def get_question_keyboard(q_idx: int) -> InlineKeyboardMarkup:
    """Builds inline keyboard with options A, B, C, D."""
    q = QUESTIONS[q_idx]
    buttons = []
    row = []
    for opt in q["options"]:
        btn = InlineKeyboardButton(
            text=f"{opt['key']}) {opt['text']}",
            callback_data=f"ans_{q_idx}_{opt['key']}"
        )
        row.append(btn)
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_after_answer_keyboard(q_idx: int, is_last: bool) -> InlineKeyboardMarkup:
    """Builds navigation and Desmos hack buttons after answering."""
    buttons = [
        [InlineKeyboardButton(text="⚡ Desmos Hack (10s yechim)", callback_data=f"hack_{q_idx}")],
    ]
    if not is_last:
        buttons.append([InlineKeyboardButton(text="Keyingi savol ➡️", callback_data=f"next_{q_idx + 1}")])
    else:
        buttons.append([InlineKeyboardButton(text="🔬 Rentgen Xulosasini Olish ➡️", callback_data="finish_quiz")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@router.callback_query(F.data == "start_diagnostic")
async def start_quiz(callback: CallbackQuery):
    user_id = callback.from_user.id
    USER_SESSIONS[user_id] = {
        "current_idx": 0,
        "correct": 0,
        "incorrect_items": []
    }
    await send_question(callback, q_idx=0)

async def send_question(callback: CallbackQuery, q_idx: int):
    q = QUESTIONS[q_idx]
    total = len(QUESTIONS)
    text = (
        f"📝 <b>SAVOL {q_idx + 1} / {total}</b>\n"
        f"🏷️ <i>Mavzu: {q['topic']}</i>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"<b>{q['question']}</b>\n\n"
        f"<i>To'g'ri javob variantini tanlang:</i>"
    )
    kb = get_question_keyboard(q_idx)
    if callback.message:
        await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data.startswith("ans_"))
async def handle_answer(callback: CallbackQuery):
    user_id = callback.from_user.id
    parts = callback.data.split("_")
    q_idx = int(parts[1])
    selected_key = parts[2]

    session = USER_SESSIONS.get(user_id, {"current_idx": q_idx, "correct": 0, "incorrect_items": []})
    q = QUESTIONS[q_idx]
    is_correct = (selected_key == q["correct"])
    is_last = (q_idx == len(QUESTIONS) - 1)

    if is_correct:
        session["correct"] += 1
        res_header = "✅ <b>BARAKALLA! JAVOB TO'G'RI!</b>\n"
    else:
        session["incorrect_items"].append(q)
        res_header = f"❌ <b>XATO! To'g'ri javob: {q['correct']}</b>\n"

    USER_SESSIONS[user_id] = session

    res_body = (
        f"{res_header}"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ <b>Tuzoq tahlili:</b> {q['trap']}\n\n"
        f"📖 <b>Klassik yechim:</b> {q['explanation']}"
    )

    kb = get_after_answer_keyboard(q_idx, is_last)
    await callback.message.edit_text(res_body, reply_markup=kb, parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data.startswith("hack_"))
async def show_desmos_hack(callback: CallbackQuery):
    q_idx = int(callback.data.split("_")[1])
    q = QUESTIONS[q_idx]
    is_last = (q_idx == len(QUESTIONS) - 1)

    hack_text = (
        f"🚀 <b>DESMOS CHEATCODE & HACK</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{q['desmos_hack']}\n\n"
        f"💡 <i>Ushbu usul bilan formulalarni eslash shart emas!</i>"
    )
    kb_buttons = []
    if not is_last:
        kb_buttons.append([InlineKeyboardButton(text="Keyingi savol ➡️", callback_data=f"next_{q_idx + 1}")])
    else:
        kb_buttons.append([InlineKeyboardButton(text="🔬 Rentgen Xulosasini Olish ➡️", callback_data="finish_quiz")])

    await callback.message.edit_text(hack_text, reply_markup=InlineKeyboardMarkup(inline_keyboard=kb_buttons), parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data.startswith("next_"))
async def next_question(callback: CallbackQuery):
    q_idx = int(callback.data.split("_")[1])
    await send_question(callback, q_idx)

@router.callback_query(F.data == "finish_quiz")
async def finish_quiz(callback: CallbackQuery):
    user_id = callback.from_user.id
    session = USER_SESSIONS.get(user_id, {"correct": 0, "incorrect_items": []})
    user_name = callback.from_user.full_name or "Abituriyent"

    # Calculate score & points lost
    points_lost = sum(item.get("points_lost", 20) for item in session["incorrect_items"])
    estimated_score = max(800 - points_lost, 400)
    weaknesses = [item.get("topic", "General") for item in session["incorrect_items"]]

    # Save to Database (MongoDB Atlas + Local)
    try:
        from database import db
        await db.save_quiz_result(
            user_id=user_id,
            score=estimated_score,
            correct=session["correct"],
            total=len(QUESTIONS),
            weaknesses=weaknesses
        )
    except Exception as e:
        pass

    report = generate_surgery_report(
        user_name=user_name,
        total_q=len(QUESTIONS),
        correct_q=session["correct"],
        incorrect_items=session["incorrect_items"]
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Testni Qayta Topshirish", callback_data="start_diagnostic")],
        [
            InlineKeyboardButton(text="👥 Do'stlarni Taklif Qilish (VIP)", callback_data="referral_menu"),
            InlineKeyboardButton(text="📊 Mening Natijam", callback_data="my_stats")
        ],
        [InlineKeyboardButton(text="📱 60 Kunlik SAT Tracker (Web App)", url="https://sat-master-bot.onrender.com/webapp")]
    ])

    await callback.message.edit_text(report, reply_markup=kb, parse_mode="HTML")
    await callback.answer()
