# -*- coding: utf-8 -*-
"""
Generates the comprehensive Telegram Mini App with:
1. Score & University Grant Predictor
2. Full SAT Mock Exam (42 College Board standard questions: 21 RW + 21 Math)
3. IELTS Listening Full Mock (40 questions, 4 sections)
4. IELTS Reading Full Mock (40 questions, 3 passages)
5. IELTS Writing Bank (42 topics: 21 Task 1 + 21 Task 2 with Band 9 structures)
"""
import json
import html
from pathlib import Path

BASE_DIR = Path(r"C:\Users\Otabek\.gemini\antigravity\scratch\sat-master-bot")
DATA_FILE = BASE_DIR / "data" / "sat_question_bank.json"
OUTPUT_HTML = BASE_DIR / "webapp" / "index.html"

# 1. Load SAT Questions
with open(DATA_FILE, "r", encoding="utf-8") as f:
    sat_all = json.load(f)

sat_rw = [q for q in sat_all if q.get("section") in ["reading", "writing"]][:21]
sat_math = [q for q in sat_all if q.get("section") == "math"][:21]
sat_mock_questions = sat_rw + sat_math

sat_cleaned = []
for i, q in enumerate(sat_mock_questions, start=1):
    sat_cleaned.append({
        "id": i,
        "section": "Reading & Writing" if q.get("section") in ["reading", "writing"] else "Math",
        "domain": q.get("domain", "Digital SAT"),
        "difficulty": q.get("difficulty", "Medium"),
        "passage": q.get("passage", ""),
        "question": q.get("question", ""),
        "options": q.get("options", []),
        "correct": q.get("correct", "A"),
        "explanation": q.get("explanation", ""),
        "strategy": q.get("strategy_or_hack", "")
    })

# 2. IELTS Listening: 40 authentic questions across 4 sections
ielts_listening = []
listening_sections = [
    {
        "section": 1,
        "title": "Section 1: Student Accommodation Booking & Service Form",
        "context": "A conversation between a university student and an accommodation officer regarding renting a student flat in Manchester.",
        "script_summary": "Officer: 'Good morning, University Housing Office, Sarah speaking.' Student: 'Hello, I'm calling to inquire about off-campus flats near the campus. My name is Alex Turner...' Officer confirms rent is £650 per month including water and internet, deposit is £400, located on 14 Meadowbank Road, available from 15th September.",
        "questions": [
            {"num": 1, "type": "form", "text": "Student's Full Name: Alex ______", "ans": "Turner", "expl": "Alex confirms his surname is Turner (T-U-R-N-E-R)."},
            {"num": 2, "type": "form", "text": "Contact Phone Number: 07892 ______", "ans": "451209", "expl": "Alex gives his mobile phone number ending in 451209."},
            {"num": 3, "type": "form", "text": "Desired Move-in Date: ______ September", "ans": "15th", "expl": "The flat becomes available on the 15th of September."},
            {"num": 4, "type": "form", "text": "Address of flat: 14 ______ Road", "ans": "Meadowbank", "expl": "The officer states the property address is 14 Meadowbank Road."},
            {"num": 5, "type": "form", "text": "Monthly rent including bills: £______", "ans": "650", "expl": "The total monthly rent including water and WiFi is 650 pounds."},
            {"num": 6, "type": "form", "text": "Security Deposit required: £______", "ans": "400", "expl": "The landlord requires a refundable deposit of 400 pounds."},
            {"num": 7, "type": "form", "text": "Distance to central library: ______ minutes on foot", "ans": "12", "expl": "The flat is just a 12-minute walk from the central library."},
            {"num": 8, "type": "form", "text": "Nearest bus stop: Outside the ______", "ans": "Post Office", "expl": "Bus number 4 stops directly outside the local Post Office."},
            {"num": 9, "type": "form", "text": "Included appliances: Washing machine and ______", "ans": "Microwave", "expl": "The kitchen comes fitted with a brand new microwave oven."},
            {"num": 10, "type": "form", "text": "Inspection scheduled for Friday at ______ pm", "ans": "3:30", "expl": "They agree to meet for an inspection at half past three in the afternoon."}
        ]
    },
    {
        "section": 2,
        "title": "Section 2: City Botanical Gardens Guide Tour",
        "context": "A talk by the head coordinator of the Royal Botanical Gardens welcoming a new group of seasonal volunteers.",
        "script_summary": "The coordinator describes the layout of the conservatory, the new solar-heated glasshouse built in 2022, volunteer shift rotations, and visitor safety guidelines.",
        "questions": [
            {"num": 11, "type": "mcq", "text": "When was the new tropical glasshouse officially opened?", "options": ["A) 2018", "B) 2020", "C) 2022", "D) 2024"], "ans": "C", "expl": "The speaker mentions the solar glasshouse opened in 2022 following renovation."},
            {"num": 12, "type": "mcq", "text": "What is the primary role of the weekend volunteers?", "options": ["A) Selling entrance tickets", "B) Guiding visitors and giving maps", "C) Pruning exotic trees", "D) Operating the cafeteria"], "ans": "B", "expl": "Volunteers primarily assist with visitor orientation and distributing garden trail maps."},
            {"num": 13, "type": "mcq", "text": "Where should volunteers store their personal belongings?", "options": ["A) In the main gift shop", "B) In the Staff Pavilion lockers", "C) Under the reception desk", "D) In the car park shed"], "ans": "B", "expl": "Keycards allow access to secure lockers located inside the Staff Pavilion."},
            {"num": 14, "type": "mcq", "text": "Which plant collection is currently undergoing pest control treatment?", "options": ["A) Mediterranean herbs", "B) Amazonian orchids", "C) Alpine succulents", "D) Japanese Bonsai"], "ans": "B", "expl": "The Amazonian orchid exhibit is temporarily quarantined for biological pest control."},
            {"num": 15, "type": "mcq", "text": "What should volunteers do if a visitor reports a lost child?", "options": ["A) Search the maze immediately", "B) Call the local emergency services", "C) Radio the security center with Code Yellow", "D) Announce it over the loudspeaker"], "ans": "C", "expl": "Garden protocol requires transmitting a Code Yellow radio alert immediately to security."},
            {"num": 16, "type": "form", "text": "Minimum required volunteer hours per month: ______ hours", "ans": "16", "expl": "All active volunteers commit to at least 16 hours each calendar month."},
            {"num": 17, "type": "form", "text": "Discount on cafeteria meals for volunteers: ______ percent", "ans": "25", "expl": "Staff ID cards grant a 25 percent discount across all on-site dining."},
            {"num": 18, "type": "form", "text": "Annual floral exhibition begins in the month of ______", "ans": "May", "expl": "The famous annual tulip and rose exhibition begins in mid-May."},
            {"num": 19, "type": "form", "text": "Special training workshop on Saturday covers first ______", "ans": "aid", "expl": "A certified first aid and CPR course takes place on Saturday morning."},
            {"num": 20, "type": "form", "text": "Uniform provided: Green vest and official ______", "ans": "badge", "expl": "Volunteers wear an embroidered green vest and photo identification badge."}
        ]
    },
    {
        "section": 3,
        "title": "Section 3: Academic Tutorial on Marine Renewable Energy",
        "context": "Two engineering undergraduates, Mark and Chloe, discussing their research project on tidal stream turbines with Professor Vance.",
        "script_summary": "Mark explains the advantages of underwater turbines over offshore wind farms. Chloe presents experimental data on blade cavitation and material corrosion in saltwater. Professor Vance suggests focusing the literature review on Scottish tidal projects.",
        "questions": [
            {"num": 21, "type": "mcq", "text": "Why did Mark choose tidal stream turbines over offshore wind?", "options": ["A) They are cheaper to construct", "B) Water density provides higher predictability", "C) Turbines do not require maintenance", "D) Government subsidies are higher"], "ans": "B", "expl": "Tidal currents are predictable years in advance and water is 800 times denser than air."},
            {"num": 22, "type": "mcq", "text": "What major obstacle did Chloe identify regarding turbine blades?", "options": ["A) Noise pollution for harbor porpoises", "B) Saltwater corrosion and cavitation damage", "C) Inability to spin at low water speeds", "D) High weight preventing installation"], "ans": "B", "expl": "Chloe highlights rapid cavitation pitting and galvanic corrosion in deep sea water."},
            {"num": 23, "type": "mcq", "text": "Which geographic location does Professor Vance recommend for their case study?", "options": ["A) The Bay of Fundy, Canada", "B) Pentland Firth, Scotland", "C) Cook Strait, New Zealand", "D) The English Channel"], "ans": "B", "expl": "The MeyGen tidal project in Pentland Firth, Scotland offers the most comprehensive operational dataset."},
            {"num": 24, "type": "mcq", "text": "What is the main limitation of the computer simulation model they tested?", "options": ["A) It ignored turbulence caused by seabed topology", "B) It could only calculate single-blade dynamics", "C) The software was incompatible with university Macs", "D) It overestimated annual electrical output by 50%"], "ans": "A", "expl": "The basic CAD model failed to account for complex boundary layer vortices over jagged seabeds."},
            {"num": 25, "type": "mcq", "text": "When must the final draft of the research proposal be submitted?", "options": ["A) November 10th", "B) November 24th", "C) December 1st", "D) December 15th"], "ans": "B", "expl": "Professor Vance confirms the non-negotiable deadline is Friday, November 24th at 5:00 PM."},
            {"num": 26, "type": "form", "text": "Water is roughly ______ times denser than air, amplifying power generation", "ans": "800", "expl": "Physics dictates power output scales directly with fluid density (approx 800x)."},
            {"num": 27, "type": "form", "text": "Proposed blade material to prevent rust: Carbon fiber ______", "ans": "composite", "expl": "Carbon fiber composite resists salt degradation far better than marine alloy steel."},
            {"num": 28, "type": "form", "text": "Maximum water flow velocity in the test channel: ______ meters per second", "ans": "3.5", "expl": "Current measurements peaked at three point five meters per second during spring tide."},
            {"num": 29, "type": "form", "text": "Key environmental metric monitored: Acoustic impact on marine ______", "ans": "mammals", "expl": "Passive sonar arrays monitored behavioral reactions of seals and marine mammals."},
            {"num": 30, "type": "form", "text": "Next meeting with Professor Vance scheduled for Tuesday at ______ am", "ans": "10:15", "expl": "They agree to reconvene in office 402 next Tuesday at quarter past ten."}
        ]
    },
    {
        "section": 4,
        "title": "Section 4: University Lecture on Cognitive Architecture & Memory",
        "context": "A psychology lecture by Dr. Eleanor Hughes discussing the evolution of working memory models and dual-coding theory.",
        "script_summary": "Dr. Hughes breaks down Baddeley's multi-component model of working memory: the central executive, phonological loop, visuospatial sketchpad, and episodic buffer, detailing their neurological correlates in the prefrontal cortex.",
        "questions": [
            {"num": 31, "type": "form", "text": "The central executive coordinates attention and inhibits ______ impulses", "ans": "irrelevant", "expl": "Inhibitory control suppresses task-irrelevant sensory stimuli."},
            {"num": 32, "type": "form", "text": "Phonological loop capacity is typically limited to ______ seconds of speech", "ans": "2", "expl": "Articulatory rehearsal can retain acoustic traces spanning approximately two seconds."},
            {"num": 33, "type": "form", "text": "The visuospatial sketchpad allows manipulation of 2D and 3D ______ representations", "ans": "mental", "expl": "It handles spatial navigation and mental rotation of geometric shapes."},
            {"num": 34, "type": "form", "text": "Episodic buffer integrates information across different sensory ______", "ans": "modalities", "expl": "The buffer binds acoustic, visual, and semantic streams into coherent episodes."},
            {"num": 35, "type": "form", "text": "Brain region most heavily implicated in executive control: Dorsolateral ______ cortex", "ans": "prefrontal", "expl": "fMRI scans consistently show peak activation in the dorsolateral prefrontal cortex."},
            {"num": 36, "type": "mcq", "text": "What happens during the phonological similarity effect?", "options": ["A) Similar sounding words are remembered better", "B) Similar sounding words cause interference and recall errors", "C) Words with similar meanings are confused", "D) Foreign words are translated automatically"], "ans": "B", "expl": "Acoustically similar letters (e.g. B, C, D, P) produce higher error rates due to loop confusion."},
            {"num": 37, "type": "mcq", "text": "How does the 'word length effect' support Baddeley's model?", "options": ["A) Longer words take longer to articulate, reducing memory span", "B) Short words contain less emotional valence", "C) Syllable count is irrelevant to working memory", "D) Reading speed is identical across languages"], "ans": "A", "expl": "Long polysyllabic words take longer to rehearse, leading to faster trace decay."},
            {"num": 38, "type": "form", "text": "Sleep deprivation causes an immediate decrease in working memory ______", "ans": "capacity", "expl": "Acute lack of slow-wave sleep curtails operational memory capacity by up to 30%."},
            {"num": 39, "type": "form", "text": "Technique of grouping items to improve retention: ______", "ans": "chunking", "expl": "Chunking aggregates discrete elements into meaningful conceptual units."},
            {"num": 40, "type": "form", "text": "Working memory scores correlate strongly with general ______ performance", "ans": "academic", "expl": "Working memory is a statistically robust predictor of academic and standardized test success."}
        ]
    }
]

