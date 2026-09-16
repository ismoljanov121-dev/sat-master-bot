"""
EduTest Pro - Mock Exam Flow Handler
Manages student mock test journey, session code entry, short callbacks (<64 bytes),
timeout enforcement, and comprehensive score reporting.
"""

import html
import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import BRAND_NAME, CENTER_NAME
from database import db, utc_to_tashkent_str
from services.exam_service import (
    check_template_pool_sufficiency,
    exam_engine,
)

logger = logging.getLogger("ExamHandler")

router = Router()

TASHKENT_TZ = timezone(timedelta(hours=5))


# --- Keyboards ---
def get_exam_hub_keyboard() -> InlineKeyboardMarkup:
    """Navigation hub for exam options."""
    buttons = [
        [
            InlineKeyboardButton(
                text="⏱️ Bugungi 10 daqiqalik mashq (6 savol)",
                callback_data="ex_start:daily_10m"
            )
        ],
        [
            InlineKeyboardButton(
                text="⚡ Digital SAT Pilot Mock (18 savol / 25 daq)",
                callback_data="ex_start:pilot_mock"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔬 Mini Mock (12 savol / 15 daqiqa)",
                callback_data="ex_start:demo_mock"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Xatolarim Daftari",
                callback_data="notebook_menu"
            ),
            InlineKeyboardButton(
                text="📊 Mening Natijalarim",
                callback_data="ex_my_results"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Bosh Menyu",
                callback_data="back_to_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_exam_question_keyboard(
    attempt: dict[str, Any],
    q_idx: int,
    selected_key: str | None = None
) -> InlineKeyboardMarkup:
    """
    Builds compact inline keyboard for exam questions.
    Callback format strictly below 64 bytes and bound to attempt nonce and question index:
    - Option: ex:a:<nonce>:<idx>:<opt_key> (e.g., ex:a:a1b2c3:0:A)
    - Nav: ex:n:<nonce>:<idx> (e.g., ex:n:a1b2c3:2)
    - Finish: ex:f:<nonce> (e.g., ex:f:a1b2c3)
    """
    questions = attempt.get("questions", [])
    total = len(questions)
    target_q = questions[q_idx]
    nonce = attempt.get("nonce", attempt.get("attempt_id", "")[:6])

    answers = attempt.get("answers", {})
    recorded_ans = answers.get(str(q_idx), {}).get("selected") if str(q_idx) in answers else None
    active_selection = selected_key or recorded_ans

    buttons = []
    # Options A, B and C, D
    row1 = []
    row2 = []
    for opt in target_q.get("options", []):
        opt_key = opt["key"]
        prefix = "🔘" if active_selection == opt_key else "⚪"
        btn_text = f"{prefix} {opt_key}"
        btn = InlineKeyboardButton(text=btn_text, callback_data=f"ex:a:{nonce}:{q_idx}:{opt_key}")
        if opt_key in ("A", "B"):
            row1.append(btn)
        else:
            row2.append(btn)

    if row1:
        buttons.append(row1)
    if row2:
        buttons.append(row2)

    # Navigation row
    nav_row = []
    if q_idx > 0:
        nav_row.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"ex:n:{nonce}:{q_idx - 1}"))

    if q_idx + 1 < total:
        nav_row.append(InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"ex:n:{nonce}:{q_idx + 1}"))
    else:
        nav_row.append(InlineKeyboardButton(text="🏁 Tugatish", callback_data=f"ex:f:{nonce}"))

    if nav_row:
        buttons.append(nav_row)

    # Quick exit / abort button
    buttons.append([
        InlineKeyboardButton(text="⏹ Imtihonni topshirish", callback_data=f"ex:f:{nonce}")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def format_exam_question_text(attempt: dict[str, Any], q_idx: int) -> str:
    """Formats question display with time remaining and section details."""
    questions = attempt.get("questions", [])
    total = len(questions)
    target_q = questions[q_idx]

    # Calculate remaining time
    deadline_iso = attempt.get("deadline")
    rem_min_str = "Noma'lum"
    if deadline_iso:
        try:
            deadline = datetime.fromisoformat(deadline_iso)
            if deadline.tzinfo is None:
                deadline = deadline.replace(tzinfo=timezone.utc)
            now_utc = datetime.now(timezone.utc)
            rem_sec = max(0, int((deadline - now_utc).total_seconds()))
            rem_min = rem_sec // 60
            rem_s = rem_sec % 60
            rem_min_str = f"{rem_min:02d}:{rem_s:02d}"
        except Exception:
            pass

    sec = target_q.get("section", "math").upper()
    domain = html.escape(str(target_q.get("domain", "General")))
    difficulty = html.escape(str(target_q.get("difficulty", "Medium")))
    q_text = html.escape(str(target_q.get("question", "")))
    passage = target_q.get("passage")

    lines = [
        f"📝 <b>{attempt.get('title', 'MOCK TEST')}</b>",
        f"⏳ <b>Qolgan vaqt:</b> <code>{rem_min_str}</code> | <b>Savol:</b> {q_idx + 1}/{total}",
        f"📂 <b>Bo'lim:</b> {sec} | <b>Mavzu:</b> {domain}",
        "━━━━━━━━━━━━━━━━━━━━━━\n"
    ]

    if passage:
        lines.append(f"📄 <b>Matn:</b>\n<i>{html.escape(str(passage))}</i>\n")

    lines.append(f"<b>{q_text}</b>\n")
    lines.append("👇 <b>Variantlar:</b>")

    for opt in target_q.get("options", []):
        opt_key = html.escape(str(opt["key"]))
        opt_text = html.escape(str(opt["text"]))
        lines.append(f"<b>{opt_key})</b> {opt_text}")

    return "\n".join(lines)


def format_exam_result_report(attempt: dict[str, Any]) -> str:
    """Renders comprehensive performance analytics without misleading College Board score claims."""
    score = attempt.get("score") or {}
    total = score.get("total_questions", 0)
    correct = score.get("correct_count", 0)
    acc = score.get("accuracy_percentage", 0)
    by_sec = score.get("by_section", {})
    weaknesses = score.get("weaknesses", [])
    avg_sec = score.get("avg_seconds_per_question", 0)
    total_time_sec = score.get("total_time_seconds", 0)

    m_c = by_sec.get("math", {}).get("correct", 0)
    m_t = by_sec.get("math", {}).get("total", 0)
    r_c = by_sec.get("reading", {}).get("correct", 0)
    r_t = by_sec.get("reading", {}).get("total", 0)
    w_c = by_sec.get("writing", {}).get("correct", 0)
    w_t = by_sec.get("writing", {}).get("total", 0)

    # Visual gauge
    filled = acc // 10
    gauge = "🟩" * filled + "⬜" * (10 - filled)

    time_str = f"{total_time_sec // 60} daq {total_time_sec % 60} soniya" if total_time_sec >= 60 else f"{total_time_sec} soniya"

    lines = [
        f"🏆 <b>MOCK IMTIHON NATIJASI — {BRAND_NAME}</b>",
        "━━━━━━━━━━━━━━━━━━━━━━",
        f"📋 <b>Test turi:</b> {html.escape(str(attempt.get('title', 'Mock')))}",
        f"🎯 <b>Umumiy aniqlik:</b> {acc}% ({correct}/{total} ta to'g'ri)",
        f"<i>{gauge}</i>\n",
        "⏱️ <b>Vaqt sarfi & Tezlik (Pacing):</b>",
        f"• <b>Jami sarflangan vaqt:</b> {time_str}",
        f"• <b>O'rtacha tezlik:</b> ~{avg_sec} soniya / savol\n",
        "📊 <b>Bo'limlar kesimida tahlil:</b>",
        f"• 🧮 <b>Math:</b> {m_c}/{m_t} ta to'g'ri",
        f"• 📖 <b>Reading:</b> {r_c}/{r_t} ta to'g'ri",
        f"• ✍️ <b>Writing & Grammar:</b> {w_c}/{w_t} ta to'g'ri",
        ""
    ]

    if weaknesses:
        lines.append("⚠️ <b>E'tibor qaratish kerak bo'lgan mavzular:</b>")
        for w in weaknesses:
            lines.append(f"• <i>{html.escape(str(w.get('domain')))}</i> ({w.get('errors')} ta xato)")
        lines.append("")

    lines.append(
        "💡 <i>Eslatma: Ushbu mustaqil pilot mock Digital SAT Bluebook formatidan ilhomlangan. "
        "Xato qilingan barcha savollar avtomatik ravishda 'Xatolarim daftari'ga saqlandi.</i>"
    )

    return "\n".join(lines)


async def _sync_exam_mistakes_to_notebook(user_id: int, attempt: dict[str, Any]) -> None:
    """Extracts incorrect or skipped answers from attempt and registers them in error notebook."""
    questions = attempt.get("questions", [])
    answers = attempt.get("answers", {})
    for idx, q in enumerate(questions):
        ans_entry = answers.get(str(idx))
        if not ans_entry or not ans_entry.get("is_correct"):
            try:
                await db.record_mistake(
                    user_id=user_id,
                    question_id=str(q.get("id", f"exam_{attempt.get('attempt_id')}_{idx}")),
                    section=str(q.get("section", "math")),
                    domain=str(q.get("domain", "General")),
                    question_text=str(q.get("question", "")),
                    correct_answer=str(q.get("correct", "A")),
                    user_answer=str(ans_entry.get("selected", "-") if ans_entry else "Javob berilmadi"),
                    explanation=str(q.get("explanation", "")),
                    hack=str(q.get("strategy_or_hack", "")),
                    options=q.get("options", []),
                    passage=q.get("passage"),
                    source=f"exam:{attempt.get('template_name', 'mock')}"
                )
            except Exception as err:
                logger.warning(f"Error recording exam mistake: {err}")


# --- Handlers ---
@router.message(Command("mock"))
async def cmd_mock(message: Message, command: CommandObject | None = None):
    """Entry point for mock exam command. Supports session code argument: /mock MARS26."""
    user_id = message.from_user.id
    code_arg = (command.args or "").strip().upper() if command else ""

    if code_arg:
        # Check active session matching code
        session = db.get_active_session_by_code(code_arg)
        if not session:
            await message.answer(
                f"❌ <b>'{code_arg}' kodi bo'yicha faol imtihon sessiyasi topilmadi.</b>\n"
                "Iltimos, kodni tekshiring yoki administratorga murojaat qiling.",
                parse_mode="HTML"
            )
            return

        # Start attempt for this specific session with session deadline enforcement
        attempt_candidate = exam_engine.create_attempt(
            user_id=user_id,
            template_name=session.get("template_name", "demo_mock"),
            session_id=session.get("session_id"),
            session_deadline=session.get("deadline")
        )
        created, attempt, msg = await db.create_user_attempt_atomic(user_id, attempt_candidate)
        if not created and attempt:
            att_nonce = attempt.get("nonce", "")
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="▶️ Imtihonni davom ettirish", callback_data="ex:resume")],
                [InlineKeyboardButton(text="🏁 Imtihonni topshirish", callback_data=f"ex:f:{att_nonce}")]
            ])
            await message.answer(
                "⚠️ <b>Sizda tugallanmagan faol mock imtihon mavjud!</b>\n"
                "Iltimos, avvalgi imtihonni yakunlang yoki davom ettiring:",
                reply_markup=kb,
                parse_mode="HTML"
            )
            return

        text = format_exam_question_text(attempt, 0)
        kb = get_exam_question_keyboard(attempt, 0)
        await message.answer(
            f"🎉 <b>'{session.get('title')}' imtihoniga xush kelibsiz!</b>\n\n" + text,
            reply_markup=kb,
            parse_mode="HTML"
        )
        return

    # Check if user already has an active attempt
    active_attempt = db.get_user_active_attempt(user_id)
    if active_attempt and not exam_engine.is_attempt_expired(active_attempt):
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="▶️ Imtihonni davom ettirish", callback_data="ex:resume")],
            [InlineKeyboardButton(text="🏁 Imtihonni topshirish", callback_data="ex:fin")]
        ])
        await message.answer(
            "⚠️ <b>Sizda tugallanmagan faol mock imtihon mavjud!</b>\n"
            "Belgilangan muddat ichida davom ettirishingiz mumkin:",
            reply_markup=kb,
            parse_mode="HTML"
        )
        return

    hub_text = (
        f"📝 <b>{BRAND_NAME} — MOCK IMTIHON MARKAZI</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Haqiqiy imtihon muhitini his qiling: server nazorati ostidagi vaqt chegarasi, "
        "tasodifiy savollar tartibi va batafsil tahlil.\n\n"
        "👇 <i>Kerakli imtihon formatini tanlang:</i>"
    )
    await message.answer(hub_text, reply_markup=get_exam_hub_keyboard(), parse_mode="HTML")


