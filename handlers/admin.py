"""
EduTest Pro - Administrator Panel Handler
Features:
- Strict authorization: every command and callback verifies is_admin(user_id)
- Real-time center dashboard statistics
- Live mock session creation with 6-char join codes and close controls
- Recent results drilldown with student weaknesses
- 1-click CSV export directly uploaded to Telegram chat
- Secure backup triggers
"""

import html
import logging
import uuid
from datetime import datetime, timedelta, timezone

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (
    BufferedInputFile,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import BRAND_NAME, CENTER_NAME, is_admin
from database import TASHKENT_TZ, db, get_tashkent_now_str, utc_to_tashkent_str
from services.backup_service import perform_backup
from services.exam_service import (
    EXAM_TEMPLATES,
    check_template_pool_sufficiency,
    exam_engine,
)

logger = logging.getLogger("AdminHandler")

router = Router()


# --- Admin Keyboards ---
def get_admin_main_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="🎯 Yangi Mock Sessiya Ochish", callback_data="adm:new_session")
        ],
        [
            InlineKeyboardButton(text="📋 Faol Sessiyalar", callback_data="adm:active_sessions"),
            InlineKeyboardButton(text="👥 So'nggi Natijalar", callback_data="adm:results")
        ],
        [
            InlineKeyboardButton(text="📥 Natijalarni CSV Yuklab Olish", callback_data="adm:export_csv")
        ],
        [
            InlineKeyboardButton(text="💾 Tizim Zaxirasi (Backup)", callback_data="adm:backup"),
            InlineKeyboardButton(text="🔄 Yangilash", callback_data="adm:refresh")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def format_admin_dashboard_text() -> str:
    """Renders real-time statistics dashboard for the administrator."""
    stats = db.get_admin_dashboard_stats()
    now_tashkent = get_tashkent_now_str()

    lines = [
        f"👑 <b>{BRAND_NAME} — ADMINISTRATOR PANELI</b>",
        f"🏛️ <b>Markaz:</b> {CENTER_NAME}",
        f"📅 <b>Vaqt:</b> {now_tashkent} (Toshkent)",
        "━━━━━━━━━━━━━━━━━━━━━━\n",
        "📈 <b>REAL-TIME STATISTIKA:</b>",
        f"• 👥 Jami o'quvchilar: <b>{stats['total_students']} nafar</b>",
        f"• ⚡ Bugun faol o'quvchilar: <b>{stats['active_today']} nafar</b>",
        f"• 📝 Yakunlangan mocklar: <b>{stats['completed_exams']} ta</b>",
        f"• 🎯 O'rtacha aniqlik ko'rsatkichi: <b>{stats['average_accuracy']}%</b>",
        f"• 🟢 Faol imtihon sessiyalari: <b>{stats['active_sessions_count']} ta</b>\n",
        "👇 <i>Kerakli boshqaruv bo'limini tanlang:</i>"
    ]
    return "\n".join(lines)


# --- Authorization Filter Helper ---
async def check_admin_access(event: Message | CallbackQuery) -> bool:
    """Verifies that the user is an authorized administrator."""
    user_id = event.from_user.id
    if not is_admin(user_id):
        logger.warning(f"Unauthorized admin access attempt by user_id: {user_id}")
        if isinstance(event, CallbackQuery):
            await event.answer("⛔ Ushbu bo'lim faqat administratorlar uchun mo'ljallangan.", show_alert=True)
        else:
            await event.answer(
                "⛔ <b>Kirish taqiqlandi!</b>\n"
                "Ushbu buyruq faqat o'quv markaz administratorlari uchun mo'ljallangan.",
                parse_mode="HTML"
            )
        return False
    return True


# --- Handlers ---
@router.message(Command("admin"))
async def cmd_admin(message: Message):
    """Entry point for /admin dashboard."""
    if not await check_admin_access(message):
        return

    text = format_admin_dashboard_text()
    await message.answer(text, reply_markup=get_admin_main_keyboard(), parse_mode="HTML")


@router.callback_query(F.data == "adm:refresh")
async def cb_admin_refresh(callback: CallbackQuery):
    if not await check_admin_access(callback):
        return

    try:
        text = format_admin_dashboard_text()
        await callback.message.edit_text(text, reply_markup=get_admin_main_keyboard(), parse_mode="HTML")
    finally:
        try:
            await callback.answer("Statistika yangilandi!")
        except Exception:
            pass


@router.callback_query(F.data == "adm:new_session")
async def cb_admin_new_session_menu(callback: CallbackQuery):
    if not await check_admin_access(callback):
        return

    try:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⚡ Demo Mock (12 savol / 12 daqiqa)",
                    callback_data="adm:create_sess:demo_mock"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"🏛️ {CENTER_NAME} Full Mock (122 savol)",
                    callback_data="adm:create_sess:marstif_full"
                )
            ],
            [
                InlineKeyboardButton(text="⬅️ Boshqaruv Paneliga Qaytish", callback_data="adm:refresh")
            ]
        ])

        text = (
            "🎯 <b>YANGI MOCK SESSIYA OCHISH</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "O'quvchilar bir vaqtda guruh bo'lib kirishi uchun yangi sessiya yarating. "
            "Tizim avtomatik ravishda 6 xonali maxsus taklif kodini shakllantiradi.\n\n"
            "<i>Imtihon shablonini tanlang:</i>"
        )
        await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    finally:
        try:
            await callback.answer()
        except Exception:
            pass


