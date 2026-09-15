# EduTest Pro — Administrator Demo Qo'llanmasi (5 Daqiqalik Runbook)

Ushbu qo'llanma bugun **Marstif Academy** rahbari va ma'muriyati (Marifat Jamal) oldida **EduTest Pro** tizimini 5 daqiqa ichida xatosiz, professional va hayratlanarli darajada ko'rsatish uchun mo'ljallangan.

---

## 1. Uchrashuvdan 15 daqiqa oldin tayyorgarlik (Checklist)

1. **Telegram Akkaunt va Bot tekshiruvi:**
   - O'zingizning Telegram ID raqamingiz `.env` faylida `ADMIN_IDS` ro'yxatiga kiritilganini tekshiring:
     ```env
     ADMIN_IDS=SIZNING_TELEGRAM_ID
     CENTER_NAME="MARSTIF ACADEMY"
     MENTOR_NAME="Marifat Jamal"
     ```
2. **Botni lokal ishga tushirish:**
   ```powershell
   cd D:\AntigravityWorkspace\projects\sat_ai_bot
   python bot.py
   ```
   Konsolda quyidagi xabarni ko'ring:
   ```
   🚀 EduTest Pro TIZIMI ISHGA TUSHDI!
   🤖 Bot: @edutest_pro_bot
   🏛️ Markaz: MARSTIF ACADEMY
   🌐 Web Server & /api/v1/ listening on port 8080
   ```
3. **Avtomatlashtirilgan testlarni yashil holatini tekshirish:**
   ```powershell
   python -m unittest discover -v tests
   # 11 tests in 0.002s — OK!
   ```

---

## 2. 5 Daqiqalik Administrator Demo Ssenariysi

### 00:00 – 01:00 | 1-qadam: Kirish va Mahsulot Pozitsionirovkasi
- **Siz aytasiz:**
  > *"Assalomu alaykum! Biz bilamizki, har shanba-yakshanba markazda Digital SAT mock imtihonini o'tkazish, test varaqalarini tarqatish, 50-60 ta o'quvchining javobini qo'lda tekshirish kamida 3-4 soat o'qituvchi va ma'murlar vaqtini oladi. O'quvchi natijasini esa 2 kundan keyin oladi.
  > Biz Marstif Academy uchun **EduTest Pro** tizimini tayyorladik. Hozir 3 daqiqa ichida bu jarayon qanday qilib to'liq avtomatlashtirilgan va lahzalik (real-time) natijaga aylanishini ko'rsataman."*

---

