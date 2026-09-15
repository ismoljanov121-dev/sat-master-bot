# CHANGELOG — EduTest Pro Demo Hardening

Ushbu hujjatda `feature/edutest-pro-demo` branchida bugungi Marstif Academy administrator namoyishi uchun amalga oshirilgan barcha o'zgarishlar, xavfsizlik mustahkamlanishlari va yangi modullar qayd etilgan.

---

## 1. Yangi Modullar va Funksiyalar (New Features)

1. **`services/exam_service.py`:**
   - Server-authoritative `ExamEngine` state machine (`created` → `active` → `submitted` / `expired`).
   - `demo_mock` shabloni (12 savol / 12 daqiqa: 4 Math, 4 Reading, 4 Writing).
   - `marstif_full` shabloni va pool yetarliligini halol tekshiruvchi guard (`check_template_pool_sufficiency`).
   - Deterministik randomizatsiya va variantlar (A, B, C, D) almashganda to'g'ri kalitni avtomatik remap qilish.
   - Server tomondan qat'iy deadline nazorati va timeout boshqaruvi.
   - Natijalarni aniqlik foizi va zaif mavzular bo'yicha tahlil qilish.

2. **`handlers/exam.py`:**
   - O'quvchilar uchun `/mock` buyrug'i va `ex:*` callbacklari.
   - 64-bayt Telegram limitidan oshmaydigan ultra-qisqa callback formati (`ex:a:<opt>`, `ex:n:<idx>`).
   - Guruh imtihoni uchun 6 xonali sessiya kodi orqali kirish (`/mock MARS26`).
   - To'xtatilgan testni davom ettirish (Resume) imkoniyati.

3. **`handlers/admin.py`:**
   - Qat'iy `is_admin(user_id)` tekshiruvi bilan himoyalangan `/admin` boshqaruv paneli.
   - Real-time statistika: Jami o'quvchilar, bugun faollar, o'rtacha aniqlik, topshirilgan mocklar.
   - Jonli mock sessiya ochish va 6 xonali join code shakllantirish (`MARS26`).
   - Faol sessiyalarni yopish (Close session).
   - O'quvchilar natijalari va zaif mavzularini ko'rish.
   - 1-klikda to'liq natijalar hisobotini CSV fayl sifatida yuklab olish.

4. **`services/auth_service.py`:**
   - Telegram WebApp `initData` ma'lumotlarini rasmiy HMAC-SHA256 algoritmi orqali tekshirish.
   - `auth_date` eskirish chegarasi (24 soat) bilan replay-hujumlarni bartaraf etish.

5. **`tests/test_edutest_core.py`:**
   - 11 ta to'liq avtomatlashtirilgan unit/integration testlar (Branding, Question Schema, Exam Engine, Shuffle Remapping, Timeout, Sufficiency, Admin Auth, Idempotency, HMAC Validation, Atomic Persistence, XSS Sanitization).

---

## 2. Mustahkamlangan va Xavfsizlashtirilgan Qismlar (Hardening & Bug Fixes)

1. **`database.py` (Atomik Yozish & Yangi Jadvallar):**
   - Lokal faylga yozish `asyncio.Lock` va vaqtinchalik `.tmp` fayl + `flush` + `os.fsync` + `os.replace` orqali atomik holatga keltirildi.
   - Buzilgan JSON aniqlansa, avtomatik zaxira nusxa yaratilib, default schema tiklanishi ta'minlandi.
   - `exam_sessions`, `exam_attempts` va `webapp_data` yangi jadvallari qo'shildi.
   - Toshkent vaqti (UTC+5) bo'yicha hisobotlar shakllantirish qo'shildi.

2. **`handlers/diagnostic.py` (Idempotency Himoyasi):**
   - `answered_indices` ro'yxati joriy etildi. Foydalanuvchi bir savol tugmasini bir necha marta bosganda yoki eski callback qayta yuborilganda ball sun'iy oshib ketishi butunlay bartaraf etildi.

3. **`handlers/stats.py` (/backup Huquqi):**
   - Oldin ochiq bo'lgan `/backup` buyrug'i faqat `ADMIN_IDS` a'zolari uchungina ruxsat beriladigan qilib filtrlandi.

4. **`handlers/start.py` (3 Asosiy P0 Yo'nalish & Brending):**
   - Asosiy menyuda 3 ta aniq P0 tugma: `🔬 Diagnostika`, `📝 Mock Imtihon`, `📚 SAT Mashq Bazasi`.
   - "AI 100 ball oshiradi" kabi isbotlanmagan da'volar olib tashlandi.
   - "Desmos Hiylalari" o'rniga professional "Desmos Strategiyalari" kiritildi.
   - Adminlar uchun `⚙️ Administrator Paneli` tugmasi avtomatik ko'rinishi ta'minlandi.

5. **`bot.py` (API & Graceful Shutdown):**
   - aiohttp serverida `/api/v1/auth/validate`, `/api/v1/user/progress` va `/api/v1/user/attention-event` APIlari ishga tushirildi.
   - Bot yopilayotganda backup task, bot session, database client va web runner toza yopilishi (graceful shutdown) ta'minlandi.

6. **`webapp/index.html` (XSS Sanitizatsiyasi & Backend Sinxronlash):**
   - Foydalanuvchi kiritgan vazifa va xatolar matnlari `escapeHTML()` orqali xavfsiz holatga keltirildi.
   - Yechim havolalari faqat `https://` protokoli orqali ochilishi chegaralandi.
   - Brauzerda tashqaridan ochilganda "Demo Ko'rgazma Rejimi" baneri ko'rsatiladi.
