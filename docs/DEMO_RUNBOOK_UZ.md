# Markaz rahbariyati uchun 5 daqiqalik demo

Bu qo'llanma tizimni o'quv markazi rahbariyatiga ko'rsatish uchun. Hamma qadamlar hozirgi bot va Mini App'da ishlaydi.

Demo uchun ikkita telefon kerak: biri o'qituvchi, biri o'quvchi.

---

## 1. Uchrashuvdan oldin

1. Render'da `ADMIN_IDS`, `DATABASE_URL` va `GEMINI_API_KEY` sozlanganini tekshiring.
2. Botga `/admin` yuboring. Saqlash qatorida Postgres ko'rinishi kerak.
3. Markaz yarating: `/center_add Marstif Academy`. Bot o'qituvchilar uchun taklif havolasini beradi.
4. O'qituvchi telefonida havolani oching. Mini App'dagi Profil bo'limida Markaz paneli paydo bo'ladi.
5. O'quvchi telefonida bir marta mock yoki mashq ishlab qo'ying, shunda Natijalar bo'limi bo'sh bo'lmaydi.

---

## 2. Demo ssenariysi

### 00:00 – 01:00 | Muammo

> "Mock imtihonni qog'ozda o'tkazish va 50 ta o'quvchining javobini qo'lda tekshirish soatlab vaqt oladi. Bu tizimda o'quvchi testni tugatishi bilan natija o'qituvchining telefonida turadi."

### 01:00 – 02:30 | O'quvchi tajribasi

1. Mini App'ni oching va Bugun ekranini ko'rsating: kunlik reja, seriya, haftalik faollik.
2. SAT bo'limida mock'ni boshlang. Taymer, savollar xaritasi, kalkulyator va formulalar varag'ini ko'rsating.
3. Natijalar bo'limida oldingi hisobotni oching: ball oralig'i, mavzular bo'yicha tahlil, keyingi qadamlar.

> "O'quvchi faqat ball emas, aynan qaysi mavzuda oqsayotganini va keyin nima qilishni ko'radi."

### 02:30 – 04:00 | Guruh imtihoni

1. O'qituvchi telefonida: Profil, Markaz paneli, Yangi guruh imtihoni.
2. 🔒 belgili imtihonni tanlang. Tizim 6 belgili kod beradi.
3. O'quvchi telefonida botga `/mock KOD` yozing yoki "Guruhga havola yuborish" tugmasidan foydalaning.
4. O'quvchi ism-familiyasini yozib, imtihonni boshlaydi.
5. O'qituvchi telefonida "Yangilash" tugmasini bosing: o'quvchi "Ishlamoqda" bo'lib chiqadi.

> "O'qituvchi kodni doskaga yozadi, o'quvchilar telefonida ochadi. Qog'oz kerak emas. Kim ishlayotganini shu yerdan ko'rib turasiz."

Vaqt kam bo'lsa, oldindan tugatilgan imtihon natijalarini oching.

### 04:00 – 05:00 | Natijalar va hisobot

1. Markaz panelida imtihonni oching: topshirganlar, o'rtacha ball, natijalar jadvali.
2. Guruhning zaif mavzulari blokini ko'rsating.
3. CSV yuklash tugmasini bosing. Fayl bot chatiga keladi va Excel'da ochiladi.

> "O'qituvchi keyingi darsni aynan shu zaif mavzulardan boshlashi mumkin."

---

## 3. Kutilmagan vaziyatlar

- **Mini App ochilmasa:** `https://sat-master-bot.onrender.com/health` manzilini tekshiring. `status: ok` chiqishi kerak.
- **Internet uzilsa:** o'quvchi tugatgan test telefonda saqlanadi va keyingi ochilishda serverga yuboriladi.
- **Himoyalangan imtihonda modul oxirida internet uzilsa:** javoblar saqlanadi, ekranda "Qayta urinish" tugmasi chiqadi.
- **Mini App yopilib qolsa:** tugallanmagan mock Bugun ekranida "Tugallanmagan imtihon" bo'lib chiqadi. Vaqt to'xtamaydi.
- **AI band bo'lsa:** tekshiruv sarflanmaydi, bir ozdan keyin qayta uriniladi.

---

## 4. Halol javoblar

**"Bu rasmiy 1600 ballik natijami?"**
Yo'q. Ball savollarning qiyinligini hisobga olib taxminan hisoblanadi va oraliq bilan ko'rsatiladi. Savollar College Board'niki emas, bu mustaqil mashq platformasi.

**"O'quvchi javoblarni ko'chira oladimi?"**
🔒 belgili imtihonda javob kalitlari telefonga tushmaydi, ikkinchi modulni server tanlaydi, bir o'quvchidan bitta natija olinadi va vaqtni server hisoblaydi. Variantlar tartibi hamma uchun bir xil va o'quvchi boshqa telefonga qarashi mumkin, shuning uchun xonada kuzatuv baribir kerak. Bunday imtihon hozircha 1 ta SAT mock va 1 ta Reading. Ochiq testlarda kalitlar ilova ma'lumotida turadi.

**"AI bahosiga ishonsa bo'ladimi?"**
U mashq uchun yo'l-yo'riq beradi. Rasmiy IELTS bahosi o'rnini bosmaydi, yakuniy bahoni o'qituvchi beradi.

**"Savollar qancha?"**
967 ta SAT savoli, 5 ta to'liq mock (1 tasi himoyalangan), 4 ta Reading (1 tasi himoyalangan), 2 ta Listening testi va 46 ta Writing mavzusi. Yangi savollar qo'shib boriladi.
