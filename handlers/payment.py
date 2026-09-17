"""
EduTest Pro - Telegram Stars (XTR) Payment Handler
Provides:
- /pro, /stars, /tariffs commands and interactive plan selector
- Official Telegram Stars invoice dispatch (currency="XTR", provider_token="")
- PreCheckoutQuery verification
- SuccessfulPayment event handling with idempotency protection
- Automatic PRO subscription activation and database recording
"""

import html
import logging
from datetime import datetime, timezone

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    LabeledPrice,
    Message,
    PreCheckoutQuery,
)

from config import BRAND_NAME, PAYMENTS_ENABLED, PRO_BETA_MODE, WEBAPP_URL
from database import db
from services.tier_service import (
    FREE_DAILY_QUESTIONS_LIMIT,
    FREE_WEEKLY_MOCKS_LIMIT,
    PRO_DAILY_FAIR_USE_LIMIT,
    TIER_PLANS,
    get_user_tier,
    is_user_pro,
)
from aiogram.types import WebAppInfo

logger = logging.getLogger("PaymentHandler")
router = Router()


def get_plans_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Generates inline keyboard with all available Telegram Stars plans."""
    if not PAYMENTS_ENABLED:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎯 'Xatomni tuzat' (Xatolarim)", callback_data="notebook_menu")],
            [InlineKeyboardButton(text="⏱️ Bugungi 10 daqiqalik mashq", callback_data="ex_start:daily_10m")],
            [InlineKeyboardButton(text="📱 Mini Appni Ochish", web_app=WebAppInfo(url=WEBAPP_URL))],
            [InlineKeyboardButton(text="⬅️ Asosiy Menyu", callback_data="back_to_menu")]
        ])

    buttons = []
    for plan_id, plan in TIER_PLANS.items():
        buttons.append([
            InlineKeyboardButton(
                text=f"{plan['title']} — {plan['stars']} ⭐",
                callback_data=f"buy_plan_{plan_id}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(text="ℹ️ Ta'riflar Taqqoslovi", callback_data="tier_comparison"),
        InlineKeyboardButton(text="⬅️ Asosiy Menyu", callback_data="back_to_menu")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command("pro", "stars", "tariff", "tariffs", "plans"))
async def cmd_pro_plans(message: Message):
    """Displays user's current subscription status and upgrade options."""
    user_id = message.from_user.id
    user_name = html.escape(message.from_user.first_name or "Abituriyent")
    tier_info = get_user_tier(user_id)

    if not PAYMENTS_ENABLED:
        beta_text = (
            f"🚀 <b>{BRAND_NAME} — OCHIQ BETA BOSQICHI</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Assalomu alaykum, <b>{user_name}</b>!\n\n"
            f"Hozirda EduTest Pro barcha o'quvchilar uchun <b>BEPUL BETA</b> rejimida ishlamoqda! "
            f"Sizga sifatli va doimiy foydali tayyorgarlik vositasini taqdim etish biz uchun birinchi o'rinda.\n\n"
            f"<b>🆓 Barcha O'quvchilar Uchun Ochiq Imkoniyatlar:</b>\n"
            f"• 🎯 <b>Kuniga 50 ta yangi savol</b> (barcha mavzular, to'liq yechimlar bilan)\n"
            f"• 🔄 <b>Xatolar daftarchasi</b> — cheksiz va bepul qayta ishlash\n"
            f"• 🧠 <b>Moslashuvchan tayyorgarlik rejasi</b> (imtihon sanangizga mos)\n"
            f"• 🛠️ <b>'Xatomni tuzat' mashg'uloti</b> (eski savolni yodlamasdan, yangi o'xshash savol yechish)\n"
            f"• ⏱️ <b>Shaxsiy sinov yaratish</b> (mavzu, qiyinlik va vaqtni o'zingiz belgilaysiz)\n"
            f"• 📊 <b>Vaqt strategiyasi</b> (Overtime vs Rushed xatoliklar tahlili)\n"
            f"• 📝 <b>Haftasiga to'liq Mock Imtihonlar</b> (haftasiga 1 ta Free, Pro Beta'da cheksiz)\n\n"
            f"🛡️ <b>Muhim kafolat:</b> Hech qanday to'lov yoki karta talab etilmaydi. "
            f"Sizning barcha natijalaringiz, xatolar daftarchangiz va tarixingiz doimiy saqlanadi!"
        )
        await message.answer(beta_text, reply_markup=get_plans_keyboard(user_id), parse_mode="HTML")
        return

    if tier_info["is_pro"]:
        status_text = (
            f"👑 <b>Sizning Ta'rifingiz: PRO A'ZO</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Assalomu alaykum, <b>{user_name}</b>!\n"
            f"• Holat: <b>Faol ✅</b>\n"
            f"• Amal qilish muddati: <b>{tier_info['expires_at']}</b> gacha\n"
            f"• Kunlik mashq chegarasi: <b>{PRO_DAILY_FAIR_USE_LIMIT} ta savol</b> (Fair Use)\n"
            f"• Imkoniyatlar: To'liq mock imtihonlar, shaxsiy zaif mavzular rejasi, 'Xatomni tuzat'.\n\n"
            f"<i>Muddatingizni oldindan uzaytirmoqchi bo'lsangiz, quyidagi paketlardan birini tanlang:</i>"
        )
    else:
        status_text = (
            f"💎 <b>{BRAND_NAME} — PRO IMKONIYATLARI</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Assalomu alaykum, <b>{user_name}</b>!\n"
            f"Siz hozirda <b>FREE (Bepul)</b> rejimdasiz.\n\n"
            f"<b>🆓 FREE ta'rifida:</b>\n"
            f"• Kuniga {FREE_DAILY_QUESTIONS_LIMIT} ta yangi savol\n"
            f"• Barcha savollar yechimlari va tushuntirishlari (100% ochiq)\n"
            f"• Xatolar daftarchasidagi barcha xatolarni qayta yechish cheklovsiz\n"
            f"• Haftasiga {FREE_WEEKLY_MOCKS_LIMIT} ta to'liq Mock imtihon\n"
            f"• Diagnostika testi\n\n"
            f"<b>👑 PRO ta'rifida nimalar qo'shiladi:</b>\n"
            f"• 🚀 Cheksiz to'liq Mock Testlar (Module 1 + Module 2)\n"
            f"• 🎯 Kuchsiz mavzular bo'yicha moslashuvchan reja\n"
            f"• 🛠️ 'Xatomni tuzat' (yangi o'xshash savollar bilan mashq)\n"
            f"• 📈 Vaqt tahlili (Overtime vs Rushed xatolar)\n"
            f"• Kunlik {PRO_DAILY_FAIR_USE_LIMIT} ta savollik mashq chegarasi (Fair Use)\n\n"
            f"👇 <i>To'lov rasmiy Telegram Stars (⭐) orqali xavfsiz va bir zumda amalga oshiriladi:</i>"
        )

    await message.answer(status_text, reply_markup=get_plans_keyboard(user_id), parse_mode="HTML")


