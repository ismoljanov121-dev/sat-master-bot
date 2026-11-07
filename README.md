# IELTS & SAT Daily

Telegram bot va Mini App: Digital SAT va IELTS Academic'ka bepul tayyorgarlik, o'quv markazlari uchun guruh imtihonlari.

Bot: [@ieltssat_dailybot](https://t.me/ieltssat_dailybot) · Kanal: [@ieltssat_daily](https://t.me/ieltssat_daily)

## Imkoniyatlar

**O'quvchi uchun**
- 5 ta adaptiv Digital SAT mock: 98 savol, ikkinchi modul birinchi modul natijasiga qarab tanlanadi
- Imtihon asboblari: kalkulyator, formulalar varag'i, savolni belgilash, variantni chizish, matnni ajratish
- Formulalar, grid-in savollar, grafik va chizmalar
- Ball oralig'i bilan hisobot: mavzular, qiyinlik va vaqt bo'yicha tahlil
- Mavzu bo'yicha 10 savollik mashqlar va xatolar daftari (1, 3, 7 kunlik takrorlash)
- Diagnostika, kunlik reja, eslatmalar va haftalik hisobot
- IELTS Listening (MP3 audio), Reading (4 ta test, 2 tasi to'liq uzunlikda), Writing (46 mavzu va AI tekshiruvi)
- Natijani ulashish va do'stlarni taklif qilish
- To'liq ekran: telefonda avtomatik, kompyuterda Bosh sahifa, Profil va imtihon ekranidagi tugma bilan. Tanlov eslab qolinadi

**O'quv markazi uchun**
- 6 belgili kod bilan guruh imtihoni, natijalar jadvali, guruhning zaif mavzulari, CSV eksport
- O'qituvchilarni taklif havolasi orqali qo'shish

**Kanal uchun**
- Kuniga 3 ta avtomatik post: lug'at, SAT savoli, strategiya. Hamma kontent ishlatilmaguncha takrorlanmaydi

## O'rnatish

```bash
pip install -r requirements.txt
cp .env.example .env
python bot.py
```

Python 3.10 yoki yangiroq kerak. Render va CI 3.14 da ishlaydi (`.python-version`).

## Sozlamalar

| O'zgaruvchi | Vazifasi |
| :--- | :--- |
| `BOT_TOKEN` | BotFather'dan olingan token |
| `ADMIN_IDS` | Administratorlarning Telegram ID'lari, vergul bilan |
| `DATABASE_URL` | Postgres manzili. Busiz natijalar Render'da har deploy'da o'chadi |
| `GEMINI_API_KEY` | AI Writing uchun. Busiz bu funksiya o'chiq turadi |
| `GEMINI_MODELS` | Modellar ro'yxati, navbat bilan sinaladi |
| `AI_DAILY_LIMIT` | Bir foydalanuvchi uchun kunlik AI tekshiruvlar soni, standart 3 |
| `AI_GLOBAL_DAILY_LIMIT` | Hamma uchun kunlik chegara, standart 200 |
| `WEBAPP_URL` | Mini App manzili |
| `CHANNEL_ID`, `CHANNEL_URL` | Kunlik postlar kanali |
| `DESMOS_API_KEY` | Bo'lsa, grafik Desmos kalkulyatori ochiladi. Ishlab chiqarish kaliti Desmos'dan so'raladi |
| `SENTRY_DSN` | Ixtiyoriy xatolar monitoringi |

Xatolar `ADMIN_IDS`dagi administratorlarga Telegram orqali ham yuboriladi.

## Lokal ko'rish

Telegram'siz Mini App'ni brauzerda ochish uchun:

```bash
python scripts/dev_server.py
```

Skript yorug' va qorong'i mavzu uchun imzolangan test havolalarini chiqaradi. Administrator panelini ko'rish uchun `ADMIN_IDS=1000` bilan ishga tushiring.

## Kontent

Manba fayllar `data/` papkasida, Listening matnlari `scripts/listening_scripts.py`da. O'zgartirishdan keyin:

```bash
python scripts/build_content.py
node scripts/check_math.mjs
```

Birinchi buyruq `webapp/data/` fayllarini va mock'larni qayta yig'adi, ikkinchisi hamma formulalarni KaTeX bilan tekshiradi. Formulalar `\(...\)` ichida yoziladi. Listening audiosini qayta yaratish tartibi `scripts/generate_listening_audio.py` boshida yozilgan.

## Testlar

```bash
python -m unittest discover -s tests -t .
```

GitHub Actions har push'da testlarni SQLite va Postgres'da ishlatadi.

## Deploy

Render `main` branch'idan avtomatik deploy qiladi. Tashqi uptime monitori (masalan, cron-job.org) quyidagi manzilni har 10 daqiqada tekshirsin:

```text
https://sat-master-bot.onrender.com/health
```

`/health` baza yoki polling ishlamasa, 503 qaytaradi.

## Tuzilishi

```text
bot.py            ishga tushirish, veb-server, health check
webapi.py         Mini App uchun /api/v1, initData bilan himoyalangan
database.py       Postgres yoki SQLite
scheduler.py      kanal postlari, eslatmalar, haftalik hisobot
handlers/         bot buyruqlari
services/         baholash, takrorlash, reja, AI, markazlar
webapp/           Mini App
data/             savollar va IELTS manbalari
scripts/          kontent yig'ish va lokal server
```

## Cheklovlar

- Ballar taxminiy, rasmiy College Board yoki IELTS natijasi emas.
- Javob kalitlari Mini App ma'lumotida turadi, shunda imtihon yomon internetda ham ishlaydi. Server har urinishni qayta baholaydi, lekin nazoratli imtihonda telefonlarni kuzatish markaz zimmasida.
- Taymer qurilmada ishlaydi.
- AI Writing bahosi yo'l-yo'riq uchun, rasmiy baho o'rnini bosmaydi.