@router.callback_query(F.data.startswith("adm:create_sess:"))
async def cb_admin_create_session(callback: CallbackQuery):
    if not await check_admin_access(callback):
        return

    try:
        template_name = callback.data.replace("adm:create_sess:", "").strip()
        template = EXAM_TEMPLATES.get(template_name)
        if not template:
            await callback.answer("Noma'lum imtihon shabloni.", show_alert=True)
            return

        # Check sufficiency
        is_suff, suff_msg, _ = check_template_pool_sufficiency(template_name)
        if not is_suff:
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⚡ Demo Mock yaratish", callback_data="adm:create_sess:demo_mock")],
                [InlineKeyboardButton(text="⬅️ Ortga", callback_data="adm:new_session")]
            ])
            await callback.message.edit_text(suff_msg, reply_markup=kb, parse_mode="HTML")
            return

        # Generate unique alphanumeric join code
        active_codes = {
            s.get("code", "").upper()
            for s in db.local_cache.get("exam_sessions", {}).values()
            if s.get("status") == "active"
        }
        code = exam_engine.generate_join_code(prefix="MARS", existing_codes=active_codes)
        session_id = f"sess_{uuid.uuid4().hex[:8]}"

        now_utc = datetime.now(timezone.utc)
        dur_sec = template["duration_seconds"]
        deadline_utc = now_utc + timedelta(seconds=dur_sec)

        session_data = {
            "session_id": session_id,
            "code": code,
            "template_name": template_name,
            "title": template["title"],
            "duration_seconds": dur_sec,
            "created_by": callback.from_user.id,
            "starts_at": now_utc.isoformat(),
            "deadline": deadline_utc.isoformat(),
            "created_at": now_utc.isoformat(),
            "status": "active"
        }
        await db.save_exam_session(session_data)

        dur_min = dur_sec // 60
        announce_text = (
            f"✅ <b>YANGI MOCK SESSIYA OCHILDI!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏷️ <b>Nomi:</b> {template['title']}\n"
            f"🔑 <b>Qo'shilish Kodi:</b> <code>{code}</code>\n"
            f"⏱ <b>Imtihon Vaqti:</b> {dur_min} daqiqa\n"
            f"🟢 <b>Holati:</b> Faol (O'quvchilarni qabul qilmoqda)\n\n"
            f"📢 <b>O'quvchilarga yuborish uchun matn:</b>\n"
            f"<i>Assalomu alaykum! {CENTER_NAME} mock imtihoniga kirish uchun botga "
            f"<code>/mock {code}</code> buyrug'ini yuboring!</i>"
        )

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⏹ Sessiyani Yopish", callback_data=f"adm:close_sess:{session_id}")],
            [InlineKeyboardButton(text="⬅️ Boshqaruv Paneliga Qaytish", callback_data="adm:refresh")]
        ])
        await callback.message.edit_text(announce_text, reply_markup=kb, parse_mode="HTML")
    finally:
        try:
            await callback.answer()
        except Exception:
            pass


