"""
Curated question & content bank for automated daily posting with 10-word power packs.
"""

IELTS_VOCAB_PACKS = [
    {
        "topic": "Technology, Society & Modern Life",
        "words": [
            {"w": "Ubiquitous", "m": "Hamma joyda uchraydigan", "c": "ubiquitous presence"},
            {"w": "Proliferation", "m": "Jadal ko'payish, tarqalish", "c": "rapid proliferation"},
            {"w": "Indispensable", "m": "O'rnini bosib bo'lmas, zarur", "c": "indispensable tool"},
            {"w": "Transformative", "m": "Tarixiy o'zgartiruvchi", "c": "transformative impact"},
            {"w": "Obsolete", "m": "Eskirgan, qo'llanilmaydigan", "c": "render obsolete"},
            {"w": "Detrimental", "m": "Zararli, ziyon keltiruvchi", "c": "detrimental effect"},
            {"w": "Plausible", "m": "Ishonarli, aqlga to'g'ri keladigan", "c": "plausible explanation"},
            {"w": "Unprecedented", "m": "Misli ko'rilmagan", "c": "unprecedented scale"},
            {"w": "Exacerbate", "m": "Vaziyatni og'irlashtirmoq", "c": "exacerbate tensions"},
            {"w": "Paradigm", "m": "Yangi model, qarash tizimi", "c": "paradigm shift"}
        ]
    },
    {
        "topic": "Education, Brain & Intellectual Development",
        "words": [
            {"w": "Acquisition", "m": "Egallash, o'zlashtirish", "c": "language acquisition"},
            {"w": "Cognitive", "m": "Aqliy, tafakkurga oid", "c": "cognitive development"},
            {"w": "Curriculum", "m": "O'quv dasturi", "c": "comprehensive curriculum"},
            {"w": "Proficiency", "m": "Yuqori darajadagi malaka", "c": "linguistic proficiency"},
            {"w": "Facilitate", "m": "Yengillashtirmoq, ko'maklashmoq", "c": "facilitate learning"},
            {"w": "Pedagogical", "m": "Pedagogik, o'qitishga oid", "c": "pedagogical approach"},
            {"w": "Cultivate", "m": "Rivojlantirmoq, shakllantirmoq", "c": "cultivate critical thinking"},
            {"w": "Disparity", "m": "Tengsizlik, tafovut", "c": "educational disparity"},
            {"w": "Inherent", "m": "Tabiiy xos bo'lgan", "c": "inherent capability"},
            {"w": "Substantiate", "m": "Fikrni dalillar bilan isbotlamoq", "c": "substantiate claims"}
        ]
    }
]

SAT_QUIZZES = [
    {
        "type": "SAT Math (Heart of Algebra)",
        "question": "If 3x + 7 = 2(x + 4) + 5, what is the value of 2x - 3?",
        "options": ["5", "7", "9", "11"],
        "correct_option_id": 2,
        "explanation": "3x + 7 = 2x + 13 => x = 6 => 2(6) - 3 = 9."
    },
    {
        "type": "SAT Math (Advanced Math / Quadratics)",
        "question": "The quadratic equation x² - 8x + k = 0 has exactly ONE real solution. What is the value of k?",
        "options": ["8", "16", "32", "64"],
        "correct_option_id": 1,
        "explanation": "A quadratic equation has exactly one real solution when b² - 4ac = 0. 64 - 4k = 0 => k = 16."
    },
    {
        "type": "SAT Reading & Writing (Words in Context)",
        "question": "Although the new policy was met with skepticism, recent economic data suggests its positive impacts are not merely transitory but _______.",
        "options": ["ephemeral", "enduring", "redundant", "speculative"],
        "correct_option_id": 1,
        "explanation": "'Transitory' means temporary. Antonym needed: 'enduring' (lasting)."
    }
]

IELTS_TIPS = [
    {
        "title": "Writing Task 2: PEEL Usuli",
        "body": "Har bir abzasni 4 qismda tuzing: Point (Asosiy fikr), Explain (Nega to'g'riligi), Example (Misol), Link (Insho mavzusiga bog'lash)."
    },
    {
        "title": "SAT Reading: Transition Qoidasi",
        "body": "Agar variantlarda bir xil ma'nodagi ikkita bog'lovchi kelsa (masalan: Furthermore va Moreover), ikkalasi ham 100% xato bo'ladi."
    },
    {
        "title": "Speaking Part 3: PPF Usuli",
        "body": "Part 3 savollariga keng javob berish uchun Past (O'tmish), Present (Hozir), va Future (Kelajak) vaqtlarini solishtirib gapiring."
    }
]
