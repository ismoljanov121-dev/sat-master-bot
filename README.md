# EduTest Pro — Raqamli Diagnostika va Mock Imtihon Ekotizimi

EduTest Pro o'quv markazlari (IELTS, Digital SAT, Fanlar) uchun mo'ljallangan markazlashtirilgan diagnostika, mock imtihon, dars nazorati va o'quvchi natijalari monitoringi tizimidir.

Demo muhiti: **MARSTIF ACADEMY**

---

## 1. Talablar (Requirements)

- **Python:** 3.10 yoki undan yuqori (tizimda Python 3.14 o'rnatilgan)
- **Kutubxonalar:**
  - `aiogram >= 3.31.0`
  - `aiohttp >= 3.14.0`
  - `python-dotenv >= 1.0.0`
  - `motor >= 3.7.0` (ixtiyoriy MongoDB uchun)

---

## 2. O'rnatish va Sozlash (Setup)

1. **Repozitoriyga o'tish:**
   ```powershell
   cd D:\AntigravityWorkspace\projects\sat_ai_bot
   ```

2. **Kutubxonalarni o'rnatish:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Konfiguratsiya (.env):**
   `.env.example` faylidan nusxa olib, `.env` faylini shakllantiring:
   ```env
   BOT_TOKEN="sizning_telegram_bot_tokeningiz"
   ADMIN_IDS="sizning_telegram_id_raqamingiz"
   CENTER_NAME="MARSTIF ACADEMY"
   MENTOR_NAME="Marifat Jamal"
   PORT=8080
   ```

---

## 3. Avtomatlashtirilgan Testlarni Ishga Tushirish (Testing)

Loyiha to'liq avtomatlashtirilgan unit va integration testlar bilan ta'minlangan (tashqi internet ulanishini talab qilmaydi):

```powershell
# Barcha testlarni ishga tushirish (11 ta test)
python -m unittest discover -v tests

# Sintaksis va kompilyatsiya tekshiruvi
python -m compileall -q .
```

---

## 4. Botni Ishga Tushirish (Run)

```powershell
python bot.py
```

Ishga tushgach:
- Telegram Bot: `@edutest_pro_bot`
- Web Server & API: `http://127.0.0.1:8080/`
- Health check: `http://127.0.0.1:8080/health`
- Mini App WebApp: `http://127.0.0.1:8080/webapp`

---

## 5. Demo Qo'llanmasi (Runbook)

Administrator bilan uchrashuvda 5 daqiqalik namoyish uchun batafsil ko'rsatmalar:
👉 **[DEMO_RUNBOOK_UZ.md](docs/DEMO_RUNBOOK_UZ.md)**

Markaz rahbariyati uchun B2B qiymat va hamkorlik taklifi:
👉 **[ADMIN_VALUE_PROPOSITION_UZ.md](docs/ADMIN_VALUE_PROPOSITION_UZ.md)**
