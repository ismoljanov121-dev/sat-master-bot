# EduTest Pro: Pedagogik Ramka va O'qitish Metodologiyasi
**Hujjat kodi:** `DOC-PED-2026-V1`  
**Muallif:** SAT Pedagogika & Cognitive Science Bo'limi  
**Maqsad:** SAT tayyorgarligini passiv yodlashdan faol tahliliy fikrlash va tizimli xatolarni bartaraf etishga aylantirish.

---

## 1. Asosiy Falsafa: "Micro-Drill & Honest Mastery"

Ko'plab onlayn botlar va platformalar o'quvchiga 10 ta savol berib, so'ng asossiz ravishda: *"Sizning balingiz: 1480!"* degan soxta hisobot chiqaradi. 

### Nega biz kichik testlarda (6–18 ta savol) 200–800 ballik shkalani ko'rsatmaymiz?
1. **Rasmiy Digital SAT Multistage Adaptive Testing (MST) tuzilishi:**
   - Rasmiy SAT imtihonida har bir bo'lim (Reading & Writing: 54 ta savol, Math: 44 ta savol) 2 ta adaptiv moduldan iborat.
   - 2-modulning qiyinlik darajasi 1-moduldagi natijaga qarab (Routing logic) o'zgaradi va Item Response Theory (IRT) algoritmi asosida vaznlangan ball (Scaled Score) hisoblanadi.
2. **Statistik ishonchlilik (Confidence Interval):**
   - 10 ta savolli mashqda tasodifiy xato yoki to'g'ri topish ehtimoli standart xatolikni (Standard Error of Measurement) $\pm 180$ ballgacha oshirib yuboradi.
   - O'quvchiga yolg'on ishonch berish uning haqiqiy imtihondagi tayyorgarligiga putur yetkazadi.
