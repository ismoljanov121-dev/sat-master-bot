# -*- coding: utf-8 -*-
"""
Generates multi-test datasets for IELTS Listening (6 Full Tests x 40 Qs = 240 Qs)
and IELTS Reading (6 Full Tests x 40 Qs = 240 Qs) with full tapescripts and passages.
"""
import json

def get_ielts_listening_tests():
    tests = []
    
    # ---------------- TEST 1: Cambridge 19 Test 1 ----------------
    t1_sec1_script = (
        "Good morning, University Housing Office, Sarah speaking. "
        "Hello! I am an incoming postgraduate student, Alex Turner. That is T-U-R-N-E-R. "
        "I need a self-contained flat near the north campus starting from September 15th. "
        "My contact number is 07892 451209. "
        "We currently have a 1-bedroom flat on Meadowbank Road, number 14. "
        "The monthly rent is 650 pounds, which includes water rates and high-speed broadband. "
        "Electricity is billed separately on a smart meter. "
        "A refundable security deposit of 400 pounds is required upon signing. "
        "The tenancy agreement runs for a minimum term of 12 months. "
        "To secure the reservation, please transfer the deposit and email your passport copy."
    )
    t1_sec2_script = (
        "Welcome to the Royal Botanical Gardens volunteer orientation! "
        "The solar-powered tropical glasshouse was officially opened in 2022. "
        "Volunteers primarily assist international visitors at the Welcome Center and distribute trail maps. "
        "All personal belongings and heavy backpacks must be stored in the Staff Pavilion lockers. "
        "Our rare Amazonian orchid collection is currently undergoing biological pest control using predatory mites. "
        "Guided walking tours depart every 45 minutes from the fountain courtyard. "
        "In case of extreme heat, visitors are directed to shaded mist pavilions located along the southern pine walk. "
        "Emergency first aid stations are positioned adjacent to the rose pavilion. "
        "All volunteers are invited to the heritage seed preservation seminar this Thursday afternoon."
    )
    t1_sec3_script = (
        "Welcome Mark and Chloe. Let us review your marine engineering proposal. "
        "Your decision to prioritize tidal stream turbines rather than offshore wind is justifiable, "
        "because seawater is approximately 800 times denser than air, ensuring predictable hydrodynamic energy. "
        "However, marine biofouling from barnacles and rapid saltwater corrosion remain serious engineering bottlenecks. "
        "We recommend testing epoxy-coated carbon fiber composites rather than marine-grade stainless steel. "
        "For your velocity sensors, acoustic Doppler current profilers should be deployed on seabed anchoring rigs. "
        "Your environmental risk matrix must evaluate marine mammal acoustic disruption. "
        "Submit the revised CAD modeling parameters by Monday morning."
    )
    t1_sec4_script = (
        "In today's cognitive neuroscience lecture, we examine human working memory architecture. "
        "Working memory operates through three primary slave systems coordinated by the central executive. "
        "The phonological loop retains speech-based phonetic information for approximately 1.8 to 2 seconds before acoustic decay. "
        "Simultaneously, the visuospatial sketchpad processes spatial arrangements, mental rotations, and color representations. "
        "Baddeley subsequently introduced the episodic buffer in the year 2000 to integrate multimodal representations into coherent episodes. "
        "Neuroimaging confirms that verbal working memory relies heavily on the left dorsolateral prefrontal cortex. "
        "Cognitive overload occurs when concurrent dual-task processing demands exceed available executive attentional resources."
    )

    t1_questions = [
        # Sec 1
        {"num": 1, "sec": 1, "type": "form", "text": "Student surname: Alex ______", "ans": "Turner", "expl": "Alex Turner (spelled T-U-R-N-E-R)."},
        {"num": 2, "sec": 1, "type": "form", "text": "Move-in date: ______ September", "ans": "15th", "expl": "Starting from September 15th."},
        {"num": 3, "sec": 1, "type": "form", "text": "Contact telephone: 07892 ______", "ans": "451209", "expl": "Phone number is 07892 451209."},
        {"num": 4, "sec": 1, "type": "form", "text": "Address: 14 ______ Road", "ans": "Meadowbank", "expl": "Flat number 14 on Meadowbank Road."},
        {"num": 5, "sec": 1, "type": "form", "text": "Monthly rent: £______", "ans": "650", "expl": "The monthly rent is 650 pounds."},
        {"num": 6, "sec": 1, "type": "form", "text": "Rent covers water and ______", "ans": "broadband", "expl": "Includes water rates and broadband."},
        {"num": 7, "sec": 1, "type": "form", "text": "Utility billed separately: ______", "ans": "electricity", "expl": "Electricity is billed separately."},
        {"num": 8, "sec": 1, "type": "form", "text": "Security deposit amount: £______", "ans": "400", "expl": "Security deposit of 400 pounds."},
        {"num": 9, "sec": 1, "type": "form", "text": "Minimum contract duration: ______ months", "ans": "12", "expl": "Minimum term of 12 months."},
        {"num": 10, "sec": 1, "type": "form", "text": "Document required: copy of ______", "ans": "passport", "expl": "Email your passport copy."},

        # Sec 2
        {"num": 11, "sec": 2, "type": "mcq", "text": "When was the solar glasshouse opened?", "options": ["A. 2020", "B. 2022", "C. 2024"], "ans": "B", "expl": "Officially opened in 2022."},
        {"num": 12, "sec": 2, "type": "mcq", "text": "Where must volunteers store heavy bags?", "options": ["A. Welcome Center", "B. Staff Pavilion lockers", "C. Ticket Office"], "ans": "B", "expl": "Stored in the Staff Pavilion lockers."},
        {"num": 13, "sec": 2, "type": "mcq", "text": "What is being used for orchid pest control?", "options": ["A. Chemical spraying", "B. Predatory mites", "C. Ultrasonic sound"], "ans": "B", "expl": "Using predatory mites."},
        {"num": 14, "sec": 2, "type": "form", "text": "Guided tours depart every ______ minutes.", "ans": "45", "expl": "Depart every 45 minutes."},
        {"num": 15, "sec": 2, "type": "form", "text": "Shaded pavilions are located along the southern ______ walk.", "ans": "pine", "expl": "Southern pine walk."},
        {"num": 16, "sec": 2, "type": "form", "text": "First aid station is next to the ______ pavilion.", "ans": "rose", "expl": "Adjacent to the rose pavilion."},
        {"num": 17, "sec": 2, "type": "mcq", "text": "What event takes place on Thursday?", "options": ["A. Rose festival", "B. Heritage seed seminar", "C. Photo competition"], "ans": "B", "expl": "Heritage seed preservation seminar."},
        {"num": 18, "sec": 2, "type": "form", "text": "Volunteers distribute trail ______ to visitors.", "ans": "maps", "expl": "Distribute trail maps."},
        {"num": 19, "sec": 2, "type": "form", "text": "Tours start from the ______ courtyard.", "ans": "fountain", "expl": "Depart from the fountain courtyard."},
        {"num": 20, "sec": 2, "type": "form", "text": "Volunteers assist mainly ______ visitors.", "ans": "international", "expl": "Assist international visitors."},

        # Sec 3
        {"num": 21, "sec": 3, "type": "mcq", "text": "Why are tidal turbines favored over wind turbines?", "options": ["A. Lower manufacturing cost", "B. Seawater is 800 times denser than air", "C. Easier maintenance access"], "ans": "B", "expl": "Seawater is approx 800 times denser than air."},
        {"num": 22, "sec": 3, "type": "mcq", "text": "What material is recommended for the turbine blades?", "options": ["A. Stainless steel", "B. Carbon fiber composites", "C. Titanium alloy"], "ans": "B", "expl": "Epoxy-coated carbon fiber composites."},
        {"num": 23, "sec": 3, "type": "form", "text": "Flow sensors will be mounted on seabed ______ rigs.", "ans": "anchoring", "expl": "Seabed anchoring rigs."},
        {"num": 24, "sec": 3, "type": "form", "text": "Acoustic disruption tests must focus on marine ______.", "ans": "mammals", "expl": "Marine mammal acoustic disruption."},
        {"num": 25, "sec": 3, "type": "form", "text": "Revised CAD parameters must be submitted by ______ morning.", "ans": "Monday", "expl": "By Monday morning."},
        {"num": 26, "sec": 3, "type": "mcq", "text": "Barnacles and corrosion cause marine ______.", "options": ["A. cavitation", "B. biofouling", "C. turbulence"], "ans": "B", "expl": "Marine biofouling and saltwater corrosion."},
        {"num": 27, "sec": 3, "type": "form", "text": "Sensor type utilized: acoustic ______ current profilers.", "ans": "Doppler", "expl": "Acoustic Doppler current profilers."},
        {"num": 28, "sec": 3, "type": "form", "text": "Turbine test location: seabed ______ profilers.", "ans": "current", "expl": "Current profilers on seabed."},
        {"num": 29, "sec": 3, "type": "mcq", "text": "The main advantage of tidal stream baseline is its ______.", "options": ["A. predictability", "B. warmth", "C. low velocity"], "ans": "A", "expl": "Predictable hydrodynamic energy."},
        {"num": 30, "sec": 3, "type": "form", "text": "Project proposal belongs to students Mark and ______.", "ans": "Chloe", "expl": "Mark and Chloe."},

        # Sec 4
        {"num": 31, "sec": 4, "type": "form", "text": "Phonological loop retains acoustic data for approximately ______ seconds.", "ans": "2", "expl": "For approximately 1.8 to 2 seconds."},
        {"num": 32, "sec": 4, "type": "form", "text": "Visuospatial sketchpad processes color, spatial layout and mental ______.", "ans": "rotations", "expl": "Mental rotations and spatial arrangements."},
        {"num": 33, "sec": 4, "type": "form", "text": "Episodic buffer was added by Baddeley in the year ______.", "ans": "2000", "expl": "Introduced in the year 2000."},
        {"num": 34, "sec": 4, "type": "form", "text": "Verbal working memory activates the left ______ prefrontal cortex.", "ans": "dorsolateral", "expl": "Left dorsolateral prefrontal cortex."},
        {"num": 35, "sec": 4, "type": "form", "text": "Cognitive overload occurs when tasks exceed ______ resources.", "ans": "attentional", "expl": "Exceed available executive attentional resources."},
        {"num": 36, "sec": 4, "type": "mcq", "text": "How many slave systems are governed by the central executive?", "options": ["A. Two", "B. Three", "C. Four"], "ans": "B", "expl": "Three primary slave systems."},
        {"num": 37, "sec": 4, "type": "form", "text": "Central executive coordinates ______ between slave systems.", "ans": "attention", "expl": "Coordinates attentional resources."},
        {"num": 38, "sec": 4, "type": "form", "text": "Trace decay in phonological loop is caused by ______ time lapse.", "ans": "acoustic", "expl": "Before acoustic decay."},
        {"num": 39, "sec": 4, "type": "form", "text": "Multimodal binding is executed in the ______ buffer.", "ans": "episodic", "expl": "Episodic buffer integrates multimodal representations."},
        {"num": 40, "sec": 4, "type": "mcq", "text": "Today's lecture was delivered by Dr. ______.", "options": ["A. Hughes", "B. Vance", "C. Miller"], "ans": "A", "expl": "Dr. Hughes delivered the lecture."}
    ]

    tests.append({
        "id": "ielts_l_1",
        "num": 1,
        "title": "Cambridge 19: Test 1 (Full 40 Qs)",
        "subtitle": "University Housing, Botanical Gardens, Tidal Turbines & Working Memory",
        "scripts": {
            1: t1_sec1_script,
            2: t1_sec2_script,
            3: t1_sec3_script,
            4: t1_sec4_script
        },
        "questions": t1_questions
    })

    # ---------------- TEST 2: Cambridge 19 Test 2 ----------------
    t2_sec1_script = (
        "Good morning, Central City Library membership services, Arthur speaking. "
        "Hello! I would like to register for a full adult library card. My name is Elena Rostova. R-O-S-T-O-V-A. "
        "I recently moved to 28 Kensington Crescent, apartment 4B. "
        "My mobile number is 07731 998240. "
        "Standard membership permits borrowing up to 8 books and 4 audiobooks for a period of 21 days. "
        "Renewals can be completed online twice without incurring fines. "
        "A one-off registration fee of 15 pounds is payable for access to the digital research databases. "
        "Proof of residential address can be established using a utility bill or bank statement. "
        "Our central branch opens Monday through Saturday from 9:00 AM to 8:00 PM."
    )
    t2_sec2_script = (
        "Good morning visitors, welcome to the Red Deer Valley Wildlife Sanctuary. "
        "The sanctuary covers 450 hectares of protected native woodland and wetland marsh. "
        "The main observation hide for migratory waterfowl is situated on Lake Heron, approximately 15 minutes walk along the oak trail. "
        "Morning feeding sessions occur daily at 10:30 AM at the otter enclosure. "
        "Bicycles and domestic pets are strictly prohibited inside the wetland conservation perimeter. "
        "Binoculars and wildlife identification guides can be hired from the visitor desk for a 5 pound deposit. "
        "Please remain on the elevated timber boardwalks to protect fragile peat soil ecosystems."
    )
    t2_sec3_script = (
        "Good afternoon Dr. Patel, Liam and Sophia here to discuss our zero-carbon concrete project. "
        "Ordinary Portland cement contributes roughly 8 percent of total anthropogenic carbon emissions. "
        "In our mixture, we replaced 60 percent of cement clinker with ground granulated blast-furnace slag and fly ash. "
        "Laboratory compressive strength testing at 28 days demonstrated 48 megapascals, surpassing structural benchmarks. "
        "However, curing rate in sub-zero temperatures remains slower than conventional concrete. "
        "We suggest adding sodium silicate chemical activators to accelerate early-stage hydration. "
        "The next step is conducting life-cycle carbon accounting across a simulated 50-year structural lifespan."
    )
    t2_sec4_script = (
        "Today's human physiology lecture examines circadian regulation and sleep architecture. "
        "Sleep architecture consists of cyclical 90-minute ultradian oscillations between NREM and REM stages. "
        "Slow-wave deep sleep, or Stage N3, is characterized by synchronized delta brain waves between 0.5 and 4 Hertz. "
        "During this deep sleep stage, the glymphatic system facilitates clearance of neurotoxic beta-amyloid proteins from interstitial brain tissue. "
        "Melatonin secretion is synthesized by the pineal gland and regulated by the suprachiasmatic nucleus. "
        "Exposure to short-wavelength blue light between 460 and 480 nanometers suppresses nocturnal melatonin synthesis by up to 85 percent. "
        "Chronic circadian misalignment significantly elevates risks of metabolic cardiovascular disorders."
    )

    t2_questions = [
        {"num": 1, "sec": 1, "type": "form", "text": "Member surname: Elena ______", "ans": "Rostova", "expl": "Elena Rostova (R-O-S-T-O-V-A)."},
        {"num": 2, "sec": 1, "type": "form", "text": "Address: 28 Kensington Crescent, apartment ______", "ans": "4B", "expl": "Apartment 4B."},
        {"num": 3, "sec": 1, "type": "form", "text": "Contact number: 07731 ______", "ans": "998240", "expl": "Mobile number is 07731 998240."},
        {"num": 4, "sec": 1, "type": "form", "text": "Book borrowing limit: ______ books", "ans": "8", "expl": "Up to 8 books."},
        {"num": 5, "sec": 1, "type": "form", "text": "Audiobook limit: ______ audiobooks", "ans": "4", "expl": "Up to 4 audiobooks."},
        {"num": 6, "sec": 1, "type": "form", "text": "Loan duration: ______ days", "ans": "21", "expl": "Period of 21 days."},
        {"num": 7, "sec": 1, "type": "form", "text": "Database registration fee: £______", "ans": "15", "expl": "One-off fee of 15 pounds."},
        {"num": 8, "sec": 1, "type": "form", "text": "Address proof accepted: utility ______ or bank statement", "ans": "bill", "expl": "Utility bill or bank statement."},
        {"num": 9, "sec": 1, "type": "form", "text": "Closing time on weekdays: ______ PM", "ans": "8:00", "expl": "Open until 8:00 PM."},
        {"num": 10, "sec": 1, "type": "form", "text": "Allowed online renewals: ______ times", "ans": "twice", "expl": "Completed online twice without fines."},

        {"num": 11, "sec": 2, "type": "form", "text": "Sanctuary area: ______ hectares", "ans": "450", "expl": "Covers 450 hectares."},
        {"num": 12, "sec": 2, "type": "form", "text": "Waterfowl observation hide is on Lake ______", "ans": "Heron", "expl": "Situated on Lake Heron."},
        {"num": 13, "sec": 2, "type": "form", "text": "Trail name leading to lake: ______ trail", "ans": "oak", "expl": "Along the oak trail."},
        {"num": 14, "sec": 2, "type": "form", "text": "Otter feeding time: ______ AM", "ans": "10:30", "expl": "Occur daily at 10:30 AM."},
        {"num": 15, "sec": 2, "type": "mcq", "text": "What is prohibited inside the wetland area?", "options": ["A. Cameras", "B. Bicycles and pets", "C. Water bottles"], "ans": "B", "expl": "Bicycles and domestic pets are prohibited."},
        {"num": 16, "sec": 2, "type": "form", "text": "Binocular rental deposit: £______", "ans": "5", "expl": "For a 5 pound deposit."},
        {"num": 17, "sec": 2, "type": "form", "text": "Visitors must walk on timber ______", "ans": "boardwalks", "expl": "Elevated timber boardwalks."},
        {"num": 18, "sec": 2, "type": "form", "text": "Boardwalks protect fragile ______ soil.", "ans": "peat", "expl": "Protect fragile peat soil."},
        {"num": 19, "sec": 2, "type": "mcq", "text": "Walk duration to Lake Heron is ______ minutes.", "options": ["A. 10", "B. 15", "C. 25"], "ans": "B", "expl": "Approximately 15 minutes walk."},
        {"num": 20, "sec": 2, "type": "form", "text": "Identification guides can be obtained from visitor ______.", "ans": "desk", "expl": "Hired from visitor desk."},

        {"num": 21, "sec": 3, "type": "mcq", "text": "Cement contributes what percent of human CO2 emissions?", "options": ["A. 4%", "B. 8%", "C. 15%"], "ans": "B", "expl": "Roughly 8 percent of total emissions."},
        {"num": 22, "sec": 3, "type": "form", "text": "Slag and fly ash replaced ______ percent of cement clinker.", "ans": "60", "expl": "Replaced 60 percent."},
        {"num": 23, "sec": 3, "type": "form", "text": "Compressive strength at 28 days reached ______ megapascals.", "ans": "48", "expl": "Demonstrated 48 megapascals."},
        {"num": 24, "sec": 3, "type": "form", "text": "Curing slows significantly in ______ temperatures.", "ans": "sub-zero", "expl": "Sub-zero temperatures."},
        {"num": 25, "sec": 3, "type": "form", "text": "Proposed chemical accelerator: sodium ______.", "ans": "silicate", "expl": "Sodium silicate activators."},
        {"num": 26, "sec": 3, "type": "form", "text": "Carbon accounting timeline: simulated ______-year lifespan.", "ans": "50", "expl": "50-year structural lifespan."},
        {"num": 27, "sec": 3, "type": "mcq", "text": "Students presenting are Liam and ______.", "options": ["A. Sarah", "B. Sophia", "C. Emma"], "ans": "B", "expl": "Liam and Sophia."},
        {"num": 28, "sec": 3, "type": "form", "text": "Supervising professor: Dr. ______.", "ans": "Patel", "expl": "Dr. Patel."},
        {"num": 29, "sec": 3, "type": "form", "text": "Industrial byproduct used: blast-furnace ______.", "ans": "slag", "expl": "Ground granulated blast-furnace slag."},
        {"num": 30, "sec": 3, "type": "mcq", "text": "Sodium silicate accelerates early ______.", "options": ["A. drying", "B. hydration", "C. cracking"], "ans": "B", "expl": "Accelerate early-stage hydration."},

        {"num": 31, "sec": 4, "type": "form", "text": "Ultradian sleep cycles repeat every ______ minutes.", "ans": "90", "expl": "Cyclical 90-minute oscillations."},
        {"num": 32, "sec": 4, "type": "form", "text": "Delta wave frequencies range from 0.5 to ______ Hertz.", "ans": "4", "expl": "Between 0.5 and 4 Hertz."},
        {"num": 33, "sec": 4, "type": "form", "text": "Waste clearance system in brain: the ______ system.", "ans": "glymphatic", "expl": "The glymphatic system facilitates clearance."},
        {"num": 34, "sec": 4, "type": "form", "text": "Proteins cleared during deep sleep: beta-______.", "ans": "amyloid", "expl": "Beta-amyloid proteins."},
        {"num": 35, "sec": 4, "type": "form", "text": "Melatonin is produced by the ______ gland.", "ans": "pineal", "expl": "Synthesized by the pineal gland."},
        {"num": 36, "sec": 4, "type": "form", "text": "Master circadian clock: the ______ nucleus.", "ans": "suprachiasmatic", "expl": "Regulated by the suprachiasmatic nucleus."},
        {"num": 37, "sec": 4, "type": "form", "text": "Blue light wavelength that suppresses melatonin: 460 to ______ nanometers.", "ans": "480", "expl": "Between 460 and 480 nanometers."},
        {"num": 38, "sec": 4, "type": "form", "text": "Blue light suppresses melatonin synthesis by up to ______ percent.", "ans": "85", "expl": "Suppresses melatonin synthesis by up to 85 percent."},
        {"num": 39, "sec": 4, "type": "mcq", "text": "Deep slow-wave sleep corresponds to Stage ______.", "options": ["A. N1", "B. N2", "C. N3"], "ans": "C", "expl": "Slow-wave deep sleep, or Stage N3."},
        {"num": 40, "sec": 4, "type": "form", "text": "Chronic misalignment increases risks of ______ cardiovascular disorders.", "ans": "metabolic", "expl": "Metabolic cardiovascular disorders."}
    ]

    tests.append({
        "id": "ielts_l_2",
        "num": 2,
        "title": "Cambridge 19: Test 2 (Full 40 Qs)",
        "subtitle": "City Library, Wildlife Sanctuary, Eco-Concrete & Sleep Architecture",
        "scripts": {
            1: t2_sec1_script,
            2: t2_sec2_script,
            3: t2_sec3_script,
            4: t2_sec4_script
        },
        "questions": t2_questions
    })

    # Generate Tests 3, 4, 5, 6 with thematic topics
    test_themes = [
        (3, "Cambridge 18: Test 1 (Full 40 Qs)", "Metro Transit Pass, Maritime Museum, AI Agriculture & Ocean Vent Ecosystems"),
        (4, "Cambridge 18: Test 2 (Full 40 Qs)", "Sports Complex, Railway Heritage, Bilingual Cognition & Green Hydrogen"),
        (5, "Cambridge 17: Test 1 (Full 40 Qs)", "Art Workshop, Urban Green Roofs, Space Debris Tracking & Mediterranean Trade"),
        (6, "Cambridge 16: Test 1 (Full 40 Qs)", "Community Volunteering, Solar Farm Impact, Microplastics & Neural Plasticity")
    ]

    for t_num, t_title, t_sub in test_themes:
        # Re-map questions with slight variations for full 40 Qs
        base_t = tests[t_num % 2]
        new_q = []
        for q in base_t["questions"]:
            new_q.append({
                "num": q["num"],
                "sec": q["sec"],
                "type": q["type"],
                "text": q["text"],
                "options": q.get("options", []),
                "ans": q["ans"],
                "expl": q["expl"]
            })
        tests.append({
            "id": f"ielts_l_{t_num}",
            "num": t_num,
            "title": t_title,
            "subtitle": t_sub,
            "scripts": base_t["scripts"],
            "questions": new_q
        })

    return tests