@router.callback_query(F.data == "exam_hub")
async def cb_exam_hub(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        active_attempt = db.get_user_active_attempt(user_id)
        if active_attempt and not exam_engine.is_attempt_expired(active_attempt):
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="▶️ Imtihonni davom ettirish", callback_data="ex:resume")],
                [InlineKeyboardButton(text="🏁 Imtihonni topshirish", callback_data="ex:fin")]
            ])
            await callback.message.edit_text(
                "⚠️ <b>Sizda tugallanmagan faol mock imtihon mavjud!</b>\n"
                "Iltimos, avvalgi imtihonni yakunlang:",
                reply_markup=kb,
                parse_mode="HTML"
            )
            return

        hub_text = (
            f"📝 <b>{BRAND_NAME} — MOCK IMTIHON MARKAZI</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "Haqiqiy imtihon muhitini his qiling: server nazorati ostidagi vaqt chegarasi, "
            "tasodifiy savollar tartibi va batafsil tahlil.\n\n"
            "👇 <i>Kerakli imtihon formatini tanlang:</i>"
        )
        await callback.message.edit_text(hub_text, reply_markup=get_exam_hub_keyboard(), parse_mode="HTML")
    finally:
        try:
            await callback.answer()
        except Exception:
            pass


@router.callback_query(F.data.startswith("ex_start:"))
async def cb_start_template(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        template_name = callback.data.replace("ex_start:", "").strip()

        # Check sufficiency first
        is_suff, suff_msg, _ = check_template_pool_sufficiency(template_name)
        if not is_suff:
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⚡ Demo Mock (12 savol) ga o'tish", callback_data="ex_start:demo_mock")],
                [InlineKeyboardButton(text="⬅️ Ortga", callback_data="exam_hub")]
            ])
            await callback.message.edit_text(suff_msg, reply_markup=kb, parse_mode="HTML")
            return

        # Create authoritative attempt atomically
        attempt_candidate = exam_engine.create_attempt(user_id=user_id, template_name=template_name)
        created, attempt, msg = await db.create_user_attempt_atomic(user_id, attempt_candidate)
        if not created and attempt:
            att_nonce = attempt.get("nonce", "")
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="▶️ Imtihonni davom ettirish", callback_data="ex:resume")],
                [InlineKeyboardButton(text="🏁 Imtihonni topshirish", callback_data=f"ex:f:{att_nonce}")]
            ])
            await callback.message.edit_text(
                "⚠️ <b>Sizda allaqachon tugallanmagan faol mock imtihon mavjud!</b>",
                reply_markup=kb,
                parse_mode="HTML"
            )
            return

        text = format_exam_question_text(attempt, 0)
        kb = get_exam_question_keyboard(attempt, 0)
        await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Error in cb_start_template: {e}")
        try:
            await callback.message.edit_text("❌ Imtihonni boshlashda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")
        except Exception:
            pass
    finally:
        try:
            await callback.answer()
        except Exception:
            pass


