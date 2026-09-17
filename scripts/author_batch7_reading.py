"""
EduTest Pro - Batch 7 Reading Authoring and Verification Suite
Generates 50 authentic Digital SAT Reading questions across official domains:
- Craft and Structure (25 questions: Words in Context, Text Structure & Purpose, Cross-Text Connections)
- Information and Ideas (25 questions: Central Ideas & Details, Command of Evidence, Inferences)
"""

import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from services.question_validator import validate_question

READING_RAW = [
    # --- WORDS IN CONTEXT (10 questions) ---
    {
        "id": "r_b6_01",
        "domain": "Craft and Structure - Words in Context",
        "skill": "Words in Context",
        "difficulty": "Easy",
        "passage": "Although the archival documents were fragile and severely degraded by humidity, the conservator handled each manuscript with exceptional care, taking pains not to compromise the ______ integrity of the centuries-old parchment.",
        "question": "Which choice completes the text with the most logical and precise word or phrase?",
        "options": [
            {"key": "A", "text": "physical"},
            {"key": "B", "text": "theoretical"},
            {"key": "C", "text": "financial"},
            {"key": "D", "text": "artificial"}
        ],
        "correct": "A",
        "explanation": "The text discusses fragile manuscripts degraded by humidity that need to be preserved without damaging the parchment itself. 'Physical' correctly describes the material condition and structure of the parchment.",
        "strategy_or_hack": "Kontekst kaliti: 'fragile', 'degraded by humidity', 'parchment' (moddiy ashyo). Faqat 'physical' mos keladi."
    },
    {
        "id": "r_b6_02",
        "domain": "Craft and Structure - Words in Context",
        "skill": "Words in Context",
        "difficulty": "Medium",
        "passage": "During the late nineteenth century, public health officials encountered widespread resistance when attempting to mandate municipal water chlorination. Far from being embraced as a life-saving innovation, the chemical treatment was initially regarded with deep ______ by citizens who suspected hidden corporate motives.",
        "question": "Which choice completes the text with the most logical and precise word or phrase?",
        "options": [
            {"key": "A", "text": "enthusiasm"},
            {"key": "B", "text": "skepticism"},
            {"key": "C", "text": "reverence"},
            {"key": "D", "text": "indifference"}
        ],
        "correct": "B",
        "explanation": "'Far from being embraced' and 'suspected hidden corporate motives' signal strong distrust and doubt. 'Skepticism' precisely matches this attitude of doubt and suspicion.",
        "strategy_or_hack": "Ziddiyat kaliti: 'Far from being embraced' + 'suspected hidden motives' => shubha va ishonchsizlik (skepticism)."
    },
    {
        "id": "r_b6_03",
        "domain": "Craft and Structure - Words in Context",
        "skill": "Words in Context",
        "difficulty": "Hard",
        "passage": "Contemporary cognitive scientists often criticize early computational models of human memory for being overly rigid; human recollection, modern studies suggest, is not an exact retrieval of static files but rather an inherently ______ process that reconstructs past events anew with each remembering.",
        "question": "Which choice completes the text with the most logical and precise word or phrase?",
        "options": [
            {"key": "A", "text": "static"},
            {"key": "B", "text": "malleable"},
            {"key": "C", "text": "infallible"},
            {"key": "D", "text": "monolithic"}
        ],
        "correct": "B",
        "explanation": "The contrast set up by 'not an exact retrieval of static files but rather...' requires a word opposite to rigid and static. 'Malleable' (easily influenced, adaptable, flexible) accurately characterizes a process that reconstructs events anew each time.",
        "strategy_or_hack": "Qarama-qarshilik: 'rigid/static' ga zid so'z kerak. 'Malleable' (o'zgaruvchan, egiluvchan) to'liq mos keladi."
    },
    {
        "id": "r_b6_04",
        "domain": "Craft and Structure - Words in Context",
        "skill": "Words in Context",
        "difficulty": "Medium",
        "passage": "To verify the authenticity of the Renaissance painting, the museum curator sought to ______ the findings of the pigment analysis with independent historical provenance records.",
        "question": "Which choice completes the text with the most logical and precise word or phrase?",
        "options": [
            {"key": "A", "text": "corroborate"},
            {"key": "B", "text": "contradict"},
            {"key": "C", "text": "obscure"},
            {"key": "D", "text": "fabricate"}
        ],
        "correct": "A",
        "explanation": "To verify authenticity, a researcher wants independent evidence to confirm and support the initial scientific findings. 'Corroborate' means to confirm or give support to a statement or finding.",
        "strategy_or_hack": "'Verify authenticity' uchun dalillarni bir-biri bilan tasdiqlash (corroborate) talab etiladi."
    },
    {
        "id": "r_b6_05",
        "domain": "Craft and Structure - Words in Context",
        "skill": "Words in Context",
        "difficulty": "Hard",
        "passage": "Despite his reputation for writing dense and convoluted philosophical treatises, Professor Alvarez was remarkably ______ in his public lectures, distilling intricate metaphysical doctrines into clear, accessible prose.",
        "question": "Which choice completes the text with the most logical and precise word or phrase?",
        "options": [
            {"key": "A", "text": "abstruse"},
            {"key": "B", "text": "lucid"},
            {"key": "C", "text": "redundant"},
            {"key": "D", "text": "pedantic"}
        ],
        "correct": "B",
        "explanation": "'Despite his reputation for dense and convoluted... distilling intricate doctrines into clear, accessible prose' indicates that in public lectures he was exceptionally clear and easy to understand. 'Lucid' means expressed clearly; easy to understand.",
        "strategy_or_hack": "Ziddiyat: 'dense and convoluted' ga qarama-qarshi so'z 'clear, accessible' => 'lucid' (ravshan, tushunarli)."
    },
    {
        "id": "r_b6_06",
        "domain": "Craft and Structure - Words in Context",
        "skill": "Words in Context",
        "difficulty": "Easy",
        "passage": "The engineer noted that the bridge’s steel suspension cables had begun to ______ under the relentless coastal winds and salty marine air, exhibiting significant rust and structural weakness.",
        "question": "Which choice completes the text with the most logical and precise word or phrase?",
        "options": [
            {"key": "A", "text": "deteriorate"},
            {"key": "B", "text": "proliferate"},
            {"key": "C", "text": "strengthen"},
            {"key": "D", "text": "crystallize"}
        ],
        "correct": "A",
        "explanation": "Contextual clues 'exhibiting significant rust and structural weakness' directly point to physical degradation and worsening condition. 'Deteriorate' means to become progressively worse.",
        "strategy_or_hack": "Kalit so'zlar: 'rust', 'structural weakness' => yemirilish, yomonlashish (deteriorate)."
    },
    {
        "id": "r_b6_07",
        "domain": "Craft and Structure - Words in Context",
        "skill": "Words in Context",
        "difficulty": "Medium",
        "passage": "Because the urban planning committee was composed of representatives with conflicting political agendas, reaching a consensus on the new zoning laws proved to be an exceptionally ______ endeavor.",
        "question": "Which choice completes the text with the most logical and precise word or phrase?",
        "options": [
            {"key": "A", "text": "contentious"},
            {"key": "B", "text": "harmonious"},
            {"key": "C", "text": "spontaneous"},
            {"key": "D", "text": "lucrative"}
        ],
        "correct": "A",
        "explanation": "The presence of 'conflicting political agendas' making agreement difficult indicates an endeavor marked by dispute and argument. 'Contentious' means causing or likely to cause an argument; controversial.",
        "strategy_or_hack": "'Conflicting agendas' sababli jarayon munozarali va nizoli (contentious) bo'ladi."
    },
    {
        "id": "r_b6_08",
        "domain": "Craft and Structure - Words in Context",
        "skill": "Words in Context",
        "difficulty": "Hard",
        "passage": "Rather than attempting to eliminate all ambient noise in recording studios, acoustic engineers often deploy low-level white noise to ______ minor acoustical imperfections, rendering sudden extraneous sounds imperceptible to listeners.",
        "question": "Which choice completes the text with the most logical and precise word or phrase?",
        "options": [
            {"key": "A", "text": "mask"},
            {"key": "B", "text": "amplify"},
            {"key": "C", "text": "exacerbate"},
            {"key": "D", "text": "catalog"}
        ],
        "correct": "A",
        "explanation": "The text explains that white noise makes minor imperfections and sudden sounds 'imperceptible' (unable to be noticed). 'Mask' means to conceal, disguise, or cover up auditory stimuli.",
        "strategy_or_hack": "Natija: 'imperceptible' qilish uchun shovqinni 'mask' qilish (yopish, bildirmaslik) kerak."
    },
    {
        "id": "r_b6_09",
        "domain": "Craft and Structure - Words in Context",
        "skill": "Words in Context",
        "difficulty": "Medium",
        "passage": "In her comprehensive biography of Ada Lovelace, historian Miranda Chen cautions against the temptation to ______ Lovelace’s mathematical accomplishments, arguing that exaggeration diminishes the genuine significance of her pioneering insights into mechanical computing.",
        "question": "Which choice completes the text with the most logical and precise word or phrase?",
        "options": [
            {"key": "A", "text": "hyperbolize"},
            {"key": "B", "text": "scrutinize"},
            {"key": "C", "text": "discredit"},
            {"key": "D", "text": "document"}
        ],
        "correct": "A",
        "explanation": "The following clause clarifies: 'arguing that exaggeration diminishes the genuine significance...'. 'Hyperbolize' means to exaggerate, directly mirroring the context.",
        "strategy_or_hack": "To'g'ridan-to'g'ri sinonim kalit: 'exaggeration' => 'hyperbolize' (bo'rttirib yubormoq)."
    },
    {
        "id": "r_b6_10",
        "domain": "Craft and Structure - Words in Context",
        "skill": "Words in Context",
        "difficulty": "Hard",
        "passage": "While some critics dismissed the avant-garde novelist's fragmented chronology as mere stylistic posturing, more perceptive literary scholars recognized that the disjointed timeline was ______ to the protagonist's fractured psychological state.",
        "question": "Which choice completes the text with the most logical and precise word or phrase?",
        "options": [
            {"key": "A", "text": "integral"},
            {"key": "B", "text": "peripheral"},
            {"key": "C", "text": "detrimental"},
            {"key": "D", "text": "irrelevant"}
        ],
        "correct": "A",
        "explanation": "The sentence contrasts superficial critics with perceptive scholars who see that the technique is fundamentally tied and essential to portraying the protagonist's psychology. 'Integral' means necessary to make a whole complete; essential.",
        "strategy_or_hack": "Qarama-qarshilik: 'mere posturing' ga qarshi o'laroq, bu uslub qahramon ruhiyatiga uzviy bog'liq ('integral')."
    },

    # --- TEXT STRUCTURE AND PURPOSE (8 questions) ---
    {
        "id": "r_b6_11",
        "domain": "Craft and Structure - Text Structure and Purpose",
        "skill": "Text Structure and Purpose",
        "difficulty": "Medium",
        "passage": "For decades, evolutionary biologists assumed that bioluminescence in marine organisms evolved primarily for predatory lure or mate recognition. However, recent deep-sea submersibles equipped with hypersensitive photometers revealed that over seventy percent of abyssal bioluminescent flashes occur in response to mechanical touch. This empirical discovery suggests that illumination primarily serves as a startle mechanism against approaching grazers rather than as an offensive weapon.",
        "question": "Which choice best describes the overall structure of the text?",
        "options": [
            {"key": "A", "text": "It outlines a longstanding scientific assumption, presents new empirical observations, and proposes a revised explanation."},
            {"key": "B", "text": "It summarizes an ongoing debate among biologists, introduces experimental data supporting both sides, and calls for further research."},
            {"key": "C", "text": "It describes an experimental apparatus, details its operational limitations, and suggests alternative technological solutions."},
            {"key": "D", "text": "It defines a biological phenomenon, identifies its cellular mechanisms, and evaluates its ecological disadvantages."}
        ],
        "correct": "A",
        "explanation": "Sentence 1 introduces the longstanding assumption. Sentence 2 introduces recent empirical findings ('However, recent deep-sea...'). Sentence 3 synthesizes these findings to propose a revised functional explanation. Choice A accurately captures this three-part structural progression.",
        "strategy_or_hack": "Tuzilish qolipi: 1) Eski qarash ('For decades assumed') -> 2) Yangi kashfiyot ('However, recent discovery') -> 3) Yangilangan xulosa ('This suggests')."
    },
    {
        "id": "r_b6_12",
        "domain": "Craft and Structure - Text Structure and Purpose",
        "skill": "Text Structure and Purpose",
        "difficulty": "Hard",
        "passage": "In his 1928 critique of modernist architecture, Lewis Mumford observed that glass and steel skyscrapers, while celebrating industrial triumphs, severed city dwellers from natural diurnal rhythms. By replacing masonry with curtain walls, architects intended to flood interiors with sunlight; in practice, excessive glare necessitated heavy blinds, paradoxically encasing workers in artificial illumination. For Mumford, the tower was less a beacon of liberation than a monument to technical overconfidence.",
        "question": "Which choice best states the main purpose of the text?",
        "options": [
            {"key": "A", "text": "To celebrate the engineering innovations that enabled skyscraper construction in early twentieth-century cities."},
            {"key": "B", "text": "To highlight an architectural critic’s analysis of how an intended design benefit produced an unexpected drawback."},
            {"key": "C", "text": "To contrast the aesthetic philosophies of Lewis Mumford with those of contemporary industrial architects."},
            {"key": "D", "text": "To argue that modern building codes should mandate the use of traditional masonry materials."}
        ],
        "correct": "B",
        "explanation": "The text focuses on Mumford's critique: architects intended to bring sunlight inside (intended benefit), but glare forced the use of blinds and artificial lights (unexpected drawback). Choice B directly summarizes this purpose.",
        "strategy_or_hack": "Matnning asosiy maqsadi: Mumfordning kutilgan maqsad (quyosh nuri) va kutilmagan salbiy natija (sun'iy yorug'lik) haqidagi tahlilini yoritish."
    },
    {
        "id": "r_b6_13",
        "domain": "Craft and Structure - Text Structure and Purpose",
        "skill": "Text Structure and Purpose",
        "difficulty": "Easy",
        "passage": "Photosynthesis is often summarized simply as the conversion of carbon dioxide and water into glucose and oxygen. Yet this overarching equation conceals a complex sequence of sub-reactions divided into two interdependent phases: the light-dependent reactions that harvest solar photon energy, and the Calvin cycle, which fixes gaseous carbon into organic molecules.",
        "question": "Which choice best describes the function of the underlined sentence in the overall text?",
        "options": [
            {"key": "A", "text": "It provides a simplified baseline description of a process before revealing its underlying intricacy."},
            {"key": "B", "text": "It refutes an obsolete historical theory regarding the role of oxygen in plant physiology."},
            {"key": "C", "text": "It illustrates a common experimental mistake made by introductory biology students."},
            {"key": "D", "text": "It introduces a controversial scientific hypothesis that lacks empirical confirmation."}
        ],
        "correct": "A",
        "explanation": "The first sentence presents the basic, simplified overview ('is often summarized simply as...'), allowing the second sentence to contrast it with the true two-stage intricacy. Thus, it establishes a simplified baseline.",
        "strategy_or_hack": "Funktsiya: Sodda umumiy formulani berish, so'ngra jarayonning asl murakkabligini ochib berish."
    },
    {
        "id": "r_b6_14",
        "domain": "Craft and Structure - Text Structure and Purpose",
        "skill": "Text Structure and Purpose",
        "difficulty": "Medium",
        "passage": "Standard economic models frequently operate under the assumption of 'rational actors' who dispassionately maximize personal utility. Behavioral economists, however, have documented consistent cognitive anomalies, such as loss aversion—the psychological tendency to experience the pain of losing $100 far more acutely than the joy of gaining $100. By integrating psychological realism into economic equations, researchers have developed predictive models that far better mirror actual market behavior.",
        "question": "Which choice best describes the primary purpose of the text?",
        "options": [
            {"key": "A", "text": "To demonstrate how empirical psychological insights have refined traditional economic assumptions."},
            {"key": "B", "text": "To condemn the mathematical methods used by twentieth-century economic theorists."},
            {"key": "C", "text": "To prove that financial markets are entirely chaotic and cannot be reliably modeled."},
            {"key": "D", "text": "To compare the personal monetary decisions of behavioral economists with ordinary consumers."}
        ],
        "correct": "A",
        "explanation": "The text explains how behavioral economics incorporated psychological realism (like loss aversion) to improve the unrealistic 'rational actor' assumption and create models that better mirror real behavior.",
        "strategy_or_hack": "Asosiy g'oya: Psixologik tushunchalar an'anaviy iqtisodiy modellarni qanday takomillashtirgani."
    },
    {
        "id": "r_b6_15",
        "domain": "Craft and Structure - Text Structure and Purpose",
        "skill": "Text Structure and Purpose",
        "difficulty": "Hard",
        "passage": "In literary criticism, the concept of the 'unreliable narrator' is often treated as a modern narrative invention popularized by early twentieth-century psychological novels. However, Geoffrey Chaucer’s fourteenth-century *Canterbury Tales* features speakers whose self-aggrandizing exaggerations and moral contradictions explicitly invite reader skepticism. Acknowledging these pre-modern antecedents challenges the teleological narrative that narrative complexity arose solely with literary modernism.",
        "question": "Which choice best states the primary claim of the author?",
        "options": [
            {"key": "A", "text": "Modern psychological novels lack the genuine narrative sophistication found in Chaucer’s poetry."},
            {"key": "B", "text": "Narrative unreliability existed well before modernism, demonstrating that narrative complexity has a deeper historical lineage."},
            {"key": "C", "text": "Chaucer was the first European author to intentionally deceive his readers through first-person narration."},
            {"key": "D", "text": "Literary modernism should be defined primarily by its rejection of medieval storytelling devices."}
        ],
        "correct": "B",
        "explanation": "The author points out that Chaucer used unreliable narrators in the 14th century, which challenges the idea that complexity is strictly a modern invention, thereby establishing that it has a deeper history.",
        "strategy_or_hack": "Xulosa kaliti: 'challenges the teleological narrative that narrative complexity arose solely with modernism' => Ishonchsiz roviy modernizmdan ancha oldin mavjud bo'lgan."
    },
    {
        "id": "r_b6_16",
        "domain": "Craft and Structure - Text Structure and Purpose",
        "skill": "Text Structure and Purpose",
        "difficulty": "Medium",
        "passage": "Paleontologists studying fossilized avian trackways face an intrinsic interpretive dilemma. Unlike skeletal remains, which reveal precise skeletal morphology and bone dimensions, trackways preserve dynamic behavioral interactions with substrate surfaces. However, varying sediment moisture can drastically alter the apparent morphology of identical footfalls made by the same animal, complicating taxonomic classification.",
        "question": "Which choice best describes the relationship between the two halves of the passage?",
        "options": [
            {"key": "A", "text": "The first half emphasizes an advantage of trackways over bones, while the second half identifies an environmental factor that complicates their interpretation."},
            {"key": "B", "text": "The first half proposes a new method of excavation, while the second half dismisses that method as impractical."},
            {"key": "C", "text": "The first half lists various avian species, while the second half describes their migration patterns across coastal substrates."},
            {"key": "D", "text": "The first half explains skeletal fossilization, while the second half proves that trackways cannot be preserved in sediment."}
        ],
        "correct": "A",
        "explanation": "First half: trackways preserve dynamic behavior (advantage over bones). Second half ('However...'): sediment moisture changes how tracks look, making classification difficult (environmental complication). Choice A matches perfectly.",
        "strategy_or_hack": "Birinchi qism: izlarning ustunligi (behavioral interactions); Ikkinchi qism: namlik tufayli yuzaga keladigan qiyinchilik (complication)."
    },
    {
        "id": "r_b6_17",
        "domain": "Craft and Structure - Text Structure and Purpose",
        "skill": "Text Structure and Purpose",
        "difficulty": "Easy",
        "passage": "Urban rooftop gardens have garnered praise for mitigating the urban heat island effect by absorbing solar radiation and releasing moisture through evapotranspiration. Furthermore, these green roofs provide crucial resting habitats for migrating pollinator species traversing fragmented cityscapes.",
        "question": "Which choice best describes the function of the second sentence?",
        "options": [
            {"key": "A", "text": "It introduces an additional ecological benefit provided by urban rooftop gardens."},
            {"key": "B", "text": "It refutes the claim that rooftop gardens lower ambient city temperatures."},
            {"key": "C", "text": "It details the financial expenditures required to maintain urban green roofs."},
            {"key": "D", "text": "It questions the long-term survival rates of pollinator populations in urban areas."}
        ],
        "correct": "A",
        "explanation": "The first sentence explains temperature reduction (benefit 1). The second sentence starts with 'Furthermore' and introduces habitat for pollinators (benefit 2). Thus, it introduces an additional ecological benefit.",
        "strategy_or_hack": "'Furthermore' ulovchisi yangi qo'shimcha ijobiy jihat (additional benefit) qo'shilishini bildiradi."
    },
    {
        "id": "r_b6_18",
        "domain": "Craft and Structure - Text Structure and Purpose",
        "skill": "Text Structure and Purpose",
        "difficulty": "Hard",
        "passage": "Advocates of strict textualism in constitutional law maintain that legal provisions must be interpreted exclusively according to the original public meaning of their text at the time of enactment. Critics, however, contend that this doctrine rests on an untenable premise: that eighteenth-century framing conventions embodied a singular, uncontested consensus rather than a cacophony of competing compromises.",
        "question": "Which choice best summarizes the critics' argument as presented in the text?",
        "options": [
            {"key": "A", "text": "Original public meaning is flawed because the historical authors themselves did not share a single unified understanding of the text."},
            {"key": "B", "text": "Constitutional provisions are inherently ambiguous and should therefore be rewritten by modern legislatures."},
            {"key": "C", "text": "Textualist judges intentionally misrepresent historical documents to advance partisan political goals."},
            {"key": "D", "text": "Eighteenth-century framing debates were irrelevant to the eventual ratification of constitutional amendments."}
        ],
        "correct": "A",
        "explanation": "The critics argue that the premise of a 'singular, uncontested consensus' is untenable because historical debates actually involved 'a cacophony of competing compromises'. Hence, there was no single unified meaning.",
        "strategy_or_hack": "Tanqidchilar da'vosi: Mualliflarning o'zi bitta yakdil fikrda bo'lmagan, ko'plab o'zaro murosalardan iborat bo'lgan."
    },

    # --- CROSS-TEXT CONNECTIONS (7 questions) ---
    {
        "id": "r_b6_19",
        "domain": "Craft and Structure - Cross-Text Connections",
        "skill": "Cross-Text Connections",
        "difficulty": "Hard",
        "passage": "Text 1: Geothermal energy systems represent the pinnacle of baseload renewable power. Because subterranean thermal reservoirs remain completely unaffected by atmospheric weather fluctuations or daylight cycles, geothermal plants deliver continuous, dispatchable electrical output without requiring supplementary battery storage infrastructure.\n\nText 2: While geothermal facilities generate reliable baseload electricity, their deployment is constrained by geographic realities. Deep drilling into hydrothermal reservoirs carries substantial seismic risks, as hydraulic fracturing can induce micro-earthquakes, creating formidable permitting hurdles in densely populated regions.",
        "question": "Based on the texts, how would the author of Text 2 most likely respond to the characterization of geothermal energy in Text 1?",
        "options": [
            {"key": "A", "text": "By acknowledging its operational reliability while emphasizing the safety and geographic constraints that limit widespread adoption."},
            {"key": "B", "text": "By disputing the claim that geothermal power output remains unaffected by subterranean conditions."},
            {"key": "C", "text": "By arguing that solar and wind technologies are substantially more dependable than geothermal facilities."},
            {"key": "D", "text": "By proving that battery storage infrastructure is cheaper than deep geothermal drilling operations."}
        ],
        "correct": "A",
        "explanation": "Text 2 concedes Text 1's main claim ('While geothermal facilities generate reliable baseload electricity...'), but immediately introduces limitations (geographic constraints, seismic risks, permitting hurdles). Choice A captures this nuanced reaction.",
        "strategy_or_hack": "Cross-text mantiqi: Text 2 Text 1 ning afzalligini tan oladi ('reliable'), lekin xatarlari va cheklovlarini ko'rsatadi ('seismic risks, geographic constraints')."
    },
    {
        "id": "r_b6_20",
        "domain": "Craft and Structure - Cross-Text Connections",
        "skill": "Cross-Text Connections",
        "difficulty": "Medium",
        "passage": "Text 1: Traditional classroom education relies heavily on direct lectures, ensuring standardized curriculum delivery across diverse student populations. When experienced educators articulate foundational concepts systematically, students acquire a coherent structural framework for subsequent independent problem-solving.\n\nText 2: Purely lecture-driven pedagogical models fail to engage active student cognition. Cognitive research demonstrates that when learners construct knowledge collaboratively through experiential workshops and peer debate, long-term conceptual retention rates exceed those produced by passive listening by over thirty percent.",
        "question": "Which choice best describes the central tension between Text 1 and Text 2?",
        "options": [
            {"key": "A", "text": "Whether teacher-directed direct instruction or collaborative experiential learning produces superior pedagogical outcomes."},
            {"key": "B", "text": "Whether standardized testing should remain the primary metric for evaluating student performance."},
            {"key": "C", "text": "Whether independent problem-solving should be eliminated entirely from secondary school curricula."},
            {"key": "D", "text": "Whether online instructional videos can successfully replace experienced classroom educators."}
        ],
        "correct": "A",
        "explanation": "Text 1 advocates for direct teacher lectures as foundational, while Text 2 argues that passive lectures fail and collaborative experiential learning yields higher retention. The central debate is between lecture-based instruction vs collaborative experiential learning.",
        "strategy_or_hack": "Asosiy qarama-qarshilik: Text 1 (o'qituvchi ma'ruzasi/direct lecture) vs Text 2 (hamkorlikdagi tajriba/experiential learning)."
    },
    {
        "id": "r_b6_21",
        "domain": "Craft and Structure - Cross-Text Connections",
        "skill": "Cross-Text Connections",
        "difficulty": "Hard",
        "passage": "Text 1: Economist David Ricardo formulated the theory of comparative advantage, arguing that nations maximize mutual wealth by specializing exclusively in producing commodities with the lowest opportunity costs, trading freely for all remaining goods.\n\nText 2: The supply chain disruptions of the early 2020s revealed a perilous vulnerability in unconstrained Ricardian specialization. When nations concentrate domestic capacity in narrow sectors, unforeseen geopolitical or logistical shocks can completely sever access to critical medicines and technological components.",
        "question": "The author of Text 2 would most likely characterize Ricardo’s theory in Text 1 as",
        "options": [
            {"key": "A", "text": "theoretically coherent under ideal conditions but dangerously indifferent to the risks of catastrophic supply disruptions."},
            {"key": "B", "text": "mathematically flawed from its inception due to incorrect assumptions about commodity pricing."},
            {"key": "C", "text": "wholly inapplicable to modern agricultural commerce while perfectly suited for advanced manufacturing."},
            {"key": "D", "text": "an obsolete doctrine that has been universally rejected by contemporary international trade organizations."}
        ],
        "correct": "A",
        "explanation": "Text 2 does not claim Ricardo's logic was mathematically erroneous; rather, it highlights that real-world shocks create 'perilous vulnerability' when nations specialize completely, exposing them to catastrophic disruptions.",
        "strategy_or_hack": "Bo'rttirilgan variantlarni rad eting ('mathematically flawed', 'universally rejected'). Text 2 kutilmagan uzilishlar xatarini ko'rsatmoqda."
    },
    {
        "id": "r_b6_22",
        "domain": "Craft and Structure - Cross-Text Connections",
        "skill": "Cross-Text Connections",
        "difficulty": "Medium",
        "passage": "Text 1: De-extinction initiatives using CRISPR gene-editing to resurrect woolly mammoth phenotypes aim to restore Arctic tundra ecosystems. By trampling dense shrubs and compacting snow, recreated megafauna could prevent permafrost melt, sequestering gigatons of subterranean carbon dioxide.\n\nText 2: Releasing genetically modified proxies into fragile subpolar biomes carries unpredictable ecological liabilities. Resources directed toward mammoth resurrection would yield far greater biodiversity returns if allocated toward protecting existing endangered species currently teetering on the brink of extinction.",
        "question": "Based on the texts, what primary concern does the author of Text 2 raise that is not addressed in Text 1?",
        "options": [
            {"key": "A", "text": "The opportunity cost of diverting conservation capital away from surviving endangered wildlife."},
            {"key": "B", "text": "The technological impossibility of successfully synthesizing ancient mammoth genetic sequences."},
            {"key": "C", "text": "The likelihood that mammoth herds would accelerate the melting of Arctic permafrost layers."},
            {"key": "D", "text": "The ethical rights of individual animals bred under artificial laboratory conditions."}
        ],
        "correct": "A",
        "explanation": "Text 2 explicitly states that resources spent on resurrection 'would yield far greater biodiversity returns if allocated toward protecting existing endangered species'. This financial/resource trade-off (opportunity cost) is absent in Text 1.",
        "strategy_or_hack": "Yangi dalil kaliti: Text 2 mablag'ni mavjud yo'qolib borayotgan turlarni saqlashga yo'naltirish (opportunity cost) masalasini ko'taradi."
    },
    {
        "id": "r_b6_23",
        "domain": "Craft and Structure - Cross-Text Connections",
        "skill": "Cross-Text Connections",
        "difficulty": "Easy",
        "passage": "Text 1: Electric vehicles eliminate direct tailpipe greenhouse emissions, making personal transportation substantially cleaner and drastically reducing localized urban smog in densely populated metropolitan areas.\n\nText 2: While electric cars eliminate tailpipe exhaust, their overall environmental footprint depends heavily on how regional power grids generate electricity. If battery charging relies on coal-fired power plants, net carbon emissions are merely displaced from highways to rural generation facilities.",
        "question": "Both authors would most likely agree with which statement regarding electric vehicles?",
        "options": [
            {"key": "A", "text": "They produce zero tailpipe emissions at the point of vehicle operation."},
            {"key": "B", "text": "They are fundamentally dirtier than conventional internal combustion engine automobiles."},
            {"key": "C", "text": "They cannot function efficiently in regions dependent on renewable energy sources."},
            {"key": "D", "text": "They should be banned until all electrical grids achieve complete decarbonization."}
        ],
        "correct": "A",
        "explanation": "Text 1 states 'Electric vehicles eliminate direct tailpipe greenhouse emissions', and Text 2 begins 'While electric cars eliminate tailpipe exhaust...'. Both agree that at the point of vehicle operation, there are no tailpipe emissions.",
        "strategy_or_hack": "Umumiy kelishuv nuqtasi: Ikkala matn ham EV avtomobillari quvuridan chiqindi chiqmasligini (zero tailpipe emissions) tasdiqlaydi."
    },
    {
        "id": "r_b6_24",
        "domain": "Craft and Structure - Cross-Text Connections",
        "skill": "Cross-Text Connections",
        "difficulty": "Hard",
        "passage": "Text 1: Digital archives democratize historical inquiry. By digitizing fragile nineteenth-century manuscripts, cultural institutions enable researchers worldwide to examine rare source materials without the prohibitive financial expense of transatlantic travel.\n\nText 2: The transition from physical manuscript inspection to digital scans is not without interpretive loss. Digital reproductions frequently flatten paper textures, obscure watermarks, and homogenize faded ink tones, blinding historians to the material sociology of text production.",
        "question": "How does Text 2 qualify the optimistic assessment presented in Text 1?",
        "options": [
            {"key": "A", "text": "By demonstrating that digitization introduces material blind spots that can undermine nuanced historical analysis."},
            {"key": "B", "text": "By proving that online archives charge higher subscription fees than physical library memberships."},
            {"key": "C", "text": "By arguing that digital file corruption permanently destroys ancient manuscript collections."},
            {"key": "D", "text": "By claiming that non-academic researchers should be barred from accessing digitized primary sources."}
        ],
        "correct": "A",
        "explanation": "Text 1 praises digital access and democratization. Text 2 qualifies this by pointing out what is lost in digital scans: texture, watermarks, ink tone (material blind spots that affect historical interpretation).",
        "strategy_or_hack": "Cheklov: Text 2 raqamli nusxalarda qog'oz teksturasi, siyoh nozikliklari yo'qolib, tarixiy tahlilga zarar yetishi mumkinligini aytadi."
    },
    {
        "id": "r_b6_25",
        "domain": "Craft and Structure - Cross-Text Connections",
        "skill": "Cross-Text Connections",
        "difficulty": "Medium",
        "passage": "Text 1: Space agencies should prioritize crewed missions to Mars. Human astronauts possess tactile adaptability, spontaneous problem-solving capacity, and observational intuition that robotic rovers cannot match when seeking extraterrestrial biosignatures.\n\nText 2: Robotic exploration missions to the Martian surface cost a fraction of human voyages and eliminate the catastrophic risk to human life. Furthermore, autonomous robotic rovers can operate uninterrupted for decades without demanding life-support infrastructure or return launch vehicles.",
        "question": "On which point do the authors of Text 1 and Text 2 disagree?",
        "options": [
            {"key": "A", "text": "Whether exploration missions to Mars should prioritize human crews or robotic platforms."},
            {"key": "B", "text": "Whether Mars possesses potential biosignatures worthy of scientific investigation."},
            {"key": "C", "text": "Whether robotic rovers require electrical power systems to operate on Mars."},
            {"key": "D", "text": "Whether human astronauts require life-support systems during spaceflight."}
        ],
        "correct": "A",
        "explanation": "Text 1 argues space agencies should prioritize crewed missions due to human adaptability. Text 2 argues robotic missions should be prioritized due to lower costs, safety, and longevity. The fundamental disagreement is human vs robotic priority.",
        "strategy_or_hack": "Ixtilof nuqtasi: Mars tadqiqotida odamlar (crewed) yoki robotlar (robotic rovers) ustuvor bo'lishi kerakligi."
    },

    # --- CENTRAL IDEAS AND DETAILS (8 questions) ---
    {
        "id": "r_b6_26",
        "domain": "Information and Ideas - Central Ideas and Details",
        "skill": "Central Ideas and Details",
        "difficulty": "Easy",
        "passage": "In temperate forest ecosystems, mycorrhizal fungi form expansive underground networks that connect the root systems of disparate tree species. Through these fungal conduits, mature canopy trees transfer surplus carbohydrates to shaded saplings that cannot yet perform sufficient photosynthesis, while receiving mineral nutrients that fungi extract from deep soil strata. This reciprocal exchange challenges conventional models of forest dynamics that characterize trees solely as fierce competitors for light.",
        "question": "Which choice best states the main idea of the text?",
        "options": [
            {"key": "A", "text": "Underground mycorrhizal networks facilitate nutrient sharing among trees, revealing a cooperative dimension in forest ecology."},
            {"key": "B", "text": "Temperate saplings frequently parasitize mature canopy trees, causing extensive canopy dieback across old-growth forests."},
            {"key": "C", "text": "Fungi extract carbohydrates from soil layers without providing any physiological benefits to tree root systems."},
            {"key": "D", "text": "Trees compete so aggressively for sunlight that underground root networks rarely survive into maturity."}
        ],
        "correct": "A",
        "explanation": "The text explains that fungal networks allow mature trees to share sugars with shaded saplings in exchange for minerals, demonstrating mutual cooperation rather than pure competition. Choice A accurately captures this central idea.",
        "strategy_or_hack": "Asosiy g'oya: daraxtlar bir-biri bilan qo'ziqorin to'rlari orqali ozuqa almashadi va hamkorlik qiladi (cooperative dimension)."
    },
    {
        "id": "r_b6_27",
        "domain": "Information and Ideas - Central Ideas and Details",
        "skill": "Central Ideas and Details",
        "difficulty": "Medium",
        "passage": "During the Bronze Age, the Mediterranean tin trade was vital for bronze weapon production, yet the geographical origins of ancient tin ingots have long baffled archaeologists. While copper deposits were abundant in Cyprus and Anatolia, geological tin deposits are notoriously sparse in the eastern Mediterranean. Recent chemical isotope analysis of shipwrecks at Uluburun suggests that much of this tin originated in deposits as distant as Central Asia and Cornwall, proving that Bronze Age trade networks were far more intercontinental than previously believed.",
        "question": "According to the text, what did isotope analysis of the Uluburun shipwreck tin ingots demonstrate?",
        "options": [
            {"key": "A", "text": "Bronze Age trade routes spanned vast intercontinental distances reaching far beyond the eastern Mediterranean."},
            {"key": "B", "text": "Cypriot miners were the exclusive suppliers of refined tin to ancient Aegean metalworkers."},
            {"key": "C", "text": "Bronze Age weapons were constructed primarily of copper rather than alloyed bronze."},
            {"key": "D", "text": "Tin mining was widely practiced throughout the Peloponnese peninsula."}
        ],
        "correct": "A",
        "explanation": "The text explicitly states that isotope analysis showed tin came from places as far as Central Asia and Cornwall, 'proving that Bronze Age trade networks were far more intercontinental than previously believed.'",
        "strategy_or_hack": "Matndan aniq fakt: 'trade networks were far more intercontinental than previously believed' => A."
    },
    {
        "id": "r_b6_28",
        "domain": "Information and Ideas - Central Ideas and Details",
        "skill": "Central Ideas and Details",
        "difficulty": "Medium",
        "passage": "Linguistic anthropologist Dr. Kenji Sato investigated the acoustic properties of whistling languages used in mountainous terrain across Turkey, the Canary Islands, and the Mexican highlands. Sato discovered that whistled speech operates by mimicking the fundamental frequency contours of spoken vowels while compressing acoustic energy into high-decibel tones between 1 and 4 kHz. This specific frequency band minimizes atmospheric scattering and echoes against rocky canyon walls, enabling clear communication across valleys up to five miles wide.",
        "question": "Which choice best describes the primary function of whistling languages according to the text?",
        "options": [
            {"key": "A", "text": "They utilize specialized acoustic frequencies to transmit intelligible messages across expansive, rugged terrain."},
            {"key": "B", "text": "They replace traditional alphabets with musical notes to prevent neighboring villages from understanding conversations."},
            {"key": "C", "text": "They were invented by military scouts to evade detection by acoustic surveillance technologies."},
            {"key": "D", "text": "They allow mountaineers to signal wildlife without disturbing native bird species."}
        ],
        "correct": "A",
        "explanation": "The text explains that whistled languages compress acoustic energy into 1-4 kHz frequencies, minimizing echoes against canyon walls to communicate across valleys up to 5 miles wide (intelligible communication across rugged terrain).",
        "strategy_or_hack": "Asosiy funktsiya: tog'li va keng hududlarda 5 milgacha ovozli axborotni uzatish."
    },
    {
        "id": "r_b6_29",
        "domain": "Information and Ideas - Central Ideas and Details",
        "skill": "Central Ideas and Details",
        "difficulty": "Hard",
        "passage": "In standard macroeconomic theory, high inflation is typically assumed to suppress aggregate consumer spending as household purchasing power declines. However, during the post-pandemic recovery, economists observed an unusual phenomenon termed 'inflationary psychology': anticipating that durable goods, vehicles, and electronics would become even more expensive in subsequent quarters, consumers accelerated major purchases rather than postponing them. This front-loading of demand temporarily intensified price pressures, illustrating how consumer expectations can actively perpetuate the very inflationary cycles they fear.",
        "question": "Which choice best summarizes the central mechanism of 'inflationary psychology' described in the passage?",
        "options": [
            {"key": "A", "text": "Consumers rush to purchase expensive durable goods immediately to avoid anticipated future price hikes, thereby sustaining inflationary momentum."},
            {"key": "B", "text": "Households drastically curtail all retail expenditures, causing sudden deflation in durable consumer goods."},
            {"key": "C", "text": "Commercial banks lower interest rates on loans, encouraging consumer borrowing during economic contractions."},
            {"key": "D", "text": "Consumers mistakenly assume that wages will decline, leading to long-term reductions in consumer debt."}
        ],
        "correct": "A",
        "explanation": "The passage states that expecting higher future prices, consumers 'accelerated major purchases rather than postponing them', which front-loaded demand and intensified price pressures. Choice A captures this dynamic precisely.",
        "strategy_or_hack": "Mexanizm: Narxlar yana oshadi deb hozirdan ommaviy xarid qilish talabni oshirib, inflatsiyani battar kuchaytiradi."
    },
    {
        "id": "r_b6_30",
        "domain": "Information and Ideas - Central Ideas and Details",
        "skill": "Central Ideas and Details",
        "difficulty": "Easy",
        "passage": "Tardigrades, microscopic eight-legged invertebrates, can survive extreme environments that would prove instantly fatal to most multicellular organisms. When faced with complete desiccation or freezing temperatures, tardigrades enter an extraordinary state of suspended animation known as anhydrobiosis, expelling nearly all cellular water and replacing it with specialized protective proteins. In this vitrified state, their metabolic activity slows to undetectable levels until rehydration revives them.",
        "question": "According to the passage, what physiological adaptation enables tardigrades to survive desiccation?",
        "options": [
            {"key": "A", "text": "They enter anhydrobiosis by replacing cellular water with protective proteins and suspending measurable metabolism."},
            {"key": "B", "text": "They burrow deep into damp subterranean soil to absorb groundwater during droughts."},
            {"key": "C", "text": "They rapidly accelerate their metabolic rate to generate internal heat and moisture."},
            {"key": "D", "text": "They shed their outer exoskeleton and migrate to high-humidity aquatic environments."}
        ],
        "correct": "A",
        "explanation": "The text directly states that when facing desiccation, they enter 'anhydrobiosis, expelling nearly all cellular water and replacing it with specialized protective proteins' while metabolic activity drops to undetectable levels.",
        "strategy_or_hack": "Matndagi to'g'ridan-to'g'ri dalil: 'anhydrobiosis, replacing water with protective proteins'."
    },
    {
        "id": "r_b6_31",
        "domain": "Information and Ideas - Central Ideas and Details",
        "skill": "Central Ideas and Details",
        "difficulty": "Medium",
        "passage": "Urban heat islands occur when dense metropolitan infrastructure—such as asphalt roadways, concrete buildings, and dark rooftops—absorbs and re-radiates daytime solar thermal energy much more effectively than rural landscapes composed of vegetation and open soil. Consequently, nighttime temperatures in major metropolitan cores can remain up to 10 degrees Fahrenheit warmer than surrounding rural countryside.",
        "question": "What is the primary cause of nighttime urban warmth described in the text?",
        "options": [
            {"key": "A", "text": "Dense building materials absorb heat during the day and re-radiate it into the atmosphere at night."},
            {"key": "B", "text": "High volumes of vehicle exhaust trap atmospheric moisture over metropolitan centers."},
            {"key": "C", "text": "Industrial factories operate exclusively during evening hours, emitting massive heat plumes."},
            {"key": "D", "text": "Vegetation in rural areas reflects all solar radiation back into space during daylight hours."}
        ],
        "correct": "A",
        "explanation": "The passage explains that dense materials (asphalt, concrete, dark rooftops) absorb solar thermal energy during the day and re-radiate it, keeping nighttime temperatures elevated.",
        "strategy_or_hack": "Sabab: asfalt va beton kunduzi issiqlikni yutib, kechasi chiqarishi (absorb and re-radiate)."
    },
    {
        "id": "r_b6_32",
        "domain": "Information and Ideas - Central Ideas and Details",
        "skill": "Central Ideas and Details",
        "difficulty": "Hard",
        "passage": "The rediscovery of Gregor Mendel’s genetic hybridization experiments in 1900 initially appeared to undermine Charles Darwin’s theory of natural selection. Early Mendelians argued that evolution proceeded in sudden, discontinuous jumps driven by large-scale genetic mutations. It was not until the 'Modern Synthesis' of the 1930s that mathematical population geneticists demonstrated that continuous phenotypic variation could be produced by the additive accumulation of many discrete Mendelian alleles subject to gradual selection.",
        "question": "Which choice best summarizes the historical resolution between Mendelian genetics and Darwinian evolution?",
        "options": [
            {"key": "A", "text": "Population geneticists mathematically showed that gradual Darwinian selection acts upon combinations of discrete Mendelian genes."},
            {"key": "B", "text": "Darwinian natural selection was discarded in favor of sudden mutational leaps across all vertebrate species."},
            {"key": "C", "text": "Mendel’s experimental results were discredited after modern researchers discovered errors in his pea-plant ratios."},
            {"key": "D", "text": "Biologists concluded that phenotypic traits are governed exclusively by environmental exposure rather than genetic inheritance."}
        ],
        "correct": "A",
        "explanation": "The text states that in the 1930s Modern Synthesis, mathematical geneticists proved that continuous variation can arise from additive combinations of discrete Mendelian alleles under gradual natural selection.",
        "strategy_or_hack": "Tarixiy yechim: Mendel genlari (discrete alleles) va Darvinning asta-sekin tanlanishi (gradual selection) matematik birlashtirilgan."
    },
    {
        "id": "r_b6_33",
        "domain": "Information and Ideas - Central Ideas and Details",
        "skill": "Central Ideas and Details",
        "difficulty": "Medium",
        "passage": "In classical Islamic astronomy, scholars at observatories like Maragha and Samarkand did not merely translate ancient Greek Ptolemaic texts; they systematically identified mathematical flaws in Ptolemy’s geocentric equant model. Astronomers such as Nasir al-Din al-Tusi developed geometric devices like the 'Tusi couple'—which generates rectilinear motion from two circular rotations—to resolve mechanical contradictions without abandoning observational fidelity.",
        "question": "According to the passage, what was the primary significance of the 'Tusi couple' in medieval astronomy?",
        "options": [
            {"key": "A", "text": "It provided a geometric mechanism that eliminated mathematical contradictions in Greek planetary models."},
            {"key": "B", "text": "It proved definitively that the Sun occupies the physical center of the solar system."},
            {"key": "C", "text": "It replaced all celestial observation instruments with mechanical computing clocks."},
            {"key": "D", "text": "It demonstrated that planetary orbits are elliptical rather than circular."}
        ],
        "correct": "A",
        "explanation": "The text states al-Tusi developed the Tusi couple 'to resolve mechanical contradictions' in Ptolemy's models 'without abandoning observational fidelity'. Choice A matches this purpose directly.",
        "strategy_or_hack": "'Tusi couple' maqsadi: Ptolemey modellaridagi geometrik va mexanik ziddiyatlarni bartaraf etish."
    },

    # --- COMMAND OF EVIDENCE & INFERENCES (17 questions) ---
    {
        "id": "r_b6_34",
        "domain": "Information and Ideas - Command of Evidence (Textual)",
        "skill": "Command of Evidence",
        "difficulty": "Hard",
        "passage": "Ecologist Dr. Elena Vance hypothesized that invasive zebra mussels in the Great Lakes selectively consume non-toxic green algae while rejecting toxin-producing cyanobacteria, thereby triggering toxic algae blooms. To test this hypothesis, Vance placed zebra mussels into aquariums with mixed phytoplankton cultures. After twelve hours, cell counts revealed a 78% reduction in green algae concentrations, whereas cyanobacteria cell densities remained entirely unaffected.",
        "question": "Which finding from Vance's experiment, if true, most directly supports her hypothesis?",
        "options": [
            {"key": "A", "text": "Zebra mussels filtered out substantial amounts of green algae while leaving toxic cyanobacteria populations untouched."},
            {"key": "B", "text": "Zebra mussels grew at equal rates regardless of whether phytoplankton cultures contained cyanobacteria."},
            {"key": "C", "text": "Green algae populations replicated faster in open lake water than in controlled aquarium settings."},
            {"key": "D", "text": "Cyanobacteria populations consumed organic nutrients secreted by dying zebra mussels."}
        ],
        "correct": "A",
        "explanation": "The hypothesis is that zebra mussels selectively eat green algae and reject toxic cyanobacteria. The cell counts showed a 78% drop in green algae and zero change in cyanobacteria, which directly confirms this selective consumption.",
        "strategy_or_hack": "Gipotezani tasdiqlovchi dalil: Yaxshi suv o'tlarini yeb (78% reduction), zaharli sianobakteriyalarga tegmadi (untouched)."
    },
    {
        "id": "r_b6_35",
        "domain": "Information and Ideas - Inferences",
        "skill": "Inferences",
        "difficulty": "Medium",
        "passage": "In many social bird species, individuals emit alarm calls when spotting aerial predators, alerting the entire flock to take cover. While alarm calls temporarily increase the caller’s visibility to hawks, evolutionary biologists observe that sentinel birds call most frequently when foraging alongside direct genetic kin (offspring, siblings, and parents) and significantly reduce vocalizations when foraging among unrelated flocks.",
        "question": "Which choice most logically completes the text based on the evolutionary dynamics described?",
        "options": [
            {"key": "A", "text": "This behavior suggests that alarm calling is maintained by kin selection, where the reproductive benefits to shared genes outweigh the caller’s immediate risk."},
            {"key": "B", "text": "This behavior proves that sentinel birds are incapable of distinguishing between aerial predators and ground predators."},
            {"key": "C", "text": "This behavior demonstrates that birds only forage when their genetic parents are present in the immediate flock."},
            {"key": "D", "text": "This behavior indicates that aerial predators intentionally avoid attacking flocks with close genetic relatedness."}
        ],
        "correct": "A",
        "explanation": "The callers take personal risk to alert genetic kin, but remain quiet around non-relatives. This fits the evolutionary principle of kin selection: protecting shared genes justifies individual risk. Choice A is the only logically sound conclusion.",
        "strategy_or_hack": "Mantiqiy xulosa: Faqat qarindoshlar (genetic kin) yonida ogohlantirish signali berilishi qarindoshlik tanlanishi (kin selection) bilan izohlanadi."
    },
    {
        "id": "r_b6_36",
        "domain": "Information and Ideas - Command of Evidence (Textual)",
        "skill": "Command of Evidence",
        "difficulty": "Medium",
        "passage": "Historians debating the collapse of the Maya city-state of Copán in the ninth century have proposed two competing theories. Dr. Harris argues that prolonged megadroughts caused catastrophic crop failures. Conversely, Dr. Mendez contends that intensive deforestation of hillside slopes for agriculture caused severe soil erosion that ruined valley farmlands even before drought periods commenced.",
        "question": "Which discovery, if true, would most strongly support Dr. Mendez's contention over Dr. Harris's theory?",
        "options": [
            {"key": "A", "text": "Sediment core samples from the Copán valley reveal massive layers of eroded hillside silt deposited decades prior to the onset of the ninth-century drought."},
            {"key": "B", "text": "Meteorological tree-ring data from neighboring regions indicate severe rainfall deficits throughout the entire ninth century."},
            {"key": "C", "text": "Archaeological excavations at Copán reveal granaries filled with surplus maize dating to the height of the drought."},
            {"key": "D", "text": "Royal inscriptions celebrate successful irrigation canal construction across Copán’s lower valley."}
        ],
        "correct": "A",
        "explanation": "Dr. Mendez claims hillside deforestation caused soil erosion that ruined farmland BEFORE the drought started. Finding eroded hillside silt layers deposited decades before the drought provides concrete physical evidence for Mendez's timeline.",
        "strategy_or_hack": "Mendez dalili: qurg'oqchilikdan oldin (decades prior) tuproq eroziyasi sodir bo'lganini isbotlovchi cho'kindi qatlamlari (eroded silt)."
    },
    {
        "id": "r_b6_37",
        "domain": "Information and Ideas - Inferences",
        "skill": "Inferences",
        "difficulty": "Hard",
        "passage": "Deep-sea hydrothermal vents emit superheated mineral plumes completely devoid of sunlight. While terrestrial and epipelagic marine ecosystems derive their primary energy from solar photosynthesis, hydrothermal vent ecosystems thrive on chemosynthesis conducted by autotrophic bacteria that oxidize dissolved hydrogen sulfide into organic matter. Therefore, if a planetary body possessed sub-surface liquid oceans beneath a lightless frozen crust and had active geothermal hydrothermal vents, ______",
        "question": "Which choice most logically completes the text?",
        "options": [
            {"key": "A", "text": "it could theoretically sustain chemosynthetic life forms without requiring any solar illumination."},
            {"key": "B", "text": "photosynthetic plant species would quickly colonize the subterranean oceanic hydrothermal vents."},
            {"key": "C", "text": "its icy crust would inevitably melt within several decades due to geothermal water circulation."},
            {"key": "D", "text": "its atmospheric gases would be chemically identical to those found in Earth's lower troposphere."}
        ],
        "correct": "A",
        "explanation": "The text establishes that chemosynthetic life requires hydrothermal vents/minerals and zero sunlight. Therefore, an icy planet with geothermal vents beneath lightless ice could theoretically support chemosynthetic life. Choice A is the direct logical deduction.",
        "strategy_or_hack": "Mantiqiy davom: Quyosh nuri yo'q joyda ham xemotrof bakteriyalar yashay oladi => quyoshsiz hayot mavjud bo'lishi mumkin."
    },
    {
        "id": "r_b6_38",
        "domain": "Information and Ideas - Command of Evidence (Textual)",
        "skill": "Command of Evidence",
        "difficulty": "Hard",
        "passage": "In behavioral economics, the 'endowment effect' describes how individuals assign greater subjective value to an object simply because they own it. To test whether the effect is rooted in loss aversion rather than sentimental attachment, researchers gave participants an ordinary coffee mug and measured how much money they demanded to sell it immediately, before any emotional attachment could develop.",
        "question": "Which experimental outcome would most strongly support the hypothesis that the endowment effect is driven by instantaneous loss aversion rather than gradual sentimental attachment?",
        "options": [
            {"key": "A", "text": "Participants demanded nearly twice as much money to sell the mug within seconds of receiving it as non-owners were willing to pay to buy it."},
            {"key": "B", "text": "Participants who held the mug for several weeks demanded the same selling price as those who held it for only five minutes."},
            {"key": "C", "text": "Participants willingly traded the mug for an equivalent ballpoint pen of identical monetary value."},
            {"key": "D", "text": "Participants refused to sell the mug regardless of how high an offer the researchers presented."}
        ],
        "correct": "A",
        "explanation": "If the endowment effect appears 'within seconds of receiving it' (before emotional attachment can develop), it demonstrates that the higher valuation is caused by immediate aversion to losing possession, rather than time-based sentimental bonding.",
        "strategy_or_hack": "Oniy yo'qotishdan qo'rqish: bir necha soniyada (within seconds) sotish narxini xaridor narxidan 2 barobar yuqori qo'yish."
    },
    {
        "id": "r_b6_39",
        "domain": "Information and Ideas - Inferences",
        "skill": "Inferences",
        "difficulty": "Easy",
        "passage": "In desert plants known as succulents, stomata remain tightly closed throughout hot daylight hours to prevent moisture evaporation. Instead, these plants open their stomata during cool nights to absorb and store carbon dioxide as malic acid, which is then broken down for photosynthesis when the sun rises. This specialized metabolic pathway implies that ______",
        "question": "Which choice most logically completes the text?",
        "options": [
            {"key": "A", "text": "succulents prioritize water conservation over maximizing the speed of daytime carbon uptake."},
            {"key": "B", "text": "succulents do not require sunlight or chlorophyll to produce glucose molecules."},
            {"key": "C", "text": "succulents release large volumes of water vapor into desert atmospheres during the day."},
            {"key": "D", "text": "succulents grow substantially faster than temperate crops grown under constant irrigation."}
        ],
        "correct": "A",
        "explanation": "By closing stomata by day to prevent water loss and only taking in CO2 at night, succulents sacrifice fast daytime CO2 intake to prioritize survival and water retention in arid conditions.",
        "strategy_or_hack": "Mantiq: Kunduzi barg teshiklarini yopib turish suvni saqlashni birinchi o'ringa qo'yishni (water conservation) anglatadi."
    },
    {
        "id": "r_b6_40",
        "domain": "Information and Ideas - Command of Evidence (Textual)",
        "skill": "Command of Evidence",
        "difficulty": "Medium",
        "passage": "Cognitive psychologists hypothesized that sleep spindles—brief bursts of high-frequency oscillatory brain activity during non-REM sleep—play an active role in consolidating newly learned motor memories. In an experiment, participants practiced a complex finger-tapping sequence before either taking a nap or remaining awake.",
        "question": "Which finding from the experiment would most directly reinforce the researchers’ hypothesis?",
        "options": [
            {"key": "A", "text": "Participants who exhibited higher densities of sleep spindles during their nap showed significantly greater speed and accuracy improvements on the motor task when retested."},
            {"key": "B", "text": "Participants in the wake group performed equally well on verbal vocabulary tests as participants in the nap group."},
            {"key": "C", "text": "Sleep spindles occurred at identical frequencies during both rapid eye movement (REM) and non-REM sleep cycles."},
            {"key": "D", "text": "Participants reported feeling more alert after taking a 90-minute nap than after resting quietly awake."}
        ],
        "correct": "A",
        "explanation": "The hypothesis links sleep spindle density with motor memory consolidation. If participants with more spindles show significantly higher speed/accuracy upon retesting, it directly supports the hypothesis.",
        "strategy_or_hack": "To'g'ridan-to'g'ri bog'liqlik: Ko'proq uyqu spindillari = harakat xotirasining sezilarli darajada yaxshilanishi (speed and accuracy improvements)."
    },
    {
        "id": "r_b6_41",
        "domain": "Information and Ideas - Inferences",
        "skill": "Inferences",
        "difficulty": "Hard",
        "passage": "Astronomers surveying distant exoplanets utilize transmission spectroscopy, measuring starlight filtering through a planet’s upper atmosphere during transit. If an exoplanet’s atmosphere contains methane and carbon dioxide in thermodynamic disequilibrium without high levels of carbon monoxide, it suggests that active biological metabolisms may be constantly replenishing the short-lived atmospheric methane against photochemical destruction. Thus, detecting this specific disequilibrium ______",
        "question": "Which choice most logically completes the text?",
        "options": [
            {"key": "A", "text": "serves as a compelling potential biosignature warranting rigorous observational follow-up."},
            {"key": "B", "text": "proves conclusively that advanced multicellular vegetation covers the planetary surface."},
            {"key": "C", "text": "demonstrates that the exoplanet's atmosphere has been completely stripped away by stellar winds."},
            {"key": "D", "text": "indicates that the host star is too cool to emit ultraviolet radiation."}
        ],
        "correct": "A",
        "explanation": "The passage states that this specific chemical disequilibrium suggests ongoing biological replenishing. In astrobiology, such a chemical signature is considered a strong potential biosignature that merits further study. It does not 'prove conclusively' (which is too extreme).",
        "strategy_or_hack": "SAT qoidasi: 'Proves conclusively' kabi mutlaq so'zlardan qoching. 'Serves as a compelling potential biosignature' to'g'ri ilmiy xulosa."
    },
    {
        "id": "r_b6_42",
        "domain": "Information and Ideas - Command of Evidence (Textual)",
        "skill": "Command of Evidence",
        "difficulty": "Medium",
        "passage": "Linguists studying historical vowel shifts analyzed audio recordings of twentieth-century English radio broadcasts from diverse decades. Dr. Patel proposed that phonetic drift in vowel pronunciation is accelerated during periods of significant demographic migration into major broadcast hubs.",
        "question": "Which piece of evidence, if true, would most strongly support Dr. Patel's proposition?",
        "options": [
            {"key": "A", "text": "Decades with the highest rates of interregional domestic migration into broadcast centers exhibited the most rapid phonetic shifts in recorded vowel formants."},
            {"key": "B", "text": "Broadcasters who received formal elocution training maintained identical vowel pronunciations across their four-decade careers."},
            {"key": "C", "text": "Rural dialects spoken in isolated agricultural communities underwent substantial vowel modifications during periods of strict demographic stability."},
            {"key": "D", "text": "Radio receiver technology improved significantly, allowing sound engineers to eliminate background static from live broadcasts."}
        ],
        "correct": "A",
        "explanation": "Dr. Patel's claim is that migration accelerates phonetic vowel drift. Finding that decades with the highest migration rates coincided with the most rapid shifts in vowel formants provides direct empirical correlation.",
        "strategy_or_hack": "Korrelatsiya: Migratsiya eng yuqori bo'lgan davrlarda unli tovushlarning eng tez o'zgarishi qayd etilgan."
    },
    {
        "id": "r_b6_43",
        "domain": "Information and Ideas - Inferences",
        "skill": "Inferences",
        "difficulty": "Easy",
        "passage": "In a controlled laboratory experiment, agricultural scientists treated tomato plants with either a standard nitrogen fertilizer or a bio-inoculant containing beneficial rhizobacteria. Plants treated with rhizobacteria developed 40% more root surface area and exhibited higher drought tolerance during dry soil trials, despite receiving 30% less synthetic fertilizer. These results indicate that ______",
        "question": "Which choice most logically completes the text?",
        "options": [
            {"key": "A", "text": "rhizobacteria can enhance plant root development and resource efficiency while reducing dependence on synthetic fertilizers."},
            {"key": "B", "text": "synthetic nitrogen fertilizers are completely toxic to tomato plant root systems."},
            {"key": "C", "text": "tomato plants cannot absorb water from dry soil unless synthetic fertilizers are applied."},
            {"key": "D", "text": "bio-inoculants will cause severe soil acidification if applied in agricultural fields."}
        ],
        "correct": "A",
        "explanation": "The plants with rhizobacteria grew more roots and survived drought better while using less synthetic fertilizer. This shows they enhance root development and efficiency while decreasing synthetic fertilizer needs.",
        "strategy_or_hack": "To'g'ridan-to'g'ri xulosa: rizobakteriyalar ildizni o'stiradi va kimyoviy o'g'itga ehtiyojni kamaytiradi."
    },
    {
        "id": "r_b6_44",
        "domain": "Information and Ideas - Command of Evidence (Textual)",
        "skill": "Command of Evidence",
        "difficulty": "Hard",
        "passage": "Ornithologist Dr. Marcus Thorne investigated why black-capped chickadees significantly expand their hippocampus volume during autumn months. Thorne hypothesized that this seasonal neurogenesis allows chickadees to store and retrieve spatial memory maps for thousands of cached seed caches hidden across woodland territories.",
        "question": "Which finding, if true, would provide the most direct support for Dr. Thorne’s hypothesis?",
        "options": [
            {"key": "A", "text": "Chickadees prevented from caching food in experimental aviaries during autumn failed to exhibit the seasonal increase in hippocampal volume observed in caching birds."},
            {"key": "B", "text": "Non-caching songbird species living in the same forest habitats experienced identical autumn increases in hippocampus volume."},
            {"key": "C", "text": "Chickadees consumed cached seeds within twelve hours of storage rather than retrieving them during winter months."},
            {"key": "D", "text": "Chickadees in captivity preferred sunflower seeds over wild conifer seeds when given free access to both."}
        ],
        "correct": "A",
        "explanation": "If birds that are prevented from caching seeds do NOT show the hippocampus volume increase, it proves that the act and need of caching triggers this brain growth.",
        "strategy_or_hack": "Nazorat guruhi: Ozuqa yashirishdan mahrum qilingan qushlarda miya kattalashmagan bo'lsa, bu gipotezani to'liq isbotlaydi."
    },
    {
        "id": "r_b6_45",
        "domain": "Information and Ideas - Inferences",
        "skill": "Inferences",
        "difficulty": "Medium",
        "passage": "Coral bleaching occurs when marine thermal stress causes corals to expel their symbiotic photosynthetic zooxanthellae algae, leaving behind a stark white calcium carbonate skeleton. While bleached corals can survive for several weeks by feeding on passing plankton, they cannot sustain calcification and tissue growth without the sugars provided by algal photosynthesis. Consequently, if elevated sea temperatures persist for several months, ______",
        "question": "Which choice most logically completes the text?",
        "options": [
            {"key": "A", "text": "prolonged starvation will ultimately cause widespread coral tissue mortality across the reef."},
            {"key": "B", "text": "corals will permanently adapt to synthesize glucose without requiring algal endosymbionts."},
            {"key": "C", "text": "the surrounding water will become saturated with oxygen produced by calcifying skeletons."},
            {"key": "D", "text": "plankton populations will double in density to replace lost algal biomass."}
        ],
        "correct": "A",
        "explanation": "Bleached corals can only survive a few weeks on plankton alone and cannot sustain themselves long-term without algae. If warm water persists for months, they will starve and die.",
        "strategy_or_hack": "Mantiqiy zanjir: Suvo'tsiz bir necha hafta yashay oladi -> Issiqlik oylab davom etsa -> ochlikdan nobud bo'ladi (mortality)."
    },
    {
        "id": "r_b6_46",
        "domain": "Information and Ideas - Command of Evidence (Textual)",
        "skill": "Command of Evidence",
        "difficulty": "Medium",
        "passage": "Archaeologist Dr. Aris Thorne excavated ancient Roman cisterns in southern Spain to determine whether lead pipe plumbing posed a widespread chronic toxicity danger to urban populations. Dr. Thorne hypothesized that thick calcium carbonate mineral scale deposited by hard groundwater lined the inner pipe walls, creating a physical barrier that prevented lead from dissolving into drinking water.",
        "question": "Which piece of evidence, if true, would most strongly substantiate Dr. Thorne’s hypothesis?",
        "options": [
            {"key": "A", "text": "Chemical testing of water remnants in the ancient cisterns revealed lead concentrations well below modern safety thresholds whenever dense calcium encrustations lined the pipes."},
            {"key": "B", "text": "Skeletal remains from wealthy Romans living near the cisterns exhibited severe bone lead accumulation."},
            {"key": "C", "text": "Roman municipal laws mandated the regular cleaning and scraping of sediment from municipal aqueducts."},
            {"key": "D", "text": "Lead pipes in coastal Roman villas corroded rapidly when exposed to acidic marsh water."}
        ],
        "correct": "A",
        "explanation": "Dr. Thorne's hypothesis is that calcium carbonate scale prevented lead from leaching into drinking water. Finding low lead levels in water whenever dense calcium scale lined the pipes directly validates this barrier mechanism.",
        "strategy_or_hack": "Gipoteza tasdig'i: Qalin mineral qatlam (calcium scale) bo'lgan quvurlarda suvda qo'rg'oshin miqdori xavfsiz darajada past bo'lgan."
    },
    {
        "id": "r_b6_47",
        "domain": "Information and Ideas - Inferences",
        "skill": "Inferences",
        "difficulty": "Hard",
        "passage": "In economics, the 'tragedy of the commons' describes how unrestricted access to a shared finite resource inevitably leads individuals acting in rational self-interest to overexploit and deplete the resource. However, Nobel laureate Elinor Ostrom documented hundreds of real-world communal pastures, fisheries, and irrigation systems where user communities successfully maintained resources for centuries without external government regulation or private privatization, provided that local community members established clear boundaries, monitored usage collaboratively, and enforced graduated sanctions against violators. This empirical finding implies that ______",
        "question": "Which choice most logically completes the text?",
        "options": [
            {"key": "A", "text": "resource depletion is not an inevitable outcome of shared ownership when communities implement effective collective self-governance rules."},
            {"key": "B", "text": "centralized government regulation is the only viable method for preventing the collapse of global oceanic fisheries."},
            {"key": "C", "text": "private property rights are fundamentally incompatible with successful natural resource conservation."},
            {"key": "D", "text": "local communities always manage natural resources more destructively than multinational corporations."}
        ],
        "correct": "A",
        "explanation": "Ostrom proved that communities with self-monitoring and clear rules managed resources for centuries without depletion. Thus, depletion is not inevitable if effective collective self-governance exists.",
        "strategy_or_hack": "Ostrom xulosasi: 'Fojia' muqarrar emas (not inevitable); jamoaviy qoidalar bo'lsa umumiy resursni asrab qolish mumkin."
    },
    {
        "id": "r_b6_48",
        "domain": "Information and Ideas - Command of Evidence (Textual)",
        "skill": "Command of Evidence",
        "difficulty": "Medium",
        "passage": "Environmental scientists investigated whether restoring native oyster reefs in estuaries improves coastal water clarity by accelerating suspended sediment filtration. In a three-year study, researchers installed artificial oyster reefs across selected Chesapeake Bay inlets while leaving identical neighboring inlets unrestored as control sites.",
        "question": "Which finding from the study, if true, provides the strongest evidence supporting the scientists' hypothesis?",
        "options": [
            {"key": "A", "text": "Inlets with restored oyster reefs exhibited a 65% increase in water light-penetration depth compared to unrestored control inlets."},
            {"key": "B", "text": "Commercial fishermen caught equal quantities of finfish in both restored and unrestored inlets."},
            {"key": "C", "text": "Oysters on the restored reefs grew at rates comparable to oysters in commercial aquaculture farms."},
            {"key": "D", "text": "Salinity levels in the Chesapeake Bay fluctuated consistently across both rainy and drought seasons."}
        ],
        "correct": "A",
        "explanation": "The hypothesis is that oyster reefs improve water clarity. A 65% increase in light-penetration depth (water clarity) in restored inlets vs control inlets directly proves the effect.",
        "strategy_or_hack": "Gipoteza: suv tiniqlashishi (clarity). Dalil: yorug'lik o'tish chuqurligining 65% ga oshishi (light-penetration depth)."
    },
    {
        "id": "r_b6_49",
        "domain": "Information and Ideas - Inferences",
        "skill": "Inferences",
        "difficulty": "Easy",
        "passage": "In alpine zones, the short summer growing season severely limits the reproductive window for flowering plants. Species that rely exclusively on generalist insect pollinators often fail to set seed during unseasonably cold, windy summers when bumblebee foraging flights are curtailed. In contrast, alpine plants capable of both insect pollination and self-pollination (autogamy) maintain consistent seed production regardless of weather fluctuations. This contrast suggests that autogamy ______",
        "question": "Which choice most logically completes the text?",
        "options": [
            {"key": "A", "text": "serves as a crucial reproductive insurance policy for alpine plants when pollinator activity is suppressed by adverse weather."},
            {"key": "B", "text": "causes alpine plants to produce seeds with lower genetic viability than lowland plant species."},
            {"key": "C", "text": "completely prevents flowering plants from attracting bumblebees during warm summer seasons."},
            {"key": "D", "text": "is an evolutionary disadvantage that accelerates the extinction of high-altitude flora."}
        ],
        "correct": "A",
        "explanation": "When cold weather stops bees from flying, plants that can self-pollinate still produce seeds. Thus, self-pollination acts as 'reproductive insurance' against bad weather.",
        "strategy_or_hack": "Mantiqiy xulosa: O'z-o'zidan changlanish noqulay ob-havoda sug'urta (insurance policy) vazifasini bajaradi."
    },
    {
        "id": "r_b6_50",
        "domain": "Information and Ideas - Command of Evidence (Textual)",
        "skill": "Command of Evidence",
        "difficulty": "Hard",
        "passage": "Neurologists debating the neural mechanisms of bilingualism sought to determine whether proficient bilinguals completely suppress their native language (L1) when speaking in their secondary language (L2). Dr. Zhang hypothesized that lexical representations of both languages remain continuously active simultaneously, requiring active executive inhibition by the prefrontal cortex to prevent cross-language interference.",
        "question": "Which experimental result would provide the strongest evidence in favor of Dr. Zhang's hypothesis?",
        "options": [
            {"key": "A", "text": "Functional MRI brain scans showed elevated prefrontal cortex activity and involuntary micro-activations of L1 vocabulary centers whenever bilinguals named objects in L2."},
            {"key": "B", "text": "Bilingual speakers named objects in L2 just as quickly as monolingual speakers named objects in their native language."},
            {"key": "C", "text": "Bilingual participants made fewer grammatical errors when writing in L1 than when writing in L2."},
            {"key": "D", "text": "Language immersion students learned second-language vocabulary faster when studying in morning classes than in evening classes."}
        ],
        "correct": "A",
        "explanation": "Dr. Zhang's hypothesis claims both languages remain active simultaneously and prefrontal inhibition is required. fMRI scans showing involuntary L1 activations and elevated prefrontal activity during L2 speech directly confirm both parts of the hypothesis.",
        "strategy_or_hack": "Ikki tomonlama isbot: fMRI orqali bir vaqtning o'zida L1 so'zlarining faollashishi va miya boshqaruv markazining zo'riqishi (prefrontal cortex activity)."
    }
]

def build_reading_batch() -> list[dict]:
    batch = []
    for raw in READING_RAW:
        q = {
            "id": raw["id"],
            "version": 1,
            "section": "reading",
            "domain": raw["domain"],
            "skill": raw["skill"],
            "difficulty": raw["difficulty"],
            "passage": raw["passage"],
            "question": raw["question"],
            "options": raw["options"],
            "correct": raw["correct"],
            "explanation": raw["explanation"],
            "strategy_or_hack": raw["strategy_or_hack"],
            "author": "EduTest Pro Original",
            "license": "Proprietary",
            "status": "published"
        }
        batch.append(q)
    return batch


if __name__ == "__main__":
    batch = build_reading_batch()
    print(f"Generated {len(batch)} Reading questions for Batch 7.")
    all_valid = True
    for q in batch:
        ok, errs = validate_question(q)
        if not ok:
            print(f"Validation failed for {q['id']}: {errs}")
            all_valid = False

    if all_valid:
        out_path = os.path.join(BASE_DIR, "data", "batch7_reading.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(batch, f, indent=2, ensure_ascii=False)
        print(f"Successfully verified and saved Batch 7 to {out_path}!")
    else:
        print("Fix validation errors before exporting.")