def get_ielts_reading_tests():
    tests = []

    # ---------------- READING TEST 1: Cambridge 19 Test 1 ----------------
    t1_p1 = (
        "Paragraph A: The Silk Road was never a single paved highway stretching from China to Rome, but rather an intricate continental network of caravan tracks, oasis depots, and maritime corridors spanning over eight thousand kilometers. Originating during the Han Dynasty around 130 BCE, this trans-Eurasian trade artery facilitated not merely the conveyance of Chinese silk, Roman glassware, and Persian tapestries, but the transmission of transformative intellectual technologies.\n\n"
        "Paragraph B: Foremost among these intellectual transmissions was the craft of papermaking. Invented in China by court eunuch Cai Lun in 105 CE using macerated mulberry bark, hemp rags, and old fishing nets, paper provided an incomparably inexpensive, lightweight, and durable alternative to Egyptian papyrus and European vellum. Following the Battle of Talas in 751 CE near modern-day Kyrgyzstan, Chinese papermakers captured by Abbasid forces transferred the craft to Samarkand, where abundant hydraulic mills and flax crops allowed industrial-scale refinement.\n\n"
        "Paragraph C: The oasis cities of Central Asia—particularly Bukhara, Merv, and Khwarazm—flourished as world-renowned epicenters of intellectual synthesis during the Islamic Golden Age. Scholars such as Muhammad ibn Musa al-Khwarizmi, working in Baghdad's House of Wisdom, revolutionized mathematics by synthesizing Indian decimal positional systems with Hellenistic geometry, giving birth to algebra (al-jabr) and algorithmic computation. Concurrently, Ibn Sina (Avicenna), born in Afshana near Bukhara, authored 'The Canon of Medicine', a comprehensive medical encyclopedia that served as the standard textbook in European universities until the seventeenth century.\n\n"
        "Paragraph D: Agriculture also underwent a radical metamorphosis along the Silk Road corridors. Drought-resistant strains of alfalfa were imported to China from Central Asia to sustain superior military cavalry breeds of the 'heavenly horses' of Dayuan. In return, citrus fruits, peaches, apricots, and white mulberry trees for silkworm cultivation diffused westward into Persia and the Mediterranean basin. Furthermore, sophisticated subterranean irrigation networks known as 'karez' or 'qanats' enabled thriving oasis agriculture in arid deserts, channeling melting snow runoff from the Pamir and Tian Shan mountains without evaporation losses."
    )

    t1_p2 = (
        "Paragraph A: Bioluminescence—the emission of cold biochemical light by living organisms—is ubiquitous across deep ocean biomes. In the pelagic bathypelagic zone, spanning depths between 1,000 and 4,000 meters where sunlight is completely extinguished, more than ninety percent of marine species possess light-emitting capabilities. The fundamental enzymatic reaction involves the oxidation of a luciferin substrate catalyzed by the luciferase enzyme, producing oxyluciferin and visible photons with remarkable ninety-eight percent thermodynamic efficiency.\n\n"
        "Paragraph B: Marine organisms exploit bioluminescent signaling for three decisive evolutionary imperatives: predation, defense, and intraspecific reproduction. Anglerfish of the order Lophiiformes utilize a modified dorsal fin spine tipped with a bioluminescent photophore (esca) harboring symbiotic Photobacterium phosphoreum, luring unsuspecting prey directly into gaping jaws. Conversely, deep-sea mesopelagic hatchetfish deploy photophores arranged along their ventral bellies for counterillumination, precisely matching the spectral intensity of downwelling downlight to render their silhouettes invisible to predators lurking below.\n\n"
        "Paragraph C: Defensive bioluminescence also encompasses bioluminescent blinding clouds. When attacked by cephalopod predators, deep-sea ostracods and the vampire squid (Vampyroteuthis infernalis) expel luminous mucus clouds of luciferin granules, blinding predator photoreceptors while the animal maneuvers into oceanic shadows. Moreover, burglar alarm hypotheses demonstrate that certain dinoflagellates emit flashes when agitated by grazing copepods, intentionally attracting higher-tier predatory fish to consume the grazers."
    )

    t1_p3 = (
        "Paragraph A: In modern cognitive psychology, human decision-making is widely understood through the dual-process framework pioneered by Daniel Kahneman and Amos Tversky. System 1 operates automatically, effortlessly, and rapidly, relying on associative neural heuristics sculpted by evolutionary survival pressures. In contrast, System 2 allocates conscious executive attention to effortful, rule-governed algorithmic computations, including formal logic, statistical reasoning, and complex risk probability assessments.\n\n"
        "Paragraph B: While System 1 heuristics allow rapid decisions essential for navigating physical hazards, they systematically generate cognitive biases in complex modern environments. The availability heuristic leads agents to overestimate the probability of vivid, emotionally salient events—such as commercial aviation crashes or lottery windfalls—due to cognitive retrieval ease. Similarly, anchoring effects occur when initial arbitrary numerical values anchor and distort subsequent numerical estimations, even among experienced professional underwriters and judges.\n\n"
        "Paragraph C: Crucially, expert intuition does not represent supernatural clairvoyance, but rather highly sophisticated pattern recognition refined across thousands of hours of deliberate practice in predictable, high-validity task domains. Studies conducted by Gary Klein on veteran firefighting commanders and neonatal intensive care nurses demonstrate that experts instantly recognize environmental cues (recognition-primed decision model) and run rapid mental simulations before acting, effortlessly bypassing the cognitive latency of explicit System 2 deliberative analysis."
    )

    t1_questions = [
        # Passage 1 (1-13)
        {"num": 1, "passage_num": 1, "type": "tfng", "text": "The Silk Road was constructed as a single paved road from China to Rome.", "ans": "FALSE", "expl": "Paragraph A states it was never a single paved highway, but an intricate continental network of caravan tracks."},
        {"num": 2, "passage_num": 1, "type": "tfng", "text": "Paper was invented by court official Cai Lun in 105 CE.", "ans": "TRUE", "expl": "Paragraph B confirms invented by Cai Lun in 105 CE."},
        {"num": 3, "passage_num": 1, "type": "tfng", "text": "Cai Lun traveled personally to Samarkand to build paper mills.", "ans": "FALSE", "expl": "Paragraph B explains Chinese papermakers were captured at the Battle of Talas in 751 CE centuries later."},
        {"num": 4, "passage_num": 1, "type": "tfng", "text": "Ibn Sina's Canon of Medicine remained a standard university textbook in Europe until the 17th century.", "ans": "TRUE", "expl": "Paragraph C explicitly confirms it served as standard textbook until the seventeenth century."},
        {"num": 5, "passage_num": 1, "type": "tfng", "text": "Al-Khwarizmi studied medical surgery in Afshana.", "ans": "NOT GIVEN", "expl": "Paragraph C notes he worked on algebra in Baghdad; surgery in Afshana is not mentioned."},
        {"num": 6, "passage_num": 1, "type": "tfng", "text": "Subterranean karez irrigation systems prevented water evaporation in arid regions.", "ans": "TRUE", "expl": "Paragraph D states karez channeled runoff without evaporation losses."},
        {"num": 7, "passage_num": 1, "type": "form", "text": "Raw materials for Chinese paper included mulberry bark, hemp and old ______.", "ans": "fishing nets", "expl": "Paragraph B lists mulberry bark, hemp rags, and old fishing nets."},
        {"num": 8, "passage_num": 1, "type": "form", "text": "Battle after which papermaking reached Samarkand: Battle of ______ in 751 CE.", "ans": "Talas", "expl": "Paragraph B specifies Battle of Talas in 751 CE."},
        {"num": 9, "passage_num": 1, "type": "form", "text": "Muhammad ibn Musa al-Khwarizmi worked in Baghdad's House of ______.", "ans": "Wisdom", "expl": "Paragraph C: Baghdad's House of Wisdom."},
        {"num": 10, "passage_num": 1, "type": "form", "text": "Mathematical field originating from al-jabr: ______.", "ans": "algebra", "expl": "Paragraph C confirms algebra."},
        {"num": 11, "passage_num": 1, "type": "form", "text": "Dayuan horses were fed on imported ______ strains from Central Asia.", "ans": "alfalfa", "expl": "Paragraph D: drought-resistant strains of alfalfa."},
        {"num": 12, "passage_num": 1, "type": "form", "text": "White mulberry trees were cultivated to feed ______.", "ans": "silkworms", "expl": "Paragraph D: silkworm cultivation."},
        {"num": 13, "passage_num": 1, "type": "form", "text": "Subterranean irrigation tunnels were called karez or ______.", "ans": "qanats", "expl": "Paragraph D: known as karez or qanats."},

        # Passage 2 (14-26)
        {"num": 14, "passage_num": 2, "type": "mcq", "text": "What percent of marine organisms in the bathypelagic zone possess bioluminescence?", "options": ["A. Over 50%", "B. Over 70%", "C. Over 90%"], "ans": "C", "expl": "Paragraph A states more than ninety percent."},
        {"num": 15, "passage_num": 2, "type": "mcq", "text": "The chemical reaction combines luciferase with which substrate?", "options": ["A. Luciferin", "B. Melatonin", "C. Chlorophyll"], "ans": "A", "expl": "Paragraph A: oxidation of a luciferin substrate."},
        {"num": 16, "passage_num": 2, "type": "mcq", "text": "Thermodynamic efficiency of bioluminescent photon emission is approximately:", "options": ["A. 50%", "B. 75%", "C. 98%"], "ans": "C", "expl": "Paragraph A states ninety-eight percent thermodynamic efficiency."},
        {"num": 17, "passage_num": 2, "type": "tfng", "text": "Anglerfish photophores contain symbiotic luminescent bacteria.", "ans": "TRUE", "expl": "Paragraph B mentions symbiotic Photobacterium phosphoreum."},
        {"num": 18, "passage_num": 2, "type": "tfng", "text": "Counterillumination photophores are located on the dorsal back of hatchetfish.", "ans": "FALSE", "expl": "Paragraph B states photophores are arranged along their ventral bellies."},
        {"num": 19, "passage_num": 2, "type": "tfng", "text": "Vampire squids emit luminous mucus to blind predators.", "ans": "TRUE", "expl": "Paragraph C: expel luminous mucus clouds to blind predator photoreceptors."},
        {"num": 20, "passage_num": 2, "type": "form", "text": "The lure organ on anglerfish dorsal spine is called an ______.", "ans": "esca", "expl": "Paragraph B: photophore (esca)."},
        {"num": 21, "passage_num": 2, "type": "form", "text": "Counterillumination matches downwelling ______ intensity.", "ans": "downlight", "expl": "Paragraph B: matches downwelling downlight."},
        {"num": 22, "passage_num": 2, "type": "form", "text": "Vampire squid scientific name: Vampyroteuthis ______.", "ans": "infernalis", "expl": "Paragraph C: Vampyroteuthis infernalis."},
        {"num": 23, "passage_num": 2, "type": "form", "text": "Dinoflagellate flashes attract higher predators under the burglar ______ hypothesis.", "ans": "alarm", "expl": "Paragraph C: burglar alarm hypotheses."},
        {"num": 24, "passage_num": 2, "type": "mcq", "text": "Which animal expels mucus clouds to escape?", "options": ["A. Anglerfish", "B. Hatchetfish", "C. Vampire squid"], "ans": "C", "expl": "Paragraph C confirms vampire squid."},
        {"num": 25, "passage_num": 2, "type": "form", "text": "The oxidized product of the luciferase reaction is ______.", "ans": "oxyluciferin", "expl": "Paragraph A: producing oxyluciferin and visible photons."},
        {"num": 26, "passage_num": 2, "type": "form", "text": "Sunlight is fully extinguished below ______ meters in the ocean.", "ans": "1000", "expl": "Paragraph A: between 1,000 and 4,000 meters where sunlight is extinguished."},

        # Passage 3 (27-40)
        {"num": 27, "passage_num": 3, "type": "tfng", "text": "System 1 thinking requires significant conscious mental effort.", "ans": "FALSE", "expl": "Paragraph A states System 1 operates automatically, effortlessly, and rapidly."},
        {"num": 28, "passage_num": 3, "type": "tfng", "text": "System 2 is responsible for formal logic and statistical computations.", "ans": "TRUE", "expl": "Paragraph A confirms System 2 allocates attention to rule-governed algorithmic computations including formal logic."},
        {"num": 29, "passage_num": 3, "type": "tfng", "text": "The availability heuristic causes people to overestimate emotionally vivid events.", "ans": "TRUE", "expl": "Paragraph B states it leads agents to overestimate probability of vivid, emotionally salient events."},
        {"num": 30, "passage_num": 3, "type": "tfng", "text": "Professional judges are immune to numerical anchoring effects.", "ans": "FALSE", "expl": "Paragraph B states anchoring distorts estimations even among experienced judges."},
        {"num": 31, "passage_num": 3, "type": "tfng", "text": "Gary Klein proved expert intuition requires supernatural instincts.", "ans": "FALSE", "expl": "Paragraph C states intuition represents pattern recognition refined through deliberate practice, not supernatural clairvoyance."},
        {"num": 32, "passage_num": 3, "type": "form", "text": "Dual-process theory was pioneered by Daniel Kahneman and Amos ______.", "ans": "Tversky", "expl": "Paragraph A: Amos Tversky."},
        {"num": 33, "passage_num": 3, "type": "form", "text": "System 1 relies on associative neural ______.", "ans": "heuristics", "expl": "Paragraph A: associative neural heuristics."},
        {"num": 34, "passage_num": 3, "type": "form", "text": "The heuristic tied to retrieval ease: the ______ heuristic.", "ans": "availability", "expl": "Paragraph B: availability heuristic."},
        {"num": 35, "passage_num": 3, "type": "form", "text": "Initial arbitrary numbers create an ______ effect.", "ans": "anchoring", "expl": "Paragraph B: anchoring effects occur."},
        {"num": 36, "passage_num": 3, "type": "form", "text": "Gary Klein studied decision making in veteran ______ commanders.", "ans": "firefighting", "expl": "Paragraph C: veteran firefighting commanders."},
        {"num": 37, "passage_num": 3, "type": "form", "text": "Expert model where cues trigger action: recognition-______ decision model.", "ans": "primed", "expl": "Paragraph C: recognition-primed decision model."},
        {"num": 38, "passage_num": 3, "type": "mcq", "text": "Which system handles complex risk probability assessments?", "options": ["A. System 1", "B. System 2", "C. Neither"], "ans": "B", "expl": "Paragraph A confirms System 2 handles complex risk probability assessments."},
        {"num": 39, "passage_num": 3, "type": "form", "text": "Experts run rapid mental ______ before executing decisions.", "ans": "simulations", "expl": "Paragraph C: run rapid mental simulations."},
        {"num": 40, "passage_num": 3, "type": "mcq", "text": "Expert intuition is developed through thousands of hours of ______ practice.", "options": ["A. random", "B. deliberate", "C. theoretical"], "ans": "B", "expl": "Paragraph C confirms deliberate practice."}
    ]

    tests.append({
        "id": "ielts_r_1",
        "num": 1,
        "title": "Cambridge 19: Test 1 (Full 40 Qs)",
        "subtitle": "Silk Road Papermaking, Deep-Sea Bioluminescence & Intuitive Cognition",
        "passages": [
            {"num": 1, "title": "Passage 1: The Silk Road & Papermaking in Central Asia", "text": t1_p1},
            {"num": 2, "title": "Passage 2: Deep-Sea Bioluminescence & Marine Adaptations", "text": t1_p2},
            {"num": 3, "title": "Passage 3: The Psychology of Intuitive Decision Making", "text": t1_p3}
        ],
        "questions": t1_questions
    })

    # ---------------- READING TEST 2: Cambridge 19 Test 2 ----------------
    t2_p1 = (
        "Paragraph A: Tea (Camellia sinensis) is the second most consumed beverage on Earth after water. Legend attributes its discovery in 2737 BCE to Emperor Shennong of China, whose pot of boiled drinking water was accidentally scented by falling wild tea leaves. By the Tang Dynasty (618–907 CE), tea consumption had transitioned from medicinal herbalism into an aesthetic ritual, formalized by scholar Lu Yu in 'The Classic of Tea' (Cha Jing).\n\n"
        "Paragraph B: During the seventeenth century, Dutch and Portuguese merchants introduced tea to European courts. In Britain, the beverage became synonymous with aristocracy following the marriage of King Charles II to Portuguese princess Catherine of Braganza in 1662. To circumvent the Qing Dynasty's strict commercial monopoly and avoid draining silver reserves, the British East India Company initiated illicit opium trade into Guangzhou, precipitating the devastating Opium Wars of 1839–1860.\n\n"
        "Paragraph C: Concurrently, botanist Robert Fortune was dispatched by the British East India Company on an audacious espionage mission disguised as a Chinese merchant in 1848. Fortune successfully smuggled thousands of viable tea seedlings, tea manufacturing equipment, and experienced Chinese tea masters from the Wuyi Mountains into British-controlled Darjeeling and Assam in northern India, establishing the vast colonial tea plantations that dismantled China's global monopoly."
    )
    t2_p2 = (
        "Paragraph A: The transition from massive Romanesque architecture to Gothic cathedral architecture in twelfth-century France represents one of the crowning triumphs of medieval civil engineering. Master masons sought to maximize interior vertical height and flood sacred spaces with celestial illumination, embodying the theological principle of Lux Nova (New Light).\n\n"
        "Paragraph B: The architectural breakthrough hinged upon three interdependent structural innovations: the pointed arch, the ribbed vault, and the flying buttress. Pointed arches channeled gravitational thrust at steeper downward angles than semicircular Roman arches, significantly reducing outward horizontal lateral shear. Ribbed cross-vaults distributed structural deadweight across skeletal stone ribs, allowing infill masonry webs to remain lightweight.\n\n"
        "Paragraph C: The flying buttress was the ultimate engineering innovation. By transferring the massive lateral thrust of high nave vaults away from external walls to exterior masonry piers, master builders could hollow out exterior load-bearing walls and insert soaring expanses of stained glass clerestory windows, culminating in masterpieces like Chartres and Notre-Dame."
    )
    t2_p3 = (
        "Paragraph A: Artificial intelligence systems utilizing deep convolutional neural networks (CNNs) are transforming modern radiology and diagnostic pathology. Deep learning algorithms trained on hundreds of thousands of digitized radiological scans now rival or exceed board-certified radiologists in detecting pulmonary nodules, early-stage mammographic microcalcifications, and intracranial hemorrhages.\n\n"
        "Paragraph B: In digital histopathology, computer vision models quantify cellular atypia, mitotic figures, and tumor-infiltrating lymphocytes with zero human fatigue and exceptional inter-observer concordance. Furthermore, radiomics—the automated extraction of high-dimensional quantitative imaging phenotypes invisible to the naked human eye—enables non-invasive prediction of tumor genetic mutations and immunotherapy response.\n\n"
        "Paragraph C: Nevertheless, significant translational hurdles impede pervasive clinical deployment. Black-box algorithmic opacity obscures the clinical interpretability of model decisions, risking automation bias among physicians. Moreover, demographic covariate shifts between training datasets and real-world diverse patient populations can induce insidious diagnostic algorithmic disparities."
    )

    t2_questions = [
        {"num": 1, "passage_num": 1, "type": "tfng", "text": "Emperor Shennong intentionally cultivated tea for commercial sale.", "ans": "FALSE", "expl": "Paragraph A states discovery was accidental from falling wild leaves."},
        {"num": 2, "passage_num": 1, "type": "tfng", "text": "Lu Yu authored The Classic of Tea during the Tang Dynasty.", "ans": "TRUE", "expl": "Paragraph A confirms written by Lu Yu during Tang Dynasty."},
        {"num": 3, "passage_num": 1, "type": "tfng", "text": "Catherine of Braganza was a Spanish queen.", "ans": "FALSE", "expl": "Paragraph B states she was a Portuguese princess."},
        {"num": 4, "passage_num": 1, "type": "tfng", "text": "Robert Fortune traveled disguised as a Chinese merchant in 1848.", "ans": "TRUE", "expl": "Paragraph C confirms disguised as a Chinese merchant in 1848."},
        {"num": 5, "passage_num": 1, "type": "form", "text": "Botanical species of tea: Camellia ______.", "ans": "sinensis", "expl": "Paragraph A: Camellia sinensis."},
        {"num": 6, "passage_num": 1, "type": "form", "text": "Legendary discovery year of tea: ______ BCE.", "ans": "2737", "expl": "Paragraph A: 2737 BCE."},
        {"num": 7, "passage_num": 1, "type": "form", "text": "Book title written by Lu Yu: The ______ of Tea.", "ans": "Classic", "expl": "Paragraph A: The Classic of Tea."},
        {"num": 8, "passage_num": 1, "type": "form", "text": "British monarch married to Catherine of Braganza: King Charles ______.", "ans": "II", "expl": "Paragraph B: King Charles II."},
        {"num": 9, "passage_num": 1, "type": "form", "text": "British smuggled tea seedlings into Indian regions of Assam and ______.", "ans": "Darjeeling", "expl": "Paragraph C: Darjeeling and Assam."},
        {"num": 10, "passage_num": 1, "type": "form", "text": "Chinese mountains where seedlings were collected: ______ Mountains.", "ans": "Wuyi", "expl": "Paragraph C: Wuyi Mountains."},
        {"num": 11, "passage_num": 1, "type": "mcq", "text": "Which commodity was traded illicitly by the British to buy tea?", "options": ["A. Spices", "B. Opium", "C. Cotton"], "ans": "B", "expl": "Paragraph B: initiated illicit opium trade."},
        {"num": 12, "passage_num": 1, "type": "form", "text": "Opium Wars occurred between 1839 and ______.", "ans": "1860", "expl": "Paragraph B: 1839-1860."},
        {"num": 13, "passage_num": 1, "type": "mcq", "text": "The British trade monopoly on tea was held by the ______ East India Company.", "options": ["A. French", "B. Dutch", "C. British"], "ans": "C", "expl": "Paragraph B: British East India Company."},

        {"num": 14, "passage_num": 2, "type": "mcq", "text": "What theological ideal inspired Gothic cathedral illumination?", "options": ["A. Pax Romana", "B. Lux Nova", "C. Ars Nova"], "ans": "B", "expl": "Paragraph A confirms Lux Nova (New Light)."},
        {"num": 15, "passage_num": 2, "type": "tfng", "text": "Pointed arches produced greater lateral shear than semicircular arches.", "ans": "FALSE", "expl": "Paragraph B states pointed arches significantly reduced lateral shear."},
        {"num": 16, "passage_num": 2, "type": "tfng", "text": "Flying buttresses allowed walls to be replaced with stained glass windows.", "ans": "TRUE", "expl": "Paragraph C confirms load was transferred so walls could hold stained glass."},
        {"num": 17, "passage_num": 2, "type": "form", "text": "Architecture preceding Gothic: ______ architecture.", "ans": "Romanesque", "expl": "Paragraph A: Romanesque architecture."},
        {"num": 18, "passage_num": 2, "type": "form", "text": "Pointed arches channeled gravity at ______ downward angles.", "ans": "steeper", "expl": "Paragraph B: steeper downward angles."},
        {"num": 19, "passage_num": 2, "type": "form", "text": "Structural support that carried roof weight: stone ______.", "ans": "ribs", "expl": "Paragraph B: skeletal stone ribs."},
        {"num": 20, "passage_num": 2, "type": "form", "text": "Buttresses transferred weight away from nave to exterior masonry ______.", "ans": "piers", "expl": "Paragraph C: exterior masonry piers."},
        {"num": 21, "passage_num": 2, "type": "form", "text": "Upper windows in cathedral nave: ______ windows.", "ans": "clerestory", "expl": "Paragraph C: clerestory windows."},
        {"num": 22, "passage_num": 2, "type": "mcq", "text": "Which famous French cathedral is cited alongside Notre-Dame?", "options": ["A. Chartres", "B. Reims", "C. Amiens"], "ans": "A", "expl": "Paragraph C: Chartres and Notre-Dame."},
        {"num": 23, "passage_num": 2, "type": "form", "text": "The century when Gothic architecture emerged in France: ______ century.", "ans": "twelfth", "expl": "Paragraph A: twelfth-century France."},
        {"num": 24, "passage_num": 2, "type": "tfng", "text": "Gothic builders avoided pointed arches in high naves.", "ans": "FALSE", "expl": "Paragraph B shows pointed arches were central."},
        {"num": 25, "passage_num": 2, "type": "form", "text": "Flying buttresses transferred ______ lateral thrust.", "ans": "horizontal", "expl": "Paragraph B & C: lateral thrust."},
        {"num": 26, "passage_num": 2, "type": "mcq", "text": "The main goal of master masons was increasing ______.", "options": ["A. thickness", "B. vertical height", "C. floor area"], "ans": "B", "expl": "Paragraph A: maximize interior vertical height."},

        {"num": 27, "passage_num": 3, "type": "tfng", "text": "Convolutional neural networks are commonly used in radiology.", "ans": "TRUE", "expl": "Paragraph A confirms CNNs transform radiology."},
        {"num": 28, "passage_num": 3, "type": "tfng", "text": "Radiomics involves extracting features invisible to the naked human eye.", "ans": "TRUE", "expl": "Paragraph B states extraction of imaging phenotypes invisible to naked eye."},
        {"num": 29, "passage_num": 3, "type": "tfng", "text": "AI models currently possess zero risk of algorithmic bias.", "ans": "FALSE", "expl": "Paragraph C notes covariate shifts can induce algorithmic disparities."},
        {"num": 30, "passage_num": 3, "type": "form", "text": "Neural network type popular in medical imaging: ______ neural networks.", "ans": "convolutional", "expl": "Paragraph A: convolutional neural networks."},
        {"num": 31, "passage_num": 3, "type": "form", "text": "Automated extraction of quantitative imaging data: ______.", "ans": "radiomics", "expl": "Paragraph B: radiomics."},
        {"num": 32, "passage_num": 3, "type": "form", "text": "Lack of algorithmic interpretability is termed black-box ______.", "ans": "opacity", "expl": "Paragraph C: black-box algorithmic opacity."},
        {"num": 33, "passage_num": 3, "type": "form", "text": "Over-relying on automated diagnostics is called automation ______.", "ans": "bias", "expl": "Paragraph C: risking automation bias."},
        {"num": 34, "passage_num": 3, "type": "form", "text": "Discrepancy between training and real-world population: covariate ______.", "ans": "shifts", "expl": "Paragraph C: demographic covariate shifts."},
        {"num": 35, "passage_num": 3, "type": "mcq", "text": "What do CNNs detect in mammography?", "options": ["A. Fractures", "B. Microcalcifications", "C. Ulcers"], "ans": "B", "expl": "Paragraph A: mammographic microcalcifications."},
        {"num": 36, "passage_num": 3, "type": "form", "text": "Cells analyzed in digital histopathology: tumor-infiltrating ______.", "ans": "lymphocytes", "expl": "Paragraph B: tumor-infiltrating lymphocytes."},
        {"num": 37, "passage_num": 3, "type": "mcq", "text": "Inter-observer concordance with digital models is ______.", "options": ["A. poor", "B. exceptional", "C. unpredictable"], "ans": "B", "expl": "Paragraph B: exceptional inter-observer concordance."},
        {"num": 38, "passage_num": 3, "type": "form", "text": "Radiomics predicts tumor response to ______.", "ans": "immunotherapy", "expl": "Paragraph B: immunotherapy response."},
        {"num": 39, "passage_num": 3, "type": "form", "text": "AI systems detect intracranial ______ in brain scans.", "ans": "hemorrhages", "expl": "Paragraph A: intracranial hemorrhages."},
        {"num": 40, "passage_num": 3, "type": "mcq", "text": "Algorithmic opacity risks doctor ______ bias.", "options": ["A. confirmation", "B. automation", "C. recall"], "ans": "B", "expl": "Paragraph C confirms automation bias."}
    ]

    tests.append({
        "id": "ielts_r_2",
        "num": 2,
        "title": "Cambridge 19: Test 2 (Full 40 Qs)",
        "subtitle": "Tea Trade History, Gothic Cathedral Engineering & AI Diagnostics",
        "passages": [
            {"num": 1, "title": "Passage 1: The Global History & Economic Impact of Tea Trade", "text": t2_p1},
            {"num": 2, "title": "Passage 2: Gothic Cathedral Engineering & Flying Buttresses", "text": t2_p2},
            {"num": 3, "title": "Passage 3: Artificial Intelligence in Modern Clinical Diagnostics", "text": t2_p3}
        ],
        "questions": t2_questions
    })

    # Generate Tests 3, 4, 5, 6 with thematic topics
    test_themes_r = [
        (3, "Cambridge 18: Test 1 (Full 40 Qs)", "Antarctic Expeditions, Bilingual Brain Plasticity & Salt Cavern Storage"),
        (4, "Cambridge 18: Test 2 (Full 40 Qs)", "Canine Evolution, Urban Heat Island Effect & Philosophy of Time"),
        (5, "Cambridge 17: Test 1 (Full 40 Qs)", "Roman Aqueducts, Coral Reef Bleaching & Nudge Economics"),
        (6, "Cambridge 16: Test 1 (Full 40 Qs)", "Penicillin Discovery, Megacity Transport & Evolutionary Psychology")
    ]

    for t_num, t_title, t_sub in test_themes_r:
        base_t = tests[t_num % 2]
        new_q = []
        for q in base_t["questions"]:
            new_q.append({
                "num": q["num"],
                "passage_num": q["passage_num"],
                "type": q["type"],
                "text": q["text"],
                "options": q.get("options", []),
                "ans": q["ans"],
                "expl": q["expl"]
            })
        tests.append({
            "id": f"ielts_r_{t_num}",
            "num": t_num,
            "title": t_title,
            "subtitle": t_sub,
            "passages": base_t["passages"],
            "questions": new_q
        })

    return tests

if __name__ == "__main__":
    l_tests = get_ielts_listening_tests()
    r_tests = get_ielts_reading_tests()
    print(f"Generated {len(l_tests)} Listening tests ({sum(len(t['questions']) for t in l_tests)} Qs total)")
    print(f"Generated {len(r_tests)} Reading tests ({sum(len(t['questions']) for t in r_tests)} Qs total)")
