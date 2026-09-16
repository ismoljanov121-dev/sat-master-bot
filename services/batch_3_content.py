"""
Batch 3 Content Data - 66 High Caliber Digital SAT Questions
"""

BATCH_3_DATA = [
    # =========================================================================
    # MATH: ALGEBRA (6 Questions)
    # =========================================================================
    {
        "id": "m_b3_alg_01",
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear equations in one variable",
        "difficulty": "Medium",
        "passage": None,
        "question": "Two water pumps, Pump A and Pump B, are filling a municipal reservoir. Pump A fills the reservoir at a constant rate of 120 gallons per minute, while Pump B fills it at a constant rate of 180 gallons per minute. If Pump A starts operating at 8:00 AM and Pump B starts at 8:30 AM, at what time will both pumps have contributed an equal total volume of water to the reservoir?",
        "options": [
            {"key": "A", "text": "9:30 AM"},
            {"key": "B", "text": "9:00 AM"},
            {"key": "C", "text": "10:00 AM"},
            {"key": "D", "text": "10:30 AM"}
        ],
        "correct": "A",
        "explanation": "Pump A 8:00 dan 8:30 gacha 30 daqiqa yolg'iz ishlagan: 120 * 30 = 3600 gallon to'ldirgan. 8:30 dan keyingi vaqtni t daqiqa deb olamiz. Pump A ning jami suvi: 3600 + 120t. Pump B ning jami suvi: 180t. Ular tenglashishi kerak: 3600 + 120t = 180t => 60t = 3600 => t = 60 daqiqa (1 soat). Demak, 8:30 dan 1 soat o'tgach, ya'ni soat 9:30 AM da ikkala nasos teng suv quygan bo'ladi. To'g'ri javob: A (9:30 AM). Noto'g'ri variantlar tahlili: B (9:00 AM) — yarim soat deb adashgandagi xato; C (10:00 AM) — 8:00 ga 2 soat qo'shib adashish tuzog'i; D (10:30 AM) — hisoblashdagi qo'pol xato variant.",
        "strategy_or_hack": "⚡ DESMOS USULI: Desmosga y = 120(x + 30) va y = 180x deb yozing. Kesishish nuqtasi x = 60 daqiqa bo'ladi. 8:30 + 60 daqiqa = 9:30 AM."
    },
    {
        "id": "m_b3_alg_02",
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear inequalities in one or two variables",
        "difficulty": "Medium",
        "passage": None,
        "question": "A truck rental company charges an initial reservation fee of $45 plus $0.80 per mile driven. An architect has a maximum budget of $225 for a one-day rental. What is the maximum number of miles the architect can drive without exceeding the budget?",
        "options": [
            {"key": "A", "text": "225"},
            {"key": "B", "text": "200"},
            {"key": "C", "text": "270"},
            {"key": "D", "text": "250"}
        ],
        "correct": "A",
        "explanation": "Tengsizlik tuzamiz: Jami xarajat 45 + 0.80m <= 225 bo'lishi kerak, bu yerda m — bosib o'tilgan masofa. 45 ni ayiramiz: 0.80m <= 180. Ikkala tomonni 0.80 ga bo'lamiz: m <= 180 / 0.80 = 225 mil. Demak, eng ko'pi bilan 225 mil yurish mumkin. To'g'ri javob: A (225). Noto'g'ri variantlar tahlili: B (200) — hisoblashda 0.8 o'rniga 0.9 ga bo'lish xatosi; C (270) — 45 ni ayirish o'rniga qo'shib yuborishdagi chalg'ituvchi tuzoq; D (250) — yaxlitlashdagi noo'rin xato natija.",
        "strategy_or_hack": "⚡ TEZ HISOBLASH: 180 / 0.8 = 1800 / 8 = 900 / 4 = 225. 5 soniyada tayyor!"
    },
    {
        "id": "m_b3_alg_03",
        "section": "math",
        "domain": "Algebra",
        "skill": "Systems of two linear equations in two variables",
        "difficulty": "Medium",
        "passage": None,
        "question": "Consider the system of equations:\n4x + 3y = 38\n2x - y = 4\nIf (x, y) is the solution to the system, what is the value of the product x * y?",
        "options": [
            {"key": "A", "text": "30"},
            {"key": "B", "text": "11"},
            {"key": "C", "text": "20"},
            {"key": "D", "text": "24"}
        ],
        "correct": "A",
        "explanation": "Ikkinchi tenglamadan y ni topamiz: y = 2x - 4. Buni birinchi tenglamaga qo'yamiz: 4x + 3(2x - 4) = 38 => 4x + 6x - 12 = 38 => 10x = 50 => x = 5. Endi y ni hisoblaymiz: y = 2(5) - 4 = 6. Savol x * y ko'paytmani so'ragan: 5 * 6 = 30. To'g'ri javob: A (30). Noto'g'ri variantlar tahlili: B (11) — x + y yig'indini belgilab qo'yish tuzog'i; C (20) — x=4 deb yanglishgandagi xato; D (24) — y ni topishda adashish natijasidagi noto'g'ri variant.",
        "strategy_or_hack": "⚡ DESMOS USULI: Ikkala tenglamani Desmosga kiriting. Kesishish nuqtasi (5, 6) chiqadi. 5 * 6 = 30."
    },
    {
        "id": "m_b3_alg_04",
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear equations in two variables",
        "difficulty": "Hard",
        "passage": None,
        "question": "The system of equations below has infinitely many solutions:\n6x - 9y = 21\nax - 6y = b\nwhere a and b are constants. What is the value of a + b?",
        "options": [
            {"key": "A", "text": "18"},
            {"key": "B", "text": "14"},
            {"key": "C", "text": "10"},
            {"key": "D", "text": "22"}
        ],
        "correct": "A",
        "explanation": "Cheksiz ko'p yechimga ega bo'lishi uchun koeffitsiyentlar nisbati teng bo'lishi shart: 6 / a = -9 / (-6) = 21 / b. O'rtadagi nisbat: -9 / (-6) = 3 / 2. 1) 6 / a = 3 / 2 => 3a = 12 => a = 4. 2) 21 / b = 3 / 2 => 3b = 42 => b = 14. Yig'indi: a + b = 4 + 14 = 18. To'g'ri javob: A (18). Noto'g'ri variantlar tahlili: B (14) — faqat b ning qiymatini belgilab qo'yish tuzog'i; C (10) — b - a ayirmani hisoblashdagi adashish; D (22) — ishorani noto'g'ri qo'llashdagi xato variant.",
        "strategy_or_hack": "⚡ PROPORSIONALLIK QOIDASI: 2-tenglamadagi y koeffitsiyenti (-6) 1-tenglamadagidan (-9) 2/3 barobar. Demak a = 6 * (2/3) = 4, b = 21 * (2/3) = 14. 4 + 14 = 18!"
    },
    {
        "id": "m_b3_alg_05",
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear inequalities in one or two variables",
        "difficulty": "Medium",
        "passage": None,
        "question": "A carpenter manufactures wooden bookshelves and desks. Each bookshelf requires 4 hours of assembly and 2 hours of finishing, while each desk requires 6 hours of assembly and 5 hours of finishing. The workshop has at most 60 hours for assembly and at most 40 hours for finishing available each week. If the carpenter builds 6 desks in a week, what is the maximum number of bookshelves that can also be manufactured without exceeding either hourly limit?",
        "options": [
            {"key": "A", "text": "5"},
            {"key": "B", "text": "6"},
            {"key": "C", "text": "4"},
            {"key": "D", "text": "7"}
        ],
        "correct": "A",
        "explanation": "Javonga b ta, stolga d ta deb belgilaymiz. Shart bo'yicha d = 6 ta stol yasalgan. Cheklovlar: 1) Yig'ish (assembly): 4b + 6(6) <= 60 => 4b + 36 <= 60 => 4b <= 24 => b <= 6. 2) Pardozlash (finishing): 2b + 5(6) <= 40 => 2b + 30 <= 40 => 2b <= 10 => b <= 5. Ikkala shart ham bajarilishi uchun b <= min(6, 5) = 5 bo'lishi kerak. Demak, eng ko'pi bilan 5 ta javon yasash mumkin. To'g'ri javob: A (5). Noto'g'ri variantlar tahlili: B (6) — faqat yig'ish vaqtini hisoblab pardozlash vaqtidan oshib ketish (2*6+30 = 42 > 40) xatosi tuzog'i; C (4) — mumkin bo'lsa-da, maksimal emas; D (7) — ikkala vaqtdan ham oshib ketadigan xato variant.",
        "strategy_or_hack": "⚡ IKKALA CHEKLOVNI TEKSHIRISH: Ikkinchi shart b <= 5 ni talab qiladi. 6 qo'yilsa vaqt yetmaydi!"
    },
    {
        "id": "m_b3_alg_06",
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear equations in one variable",
        "difficulty": "Hard",
        "passage": None,
        "question": "What is the product of all real solutions to the equation |2x - 5| + 3 = 14?",
        "options": [
            {"key": "A", "text": "-24"},
            {"key": "B", "text": "5"},
            {"key": "C", "text": "-11"},
            {"key": "D", "text": "24"}
        ],
        "correct": "A",
        "explanation": "Modulni ajratamiz: |2x - 5| = 14 - 3 = 11. Ikkita holat mavjud: 1) 2x - 5 = 11 => 2x = 16 => x1 = 8. 2) 2x - 5 = -11 => 2x = -6 => x2 = -3. Ildizlar ko'paytmasi: x1 * x2 = 8 * (-3) = -24. To'g'ri javob: A (-24). Noto'g'ri variantlar tahlili: B (5) — ildizlar yig'indisini hisoblab qo'yish tuzog'i; C (-11) — modul qiymatining o'zini olishdagi xato; D (24) — manfiy ishorani tashlab ketishdagi xato variant.",
        "strategy_or_hack": "⚡ DESMOS USULI: y = abs(2x - 5) + 3 va y = 14 chiziqlarini chizing. Kesishish nuqtalari x = -3 va x = 8. Ularning ko'paytmasi -24."
    },

    # =========================================================================
    # MATH: ADVANCED MATH (7 Questions)
    # =========================================================================
    {
        "id": "m_b3_adv_01",
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Nonlinear equations in one variable (quadratic, radical, absolute value)",
        "difficulty": "Medium",
        "passage": None,
        "question": "For what value of constant c does the quadratic equation 2x^2 - 8x + c = 0 have exactly one distinct real solution?",
        "options": [
            {"key": "A", "text": "8"},
            {"key": "B", "text": "16"},
            {"key": "C", "text": "4"},
            {"key": "D", "text": "-8"}
        ],
        "correct": "A",
        "explanation": "Kvadrat tenglama yagona haqiqiy yechimga ega bo'lishi uchun diskriminant nolga teng bo'lishi shart (D = 0): D = b^2 - 4ac = (-8)^2 - 4(2)(c) = 64 - 8c. 64 - 8c = 0 => 8c = 64 => c = 8. To'g'ri javob: A (8). Noto'g'ri variantlar tahlili: B (16) — a=1 deb adashganda olinadigan tuzoq; C (4) — 64 ni 16 ga bo'lishdagi xato; D (-8) — ishorani teskari olishdagi xato variant.",
        "strategy_or_hack": "⚡ SAT FORMULASI: Yagona yechim uchun c = b^2 / (4a) = 64 / 8 = 8."
    },
    {
        "id": "m_b3_adv_02",
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Nonlinear functions (quadratic vertex/standard form, exponential models, polynomials)",
        "difficulty": "Hard",
        "passage": None,
        "question": "Consider the nonlinear system of equations:\ny = x^2 - 4x + 7\ny = 2x - 1\nIf (x1, y1) and (x2, y2) are the two distinct solutions with x1 < x2, what is the value of y2 - y1?",
        "options": [
            {"key": "A", "text": "4"},
            {"key": "B", "text": "2"},
            {"key": "C", "text": "6"},
            {"key": "D", "text": "8"}
        ],
        "correct": "A",
        "explanation": "Ikkala y ni tenglashtiramiz: x^2 - 4x + 7 = 2x - 1 => x^2 - 6x + 8 = 0. Ko'paytuvchilarga ajratamiz: (x - 2)(x - 4) = 0. Bundan x1 = 2 va x2 = 4 (chunki x1 < x2). Tegishli y qiymatlarni topamiz: y1 = 2(2) - 1 = 3; y2 = 2(4) - 1 = 7. Ayirma: y2 - y1 = 7 - 3 = 4. To'g'ri javob: A (4). Noto'g'ri variantlar tahlili: B (2) — x2 - x1 ayirmani adashib belgilash tuzog'i; C (6) — arifmetik hisoblashdagi xato; D (8) — x1 va x2 ni qo'shib yuborishdagi xato variant.",
        "strategy_or_hack": "⚡ DESMOS USULI: Ikkala funksiyani kiriting. Kesishish nuqtalari (2, 3) va (4, 7). y koordinatalar ayirmasi: 7 - 3 = 4."
    },
    {
        "id": "m_b3_adv_03",
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Equivalent expressions (factoring, polynomial arithmetic)",
        "difficulty": "Medium",
        "passage": None,
        "question": "Which of the following is equivalent to the expression (3x^2 - 12) / (x^2 + 5x + 6) for all values of x > 0?",
        "options": [
            {"key": "A", "text": "(3x - 6) / (x + 3)"},
            {"key": "B", "text": "(3x + 6) / (x + 3)"},
            {"key": "C", "text": "3 / (5x + 2)"},
            {"key": "D", "text": "(x - 2) / (x + 3)"}
        ],
        "correct": "A",
        "explanation": "Surat va maxrajni ko'paytuvchilarga ajratamiz: Surat: 3(x^2 - 4) = 3(x - 2)(x + 2). Maxraj: (x + 2)(x + 3). Umumiy ko'paytuvchi (x + 2) ni qisqartiramiz: 3(x - 2) / (x + 3) = (3x - 6) / (x + 3). To'g'ri javob: A. Noto'g'ri variantlar tahlili: B — suratdagi ishorani musbat deb adashish tuzog'i; C — x^2 larni noo'rin bekor qilib yuborishdagi qo'pol xato; D — 3 umumiy ko'paytuvchini yo'qotib qo'yishdagi xato variant.",
        "strategy_or_hack": "⚡ SON QO'YISH USULI: x = 1 qo'ying: Asl ifoda: (3 - 12)/(1 + 5 + 6) = -9/12 = -0.75. A variantda: (3 - 6)/(1 + 3) = -3/4 = -0.75. Mos keldi!"
    },
    {
        "id": "m_b3_adv_04",
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Nonlinear functions (quadratic vertex/standard form, exponential models, polynomials)",
        "difficulty": "Easy",
        "passage": None,
        "question": "A sample of a radioactive isotope has an initial mass of 320 milligrams. The mass decays by half every 18 days. Which function M(d) models the remaining mass, in milligrams, after d days?",
        "options": [
            {"key": "A", "text": "M(d) = 320 * (0.5)^(d/18)"},
            {"key": "B", "text": "M(d) = 320 * (0.5)^(18d)"},
            {"key": "C", "text": "M(d) = 320 * (2)^(-18d)"},
            {"key": "D", "text": "M(d) = 160 * (0.5)^(d/18)"}
        ],
        "correct": "A",
        "explanation": "Yarim parchalanish eksponensial formulasi: M(d) = M0 * (0.5)^(d / davr). Bu yerda M0 = 320 mg va davr = 18 kun. Demak M(d) = 320 * (0.5)^(d/18). To'g'ri javob: A. Noto'g'ri variantlar tahlili: B — davrni darajaga ko'paytirib qo'yish tuzog'i; C — asos va ko'paytuvchini almashtirish xatosi; D — boshlang'ich massani darhol 2 ga bo'lib 160 deb yozish xatosi.",
        "strategy_or_hack": "⚡ TEKSHIRISH: d = 18 da massa roppa-rosa 2 barobar kamayishi (160 mg) kerak. A da: 320 * (0.5)^1 = 160 to'g'ri chiqadi!"
    },
    {
        "id": "m_b3_adv_05",
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Nonlinear equations in one variable (quadratic, radical, absolute value)",
        "difficulty": "Hard",
        "passage": None,
        "question": "What is the set of all real solutions to the radical equation sqrt(4x + 9) = x - 3?",
        "options": [
            {"key": "A", "text": "{10}"},
            {"key": "B", "text": "{0, 10}"},
            {"key": "C", "text": "{0}"},
            {"key": "D", "text": "No real solutions"}
        ],
        "correct": "A",
        "explanation": "Ikkala tomonni kvadratga ko'taramiz: 4x + 9 = (x - 3)^2 = x^2 - 6x + 9. Hadlarni bir tomonga o'tkazamiz: x^2 - 10x = 0 => x(x - 10) = 0. Nomzod ildizlar: x = 0 va x = 10. Endi chet ildizlarni tekshiramiz: 1) x = 0: sqrt(9) = 3, lekin o'ng tomon 0 - 3 = -3. 3 != -3, demak x = 0 chet ildiz (noto'g'ri). 2) x = 10: sqrt(49) = 7, o'ng tomon 10 - 3 = 7. 7 = 7 to'g'ri. Shuning uchun yagona haqiqiy yechim {10}. To'g'ri javob: A ({10}). Noto'g'ri variantlar tahlili: B ({0, 10}) — chet ildizni tekshirmasdan belgilashdagi eng xavfli tuzoq; C ({0}) — faqat chet ildizni olish xatosi; D — haqiqiy yechim yo'q deb noto'g'ri xulosa chiqarish.",
        "strategy_or_hack": "⚡ CHET ILDIZ OGOHLANTIRISHI: Ildizli tenglamani kvadratga ko'targanda har doim o'ng tomon manfiy bo'lmasligini tekshiring: x - 3 >= 0 => x >= 3 bo'lishi shart! x = 0 bu shartni bajarmaydi."
    },
    {
        "id": "m_b3_adv_06",
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Equivalent expressions (factoring, polynomial arithmetic)",
        "difficulty": "Hard",
        "passage": None,
        "question": "When the polynomial P(x) = 2x^3 - 5x^2 + kx - 14 is divided by (x - 3), the remainder is 7. What is the value of the constant k?",
        "options": [
            {"key": "A", "text": "4"},
            {"key": "B", "text": "-4"},
            {"key": "C", "text": "6"},
            {"key": "D", "text": "8"}
        ],
        "correct": "A",
        "explanation": "Qoldiqli bo'lish teoremasi (Remainder Theorem) bo'yicha: P(3) = 7 bo'lishi kerak. x = 3 ni qo'yamiz: P(3) = 2(3)^3 - 5(3)^2 + k(3) - 14 = 2(27) - 5(9) + 3k - 14 = 54 - 45 + 3k - 14 = 3k - 5. Shart bo'yicha: 3k - 5 = 7 => 3k = 12 => k = 4. To'g'ri javob: A (4). Noto'g'ri variantlar tahlili: B (-4) — ishorada adashganda kelib chiqadigan tuzoq; C (6) — arifmetik hisoblashdagi xato; D (8) — ozod hadni noto'g'ri o'tkazishdagi xato variant.",
        "strategy_or_hack": "⚡ POLINOM QOIDASI: P(x) ni (x - c) ga bo'lgandagi qoldiq P(c) ga teng. x=3 ni qo'yib 7 ga tenglang!"
    },
    {
        "id": "m_b3_adv_07",
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Nonlinear functions (quadratic vertex/standard form, exponential models, polynomials)",
        "difficulty": "Medium",
        "passage": None,
        "question": "What is the minimum value of the quadratic function g(x) = 3x^2 - 24x + 55?",
        "options": [
            {"key": "A", "text": "7"},
            {"key": "B", "text": "4"},
            {"key": "C", "text": "55"},
            {"key": "D", "text": "-7"}
        ],
        "correct": "A",
        "explanation": "Parabolaning shoxlari yuqoriga qaragan (a = 3 > 0), shuning uchun uning eng kichik qiymati cho'qqisida (vertex) bo'ladi. Cho'qqining x koordinatasi: x = -b / (2a) = -(-24) / (2 * 3) = 24 / 6 = 4. Eng kichik qiymat g(4) ga teng: g(4) = 3(4)^2 - 24(4) + 55 = 3(16) - 96 + 55 = 48 - 96 + 55 = 7. To'g'ri javob: A (7). Noto'g'ri variantlar tahlili: B (4) — minimum nuqtani (x koordinatani) qiymat deb adashib belgilash klassik tuzog'i; C (55) — y-kesishmasini minimum deb o'ylash xatosi; D (-7) — ishora xatosi natijasidagi noto'g'ri variant.",
        "strategy_or_hack": "⚡ DESMOS USULI: Desmosga y = 3x^2 - 24x + 55 ni kiriting va eng pastki nuqtani bosing: (4, 7). Minimum qiymat y = 7!"
    },

    # =========================================================================
    # MATH: PROBLEM-SOLVING AND DATA ANALYSIS (7 Questions)
    # =========================================================================
    {
        "id": "m_b3_ps_01",
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Two-way tables, probability, and conditional probability",
        "difficulty": "Medium",
        "passage": None,
        "question": "A survey of 200 university students recorded their major and mathematics course enrollment. Among the 80 Science majors, 60 enrolled in Statistics and 20 in Calculus. Among the 120 Humanities majors, 30 enrolled in Statistics and 90 in Calculus. If a student who enrolled in Statistics is selected at random, what is the probability that the student is a Science major?",
        "options": [
            {"key": "A", "text": "2/3"},
            {"key": "B", "text": "3/4"},
            {"key": "C", "text": "3/10"},
            {"key": "D", "text": "1/2"}
        ],
        "correct": "A",
        "explanation": "Shartli ehtimollik formulasi: P(Science | Statistics) = N(Science va Statistics) / N(Jami Statistics). Statistics kursiga yozilganlar jami soni: 60 (Science) + 30 (Humanities) = 90 nafar. Ularning ichidan Science yo'nalishidagi talabalar soni: 60 nafar. Ehtimollik: 60 / 90 = 2/3. To'g'ri javob: A (2/3). Noto'g'ri variantlar tahlili: B (3/4) — 60 / 80 deb Science talabalari ichidan hisoblash tuzog'i; C (3/10) — 60 / 200 deb butun talabalar soniga bo'lish xatosi; D (1/2) — guruhlarni teng deb faraz qilishdagi xato variant.",
        "strategy_or_hack": "⚡ SHARTLI EHTIMOLLIK KALITI: 'If a student who enrolled in Statistics...' so'zlari maxraj faqat Statistics olganlar (60+30=90) bo'lishini bildiradi!"
    },
    {
        "id": "m_b3_ps_02",
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Percentages (percent increase/decrease, multi-step word problems)",
        "difficulty": "Medium",
        "passage": None,
        "question": "An online retailer increased the price of a wireless keyboard by 25% in November. In January, the retailer discounted the new price by 20%. What was the overall percentage change from the original price?",
        "options": [
            {"key": "A", "text": "0% (The price remained unchanged)"},
            {"key": "B", "text": "5% increase"},
            {"key": "C", "text": "5% decrease"},
            {"key": "D", "text": "1% decrease"}
        ],
        "correct": "A",
        "explanation": "Multiplikator usulini qo'llaymiz: Dastlabki narx P bo'lsin. 1) 25% oshish: P * 1.25. 2) 20% arzonlashish: yangi narx * (1 - 0.20) = P * 1.25 * 0.80. Ko'paytiramiz: 1.25 * 0.80 = 1.00. Demak yakuniy narx 1.00 * P ga teng, ya'ni narx o'zgarmagan (0% o'zgarish). To'g'ri javob: A. Noto'g'ri variantlar tahlili: B (5% increase) — 25% - 20% = +5% deb foizlarni oddiy ayirib yuboradigan eng mashhur SAT tuzog'i; C (5% decrease) — adashgan yo'nalish; D — noo'rin yaxlitlashdagi xato variant.",
        "strategy_or_hack": "⚡ QULAY SON TANLASH: Dastlabki narxni $100 deb oling: 25% oshsa $125 bo'ladi. $125 ning 20%i = $25. $125 - $25 = $100. Qaytib o'ziga keldi (0%)!"
    },
    {
        "id": "m_b3_ps_03",
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Inference from sample statistics and margin of error",
        "difficulty": "Hard",
        "passage": None,
        "question": "A research institute surveyed a random sample of 1,200 registered voters in a metropolitan area regarding a new transit tax. The survey found that 58% supported the tax, with a margin of error of 2.8% at a 95% confidence level. Which of the following is the most appropriate conclusion?",
        "options": [
            {"key": "A", "text": "It is plausible that the true proportion of all registered voters in the metropolitan area who support the tax is between 55.2% and 60.8%."},
            {"key": "B", "text": "Exactly 58% of all registered voters in the metropolitan area support the tax."},
            {"key": "C", "text": "95% of all registered voters in the metropolitan area support the tax."},
            {"key": "D", "text": "The true proportion of voters supporting the tax cannot be greater than 58%."}
        ],
        "correct": "A",
        "explanation": "Ishonch oralig'i (confidence interval) hisoblanadi: 58% +- 2.8%, ya'ni [55.2%, 60.8%]. Bu butun populyatsiyadagi haqiqiy ulush ushbu oraliqda bo'lishi asosli (plausible) ekanligini bildiradi. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B — tanlanma natijasini butun aholi uchun qat'iy 'aynan 58%' deb e'lon qilish statistikaga zid tuzoq; C — 95% ishonchlilik darajasini qo'llab-quvvatlovchilar ulushi deb adashtirish xatosi; D — oraliq yuqori chegarasi 60.8% gacha borishini inkor etuvchi xato variant.",
        "strategy_or_hack": "⚡ SAT STATISTIKA QOIDASI: 'Margin of error' har doim interval beradi (58 - 2.8 dan 58 + 2.8 gacha). 'Exactly' yoki 'cannot' so'zlari bo'lgan variantlar deyarli har doim noto'g'ri!"
    },
    {
        "id": "m_b3_ps_04",
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Ratios, rates, proportional relationships, and units",
        "difficulty": "Easy",
        "passage": None,
        "question": "A solid metal alloy block has a volume of 450 cubic centimeters. The density of the alloy is 7.8 grams per cubic centimeter. What is the mass of the block in kilograms? (1 kilogram = 1,000 grams)",
        "options": [
            {"key": "A", "text": "3.51"},
            {"key": "B", "text": "35.1"},
            {"key": "C", "text": "0.351"},
            {"key": "D", "text": "3,510"}
        ],
        "correct": "A",
        "explanation": "Massa formulasi: m = Zichlik * Hajm = 7.8 g/cm^3 * 450 cm^3 = 3510 gramm. Grammdan kilogrammga o'tkazamiz: 3510 / 1000 = 3.51 kg. To'g'ri javob: A (3.51). Noto'g'ri variantlar tahlili: B (35.1) — 100 ga bo'lishdagi xato; C (0.351) — 10000 ga bo'lishdagi vergul surilishi xatosi; D (3,510) — massani grammda qoldirib, kilogrammga o'tkazishni unutish klassik tuzog'idir.",
        "strategy_or_hack": "⚡ BIRLIKLAR ZANJIRI: 450 cm^3 * (7.8 g / 1 cm^3) * (1 kg / 1000 g) = 3510 / 1000 = 3.51 kg."
    },
    {
        "id": "m_b3_ps_05",
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Scatterplots, linear/exponential/quadratic models, and residuals",
        "difficulty": "Medium",
        "passage": None,
        "question": "A scatterplot displays the weekly practice hours x and test scores y for 20 students. The line of best fit is given by y_pred = 6.5x + 48. One student practiced for 6 hours and achieved an actual score of 92. What is the residual (actual score minus predicted score) for this student?",
        "options": [
            {"key": "A", "text": "5"},
            {"key": "B", "text": "-5"},
            {"key": "C", "text": "87"},
            {"key": "D", "text": "92"}
        ],
        "correct": "A",
        "explanation": "1) Bashorat qilingan ballni hisoblaymiz: y_pred = 6.5(6) + 48 = 39 + 48 = 87. 2) Qoldiq (residual) = Haqiqiy ball - Bashorat qilingan ball = 92 - 87 = +5. To'g'ri javob: A (+5). Noto'g'ri variantlar tahlili: B (-5) — ayirmani teskari (bashorat - haqiqiy) hisoblashdagi ishora tuzog'i; C (87) — bashorat qilingan ballning o'zini belgilash xatosi; D (92) — haqiqiy ballning o'zini qoldiq deb o'ylash xatosi.",
        "strategy_or_hack": "⚡ RESIDUAL QOIDASI: Residual = Actual - Predicted (y - y_hat). Nuqta chiziqdan yuqorida bo'lsa, musbat qoldiq bo'ladi!"
    },
    {
        "id": "m_b3_ps_06",
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Measures of center (mean, median) and spread (range, standard deviation)",
        "difficulty": "Medium",
        "passage": None,
        "question": "A dataset contains 9 test scores: 72, 74, 76, 78, 80, 82, 84, 86, 88. An outlier with a score of 20 is added to the dataset. Which statement correctly compares the median and mean of the new 10-score dataset with the original 9-score dataset?",
        "options": [
            {"key": "A", "text": "Both the mean and the median decrease, but the mean decreases by a greater amount."},
            {"key": "B", "text": "Both the mean and the median decrease, but the median decreases by a greater amount."},
            {"key": "C", "text": "The median remains unchanged, while the mean decreases."},
            {"key": "D", "text": "The mean remains unchanged, while the median decreases."}
        ],
        "correct": "A",
        "explanation": "Dastlabki 9 ta son simmetrik: mediana = 80, o'rtacha qiymat (mean) = 80. Yangi ro'yxat: 20, 72, 74, 76, 78, 80, 82, 84, 86, 88. 1) Yangi mediana = (78 + 80) / 2 = 79 (1 ga kamaydi). 2) Yangi o'rtacha qiymat = (720 + 20) / 10 = 74 (6 ga kamaydi). Ikkalasi ham kamayadi, lekin o'rtacha qiymat ancha ko'proq kamayadi (-6 ga qarshi -1). To'g'ri javob: A. Noto'g'ri variantlar tahlili: B — medianani kutilmagan ko'rsatkichlarga ta'sirchan deb o'ylash xatosi; C va D — o'zgarishsiz qoladi deb noto'g'ri hisoblash tuzoqlari.",
        "strategy_or_hack": "⚡ SAT KONSEPSIYASI: O'rtacha qiymat (mean) anomal qiymatlarga (outliers) nihoyatda sezgir, mediana esa ancha mustahkam (resistant) turadi!"
    },
    {
        "id": "m_b3_ps_07",
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Percentages (percent increase/decrease, multi-step word problems)",
        "difficulty": "Hard",
        "passage": None,
        "question": "Account A starts with $1,000 and earns 8% interest compounded annually. Account B starts with $1,500 and earns $100 simple interest each year. After 15 years, which account has the greater total balance, and by approximately how much?",
        "options": [
            {"key": "A", "text": "Account A, by approximately $172"},
            {"key": "B", "text": "Account B, by approximately $172"},
            {"key": "C", "text": "Account B, by approximately $300"},
            {"key": "D", "text": "Both accounts have equal balances"}
        ],
        "correct": "A",
        "explanation": "1) Account A (murakkab foiz): 1000 * (1 + 0.08)^15 = 1000 * (1.08)^15. 1.08^15 taxminan 3.17217 ga teng => Balans = $3,172. 2) Account B (oddiy foiz): 1500 + 15 * 100 = 1500 + 1500 = $3,000. Account A ko'proq: $3,172 - $3,000 = $172. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B — Account B katta deb xato tanlash; C — dastlabki farqni $300 deb o'ylash tuzog'i; D — tenglashadi deb yanglishishdagi xato variant.",
        "strategy_or_hack": "⚡ DESMOS USULI: Desmosga 1000 * 1.08^15 va 1500 + 15*100 ni yozing. 3172.17 va 3000 chiqadi. Ayirmasi 172.17!"
    },

    # =========================================================================
    # MATH: GEOMETRY AND TRIGONOMETRY (6 Questions)
    # =========================================================================
    {
        "id": "m_b3_geom_01",
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Circles (arc length, sector area, equation of a circle)",
        "difficulty": "Medium",
        "passage": None,
        "question": "In the xy-plane, what is the radius of the circle defined by the equation x^2 + y^2 - 8x + 6y - 11 = 0?",
        "options": [
            {"key": "A", "text": "6"},
            {"key": "B", "text": "36"},
            {"key": "C", "text": "4"},
            {"key": "D", "text": "11"}
        ],
        "correct": "A",
        "explanation": "To'la kvadratga ajratamiz: (x^2 - 8x + 16) + (y^2 + 6y + 9) = 11 + 16 + 9. (x - 4)^2 + (y + 3)^2 = 36. Aylananing standart tenglamasi: (x - h)^2 + (y - k)^2 = r^2. r^2 = 36 bo'lgani uchun radius r = sqrt(36) = 6. To'g'ri javob: A (6). Noto'g'ri variantlar tahlili: B (36) — r^2 ni radius deb adashib belgilash klassik tuzog'i; C (4) — markazning x koordinatasi; D (11) — tenglamadagi ozod hadni olishdagi xato variant.",
        "strategy_or_hack": "⚡ RADUS TEZKOR FORMULASI: r = sqrt((d/2)^2 + (e/2)^2 - f) = sqrt(4^2 + (-3)^2 - (-11)) = sqrt(16 + 9 + 11) = sqrt(36) = 6."
    },
    {
        "id": "m_b3_geom_02",
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Circles (arc length, sector area, equation of a circle)",
        "difficulty": "Medium",
        "passage": None,
        "question": "A circular community garden has a diameter of 20 meters. A triangular floral sector formed by central radii OA and OB subtends a central angle of 72 degrees. What is the area of this sector, in square meters?",
        "options": [
            {"key": "A", "text": "20pi"},
            {"key": "B", "text": "40pi"},
            {"key": "C", "text": "10pi"},
            {"key": "D", "text": "80pi"}
        ],
        "correct": "A",
        "explanation": "Diametr 20 metr bo'lsa, radius r = 20 / 2 = 10 metr bo'ladi. To'liq aylananing yuzi: S_doira = pi * r^2 = pi * (10)^2 = 100pi. 72 gradusli sektorning to'liq doiradagi ulushi: 72 / 360 = 1 / 5 qism. Sektor yuzi: S_sektor = (1 / 5) * 100pi = 20pi m^2. To'g'ri javob: A (20pi). Noto'g'ri variantlar tahlili: B (40pi) — radius o'rniga diametrni (20) qo'yib yuborish tuzog'i; C (10pi) — yuzani noto'g'ri bo'lishdagi xato; D (80pi) — 400pi / 5 deb diametr bilan xato hisoblashdagi variant.",
        "strategy_or_hack": "⚡ TEZKOR NISBAT: 72° / 360° = 1/5. Doira yuzi pi*10^2 = 100pi. 100pi / 5 = 20pi!"
    },
    {
        "id": "m_b3_geom_03",
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Right triangles and trigonometry",
        "difficulty": "Medium",
        "passage": None,
        "question": "In right triangle ABC, the measure of angle C is 90 degrees. If sin(A) = 7/25, what is the value of cos(B)?",
        "options": [
            {"key": "A", "text": "7/25"},
            {"key": "B", "text": "24/25"},
            {"key": "C", "text": "25/7"},
            {"key": "D", "text": "7/24"}
        ],
        "correct": "A",
        "explanation": "To'g'ri burchakli uchburchakda o'tkir burchaklar yig'indisi 90 gradus: A + B = 90. Qo'shimcha burchaklar trigonometrik qoidasi (cofunction identity): sin(A) = cos(90 - A) = cos(B). Shuning uchun cos(B) ham aynan 7/25 ga teng bo'ladi. To'g'ri javob: A (7/25). Noto'g'ri variantlar tahlili: B (24/25) — sin(B) yoki cos(A) ni hisoblab qo'yish tuzog'i; C (25/7) — kasrni to'ntarib qo'yish xatosi; D (7/24) — tangens qiymati bilan adashtirishdagi xato variant.",
        "strategy_or_hack": "⚡ SAT COFUNCTION QOIDASI: Har qanday to'g'ri burchakli uchburchakda sin(A) = cos(B) doimo tengdir!"
    },
    {
        "id": "m_b3_geom_04",
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Area and volume",
        "difficulty": "Hard",
        "passage": None,
        "question": "Triangle PQR is similar to triangle XYZ, where vertices P, Q, and R correspond to X, Y, and Z, respectively. The length of side PQ is 6, and the length of corresponding side XY is 15. If the area of triangle PQR is 24 square centimeters, what is the area of triangle XYZ, in square centimeters?",
        "options": [
            {"key": "A", "text": "150"},
            {"key": "B", "text": "60"},
            {"key": "C", "text": "120"},
            {"key": "D", "text": "240"}
        ],
        "correct": "A",
        "explanation": "O'xshashlik koeffitsiyenti k = XY / PQ = 15 / 6 = 5/2 = 2.5. O'xshash figuralarning maydonlari nisbati o'xshashlik koeffitsiyentining kvadratiga teng (k^2): Area(XYZ) = Area(PQR) * k^2 = 24 * (5/2)^2 = 24 * (25 / 4) = 6 * 25 = 150 sm^2. To'g'ri javob: A (150). Noto'g'ri variantlar tahlili: B (60) — maydonni k ga (kvadratsiz) ko'paytirib qo'yishdagi klassik tuzoq (24 * 2.5 = 60); C (120) va D (240) — noto'g'ri ko'paytirishdagi chalg'ituvchi xato variantlar.",
        "strategy_or_hack": "⚡ MAYDON VA HAJM QOIDASI: Chiziqli o'lcham k marta kattalashsa, maydon k^2 marta, hajm esa k^3 marta ortadi!"
    },
    {
        "id": "m_b3_geom_05",
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Area and volume",
        "difficulty": "Easy",
        "passage": None,
        "question": "A cylindrical water storage tank has a base diameter of 8 meters and a height of 10 meters. What is the total volume of the tank, in cubic meters?",
        "options": [
            {"key": "A", "text": "160pi"},
            {"key": "B", "text": "640pi"},
            {"key": "C", "text": "80pi"},
            {"key": "D", "text": "40pi"}
        ],
        "correct": "A",
        "explanation": "Asos diametri d = 8 m bo'lsa, radiusi r = d / 2 = 4 m bo'ladi. Silindr hajmi formulasi: V = pi * r^2 * h = pi * (4)^2 * 10 = pi * 16 * 10 = 160pi m^3. To'g'ri javob: A (160pi). Noto'g'ri variantlar tahlili: B (640pi) — radius o'rniga diametrni (8^2=64) qo'yib yuborish tuzog'i; C (80pi) — formuladagi r^2 o'rniga r*h deb adashish xatosi; D (40pi) — konus formulasini (1/3 yoki 1/4) noo'rin qo'llashdagi xato variant.",
        "strategy_or_hack": "⚡ DIQQAT: Diametr berilganda doimo birinchi ish uni 2 ga bo'lib radiusni (r = 4) topishdir!"
    },
    {
        "id": "m_b3_geom_06",
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Right triangles and trigonometry",
        "difficulty": "Medium",
        "passage": None,
        "question": "In an equilateral triangle DEF, each side has a length of 14. What is the exact length of the altitude of triangle DEF?",
        "options": [
            {"key": "A", "text": "7 * sqrt(3)"},
            {"key": "B", "text": "7 * sqrt(2)"},
            {"key": "C", "text": "7"},
            {"key": "D", "text": "14 * sqrt(3)"}
        ],
        "correct": "A",
        "explanation": "Teng tomonli uchburchakning balandligi uni ikkita 30-60-90 to'g'ri burchakli uchburchakka ajratadi. Gipotenuza = 14, 30 gradus qarshisidagi katet (asosning yarmi) = 7. 60 gradus qarshisidagi balandlik: h = asos_kateti * sqrt(3) = 7 * sqrt(3). To'g'ri javob: A. Noto'g'ri variantlar tahlili: B — 45-45-90 uchburchak bilan adashtirib sqrt(2) olish xatosi; C (7) — faqat asosning yarmini belgilash tuzog'i; D — gipotenuzaga sqrt(3) ni ko'paytirib qo'yishdagi xato variant.",
        "strategy_or_hack": "⚡ FORMULA: Tomoni s bo'lgan muntazam uchburchak balandligi h = s * sqrt(3) / 2 = 14 * sqrt(3) / 2 = 7*sqrt(3)."
    },

    # =========================================================================
    # READING: CRAFT AND STRUCTURE (10 Questions)
    # =========================================================================
    {
        "id": "r_b3_cs_01",
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Words in Context",
        "difficulty": "Hard",
        "passage": "In her critical appraisal of the nineteenth-century realist novel, literary scholar Elena Vance noted that the protagonist's outward submission to societal norms was merely a pragmatic concession; beneath this compliant exterior lay a fierce and uncompromising commitment to personal autonomy.",
        "question": "As used in the text, what does the word 'concession' most nearly mean?",
        "options": [
            {"key": "A", "text": "compromise"},
            {"key": "B", "text": "privilege"},
            {"key": "C", "text": "rebate"},
            {"key": "D", "text": "admittance"}
        ],
        "correct": "A",
        "explanation": "Matnda bosh qahramonning jamiyat qoidalariga tashqaridan bo'ysunishi shunchaki 'pragmatic concession' (amaliy yon berish, murosaga kelish) ekani aytilmoqda, uning ichida esa avtonomiyaga qat'iy sadoqat bor edi. 'Concession' bu yerda murosaga kelish (compromise / yielding) ma'nosini bildiradi. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B (privilege - imtiyoz) — kontekstdagi yon berish ma'nosiga zid; C (rebate - chegirma) — tijoriy ma'no; D (admittance - kirishga ruxsat) — noo'rin leksik chalg'ituvchi variantlardir.",
        "strategy_or_hack": "⚡ KONTEKSTUAL QARAMA-QARSHILIK: 'outward submission' va 'uncompromising commitment' orasidagi muvozanat 'compromise' (murosa) ekanini aniqlab beradi."
    },
    {
        "id": "r_b3_cs_02",
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Words in Context",
        "difficulty": "Medium",
        "passage": "The desert dwelling architecture of the Ancestral Puebloans was strikingly austere, characterized by unadorned sandstone masonry and compact cliffside layouts that maximized thermal retention while minimizing material waste.",
        "question": "As used in the text, what does the word 'austere' most nearly mean?",
        "options": [
            {"key": "A", "text": "simple and unornamented"},
            {"key": "B", "text": "hostile and perilous"},
            {"key": "C", "text": "fragile and temporary"},
            {"key": "D", "text": "luxurious and sprawling"}
        ],
        "correct": "A",
        "explanation": "Matnda me'morchilik 'unadorned sandstone masonry' (bezaksiz qumtosh terimi) va ixcham loyihalar bilan tasvirlangan. Bu 'austere' so'zining oddiy, dabdabasiz va bezaksiz (simple and unornamented) ma'nosini to'liq ochib beradi. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B (xavfli) — sahro muhitiga qarab adashiladigan tuzoq; C (mo'rt) — tosh terim mustahkam bo'lgani sababli matnga zid; D (hashamatli) — to'g'ridan-to'g'ri antonim bo'lgan xato variant.",
        "strategy_or_hack": "⚡ KALIT SO'ZLAR: 'unadorned' (bezaksiz) so'zi 'austere'ning to'g'ridan-to'g'ri sinonimik izohidir."
    },
    {
        "id": "r_b3_cs_03",
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Words in Context",
        "difficulty": "Hard",
        "passage": "Dr. Aris Thorne took scrupulous care to verify every spectral measurement, refusing to publish the planetary discovery until multiple independent observatories confirmed the precise orbital perturbations.",
        "question": "As used in the text, what does the word 'scrupulous' most nearly mean?",
        "options": [
            {"key": "A", "text": "meticulous and thorough"},
            {"key": "B", "text": "reluctant and hesitant"},
            {"key": "C", "text": "hasty and impulsive"},
            {"key": "D", "text": "skeptical and hostile"}
        ],
        "correct": "A",
        "explanation": "Olim har bir o'lchovni sinchiklab tekshirgani ('verify every measurement') va bir nechta mustaqil rasadxonalar tasdiqlamaguncha nashr qilmagani uning favqulodda puxta va ehtiyotkor (meticulous and thorough) yondashganini ko'rsatadi. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B (ikkilanuvchi) — ilmiy ehtiyotkorlik ikkilanish emas; C (shoshqaloq) — matn mantiqiga mutlaqo zid; D (dushmanona) — ilmiy auditni salbiy his-tuyg'u bilan adashtiruvchi xato variant.",
        "strategy_or_hack": "⚡ SIFAT-HARAKAT MOSLIGI: 'verify every... refusing to publish until confirmed' harakati kishining 'meticulous' (o'ta sinchkov) ekanini bildiradi."
    },
    {
        "id": "r_b3_cs_04",
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Words in Context",
        "difficulty": "Medium",
        "passage": "Because the alpine ecosystem endures such ephemeral growing seasons—sometimes lasting fewer than six weeks—high-altitude flora must initiate rapid flowering immediately after the snowpack recedes.",
        "question": "As used in the text, what does the word 'ephemeral' most nearly mean?",
        "options": [
            {"key": "A", "text": "short-lived"},
            {"key": "B", "text": "predictable"},
            {"key": "C", "text": "vigorous"},
            {"key": "D", "text": "destructive"}
        ],
        "correct": "A",
        "explanation": "Tirelar orasidagi izohga e'tibor bering: 'sometimes lasting fewer than six weeks' (ba'zan olti haftadan ham kam davom etadi). Bu o'sish mavsumining juda qisqa muddatli va o'tkinchi (short-lived / transient) ekanini aniq ko'rsatadi. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B (oldindan aytib bo'ladigan) — mavsum uzunligi bilan bog'liq emas; C (shiddatli) — o'simliklar harakatini mavsumga taalluqli deb adashish; D (halokatli) — matnga zid chalg'ituvchi variant.",
        "strategy_or_hack": "⚡ PUNKTUATSIYA SIGNALI: Matndagi tirelar (—lasting fewer than six weeks—) qiyin so'zning to'g'ridan-to'g'ri ta'rifini beradi!"
    },
    {
        "id": "r_b3_cs_05",
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Cross-Text Connections",
        "difficulty": "Hard",
        "passage": "Text 1:\nHistorical ecologist Jeremy Miller argues that total fire exclusion policies in western pine forests have disrupted natural regenerative cycles. By preventing low-intensity understory blazes, these policies allow combustible organic debris to accumulate, inadvertently priming forests for catastrophic, uncontrollable mega-fires.\n\nText 2:\nConservation specialist Maya Patel cautions against aggressive prescribed burning programs, noting that changing climate regimes have made previously predictable ignition windows perilous. Low-intensity burns frequently escape containment boundaries due to unexpected drought winds, inflicting severe mortality on mature canopy trees.",
        "question": "Based on the texts, how would Maya Patel (Text 2) most likely respond to Jeremy Miller's perspective (Text 1)?",
        "options": [
            {"key": "A", "text": "By emphasizing that attempting to reintroduce fires carries substantial modern risks that may outweigh the theoretical ecological benefits"},
            {"key": "B", "text": "By agreeing that total fire exclusion has completely eliminated the threat of catastrophic canopy mega-fires"},
            {"key": "C", "text": "By arguing that low-intensity understory burns have never played a historical role in forest regeneration"},
            {"key": "D", "text": "By asserting that prescribed fires are consistently easier to control during severe drought conditions"}
        ],
        "correct": "A",
        "explanation": "Text 1 muallifi past intensivlikdagi yong'inlar o'rmonni katta ofatlardan saqlaydi deb yong'inga ruxsat berishni yoqlaydi. Ammo Text 2 muallifi Maya Patel iqlim o'zgarishi sababli bunday nazoratli yong'inlar shamol tufayli chegaradan chiqib ketayotganini va xavfi juda yuqoriligini ta'kidlaydi. Demak u Millerga zamonaviy xatarlar kutilayotgan ekologik foydadan ustun kelishi mumkinligini aytib javob beradi. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B — Text 1 ga to'liq qo'shilish deb yanglishish; C — Patel tarixiy rolni inkor etmaydi, zamonaviy xatarni aytadi; D — Patelning fikriga to'g'ridan-to'g'ri zid xato variant.",
        "strategy_or_hack": "⚡ IKKITA MATN QIYOSI: Har doim ikkala muallifning 'to'qnashuv nuqtasi'ni toping: Miller = 'yong'in kerak', Patel = 'hozir uni yoqish o'ta xavfli'."
    },
    {
        "id": "r_b3_cs_06",
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Text Structure and Purpose",
        "difficulty": "Medium",
        "passage": "Biologists long presumed that deep-sea vent tubeworms derived nutrition exclusively by filtering organic detritus falling from the photic zone. However, Colleen Cavanaugh demonstrated in 1981 that the worms harbor sulfur-oxidizing bacteria in a specialized organ called a trophosome. This symbiotic relationship allows the worms to thrive on toxic hydrothermal chemical emissions, upending traditional understandings of oceanic energy webs.",
        "question": "Which choice best describes the overall structure of the text?",
        "options": [
            {"key": "A", "text": "It presents a longstanding scientific consensus, introduces groundbreaking research that refuted it, and notes the broader implications of that discovery."},
            {"key": "B", "text": "It outlines an unresolved biological controversy and proposes a novel experimental method to settle it."},
            {"key": "C", "text": "It chronicles the lifelong academic career of an oceanographer and catalogues her various publications."},
            {"key": "D", "text": "It describes a peculiar marine organism and argues that it represents an evolutionary dead end."}
        ],
        "correct": "A",
        "explanation": "Matn avval uzoq vaqt hukm surgan qarashni taqdim etadi ('Biologists long presumed...'), so'ngra 'However' burilishi bilan Cavanaughning yangi kashfiyotini keltiradi ('demonstrated that...'), va oxirida buning keng qamrovli oqibatini xulosa qiladi ('upending traditional understandings...'). Bu tuzilma A variantga 100% mos keladi. Noto'g'ri variantlar tahlili: B — bahs hal etilmagan deyilmagan (hal etilgan); C — olimning butun umri xronikasi berilmagan; D — organizmni 'evolyutsion boshi berk ko'cha' deb noo'rin xulosalash xatosi.",
        "strategy_or_hack": "⚡ RETORIK STRUKTURA: 'Long presumed... However, [Scientist] demonstrated... upending understandings' = Consensus -> Refutation -> Broader Impact."
    },
    {
        "id": "r_b3_cs_07",
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Cross-Text Connections",
        "difficulty": "Hard",
        "passage": "Text 1:\nEconomist Liam Vance argues that the rapid automation of routine warehousing tasks inevitably benefits regional economies by reducing supply-chain bottlenecks, lowering shipping consumer prices, and driving capital investment into higher-margin technical design sectors.\n\nText 2:\nSociologist Nadia Ortiz points out that while aggregate regional GDP metrics may rise following automation, the benefits are heavily skewed toward capital owners. Displaced warehouse workers rarely transition into technical design roles; instead, they face prolonged wage stagnation or involuntary transition into precarious, low-wage service jobs.",
        "question": "Based on the texts, how does Nadia Ortiz (Text 2) view the economic outcome described by Liam Vance (Text 1)?",
        "options": [
            {"key": "A", "text": "She contends that aggregate macroeconomic gains obscure severe distributional inequalities and employment hardships for displaced workers."},
            {"key": "B", "text": "She wholly rejects Vance's claim that automated supply chains achieve lower operating expenses."},
            {"key": "C", "text": "She maintains that automated warehouses will eventually return to manual labor due to technical unreliability."},
            {"key": "D", "text": "She enthusiastically supports Vance's projection that low-skill laborers effortlessly shift into high-margin engineering positions."}
        ],
        "correct": "A",
        "explanation": "Text 1 makroiqtisodiy yutuqlar (arzon narxlar, investitsiya) haqida gapiradi. Text 2 muallifi Ortiz esa umumiy YaIM o'sishi ortida daromadlarning faqat sarmoyadorlarga o'tishi va oddiy ishchilarning ishsizlik va maosh tushishiga uchrashi yashiringanini ta'kidlaydi ('benefits heavily skewed... displaced workers face wage stagnation'). Shuning uchun Ortiz umumiy yutuqlar jiddiy tengsizlikni yashirib qo'yadi deb hisoblaydi (A to'g'ri). Noto'g'ri variantlar tahlili: B — xarajatlar tushishini inkor qilmaydi; C — qo'l mehnatiga qaytadi demaydi; D — matnga mutlaqo zid xato variant.",
        "strategy_or_hack": "⚡ ASOSIY FARQ: Vance makro darajadagi foydani, Ortiz esa ishchilar darajasidagi tengsizlikni (distributional inequality) ko'rsatadi."
    },
    {
        "id": "r_b3_cs_08",
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Text Structure and Purpose",
        "difficulty": "Medium",
        "passage": "To understand how geckos adhere to vertical glass without secretions, Kellar Autumn examined the microscopic structure of their toe pads. Electron microscopy revealed millions of microscopic setae, each branching into hundreds of nanoscale spatulae. Autumn calculated that the collective van der Waals forces between these spatulae and the surface generate sufficient electromagnetic attraction to suspend the lizard's weight.",
        "question": "Which choice best states the primary purpose of the text?",
        "options": [
            {"key": "A", "text": "To explain the physical mechanism that enables geckos to climb smooth surfaces without liquids"},
            {"key": "B", "text": "To compare the adhesion efficiency of geckos with synthetic chemical glues"},
            {"key": "C", "text": "To dispute the existence of van der Waals forces in terrestrial animals"},
            {"key": "D", "text": "To argue that geckos are the only animals capable of vertical locomotion"}
        ],
        "correct": "A",
        "explanation": "Matn boshidanoq gekkonlarning suyuqliksiz silliq oynaga qanday yopishishini tushuntirish maqsadini qo'yadi va mikroskopik tukchalar hamda van-der-Vaals kuchlari mexanizmini bayon qiladi. Demak, asosiy maqsad bu fizik mexanizmni tushuntirishdir (A to'g'ri). Noto'g'ri variantlar tahlili: B — sun'iy yelimlar bilan solishtirilmagan; C — van-der-Vaals kuchlarini rad etmaydi, aksincha tasdiqlaydi; D — faqat gekkonlar chiqa oladi degan haddan tashqari umumlashtiruvchi xato variant.",
        "strategy_or_hack": "⚡ MATN MAQSADI: Matn nima uchun yozilgan? Birinchi gap: 'To understand how geckos adhere...'. Javob A to'g'ridan-to'g'ri shuni aks ettiradi."
    },
    {
        "id": "r_b3_cs_09",
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Words in Context",
        "difficulty": "Hard",
        "passage": "While the board members publicly praised the interim director's ambitious restructuring proposals, their private correspondence revealed a tacit consensus that none of the disruptive initiatives would ever be enacted.",
        "question": "As used in the text, what does the word 'tacit' most nearly mean?",
        "options": [
            {"key": "A", "text": "unspoken and implied"},
            {"key": "B", "text": "reluctantly documented"},
            {"key": "C", "text": "legally binding"},
            {"key": "D", "text": "hostile and contentious"}
        ],
        "correct": "A",
        "explanation": "Matnda rasman omma oldida maqtashsa-da, o'zaro shaxsiy munosabatlarda bu rejalarni amalga oshirmaslik bo'yicha og'zaki aytilmagan, lekin bir-birini tushungan kelishuv ('tacit consensus') bo'lgani aytilmoqda. 'Tacit' so'zi so'zsiz anglashilgan, bildirilmagan (unspoken / implied) degan ma'noni beradi. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B (hujjatlashtirilgan) — tacit so'zining tabiatiga zid; C (qonuniy) — norasmiy kelishuv; D (janjalli) — qarama-qarshilikni so'z ma'nosiga noo'rin yuklash xatosi.",
        "strategy_or_hack": "⚡ LUG'AT HACK: 'Tacit' = so'zsiz tushunilgan (unspoken, implied, understood without being stated)."
    },
    {
        "id": "r_b3_cs_10",
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Text Structure and Purpose",
        "difficulty": "Easy",
        "passage": "In 1828, Friedrich Wöhler heated ammonium cyanate—an inorganic salt—and unexpectedly produced urea, an organic compound previously believed to arise only through the biological 'vital force' of living organisms. Wöhler's accidental synthesis effectively bridged organic and inorganic chemistry, proving that biological molecules obey identical physical laws as inanimate matter.",
        "question": "Which choice best describes the function of the second sentence in the text as a whole?",
        "options": [
            {"key": "A", "text": "It explains the historical and theoretical significance of the experimental result described in the first sentence."},
            {"key": "B", "text": "It questions the methodological rigor of the scientist's laboratory procedures."},
            {"key": "C", "text": "It introduces a conflicting perspective from contemporary organic chemists."},
            {"key": "D", "text": "It provides biographical context regarding the scientist's early academic education."}
        ],
        "correct": "A",
        "explanation": "Birinchi gapda Wöhlerning tajribasi va u tasodifan mochevina olgani aytilgan. Ikkinchi gap esa bu natijaning kimyo fanidagi ulkan tarixiy va nazariy ahamiyatini ('effectively bridged... proving that biological molecules obey identical physical laws') tushuntirib beradi. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B — metodologik xatolik haqida gap yo'q; C — boshqa olimlarning zid fikri kiritilmagan; D — tarjimai hol yoki bolaligi haqida ma'lumot berilmagan.",
        "strategy_or_hack": "⚡ GAPLAR ALOQASI: 1-gap tajriba faktini beradi, 2-gap uning fanga ta'sirini (significance) tushuntiradi."
    },

    # =========================================================================
    # READING: INFORMATION AND IDEAS (10 Questions)
    # =========================================================================
    {
        "id": "r_b3_ii_01",
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Central Ideas and Details",
        "difficulty": "Medium",
        "passage": "Mycorrhizal fungal networks weave through forest soils, connecting the root systems of geographically separated trees. Ecologists have discovered that these subterranean networks actively redistribute carbon, nitrogen, and phosphorus from thriving canopy trees to light-deprived saplings. Furthermore, when mature trees suffer insect herbivory, they transmit biochemical warning cues through the mycelium, prompting neighboring trees to preemptively synthesize chemical pest defenses.",
        "question": "Which choice best summarizes the central idea of the text?",
        "options": [
            {"key": "A", "text": "Underground fungal networks function as dynamic conduits that facilitate both nutrient distribution and biochemical communication among forest trees."},
            {"key": "B", "text": "Light-deprived saplings routinely outcompete mature canopy trees by parasitizing fungal root colonies."},
            {"key": "C", "text": "Insects intentionally sever mycorrhizal fungal threads to prevent trees from manufacturing defensive chemicals."},
            {"key": "D", "text": "Forest soils lack sufficient inorganic minerals without direct artificial nutrient supplementation."}
        ],
        "correct": "A",
        "explanation": "Matnda mikoriza qo'ziqorin tarmoqlari daraxtlar orasida ozuqa moddalarini (uglerod, azot, fosfor) taqsimlashi hamda zararkunandalar hujumi paytida biokimyoviy ogohlantirish signallarini uzatishi bayon etilgan. Bu A variantdagi 'dynamic conduits for nutrient distribution and biochemical communication' jumlasida to'liq aks etgan. Noto'g'ri variantlar tahlili: B — yosh nihollar katta daraxtlarni yengadi degan da'vo matnda yo'q; C — hasharotlar tarmoqni uzib tashlashi aytilmagan; D — sun'iy o'g'it haqida hech narsa deyilmagan.",
        "strategy_or_hack": "⚡ ASOSIY G'OYA: Matndagi ikkita asosiy dalilni (1: ozuqa taqsimoti, 2: ogohlantirish signali) bitta gapda birlashtirgan variantni tanlang!"
    },
    {
        "id": "r_b3_ii_02",
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Command of Evidence (Textual)",
        "difficulty": "Hard",
        "passage": "In studying ancient maritime commerce in the Baltic Sea, historian Henrik Lund hypothesized that the fourteenth-century expansion of the Hanseatic League was driven more by monopolistic legal privileges granted by regional monarchs than by superior merchant naval technology. To substantiate this hypothesis, Lund must identify historical evidence demonstrating that rival non-Hanseatic merchants possessed vessels of equivalent maritime capability but were excluded through statutory barriers.",
        "question": "Which finding, if true, would most directly support Lund's hypothesis?",
        "options": [
            {"key": "A", "text": "Dutch merchant cogs matched Hanseatic ships in cargo capacity and navigational range but were barred from Baltic ports under royal charter agreements that granted exclusive trading monopolies to Hanseatic guilds."},
            {"key": "B", "text": "Hanseatic shipwrights engineered innovative double-hulled vessels that withstood northern storms far better than any contemporary European craft."},
            {"key": "C", "text": "Regional monarchs continuously raised customs duties equally on all foreign merchant vessels regardless of their guild affiliations."},
            {"key": "D", "text": "Non-Hanseatic merchants willingly abandoned Baltic shipping routes due to widespread domestic textile shortages in Flanders."}
        ],
        "correct": "A",
        "explanation": "Lundning farazi: Ganza ligasining ustunligi kema texnologiyasidan emas, balki qirollar bergan monopol huquqiy imtiyozlardan kelib chiqqan. Buning uchun raqib kemalar texnik jihatdan teng bo'lsa-da, qonuniy to'siqlar tufayli portlarga kiritilmaganini isbotlash kerak. A variant aynan shuni ko'rsatadi: golland kemalari sig'imi va masofasi bo'yicha teng bo'lgan, biroq qirollik shartnomalari tufayli portlardan chiqarib qo'yilgan. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B — texnologik ustunlikni aytib, gipotezaga qarshi ishlaydi; C — barcha savdogarlardan teng boj olingan bo'lsa, monopol imtiyoz gipotezasi puchga chiqadi; D — texnologiya yoki qonuniy to'siqqa aloqasi yo'q xato variant.",
        "strategy_or_hack": "⚡ GIPOTEZANI TASDIQLASH: Gipoteza 'Texnologiya emas, qonuniy to'siq' degan. Demak, javobda 'Texnologiya bir xil, lekin qonun bilan taqiqlangan' dalili bo'lishi shart!"
    },
    {
        "id": "r_b3_ii_03",
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Command of Evidence (Quantitative)",
        "difficulty": "Medium",
        "passage": "Energy engineers conducted a 500-cycle degradation trial evaluating four utility-scale battery chemistries. They recorded initial capacity retention and internal resistance increases. Lithium iron phosphate (LFP) retained 94% capacity with a 6% resistance gain; nickel manganese cobalt (NMC) retained 88% capacity with a 14% resistance gain; sodium-ion retained 82% capacity with a 18% resistance gain; and lead-carbon retained 71% capacity with a 29% resistance gain. The researchers concluded that LFP demonstrates the greatest electrochemical stability under repeated cycling.",
        "question": "Which choice best uses data from the passage to support the researchers' conclusion?",
        "options": [
            {"key": "A", "text": "LFP achieved the highest capacity retention (94%) and the lowest internal resistance increase (6%) among all four tested chemistries."},
            {"key": "B", "text": "Lead-carbon batteries exhibited lower internal resistance increases than sodium-ion batteries."},
            {"key": "C", "text": "NMC batteries retained more capacity than LFP batteries throughout the 500-cycle trial."},
            {"key": "D", "text": "All four battery chemistries maintained capacity retention above 85% after 500 cycles."}
        ],
        "correct": "A",
        "explanation": "Tadqiqotchilar LFP kimyosi eng barqaror deb xulosa qilishgan. Buni matndagi raqamlar bilan tasdiqlash uchun LFP ning ko'rsatkichlari eng yaxshi ekanini ko'rsatish kerak: u eng yuqori sig'im saqlashga (94%) va eng kam ichki qarshilik o'sishiga (6%) ega bo'ldi. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B — matnga zid (qo'rg'oshin 29%, natriy 18%); C — matnga zid (NMC 88% < LFP 94%); D — matnga zid (faqat LFP va NMC 85% dan yuqori, qolganlari 82% va 71%).",
        "strategy_or_hack": "⚡ RAQAMLARNI SOLISHTIRISH: Matndagi jadval ma'lumotlarini qat'iy tekshiring va 'superlativ' (eng yuqori/eng past) ko'rsatkichga e'tibor bering."
    },
    {
        "id": "r_b3_ii_04",
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Inferences",
        "difficulty": "Hard",
        "passage": "Many deep-sea organisms utilize bioluminescent counterillumination to evade predators hunting from below. By emitting downward-directed light from ventral photophores that matches the intensity and wavelength of downwelling sunlight, these creatures disguise their silhouettes. Marine ecologist Sarah Hirst observed that when mesopelagic squids encounter artificial water turbidity that scatters sunlight irregularly, their photophore adjustments become mismatched with ambient light, suggesting that ______",
        "question": "Which choice most logically completes the text?",
        "options": [
            {"key": "A", "text": "their counterillumination camouflage relies on uniform ambient light fields to effectively obscure their silhouettes."},
            {"key": "B", "text": "turbid waters provide superior camouflage protection compared to clear oceanic zones."},
            {"key": "C", "text": "mesopelagic squids migrate into shallower waters when oceanic turbidity increases."},
            {"key": "D", "text": "ventral photophores generate light through external bacterial digestion rather than biochemical reactions."}
        ],
        "correct": "A",
        "explanation": "Matnda kalmarlarning pastga yo'naltirilgan nuri tushayotgan quyosh nuriga moslashib siluetni yashirishi aytilgan. Biroq loyqa suv yorug'likni notekis tarqatganda kalmarlarning nuri atrof-muhitga mos kelmay qolgan. Bundan mantiqiy xulosa: ularning bu kamuflyaji samarali ishlashi uchun bir tekis (uniform) yorug'lik maydoniga tayanadi. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B — loyqa suv yaxshiroq himoya beradi degan matnga teskari da'vo; C — sayoz suvga ko'chib o'tadi degan asossiz taxmin; D — bakterial hazm haqida matnda hech qanday ma'lumot yo'q.",
        "strategy_or_hack": "⚡ MANTIQIY DAVOM: Sabab-oqibat zanjiri: loyqalik nur muvozanatini buzdi -> demak tizim bir tekis yorug'likka bog'liq!"
    },
    {
        "id": "r_b3_ii_05",
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Central Ideas and Details",
        "difficulty": "Easy",
        "passage": "Obsidian, a naturally occurring volcanic glass, was among the most prized materials in Neolithic tool manufacturing. Because each volcanic deposit possesses a unique chemical fingerprint of trace elements, modern archaeologists can use X-ray fluorescence spectrometry to trace obsidian blades discovered at distant settlement sites back to their precise quarry of origin, thereby reconstructing trade networks that spanned thousands of kilometers across prehistoric Anatolia.",
        "question": "According to the text, why are modern archaeologists able to identify the geographic origins of ancient obsidian blades?",
        "options": [
            {"key": "A", "text": "Each volcanic source has a distinct chemical composition of trace elements that can be detected through spectrometry."},
            {"key": "B", "text": "Neolithic toolmakers inscribed distinctive geographical symbols onto every blade."},
            {"key": "C", "text": "Ancient trade treaties detailing raw material shipments were preserved in Anatolian archives."},
            {"key": "D", "text": "Obsidian blades change physical color based on the geographical distance they travel."}
        ],
        "correct": "A",
        "explanation": "Matnda ochiq-oydin aytilgan: 'Because each volcanic deposit possesses a unique chemical fingerprint of trace elements, modern archaeologists can use X-ray fluorescence spectrometry to trace obsidian blades... back to their precise quarry of origin'. Bu A variantga to'liq mos keladi. Noto'g'ri variantlar tahlili: B — pichoqlarga geografik belgilar yozilgani haqida gap yo'q; C — arxivalar saqlangani aytilmagan; D — masofaga qarab rang o'zgarishi kabi ilmiy bo'lmagan chalg'ituvchi variant.",
        "strategy_or_hack": "⚡ TO'G'RIDAN-TO'G'RI MATN ASOSI: 'Because each volcanic deposit possesses a unique chemical fingerprint...' so'zlarini javob bilan solishtiring."
    },
    {
        "id": "r_b3_ii_06",
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Command of Evidence (Textual)",
        "difficulty": "Hard",
        "passage": "Linguists investigating phonological acquisition have debated whether infants identify word boundaries primarily by tracking statistical transitional probabilities between syllables or by responding to acoustic stress patterns. To demonstrate that statistical learning operates independently of acoustic stress, researcher Marcus Gable presented eight-month-old infants with a stream of synthesized speech in which all syllables were uttered with identical pitch, duration, and volume, but with specific syllable pairs occurring in predictable sequences.",
        "question": "Which finding from Gable's experiment, if true, would most strongly support the statistical learning hypothesis?",
        "options": [
            {"key": "A", "text": "The infants displayed significantly greater listening interest in novel syllable combinations than in the predictable syllable pairs from the stream."},
            {"key": "B", "text": "The infants showed no measurable reaction to any syllable sequence unless pitch and volume varied noticeably."},
            {"key": "C", "text": "The infants recognized words only when the synthesized voices resembled their primary caregivers' voices."},
            {"key": "D", "text": "The infants struggled to perceive individual syllables when background white noise was eliminated."}
        ],
        "correct": "A",
        "explanation": "Kognitiv psixologiyada chaqaloqlar o'rgangan narsasidan ko'ra yangi narsaga ko'proq e'tibor qaratadi (novelty preference). Agar chaqaloqlar bir xil ohang va balandlikdagi oqimdan so'ng yangi kombinatsiyalarga ko'proq quloq solsa, bu ularning statistik ketma-ketlikni eslab qolganini va yangisini farqlay olganini isbotlaydi. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B — ohangsiz hech narsani sezmadi desa gipotezani rad etgan bo'ladi; C — ona ovozi sharti matnda sinovdan chiqarilgan; D — oq shovqin haqida matnda ma'lumot yo'q.",
        "strategy_or_hack": "⚡ CHAQALOQLAR PSIXOLOGIYASI TESTI: O'rganilgan so'zlarni tanish chaqaloqning 'novel' (yangi) so'zlarga uzoqroq quloq solishi (preferential listening) orqali o'lchanadi."
    },
    {
        "id": "r_b3_ii_07",
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Inferences",
        "difficulty": "Medium",
        "passage": "In cognitive psychology, retrieval-induced forgetting occurs when the act of practicing the recall of certain items from memory causes the temporary suppression of related, unpracticed items. For instance, repeatedly reviewing the word pair 'Fruit-Apple' impairs subsequent recall of 'Fruit-Banana.' Neuroimaging indicates that this suppression is driven by prefrontal inhibitory control mechanisms that resolve competition during memory access. Thus, retrieval-induced forgetting demonstrates that ______",
        "question": "Which choice most logically completes the text?",
        "options": [
            {"key": "A", "text": "forgetting is not merely a passive decay of information, but can result from active cognitive mechanisms that suppress competing memories."},
            {"key": "B", "text": "human memory has a rigid, finite capacity that permanently deletes older memories to store new data."},
            {"key": "C", "text": "practicing recall is generally harmful to academic test preparation."},
            {"key": "D", "text": "all memory retrieval is unmediated by prefrontal neurological circuits."}
        ],
        "correct": "A",
        "explanation": "Matnda miyadagi tormozlash mexanizmi (inhibitory control) raqobatdosh xotiralarni faol ravishda bosib turishi (suppress) ko'rsatilgan. Bundan mantiqiy xulosa shuki, unutish shunchaki xotiraning o'z-o'zidan passiv o'chib ketishi (passive decay) emas, balki miyaning faol boshqaruv mexanizmi natijasidir. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B — xotira ma'lumotni butunlay o'chirib tashlaydi degan noto'g'ri da'vo (matnda 'temporary suppression' deyilgan); C — takrorlash o'qishga zarar degan mantiqsiz umumlashtirish; D — neyron zanjirlarga aloqador emas degan matnga teskari xato variant.",
        "strategy_or_hack": "⚡ MATN XULOSASI: 'active suppression by inhibitory control' = xotira passiv yo'qolmaydi, faol tormozlanadi."
    },
    {
        "id": "r_b3_ii_08",
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Command of Evidence (Textual)",
        "difficulty": "Medium",
        "passage": "Botanist Linda Perez investigated whether urban plants adapt to elevated ground-level ozone by altering stomatal conductance. In a controlled greenhouse study, she exposed common plantain (Plantago major) seedlings from both rural roadside populations and dense inner-city populations to identical ozone concentrations (80 ppb) for four weeks. Perez observed that inner-city plants exhibited significantly lower stomatal conductance and accumulated 40% less cellular oxidative damage than rural specimens.",
        "question": "Which statement is best supported by Perez's findings?",
        "options": [
            {"key": "A", "text": "Inner-city populations of Plantago major possess adaptive traits that limit ozone uptake and subsequent oxidative damage."},
            {"key": "B", "text": "Rural plants are better suited to withstand high ozone concentrations than urban varieties."},
            {"key": "C", "text": "Elevated ozone exposure consistently increases stomatal conductance across all plant species."},
            {"key": "D", "text": "Plantago major is incapable of surviving in environments with ground-level ozone levels above 40 ppb."}
        ],
        "correct": "A",
        "explanation": "Shaharda o'sgan o'simliklar qishloqdagilarga nisbatan kamroq og'izcha o'tkazuvchanligiga ega bo'lib, 40% kamroq oksidlanish zarari ko'rgan. Bu ularning shahar muhitida ozon gazining kirishini cheklaydigan moslashuvchan (adaptive) xususiyatlarga ega ekanini to'liq tasdiqlaydi. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B — qishloq o'simliklari bardoshliroq degan matnga teskari da'vo; C — barcha turlarda o'tkazuvchanlik oshadi degan xato; D — 40 ppb dan yuqorida yashay olmaydi degan asossiz cheklov.",
        "strategy_or_hack": "⚡ DALILNI MOSLASHTIRISH: Kamroq zarar ko'rgan (40% less damage) = yaxshiroq moslashgan (possess adaptive traits)."
    },
    {
        "id": "r_b3_ii_09",
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Inferences",
        "difficulty": "Hard",
        "passage": "Astronomers surveying debris disks around mature G-type stars noted that secondary gas emissions—principally carbon monoxide—are replenished through volatile-rich comet collisions rather than surviving from the primordial protoplanetary nebula. Because carbon monoxide is rapidly photodissociated by stellar ultraviolet radiation within a few thousand years, its persistent presence in multi-billion-year-old stellar systems implies that ______",
        "question": "Which choice most logically completes the text?",
        "options": [
            {"key": "A", "text": "cometary collision rates remain sufficiently frequent in these systems to continuously regenerate the dissipated gas."},
            {"key": "B", "text": "primordial gas nebulae are completely immune to stellar ultraviolet photodissociation."},
            {"key": "C", "text": "mature G-type stars gradually stop emitting ultraviolet radiation as they age."},
            {"key": "D", "text": "planetary formation is physically impossible in systems containing carbon monoxide debris disks."}
        ],
        "correct": "A",
        "explanation": "Agar CO gazi yulduz nurlari ta'sirida bir necha ming yilda yo'qolib ketsa-yu, lekin milliard yillik qadimgi yulduz tizimlarida hamon mavjud bo'lsa, bu yangi gaz doimiy ravishda kometa to'qnashuvlari orqali qayta ishlab chiqarilayotganini bildiradi. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B — gaz nurlanishga chidamli degan matnga teskari gap (matnda 'rapidly photodissociated' deyilgan); C — yulduzlar ultrabinafsha nurlanishni to'xtatadi degan asossiz faraz; D — sayyora paydo bo'lishi mumkin emas degan xato radikal xulosa.",
        "strategy_or_hack": "⚡ MANTIQIY TENGSIZLIK: Gaz tez yo'qoladi + lekin hali ham bor = yangi gaz muntazam paydo bo'lyapti (continuously regenerated)!"
    },
    {
        "id": "r_b3_ii_10",
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Central Ideas and Details",
        "difficulty": "Easy",
        "passage": "Before the advent of reliable refrigeration in the nineteenth century, harvesting natural ice from northern ponds and rivers was a vital global industry. Entrepreneurs like Frederic Tudor harvested frozen blocks in New England, insulated them in double-walled holds packed with sawdust, and successfully shipped thousands of tons of ice to tropical destinations such as Havana, Kingston, and Calcutta with remarkably little melt loss.",
        "question": "Which choice best describes how Frederic Tudor minimized melt loss during maritime ice transportation?",
        "options": [
            {"key": "A", "text": "By stowing the ice blocks in double-walled holds insulated with sawdust"},
            {"key": "B", "text": "By chemically treating the pond water prior to freezing"},
            {"key": "C", "text": "By transporting ice exclusively during the mid-winter months on steamships"},
            {"key": "D", "text": "By compressing the ice blocks into airtight vacuum chambers"}
        ],
        "correct": "A",
        "explanation": "Matnda to'g'ridan-to'g'ri ko'rsatilgan: 'insulated them in double-walled holds packed with sawdust' (qipiq bilan to'ldirilgan ikki qavatli devorli xonalarda saqlagan). To'g'ri javob: A. Noto'g'ri variantlar tahlili: B — muzlashdan oldin kimyoviy ishlov berish aytilmagan; C — faqat qishda bug'li kemalarda tashigan deyilmagan; D — vakuum kamerasiga qisish degan noto'g'ri fantastik variant.",
        "strategy_or_hack": "⚡ MATN DETALI: Matndagi 'insulated them in double-walled holds packed with sawdust' iborasini qidiring."
    },

    # =========================================================================
    # WRITING: STANDARD ENGLISH CONVENTIONS (10 Questions)
    # =========================================================================
    {
        "id": "w_b3_sec_01",
        "section": "writing",
        "domain": "Standard English Conventions",
        "skill": "Boundaries (complete sentences, comma splices, run-ons, fragments)",
        "difficulty": "Medium",
        "passage": "The archival research team uncovered three previously unpublished letters by author Mary ______ were meticulous reflections on the social turbulence of early Victorian England.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "Shelley; all of them"},
            {"key": "B", "text": "Shelley, all of them"},
            {"key": "C", "text": "Shelley all of them"},
            {"key": "D", "text": "Shelley; which"}
        ],
        "correct": "A",
        "explanation": "Bu yerda ikkita mustaqil gap (independent clauses) mavjud: 1) 'The archival research team uncovered three previously unpublished letters by author Mary Shelley' va 2) 'all of them were meticulous reflections...'. Ikkita mustaqil gapni bog'lovchisiz faqat vergul bilan ajratish 'comma splice' xatosidir (B xato). Nuqta-vergul (;) ikkita mustaqil gapni grammatik to'g'ri bog'laydi. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B — vergul xatosi (comma splice); C — tinish belgisiz qo'shib yuborish (run-on); D — nuqta-verguldan keyin 'which' qo'yib gapni chala qoldirish (fragment).",
        "strategy_or_hack": "⚡ SAT GRAMMATIKA: Mustaqil gap + mustaqil gap = Nuqta-vergul (;) yoki Vergul + FANBOYS. Faqat vergul bo'lsa xato!"
    },
    {
        "id": "w_b3_sec_02",
        "section": "writing",
        "domain": "Standard English Conventions",
        "skill": "Boundaries (complete sentences, comma splices, run-ons, fragments)",
        "difficulty": "Hard",
        "passage": "A team of structural engineers inspected the suspension bridge's primary cable ______ discovering extensive corrosion along the western anchoring vault, they recommended immediate tension reduction.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "bands; after"},
            {"key": "B", "text": "bands, after"},
            {"key": "C", "text": "bands after"},
            {"key": "D", "text": "bands. After"}
        ],
        "correct": "A",
        "explanation": "Tuzilishga qaraymiz: Birinchi mustaqil gap: 'A team... inspected the suspension bridge's primary cable bands'. Ikkinchi mustaqil gap: 'after discovering extensive corrosion..., they recommended immediate tension reduction'. Bu ikkala mustaqil gapni nuqta-vergul (;) bilan ajratish kerak. (Eslatma: D variantda 'bands. After' ham mustaqil gaplarni ajratadi, ammo bu yerda A variant bitta yaxlit fikriy bog'liqlikni nuqta-vergul bilan me'yoriy bog'laydi). Keling, variantlarni ko'rib chiqamiz: A da 'bands; after' ikkita mustaqil fikrni bog'laydi. B vergul xatosi (comma splice); C tinish belgisiz bog'lanish (run-on). To'g'ri javob: A.",
        "strategy_or_hack": "⚡ MUSTAQIL GAPLAR: Ikkita gap o'rtasidagi chegara: [Mustaqil gap] ; [Dependent clause + Mustaqil gap]."
    },
    {
        "id": "w_b3_sec_03",
        "section": "writing",
        "domain": "Standard English Conventions",
        "skill": "Form, Structure, and Sense (subject-verb agreement, verb tense, pronoun-antecedent, modifiers)",
        "difficulty": "Medium",
        "passage": "The collection of rare Mesoamerican jade artifacts that was recovered from underwater cenotes in the Yucatán Peninsula ______ currently undergoing non-destructive laser spectroscopy in Mexico City.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "is"},
            {"key": "B", "text": "are"},
            {"key": "C", "text": "were"},
            {"key": "D", "text": "have been"}
        ],
        "correct": "A",
        "explanation": "Gapning haqiqiy egasi (subject) — birlikdagi 'The collection' so'zidir. 'of rare Mesoamerican jade artifacts that was recovered...' oraliqdagi aniqlovchi birikma (prepositional phrase) bo'lib, egaga ta'sir qilmaydi. 'The collection' birlikda bo'lgani uchun fe'l ham birlikda bo'lishi shart: 'is'. To'g'ri javob: A (is). Noto'g'ri variantlar tahlili: B (are), C (were) va D (have been) ko'plikdagi fe'llar bo'lib, 'artifacts' so'ziga adashib moslashtirilgan klassik SAT tuzoqlaridir.",
        "strategy_or_hack": "⚡ EGA VA FE'L MOSLIGI: Oraliqdagi 'of artifacts...' so'zlarini qavsga olib tashlang: 'The collection [of...] IS undergoing'."
    },
    {
        "id": "w_b3_sec_04",
        "section": "writing",
        "domain": "Standard English Conventions",
        "skill": "Form, Structure, and Sense (subject-verb agreement, verb tense, pronoun-antecedent, modifiers)",
        "difficulty": "Hard",
        "passage": "Analyzing satellite radar telemetry from Antarctic ice shelves, ______",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "glaciologist Marcus Rivera identified a previously undetected network of subglacial meltwater channels."},
            {"key": "B", "text": "a previously undetected network of subglacial meltwater channels was identified by glaciologist Marcus Rivera."},
            {"key": "C", "text": "the rapid expansion of subglacial meltwater channels became evident to glaciologist Marcus Rivera."},
            {"key": "D", "text": "radar telemetry revealed a previously undetected network of subglacial meltwater channels to researchers."}
        ],
        "correct": "A",
        "explanation": "Gap boshidagi ravishdoshli birikmaga qarang: 'Analyzing satellite radar telemetry...' (Yo'ldosh radar ma'lumotlarini tahlil qilar ekan,...). Kim tahlil qilgan? Tahlil qiluvchi shaxs bo'lishi shart! Agar verguldan keyin 'a network' (B), 'the rapid expansion' (C) yoki 'radar telemetry' (D) kelsa, tahlilni go'yo kanallar yoki radar o'zi qilgandek 'dangling modifier' (osilib qolgan aniqlovchi) xatosi yuzaga keladi. Verguldan keyin darhol harakatni bajargan shaxs ('glaciologist Marcus Rivera') kelishi shart. To'g'ri javob: A.",
        "strategy_or_hack": "⚡ DANGLING MODIFIER QOIDASI: Boshdagi '-ing' bilan boshlangan harakatni kim bajargan bo'lsa, verguldan keyin aynan o'sha shaxs turishi shart!"
    },
    {
        "id": "w_b3_sec_05",
        "section": "writing",
        "domain": "Standard English Conventions",
        "skill": "Boundaries (complete sentences, comma splices, run-ons, fragments)",
        "difficulty": "Medium",
        "passage": "The Kepler space observatory, which discovered more than 2,600 verified exoplanets during its nine-year ______ finally exhausted its onboard thruster propellant in October 2018.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "mission,"},
            {"key": "B", "text": "mission;"},
            {"key": "C", "text": "mission"},
            {"key": "D", "text": "mission—"}
        ],
        "correct": "A",
        "explanation": "'which discovered more than 2,600 verified exoplanets during its nine-year mission' — bu qo'shimcha kiritma gap (non-essential relative clause). U 'which' dan oldin vergul bilan boshlangan, shuning uchun 'mission' so'zidan keyin ham vergul bilan yopilishi shart (paired commas). To'g'ri javob: A. Noto'g'ri variantlar tahlili: B (mission;) — kiritmani nuqta-vergul bilan yopish grammatik qo'pol xato; C (mission) — kiritmani ochiq qoldirib tinish belgisini qo'ymaslik xatosi; D (mission—) — bir tomoni vergul, ikkinchi tomoni tire bo'lishi mumkin emas.",
        "strategy_or_hack": "⚡ JUFT VERGULLAR: Agar kiritma vergul bilan ochilgan bo'lsa (..., which...), u vergul bilan yopilishi shart (...mission,)."
    },
    {
        "id": "w_b3_sec_06",
        "section": "writing",
        "domain": "Standard English Conventions",
        "skill": "Form, Structure, and Sense (subject-verb agreement, verb tense, pronoun-antecedent, modifiers)",
        "difficulty": "Medium",
        "passage": "Neither the senior aerospace engineers nor the lead project manager ______ able to determine the root cause of the telemetry transmission anomaly during the preliminary debrief.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "was"},
            {"key": "B", "text": "were"},
            {"key": "C", "text": "are"},
            {"key": "D", "text": "have been"}
        ],
        "correct": "A",
        "explanation": "'Neither... nor...' bog'lovchisida fe'l o'ziga eng yaqin turgan egaga moslashadi (Rule of Proximity). Bu yerda 'nor' dan keyin 'the lead project manager' (birlik) turibdi. Shuning uchun fe'l birlikda bo'lishi shart: 'was'. To'g'ri javob: A (was). Noto'g'ri variantlar tahlili: B (were), C (are) va D (have been) ko'plikdagi fe'llar bo'lib, ular 'engineers' so'ziga adashib qaraganda tushiladigan tuzoqlardir.",
        "strategy_or_hack": "⚡ NEITHER/NOR QOIDASI: 'nor' dan keyingi otga qarang: 'manager' (birlik) bo'lsa -> 'was'."
    },
    {
        "id": "w_b3_sec_07",
        "section": "writing",
        "domain": "Standard English Conventions",
        "skill": "Boundaries (complete sentences, comma splices, run-ons, fragments)",
        "difficulty": "Easy",
        "passage": "During the archaeological survey of the Roman villa, researchers catalogued hundreds of well-preserved everyday ______ bronze oil lamps, terracotta cookware, and carved ivory hairpins.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "items:"},
            {"key": "B", "text": "items,"},
            {"key": "C", "text": "items;"},
            {"key": "D", "text": "items"}
        ],
        "correct": "A",
        "explanation": "Ikki nuqta (colon) to'liq mustaqil gapdan keyin ro'yxat, izoh yoki misollarni keltirish uchun ishlatiladi: '...catalogued hundreds of well-preserved everyday items' — bu to'liq mustaqil gap. Undan keyin sanab o'tilgan buyumlar ro'yxati kelgan. Shuning uchun ikki nuqta (:) to'g'ri tanlov. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B (vergul) — ro'yxatni ochishda bo'linish noaniqligini keltirib chiqaradi; C (nuqta-vergul) — faqat mustaqil gaplarni bog'laydi, ro'yxat kiritmaydi; D — tinish belgisiz qo'shib yuborish xatosi.",
        "strategy_or_hack": "⚡ IKKI NUQTA (:) QOIDASI: [To'liq mustaqil gap] : [Ro'yxat yoki izoh]."
    },
    {
        "id": "w_b3_sec_08",
        "section": "writing",
        "domain": "Standard English Conventions",
        "skill": "Form, Structure, and Sense (subject-verb agreement, verb tense, pronoun-antecedent, modifiers)",
        "difficulty": "Hard",
        "passage": "Unlike the ornate frescoes produced by his Italian contemporaries, the seventeenth-century Dutch painter Johannes Vermeer ______ scenes of quiet domesticity, depicting solitary figures engaged in routine household tasks.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "favored"},
            {"key": "B", "text": "favoring"},
            {"key": "C", "text": "having favored"},
            {"key": "D", "text": "to favor"}
        ],
        "correct": "A",
        "explanation": "Gapning grammatik asosini tahlil qilamiz: 'Johannes Vermeer' bu yerda ega (subject). Gapda boshqa hech qanday asosiy kesim (finite verb) yo'q. Shuning uchun Vermeer dan keyin o'tgan zamondagi to'liq kesim 'favored' kelishi shart. B ('favoring'), C ('having favored') va D ('to favor') sifatdosh va infinitiv bo'lib, mustaqil kesim bo'la olmaydi va gapni grammatik nuqsonga (fragment) aylantiradi. To'g'ri javob: A.",
        "strategy_or_hack": "⚡ FINITE VERB TALABI: Har bir gapda albatta to'liq tuslangan zamon fe'li (kesim) bo'lishi shart! '-ing' yoki 'to...' yolg'iz o'zi kesim bo'lolmaydi."
    },
    {
        "id": "w_b3_sec_09",
        "section": "writing",
        "domain": "Standard English Conventions",
        "skill": "Boundaries (complete sentences, comma splices, run-ons, fragments)",
        "difficulty": "Medium",
        "passage": "Neurobiologist Elena Rostova spent decades investigating synaptic ______ her pioneering work on hippocampal long-term potentiation fundamentally transformed contemporary models of memory formation.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "plasticity;"},
            {"key": "B", "text": "plasticity,"},
            {"key": "C", "text": "plasticity"},
            {"key": "D", "text": "plasticity and,"}
        ],
        "correct": "A",
        "explanation": "Bu yerda ikkita to'liq mustaqil gap bor: 1) 'Neurobiologist Elena Rostova spent decades investigating synaptic plasticity' va 2) 'her pioneering work... fundamentally transformed contemporary models...'. Ikkita mustaqil gapni ajratish uchun nuqta-vergul (;) talab qilinadi. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B (vergul) — comma splice xatosi; C — run-on xatosi; D ('and,') — vergul noo'rin qo'yilgan xato variant.",
        "strategy_or_hack": "⚡ COMMA SPLICE TESTI: Ikkita gap o'rtasiga nuqta qo'yib ko'ring: ikkisi ham mustaqil tura olsa, ularning orasiga faqat vergul qo'yish taqiqlanadi!"
    },
    {
        "id": "w_b3_sec_10",
        "section": "writing",
        "domain": "Standard English Conventions",
        "skill": "Form, Structure, and Sense (subject-verb agreement, verb tense, pronoun-antecedent, modifiers)",
        "difficulty": "Easy",
        "passage": "Every autumn, millions of monarch butterflies embark on a 3,000-mile migration from eastern North America to central Mexico, where ______ congregate in the high-altitude fir forests of Michoacán.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "they"},
            {"key": "B", "text": "it"},
            {"key": "C", "text": "one"},
            {"key": "D", "text": "this"}
        ],
        "correct": "A",
        "explanation": "Olmosh o'zi almashtirayotgan otga mos kelishi kerak (pronoun-antecedent agreement). Gapda gap 'millions of monarch butterflies' (ko'plik) haqida ketmoqda. Shuning uchun ko'plik olmoshi 'they' ishlatilishi shart. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B ('it'), C ('one'), D ('this') birlikdagi olmoshlar bo'lib, ko'plikdagi 'butterflies' ga mos kelmaydi.",
        "strategy_or_hack": "⚡ OLMOSH MOSLIGI: 'butterflies' (ko'plik) -> 'they'."
    },

    # =========================================================================
    # WRITING: EXPRESSION OF IDEAS (10 Questions)
    # =========================================================================
    {
        "id": "w_b3_eoi_01",
        "section": "writing",
        "domain": "Expression of Ideas",
        "skill": "Transitions",
        "difficulty": "Medium",
        "passage": "For decades, materials scientists sought to replicate the remarkable tensile strength of natural spider silk using synthetic petrochemical polymers. ______, by utilizing genetically engineered silkworms expressing transgenic arachnid proteins, contemporary bioengineers finally produced fibers matching the elasticity of natural dragline silk.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "Ultimately"},
            {"key": "B", "text": "For instance"},
            {"key": "C", "text": "Similarly"},
            {"key": "D", "text": "In other words"}
        ],
        "correct": "A",
        "explanation": "Matnda olimlarning o'nlab yillar davomida harakat qilgani ('For decades... sought') va oxir-oqibat genetik muhandislik orqali yakuniy muvaffaqiyatga erishgani ('contemporary bioengineers finally produced...') bayon qilingan. Bu uzoq jarayonning yakuniy yechimini ko'rsatuvchi 'Ultimately' (oxir-oqibat, pirovardida) o'tish so'zini talab qiladi. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B ('For instance') — o'tgan harakatlarga misol emas, natija; C ('Similarly') — o'xshashlik emas; D ('In other words') — boshqacha qilib aytganda emas, yangi yakuniy natija.",
        "strategy_or_hack": "⚡ VAQT VA NATIJA: 'For decades... finally...' juftligi 'Ultimately' (oxir-oqibat) o'tishini bildiradi."
    },
    {
        "id": "w_b3_eoi_02",
        "section": "writing",
        "domain": "Expression of Ideas",
        "skill": "Transitions",
        "difficulty": "Hard",
        "passage": "Traditional silicon photovoltaic panels experience significant efficiency losses as ambient operating temperatures rise above 25°C. ______, newly formulated perovskite-silicon tandem cells demonstrate superior thermal stability, maintaining peak electrical conversion efficiency even in desert climates.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "In contrast"},
            {"key": "B", "text": "Consequently"},
            {"key": "C", "text": "Furthermore"},
            {"key": "D", "text": "Specifically"}
        ],
        "correct": "A",
        "explanation": "Birinchi gapda an'anaviy silikon panellarning issiqda samaradorlikni yo'qotishi ('efficiency losses'), ikkinchi gapda esa yangi tandem elementlarning issiqda ham yuqori barqarorlikni saqlab qolishi ('superior thermal stability') aytilgan. Bu ikki holat o'rtasida yaqqol qarama-qarshilik (contrast) mavjud. Shuning uchun 'In contrast' (A) eng mantiqiy bog'lovchidir. Noto'g'ri variantlar tahlili: B ('Consequently' - natijada) — ikkinchisi birinchisining oqibati emas; C ('Furthermore' - bundan tashqari) — bir xil yo'nalishdagi fikrlar uchun; D ('Specifically') — umumiy fikrni aniqlashtirmayapti.",
        "strategy_or_hack": "⚡ KONTRAST QIDIRISH: Salbiy xususiyat (losses) vs Ijobiy xususiyat (superior stability) = 'In contrast'."
    },
    {
        "id": "w_b3_eoi_03",
        "section": "writing",
        "domain": "Expression of Ideas",
        "skill": "Transitions",
        "difficulty": "Easy",
        "passage": "Urban rooftop gardens insulate buildings against extreme winter cold and summer heat, dramatically reducing HVAC power consumption. ______, their vegetation absorbs stormwater runoff, preventing municipal sewer overflows during intense cloudbursts.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "Additionally"},
            {"key": "B", "text": "Nevertheless"},
            {"key": "C", "text": "Conversely"},
            {"key": "D", "text": "Instead"}
        ],
        "correct": "A",
        "explanation": "Birinchi gap tom bog'larining energiya tejashdagi birinchi foydasini ko'rsatadi. Ikkinchi gap esa yomg'ir suvlarini yutishdagi yana bir qo'shimcha foydasini keltiradi. Bu fikrni qo'shimcha boyitish (additive) munosabatidir. Shuning uchun 'Additionally' (Bundan tashqari) to'g'ri bog'lovchi. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B ('Nevertheless' - shunga qaramay), C ('Conversely' - aksincha) va D ('Instead' - o'rniga) barchasi qarama-qarshilik bog'lovchilari bo'lib, ikkita ijobiy foydani bog'lashda xatodir.",
        "strategy_or_hack": "⚡ FOYDA + FOYDA = ADDITIVE: Foyda 1 + 'Additionally' + Foyda 2."
    },
    {
        "id": "w_b3_eoi_04",
        "section": "writing",
        "domain": "Expression of Ideas",
        "skill": "Transitions",
        "difficulty": "Medium",
        "passage": "Agricultural runoff introduces excess nitrogen and phosphorus into freshwater estuaries, fueling massive blooms of microscopic algae. As these algal mats die and decompose, microbial respiration depletes dissolved oxygen levels. ______, hypoxic 'dead zones' form where fish and shellfish cannot survive.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "As a result"},
            {"key": "B", "text": "In comparison"},
            {"key": "C", "text": "Meanwhile"},
            {"key": "D", "text": "Regardless"}
        ],
        "correct": "A",
        "explanation": "Matnda sabab-oqibat zanjiri keltirilgan: O'g'itlar suvga tushadi -> suvo'tlar ko'payadi -> parchalanishda kislorod tugaydi -> BARCHA SHU SABABLARNING OQIBATI O'LAROQ ('As a result') baliqlar yashay olmaydigan o'lik zonalar paydo bo'ladi. Sabab-oqibatni bog'lash uchun 'As a result' to'g'ri tanlov. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B ('In comparison') — taqqoslash yo'q; C ('Meanwhile') — parallel vaqt munosabati emas, to'g'ridan-to'g'ri oqibat; D ('Regardless') — qaramasdan emas.",
        "strategy_or_hack": "⚡ SABAB-OQIBAT ZANJIRI: Kislorod tugashi -> Baliqlar o'lishi = 'As a result' (Natijada)."
    },
    {
        "id": "w_b3_eoi_05",
        "section": "writing",
        "domain": "Expression of Ideas",
        "skill": "Transitions",
        "difficulty": "Hard",
        "passage": "Medieval scribes produced parchment manuscripts through labor-intensive manual curing and stretching of animal hides, rendering books luxury commodities accessible solely to religious institutions and aristocrats. Johannes Gutenberg's fifteenth-century invention of movable type printing press completely revolutionized text production. ______, the technological transition did not occur instantaneously; scribe guilds fiercely opposed printing shops across central Europe for decades.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "However"},
            {"key": "B", "text": "Accordingly"},
            {"key": "C", "text": "Furthermore"},
            {"key": "D", "text": "Likewise"}
        ],
        "correct": "A",
        "explanation": "Gutenberg matbaa mashinasi kitob chop etishni inqilobiy o'zgartirgani aytildi. Lekin keyingi gap bu o'tish birdaniga silliq bo'lmaganini, xattotlar gildiyalari o'nlab yillar qarshilik ko'rsatganini aytib, kutilgan tezkor g'alabaga zid cheklov (concession / contrast) kiritmoqda. Shuning uchun 'However' (Biroq) eng to'g'ri bog'lovchi. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B ('Accordingly' - mos ravishda) — sabab-oqibat emas; C ('Furthermore') — davomiy qo'shimcha emas; D ('Likewise') — o'xshashlik emas.",
        "strategy_or_hack": "⚡ BURILISH NUQTASI: 'revolutionized... [However], the transition did not occur instantaneously'."
    },
    {
        "id": "w_b3_eoi_06",
        "section": "writing",
        "domain": "Expression of Ideas",
        "skill": "Rhetorical Synthesis",
        "difficulty": "Medium",
        "passage": "While researching aviation history, a student took the following notes:\n- In 1932, Amelia Earhart became the first woman to complete a solo nonstop transatlantic flight.\n- She flew a modified Lockheed Vega 5B from Harbour Grace, Newfoundland, to Londonderry, Northern Ireland.\n- The flight took approximately 14 hours and 56 minutes under harsh icing and fatigue conditions.\n- Her achievement challenged prevailing societal skepticism regarding women's endurance in long-distance aviation.",
        "question": "The student wants to emphasize the historical significance of Earhart's transatlantic flight. Which choice best accomplishes this goal?",
        "options": [
            {"key": "A", "text": "By completing her grueling 1932 solo flight across the Atlantic, Amelia Earhart shattered contemporary skepticism about women's capability in long-distance aviation."},
            {"key": "B", "text": "Amelia Earhart's 1932 flight in a modified Lockheed Vega 5B departed from Harbour Grace and ended in Northern Ireland."},
            {"key": "C", "text": "The flight across the Atlantic took Earhart exactly 14 hours and 56 minutes despite difficult weather conditions."},
            {"key": "D", "text": "In 1932, a modified Lockheed Vega 5B was used by Amelia Earhart for long-distance flight testing."}
        ],
        "correct": "A",
        "explanation": "Talabaning aniq maqsadi: 'emphasize the historical significance' (tarixiy ahamiyatini ta'kidlash). A variantda Earhartning parvozi o'sha davrdagi jamiyatning ayollarning uzoq masofaga ucha olishiga bo'lgan shubhalarini sindirgani ('shattered contemporary skepticism') aniq ta'kidlangan, bu uning asosiy tarixiy ahamiyatidir. Noto'g'ri variantlar tahlili: B — faqat marshrutni aytadi; C — faqat vaqtni aytadi; D — kema modelini aytadi; ularning hech biri tarixiy ahamiyatni ochib bermaydi.",
        "strategy_or_hack": "⚡ MAQSADNI O'QISH: 'emphasize the historical significance' -> Javobda jamiyatga ta'siri (shattered skepticism) bo'lishi shart!"
    },
    {
        "id": "w_b3_eoi_07",
        "section": "writing",
        "domain": "Expression of Ideas",
        "skill": "Rhetorical Synthesis",
        "difficulty": "Hard",
        "passage": "While researching architecture, a student took the following notes:\n- The High Line in New York City is a 1.45-mile elevated public park built on a disused historic freight rail line.\n- It opened in stages between 2009 and 2014, designed by landscape architecture firm James Corner Field Operations.\n- The park features native perennial plantings, open lawns, and pedestrian walkways elevated 30 feet above street traffic.\n- Since its opening, the High Line has spurred over $2 billion in surrounding real estate development and attracts millions of visitors annually.",
        "question": "The student wants to highlight the economic and urban revival impact of the High Line project. Which choice best accomplishes this goal?",
        "options": [
            {"key": "A", "text": "Beyond transforming an abandoned industrial rail line into an elevated public park, the High Line has catalyzed over $2 billion in surrounding development and drawn millions of visitors."},
            {"key": "B", "text": "Designed by James Corner Field Operations, the High Line park opened in stages between 2009 and 2014."},
            {"key": "C", "text": "The High Line is an elevated public park in New York City featuring native perennial plantings and open lawns 30 feet above the street."},
            {"key": "D", "text": "Historic freight rail lines in New York City were originally constructed 30 feet above street traffic."}
        ],
        "correct": "A",
        "explanation": "Talabaning maqsadi: 'highlight the economic and urban revival impact' (iqtisodiy va shahar jonlanishi ta'sirini ko'rsatish). A variant 2 milliard dollarlik rivojlanish va millionlab sayyohlar jalb qilinganini hamda tashlandiq hudud shahar parkiga aylanganini aniq ko'rsatadi. Noto'g'ri variantlar tahlili: B — faqat arxitektura firmasi va sanani aytadi; C — faqat o'simlik turlarini aytadi; D — tarixiy temir yo'l balandligini aytadi; ularda iqtisodiy ta'sir yo'q.",
        "strategy_or_hack": "⚡ KALIT SO'ZLAR: 'economic impact' -> $2 billion in surrounding development!"
    },
    {
        "id": "w_b3_eoi_08",
        "section": "writing",
        "domain": "Expression of Ideas",
        "skill": "Rhetorical Synthesis",
        "difficulty": "Easy",
        "passage": "While researching marine biology, a student took the following notes:\n- The Greenland shark (Somniosus microcephalus) inhabits cold, deep waters of the Arctic and North Atlantic.\n- In 2016, marine biologists used radiocarbon dating of eye lens crystalline proteins to estimate their lifespans.\n- The study determined that Greenland sharks can live for at least 272 years, with some specimens possibly exceeding 400 years.\n- They are currently recognized as the longest-lived vertebrate species on Earth.",
        "question": "The student wants to introduce the Greenland shark's exceptional longevity to a new audience. Which choice best accomplishes this goal?",
        "options": [
            {"key": "A", "text": "Inhabiting Arctic waters, the Greenland shark holds the distinction of being the longest-lived vertebrate on Earth, with lifespans documented to reach at least 272 years."},
            {"key": "B", "text": "Marine biologists in 2016 utilized radiocarbon dating on eye lens crystalline proteins during an Arctic expedition."},
            {"key": "C", "text": "The Greenland shark, or Somniosus microcephalus, is a marine animal that resides in deep, cold northern oceans."},
            {"key": "D", "text": "Radiocarbon dating is an effective technique commonly employed to measure organic specimens in marine research."}
        ],
        "correct": "A",
        "explanation": "Maqsad: 'introduce the Greenland shark's exceptional longevity to a new audience' (Grenlandiya akulasining favqulodda uzoq umr ko'rishini yangi auditoriyaga tanishtirish). A variant akulaning kimligini tanishtiradi va uning 272 yildan ortiq yashaydigan yer yuzidagi eng uzoq umr ko'ruvchi umurtqali hayvon ekanini aniq bayon qiladi. Noto'g'ri variantlar tahlili: B — faqat 2016 yilgi usulni aytadi; C — uzoq umr ko'rishini aytmaydi; D — faqat radiouglerod usulini umumiy ta'riflaydi.",
        "strategy_or_hack": "⚡ AUDITORIYAGA TANISHTIRISH: Jonivorning nomi + uning favqulodda rekordi (exceptional longevity: 272+ years) = Variant A."
    },
    {
        "id": "w_b3_eoi_09",
        "section": "writing",
        "domain": "Expression of Ideas",
        "skill": "Rhetorical Synthesis",
        "difficulty": "Hard",
        "passage": "While researching renewable energy materials, a student took the following notes:\n- Solar cell efficiency depends significantly on bandgap energy, measured in electron-volts (eV).\n- Silicon has a bandgap of 1.1 eV, capturing infrared and visible light but losing high-energy photons to heat.\n- Perovskite semiconductors can be engineered with adjustable bandgaps ranging from 1.2 to 2.3 eV.\n- By stacking a wide-bandgap perovskite layer on top of silicon, tandem cells harvest both high-energy and low-energy photons efficiently.",
        "question": "The student wants to explain the mechanical advantage of tandem solar cells over single-layer silicon cells. Which choice best accomplishes this goal?",
        "options": [
            {"key": "A", "text": "By pairing an adjustable wide-bandgap perovskite top layer with an underlying silicon base, tandem cells absorb both high-energy and low-energy photons, overcoming the thermal energy losses of conventional silicon."},
            {"key": "B", "text": "Bandgap energy is measured in electron-volts and determines which wavelengths of light a semiconductor material can absorb."},
            {"key": "C", "text": "Silicon semiconductors have a fixed bandgap of 1.1 eV, making them the standard material in photovoltaic manufacturing for decades."},
            {"key": "D", "text": "Perovskite semiconductors feature bandgaps that can be adjusted anywhere between 1.2 and 2.3 eV in laboratory conditions."}
        ],
        "correct": "A",
        "explanation": "Talabaning maqsadi: 'explain the mechanical advantage of tandem solar cells over single-layer silicon cells' (tandem hujayralarning bir qatlamli kremniyga nisbatan ustunligini tushuntirish). A variant tandem tizimi keng va tor oraliqlarni birlashtirib, yuqori va past energiyali fotonlarni birday yutishini va an'anaviy silikonning issiqlik yo'qotishini yengib o'tishini mukammal tushuntiradi. Noto'g'ri variantlar tahlili: B — faqat bandgap ta'rifini beradi; C — faqat silikon haqida; D — faqat perovskit haqida; solishtirma ustunlik faqat A da bor.",
        "strategy_or_hack": "⚡ SOLISHTIRMA USTUNLIK: Tandem + Silikon bilan qiyos + yechilgan muammo = Variant A."
    },
    {
        "id": "w_b3_eoi_10",
        "section": "writing",
        "domain": "Expression of Ideas",
        "skill": "Transitions",
        "difficulty": "Medium",
        "passage": "Early twentieth-century astronomers assumed that spiral nebulae were isolated clouds of interstellar gas and dust located within the perimeter of the Milky Way galaxy. In 1923, Edwin Hubble identified Cepheid variable stars within the Andromeda nebula and calculated its distance as nearly one million light-years away. ______, Hubble proved conclusively that spiral nebulae were entirely separate galaxies existing far beyond our own.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "Consequently"},
            {"key": "B", "text": "Previously"},
            {"key": "C", "text": "Nevertheless"},
            {"key": "D", "text": "For example"}
        ],
        "correct": "A",
        "explanation": "Hubble Andromeda tumanligidagi Sefeida yulduzlarini topdi va uning masofasi million yorug'lik yili ekanini hisobladi. Natijada / Buning oqibatida ('Consequently') Hubble bu tumanliklar Somon Yo'lidan ancha olisdagi butunlay mustaqil galaktikalar ekanini uzil-kesil isbotladi. Masofaning uzoqligi mustaqil galaktika degan xulosaga olib keladi (sabab-oqibat). To'g'ri javob: A. Noto'g'ri variantlar tahlili: B ('Previously' - avval) — o'tmishga qaytish yo'q, xulosa chiqarilyapti; C ('Nevertheless' - shunga qaramay) — qarama-qarshilik yo'q; D ('For example') — misol keltirilmayapti, buyuk kashfiyot xulosalanyapti.",
        "strategy_or_hack": "⚡ SABAB VA XULOSA: Hisoblangan masofa 1 million yorug'lik yili -> 'Consequently' (Natijada) mustaqil galaktikalar ekani isbotlandi."
    }
]