@router.callback_query(F.data == "show_pro_plans")
async def cb_show_pro_plans(callback: CallbackQuery):
    """Callback returning or opening pro plans menu."""
    user_id = callback.from_user.id
    user_name = html.escape(callback.from_user.first_name or "Abituriyent")
    tier_info = get_user_tier(user_id)

    if not PAYMENTS_ENABLED:
        text = (
            f"🚀 <b>{BRAND_NAME} — OCHIQ BETA REJIMI</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Hurmatli <b>{user_name}</b>, barcha Pro imkoniyatlari hozirda <b>bepul</b> ochiq!\n\n"
            f"• Kuniga {FREE_DAILY_QUESTIONS_LIMIT} ta savol (Free) / {PRO_DAILY_FAIR_USE_LIMIT} ta (Pro Beta)\n"
            f"• Cheksiz xatolar tahlili va 'Xatomni tuzat' mashqlari\n"
            f"• Moslashuvchan haftalik reja va shaxsiy testlar\n"
            f"• Haftalik to'liq mock imtihonlar\n\n"
            f"<i>Hech qanday to'lov talab qilinmaydi. Natijalaringiz doimiy saqlanadi!</i>"
        )
        try:
            await callback.message.edit_text(text, reply_markup=get_plans_keyboard(user_id), parse_mode="HTML")
        except Exception:
            await callback.message.answer(text, reply_markup=get_plans_keyboard(user_id), parse_mode="HTML")
        await callback.answer()
        return

    text = (
        f"💎 <b>{BRAND_NAME} — TA'RIF VA PAKETLAR</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Hurmatli <b>{user_name}</b>, o'zingizga qulay muddatni tanlang:\n\n"
        f"• <b>👑 1 Oylik PRO</b>: 250 ⭐ (~$4.99) — 30 kun to'liq tayyorgarlik\n"
        f"• <b>🏆 3 Oylik PRO</b>: 600 ⭐ (~$11.99) — 90 kunlik to'liq SAT kursi\n"
        f"• <b>⚡ 7 Kunlik PRO</b>: 75 ⭐ (~$1.49) — Imtihon oldi 1 haftalik intensiv\n\n"
        f"<i>To'lov bir zumda Telegram hisobingizdan yechiladi va barcha funksiyalar darhol ochiladi!</i>"
    )
    try:
        await callback.message.edit_text(text, reply_markup=get_plans_keyboard(user_id), parse_mode="HTML")
    except Exception:
        await callback.message.answer(text, reply_markup=get_plans_keyboard(user_id), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "tier_comparison")