@router.callback_query(F.data == "adm:active_sessions")
async def cb_admin_active_sessions(callback: CallbackQuery):
    if not await check_admin_access(callback):
        return

    try:
        sessions = db.list_exam_sessions(limit=10)
        active = [s for s in sessions if s.get("status") == "active"]

        if not active:
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🎯 Yangi Sessiya Ochish", callback_data="adm:new_session")],
                [InlineKeyboardButton(text="⬅️ Ortga", callback_data="adm:refresh")]
            ])
            await callback.message.edit_text(
                "ℹ️ <b>Hozirda faol imtihon sessiyalari mavjud emas.</b>\n"
                "O'quvchilar uchun yangi sessiya ochishingiz mumkin.",
                reply_markup=kb,
                parse_mode="HTML"
            )
            return

        lines = [
            "📋 <b>FAOL IMTIHON SESSIYALARI:</b>",
            "━━━━━━━━━━━━━━━━━━━━━━\n"
        ]
        buttons = []
        for s in active:
            code = s.get("code")
            title = s.get("title")
            sess_id = s.get("session_id")
            time_str = utc_to_tashkent_str(s.get("created_at"))
            lines.append(f"🟢 <b>Kod: {code}</b> | {title}\n   <i>Ochilgan: {time_str}</i>\n")
            buttons.append([
                InlineKeyboardButton(
                    text=f"📊 Natijalar: {code}",
                    callback_data=f"adm:sess_filter:{sess_id}"
                ),
                InlineKeyboardButton(
                    text=f"⏹ Yopish: {code}",
                    callback_data=f"adm:close_sess:{sess_id}"
                )
            ])

        buttons.append([InlineKeyboardButton(text="⬅️ Ortga", callback_data="adm:refresh")])
        kb = InlineKeyboardMarkup(inline_keyboard=buttons)
        await callback.message.edit_text("\n".join(lines), reply_markup=kb, parse_mode="HTML")
    finally:
        try:
            await callback.answer()
        except Exception:
            pass


@router.callback_query(F.data.startswith("adm:close_sess:"))
async def cb_admin_close_session(callback: CallbackQuery):
    if not await check_admin_access(callback):
        return

    try:
        session_id = callback.data.replace("adm:close_sess:", "").strip()
        success = await db.close_exam_session(session_id)
        if success:
            await callback.answer("Sessiya muvaffaqiyatli yopildi!", show_alert=True)
        else:
            await callback.answer("Sessiya topilmadi.", show_alert=True)

        text = format_admin_dashboard_text()
        await callback.message.edit_text(text, reply_markup=get_admin_main_keyboard(), parse_mode="HTML")
    finally:
        try:
            await callback.answer()
        except Exception:
            pass