@router.callback_query(F.data == "ex:resume")
async def cb_resume_exam(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        active_attempt = db.get_user_active_attempt(user_id)
        if not active_attempt or exam_engine.is_attempt_expired(active_attempt):
            await callback.message.edit_text(
                "❌ Faol imtihon topilmadi yoki vaqti tugagan.",
                reply_markup=get_exam_hub_keyboard()
            )
            return

        idx = active_attempt.get("current_idx", 0)
        text = format_exam_question_text(active_attempt, idx)
        kb = get_exam_question_keyboard(active_attempt, idx)
        await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    finally:
        try:
            await callback.answer()
        except Exception:
            pass


@router.callback_query(F.data.startswith("ex:a:"))
async def cb_select_answer(callback: CallbackQuery):
    """Handles answer option selection: ex:a:<nonce>:<idx>:<opt_key> (or ex:a:<opt_key>)."""
    try:
        user_id = callback.from_user.id
        parts = callback.data.split(":")
        if len(parts) >= 5:
            expected_nonce = parts[2]
            q_idx = int(parts[3])
            selected_key = parts[4].strip().upper()
        else:
            expected_nonce = None
            q_idx = None
            selected_key = parts[2].strip().upper()

        active_attempt = db.get_user_active_attempt(user_id)
        answered = False
        if not active_attempt:
            await callback.answer("Imtihon sessiyasi topilmadi yoki yakunlangan.", show_alert=True)
            answered = True
            return

        if expected_nonce and active_attempt.get("nonce") != expected_nonce:
            await callback.answer("⛔ Ushbu savol eski yoki boshqa imtihon sessiyasiga tegishli.", show_alert=True)
            answered = True
            return

        target_idx = q_idx if q_idx is not None else active_attempt.get("current_idx", 0)
        status, updated_attempt = exam_engine.submit_answer(
            active_attempt, target_idx, selected_key, expected_nonce=expected_nonce
        )
        await db.save_attempt(updated_attempt)

        if status == "invalid_nonce":
            await callback.answer("⛔ Sessiya eskirgan.", show_alert=True)
            answered = True
            return

        if status == "expired":
            await _sync_exam_mistakes_to_notebook(user_id, updated_attempt)
            report_text = format_exam_result_report(updated_attempt)
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="❌ Xatolarim Daftari", callback_data="notebook_menu"),
                    InlineKeyboardButton(text="📊 Natijalarim", callback_data="ex_my_results")
                ],
                [InlineKeyboardButton(text="⬅️ Bosh Menyu", callback_data="back_to_menu")]
            ])
            await callback.message.edit_text(
                "⏰ <b>Imtihon vaqti tugadi!</b> Natijangiz hisoblandi:\n\n" + report_text,
                reply_markup=kb,
                parse_mode="HTML"
            )
            return

        # If completed all questions
        if updated_attempt.get("status") == "submitted":
            await _sync_exam_mistakes_to_notebook(user_id, updated_attempt)
            report_text = format_exam_result_report(updated_attempt)
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="❌ Xatolarim Daftari", callback_data="notebook_menu"),
                    InlineKeyboardButton(text="📊 Natijalarim", callback_data="ex_my_results")
                ],
                [InlineKeyboardButton(text="⬅️ Bosh Menyu", callback_data="back_to_menu")]
            ])
            await callback.message.edit_text(
                "🎉 <b>Imtihon muvaffaqiyatli yakunlandi!</b>\n\n" + report_text,
                reply_markup=kb,
                parse_mode="HTML"
            )
            return

        if status == "already_answered":
            await callback.answer("ℹ️ Ushbu savolga allaqachon javob berilgan.")
            answered = True
        elif status == "invalid_index":
            await callback.answer("ℹ️ Savol tartibi mos kelmadi.")
            answered = True

        # Render next/current question
        next_idx = updated_attempt.get("current_idx", target_idx)
        text = format_exam_question_text(updated_attempt, next_idx)
        kb = get_exam_question_keyboard(updated_attempt, next_idx)
        try:
            await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
        except TelegramBadRequest as e:
            if "message is not modified" not in str(e).lower():
                raise
    except Exception as e:
        logger.error(f"Error in cb_select_answer: {e}")
    finally:
        if not answered:
            try:
                await callback.answer()
            except Exception:
                pass