for sec in listening_sections:
    for q in sec["questions"]:
        ielts_listening.append({
            "num": q["num"],
            "section": sec["section"],
            "title": sec["title"],
            "type": q["type"],
            "text": q["text"],
            "options": q.get("options", []),
            "ans": q["ans"],
            "expl": q["expl"]
        })

# 3. IELTS Reading: 40 authentic questions across 3 Academic Passages
ielts_reading_passages = [
    {
        "passage_num": 1,
        "title": "Passage 1: The Trans-Eurasian Silk Road & Early Innovation",
        "text": """Paragraph A: For over a millennium, the Silk Road was not merely a single trade highway, but an intricate network of oasis routes and maritime sea paths that spanned over 6,000 kilometers from Chang'an (modern-day Xi'an) in China across the fertile Fergana Valley of Central Asia to Antioch and Rome. While precious silk textiles and spices were celebrated luxury items, the true transformational legacy of these caravan routes lay in the reciprocal dissemination of technological innovations, agronomic crops, and scientific philosophies.

Paragraph B: Among the most revolutionary technological transfers was the craft of papermaking. Originating in China during the Han Dynasty (attributed to court official Cai Lun in 105 CE), paper was vastly cheaper, more durable, and lighter than European parchment made of animal hides or Egyptian papyrus reeds. Following the pivotal Battle of Talas River in 751 CE near the modern border of Kazakhstan and Kyrgyzstan, Arab forces captured several Chinese artisans skilled in mulberry-bark papermaking. This encounter catalyzed the establishment of the Islamic world's first great paper mills in Samarkand, renowned for producing exquisite, glossy sheets that soon replaced vellum across Baghdad, Cairo, and Andalusia.

Paragraph C: The oasis cities of Central Asia—particularly Bukhara, Merv, and Khwarazm—flourished as world-renowned epicenters of intellectual synthesis during the Islamic Golden Age. Scholars such as Muhammad ibn Musa al-Khwarizmi, working in Baghdad's House of Wisdom, revolutionized mathematics by synthesizing Indian decimal positional systems with Hellenistic geometry, giving birth to algebra (al-jabr) and algorithmic computation. Concurrently, Ibn Sina (Avicenna), born in Afshana near Bukhara, authored 'The Canon of Medicine', a comprehensive medical encyclopedia that served as the standard medical textbook in European universities until the seventeenth century.

Paragraph D: Agriculture also underwent a radical metamorphosis along the Silk Road corridors. Drought-resistant strains of alfalfa were imported to China from Central Asia to sustain superior military cavalry breeds of the 'heavenly horses' of Dayuan. In return, citrus fruits, peaches, apricots, and white mulberry trees for silkworm cultivation diffused westward into Persia and the Mediterranean basin. Furthermore, sophisticated subterranean irrigation networks known as 'karez' or 'qanats' enabled thriving oasis agriculture in arid deserts, channeling melting snow runoff from the Pamir and Tian Shan mountains without evaporation losses.""",
        "questions": [
            {"num": 1, "type": "tfng", "text": "The Silk Road consisted of a single direct paved road stretching from China to Rome.", "ans": "FALSE", "expl": "Paragraph A clearly states it was 'not merely a single trade highway, but an intricate network of oasis routes and maritime sea paths'."},
            {"num": 2, "type": "tfng", "text": "Paper was significantly less expensive and lighter than parchment made of animal skins.", "ans": "TRUE", "expl": "Paragraph B states paper was 'vastly cheaper, more durable, and lighter than European parchment made of animal hides'."},
            {"num": 3, "type": "tfng", "text": "Cai Lun personally traveled to Samarkand to construct the first Central Asian paper mill.", "ans": "FALSE", "expl": "Paragraph B shows Cai Lun lived in 105 CE in China; Samarkand mills were established after the Battle of Talas in 751 CE by captured artisans."},
            {"num": 4, "type": "tfng", "text": "Samarkand paper was made using mulberry bark.", "ans": "TRUE", "expl": "Paragraph B mentions 'artisans skilled in mulberry-bark papermaking' established the mills in Samarkand."},
            {"num": 5, "type": "tfng", "text": "Ibn Sina was born within the borders of modern-day Italy.", "ans": "FALSE", "expl": "Paragraph C states Ibn Sina was 'born in Afshana near Bukhara'."},
            {"num": 6, "type": "tfng", "text": "Al-Khwarizmi's algebraic treatises drew exclusively on Greek sources without any Indian influences.", "ans": "FALSE", "expl": "Paragraph C explains he synthesized 'Indian decimal positional systems with Hellenistic geometry'."},
            {"num": 7, "type": "tfng", "text": "The Canon of Medicine was abandoned by European universities within ten years of publication.", "ans": "FALSE", "expl": "Paragraph C confirms it 'served as the standard medical textbook in European universities until the seventeenth century'."},
            {"num": 8, "type": "tfng", "text": "Silk Road merchants paid higher customs duties in Samarkand than in Antioch.", "ans": "NOT GIVEN", "expl": "The passage discusses goods and ideas traded, but does not compare specific customs tax rates between cities."},
            {"num": 9, "type": "fill", "text": "Alfalfa was introduced to China to feed high-quality military ______", "ans": "horses", "expl": "Paragraph D states alfalfa was imported to sustain 'superior military cavalry breeds of the 'heavenly horses'.'"},
            {"num": 10, "type": "fill", "text": "Subterranean irrigation systems called karez prevented water loss through ______", "ans": "evaporation", "expl": "Paragraph D highlights channeling snow runoff 'without evaporation losses'."},
            {"num": 11, "type": "mcq", "text": "What was the primary factor leading to papermaking in the Islamic world?", "options": ["A) Cai Lun's royal embassy to Baghdad", "B) The capture of Chinese paper artisans at the Battle of Talas", "C) Depletion of Egyptian papyrus supplies", "D) An imperial trade treaty signed in Bukhara"], "ans": "B", "expl": "Paragraph B attributes this directly to captured artisans after the 751 CE Battle of Talas."},
            {"num": 12, "type": "mcq", "text": "Which mountain ranges provided snowmelt for the karez irrigation canals?", "options": ["A) Alps and Pyrenees", "B) Himalayas and Urals", "C) Pamir and Tian Shan", "D) Caucasus and Zagros"], "ans": "C", "expl": "Paragraph D states 'melting snow runoff from the Pamir and Tian Shan mountains'."},
            {"num": 13, "type": "mcq", "text": "What is the best overall title for Passage 1?", "options": ["A) The Military Expansion of Han Dynasty China", "B) The Silk Road: Catalyst for Global Technological and Intellectual Exchange", "C) Medical Revolutions of Medieval Europe", "D) Agricultural Collapse in Ancient Central Asia"], "ans": "B", "expl": "The passage comprehensively details the diffusion of technology, mathematics, medicine, and agriculture along the route."}
        ]
    },
    {
        "passage_num": 2,
        "title": "Passage 2: Biomimicry and Sustainable Architectural Engineering",
        "text": """Paragraph A: Over 3.8 billion years of evolutionary selection, nature has resolved complex engineering challenges—energy efficiency, structural resilience, self-repair, and temperature regulation—with minimal waste and maximum thermodynamic efficiency. Biomimicry, an architectural and scientific discipline popularized by Janine Benyus, seeks sustainable human solutions by emulating nature's time-tested blueprints and biological processes. Rather than treating natural ecosystems as passive resources to extract, architects are investigating how biological structures endure extreme environmental stressors.

Paragraph B: One celebrated manifestation of biomimetic architecture is the Eastgate Centre, a mid-rise shopping and office complex in Harare, Zimbabwe, designed by architect Mick Pearce in collaboration with Arup engineers. Tropical sub-Saharan climates often necessitate massive air conditioning systems, consuming substantial fossil-fuel electrical grids. Pearce observed that indigenous African termite mounds constructed by Macrotermes bellicosus maintain an unvarying interior temperature of precisely 30.5°C (87°F), despite external desert fluctuations ranging from 2°C at night to over 42°C during daylight. Termites achieve this equilibrium through passive stack ventilation: an intricate array of subterranean cooling chambers, convective air vents, and chimney flues.

Paragraph C: By mimicking this chimney convection system, the Eastgate Centre was built entirely without conventional mechanical refrigeration equipment. High thermal mass concrete absorbs building heat during the day. At night, heavy roof fans flush warm stale air outward while drawing cool nocturnal breezes through floor flues. As a consequence, the building utilizes 35% less energy than comparable conventional office buildings in Harare, saving the building owners over $3.5 million in upfront air-conditioning equipment costs and substantially reducing carbon emissions.

Paragraph D: Contemporary materials science has extended biomimicry to nanoscale surface textures. The leaves of the sacred lotus flower (Nelumbo nucifera) remain immaculate despite flourishing in muddy aquatic habitats. Under electron microscopy, the leaf surface exhibits micro-papillae coated in hydrophobic epicuticular wax crystals. Raindrops rolling across this bumpy topography cannot flatten; instead, they remain spherical beads that pick up dust particles and contaminants, effortlessly washing the surface clean—a phenomenon known as the 'Lotus Effect'. Paint manufacturers and glass engineers have patented self-cleaning exterior coatings (such as Lotusan) based on this mechanism, slashing facade maintenance expenditure and hazardous chemical solvent usage in skyscrapers worldwide.""",
        "questions": [
            {"num": 14, "type": "tfng", "text": "Janine Benyus is credited with popularizing the concept of biomimicry.", "ans": "TRUE", "expl": "Paragraph A states 'Biomimicry, an architectural and scientific discipline popularized by Janine Benyus...'"},
            {"num": 15, "type": "tfng", "text": "The Eastgate Centre relies on a massive conventional mechanical air conditioner.", "ans": "FALSE", "expl": "Paragraph C clearly states it was 'built entirely without conventional mechanical refrigeration equipment'."},
            {"num": 16, "type": "tfng", "text": "Macrotermes bellicosus termites maintain their interior mound temperature at exactly 30.5°C.", "ans": "TRUE", "expl": "Paragraph B states they 'maintain an unvarying interior temperature of precisely 30.5°C'."},
            {"num": 17, "type": "tfng", "text": "Mick Pearce designed the Eastgate Centre alone without engineering partners.", "ans": "FALSE", "expl": "Paragraph B notes he designed it 'in collaboration with Arup engineers'."},
            {"num": 18, "type": "tfng", "text": "The Eastgate Centre consumes 35% more energy than standard Harare complexes.", "ans": "FALSE", "expl": "Paragraph C states it 'utilizes 35% less energy'."},
            {"num": 19, "type": "tfng", "text": "Lotus leaves remain clean because the surface is completely smooth like glass.", "ans": "FALSE", "expl": "Paragraph D states the surface exhibits 'micro-papillae coated in hydrophobic epicuticular wax crystals'."},
            {"num": 20, "type": "tfng", "text": "Water droplets on lotus leaves form spherical beads rather than spreading out.", "ans": "TRUE", "expl": "Paragraph D states 'raindrops rolling across this bumpy topography cannot flatten; instead, they remain spherical beads'."},
            {"num": 21, "type": "tfng", "text": "The Zimbabwean government provided tax exemptions for the construction of Eastgate Centre.", "ans": "NOT GIVEN", "expl": "The passage discusses savings in equipment and energy, but mentions nothing about government tax exemptions."},
            {"num": 22, "type": "fill", "text": "African termite mounds utilize passive ______ ventilation to regulate heat", "ans": "stack", "expl": "Paragraph B states 'termites achieve this equilibrium through passive stack ventilation'."},
            {"num": 23, "type": "fill", "text": "Building heat is absorbed during the day by high ______ mass concrete", "ans": "thermal", "expl": "Paragraph C states 'high thermal mass concrete absorbs building heat during the day'."},
            {"num": 24, "type": "fill", "text": "The self-cleaning property observed on lotus leaves is termed the ______ Effect", "ans": "Lotus", "expl": "Paragraph D defines this as 'a phenomenon known as the Lotus Effect'."},
            {"num": 25, "type": "mcq", "text": "What financial benefit did the owners of Eastgate Centre gain initially?", "options": ["A) Complete refund of building land purchase taxes", "B) Over $3.5 million saved on HVAC equipment purchases", "C) Free electricity provided by city utility companies", "D) Tripled rental rates due to architectural awards"], "ans": "B", "expl": "Paragraph C states it saved 'over $3.5 million in upfront air-conditioning equipment costs'."},
            {"num": 26, "type": "mcq", "text": "How do self-cleaning exterior facade coatings help the environment?", "options": ["A) By absorbing urban smog directly into walls", "B) By reducing reliance on chemical solvents for cleaning", "C) By generating solar electricity from rain showers", "D) By attracting birds to pollinate flowers"], "ans": "B", "expl": "Paragraph D states it slashes 'hazardous chemical solvent usage in skyscrapers'."}
        ]
    },
    {
        "passage_num": 3,
        "title": "Passage 3: Neuroplasticity, Cognitive Reserve, and Adult Brain Resilience",
        "text": """Paragraph A: Throughout the greater part of the twentieth century, the prevailing dogma within neurobiology maintained that the adult mammalian brain was a static, hard-wired organ. Following childhood developmental windows, neurons were presumed incapable of regeneration, with cognitive aging considered an irreversible trajectory of synaptic decay. However, landmark investigations in the late 1990s spearheaded by researchers like Fred Gage and Elizabeth Gould upended this neuroscientific orthodoxy, providing definitive empirical evidence of adult neurogenesis—the de novo creation and functional integration of new neurons in the subgranular zone of the dentate gyrus within the human hippocampus.

Paragraph B: Neuroplasticity describes the nervous system's capacity to modify its structural architecture and functional organization in response to environmental demands, experiential learning, and pathological trauma. Structural plasticity encompasses synaptogenesis (formation of novel synaptic contacts), dendritic branching, and axonal sprouting. A classic confirmation of structural neuroplasticity emerged from neuroimaging investigations of London licensed taxi drivers conducted by Professor Eleanor Maguire. London cabbies undergo years of rigorous spatial memorization known as 'The Knowledge', committing 25,000 streets and thousands of landmarks to memory. MRI volumetric analysis revealed that qualified drivers exhibited significantly greater grey matter volume in the posterior hippocampus compared to age-matched controls, with hippocampal volume correlating directly with years spent driving.

Paragraph C: Closely tethered to neuroplasticity is the epidemiological concept of 'cognitive reserve', formulated by neuropsychologist Yaakov Stern. Cognitive reserve posits that individuals possess differing thresholds of resilience against neurodegenerative pathologies such as Alzheimer's disease. Stern observed that two individuals exhibiting identical amounts of amyloid-beta plaques and neurofibrillary tau tangles on post-mortem histological examination could manifest drastically divergent cognitive states during life: one remained sharp, lucid, and functionally autonomous, while the other suffered profound dementia.

Paragraph D: Cognitive reserve is not determined solely by genetics; rather, it is continuously accumulated across the lifespan through mentally stimulating occupations, bilingualism, formal higher education, and vigorous aerobic physical exercise. Lifelong bilingual individuals, for example, demonstrate an average delay of four to five years in the clinical onset of Alzheimer's symptoms compared to monolinguals. Aerobic exercise stimulates the release of Brain-Derived Neurotrophic Factor (BDNF), a master regulatory protein that fuels hippocampal neurogenesis, improves cerebral microvascular perfusion, and fortifies synaptic connectivity against age-associated deterioration.""",
        "questions": [
            {"num": 27, "type": "tfng", "text": "Twentieth-century neuroscientists believed adult brains could readily produce new neurons.", "ans": "FALSE", "expl": "Paragraph A states they believed 'the adult mammalian brain was a static, hard-wired organ... neurons were presumed incapable of regeneration'."},
            {"num": 28, "type": "tfng", "text": "Adult neurogenesis takes place in the dentate gyrus of the hippocampus.", "ans": "TRUE", "expl": "Paragraph A identifies 'the subgranular zone of the dentate gyrus within the human hippocampus'."},
            {"num": 29, "type": "tfng", "text": "London taxi drivers must memorize 25,000 streets for 'The Knowledge' test.", "ans": "TRUE", "expl": "Paragraph B states cabbies undergo 'The Knowledge', committing 25,000 streets and thousands of landmarks to memory."},
            {"num": 30, "type": "tfng", "text": "London taxi drivers had smaller posterior hippocampi than ordinary citizens.", "ans": "FALSE", "expl": "Paragraph B shows they exhibited 'significantly greater grey matter volume in the posterior hippocampus'."},
            {"num": 31, "type": "tfng", "text": "Yaakov Stern pioneered the conceptual framework of cognitive reserve.", "ans": "TRUE", "expl": "Paragraph C introduces 'the epidemiological concept of cognitive reserve, formulated by neuropsychologist Yaakov Stern'."},
            {"num": 32, "type": "tfng", "text": "Amyloid plaques always cause severe dementia symptoms immediately upon appearing.", "ans": "FALSE", "expl": "Paragraph C explains individuals with identical plaque loads could remain sharp and lucid due to cognitive reserve."},
            {"num": 33, "type": "tfng", "text": "Bilingualism has been linked to a 4 to 5 year delay in dementia symptoms.", "ans": "TRUE", "expl": "Paragraph D states lifelong bilinguals 'demonstrate an average delay of four to five years in the clinical onset of Alzheimer's symptoms'."},
            {"num": 34, "type": "tfng", "text": "Exercise reduces the concentration of Brain-Derived Neurotrophic Factor (BDNF) in the brain.", "ans": "FALSE", "expl": "Paragraph D states aerobic exercise 'stimulates the release of Brain-Derived Neurotrophic Factor (BDNF)'."},
            {"num": 35, "type": "tfng", "text": "Playing classical chess produces more hippocampal growth than aerobic running.", "ans": "NOT GIVEN", "expl": "The passage discusses mental stimulation and aerobic exercise, but makes no specific comparison between chess and running."},
            {"num": 36, "type": "fill", "text": "The creation of new synapses between existing neurons is called ______", "ans": "synaptogenesis", "expl": "Paragraph B defines this as 'synaptogenesis (formation of novel synaptic contacts)'."},
            {"num": 37, "type": "fill", "text": "Brain regulatory protein stimulated by aerobic exercise: ______ (abbreviation)", "ans": "BDNF", "expl": "Paragraph D names 'Brain-Derived Neurotrophic Factor (BDNF)'."},
            {"num": 38, "type": "mcq", "text": "What does structural plasticity primarily refer to?", "options": ["A) The skull's ability to withstand blunt trauma", "B) The physical reorganization of synapses, dendrites, and neural circuits", "C) The chemical synthesis of artificial neurotransmitters", "D) The genetic cloning of cerebral cortex tissues"], "ans": "B", "expl": "Paragraph B explains structural plasticity includes synaptogenesis, dendritic branching, and axonal sprouting."},
            {"num": 39, "type": "mcq", "text": "Why do bilingual individuals exhibit higher cognitive reserve?", "options": ["A) They have larger overall skull circumferences", "B) Constant linguistic conflict resolution strengthens executive control networks", "C) They read fewer books than monolinguals", "D) Second languages alter blood typing in the brain"], "ans": "B", "expl": "Lifelong dual-language management trains frontal executive brain networks to resist pathology."},
            {"num": 40, "type": "mcq", "text": "What is the primary conclusion of the passage regarding cognitive aging?", "options": ["A) Mental deterioration is 100% predetermined by genetics at birth", "B) Adult brains retain the capacity to rewire and resist decay through lifestyle engagement", "C) Memory loss is inevitable and cannot be delayed by any intervention", "D) Taxi driving is the only effective treatment for neurodegeneration"], "ans": "B", "expl": "The passage demonstrates that neuroplasticity and lifestyle factors allow the brain to adapt, generate neurons, and build reserve against decline."}
        ]
    }
]

