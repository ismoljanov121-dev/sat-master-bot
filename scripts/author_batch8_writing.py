"""
EduTest Pro - Batch 8 Writing Authoring & Verification Engine
Generates 50 Digital SAT Writing questions:
- Expression of Ideas: Transitions (15)
- Expression of Ideas: Rhetorical Synthesis (10)
- Standard English Conventions: Boundaries (10)
- Standard English Conventions: Form, Structure, Sense (15)
"""

import json
import os
import sys

BASE_DIR = r"D:\AntigravityWorkspace\projects\sat_ai_bot"
sys.path.insert(0, BASE_DIR)

from services.question_validator import validate_question

WRITING_RAW = [
    # =========================================================================
    # PART 1: TRANSITIONS (15 questions: w_b8_01 to w_b8_15)
    # =========================================================================
    {
        "id": "w_b8_01",
        "domain": "Expression of Ideas - Transitions",
        "skill": "Transitions",
        "difficulty": "Easy",
        "passage": "Early mechanical timepieces were notoriously prone to gaining or losing minutes depending on ambient temperature changes. ______ nineteenth-century horologists developed temperature-compensating balance wheels that maintained regular oscillations even during seasonal extremes.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "Consequently,"},
            {"key": "B", "text": "In contrast,"},
            {"key": "C", "text": "For example,"},
            {"key": "D", "text": "Nevertheless,"}
        ],
        "correct": "A",
        "explanation": "The first sentence establishes a problem (mechanical clocks losing or gaining time due to temperature fluctuations). The second describes the technological solution developed in response. 'Consequently' logically connects the cause/problem to its resulting solution.",
        "strategy_or_hack": "Sabab-oqibat bog'lanishi: Soatlar harorat tufayli adashardi -> Shu sababli (Consequently) haroratni kompensatsiya qiluvchi mexanizm yaratildi."
    },
    {
        "id": "w_b8_02",
        "domain": "Expression of Ideas - Transitions",
        "skill": "Transitions",
        "difficulty": "Easy",
        "passage": "In alpine ecosystems, perennial plants develop compact rosette growth forms to minimize exposure to freezing wind gusts. ______ their dense root structures store carbohydrates essential for rapid flowering during brief summer windows.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "However,"},
            {"key": "B", "text": "Furthermore,"},
            {"key": "C", "text": "Instead,"},
            {"key": "D", "text": "Therefore,"}
        ],
        "correct": "B",
        "explanation": "The first sentence introduces one adaptation (compact rosettes); the second introduces another complementary adaptation (dense root structures). 'Furthermore' correctly marks an additive continuation.",
        "strategy_or_hack": "Qo'shimcha ma'lumot (Addition): Alp o'simliklarining ikki foydali xususiyati birin-ketin keltirilmoqda. 'Furthermore' to'g'ri."
    },
    {
        "id": "w_b8_03",
        "domain": "Expression of Ideas - Transitions",
        "skill": "Transitions",
        "difficulty": "Medium",
        "passage": "Proponents of urban micro-mobility predicted that shared electric scooters would swiftly replace short car journeys in downtown districts. ______ recent municipal transport surveys demonstrate that over sixty percent of scooter trips displace pedestrian walking or public transit journeys rather than automobile travel.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "Similarly,"},
            {"key": "B", "text": "However,"},
            {"key": "C", "text": "Therefore,"},
            {"key": "D", "text": "Indeed,"}
        ],
        "correct": "B",
        "explanation": "The first sentence states an optimistic prediction. The second reveals empirical survey results that contradict that prediction. 'However' establishes the needed contrast.",
        "strategy_or_hack": "Kutilma va amaliyot ziddiyati: Samokatlar avtomobil o'rnini bosadi deb kutilgan, lekin (However) piyodalar o'rnini egalladi."
    },
    {
        "id": "w_b8_04",
        "domain": "Expression of Ideas - Transitions",
        "skill": "Transitions",
        "difficulty": "Medium",
        "passage": "Deep-sea hydrothermal vent organisms cannot rely on solar photons to fuel photosynthesis. ______ chemoautotrophic bacteria synthesize organic nutrients using hydrogen sulfide dissolved in scalding mineral plumes.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "Instead,"},
            {"key": "B", "text": "Likewise,"},
            {"key": "C", "text": "In addition,"},
            {"key": "D", "text": "Consequently,"}
        ],
        "correct": "A",
        "explanation": "The first sentence states what vent organisms cannot do. The second presents the alternative mechanism they actually use. 'Instead' signals an alternative in place of the negated option.",
        "strategy_or_hack": "Inkor va muqobil yechim: 'cannot rely...' keyin nima qilishi aytilganda 'Instead' (uning o'rniga) to'g'ri keladi."
    },
    {
        "id": "w_b8_05",
        "domain": "Expression of Ideas - Transitions",
        "skill": "Transitions",
        "difficulty": "Medium",
        "passage": "Paleontologists long debated whether non-avian theropod dinosaurs possessed physiological mechanisms for metabolic heat generation. ______ multiple recent histological studies of dinosaur bone vascularization indicate rapid growth rates comparable exclusively to modern endothermic vertebrates.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "Today,"},
            {"key": "B", "text": "For example,"},
            {"key": "C", "text": "Otherwise,"},
            {"key": "D", "text": "In other words,"}
        ],
        "correct": "A",
        "explanation": "The sentence shifts chronologically from an ongoing past debate ('long debated') to the current empirical consensus established by recent studies. 'Today,' marks this temporal transition.",
        "strategy_or_hack": "Vaqt zanjiri (Past -> Present): O'tmishdagi uzoq bahslardan hozirgi kun xulosasiga o'tishda 'Today,' qo'llaniladi."
    },
    {
        "id": "w_b8_06",
        "domain": "Expression of Ideas - Transitions",
        "skill": "Transitions",
        "difficulty": "Medium",
        "passage": "Certain bird species exhibit extraordinary cognitive adaptability when foraging in novel environments. New Caledonian crows, ______ fashion hooked twigs into specialized probes to extract beetle larvae concealed within tree cavities.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "for instance,"},
            {"key": "B", "text": "nonetheless,"},
            {"key": "C", "text": "in contrast,"},
            {"key": "D", "text": "hence,"}
        ],
        "correct": "A",
        "explanation": "The first sentence provides a general claim about cognitive adaptability in birds. The second illustrates this claim with a specific species. 'For instance,' marks exemplification.",
        "strategy_or_hack": "Umumiy fikrga misol: Qushlarning moslashuvi aytilgach, Yangi Kaledoniya qarg'asi misol keltirilyapti ('for instance')."
    },
    {
        "id": "w_b8_07",
        "domain": "Expression of Ideas - Transitions",
        "skill": "Transitions",
        "difficulty": "Medium",
        "passage": "In semiconductor fabrication, airborne dust particles smaller than a micrometer can disrupt microchip circuitry and ruin entire silicon wafers. ______ cleanroom facilities maintain positive air pressure and multistage HEPA filtration systems to eliminate airborne particulates.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "Thus,"},
            {"key": "B", "text": "Nevertheless,"},
            {"key": "C", "text": "On the other hand,"},
            {"key": "D", "text": "Similarly,"}
        ],
        "correct": "A",
        "explanation": "The threat of particulate damage directly causes chipmakers to build cleanrooms with positive pressure. 'Thus' signals this cause-and-effect link.",
        "strategy_or_hack": "Natija ko'rsatkichi: Chang chiplarni buzadi, shuning uchun / demak (Thus) toza xonalar quriladi."
    },
    {
        "id": "w_b8_08",
        "domain": "Expression of Ideas - Transitions",
        "skill": "Transitions",
        "difficulty": "Hard",
        "passage": "Renaissance painters frequently added egg yolk to oil pigments to accelerate surface drying and enhance paint elasticity. ______ Flemish masters like Jan van Eyck refined oil glazes without egg emulsions, achieving unprecedented translucent depth through layered walnut-oil varnishes.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "Conversely,"},
            {"key": "B", "text": "Accordingly,"},
            {"key": "C", "text": "Specifically,"},
            {"key": "D", "text": "Furthermore,"}
        ],
        "correct": "A",
        "explanation": "The text contrasts two different historical painting techniques: adding egg yolk vs. avoiding egg emulsions altogether to create pure layered glazes. 'Conversely' introduces this contrasting method.",
        "strategy_or_hack": "Teskari usul (Contrast): Bir guruh rassomlar tuxum sarig'i qo'shgan bo'lsa, Flamand ustalari aksincha (Conversely) sof moy ishlatgan."
    },
    {
        "id": "w_b8_09",
        "domain": "Expression of Ideas - Transitions",
        "skill": "Transitions",
        "difficulty": "Hard",
        "passage": "Quantum computing architectures require superconducting qubits to operate at temperatures hovering mere millikelvins above absolute zero. ______ thermal noise from surrounding electrical wiring can induce quantum decoherence and destroy ongoing computations.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "Otherwise,"},
            {"key": "B", "text": "Even so,"},
            {"key": "C", "text": "In summary,"},
            {"key": "D", "text": "Namely,"}
        ],
        "correct": "A",
        "explanation": "Operating at millikelvin temperatures is mandatory; if this condition is not met, thermal noise causes decoherence. 'Otherwise' expresses the adverse consequence of failing to meet the condition.",
        "strategy_or_hack": "Aks holda (Otherwise): Harorat o'ta past bo'lishi shart, aks holda (Otherwise) issiqlik shovqini hisoblashni yo'q qiladi."
    },
    {
        "id": "w_b8_10",
        "domain": "Expression of Ideas - Transitions",
        "skill": "Transitions",
        "difficulty": "Hard",
        "passage": "Linguistic analysis suggests that Proto-Indo-European vocabulary possessed distinct terms for agricultural implements and pastoral animals. ______ comparative mythologists have identified parallel archetypal deities across Vedic, Celtic, and Norse oral traditions, reinforcing theories of a shared ancestral culture.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "Moreover,"},
            {"key": "B", "text": "Nevertheless,"},
            {"key": "C", "text": "Instead,"},
            {"key": "D", "text": "Conversely,"}
        ],
        "correct": "A",
        "explanation": "Linguistic evidence supports the shared culture theory; mythological evidence independently reinforces it. 'Moreover' marks this additive, corroborating line of evidence.",
        "strategy_or_hack": "Dalil ustiga dalil (Addition): Tilshunoslik dalili yetmagandek, bundan tashqari (Moreover) mifologik dalillar ham bor."
    },
    {
        "id": "w_b8_11",
        "domain": "Expression of Ideas - Transitions",
        "skill": "Transitions",
        "difficulty": "Hard",
        "passage": "The archaeological site at Göbekli Tepe revealed massive megalithic pillars carved with animal reliefs dating to roughly 9500 BCE. Prevailing anthropological models held that monumental architecture could arise only within settled agrarian societies. ______ the discovery at Göbekli Tepe suggested that hunter-gatherer bands organized complex social labor long before agricultural domestication.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "Surprisingly,"},
            {"key": "B", "text": "In other words,"},
            {"key": "C", "text": "Likewise,"},
            {"key": "D", "text": "Specifically,"}
        ],
        "correct": "A",
        "explanation": "The discovery overturned the long-held anthropological dogma that monumental construction required agriculture. 'Surprisingly,' introduces this unexpected, paradigm-shifting finding.",
        "strategy_or_hack": "Kutilmagan burilish: Eskirgan qarashga qarshi kutilmagan haqiqat chiqqanda 'Surprisingly' (Hayratlanarli tomoni) to'g'ri bo'ladi."
    },
    {
        "id": "w_b8_12",
        "domain": "Expression of Ideas - Transitions",
        "skill": "Transitions",
        "difficulty": "Medium",
        "passage": "When atmospheric ozone levels diminish in the stratosphere, increased ultraviolet radiation reaches the ocean surface. Marine phytoplankton, ______ experience cellular DNA degradation and reduced rates of carbon fixation.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "as a result,"},
            {"key": "B", "text": "on the contrary,"},
            {"key": "C", "text": "by contrast,"},
            {"key": "D", "text": "in comparison,"}
        ],
        "correct": "A",
        "explanation": "Higher UV radiation causes DNA degradation in phytoplankton. 'As a result,' correctly specifies the causal effect.",
        "strategy_or_hack": "Sabab-oqibat (as a result): UV radiatsiyasining oshishi oqibatida fitoplanktonlar shikastlanadi."
    },
    {
        "id": "w_b8_13",
        "domain": "Expression of Ideas - Transitions",
        "skill": "Transitions",
        "difficulty": "Hard",
        "passage": "In fluid dynamics, laminar flow describes smooth, parallel fluid layers sliding past one another with negligible mixing. At higher velocities, ______ viscous forces can no longer suppress inertial perturbations, and the stream transitions into chaotic turbulence.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "however,"},
            {"key": "B", "text": "similarly,"},
            {"key": "C", "text": "for example,"},
            {"key": "D", "text": "therefore,"}
        ],
        "correct": "A",
        "explanation": "The passage contrasts orderly laminar flow with chaotic turbulent flow at high velocities. 'However,' establishes the contrast.",
        "strategy_or_hack": "Holat o'zgarishi: Tartibli silliq oqimdan notinch turbulent oqimga o'tishda 'however' (ammo) ziddiyatni bildiradi."
    },
    {
        "id": "w_b8_14",
        "domain": "Expression of Ideas - Transitions",
        "skill": "Transitions",
        "difficulty": "Easy",
        "passage": "Urban heat island mitigation policies often prioritize tree planting programs along residential corridors. Deciduous trees intercept solar radiation during sweltering summer months. ______ their bare winter branches permit warmth from low-angled sunlight to reach homes, lowering heating demands.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "Additionally,"},
            {"key": "B", "text": "Instead,"},
            {"key": "C", "text": "Conversely,"},
            {"key": "D", "text": "Consequently,"}
        ],
        "correct": "A",
        "explanation": "The text lists two distinct benefits: summer cooling and winter passive heating. 'Additionally,' connects the second benefit to the first.",
        "strategy_or_hack": "Foydalarni sanash (Addition): Yozgi soya + Qishki quyosh nuri ('Additionally')."
    },
    {
        "id": "w_b8_15",
        "domain": "Expression of Ideas - Transitions",
        "skill": "Transitions",
        "difficulty": "Hard",
        "passage": "Economists studying auction theory noted that English open-outcry auctions and second-price sealed-bid auctions appear structurally dissimilar to participants. ______ mathematically, both formats generate equivalent revenue expectations when bidders value assets independently.",
        "question": "Which choice completes the text with the most logical transition?",
        "options": [
            {"key": "A", "text": "In practice,"},
            {"key": "B", "text": "Yet,"},
            {"key": "C", "text": "Hence,"},
            {"key": "D", "text": "Namely,"}
        ],
        "correct": "B",
        "explanation": "The auction formats appear completely different, yet mathematically they yield identical revenue. 'Yet,' conveys this counter-intuitive reality.",
        "strategy_or_hack": "Tashqi ko'rinish vs Haqiqat ziddiyati: Shakli turlicha ko'ringani bilan, lekin (Yet,) matematik kutilmasi bir xil."
    },

    # =========================================================================
    # PART 2: RHETORICAL SYNTHESIS (10 questions: w_b8_16 to w_b8_25)
    # =========================================================================
    {
        "id": "w_b8_16",
        "domain": "Expression of Ideas - Rhetorical Synthesis",
        "skill": "Rhetorical Synthesis",
        "difficulty": "Medium",
        "passage": "While researching an exoplanet, a student took the following notes:\n• HD 209458b is a gas giant exoplanet located 159 light-years from Earth.\n• It orbits its parent star at an extremely close distance of just 0.047 AU.\n• In 2001, an international team led by David Charbonneau used transit spectroscopy to analyze starlight filtering through HD 209458b's upper atmosphere.\n• The team detected clear absorption signatures of vaporized atmospheric sodium.\n• This was the first direct chemical detection of an atmosphere on an exoplanet.",
        "question": "The student wants to emphasize the historical significance of Charbonneau's discovery. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
        "options": [
            {"key": "A", "text": "In 2001, David Charbonneau's team detected vaporized sodium on HD 209458b, marking the first direct chemical detection of an atmosphere on an exoplanet."},
            {"key": "B", "text": "Located 159 light-years from Earth, HD 209458b is a gas giant that orbits its parent star at a distance of 0.047 AU."},
            {"key": "C", "text": "David Charbonneau used transit spectroscopy to observe starlight filtering through an exoplanet's atmosphere in 2001."},
            {"key": "D", "text": "Transit spectroscopy allows astronomers to analyze the atmospheres of gas giants orbiting close to their host stars."}
        ],
        "correct": "A",
        "explanation": "Choice A directly addresses the prompt's specific goal (emphasizing the historical significance of the discovery) by noting it was the very first direct chemical detection of an exoplanetary atmosphere.",
        "strategy_or_hack": "Talab qilingan maqsad: 'historical significance of Charbonneau's discovery'. Variant A 'marking the first direct chemical detection' bilan aynan shu maqsadga javob beradi."
    },
    {
        "id": "w_b8_17",
        "domain": "Expression of Ideas - Rhetorical Synthesis",
        "skill": "Rhetorical Synthesis",
        "difficulty": "Hard",
        "passage": "While researching bioarchaeological methods, a student took the following notes:\n• Strontium isotope analysis helps archaeologists trace ancient human and animal migration.\n• Strontium ratios in local bedrock and groundwater are absorbed into local crops and vegetation.\n• When humans consume regional food and water, the local strontium isotope signature is permanently incorporated into their tooth enamel during childhood.\n• Adult bone tissue remodels continuously, reflecting strontium ingested in recent decades.\n• By comparing enamel ratios to bone ratios, researchers can determine whether an individual moved from their birthplace.",
        "question": "The student wants to explain how strontium isotope analysis determines whether an individual migrated during their lifetime. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
        "options": [
            {"key": "A", "text": "Because tooth enamel preserves childhood strontium signatures while bone tissue reflects recent decades, comparing the two reveals whether an individual moved from their birthplace."},
            {"key": "B", "text": "Strontium isotope analysis is an innovative bioarchaeological method used to trace ancient human and animal migrations across different regions."},
            {"key": "C", "text": "Local strontium signatures from bedrock and groundwater are absorbed by plants and subsequently ingested by ancient humans."},
            {"key": "D", "text": "Adult bone tissue continually remodels over time, incorporating strontium from local crops consumed in recent decades."}
        ],
        "correct": "A",
        "explanation": "Choice A explicitly explains the comparative mechanism (tooth enamel for childhood vs. bone tissue for adulthood) to show how migration during a lifetime is determined.",
        "strategy_or_hack": "Maqsadni qidiring: 'explain how ... determines whether an individual migrated'. Variant A enamel (bolalik) va suyak (yaqin davr) taqqoslashini tushuntirib beradi."
    },
    {
        "id": "w_b8_18",
        "domain": "Expression of Ideas - Rhetorical Synthesis",
        "skill": "Rhetorical Synthesis",
        "difficulty": "Medium",
        "passage": "While researching medieval West African commerce, a student took the following notes:\n• Trans-Saharan trade routes flourished between the eighth and sixteenth centuries.\n• Historian E.W. Bovill argued that salt from northern salt pans was the primary commodity driving the southern merchant caravans.\n• Later economic historians, including Nehemia Levtzion, argued that gold from the Wangara goldfields was the true foundational stimulus for the entire desert commercial network.\n• Both historians agreed that camel caravan logistics transformed desert transit.",
        "question": "The student wants to contrast the historical interpretations of Bovill and Levtzion. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
        "options": [
            {"key": "A", "text": "While Bovill maintained that northern salt drove trans-Saharan commerce, Levtzion argued that southern gold was the true foundational stimulus."},
            {"key": "B", "text": "Trans-Saharan trade networks flourished between the eighth and sixteenth centuries due to camel caravan innovations."},
            {"key": "C", "text": "Both Bovill and Levtzion agreed that camel caravans transformed trans-Saharan commercial routes across the desert."},
            {"key": "D", "text": "Historians have long examined medieval West African commerce and the valuable commodities exchanged between northern and southern regions."}
        ],
        "correct": "A",
        "explanation": "The prompt asks to contrast the interpretations of the two historians. Choice A contrasts Bovill's view (salt) with Levtzion's view (gold).",
        "strategy_or_hack": "Maqsad: 'contrast the historical interpretations'. Variant A 'While Bovill... Levtzion argued...' orqali ikkala qarashni taqqoslaydi."
    },
    {
        "id": "w_b8_19",
        "domain": "Expression of Ideas - Rhetorical Synthesis",
        "skill": "Rhetorical Synthesis",
        "difficulty": "Medium",
        "passage": "While researching Nobel laureates in chemistry, a student took the following notes:\n• The ribosome is a complex cellular machine that translates genetic code into proteins.\n• For decades, scientists believed the ribosome was too large and flexible to be crystallized for X-ray diffraction.\n• In 1980, Israeli crystallographer Ada Yonath developed pioneering cryogenic cooling techniques that stabilized ribosomal crystals.\n• Yonath's breakthrough enabled high-resolution three-dimensional imaging of the ribosome.\n• In 2009, Yonath was awarded the Nobel Prize in Chemistry alongside Venkatraman Ramakrishnan and Thomas A. Steitz.",
        "question": "The student wants to emphasize Ada Yonath's specific technical breakthrough. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
        "options": [
            {"key": "A", "text": "Overcoming decades of skepticism, Ada Yonath developed pioneering cryogenic cooling techniques that stabilized ribosomal crystals for high-resolution imaging."},
            {"key": "B", "text": "In 2009, Ada Yonath received the Nobel Prize in Chemistry alongside Venkatraman Ramakrishnan and Thomas A. Steitz."},
            {"key": "C", "text": "The ribosome is a vital cellular structure responsible for synthesizing proteins from genetic messenger RNA."},
            {"key": "D", "text": "Before 1980, scientists considered the ribosome too large and unstable to analyze with X-ray diffraction methods."}
        ],
        "correct": "A",
        "explanation": "Choice A highlights Yonath's specific technical breakthrough (cryogenic cooling techniques that stabilized ribosomal crystals for imaging).",
        "strategy_or_hack": "Maqsad: 'emphasize Ada Yonath's specific technical breakthrough'. Variant A aynan texnik ixtironi (kriogenik sovutish) ko'rsatadi."
    },
    {
        "id": "w_b8_20",
        "domain": "Expression of Ideas - Rhetorical Synthesis",
        "skill": "Rhetorical Synthesis",
        "difficulty": "Hard",
        "passage": "While researching amphibian ecology, a student took the following notes:\n• Plethodontid salamanders lack lungs and respire entirely through their moist skin.\n• The Appalachian Mountains are home to over 70 distinct species of plethodontids, representing the world's highest diversity for this family.\n• Many species, such as the Shenandoah salamander, are confined to isolated, high-altitude talus slopes on single mountain peaks.\n• These isolated mountaintop populations are highly vulnerable to temperature increases and declining moisture driven by regional warming.",
        "question": "The student wants to present the diversity and ecological vulnerability of Appalachian plethodontid salamanders to an audience of conservation biologists. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
        "options": [
            {"key": "A", "text": "Although the Appalachian Mountains harbor the world's greatest plethodontid diversity, many species are confined to isolated mountain peaks where warming and drying threaten their skin-based respiration."},
            {"key": "B", "text": "Plethodontid salamanders do not have lungs, meaning they must keep their skin moist at all times to absorb atmospheric oxygen."},
            {"key": "C", "text": "The Shenandoah salamander is one of more than 70 plethodontid species that can be observed throughout the Appalachian mountain range."},
            {"key": "D", "text": "High-altitude talus slopes in the Appalachian Mountains provide moist microhabitats essential for lungless salamanders."}
        ],
        "correct": "A",
        "explanation": "Choice A synthesizes both required elements: diversity (world's greatest diversity, >70 species) and ecological vulnerability (confined to isolated peaks threatened by warming/drying).",
        "strategy_or_hack": "Ikkita talab: 'diversity' VA 'ecological vulnerability'. Faqat A variant har ikkala omilni o'zida birlashtirgan."
    },
    {
        "id": "w_b8_21",
        "domain": "Expression of Ideas - Rhetorical Synthesis",
        "skill": "Rhetorical Synthesis",
        "difficulty": "Easy",
        "passage": "While researching NASA materials engineering, a student took the following notes:\n• Aerogels are ultralight synthetic porous materials composed of 99.8% air by volume.\n• In 1999, NASA launched the Stardust spacecraft to collect samples from Comet Wild 2.\n• Cometary dust particles travel at hypervelocity speeds exceeding 6 kilometers per second.\n• Traditional collection surfaces would pulverize or vaporize incoming dust grains upon impact.\n• Stardust's silica aerogel collector safely slowed and captured the hypervelocity grains without altering their chemical composition.",
        "question": "The student wants to explain why silica aerogel was essential to the Stardust mission. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
        "options": [
            {"key": "A", "text": "Silica aerogel was essential to the Stardust mission because it decelerated cometary dust traveling at hypervelocity speeds without destroying or altering the grains."},
            {"key": "B", "text": "Composed of 99.8% air, aerogels are ultralight materials used in diverse aerospace and industrial engineering applications."},
            {"key": "C", "text": "NASA launched the Stardust spacecraft in 1999 to encounter Comet Wild 2 and analyze interplanetary materials."},
            {"key": "D", "text": "Cometary dust grains travel through space at speeds exceeding 6 kilometers per second, presenting major engineering hurdles."}
        ],
        "correct": "A",
        "explanation": "Choice A directly explains why aerogel was essential: it safely slowed cometary grains without altering them, whereas traditional surfaces would pulverize them.",
        "strategy_or_hack": "Maqsad: 'explain why silica aerogel was essential to the Stardust mission'. Variant A 'because it decelerated cometary dust... without destroying' sababini to'liq beradi."
    },
    {
        "id": "w_b8_22",
        "domain": "Expression of Ideas - Rhetorical Synthesis",
        "skill": "Rhetorical Synthesis",
        "difficulty": "Easy",
        "passage": "While researching contemporary American sculpture, a student took the following notes:\n• Dale Chihuly is an American artist born in 1941 in Tacoma, Washington.\n• He introduced large-scale blown glass sculpture into fine art museum collections.\n• Chihuly utilizes an ensemble approach, directing teams of master glassblowers to craft complex organic forms.\n• His monumental installation 'The Sun' features over 1,300 blown-glass elements in vibrant red, orange, and yellow hues.\n• His installations are celebrated for their dynamic interplay with natural light.",
        "question": "The student wants to introduce Dale Chihuly and his artistic medium to a museum visitor guide. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
        "options": [
            {"key": "A", "text": "American artist Dale Chihuly is renowned for transforming large-scale blown glass into vibrant, light-filled fine art sculptures."},
            {"key": "B", "text": "Born in Tacoma, Washington, Dale Chihuly works with a team of glassblowers to assemble installations containing over 1,000 pieces."},
            {"key": "C", "text": "The monumental sculpture 'The Sun' incorporates over 1,300 glass parts rendered in dynamic warm colors."},
            {"key": "D", "text": "Museum visitors often admire how glass installations interact with changing angles of natural daylight."}
        ],
        "correct": "A",
        "explanation": "Choice A effectively introduces the artist (Dale Chihuly) and defines his distinctive artistic medium (large-scale blown glass fine art).",
        "strategy_or_hack": "Maqsad: 'introduce Dale Chihuly and his artistic medium'. Variant A rassomni tanishtirib, uning asosi bo'lgan puflama shisha (blown glass) vositasini ko'rsatadi."
    },
    {
        "id": "w_b8_23",
        "domain": "Expression of Ideas - Rhetorical Synthesis",
        "skill": "Rhetorical Synthesis",
        "difficulty": "Hard",
        "passage": "While researching the Cambrian fossil record, a student took the following notes:\n• The Burgess Shale in Canada preserves exquisite fossils from the Cambrian explosion (approx. 508 million years ago).\n• Rapid sediment burial in anoxic underwater conditions allowed preservation of soft tissues such as eyes, gills, and digestive tracts.\n• Soft-bodied organisms like Marrella and Opabinia constitute the vast majority of preserved specimens at the site.\n• Most other Cambrian fossil sites preserve only mineralized hard shells and exoskeletons.\n• Paleontologists caution that the Burgess Shale represents a unique depositional environment rather than a typical global Cambrian ecosystem.",
        "question": "The student wants to acknowledge a limitation of using the Burgess Shale to generalize about global Cambrian life. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
        "options": [
            {"key": "A", "text": "Because the Burgess Shale reflects exceptional anoxic preservation conditions, scientists caution that its diverse community may not represent typical global ecosystems of the Cambrian period."},
            {"key": "B", "text": "The Burgess Shale is famous for preserving delicate soft tissues, such as the gills and eyes of Cambrian organisms like Marrella."},
            {"key": "C", "text": "Unlike most Cambrian fossil deposits that only preserve mineralized shells, the Burgess Shale captures soft-bodied creatures."},
            {"key": "D", "text": "Sediments that buried ancient marine animals 508 million years ago were deficient in dissolved oxygen."}
        ],
        "correct": "A",
        "explanation": "Choice A directly presents the scientific limitation: the exceptional preservation at Burgess Shale cannot be assumed to represent typical worldwide ecosystems.",
        "strategy_or_hack": "Maqsad: 'acknowledge a limitation ... to generalize'. Variant A 'scientists caution that its diverse community may not represent typical global ecosystems' orqali cheklovni keltiradi."
    },
    {
        "id": "w_b8_24",
        "domain": "Expression of Ideas - Rhetorical Synthesis",
        "skill": "Rhetorical Synthesis",
        "difficulty": "Medium",
        "passage": "While researching the theory of plate tectonics, a student took the following notes:\n• In 1912, Alfred Wegener proposed the continental drift hypothesis based on fossil and coastline matches.\n• Wegener could not identify a convincing geophysical mechanism capable of moving continents.\n• In 1963, Fred Vine and Drummond Matthews analyzed alternating magnetic stripes on the ocean floor.\n• The magnetic stripes confirmed seafloor spreading at mid-ocean ridges.\n• Vine and Matthews's discovery provided the definitive physical mechanism that validated Wegener's early proposal.",
        "question": "The student wants to emphasize the chronological connection between Wegener's hypothesis and Vine and Matthews's discovery. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
        "options": [
            {"re_key": "A", "key": "A", "text": "Decades after Alfred Wegener proposed continental drift in 1912 without a driving mechanism, Fred Vine and Drummond Matthews's 1963 magnetic stripe discovery finally confirmed the process."},
            {"re_key": "B", "key": "B", "text": "In 1963, Vine and Matthews analyzed alternating magnetic stripes across mid-ocean ridges to verify seafloor spreading."},
            {"re_key": "C", "key": "C", "text": "Alfred Wegener used fossil distributions and matching continental coastlines to propose continental drift in 1912."},
            {"re_key": "D", "key": "D", "text": "Mid-ocean ridges produce symmetrical bands of alternating magnetic polarity as fresh magma solidifies."}
        ],
        "correct": "A",
        "explanation": "Choice A unites both discoveries chronologically, showing how the 1963 discovery confirmed the 1912 hypothesis.",
        "strategy_or_hack": "Maqsad: 'chronological connection between Wegener ... and Vine and Matthews'. Variant A 'Decades after 1912 ... 1963 discovery confirmed' orqali vaqt ketma-ketligini bog'laydi."
    },
    {
        "id": "w_b8_25",
        "domain": "Expression of Ideas - Rhetorical Synthesis",
        "skill": "Rhetorical Synthesis",
        "difficulty": "Hard",
        "passage": "While researching urban heat management, a student took the following notes:\n• In 2018, Baltimore community organizations launched an urban canopy initiative in historically disinvested neighborhoods.\n• Neighborhoods with low tree canopy historically experienced surface temperatures up to 8°C hotter than wealthier, shaded districts.\n• Over three years, volunteers and city workers planted 4,500 shade trees across five target neighborhoods.\n• Follow-up satellite thermal imaging in 2022 documented an average summer surface temperature reduction of 2.1°C in the reforested zones.\n• The initiative also improved local air quality and increased neighborhood foot traffic.",
        "question": "The student wants to present evidence that the 2018 urban canopy initiative successfully reduced heat in target neighborhoods. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
        "options": [
            {"key": "A", "text": "After volunteers planted 4,500 shade trees in target Baltimore neighborhoods, satellite imaging confirmed an average summer surface temperature drop of 2.1°C by 2022."},
            {"key": "B", "text": "Historically disinvested Baltimore neighborhoods suffered from extreme heat differences of up to 8°C compared to shaded areas."},
            {"key": "C", "text": "In 2018, community organizers in Baltimore launched a tree-planting program to improve public health and increase foot traffic."},
            {"key": "D", "text": "Satellite thermal imaging is a valuable remote sensing technique used by city planners to measure urban surface temperatures."}
        ],
        "correct": "A",
        "explanation": "Choice A presents the quantitative before-and-after evidence demonstrating that planting 4,500 trees lowered summer temperatures by 2.1°C.",
        "strategy_or_hack": "Maqsad: 'present evidence that the initiative successfully reduced heat'. Variant A 'planted 4,500 trees ... confirmed average temperature drop of 2.1°C' aniq dalilini keltiradi."
    },

    # =========================================================================
    # PART 3: BOUNDARIES (10 questions: w_b8_26 to w_b8_35)
    # =========================================================================
    {
        "id": "w_b8_26",
        "domain": "Standard English Conventions - Boundaries",
        "skill": "Boundaries",
        "difficulty": "Easy",
        "passage": "Deep ocean trenches are among the most inhospitable habitats on ______ intense hydrostatic pressure and total darkness require specialized biochemical adaptations in endemic fauna.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "Earth, where"},
            {"key": "B", "text": "Earth; where"},
            {"key": "C", "text": "Earth, however"},
            {"key": "D", "text": "Earth"}
        ],
        "correct": "A",
        "explanation": "'Earth, where' uses a comma and the relative adverb 'where' to smoothly attach the dependent clause describing conditions in the trenches without creating a run-on or semicolon error.",
        "strategy_or_hack": "Grammatik chegara: Asosiy gapdan keyin izohlovchi ergash gap kelganda vergul + 'where' to'g'ri bog'laydi."
    },
    {
        "id": "w_b8_27",
        "domain": "Standard English Conventions - Boundaries",
        "skill": "Boundaries",
        "difficulty": "Medium",
        "passage": "Linguists studying morphological typology classify languages according to how words are ______ analytic languages rely on word order, whereas synthetic languages combine multiple morphemes into single lexical items.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "structured:"},
            {"key": "B", "text": "structured,"},
            {"key": "C", "text": "structured and"},
            {"key": "D", "text": "structured"}
        ],
        "correct": "A",
        "explanation": "A colon is the correct punctuation mark following a complete independent clause when introducing an elaboration or explanation of that clause.",
        "strategy_or_hack": "Ikki nuqta (Colon) qoidasi: To'liq gapdan keyin unga batafsil tushuntirish yoki misol berilganda ':' qo'yiladi."
    },
    {
        "id": "w_b8_28",
        "domain": "Standard English Conventions - Boundaries",
        "skill": "Boundaries",
        "difficulty": "Medium",
        "passage": "In 1919, architect Walter Gropius founded the Bauhaus ______ an avant-garde design school that sought to bridge the historical divide between fine art and industrial craft.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "School—"},
            {"key": "B", "text": "School,"},
            {"key": "C", "text": "School;"},
            {"key": "D", "text": "School"}
        ],
        "correct": "B",
        "explanation": "A comma correctly sets off the nonessential appositive phrase ('an avant-garde design school...') modifying Bauhaus School.",
        "strategy_or_hack": "Ajratilgan izoh (Appositive): 'the Bauhaus School, an avant-garde design school...' - otni izohlovchi ibora oldidan vergul tushadi."
    },
    {
        "id": "w_b8_29",
        "domain": "Standard English Conventions - Boundaries",
        "skill": "Boundaries",
        "difficulty": "Easy",
        "passage": "Carnivorous pitcher plants thrive in nutrient-deficient peat bogs by trapping insects, ______ their roots absorb essential nitrogen and phosphorus from digested prey.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "and"},
            {"key": "B", "text": "so"},
            {"key": "C", "text": "but"},
            {"key": "D", "text": "whereas"}
        ],
        "correct": "A",
        "explanation": "The sentence already includes a comma before the blank. Joining two independent clauses requires a coordinating conjunction (FANBOYS); 'and' correctly conveys the cumulative relationship.",
        "strategy_or_hack": "FANBOYS qoidasi: Verguldan keyin 'and' kelishi orqali ikkita mustaqil gap (independent clauses) to'g'ri birikadi."
    },
    {
        "id": "w_b8_30",
        "domain": "Standard English Conventions - Boundaries",
        "skill": "Boundaries",
        "difficulty": "Hard",
        "passage": "The civil rights organizer Septima Poinsette Clark established Citizenship Schools across the American South ______ taught adult literacy and voting rights to thousands of Black citizens.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "that"},
            {"key": "B", "text": ", that"},
            {"key": "C", "text": ", which they"},
            {"key": "D", "text": "where it"}
        ],
        "correct": "A",
        "explanation": "'That' introduces an essential (restrictive) relative clause specifying which Citizenship Schools are meant, and essential clauses are never preceded by a comma.",
        "strategy_or_hack": "Restrictive clause (that): 'Citizenship Schools that taught...' iborasida 'that' oldidan hech qachon vergul qo'yilmaydi."
    },
    {
        "id": "w_b8_31",
        "domain": "Standard English Conventions - Boundaries",
        "skill": "Boundaries",
        "difficulty": "Hard",
        "passage": "Neuroscientists once believed that the adult mammalian brain could not generate new ______ numerous recent studies demonstrate adult neurogenesis in the subgranular zone of the hippocampus.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "neurons; however,"},
            {"key": "B", "text": "neurons, however,"},
            {"key": "C", "text": "neurons however"},
            {"key": "D", "text": "neurons; however"}
        ],
        "correct": "A",
        "explanation": "Joining two independent clauses with a conjunctive adverb requires a semicolon before the conjunctive adverb and a comma immediately after ('neurons; however,').",
        "strategy_or_hack": "Semicolon + Conjunctive Adverb: Ikkita mustaqil gapni bog'lashda '; however,' formulasi qat'iy qo'llaniladi (vergul qo'yilsa comma splice bo'ladi)."
    },
    {
        "id": "w_b8_32",
        "domain": "Standard English Conventions - Boundaries",
        "skill": "Boundaries",
        "difficulty": "Medium",
        "passage": "Atmospheric physicists examining volcanic eruption plumes observed a rare electrostatic phenomenon ______ lightning discharges generated entirely within towering clouds of silicate ash.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": ": volcanic"},
            {"key": "B", "text": "; volcanic"},
            {"key": "C", "text": ", and volcanic"},
            {"key": "D", "text": "volcanic"}
        ],
        "correct": "A",
        "explanation": "A colon is used after an independent clause to introduce an explanation, appositive, or clarification of the noun phrase 'a rare electrostatic phenomenon'.",
        "strategy_or_hack": "Izohlovchi ikki nuqta: 'a rare electrostatic phenomenon: volcanic lightning discharges...' - hodisaning aniq nomi va izohi keltirilmoqda."
    },
    {
        "id": "w_b8_33",
        "domain": "Standard English Conventions - Boundaries",
        "skill": "Boundaries",
        "difficulty": "Easy",
        "passage": "Marine cyanobacteria produce substantial quantities of oxygen through ______ they are among the most abundant photosynthetic organisms on Earth.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "photosynthesis, so"},
            {"key": "B", "text": "photosynthesis, and"},
            {"key": "C", "text": "photosynthesis; so"},
            {"key": "D", "text": "photosynthesis so"}
        ],
        "correct": "B",
        "explanation": "Comma followed by the coordinating conjunction 'and' correctly joins the two independent clauses. Choice A changes the logic improperly (producing oxygen is not the reason they are abundant).",
        "strategy_or_hack": "Bog'lovchi tanlash: Ikkita mustaqil fikrni qo'shimcha tarzda bog'lashda ', and' eng to'g'ri grammatik chegara."
    },
    {
        "id": "w_b8_34",
        "domain": "Standard English Conventions - Boundaries",
        "skill": "Boundaries",
        "difficulty": "Medium",
        "passage": "Renowned for their intricate basketry, weavers of the Pomo ______ sedge root, willow shoots, and redbud bark to craft watertight vessels with geometric motifs.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "nation harvested"},
            {"key": "B", "text": "nation, harvested"},
            {"key": "C", "text": "nation; harvested"},
            {"key": "D", "text": "nation, having harvested"}
        ],
        "correct": "A",
        "explanation": "The subject is 'weavers of the Pomo nation' and the main verb is 'harvested'. No comma should separate the subject noun phrase from its verb.",
        "strategy_or_hack": "Ega va kesim o'rtasiga vergul qo'yilmaydi: 'weavers of the Pomo nation harvested' - orasiga noo'rin tinish belgisi kiritilmaydi."
    },
    {
        "id": "w_b8_35",
        "domain": "Standard English Conventions - Boundaries",
        "skill": "Boundaries",
        "difficulty": "Hard",
        "passage": "During the Harlem Renaissance, author Zora Neale Hurston collected African American folklore in rural ______ she documented work songs, sermons, and oral tales with unmatched anthropological rigor.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "Florida; there,"},
            {"key": "B", "text": "Florida, there"},
            {"key": "C", "text": "Florida there,"},
            {"key": "D", "text": "Florida, where"}
        ],
        "correct": "A",
        "explanation": "Choice A uses a semicolon to separate two complete independent clauses, followed by the transitional adverb 'there' and a comma, preventing a comma splice.",
        "strategy_or_hack": "Comma splice oldini olish: 'Florida, there she documented...' xato (comma splice). Nuqtali vergul bilan ajratilgan 'Florida; there,' to'g'ri."
    },

    # =========================================================================
    # PART 4: FORM, STRUCTURE, AND SENSE (15 questions: w_b8_36 to w_b8_50)
    # =========================================================================
    {
        "id": "w_b8_36",
        "domain": "Standard English Conventions - Form, Structure, and Sense",
        "skill": "Form, Structure, and Sense",
        "difficulty": "Easy",
        "passage": "The rapid proliferation of microscopic plastic fragments in global freshwater systems ______ a severe ecotoxicological hazard for benthic macroinvertebrates.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "poses"},
            {"key": "B", "text": "pose"},
            {"key": "C", "text": "have posed"},
            {"key": "D", "text": "are posing"}
        ],
        "correct": "A",
        "explanation": "The grammatical subject is the singular noun 'proliferation' (not the plural 'fragments' or 'systems'). A singular subject requires the singular verb 'poses'.",
        "strategy_or_hack": "Ega-kesim moslashuvi: Ega - 'proliferation' (birlik). Oraliqdagi 'of microscopic plastic fragments' chalg'ituvchi bo'lib, kesim 'poses' birlikda bo'lishi shart."
    },
    {
        "id": "w_b8_37",
        "domain": "Standard English Conventions - Form, Structure, and Sense",
        "skill": "Form, Structure, and Sense",
        "difficulty": "Medium",
        "passage": "Concealed beneath Antarctica's thick ice sheet ______ hundreds of interconnected subglacial lakes that harbor microbial ecosystems isolated for millennia.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "lies"},
            {"key": "B", "text": "lie"},
            {"key": "C", "text": "is lying"},
            {"key": "D", "text": "has lain"}
        ],
        "correct": "B",
        "explanation": "This sentence uses inverted syntax: the subject follows the verb. The true subject is the plural noun phrase 'hundreds of interconnected subglacial lakes', requiring the plural verb 'lie'.",
        "strategy_or_hack": "Inversiya (Inverted order): Gap o'rni almashgan: 'Beneath the ice lie hundreds of lakes'. Ega 'lakes' (ko'plikda), demak kesim 'lie' bo'ladi."
    },
    {
        "id": "w_b8_38",
        "domain": "Standard English Conventions - Form, Structure, and Sense",
        "skill": "Form, Structure, and Sense",
        "difficulty": "Easy",
        "passage": "In 1928, Scottish bacteriologist Alexander Fleming ______ that an accidental penicillium mold contaminant in a petri dish inhibited the growth of staphylococcal bacteria.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "observed"},
            {"key": "B", "text": "observes"},
            {"key": "C", "text": "has observed"},
            {"key": "D", "text": "is observing"}
        ],
        "correct": "A",
        "explanation": "The specific past-time indicator 'In 1928' requires simple past tense ('observed').",
        "strategy_or_hack": "Aniq o'tgan zamon belgisi: 'In 1928' ko'rsatilgani uchun fe'l faqat Simple Past ('observed') bo'lishi lozim."
    },
    {
        "id": "w_b8_39",
        "domain": "Standard English Conventions - Form, Structure, and Sense",
        "skill": "Form, Structure, and Sense",
        "difficulty": "Medium",
        "passage": "When specialized plasma cells detect circulating antigens, they immediately ______ antibody proteins designed to neutralize the invasive pathogen.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "synthesize"},
            {"key": "B", "text": "synthesized"},
            {"key": "C", "text": "are synthesizing"},
            {"key": "D", "text": "had synthesized"}
        ],
        "correct": "A",
        "explanation": "The dependent clause uses present tense ('detect') to describe a general biological process; the main clause must maintain consistent present tense ('synthesize') to agree with plural 'they'.",
        "strategy_or_hack": "Zamonlar muvofiqligi (General factual present): 'When cells detect..., they synthesize...' umumiy ilmiy haqiqat hozirgi zamonda bo'ladi."
    },
    {
        "id": "w_b8_40",
        "domain": "Standard English Conventions - Form, Structure, and Sense",
        "skill": "Form, Structure, and Sense",
        "difficulty": "Hard",
        "passage": "Analyzing the geochemical composition of ancient lake sediments, ______ anomalous concentrations of iridium consistent with a major meteoritic impact.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "geologists discovered"},
            {"key": "B", "text": "the discovery was made by geologists of"},
            {"key": "C", "text": "anomalous levels were detected, showing"},
            {"key": "D", "text": "the sediments yielded"}
        ],
        "correct": "A",
        "explanation": "The introductory participial phrase 'Analyzing...' must modify the logical agent performing the analysis. Sediments or discoveries cannot analyze sediments; only 'geologists' can.",
        "strategy_or_hack": "Dangling modifier tuzog'i: 'Analyzing...' harakatini faqat geologlar bajara oladi, shuning uchun verguldan keyin 'geologists' kelishi shart."
    },
    {
        "id": "w_b8_41",
        "domain": "Standard English Conventions - Form, Structure, and Sense",
        "skill": "Form, Structure, and Sense",
        "difficulty": "Hard",
        "passage": "Originally constructed to defend against naval incursions, ______ now houses a celebrated maritime history museum visited by thousands of tourists annually.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "the coastal stone fortress"},
            {"key": "B", "text": "tourists can visit the fortress, which"},
            {"key": "C", "text": "naval officers designed the fortress that"},
            {"key": "D", "text": "the city's historic preservation board"}
        ],
        "correct": "A",
        "explanation": "The introductory modifier 'Originally constructed...' must logically describe the subject that follows the comma. Only 'the coastal stone fortress' was constructed to defend against incursions.",
        "strategy_or_hack": "Modifier mosligi: 'Originally constructed...' faqat qal'aga ('fortress') tegishli bo'lishi mumkin, odamlar yoki kengashga emas."
    },
    {
        "id": "w_b8_42",
        "domain": "Standard English Conventions - Form, Structure, and Sense",
        "skill": "Form, Structure, and Sense",
        "difficulty": "Medium",
        "passage": "After conducting rigorous clinical trials across multiple testing facilities, the biomedical research team announced that ______ had formulated a stable synthetic vaccine.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "it"},
            {"key": "B", "text": "they"},
            {"key": "C", "text": "one"},
            {"key": "D", "text": "he"}
        ],
        "correct": "A",
        "explanation": "'The biomedical research team' is a singular collective noun acting as a single entity, requiring the singular pronoun 'it'.",
        "strategy_or_hack": "Kollektiv ot va olmosh: 'team' birlikdagi bitta guruh sifatida qaralganda 'it' olmoshi talab etiladi."
    },
    {
        "id": "w_b8_43",
        "domain": "Standard English Conventions - Form, Structure, and Sense",
        "skill": "Form, Structure, and Sense",
        "difficulty": "Hard",
        "passage": "Environmental regulators issued citations to industrial plant operators ______ had repeatedly discharged untreated wastewater into municipal drainage canals.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "who"},
            {"key": "B", "text": "whom"},
            {"key": "C", "text": "which"},
            {"key": "D", "text": "whose"}
        ],
        "correct": "A",
        "explanation": "'Who' serves as the subject pronoun of the relative clause ('who had repeatedly discharged...'). 'Whom' is objective and cannot function as the subject.",
        "strategy_or_hack": "Who vs Whom: Nisbiy gapning egasi sifatida ('who had discharged...') faqat 'who' ishlatiladi ('whom' to'ldiruvchi o'rnida keladi)."
    },
    {
        "id": "w_b8_44",
        "domain": "Standard English Conventions - Form, Structure, and Sense",
        "skill": "Form, Structure, and Sense",
        "difficulty": "Easy",
        "passage": "To survive harsh winters in the subarctic tundra, willow ptarmigans molt into white plumage, burrow beneath snowpacks for insulation, and ______ their diet to nutrient-poor woody twigs.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "restrict"},
            {"key": "B", "text": "restricting"},
            {"key": "C", "text": "restricted"},
            {"key": "D", "text": "to restrict"}
        ],
        "correct": "A",
        "explanation": "The sentence presents a parallel series of base-form verbs: 'molt...', 'burrow...', and 'restrict...'.",
        "strategy_or_hack": "Parallel struktura: 'molt...', 'burrow...', and 'restrict...' - barcha fe'llar bir xil boshlang'ich zamonda bo'lishi shart."
    },
    {
        "id": "w_b8_45",
        "domain": "Standard English Conventions - Form, Structure, and Sense",
        "skill": "Form, Structure, and Sense",
        "difficulty": "Medium",
        "passage": "The innovative acoustic hall was designed not only to amplify subtle violin harmonics ______ background HVAC vibrations from neighboring subway tunnels.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "but also to dampen"},
            {"key": "B", "text": "and dampening"},
            {"key": "C", "text": "but also dampens"},
            {"key": "D", "text": "as well as dampening"}
        ],
        "correct": "A",
        "explanation": "Correlative conjunctions require parallel structures: 'not only to amplify... but also to dampen...'.",
        "strategy_or_hack": "Correlative Conjunctions: 'not only [to infinitive] ... but also [to infinitive]' juftligi parallel grammatik shaklni talab qiladi."
    },
    {
        "id": "w_b8_46",
        "domain": "Standard English Conventions - Form, Structure, and Sense",
        "skill": "Form, Structure, and Sense",
        "difficulty": "Hard",
        "passage": "Agronomists found that the root tensile strength of drought-tolerant sorghum hybrids was significantly greater than ______ conventional corn varieties under water stress.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "that of"},
            {"key": "B", "text": "those of"},
            {"key": "C", "text": "the roots of"},
            {"key": "D", "text": "compared to"}
        ],
        "correct": "A",
        "explanation": "The comparison is between the 'tensile strength' (singular) of sorghum and the 'tensile strength' of corn varieties. The singular demonstrative pronoun 'that of' correctly maintains logical comparison.",
        "strategy_or_hack": "Mantiqiy taqqoslash (Logical Comparison): 'tensile strength' (birlik) bilan taqqoslashda 'that of' ishlatiladi ('those of' ko'plikka ketadi)."
    },
    {
        "id": "w_b8_47",
        "domain": "Standard English Conventions - Form, Structure, and Sense",
        "skill": "Form, Structure, and Sense",
        "difficulty": "Easy",
        "passage": "Cognitive psychologists noted that participants' reaction times in spatial recognition trials were remarkably consistent ______ previous theoretical projections.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "with"},
            {"key": "B", "text": "to"},
            {"key": "C", "text": "by"},
            {"key": "D", "text": "at"}
        ],
        "correct": "A",
        "explanation": "The standard English idiomatic collocation is 'consistent with'.",
        "strategy_or_hack": "Idiomatik predlog: Ingliz tilida har doim 'consistent with' iborasi to'g'ri hisoblanadi."
    },
    {
        "id": "w_b8_48",
        "domain": "Standard English Conventions - Form, Structure, and Sense",
        "skill": "Form, Structure, and Sense",
        "difficulty": "Hard",
        "passage": "Urban planners noted that the thermal absorption characteristics of asphalt parking surfaces differ dramatically from ______ pervious concrete pavements.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "those of"},
            {"key": "B", "text": "that of"},
            {"key": "C", "text": "when compared to"},
            {"key": "D", "text": "the pavement of"}
        ],
        "correct": "A",
        "explanation": "The subject being compared is plural ('the thermal absorption characteristics'). Plural comparisons require 'those of'.",
        "strategy_or_hack": "Ko'plikdagi taqqoslash: 'characteristics' (ko'plikda bo'lgani uchun) 'those of' bilan to'g'ri solishtiriladi."
    },
    {
        "id": "w_b8_49",
        "domain": "Standard English Conventions - Form, Structure, and Sense",
        "skill": "Form, Structure, and Sense",
        "difficulty": "Hard",
        "passage": "Climatologists warn that if atmospheric methane emissions ______ to rise unabated over the coming decades, feedback loops in thawing Arctic permafrost could accelerate global warming.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "were"},
            {"key": "B", "text": "was"},
            {"key": "C", "text": "is"},
            {"key": "D", "text": "will be"}
        ],
        "correct": "A",
        "explanation": "Hypothetical future conditional statements using subjunctive mood require 'were' ('if emissions were to rise...').",
        "strategy_or_hack": "Subjunctive mood (Gipotetik shart): 'if ... were to rise' gipotetik kelajak taxmini uchun 'were' to'g'ri shakldir."
    },
    {
        "id": "w_b8_50",
        "domain": "Standard English Conventions - Form, Structure, and Sense",
        "skill": "Form, Structure, and Sense",
        "difficulty": "Medium",
        "passage": "An elusive nocturnal inhabitant of the high-altitude Andean cloud forests, ______ spends daytime hours resting in concealed canopy nests constructed of twigs and leaves.",
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "options": [
            {"key": "A", "text": "the spectacled bear"},
            {"key": "B", "text": "dense foliage protects the spectacled bear, which"},
            {"key": "C", "text": "biologists have tracked the spectacled bear, which"},
            {"key": "D", "text": "the habitat of the spectacled bear"}
        ],
        "correct": "A",
        "explanation": "The introductory descriptive modifier 'An elusive nocturnal inhabitant...' must logically modify the animal itself ('the spectacled bear'), not foliage or biologists or habitat.",
        "strategy_or_hack": "Kirish iborasiga mos ega: 'An elusive nocturnal inhabitant...' ta'rifi faqat ayiqqa ('the spectacled bear') mos keladi."
    }
]

def build_writing_batch():
    batch = []
    for raw in WRITING_RAW:
        q = {
            "id": raw["id"],
            "version": 1,
            "section": "writing",
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
    batch = build_writing_batch()
    print(f"Generated {len(batch)} Writing questions for Batch 8.")
    all_valid = True
    for q in batch:
        ok, errs = validate_question(q)
        if not ok:
            print(f"Validation error in {q['id']}: {errs}")
            all_valid = False
            
    if all_valid:
        out_path = os.path.join(BASE_DIR, "data", "batch8_writing.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(batch, f, indent=2, ensure_ascii=False)
        print(f"Successfully verified and saved Batch 8 to {out_path}!")
        
        # Also copy script to scripts/author_batch8_writing.py for version control & reproducibility
        target_script = os.path.join(BASE_DIR, "scripts", "author_batch8_writing.py")
        with open(__file__, "r", encoding="utf-8") as src, open(target_script, "w", encoding="utf-8") as dst:
            dst.write(src.read())
        print(f"Archived authoring script to {target_script}")
    else:
        print("Validation errors encountered. Fix them before saving.")
