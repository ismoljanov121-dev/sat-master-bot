"""
Batch 5 Math Questions (34 Items: m_b5_01 through m_b5_34)
Authentic Digital SAT style, distinct options, SymPy verifiable.
"""

from typing import Any

BATCH_5_MATH: list[dict[str, Any]] = [
    # ==================== ALGEBRA (9 Questions) ====================
    {
        "id": "m_b5_01",
        "version": 1,
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear equations in one variable",
        "difficulty": "Easy",
        "status": "published",
        "passage": None,
        "question": "An environmental monitoring station uses a digital thermometer calibrated according to the formula T_c = 0.85 * T_raw - 4.2, where T_raw is the sensor resistance signal and T_c is the temperature in degrees Celsius. If the recorded Celsius temperature is 34.05 degrees, what was the sensor resistance signal T_raw?",
        "options": [
            {"key": "A", "text": "38.25"},
            {"key": "B", "text": "42.5"},
            {"key": "C", "text": "45"},
            {"key": "D", "text": "48"}
        ],
        "correct": "C",
        "explanation": "Berilgan formulaga T_c = 34.05 qiymatini qo'yamiz: 0.85 * T_raw - 4.2 = 34.05. Ikkala tomonga 4.2 qo'shamiz: 0.85 * T_raw = 38.25. T_raw ni topish uchun 38.25 ni 0.85 ga bo'lamiz: T_raw = 38.25 / 0.85 = 45. C variant to'g'ri. A variant (38.25) bo'lishni unutish natijasidir.",
        "strategy_or_hack": "⚡ DESMOS HACK: 1-qator: y = 0.85x - 4.2; 2-qator: y = 34.05. Kesishish nuqtasining x koordinatasi x = 45.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_02",
        "version": 1,
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear equations in two variables",
        "difficulty": "Medium",
        "status": "published",
        "passage": None,
        "question": "A community theater charges $14 per adult ticket and $9 per child ticket. For a Saturday matinee, a total of 320 tickets were sold, generating $3,630 in revenue. How many adult tickets were sold?",
        "options": [
            {"key": "A", "text": "150"},
            {"key": "B", "text": "170"},
            {"key": "C", "text": "185"},
            {"key": "D", "text": "210"}
        ],
        "correct": "A",
        "explanation": "Kattalar chiptasi soni a, bolalar chiptasi soni c bo'lsin. Sistema: a + c = 320 va 14a + 9c = 3630. Birinchi tenglamadan c = 320 - a ni ikkinchisiga qo'yamiz: 14a + 9(320 - a) = 3630 => 14a + 2880 - 9a = 3630 => 5a = 3630 - 2880 = 750 => a = 150 ta kattalar chiptasi sotilgan. Bolalar chiptasi: 320 - 150 = 170 ta (B variant chalg'ituvchi tuzoq).",
        "strategy_or_hack": "⚡ DESMOS HACK: Desmosga x + y = 320 va 14x + 9y = 3630 kiritiladi. Kesishish nuqtasi (150, 170). x = 150 darhol chiqadi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_03",
        "version": 1,
        "section": "math",
        "domain": "Algebra",
        "skill": "Systems of two linear equations in two variables",
        "difficulty": "Hard",
        "status": "published",
        "passage": None,
        "question": "A venture capital fund allocated a total of $4,500,000 across early-stage biotech and clean-energy startups. The expected annual return on biotech investments is 12%, and the expected return on clean-energy investments is 7%. If the total anticipated return from both sectors combined is $410,000, how much capital was invested in clean-energy startups?",
        "options": [
            {"key": "A", "text": "$1,900,000"},
            {"key": "B", "text": "$2,250,000"},
            {"key": "C", "text": "$2,600,000"},
            {"key": "D", "text": "$2,900,000"}
        ],
        "correct": "C",
        "explanation": "Biotech investitsiyasi b, toza energiya investitsiyasi c bo'lsin. Sistema: b + c = 4500000 va 0.12b + 0.07c = 410000. Birinchi tenglamadan b = 4500000 - c ni ikkinchisiga qo'yamiz: 0.12(4500000 - c) + 0.07c = 410000 => 540000 - 0.05c = 410000 => 0.05c = 130000 => c = $2,600,000. Biotech ulushi b = $1,900,000 (A variant tuzoq). C to'g'ri.",
        "strategy_or_hack": "⚡ DESMOS HACK: x + y = 4500000 va 0.12x + 0.07y = 410000 ni Desmosga kiritib, y koordinatasini qarang: y = 2600000.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_04",
        "version": 1,
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear functions and graphing (slopes, intercepts)",
        "difficulty": "Medium",
        "status": "published",
        "passage": None,
        "question": "Line L in the xy-plane passes through the points (-3, 7) and (5, -9). Line M is perpendicular to line L and passes through the point (4, 1). What is the y-intercept of line M?",
        "options": [
            {"key": "A", "text": "-1"},
            {"key": "B", "text": "-0.5"},
            {"key": "C", "text": "0.5"},
            {"key": "D", "text": "2"}
        ],
        "correct": "A",
        "explanation": "L chiziqning burchak koeffitsiyenti (slope): m_L = (-9 - 7) / (5 - (-3)) = -16 / 8 = -2. L chiziqqa perpendikulyar bo'lgan M chiziqning burchak koeffitsiyenti manfiy teskari (negative reciprocal) bo'ladi: m_M = -1 / (-2) = 1/2 = 0.5. M chiziq tenglamasi: y - 1 = 0.5(x - 4) => y = 0.5x - 2 + 1 => y = 0.5x - 1. y-intercept qiymati b = -1. D variant (2) x-intercept bilan adashtirish oqibatidir.",
        "strategy_or_hack": "⚡ DESMOS HACK: Desmosga m = (-9 - 7)/(5 - (-3)) deb kiritib, so'ng y - 1 = (-1/m)(x - 4) chiziladi. (0, -1) nuqta ko'rinadi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_05",
        "version": 1,
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear inequalities in one or two variables",
        "difficulty": "Medium",
        "status": "published",
        "passage": None,
        "question": "A catering service prepares boxed lunches. Each deluxe lunch requires 12 minutes to assemble, and each standard lunch requires 8 minutes. The catering staff can spend at most 6 hours assembling lunches today, and they must produce at least 35 total lunches. If d represents deluxe lunches and s represents standard lunches, which system models this situation?",
        "options": [
            {"key": "A", "text": "12d + 8s <= 360 and d + s >= 35"},
            {"key": "B", "text": "12d + 8s >= 360 and d + s <= 35"},
            {"key": "C", "text": "8d + 12s <= 6 and d + s >= 35"},
            {"key": "D", "text": "12d + 8s <= 6 and d + s >= 35"}
        ],
        "correct": "A",
        "explanation": "Vaqt birliklarini tenglashtiramiz: 6 soat = 6 * 60 = 360 daqiqa. 'At most 6 hours' demak <= 360 daqiqa: 12d + 8s <= 360. 'At least 35 lunches' demak d + s >= 35. C va D variantlarida soat va daqiqa birlashtirilmagan (6 deb olingan), B variantida esa tengsizlik ishoralari teskari.",
        "strategy_or_hack": "⚡ SAT STRATEGY: Birlik konversiyasiga doimo e'tibor bering: 6 soat = 360 minut. 'At most' = <=, 'at least' = >=.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_06",
        "version": 1,
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear equations in two variables",
        "difficulty": "Easy",
        "status": "published",
        "passage": None,
        "question": "The total cost C, in dollars, of renting a utility trailer for d days is given by the function C(d) = 42d + 35, where 35 represents a mandatory reservation and insurance fee. What is the rental cost for a customer who uses the trailer for 5 days?",
        "options": [
            {"key": "A", "text": "$210"},
            {"key": "B", "text": "$245"},
            {"key": "C", "text": "$280"},
            {"key": "D", "text": "$315"}
        ],
        "correct": "B",
        "explanation": "Funksiyaga d = 5 ni qo'yamiz: C(5) = 42(5) + 35 = 210 + 35 = $245. A variant ($210) faqat kunlik ijara haqini hisoblab, boshlang'ich $35 sug'urta to'lovini unutish natijasidir.",
        "strategy_or_hack": "⚡ DESMOS HACK: Desmosga C(d) = 42d + 35 kiritib, C(5) deb yozilsa, darhol 245 qiymatini qaytaradi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_07",
        "version": 1,
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear inequalities in one or two variables",
        "difficulty": "Hard",
        "status": "published",
        "passage": None,
        "question": "A logistics warehouse uses heavy-duty forklifts that can carry at most 3,200 kilograms per load. Each crate of industrial machinery weighs 140 kilograms, and each pallet of steel fasteners weighs 85 kilograms. If a forklift operator loads 12 crates of machinery, what is the maximum number of full pallets of fasteners that can be loaded without exceeding the forklift weight limit?",
        "options": [
            {"key": "A", "text": "16"},
            {"key": "B", "text": "17"},
            {"key": "C", "text": "18"},
            {"key": "D", "text": "19"}
        ],
        "correct": "B",
        "explanation": "12 ta uskuna qutisining umumiy og'irligi: 12 * 140 = 1680 kg. Qolgan ko'tarish quvvati: 3200 - 1680 = 1520 kg. Fastener palletlari soni p: 85 * p <= 1520 => p <= 1520 / 85 = 17.88... To'liq palletlar so'ralgani uchun maksimal butun son p = 17 bo'ladi. B variant to'g'ri. C variant (18) 1530 kg og'irlik hosil qilib limitdan oshadi.",
        "strategy_or_hack": "⚡ DESMOS HACK: (3200 - 12 * 140) / 85 hisoblansa 17.88 chiqadi. Pastga yaxlitlanadi: 17 ta.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_08",
        "version": 1,
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear functions and graphing (slopes, intercepts)",
        "difficulty": "Easy",
        "status": "published",
        "passage": None,
        "question": "The graph of the linear function f has an x-intercept at (8, 0) and a y-intercept at (0, -6). What is the slope of the graph of f?",
        "options": [
            {"key": "A", "text": "-4/3"},
            {"key": "B", "text": "-3/4"},
            {"key": "C", "text": "3/4"},
            {"key": "D", "text": "4/3"}
        ],
        "correct": "C",
        "explanation": "Burchak koeffitsiyenti formulasi: m = (y2 - y1) / (x2 - x1). Berilgan nuqtalar (x1, y1) = (8, 0) va (x2, y2) = (0, -6). m = (-6 - 0) / (0 - 8) = -6 / -8 = 3/4. B variant (-3/4) ishorada adashish, D variant (4/3) esa teskari nisbat (run over rise) xatosidir.",
        "strategy_or_hack": "⚡ DESMOS HACK: Desmos jadvaliga (8, 0) va (0, -6) kiritib, y1 ~ m*x1 + b regressiya chaqirilsa, m = 0.75 = 3/4 chiqadi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_09",
        "version": 1,
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear functions and graphing (slopes, intercepts)",
        "difficulty": "Hard",
        "status": "published",
        "passage": None,
        "question": "In the xy-plane, the vertices of a triangle are located at A(2, 3), B(8, 3), and C(5, 7). What is the area of triangle ABC?",
        "options": [
            {"key": "A", "text": "10"},
            {"key": "B", "text": "12"},
            {"key": "C", "text": "15"},
            {"key": "D", "text": "24"}
        ],
        "correct": "B",
        "explanation": "A(2, 3) va B(8, 3) nuqtalar y = 3 gorizontal to'g'ri chizig'ida yotadi. Demak, uchburchak asosi uzunligi: asos = 8 - 2 = 6 birlik. Balandlik esa C(5, 7) nuqtadan y = 3 to'g'ri chiziqqacha bo'lgan vertikal masofadir: balandlik = 7 - 3 = 4 birlik. Uchburchak yuzi formulasi: S = 0.5 * asos * balandlik = 0.5 * 6 * 4 = 12. B variant to'g'ri.",
        "strategy_or_hack": "⚡ DESMOS HACK: Desmosga polygon((2,3), (8,3), (5,7)) deb yozing, Desmos uning yuzini darhol 12 deb ko'rsatadi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },

    # ==================== ADVANCED MATH (9 Questions) ====================
    {
        "id": "m_b5_10",
        "version": 1,
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Nonlinear functions (quadratic vertex/standard form, exponential models, polynomials)",
        "difficulty": "Medium",
        "status": "published",
        "passage": None,
        "question": "An agricultural agronomist models the yield Y, in bushels of wheat per acre, as a function of fertilizer application x, in kilograms per hectare, using the quadratic function Y(x) = -0.05x^2 + 6x + 80. According to this model, what amount of fertilizer x maximizes the per-acre wheat yield?",
        "options": [
            {"key": "A", "text": "30"},
            {"key": "B", "text": "50"},
            {"key": "C", "text": "60"},
            {"key": "D", "text": "120"}
        ],
        "correct": "C",
        "explanation": "Kvadratik funksiya a = -0.05 < 0 bo'lgani uchun o'zining cho'qqi (vertex) nuqtasida maksimal qiymatga erishadi. Cho'qqining x koordinatasi: x = -b / (2a) = -6 / (2 * (-0.05)) = -6 / (-0.10) = 60 kg/ga. Demak, x = 60 bo'lganda hosildorlik eng yuqori bo'ladi. C to'g'ri.",
        "strategy_or_hack": "⚡ DESMOS HACK: y = -0.05x^2 + 6x + 80 ni chizib, parabolaning cho'qqisini bosing: (60, 260). x = 60 darhol ko'rinadi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_11",
        "version": 1,
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Nonlinear equations in one variable (quadratic, radical, absolute value)",
        "difficulty": "Hard",
        "status": "published",
        "passage": None,
        "question": "A model rocket is launched vertically from a platform. Its height h, in meters above the ground, t seconds after launch is modeled by the equation h(t) = -4.9t^2 + 39.2t + 4. At what time t, in seconds, does the rocket reach its maximum height?",
        "options": [
            {"key": "A", "text": "2.5"},
            {"key": "B", "text": "4.0"},
            {"key": "C", "text": "5.2"},
            {"key": "D", "text": "8.0"}
        ],
        "correct": "B",
        "explanation": "Maksimal balandlikka erishish vaqti parabolaning cho'qqisiga to'g'ri keladi: t = -b / (2a) = -39.2 / (2 * (-4.9)) = -39.2 / -9.8 = 4.0 soniya. B variant to'g'ri. D variant (8.0) raketaning yerga qaytib tushish vaqtiga yaqin bo'lib chalg'ituvchi tuzoqdir.",
        "strategy_or_hack": "⚡ DESMOS HACK: y = -4.9x^2 + 39.2x + 4 parabola cho'qqisi (4, 82.4) da joylashgan. Maksimal vaqt t = 4 soniya.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_12",
        "version": 1,
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Equivalent expressions (factoring, polynomial arithmetic)",
        "difficulty": "Medium",
        "status": "published",
        "passage": None,
        "question": "In quantum physics calculations, two state amplitudes are represented by complex numbers z1 = 4 - 3i and z2 = 2 + 5i, where i = sqrt(-1). What is the value of the complex product z1 * z2?",
        "options": [
            {"key": "A", "text": "23 + 14i"},
            {"key": "B", "text": "-7 + 14i"},
            {"key": "C", "text": "23 - 14i"},
            {"key": "D", "text": "8 - 15i"}
        ],
        "correct": "A",
        "explanation": "Qavslarni ochamiz: (4 - 3i)(2 + 5i) = 4(2) + 4(5i) - 3i(2) - 3i(5i) = 8 + 20i - 6i - 15(i^2). i^2 = -1 ekanini bilamiz, demak -15(-1) = +15. Haqiqiy qismlarni qo'shamiz: 8 + 15 = 23. Mavhum qismlarni qo'shamiz: 20i - 6i = 14i. Yakuniy natija: 23 + 14i. A variant to'g'ri. B variant i^2 = +1 deb xato olish natijasidir.",
        "strategy_or_hack": "⚡ SAT COMPLEX NUMBERS RULE: i^2 = -1 qoidasini unutmang: -15i^2 = -15(-1) = +15. Natija: 8 + 15 + 14i = 23 + 14i.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_13",
        "version": 1,
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Nonlinear functions (quadratic vertex/standard form, exponential models, polynomials)",
        "difficulty": "Hard",
        "status": "published",
        "passage": None,
        "question": "A sample of a radioactive isotope decays according to the model N(t) = 480 * (0.85)^(t / 12), where N(t) is the remaining mass in milligrams after t hours. Which of the following is the best interpretation of the number 12 in this context?",
        "options": [
            {"key": "A", "text": "The mass decreases by 15% every 12 hours."},
            {"key": "B", "text": "The mass decreases by 85% every 12 hours."},
            {"key": "C", "text": "The initial mass is 12 milligrams."},
            {"key": "D", "text": "The isotope completely decays after 12 hours."}
        ],
        "correct": "A",
        "explanation": "Eksponentsial ifodada 0.85 asos 1 - 0.15 ga teng, demak miqdor har bir siklda 15% ga kamayadi. Darajadagi t / 12 ifodasi ushbu 15% pasayish har 12 soatda bir marta sodir bo'lishini ko'rsatadi (t = 12 bo'lganda daraja 1 bo'ladi). Shuning uchun har 12 soatda massa 15% ga kamayadi.",
        "strategy_or_hack": "⚡ SAT STRATEGY: Ko'paytiruvchi 0.85 = (1 - 0.15) -> 15% pasayish. Daraja maxraji (12) esa bu o'zgarishning davriyligini (har 12 soat) belgilaydi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_14",
        "version": 1,
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Nonlinear functions (quadratic vertex/standard form, exponential models, polynomials)",
        "difficulty": "Medium",
        "status": "published",
        "passage": None,
        "question": "The rational function R is defined by R(x) = (3x + 12) / (x^2 - 7x + 10). For which of the following positive values of x is the function R undefined?",
        "options": [
            {"key": "A", "text": "2"},
            {"key": "B", "text": "3"},
            {"key": "C", "text": "4"},
            {"key": "D", "text": "7"}
        ],
        "correct": "A",
        "explanation": "Kasr funksiya maxraji nolga teng bo'lganda aniqlanmagan (undefined) bo'ladi: x^2 - 7x + 10 = 0. Ko'paytuvchilarga ajratamiz: (x - 2)(x - 5) = 0. Funksiya x = 2 va x = 5 da aniqlanmagan. Variantlar orasida x = 2 (A varianti) mavjud.",
        "strategy_or_hack": "⚡ DESMOS HACK: y = (3x + 12)/(x^2 - 7x + 10) ni kiritib, vertikal asimptotalarni qidiring: x = 2 va x = 5.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_15",
        "version": 1,
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Equivalent expressions (factoring, polynomial arithmetic)",
        "difficulty": "Hard",
        "status": "published",
        "passage": None,
        "question": "If (x^3 - 2x^2 - 17x + 10) / (x - 5) = ax^2 + bx + c for all x != 5, what is the value of a + b + c?",
        "options": [
            {"key": "A", "text": "2"},
            {"key": "B", "text": "4"},
            {"key": "C", "text": "6"},
            {"key": "D", "text": "8"}
        ],
        "correct": "A",
        "explanation": "Ko'phadni bo'lamiz: (x^3 - 2x^2 - 17x + 10) : (x - 5) = x^2 + 3x - 2. Tekshiramiz: (x - 5)(x^2 + 3x - 2) = x^3 + 3x^2 - 2x - 5x^2 - 15x + 10 = x^3 - 2x^2 - 17x + 10. Demak, ax^2 + bx + c = x^2 + 3x - 2, bu yerda a = 1, b = 3, c = -2. a + b + c = 1 + 3 + (-2) = 2. A variant to'g'ri.",
        "strategy_or_hack": "⚡ DESMOS HACK: y1 = (x^3 - 2x^2 - 17x + 10)/(x - 5) va y2 = x^2 + 3x - 2. x = 1 qo'yilsa, 1 + 3 - 2 = 2.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_16",
        "version": 1,
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Nonlinear equations in one variable (quadratic, radical, absolute value)",
        "difficulty": "Medium",
        "status": "published",
        "passage": None,
        "question": "What is the positive solution to the equation sqrt(3x + 16) - x = 2?",
        "options": [
            {"key": "A", "text": "1"},
            {"key": "B", "text": "3"},
            {"key": "C", "text": "4"},
            {"key": "D", "text": "7"}
        ],
        "correct": "B",
        "explanation": "Ildizni ajratamiz: sqrt(3x + 16) = x + 2. Ikkala tomonni kvadratga ko'taramiz: 3x + 16 = (x + 2)^2 => 3x + 16 = x^2 + 4x + 4. Tartiblaymiz: x^2 + x - 12 = 0. Ko'paytuvchilarga ajratamiz: (x + 4)(x - 3) = 0. Ildizlar x = -4 va x = 3. x = -4 ni tekshiramiz: sqrt(-12 + 16) - (-4) = 2 + 4 = 6 != 2 (chet ildiz). x = 3 ni tekshiramiz: sqrt(9 + 16) - 3 = 5 - 3 = 2 (to'g'ri). Musbat yechim x = 3.",
        "strategy_or_hack": "⚡ DESMOS HACK: y = sqrt(3x + 16) - x va y = 2 ni chizing. Kesishish nuqtasi x = 3 da aniq ko'rinadi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_17",
        "version": 1,
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Nonlinear functions (quadratic vertex/standard form, exponential models, polynomials)",
        "difficulty": "Easy",
        "status": "published",
        "passage": None,
        "question": "A colony of marine bioluminescent algae has an initial population of 2,500 cells and quadruples every 6 hours. Which of the following functions P models the population of the algae colony t hours after observation begins?",
        "options": [
            {"key": "A", "text": "P(t) = 2,500 * (4)^(t / 6)"},
            {"key": "B", "text": "P(t) = 2,500 * (4)^(6t)"},
            {"key": "C", "text": "P(t) = 2,500 * (1.25)^(t / 6)"},
            {"key": "D", "text": "P(t) = 10,000 * (4)^t"}
        ],
        "correct": "A",
        "explanation": "Boshlang'ich populyatsiya 2500 ga teng. 'Quadruples' so'zi har bir siklda 4 barobarga ko'payishini bildiradi (asos = 4). Ushbu to'rt baravar ortish har 6 soatda yuz berganligi sababli, daraja t / 6 bo'ladi. Funksiya: P(t) = 2500 * (4)^(t / 6). A variant to'g'ri. B variantida har soatda 4^6 ko'payish xatosi qilingan.",
        "strategy_or_hack": "⚡ SAT EXPONENTIAL MODEL: Boshlang'ich qiymat (2500) * (ko'payish koeffitsiyenti: 4)^(vaqt / davr: t/6).",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_18",
        "version": 1,
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Nonlinear functions (quadratic vertex/standard form, exponential models, polynomials)",
        "difficulty": "Hard",
        "status": "published",
        "passage": None,
        "question": "The function h is defined by h(x) = (x - 2)^2 * (x + 4). For how many distinct real values of x does the graph of y = h(x) cross or touch the x-axis?",
        "options": [
            {"key": "A", "text": "1"},
            {"key": "B", "text": "2"},
            {"key": "C", "text": "3"},
            {"key": "D", "text": "4"}
        ],
        "correct": "B",
        "explanation": "Funksiyaning x o'qi bilan kesishishi yoki urinishi h(x) = 0 bo'lganda ro'y beradi: (x - 2)^2 * (x + 4) = 0. Bu tenglamaning haqiqiy ildizlari x = 2 (karrali ildiz, grafik urinadi) va x = -4 (oddiy ildiz, grafik kesib o'tadi). Jami 2 ta turlicha haqiqiy qiymat mavjud. C variant (3) darajalar soni (ildizlar karraligi) bilan adashtirishdir.",
        "strategy_or_hack": "⚡ DESMOS HACK: Desmosga y = (x - 2)^2 * (x + 4) kiritilsa, grafik x o'qini faqat (-4, 0) va (2, 0) nuqtalarida kesishi/urinishi ko'rinadi (2 ta nuqta).",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },

    # ==================== PROBLEM-SOLVING AND DATA ANALYSIS (8 Questions) ====================
    {
        "id": "m_b5_19",
        "version": 1,
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Percentages (increase, decrease, markups, successive changes)",
        "difficulty": "Medium",
        "status": "published",
        "passage": None,
        "question": "An online electronics retailer discounted the price of a tablet by 20%. During a holiday flash sale, the retailer applied an additional 15% discount to the already reduced price. The final sale price was $272. What was the original price of the tablet before any discounts?",
        "options": [
            {"key": "A", "text": "$380"},
            {"key": "B", "text": "$400"},
            {"key": "C", "text": "$418"},
            {"key": "D", "text": "$425"}
        ],
        "correct": "B",
        "explanation": "Dastlabki narx P bo'lsin. 20% chegirmadan so'ng narx: P * (1 - 0.20) = 0.80P bo'ldi. Ikkinchi 15% chegirmadan so'ng: 0.80P * (1 - 0.15) = 0.80P * 0.85 = 0.68P bo'ldi. Yakuniy narx 0.68P = 272. Bundan P = 272 / 0.68 = $400 kelib chiqadi. 20% + 15% = 35% deb xato hisoblansa (272 / 0.65 = $418.46) C varianti tuzog'iga tushiladi.",
        "strategy_or_hack": "⚡ DESMOS HACK: 272 / (0.80 * 0.85) hisoblansa to'g'ridan-to'g'ri 400 chiqadi. Ketma-ket chegirmalarni hech qachon shunchaki qo'shmang!",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_20",
        "version": 1,
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Ratios, rates, proportional relationships, and unit conversion",
        "difficulty": "Easy",
        "status": "published",
        "passage": None,
        "question": "A commercial water pump discharges 45 gallons of water per minute. At this rate, how many hours will it take to pump out 8,100 gallons from a flooded reservoir?",
        "options": [
            {"key": "A", "text": "2.5"},
            {"key": "B", "text": "3.0"},
            {"key": "C", "text": "3.5"},
            {"key": "D", "text": "4.0"}
        ],
        "correct": "B",
        "explanation": "Dastlab umumiy sarflanadigan daqiqalarni topamiz: 8100 / 45 = 180 daqiqa. Daqiqalarni soatga aylantirish uchun 60 ga bo'lamiz: 180 / 60 = 3.0 soat. B variant to'g'ri.",
        "strategy_or_hack": "⚡ SAT STRATEGY: 8100 gallon / (45 gallon/min * 60 min/hour) = 8100 / 2700 = 3 soat.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_21",
        "version": 1,
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Probability and conditional probability from two-way tables",
        "difficulty": "Hard",
        "status": "published",
        "passage": None,
        "question": "The table below categorizes 180 college seniors by their major and career path intention:\n\nMajor | Graduate School | Industry Job | Total\nSTEM | 36 | 54 | 90\nHumanities | 24 | 26 | 50\nBusiness | 8 | 32 | 40\nTotal | 68 | 112 | 180\n\nIf a student is chosen at random from those who intend to enter an industry job, what is the probability that the student is a STEM major?",
        "options": [
            {"key": "A", "text": "54/180"},
            {"key": "B", "text": "54/112"},
            {"key": "C", "text": "54/90"},
            {"key": "D", "text": "90/180"}
        ],
        "correct": "B",
        "explanation": "Shartli ehtimollik: tanlov 'from those who intend to enter an industry job' guruhidan qilinmoqda, demak namuna fazosi (maxraj) jami Industry Job tanlaganlar soni = 112. Ular orasidan STEM mutaxassisligi bo'lganlar (surat) = 54. Ehtimollik: 54/112 (qisqartirganda 27/56). A variant (54/180) shartli ehtimollikni umumiy talabalar soniga bo'lish xatosidir.",
        "strategy_or_hack": "⚡ SAT STRATEGY: 'Given that' yoki 'from those who...' iborasidan keyingi guruh maxrajga qo'yiladi: maxraj = 112, surat = 54 -> 54/112.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_22",
        "version": 1,
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "One-variable data: distributions, mean, median, and spread",
        "difficulty": "Medium",
        "status": "published",
        "passage": None,
        "question": "A dataset consists of 9 distinct positive integers with a median of 45 and a mean of 50. If the largest number in the dataset, which is 88, is increased to 124, which of the following statements must be true about the updated dataset?",
        "options": [
            {"key": "A", "text": "Both the median and the mean will increase."},
            {"key": "B", "text": "The median will increase, but the mean will remain unchanged."},
            {"key": "C", "text": "The mean will increase, but the median will remain unchanged."},
            {"key": "D", "text": "Both the median and the mean will remain unchanged."}
        ],
        "correct": "C",
        "explanation": "To'plamda 9 ta son bor, mediana o'rtadagi 5-o'rindagi sondir (45). Eng katta son (9-o'rindagi son) 88 dan 124 ga oshirilsa, o'rtadagi 5-son (mediana) o'zgarmay qoladi (chunki 124 hali ham medianadan ancha katta). Biroq elementlar yig'indisi oshgani sababli, o'rtacha arifmetik (mean) ortadi. Shuning uchun C to'g'ri.",
        "strategy_or_hack": "⚡ SAT STRATEGY: Ekstremal qiymat (outlier) o'zgarganda o'rtacha qiymat (mean) darhol sezadi, mediana esa tartiblangan o'rinda barqaror qoladi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_23",
        "version": 1,
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Inference from sample statistics and margin of error",
        "difficulty": "Hard",
        "status": "published",
        "passage": None,
        "question": "A random sample of 600 voters in a metropolitan district showed that 54% support a municipal public transit initiative, with an associated margin of error of 4% at a 95% confidence level. Which of the following is the most appropriate conclusion?",
        "options": [
            {"key": "A", "text": "Exactly 54% of all voters in the district support the initiative."},
            {"key": "B", "text": "It is plausible that between 50% and 58% of all voters in the district support the initiative."},
            {"key": "C", "text": "The sample size was too small to draw any meaningful statistical inference."},
            {"key": "D", "text": "If a new sample of 600 voters is surveyed, exactly 54% of them will support the initiative."}
        ],
        "correct": "B",
        "explanation": "Ishonch oralig'i (confidence interval) = nuqtaviy baho +- xatolik chegarasi: 54% +- 4% = [50%, 58%]. Bu butun tuman saylovchilarining haqiqiy qo'llab-quvvatlash ulushi 50% dan 58% gacha bo'lishi ehtimoli yuqori (plausible) ekanini bildiradi. A va D variantlari deterministik ('exactly') noto'g'ri da'volardir.",
        "strategy_or_hack": "⚡ SAT STRATEGY: SAT statistikasida 'exactly' so'zi deyarli har doim xato bo'ladi. Ishonch oralig'i doimo oraliq ('between A% and B%') ifodasini talab qiladi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_24",
        "version": 1,
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Two-variable data: models and scatterplots",
        "difficulty": "Medium",
        "status": "published",
        "passage": None,
        "question": "A scatterplot displays the relationship between weekly advertising expenditure x, in hundreds of dollars, and weekly customer foot traffic y, in hundreds of visits. The line of best fit is given by y = 1.45x + 18.2. According to this model, what is the predicted weekly foot traffic, in visits, when advertising expenditure is $1,200?",
        "options": [
            {"key": "A", "text": "1,994 visits"},
            {"key": "B", "text": "3,560 visits"},
            {"key": "C", "text": "1,758 visits"},
            {"key": "D", "text": "3,280 visits"}
        ],
        "correct": "B",
        "explanation": "Birliklarga e'tibor beramiz: x 'hundreds of dollars'da o'lchanadi. Reklama xarajati $1,200 bo'lsa, x = 1200 / 100 = 12 bo'ladi. Tenglamaga qo'yamiz: y = 1.45(12) + 18.2 = 17.4 + 18.2 = 35.6. y ham 'hundreds of visits'da o'lchanganligi uchun tashriflar soni: 35.6 * 100 = 3,560 ta tashrif bo'ladi. B variant to'g'ri.",
        "strategy_or_hack": "⚡ SAT STRATEGY: Birlik masshtabi tuzog'i! $1,200 -> x = 12; natija y = 35.6 -> 35.6 * 100 = 3,560 visits.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_25",
        "version": 1,
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Ratios, rates, proportional relationships, and unit conversion",
        "difficulty": "Hard",
        "status": "published",
        "passage": None,
        "question": "An artisan ceramicist mixes two clay compounds. Compound A contains 18% kaolin by weight, and Compound B contains 42% kaolin by weight. The artisan wants to create a 60-kilogram mixture that contains exactly 34% kaolin by weight. How many kilograms of Compound B should be used?",
        "options": [
            {"key": "A", "text": "20"},
            {"key": "B", "text": "35"},
            {"key": "C", "text": "40"},
            {"key": "D", "text": "45"}
        ],
        "correct": "C",
        "explanation": "Compound B og'irligi x kg bo'lsin, shunda Compound A og'irligi 60 - x kg bo'ladi. Kaolin miqdori bo'yicha tenglama: 0.18(60 - x) + 0.42x = 0.34(60). Qavslarni ochamiz: 10.8 - 0.18x + 0.42x = 20.4 => 0.24x = 20.4 - 10.8 = 9.6 => x = 9.6 / 0.24 = 40 kg. Demak, 40 kg Compound B va 20 kg Compound A kerak. C variant to'g'ri.",
        "strategy_or_hack": "⚡ DESMOS HACK: Desmosga 0.18(60 - x) + 0.42x = 0.34 * 60 deb yozing. To'g'ri chiziq x = 40 da hosil bo'ladi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_26",
        "version": 1,
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Percentages (increase, decrease, markups, successive changes)",
        "difficulty": "Easy",
        "status": "published",
        "passage": None,
        "question": "In a municipal botanical greenhouse, the number of exotic orchid varieties increased from 160 to 208 over a three-year period. What was the percentage increase in the number of orchid varieties?",
        "options": [
            {"key": "A", "text": "23%"},
            {"key": "B", "text": "30%"},
            {"key": "C", "text": "35%"},
            {"key": "D", "text": "48%"}
        ],
        "correct": "B",
        "explanation": "Foiz oshishi formulasi: (Yangi - Eski) / Eski * 100% = (208 - 160) / 160 * 100% = 48 / 160 * 100% = 0.30 * 100% = 30%. D variant (48%) mutlaq sonni (48 ta) foiz bilan adashtirish natijasidir.",
        "strategy_or_hack": "⚡ DESMOS HACK: (208 - 160) / 160 hisoblansa darhol 0.30 = 30% chiqadi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },

    # ==================== GEOMETRY AND TRIGONOMETRY (8 Questions) ====================
    {
        "id": "m_b5_27",
        "version": 1,
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Right triangle trigonometry (sine, cosine, tangent, complementary angles)",
        "difficulty": "Medium",
        "status": "published",
        "passage": None,
        "question": "A surveyor stands 120 feet away from the base of a vertical communications tower on level ground. The angle of elevation from the surveyor's transit instrument, which is mounted 5 feet above ground level, to the top of the tower is 35 degrees. Which of the following expressions represents the total height of the tower, in feet?",
        "options": [
            {"key": "A", "text": "120 * sin(35°) + 5"},
            {"key": "B", "text": "120 * tan(35°) + 5"},
            {"key": "C", "text": "120 / tan(35°) + 5"},
            {"key": "D", "text": "125 * tan(35°)"}
        ],
        "correct": "B",
        "explanation": "Asbob balandligidan minora cho'qqisigacha bo'lgan to'g'ri burchakli uchburchakda: yondosh katet = 120 fut, burchak = 35°. Qarama-qarshi katet h_top bo'lsa: tan(35°) = h_top / 120 => h_top = 120 * tan(35°). Minoraning umumiy balandligi yer sathidan hisoblangani uchun asbobning 5 fut balandligini qo'shamiz: H = 120 * tan(35°) + 5. B variant to'g'ri.",
        "strategy_or_hack": "⚡ SAT TRIGONOMETRY HACK: tan(theta) = qarshi / yondosh. h_top = 120 * tan(35°); yer sathiga nisbatan +5 fut qo'shiladi -> B.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_28",
        "version": 1,
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Circles (equations, radius, arc length, sector area)",
        "difficulty": "Hard",
        "status": "published",
        "passage": None,
        "question": "A circle in the xy-plane has its center at the origin (0, 0). A line segment with length 16 is a chord of the circle. If the distance from the origin to the midpoint of this chord is 6, what is the area of the circle?",
        "options": [
            {"key": "A", "text": "64*pi"},
            {"key": "B", "text": "100*pi"},
            {"key": "C", "text": "136*pi"},
            {"key": "D", "text": "256*pi"}
        ],
        "correct": "B",
        "explanation": "Markazdan vatarning o'rtasigacha bo'lgan masofa vatarga perpendikulyar bo'ladi va to'g'ri burchakli uchburchak hosil qiladi. Uchburchak katetlari: markazdan masofa d = 6 va vatar yarmi = 16 / 2 = 8. Gipotenuza aylananing radiusi r bo'ladi: r^2 = 6^2 + 8^2 = 36 + 64 = 100. Aylana yuzi: S = pi * r^2 = 100*pi. B variant to'g'ri.",
        "strategy_or_hack": "⚡ SAT GEOMETRY TRAP: 6-8-10 to'g'ri burchakli uchburchak! Radius r = 10 bo'ladi. Doira yuzi: pi * 10^2 = 100*pi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_29",
        "version": 1,
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Circles (equations, radius, arc length, sector area)",
        "difficulty": "Medium",
        "status": "published",
        "passage": None,
        "question": "A circle has a radius of 18 centimeters. What is the area, in square centimeters, of a sector formed by a central angle measuring 80 degrees?",
        "options": [
            {"key": "A", "text": "36*pi"},
            {"key": "B", "text": "72*pi"},
            {"key": "C", "text": "144*pi"},
            {"key": "D", "text": "324*pi"}
        ],
        "correct": "B",
        "explanation": "Doira sektori yuzi formulasi: S = (theta / 360) * pi * r^2. Berilgan: theta = 80°, r = 18. S = (80 / 360) * pi * (18)^2 = (2 / 9) * pi * 324 = 2 * 36 * pi = 72*pi sm^2. A variant (36*pi) yoy uzunligi bilan aralashtirish xatosi.",
        "strategy_or_hack": "⚡ DESMOS HACK: (80 / 360) * 18^2 = 72. Natija darhol 72*pi ekanligi ko'rinadi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_30",
        "version": 1,
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Area and volume formulas (circles, cylinders, prisms)",
        "difficulty": "Hard",
        "status": "published",
        "passage": None,
        "question": "Two right circular cylinders, Cylinder X and Cylinder Y, are mathematically similar. The height of Cylinder Y is 3 times the height of Cylinder X. If the volume of Cylinder X is 24 cubic inches, what is the volume of Cylinder Y, in cubic inches?",
        "options": [
            {"key": "A", "text": "72"},
            {"key": "B", "text": "216"},
            {"key": "C", "text": "648"},
            {"key": "D", "text": "1,728"}
        ],
        "correct": "C",
        "explanation": "O'xshash uch o'lchamli geometrik jismlar uchun chiziqli o'lchamlar nisbati k bo'lsa, ularning hajmlari nisbati k^3 bo'ladi. Bu yerda balandliklar nisbati k = 3. Shuning uchun hajmlar nisbati k^3 = 3^3 = 27. Cylinder Y hajmi: V_Y = 24 * 27 = 648 kub dyuym. A variant (72) faqat 24 * 3 ni hisoblash (chiziqli nisbat xatosi) natijasidir.",
        "strategy_or_hack": "⚡ SAT GEOMETRY TRAP: Chiziqli nisbat = k; Yuza nisbati = k^2; Hajm nisbati = k^3! 24 * 3^3 = 24 * 27 = 648.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_31",
        "version": 1,
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Lines, angles, and triangles (congruence, similarity, Pythagorean theorem, special triangles)",
        "difficulty": "Easy",
        "status": "published",
        "passage": None,
        "question": "In triangle PQR, the measure of angle P is 48 degrees and the measure of angle Q is 74 degrees. What is the measure of the exterior angle at vertex R?",
        "options": [
            {"key": "A", "text": "58 degrees"},
            {"key": "B", "text": "112 degrees"},
            {"key": "C", "text": "122 degrees"},
            {"key": "D", "text": "132 degrees"}
        ],
        "correct": "C",
        "explanation": "Uchburchak tashqi burchagi xossasiga ko'ra, har qanday cho'qqidagi tashqi burchak o'ziga qo'shni bo'lmagan ikkita ichki burchak yig'indisiga teng: Ext_R = Angle_P + Angle_Q = 48° + 74° = 122°. Shu bilan birga, ichki burchak R = 180° - (48° + 74°) = 180° - 122° = 58° (A varianti bu ichki burchak). Tashqi burchak: 180° - 58° = 122°.",
        "strategy_or_hack": "⚡ SAT STRATEGY: Tashqi burchak teoremasi: Ext = P + Q = 48 + 74 = 122°. Bir qadamda topiladi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_32",
        "version": 1,
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Lines, angles, and triangles (congruence, similarity, Pythagorean theorem, special triangles)",
        "difficulty": "Medium",
        "status": "published",
        "passage": None,
        "question": "A 26-foot extension ladder leans against the vertical exterior wall of a building. The base of the ladder is placed 10 feet away from the wall on level ground. How many feet up the wall does the top of the ladder reach?",
        "options": [
            {"key": "A", "text": "20"},
            {"key": "B", "text": "24"},
            {"key": "C", "text": "25"},
            {"key": "D", "text": "28"}
        ],
        "correct": "B",
        "explanation": "Zina, devor va yer to'g'ri burchakli uchburchak hosil qiladi. Pifagor teoremasi bo'yicha: a^2 + b^2 = c^2, bu yerda gipotenuza c = 26 fut, katet a = 10 fut. b^2 = 26^2 - 10^2 = 676 - 100 = 576. b = sqrt(576) = 24 fut. (Bu 5-12-13 Pifagor uchligining 2 ga ko'paytirilgan shakli: 10-24-26).",
        "strategy_or_hack": "⚡ DESMOS HACK: sqrt(26^2 - 10^2) = 24. Pifagor uchliklarini eslab qoling: 5-12-13 -> 10-24-26.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_33",
        "version": 1,
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Right triangle trigonometry (sine, cosine, tangent, complementary angles)",
        "difficulty": "Hard",
        "status": "published",
        "passage": None,
        "question": "In right triangle DEF, angle F is the right angle, and tan(D) = 15/8. What is the value of sin(D)?",
        "options": [
            {"key": "A", "text": "8/17"},
            {"key": "B", "text": "15/17"},
            {"key": "C", "text": "8/15"},
            {"key": "D", "text": "17/15"}
        ],
        "correct": "B",
        "explanation": "tan(D) = qarshisidagi katet / yondosh katet = 15/8. Gipotenuzani Pifagor teoremasi orqali topamiz: c = sqrt(15^2 + 8^2) = sqrt(225 + 64) = sqrt(289) = 17. (8-15-17 mashhur Pifagor uchligi). sin(D) = qarshisidagi katet / gipotenuza = 15/17. A variant (8/17) cos(D) qiymatidir.",
        "strategy_or_hack": "⚡ SAT STRATEGY: 8-15-17 uchburchagini yodda saqlang. tan = 15/8 -> gipotenuza = 17. sin = qarama-qarshi / gipotenuza = 15/17.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "m_b5_34",
        "version": 1,
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Area and volume formulas (circles, cylinders, prisms)",
        "difficulty": "Medium",
        "status": "published",
        "passage": None,
        "question": "A solid rectangular storage container has a base with length 14 meters and width 8 meters. If the total volume of the container is 504 cubic meters, what is the height of the container, in meters?",
        "options": [
            {"key": "A", "text": "4.5"},
            {"key": "B", "text": "5.0"},
            {"key": "C", "text": "6.0"},
            {"key": "D", "text": "7.5"}
        ],
        "correct": "A",
        "explanation": "To'g'ri to'rtburchakli parallelepiped hajmi: V = l * w * h. Berilgan: V = 504, l = 14, w = 8. Asos yuzi: 14 * 8 = 112 m^2. Balandlik: h = 504 / 112 = 4.5 metr. A variant to'g'ri.",
        "strategy_or_hack": "⚡ DESMOS HACK: 504 / (14 * 8) hisoblansa 4.5 chiqadi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    }
]