@router.callback_query(F.data.startswith("adm:results") | F.data.startswith("adm:sess_filter:"))
async def cb_admin_recent_results(callback: CallbackQuery):
    if not await check_admin_access(callback):
        return

    try:
        is_sess_filter = callback.data.startswith("adm:sess_filter:")
        if is_sess_filter:
            sess_id = callback.data.replace("adm:sess_filter:", "").strip()
            results = db.get_session_results(sess_id)
            sess_obj = db.get_exam_session(sess_id)
            code_label = sess_obj.get("code", sess_id) if sess_obj else sess_id
            header = f"👥 <b>SESSIYA NATIJALARI (Kod: {code_label}):</b>"
        else:
            results = db.get_recent_exam_results(limit=10)
            header = "👥 <b>SO'NGGI MOCK NATIJALARI:</b>"

        if not results:
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Ortga", callback_data="adm:refresh")]
            ])
            await callback.message.edit_text(
                f"ℹ️ <b>Hozircha natijalar mavjud emas.</b>",
                reply_markup=kb,
                parse_mode="HTML"
            )
            return

        lines = [
            header,
            "━━━━━━━━━━━━━━━━━━━━━━\n"
        ]
        for idx, r in enumerate(results, 1):
            name = html.escape(str(r["student_name"]))
            acc = r["accuracy"]
            corr = r["correct_count"]
            tot = r["total_questions"]
            dt = r["date_tashkent"]
            sec = r.get("by_section") or {}
            m_stat = f"M: {sec.get('math', {}).get('correct', 0)}/{sec.get('math', {}).get('total', 0)}"
            r_stat = f"R: {sec.get('reading', {}).get('correct', 0)}/{sec.get('reading', {}).get('total', 0)}"
            w_stat = f"W: {sec.get('writing', {}).get('correct', 0)}/{sec.get('writing', {}).get('total', 0)}"
            weak = r.get("weaknesses") or []
            weak_domains = [w.get("domain", "") for w in weak[:2] if w.get("domain")]
            weak_text = f" | Zaif: {', '.join(weak_domains)}" if weak_domains else ""

            lines.append(
                f"<b>{idx}. {name}</b> — <b>{acc}%</b> ({corr}/{tot})\n"
                f"   <i>Taqsimot: {m_stat} | {r_stat} | {w_stat}{weak_text}</i>\n"
                f"   <i>Vaqt: {dt}</i>\n"
            )

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📥 Barcha Natijalarni CSV Eksport Qilish", callback_data="adm:export_csv")],
            [InlineKeyboardButton(text="⬅️ Ortga", callback_data="adm:refresh")]
        ])
        await callback.message.edit_text("\n".join(lines), reply_markup=kb, parse_mode="HTML")
    finally:
        try:
            await callback.answer()
        except Exception:
            pass


@router.callback_query(F.data == "adm:export_csv")
async def cb_admin_export_csv(callback: CallbackQuery):
    """Generates CSV and uploads it as a file to the administrator."""
    if not await check_admin_access(callback):
        return

    try:
        csv_content = db.export_results_csv()
        now_str = datetime.now(TASHKENT_TZ).strftime("%Y%m%d_%H%M")
        filename = f"edutest_pro_results_{now_str}.csv"

        csv_bytes = csv_content.encode("utf-8-sig")  # utf-8-sig opens cleanly in Excel
        doc_file = BufferedInputFile(csv_bytes, filename=filename)

        caption = (
            f"📊 <b>{BRAND_NAME} — NATIJALAR HISOBOTI (CSV)</b>\n"
            f"🏛️ <b>Markaz:</b> {CENTER_NAME}\n"
            f"📅 <b>Sana:</b> {get_tashkent_now_str()}\n"
            f"✅ <i>Excel dasturida to'g'ridan-to'g'ri ochiladi.</i>"
        )

        await callback.message.bot.send_document(
            chat_id=callback.from_user.id,
            document=doc_file,
            caption=caption,
            parse_mode="HTML"
        )
        await callback.answer("✅ CSV hisoboti yuborildi!")
    except Exception as e:
        logger.error(f"Error in cb_admin_export_csv: {e}")
        await callback.answer("❌ CSV eksportda xatolik yuz berdi.", show_alert=True)


@router.callback_query(F.data == "adm:backup")
async def cb_admin_backup(callback: CallbackQuery):
    if not await check_admin_access(callback):
        return

    try:
        await callback.answer("⏳ Zaxira olinmoqda...")
        success = await perform_backup(callback.message.bot, manual=True)
        if success:
            await callback.message.answer(
                "✅ <b>Tizim zaxirasi muvaffaqiyatli saqlandi va yuklandi!</b>",
                parse_mode="HTML"
            )
        else:
            await callback.message.answer(
                "⚠️ Zaxira kanali sozlanmagan yoki yuklashda xatolik bo'ldi. Loglarni tekshiring.",
                parse_mode="HTML"
            )
    except Exception as e:
        logger.error(f"Error in cb_admin_backup: {e}")