ielts_reading = []
for p in ielts_reading_passages:
    for q in p["questions"]:
        ielts_reading.append({
            "num": q["num"],
            "passage_num": p["passage_num"],
            "passage_title": p["title"],
            "passage_text": p["text"],
            "type": q["type"],
            "text": q["text"],
            "options": q.get("options", []),
            "ans": q["ans"],
            "expl": q["expl"]
        })

# 4. IELTS Writing Bank: 42 Comprehensive Topics (21 Task 1 + 21 Task 2)
writing_task1_topics = [
    {
        "id": "t1_01",
        "title": "Line Graph: Renewable Energy Production (2000–2025)",
        "type": "Line Graph",
        "prompt": "The line graph below illustrates the percentage of total electricity generated from renewable sources (solar, wind, hydroelectric) in four European countries between 2000 and 2025.",
        "key_features": "Hydroelectric remained steady around 30%; solar experienced exponential growth after 2012; Germany overtook Norway in solar generation; wind power grew four-fold.",
        "overview": "Overall, all four nations saw an upward trajectory in renewable adoption, with solar power recording the most dramatic acceleration.",
        "band9_vocab": ["exponential surge", "plateaued steadily", "experienced a fivefold increase", "outstripped", "underwent a modest oscillation"],
        "structure": "Paragraph 1: Paraphrase prompt; Paragraph 2: Overview of major trends; Paragraph 3: Detailed comparison of Solar and Wind; Paragraph 4: Detailed comparison of Hydro and Biomass."
    },
    {
        "id": "t1_02",
        "title": "Bar Chart: University Graduation Rates by Field and Gender",
        "type": "Bar Chart",
        "prompt": "The bar chart compares the proportion of male and female graduates across five academic disciplines (STEM, Humanities, Business, Medicine, Law) in the UK in 2024.",
        "key_features": "Males dominated Engineering and Computer Science (72% vs 28%); females significantly outnumbered males in Medicine and Humanities (65% vs 35%); Business achieved near gender parity.",
        "overview": "Overall, noticeable gender disparities persisted in technical STEM disciplines and health sciences, whereas commerce maintained an equitable split.",
        "band9_vocab": ["marked discrepancy", "near gender parity", "significantly outstripped", "stark gender gap", "marginal difference"],
        "structure": "Intro + Overview (2 main contrasting fields) + Body 1 (STEM & Medicine) + Body 2 (Business & Humanities)."
    },
    {
        "id": "t1_03",
        "title": "Pie Charts: Household Expenditure in Japan (1990 vs 2020)",
        "type": "Pie Chart",
        "prompt": "The two pie charts compare household expenditure patterns across five categories (Food, Housing, Transport, Leisure, Technology) in Japan in 1990 and 2020.",
        "key_features": "Technology spending expanded from 3% to 18%; Food dropped from 32% to 19%; Housing remained the single largest expenditure throughout both eras.",
        "overview": "Overall, spending shifted noticeably from physical necessities like food toward digital technology and entertainment, while accommodation swallowed the largest proportion in both years.",
        "band9_vocab": ["commanded the lion's share", "witnessed a sixfold expansion", "contracted markedly", "accounted for almost a third"],
        "structure": "Intro + Overview + Body 1 (Housing & Food trends) + Body 2 (Technology, Leisure, and Transport shifts)."
    },
    {
        "id": "t1_04",
        "title": "Process Diagram: Production of Refined Lithium for EV Batteries",
        "type": "Process",
        "prompt": "The diagram illustrates the industrial stages involved in extracting lithium from underground brine pools and refining it into battery-grade lithium carbonate.",
        "key_features": "Seven discrete sequential phases: brine pumping, solar evaporation pans (12-18 months), chemical precipitation of magnesium, purification, crystallization, drying, and micronized packaging.",
        "overview": "Overall, the multi-step industrial process transforms raw saline water into high-purity chemical compound through extensive evaporation followed by chemical refinement.",
        "band9_vocab": ["extracted subterranean brine", "subjected to prolonged evaporation", "precipitated out", "centrifuged and dried", "dispatched for manufacturing"],
        "structure": "Intro + Overview of input vs final output + Body 1 (Pumping through Evaporation ponds) + Body 2 (Chemical precipitation through final packaging)."
    },
    {
        "id": "t1_05",
        "title": "Map Comparison: Redevelopment of Riverside Industrial Estate (2010 vs Present)",
        "type": "Map",
        "prompt": "The two maps show changes in a riverside industrial district between 2010 and the present day.",
        "key_features": "Demolition of derelict factories; construction of modern eco-apartments, public marina, pedestrianized promenade, and light rail station; preservation of the historic clock tower.",
        "overview": "Overall, the district underwent comprehensive urban regeneration, transitioning from a utilitarian industrial zone into a residential, recreational, and transit-oriented neighborhood.",
        "band9_vocab": ["underwent extensive urban regeneration", "bulldozed and replaced by", "pedestrianized boulevard", "erected on the former site", "preserved intact"],
        "structure": "Intro + Overview + Body 1 (Northern riverfront developments) + Body 2 (Southern transport and residential additions)."
    },
    {
        "id": "t1_06",
        "title": "Table: Public Transport Punctuality Across 5 European Metropolises",
        "type": "Table",
        "prompt": "The table provides data on on-time performance, passenger volume, and ticket affordability across five capital cities in 2023.",
        "key_features": "Vienna scored highest punctuality (96.4%) with lowest ticket cost; London carried highest volume (4.1M daily) with lowest punctuality (84.1%).",
        "overview": "Overall, smaller integrated transit networks exhibited superior reliability and cost-effectiveness compared to sprawling megacities.",
        "band9_vocab": ["punctuality metric", "eclipsed all competitors", "lagged behind", "inversely proportional", "daily passenger footfall"],
        "structure": "Intro + Overview + Body 1 (Vienna & Zurich excellence) + Body 2 (London, Paris, Berlin comparison)."
    },
    {
        "id": "t1_07",
        "title": "Multiple Graphs: Global Coffee Production & Consumption (2015–2025)",
        "type": "Multiple Graphs",
        "prompt": "The bar chart shows coffee bean production by top exporters, while the line graph depicts annual per capita consumption in four consumer countries.",
        "key_features": "Brazil led global export volume (over 40%); Nordic nations (Finland, Norway) maintained world-highest per capita consumption (12kg/yr).",
        "overview": "Overall, South American dominance in harvest volumes correlated with escalating European and North American consumer demand.",
        "band9_vocab": ["undisputed market leader", "per capita intake", "plateaued around", "registered consistent escalation"],
        "structure": "Intro + Overview + Body 1 (Bar chart exporter data) + Body 2 (Line graph consumer trends)."
    },
    {
        "id": "t1_08",
        "title": "Process Diagram: Traditional Tea Fermentation and Packaging",
        "type": "Process",
        "prompt": "The flow chart shows the stages in processing green and black tea from plucked Camellia sinensis leaves.",
        "key_features": "Branching step: Green tea is steamed to halt oxidation; Black tea undergoes bruising and complete enzymatic oxidation before firing.",
        "overview": "Overall, while both varieties originate from identical harvested leaves, the presence or absence of oxidation serves as the critical divergence point.",
        "band9_vocab": ["plucked manually", "enzymatic oxidation", "steamed to deactivate enzymes", "roasted in rotary kilns", "vacuum sealed"],
        "structure": "Intro + Overview + Body 1 (Harvesting, withering, and green tea pathway) + Body 2 (Black tea oxidation and packaging)."
    },
    {
        "id": "t1_09",
        "title": "Bar Chart: Percentage of Remote Workers Across Economic Sectors",
        "type": "Bar Chart",
        "prompt": "The bar chart compares teleworking rates across six industries before, during, and after the pandemic.",
        "key_features": "IT & Financial services peaked at 88% and sustained 65% remote post-pandemic; Manufacturing and Healthcare returned swiftly to baseline levels (<15%).",
        "overview": "Overall, digital knowledge industries cemented hybrid workflows, whereas physical labor sectors witnessed temporary surges followed by sharp normalization.",
        "band9_vocab": ["telecommuting adoption", "skyrocketed to a peak", "reverted to pre-crisis levels", "sustained hybrid arrangements"],
        "structure": "Intro + Overview + Body 1 (Knowledge sectors: Tech & Finance) + Body 2 (Physical sectors: Healthcare & Manufacturing)."
    },
    {
        "id": "t1_10",
        "title": "Line Graph: Atmospheric CO2 Levels and Global Temperature Anomalies",
        "type": "Line Graph",
        "prompt": "The line graph traces atmospheric carbon dioxide concentrations (ppm) against global mean temperature deviations from 1950 to 2025.",
        "key_features": "CO2 rose steadily from 310 ppm to 422 ppm; temperature anomaly tracked CO2 closely, breaking +1.2°C above pre-industrial averages by 2024.",
        "overview": "Overall, both metrics exhibited unbroken compounding upward momentum, displaying a stark positive correlation over the 75-year timeframe.",
        "band9_vocab": ["inexorable upward march", "striking positive correlation", "breached the threshold", "compounding escalation"],
        "structure": "Intro + Overview + Body 1 (CO2 atmospheric accumulation) + Body 2 (Temperature anomaly curve and correlation)."
    },
    {
        "id": "t1_11",
        "title": "Map: Proposed High-Speed Rail Corridor Between Metropolis A and Port B",
        "type": "Map",
        "prompt": "The plans show two alternative proposals (Route Alpha and Route Beta) for constructing a high-speed railway between an inland metropolis and an international seaport.",
        "key_features": "Route Alpha is shorter (120km) but traverses protected wetland nature reserves requiring expensive tunnels; Route Beta is 40km longer along highway bypasses avoiding ecological zones.",
        "overview": "Overall, Route Alpha prioritizes travel speed at high environmental and fiscal cost, while Route Beta minimizes ecological disturbance at the expense of rail distance.",
        "band9_vocab": ["traverses protected ecological reserves", "necessitates subterranean tunneling", "parallels the existing expressway", "environmental trade-off"],
        "structure": "Intro + Overview + Body 1 (Route Alpha analysis) + Body 2 (Route Beta contrast)."
    },
    {
        "id": "t1_12",
        "title": "Pie Charts: Sources of Municipal Electricity in South Korea",
        "type": "Pie Chart",
        "prompt": "The pie charts illustrate the composition of primary fuels used for power generation in South Korea in 2010 and 2024.",
        "key_features": "Coal contracted from 42% to 26%; Nuclear stabilized at ~29%; Solar and Wind expanded from 2% to 19%; Liquefied Natural Gas (LNG) filled the bridging gap.",
        "overview": "Overall, reliance on coal diminished substantially as the grid diversified into clean renewables and natural gas.",
        "band9_vocab": ["fossil fuel contraction", "grid diversification", "accounted for roughly a quarter", "clean energy ascension"],
        "structure": "Intro + Overview + Body 1 (Coal & Gas transitions) + Body 2 (Nuclear & Renewable expansion)."
    },
    {
        "id": "t1_13",
        "title": "Table: Academic Performance Metrics Across 4 High School Curricula",
        "type": "Table",
        "prompt": "The table compares student retention, university matriculation, and median exam scores for IB Diploma, A-Levels, AP, and National High School Diploma.",
        "key_features": "IB students achieved highest university matriculation (92%) and scholarship awards; National diploma had highest graduation rate but lower foreign admissions.",
        "overview": "Overall, internationally recognized holistic programs outperformed national baselines in competitive tertiary admissions.",
        "band9_vocab": ["tertiary matriculation", "outperformed domestic baselines", "commanded the highest rate", "marginal variance"],
        "structure": "Intro + Overview + Body 1 (IB & A-Levels comparison) + Body 2 (AP & National diploma metrics)."
    },
    {
        "id": "t1_14",
        "title": "Line Graph: Urbanization Rates in 5 Developing Regions (1970–2030)",
        "type": "Line Graph",
        "prompt": "The graph depicts the proportion of the population residing in urban agglomerations across East Asia, South Asia, Latin America, Sub-Saharan Africa, and Central Asia.",
        "key_features": "Latin America was already 60% urban in 1970 reaching 84%; East Asia witnessed the fastest steep rise (20% to 68%); South Asia grew steadily to 40%.",
        "overview": "Overall, all developing regions experienced irreversible urbanization, though initial baselines and rates of velocity varied markedly.",
        "band9_vocab": ["unprecedented rural-to-urban migration", "steepest trajectory", "urban agglomerations", "widening disparity"],
        "structure": "Intro + Overview + Body 1 (Fast movers: East Asia & Latin America) + Body 2 (Slower trajectories: South Asia & Africa)."
    },
    {
        "id": "t1_15",
        "title": "Process Diagram: Wastewater Purification and Desalination Plant",
        "type": "Process",
        "prompt": "The flow diagram illustrates how municipal wastewater is purified into potable drinking water via microfiltration and reverse osmosis.",
        "key_features": "Bar screens remove large solids; primary clarifier settles sludge; bioreactors digest organics; microfiltration; high-pressure reverse osmosis membranes; UV disinfection.",
        "overview": "Overall, the recycling cycle transforms contaminated effluent into medical-grade potable water through physical, biological, and chemical barriers.",
        "band9_vocab": ["solid particulate separation", "biological aerobic digestion", "pressurized reverse osmosis membranes", "potable water reservoir"],
        "structure": "Intro + Overview + Body 1 (Physical filtration & Clarification) + Body 2 (Membrane filtration, UV disinfection, and distribution)."
    },
    {
        "id": "t1_16",
        "title": "Bar Chart: Average Daily Screen Time Among Adolescents by Device",
        "type": "Bar Chart",
        "prompt": "The bar chart compares daily minutes spent by teenagers on smartphones, gaming consoles, tablets, and computers across four continents in 2024.",
        "key_features": "Smartphones absorbed over 260 mins/day globally; North America had highest console gaming; Asia led in educational computer usage.",
        "overview": "Overall, smartphones proved the overwhelmingly ubiquitous screen medium across all territories, eclipsing legacy televisions and desktop computers.",
        "band9_vocab": ["ubiquitous personal screen", "dwarfed rival media", "consumed an average of", "divergent regional preferences"],
        "structure": "Intro + Overview + Body 1 (Smartphones dominance) + Body 2 (Consoles and PC comparisons)."
    },
    {
        "id": "t1_17",
        "title": "Map: Coastal Town Flood Defense Infrastructure (Before and After Project)",
        "type": "Map",
        "prompt": "The two plans display the shoreline defenses of an estuary town before and after an extensive civil engineering storm surge barrier scheme.",
        "key_features": "Replacement of damaged wooden groynes with concrete revetments; addition of retractable tidal gates across the river mouth; planting of salt marsh buffer zones.",
        "overview": "Overall, rudimentary natural barriers were transformed into modern, fortified dual-action civil defense infrastructure to withstand sea-level rises.",
        "band9_vocab": ["storm surge mitigation", "retractable tidal barrier", "constructed along the shoreline", "salt marsh buffer zone"],
        "structure": "Intro + Overview + Body 1 (Seaward barriers and revetments) + Body 2 (River mouth gates and ecological wetlands)."
    },
    {
        "id": "t1_18",
        "title": "Line Graph: Average Global Air Cargo Tariffs vs Marine Freight Rates",
        "type": "Line Graph",
        "prompt": "The line graph traces shipping costs per kilogram for air freight versus forty-foot ocean shipping containers between 2018 and 2024.",
        "key_features": "Ocean container spot rates spiked tenfold in 2021 during supply chain shocks; air cargo remained roughly 4-5x more expensive per kg but stabilized much faster.",
        "overview": "Overall, ocean freight witnessed severe volatility during global trade disruptions, whereas air freight sustained premium, predictable pricing.",
        "band9_vocab": ["supply chain disruption", "exponential spot rate volatility", "stabilized at a plateau", "commanded a significant premium"],
        "structure": "Intro + Overview + Body 1 (Ocean freight spike & collapse) + Body 2 (Air cargo premium stability)."
    },
    {
        "id": "t1_19",
        "title": "Pie Charts: Agricultural Land Use and Irrigation Types in Central Asia",
        "type": "Pie Chart",
        "prompt": "The charts display the distribution of arable land dedicated to cotton, wheat, orchards, and forage crops, alongside irrigation techniques in Uzbekistan.",
        "key_features": "Wheat and cotton dominated acreage (38% and 34%); drip irrigation expanded rapidly to 22%, reducing furrow flooding.",
        "overview": "Overall, staple grains and cash crops occupied the majority of farmland, accompanied by an aggressive modernization of water-saving drip systems.",
        "band9_vocab": ["dedicated arable acreage", "furrow irrigation dominance", "water-efficient drip mechanisms", "cash crop allocation"],
        "structure": "Intro + Overview + Body 1 (Crop land distribution) + Body 2 (Irrigation technology breakdown)."
    },
    {
        "id": "t1_20",
        "title": "Process Diagram: Glass Bottle Recycling Cycle",
        "type": "Process",
        "prompt": "The graphic shows how post-consumer glass containers are collected, sorted by color, melted in glass furnaces, and remanufactured into new consumer bottles.",
        "key_features": "Consumer return bins -> Color sorting (clear, amber, green) -> Crushing into cullet -> Furnace melting at 1500°C -> Mold blowing -> Cooling -> Distribution.",
        "overview": "Overall, glass recycling forms a closed-loop circular economy that eliminates landfill waste through infinite thermal remolding.",
        "band9_vocab": ["closed-loop recycling", "crushed into uniform cullet", "color-segregated bins", "molten liquid glass", "blown into cast molds"],
        "structure": "Intro + Overview + Body 1 (Collection and sorting) + Body 2 (Melting, mold shaping, and distribution)."
    },
    {
        "id": "t1_21",
        "title": "Table: Global Electric Vehicle Sales and Charging Infrastructure Growth",
        "type": "Table",
        "prompt": "The table compares EV market share, public fast chargers per 100km, and governmental consumer subsidies across Norway, China, USA, Germany, and Japan.",
        "key_features": "Norway held 88% EV market share; China installed highest absolute volume of fast chargers (over 1.2M); Japan lagged in battery EV uptake.",
        "overview": "Overall, Scandinavian tax exemptions and Chinese infrastructure investment spurred unprecedented EV saturation compared to other automotive giants.",
        "band9_vocab": ["market penetration", "robust public charging density", "government fiscal subsidies", "lagged considerably behind"],
        "structure": "Intro + Overview + Body 1 (Norway & China leadership) + Body 2 (Germany, USA, and Japan adoption)."
    }
]

