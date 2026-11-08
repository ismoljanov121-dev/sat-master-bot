"""
The ready-made advert post: video, caption and buttons that an admin forwards to other channels and groups.
"""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import BOT_USERNAME, CHANNEL_ID, CHANNEL_URL

# New users who arrive through the advert button are stored with this source. /admin counts them.
SOURCE = "promo"
CAPTION_LIMIT = 1024


def channel_handle() -> str:
    if CHANNEL_ID.startswith("@"):
        return CHANNEL_ID
    return "@" + CHANNEL_URL.rstrip("/").rsplit("/", 1)[-1]


CAPTION = (
    "🎓 <b>SAT va IELTS'ga Telegram'da bepul tayyorlaning!</b>\n\n"
    "✅ 5 ta adaptiv Digital SAT mock: 98 savol, taymer, kalkulyator va formulalar\n"
    "✅ Taxminiy ball oralig'i va zaif mavzular tahlili\n"
    "✅ Xatolar daftari: xato savollar 1, 3 va 7 kundan keyin qaytadi\n"
    "✅ IELTS Listening (audio bilan) va Reading testlari\n"
    "✅ Kunlik reja, eslatmalar va haftalik hisobot\n\n"
    f"📢 {channel_handle()} kanalida har kuni 10 ta post: so'zlar, testlar va maslahatlar.\n\n"
    "🆓 Hammasi bepul, faqat kanalga obuna bo'lasiz.\n\n"
    f"👇 Boshlash uchun tugmani bosing yoki @{BOT_USERNAME} ga yozing"
)

HELP = (
    "📣 <b>Reklama posti</b>\n\n"
    "Videoni botga oddiy video qilib yuboring (fayl qilib emas) va izohiga <code>/reklama</code> deb yozing. "
    "Bot uni matn va tugmalar bilan tayyor post qilib qaytaradi. Shu postni kanal va guruhlarga uzatasiz, "
    "tugmalar ham birga o'tadi.\n\n"
    "Videosiz varianti pastda 👇"
)


def keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Botni ochish", url=f"https://t.me/{BOT_USERNAME}?start={SOURCE}")],
        [InlineKeyboardButton(text="📢 Kanalga obuna bo'lish", url=CHANNEL_URL)],
    ])