3. **Bizning Yondashuv:**
   - Kichik mashqlarda biz **Haqiqiy Ko'nikma Ko'rsatkichlari (Honest Mastery Metrics)**ni beramiz:
     - **Aniqlik foizi (Accuracy %)**: Aniq mavzular kesimida (masalan, Algebra 80%, Advanced Math 40%).
     - **Pacing / Sarflangan vaqt (O'rtacha sekund/savol)**: SAT'da vaqt taqsimoti eng kritik ko'nikma hisoblanadi.
     - **Zaif domenlar (Weak Areas)**: O'quvchining aynan qaysi qoidada qoqilayotgani.
   - 200–800 ballik rasmiy prognoz faqat to'liq 98 ta savolli **Full Diagnostic Mock** topshirilgandagina IRT simulyatsiyasi bilan hisoblanadi.

---

## 2. Besh Bosqichli Kognitiv O'rganish Sikli (The 5-Step Learning Loop)

EduTest Pro tizimi kognitiv psixologiyaning **Active Recall**, **Immediate Feedback** va **Spaced Repetition** qoidalariga tayanadi:

```
┌─────────────┐     ┌─────────────┐     ┌──────────────────┐
│  1. BUGUN   │ ──> │  2. MASHQ   │ ──> │ 3. JAVOB IZOHI   │
│ (Kunlik Maqsad)│     │(Fokus Mashq)│     │(Darhol Fikr-Mulohaza)│
└─────────────┘     └─────────────┘     └──────────────────┘
                                                  │
                                                  ▼
┌─────────────┐                         ┌──────────────────┐
│5. NATIJALAR │ <────────────────────── │ 4. XATOLARIM     │
│(Haqiqiy Tahlil)                        │ (Error Notebook) │
└─────────────┘                         └──────────────────┘
```

### 1-Qadam: Bugun (Daily Habit & Habit Loop)
- **Maqsad:** Har kuni muntazam shug'ullanish odatini (Atomic Habit) shakllantirish.
- **Mexanizm:**
  - Kunlik kvota: Har kuni 10 ta savol.
  - Streak (Ketma-ketlik): O'quvchining har kunlik faolligini qayd etish. 1 kun qoldirilsa streak sinishi mumkinligi doimiy intizomni ushlaydi.
  - Tezkor start: Oldingi yakunlanmagan mashqni bir bosish bilan davom ettirish (`resume_session`).

### 2-Qadam: Mashq (Targeted Practice)
- **Fokusli Tanlov:**
  - `Algebra` (Chiziqli tenglamalar, sistemalar, tengsizliklar).
  - `Advanced Math` (Kvadrat tenglamalar, ko'phadlar, nochiziqli funksiyalar).
  - `Problem Solving & Data Analysis` (Nisbatlar, foizlar, ehtimollik, statistik ma'lumotlar).
  - `Geometry & Trigonometry` (Burchaklar, aylanalar, trigonometriya, 3D shakllar).
  - `Reading & Writing` (Craft & Structure, Information & Ideas, Standard English Conventions, Expression of Ideas).
  - `Mixed Drill` (Aralash tezkor mashq).
- **Format:** 6 tadan 12 tagacha savolli ixcham partiyalar. O'quvchi charchamaydi, diqqat 100% jamlanadi.

### 3-Qadam: Javob Izohi (Instant Dual Explanation)
- **Muammo:** O'quvchi xato qilgach, to'g'ri javobni ko'ribgina keyingi savolga o'tib ketsa, kognitiv rivojlanish yuz bermaydi.
- **Yechim (Ikkilamchi Tushuntirish Tizimi):**
  1. **Konseptual Yechim (Step-by-Step Breakdown):**
     - Nega aynan shu javob to'g'ri?
     - Qaysi formulalar yoki grammatik qoidalar qo'llandi?
     - Qolgan variantlar nega xato (Distractor analysis)?
  2. **SAT Taktikasi & Desmos Hack:**
     - Math bo'limi uchun: Savolni Desmos Graphing Calculator orqali 15 soniyada qanday yechish mumkin (Regression `~`, Intersect, Table usuli).
     - Reading & Writing uchun: POE (Process of Elimination), Transition words mantiqi, kontekstdan kelib chiqish texnikasi.

### 4-Qadam: Xatolarim (Error Notebook / Spaced Repetition)
- Har qanday noto'g'ri belgilangan savol avtomatik ravishda o'quvchining shaxsiy **Xatolar daftari (Error Notebook)** bazasiga tushadi.
- Xatolar shunchaki saqlanib qolmaydi — o'quvchi ularni **"Xatolarni qayta yechish"** rejimi orqali qayta sinovdan o'tkazadi.
- Qachonki o'quvchi xato qilgan savolini qayta to'g'ri topsagina, u "O'zlashtirildi" (Resolved) deb belgilanadi.
- Bu orqali "bir marta ko'rdim va unutdim" sindromi ildizi bilan yo'qotiladi.

### 5-Qadam: Natijalar va Tahlil (Actionable Analytics)
- Mashq yakunida ko'rsatiladigan ma'lumotlar:
  - **Savollar soni va To'g'rilik foizi** (masalan, 10 tadan 8 tasi to'g'ri — 80%).
  - **O'rtacha sarflangan vaqt** (masalan, 52 sek/savol — rasmiy SAT Math me'yori 95 sek, demak pacing a'lo darajada).
  - **Kuchli va Zaif tomonlar ro'yxati**: O'quvchiga ertangi mashq uchun aniq tavsiya (masalan: *"Geometry bo'yicha yana 5 ta mashq bajaring"*).

---

## 3. Pedagogik Maslahatlar va Ko'rsatmalar
1. **Stressni kamaytirish:** Tayyorgarlik jarayoni imtihon qo'rquvini emas, balki qobiliyatga bo'lgan ishonchni oshirishi shart.
2. **Kichik g'alabalar (Micro-wins):** 10 ta savoldan 8 tasini to'g'ri yechish 100 ta savolli og'ir testdan ko'ra ko'proq motivatsiya va dofamin beradi.
3. **O'zbek tilidagi tushuntirish kuchi:** Ko'plab o'quvchilar ingliz tilidagi rasmiy tushuntirishlarni to'liq anglay olmaydi. O'zbek tilidagi tushunarli, aniq va lisoniy jihatdan mukammal tushuntirishlar tushunish tezligini 3 barobarga oshiradi.
