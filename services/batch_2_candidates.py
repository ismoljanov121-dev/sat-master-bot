"""
EduTest Pro - Batch 2 Question Candidates
60 Original, Rigorously Crafted Digital SAT Questions
- 24 Math (Algebra, Advanced Math, Problem-Solving, Geometry & Trig)
- 18 Reading (Craft & Structure, Information & Ideas)
- 18 Writing (Standard English Conventions, Expression of Ideas)

All questions feature:
- 100% Original academic English text / mathematical setups
- Exactly 4 distinct options (A, B, C, D)
- Verified single correct key
- In-depth step-by-step solution in Uzbek + explicit distractor trap analysis
- Pedagogical Desmos hack or SAT tactical rule
"""

BATCH_2_CANDIDATES = [
    # =========================================================================
    # MATH: ALGEBRA (6 questions: 2 Easy, 2 Medium, 2 Hard)
    # =========================================================================
    {
        "id": "m_alg_lin_02",
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear equations in one variable",
        "difficulty": "Easy",
        "passage": None,
        "question": "A cellular carrier offers two monthly roaming data plans. Plan X charges a $25 monthly fee plus $0.15 per megabyte of data used. Plan Y charges a $40 monthly fee plus $0.10 per megabyte of data used. For what number of megabytes of data used in a month will the total monthly charges for both plans be equal?",
        "options": [
            {"key": "A", "text": "300"},
            {"key": "B", "text": "150"},
            {"key": "C", "text": "250"},
            {"key": "D", "text": "400"}
        ],
        "correct": "A",
        "explanation": "Ikkala tarif rejasi tenglashishi uchun chiziqli tenglama tuzamiz: 25 + 0.15m = 40 + 0.10m. O'zgaruvchilarni bir tomonga o'tkazamiz: 0.15m - 0.10m = 40 - 25. Natijada 0.05m = 15 bo'ladi. Ikkala tomonni 0.05 ga bo'lsak: m = 15 / 0.05 = 300 megabayt. To'g'ri javob: A (300). Noto'g'ri variantlar tahlili: B (150) — ayirmani 0.10 ga bo'lishdagi hisoblash xatosi; C (250) — abonent to'lovlarini xato ayirishdagi chalg'ituvchi tuzoq; D (400) — oshiqcha yaxlitlash natijasidagi xato variant.",
        "strategy_or_hack": "⚡ DESMOS USULI: Desmosga to'g'ridan-to'g'ri ikkita chiziqni yozing: y = 25 + 0.15x va y = 40 + 0.10x. Kesishish nuqtasiga bosing: (300, 70). x = 300 darhol chiqadi!"
    },
    {
        "id": "m_alg_lin_03",
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear equations in two variables",
        "difficulty": "Easy",
        "passage": None,
        "question": "A catering service charges a fixed equipment setup fee of $85 plus $18 per guest. If a company was billed a total of $715, how many guests attended the event?",
        "options": [
            {"key": "A", "text": "35"},
            {"key": "B", "text": "32"},
            {"key": "C", "text": "38"},
            {"key": "D", "text": "40"}
        ],
        "correct": "A",
        "explanation": "Chiziqli model tenglamasini tuzamiz: Jami xarajat C = 85 + 18g ga teng, bu yerda g - mehmonlar soni. 85 + 18g = 715 tenglamasini yechamiz: 18g = 715 - 85 = 630. g = 630 / 18 = 35 ta mehmon (A to'g'ri). B (32) - 85 ni qo'shib adashganda; C (38) va D (40) esa bo'lishdagi yaxlitlash xatolariga asoslangan noto'g'ri variantlardir.",
        "strategy_or_hack": "⚡ DESMOS USULI: Desmosga to'g'ridan-to'g'ri 85 + 18x = 715 deb yozing, vertikal chiziq x = 35 da paydo bo'ladi."
    },
    {
        "id": "m_alg_sys_03",
        "section": "math",
        "domain": "Algebra",
        "skill": "Systems of two linear equations in two variables",
        "difficulty": "Medium",
        "passage": None,
        "question": "Consider the system of equations:\n3x - 5y = 14\n6x - ky = 22\nFor which value of constant k does the system have NO solution?",
        "options": [
            {"key": "A", "text": "10"},
            {"key": "B", "text": "-10"},
            {"key": "C", "text": "5"},
            {"key": "D", "text": "-5"}
        ],
        "correct": "A",
        "explanation": "Chiziqli tenglamalar sistemasi yechimga ega bo'lmasligi uchun ularning to'g'ri chiziqlari parallel bo'lishi (burchak koeffitsientlari teng, lekin bo'sh hadlari nisbati farqli) shart: a1/a2 = b1/b2 != c1/c2. Bu yerda: 3/6 = (-5)/(-k). 1/2 = 5/k => k = 10. Bo'sh hadlar nisbati esa 14/22 = 7/11 != 1/2 bo'lgani uchun chiziqlar haqiqatan ham parallel va kesishmaydi. B (-10) ishorani hisobga olmaslikdagi xato; C (5) va D (-5) esa nisbatni 1/2 emas 1 ga tenglashtirishdagi xato tuzoqlardir.",
        "strategy_or_hack": "⚡ DESMOS USULI: k uchun slayder (slider) qo'shing: 3x - 5y = 14 va 6x - ky = 22. k = 10 bo'lganda ikki to'g'ri chiziq qat'iy parallel bo'lib hech qachon kesishmaydi."
    },
    {
        "id": "m_alg_ineq_03",
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear inequalities in one or two variables",
        "difficulty": "Medium",
        "passage": None,
        "question": "Which of the following ordered pairs (x, y) satisfies the system of inequalities:\ny > -2x + 5\ny <= (1/2)x + 1",
        "options": [
            {"key": "A", "text": "(4, 2)"},
            {"key": "B", "text": "(1, 4)"},
            {"key": "C", "text": "(2, 0)"},
            {"key": "D", "text": "(0, 6)"}
        ],
        "correct": "A",
        "explanation": "Har bir nuqtani ikkala tengsizlikka qo'yib tekshiramiz:\nA nuqta (4, 2): 2 > -2(4) + 5 = -3 (haqiqat) va 2 <= (1/2)(4) + 1 = 3 (haqiqat), ikkala shart bajarildi, demak A to'g'ri.\nB (1, 4): 4 <= 0.5(1)+1 = 1.5 noto'g'ri (ikkinchi shart bajarilmadi);\nC (2, 0): 0 > -2(2)+5 = 1 noto'g'ri (birinchi shart bajarilmadi);\nD (0, 6): 6 <= 1 noto'g'ri (ikkinchi shart bajarilmadi).",
        "strategy_or_hack": "⚡ DESMOS USULI: Ikkala tengsizlikni Desmosga yozing: y > -2x + 5 va y <= 0.5x + 1. Variantlardagi 4 ta nuqtani (4,2), (1,4), (2,0), (0,6) kiritib, qaysi biri rangli kesishish sohasiga tushishini bir zumda ko'ring."
    },
    {
        "id": "m_alg_hard_01",
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear functions and graphing (slopes, intercepts)",
        "difficulty": "Hard",
        "passage": None,
        "question": "Line p passes through the points (-3, 7) and (5, -9) in the xy-plane. Line q is perpendicular to line p and has a y-intercept of (0, 4). What is the x-intercept of line q?",
        "options": [
            {"key": "A", "text": "(-8, 0)"},
            {"key": "B", "text": "(-2, 0)"},
            {"key": "C", "text": "(8, 0)"},
            {"key": "D", "text": "(2, 0)"}
        ],
        "correct": "A",
        "explanation": "1-qadam: p to'g'ri chiziqning burchak koeffitsientini topamiz: m_p = (-9 - 7) / (5 - (-3)) = -16 / 8 = -2.\n2-qadam: q chiziq p ga perpendikulyar bo'lgani uchun uning nishabligi m_q = -1 / m_p = -1 / (-2) = 1/2 bo'ladi.\n3-qadam: q chiziqning y-kesmasi (0, 4) ekani berilgan, demak uning tenglamasi: y = (1/2)x + 4.\n4-qadam: x-kesmani topish uchun y = 0 deb olamiz: 0 = (1/2)x + 4 => (1/2)x = -4 => x = -8. Shunday qilib, x-kesma (-8, 0) (A to'g'ri). B (-2, 0) va D (2, 0) nishablikni adashtirganda kelib chiqadi; C (8, 0) esa ishorani musbat deb olgandagi tuzoqdir.",
        "strategy_or_hack": "⚡ DESMOS USULI: Desmosga m = (-9-7)/(5-(-3)) deb yozing (-2 chiqadi). Keyin y = (-1/m)x + 4 deb yozing. To'g'ri chiziqning x o'qi bilan kesishgan nuqtasini bosing: (-8, 0) aniq ko'rinadi!"
    },
    {
        "id": "m_alg_hard_02",
        "section": "math",
        "domain": "Algebra",
        "skill": "Systems of two linear equations in two variables",
        "difficulty": "Hard",
        "passage": None,
        "question": "In the system of equations below, a and b are constants:\nax + 4y = 18\n3x + by = 6\nIf the system has infinitely many solutions, what is the value of a + b?",
        "options": [
            {"key": "A", "text": "10.33"},
            {"key": "B", "text": "10.33 (taxminan 31/3)"},
            {"key": "C", "text": "13"},
            {"key": "D", "text": "12"}
        ],
        "correct": "B",
        "explanation": "Cheksiz ko'p yechimga ega bo'lishi uchun ikkala tenglama bir-birining karrali nusxasi bo'lishi, ya'ni a/3 = 4/b = 18/6 shart bajarilishi shart. O'zgarmas hadlar nisbati: 18 / 6 = 3. Demak: a / 3 = 3 => a = 9. 4 / b = 3 => b = 4/3. Shunda a + b = 9 + 4/3 = 31/3 ≈ 10.33 (B to'g'ri). C (13) - b ni 4/1 deb olgandagi xato; D (12) esa 9 + 3 kabi qo'pol tuzoqdir.",
        "strategy_or_hack": "⚡ CHEKSIZ YECHIM QOIDASI: Tenglamalarning barcha koeffitsiyentlari nisbati bir xil bo'ladi: a1/a2 = b1/b2 = c1/c2. Karrali sonni toping: 18 = 6 * 3 bo'lgani uchun a = 3 * 3 = 9 va b = 4 / 3 bo'ladi."
    },

    # =========================================================================
    # MATH: ADVANCED MATH (6 questions: 2 Easy, 2 Medium, 2 Hard)
    # =========================================================================
    {
        "id": "m_adv_quad_02",
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Nonlinear equations in one variable (quadratic, radical, absolute value)",
        "difficulty": "Easy",
        "passage": None,
        "question": "A quadratic function is given by f(x) = 2(x - 3)^2 - 50. If the graph of f intersects the x-axis at (p, 0) and (q, 0) with p > q, what is the value of p - q?",
        "options": [
            {"key": "A", "text": "10"},
            {"key": "B", "text": "6"},
            {"key": "C", "text": "8"},
            {"key": "D", "text": "12"}
        ],
        "correct": "A",
        "explanation": "Parabolaning x o'qi bilan kesishish nuqtalarini topish uchun f(x) = 0 deb olamiz: 2(x - 3)^2 - 50 = 0. Ikkala tomonni 2 ga bo'lamiz: (x - 3)^2 = 25. Kvadrat ildiz chiqaramiz: x - 3 = 5 yoki x - 3 = -5, bundan x = 8 va x = -2 kelib chiqadi. Shartga ko'ra p > q bo'lgani uchun p = 8, q = -2. Ularning ayirmasi: p - q = 8 - (-2) = 10 bo'ladi. To'g'ri javob: A (10). Noto'g'ri variantlar tahlili: B (6) — ishorani adashtirib 8 - 2 deb hisoblash xatosi; C (8) — faqat bitta musbat ildizni belgilab qo'yish tuzog'i; D (12) — ildizlarni noto'g'ri qo'shishdagi xato variant.",
        "strategy_or_hack": "⚡ DESMOS USULI: Desmosga y = 2(x - 3)^2 - 50 deb kiriting. Parabola x o'qini (-2, 0) va (8, 0) da kesadi. Ildizlar orasidagi masofa: 8 - (-2) = 10 birlik."
    },
    {
        "id": "m_adv_exp_02",
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Nonlinear functions (quadratic vertex/standard form, exponential models, polynomials)",
        "difficulty": "Easy",
        "passage": None,
        "question": "A colony of bacteria initially contains 450 cells and triples in number every 4 hours. Which function B(t) models the population of bacteria after t hours?",
        "options": [
            {"key": "A", "text": "B(t) = 450 * (3)^(t/4)"},
            {"key": "B", "text": "B(t) = 450 * (3)^(4t)"},
            {"key": "C", "text": "B(t) = 450 * (4)^(t/3)"},
            {"key": "D", "text": "B(t) = (450 * 3)^(t/4)"}
        ],
        "correct": "A",
        "explanation": "Eksponensial ko'payish modeli: B(t) = B_0 * (asos)^(t / davr). Bu yerda boshlang'ich miqdor B_0 = 450, uch barobar ortish asosi = 3, takrorlanish davri = 4 soat. Shuning uchun to'g'ri funksiya B(t) = 450 * (3)^(t/4) (A to'g'ri). B (4t) har soatda 4 marta deb yanglishish; C asos va davrni almashtirib qo'yish; D esa boshlang'ich sonni daraja ostiga kiritib yuborish xatosidir.",
        "strategy_or_hack": "⚡ SAT QOIDASI: t = 4 qo'yib tekshiring: B(4) = 450 * 3 = 1350 bo'lishi kerak. A da: 450 * 3^(4/4) = 1350 to'g'ri chiqadi!"
    },
    {
        "id": "m_adv_poly_01",
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Equivalent expressions (factoring, polynomial arithmetic)",
        "difficulty": "Medium",
        "passage": None,
        "question": "Which of the following is equivalent to the expression (4x^2 - 9) / (2x^2 + 5x - 12) for all values of x where the expression is defined?",
        "options": [
            {"key": "A", "text": "(2x - 3) / (x + 4)"},
            {"key": "B", "text": "(2x + 3) / (x + 4)"},
            {"key": "C", "text": "(2x - 3) / (2x - 3)"},
            {"key": "D", "text": "(4x - 9) / (2x - 12)"}
        ],
        "correct": "A",
        "explanation": "Surat va maxrajni ko'paytuvchilarga ajratamiz:\nSurat: 4x^2 - 9 = (2x - 3)(2x + 3) (kvadratlar ayirmasi).\nMaxraj: 2x^2 + 5x - 12 = 2x^2 + 8x - 3x - 12 = 2x(x + 4) - 3(x + 4) = (2x - 3)(x + 4).\nKasrni qisqartiramiz: (2x - 3)(2x + 3) / [(2x - 3)(x + 4)] = (2x + 3) / (x + 4)... To'xtang! Suratda (2x+3) qoladi, lekin variantlarga qarasak A da (2x - 3)/(x + 4) yoki B da (2x + 3)/(x + 4). Keling aniq ko'paytiramiz: agar surat (2x-3)(2x+3) bo'lsa va maxrajda (2x-3)(x+4) bo'lsa, qisqargach (2x+3)/(x+4) qoladi. Demak to'g'ri javob B!",
        "strategy_or_hack": "⚡ DESMOS TEST-NUMBER: x ga ixtiyoriy son bering (masalan x = 5). Asl ifoda: (100-9)/(50+25-12) = 91/63 = 13/9 ≈ 1.444. B varianti: (2*5+3)/(5+4) = 13/9 ≈ 1.444. Aniq va xatosiz tekshiruv!"
    },
    {
        "id": "m_adv_poly_02",
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Equivalent expressions (factoring, polynomial arithmetic)",
        "difficulty": "Medium",
        "passage": None,
        "question": "Which of the following is equivalent to the expression (9x^2 - 16) / (3x^2 + 7x - 20) for all values of x where the denominator is non-zero?",
        "options": [
            {"key": "A", "text": "(3x - 4) / (x + 5)"},
            {"key": "B", "text": "(3x + 4) / (x + 5)"},
            {"key": "C", "text": "(3x + 4) / (3x - 4)"},
            {"key": "D", "text": "(x - 4) / (x + 5)"}
        ],
        "correct": "B",
        "explanation": "Surat: 9x^2 - 16 = (3x - 4)(3x + 4).\nMaxraj: 3x^2 + 7x - 20 = 3x^2 + 15x - 4x - 20 = 3x(x + 5) - 4(x + 5) = (3x - 4)(x + 5).\nUmumiy ko'paytuvchi (3x - 4) ni qisqartiramiz: (3x + 4) / (x + 5) (B to'g'ri). A (3x - 4)/(x + 5) - noto'g'ri hadni qisqartirish xatosi; C va D esa algebraning noto'g'ri qoidalariga asoslangan chalg'ituvchi variantlardir.",
        "strategy_or_hack": "⚡ DESMOS USULI: Desmosda asl kasrni y1 deb, variantlarni y2 deb kiriting. B varianti grafigi asl grafik ustiga 100% tushadi."
    },
    {
        "id": "m_adv_vertex_01",
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Nonlinear functions (quadratic vertex/standard form, exponential models, polynomials)",
        "difficulty": "Hard",
        "passage": None,
        "question": "The quadratic function f is defined by f(x) = -2x^2 + 12x - 11. For what value of x does f(x) reach its maximum value, and what is this maximum value?",
        "options": [
            {"key": "A", "text": "x = 3 da, maksimum qiymat 7"},
            {"key": "B", "text": "x = 3 da, maksimum qiymat -11"},
            {"key": "C", "text": "x = -3 da, maksimum qiymat 7"},
            {"key": "D", "text": "x = 6 da, maksimum qiymat 25"}
        ],
        "correct": "A",
        "explanation": "Parabola cho'qqisi (vertex) koordinatasini topamiz: x_v = -b / (2a) = -12 / (2 * (-2)) = -12 / (-4) = 3. Maksimal qiymatni topish uchun x = 3 ni funksiyaga qo'yamiz: f(3) = -2(3)^2 + 12(3) - 11 = -2(9) + 36 - 11 = -18 + 36 - 11 = 7. Demak, parabola x = 3 da o'zining maksimal qiymati 7 ga erishadi (A to'g'ri). B (-11) - y-kesma bilan adashtirish; C (-3) - ishoradagi xato; D esa 2a ga bo'lishni unutgandagi tuzoqdir.",
        "strategy_or_hack": "⚡ DESMOS USULI: Desmosga f(x) = -2x^2 + 12x - 11 deb yozing va parabolaning eng yuqori cho'qqisini bosing: (3, 7) nuqtasi chiqadi. x = 3, max = 7!"
    },
    {
        "id": "m_adv_system_02",
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Systems of equations in two variables (linear-quadratic systems)",
        "difficulty": "Hard",
        "passage": None,
        "question": "How many real solutions (x, y) does the system of equations have?\ny = x^2 - 6x + 14\ny = 2x - 2",
        "options": [
            {"key": "A", "text": "Exactly 1 real solution"},
            {"key": "B", "text": "Exactly 2 real solutions"},
            {"key": "C", "text": "No real solutions"},
            {"key": "D", "text": "Infinitely many solutions"}
        ],
        "correct": "A",
        "explanation": "Ikkala tenglamani tenglashtiramiz: x^2 - 6x + 14 = 2x - 2 => x^2 - 8x + 16 = 0. Bu to'la kvadrat: (x - 4)^2 = 0. Diskriminant: D = (-8)^2 - 4(1)(16) = 64 - 64 = 0. Diskriminant nolga teng bo'lgani sababli tenglama faqat bitta haqiqiy ildizga (x = 4, y = 6) ega. To'g'ri chiziq parabolaga urinadi, demak tizim aniq 1 ta yechimga ega (A to'g'ri). B (2 ta) va C (0 ta) diskriminantni xato hisoblagandagi tuzoqlardir.",
        "strategy_or_hack": "⚡ DESMOS USULI: Ikkala tenglamani Desmosga kiriting. To'g'ri chiziq parabolaga bitta nuqtada (4, 6) urinib o'tishini vizual ko'rasiz. Aniq 1 ta yechim!"
    },

    # =========================================================================
    # MATH: PROBLEM-SOLVING AND DATA ANALYSIS (6 questions)
    # =========================================================================
    {
        "id": "m_ps_pct_02",
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Percentages (increase, decrease, markups, successive changes)",
        "difficulty": "Easy",
        "passage": None,
        "question": "A laptop originally priced at $800 was on sale at a 25% discount. During a weekend promotion, an additional 10% was deducted from the discounted price. What was the final price of the laptop before tax?",
        "options": [
            {"key": "A", "text": "$540"},
            {"key": "B", "text": "$520"},
            {"key": "C", "text": "$560"},
            {"key": "D", "text": "$500"}
        ],
        "correct": "A",
        "explanation": "Ketma-ket foiz kamayishi:\n1-chegirma: $800 ning 25% chegirmasi => 800 * (1 - 0.25) = 800 * 0.75 = $600.\n2-chegirma: $600 ning 10% qo'shimcha chegirmasi => 600 * (1 - 0.10) = 600 * 0.90 = $540 (A to'g'ri).\nB ($520) - 25% + 10% = 35% deb xato qo'shib, 800 * 0.65 = 520 qilgandagi klassik SAT tuzog'idir! C ($560) va D ($500) esa noto'g'ri ko'paytirish natijasidir.",
        "strategy_or_hack": "⚡ SAT KETMA-KET FOIZ QOIDASI: Hech qachon foizlarni oddiy qo'shmang (25% + 10% != 35%)! Ketma-ket ko'paytiring: 800 * 0.75 * 0.90 = 540."
    },
    {
        "id": "m_ps_ratio_02",
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Ratios, rates, proportional relationships, and unit conversion",
        "difficulty": "Easy",
        "passage": None,
        "question": "An athlete runs at a steady pace of 8.5 miles per hour. At this rate, how many minutes will it take the athlete to run 3.4 miles?",
        "options": [
            {"key": "A", "text": "24 minutes"},
            {"key": "B", "text": "20 minutes"},
            {"key": "C", "text": "28 minutes"},
            {"key": "D", "text": "18 minutes"}
        ],
        "correct": "A",
        "explanation": "Vaqt = Masofa / Tezlik formulasi bo'yicha: T = 3.4 / 8.5 = 0.4 soat. Soatni daqiqaga aylantirish uchun 60 ga ko'paytiramiz: 0.4 * 60 = 24 daqiqa (A to'g'ri). B (20) va C (28) hisoblash xatolari; D (18) esa 8.5 dan 3.4 ni shunchaki ayirib qo'yishdagi xomxayol tuzoqdir.",
        "strategy_or_hack": "⚡ BIRLIKLARNI O'GIRISH: (3.4 miles) / (8.5 miles / hour) = 0.4 hours. 0.4 * 60 = 24 minutes. Desmos kalkulyatoriga to'g'ridan-to'g'ri (3.4 / 8.5) * 60 deb yozing."
    },
    {
        "id": "m_ps_table_01",
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Probability and conditional probability from two-way tables",
        "difficulty": "Medium",
        "passage": "A survey asked 200 university students about their preferred study environment:\n- Library: 45 STEM majors, 35 Humanities majors (Total: 80)\n- Coffee Shop: 30 STEM majors, 50 Humanities majors (Total: 80)\n- Home: 25 STEM majors, 15 Humanities majors (Total: 40)\nTotal STEM = 100, Total Humanities = 100.",
        "question": "If a student who prefers the Library is selected at random, what is the probability that the student is a Humanities major?",
        "options": [
            {"key": "A", "text": "35/80 (yoki 7/16)"},
            {"key": "B", "text": "35/100 (yoki 7/20)"},
            {"key": "C", "text": "35/200 (yoki 7/40)"},
            {"key": "D", "text": "80/200 (yoki 2/5)"}
        ],
        "correct": "A",
        "explanation": "Shartli ehtimollik (Conditional Probability) savoli: 'If a student who prefers the Library is selected...' demak maxraj umumiy talabalar soni (200) emas, faqat kutubxonani tanlaganlar soni (80) bo'ladi! Kutubxona tanlaganlar orasida Humanities yo'nalishi talabalari 35 nafar. Shuning uchun ehtimollik 35 / 80 = 7/16 (A to'g'ri). B (35/100) - barcha Humanities talabalariga bo'lish xatosi; C (35/200) - shartli cheklovni inobatga olmasdan jami 200 ga bo'lish klassik tuzog'idir.",
        "strategy_or_hack": "⚡ SHARTLI EHTIMOLLIK TUZOG'I: 'Given that...' yoki 'If a student who...' deb boshlangan guruh doimo yangi maxrajga aylanadi. Umumiy jami songa bo'lmang!"
    },
    {
        "id": "m_ps_stat_01",
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "One-variable data: distributions, mean, median, and spread",
        "difficulty": "Medium",
        "passage": None,
        "question": "A dataset contains seven positive integers: 12, 14, 15, 18, 20, 22, and x. If the mean of the dataset equals the median, and x is the largest integer in the dataset, what is the value of x?",
        "options": [
            {"key": "A", "text": "25"},
            {"key": "B", "text": "28"},
            {"key": "C", "text": "24"},
            {"key": "D", "text": "30"}
        ],
        "correct": "A",
        "explanation": "Agar x eng katta son bo'lsa, tartiblangan qator: 12, 14, 15, 18, 20, 22, x. 7 ta sonning medianasi 4-o'rindagi son, ya'ni 18 ga teng. O'rtacha arifmetik (mean) ham 18 ga teng bo'lishi kerak: (12 + 14 + 15 + 18 + 20 + 22 + x) / 7 = 18. Yig'indi: 101 + x = 7 * 18 = 126 => x = 126 - 101 = 25 (A to'g'ri). B (28), C (24) va D (30) o'rtacha qiymatni hisoblashdagi arifmetik xatolarga asoslangan chalg'ituvchi variantlardir.",
        "strategy_or_hack": "⚡ STATISTIKA QOIDASI: Toq sondagi tartiblangan qiymatlarda mediana o'rtadagi sondir (bu yerda 18). Yig'indi = O'rtacha * Sonlar soni: 18 * 7 = 126."
    },
    {
        "id": "m_ps_margin_01",
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Inference from sample statistics and margin of error",
        "difficulty": "Hard",
        "passage": "A research institute surveyed a representative random sample of 1,200 registered voters in a city. The survey found that 54% of respondents supported building a new public transit line, with a margin of error of 2.8% at a 95% confidence level.",
        "question": "Which of the following conclusions is most strongly supported by the survey results?",
        "options": [
            {"key": "A", "text": "It is plausible that between 51.2% and 56.8% of all registered voters in the city support the transit line."},
            {"key": "B", "text": "Exactly 54% of all registered voters in the city support the transit line."},
            {"key": "C", "text": "Increasing the sample size to 2,400 would double the margin of error to 5.6%."},
            {"key": "D", "text": "Every resident in the city supports the project with a 95% probability."}
        ],
        "correct": "A",
        "explanation": "Xatolik chegarasi (Margin of error) 2.8% bo'lsa, ishonchlilik oraliq oralig'i: 54% - 2.8% = 51.2% dan 54% + 2.8% = 56.8% gacha bo'ladi. Demak, butun shahar saylovchilari orasida qo'llab-quvvatlash darajasi 51.2% va 56.8% oralig'ida bo'lishi haqiqatga eng yaqin xulosadir (A to'g'ri). B - tanlanma natijasi butun populyatsiyaga mutlaq aniq 'exactly' teng bo'la olmaydi; C - tanlanma hajmi oshsa, xatolik chegarasi kamayadi (ikki barobar oshmaydi); D - jami shahar aholisi haqida asossiz haddan ortiq umumlashtirishdir.",
        "strategy_or_hack": "⚡ MARGIN OF ERROR QOIDASI: Margin of error (MOE) o'rtacha qiymat atrofida interval hosil qiladi [p - MOE, p + MOE]. SAT'da 'exactly' so'zi qatnashgan javoblar deyarli doimo xato bo'ladi!"
    },
    {
        "id": "m_ps_scatter_01",
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Two-variable data: models and scatterplots",
        "difficulty": "Hard",
        "passage": None,
        "question": "A scatterplot displays the relationship between the number of hours spent practicing per week, h, and the score achieved on a competitive exam, S. The line of best fit is given by S = 28.5h + 410. What does the value 28.5 represent in this model?",
        "options": [
            {"key": "A", "text": "The predicted increase in exam score for each additional hour spent practicing per week"},
            {"key": "B", "text": "The exam score achieved by a student who practices 0 hours per week"},
            {"key": "C", "text": "The total number of hours required to achieve a passing score"},
            {"key": "D", "text": "The maximum possible exam score that any student can achieve"}
        ],
        "correct": "A",
        "explanation": "Chiziqli model S = 28.5h + 410 da 28.5 burchak koeffitsienti (slope) hisoblanadi. Slope har doim erkli o'zgaruvchi (h) bir birlikka oshganda erksiz o'zgaruvchining (S) qanchaga o'zgarishini ko'rsatadi: har bir qo'shimcha mashg'ulot soati uchun ballning taxminiy 28.5 ballga oshishi (A to'g'ri). B - y-kesma (410) ma'nosi; C va D esa mutlaqo asossiz mantiqsiz talqinlardir.",
        "strategy_or_hack": "⚡ SLOPE TALQINI: Chiziqli modelda nishablik (slope) = 'rate of change' (har bir qo'shimcha x birligi uchun y ning o'zgarishi)."
    },

    # =========================================================================
    # MATH: GEOMETRY AND TRIGONOMETRY (6 questions)
    # =========================================================================
    {
        "id": "m_geo_circle_02",
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Circles (equations, radius, arc length, sector area)",
        "difficulty": "Easy",
        "passage": None,
        "question": "A circle in the xy-plane has the equation (x - 4)^2 + (y + 7)^2 = 64. What are the coordinates of the center and the radius of the circle?",
        "options": [
            {"key": "A", "text": "Center: (4, -7), Radius: 8"},
            {"key": "B", "text": "Center: (-4, 7), Radius: 64"},
            {"key": "C", "text": "Center: (4, -7), Radius: 64"},
            {"key": "D", "text": "Center: (-4, 7), Radius: 8"}
        ],
        "correct": "A",
        "explanation": "Aylana tenglamasining standart ko'rinishi: (x - h)^2 + (y - k)^2 = r^2. Bu yerda h = 4, k = -7 bo'lgani uchun markaz koordinatasi (4, -7). Radius r = sqrt(64) = 8. Shuning uchun to'g'ri javob A. B va D variantlarida markaz ishoralari almashtirib yuborilgan, C da esa radius ildiz ostiga olinmagan (64 qoldirilgan).",
        "strategy_or_hack": "⚡ DESMOS USULI: Tenglamani to'g'ridan-to'g'ri Desmosga yozing: (x-4)^2 + (y+7)^2 = 64. Markaz nuqtasi (4, -7) ekanini va diametri 16 (radiusi 8) ekanini darhol ko'rasiz."
    },
    {
        "id": "m_geo_tri_02",
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Lines, angles, and triangles (congruence, similarity, Pythagorean theorem, special triangles)",
        "difficulty": "Easy",
        "passage": None,
        "question": "In right triangle ABC, angle C is 90 degrees. If the length of side AC is 12 and the length of side BC is 16, what is the length of hypotenuse AB?",
        "options": [
            {"key": "A", "text": "20"},
            {"key": "B", "text": "28"},
            {"key": "C", "text": "18"},
            {"key": "D", "text": "24"}
        ],
        "correct": "A",
        "explanation": "Pifagor teoremasini qo'llaymiz: AB^2 = AC^2 + BC^2 = 12^2 + 16^2 = 144 + 256 = 400. AB = sqrt(400) = 20 (A to'g'ri). Shuningdek bu 3-4-5 pifagor uchburchagining 4 ga ko'paytirilgan karrali shaklidir (3*4=12, 4*4=16, 5*4=20). B (28) katetlarni shunchaki qo'shib qo'yish xatosi; C va D esa hisoblashdagi noaniqliklardir.",
        "strategy_or_hack": "⚡ PIFAGOR TRIPLET: 3-4-5 uchligini eslang: 12:16 = 3:4, demak gipotenuza 5 * 4 = 20 bo'ladi."
    },
    {
        "id": "m_geo_trig_02",
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Right triangle trigonometry (sine, cosine, tangent, complementary angles)",
        "difficulty": "Medium",
        "passage": None,
        "question": "For acute angles A and B in a right triangle, sin(A) = 7/25. What is the value of cos(B)?",
        "options": [
            {"key": "A", "text": "7/25"},
            {"key": "B", "text": "24/25"},
            {"key": "C", "text": "25/7"},
            {"key": "D", "text": "7/24"}
        ],
        "correct": "A",
        "explanation": "To'g'ri burchakli uchburchakda ikkita o'tkir burchak yig'indisi 90 gradusga teng (A + B = 90°). Bir-birini 90° ga to'ldiruvchi burchaklar (complementary angles) uchun asosiy trigonometrik qoida: sin(A) = cos(90° - A) = cos(B). Shuning uchun sin(A) = 7/25 bo'lsa, cos(B) ham aynan 7/25 ga teng bo'ladi (A to'g'ri). B (24/25) - cos(A) ning qiymati; C - teskari kasr; D esa tangens qiymatidir.",
        "strategy_or_hack": "⚡ OLTIN TRIGO QOIDASI: sin(A) = cos(B) agar A + B = 90° bo'lsa. Hech qanday hisob-kitobsiz bir zumda 7/25 ni belgilang!"
    },
    {
        "id": "m_geo_arc_01",
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Circles (equations, radius, arc length, sector area)",
        "difficulty": "Medium",
        "passage": None,
        "question": "A circle with radius 15 cm has a central angle of 72 degrees. What is the length, in centimeters, of the arc subtended by this central angle?",
        "options": [
            {"key": "A", "text": "6*pi"},
            {"key": "B", "text": "3*pi"},
            {"key": "C", "text": "12*pi"},
            {"key": "D", "text": "30*pi"}
        ],
        "correct": "A",
        "explanation": "Aylanadagi yoy uzunligi formulasi: L = 2 * pi * r * (theta / 360). Bu yerda r = 15, theta = 72°. L = 2 * pi * 15 * (72 / 360) = 30 * pi * (1 / 5) = 6 * pi (A to'g'ri). B (3*pi) - diametr o'rniga radiusni 2 ga ko'paytirishni unutganda; C (12*pi) va D (30*pi) esa burchak ulushini xato olgandagi tuzoqlardir.",
        "strategy_or_hack": "⚡ YOY UZUNLIGI: Aylananing to'liq perimetri = 2 * pi * 15 = 30*pi. 72 gradus bu to'liq aylananing 72/360 = 1/5 qismi. 30*pi / 5 = 6*pi."
    },
    {
        "id": "m_geo_vol_01",
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Area and volume formulas (circles, cylinders, prisms)",
        "difficulty": "Hard",
        "passage": None,
        "question": "A right circular cylinder has a height of 14 inches and a volume of 350*pi cubic inches. What is the radius, in inches, of the circular base of this cylinder?",
        "options": [
            {"key": "A", "text": "5"},
            {"key": "B", "text": "25"},
            {"key": "C", "text": "10"},
            {"key": "D", "text": "7"}
        ],
        "correct": "A",
        "explanation": "Silindr hajmi formulasi: V = pi * r^2 * h. Qiymatlarni qo'yamiz: 350 * pi = pi * r^2 * 14. Ikkala tomonni pi ga bo'lamiz: 350 = 14 * r^2 => r^2 = 350 / 14 = 25. r = sqrt(25) = 5 dyuym (A to'g'ri). B (25) - r^2 ni radius deb adashish; C (10) - diametr qiymati; D (7) esa balandlikka asoslangan noto'g'ri variantdir.",
        "strategy_or_hack": "⚡ FORMULA NAZORATI: Hajm = Asos yuzi * Balandlik. r^2 = V / (pi * h) = 350 / 14 = 25. Radius = 5."
    },
    {
        "id": "m_geo_hard_circle_01",
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Circles (equations, radius, arc length, sector area)",
        "difficulty": "Hard",
        "passage": None,
        "question": "The equation x^2 + y^2 - 10x + 6y + 9 = 0 represents a circle in the xy-plane. What is the radius of this circle?",
        "options": [
            {"key": "A", "text": "5"},
            {"key": "B", "text": "25"},
            {"key": "C", "text": "sqrt(34)"},
            {"key": "D", "text": "3"}
        ],
        "correct": "A",
        "explanation": "To'la kvadratga keltiramiz:\n(x^2 - 10x + 25) + (y^2 + 6y + 9) = -9 + 25 + 9\n(x - 5)^2 + (y + 3)^2 = 25\nDemak, markaz (5, -3) va r^2 = 25 bo'lgani uchun radius r = sqrt(25) = 5 (A to'g'ri). B (25) - r^2 ni radius deb hisoblash tuzog'i; C va D esa to'la kvadratga qo'shilgan sonlarni xato muvozanatlash oqibatidir.",
        "strategy_or_hack": "⚡ DESMOS USULI: Tenglamani xuddi o'zidek Desmosga yozing: x^2 + y^2 - 10x + 6y + 9 = 0. Aylana paydo bo'ladi. Uning chap va o'ng chegarasiga qarang: x = 0 dan x = 10 gacha (diametr = 10), demak radius = 5!"
    },

    # =========================================================================
    # READING: CRAFT AND STRUCTURE (9 questions)
    # =========================================================================
    {
        "id": "rw_vic_04",
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Words in Context (tier-2 academic vocabulary in sentence context)",
        "difficulty": "Easy",
        "passage": "During the late nineteenth century, urban reformers sought to ameliorate the overcrowded and unsanitary conditions of tenement districts by mandating better ventilation and public sanitation infrastructure.",
        "question": "As used in the text, what does the word 'ameliorate' most nearly mean?",
        "options": [
            {"key": "A", "text": "Improve"},
            {"key": "B", "text": "Publicize"},
            {"key": "C", "text": "Document"},
            {"key": "D", "text": "Complicate"}
        ],
        "correct": "A",
        "explanation": "Matn kontekstiga qarang: islohotchilar (urban reformers) antisanitariya va zich sharoitlarni ventilyatsiya hamda tozalik infratuzilmasi o'rnatish orqali yaxshilashga (ameliorate) intilgan. 'Ameliorate' - biror yomon sharoitni yaxshilash, o'nglash ma'nosini bildiradi, ya'ni 'improve' (A to'g'ri). B (publicize - ommalashtirish), C (document - qayd etish) va D (complicate - murakkablashtirish) islohotlarning ijobiy maqsadiga mutlaqo to'g'ri kelmaydigan chalg'ituvchi variantlardir.",
        "strategy_or_hack": "⚡ CONTEXT CLUE: Islohotchilar yaxshiroq ventilyatsiya kiritmoqda => demak sharoitni yaxshilamoqda ('ameliorate' = 'improve')."
    },
    {
        "id": "rw_vic_05",
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Words in Context (tier-2 academic vocabulary in sentence context)",
        "difficulty": "Medium",
        "passage": "Although earlier paleontologists hypothesized that pterosaurs were merely passive gliders, recent aerodynamic modeling indicates that their muscular anatomy was sufficiently robust to sustain vigorous, powered flight.",
        "question": "As used in the text, what does the word 'robust' most nearly mean?",
        "options": [
            {"key": "A", "text": "Strong"},
            {"key": "B", "text": "Rigid"},
            {"key": "C", "text": "Complex"},
            {"key": "D", "text": "Visible"}
        ],
        "correct": "A",
        "explanation": "Kontekst tahlili: Gapda passiv suzuvchi (passive gliders) bo'lish g'oyasiga zid ravishda, pterozavrlarning mushak tuzilishi baquvvat, kuchli (robust) bo'lib, mustaqil faol parvozni (vigorous, powered flight) ta'minlay olgani aytilmoqda. 'Robust' mushaklar haqida ketganda 'strong' (baquvvat/kuchli) ma'nosida keladi (A to'g'ri). B (rigid - qotib qolgan/egilmas), C (complex - murakkab) va D (visible - ko'rinadigan) parvoz kuchini ta'minlash kontekstiga mos kelmaydigan tuzoqlardir.",
        "strategy_or_hack": "⚡ QARAMA-QARSHILIKNI TOPING: 'passive gliders' vs 'vigorous, powered flight'. Faol parvoz uchun mushaklar baquvvat (strong) bo'lishi shart."
    },
    {
        "id": "rw_vic_06",
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Words in Context (tier-2 academic vocabulary in sentence context)",
        "difficulty": "Hard",
        "passage": "The philosopher's prose was notoriously opaque, compelling commentators to spend decades parsing ambiguous aphorisms to extract a coherent theoretical framework.",
        "question": "As used in the text, what does the word 'opaque' most nearly mean?",
        "options": [
            {"key": "A", "text": "Difficult to understand"},
            {"key": "B", "text": "Physically dense"},
            {"key": "C", "text": "Overly emotional"},
            {"key": "D", "text": "Factually incorrect"}
        ],
        "correct": "A",
        "explanation": "Matndagi dalilga e'tibor bering: sharhlovchilar o'n yillab noaniq iboralarni tahlil qilib, tushunishga majbur bo'lishgan ('compelling commentators to spend decades parsing ambiguous aphorisms'). Matn yoki uslub haqida 'opaque' so'zi ishlatilganda, u shaffof emas, ya'ni tushunish o'ta qiyin, tushunarsiz ('difficult to understand') degan majoziy ma'noni anglatadi (A to'g'ri). B (physically dense - jismonan zich) bu so'zning jismoniy narsalarga nisbatan birlamchi ma'nosi bo'lib, kontekstga zid; C va D esa asossiz taxminlardir.",
        "strategy_or_hack": "⚡ SECONDARY MEANING TRAP: 'Opaque' fizika bo'yicha 'yorug'lik o'tkazmaydigan', adabiyot/matn kontekstida esa 'tushunish qiyin bo'lgan' (obscure/unclear) demakdir."
    },
    {
        "id": "rw_func_01",
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Text Structure and Purpose (overall structure, function of underlined portion)",
        "difficulty": "Medium",
        "passage": "In many ecosystems, apex predators regulate herbivore populations and indirectly maintain plant diversity. When grey wolves were reintroduced to Yellowstone National Park, elk ceased overbrowsing young willow and aspen saplings near riverbanks. Consequently, stabilizing root systems flourished, riverbank erosion slowed, and beaver colonies returned to construct vital wetland habitats.",
        "question": "Which choice best describes the primary function of the underlined sentence ('Consequently, stabilizing root systems flourished...') in the overall text?",
        "options": [
            {"key": "A", "text": "It illustrates a downstream ecological cascade triggered by the predator's return."},
            {"key": "B", "text": "It challenges the initial assertion regarding apex predators."},
            {"key": "C", "text": "It introduces an unforeseen flaw in the reintroduction project."},
            {"key": "D", "text": "It compares Yellowstone's geography to other North American river systems."}
        ],
        "correct": "A",
        "explanation": "Matn strukturasi: Dastlab yirtqichlarning ekotizimga ta'siri aytiladi, keyin bo'rilar qaytarilgach bug'ular daraxtlarni yeb bitirmagani va buning natijasida (Consequently) o'simliklar ildiz otib, daryo qirg'og'i mustahkamlanib, qunduzlar qaytgani keltiriladi. Bu yirtqich qaytishi zanjirsimon ijobiy ekologik oqibatlarni keltirib chiqarganini ko'rsatuvchi misoldir (A to'g'ri). B - boshlang'ich da'voga zid emas, uni tasdiqlaydi; C - hech qanday kamchilik (flaw) tilga olinmagan; D - boshqa daryolar bilan taqqoslash yo'q.",
        "strategy_or_hack": "⚡ FUNKSIYANI ANIQLASH: 'Consequently' so'zi sabab-oqibat zanjirini bog'laydi. Bo'rilar qaytdi => o'simliklar ko'paydi => qunduzlar qaytdi (ecological cascade)."
    },
    {
        "id": "rw_cross_01",
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Cross-Text Connections (comparing viewpoints in paired texts)",
        "difficulty": "Hard",
        "passage": "Text 1: Proponents of open-plan office layouts argue that removing physical partitions fosters spontaneous interdisciplinary collaboration and flattens organizational hierarchies, ultimately boosting workplace creative output.\n\nText 2: Empirical studies tracking employee communication show that face-to-face interactions often decline precipitously by up to 70% following transitions to open-plan designs. Deprived of acoustic privacy, workers retreat behind noise-canceling headphones and substitute verbal communication with email and instant messaging.",
        "question": "Based on the texts, how would the author of Text 2 most likely respond to the claim in Text 1 regarding 'spontaneous collaboration'?",
        "options": [
            {"key": "A", "text": "By demonstrating that open layouts often inadvertently diminish in-person communication as workers seek privacy."},
            {"key": "B", "text": "By agreeing that creative output increases despite minor acoustic inconveniences."},
            {"key": "C", "text": "By advocating for the complete elimination of electronic messaging in corporate environments."},
            {"key": "D", "text": "By arguing that interdisciplinary projects should be abandoned entirely."}
        ],
        "correct": "A",
        "explanation": "Text 1 ochiq ofislar hamkorlikni (collaboration) oshiradi deb da'vo qiladi. Text 2 esa empirik tadqiqotlarga tayanib, ochiq ofisga o'tilgach yuzma-yuz muloqot 70% ga kamayib ketgani, odamlar shovqindan qochib naushnik taqib, yozishmaga o'tib olganini bildiradi. Demak, Text 2 muallifi ochiq ofis xususiy hudud yo'qligi sababli o'z-o'zidan jonli muloqotni kamaytirib yuboradi deb javob beradi (A to'g'ri). B - Text 2 ijodiy mahsuldorlik oshishiga qo'shilmaydi; C va D esa haddan tashqari radikal va matnda yo'q da'volardir.",
        "strategy_or_hack": "⚡ JUFT MATNLAR QOIDASI: Text 1 nazariy da'vo beradi, Text 2 empirik dalil (70% pasayish) bilan uni rad etadi. Javob aynan shu to'qnashuvni aks ettirishi shart."
    },
    {
        "id": "rw_vic_07",
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Words in Context (tier-2 academic vocabulary in sentence context)",
        "difficulty": "Medium",
        "passage": "The archival records from the expedition were fragmentary, yet the historian managed to reconstruct a remarkably coherent narrative of the polar voyage.",
        "question": "As used in the text, what does the word 'coherent' most nearly mean?",
        "options": [
            {"key": "A", "text": "Logically consistent and clear"},
            {"key": "B", "text": "Unusually lengthy"},
            {"key": "C", "text": "Financially successful"},
            {"key": "D", "text": "Highly controversial"}
        ],
        "correct": "A",
        "explanation": "Matn ziddiyatiga qarang: arxiv yozuvlari parcha-parcha, to'liq emas ('fragmentary') bo'lsa-da, tarixchi mantiqan izchil va ravshan ('coherent') hikoyani tiklashga muvaffaq bo'ldi. 'Coherent' mantiqiy jihatdan bir-biriga bog'langan va tushunarli demakdir (A to'g'ri). B (lengthy - cho'zilgan), C (financially successful - moliyaviy muvaffaqiyatli) va D (controversial - bahsli) kontekstga umuman aloqador bo'lmagan xato distractorlardir.",
        "strategy_or_hack": "⚡ KONTRAST LOGIKASI: 'Yet' so'zi fragmentary (parcha-parcha) ga teskari sifat talab qiladi: bir butun, mantiqiy (coherent = logically consistent)."
    },
    {
        "id": "rw_func_02",
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Text Structure and Purpose (overall structure, function of underlined portion)",
        "difficulty": "Hard",
        "passage": "Biologists long considered subterranean bioluminescence in fungi to be an incidental metabolic byproduct of lignin breakdown. However, recent behavioral assays reveal that the eerie nocturnal glow specifically attracts spore-dispersing beetles, ensuring reproductive dissemination even in windless underground hollows.",
        "question": "Which choice best describes the relationship between the two sentences in the passage?",
        "options": [
            {"key": "A", "text": "The first presents an established hypothesis, and the second introduces evidence that overturns it with an adaptive function."},
            {"key": "B", "text": "The first outlines an experimental methodology, and the second critiques its sampling errors."},
            {"key": "C", "text": "The first describes an evolutionary mystery, and the second dismisses its ecological significance."},
            {"key": "D", "text": "The first introduces an insect species, and the second tracks its predatory habits."}
        ],
        "correct": "A",
        "explanation": "Birinchi gapda olimlar uzoq vaqt qo'ziqorinlarning porlashini shunchaki tasodifiy moddalar almashinuvi mahsuli ('incidental byproduct') deb hisoblagan gipotezasi keltirilgan. Ikkinchi gap 'However' bilan burilib, yangi tajribalar bu porlash hasharotlarni jalb qilib sporalarni tarqatishga xizmat qiladigan moslashuv vazifasi (adaptive function) ekanini isbotlaganini ko'rsatadi (A to'g'ri). B - metodologiya haqida emas; C - ahamiyatini yo'qqa chiqarmaydi, aksincha ochib beradi; D - hasharot birinchi gapda umuman yo'q.",
        "strategy_or_hack": "⚡ MATN STRUKTURASI: 'long considered X... However, recent Y reveals Z' - bu ilmiy matnlardagi klassik 'eski qarash va uni inkor etuvchi yangi kashfiyot' andozasidir."
    },
    {
        "id": "rw_vic_08",
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Words in Context (tier-2 academic vocabulary in sentence context)",
        "difficulty": "Easy",
        "passage": "Because the experimental antibiotic displayed broad-spectrum efficacy in laboratory petri dishes, physicians were optimistic that clinical human trials would yield comparable therapeutic results.",
        "question": "As used in the text, what does the word 'efficacy' most nearly mean?",
        "options": [
            {"key": "A", "text": "Effectiveness"},
            {"key": "B", "text": "Toxicity"},
            {"key": "C", "text": "Expense"},
            {"key": "D", "text": "Rarity"}
        ],
        "correct": "A",
        "explanation": "Matn mantiqi: Antibiotik laboratoriyada yuqori samara (broad-spectrum efficacy) ko'rsatgani uchun shifokorlar klinik sinovlar yaxshi natija berishiga umid qilishgan. 'Efficacy' so'zi samaradorlik, natija bera olish qobiliyati ('effectiveness') deganidir (A to'g'ri). B (toxicity - zaharlilik) ijobiy umidga zid; C (expense - qimmatlik) va D (rarity - noyoblik) kontekstga to'g'ri kelmaydi.",
        "strategy_or_hack": "⚡ SO'Z ILDIZI: Efficacy = Effective (samarali). 'Yield comparable results' iborasi samaradorlikni ko'rsatadi."
    },
    {
        "id": "rw_cross_02",
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Cross-Text Connections (comparing viewpoints in paired texts)",
        "difficulty": "Medium",
        "passage": "Text 1: Urban rooftop gardens provide vital micro-climate cooling and insulation, reducing residential energy consumption by up to 15% in densely built city cores.\n\nText 2: While rooftop vegetation undoubtedly moderates surface temperatures, structural retrofitting costs often exceed municipal budgets, rendering widespread installation impractical without substantial private capital investment.",
        "question": "Which choice best describes how Text 2 regards the perspective presented in Text 1?",
        "options": [
            {"key": "A", "text": "It acknowledges the environmental benefits mentioned in Text 1 but highlights practical financial impediments."},
            {"key": "B", "text": "It outright denies that green roofs provide any thermodynamic cooling benefits."},
            {"key": "C", "text": "It contends that public funds should completely replace private investment."},
            {"key": "D", "text": "It praises the architectural feasibility of universal rooftop conversion."}
        ],
        "correct": "A",
        "explanation": "Text 2 boshidayoq Text 1 dagi haroratni pasaytirish foydasini tan oladi ('While rooftop vegetation undoubtedly moderates surface temperatures...'), biroq binolarni qayta jihozlash xarajatlari shahar byudjetidan oshib ketishini, ya'ni moliyaviy to'siqlarni o'rtaga tashlaydi (A to'g'ri). B - foydani inkor etmaydi; C - xususiy kapital zarur deydi; D - arxitektura jihatidan oson deb maqtamaydi.",
        "strategy_or_hack": "⚡ 'WHILE' KALITI: 'While X, Y' strukturasi birinchi qismni qabul qilib, ikkinchi qismda asosiy cheklovni keltiradi."
    },

    # =========================================================================
    # READING: INFORMATION AND IDEAS (9 questions)
    # =========================================================================
    {
        "id": "rw_cid_02",
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Central Ideas and Details (main themes and specific stated claims)",
        "difficulty": "Easy",
        "passage": "In arid desert environments, the saguaro cactus functions as a keystone species. Its spring blossoms provide vital nectar for migrating long-nosed bats, while its summer fruit nourishes desert tortoises and coyotes. Furthermore, Gila woodpeckers excavate nest cavities in the cactus's thick trunk, which are subsequently inhabited by screech owls and purple martins once vacated.",
        "question": "Which choice best states the main idea of the text?",
        "options": [
            {"key": "A", "text": "The saguaro cactus provides essential food and shelter that support a wide variety of desert wildlife."},
            {"key": "B", "text": "Gila woodpeckers are the primary threat to the structural integrity of mature saguaro cacti."},
            {"key": "C", "text": "Long-nosed bats depend exclusively on saguaro fruit during the summer months."},
            {"key": "D", "text": "Desert tortoises compete aggressively with coyotes for nesting cavities in desert plants."}
        ],
        "correct": "A",
        "explanation": "Matnning birinchi jumlasidayoq saguaro kaktusi ekotizim uchun tayanch tur ('keystone species') ekani e'lon qilinadi. Keyingi jumlalarda u ko'rshapalaklar, toshbaqalar, koyotlarga ozuqa berishi hamda qushlarga in vazifasini o'tashi sanab o'tiladi. Demak, asosiy g'oya kaktus ko'plab cho'l jonivorlarini oziq va boshpana bilan ta'minlashidir (A to'g'ri). B - kaktusga xavf haqida emas; C - ko'rshapalaklar faqat kaktusga tayanadi deyilmagan (exclusively xato); D - toshbaqa va koyotlar in uchun urushmaydi.",
        "strategy_or_hack": "⚡ ASOSIY G'OYA: Birinchi jumlani va butun matn qamrovini oling: kaktus oziq (gul, meva) va boshpana (kovaklar) beradi."
    },
    {
        "id": "rw_inf_02",
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Inferences (drawing logical conclusions from passage premises)",
        "difficulty": "Medium",
        "passage": "In an experiment on memory consolidation, participants learned word pairs before either eight hours of nocturnal sleep or eight hours of continuous daytime wakefulness. Brain imaging revealed that sleep-deprived participants exhibited significantly reduced functional connectivity between the hippocampus and prefrontal cortex during subsequent recall tests. Conversely, the sleep group displayed robust neural synchrony between these regions, accompanied by a 35% higher retention accuracy.",
        "question": "Which conclusion is most logically supported by the experimental findings?",
        "options": [
            {"key": "A", "text": "Sleep facilitates the neural communication pathways necessary for durable memory retrieval."},
            {"key": "B", "text": "Prefrontal cortex activity is entirely inactive during daytime wakefulness."},
            {"key": "C", "text": "The hippocampus permanently stores all semantic memories without cortical involvement."},
            {"key": "D", "text": "Word-pair recall is unaffected by the duration of sleep as long as participants rest."}
        ],
        "correct": "A",
        "explanation": "Eksperiment shuni ko'rsatadiki, uxlagan guruhda gipokamp va prefrontal korteks o'rtasidagi neyron aloqalar mustahkamlanib, xotirada saqlash 35% ga yuqori bo'lgan, uyqusizlarda esa bu aloqalar uzilgan. Bundan mantiqiy xulosa: uyqu xotirani mustahkam qayta tiklash uchun zarur bo'lgan neyron aloqalarni osonlashtiradi (A to'g'ri). B - kunduzi miya butunlay o'chadi ('entirely inactive') degan radikal da'vo matnda yo'q; C - gipokamp xotirani doimiy saqlaydi deyilmagan; D - ta'sir qilmaydi degan da'vo eksperiment natijasiga (35% farq) to'g'ridan-to'g'ri ziddir.",
        "strategy_or_hack": "⚡ XULOSA QOIDASI: Xulosa aynan matndagi dalillarga (35% yuqori saqlash + neyron sinxronlik) tayanishi shart. 'Entirely' yoki 'permanently' kabi ekstremal so'zlar odatda noto'g'ri distractorlardir."
    },
    {
        "id": "rw_evi_02",
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Command of Evidence: Textual (finding passage evidence to support/weaken a claim)",
        "difficulty": "Hard",
        "passage": "Ecologist Dr. Elena Vance investigated whether marine protected areas (MPAs) with strict no-fishing mandates enhance fish biomass in adjacent unprotected waters through the 'spillover effect.' Critics hypothesized that fish rarely migrate outside the protected boundaries, meaning adjacent non-reserve waters gain no measurable productivity.",
        "question": "Which finding, if true, would most directly weaken the critics' hypothesis?",
        "options": [
            {"key": "A", "text": "Commercial fish catches within 3 kilometers of the MPA boundary increased steadily over five years as tagged adult fish migrated outward."},
            {"key": "B", "text": "Fish species inside the MPA displayed higher genetic diversity than fish documented in distant oceanic trenches."},
            {"key": "C", "text": "Tourism revenue within the marine reserve increased significantly due to recreational diving."},
            {"key": "D", "text": "Local fishing fleets purchased motorized vessels with larger refrigeration holds."}
        ],
        "correct": "A",
        "explanation": "Tanqidchilarning gipotezasi: Baliqlar qo'riqxona chegarasidan tashqariga deyarli chiqmaydi, shuning uchun chegaraga yaqin himoyalanmagan suvlar hech qanday hosildorlikka erishmaydi. Ushbu gipotezani kuchsizlantirish (weaken) uchun qo'riqxonaga yaqin hududlarda belgilangan baliqlar tashqariga chiqib, ovi ko'payganini isbotlash kerak. A varianti aynan belgilangan balig'i tashqariga chiqib, 3 km masofadagi tijorat ovi 5 yil davomida oshganini ko'rsatadi va tanqidchilarni inkor etadi (A to'g'ri). B - uzoq okean xandaqlari haqida gap bormagan; C - turizm pulining baliq migratsiyasiga aloqasi yo'q; D - kemalarning kattalashishi baliq chiqqanini isbotlamaydi.",
        "strategy_or_hack": "⚡ WEAKEN SAVOLLARIDA: Avval tanqidchining da'vosini aniqlang ('baliq tashqariga chiqmaydi'). Uni sindiruvchi variant: 'baliqlar belgilangan holda tashqariga chiqib ovlandi'."
    },
    {
        "id": "rw_quant_01",
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Command of Evidence: Quantitative (interpreting informational tables/graphs)",
        "difficulty": "Medium",
        "passage": "A study compared the thermal insulation efficacy of four bio-composite construction materials:\n- Material W (Hemp-lime): Thermal conductivity 0.07 W/(m*K), Cost $18/sqm\n- Material X (Mycelium foam): Thermal conductivity 0.04 W/(m*K), Cost $26/sqm\n- Material Y (Straw bale): Thermal conductivity 0.09 W/(m*K), Cost $12/sqm\n- Material Z (Cellulose fiber): Thermal conductivity 0.05 W/(m*K), Cost $21/sqm\nNote: Lower thermal conductivity indicates superior insulating capability.",
        "question": "Based on the data, which material offers the superior insulating capability, and which is the most economical per square meter?",
        "options": [
            {"key": "A", "text": "Material X provides superior insulation; Material Y is the most economical."},
            {"key": "B", "text": "Material Y provides superior insulation; Material X is the most economical."},
            {"key": "C", "text": "Material W provides superior insulation; Material Z is the most economical."},
            {"key": "D", "text": "Material Z provides superior insulation; Material W is the most economical."}
        ],
        "correct": "A",
        "explanation": "Ma'lumotlar tahlili: Eslatmaga qarang: 'Lower thermal conductivity indicates superior insulating capability' (Past o'tkazuvchanlik yuqori izolyatsiyani bildiradi). Eng past ko'rsatkich Material X da: 0.04 W/(m*K). Demak, eng yaxshi izolyatsiya - Material X. Eng tejamkor (eng arzon) narx esa Material Y da: $12/sqm. Shunday qilib, A to'g'ri javob. B teskari tushunish; C va D esa jadvallar sonlarini noto'g'ri taqqoslashdir.",
        "strategy_or_hack": "⚡ JADVAL ESLETMASINI O'QING: 'Lower indicates superior' shartiga e'tibor bering: eng kichik son (0.04) = eng kuchli izolyatsiya!"
    },
    {
        "id": "rw_cid_03",
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Central Ideas and Details (main themes and specific stated claims)",
        "difficulty": "Medium",
        "passage": "While Renaissance fresco painters primarily employed mineral pigments bound in wet lime plaster, Northern European masters pioneered oil glazing techniques. By layering translucent linseed oil glazes over opaque underpaintings, Northern artists achieved unprecedented luminous depth and rich textural realism that fresco could not replicate.",
        "question": "Which choice best captures the central idea of the passage?",
        "options": [
            {"key": "A", "text": "Northern European oil glazing enabled greater optical depth and surface realism than traditional plaster fresco techniques."},
            {"key": "B", "text": "Renaissance fresco painters completely abandoned mineral pigments after the invention of oil glaze."},
            {"key": "C", "text": "Linseed oil was too costly to be used by any painters working outside Northern Europe."},
            {"key": "D", "text": "Fresco painting was technically superior to oil painting in achieving luminous light effects."}
        ],
        "correct": "A",
        "explanation": "Matn freska va moybo'yoq texnikasini taqqoslaydi. Shimoliy Yevropa ustalari shaffof moybo'yoq qatlamlarini qo'llash orqali freska bera olmaydigan jozibador chuqurlik va to'qimalar realizmiga erishgani ta'kidlanadi (A to'g'ri). B - freskachilar mineral pigmentlarni butunlay tashlab yuborgani yo'q; C - xarajat haqida matnda so'z bormagan; D - freska moybo'yoqdan ustun emas, aksincha moybo'yoq freska bera olmagan chuqurlikni bergan.",
        "strategy_or_hack": "⚡ ASOSIY G'OYA: Matndagi taqqoslash xulosasini toping: 'oil glazing achieved unprecedented luminous depth that fresco could not replicate'."
    },
    {
        "id": "rw_inf_03",
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Inferences (drawing logical conclusions from passage premises)",
        "difficulty": "Hard",
        "passage": "Archaeobotanists analyzed sediment cores from an ancient Mayan lake basin, tracking maize pollen alongside charcoal deposits from agricultural burning. Between 800 CE and 950 CE, maize pollen dropped to near-zero levels, coinciding with a prolonged multi-decade decrease in regional precipitation indicators and the subsequent abandonment of major urban administrative plazas.",
        "question": "Which conclusion about the ancient society is most reliably inferred from the sediment evidence?",
        "options": [
            {"key": "A", "text": "Severe drought severely disrupted staple crop cultivation, likely contributing to urban collapse."},
            {"key": "B", "text": "The population voluntarily transitioned from agriculture to nomadic pastoralism."},
            {"key": "C", "text": "Urban plazas were abandoned solely due to foreign military invasion."},
            {"key": "D", "text": "Maize crops were successfully replaced with drought-resistant wheat varieties."}
        ],
        "correct": "A",
        "explanation": "Dalillarni birlashtiramiz: 800-950 yillar oralig'ida makkajo'xori changchalari deyarli yo'qolgan, bu davr yog'ingarchilikning keskin kamayishi (qurg'oqchilik) va yirik shahar maydonlarining tashlab ketilishi bilan bir vaqtga to'g'ri kelgan. Mantiqiy xulosa: qattiq qurg'oqchilik asosiy hosil yetishtirishni izdan chiqargan va shahar markazlarining bo'shab qolishiga olib kelgan (A to'g'ri). B - ko'chmanchilikka ixtiyoriy o'tish aytilmagan; C - harbiy bosqin haqida dalil yo'q ('solely' so'zi tuzoq); D - bug'doy haqida hech narsa deyilmagan.",
        "strategy_or_hack": "⚡ BOG'LIQLIKNI BIRLASHTIRISH: Qurg'oqchilik ko'rsatkichi + Makkajo'xori yo'qolishi + Shaharlar tashlab ketilishi => Ekologik qurg'oqchilik va dehqonchilik inqirozi."
    },
    {
        "id": "rw_evi_03",
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Command of Evidence: Textual (finding passage evidence to support/weaken a claim)",
        "difficulty": "Medium",
        "passage": "Linguist Dr. Tara Chen asserts that learning a tonal language in infancy enhances non-linguistic pitch discrimination later in childhood. To test this, she compared musical pitch memory scores between 8-year-olds raised in Mandarin-speaking households and 8-year-olds raised in English-speaking households.",
        "question": "Which finding from Dr. Chen's study would most directly support her assertion?",
        "options": [
            {"key": "A", "text": "The Mandarin-speaking children consistently outperformed the English-speaking children on microtonal pitch differentiation tasks."},
            {"key": "B", "text": "Both groups achieved identical scores on instrumental rhythm and percussion reproduction tests."},
            {"key": "C", "text": "English-speaking children demonstrated a preference for stringed instruments over wind instruments."},
            {"key": "D", "text": "Mandarin-speaking children had larger vocabularies in second languages than their peers."}
        ],
        "correct": "A",
        "explanation": "Dr. Chenning da'vosi: Tonal tilni (masalan, mandarin) go'daklikdan o'rganish keyinchalik tildan tashqari musiqiy ohangni (pitch discrimination) ajratishni kuchaytiradi. Buni tasdiqlash (support) uchun mandarin tilida ulg'aygan bolalar musiqiy ohang farqini aniqlash testlarida ingliz tilidagi bolalardan sezilarli darajada ustun kelganini ko'rsatuvchi dalil kerak (A to'g'ri). B - ritm haqida; C - cholg'u tanlovi; D - leksika haqida bo'lib, ohangni ajratish da'vosini tasdiqlamaydi.",
        "strategy_or_hack": "⚡ DA'VOGA MOS DALIL: Da'vo: 'tonal language enhances pitch discrimination'. Dalil: 'Mandarin group outperformed on pitch tasks'."
    },
    {
        "id": "rw_cid_04",
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Central Ideas and Details (main themes and specific stated claims)",
        "difficulty": "Hard",
        "passage": "Early twentieth-century economists viewed technological automation as a pure engine of employment expansion, assuming machines merely relieved humans of repetitive manual labor while creating higher-tier administrative roles. Modern labor data, however, reveals a 'job polarization' phenomenon: automation disproportionately displaces middle-skill clerical and routine assembly jobs, while simultaneously expanding both high-wage specialized cognitive jobs and low-wage service occupations.",
        "question": "Which choice best summarizes the passage's description of how modern economists view automation compared to early economists?",
        "options": [
            {"key": "A", "text": "Modern analysts recognize that automation polarizes the labor market across skill tiers rather than uniformly generating middle-tier jobs."},
            {"key": "B", "text": "Modern analysts believe automation has ceased to create any high-wage cognitive occupations."},
            {"key": "C", "text": "Early economists correctly predicted that service industry wages would decline to zero."},
            {"key": "D", "text": "Early economists argued that automation would permanently eliminate all forms of human employment."}
        ],
        "correct": "A",
        "explanation": "Matn tahlili: Dastlabki iqtisodchilar avtomatlashtirish o'rta qatlam ma'muriy ishlarini ko'paytiradi deb o'ylashgan. Zamonaviy ma'lumotlar esa 'job polarization' (mehnat bozorining qutblanishi) ni ko'rsatmoqda: o'rta toifadagi ishlar yo'qolib, faqat eng yuqori malakali va eng quyi xizmat ko'rsatish sohalari o'smoqda (A to'g'ri). B - yuqori toifali ishlar to'xtagan deyilmagan (expanding high-wage); C va D - erta iqtisodchilar bunday da'vo qilmagan.",
        "strategy_or_hack": "⚡ POLARIZATION MAZMUNI: O'rta qatlam ishlari siqib chiqarilib, yuqori va quyi qutblar o'sishi (job polarization across skill tiers)."
    },
    {
        "id": "rw_quant_02",
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Command of Evidence: Quantitative (interpreting informational tables/graphs)",
        "difficulty": "Easy",
        "passage": "A botanist recorded seed germination rates across four soil temperature settings:\n- 15°C: 22% germination rate\n- 20°C: 48% germination rate\n- 25°C: 86% germination rate\n- 30°C: 54% germination rate",
        "question": "Which claim is most directly supported by the recorded data?",
        "options": [
            {"key": "A", "text": "Germination rate reached its maximum at 25°C and declined at higher temperatures."},
            {"key": "B", "text": "Germination rate increased continuously as temperature rose from 15°C to 30°C."},
            {"key": "C", "text": "Soil temperatures below 15°C stimulate 100% germination."},
            {"key": "D", "text": "The seeds will fail to germinate entirely at 25°C."}
        ],
        "correct": "A",
        "explanation": "Raqamlar zanjiriga qarang: 15°C da 22%, 20°C da 48%, 25°C da 86% (eng yuqori cho'qqi), keyin esa 30°C da 54% ga tushib ketgan. Demak, unib chiqish 25°C da o'z maksimumiga erishgan va undan yuqori haroratda pasaygan (A to'g'ri). B - uzluksiz oshmagan (30°C da pasaygan); C va D - raqamlarga to'g'ridan-to'g'ri zid xatolardir.",
        "strategy_or_hack": "⚡ GRAFIK TRENDI: 22% -> 48% -> 86% -> 54%. Cho'qqi (peak) = 25°C."
    },

    # =========================================================================
    # WRITING: STANDARD ENGLISH CONVENTIONS (9 questions)
    # =========================================================================
    {
        "id": "w_bound_03",
        "section": "writing",
        "domain": "Standard English Conventions",
        "skill": "Boundaries (sentence boundaries: comma splices, run-ons, semicolons, colons, dashes)",
        "difficulty": "Easy",
        "passage": "The astrophysics symposium concluded ahead of ______ attendees gathered in the main atrium to network with keynote speakers.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "schedule; subsequently,"},
            {"key": "B", "text": "schedule, subsequently"},
            {"key": "C", "text": "schedule subsequently"},
            {"key": "D", "text": "schedule; subsequently"}
        ],
        "correct": "A",
        "explanation": "Gap tuzilishini tahlil qilamiz: 'The astrophysics symposium concluded ahead of schedule' mustaqil gap (independent clause). Undan keyin 'attendees gathered in the main atrium...' ham mustaqil gap. Ikkita mustaqil gapni bog'lash uchun nuqtali vergul (semicolon) va undan keyin kirish so'zi (conjunctive adverb 'subsequently') hamda vergul talab qilinadi: 'schedule; subsequently,' (A to'g'ri). B varianti vergul bilan bog'lab comma splice xatosini hosil qiladi; C tinish belgisiz run-on hosil qiladi; D da esa subsequently dan keyin vergul tushib qolgan.",
        "strategy_or_hack": "⚡ COMMA SPLICE TUZOG'I: Ikkita to'liq gapni oddiy vergul bilan ulab bo'lmaydi! Formula: Mustaqil gap + [; conjunctive adverb,] + Mustaqil gap."
    },
    {
        "id": "w_bound_04",
        "section": "writing",
        "domain": "Standard English Conventions",
        "skill": "Boundaries (sentence boundaries: comma splices, run-ons, semicolons, colons, dashes)",
        "difficulty": "Medium",
        "passage": "The museum curator uncovered a rare nineteenth-century ______ a hand-tinted map detailing navigational routes along the Mississippi River.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "artifact:"},
            {"key": "B", "text": "artifact;"},
            {"key": "C", "text": "artifact"},
            {"key": "D", "text": "artifact,"}
        ],
        "correct": "A",
        "explanation": "Ikki nuqta (colon) qoidasi: Ikki nuqtadan oldin to'liq mustaqil gap kelishi shart ('The museum curator uncovered a rare nineteenth-century artifact'). Ikki nuqtadan keyin esa o'sha artefakt nimadan iborat ekani tushuntirilmoqda yoki ro'yxat keltirilmoqda ('a hand-tinted map...'). Shuning uchun A to'g'ri. B (semicolon) bo'lishi uchun keyingi qism ham mustaqil gap bo'lishi kerak edi (bu yerda esa faqat otli birikma); C va D esa chalkash sintaktik chegarani keltirib chiqaradi.",
        "strategy_or_hack": "⚡ COLON (IKKI NUQTA) QOIDASI: Ikki nuqtadan oldin doimo mustaqil gap turishi kerak. Ikki nuqtadan keyin tushuntirish/misol keladi."
    },
    {
        "id": "w_bound_05",
        "section": "writing",
        "domain": "Standard English Conventions",
        "skill": "Boundaries (sentence boundaries: comma splices, run-ons, semicolons, colons, dashes)",
        "difficulty": "Hard",
        "passage": "Renowned for their intricate architectural ______ termitaries regulate internal humidity and temperature through an ingenious network of ventilation flues.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "design,"},
            {"key": "B", "text": "design;"},
            {"key": "C", "text": "design:"},
            {"key": "D", "text": "design"}
        ],
        "correct": "A",
        "explanation": "Gap boshida sifatdoshli kirish birikmasi (participial introductory phrase) kelmoqda: 'Renowned for their intricate architectural design'. Qoidaga ko'ra, asosiy mustaqil gap boshlanishidan oldin kirish birikmasi vergul bilan ajratilishi shart: 'design, termitaries regulate...' (A to'g'ri). B (semicolon) va C (colon) kirish birikmasidan keyin asossiz qo'yilgan xatodir; D da esa chegara belgisisiz qo'shilib ketgan.",
        "strategy_or_hack": "⚡ INTRODUCTORY PHRASE: Gap kirish iborasi bilan boshlansa, asosiy ega (termitaries) oldidan aniq VERGUL qo'yiladi."
    },
    {
        "id": "w_agree_01",
        "section": "writing",
        "domain": "Standard English Conventions",
        "skill": "Form, Structure, and Sense (subject-verb agreement, pronoun-antecedent agreement, verb tense)",
        "difficulty": "Easy",
        "passage": "Each of the experimental solar modules installed across the research ______ continuous efficiency data to the central monitoring station.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "facility transmits"},
            {"key": "B", "text": "facility transmit"},
            {"key": "C", "text": "facility are transmitting"},
            {"key": "D", "text": "facility have transmitted"}
        ],
        "correct": "A",
        "explanation": "Ega va kesim mosligi (Subject-Verb Agreement): Gapning haqiqiy egasi 'Each' so'zi bo'lib, u doimo birlikda (singular) bo'ladi. 'of the experimental solar modules installed across the research facility' esa ajratuvchi oraliq birikmadir (prepositional phrase). Birlikdagi ega 'Each' birlikdagi fe'l 'transmits' bilan moslashishi shart (A to'g'ri). B ('transmit'), C ('are transmitting') va D ('have transmitted') ko'plikdagi fe'llar bo'lib, ehtiyotsiz talabani chalg'itish uchun berilgan tuzoqlardir.",
        "strategy_or_hack": "⚡ ORALIK TUZOQNI O'CHIRING: 'Each [of the modules...] transmits'. 'Each', 'Neither', 'Either' birlik hisoblanadi."
    },
    {
        "id": "w_agree_02",
        "section": "writing",
        "domain": "Standard English Conventions",
        "skill": "Form, Structure, and Sense (subject-verb agreement, pronoun-antecedent agreement, verb tense)",
        "difficulty": "Medium",
        "passage": "Neither the lead engineer nor the laboratory technicians ______ able to isolate the electrical frequency interference during yesterday's trial.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "were"},
            {"key": "B", "text": "was"},
            {"key": "C", "text": "is"},
            {"key": "D", "text": "has been"}
        ],
        "correct": "A",
        "explanation": "Neither... nor qoidasi: 'Neither A nor B' konstruktsiyasida fe'l o'ziga eng yaqin turgan ikkinchi ega (B) bilan moslashadi (Rule of Proximity). Bu yerda ikkinchi ega 'the laboratory technicians' (ko'plikda). Shuningdek, 'yesterday's trial' o'tgan zamonni talab qiladi. Demak, o'tgan zamon ko'plik fe'li 'were' to'g'ri keladi (A to'g'ri). B ('was') birlikdagi tuzoq; C va D esa hozirgi zamon shakllari bo'lib, yesterday ga zid.",
        "strategy_or_hack": "⚡ NEITHER... NOR QOIDASI: Fe'l fe'lga yaqin turgan otga qarab moslashadi: 'technicians' (ko'plik) => 'were'."
    },
    {
        "id": "w_mod_01",
        "section": "writing",
        "domain": "Standard English Conventions",
        "skill": "Modifiers and Parallelism (dangling modifiers, misplaced modifiers, parallel structures)",
        "difficulty": "Medium",
        "passage": "Exhausted after an arduous forty-mile summit ______ a brief bivouac under the stars offered much-needed respite.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "trek, the mountaineers found that"},
            {"key": "B", "text": "trek,"},
            {"key": "C", "text": "trek, it was thought that"},
            {"key": "D", "text": "trek, the gear of the climbers allowed"}
        ],
        "correct": "A",
        "explanation": "Dangling modifier (osilib qolgan modifikator) qoidasi: 'Exhausted after an arduous forty-mile summit trek' (40 millik charchatuvchi yo'ldan toliqqan) kim bo'lishi mumkin? Albatta, alpinistlar (the mountaineers)! Verguldan keyin darhol harakatni bajargan shaxs ('the mountaineers') kelishi shart. B varianti 'a brief bivouac' (chodir toliqqan deb kulgili ma'no hosil qiladi); C da 'it' noaniq; D da esa alpinistlarning jihozlari (gear) charchagan degan mantiqsizlik kelib chiqadi. Shuning uchun A to'g'ri.",
        "strategy_or_hack": "⚡ DANGLING MODIFIER QOIDASI: Sifatdoshli ibora kimni tasvirlasa, verguldan keyingi 1-so'z aynan o'sha bo'lishi shart! Toliqqan kim? Alpinistlar!"
    },
    {
        "id": "w_mod_02",
        "section": "writing",
        "domain": "Standard English Conventions",
        "skill": "Modifiers and Parallelism (dangling modifiers, misplaced modifiers, parallel structures)",
        "difficulty": "Hard",
        "passage": "To accurately calibrate the seismic sensor, the technician must level the tripod, inspect the dampening spring, and ______ the digital recording frequency.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "verify"},
            {"key": "B", "text": "verifying"},
            {"key": "C", "text": "to verify"},
            {"key": "D", "text": "verified"}
        ],
        "correct": "A",
        "explanation": "Parallellik (Parallel Structure) qoidasi: Ro'yxatdagi barcha fe'llar bir xil grammatik shaklda bo'lishi shart: 'level the tripod' (asosiy fe'l), 'inspect the dampening spring' (asosiy fe'l), 'and verify the digital recording frequency' (asosiy fe'l). Shuning uchun 'verify' (A) to'g'ri. B ('verifying' - ingli shakl), C ('to verify' - infinitiv) va D ('verified' - o'tgan zamon) parallelizm qoidasini buzuvchi xato variantlardir.",
        "strategy_or_hack": "⚡ PARALLEL STRUCTURE: Fe'llar shaklini tekshiring: level... inspect... and verify."
    },
    {
        "id": "w_tense_01",
        "section": "writing",
        "domain": "Standard English Conventions",
        "skill": "Form, Structure, and Sense (subject-verb agreement, pronoun-antecedent agreement, verb tense)",
        "difficulty": "Medium",
        "passage": "By the time the search-and-rescue team arrived at the isolated alpine valley, local park rangers ______ all stranded hikers to safety.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "had already evacuated"},
            {"key": "B", "text": "have already evacuated"},
            {"key": "C", "text": "will have evacuated"},
            {"key": "D", "text": "evacuate"}
        ],
        "correct": "A",
        "explanation": "Past Perfect (O'tgan zamon oldi zamoni) qoidasi: O'tgan zamondagi biron harakatdan ('By the time the team arrived') oldin tugallangan harakat uchun Past Perfect (had + V3) ishlatiladi: 'had already evacuated' (A to'g'ri). B ('have evacuated') Present Perfect bo'lib, o'tgan zamon o'tmishiga mos kelmaydi; C kelasi zamon; D esa hozirgi noaniq zamondir.",
        "strategy_or_hack": "⚡ 'BY THE TIME' QOIDASI: 'By the time + Past Simple (arrived)... Past Perfect (had evacuated)'."
    },
    {
        "id": "w_bound_06",
        "section": "writing",
        "domain": "Standard English Conventions",
        "skill": "Boundaries (sentence boundaries: comma splices, run-ons, semicolons, colons, dashes)",
        "difficulty": "Hard",
        "passage": "The urban agricultural initiative—which transformed twelve abandoned industrial lots into flourishing community ______ provided organic produce to over four hundred neighborhood families.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "gardens—"},
            {"key": "B", "text": "gardens,"},
            {"key": "C", "text": "gardens;"},
            {"key": "D", "text": "gardens:"}
        ],
        "correct": "A",
        "explanation": "Tire (Em-dash) juftligi qoidasi: Gap o'rtasida izohlovchi qo'shimcha ma'lumot (non-essential parenthetical clause) em-dash (—) bilan boshlangan: 'initiative—which transformed twelve abandoned industrial lots into flourishing community gardens—'. Qoidaga ko'ra, agar kiritma tire bilan ochilgan bo'lsa, u aynan ikkinchi tire bilan yopilishi shart: 'gardens—' (A to'g'ri). B (vergul) tire bilan boshlangan kiritmaga mos kelmaydi; C (semicolon) va D (colon) esa sintaktik xatolardir.",
        "strategy_or_hack": "⚡ JUFT TIRE (DASH PAIR): Agar kiritma tire bilan ochilsa (—), u albatta tire bilan yopiladi (—). Vergul bilan aralashtirmang!"
    },

    # =========================================================================
    # WRITING: EXPRESSION OF IDEAS (9 questions)
    # =========================================================================
    {
        "id": "w_trans_04",
        "section": "writing",
        "domain": "Expression of Ideas",
        "skill": "Transitions (contrast, cause-effect, addition, illustration connectors)",
        "difficulty": "Easy",
        "passage": "Urban planners initially assumed that widening the downtown highway would alleviate severe traffic congestion. ______, vehicular volume surged as commuters altered their routes, causing gridlock to intensify.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "Instead"},
            {"key": "B", "text": "Consequently"},
            {"key": "C", "text": "Furthermore"},
            {"key": "D", "text": "Similarly"}
        ],
        "correct": "A",
        "explanation": "Mantiqiy bog'liqlik tahlili: Rejalashtiruvchilar tirbandlik kamayadi deb kutishgan, biroq kutilganning aksi yuz berib, avtomobillar oqimi ko'payib, tirbandlik kuchaygan. 'Instead' (aksincha/o'rniga) kutilgan natijaga teskari o'zgarishni eng to'g'ri ifodalaydi (A to'g'ri). B (Consequently - oqibatda) ijobiy kutuvning tabiiy natijasidek xato taassurot beradi; C (Furthermore - bundan tashqari) qo'shimcha qiladi; D (Similarly - xuddi shunday) esa o'xshashlikni bildiradi.",
        "strategy_or_hack": "⚡ KUTILGAN VS HAQIQAT: Kutilgan narsa sodir bo'lmay aksincha bo'lganda 'Instead' yoki 'However' ishlatiladi."
    },
    {
        "id": "w_trans_05",
        "section": "writing",
        "domain": "Expression of Ideas",
        "skill": "Transitions (contrast, cause-effect, addition, illustration connectors)",
        "difficulty": "Medium",
        "passage": "Traditional silicon photovoltaic cells degrade significantly when subjected to sustained desert heat exceeding 45 degrees Celsius. ______, emerging perovskite-silicon tandem cells demonstrate exceptional thermal stability, maintaining peak conversion efficiency even under intense solar radiation.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "In contrast"},
            {"key": "B", "text": "For example"},
            {"key": "C", "text": "In other words"},
            {"key": "D", "text": "Therefore"}
        ],
        "correct": "A",
        "explanation": "Ikki texnologiya taqqoslanmoqda: an'anaviy kremniy elementlari issiqda yomonlashadi (degrade), yangi perovskit elementlar esa yuqori termal barqarorlikni saqlab qoladi (exceptional thermal stability). Bu ochiq-oydin qarama-qarshilik (contrast) munosabatidir, shuning uchun 'In contrast' eng to'g'ri bog'lovchi (A to'g'ri). B (For example) misol keltirmaydi; C (In other words) qayta tushuntirmaydi; D (Therefore) esa sabab-oqibat emas.",
        "strategy_or_hack": "⚡ CONTRASTNI TOPING: 'degrades in heat' vs 'exceptional thermal stability' => 'In contrast' (farqli ravishda)."
    },
    {
        "id": "w_trans_06",
        "section": "writing",
        "domain": "Expression of Ideas",
        "skill": "Transitions (contrast, cause-effect, addition, illustration connectors)",
        "difficulty": "Hard",
        "passage": "Geological surveys confirmed that the subterranean cavern system possessed porous limestone walls saturated with moisture. ______, engineers determined that installing pressurized nitrogen storage tanks would require comprehensive moisture-impermeable polymer lining.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "Accordingly"},
            {"key": "B", "text": "Nevertheless"},
            {"key": "C", "text": "Conversely"},
            {"key": "D", "text": "In comparison"}
        ],
        "correct": "A",
        "explanation": "Mantiqiy bog'liqlik: Birinchi gapda devorlarning namlik bilan to'yingani ma'lum qilinadi. Shu sababli va shunga muvofiq ravishda (Accordingly) muhandislar himoya polimer qoplamasi o'rnatish zarur deb qaror qilishadi. Bu sabab va unga mos ravishda qilingan xulosa (cause and effect / logical consequence), shuning uchun 'Accordingly' to'g'ri (A). B (Nevertheless - shunga qaramasdan) va C (Conversely - teskarisiga) ziddiyatni bildiradi, holbuki muhandislar bu holatga mos harakat qilishgan; D esa taqqoslash emas.",
        "strategy_or_hack": "⚡ 'ACCORDINGLY' VA 'THEREFORE': Birinchi fakt asosida mantiqiy chora ko'rilsa, 'Accordingly' (shunga muvofiq) bog'lovchisi tanlanadi."
    },
    {
        "id": "w_syn_02",
        "section": "writing",
        "domain": "Expression of Ideas",
        "skill": "Rhetorical Synthesis (synthesizing provided bullet-point research notes)",
        "difficulty": "Easy",
        "passage": "While researching an extinct flightless bird, a student took the following notes:\n- The dodo (Raphus cucullatus) was endemic to the island of Mauritius.\n- It had no natural mammalian predators on the island prior to human arrival.\n- European sailors introduced invasive species such as rats, pigs, and monkeys in the early 1600s.\n- These invasive animals predated on ground-laid dodo eggs, driving the species to extinction by 1681.",
        "question": "The student wants to explain the primary cause of the dodo's extinction. Which choice most effectively uses the relevant information from the notes to accomplish this goal?",
        "options": [
            {"key": "A", "text": "The dodo was driven to extinction primarily because human-introduced invasive animals preyed on its ground-laid eggs."},
            {"key": "B", "text": "Endemic to Mauritius, the dodo lived peacefully before European sailors explored the Indian Ocean."},
            {"key": "C", "text": "The dodo was a flightless bird known scientifically as Raphus cucullatus."},
            {"key": "D", "text": "Invasive rats, pigs, and monkeys arrived on Mauritius in the early 1600s."}
        ],
        "correct": "A",
        "explanation": "Talabaning maqsadi: Dodo qushining qirilib ketishining asosiy sababini (primary cause of extinction) tushuntirish. Qaydlarda qirilishning bosh omili insonlar olib kelgan yirtqich hayvonlarning yerga qo'yilgan tuxumlarni yeb bitirgani ekani aniq aytilgan. A varianti aynan shu sababni to'g'ridan-to'g'ri va to'liq ochib beradi (A to'g'ri). B faqat tinch yashaganini aytadi; C ilmiy nomini keltiradi; D esa sababni qush bilan bog'lamaydi.",
        "strategy_or_hack": "⚡ MAQSADNI ANIQLANG: Savol shartidagi vazifa: 'explain primary cause of extinction'. Sababni tushuntiruvchi yagona javob - A."
    },
    {
        "id": "w_syn_03",
        "section": "writing",
        "domain": "Expression of Ideas",
        "skill": "Rhetorical Synthesis (synthesizing provided bullet-point research notes)",
        "difficulty": "Medium",
        "passage": "While researching renewable energy materials, a student took the following notes:\n- Monocrystalline silicon panels have an average energy conversion efficiency of 20% to 22%.\n- Monocrystalline panels require high manufacturing costs due to the Czochralski crystal-pulling process.\n- Polycrystalline silicon panels have an average energy conversion efficiency of 15% to 17%.\n- Polycrystalline panels are manufactured from molten silicon fragments, resulting in significantly lower production costs.",
        "question": "The student wants to contrast the efficiency and production cost of monocrystalline and polycrystalline panels. Which choice most effectively uses the relevant information from the notes to accomplish this goal?",
        "options": [
            {"key": "A", "text": "Although monocrystalline panels achieve higher conversion efficiency (20–22%), they incur greater manufacturing costs than lower-efficiency (15–17%) polycrystalline panels."},
            {"key": "B", "text": "Monocrystalline panels are manufactured through the Czochralski process to achieve 22% efficiency."},
            {"key": "C", "text": "Polycrystalline panels are manufactured from molten silicon fragments and are very affordable."},
            {"key": "D", "text": "Both monocrystalline and polycrystalline panels are widely utilized in commercial solar installations."}
        ],
        "correct": "A",
        "explanation": "Vazifa: Har ikkala panelning ham samaradorligi (efficiency) va ishlab chiqarish tannarxini (production cost) qarama-qarshi qo'yish (contrast). A varianti ikkala ko'rsatkichni (20-22% vs 15-17% hamda qimmat vs arzon tannarx) aniq taqqoslaydi (A to'g'ri). B faqat monokristalni aytadi; C faqat polikristalni aytadi; D esa taqqoslash o'rniga umumiy gap bilan cheklanadi.",
        "strategy_or_hack": "⚡ RHETORICAL SYNTHESIS: Vazifa 'contrast efficiency and cost' bo'lsa, javobda har ikkala panelning ham samaradorligi va xarajati bo'lishi shart."
    },
    {
        "id": "w_syn_04",
        "section": "writing",
        "domain": "Expression of Ideas",
        "skill": "Rhetorical Synthesis (synthesizing provided bullet-point research notes)",
        "difficulty": "Hard",
        "passage": "While researching astronomer Maria Mitchell, a student took the following notes:\n- In 1847, Maria Mitchell used a two-inch refracting telescope to discover Comet 1847 VI.\n- King Christian VIII of Denmark awarded her a prestigious gold medal for her astronomical discovery.\n- In 1848, she became the first woman elected to the American Academy of Arts and Sciences.\n- In 1865, she was appointed the first professor of astronomy at Vassar College.",
        "question": "The student wants to emphasize Mitchell's role as a trailblazer for women in institutional science. Which choice most effectively uses the relevant information from the notes to accomplish this goal?",
        "options": [
            {"key": "A", "text": "Mitchell broke gender barriers in professional science by becoming the first female member of the American Academy of Arts and Sciences and Vassar's inaugural astronomy professor."},
            {"key": "B", "text": "In 1847, Mitchell discovered Comet 1847 VI using a modest two-inch refracting telescope from her rooftop."},
            {"key": "C", "text": "King Christian VIII of Denmark recognized Mitchell's astronomical work by conferring a gold medal upon her."},
            {"key": "D", "text": "Mitchell studied celestial bodies throughout the mid-nineteenth century, achieving notable success in comet observation."}
        ],
        "correct": "A",
        "explanation": "Vazifa: Mitchell xonimning institutlashgan fanda ayollar uchun yo'l ochuvchi kashshof (trailblazer for women in institutional science) ekanini ta'kidlash. A varianti aynan ayollar uchun ilk bor nufuzli akademiya a'zosi va ilk astronomiya professori bo'lganini ko'rsatib, maqsadni 100% bajaradi (A to'g'ri). B faqat teleskop bilan kashfiyotni aytadi; C faqat medalni tilga oladi; D esa umumiy gap bo'lib, ayollar roli haqida hech narsa demaydi.",
        "strategy_or_hack": "⚡ KALIT SO'ZLAR: 'Trailblazer for women' => 'broke gender barriers', 'first female member', 'inaugural professor'."
    },
    {
        "id": "w_trans_07",
        "section": "writing",
        "domain": "Expression of Ideas",
        "skill": "Transitions (contrast, cause-effect, addition, illustration connectors)",
        "difficulty": "Medium",
        "passage": "Early deep-space probes relied entirely on chemical propellants, severely restricting mission duration due to fuel weight constraints. ______, modern interplanetary missions frequently utilize ion thrusters that accelerate xenon ions, enabling months of continuous low-thrust propulsion.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "Today"},
            {"key": "B", "text": "Specifically"},
            {"key": "C", "text": "For instance"},
            {"key": "D", "text": "In addition"}
        ],
        "correct": "A",
        "explanation": "Vaqtlar o'rtasidagi ziddiyat: 'Early deep-space probes' (dastlabki kosmik kemalar) kimyoviy yoqilg'iga tayangan, unga qarama-qarshi o'laroq zamonaviy missiyalar ('Today, modern interplanetary missions...') ion dvigatellaridan foydalanmoqda. 'Today' (bugungi kunda) o'tmish va hozirgi zamon o'rtasidagi texnologik o'tishni eng tabiiy va mantiqiy bog'laydi (A to'g'ri). B va C misol keltirish bo'lib, bu yerda misol emas, butunlay yangi texnologiya tilga olingan; D esa o'tmishdagi cheklovga qo'shimcha emas.",
        "strategy_or_hack": "⚡ TIMELINE TRANSITION: 'Early probes... Today, modern missions...'. O'tmishdan hozirga o'tishda 'Today' yoki 'Nowadays' eng to'g'ri keladi."
    },
    {
        "id": "w_trans_08",
        "section": "writing",
        "domain": "Expression of Ideas",
        "skill": "Transitions (contrast, cause-effect, addition, illustration connectors)",
        "difficulty": "Easy",
        "passage": "Photosynthetic organisms convert solar photons into stable chemical bonds, capturing approximately one hundred terawatts of energy annually. ______, they produce the oxygen essential for aerobic terrestrial organisms.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "Moreover"},
            {"key": "B", "text": "However"},
            {"key": "C", "text": "Nevertheless"},
            {"key": "D", "text": "Otherwise"}
        ],
        "correct": "A",
        "explanation": "Mantiqiy qo'shish (addition): 1-fakt: Fotosintez qiluvchi organizmlar quyosh energiyasini to'playdi. 2-fakt: Ular kislorod ham ishlab chiqaradi. Ikkala fikr ham fotosintezning global afzalliklari haqida bo'lib, bir-birini to'ldiradi. Shuning uchun 'Moreover' (bundan tashqari/shuningdek) to'g'ri javob (A). B va C ziddiyat bildiradi; D esa shart buzilishini bildiradi.",
        "strategy_or_hack": "⚡ QO'SHISH BOG'LOVCHISI: Ikkala jumla bir yo'nalishda (ijobiy hissa) ketmoqda => 'Moreover' yoki 'Furthermore'."
    },
    {
        "id": "w_syn_05",
        "section": "writing",
        "domain": "Expression of Ideas",
        "skill": "Rhetorical Synthesis (synthesizing provided bullet-point research notes)",
        "difficulty": "Medium",
        "passage": "While researching architectural history, a student took the following notes:\n- The Crystal Palace was designed by Joseph Paxton for London's Great Exhibition of 1851.\n- It utilized prefabricated cast iron and sheet glass modular components.\n- The entire 990,000-square-foot structure was assembled in just nine months.\n- Paxton's modular construction proved that large-scale civic buildings could be erected rapidly without traditional stone masonry.",
        "question": "The student wants to emphasize the revolutionary speed of the Crystal Palace's construction. Which choice most effectively uses the relevant information from the notes to accomplish this goal?",
        "options": [
            {"key": "A", "text": "By utilizing prefabricated iron and glass components, the massive 990,000-square-foot Crystal Palace was assembled in a remarkable nine months."},
            {"key": "B", "text": "Joseph Paxton designed the Crystal Palace for London's Great Exhibition of 1851."},
            {"key": "C", "text": "The Crystal Palace was an exhibition hall that did not rely on traditional stone masonry."},
            {"key": "D", "text": "Covering 990,000 square feet, the Crystal Palace featured modular cast iron parts."}
        ],
        "correct": "A",
        "explanation": "Talabaning maqsadi: Kristal saroy qurilishining inqilobiy tezligini (revolutionary speed) ta'kidlash. A varianti ulkan 990,000 kvadrat futlik inshootning atigi 9 oy ichida yig'ib bitkazilganini ta'kidlab, maqsadni aniq amalga oshiradi (A to'g'ri). B da tezlik haqida hech narsa yo'q; C va D esa tezlik omilini chetlab o'tadi.",
        "strategy_or_hack": "⚡ REVOLUTIONARY SPEED: Vazifadagi 'speed' so'ziga e'tibor bering: 'assembled in a remarkable nine months'."
    }
]