async def cb_tier_comparison(callback: CallbackQuery):
    """Detailed comparison between Free and Pro tiers."""
    text = (
        f"⚖️ <b>FREE VA PRO TAQQOSLOVI</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"• <b>Diagnostika:</b> Free: ✅ | Pro: ✅\n"
        f"• <b>Kunlik yangi savollar:</b> Free: {FREE_DAILY_QUESTIONS_LIMIT} ta | Pro: {PRO_DAILY_FAIR_USE_LIMIT} ta\n"
        f"• <b>Yechimlar va izohlar:</b> Free: ✅ (100%) | Pro: ✅ (100% + Desmos)\n"
        f"• <b>Xatolar daftarchasi:</b> Free: Cheklovsiz ✅ | Pro: Cheklovsiz ✅\n"
        f"• <b>To'liq Mock Imtihonlar:</b> Free: Haftasiga {FREE_WEEKLY_MOCKS_LIMIT} ta ✅ | Pro: Cheksiz ✅\n"
        f"• <b>Moslashuvchan reja:</b> Free: Asosiy | Pro: Avtomatik qayta muvozanat ✅\n"
        f"• <b>'Xatomni tuzat' tizimi:</b> Free: Oddiy xatolar | Pro: Yangi o'xshash savollar ✅\n"
        f"• <b>Vaqt strategiyasi (Pacing):</b> Free: O'rtacha vaqt | Pro: Overtime & Rushed tahlili ✅\n\n"
        f"🛡️ <i>Muhim kafolat: Obuna muddati tugaganda ham barcha yechilgan savollar, natijalar va xatolar daftarchasi o'chmaydi!</i>"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="show_pro_plans")]
    ])
    try:
        await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    except Exception:
        await callback.message.answer(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()



@router.callback_query(F.data.startswith("buy_plan_"))
async def cb_buy_plan(callback: CallbackQuery):
    """Sends official Telegram Stars invoice for the selected plan."""
    user_id = callback.from_user.id
    plan_id = callback.data.replace("buy_plan_", "").strip()

    if not PAYMENTS_ENABLED:
        await callback.answer(
            "🚀 EduTest Pro hozirda Beta sinovida va barcha imkoniyatlar siz uchun bepul! Jonli to'lovlar yoqilmagan.",
            show_alert=True
        )
        return

    if plan_id not in TIER_PLANS:
        await callback.answer("Tanlangan ta'rif topilmadi!", show_alert=True)
        return

    plan = TIER_PLANS[plan_id]
    payload = f"sub_{plan_id}_{user_id}_{int(datetime.now(timezone.utc).timestamp())}"

    prices = [LabeledPrice(label=plan["title"][:30], amount=plan["stars"])]

    try:
        await callback.message.answer_invoice(
            title=plan["title"],
            description=plan["description"][:250],
            payload=payload,
            provider_token="",  # Must be empty string for Telegram Stars (XTR)
            currency="XTR",
            prices=prices,
            start_parameter=f"sub-{plan_id}"
        )
        await callback.answer("To'lov oynasi yuborildi! ⭐")
    except Exception as e:
        logger.error(f"Error sending invoice to user {user_id}: {e}")
        await callback.answer(f"Xatolik yuz berdi: {str(e)[:50]}", show_alert=True)


@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    """
    Validates pre-checkout query for Telegram Stars.
    Must always be answered within 10 seconds.
    """
    payload = pre_checkout_query.invoice_payload or ""
    if payload.startswith("sub_"):
        await pre_checkout_query.answer(ok=True)
    else:
        await pre_checkout_query.answer(ok=False, error_message="To'lov ma'lumotlarida noaniqlik mavjud.")


@router.message(F.successful_payment)
async def successful_payment_handler(message: Message):
    """
    Processes confirmed Telegram Stars payment:
    1. Idempotency check via telegram_payment_charge_id.
    2. Records transaction in database.
    3. Activates/extends PRO subscription.
    4. Congratulates user with onboarding instructions.
    """
    user_id = message.from_user.id
    payment = message.successful_payment
    charge_id = payment.telegram_payment_charge_id
    provider_charge_id = payment.provider_payment_charge_id
    total_stars = payment.total_amount
    payload = payment.invoice_payload or ""

    logger.info(
        f"Payment received: User={user_id}, Amount={total_stars} XTR, "
        f"ChargeID={charge_id}, Payload={payload}"
    )

    # Idempotency guard
    if db.has_payment_charge_id(charge_id):
        logger.warning(f"Duplicate payment charge_id ignored: {charge_id}")
        await message.answer("✅ Ushbu to'lov avval qabul qilingan va a'zoligingiz faollashtirilgan!")
        return

    # Determine plan from payload
    plan_id = "pro_1m"
    duration_days = 30
    for pid, pdata in TIER_PLANS.items():
        if pid in payload:
            plan_id = pid
            duration_days = pdata["days"]
            break

    # Record payment transaction
    await db.record_payment(
        user_id=user_id,
        plan_id=plan_id,
        stars_amount=total_stars,
        telegram_charge_id=charge_id,
        provider_payment_charge_id=provider_charge_id
    )

    # Activate PRO subscription
    sub = await db.add_user_subscription(
        user_id=user_id,
        plan_id=plan_id,
        duration_days=duration_days,
        stars_paid=total_stars,
        telegram_charge_id=charge_id
    )

    tier_info = get_user_tier(user_id)

    congrats_text = (
        f"🎉 <b>TABRIKLAYMIZ! TO'LOV MUVAFFAQIYATLI QABUL QILINDI!</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👑 <b>Siz endi EduTest Pro a'zosisiz!</b>\n\n"
        f"• Ta'rif: <b>{TIER_PLANS.get(plan_id, {}).get('title', 'PRO')}</b>\n"
        f"• Amal qilish muddati: <b>{tier_info['expires_at']}</b> gacha\n"
        f"• To'langan miqdor: <b>{total_stars} ⭐ (Telegram Stars)</b>\n\n"
        f"🚀 <b>Siz uchun ochilgan yangi imkoniyatlar:</b>\n"
        f"1. To'liq formatdagi Mock Testlar (/exam)\n"
        f"2. Kuchsiz mavzular bo'yicha shaxsiy drill mashqlari (/practice)\n"
        f"3. 3000+ original savollar banki\n"
        f"4. Kunlik 150 ta savollik erkin mashq chegarasi\n\n"
        f"<i>Mashg'ulotlarni boshlash uchun quyidagi tugmani bosing:</i>"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Mashq Markazini Ochish", callback_data="practice_hub")],
        [InlineKeyboardButton(text="📝 To'liq Mock Imtihon", callback_data="exam_hub")]
    ])

    await message.answer(congrats_text, reply_markup=kb, parse_mode="HTML")
