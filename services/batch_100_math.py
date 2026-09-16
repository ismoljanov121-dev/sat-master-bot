"""
Batch 100 Expansion - Math Section (40 Questions)
Algebra (10), Advanced Math (12), Problem-Solving and Data Analysis (10), Geometry and Trigonometry (8)
"""

BATCH_100_MATH = [
    # =========================================================================
    # ALGEBRA (10 Questions)
    # =========================================================================
    {
        "id": "m_b4_01",
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear inequalities in one or two variables",
        "difficulty": "Easy",
        "passage": None,
        "question": "A drone logistics company charges an initial dispatch fee of $15 plus $1.25 per kilometer flown. A client has a maximum spending budget of $65 for a single package delivery. What is the maximum distance, in kilometers, the drone can fly without exceeding the client's budget?",
        "options": [
            {"key": "A", "text": "40"},
            {"key": "B", "text": "35"},
            {"key": "C", "text": "50"},
            {"key": "D", "text": "45"}
        ],
        "correct": "A",
        "explanation": "Tengsizlik tuzamiz: Jami to'lov 15 + 1.25d <= 65 bo'lishi lozim, bu yerda d — masofa. Dastlabki to'lov 15 ni ayiramiz: 1.25d <= 50. Ikkala tomonni 1.25 ga bo'lamiz: d <= 50 / 1.25 = 40 km. Demak, eng ko'pi bilan 40 km uchish mumkin. To'g'ri javob: A (40). Noto'g'ri variantlar tahlili: B (35) — hisoblashda 15 ni ikki marta ayirish xatosi; C (50) — bazaviy to'lovni hisobga olmaslik tuzog'i; D (45) — yaxlitlashdagi xato variant.",
        "strategy_or_hack": "⚡ TEZ HISOBLASH: 50 / 1.25 = 50 / (5/4) = 50 * 4 / 5 = 40. 3 soniyada tayyor!"
    },
    {
        "id": "m_b4_02",
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear equations in one variable",
        "difficulty": "Medium",
        "passage": None,
        "question": "If 4(2x - 7) + 5(x + 3) = 65, what is the value of the expression 3x - 5?",
        "options": [
            {"key": "A", "text": "13"},
            {"key": "B", "text": "6"},
            {"key": "C", "text": "18"},
            {"key": "D", "text": "21"}
        ],
        "correct": "A",
        "explanation": "Qavslarni ochamiz: 8x - 28 + 5x + 15 = 65. O'xshash hadlarni jamlaymiz: 13x - 13 = 65. 13 ni o'ng tomonga qo'shamiz: 13x = 78 => x = 6. Savol x ni emas, 3x - 5 ifodani so'ragan: 3(6) - 5 = 18 - 5 = 13. To'g'ri javob: A (13). Noto'g'ri variantlar tahlili: B (6) — x ning o'zini shoshib belgilash klassik SAT tuzog'i; C (18) — 3x ning qiymati; D (21) — qo'shishdagi adashish natijasidagi xato variant.",
        "strategy_or_hack": "⚡ DIQQAT: Savol x ni emas, 3x - 5 ni so'ramoqda! Desmosda x = 6 ni topib, darhol 3(6)-5 = 13 deb hisoblang."
    },
    {
        "id": "m_b4_03",
        "section": "math",
        "domain": "Algebra",
        "skill": "Systems of two linear equations in two variables",
        "difficulty": "Medium",
        "passage": None,
        "question": "An art gallery sells large canvas prints for $120 each and small prints for $45 each. A collector purchases a total of 14 prints and spends exactly $1,080. How many large canvas prints did the collector purchase?",
        "options": [
            {"key": "A", "text": "6"},
            {"key": "B", "text": "8"},
            {"key": "C", "text": "5"},
            {"key": "D", "text": "9"}
        ],
        "correct": "A",
        "explanation": "Katta rasmlar L ta, kichiklari S ta bo'lsin. 1) L + S = 14 => S = 14 - L. 2) 120L + 45S = 1080. O'rniga qo'yamiz: 120L + 45(14 - L) = 1080 => 120L + 630 - 45L = 1080 => 75L = 450 => L = 6 ta katta rasm. To'g'ri javob: A (6). Noto'g'ri variantlar tahlili: B (8) — kichik rasmlar sonini (S = 8) belgilab qo'yish tuzog'i; C (5) va D (9) — hisob-kitobdagi xato variantlar.",
        "strategy_or_hack": "⚡ DESMOS USULI: Desmosga x + y = 14 va 120x + 45y = 1080 ni kiriting. Kesishish nuqtasi (6, 8). Katta rasm x = 6!"
    },
    {
        "id": "m_b4_04",
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear equations in one variable",
        "difficulty": "Hard",
        "passage": None,
        "question": "The linear equation 8x - 12 = 2(kx + 5) has no real solution, where k is a constant. What is the value of k?",
        "options": [
            {"key": "A", "text": "4"},
            {"key": "B", "text": "-4"},
            {"key": "C", "text": "8"},
            {"key": "D", "text": "2"}
        ],
        "correct": "A",
        "explanation": "O'ng tomonni ochamiz: 8x - 12 = 2kx + 10. Chiziqli tenglama yechimga ega bo'lmasligi (no solution) uchun x oldidagi koeffitsiyentlar teng, ozod hadlar esa turli bo'lishi shart: 8 = 2k => k = 4. Ozod hadlar -12 != 10 bo'lgani uchun tenglama hech qachon bajarilmaydi. To'g'ri javob: A (4). Noto'g'ri variantlar tahlili: B (-4) — ishorani adashtirish tuzog'i; C (8) — 2 ga bo'lishni unutish xatosi; D (2) — arifmetik yanglishishdagi xato variant.",
        "strategy_or_hack": "⚡ NO SOLUTION QOIDASI: x ning koeffitsiyentlari teng bo'lishi shart: 8 = 2k => k = 4!"
    },
    {
        "id": "m_b4_05",
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear inequalities in one or two variables",
        "difficulty": "Easy",
        "passage": None,
        "question": "A theater sells adult admission tickets for $14 each and student tickets for $9 each. A community group has a maximum budget of $150 and must purchase at least 12 tickets in total. If x represents the number of adult tickets and y represents the number of student tickets, which system of inequalities represents this scenario?",
        "options": [
            {"key": "A", "text": "14x + 9y <= 150 and x + y >= 12"},
            {"key": "B", "text": "14x + 9y >= 150 and x + y <= 12"},
            {"key": "C", "text": "9x + 14y <= 150 and x + y >= 12"},
            {"key": "D", "text": "14x + 9y <= 150 and x + y <= 12"}
        ],
        "correct": "A",
        "explanation": "Masala tahlili va bosqichma-bosqich yechim: 1) Jami sarf 150 dollardan oshmasligi kerak (maximum budget): 14x + 9y <= 150. 2) Jami biletlar soni kamida 12 ta bo'lishi shart (at least 12): x + y >= 12. Bu shartlar A variantda aynan to'g'ri ifodalangan. Noto'g'ri variantlar tahlili: B variantida tengsizlik ishoralari teskari qo'yilgan; C variantida x va y narxlari almashtirilgan; D variantida kamida 12 ta degan shart 'x + y <= 12' deb xato yozilgan.",
        "strategy_or_hack": "⚡ KALIT SO'ZLAR: 'at most / maximum' = <= ; 'at least / minimum' = >=."
    },
    {
        "id": "m_b4_06",
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear equations in one variable",
        "difficulty": "Medium",
        "passage": None,
        "question": "What is the sum of all real solutions to the absolute value equation |4x - 6| = 18?",
        "options": [
            {"key": "A", "text": "3"},
            {"key": "B", "text": "-18"},
            {"key": "C", "text": "6"},
            {"key": "D", "text": "9"}
        ],
        "correct": "A",
        "explanation": "Ikkita holat: 1) 4x - 6 = 18 => 4x = 24 => x1 = 6. 2) 4x - 6 = -18 => 4x = -12 => x2 = -3. Ildizlar yig'indisi: x1 + x2 = 6 + (-3) = 3. To'g'ri javob: A (3). Noto'g'ri variantlar tahlili: B (-18) — modul qiymati bilan adashish; C (6) — faqat bitta musbat ildizni belgilab qo'yish tuzog'i; D (9) — ildizlarni noto'g'ri ayirishdagi xato variant.",
        "strategy_or_hack": "⚡ MODUL SIMMETRIYASI: |ax - b| = c ning ildizlari b/a markaziga nisbatan simmetrik. Yig'indi doimo 2*(b/a) = 2*(6/4) = 3 bo'ladi!"
    },
    {
        "id": "m_b4_07",
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear functions",
        "difficulty": "Easy",
        "passage": None,
        "question": "The graph of a linear function f passes through points (2, 11) and (5, 23) in the xy-plane. What is the value of f(9)?",
        "options": [
            {"key": "A", "text": "39"},
            {"key": "B", "text": "36"},
            {"key": "C", "text": "41"},
            {"key": "D", "text": "43"}
        ],
        "correct": "A",
        "explanation": "Chiziqli funksiya qiyaligi (slope): m = (23 - 11) / (5 - 2) = 12 / 3 = 4. Funksiya tenglamasi: f(x) - 11 = 4(x - 2) => f(x) = 4x + 3. Endi x = 9 ni qo'yamiz: f(9) = 4(9) + 3 = 36 + 3 = 39. To'g'ri javob: A (39). Noto'g'ri variantlar tahlili: B (36) — ozod had 3 ni qo'shishni unutish xatosi; C (41) va D (43) — hisoblashdagi xato variantlar.",
        "strategy_or_hack": "⚡ BOSQICHMA-BOSQICH QADAM: x har 3 ga oshganda y 12 ga oshyapti (har 1 birlik x uchun +4 y). x = 5 dan x = 9 gacha +4 qadam: 23 + 4*4 = 39!"
    },
    {
        "id": "m_b4_08",
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear equations in two variables",
        "difficulty": "Medium",
        "passage": None,
        "question": "Line L1 passes through the points (1, 4) and (4, 13) in the xy-plane. Line L2 is parallel to line L1 and passes through the point (2, -1). What is the y-intercept of line L2?",
        "options": [
            {"key": "A", "text": "(0, -7)"},
            {"key": "B", "text": "(0, 7)"},
            {"key": "C", "text": "(0, -1)"},
            {"key": "D", "text": "(0, -5)"}
        ],
        "correct": "A",
        "explanation": "L1 ning qiyaligi: m = (13 - 4) / (4 - 1) = 9 / 3 = 3. Parallel to'g'ri chiziqlarning qiyaliklari teng bo'ladi, shuning uchun L2 ning ham m = 3. L2 (2, -1) nuqtadan o'tadi: y - (-1) = 3(x - 2) => y + 1 = 3x - 6 => y = 3x - 7. y-kesishma nuqtasi (x = 0): (0, -7). To'g'ri javob: A. Noto'g'ri variantlar tahlili: B (0, 7) — ishorani teskari olishdagi tuzoq; C (0, -1) — berilgan nuqtani y-kesishma deb o'ylash xatosi; D (0, -5) — arifmetik xato.",
        "strategy_or_hack": "⚡ PARALLEL TO'G'RI CHIZIQ: m = 3. y = 3x + b da (2, -1) qo'ying: -1 = 6 + b => b = -7. Kesishma: (0, -7)."
    },
    {
        "id": "m_b4_09",
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear equations in two variables",
        "difficulty": "Hard",
        "passage": None,
        "question": "In the xy-plane, line j is defined by the equation 2x + 5y = 15. If line k is perpendicular to line j, what is the slope of line k?",
        "options": [
            {"key": "A", "text": "5/2"},
            {"key": "B", "text": "-2/5"},
            {"key": "C", "text": "-5/2"},
            {"key": "D", "text": "2/5"}
        ],
        "correct": "A",
        "explanation": "Line j ni y = mx + b ko'rinishiga keltiramiz: 5y = -2x + 15 => y = (-2/5)x + 3. Line j ning qiyaligi m1 = -2/5. Perpendikulyar to'g'ri chiziqning qiyaligi teskari va qarama-qarshi ishorali bo'ladi (negative reciprocal): m2 = -1 / m1 = -1 / (-2/5) = 5/2. To'g'ri javob: A (5/2). Noto'g'ri variantlar tahlili: B (-2/5) — parallel chiziq qiyaligini belgilash tuzog'i; C (-5/2) — ishorani almashtirishni unutish xatosi; D (2/5) — to'ntarishni unutishdagi xato variant.",
        "strategy_or_hack": "⚡ PERPENDIKULYAR QOIDASI: Kasrni to'ntaring va ishorasini teskari qiling: -2/5 -> +5/2!"
    },
    {
        "id": "m_b4_10",
        "section": "math",
        "domain": "Algebra",
        "skill": "Linear functions",
        "difficulty": "Medium",
        "passage": None,
        "question": "Two cyclists start from the exact same trailhead at the same time and travel in opposite directions along a straight path. Cyclist A travels at a constant speed of 14 miles per hour, while Cyclist B travels at a constant speed of 18 miles per hour. After how many hours will the two cyclists be exactly 80 miles apart?",
        "options": [
            {"key": "A", "text": "2.5"},
            {"key": "B", "text": "2.0"},
            {"key": "C", "text": "3.0"},
            {"key": "D", "text": "3.5"}
        ],
        "correct": "A",
        "explanation": "Qarama-qarshi yo'nalishda harakatlanayotgani sababli ularning bir-biridan uzoqlashish tezligi qo'shiladi: v_nisbiy = 14 + 18 = 32 mil/soat. Masofa 80 mil bo'lishi uchun vaqt: t = Masofa / v_nisbiy = 80 / 32 = 5 / 2 = 2.5 soat. To'g'ri javob: A (2.5). Noto'g'ri variantlar tahlili: B (2.0) — tezliklarni ayirib hisoblash xatosi; C (3.0) va D (3.5) — noto'g'ri bo'lishdagi chalg'ituvchi variantlar.",
        "strategy_or_hack": "⚡ HARAKAT TENGLAMASI: 14t + 18t = 80 => 32t = 80 => t = 80/32 = 2.5 soat."
    },

    # =========================================================================
    # ADVANCED MATH (12 Questions)
    # =========================================================================
    {
        "id": "m_b4_11",
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Nonlinear functions (quadratic vertex/standard form, exponential models, polynomials)",
        "difficulty": "Easy",
        "passage": None,
        "question": "What is the maximum value of the quadratic function f(x) = -3(x - 4)^2 + 27?",
        "options": [
            {"key": "A", "text": "27"},
            {"key": "B", "text": "4"},
            {"key": "C", "text": "-3"},
            {"key": "D", "text": "-27"}
        ],
        "correct": "A",
        "explanation": "Funksiya cho'qqi ko'rinishida (vertex form) berilgan: f(x) = a(x - h)^2 + k. Bu yerda a = -3 < 0 bo'lgani uchun parabola pastga qaragan va o'zining eng katta (maksimal) qiymatiga cho'qqisida erishadi: k = 27 (x = 4 bo'lganda). To'g'ri javob: A (27). Noto'g'ri variantlar tahlili: B (4) — maksimum nuqtani (x koordinatani) qiymat deb adashib belgilash tuzog'i; C (-3) — a koeffitsiyenti; D (-27) — ishorani teskari olishdagi xato variant.",
        "strategy_or_hack": "⚡ VERTEX FORM: y = a(x - h)^2 + k da maksimum/minimum qiymat doimo k ning o'zidir (k = 27)!"
    },
    {
        "id": "m_b4_12",
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Nonlinear equations in one variable (quadratic, radical, absolute value)",
        "difficulty": "Medium",
        "passage": None,
        "question": "The quadratic equation x^2 - 10x + 21 = 0 has two distinct real solutions, p and q, where p > q. What is the value of p - q?",
        "options": [
            {"key": "A", "text": "4"},
            {"key": "B", "text": "10"},
            {"key": "C", "text": "7"},
            {"key": "D", "text": "21"}
        ],
        "correct": "A",
        "explanation": "Kvadrat tenglamani ko'paytuvchilarga ajratamiz: (x - 7)(x - 3) = 0. Ildizlar: x = 7 va x = 3. Shart bo'yicha p > q, demak p = 7 va q = 3. Ayirma: p - q = 7 - 3 = 4. To'g'ri javob: A (4). Noto'g'ri variantlar tahlili: B (10) — ildizlar yig'indisini belgilash tuzog'i; C (7) — faqat bitta ildizni olish xatosi; D (21) — ozod hadni belgilashdagi xato variant.",
        "strategy_or_hack": "⚡ DESMOS USULI: Desmosda y = x^2 - 10x + 21 ni kiritib x-kesishmalarini ko'ring: (3, 0) va (7, 0). Masofa: 7 - 3 = 4."
    },
    {
        "id": "m_b4_13",
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Nonlinear equations in one variable (quadratic, radical, absolute value)",
        "difficulty": "Hard",
        "passage": None,
        "question": "For what integer value of constant c does the quadratic equation x^2 - 6x + c = 0 have two distinct real solutions?",
        "options": [
            {"key": "A", "text": "7"},
            {"key": "B", "text": "9"},
            {"key": "C", "text": "12"},
            {"key": "D", "text": "15"}
        ],
        "correct": "A",
        "explanation": "Ikkita turli haqiqiy ildizga ega bo'lishi uchun diskriminant noldan qat'iy katta bo'lishi shart (D > 0): D = b^2 - 4ac = (-6)^2 - 4(1)(c) = 36 - 4c > 0. 4c < 36 => c < 9. Variantlar orasida 9 dan kichik bo'lgan yagona butun son 7 dir. To'g'ri javob: A (7). Noto'g'ri variantlar tahlili: B (9) — D = 0 bo'lib bitta ildiz beradi; C (12) va D (15) — D < 0 bo'lib haqiqiy ildiz bermaydi (noto'g'ri variantlar).",
        "strategy_or_hack": "⚡ DISKRIMINANT QOIDASI: Ikkita haqiqiy yechim -> D > 0. c < 9 bo'lishi kerak, faqat A (7) to'g'ri!"
    },
    {
        "id": "m_b4_14",
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Nonlinear functions (quadratic vertex/standard form, exponential models, polynomials)",
        "difficulty": "Hard",
        "passage": None,
        "question": "In the xy-plane, the circle C is defined by the equation (x - 5)^2 + (y + 2)^2 = 49. The horizontal line y = 5 intersects circle C at how many distinct points?",
        "options": [
            {"key": "A", "text": "Exactly 1"},
            {"key": "B", "text": "Exactly 2"},
            {"key": "C", "text": "0"},
            {"key": "D", "text": "Infinitely many"}
        ],
        "correct": "A",
        "explanation": "Aylana markazi (h, k) = (5, -2), radiusi esa r = sqrt(49) = 7 ga teng. Gorizontal to'g'ri chiziq y = 5 aylananing markazidan vertikal ravishda d = |5 - (-2)| = 7 birlik masofada joylashgan. Masofa aylananing radiusiga teng bo'lgani sababli (d = r = 7), chiziq aylanaga urinadi (tangent) va uni aynan 1 ta nuqtada (5, 5) kesib o'tadi. To'g'ri javob: A (Exactly 1). Noto'g'ri variantlar tahlili: B (Exactly 2) — chiziq aylanani ikkita joydan kesadi deb o'ylash; C (0) — kesishmaydi deb adashish; D — to'g'ri chiziq aylanani cheksiz nuqtada kesa olmaydi.",
        "strategy_or_hack": "⚡ DESMOS USULI: Desmosda (x-5)^2 + (y+2)^2 = 49 va y = 5 ni kiriting. To'g'ri chiziq aylananing eng yuqori uchiga urinib o'tishini ko'rasiz — aynan 1 ta nuqta!"
    },
    {
        "id": "m_b4_15",
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Equivalent expressions (factoring, polynomial arithmetic)",
        "difficulty": "Medium",
        "passage": None,
        "question": "A medical researcher models the concentration of an antibiotic in a patient's bloodstream using the function C(t) = 180 * (0.72)^(t / 6), where C(t) is the concentration in micrograms per milliliter t hours after administration. By what percentage does the antibiotic concentration decrease every 6 hours?",
        "options": [
            {"key": "A", "text": "28%"},
            {"key": "B", "text": "72%"},
            {"key": "C", "text": "18%"},
            {"key": "D", "text": "12%"}
        ],
        "correct": "A",
        "explanation": "Eksponensial kamayish modelida har 6 soat o'tganda (t/6 ko'rsatkichi 1 ga oshganda) konsentratsiya 0.72 koeffitsiyentiga ko'paytiriladi. Bu dastlabki miqdorning 72% qismi qolishini bildiradi. Demak, kamayish foizi: 100% - 72% = 28%. To'g'ri javob: A (28%). Noto'g'ri variantlar tahlili: B (72%) — qolgan miqdorni kamayish ulushi deb chalkashtirish klassik SAT tuzog'i; C (18%) — boshlang'ich konsentratsiyadagi 180 soni bilan adashish; D (12%) — noto'g'ri hisob-kitob.",
        "strategy_or_hack": "⚡ FOIZ KAMAYISHI QOIDASI: Kamayish foizi = 1 - asos = 1 - 0.72 = 0.28, ya'ni 28%!"
    },
    {
        "id": "m_b4_16",
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Equivalent expressions (factoring, polynomial arithmetic)",
        "difficulty": "Medium",
        "passage": None,
        "question": "When the polynomial f(x) = x^3 - 4x^2 + 7x - 5 is divided by (x - 2), what is the remainder?",
        "options": [
            {"key": "A", "text": "1"},
            {"key": "B", "text": "5"},
            {"key": "C", "text": "-1"},
            {"key": "D", "text": "9"}
        ],
        "correct": "A",
        "explanation": "Polinom qoldiq teoremasi (Remainder Theorem): f(x) ni (x - c) ga bo'lgandagi qoldiq f(c) ga teng. Bu yerda c = 2. x = 2 ni qo'yamiz: f(2) = (2)^3 - 4(2)^2 + 7(2) - 5 = 8 - 16 + 14 - 5 = 1. To'g'ri javob: A (1). Noto'g'ri variantlar tahlili: B (5) — ozod hadni adashtirish; C (-1) — hisoblashdagi ishora xatosi; D (9) — darajalarni xato hisoblashdagi noto'g'ri variant.",
        "strategy_or_hack": "⚡ POLINOM QOIDASI: f(x) ni (x - 2) ga bo'lish uchun x = 2 ni funksiyaga qo'yish kifoya!"
    },
    {
        "id": "m_b4_17",
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Nonlinear functions (quadratic vertex/standard form, exponential models, polynomials)",
        "difficulty": "Easy",
        "passage": None,
        "question": "A business computer system depreciates in monetary value according to the model V(t) = 2,400 * (0.85)^t, where V(t) is the estimated value in dollars t years after purchase. By what percentage does the computer system's value decrease each year?",
        "options": [
            {"key": "A", "text": "15%"},
            {"key": "B", "text": "85%"},
            {"key": "C", "text": "24%"},
            {"key": "D", "text": "1.5%"}
        ],
        "correct": "A",
        "explanation": "Eksponensial kamayish modeli: V(t) = V0 * (1 - r)^t, bu yerda r — yillik kamayish foizi. Asos 0.85 ga teng: 1 - r = 0.85 => r = 0.15, ya'ni har yili 15% ga kamayadi. To'g'ri javob: A (15%). Noto'g'ri variantlar tahlili: B (85%) — qolgan qiymat ulushini kamayish foizi deb adashish klassik SAT tuzog'i; C (24%) — boshlang'ich narxdagi son bilan adashish; D (1.5%) — vergul siljishi xatosi.",
        "strategy_or_hack": "⚡ SAT KONSEPSIYASI: Kamayish foizi = 1 - asos = 1 - 0.85 = 0.15 (15%)!"
    },
    {
        "id": "m_b4_18",
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Equivalent expressions (factoring, polynomial arithmetic)",
        "difficulty": "Hard",
        "passage": None,
        "question": "If x and y are positive real numbers such that the expression (x^(5/2) * y^(-1/3)) / (x^3 * y^(-4/3))^(1/2) is equivalent to x^a * y^b, what is the value of the product a * b?",
        "options": [
            {"key": "A", "text": "1/3"},
            {"key": "B", "text": "2/3"},
            {"key": "C", "text": "1"},
            {"key": "D", "text": "-1/6"}
        ],
        "correct": "A",
        "explanation": "Kasr maxrajini soddalashtiramiz: (x^3 * y^(-4/3))^(1/2) = x^(3/2) * y^(-2/3). Endi suratni maxrajga bo'lamiz: x ning darajasi a = 5/2 - 3/2 = 2/2 = 1. y ning darajasi b = -1/3 - (-2/3) = -1/3 + 2/3 = 1/3. Ko'paytma qiymati: a * b = 1 * (1/3) = 1/3. To'g'ri javob: A (1/3). Noto'g'ri variantlar tahlili: B (2/3) — darajalarni qo'shib yuborishdagi xato; C (1) — faqat a qiymatini belgilash tuzog'i; D (-1/6) — ishoralarni noto'g'ri ko'paytirish xatosi.",
        "strategy_or_hack": "⚡ DARAJA QOIDALARI: (x^m)^n = x^(m*n) va x^m / x^n = x^(m-n). Bosqichma-bosqich hisoblang: a=1, b=1/3 => ab = 1/3!"
    },
    {
        "id": "m_b4_19",
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Nonlinear functions (quadratic vertex/standard form, exponential models, polynomials)",
        "difficulty": "Medium",
        "passage": None,
        "question": "A civil engineer models the parabolic cable of a suspension footbridge using the function h(x) = 0.04(x - 25)^2 + 8, where h(x) is the height of the cable in meters above the water and x is the horizontal distance in meters from the western anchorage (0 <= x <= 50). What is the minimum height, in meters, of the cable above the water?",
        "options": [
            {"key": "A", "text": "8"},
            {"key": "B", "text": "25"},
            {"key": "C", "text": "0.04"},
            {"key": "D", "text": "33"}
        ],
        "correct": "A",
        "explanation": "Parabola cho'qqi formulasida (vertex form) berilgan: h(x) = a(x - h)^2 + k. Bu yerda a = 0.04 > 0 bo'lgani sababli parabolaning shoxlari yuqoriga qaragan va kabel o'zining eng past (minimum) balandligiga cho'qqi nuqtasida erishadi: k = 8 metr (x = 25 metr masofada). To'g'ri javob: A (8). Noto'g'ri variantlar tahlili: B (25) — minimumga erishiladigan gorizontal masofa x ni balandlik deb chalkashtirish; C (0.04) — burchak koeffitsiyenti; D (33) — 25 + 8 ni qo'shib yuborishdagi chalg'ituvchi variant.",
        "strategy_or_hack": "⚡ VERTEX SHAKLI: h(x) = a(x - 25)^2 + 8 da eng kichik qiymat to'g'ridan-to'g'ri ozod had k = 8 bo'ladi!"
    },
    {
        "id": "m_b4_20",
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Nonlinear functions (quadratic vertex/standard form, exponential models, polynomials)",
        "difficulty": "Medium",
        "passage": None,
        "question": "In the xy-plane, what is the minimum point of the parabola defined by the function h(x) = x^2 + 8x + 23?",
        "options": [
            {"key": "A", "text": "(-4, 7)"},
            {"key": "B", "text": "(4, 7)"},
            {"key": "C", "text": "(-4, 23)"},
            {"key": "D", "text": "(8, 23)"}
        ],
        "correct": "A",
        "explanation": "To'la kvadratga ajratamiz: h(x) = (x^2 + 8x + 16) + 23 - 16 = (x + 4)^2 + 7. Parabolaning cho'qqisi: (-4, 7). Parabola yuqoriga qaragan (a = 1 > 0), shuning uchun cho'qqi minimum nuqtadir. To'g'ri javob: A ((-4, 7)). Noto'g'ri variantlar tahlili: B ((4, 7)) — ishorani adashtirish klassik tuzog'i; C ((-4, 23)) — y-koordinatani to'g'rilamaslik xatosi; D — koeffitsiyentlarni to'g'ridan-to'g'ri olishdagi xato variant.",
        "strategy_or_hack": "⚡ DESMOS: y = x^2 + 8x + 23 ni kiriting va eng pastki nuqtani bosing: (-4, 7)."
    },
    {
        "id": "m_b4_21",
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Equivalent expressions (factoring, polynomial arithmetic)",
        "difficulty": "Easy",
        "passage": None,
        "question": "For all positive values of x, which of the following expressions is equivalent to (x^(3/4) * x^(1/2)) / x^(1/4)?",
        "options": [
            {"key": "A", "text": "x"},
            {"key": "B", "text": "x^2"},
            {"key": "C", "text": "x^(3/8)"},
            {"key": "D", "text": "x^(5/4)"}
        ],
        "correct": "A",
        "explanation": "Daraja qoidalarini qo'llaymiz: Bir xil asosli sonlar ko'paytirilganda darajalar qo'shiladi, bo'linganda ayiriladi: Daraja = 3/4 + 1/2 - 1/4 = 3/4 + 2/4 - 1/4 = 4/4 = 1. Demak x^1 = x. To'g'ri javob: A (x). Noto'g'ri variantlar tahlili: B (x^2) — qo'shishda xato qilish; C (x^(3/8)) — darajalarni ko'paytirib yuborishdagi qo'pol xato; D (x^(5/4)) — maxrajdagi darajani ayirishni unutish tuzog'i.",
        "strategy_or_hack": "⚡ DARAJA QOIDASI: x^(a) * x^(b) / x^(c) = x^(a + b - c). 3/4 + 2/4 - 1/4 = 1."
    },
    {
        "id": "m_b4_22",
        "section": "math",
        "domain": "Advanced Math",
        "skill": "Equivalent expressions (factoring, polynomial arithmetic)",
        "difficulty": "Hard",
        "passage": None,
        "question": "The polynomial function p is defined by p(x) = x^3 - 5x^2 - 4x + 20. Which of the following is NOT an x-intercept of the graph of p in the xy-plane?",
        "options": [
            {"key": "A", "text": "(4, 0)"},
            {"key": "B", "text": "(2, 0)"},
            {"key": "C", "text": "(-2, 0)"},
            {"key": "D", "text": "(5, 0)"}
        ],
        "correct": "A",
        "explanation": "Guruhlash usuli bilan ko'paytuvchilarga ajratamiz: p(x) = x^2(x - 5) - 4(x - 5) = (x^2 - 4)(x - 5) = (x - 2)(x + 2)(x - 5). Funksiyaning nollari (x-kesishmalari): x = 2, x = -2 va x = 5. Demak (2, 0), (-2, 0) va (5, 0) kesishmalar hisoblanadi. (4, 0) esa kesishma emas (p(4) = 64 - 80 - 16 + 20 = -12 != 0). To'g'ri javob: A ((4, 0)). Noto'g'ri variantlar tahlili: B, C va D haqiqiy kesishmalar bo'lgani sababli savol shartiga ('NOT an x-intercept') mos kelmaydi.",
        "strategy_or_hack": "⚡ VARIANTLARNI QO'YIB KO'RISH: p(4) = 4^3 - 5(16) - 4(4) + 20 = 64 - 80 - 16 + 20 = -12 != 0. Demak (4, 0) x-kesishma emas!"
    },

    # =========================================================================
    # PROBLEM-SOLVING AND DATA ANALYSIS (10 Questions)
    # =========================================================================
    {
        "id": "m_b4_23",
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Two-way tables, probability, and conditional probability",
        "difficulty": "Medium",
        "passage": None,
        "question": "A clinical trial evaluated a therapeutic drug on 100 participants. Among the 50 participants receiving the drug (Group A), 35 improved and 15 did not. Among the 50 participants receiving a placebo (Group B), 20 improved and 30 did not. If a participant who improved is chosen at random, what is the probability that this participant received the drug (Group A)?",
        "options": [
            {"key": "A", "text": "7/11"},
            {"key": "B", "text": "35/50"},
            {"key": "C", "text": "35/100"},
            {"key": "D", "text": "1/2"}
        ],
        "correct": "A",
        "explanation": "Shartli ehtimollik: 'If a participant who improved is chosen at random...' sharti maxraj faqat yaxshilanganlar soni bo'lishini bildiradi: Jami yaxshilanganlar = 35 (Group A) + 20 (Group B) = 55. Ularning ichidan preparat qabul qilganlar soni = 35. Ehtimollik = 35 / 55 = 7 / 11. To'g'ri javob: A (7/11). Noto'g'ri variantlar tahlili: B (35/50) — Group A ning jami soniga bo'lish xatosi; C (35/100) — barcha 100 qatnashchiga bo'lish tuzog'i; D (1/2) — guruhlarni teng deb yanglishish.",
        "strategy_or_hack": "⚡ SHARTLI EHTIMOLLIK: 'Given that...' yoki 'If a participant who improved...' so'zlari maxrajni faqat yaxshilanganlar (35+20=55) ga cheklaydi!"
    },
    {
        "id": "m_b4_24",
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Percentages (percent increase/decrease, multi-step word problems)",
        "difficulty": "Medium",
        "passage": None,
        "question": "An investment fund gained 30% in its first fiscal year and subsequently declined by 10% in its second fiscal year. What was the overall percentage change of the fund across the two-year period?",
        "options": [
            {"key": "A", "text": "17% increase"},
            {"key": "B", "text": "20% increase"},
            {"key": "C", "text": "23% increase"},
            {"key": "D", "text": "15% increase"}
        ],
        "correct": "A",
        "explanation": "Multiplikator usuli: 1) 30% o'sish: 1.30. 2) 10% pasayish: 1 - 0.10 = 0.90. Yakuniy multiplikator: 1.30 * 0.90 = 1.17. 1.17 bu dastlabki qiymatga nisbatan 17% o'sish demakdir (1.17 - 1 = 0.17). To'g'ri javob: A (17% increase). Noto'g'ri variantlar tahlili: B (20% increase) — 30% - 10% = 20% deb foizlarni shunchaki ayirib yuborishdagi eng mashhur SAT tuzog'i; C (23%) va D (15%) — hisoblashdagi xato variantlar.",
        "strategy_or_hack": "⚡ $100 QOIDASI: Dastlab $100 bo'lsa: 30% oshgach $130 bo'ladi. $130 ning 10%i = $13. $130 - $13 = $117. Jami o'sish: 17%!"
    },
    {
        "id": "m_b4_25",
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Measures of center (mean, median) and spread (range, standard deviation)",
        "difficulty": "Medium",
        "passage": None,
        "question": "A small software startup employs 8 engineers with salaries ranging from $40,000 to $60,000. When a new chief executive officer is hired with an annual salary of $350,000, which summary statistic of the employee compensation dataset increases by the greatest percentage?",
        "options": [
            {"key": "A", "text": "The mean"},
            {"key": "B", "text": "The median"},
            {"key": "C", "text": "Both increase by identical percentages"},
            {"key": "D", "text": "Neither increases"}
        ],
        "correct": "A",
        "explanation": "O'rtacha arifmetik qiymat (mean) anomal katta qiymatga (outlier $350,000) favqulodda sezgir va keskin ko'tariladi. Mediana esa o'rtadagi 1-2 ta qiymatning o'rniga qaraydi va juda kam miqdorda siljiydi. Shuning uchun eng katta foizli o'sish o'rtacha qiymatda (mean) ro'y beradi. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B — medianani sezgir deb yanglishish tuzog'i; C va D — statistik parametrlarning xususiyatlariga zid xato variantlar.",
        "strategy_or_hack": "⚡ SAT STATISTIKA QOIDASI: Ekstremal anomal qiymatlar (outliers) har doim o'rtacha qiymatni (mean) medianaga nisbatan ancha kuchli siljitadi!"
    },
    {
        "id": "m_b4_26",
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Inference from sample statistics and margin of error",
        "difficulty": "Hard",
        "passage": None,
        "question": "A researcher conducts a public opinion survey and determines a margin of error of 4% at a 95% confidence level. If the researcher wants to conduct a follow-up survey of the same population with a margin of error of 2% at the same confidence level, by what factor must the sample size be multiplied?",
        "options": [
            {"key": "A", "text": "4"},
            {"key": "B", "text": "2"},
            {"key": "C", "text": "8"},
            {"key": "D", "text": "16"}
        ],
        "correct": "A",
        "explanation": "Xatolik chegarasi (margin of error) tanlanma hajmining kvadrat ildiziga teskari proportsional: ME = z * sqrt(p(1-p) / n). Xatolikni 2 barobar kamaytirish uchun (4% dan 2% ga) tanlanma hajmi n roppa-rosa 2^2 = 4 barobarga oshirilishi shart. To'g'ri javob: A (4). Noto'g'ri variantlar tahlili: B (2) — ildizni hisobga olmasdan tanlanmani 2 marta oshirish yetadi deb o'ylash klassik tuzog'i; C (8) va D (16) — darajani noto'g'ri qo'llashdagi xato variantlar.",
        "strategy_or_hack": "⚡ SAMPLE SIZE FORMULASI: Xatolikni k marta kamaytirish uchun tanlanma sonini k^2 marta oshirish kerak: 2^2 = 4 marta!"
    },
    {
        "id": "m_b4_27",
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Ratios, rates, proportional relationships, and units",
        "difficulty": "Easy",
        "passage": None,
        "question": "A municipal water pump operates at a steady flow rate of 180 liters per minute. What is the flow rate of the pump in milliliters per second? (1 liter = 1,000 milliliters, 1 minute = 60 seconds)",
        "options": [
            {"key": "A", "text": "3,000"},
            {"key": "B", "text": "18,000"},
            {"key": "C", "text": "300"},
            {"key": "D", "text": "10,800"}
        ],
        "correct": "A",
        "explanation": "Birliklarni bosqichma-bosqich o'zgartiramiz: 180 litr / minut = (180 * 1,000 ml) / (60 soniya) = 180,000 ml / 60 soniya = 3,000 ml/soniya. To'g'ri javob: A (3,000). Noto'g'ri variantlar tahlili: B (18,000) — 60 o'rniga 10 ga bo'lish xatosi; C (300) — 1,000 o'rniga 100 ga ko'paytirish tuzog'i; D (10,800) — bo'lish o'rniga 60 ga ko'paytirib yuborishdagi xato variant.",
        "strategy_or_hack": "⚡ BIRLIKLAR ZANJIRI: (180 L / 1 min) * (1000 mL / 1 L) * (1 min / 60 s) = 180000 / 60 = 3000 mL/s."
    },
    {
        "id": "m_b4_28",
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Scatterplots, linear/exponential/quadratic models, and residuals",
        "difficulty": "Medium",
        "passage": None,
        "question": "A pediatric study calculates a linear correlation coefficient of r = -0.89 between daily recreational screen hours and nighttime sleep duration in adolescents. Which of the following is the most valid interpretation of this statistic?",
        "options": [
            {"key": "A", "text": "There is a strong negative linear association between daily screen time and sleep duration."},
            {"key": "B", "text": "Daily screen time causes adolescents to experience lower sleep duration."},
            {"key": "C", "text": "There is a weak positive linear association between the two variables."},
            {"key": "D", "text": "Exactly 89% of adolescents experience inadequate sleep duration."}
        ],
        "correct": "A",
        "explanation": "r = -0.89 qiymati noldan ancha uzoq va -1 ga yaqin bo'lgani uchun bu kuchli manfiy chiziqli bog'liqlikni (strong negative linear association) anglatadi. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B — korrelyatsiya sabab-oqibatni (causation) isbotlamaydi, shuning uchun 'causes' so'zi statistik jihatdan xato; C — musbat emas, manfiy; D — 89% o'smirlar degan raqamli foiz matnga aloqador emas.",
        "strategy_or_hack": "⚡ SAT KONSEPSIYASI: 'Correlation does NOT imply causation' (Korrelyatsiya sababiyatni anglatmaydi). 'Causes' so'zi bo'lgan variantlar deyarli har doim noto'g'ri!"
    },
    {
        "id": "m_b4_29",
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Ratios, rates, proportional relationships, and units",
        "difficulty": "Easy",
        "passage": None,
        "question": "In a school science laboratory, the ratio of test tubes to glass beakers is 7 to 4. If the laboratory contains 84 test tubes, how many glass beakers are in the laboratory?",
        "options": [
            {"key": "A", "text": "48"},
            {"key": "B", "text": "56"},
            {"key": "C", "text": "36"},
            {"key": "D", "text": "64"}
        ],
        "correct": "A",
        "explanation": "Proporsiya tuzamiz: Prozkalar / Menzurkalar = 7 / 4. 84 / B = 7 / 4. Birlikka to'g'ri keluvchi miqdor: 84 / 7 = 12. Demak menzurkalar soni: 12 * 4 = 48 ta. To'g'ri javob: A (48). Noto'g'ri variantlar tahlili: B (56) — noto'g'ri proporsiya; C (36) — 84 ni 7 ga emas, 9 ga bo'lish xatosi; D (64) — hisob-kitobdagi adashish natijasidagi xato variant.",
        "strategy_or_hack": "⚡ PROPORSIONALLIK: 7 qism = 84 bo'lsa, 1 qism = 12. 4 qism = 4 * 12 = 48!"
    },
    {
        "id": "m_b4_30",
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Measures of center (mean, median) and spread (range, standard deviation)",
        "difficulty": "Medium",
        "passage": None,
        "question": "A student's course grade is calculated using a weighted average: Homework is weighted at 20%, the Midterm Exam at 30%, and the Final Exam at 50%. If the student earns 90 on Homework, 80 on the Midterm Exam, and 86 on the Final Exam, what is the student's final weighted course score?",
        "options": [
            {"key": "A", "text": "85"},
            {"key": "B", "text": "86"},
            {"key": "C", "text": "84"},
            {"key": "D", "text": "88"}
        ],
        "correct": "A",
        "explanation": "Vaznli o'rtacha qiymatni hisoblaymiz: Jami ball = (0.20 * 90) + (0.30 * 80) + (0.50 * 86) = 18 + 24 + 43 = 85 ball. To'g'ri javob: A (85). Noto'g'ri variantlar tahlili: B (86) — ballarning oddiy arifmetik o'rtachasini olishga yaqin adashish; C (84) va D (88) — vaznlarni ko'paytirishdagi hisoblash xatolari.",
        "strategy_or_hack": "⚡ VAZNLI O'RTACHA: 0.2(90) + 0.3(80) + 0.5(86) = 18 + 24 + 43 = 85."
    },
    {
        "id": "m_b4_31",
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Percentages (percent increase/decrease, multi-step word problems)",
        "difficulty": "Easy",
        "passage": None,
        "question": "In a college cohort, 60% of students live in university dormitory halls. Of those students residing in dormitories, 45% participate in campus club sports. What percentage of the entire college cohort lives in dormitories AND participates in club sports?",
        "options": [
            {"key": "A", "text": "27%"},
            {"key": "B", "text": "52.5%"},
            {"key": "C", "text": "15%"},
            {"key": "D", "text": "30%"}
        ],
        "correct": "A",
        "explanation": "Foizning foizini hisoblaymiz: Jami talabalarning 60% yotoqxonada yashaydi (0.60). Ularning 45%i sport bilan shug'ullanadi (0.45). Jami ulush: 0.60 * 0.45 = 0.27, ya'ni 27%. To'g'ri javob: A (27%). Noto'g'ri variantlar tahlili: B (52.5%) — foizlarni qo'shib 2 ga bo'lish xatosi; C (15%) — 60% dan 45% ni ayirib qo'yishdagi qo'pol tuzoq; D (30%) — noo'rin yaxlitlashdagi xato variant.",
        "strategy_or_hack": "⚡ FOIZNING FOIZI: 0.60 * 0.45 = 0.27 (27%). Ko'paytirish orqali darhol topiladi!"
    },
    {
        "id": "m_b4_32",
        "section": "math",
        "domain": "Problem-Solving and Data Analysis",
        "skill": "Scatterplots, linear/exponential/quadratic models, and residuals",
        "difficulty": "Medium",
        "passage": None,
        "question": "The relationship between daily maximum temperature x, in degrees Celsius, and bottled iced tea sales y, in bottles, at an amusement park is modeled by the line of best fit y_pred = 1.8x + 14.5. Based on this model, what is the predicted number of iced tea bottles sold on a day when the maximum temperature reaches 30 degrees Celsius?",
        "options": [
            {"key": "A", "text": "68.5"},
            {"key": "B", "text": "54.0"},
            {"key": "C", "text": "65.0"},
            {"key": "D", "text": "72.5"}
        ],
        "correct": "A",
        "explanation": "Model formulasiga x = 30 ni qo'yamiz: y_pred = 1.8(30) + 14.5 = 54 + 14.5 = 68.5 shisha. To'g'ri javob: A (68.5). Noto'g'ri variantlar tahlili: B (54.0) — ozod had 14.5 ni qo'shishni unutish xatosi; C (65.0) va D (72.5) — 1.8 ga noto'g'ri ko'paytirishdagi chalg'ituvchi xato variantlar.",
        "strategy_or_hack": "⚡ HISOBLASH: 1.8 * 30 = 54. 54 + 14.5 = 68.5. 5 soniyada tayyor!"
    },

    # =========================================================================
    # GEOMETRY AND TRIGONOMETRY (8 Questions)
    # =========================================================================
    {
        "id": "m_b4_33",
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Circles (arc length, sector area, equation of a circle)",
        "difficulty": "Easy",
        "passage": None,
        "question": "In the xy-plane, what are the center coordinates and radius of the circle defined by the equation (x - 5)^2 + (y + 2)^2 = 49?",
        "options": [
            {"key": "A", "text": "Center (5, -2) and radius 7"},
            {"key": "B", "text": "Center (-5, 2) and radius 7"},
            {"key": "C", "text": "Center (5, -2) and radius 49"},
            {"key": "D", "text": "Center (-5, 2) and radius 49"}
        ],
        "correct": "A",
        "explanation": "Aylananing standart tenglamasi: (x - h)^2 + (y - k)^2 = r^2. Bu yerda h = 5, k = -2 bo'lgani uchun markaz (5, -2) da joylashgan. r^2 = 49 bo'lgani sababli radius r = sqrt(49) = 7 bo'ladi. To'g'ri javob: A. Noto'g'ri variantlar tahlili: B — markaz koordinatalarining ishoralarini teskari olish klassik tuzog'i; C va D — r^2 ni radius deb adashish xatosi.",
        "strategy_or_hack": "⚡ ISHORA VA RADIUS: (x - h) da markaz +h, (y + k) da markaz -k bo'ladi. Radius esa sqrt(49) = 7!"
    },
    {
        "id": "m_b4_34",
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Circles (arc length, sector area, equation of a circle)",
        "difficulty": "Medium",
        "passage": None,
        "question": "A circle has a radius of 8 centimeters. A sector on the circle subtends a central angle of (3pi)/4 radians. What is the area of this sector, in square centimeters?",
        "options": [
            {"key": "A", "text": "24pi"},
            {"key": "B", "text": "48pi"},
            {"key": "C", "text": "12pi"},
            {"key": "D", "text": "64pi"}
        ],
        "correct": "A",
        "explanation": "Sektor yuzi formulasi (radianlarda): Area = (1/2) * r^2 * theta. Bu yerda r = 8 va theta = 3pi / 4. Area = (1/2) * (8)^2 * (3pi / 4) = (1/2) * 64 * (3pi / 4) = 32 * (3pi / 4) = 8 * 3pi = 24pi sm^2. To'g'ri javob: A (24pi). Noto'g'ri variantlar tahlili: B (48pi) — 1/2 koeffitsiyentini unutish xatosi; C (12pi) — radiusni kvadratga ko'tarmaslik tuzog'i; D (64pi) — butun doira yuzasini belgilashdagi xato variant.",
        "strategy_or_hack": "⚡ SEKTOR YUZI FORMULASI: Area = 0.5 * r^2 * theta = 0.5 * 64 * (3pi/4) = 24pi."
    },
    {
        "id": "m_b4_35",
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Right triangles and trigonometry",
        "difficulty": "Easy",
        "passage": None,
        "question": "In an isosceles right triangle, the length of the hypotenuse is 16 * sqrt(2). What is the length of each leg?",
        "options": [
            {"key": "A", "text": "16"},
            {"key": "B", "text": "32"},
            {"key": "C", "text": "8 * sqrt(2)"},
            {"key": "D", "text": "8"}
        ],
        "correct": "A",
        "explanation": "Teng yonli to'g'ri burchakli uchburchak (45-45-90) qoidasiga ko'ra, gipotenuza katetdan sqrt(2) barobar katta: Gipotenuza = Katet * sqrt(2). Demak, Katet = Gipotenuza / sqrt(2) = (16 * sqrt(2)) / sqrt(2) = 16. To'g'ri javob: A (16). Noto'g'ri variantlar tahlili: B (32) — gipotenuzani 2 ga ko'paytirish xatosi; C (8*sqrt(2)) — 16 ni 2 ga bo'lib sqrt(2) ni qoldirish tuzog'i; D (8) — 16 ni 2 ga bo'lish xatosi.",
        "strategy_or_hack": "⚡ 45-45-90 UCHBURCHAK QOIDASI: Tomonlar nisbati 1 : 1 : sqrt(2). Gipotenuza 16*sqrt(2) bo'lsa, katetlar 16 ga teng!"
    },
    {
        "id": "m_b4_36",
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Right triangles and trigonometry",
        "difficulty": "Medium",
        "passage": None,
        "question": "In right triangle XYZ, angle Z measures 90 degrees. The length of the side opposite angle X is 15, and the length of the side adjacent to angle X is 8. What is the value of tan(X)?",
        "options": [
            {"key": "A", "text": "15/8"},
            {"key": "B", "text": "8/15"},
            {"key": "C", "text": "15/17"},
            {"key": "D", "text": "8/17"}
        ],
        "correct": "A",
        "explanation": "To'g'ri burchakli uchburchakda tangens ta'rifi: tan(X) = Qarama-qarshi katet / Yopishgan katet (Opposite / Adjacent). Bu yerda Opposite = 15 va Adjacent = 8. Shuning uchun tan(X) = 15/8. To'g'ri javob: A (15/8). Noto'g'ri variantlar tahlili: B (8/15) — kasrni to'ntarib kotangensni belgilash tuzog'i; C (15/17) — sin(X) ning qiymati (Opposite / Hypotenuse); D (8/17) — cos(X) ning qiymati.",
        "strategy_or_hack": "⚡ SOH CAH TOA: TOA -> Tan = Opposite / Adjacent = 15 / 8!"
    },
    {
        "id": "m_b4_37",
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Area and volume",
        "difficulty": "Easy",
        "passage": None,
        "question": "A solid rectangular storage container has a base length of 12 centimeters, a base width of 5 centimeters, and a vertical height of 8 centimeters. What is the total volume of the container in cubic centimeters?",
        "options": [
            {"key": "A", "text": "480"},
            {"key": "B", "text": "240"},
            {"key": "C", "text": "392"},
            {"key": "D", "text": "520"}
        ],
        "correct": "A",
        "explanation": "To'g'ri burchakli parallelepiped hajmi formulasi: V = Uzunlik * Kenglik * Balandlik = 12 * 5 * 8 = 60 * 8 = 480 sm^3. To'g'ri javob: A (480). Noto'g'ri variantlar tahlili: B (240) — piramida formulasi deb adashib 2 ga bo'lish xatosi; C (392) — to'liq sirt maydoni (surface area) bilan adashtirish klassik tuzog'i; D (520) — ko'paytirishdagi arifmetik xato.",
        "strategy_or_hack": "⚡ HAJM: V = l * w * h = 12 * 5 * 8 = 480."
    },
    {
        "id": "m_b4_38",
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Area and volume",
        "difficulty": "Hard",
        "passage": None,
        "question": "Triangle ABC is similar to triangle DEF, where vertices A, B, and C correspond to D, E, and F, respectively. Side AB has a length of 9, and corresponding side DE has a length of 21. If the area of triangle ABC is 36 square units, what is the area of triangle DEF in square units?",
        "options": [
            {"key": "A", "text": "196"},
            {"key": "B", "text": "84"},
            {"key": "C", "text": "144"},
            {"key": "D", "text": "252"}
        ],
        "correct": "A",
        "explanation": "O'xshashlik koeffitsiyenti: k = DE / AB = 21 / 9 = 7 / 3. O'xshash figuralarning maydonlari nisbati o'xshashlik koeffitsiyentining kvadratiga teng (k^2): Area(DEF) = Area(ABC) * k^2 = 36 * (7 / 3)^2 = 36 * (49 / 9) = 4 * 49 = 196 kvadrat birlik. To'g'ri javob: A (196). Noto'g'ri variantlar tahlili: B (84) — maydonni k ga (kvadratsiz) ko'paytirib qo'yish tuzog'i (36 * 7/3 = 84); C (144) va D (252) — noto'g'ri hisoblashdagi xato variantlar.",
        "strategy_or_hack": "⚡ MAYDON NISBATI: Tomonlar nisbati 7/3 bo'lsa, maydonlar nisbati (7/3)^2 = 49/9. 36 * 49/9 = 4 * 49 = 196!"
    },
    {
        "id": "m_b4_39",
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Circles (arc length, sector area, equation of a circle)",
        "difficulty": "Medium",
        "passage": None,
        "question": "In a circle, an inscribed angle intercepts an arc measuring 130 degrees. What is the measure, in degrees, of the inscribed angle?",
        "options": [
            {"key": "A", "text": "65"},
            {"key": "B", "text": "130"},
            {"key": "C", "text": "260"},
            {"key": "D", "text": "50"}
        ],
        "correct": "A",
        "explanation": "Aylanaga ichki chizilgan burchak (inscribed angle) o'zi tiralgan yoy o'lchovining yarmiga teng: Burchak = Yoy / 2 = 130 / 2 = 65 gradus. To'g'ri javob: A (65). Noto'g'ri variantlar tahlili: B (130) — markaziy burchak bilan adashtirish klassik tuzog'i; C (260) — 2 ga ko'paytirib yuborish xatosi; D (50) — 180 dan ayirishdagi noto'g'ri variant.",
        "strategy_or_hack": "⚡ ICHKI CHIZILGAN BURCHAK: Ichki chizilgan burchak = Yoy / 2 = 130 / 2 = 65°. Markaziy burchak esa yoyga teng bo'ladi!"
    },
    {
        "id": "m_b4_40",
        "section": "math",
        "domain": "Geometry and Trigonometry",
        "skill": "Area and volume",
        "difficulty": "Medium",
        "passage": None,
        "question": "A right circular cone has a base radius of 6 centimeters and a vertical height of 10 centimeters. What is the total volume of the cone, in cubic centimeters?",
        "options": [
            {"key": "A", "text": "120pi"},
            {"key": "B", "text": "360pi"},
            {"key": "C", "text": "60pi"},
            {"key": "D", "text": "40pi"}
        ],
        "correct": "A",
        "explanation": "Konus hajmi formulasi: V = (1/3) * pi * r^2 * h. Bu yerda r = 6 va h = 10. V = (1/3) * pi * (6)^2 * 10 = (1/3) * pi * 36 * 10 = 12 * 10 * pi = 120pi sm^3. To'g'ri javob: A (120pi). Noto'g'ri variantlar tahlili: B (360pi) — silindr deb adashib 1/3 koeffitsiyentini unutish tuzog'i; C (60pi) — radiusni kvadratga ko'tarmaslik xatosi; D (40pi) — arifmetik xato variant.",
        "strategy_or_hack": "⚡ KONUS HAJMI: V = (1/3) * pi * r^2 * h = (1/3) * pi * 36 * 10 = 120pi."
    }
]