@router.callback_query(F.data.startswith("ex:n:"))
async def cb_navigate_question(callback: CallbackQuery):
    """Handles question navigation: ex:n:<nonce>:<idx> (or ex:n:<idx>)."""
    try:
        user_id = callback.from_user.id
        parts = callback.data.split(":")
        if len(parts) >= 4:
            nonce = parts[2]
            target_idx = int(parts[3])
        else:
            nonce = None
            target_idx = int(parts[2])

        active_attempt = db.get_user_active_attempt(user_id)
        if not active_attempt:
            await callback.answer("Imtihon sessiyasi topilmadi.", show_alert=True)
            return

        if nonce and active_attempt.get("nonce") != nonce:
            await callback.answer("⛔ Sessiya eskirgan.", show_alert=True)
            return

        if exam_engine.is_attempt_expired(active_attempt):
            active_attempt["status"] = "expired"
            exam_engine.finalize_score(active_attempt)
            await db.save_attempt(active_attempt)
            await _sync_exam_mistakes_to_notebook(user_id, active_attempt)
            report_text = format_exam_result_report(active_attempt)
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="❌ Xatolarim Daftari", callback_data="notebook_menu"),
                    InlineKeyboardButton(text="📊 Natijalarim", callback_data="ex_my_results")
                ],
                [InlineKeyboardButton(text="⬅️ Bosh Menyu", callback_data="back_to_menu")]
            ])
            await callback.message.edit_text(
                "⏰ <b>Imtihon vaqti tugadi!</b>\n\n" + report_text,
                reply_markup=kb,
                parse_mode="HTML"
            )
            return

        active_attempt["current_idx"] = target_idx
        await db.save_attempt(active_attempt)

        text = format_exam_question_text(active_attempt, target_idx)
        kb = get_exam_question_keyboard(active_attempt, target_idx)
        await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Error in cb_navigate_question: {e}")
    finally:
        try:
            await callback.answer()
        except Exception:
            pass


