"""
Batch 5 Reading Questions (33 Items: r_b5_01 through r_b5_33)
Authentic Digital SAT style passages, distinct options, evidence-backed.
"""

from typing import Any

BATCH_5_READING: list[dict[str, Any]] = [
    # ==================== CRAFT AND STRUCTURE (17 Questions) ====================
    # --- Words in Context (9 Questions) ---
    {
        "id": "r_b5_01",
        "version": 1,
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Words in Context",
        "difficulty": "Easy",
        "status": "published",
        "passage": "During the mid-nineteenth century, steam locomotives revolutionized transcontinental shipping. Prior methods relied on horse-drawn wagons, which were notoriously sluggish and vulnerable to seasonal weather disruptions. The emergence of railroad networks rapidly transformed the commercial landscape, rendering long-distance freight delivery remarkably efficient.",
        "question": "As used in the text, what does the word 'sluggish' most nearly mean?",
        "options": [
            {"key": "A", "text": "Lazy"},
            {"key": "B", "text": "Slow-moving"},
            {"key": "C", "text": "Inflexible"},
            {"key": "D", "text": "Dormant"}
        ],
        "correct": "B",
        "explanation": "Matnda ot aravalari (horse-drawn wagons) poyezdlar bilan taqqoslanmoqda. Poyezdlar yuk yetkazishni 'tez va samarali' qilgan bo'lsa, avvalgi aravalar juda sekin va ob-havoga bog'liq bo'lgan. Shu sababli 'sluggish' so'zi bu kontekstda 'sekin harakatlanuvchi' (slow-moving) ma'nosini bildiradi. A varianti (lazy) shaxsiyatga xos bo'lib transport vositalariga nisbatan noto'g'ri ko'chma ma'nodir.",
        "strategy_or_hack": "⚡ SAT READING HACK: Kontekstdagi qarama-qarshilikka qarang: 'sluggish' so'zi keyingi gapdagi 'efficient and rapid' so'zlariga ziddir.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_02",
        "version": 1,
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Words in Context",
        "difficulty": "Medium",
        "status": "published",
        "passage": "In her critical monograph on avant-garde sculpture, art historian Evelyn Vance asserts that modernist installations cannot be appraised using classical geometric standards. Because modern sculptors deliberate to disrupt conventional symmetry, traditional frameworks are fundamentally ill-suited to capture the emotional resonance of their works.",
        "question": "As used in the text, what does the word 'appraised' most nearly mean?",
        "options": [
            {"key": "A", "text": "Purchased"},
            {"key": "B", "text": "Evaluated"},
            {"key": "C", "text": "Constructed"},
            {"key": "D", "text": "Preserved"}
        ],
        "correct": "B",
        "explanation": "Matnda modern san'at asarlarini klassik geometrik standartlar yordamida baholash yoki o'rganish mumkin emasligi aytilmoqda ('cannot be appraised using classical standards'). Demak, 'appraised' so'zi 'baholamoq' (evaluated) ma'nosida kelmoqda. A varianti (purchased - sotib olmoq) tijoriy baholash bilan adashtiruvchi tuzoqdir.",
        "strategy_or_hack": "⚡ SAT VOCAB IN CONTEXT: 'Standards' (mezonlar) bilan bog'langan fe'l tahliliy baholashni (evaluate) talab qiladi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_03",
        "version": 1,
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Words in Context",
        "difficulty": "Hard",
        "status": "published",
        "passage": "Physicist Clara Mendez notes that while quantum entanglement has been verified across microscopic distances, extrapolating these principles to macroscopic systems remains speculative. Any claims suggesting that everyday biological processes are governed by macro-entanglement must be regarded as _______, requiring rigorous experimental corroboration before gaining scientific consensus.",
        "question": "Which choice completes the text with the most logical and precise word?",
        "options": [
            {"key": "A", "text": "incontrovertible"},
            {"key": "B", "text": "conjectural"},
            {"key": "C", "text": "redundant"},
            {"key": "D", "text": "immutable"}
        ],
        "correct": "B",
        "explanation": "Matnda makroskopik tizimlarga kvant xossalarini tatbiq etish 'speculative' (taxminiy) ekani va jiddiy eksperimental isbot ('rigorous experimental corroboration') talab qilishi ta'kidlanmoqda. Demak, bunday da'volar tasdiqlanmagan, faraziy ya'ni 'conjectural' (taxminiy, farazga asoslangan) deb qaralishi lozim. A (shubhasiz) va D (o'zgarmas) mutlaqo teskari ma'noli variantlardir.",
        "strategy_or_hack": "⚡ SAT CONTEXT CLUE: 'Speculative' va 'requiring corroboration' kalit so'zlari bo'shliqqa aniq 'conjectural' so'zini joylashtirishni talab qiladi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_04",
        "version": 1,
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Words in Context",
        "difficulty": "Medium",
        "status": "published",
        "passage": "Ecologist Dr. Liam Park argues that introducing apex predators into fragmented nature reserves can sometimes yield _______ outcomes. While wolves in Yellowstone successfully restored riparian foliage by curtailing elk grazing, similar rewilding initiatives in smaller, arid habitats inadvertently triggered steep declines in endangered ground-nesting birds.",
        "question": "Which choice completes the text with the most logical and precise word?",
        "options": [
            {"key": "A", "text": "uniform"},
            {"key": "B", "text": "disparate"},
            {"key": "C", "text": "predictable"},
            {"key": "D", "text": "negligible"}
        ],
        "correct": "B",
        "explanation": "Matnda ikki xil muhitdagi oqibatlar taqqoslanmoqda: Yellowstone'da muvaffaqiyatli tiklanish yuz bergan, biroq kichikroq qurg'oqchil hududlarda qushlar populyatsiyasi keskin kamayib ketgan. Bu natijalar bir xil emas, balki bir-biridan butunlay farqli ('disparate' - contrasting/different) ekanini bildiradi. A va C variantlari qarama-qarshilikka zid.",
        "strategy_or_hack": "⚡ SAT CONTRAST CLUE: 'While X succeeded, Y triggered steep declines' strukturasi turlicha oqibatlarni (disparate outcomes) bildiradi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_05",
        "version": 1,
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Words in Context",
        "difficulty": "Hard",
        "status": "published",
        "passage": "Although the treaty was intended to foster enduring geopolitical stability, its ambiguous clauses regarding territorial boundaries actually _______ diplomatic friction. Rather than cementing peace, the disputed wording provoked repeated border skirmishes throughout the subsequent decade.",
        "question": "Which choice completes the text with the most logical and precise word?",
        "options": [
            {"key": "A", "text": "exacerbated"},
            {"key": "B", "text": "mollified"},
            {"key": "C", "text": "precluded"},
            {"key": "D", "text": "rectified"}
        ],
        "correct": "A",
        "explanation": "Matndagi 'Although' bog'lovchisi kutilgan maqsad (barqarorlik) bilan haqiqiy natija (kelishmovchiliklarning kuchayishi, 'border skirmishes') o'rtasidagi ziddiyatni bildiradi. Noaniq bandlar diplomatik nizoni yumshatmagan, aksincha yanada og'irlashtirgan ('exacerbated' - worsened). B (yumshatmoq) va C (oldini olmoq) kontekstga ziddir.",
        "strategy_or_hack": "⚡ SAT CLUE: 'provoked border skirmishes' natijasi bo'shliqda salbiy, vaziyatni yomonlashtiruvchi fe'l ('exacerbated') bo'lishini talab qiladi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_06",
        "version": 1,
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Words in Context",
        "difficulty": "Easy",
        "status": "published",
        "passage": "Marine biologists discovered that deep-sea hydrothermal vents support remarkably robust ecosystems despite the extreme pressure and complete absence of sunlight. Bacteria thriving near the vents convert toxic sulfur compounds into usable metabolic energy, providing sustenance for complex organisms like giant tube worms.",
        "question": "As used in the text, what does the word 'robust' most nearly mean?",
        "options": [
            {"key": "A", "text": "Fragile"},
            {"key": "B", "text": "Rigid"},
            {"key": "C", "text": "Resilient"},
            {"key": "D", "text": "Complicated"}
        ],
        "correct": "C",
        "explanation": "Chuqur dengizdagi haddan tashqari yuqori bosim va mutlaq qorong'ulik kabi og'ir sharoitlarga qaramay ('despite extreme pressure...'), ekotizimlar rivojlanmoqda va hayot davom etmoqda. Bunday chidamlilik va bardoshlilikni ifodalash uchun 'robust' so'zi 'resilient' (chidamliligi yuqori, yashovchan) ma'nosini bildiradi. A varianti (fragile - nozik) to'liq ziddir.",
        "strategy_or_hack": "⚡ SAT CONTEXT: 'Thriving despite extreme conditions' sharoitida ekotizim 'resilient' (bardoshli) bo'ladi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_07",
        "version": 1,
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Words in Context",
        "difficulty": "Medium",
        "status": "published",
        "passage": "Urban planners initially anticipated that opening a secondary highway bypass would alleviate morning traffic congestion in the downtown core. However, transportation economists noted that the new route merely induced additional automobile demand, leaving overall commute times essentially _______.",
        "question": "Which choice completes the text with the most logical and precise word?",
        "options": [
            {"key": "A", "text": "unaltered"},
            {"key": "B", "text": "abbreviated"},
            {"key": "C", "text": "eliminated"},
            {"key": "D", "text": "sporadic"}
        ],
        "correct": "A",
        "explanation": "'However' bog'lovchisi kutilgan yengillik amalga oshmaganini ko'rsatadi. Yangi yo'l qo'shimcha talabni yuzaga keltirgani sababli, umumiy yo'l vaqti deyarli o'zgarishsiz qolgan ('unaltered' - unchanged). B (qisqargan) va C (yo'qolgan) kutilgan samara bo'lib, 'However' inkoriga to'g'ri kelmaydi.",
        "strategy_or_hack": "⚡ SAT LOGIC: 'merely induced additional demand' iborasi tiqilinch yechilmaganini, ya'ni vaqt o'zgarmay qolganini (unaltered) anglatadi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_08",
        "version": 1,
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Words in Context",
        "difficulty": "Hard",
        "status": "published",
        "passage": "Historian Marcus Sterling contends that the prime minister's public persona of folksy simplicity was entirely _______; private archival diaries reveal a shrewd, calculating tactician who carefully orchestrated every public appearance to neutralize political rivals.",
        "question": "Which choice completes the text with the most logical and precise word?",
        "options": [
            {"key": "A", "text": "sincere"},
            {"key": "B", "text": "manufactured"},
            {"key": "C", "text": "inconsequential"},
            {"key": "D", "text": "transparent"}
        ],
        "correct": "B",
        "explanation": "Matn bosh vazirning omma oldidagi sodda ko'rinishi (folksy simplicity) bilan shaxsiy kundaliklaridagi o'ta ayyor va hisob-kitobli taktikasi (calculating tactician) o'rtasidagi soxtalikni ochib beradi. Demak, uning sodda qiyofasi samimiy emas, balki ataylab to'qib chiqarilgan, sun'iy yaratilgan ('manufactured' - fabricated/contrived).",
        "strategy_or_hack": "⚡ SAT CONTRAST CLUE: 'carefully orchestrated' va 'calculating' so'zlari ochiq qiyofaning 'manufactured' (sun'iy yasalgan) ekanini isbotlaydi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_09",
        "version": 1,
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Words in Context",
        "difficulty": "Medium",
        "status": "published",
        "passage": "In literary criticism, the term 'polyphonic' is often applied to novels where the narrator's perspective does not subordinate the viewpoints of other characters. Instead, diverse voices retain distinct autonomy, engaging in an open dialogue that remains unresolved by an authoritative narrative voice.",
        "question": "As used in the text, what does the word 'subordinate' most nearly mean?",
        "options": [
            {"key": "A", "text": "Overpower"},
            {"key": "B", "text": "Celebrate"},
            {"key": "C", "text": "Analyze"},
            {"key": "D", "text": "Illustrate"}
        ],
        "correct": "A",
        "explanation": "Matnda aytilishicha, polifonik asarda hikoyachi boshqa qahramonlarning qarashlarini o'ziga bo'ysundirmaydi yoki bosib qo'ymaydi ('does not subordinate... instead characters retain distinct autonomy'). Demak, 'subordinate' bu yerda 'ustun kelmoq, bosib olmoq' (overpower / make secondary) ma'nosida ishlatilgan.",
        "strategy_or_hack": "⚡ SAT OPPOSITE CONTEXT: 'Does not subordinate... instead retain distinct autonomy' qarama-qarshiligi 'subordinate' = overpower ekanini ko'rsatadi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },

    # --- Text Structure and Purpose (4 Questions) ---
    {
        "id": "r_b5_10",
        "version": 1,
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Text Structure and Purpose",
        "difficulty": "Medium",
        "status": "published",
        "passage": "For decades, behavioral economists maintained that humans make consumer choices primarily based on rational utility calculations. In 2002, Daniel Kahneman presented empirical evidence demonstrating that cognitive heuristics and loss aversion consistently steer decision-makers away from purely mathematical optimization. Today, contemporary financial analysts increasingly integrate psychological profiling into risk management algorithms.",
        "question": "Which choice best describes the overall structure of the text?",
        "options": [
            {"key": "A", "text": "It outlines a longstanding theory, describes a pivotal empirical challenge to it, and explains its current disciplinary impact."},
            {"key": "B", "text": "It presents an economic dilemma, proposes two incompatible resolutions, and endorses the more mathematically rigorous model."},
            {"key": "C", "text": "It criticizes traditional psychological models, highlights their methodological flaws, and advocates for strict laboratory testing."},
            {"key": "D", "text": "It traces the historical biography of an influential researcher and analyzes his most celebrated publication."}
        ],
        "correct": "A",
        "explanation": "Matn uch bosqichli tuzilishga ega: 1) Ko'p yillik klassik ratsional model bayon qilinadi ('For decades...'); 2) Kahneman tomonidan keltirilgan tajribaviy e'tiroz va xulq-atvor omillari ko'rsatiladi ('In 2002, presented evidence...'); 3) Hozirgi kunda bu o'zgarishlar moliya sohasida qanday qo'llanilayotgani tushuntiriladi ('Today, analysts integrate...'). Bu A variantiga to'liq mos keladi.",
        "strategy_or_hack": "⚡ SAT TEXT STRUCTURE: Uch bosqichli xronologiyani ajrating: Past (For decades) -> Turning point (In 2002) -> Present (Today).",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_11",
        "version": 1,
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Text Structure and Purpose",
        "difficulty": "Hard",
        "status": "published",
        "passage": "Botanist Sarah Jenkins explores how mycorrhizal fungi networks facilitate resource exchange among mature forest trees. While skeptics initially dismissed the concept of inter-plant collaboration as romanticized teleology, Jenkins utilizes isotopic carbon tracing to unequivocally demonstrate that shaded understory seedlings receive vital carbohydrates from sunlit canopy trees via subterranean fungal threads.",
        "question": "What is the primary purpose of the text?",
        "options": [
            {"key": "A", "text": "To introduce Jenkins's empirical findings as validation for an ecological hypothesis once met with skepticism"},
            {"key": "B", "text": "To caution researchers against relying on isotopic tracing when studying subterranean ecosystems"},
            {"key": "C", "text": "To argue that mature canopy trees prioritize their own survival over the nourishment of seedlings"},
            {"key": "D", "text": "To illustrate the chemical composition of carbohydrates generated through fungal photosynthesis"}
        ],
        "correct": "A",
        "explanation": "Matn Jenkinsning tajribaviy tadqiqoti (izotopik uglerod tekshiruvi) ilgari skeptiklar tomonidan inkor etilgan 'o'simliklararo resurs almashinuvi' gipotezasini qat'iy isbotlab berganini yoritish uchun yozilgan. A varianti ushbu asosiy maqsadni eng to'liq va aniq ifodalaydi. B varianti metodni rad etishni aytib matnga zid, C esa daraxtlar ko'chatlarga yordam berayotganiga teskari.",
        "strategy_or_hack": "⚡ SAT PURPOSE HACK: Skeptiklarning dastlabki shubhasini yenguvchi ilmiy dalilni taqdim etish matnning markaziy niyatidir.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_12",
        "version": 1,
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Text Structure and Purpose",
        "difficulty": "Easy",
        "status": "published",
        "passage": "Geologists categorize rocks into three foundational groups: igneous, sedimentary, and metamorphic. Igneous rocks form directly from cooling molten magma or lava. Sedimentary rocks aggregate from compressed mineral particles and organic debris over millennia. Finally, metamorphic rocks result from pre-existing formations undergoing intense underground thermal and pressure transformations without completely melting.",
        "question": "Which choice best describes the function of the second sentence in the text?",
        "options": [
            {"key": "A", "text": "It provides a specific defining characteristic of one of the categories introduced in the opening sentence."},
            {"key": "B", "text": "It challenges the conventional categorization presented by earlier mineralogists."},
            {"key": "C", "text": "It summarizes the primary distinction between sedimentary and metamorphic specimens."},
            {"key": "D", "text": "It explains why volcanic eruptions are necessary for sedimentary rock creation."}
        ],
        "correct": "A",
        "explanation": "Birinchi gapda tog' jinslarining 3 ta turi (igneous, sedimentary, metamorphic) aytiladi. Ikkinchi gap esa ulardan birinchisi - magma/lavaning sovishidan hosil bo'ladigan vulqon (igneous) jinslarining xususiyatini ta'riflab beradi. Shuning uchun A varianti eng to'g'ri tahlildir.",
        "strategy_or_hack": "⚡ SAT SENTENCE FUNCTION: 1-gap umumiy toifalarni sanaydi, 2-gap esa 1-toifaga (igneous) bevosita aniqlik kiritadi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_13",
        "version": 1,
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Text Structure and Purpose",
        "difficulty": "Hard",
        "status": "published",
        "passage": "In analyzing the sonnets of John Donne, literary critic Arthur Bloom notes that Donne's abrupt conversational openings simulate the immediacy of real-time speech. Rather than adopting the ornate, decorative phrasing characteristic of Elizabethan court poetry, Donne thrusts the reader into the midst of an intimate intellectual argument, thereby dismantling the polished facade traditionally expected in lyric verse.",
        "question": "Which choice best states the primary function of the underlined claim regarding Elizabethan court poetry?",
        "options": [
            {"key": "A", "text": "It establishes a conventional stylistic baseline against which Donne's innovative poetic technique is contrasted."},
            {"key": "B", "text": "It demonstrates that Donne's contemporaries unanimously condemned his departures from tradition."},
            {"key": "C", "text": "It proves that Elizabethan lyric verse was aesthetically superior to metaphysical poetry."},
            {"key": "D", "text": "It provides historical evidence that Donne intended to mock the royal court's literary patrons."}
        ],
        "correct": "A",
        "explanation": "Muallif Yelizaveta davri saroy she'riyatini ('ornate, decorative phrasing') Donnening yangicha, suhbatdoshlikka asoslangan uslubini solishtirish va uning o'ziga xosligini bo'rtirib ko'rsatish uchun an'anaviy fon (stylistic baseline) sifatida keltirmoqda. B, C va D matnda aytilmagan asossiz xulosalardir.",
        "strategy_or_hack": "⚡ SAT RHETORICAL FUNCTION: An'anaviy uslubni keltirishdan maqsad - yangi muallifning innovatsiyasini kontrast orqali yaqqol ko'rsatishdir.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },

    # --- Cross-Text Connections (4 Questions) ---
    {
        "id": "r_b5_14",
        "version": 1,
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Cross-Text Connections",
        "difficulty": "Medium",
        "status": "published",
        "passage": "Text 1\nAstronomer David Kuan argues that the detection of atmospheric phosphine on Venus provides compelling indirect evidence of microbial life suspended in the planet's sulfuric cloud decks, as non-biological abiotic synthesis of phosphine under Venusian conditions is thermodynamically unfeasible according to known chemical pathways.\n\nText 2\nAtmospheric chemist Elena Rostova contends that invoking extraterrestrial biochemistry to explain Venusian phosphine is prematurely speculative. Rostova's laboratory models show that deep-mantle volcanic plumes could vent volatile phosphide minerals into the upper atmosphere, where photolytic oxidation produces phosphine without any biological intervention.",
        "question": "Based on the texts, how would Rostova (Text 2) most likely respond to Kuan's claim in Text 1 regarding phosphine synthesis?",
        "options": [
            {"key": "A", "text": "By arguing that Kuan overlooked viable abiotic mechanisms involving volcanic mineral venting"},
            {"key": "B", "text": "By conceding that microbial metabolism is the only plausible explanation for Venusian sulfur clouds"},
            {"key": "C", "text": "By asserting that telescopic instruments completely misidentified the spectroscopic signature of phosphine"},
            {"key": "D", "text": "By demonstrating that phosphine decomposes too rapidly in sulfuric acid to ever be detected"}
        ],
        "correct": "A",
        "explanation": "Kuan (Text 1) nobiologik (abiotic) sintez imkonsiz deb hisoblaydi va shuning uchun fosfin mikrobial hayot dalili deydi. Rostova (Text 2) esa buni inkor etib, o'z laboratoriya modellarida vulqon minerallari (abiotic) orqali hech qanday biologiyasiz fosfin hosil bo'lishini ko'rsatgan. Shuning uchun Rostova Kuan nobiologik vulqon mexanizmlarini hisobga olmagan deb e'tiroz bildiradi. A to'g'ri.",
        "strategy_or_hack": "⚡ SAT PAIRED TEXTS: Kuan: 'abiotic synthesis is unfeasible' <-> Rostova: 'laboratory models show abiotic volcanic plumes produce it'. To'g'ridan-to'g'ri A varianti.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_15",
        "version": 1,
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Cross-Text Connections",
        "difficulty": "Hard",
        "status": "published",
        "passage": "Text 1\nHistorian Thomas Bennett argues that the collapse of the Western Roman Empire was fundamentally driven by external shocks: unprecedented nomadic migrations from Central Asia pushed Germanic confederacies across the Rhine and Danube frontiers, overwhelming Roman border defenses faster than administrative legions could redeploy.\n\nText 2\nClassicist Nadia Al-Mansoor maintains that external migrations merely administered the final blow to an empire already hollowed out by centuries of internal economic decay. Rampant currency debasement, severe labor shortages caused by agrarian plagues, and endemic tax evasion by the senatorial aristocracy had effectively crippled the imperial treasury long before the crossing of the Rhine.",
        "question": "Which choice best describes how Al-Mansoor (Text 2) views Bennett's central thesis in Text 1?",
        "options": [
            {"key": "A", "text": "As an accurate diagnosis that fully explains the collapse without needing economic factors"},
            {"key": "B", "text": "As mistaking an immediate catalytic event for the profound, underlying systemic causes of collapse"},
            {"key": "C", "text": "As fundamentally flawed because nomadic tribes were easily absorbed into Roman provincial governance"},
            {"key": "D", "text": "As an overestimation of the Roman imperial treasury's ability to finance frontier fortifications"}
        ],
        "correct": "B",
        "explanation": "Bennett tashqi bosqinlarni asosiy sabab deb biladi. Al-Mansoor esa tashqi bosqinlar faqatgina 'so'nggi zarba' (final blow) bo'lganini, imperiyaning haqiqiy va chuqur sababi ichki iqtisodiy inqiroz va xazinaning bo'shab qolishi ekanini ta'kidlaydi. Demak, u Bennettning qarashini asosiy sababni yuzaki turtki (catalytic event) bilan adashtirish deb baholaydi. B to'g'ri.",
        "strategy_or_hack": "⚡ SAT PAIRED TEXT STRATEGY: 'merely administered the final blow to an empire already hollowed out' iborasi B variantidagi 'mistaking immediate catalytic event for underlying systemic causes' bilan to'liq ma'nodosh.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_16",
        "version": 1,
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Cross-Text Connections",
        "difficulty": "Medium",
        "status": "published",
        "passage": "Text 1\nAdvocates of universal basic income (UBI) argue that unconditional cash transfers empower low-income workers by giving them the financial stability needed to pursue skill education, seek higher-quality employment, and exit exploitative workplace arrangements without fear of immediate destitution.\n\nText 2\nPolicy researcher Gregory Vance warns that unconditional transfer models risk triggering labor force withdrawal in vital low-wage service sectors. Vance points to pilot programs where recipients reduced their formal work hours, suggesting that targeted wage subsidies, such as earned income tax credits tied directly to employment, offer a more economically sustainable antipoverty mechanism.",
        "question": "Both texts address poverty-reduction strategies, but they disagree regarding which of the following?",
        "options": [
            {"key": "A", "text": "Whether low-income households benefit from enhanced financial security"},
            {"key": "B", "text": "Whether unconditional cash transfers exert desirable effects on recipient workforce participation"},
            {"key": "C", "text": "Whether technological automation will displace manufacturing jobs in coming decades"},
            {"key": "D", "text": "Whether governments should completely eliminate progressive income taxation"}
        ],
        "correct": "B",
        "explanation": "Text 1 shartsiz pul o'tkazmalari (UBI) xodimlarga erkinlik beradi va yaxshiroq ish topishga yordam beradi deb ijobiy baholaydi. Text 2 esa bu ishchi kuchi taklifining kamayishiga (ish soatlarini qisqartirishga) olib keladi deb xavotir bildiradi. Demak, ularning asosiy kelishmovchiligi shartsiz to'lovlarning mehnat bozoridagi ishtirokiga (workforce participation) ta'siri ustidadir. B to'g'ri.",
        "strategy_or_hack": "⚡ SAT COMPARISON: Text 1 (UBI fosters career advancement) vs Text 2 (UBI risks labor force withdrawal). Munozara markazi: mehnat ishtiroki.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_17",
        "version": 1,
        "section": "reading",
        "domain": "Craft and Structure",
        "skill": "Cross-Text Connections",
        "difficulty": "Hard",
        "status": "published",
        "passage": "Text 1\nLinguist Noam Chomsky posited that human language acquisition is enabled by an innate 'universal grammar' hardwired into human neural circuitry, arguing that children acquire complex syntactic rules far too rapidly for learning to depend solely on environmental exposure to spoken language.\n\nText 2\nCognitive scientist Michael Tomasello challenges universal grammar, proposing instead a usage-based construction model. Tomasello demonstrates that young children master language through general cognitive mechanisms—such as intention-reading and pattern-finding—gradually abstracting grammatical categories from the rich linguistic input provided by communicative interactions.",
        "question": "Based on the texts, how does Tomasello's model (Text 2) differ fundamentally from Chomsky's hypothesis (Text 1)?",
        "options": [
            {"key": "A", "text": "Tomasello attributes language acquisition to general cognitive pattern recognition rather than domain-specific innate grammar."},
            {"key": "B", "text": "Tomasello denies that young children ever master complex syntactic structures during early childhood development."},
            {"key": "C", "text": "Tomasello argues that speech sounds are processed entirely outside the cerebral cortex."},
            {"key": "D", "text": "Tomasello contends that animal communication systems share the exact same grammatical recursion found in human speech."}
        ],
        "correct": "A",
        "explanation": "Chomsky (Text 1) tug'ma, faqat tilga xos 'universal grammar' (innate neural circuitry) mavjudligini aytadi. Tomasello (Text 2) esa maxsus til moduli o'rniga bolalar umumiy aqliy qobiliyatlar (general cognitive mechanisms: pattern-finding, intention-reading) va atrof-muhit bilan muloqot orqali tilni o'rganishini isbotlaydi. Shuning uchun A varianti ularning tub farqini to'liq ko'rsatadi.",
        "strategy_or_hack": "⚡ SAT CORE CONTRAST: Chomsky (innate domain-specific grammar) vs Tomasello (general pattern-finding cognition from input).",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },

    # ==================== INFORMATION AND IDEAS (16 Questions) ====================
    # --- Central Ideas and Details (6 Questions) ---
    {
        "id": "r_b5_18",
        "version": 1,
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Central Ideas and Details",
        "difficulty": "Easy",
        "status": "published",
        "passage": "Honeybees communicate the precise location of rich nectar sources through an elaborate series of movements known as the 'waggle dance.' Performed on vertical combs inside the hive, the angle of the dance relative to gravity communicates the solar direction of the flower patch, while the duration of the waggle run indicates the distance to the floral food source.",
        "question": "According to the text, which element of the honeybee's waggle dance conveys the distance to a food source?",
        "options": [
            {"key": "A", "text": "The angle of the dance relative to vertical gravity"},
            {"key": "B", "text": "The duration of the waggle run"},
            {"key": "C", "text": "The frequency of wing vibrations during flight"},
            {"key": "D", "text": "The temperature of the honeycomb wax"}
        ],
        "correct": "B",
        "explanation": "Matnning so'nggi qismida aniq ta'kidlangan: 'the duration of the waggle run indicates the distance to the floral food source'. Demak, masofani tebranish yugurishining davomiyligi (duration) bildiradi. A varianti quyoshga nisbatan yo'nalishni ko'rsatadi.",
        "strategy_or_hack": "⚡ SAT DETAIL DIRECT MATCH: 'duration ... indicates the distance'. Matndagi to'g'ridan-to'g'ri dalil bilan solishtiring.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_19",
        "version": 1,
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Central Ideas and Details",
        "difficulty": "Medium",
        "status": "published",
        "passage": "In nineteenth-century Britain, the widespread introduction of gas street lighting fundamentally reshaped urban social geography. Before gas illumination, city streets after dusk were enveloped in darkness, heavily deterring evening commercial activities and social mobility across social classes. By illuminating public avenues, municipal authorities stimulated a thriving nocturnal commercial economy, extending retail shopping hours and fostering new public leisure venues like theaters and late-night restaurants.",
        "question": "Which choice best states the main idea of the text?",
        "options": [
            {"key": "A", "text": "Gas street lighting catalyzed significant economic and social shifts by rendering night-time city spaces safe and commercially active."},
            {"key": "B", "text": "Gas lamps proved far more cost-effective to maintain than earlier oil-burning lamps in British metropolises."},
            {"key": "C", "text": "Nineteenth-century theatrical productions were primarily patronized by municipal gas utility executives."},
            {"key": "D", "text": "The installation of municipal lighting encountered fierce resistance from shopkeepers who opposed evening operations."}
        ],
        "correct": "A",
        "explanation": "Matn gaz yoritgichlari paydo bo'lishi bilan shaharlarda kechki payt xavfsizlik va erkin harakat ta'minlangani, savdo soatlari uzayib, tungi iqtisodiyot va ko'ngilochar maskanlar rivojlangani haqida. A varianti barcha keltirilgan faktlarni o'z ichiga olgan bosh g'oyadir.",
        "strategy_or_hack": "⚡ SAT MAIN IDEA HACK: 1-gapdagi 'fundamentally reshaped urban social geography' va oxirgi gapdagi 'stimulated nocturnal commercial economy' umumlashtirilib A hosil bo'ladi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_20",
        "version": 1,
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Central Ideas and Details",
        "difficulty": "Medium",
        "status": "published",
        "passage": "Unlike typical bird feathers designed for aerodynamic lift and thermal insulation, the specialized wing feathers of barn owls feature serrated comb-like edges and velvety down surfaces. These microstructures break up sound-producing air turbulence into tiny vortices, absorbing high-frequency acoustic vibrations and enabling the owl to achieve virtually silent stealth flight when ambushing small rodents in total darkness.",
        "question": "According to the text, what primary acoustic function do the specialized microstructures of barn owl feathers serve?",
        "options": [
            {"key": "A", "text": "They amplify ultrasonic distress calls emitted by fleeing prey."},
            {"key": "B", "text": "They dissipate air turbulence to suppress audible flight noise."},
            {"key": "C", "text": "They insulate the wing against freezing nighttime temperatures."},
            {"key": "D", "text": "They reflect ambient moonlight to visually confuse ground predators."}
        ],
        "correct": "B",
        "explanation": "Matnda boyqush patlarining tuzilishi havo turbulentligini kichik girdoblarga bo'lib yuborishi, tovush tebranishlarini yutishi va shu orqali parvoz paytida shovqin chiqarmaslikka ('suppress flight noise / virtually silent flight') xizmat qilishi aytilgan. B varianti matnga to'liq mos keladi.",
        "strategy_or_hack": "⚡ SAT PARAPHRASE: 'break up sound-producing turbulence ... achieving silent flight' = 'dissipate air turbulence to suppress audible noise'.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_21",
        "version": 1,
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Central Ideas and Details",
        "difficulty": "Hard",
        "status": "published",
        "passage": "Archaeological excavations at the ancient Indus Valley site of Mohenjo-daro have long puzzled anthropologists due to the conspicuous absence of monumental palaces, royal tombs, or grandiose religious temples typical of contemporaneous Mesopotamian and Egyptian civilizations. Instead, urban planning prioritized sophisticated hydraulic infrastructure, including uniform brick housing, standardized weights, and an elaborate municipal sewage drainage network, suggesting an egalitarian civic governance structure rather than autocratic royal rule.",
        "question": "Which choice best summarizes the central claim of the text?",
        "options": [
            {"key": "A", "text": "The lack of royal monuments and emphasis on advanced civic sanitation suggest Mohenjo-daro operated under a decentralized, egalitarian civic model."},
            {"key": "B", "text": "Mesopotamian conquerors intentionally demolished all royal residences and temples previously built in Mohenjo-daro."},
            {"key": "C", "text": "Indus Valley engineers lacked the stone-cutting tools necessary to construct monumental religious edifices."},
            {"key": "D", "text": "Mohenjo-daro's drainage infrastructure was primarily designed to support massive agricultural irrigation rather than residential hygiene."}
        ],
        "correct": "A",
        "explanation": "Matn Mohenjo-daro shahrida saroylar va dabdabali qabrlarning yo'qligi hamda buning o'rniga barcha aholi uchun standart uylar, suv quvurlari va kanalizatsiya tizimiga ustuvorlik berilgani shahar yakka hokimlik emas, balki teng huquqli (egalitarian civic model) boshqaruvga tayanganini ko'rsatishini ta'kidlaydi. A to'g'ri.",
        "strategy_or_hack": "⚡ SAT CENTRAL CLAIM: 'suggesting an egalitarian civic governance structure rather than autocratic royal rule' matnning xulosa g'oyasidir.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_22",
        "version": 1,
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Central Ideas and Details",
        "difficulty": "Easy",
        "status": "published",
        "passage": "Chlorophyll is the primary pigment responsible for photosynthesis in green plants. Located inside cellular chloroplasts, chlorophyll molecules absorb light energy predominantly in the blue and red regions of the electromagnetic spectrum while reflecting green wavelengths, which gives foliage its characteristic emerald hue.",
        "question": "According to the text, why do green plants appear emerald in color?",
        "options": [
            {"key": "A", "text": "Chloroplasts produce green mineral crystals during nutrient transport."},
            {"key": "B", "text": "Chlorophyll absorbs blue and red wavelengths while reflecting green light."},
            {"key": "C", "text": "Infrared light damages plant cells, causing them to emit green fluorescence."},
            {"key": "D", "text": "Cell walls reflect all wavelengths across the visible spectrum equally."}
        ],
        "correct": "B",
        "explanation": "Matn so'ngida aniq aytilgan: xlorofill ko'k va qizil nurlarni yutadi (absorb), yashil nurni esa qaytaradi (reflecting green wavelengths), shu sababli barglar yashil ko'rinadi. B varianti to'g'ridan-to'g'ri matnga asoslangan.",
        "strategy_or_hack": "⚡ SAT DIRECT FACT CHECK: 'reflecting green wavelengths, which gives foliage its characteristic emerald hue' = B.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_23",
        "version": 1,
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Central Ideas and Details",
        "difficulty": "Hard",
        "status": "published",
        "passage": "While twentieth-century literary historians often portrayed early modern women writers as isolated anomalies who worked in absolute domestic obscurity, recent archival discoveries challenge this narrative. Literary scholar Anita Rao has cataloged hundreds of manuscript poetry circles across seventeenth-century England where noble and gentry women actively circulated, annotated, and critiqued each other's verse, demonstrating that early modern women participated in vibrant, collaborative intellectual networks.",
        "question": "Which choice best describes the relationship between the two sentences in the text?",
        "options": [
            {"key": "A", "text": "The first sentence introduces an established scholarly assumption, and the second sentence presents recent archival evidence that refutes it."},
            {"key": "B", "text": "The first sentence presents an unverified historical rumor, and the second sentence provides documentary proof confirming its authenticity."},
            {"key": "C", "text": "The first sentence details a biographical narrative, and the second sentence explains why the author abandoned poetry altogether."},
            {"key": "D", "text": "The first sentence defines a literary genre, and the second sentence traces its evolution across multiple centuries."}
        ],
        "correct": "A",
        "explanation": "1-gapda avvalgi adabiyotshunoslarning an'anaviy qarashi (ayol yozuvchilar yolg'iz va noma'lum bo'lgan degan faraz) keltiriladi. 2-gapda esa Rao tomonidan topilgan yangi arxiv hujjatlari (qo'lyozma to'garaklari va hamkorlik tarmoqlari) bu qarashni rad etgani bayon qilinadi. A varianti ushbu munosabatni aniq tasvirlaydi.",
        "strategy_or_hack": "⚡ SAT SENTENCE RELATIONSHIP: 'While historians portrayed X ... recent archival discoveries challenge this narrative' = established assumption refuted by new evidence.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },

    # --- Command of Evidence: Textual (5 Questions) ---
    {
        "id": "r_b5_24",
        "version": 1,
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Command of Evidence: Textual",
        "difficulty": "Medium",
        "status": "published",
        "passage": "Evolutionary biologist Dr. Teresa Gomez hypothesized that brightly colored poison dart frogs in the Amazonian rainforest do not synthesize neurotoxins endogenously, but rather sequester their chemical defenses from their dietary intake of specific arthropods. If Gomez's dietary sequestration hypothesis is correct, dart frogs raised in controlled laboratory environments without exposure to their wild diet should exhibit notable physiological differences.",
        "question": "Which finding, if true, would most directly support Gomez's hypothesis?",
        "options": [
            {"key": "A", "text": "Laboratory-reared frogs fed exclusively on non-toxic fruit flies fail to produce defensive skin alkaloids, but rapidly develop toxicity when fed native Amazonian mites."},
            {"key": "B", "text": "Wild dart frogs exhibit identical skin pigmentation regardless of whether they inhabit lowland rainforests or high-altitude cloud forests."},
            {"key": "C", "text": "Tadpoles in both laboratory and wild environments possess trace amounts of neurotoxins prior to metamorphosis."},
            {"key": "D", "text": "Predators that consume lab-reared dart frogs experience severe gastrointestinal distress similar to that caused by wild specimens."}
        ],
        "correct": "A",
        "explanation": "Gomezning gipotezasi: zahar qurbaqaning o'zida emas, uning yeydigan hasharotlaridan to'planadi (dietary sequestration). Agar laboratoriyada oddiy meva pashshasi bilan boqilgan qurbaqalar zahar chiqara olmasa, lekin Amazonka kanalari bilan oziqlanganda darhol zaharga ega bo'lsa, bu zaharning bevosita ozuqadan kelib chiqishini to'g'ridan-to'g'ri isbotlaydi. A varianti gipotezani to'liq qo'llab-quvvatlaydi.",
        "strategy_or_hack": "⚡ SAT EVIDENCE HACK: Gipotezani qo'llash: dietani o'zgartirish natijasida zahar paydo bo'lishi/yo'qolishi A variantida mukammal aks etgan.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_25",
        "version": 1,
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Command of Evidence: Textual",
        "difficulty": "Hard",
        "status": "published",
        "passage": "Psychologist Dr. Warren Chen contends that exposure to natural forest settings enhances executive cognitive attention by allowing the brain's directed attention mechanisms to rest, a process known as Attention Restoration Theory. Conversely, urban environments with flashing advertisements, unpredictable vehicular movement, and auditory clamor constantly demand active, energy-intensive attentional filtering.",
        "question": "Which finding from an experimental trial, if true, would most strongly reinforce Chen's contention?",
        "options": [
            {"key": "A", "text": "Participants who completed a 45-minute stroll through a coniferous arboretum made significantly fewer errors on a subsequent standardized proofreading task than participants who walked through a busy commercial downtown."},
            {"key": "B", "text": "Participants listening to recorded city noise in a dark room scored identically on memory recall tests to those listening to classical orchestral music."},
            {"key": "C", "text": "Individuals who frequently commute via underground subways report higher baseline satisfaction with their physical fitness than those who walk to work."},
            {"key": "D", "text": "Participants displayed heightened galvanic skin conductance while viewing digital photographs of pristine mountain landscapes."}
        ],
        "correct": "A",
        "explanation": "Chenning nazariyasi: tabiatda yurish diqqatni tiklaydi (restores directed attention), shahardagi shovqin esa charchatadi. Agar o'rmonda 45 daqiqa sayr qilganlar gavjum shaharda yurganlarga qaraganda xatolarni sezilarli darajada kam qilsa (diqqat talab qiluvchi vazifada), bu tabiatning diqqatni tiklashini eksperimental tasdiqlaydi. A varianti to'g'ri.",
        "strategy_or_hack": "⚡ SAT EVIDENCE TO SUPPORT: Nazariyada aytilgan ta'sir (tabiat = yaxshi diqqat; shahar = toliqish) bevosita A variantidagi natijada o'lchangan.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_26",
        "version": 1,
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Command of Evidence: Textual",
        "difficulty": "Medium",
        "status": "published",
        "passage": "Agricultural scientists developing drought-resistant crop strains evaluate the stomatal conductance of mutated pearl millet varieties. Stomata are microscopic pores on leaf surfaces that regulate gas exchange; closing stomata conserves moisture during arid spells but simultaneously restricts the intake of atmospheric carbon dioxide necessary for photosynthetic biomass accumulation.",
        "question": "Which finding, if true, would pose the most substantial challenge to the scientists' goal of utilizing stomatal closure mutations to maintain crop yields during prolonged droughts?",
        "options": [
            {"key": "A", "text": "Millet varieties engineered for permanent stomatal constriction during droughts exhibited profound reductions in grain yield due to severe carbon starvation."},
            {"key": "B", "text": "Pearl millet roots grown in sandy soils reached depths exceeding three meters to access deep groundwater tables."},
            {"key": "C", "text": "Stomatal density on upper leaf surfaces was found to be slightly higher than that on lower leaf surfaces."},
            {"key": "D", "text": "Wild pearl millet plants native to sub-Saharan Africa showed heightened resistance to invasive fungal blight."}
        ],
        "correct": "A",
        "explanation": "Olimlarning maqsadi: qurg'oqchilikda hosildorlikni saqlab qolish. Biroq stomatalarni yopish karbonat angidrid kirishini to'xtatadi. Agar o'simlik qurg'oqchilikda stomatalarini yopib, karbonat angidrid yetishmovchiligi (carbon starvation) sababli don hosili keskin tushib ketsa, bu olimlarning hosilni saqlash maqsadiga eng katta to'siq (substantial challenge) bo'ladi. A to'g'ri.",
        "strategy_or_hack": "⚡ SAT WEAKEN/CHALLENGE EVIDENCE: Maqsad: hosildorlikni saqlash. Salbiy oqibat: karbonat yetishmasligi hosilni barbod qildi (A).",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_27",
        "version": 1,
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Command of Evidence: Textual",
        "difficulty": "Hard",
        "status": "published",
        "passage": "In 1912, Alfred Wegener proposed the continental drift hypothesis, pointing to the jigsaw fit of Atlantic coastlines and matching fossil distributions across disparate continents. However, contemporary geophysicists rejected Wegener's model because he failed to identify a plausible physical mechanism capable of propelling massive granitic continental blocks across the dense basaltic oceanic crust.",
        "question": "Which subsequent scientific discovery provided the decisive physical evidence that validated Wegener's previously rejected hypothesis?",
        "options": [
            {"key": "A", "text": "The discovery of symmetrical paleomagnetic alternating stripes across mid-ocean ridges, proving seafloor spreading driven by mantle convection"},
            {"key": "B", "text": "The discovery of identical coal swamp plant fossils located in high-altitude Himalayan mountain valleys"},
            {"key": "C", "text": "The observation that lunar gravitational tidal pull causes minute measurable bulges in continental crust"},
            {"key": "D", "text": "The measurement of ambient ocean temperatures showing deep-sea water remains colder than surface water"}
        ],
        "correct": "A",
        "explanation": "Vegenerning gipotezasi qit'alarni qaysi mexanizm harakatga keltirishini tushuntira olmagani uchun rad etilgan edi. 1960-yillarda okean o'rtasidagi tizmalarda paleomagnit qatlamlar va mantiya konveksiyasi orqali okean tubining kengayishi (seafloor spreading) kashf etilishi ushbu harakatlantiruvchi mexanizmni isbotlab berdi. Shuning uchun A to'g'ri.",
        "strategy_or_hack": "⚡ SAT HISTORICAL EVIDENCE: 'failed to identify physical mechanism' muammosini 'seafloor spreading driven by mantle convection' kashfiyoti to'liq yechdi.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_28",
        "version": 1,
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Command of Evidence: Textual",
        "difficulty": "Medium",
        "status": "published",
        "passage": "Linguists studying endangered indigenous languages have observed that languages with small speaker populations frequently demonstrate far greater morphological complexity—such as intricate verb conjugation systems with dozens of affixes—than globally spoken languages like English or Mandarin, which favor streamlined, analytical word orders.",
        "question": "Which of the following examples best illustrates the phenomenon described in the text?",
        "options": [
            {"key": "A", "text": "Inuit-Yupik languages, spoken by isolated Arctic communities, utilize polysynthetic verbs where a single word incorporates the subject, object, and temporal nuances of an entire sentence."},
            {"key": "B", "text": "Mandarin Chinese employs lexical tones to distinguish word meanings among syllables with identical phonetic spellings."},
            {"key": "C", "text": "Spanish and Portuguese share over 85% of their core lexical vocabulary due to common descent from Vulgar Latin."},
            {"key": "D", "text": "English expanded its lexicon during the Renaissance by borrowing thousands of scientific roots from Classical Greek and Latin."}
        ],
        "correct": "A",
        "explanation": "Matnda aytilgan hodisa: kam sonli so'zlashuvchiga ega tillarda nihoyatda murakkab morfologiya (ko'plab affikslar, bitta fe'lga butun gap ma'nosini joylash) bo'ladi. A variantidagi Inuit-Yupik tillari (polysynthetic verbs where a single word incorporates subject, object, etc.) aynan shu xususiyatni mukammal ko'rsatadi.",
        "strategy_or_hack": "⚡ SAT EXEMPLIFICATION: 'intricate verb systems with dozens of affixes' misoli A variantidagi 'polysynthetic verbs' bilan 100% mos.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },

    # --- Inferences (5 Questions) ---
    {
        "id": "r_b5_29",
        "version": 1,
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Inferences",
        "difficulty": "Medium",
        "status": "published",
        "passage": "In many bird species, singing requires substantial metabolic energy and exposes the vocalizer to opportunistic aerial predators. Consequently, biologists deduce that producing elaborate, high-volume mating songs operates as an honest signal of individual biological fitness: only males with abundant nutritional reserves and superior physiological vigor can afford to _______.",
        "question": "Which choice most logically completes the text?",
        "options": [
            {"key": "A", "text": "sustain prolonged vocal displays while coping with the associated predation risks"},
            {"key": "B", "text": "abandon breeding territories entirely to forage in distant predator-free habitats"},
            {"key": "C", "text": "mimic the vocal calls of rival predatory species to deter competitors"},
            {"key": "D", "text": "suppress their metabolic energy consumption during the spring mating season"}
        ],
        "correct": "A",
        "explanation": "Matn boshida qushlarning sayrashi katta energiya talab qilishi va yirtqichlar xavfini oshirishi aytiladi. Shuning uchun murakkab va baland qo'shiq aytish qushning sog'lom va kuchli ekanini bildiradi ('honest signal of fitness'). Demak, faqat kuchi va resursi ko'p bo'lgan qushlargina bu xavf va energiya sarfiga bardosh bera oladi ('sustain prolonged vocal displays while coping with risks'). A to'g'ri.",
        "strategy_or_hack": "⚡ SAT LOGICAL COMPLETION: 'honest signal of fitness: only males with abundant reserves can afford to [do the costly behavior]' -> A.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_30",
        "version": 1,
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Inferences",
        "difficulty": "Hard",
        "status": "published",
        "passage": "Under standard atmospheric conditions, water freezes at 0 degrees Celsius. However, when microscopic droplets of ultra-pure water devoid of mineral particulates or dust motes are suspended in clean air, the lack of foreign nucleation surfaces prevents ice crystal formation. Experiments demonstrate that such supercooled liquid water droplets can persist in liquid state down to nearly -40 degrees Celsius, suggesting that the freezing of water at 0 degrees Celsius in everyday natural environments is _______.",
        "question": "Which choice most logically completes the text?",
        "options": [
            {"key": "A", "text": "dependent upon the presence of microscopic particulate impurities that serve as ice nucleation sites"},
            {"key": "B", "text": "an erroneous scientific observation that modern high-precision laboratory thermometers have disproven"},
            {"key": "C", "text": "prevented by the continuous evaporation of surface molecules into surrounding ambient vapor"},
            {"key": "D", "text": "incompatible with the thermodynamic laws that govern atmospheric cloud condensation"}
        ],
        "correct": "A",
        "explanation": "Matnda chang va zarrachalardan xoli toza suv -40 darajagacha muzlamasdan suyuq qolishi ko'rsatilgan, chunki muz kristali hosil bo'lishi uchun yadro (nucleation surface) kerak. Bundan xulosa kelib chiqadiki, oddiy tabiatda suvning 0 darajada muzlashi unda muzlash yadrosi bo'lib xizmat qiluvchi mikroskopik zarrachalar va kirlarning (particulate impurities) mavjudligiga bog'liq. A to'g'ri.",
        "strategy_or_hack": "⚡ SAT LOGICAL INFERENCE: 'lack of foreign nucleation surfaces prevents ice' -> 'freezing at 0 C requires foreign particulate impurities'.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_31",
        "version": 1,
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Inferences",
        "difficulty": "Medium",
        "status": "published",
        "passage": "Economists studying retail pricing algorithms note that automated dynamic pricing tools adjust hotel room rates in real time based on incoming browser cookies, current inventory, and concurrent demand. When a major concert is announced in an urban center, automated software instantaneously multiplies room rates, demonstrating that algorithmic pricing _______.",
        "question": "Which choice most logically completes the text?",
        "options": [
            {"key": "A", "text": "responds rapidly to sudden localized shifts in consumer demand without requiring human intervention"},
            {"key": "B", "text": "consistently reduces average profit margins for hospitality establishments during major events"},
            {"key": "C", "text": "relies on quarterly retrospective financial audits to calculate future baseline costs"},
            {"key": "D", "text": "guarantees that budget-conscious travelers always secure the lowest possible accommodations"}
        ],
        "correct": "A",
        "explanation": "Matnda konsert e'lon qilinishi bilan algoritm inson aralashuvisiz bir lahzada narxlarni oshirishi aytilgan. Bu algoritmik narxlashning talab o'zgarishlariga inson aralashuvisiz bir zumda tezkor javob berishini ('responds rapidly to shifts in demand without requiring human intervention') ko'rsatadi. A to'g'ri.",
        "strategy_or_hack": "⚡ SAT INFERENCE: 'instantaneously multiplies room rates upon concert announcement' -> 'responds rapidly to sudden shifts without human intervention'.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_32",
        "version": 1,
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Inferences",
        "difficulty": "Hard",
        "status": "published",
        "passage": "In mammalian brain physiology, the blood-brain barrier comprises tightly packed endothelial cells that restrict circulating pathogens and polar molecules from entering neural tissue. While this protective envelope shields the central nervous system from systemic infections, it simultaneously presents a formidable therapeutic obstacle: pharmacological developers find that over 98% of small-molecule neurotherapeutic drugs administered intravenously are _______.",
        "question": "Which choice most logically completes the text?",
        "options": [
            {"key": "A", "text": "unable to cross the protective endothelial barrier in concentrations sufficient to achieve clinical efficacy"},
            {"key": "B", "text": "rapidly metabolized into highly toxic compounds before reaching peripheral bloodstream vessels"},
            {"key": "C", "text": "capable of dissolving the endothelial cell lining and inducing acute cerebral hemorrhage"},
            {"key": "D", "text": "instantly recognized by red blood cells as essential nutrients for cellular respiration"}
        ],
        "correct": "A",
        "explanation": "Matnda gematoensefalik to'siq (blood-brain barrier) miyani infeksiyalardan himoya qilishi bilan birga, tibbiyot uchun to'siq ekani ta'kidlanadi. Sababi to'siq molekulalarni miyaga o'tkazmaydi. Demak, 98% dan ortiq dori vositalari bu to'siqdan klinik ta'sir ko'rsatadigan konsentratsiyada o'ta olmaydi ('unable to cross the barrier in sufficient concentrations'). A to'g'ri.",
        "strategy_or_hack": "⚡ SAT LOGICAL COMPLETION: 'formidable therapeutic obstacle' + 'restricts polar molecules' -> dori miyaga o'ta olmaydi (A).",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    },
    {
        "id": "r_b5_33",
        "version": 1,
        "section": "reading",
        "domain": "Information and Ideas",
        "skill": "Inferences",
        "difficulty": "Easy",
        "status": "published",
        "passage": "Paleontologists analyzing fossilized tooth enamel from Cretaceous theropod dinosaurs discovered that seasonal oxygen isotope ratios varied predictably between rainy and dry periods. Because oxygen isotope signatures in tooth enamel directly reflect the isotopic composition of ingested drinking water, the researchers inferred that _______.",
        "question": "Which choice most logically completes the text?",
        "options": [
            {"key": "A", "text": "the local precipitation and surface water sources experienced consistent cyclical seasonal fluctuations"},
            {"key": "B", "text": "theropod dinosaurs only ingested water during periods of total solar eclipse"},
            {"key": "C", "text": "prehistoric carnivores drank exclusively from subterranean geysers unaffected by weather"},
            {"key": "D", "text": "tooth enamel was completely permeable to mineral replacement after fossilization"}
        ],
        "correct": "A",
        "explanation": "Tishdagi izotoplar ichilgan suvdan o'tadi va ular yomg'irli hamda quruq mavsumlarda o'zgaradi. Demak, o'sha davrdagi mahalliy yog'ingarchilik va yer usti suv manbalari davriy mavsumiy tebranishlarga ega bo'lgan ('experienced consistent cyclical seasonal fluctuations'). A to'g'ri.",
        "strategy_or_hack": "⚡ SAT INFERENCE: Izotoplar ichimlik suvidan olinadi + fasllar bo'yicha farq qiladi -> iqlim va suv manbalari mavsumiy o'zgargan.",
        "author": "EduTest Pro Expert Team",
        "license": "Proprietary Original"
    }
]