writing_task2_topics = [
    {
        "id": "t2_01",
        "title": "AI & Automation in the Modern Workforce",
        "type": "Agree / Disagree (Opinion)",
        "prompt": "Artificial intelligence and autonomous robotics are developing at a pace that could eliminate millions of jobs. Some believe governments should impose heavy taxes on automation to protect human employment. To what extent do you agree or disagree?",
        "stance": "Strongly Disagree with punitive automation taxes; advocate instead for retraining funds and productivity dividends.",
        "ideas": "Taxing technological progress stifles innovation and makes domestic industries uncompetitive globally. Instead, productivity windfalls from AI should fund universal lifelong education, vocational retraining in healthcare and human-centric fields.",
        "band9_vocab": ["technological unemployment", "retard economic dynamism", "productivity windfall", "re-skilling initiative", "human-centric vocation"],
        "outline": "Intro (paraphrase + clear thesis: punitive taxes are counterproductive) -> Body 1 (Why automation taxes handicap national competitiveness and economic growth) -> Body 2 (Constructive solutions: using AI wealth generation to finance state-sponsored education and re-skilling) -> Conclusion (restate stance)."
    },
    {
        "id": "t2_02",
        "title": "University Education vs Direct Vocational Experience",
        "type": "Discuss Both Views & Give Opinion",
        "prompt": "Some people think that attending university is the best way to secure a successful career, while others argue that entering the workforce straight after secondary school provides superior long-term financial benefits. Discuss both views and give your own opinion.",
        "stance": "Balanced: Vocational entry provides immediate debt-free income, but tertiary education unlocks higher lifetime earnings ceilings in specialized intellectual professions.",
        "ideas": "Vocational trades (plumbing, electricians) escape massive student loans and earn immediately. However, high-tier professions (medicine, engineering, academia, corporate law) strictly mandate university credentials and deliver higher career longevity.",
        "band9_vocab": ["tertiary qualification", "debt-free trajectory", "lifetime earnings ceiling", "intellectual rigor", "vocational apprentice"],
        "outline": "Intro -> Body 1 (Merits of early trade entry: debt avoidance, hands-on mastery) -> Body 2 (Benefits of university degrees: specialized qualifications, lifelong networking) -> Opinion/Synthesis -> Conclusion."
    },
    {
        "id": "t2_03",
        "title": "Space Exploration vs Eradicating Terrestrial Poverty",
        "type": "Discuss Both Views & Give Opinion",
        "prompt": "Governments invest billions of dollars into space exploration programs. Some argue that this money would be far better spent tackling urgent terrestrial issues such as poverty, famine, and climate change. Discuss both views and give your opinion.",
        "stance": "While immediate human suffering demands robust state budgets, aerospace funding yields indispensable satellite technology that directly mitigates earthly crises.",
        "ideas": "Critics cite pressing humanitarian emergencies and crumbling healthcare. Yet space research generated weather observation satellites, GPS agriculture monitoring, water purification tech, and renewable solar advancements that save lives daily.",
        "band9_vocab": ["terrestrial deprivation", "aerospace investment", "spin-off technologies", "existential insurance", "humanitarian imperative"],
        "outline": "Intro -> Body 1 (The moral argument for prioritizing famine relief and poverty eradication) -> Body 2 (Crucial spin-off technologies from space that assist climate monitoring and agriculture) -> Opinion & Conclusion."
    },
    {
        "id": "t2_04",
        "title": "Free Public Healthcare and Preventive Lifestyle Responsibilities",
        "type": "Advantages vs Disadvantages",
        "prompt": "In many countries, healthcare is provided entirely free at the point of delivery through taxpayer funds. Do the advantages of universal free healthcare outweigh its disadvantages?",
        "stance": "Advantages heavily outweigh disadvantages; healthy populations yield higher taxable productivity that offsets systemic costs.",
        "ideas": "Disadvantages: Waitlists, risk of moral hazard and frivolous hospital visits. Advantages: Eliminates catastrophic medical bankruptcies, guarantees early disease detection, ensures social equality.",
        "band9_vocab": ["universal healthcare mandate", "preventative medicine", "medical bankruptcy", "frivolous clinic visits", "social equity"],
        "outline": "Intro (Advantages outweigh disadvantages) -> Body 1 (Disadvantages: long waiting times, public budget strains) -> Body 2 (Decisive advantages: disease prevention, eradication of poverty due to illness, productive labor force) -> Conclusion."
    },
    {
        "id": "t2_05",
        "title": "The Dominance of Global English & Endangered Indigenous Languages",
        "type": "Problem and Solution",
        "prompt": "As English cements its status as the global lingua franca, dozens of regional and indigenous languages face imminent extinction every year. What problems does this cause, and what measures can be taken to preserve linguistic diversity?",
        "stance": "Language loss erodes unique cultural paradigms and traditional ecological knowledge; preservation requires school immersion and digital documentation.",
        "ideas": "Problems: Irreplaceable loss of ancestral folklore, oral histories, and botanical wisdom encoded in vocabulary. Solutions: State-subsidized bilingual education, digital archiving on linguistic databases, rewarding native speaker teachers.",
        "band9_vocab": ["lingua franca", "cultural homogenisation", "indigenous heritage", "linguistic revitalization", "ancestral worldview"],
        "outline": "Intro -> Body 1 (Problems: cultural extinction, severance from historical identity) -> Body 2 (Solutions: early immersion programs, government cultural grants, AI digital recording) -> Conclusion."
    },
    {
        "id": "t2_06",
        "title": "Urban Congestion and Congestion Pricing Schemes",
        "type": "Agree / Disagree (Opinion)",
        "prompt": "The most effective way to eliminate traffic congestion in major cities is to charge high entry fees for private vehicles entering city centers. To what extent do you agree or disagree?",
        "stance": "Partially Agree: Congestion fees reduce non-essential car trips, but they must be paired with world-class public transport to avoid burdening lower-income commuters.",
        "ideas": "London and Singapore showed 20-30% drops in traffic from congestion tolls. However, without clean, affordable metros and cycling infrastructure, tolls act as an unfair regressive tax on poorer workers.",
        "band9_vocab": ["congestion pricing zone", "regressive financial penalty", "gridlock alleviation", "multi-modal transit", "deterrent mechanism"],
        "outline": "Intro -> Body 1 (Why entry charges succeed as an economic deterrent to unnecessary journeys) -> Body 2 (Why charges fail if reliable public transport alternatives are lacking) -> Conclusion."
    },
    {
        "id": "t2_07",
        "title": "Social Media and Teenage Psychological Well-being",
        "type": "Discuss Both Views & Give Opinion",
        "prompt": "Some people believe that social media platforms enrich adolescent connectivity and peer collaboration, while others argue that they are the primary driver of adolescent mental health crises. Discuss both views and give your opinion.",
        "stance": "While online communities offer marginalized youth social support, algorithmic addiction loops and unrealistic beauty comparisons pose catastrophic mental risks that outweigh benefits.",
        "ideas": "Pros: Global interest groups, collaborative study networks. Cons: Cyberbullying, sleep deprivation from endless scrolling, dopamine depletion, soaring anxiety and depression rates.",
        "band9_vocab": ["algorithmic addiction", "dopamine manipulation", "unrealistic physical standards", "digital peer support", "cyberbullying epidemic"],
        "outline": "Intro -> Body 1 (Positive aspects: creative expression, remote peer groups) -> Body 2 (Severe hazards: algorithmic echo chambers, sleep loss, depression) -> Author's weighted opinion -> Conclusion."
    },
    {
        "id": "t2_08",
        "title": "Tourism: Economic Lifeline vs Environmental Degradation",
        "type": "Discuss Both Views & Give Opinion",
        "prompt": "International tourism brings vital foreign revenue to developing nations, yet it often causes severe ecological and cultural damage. Discuss both views and give your opinion.",
        "stance": "Tourism revenue is essential, but governments must implement strict tourist caps and eco-taxes to preserve vulnerable natural assets.",
        "ideas": "Benefits: Hospitality employment, foreign currency inflow, infrastructure upgrades. Hazards: Plastic pollution, coral reef bleaching, inflated living costs for locals.",
        "band9_vocab": ["ecotourism sustainability", "carrying capacity", "foreign exchange earnings", "cultural commodification", "ecological footprint"],
        "outline": "Intro -> Body 1 (Economic benefits: jobs, regional investment) -> Body 2 (Environmental and cultural costs: pollution, gentrification) -> Opinion (Regulated ecotourism with entry quotas) -> Conclusion."
    },
    {
        "id": "t2_09",
        "title": "Compulsory Physical Education in Secondary Curricula",
        "type": "Agree / Disagree (Opinion)",
        "prompt": "Because childhood obesity is escalating worldwide, physical education should be made compulsory for all secondary school students until graduation. To what extent do you agree or disagree?",
        "stance": "Strongly Agree: Compulsory physical education combats sedentary lifestyles and enhances academic performance by stimulating brain oxygenation.",
        "ideas": "Sedentary screen time drives juvenile diabetes and postural disorders. Daily structured sports instill cardiovascular endurance, stress relief, teamwork, and lifelong fitness habits.",
        "band9_vocab": ["sedentary lifestyle", "cardiovascular stamina", "juvenile obesity", "cognitive alertness", "mandatory physical syllabus"],
        "outline": "Intro -> Body 1 (Health necessity: counteracting screen addiction and lifestyle diseases) -> Body 2 (Academic and psychological benefits: reduced anxiety, improved concentration) -> Conclusion."
    },
    {
        "id": "t2_10",
        "title": "Preservation of Historic Architecture vs Modern High-Density Housing",
        "type": "Discuss Both Views & Give Opinion",
        "prompt": "In growing metropolises, some advocate demolishing aging historic structures to construct affordable high-rise apartments, while others insist historic buildings should be preserved at all costs. Discuss both views and give your opinion.",
        "stance": "Preserve key heritage landmarks through adaptive reuse, while building modern high-rises on designated brownfield and suburban plots.",
        "ideas": "Housing advocates point to severe rent crises and urban homelessness. Preservationists emphasize irreplaceable cultural identity and architectural soul.",
        "band9_vocab": ["adaptive reuse", "architectural heritage", "housing affordability crisis", "high-density urbanization", "cultural homogenization"],
        "outline": "Intro -> Body 1 (Urgent need for high-density modern housing) -> Body 2 (Invaluable historical and aesthetic identity preserved in ancient architecture) -> Opinion (Adaptive reuse inside historic facades) -> Conclusion."
    },
    {
        "id": "t2_11",
        "title": "Consumer Society: Disposable Convenience vs Global Plastic Pollution",
        "type": "Problem and Solution",
        "prompt": "The widespread consumption of single-use disposable packaging has created an environmental crisis in oceans and landfills. What are the causes of this trend, and what effective solutions can be adopted?",
        "stance": "Root causes lie in corporate cost-cutting and consumer impatience; solutions demand bans on virgin plastics and extended producer responsibility laws.",
        "ideas": "Causes: Plastic is cheap to manufacture; busy lifestyles prioritize disposable food containers. Solutions: Mandatory biodegradable packaging, deposit return schemes for bottles, taxing virgin polymers.",
        "band9_vocab": ["single-use polymer", "extended producer responsibility", "consumerist convenience", "biodegradable alternative", "deposit-refund scheme"],
        "outline": "Intro -> Body 1 (Underlying causes: fast-paced urban lifestyle, cheap petrochemical packaging) -> Body 2 (Pragmatic solutions: legislation, container deposit return schemes, green taxation) -> Conclusion."
    },
    {
        "id": "t2_12",
        "title": "Remote Working: Permanent Evolution or Passing Trend?",
        "type": "Advantages vs Disadvantages",
        "prompt": "Following advancements in telecommunications, many companies now allow employees to work from home permanently. Do the advantages of remote working outweigh its disadvantages?",
        "stance": "Advantages decisively outweigh disadvantages; saved commute hours and flexibility boost productivity and lower carbon emissions.",
        "ideas": "Cons: Isolation, difficulty onboarding junior staff, blurred work-life boundaries. Pros: Eradication of 2-hour daily commutes, lower company overheads, wider geographic talent pool.",
        "band9_vocab": ["telecommuting flexibility", "arduous daily commute", "corporate overhead reduction", "work-life demarcation", "asynchronous collaboration"],
        "outline": "Intro (Advantages outweigh disadvantages) -> Body 1 (Drawbacks: social disconnection, blurred home-work boundaries) -> Body 2 (Major advantages: time reclaimed, environmental savings, superior talent hiring) -> Conclusion."
    },
    {
        "id": "t2_13",
        "title": "Government Subsidies for Creative Arts vs Practical Scientific Research",
        "type": "Discuss Both Views & Give Opinion",
        "prompt": "Some argue that state funding should be allocated exclusively to science, technology, engineering, and mathematics (STEM), while others believe that the visual arts, theater, and music deserve equal governmental support. Discuss both views and give your opinion.",
        "stance": "While STEM drives technological and economic prosperity, the arts nourish cultural empathy and critical philosophical thinking, warranting proportional state patronage.",
        "ideas": "STEM produces medical breakthroughs and green energy. The arts foster national heritage, mental wellness, and creative problem solving in children.",
        "band9_vocab": ["scientific breakthrough", "state patronage", "cultural preservation", "cross-disciplinary creativity", "societal enrichment"],
        "outline": "Intro -> Body 1 (Why STEM funding is critical for national economic and medical progress) -> Body 2 (Why the creative arts are indispensable for civil society and cultural legacy) -> Opinion & Conclusion."
    },
    {
        "id": "t2_14",
        "title": "The Impact of E-Commerce on Traditional Town Centers",
        "type": "Problem and Solution",
        "prompt": "The rapid growth of online shopping has led to the closure of physical retail stores and the decline of traditional town centers. What problems does this cause, and how can city councils revitalize high streets?",
        "stance": "Store closures create ghost towns and eliminate entry-level jobs; high streets must transition into social, dining, and cultural experience hubs.",
        "ideas": "Problems: Vacant shopfronts attract vandalism, local tax revenues fall, elderly lose social contact. Solutions: Lower property taxes for experiential businesses (cafes, galleries, artisan workshops), pedestrianizing plazas.",
        "band9_vocab": ["brick-and-mortar storefront", "e-commerce ascendancy", "urban decay", "pedestrianized community hub", "experiential retail"],
        "outline": "Intro -> Body 1 (Negative consequences of retail closures: empty high streets, social isolation) -> Body 2 (Strategies for council revitalization: pedestrian zones, artisan cafes, municipal arts centers) -> Conclusion."
    },
    {
        "id": "t2_15",
        "title": "Fast Fashion and Environmental Waste",
        "type": "Agree / Disagree (Opinion)",
        "prompt": "Consumers are purchasing more garments and discarding them faster than ever before. Some argue that fashion brands should be legally mandated to pay for the recycling of their garments. To what extent do you agree or disagree?",
        "stance": "Strongly Agree: Fashion brands generate millions of tons of synthetic microplastic waste and must bear full lifecycle accountability.",
        "ideas": "Synthetic clothes (polyester) take 200 years to decompose in landfills and release microplastics into waterways. Forcing brands to fund textile recycling incentivizes higher garment durability.",
        "band9_vocab": ["fast-fashion paradigm", "synthetic textile degradation", "microplastic contamination", "circular textile economy", "producer accountability"],
        "outline": "Intro -> Body 1 (The environmental catastrophe of cheap disposable clothing) -> Body 2 (Why holding corporations financially accountable forces durable and recyclable design) -> Conclusion."
    },
    {
        "id": "t2_16",
        "title": "Cashless Societies: Digital Convenience vs Financial Vulnerability",
        "type": "Discuss Both Views & Give Opinion",
        "prompt": "More countries are transitioning toward completely cashless societies where all transactions occur digitally. Discuss the advantages and disadvantages of this trend, and give your opinion.",
        "stance": "Cashless payments accelerate economic efficiency and curtail tax evasion, but states must maintain cash fail-safes to protect the unbanked and elderly.",
        "ideas": "Advantages: Speed, reduction in armed bank robberies, automated accounting. Disadvantages: Cybersecurity failures during blackouts, exclusion of elderly and homeless citizens.",
        "band9_vocab": ["cashless transaction", "unbanked demographic", "fiscal transparency", "cybersecurity vulnerability", "financial inclusion"],
        "outline": "Intro -> Body 1 (Key advantages: transactional convenience, fraud reduction) -> Body 2 (Significant risks: system blackouts, privacy erosion, exclusion of marginalized groups) -> Opinion & Conclusion."
    },
    {
        "id": "t2_17",
        "title": "Youth Crime: Retributive Imprisonment vs Community Rehabilitation",
        "type": "Discuss Both Views & Give Opinion",
        "prompt": "Some believe that juvenile offenders should receive identical custodial prison sentences as adults to deter crime, while others argue that rehabilitation and education are more effective. Discuss both views and give your opinion.",
        "stance": "Rehabilitation, counseling, and vocational schooling prevent recidivism far better than punitive adult incarceration.",
        "ideas": "Imprisoning teens with seasoned adult criminals hardens antisocial tendencies and creates career convicts. Community mentoring addresses root causes like trauma and poverty.",
        "band9_vocab": ["juvenile offender", "recidivism rate", "custodial sentencing", "restorative justice", "rehabilitative intervention"],
        "outline": "Intro -> Body 1 (Argument for harsh custodial deterrence) -> Body 2 (The overwhelming efficacy of educational rehabilitation and psychological counseling) -> Opinion & Conclusion."
    },
    {
        "id": "t2_18",
        "title": "Meat Consumption and Global Greenhouse Gas Emissions",
        "type": "Agree / Disagree (Opinion)",
        "prompt": "To combat global warming and environmental degradation, people should significantly reduce their consumption of meat and animal products. To what extent do you agree or disagree?",
        "stance": "Strongly Agree: Industrial livestock farming generates massive methane emissions, deforestation, and water waste compared to plant-based agriculture.",
        "ideas": "Cattle generate methane, a greenhouse gas 28x more potent than CO2. Clearing the Amazon for soy animal feed destroys carbon sinks. Shifting to plant protein feeds more people using 75% less land.",
        "band9_vocab": ["industrial livestock farming", "methane emission", "deforestation footprint", "plant-based protein transition", "land-use efficiency"],
        "outline": "Intro -> Body 1 (Environmental destructiveness of beef production: methane and land clearing) -> Body 2 (Nutritional viability and ecological savings of plant-centric diets) -> Conclusion."
    },
    {
        "id": "t2_19",
        "title": "Mandatory Retirement Ages vs Working in Senior Years",
        "type": "Discuss Both Views & Give Opinion",
        "prompt": "Some argue that employees should be forced to retire at age 65 to make room for younger generations, while others contend that workers should be permitted to continue working as long as they are competent. Discuss both views and give your opinion.",
        "stance": "Workers should be evaluated on competence rather than arbitrary chronological age, ensuring seasoned mentorship without blocking youth.",
        "ideas": "Forced retirement deprives companies of institutional memory and damages senior mental health. However, progressive phased-retirement models allow seniors to mentor younger successors.",
        "band9_vocab": ["mandatory retirement threshold", "institutional wisdom", "chronological age discrimination", "phased retirement", "generational succession"],
        "outline": "Intro -> Body 1 (Arguments for mandatory retirement: opening promotional ladders for youth) -> Body 2 (Arguments for voluntary continuation: intellectual capability, economic independence) -> Opinion (Phased mentoring roles) -> Conclusion."
    },
    {
        "id": "t2_20",
        "title": "International Aid: Financial Donations vs Technological and Educational Transfer",
        "type": "Discuss Both Views & Give Opinion",
        "prompt": "Rich nations should provide aid to developing countries through direct monetary grants, while others argue that transferring technology, clean energy, and educational infrastructure is far more effective. Discuss both views and give your opinion.",
        "stance": "Direct monetary aid frequently fuels corruption; technological and infrastructural partnerships cultivate sustainable, self-sufficient economic autonomy.",
        "ideas": "Cash aid easily vanishes into bureaucratic embezzlement and creates debt traps. Transferring renewable energy grids, agricultural machinery, and universities builds permanent self-reliance.",
        "band9_vocab": ["sustainable autonomy", "bureaucratic embezzlement", "dependency syndrome", "technology transfer", "infrastructure endowment"],
        "outline": "Intro -> Body 1 (Benefits and pitfalls of direct financial donations) -> Body 2 (Superior long-term advantages of knowledge and technological capacity building) -> Opinion & Conclusion."
    },
    {
        "id": "t2_21",
        "title": "Standardized Testing in School Admissions",
        "type": "Advantages vs Disadvantages",
        "prompt": "Standardized tests such as the SAT and national university entrance exams are widely used to assess students for university admissions. Do the advantages of standardized testing outweigh its disadvantages?",
        "stance": "Advantages outweigh disadvantages when complemented by holistic reviews: standardized tests provide an objective, merit-based metric across diverse high schools.",
        "ideas": "Criticisms: High-income students can afford expensive private tutoring. Strengths: Eliminates grade inflation in schools and enables gifted students from rural or underprivileged backgrounds to prove academic merit objectively.",
        "band9_vocab": ["standardized metric", "merit-based evaluation", "grade inflation", "socioeconomic disparity", "objective academic benchmark"],
        "outline": "Intro (Advantages outweigh disadvantages with holistic context) -> Body 1 (Disadvantages: commercial test prep advantages, test anxiety) -> Body 2 (Decisive advantages: combating corrupt grading, nationwide equal-footing standard) -> Conclusion."
    }
]

print(f"Loaded: SAT Mock: {len(sat_cleaned)}, IELTS Listening: {len(ielts_listening)}, IELTS Reading: {len(ielts_reading)}, Writing T1: {len(writing_task1_topics)}, Writing T2: {len(writing_task2_topics)}")

# Write to a JSON data bundle so the Mini App HTML can render it fast and interactively
data_bundle = {
    "sat": sat_cleaned,
    "ielts_listening": ielts_listening,
    "ielts_reading": ielts_reading,
    "ielts_writing_t1": writing_task1_topics,
    "ielts_writing_t2": writing_task2_topics
}

with open(BASE_DIR / "webapp" / "exam_bank.json", "w", encoding="utf-8") as f:
    json.dump(data_bundle, f, ensure_ascii=False, indent=2)

print("exam_bank.json generated successfully!")