### 01:00 – 02:30 | 2-qadam: O'quvchi Tajribasi (Student Journey & Demo Mock)
- **Ko'rsatasiz:**
  1. Telefoningizda botga `/start` yuborasiz.
  2. Ekrandagi toza brendingni ko'rsatasiz:
     - `EduTest Pro — MARSTIF ACADEMY`
     - 3 ta asosiy yo'nalish: `🔬 Diagnostika`, `📝 Mock Imtihon`, `📚 SAT Mashq Bazasi`.
  3. **`📝 Mock Imtihon`** tugmasini bosing:
     - `⚡ Demo Mock (12 savol / 12 daqiqa)` ni tanlang.
  4. Test jarayoni:
     - Ekranda savol, variantlar (A, B, C, D) va server taymeri (`⏳ Qolgan vaqt: 11:58`).
     - Variantlarni bosing — tizim javobni xavfsiz qayd etadi (qayta bosilsa ham ball ko'paymaydi).
     - 2-3 ta savolga javob berib, **`🏁 Tugatish`** tugmasini bosing.
  5. **Natija kartochkasi chiqadi:**
     - Umumiy aniqlik foizi (masalan: `75% — 9/12 to'g'ri`).
     - Bo'limlar kesimi: Math, Reading, Writing alohida ko'rsatiladi.
     - Kuchsiz mavzular (Weaknesses) aniqlab beriladi (masalan: *Algebra - Linear Equations*).
  - **Siz aytasiz:**
    > *"Ko'rib turganingizdek, o'quvchi testni tugatishi bilanoq, o'qituvchi 1 daqiqa ham vaqt sarflamasdan o'quvchining qaysi bo'limda oqsayotganini ko'radi."*

---

### 02:30 – 04:00 | 3-qadam: Administrator Paneli & Jonli Sessiya (Admin Live Control)
- **Ko'rsatasiz:**
  1. Botga `/admin` buyrug'ini yuboring (yoki menyudagi `⚙️ Administrator Paneli` tugmasini bosing).
  2. **Real-time statistika ekrani:**
     - Jami o'quvchilar soni.
     - Bugun faol o'quvchilar.
     - O'rtacha aniqlik foizi.
  3. **Guruhli Imtihon Sessiyasini Ochish:**
     - **`🎯 Yangi Mock Sessiya Ochish`** tugmasini bosing.
     - Tizim 6 xonali maxsus kod beradi (masalan: `MARS26`).
     - **Siz aytasiz:**
       > *"Dars xonasida o'qituvchi doskaga 'MARS26' deb yozib qo'yadi. Butun guruh botga '/mock MARS26' deb yozishi bilan barcha o'quvchilarda bir vaqtda test boshlanadi. Vaqt tugashi bilan test avtomatik yopiladi."*
  4. **Natijalarni ko'rish:**
     - **`👥 So'nggi Natijalar`** tugmasi orqali o'quvchilarning topshirgan testlari ro'yxatini ko'rsatasiz.

---

### 04:00 – 05:00 | 4-qadam: 1-Klikda Excel / CSV Eksport
- **Ko'rsatasiz:**
  1. Admin panelida **`📥 Natijalarni CSV Yuklab Olish`** tugmasini bosing.
  2. Bot bir necha soniyada to'liq formatlangan `.csv` faylini yuboradi (`edutest_pro_results_...csv`).
  3. Telegram ichida yoki Excelda faylni ochib ko'rsatasiz:
     - O'quvchi ismi, Telegram ID, username.
     - To'g'ri javoblar soni va aniqlik foizi.
     - Math / Reading / Writing kesimi.
     - Toshkent vaqti bilan yozilgan sana.
  - **Siz aytasiz:**
    > *"Bu hisobotni markaz rahbariyati oylik hisobotlarga, ota-onalar bilan suhbatlarga yoki o'qituvchilar monitoringiga to'g'ridan-to'g'ri biriktirishi mumkin. Hech qanday qog'ozbozliksiz."*

---

## 3. Kutilmagan vaziyatlar va Failover Rejasi (Internet va Xotira Himoyasi)

- **Tarmoq va Xotira Ishonchliligi:**
  - Telegram boti ishlashi uchun internet aloqasi majburiydir (Telegram serverlari bilan bog'lanish uchun).
  - Biroq, MongoDB buluti uzilsa yoki server to'satdan o'chib qolsa, bot lokal `users_db.json` faylida to'liq atomik keshda ishlaydi.
  - Ma'lumotlar yo'qolmaydi (`asyncio.Lock`, flush, fsync va `os.replace` himoyasi bor).
  - Agar tashqi internet uzilsa, WebApp interfeysini lokal brauzerda `http://127.0.0.1:8080/webapp` orqali "Offline Demo Rejimi"da xavfsiz ko'rsatishingiz mumkin.

---

## 4. Halol Cheklovlar va Professional Javoblar

- **Savol:** *"Bu College Board'ning rasmiy 1600 ballini beradimi?"*
  - **Javob:** *"Yo'q, va biz buni halol aytamiz. Rasmiy 1600 ballik shkala College Board'ning maxsus IRT (Item Response Theory) adaptiv algoritmi orqali hisoblanadi. EduTest Pro o'quv markazning ichki mock testi bo'lib, o'quvchining haqiqiy aniqlik foizini (Accuracy %) va zaif mavzularini aniqlab berishga ixtisoslashgan."*

- **Savol:** *"O'quvchi boshqa ilovaga chiqib ketsa qanday bilamiz?"*
  - **Javob:** *"Mini App'da o'quvchi boshqa oynaga o'tganda (tab hidden) xizmat signali loglanadi. Biroq yuqori darajadagi jiddiy imtihonlarda markaz xonasida telefonlarni stol ustiga qo'yish yoki kuzatuvchi nazorati eng ishonchli yechim bo'lib qoladi."*