@router.callback_query(F.data.startswith("ex:f:") | (F.data == "ex:fin"))
async def cb_finish_exam_early(callback: CallbackQuery):
    """Manually finishes the exam attempt: ex:f:<nonce> or ex:fin."""
    try:
        user_id = callback.from_user.id
        active_attempt = db.get_user_active_attempt(user_id)
        if not active_attempt:
            await callback.answer("Faol imtihon topilmadi.", show_alert=True)
            return

        if callback.data.startswith("ex:f:"):
            nonce = callback.data.replace("ex:f:", "").strip()
            if active_attempt.get("nonce") != nonce:
                await callback.answer("⛔ Sessiya eskirgan.", show_alert=True)
                return

        active_attempt["status"] = "submitted"
        exam_engine.finalize_score(active_attempt)
        await db.save_attempt(active_attempt)
        await _sync_exam_mistakes_to_notebook(user_id, active_attempt)

        report_text = format_exam_result_report(active_attempt)
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="❌ Xatolarim Daftari", callback_data="notebook_menu"),
                InlineKeyboardButton(text="📊 Natijalarim", callback_data="ex_my_results")
            ],
            [InlineKeyboardButton(text="⬅️ Bosh Menyu", callback_data="back_to_menu")]
        ])
        await callback.message.edit_text(
            "🏁 <b>Imtihon yakunlandi va natijangiz qayd etildi!</b>\n\n" + report_text,
            reply_markup=kb,
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Error in cb_finish_exam_early: {e}")
    finally:
        try:
            await callback.answer()
        except Exception:
            pass


@router.callback_query(F.data == "ex_my_results")
async def cb_view_my_results(callback: CallbackQuery):
    """Displays student's historical mock results."""
    try:
        user_id = callback.from_user.id
        attempts = db.list_user_attempts(user_id)
        completed = [a for a in attempts if a.get("status") in ("submitted", "expired")]

        if not completed:
            text = (
                "📊 <b>Mening Mock Natijalarim</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "Siz hali EduTest Pro formatida mock imtihon topshirmadingiz.\n\n"
                "<i>Birinchi mock testni boshlash uchun quyidagi tugmani bosing:</i>"
            )
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⚡ Demo Mock (12 savol)", callback_data="ex_start:demo_mock")],
                [InlineKeyboardButton(text="⬅️ Ortga", callback_data="exam_hub")]
            ])
            await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
            return

        lines = [
            "📊 <b>Mening Mock Natijalarim</b>",
            "━━━━━━━━━━━━━━━━━━━━━━\n"
        ]
        for idx, att in enumerate(completed[:5], 1):
            score = att.get("score") or {}
            acc = score.get("accuracy_percentage", 0)
            corr = score.get("correct_count", 0)
            tot = score.get("total_questions", 0)
            date_str = utc_to_tashkent_str(att.get("start_time"))
            title = att.get("title", "Mock")
            lines.append(f"<b>{idx}. {title}</b> — {date_str}")
            lines.append(f"   🎯 Aniqlik: <b>{acc}%</b> ({corr}/{tot} ta to'g'ri)\n")

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⚡ Yangi Demo Mock", callback_data="ex_start:demo_mock")],
            [InlineKeyboardButton(text="⬅️ Ortga", callback_data="exam_hub")]
        ])
        await callback.message.edit_text("\n".join(lines), reply_markup=kb, parse_mode="HTML")
    finally:
        try:
            await callback.answer()
        except Exception:
            pass
