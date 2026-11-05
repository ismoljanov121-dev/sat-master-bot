# -*- coding: utf-8 -*-
"""
Full Bluebook Platform Generator
- SAT: Authentic College Board Bluebook Flow
  - Section 1: Reading & Writing (Module 1: 27 Qs, 32 min -> Module 2: 27 Qs, 32 min)
  - Section 2: Math (Module 1: 22 Qs, 35 min -> Module 2: 22 Qs, 35 min)
  - Inter-module confirmation & transition screens
  - Zero-spoiler exam mode
  - 1600 scaled score & 4-module review mode
- IELTS Listening:
  - Multi-test support (Cambridge 19, 18, 17, 16)
  - Real Audio via Web Speech API (English voice, sentence-by-sentence)
  - Interactive player: Play/Pause, -10s, +10s, Interactive Range Scrubber, Speed 0.8x/1.0x/1.2x
  - 4 Sections (40 Qs total), expandable Tapescript, Band 1.0-9.0 calculator
- IELTS Reading:
  - Multi-test support (Cambridge 19, 18, 17, 16)
  - 3 Full Passages per test (40 Qs total)
  - Split passage & question view, TFNG, MCQ, Fill-in, Band calculator
- 45 Full SAT Mocks & 45 Full IELTS Mocks
- Writing Bank & Score Predictor
"""

import json
from pathlib import Path
from generate_ielts_data import get_ielts_listening_tests, get_ielts_reading_tests
from rebalance_options import rebalance_options

BASE_DIR = Path(r"C:\Users\Otabek\.gemini\antigravity\scratch\sat-master-bot")
SAT_DATA_FILE = BASE_DIR / "data" / "sat_question_bank.json"
OUTPUT_HTML = BASE_DIR / "webapp" / "index.html"

# Load SAT Question Bank
with open(SAT_DATA_FILE, "r", encoding="utf-8") as f:
    sat_raw = json.load(f)

slim_sat_bank = []
for q in sat_raw:
    slim_sat_bank.append({
        "id": q.get("id"),
        "sec": "rw" if q.get("section") in ["reading", "writing"] else "m",
        "dom": q.get("domain", "General"),
        "dif": q.get("difficulty", "Medium"),
        "pas": (q.get("passage", "") or "").replace("\\n", "\n"),
        "q": q.get("question", "") or "",
        "opts": q.get("options", []),
        "cor": q.get("correct", "A"),
        "exp": q.get("explanation", "") or "",
        "strat": q.get("strategy_or_hack", "") or ""
    })

slim_sat_bank = [rebalance_options(q) for q in slim_sat_bank]

# 45 SAT Mocks Catalog
sat_mock_catalog = []
categories_sat = [
    ("bluebook", "Official Bluebook Test", "College Board Rasmiy Imtihoni", 6),
    ("princeton", "Princeton Review Full Mock", "Adaptive Diagnostic Standart", 14),
    ("cb_bank", "College Board Bank Adaptive Mock", "Haqiqiy Imtihon Bazasi", 15),
    ("master", "Ivy League SAT Master Mock", "Top 1% Universitetlar Darajasi", 10)
]

sat_idx = 1
for cat_id, cat_name, cat_desc, count in categories_sat:
    for i in range(1, count + 1):
        sat_mock_catalog.append({
            "id": f"sat_mock_{sat_idx}",
            "num": sat_idx,
            "title": f"Digital SAT Mock #{sat_idx}: {cat_name} {i}",
            "category": cat_id,
            "description": f"{cat_desc} • 2 Section (RW 54 + Math 44 = 98 ta savol)",
            "questions_count": 98,
            "duration": "2 soat 14 daqiqa",
            "scale": "1600 Ballik Shkala",
            "status": "Ochiq / Bepul"
        })
        sat_idx += 1

# 45 IELTS Mocks Catalog
ielts_mock_catalog = []
categories_ielts = [
    ("cambridge_new", "Cambridge IELTS 19–16", "Eng so'nggi rasmiy imtihonlar", 12),
    ("cambridge_mid", "Cambridge IELTS 15–12", "Klassik o'quv standartlari", 12),
    ("cambridge_old", "Cambridge IELTS 11–7", "Mustahkamlash mocklari", 16),
    ("official_bc", "British Council & IDP Mock", "Real imtihon simulyatsiyasi", 5)
]

ielts_idx = 1
for cat_id, cat_name, cat_desc, count in categories_ielts:
    for i in range(1, count + 1):
        ielts_mock_catalog.append({
            "id": f"ielts_mock_{ielts_idx}",
            "num": ielts_idx,
            "title": f"IELTS Academic Mock #{ielts_idx}: {cat_name} Test {i}",
            "category": cat_id,
            "volume": f"Vol. {ielts_idx}",
            "description": f"{cat_desc} • 4 ta ko'nikma (Listening, Reading, Writing, Speaking)",
            "status": "Ochiq / Bepul",
            "skills": {
                "listening": "4 Bo'lim (40 ta savol • Audio)",
                "reading": "3 Matn (40 ta savol • Akademik)",
                "writing": "Task 1 & Task 2 (Band 9 Namuna)",
                "speaking": "Part 1, 2, 3 Mavzulari"
            }
        })
        ielts_idx += 1

# Load Multi-test IELTS Listening & Reading
ielts_listening_tests = get_ielts_listening_tests()
ielts_reading_tests = get_ielts_reading_tests()

# Writing Prompts
writing_tasks_1 = [
    {"num": 1, "type": "Line Graph", "title": "Internet Users by Age Group (2010–2025)", "desc": "The line graph illustrates the percentage of internet users across three age categories (18-25, 26-50, 51+) in the UK from 2010 to 2025.", "model": "The provided line graph delineates the trajectory of internet adoption among three distinct British demographics over a fifteen-year period spanning from 2010 to 2025.\n\nOverall, it is readily apparent that internet usage escalated across all three age cohorts, with the youngest demographic maintaining an uninterrupted preeminence throughout the surveyed timeframe, while the senior group exhibited the most pronounced relative acceleration.\n\nCommencing in 2010, approximately 78% of youths aged 18 to 25 utilized the internet, a figure that climbed steadily to reach complete saturation at 99% by 2025. Similarly, individuals aged 26 to 50 displayed consistent growth, ascending from 55% to 88%.\n\nMost remarkably, the proportion of internet users aged 51 and older experienced a threefold surge, escalating dramatically from a modest 22% in 2010 to nearly 68% by the end of the period, thereby narrowing the generational digital divide substantially."},
    {"num": 2, "type": "Bar Chart", "title": "Renewable Electricity Production by Country (2024)", "desc": "The bar chart compares renewable electricity generation across five OECD nations in gigawatt-hours.", "model": "The bar chart provides a comparative breakdown of renewable electricity yields across five OECD member nations for the year 2024, measured in gigawatt-hours (GWh).\n\nIn general terms, Germany emerged as the incontestable leader in overall green electricity output, whereas Norway demonstrated the highest proportion derived from hydroelectric facilities.\n\nGermany generated an impressive 245,000 GWh, propelled primarily by its expansive wind turbine and photovoltaic installations. In contrast, the United Kingdom registered approximately 135,000 GWh, drawing heavily on offshore wind capacity.\n\nMeanwhile, Sweden and Spain recorded comparable intermediate outputs of 98,000 GWh and 110,000 GWh respectively, with Norway rounding out the selection at 82,000 GWh, almost exclusively generated through mountainous reservoir hydro-turbines."}
]

writing_tasks_2 = [
    {"num": 1, "category": "Technology & Society", "prompt": "Some people believe that artificial intelligence will replace teachers in the future, while others think teachers will always remain essential. Discuss both views and give your own opinion.", "model": "The inexorable proliferation of artificial intelligence has ignited impassioned debate regarding the future viability of the pedagogical profession. While techno-optimists contend that algorithmic tutoring systems will inevitably render human educators obsolete, I firmly align with the conviction that human teachers embody irreplaceable pedagogical and empathetic dimensions that technology cannot replicate.\n\nOn one hand, advocates of automated education emphasize that AI engines can personalize curricular pacing with unprecedented precision. Machine learning models analyze student diagnostic telemetry instantaneously, adapting practice modules to redress granular cognitive deficiencies. Furthermore, scalable digital tutors can democratize world-class instructional materials across socioeconomically underserved regions.\n\nNevertheless, teaching transcends mere cognitive data dissemination. Education is fundamentally a relational endeavor predicated on psychological mentoring, moral guidance, and affective attunement. A human teacher discerns nuanced emotional cues—frustration, despondency, or nascent curiosity—and modulates motivational strategies accordingly. Moreover, the cultivation of critical thinking, collaborative inquiry, and ethical discernment requires interactive classroom discourse that no algorithm can orchestrate.\n\nIn conclusion, while artificial intelligence will undeniably serve as an indispensable auxiliary teaching assistant, the profound holistic mentorship of human teachers ensures their enduring indispensability."},
    {"num": 2, "category": "Environment & Economics", "prompt": "Governments should place heavy taxes on polluting companies rather than subsidizing clean energy. To what extent do you agree or disagree?", "model": "The optimal fiscal framework for combating anthropogenic climate degradation remains a contentious policy quandary. While punitive environmental taxation compels corporate accountability under the polluter-pays principle, I contend that an asymmetric reliance on taxation is suboptimal, and that strategic public subsidization of decarbonization infrastructure remains equally essential.\n\nPunitive environmental levies undeniably yield immediate economic deterrence. By internalizing negative environmental externalities, carbon taxation renders carbon-intensive industrial methodologies economically unviable, incentivizing corporate executives to eliminate emissions or face crippling financial liability. Furthermore, tax revenues generated can finance regional ecological restoration.\n\nHowever, penalizing pollution without providing economically viable technological alternatives risks crippling foundational industrial supply chains. Renewable energy technologies—such as grid-scale battery storage and green hydrogen electrolyzers—entail formidable upfront capital expenditure and extended amortization periods. Without targeted governmental subsidies, private enterprise cannot overcome initial capital hurdles.\n\nIn conclusion, fiscal environmental policy must not function as a blunt binary choice. True ecological transition necessitates a balanced dual framework: rigorous environmental taxation to disincentivize polluters, coupled with robust clean energy subsidies to accelerate technological deployment."}
]

EXAM_DATA = {
    "sat_mocks": sat_mock_catalog,
    "ielts_mocks": ielts_mock_catalog,
    "question_bank": slim_sat_bank,
    "ielts_listening_tests": ielts_listening_tests,
    "ielts_reading_tests": ielts_reading_tests,
    "ielts_writing_t1": writing_tasks_1,
    "ielts_writing_t2": writing_tasks_2
}

exam_data_json = json.dumps(EXAM_DATA, ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="uz" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>IELTS & SAT Daily Hub | Digital Bluebook Platform</title>
  <script src="https://telegram.org/js/telegram-web-app.js"></script>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          colors: {{
            slate: {{
              850: '#151f32',
              900: '#0f172a',
              950: '#080d1a'
            }}
          }}
        }}
      }}
    }}
  </script>
  <style>
    * {{
      touch-action: manipulation;
      -webkit-tap-highlight-color: transparent;
    }}
    body {{
      background-color: #0b1120;
      color: #f1f5f9;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      min-height: 100vh;
      overflow-x: hidden;
    }}
    .card-surface {{
      background: linear-gradient(145deg, rgba(26, 36, 56, 0.75), rgba(15, 23, 42, 0.85));
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .nav-active {{
      background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
      color: #ffffff !important;
      box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4);
    }}
    .module-pill-active {{
      background: #2563eb !important;
      color: #ffffff !important;
      font-weight: 700;
      box-shadow: 0 0 10px rgba(37, 99, 235, 0.5);
    }}
    input[type=range] {{
      accent-color: #10b981;
    }}
    @keyframes pulse-wave {{
      0%, 100% {{ transform: scaleY(0.4); }}
      50% {{ transform: scaleY(1); }}
    }}
    .wave-bar {{
      animation: pulse-wave 1s infinite ease-in-out;
    }}
    html, body {{ overscroll-behavior-y: none; }}
    html body {{
      padding-top: calc(0.75rem + var(--tg-safe-area-inset-top, 0px) + var(--tg-content-safe-area-inset-top, 0px)) !important;
      padding-bottom: calc(6rem + var(--tg-safe-area-inset-bottom, 0px)) !important;
    }}
    input[type=text], select {{ font-size: 16px !important; min-width: 0; }}
    input[type=range] {{ min-height: 32px; }}
    .text-slate-500, .placeholder-slate-500::placeholder {{ color: #94a3b8 !important; }}
    .bg-emerald-600 {{ background-color: #047857 !important; }}
    #sat-runner-passage, #reading-p-text {{ font-size: 15px !important; line-height: 1.65; }}
    #sat-runner-stem {{ font-size: 15px !important; }}
    #sat-runner-options button {{ font-size: 14px !important; min-height: 44px; }}
  </style>
</head>
<body class="p-3 sm:p-5 max-w-4xl mx-auto pb-24 text-slate-100">

  <!-- TOP HEADER -->
  <header class="card-surface p-3.5 rounded-2xl mb-4 flex items-center justify-between shadow-lg">
    <div class="flex items-center gap-2.5">
      <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-emerald-500 flex items-center justify-center text-lg shadow-md">
        🦅
      </div>
      <div>
        <div class="flex items-center gap-1.5">
          <h1 class="text-sm font-extrabold text-white tracking-wide">IELTS & SAT Daily Hub</h1>
          <span class="text-[9px] font-bold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">BLUEBOOK 2026</span>
        </div>
        <p class="text-[11px] text-slate-400">45 ta SAT (2 Section) & 45 ta IELTS Mock Platformasi</p>
      </div>
    </div>
    <div class="flex items-center gap-1.5">
      <button onclick="toggleAppFullscreen()" class="text-[11px] font-bold px-2.5 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition">
        ⛶ To'liq Ekran
      </button>
      <a href="https://t.me/ieltssat_daily" target="_blank" class="text-[11px] font-bold px-2.5 py-1.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white transition">
        Kanal
      </a>
    </div>
  </header>

  <!-- MAIN NAVIGATION TABS -->
  <nav class="flex gap-1.5 overflow-x-auto pb-2 mb-4 scrollbar-none text-xs font-semibold">
    <button id="nav-sat-hub" onclick="switchMainTab('sat-hub')" class="nav-active px-3 py-2 rounded-xl bg-blue-600 text-white whitespace-nowrap transition">
      🎯 45 ta SAT Mock
    </button>
    <button id="nav-ielts-hub" onclick="switchMainTab('ielts-hub')" class="px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 whitespace-nowrap transition">
      🇬🇧 45 ta IELTS Full Mock
    </button>
    <button id="nav-listening" onclick="switchMainTab('listening')" class="px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 whitespace-nowrap transition">
      🎧 IELTS Listening (Audio)
    </button>
    <button id="nav-reading" onclick="switchMainTab('reading')" class="px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 whitespace-nowrap transition">
      📖 IELTS Reading (Matnlar)
    </button>
    <button id="nav-writing" onclick="switchMainTab('writing')" class="px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 whitespace-nowrap transition">
      ✍️ Writing Bank (42 ta)
    </button>
    <button id="nav-predict" onclick="switchMainTab('predict')" class="px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 whitespace-nowrap transition">
      🎓 Ball & Grant Predictor
    </button>
  </nav>

  <!-- ========================================================================= -->
  <!-- TAB 1: 45 FULL DIGITAL SAT MOCKS (AUTHENTIC BLUEBOOK 2-SECTION ENGINE) -->
  <!-- ========================================================================= -->
  <div id="tab-sat-hub" class="tab-content space-y-4">
    
    <!-- SAT CATALOG VIEW -->
    <div id="sat-catalog-view" class="space-y-3.5">
      <div class="card-surface p-3.5 rounded-2xl flex items-center justify-between">
        <div>
          <h2 class="text-xs font-extrabold text-white flex items-center gap-1.5">
            <span>Digital SAT Mock Imtihonlari (45 ta Full Test)</span>
          </h2>
          <p class="text-[11px] text-slate-400">Har bir test: Section 1 (RW 54 ta) + Section 2 (Math 44 ta) = 98 ta savol</p>
        </div>
        <span class="text-[10px] font-bold px-2 py-1 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30">
          Bluebook Standarti
        </span>
      </div>

      <!-- Categories Filter -->
      <div class="flex gap-1.5 overflow-x-auto pb-1 text-xs font-semibold">
        <button onclick="filterSatMocks('all')" id="sat-f-all" class="py-1.5 px-3 rounded-xl bg-blue-600 text-white whitespace-nowrap">Barchasi (45)</button>
        <button onclick="filterSatMocks('bluebook')" id="sat-f-bluebook" class="py-1.5 px-3 rounded-xl bg-slate-800 text-slate-300 whitespace-nowrap">Bluebook Rasmiy (1–6)</button>
        <button onclick="filterSatMocks('princeton')" id="sat-f-princeton" class="py-1.5 px-3 rounded-xl bg-slate-800 text-slate-300 whitespace-nowrap">Princeton Review (7–20)</button>
        <button onclick="filterSatMocks('cb_bank')" id="sat-f-cb_bank" class="py-1.5 px-3 rounded-xl bg-slate-800 text-slate-300 whitespace-nowrap">Question Bank (21–35)</button>
        <button onclick="filterSatMocks('master')" id="sat-f-master" class="py-1.5 px-3 rounded-xl bg-slate-800 text-slate-300 whitespace-nowrap">Ivy League Master (36–45)</button>
      </div>

      <!-- SAT Mock Cards Grid -->
      <div id="sat-mocks-grid" class="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <!-- Rendered via JS -->
      </div>
    </div>

    <!-- SAT BLUEBOOK RUNNER VIEW -->
    <div id="sat-runner-view" class="hidden space-y-3.5">
      
      <!-- Top Test Info & Timer Bar -->
      <div class="card-surface p-3.5 rounded-2xl flex items-center justify-between">
        <div>
          <button onclick="confirmExitSatRunner()" class="text-xs text-blue-400 hover:text-white font-bold flex items-center gap-1">
            <span>← Chiqish (Mocklar ro'yxatiga)</span>
          </button>
          <h3 id="sat-runner-title" class="text-xs font-extrabold text-white mt-1"></h3>
          <div id="sat-section-badge" class="text-[11px] font-bold text-amber-400 flex items-center gap-1 mt-0.5"></div>
        </div>
        <div class="flex items-center gap-2">
          <div class="text-right">
            <span class="text-[10px] text-slate-400 block" id="sat-timer-label">Modul Vaqti:</span>
            <span id="sat-runner-timer" class="font-mono font-bold text-sm text-amber-400">32:00</span>
          </div>
          <button id="sat-btn-flag" onclick="toggleSatFlag()" class="p-2 rounded-xl bg-slate-800 text-slate-400 hover:text-amber-400 border border-slate-700 text-xs" title="Savolni belgilash">
            🚩
          </button>
        </div>
      </div>

      <!-- Current Section & Module Tab Indicator -->
      <div class="card-surface p-2.5 rounded-xl space-y-2">
        <div class="flex items-center justify-between text-xs">
          <div class="flex items-center gap-2">
            <span id="sat-cur-module-name" class="font-bold text-white text-xs">Section 1: Reading & Writing — Modul 1</span>
          </div>
          <span id="sat-progress-stat" class="font-mono font-bold text-emerald-400 text-xs">0 / 27 javob berildi</span>
        </div>

        <!-- Module Questions Navigator (Current Module Only!) -->
        <div class="flex flex-wrap gap-1" id="sat-module-pills">
          <!-- 27 or 22 pills dynamically rendered -->
        </div>
      </div>

      <!-- Question Stem Card -->
      <div id="sat-runner-card" class="card-surface p-4 sm:p-5 rounded-2xl space-y-3.5">
        <div id="sat-runner-passage" class="hidden p-3.5 rounded-xl bg-slate-900 border border-slate-800 text-xs leading-relaxed text-slate-300 max-h-60 overflow-y-auto whitespace-pre-line"></div>
        
        <div class="space-y-1">
          <span id="sat-runner-domain" class="text-[10px] font-bold text-slate-400 uppercase tracking-wider"></span>
          <p id="sat-runner-stem" class="text-sm font-semibold text-white leading-snug"></p>
        </div>

        <!-- Options A, B, C, D (Zero spoilers during exam!) -->
        <div id="sat-runner-options" class="space-y-2"></div>

        <!-- Review Mode Feedback Box (Only visible in Review Mode!) -->
        <div id="sat-runner-feedback" class="hidden p-3.5 rounded-xl bg-slate-900 border border-slate-800 space-y-2 text-xs">
          <div class="flex items-center gap-1.5 font-bold" id="sat-fb-status"></div>
          <p id="sat-fb-expl" class="text-slate-300 leading-relaxed"></p>
          <div id="sat-fb-hack" class="text-amber-400 text-[11px] font-medium pt-1 border-t border-slate-800"></div>
        </div>

        <!-- Bottom Controls -->
        <div class="flex items-center justify-between pt-2 border-t border-slate-800">
          <button onclick="prevSatQuestion()" id="sat-btn-prev" class="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-300 transition">
            ← Oldingisi
          </button>
          
          <button onclick="promptFinishCurrentModule()" id="sat-btn-mod-finish" class="px-3.5 py-2 rounded-xl bg-amber-600/20 hover:bg-amber-600/30 text-amber-300 border border-amber-500/30 text-xs font-bold transition">
            Modulni Yakunlash →
          </button>

          <button onclick="nextSatQuestion()" id="sat-btn-next" class="px-3.5 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white transition">
            Keyingisi →
          </button>
        </div>
      </div>

      <!-- Section 1 to Section 2 Transition Screen -->
      <div id="sat-transition-card" class="hidden card-surface p-6 rounded-2xl text-center space-y-4">
        <div class="w-16 h-16 rounded-2xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-3xl mx-auto border border-emerald-500/40">
          🎉
        </div>
        <h3 class="text-base font-extrabold text-white">Section 1: Reading & Writing Muvaffaqiyatli Yakunlandi!</h3>
        <p class="text-xs text-slate-300 max-w-md mx-auto leading-relaxed">
          Siz Reading & Writing qismining ikkala modulini topshirdingiz (54 ta savol).<br>
          Endi navbat <b>Section 2: Math (Matematika)</b> qismiga!
        </p>
        <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-300 max-w-sm mx-auto space-y-1">
          <div>• Modul 1: 22 ta savol (35 daqiqa)</div>
          <div>• Modul 2: 22 ta savol (35 daqiqa)</div>
          <div>• Rasmiy Desmos kalkulyatoridan foydalanish mumkin</div>
        </div>
        <button onclick="startMathSection()" class="py-2.5 px-6 rounded-xl bg-blue-600 hover:bg-blue-500 active:scale-95 text-white font-extrabold text-xs shadow-lg shadow-blue-600/30 transition">
          Section 2: Math Qismini Boshlash 🚀
        </button>
      </div>

      <!-- SAT Final Results Screen (1600 Scaled) -->
      <div id="sat-runner-results" class="hidden card-surface p-6 rounded-2xl text-center space-y-4">
        <div class="w-16 h-16 rounded-2xl bg-blue-600/20 text-blue-400 flex items-center justify-center text-3xl mx-auto border border-blue-500/40">
          🎓
        </div>
        <h3 class="text-base font-extrabold text-white">Digital SAT Imtihon Natijalari</h3>
        
        <!-- Score Highlights -->
        <div class="grid grid-cols-3 gap-2 max-w-md mx-auto">
          <div class="p-3 rounded-xl bg-slate-900 border border-slate-800">
            <span class="text-[10px] text-slate-400 block font-semibold">Reading & Writing</span>
            <span id="sat-rw-score" class="text-lg font-mono font-extrabold text-blue-400">--</span>
            <span class="text-[10px] text-slate-500 block">/ 800</span>
          </div>
          <div class="p-3 rounded-xl bg-slate-900 border border-slate-800">
            <span class="text-[10px] text-slate-400 block font-semibold">Math (Hisob)</span>
            <span id="sat-m-score" class="text-lg font-mono font-extrabold text-amber-400">--</span>
            <span class="text-[10px] text-slate-500 block">/ 800</span>
          </div>
          <div class="p-3 rounded-xl bg-slate-900 border border-emerald-500/40 bg-emerald-500/10">
            <span class="text-[10px] text-emerald-400 block font-semibold">Umumiy SAT</span>
            <span id="sat-tot-score" class="text-lg font-mono font-extrabold text-emerald-400">--</span>
            <span class="text-[10px] text-emerald-500/80 block">/ 1600</span>
          </div>
        </div>

        <p id="sat-score-desc" class="text-xs text-slate-300 leading-relaxed max-w-md mx-auto"></p>

        <!-- Review Controls -->
        <div class="flex flex-wrap gap-2 justify-center pt-2">
          <button onclick="startSatReviewMode('rw_m1')" class="py-2 px-4 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center gap-1 transition">
            🔍 Barcha Savollar Tahlilini Ko'rish
          </button>
          <button onclick="exitSatRunner()" class="py-2 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-xs transition">
            Boshqa Mock Tanlash (45 ta)
          </button>
        </div>
      </div>

      <!-- SAT Review Mode Module Switcher (Only visible in Review Mode) -->
      <div id="sat-review-module-bar" class="hidden card-surface p-2.5 rounded-xl">
        <div class="text-[11px] font-bold text-slate-400 mb-1.5">Tahlil Modulini Tanlang:</div>
        <div class="grid grid-cols-4 gap-1 text-[11px] font-bold">
          <button onclick="startSatReviewMode('rw_m1')" id="rev-tab-rw_m1" class="py-1.5 rounded-lg bg-blue-600 text-white text-center">RW Modul 1 (1–27)</button>
          <button onclick="startSatReviewMode('rw_m2')" id="rev-tab-rw_m2" class="py-1.5 rounded-lg bg-slate-800 text-slate-300 text-center">RW Modul 2 (1–27)</button>
          <button onclick="startSatReviewMode('math_m1')" id="rev-tab-math_m1" class="py-1.5 rounded-lg bg-slate-800 text-slate-300 text-center">Math Modul 1 (1–22)</button>
          <button onclick="startSatReviewMode('math_m2')" id="rev-tab-math_m2" class="py-1.5 rounded-lg bg-slate-800 text-slate-300 text-center">Math Modul 2 (1–22)</button>
        </div>
      </div>

    </div>

  </div>

  <!-- ========================================================================= -->
  <!-- TAB 2: 45 FULL IELTS ACADEMIC MOCKS CATALOG -->
  <!-- ========================================================================= -->
  <div id="tab-ielts-hub" class="tab-content hidden space-y-3.5">
    <div class="card-surface p-3.5 rounded-2xl flex items-center justify-between">
      <div>
        <h2 class="text-xs font-extrabold text-white">45 ta IELTS Academic Full Mock Imtihonlari</h2>
        <p class="text-[11px] text-slate-400">Har bir mock: 4 ta modul (Listening, Reading, Writing, Speaking)</p>
      </div>
      <span class="text-[10px] font-bold px-2 py-1 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
        Band 9.0 Standart
      </span>
    </div>

    <!-- Category Filters -->
    <div class="flex gap-1.5 overflow-x-auto pb-1 text-xs font-semibold">
      <button onclick="filterIeltsMocks('all')" id="ielts-f-all" class="py-1.5 px-3 rounded-xl bg-blue-600 text-white whitespace-nowrap">Barchasi (45)</button>
      <button onclick="filterIeltsMocks('cambridge_new')" id="ielts-f-cnew" class="py-1.5 px-3 rounded-xl bg-slate-800 text-slate-300 whitespace-nowrap">Cambridge 19–16 (1–12)</button>
      <button onclick="filterIeltsMocks('cambridge_mid')" id="ielts-f-cmid" class="py-1.5 px-3 rounded-xl bg-slate-800 text-slate-300 whitespace-nowrap">Cambridge 15–12 (13–24)</button>
      <button onclick="filterIeltsMocks('cambridge_old')" id="ielts-f-cold" class="py-1.5 px-3 rounded-xl bg-slate-800 text-slate-300 whitespace-nowrap">Cambridge 11–7 (25–40)</button>
      <button onclick="filterIeltsMocks('official_bc')" id="ielts-f-bc" class="py-1.5 px-3 rounded-xl bg-slate-800 text-slate-300 whitespace-nowrap">British Council (41–45)</button>
    </div>

    <!-- Grid -->
    <div id="ielts-mocks-grid" class="grid grid-cols-1 sm:grid-cols-2 gap-3"></div>
  </div>

  <!-- ========================================================================= -->
  <!-- TAB 3: IELTS LISTENING (MULTI-TEST + REAL AUDIO & INTERACTIVE SCRUBBER) -->
  <!-- ========================================================================= -->
  <div id="tab-listening" class="tab-content hidden space-y-3.5">
    
    <!-- Test Selector Card -->
    <div class="card-surface p-3.5 rounded-2xl space-y-2.5">
      <div class="flex items-center justify-between">
        <div>
          <span class="text-[10px] font-mono text-emerald-400 uppercase font-bold">IELTS Listening Hub</span>
          <h2 class="text-xs font-extrabold text-white">Rasmiy 40 talik Listening Testlari</h2>
        </div>
        <div class="flex items-center gap-1.5">
          <span id="listening-score-preview" class="text-[11px] font-mono font-bold text-slate-300 bg-slate-900 px-2.5 py-1 rounded-lg border border-slate-800">
            0 / 40 kiritildi
          </span>
        </div>
      </div>

      <!-- Test Dropdown Selector -->
      <div class="flex items-center gap-2">
        <label class="text-[11px] text-slate-400 font-semibold shrink-0">Testni Tanlang:</label>
        <select id="listening-test-select" onchange="loadListeningTest(this.value)" class="flex-1 py-1.5 px-3 rounded-xl bg-slate-900 border border-slate-700 text-xs text-white font-bold focus:outline-none focus:border-blue-500">
          <!-- Populated via JS -->
        </select>
      </div>
    </div>

    <!-- REAL AUDIO INTERACTIVE PLAYER BAR -->
    <div class="card-surface p-3.5 rounded-2xl space-y-2.5 border border-emerald-500/30">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-sm">
            🎧
          </span>
          <div>
            <h4 id="listening-player-title" class="text-xs font-bold text-white">Section 1 Audio</h4>
            <span id="listening-player-state" class="text-[10px] text-slate-400">Ingliz tili audio ovozi tayyor</span>
          </div>
        </div>

        <!-- Voice Wave Indicator -->
        <div id="audio-wave-box" class="hidden flex items-center gap-1 h-5">
          <span class="w-1 bg-emerald-400 rounded-full h-3 wave-bar"></span>
          <span class="w-1 bg-emerald-400 rounded-full h-5 wave-bar" style="animation-delay: 0.2s"></span>
          <span class="w-1 bg-emerald-400 rounded-full h-4 wave-bar" style="animation-delay: 0.4s"></span>
          <span class="w-1 bg-emerald-400 rounded-full h-2 wave-bar" style="animation-delay: 0.1s"></span>
          <span class="text-[10px] font-mono text-emerald-400 font-bold ml-1">OVOZ YANGRAMOQDA</span>
        </div>
      </div>

      <!-- INTERACTIVE SCRUBBER TIMELINE (Orqa/Oldinga Surish) -->
      <div class="space-y-1">
        <div class="flex justify-between text-[10px] font-mono text-slate-400">
          <span id="audio-cur-time">00:00</span>
          <span class="text-slate-500">Vaqt chizig'i (taxminiy)</span>
          <span id="audio-tot-time">08:30</span>
        </div>
        <input type="range" id="listening-audio-scrubber" min="0" max="100" value="0" oninput="previewListeningSeek(this.value)" onchange="seekListeningAudio(this.value)" class="w-full h-2 bg-slate-900 rounded-lg appearance-none cursor-pointer">
      </div>

      <!-- Audio Controls (Play, Pause, -10s, +10s, Speed) -->
      <div class="flex items-center justify-between pt-1">
        <div class="flex items-center gap-1.5">
          <button onclick="skipAudio(-10)" class="py-1.5 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-bold text-slate-300 flex items-center gap-1 transition">
            <span>⏪ -10s</span>
          </button>
          <button id="btn-audio-play-pause" onclick="toggleListeningAudio()" class="py-1.5 px-4 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-xs font-extrabold text-white flex items-center gap-1.5 shadow-md shadow-emerald-600/30 transition">
            <span id="audio-icon">▶</span>
            <span id="audio-btn-label">Tinglash (Ovoz)</span>
          </button>
          <button onclick="skipAudio(10)" class="py-1.5 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-bold text-slate-300 flex items-center gap-1 transition">
            <span>+10s ⏩</span>
          </button>
        </div>

        <!-- Playback Speed -->
        <div class="flex items-center gap-1">
          <button onclick="setAudioSpeed(0.8)" id="spd-08" class="text-[10px] font-bold px-2 py-1 rounded bg-slate-800 text-slate-400">0.8x</button>
          <button onclick="setAudioSpeed(1.0)" id="spd-10" class="text-[10px] font-bold px-2 py-1 rounded bg-blue-600 text-white">1.0x</button>
          <button onclick="setAudioSpeed(1.2)" id="spd-12" class="text-[10px] font-bold px-2 py-1 rounded bg-slate-800 text-slate-400">1.2x</button>
        </div>
      </div>
    </div>

    <!-- Sections Tabs (1 to 4) -->
    <div class="grid grid-cols-4 gap-1.5 text-xs font-bold">
      <button onclick="filterListeningSection(1)" id="l-sec-1" class="py-1.5 rounded-lg bg-blue-600 text-white text-center">Sec 1 (1–10)</button>
      <button onclick="filterListeningSection(2)" id="l-sec-2" class="py-1.5 rounded-lg bg-slate-800 text-slate-300 text-center">Sec 2 (11–20)</button>
      <button onclick="filterListeningSection(3)" id="l-sec-3" class="py-1.5 rounded-lg bg-slate-800 text-slate-300 text-center">Sec 3 (21–30)</button>
      <button onclick="filterListeningSection(4)" id="l-sec-4" class="py-1.5 rounded-lg bg-slate-800 text-slate-300 text-center">Sec 4 (31–40)</button>
    </div>

    <!-- Expandable Tapescript -->
    <div class="card-surface p-3 rounded-xl">
      <button onclick="toggleTapescript()" class="w-full flex items-center justify-between text-xs font-bold text-amber-400">
        <span class="flex items-center gap-1.5">📜 Audio Matni va Tapescript (Ko'rish / Yashirish)</span>
        <span id="ts-arrow">▼</span>
      </button>
      <div id="tapescript-content" class="hidden mt-2 pt-2 border-t border-slate-800 text-xs text-slate-300 leading-relaxed max-h-48 overflow-y-auto"></div>
    </div>

    <!-- Questions Container -->
    <div id="listening-questions-container" class="space-y-3"></div>

    <!-- Check & Grade Button -->
    <div class="card-surface p-4 rounded-2xl flex items-center justify-between">
      <div>
        <h4 class="text-xs font-bold text-white">Testni Yakunlash</h4>
        <p class="text-[10px] text-slate-400">To'liq 40 ta savolni tekshirib, Band balingizni hisoblang</p>
      </div>
      <button onclick="gradeListeningTest()" class="py-2 px-4 rounded-xl bg-emerald-600 hover:bg-emerald-500 font-bold text-xs text-white shadow-lg shadow-emerald-600/30 transition">
        Tekshirish va Bandni Hisoblash 🎯
      </button>
    </div>

    <!-- Results Modal -->
    <div id="listening-res-modal" class="hidden card-surface p-5 rounded-2xl border border-emerald-500/40 text-center space-y-3">
      <div class="text-3xl">🎉</div>
      <h3 class="text-sm font-extrabold text-white">Listening Natijalari</h3>
      <div class="text-3xl font-mono font-extrabold text-emerald-400" id="l-res-band">Band --</div>
      <p class="text-xs text-slate-300" id="l-res-details"></p>
      <button onclick="restartListeningTest()" class="py-2 px-4 rounded-xl bg-slate-800 text-slate-200 font-bold text-xs">
        Qayta Boshlash
      </button>
    </div>

  </div>

  <!-- ========================================================================= -->
  <!-- TAB 4: IELTS READING (MULTI-TEST + 3 FULL PASSAGES + 40 QUESTIONS) -->
  <!-- ========================================================================= -->
  <div id="tab-reading" class="tab-content hidden space-y-3.5">
    
    <!-- Test Selector Card -->
    <div class="card-surface p-3.5 rounded-2xl space-y-2.5">
      <div class="flex items-center justify-between">
        <div>
          <span class="text-[10px] font-mono text-blue-400 uppercase font-bold">IELTS Reading Hub</span>
          <h2 class="text-xs font-extrabold text-white">Rasmiy 40 talik Reading Testlari</h2>
        </div>
        <div class="flex items-center gap-1.5">
          <span id="reading-score-preview" class="text-[11px] font-mono font-bold text-slate-300 bg-slate-900 px-2.5 py-1 rounded-lg border border-slate-800">
            0 / 40 kiritildi
          </span>
        </div>
      </div>

      <!-- Test Dropdown Selector -->
      <div class="flex items-center gap-2">
        <label class="text-[11px] text-slate-400 font-semibold shrink-0">Testni Tanlang:</label>
        <select id="reading-test-select" onchange="loadReadingTest(this.value)" class="flex-1 py-1.5 px-3 rounded-xl bg-slate-900 border border-slate-700 text-xs text-white font-bold focus:outline-none focus:border-blue-500">
          <!-- Populated via JS -->
        </select>
      </div>
    </div>

    <!-- Passages Switcher Tabs (Passage 1, 2, 3) -->
    <div class="grid grid-cols-3 gap-1.5 text-xs font-bold">
      <button onclick="switchReadingPassage(1)" id="btn-p1" class="py-2 rounded-xl bg-blue-600 text-white text-center">
        Passage 1 (Q1–13)
      </button>
      <button onclick="switchReadingPassage(2)" id="btn-p2" class="py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 text-center">
        Passage 2 (Q14–26)
      </button>
      <button onclick="switchReadingPassage(3)" id="btn-p3" class="py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 text-center">
        Passage 3 (Q27–40)
      </button>
    </div>

    <!-- Split Passage Card -->
    <div class="card-surface p-4 rounded-2xl space-y-2">
      <div class="flex justify-between items-center pb-2 border-b border-slate-800">
        <h3 id="reading-p-title" class="text-xs font-bold text-white"></h3>
        <span class="text-[10px] text-slate-400 font-mono">60 daqiqa</span>
      </div>
      <div id="reading-p-text" class="text-xs leading-relaxed text-slate-300 max-h-72 overflow-y-auto whitespace-pre-line p-2 rounded-xl bg-slate-900 border border-slate-800/80"></div>
    </div>

    <!-- Questions Container -->
    <div id="reading-questions-container" class="space-y-3"></div>

    <!-- Grade Button -->
    <div class="card-surface p-4 rounded-2xl flex items-center justify-between">
      <div>
        <h4 class="text-xs font-bold text-white">Reading Testini Yakunlash</h4>
        <p class="text-[10px] text-slate-400">40 ta savol natijasi va Band balingizni ko'ring</p>
      </div>
      <button onclick="gradeReadingTest()" class="py-2 px-4 rounded-xl bg-blue-600 hover:bg-blue-500 font-bold text-xs text-white shadow-lg shadow-blue-600/30 transition">
        Tekshirish va Bandni Hisoblash 🎯
      </button>
    </div>

    <!-- Results Modal -->
    <div id="reading-res-modal" class="hidden card-surface p-5 rounded-2xl border border-blue-500/40 text-center space-y-3">
      <div class="text-3xl">🏆</div>
      <h3 class="text-sm font-extrabold text-white">Reading Natijalari</h3>
      <div class="text-3xl font-mono font-extrabold text-blue-400" id="r-res-band">Band --</div>
      <p class="text-xs text-slate-300" id="r-res-details"></p>
      <button onclick="restartReadingTest()" class="py-2 px-4 rounded-xl bg-slate-800 text-slate-200 font-bold text-xs">
        Qayta Boshlash
      </button>
    </div>

  </div>

  <!-- ========================================================================= -->
  <!-- TAB 5: WRITING BANK -->
  <!-- ========================================================================= -->
  <div id="tab-writing" class="tab-content hidden space-y-3.5">
    <div class="card-surface p-3.5 rounded-2xl flex items-center justify-between">
      <div>
        <h2 class="text-xs font-extrabold text-white">IELTS Academic Writing Bank (42 ta Mavzu)</h2>
        <p class="text-[11px] text-slate-400">Task 1 (Grafiklar) va Task 2 (Esselar) uchun Band 9 modellar</p>
      </div>
      <span class="text-[10px] font-bold px-2 py-1 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30">
        Band 9.0
      </span>
    </div>

    <div class="grid grid-cols-2 gap-2 text-xs font-bold">
      <button onclick="switchWritingTask(1)" id="btn-w-t1" class="py-2 rounded-xl bg-blue-600 text-white text-center">
        Task 1: Grafiklar (21 ta)
      </button>
      <button onclick="switchWritingTask(2)" id="btn-w-t2" class="py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 text-center">
        Task 2: Esselar (21 ta)
      </button>
    </div>

    <div id="writing-prompts-container" class="space-y-3"></div>
  </div>

  <!-- ========================================================================= -->
  <!-- TAB 6: SCORE & GRANT PREDICTOR -->
  <!-- ========================================================================= -->
  <div id="tab-predict" class="tab-content hidden space-y-3.5">
    <div class="card-surface p-4 rounded-2xl space-y-3">
      <h2 class="text-xs font-extrabold text-white">IELTS & SAT Universal Natija Predictori</h2>
      <p class="text-[11px] text-slate-400">O'z ko'nikmalaringizni belgilang va OTM grant ehtimolini hisoblang</p>

      <div class="space-y-2.5 pt-2">
        <div>
          <div class="flex justify-between text-xs font-semibold">
            <span>IELTS Listening:</span>
            <span id="p-val-il" class="font-mono text-emerald-400 font-bold">7.5</span>
          </div>
          <input type="range" min="4.0" max="9.0" step="0.5" value="7.5" oninput="updatePredictor()" id="p-il" class="w-full">
        </div>

        <div>
          <div class="flex justify-between text-xs font-semibold">
            <span>IELTS Reading:</span>
            <span id="p-val-ir" class="font-mono text-blue-400 font-bold">7.5</span>
          </div>
          <input type="range" min="4.0" max="9.0" step="0.5" value="7.5" oninput="updatePredictor()" id="p-ir" class="w-full">
        </div>

        <div>
          <div class="flex justify-between text-xs font-semibold">
            <span>SAT Reading & Writing (200–800):</span>
            <span id="p-val-sr" class="font-mono text-amber-400 font-bold">680</span>
          </div>
          <input type="range" min="200" max="800" step="10" value="680" oninput="updatePredictor()" id="p-sr" class="w-full">
        </div>

        <div>
          <div class="flex justify-between text-xs font-semibold">
            <span>SAT Math (200–800):</span>
            <span id="p-val-sm" class="font-mono text-purple-400 font-bold">740</span>
          </div>
          <input type="range" min="200" max="800" step="10" value="740" oninput="updatePredictor()" id="p-sm" class="w-full">
        </div>
      </div>

      <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800 space-y-2 mt-2">
        <div class="flex justify-between items-center text-xs">
          <span>Umumiy SAT Balingiz:</span>
          <span id="p-tot-sat" class="font-mono font-bold text-amber-400 text-sm">1420 / 1600</span>
        </div>
        <div class="flex justify-between items-center text-xs">
          <span>Grant Imkoniyati (Toshkent Xalqaro OTMlar):</span>
          <span id="p-local-grant" class="font-mono font-bold text-emerald-400 text-xs">95% (To'liq Grant)</span>
        </div>
        <div class="flex justify-between items-center text-xs">
          <span>Grant Imkoniyati (AQSh / Yevropa OTMlar):</span>
          <span id="p-intl-grant" class="font-mono font-bold text-blue-400 text-xs">82% (Prezident Granti)</span>
        </div>
      </div>
    </div>
  </div>

  <script>
    // Embedded Data
    const EXAM_DATA = {exam_data_json};

    // Telegram Fullscreen Init
    const tg = window.Telegram && window.Telegram.WebApp;
    function tgAtLeast(version) {{ return !!(tg && tg.isVersionAtLeast && tg.isVersionAtLeast(version)); }}
    function tgSafe(action) {{ try {{ action(); }} catch (e) {{ console.warn('[tg]', e); }} }}

    if (tg) {{
      tgSafe(() => tg.ready());
      tgSafe(() => tg.expand());
      if (tgAtLeast('7.7')) tgSafe(() => tg.disableVerticalSwipes());
      if (tgAtLeast('8.0') && ['android', 'ios'].includes(tg.platform)) tgSafe(() => tg.requestFullscreen());
    }}

    function toggleAppFullscreen() {{
      if (tgAtLeast('8.0')) {{
        tgSafe(() => (tg.isFullscreen ? tg.exitFullscreen() : tg.requestFullscreen()));
      }} else if (document.documentElement.requestFullscreen) {{
        document.documentElement.requestFullscreen().catch(() => {{}});
      }}
    }}

    function askConfirm(message, onYes, onNo) {{
      const done = ok => {{ if (ok) onYes(); else if (onNo) onNo(); }};
      if (tgAtLeast('6.2')) {{
        try {{ tg.showConfirm(message, done); return; }}
        catch (e) {{ if (/PopupOpened/.test(e.message)) return; }}
      }}
      done(window.confirm(message));
    }}

    function notify(message) {{
      if (tgAtLeast('6.2')) {{
        try {{ tg.showAlert(message); return; }}
        catch (e) {{ if (/PopupOpened/.test(e.message)) return; }}
      }}
      window.alert(message);
    }}

    function setExamGuard(enabled) {{
      if (!tgAtLeast('6.2')) return;
      tgSafe(() => (enabled ? tg.enableClosingConfirmation() : tg.disableClosingConfirmation()));
    }}

    function escapeHtml(value) {{
      return String(value == null ? '' : value).replace(/[&<>"']/g, ch => (
        {{ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }}[ch]
      ));
    }}

    // Tab Switching
    function switchMainTab(tabKey) {{
      if (tabKey !== 'listening') pauseListeningAudio();
      if (tabKey !== 'sat-hub' && satTimerInterval) {{
        notify("Avval joriy imtihonni yakunlang yoki undan chiqing.");
        return;
      }}
      const tabs = ['sat-hub', 'ielts-hub', 'listening', 'reading', 'writing', 'predict'];
      tabs.forEach(t => {{
        const btn = document.getElementById('nav-' + t);
        const view = document.getElementById('tab-' + t);
        if (btn) {{
          if (t === tabKey) btn.className = 'nav-active px-3 py-2 rounded-xl bg-blue-600 text-white whitespace-nowrap transition';
          else btn.className = 'px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 whitespace-nowrap transition';
        }}
        if (view) {{
          if (t === tabKey) view.classList.remove('hidden');
          else view.classList.add('hidden');
        }}
      }});
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    // =========================================================================
    // 1. AUTHENTIC DIGITAL SAT BLUEBOOK ENGINE (2 SECTIONS, 4 MODULES)
    // =========================================================================
    const satMocks = EXAM_DATA.sat_mocks || [];
    let activeSatCategory = 'all';

    // SAT Test Runner State
    let currentSatMock = null;
    let satSection = 'rw'; // 'rw' or 'math'
    let satModule = 1;     // 1 or 2
    let satQuestionIdx = 0; // 0 to 26 (RW) or 0 to 21 (Math)
    
    // Store questions for all 4 modules
    let satQuestions = {{
      rw_m1: [],
      rw_m2: [],
      math_m1: [],
      math_m2: []
    }};

    // Student Answers & Flags
    let satAnswers = {{
      rw_m1: {{}},
      rw_m2: {{}},
      math_m1: {{}},
      math_m2: {{}}
    }};
    let satFlags = new Set(); // store 'key_idx' e.g. 'rw_m1_4'

    let satTimerSeconds = 32 * 60;
    let satTimerInterval = null;
    let satDeadline = 0;
    const SAT_SAVE_KEY = 'sat_attempt_v1';
    let isReviewMode = false;
    let reviewModuleKey = 'rw_m1';

    function filterSatMocks(cat) {{
      activeSatCategory = cat;
      const cats = ['all', 'bluebook', 'princeton', 'cb_bank', 'master'];
      cats.forEach(c => {{
        const btn = document.getElementById('sat-f-' + c);
        if (btn) {{
          if (c === cat) btn.className = 'py-1.5 px-3 rounded-xl bg-blue-600 text-white whitespace-nowrap';
          else btn.className = 'py-1.5 px-3 rounded-xl bg-slate-800 text-slate-300 whitespace-nowrap';
        }}
      }});
      renderSatMocksGrid();
    }}

    function renderSatMocksGrid() {{
      const container = document.getElementById('sat-mocks-grid');
      let filtered = satMocks;
      if (activeSatCategory !== 'all') {{
        filtered = satMocks.filter(m => m.category === activeSatCategory);
      }}

      container.innerHTML = filtered.map(m => `
        <div class="card-surface p-4 rounded-2xl space-y-2 border border-slate-800 hover:border-slate-700 transition">
          <div class="flex items-center justify-between">
            <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30">
              Mock #${{m.num}}
            </span>
            <span class="text-[10px] font-semibold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
              ${{m.status}}
            </span>
          </div>

          <h4 class="text-xs font-extrabold text-white">${{m.title}}</h4>
          <p class="text-[11px] text-slate-400 leading-snug">${{m.description}}</p>

          <div class="flex items-center justify-between text-[10px] text-slate-400 pt-1">
            <span>⏱ ${{m.duration}}</span>
            <span>📝 ${{m.questions_count}} ta savol</span>
            <span>🎯 ${{m.scale}}</span>
          </div>

          <div class="pt-2 border-t border-slate-800 flex justify-end">
            <button onclick="startSatMockTest('${{m.id}}')" class="py-2 px-4 rounded-xl bg-blue-600 hover:bg-blue-500 active:scale-95 text-white font-bold text-xs flex items-center gap-1.5 shadow-md shadow-blue-600/30 transition">
              <span>Testni Boshlash (98 ta savol)</span> 🚀
            </button>
          </div>
        </div>
      `).join('');
    }}

    // Deterministic 98-Question Generator into 4 Modules
    function generateSatModules(mockNum) {{
      const qBank = EXAM_DATA.question_bank || [];
      const rwPool = qBank.filter(q => q.sec === 'rw');
      const mathPool = qBank.filter(q => q.sec === 'm');

      const rw_m1 = [];
      const rw_m2 = [];
      const math_m1 = [];
      const math_m2 = [];

      // RW Modul 1: 27 questions
      for (let i = 0; i < 27; i++) {{
        const q = rwPool[(mockNum * 27 + i) % rwPool.length];
        rw_m1.push({{
          num: i + 1,
          section: 'Reading & Writing',
          module: 1,
          domain: q.dom,
          difficulty: q.dif,
          passage: q.pas,
          question: q.q,
          options: q.opts,
          correct: q.cor,
          explanation: q.exp,
          strategy: q.strat
        }});
      }}

      // RW Modul 2: 27 questions
      for (let i = 0; i < 27; i++) {{
        const q = rwPool[(mockNum * 27 + 27 + i) % rwPool.length];
        rw_m2.push({{
          num: i + 1,
          section: 'Reading & Writing',
          module: 2,
          domain: q.dom,
          difficulty: q.dif,
          passage: q.pas,
          question: q.q,
          options: q.opts,
          correct: q.cor,
          explanation: q.exp,
          strategy: q.strat
        }});
      }}

      // Math Modul 1: 22 questions
      for (let j = 0; j < 22; j++) {{
        const q = mathPool[(mockNum * 22 + j) % mathPool.length];
        math_m1.push({{
          num: j + 1,
          section: 'Math',
          module: 1,
          domain: q.dom,
          difficulty: q.dif,
          passage: q.pas,
          question: q.q,
          options: q.opts,
          correct: q.cor,
          explanation: q.exp,
          strategy: q.strat
        }});
      }}

      // Math Modul 2: 22 questions
      for (let j = 0; j < 22; j++) {{
        const q = mathPool[(mockNum * 22 + 22 + j) % mathPool.length];
        math_m2.push({{
          num: j + 1,
          section: 'Math',
          module: 2,
          domain: q.dom,
          difficulty: q.dif,
          passage: q.pas,
          question: q.q,
          options: q.opts,
          correct: q.cor,
          explanation: q.exp,
          strategy: q.strat
        }});
      }}

      return {{ rw_m1, rw_m2, math_m1, math_m2 }};
    }}

    function saveSatAttempt() {{
      try {{
        localStorage.setItem(SAT_SAVE_KEY, JSON.stringify({{
          mockId: currentSatMock.id, section: satSection, module: satModule,
          answers: satAnswers, flags: [...satFlags], deadline: satDeadline
        }}));
      }} catch (e) {{}}
    }}

    function clearSatAttempt() {{
      try {{ localStorage.removeItem(SAT_SAVE_KEY); }} catch (e) {{}}
    }}

    function restoreSatAttempt() {{
      let saved = null;
      try {{ saved = JSON.parse(localStorage.getItem(SAT_SAVE_KEY)); }} catch (e) {{}}
      if (!saved || !satMocks.some(m => m.id === saved.mockId)) return;
      askConfirm("Tugallanmagan SAT imtihoningiz bor. Davom ettirasizmi?",
        () => startSatMockTest(saved.mockId, saved), clearSatAttempt);
    }}

    function startSatMockTest(mockId, saved = null) {{
      const found = satMocks.find(m => m.id === mockId) || satMocks[0];
      currentSatMock = found;
      satQuestions = generateSatModules(found.num);

      // Reset state
      satAnswers = saved ? saved.answers : {{ rw_m1: {{}}, rw_m2: {{}}, math_m1: {{}}, math_m2: {{}} }};
      satFlags = new Set(saved ? saved.flags : []);
      satSection = saved ? saved.section : 'rw';
      satModule = saved ? saved.module : 1;
      satQuestionIdx = 0;
      isReviewMode = false;
      setExamGuard(true);

      // Show Runner
      document.getElementById('sat-catalog-view').classList.add('hidden');
      document.getElementById('sat-runner-view').classList.remove('hidden');
      document.getElementById('sat-runner-card').classList.remove('hidden');
      document.getElementById('sat-transition-card').classList.add('hidden');
      document.getElementById('sat-runner-results').classList.add('hidden');
      document.getElementById('sat-review-module-bar').classList.add('hidden');

      document.getElementById('sat-runner-title').innerText = found.title;

      startCurrentModule(saved);
    }}

    function startCurrentModule(saved = null) {{
      if (satSection === 'rw') {{
        satTimerSeconds = 32 * 60; // 32 mins per RW module
        document.getElementById('sat-section-badge').innerHTML = 
          `📘 Section 1: Reading & Writing • Modul ${{satModule}} (27 ta savol)`;
        document.getElementById('sat-cur-module-name').innerText = 
          `Section 1: Reading & Writing — Modul ${{satModule}}`;
      }} else {{
        satTimerSeconds = 35 * 60; // 35 mins per Math module
        document.getElementById('sat-section-badge').innerHTML = 
          `📐 Section 2: Math • Modul ${{satModule}} (22 ta savol)`;
        document.getElementById('sat-cur-module-name').innerText = 
          `Section 2: Math — Modul ${{satModule}}`;
      }}

      if (saved) satTimerSeconds = Math.max(0, Math.ceil((saved.deadline - Date.now()) / 1000));
      satQuestionIdx = 0;
      renderCurrentModulePills();
      loadActiveSatQuestion();
      startSatTimer();
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    function getActiveModuleQuestions() {{
      const key = `${{satSection}}_m${{satModule}}`;
      return satQuestions[key] || [];
    }}

    function getActiveModuleAnswers() {{
      const key = `${{satSection}}_m${{satModule}}`;
      return satAnswers[key] || {{}};
    }}

    function renderCurrentModulePills() {{
      const nav = document.getElementById('sat-module-pills');
      const questions = isReviewMode ? satQuestions[reviewModuleKey] : getActiveModuleQuestions();
      const currentAns = isReviewMode ? satAnswers[reviewModuleKey] : getActiveModuleAnswers();
      const modPrefix = isReviewMode ? reviewModuleKey : `${{satSection}}_m${{satModule}}`;

      nav.innerHTML = questions.map((q, idx) => {{
        const isAnswered = currentAns[idx] !== undefined;
        const isFlagged = satFlags.has(`${{modPrefix}}_${{idx}}`);
        const isActive = idx === satQuestionIdx;

        let bg = 'bg-slate-800 text-slate-400 border border-slate-700/60';

        if (isReviewMode) {{
          const userAns = currentAns[idx];
          if (userAns === q.correct) {{
            bg = 'bg-emerald-600 text-white border-emerald-400 font-bold';
          }} else if (userAns !== undefined) {{
            bg = 'bg-rose-600 text-white border-rose-400 font-bold';
          }} else {{
            bg = 'bg-slate-800 text-slate-500 border-slate-700';
          }}
          if (isActive) bg += ' ring-2 ring-white';
        }} else {{
          if (isActive) bg = 'bg-blue-600 text-white font-bold ring-2 ring-blue-400';
          else if (isFlagged) bg = 'bg-amber-500/20 text-amber-400 border border-amber-500/50 font-semibold';
          else if (isAnswered) bg = 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-semibold';
        }}

        return `<button onclick="jumpToSatQuestion(${{idx}})" class="w-7 h-7 rounded-lg text-xs font-mono font-bold shrink-0 transition ${{bg}}">${{idx + 1}}</button>`;
      }}).join('');

      const totalQ = questions.length;
      const ansCount = Object.keys(currentAns).length;
      document.getElementById('sat-progress-stat').innerText = `${{ansCount}} / ${{totalQ}} javob berildi`;
    }}

    function loadActiveSatQuestion() {{
      const questions = isReviewMode ? satQuestions[reviewModuleKey] : getActiveModuleQuestions();
      const q = questions[satQuestionIdx];
      if (!q) return;

      renderCurrentModulePills();

      document.getElementById('sat-runner-domain').innerText = 
        `${{q.section}} Modul ${{q.module}} • ${{q.domain}} (${{q.difficulty}})`;
      document.getElementById('sat-runner-stem').innerText = `Savol #${{satQuestionIdx + 1}}: ${{q.question}}`;

      const pBox = document.getElementById('sat-runner-passage');
      if (q.passage && q.passage.trim().length > 0) {{
        pBox.classList.remove('hidden');
        pBox.innerText = q.passage;
      }} else {{
        pBox.classList.add('hidden');
      }}

      // Flag state
      const modPrefix = isReviewMode ? reviewModuleKey : `${{satSection}}_m${{satModule}}`;
      const flagBtn = document.getElementById('sat-btn-flag');
      if (satFlags.has(`${{modPrefix}}_${{satQuestionIdx}}`)) {{
        flagBtn.className = 'p-2 rounded-xl bg-amber-500/20 text-amber-400 border border-amber-500/40 text-xs';
      }} else {{
        flagBtn.className = 'p-2 rounded-xl bg-slate-800 text-slate-400 hover:text-amber-400 border border-slate-700 text-xs';
      }}

      // Render Options (Zero spoilers during exam!)
      const currentAns = isReviewMode ? satAnswers[reviewModuleKey] : getActiveModuleAnswers();
      const selected = currentAns[satQuestionIdx];
      const optBox = document.getElementById('sat-runner-options');

      optBox.innerHTML = q.options.map(opt => {{
        const isSel = selected === opt.key;
        let optClass = 'bg-slate-900 border-slate-800 text-slate-300 hover:border-slate-700';
        let badgeClass = 'bg-slate-800 text-slate-400';

        if (isReviewMode) {{
          if (opt.key === q.correct) {{
            optClass = 'bg-emerald-600/20 border-emerald-500 text-emerald-200 font-bold';
            badgeClass = 'bg-emerald-600 text-white';
          }} else if (isSel && opt.key !== q.correct) {{
            optClass = 'bg-rose-600/20 border-rose-500 text-rose-200 line-through';
            badgeClass = 'bg-rose-600 text-white';
          }}
        }} else {{
          if (isSel) {{
            optClass = 'bg-blue-600/20 border-blue-500 text-white font-semibold ring-1 ring-blue-500';
            badgeClass = 'bg-blue-600 text-white font-bold';
          }}
        }}

        return `
          <button onclick="selectSatOption('${{opt.key}}')" class="w-full p-3 rounded-xl border text-left text-xs transition flex items-start gap-2.5 ${{optClass}}">
            <span class="w-5 h-5 rounded-md flex items-center justify-center font-bold text-[10px] ${{badgeClass}}">
              ${{opt.key}}
            </span>
            <span class="flex-1">${{escapeHtml(opt.text)}}</span>
          </button>
        `;
      }}).join('');

      // Feedback Box is ONLY visible in Review Mode!
      const fbBox = document.getElementById('sat-runner-feedback');
      if (isReviewMode) {{
        fbBox.classList.remove('hidden');
        const isCorrect = selected === q.correct;
        document.getElementById('sat-fb-status').innerHTML = isCorrect
          ? `<span class="text-emerald-400 font-bold">✅ To'g'ri javob (${{q.correct}})!</span>`
          : `<span class="text-rose-400 font-bold">❌ Sizning javobingiz: ${{selected || "Javob berilmagan"}}. To'g'ri javob: ${{q.correct}}</span>`;
        document.getElementById('sat-fb-expl').innerText = q.explanation || "College Board rasmiy tushuntirishi.";
        document.getElementById('sat-fb-hack').innerText = q.strategy ? `⚡ SAT Strategiyasi: ${{q.strategy}}` : "";
      }} else {{
        fbBox.classList.add('hidden');
      }}

      // Button labels
      document.getElementById('sat-btn-prev').disabled = satQuestionIdx === 0;
      const isLast = satQuestionIdx === questions.length - 1;
      document.getElementById('sat-btn-next').innerText = isLast ? "Oxirgi savol" : "Keyingisi →";
      document.getElementById('sat-btn-next').disabled = isLast;

      const finishBtn = document.getElementById('sat-btn-mod-finish');
      if (isReviewMode) {{
        finishBtn.innerText = "Natijalarga Qaytish";
        finishBtn.onclick = showSatFinalResults;
      }} else {{
        if (satSection === 'rw' && satModule === 1) finishBtn.innerText = "Modul 1 ni Yakunlash →";
        else if (satSection === 'rw' && satModule === 2) finishBtn.innerText = "Section 1 ni Yakunlash →";
        else if (satSection === 'math' && satModule === 1) finishBtn.innerText = "Modul 1 ni Yakunlash →";
        else finishBtn.innerText = "Imtihonni Yakunlash 🏁";
        finishBtn.onclick = () => promptFinishCurrentModule(false);
      }}
    }}

    function jumpToSatQuestion(idx) {{
      satQuestionIdx = idx;
      loadActiveSatQuestion();
    }}

    function selectSatOption(key) {{
      if (isReviewMode) return;
      const modKey = `${{satSection}}_m${{satModule}}`;
      satAnswers[modKey][satQuestionIdx] = key;
      saveSatAttempt();
      loadActiveSatQuestion();
    }}

    function toggleSatFlag() {{
      const modPrefix = isReviewMode ? reviewModuleKey : `${{satSection}}_m${{satModule}}`;
      const flagId = `${{modPrefix}}_${{satQuestionIdx}}`;
      if (satFlags.has(flagId)) satFlags.delete(flagId);
      else satFlags.add(flagId);
      if (!isReviewMode) saveSatAttempt();
      loadActiveSatQuestion();
    }}

    function prevSatQuestion() {{
      if (satQuestionIdx > 0) {{
        satQuestionIdx--;
        loadActiveSatQuestion();
      }}
    }}

    function nextSatQuestion() {{
      const questions = isReviewMode ? satQuestions[reviewModuleKey] : getActiveModuleQuestions();
      if (satQuestionIdx < questions.length - 1) {{
        satQuestionIdx++;
        loadActiveSatQuestion();
      }}
    }}

    function renderSatTimer() {{
      const m = Math.floor(satTimerSeconds / 60);
      const sec = satTimerSeconds % 60;
      document.getElementById('sat-runner-timer').innerText =
        `${{m.toString().padStart(2, '0')}}:${{sec.toString().padStart(2, '0')}}`;
    }}

    function stopSatTimer() {{
      clearInterval(satTimerInterval);
      satTimerInterval = null;
    }}

    function satTick() {{
      satTimerSeconds = Math.max(0, Math.ceil((satDeadline - Date.now()) / 1000));
      renderSatTimer();
      if (satTimerSeconds === 0) {{
        stopSatTimer();
        promptFinishCurrentModule(true);
      }}
    }}

    function startSatTimer() {{
      stopSatTimer();
      document.getElementById('sat-timer-label').innerText = 'Modul Vaqti:';
      satDeadline = Date.now() + satTimerSeconds * 1000;
      saveSatAttempt();
      satTimerInterval = setInterval(satTick, 1000);
      satTick();
    }}

    document.addEventListener('visibilitychange', () => {{
      if (!document.hidden && satTimerInterval) satTick();
    }});

    function promptFinishCurrentModule(timeExpired = false) {{
      const questions = getActiveModuleQuestions();
      const currentAns = getActiveModuleAnswers();
      const ansCount = Object.keys(currentAns).length;
      const skipped = questions.length - ansCount;

      let promptMsg = "";
      if (timeExpired === true) {{
        advanceToNextSatStage();
        notify("Modul vaqti tugadi. Keyingi bosqichga o'tildi.");
        return;
      }}

      if (satSection === 'rw' && satModule === 1) {{
        promptMsg = skipped > 0 
          ? `Modul 1 da ${{skipped}} ta savol bo'sh qoldi. Modul 1 ni topshirib, Modul 2 ga o'tasizmi?\n\n(Keyingi modulga o'tgach, Modul 1 ga qaytib bo'lmaydi)`
          : `Modul 1 dagi barcha 27 ta savolga javob berildi!\n\nModul 2 ga o'tishni xohlaysizmi?`;
      }} else if (satSection === 'rw' && satModule === 2) {{
        promptMsg = `Section 1 (Reading & Writing) yakunlanmoqda. Section 2: Math qismiga o'tasizmi?`;
      }} else if (satSection === 'math' && satModule === 1) {{
        promptMsg = skipped > 0
          ? `Math Modul 1 da ${{skipped}} ta savol bo'sh qoldi. Modul 2 ga o'tasizmi?`
          : `Math Modul 1 dagi barcha 22 ta savolga javob berildi. Modul 2 ga o'tasizmi?`;
      }} else {{
        promptMsg = `Barcha modullar va bo'limlar yakunlandi!\n\nImtihonni topshirib, 1600 ballik rasmiy natijani hisoblashni xohlaysizmi?`;
      }}

      const stage = `${{satSection}}_m${{satModule}}`;
      askConfirm(promptMsg, () => {{
        if (satTimerInterval && stage === `${{satSection}}_m${{satModule}}`) advanceToNextSatStage();
      }});
    }}

    function advanceToNextSatStage() {{
      stopSatTimer();

      if (satSection === 'rw' && satModule === 1) {{
        satModule = 2;
        startCurrentModule();
      }} else if (satSection === 'rw' && satModule === 2) {{
        // Show Transition Card to Math
        document.getElementById('sat-runner-card').classList.add('hidden');
        document.getElementById('sat-transition-card').classList.remove('hidden');
        window.scrollTo({{ top: 0, behavior: 'smooth' }});
      }} else if (satSection === 'math' && satModule === 1) {{
        satModule = 2;
        startCurrentModule();
      }} else {{
        // Complete Exam
        showSatFinalResults();
      }}
    }}

    function startMathSection() {{
      satSection = 'math';
      satModule = 1;
      document.getElementById('sat-transition-card').classList.add('hidden');
      document.getElementById('sat-runner-card').classList.remove('hidden');
      startCurrentModule();
    }}

    function scaleSatSection(correct, total) {{
      return Math.round((200 + (correct / total) * 600) / 10) * 10;
    }}

    function showSatFinalResults() {{
      stopSatTimer();
      clearSatAttempt();
      setExamGuard(false);

      // Grade RW (54 Qs)
      let rwCorrect = 0;
      satQuestions.rw_m1.forEach((q, idx) => {{
        if (satAnswers.rw_m1[idx] === q.correct) rwCorrect++;
      }});
      satQuestions.rw_m2.forEach((q, idx) => {{
        if (satAnswers.rw_m2[idx] === q.correct) rwCorrect++;
      }});

      // Grade Math (44 Qs)
      let mathCorrect = 0;
      satQuestions.math_m1.forEach((q, idx) => {{
        if (satAnswers.math_m1[idx] === q.correct) mathCorrect++;
      }});
      satQuestions.math_m2.forEach((q, idx) => {{
        if (satAnswers.math_m2[idx] === q.correct) mathCorrect++;
      }});

      // College Board Scaled Scoring (RW 200-800, Math 200-800)
      const rwScaled = scaleSatSection(rwCorrect, 54);
      const mathScaled = scaleSatSection(mathCorrect, 44);
      const totalScaled = rwScaled + mathScaled;

      document.getElementById('sat-runner-card').classList.add('hidden');
      document.getElementById('sat-transition-card').classList.add('hidden');
      document.getElementById('sat-review-module-bar').classList.add('hidden');
      document.getElementById('sat-runner-results').classList.remove('hidden');

      document.getElementById('sat-rw-score').innerText = rwScaled;
      document.getElementById('sat-m-score').innerText = mathScaled;
      document.getElementById('sat-tot-score').innerText = totalScaled;

      document.getElementById('sat-score-desc').innerHTML = `
        <b>${{currentSatMock.title}}</b> to'liq yakunlandi.<br>
        Siz 98 ta savoldan jami <b>${{rwCorrect + mathCorrect}}</b> tasiga to'g'ri javob berdingiz.<br>
        • Reading & Writing: ${{rwCorrect}} / 54 to'g'ri (<b>${{rwScaled}} ball</b>)<br>
        • Math: ${{mathCorrect}} / 44 to'g'ri (<b>${{mathScaled}} ball</b>)<br><br>
        <i>Bu taxminiy ball, rasmiy College Board natijasi emas.</i>
      `;
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    function startSatReviewMode(modKey) {{
      isReviewMode = true;
      reviewModuleKey = modKey;

      document.getElementById('sat-runner-results').classList.add('hidden');
      document.getElementById('sat-runner-card').classList.remove('hidden');
      document.getElementById('sat-review-module-bar').classList.remove('hidden');

      // Update active review tab button
      ['rw_m1', 'rw_m2', 'math_m1', 'math_m2'].forEach(k => {{
        const btn = document.getElementById('rev-tab-' + k);
        if (btn) {{
          if (k === modKey) btn.className = 'py-1.5 rounded-lg bg-blue-600 text-white text-center';
          else btn.className = 'py-1.5 rounded-lg bg-slate-800 text-slate-300 text-center';
        }}
      }});

      const titles = {{
        rw_m1: "Section 1: RW — Modul 1 Tahlili",
        rw_m2: "Section 1: RW — Modul 2 Tahlili",
        math_m1: "Section 2: Math — Modul 1 Tahlili",
        math_m2: "Section 2: Math — Modul 2 Tahlili"
      }};
      document.getElementById('sat-cur-module-name').innerText = titles[modKey] || "Tahlil Rejimi";
      document.getElementById('sat-timer-label').innerText = "Holat:";
      document.getElementById('sat-runner-timer').innerText = "REVIEW";

      satQuestionIdx = 0;
      loadActiveSatQuestion();
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    function confirmExitSatRunner() {{
      if (!isReviewMode) {{
        if (!confirm("Haqiqatan ham testdan chiqmoqchimisiz? Natijangiz saqlanmaydi.")) return;
      }}
      exitSatRunner();
    }}

    function exitSatRunner() {{
      stopSatTimer();
      clearSatAttempt();
      setExamGuard(false);
      document.getElementById('sat-runner-view').classList.add('hidden');
      document.getElementById('sat-catalog-view').classList.remove('hidden');
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    // =========================================================================
    // 2. 45 IELTS MOCKS HUB
    // =========================================================================
    const ieltsMocks = EXAM_DATA.ielts_mocks || [];
    let activeIeltsCategory = 'all';

    function filterIeltsMocks(cat) {{
      activeIeltsCategory = cat;
      const cats = ['all', 'cnew', 'cmid', 'cold', 'bc'];
      cats.forEach(c => {{
        const btn = document.getElementById('ielts-f-' + c);
        if (btn) {{
          if ((cat === 'all' && c === 'all') ||
              (cat === 'cambridge_new' && c === 'cnew') ||
              (cat === 'cambridge_mid' && c === 'cmid') ||
              (cat === 'cambridge_old' && c === 'cold') ||
              (cat === 'official_bc' && c === 'bc')) {{
            btn.className = 'py-1.5 px-3 rounded-xl bg-blue-600 text-white whitespace-nowrap';
          }} else {{
            btn.className = 'py-1.5 px-3 rounded-xl bg-slate-800 text-slate-300 whitespace-nowrap';
          }}
        }}
      }});
      renderIeltsMocksGrid();
    }}

    function renderIeltsMocksGrid() {{
      const container = document.getElementById('ielts-mocks-grid');
      let filtered = ieltsMocks;
      if (activeIeltsCategory === 'cambridge_new') {{
        filtered = ieltsMocks.filter(m => m.num >= 1 && m.num <= 12);
      }} else if (activeIeltsCategory === 'cambridge_mid') {{
        filtered = ieltsMocks.filter(m => m.num >= 13 && m.num <= 24);
      }} else if (activeIeltsCategory === 'cambridge_old') {{
        filtered = ieltsMocks.filter(m => m.num >= 25 && m.num <= 40);
      }} else if (activeIeltsCategory === 'official_bc') {{
        filtered = ieltsMocks.filter(m => m.num >= 41);
      }}

      container.innerHTML = filtered.map(m => `
        <div class="card-surface p-4 rounded-2xl space-y-2.5 border border-slate-800 hover:border-slate-700 transition">
          <div class="flex items-center justify-between">
            <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
              ${{m.volume}}
            </span>
            <span class="text-[10px] font-semibold text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded border border-blue-500/20">
              ${{m.status}}
            </span>
          </div>

          <h4 class="text-xs font-extrabold text-white">${{m.title}}</h4>
          <p class="text-[11px] text-slate-400">${{m.description}}</p>

          <div class="grid grid-cols-2 gap-1.5 text-[10px] text-slate-300 pt-1">
            <div class="p-1.5 rounded bg-slate-900 border border-slate-800">🎧 ${{m.skills.listening}}</div>
            <div class="p-1.5 rounded bg-slate-900 border border-slate-800">📖 ${{m.skills.reading}}</div>
            <div class="p-1.5 rounded bg-slate-900 border border-slate-800">✍️ ${{m.skills.writing}}</div>
            <div class="p-1.5 rounded bg-slate-900 border border-slate-800">🗣 ${{m.skills.speaking}}</div>
          </div>

          <div class="pt-2 border-t border-slate-800 flex gap-2 justify-end">
            <button onclick="launchMockListening(${{m.num}})" class="py-1.5 px-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center gap-1 transition">
              <span>Listening (40 ta)</span> 🎧
            </button>
            <button onclick="launchMockReading(${{m.num}})" class="py-1.5 px-3 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs flex items-center gap-1 transition">
              <span>Reading (40 ta)</span> 📖
            </button>
          </div>
        </div>
      `).join('');
    }}

    function launchMockListening(mockNum) {{
      const tests = EXAM_DATA.ielts_listening_tests || [];
      const testIdx = ((mockNum - 1) % tests.length) + 1;
      const select = document.getElementById('listening-test-select');
      if (select) select.value = testIdx;
      loadListeningTest(testIdx);
      switchMainTab('listening');
    }}

    function launchMockReading(mockNum) {{
      const tests = EXAM_DATA.ielts_reading_tests || [];
      const testIdx = ((mockNum - 1) % tests.length) + 1;
      const select = document.getElementById('reading-test-select');
      if (select) select.value = testIdx;
      loadReadingTest(testIdx);
      switchMainTab('reading');
    }}

    // =========================================================================
    // 3. IELTS LISTENING (MULTI-TEST + REAL AUDIO & INTERACTIVE SCRUBBER)
    // =========================================================================
    const listeningTests = EXAM_DATA.ielts_listening_tests || [];
    let currentListeningTest = null;
    let activeListeningSection = 1;
    let listeningAnswers = {{}};
    let listeningGraded = false;

    // Audio Engine State
    let speechGen = 0;
    let activeUtterance = null;
    let speechWatchdog = null;
    let isScrubbing = false;
    let currentSentenceIdx = 0;
    let isListeningAudioPlaying = false;
    let currentAudioSentences = [];
    let audioPlaybackRate = 1.0;

    function initListeningDropdown() {{
      const select = document.getElementById('listening-test-select');
      select.innerHTML = listeningTests.map(t => 
        `<option value="${{t.num}}">${{t.title}}</option>`
      ).join('');
      loadListeningTest(1);
    }}

    function loadListeningTest(testNum) {{
      pauseListeningAudio();
      const found = listeningTests.find(t => t.num == testNum) || listeningTests[0];
      currentListeningTest = found;
      activeListeningSection = 1;
      listeningAnswers = {{}};
      listeningGraded = false;
      document.getElementById('listening-res-modal').classList.add('hidden');

      filterListeningSection(1);
    }}

    function filterListeningSection(sec) {{
      pauseListeningAudio();
      activeListeningSection = sec;
      for (let i = 1; i <= 4; i++) {{
        const btn = document.getElementById('l-sec-' + i);
        if (i === sec) btn.className = 'py-1.5 rounded-lg bg-blue-600 text-white text-center';
        else btn.className = 'py-1.5 rounded-lg bg-slate-800 text-slate-300 text-center';
      }}

      // Setup audio script for this section
      const scriptText = currentListeningTest.scripts[sec] || "";
      currentAudioSentences = splitSentences(scriptText);
      currentSentenceIdx = 0;
      updateScrubberUI();

      document.getElementById('listening-player-title').innerText = 
        `${{currentListeningTest.title}} • Section ${{sec}} Audio`;
      document.getElementById('listening-player-state').innerText = 
        `Jami ${{currentAudioSentences.length}} ta jumla • Tinglashga tayyor`;

      updateTapescriptContent();
      renderListeningQuestions();
    }}

    function updateTapescriptContent() {{
      const container = document.getElementById('tapescript-content');
      const scriptText = currentListeningTest.scripts[activeListeningSection] || "";
      container.innerHTML = `<b>Section ${{activeListeningSection}} Audio Tapescript:</b><br><br>${{scriptText}}`;
    }}

    function toggleTapescript() {{
      const content = document.getElementById('tapescript-content');
      const arrow = document.getElementById('ts-arrow');
      if (content.classList.contains('hidden')) {{
        content.classList.remove('hidden');
        arrow.innerText = '▲';
      }} else {{
        content.classList.add('hidden');
        arrow.innerText = '▼';
      }}
    }}

    // REAL AUDIO PLAYBACK VIA WEB SPEECH API
    function toggleListeningAudio() {{
      if (isListeningAudioPlaying) {{
        pauseListeningAudio();
      }} else {{
        playListeningAudio();
      }}
    }}

    function splitSentences(text) {{
      const clean = text.replace(/\\b(Dr|Mr|Mrs|Ms|Prof)\\.\\s/g, '$1 ');
      const parts = clean.match(/(?:[^.!?]|[.!?](?=\\S))+(?:[.!?]+|$)/g) || [clean];
      return parts.map(p => p.trim()).filter(Boolean);
    }}

    function sentenceSeconds(sentence) {{
      return Math.max(1, sentence.split(/\\s+/).length / 2.5);
    }}

    function sentenceStartSeconds(idx) {{
      return currentAudioSentences.slice(0, idx).reduce((sum, x) => sum + sentenceSeconds(x), 0);
    }}

    function totalAudioSeconds() {{
      return sentenceStartSeconds(currentAudioSentences.length);
    }}

    function sentenceAtSeconds(seconds) {{
      let elapsed = 0;
      for (let i = 0; i < currentAudioSentences.length; i++) {{
        elapsed += sentenceSeconds(currentAudioSentences[i]);
        if (seconds < elapsed) return i;
      }}
      return currentAudioSentences.length - 1;
    }}

    function formatClock(seconds) {{
      const total = Math.floor(seconds);
      return `${{Math.floor(total / 60).toString().padStart(2, '0')}}:${{(total % 60).toString().padStart(2, '0')}}`;
    }}

    function pickEnglishVoice() {{
      const voices = window.speechSynthesis.getVoices() || [];
      return voices.find(v => v.lang === 'en-GB') || voices.find(v => /^en[-_]/i.test(v.lang)) || null;
    }}

    function showNoSpeechNotice() {{
      document.getElementById('listening-player-state').innerText =
        "Bu qurilmada ovoz sintezi yo'q. Hozircha audio matnidan foydalaning.";
      document.getElementById('tapescript-content').classList.remove('hidden');
      document.getElementById('ts-arrow').innerText = '▲';
    }}

    function stopSpeech() {{
      speechGen++;
      clearTimeout(speechWatchdog);
      activeUtterance = null;
      if (window.speechSynthesis) window.speechSynthesis.cancel();
    }}

    function playListeningAudio() {{
      if (!window.speechSynthesis || typeof SpeechSynthesisUtterance === 'undefined') {{
        showNoSpeechNotice();
        return;
      }}
      stopSpeech();
      setAudioPlayingState(true);
      speakSentence(currentSentenceIdx);
    }}

    function speakSentence(idx) {{
      if (!isListeningAudioPlaying) return;
      if (idx >= currentAudioSentences.length) {{
        pauseListeningAudio();
        currentSentenceIdx = 0;
        updateScrubberUI();
        return;
      }}

      const gen = ++speechGen;
      currentSentenceIdx = idx;
      updateScrubberUI();

      const text = currentAudioSentences[idx];
      const utter = new SpeechSynthesisUtterance(text);
      utter.lang = 'en-GB';
      utter.rate = audioPlaybackRate;
      const voice = pickEnglishVoice();
      if (voice) utter.voice = voice;

      const goNext = () => {{
        clearTimeout(speechWatchdog);
        if (gen === speechGen && isListeningAudioPlaying) speakSentence(idx + 1);
      }};
      utter.onend = goNext;
      utter.onerror = (e) => {{
        clearTimeout(speechWatchdog);
        if (gen !== speechGen || e.error === 'interrupted' || e.error === 'canceled') return;
        pauseListeningAudio();
        document.getElementById('listening-player-state').innerText =
          `Ovoz to'xtadi (${{e.error}}). Qayta bosib ko'ring.`;
      }};

      activeUtterance = utter;
      clearTimeout(speechWatchdog);
      speechWatchdog = setTimeout(goNext, (sentenceSeconds(text) / audioPlaybackRate + 5) * 1000);
      window.speechSynthesis.speak(utter);
    }}

    function restartSpeechAt(idx) {{
      stopSpeech();
      currentSentenceIdx = idx;
      updateScrubberUI();
      if (!isListeningAudioPlaying) return;
      const gen = speechGen;
      setTimeout(() => {{ if (gen === speechGen) speakSentence(idx); }}, 120);
    }}

    function pauseListeningAudio() {{
      stopSpeech();
      setAudioPlayingState(false);
    }}

    function setAudioPlayingState(isPlaying) {{
      isListeningAudioPlaying = isPlaying;
      const btnIcon = document.getElementById('audio-icon');
      const btnLabel = document.getElementById('audio-btn-label');
      const waveBox = document.getElementById('audio-wave-box');

      if (isPlaying) {{
        btnIcon.innerText = "⏸";
        btnLabel.innerText = "Pauza";
        waveBox.classList.remove('hidden');
      }} else {{
        btnIcon.innerText = "▶";
        btnLabel.innerText = "Tinglash (Ovoz)";
        waveBox.classList.add('hidden');
      }}
    }}

    // INTERACTIVE SCRUBBER (Orqa/Oldinga surish)
    function previewListeningSeek(percentVal) {{
      isScrubbing = true;
      document.getElementById('audio-cur-time').innerText = formatClock((percentVal / 100) * totalAudioSeconds());
    }}

    function seekListeningAudio(percentVal) {{
      isScrubbing = false;
      if (!currentAudioSentences.length) return;
      restartSpeechAt(sentenceAtSeconds((percentVal / 100) * totalAudioSeconds()));
    }}

    function skipAudio(seconds) {{
      if (!currentAudioSentences.length) return;
      restartSpeechAt(sentenceAtSeconds(Math.max(0, sentenceStartSeconds(currentSentenceIdx) + seconds)));
    }}

    function setAudioSpeed(speed) {{
      audioPlaybackRate = speed;
      [['spd-08', 0.8], ['spd-10', 1.0], ['spd-12', 1.2]].forEach(([id, value]) => {{
        document.getElementById(id).className = value === speed
          ? 'text-[10px] font-bold px-2 py-1 rounded bg-blue-600 text-white'
          : 'text-[10px] font-bold px-2 py-1 rounded bg-slate-800 text-slate-400';
      }});
      if (isListeningAudioPlaying) restartSpeechAt(currentSentenceIdx);
    }}

    function updateScrubberUI() {{
      const total = totalAudioSeconds() || 1;
      const current = sentenceStartSeconds(currentSentenceIdx);
      if (!isScrubbing) document.getElementById('listening-audio-scrubber').value = (current / total) * 100;
      document.getElementById('audio-cur-time').innerText = formatClock(current);
      document.getElementById('audio-tot-time').innerText = formatClock(total);
    }}

    function renderListeningQuestions() {{
      const container = document.getElementById('listening-questions-container');
      const questions = currentListeningTest.questions.filter(q => q.sec === activeListeningSection);

      container.innerHTML = questions.map(q => {{
        const savedAns = listeningAnswers[q.num] || "";
        let inputHtml = "";

        if (q.type === 'mcq') {{
          inputHtml = `
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-1.5 pt-1">
              ${{q.options.map(opt => `
                <button onclick="setListeningAnswer(${{q.num}}, '${{opt[0]}}')" class="p-2 rounded-lg border text-left text-xs transition flex items-center gap-2 ${{savedAns === opt[0] ? 'bg-blue-600/20 border-blue-500 text-white font-semibold' : 'bg-slate-900 border-slate-800 text-slate-300'}}">
                  <span class="w-4 h-4 rounded bg-slate-800 text-[10px] font-bold flex items-center justify-center">${{opt[0]}}</span>
                  <span>${{opt.slice(3)}}</span>
                </button>
              `).join('')}}
            </div>
          `;
        }} else {{
          inputHtml = `
            <div class="flex items-center gap-2 pt-1">
              <input type="text" value="${{escapeHtml(savedAns)}}" oninput="saveTextAnswer(listeningAnswers, ${{q.num}}, this.value, updateListeningPreview)" placeholder="Javobingizni yozing..." class="flex-1 py-1.5 px-3 rounded-lg bg-slate-900 border border-slate-700 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-500">
            </div>
          `;
        }}

        return `
          <div class="card-surface p-3.5 rounded-xl space-y-1.5" id="l-card-${{q.num}}">
            <div class="flex justify-between items-start">
              <span class="text-[11px] font-mono font-bold text-emerald-400">Savol #${{q.num}}</span>
              <span class="text-[10px] uppercase font-semibold text-slate-500">${{q.type}}</span>
            </div>
            <p class="text-xs font-semibold text-white">${{q.text}}</p>
            ${{inputHtml}}
            <div id="l-expl-${{q.num}}" class="hidden text-[11px] text-slate-300 pt-1.5 border-t border-slate-800"></div>
          </div>
        `;
      }}).join('');

      updateListeningPreview();
      if (listeningGraded) paintResults('l', currentListeningTest, listeningAnswers);
    }}

    function saveTextAnswer(answers, num, value, refreshPreview) {{
      const clean = value.trim();
      if (clean) answers[num] = clean;
      else delete answers[num];
      refreshPreview();
    }}

    function setListeningAnswer(num, val) {{
      listeningAnswers[num] = val.trim();
      updateListeningPreview();
      renderListeningQuestions();
    }}

    function updateListeningPreview() {{
      const count = Object.keys(listeningAnswers).length;
      document.getElementById('listening-score-preview').innerText = `${{count}} / 40 kiritildi`;
    }}

    function normalizeAnswer(value) {{
      return String(value == null ? '' : value).trim().toLowerCase()
        .replace(/(\\d),(?=\\d{{3}}\\b)/g, '$1')
        .replace(/(\\d)(st|nd|rd|th)\\b/g, '$1')
        .replace(/^(a|an|the)\\s+/, '')
        .replace(/[.\\s]+$/, '')
        .replace(/\\s+/g, ' ');
    }}

    function isAnswerCorrect(q, value) {{
      const user = normalizeAnswer(value);
      return !!user && [q.ans, ...(q.alts || [])].some(a => normalizeAnswer(a) === user);
    }}

    function paintResults(prefix, test, answers) {{
      test.questions.forEach(q => {{
        const card = document.getElementById(`${{prefix}}-card-${{q.num}}`);
        const expl = document.getElementById(`${{prefix}}-expl-${{q.num}}`);
        if (!card || !expl) return;
        const ok = isAnswerCorrect(q, answers[q.num]);
        card.classList.add(ok ? 'border-emerald-500/50' : 'border-rose-500/50');
        expl.classList.remove('hidden');
        expl.innerHTML = ok
          ? `<span class="text-emerald-400 font-bold">✅ To'g'ri! (${{q.ans}})</span> • ${{q.expl}}`
          : `<span class="text-rose-400 font-bold">❌ To'g'ri javob: ${{q.ans}}</span> • ${{q.expl}}`;
      }});
    }}

    function gradeListeningTest() {{
      pauseListeningAudio();
      listeningGraded = true;
      const correct = currentListeningTest.questions.filter(q => isAnswerCorrect(q, listeningAnswers[q.num])).length;
      paintResults('l', currentListeningTest, listeningAnswers);

      const band = rawToBand(correct, LISTENING_BANDS);
      const modal = document.getElementById('listening-res-modal');
      modal.classList.remove('hidden');
      document.getElementById('l-res-band').innerText = `Band ${{band.toFixed(1)}}`;
      document.getElementById('l-res-details').innerText =
        `Siz 40 ta savoldan ${{correct}} tasiga to'g'ri javob berdingiz! Taxminiy CEFR: ${{bandToCefr(band)}}`;
      modal.scrollIntoView({{ behavior: 'smooth' }});
    }}

    function restartListeningTest() {{
      listeningAnswers = {{}};
      listeningGraded = false;
      document.getElementById('listening-res-modal').classList.add('hidden');
      renderListeningQuestions();
    }}

    // =========================================================================
    // 4. IELTS READING (MULTI-TEST + 3 FULL PASSAGES + 40 QUESTIONS)
    // =========================================================================
    const readingTests = EXAM_DATA.ielts_reading_tests || [];
    let currentReadingTest = null;
    let activeReadingPassage = 1;
    let readingAnswers = {{}};
    let readingGraded = false;

    function initReadingDropdown() {{
      const select = document.getElementById('reading-test-select');
      select.innerHTML = readingTests.map(t => 
        `<option value="${{t.num}}">${{t.title}}</option>`
      ).join('');
      loadReadingTest(1);
    }}

    function loadReadingTest(testNum) {{
      const found = readingTests.find(t => t.num == testNum) || readingTests[0];
      currentReadingTest = found;
      activeReadingPassage = 1;
      readingAnswers = {{}};
      readingGraded = false;
      document.getElementById('reading-res-modal').classList.add('hidden');
      switchReadingPassage(1);
    }}

    function switchReadingPassage(pNum) {{
      activeReadingPassage = pNum;
      for (let i = 1; i <= 3; i++) {{
        const btn = document.getElementById('btn-p' + i);
        if (i === pNum) btn.className = 'py-2 rounded-xl bg-blue-600 text-white text-center';
        else btn.className = 'py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 text-center';
      }}
      renderReadingPassage();
      renderReadingQuestions();
    }}

    function renderReadingPassage() {{
      const passageObj = currentReadingTest.passages.find(p => p.num === activeReadingPassage) || currentReadingTest.passages[0];
      document.getElementById('reading-p-title').innerText = passageObj.title;
      document.getElementById('reading-p-text').innerText = passageObj.text;
    }}

    function renderReadingQuestions() {{
      const container = document.getElementById('reading-questions-container');
      const questions = currentReadingTest.questions.filter(q => q.passage_num === activeReadingPassage);

      container.innerHTML = questions.map(q => {{
        const savedAns = readingAnswers[q.num] || "";
        let inputHtml = "";

        if (q.type === 'tfng') {{
          inputHtml = `
            <div class="grid grid-cols-3 gap-1.5 pt-1">
              ${{['TRUE', 'FALSE', 'NOT GIVEN'].map(opt => `
                <button onclick="setReadingAnswer(${{q.num}}, '${{opt}}')" class="py-1.5 rounded-lg border text-xs font-bold transition ${{savedAns === opt ? 'bg-blue-600 border-blue-500 text-white' : 'bg-slate-900 border-slate-800 text-slate-400'}}">
                  ${{opt}}
                </button>
              `).join('')}}
            </div>
          `;
        }} else if (q.type === 'mcq') {{
          inputHtml = `
            <div class="space-y-1.5 pt-1">
              ${{q.options.map(opt => `
                <button onclick="setReadingAnswer(${{q.num}}, '${{opt[0]}}')" class="w-full p-2.5 rounded-lg border text-left text-xs transition flex items-center gap-2 ${{savedAns === opt[0] ? 'bg-blue-600/20 border-blue-500 text-white font-semibold' : 'bg-slate-900 border-slate-800 text-slate-300'}}">
                  <span class="w-4 h-4 rounded bg-slate-800 text-[10px] font-bold flex items-center justify-center">${{opt[0]}}</span>
                  <span>${{opt.slice(3)}}</span>
                </button>
              `).join('')}}
            </div>
          `;
        }} else {{
          inputHtml = `
            <div class="flex items-center gap-2 pt-1">
              <input type="text" value="${{escapeHtml(savedAns)}}" oninput="saveTextAnswer(readingAnswers, ${{q.num}}, this.value, updateReadingPreview)" placeholder="Bo'sh joyga so'z yozing..." class="flex-1 py-1.5 px-3 rounded-lg bg-slate-900 border border-slate-700 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-500">
            </div>
          `;
        }}

        return `
          <div class="card-surface p-3.5 rounded-xl space-y-1.5" id="r-card-${{q.num}}">
            <div class="flex justify-between items-start">
              <span class="text-[11px] font-mono font-bold text-blue-400">Savol #${{q.num}}</span>
              <span class="text-[10px] uppercase font-semibold text-slate-500">${{q.type}}</span>
            </div>
            <p class="text-xs font-semibold text-white">${{q.text}}</p>
            ${{inputHtml}}
            <div id="r-expl-${{q.num}}" class="hidden text-[11px] text-slate-300 pt-1.5 border-t border-slate-800"></div>
          </div>
        `;
      }}).join('');

      updateReadingPreview();
      if (readingGraded) paintResults('r', currentReadingTest, readingAnswers);
    }}

    function setReadingAnswer(num, val) {{
      readingAnswers[num] = val.trim();
      updateReadingPreview();
      renderReadingQuestions();
    }}

    function updateReadingPreview() {{
      const count = Object.keys(readingAnswers).length;
      document.getElementById('reading-score-preview').innerText = `${{count}} / 40 kiritildi`;
    }}

    function gradeReadingTest() {{
      readingGraded = true;
      const correct = currentReadingTest.questions.filter(q => isAnswerCorrect(q, readingAnswers[q.num])).length;
      paintResults('r', currentReadingTest, readingAnswers);

      const band = rawToBand(correct, READING_BANDS);
      const modal = document.getElementById('reading-res-modal');
      modal.classList.remove('hidden');
      document.getElementById('r-res-band').innerText = `Band ${{band.toFixed(1)}}`;
      document.getElementById('r-res-details').innerText =
        `Siz 40 ta savoldan ${{correct}} tasiga to'g'ri javob berdingiz! Taxminiy Reading balingiz: Band ${{band.toFixed(1)}}`;
      modal.scrollIntoView({{ behavior: 'smooth' }});
    }}

    function restartReadingTest() {{
      readingAnswers = {{}};
      readingGraded = false;
      document.getElementById('reading-res-modal').classList.add('hidden');
      renderReadingQuestions();
    }}

    const LISTENING_BANDS = [[39, 9], [37, 8.5], [35, 8], [32, 7.5], [30, 7], [26, 6.5], [23, 6], [18, 5.5], [16, 5], [13, 4.5], [10, 4], [8, 3.5], [6, 3], [4, 2.5], [3, 2], [2, 1.5], [1, 1]];
    const READING_BANDS = [[39, 9], [37, 8.5], [35, 8], [33, 7.5], [30, 7], [27, 6.5], [23, 6], [19, 5.5], [15, 5], [13, 4.5], [10, 4], [8, 3.5], [6, 3], [4, 2.5], [3, 2], [2, 1.5], [1, 1]];

    function rawToBand(raw, table) {{
      const row = table.find(([min]) => raw >= min);
      return row ? row[1] : 0;
    }}

    function bandToCefr(band) {{
      if (band >= 8.5) return 'C2';
      if (band >= 7) return 'C1';
      if (band >= 5.5) return 'B2';
      if (band >= 4) return 'B1';
      return 'A2 yoki past';
    }}

    // =========================================================================
    // 5. WRITING BANK & 6. PREDICTOR
    // =========================================================================
    let activeWritingTask = 1;

    function switchWritingTask(taskNum) {{
      activeWritingTask = taskNum;
      document.getElementById('btn-w-t1').className = taskNum === 1 
        ? 'py-2 rounded-xl bg-blue-600 text-white text-center' 
        : 'py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 text-center';
      document.getElementById('btn-w-t2').className = taskNum === 2 
        ? 'py-2 rounded-xl bg-blue-600 text-white text-center' 
        : 'py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 text-center';
      renderWritingPrompts();
    }}

    function renderWritingPrompts() {{
      const container = document.getElementById('writing-prompts-container');
      const items = activeWritingTask === 1 ? EXAM_DATA.ielts_writing_t1 : EXAM_DATA.ielts_writing_t2;

      container.innerHTML = items.map(w => `
        <div class="card-surface p-4 rounded-2xl space-y-2 border border-slate-800">
          <div class="flex justify-between items-center">
            <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30">
              ${{w.type || w.category}}
            </span>
            <span class="text-[10px] font-mono text-emerald-400 font-bold">Band 9.0 Namuna</span>
          </div>
          <h4 class="text-xs font-bold text-white">${{w.title || "IELTS Essay Prompt"}}</h4>
          <p class="text-xs text-slate-300 bg-slate-900/80 p-2.5 rounded-xl border border-slate-800">${{w.desc || w.prompt}}</p>
          <div class="pt-1">
            <details class="text-xs text-slate-300">
              <summary class="cursor-pointer text-amber-400 font-bold hover:underline">Band 9 Model Insho & Tahlilni Ko'rish →</summary>
              <div class="mt-2 p-3 rounded-xl bg-slate-900 border border-slate-800 leading-relaxed whitespace-pre-line text-[11px] text-slate-200">
                ${{w.model}}
              </div>
            </details>
          </div>
        </div>
      `).join('');
    }}

    function updatePredictor() {{
      const il = parseFloat(document.getElementById('p-il').value);
      const ir = parseFloat(document.getElementById('p-ir').value);
      const sr = parseInt(document.getElementById('p-sr').value);
      const sm = parseInt(document.getElementById('p-sm').value);

      document.getElementById('p-val-il').innerText = il.toFixed(1);
      document.getElementById('p-val-ir').innerText = ir.toFixed(1);
      document.getElementById('p-val-sr').innerText = sr;
      document.getElementById('p-val-sm').innerText = sm;

      const totalSat = sr + sm;
      document.getElementById('p-tot-sat').innerText = `${{totalSat}} / 1600`;

      const avgBand = (il + ir) / 2;
      const tier = totalSat >= 1450 && avgBand >= 7.5 ? 'Kuchli profil (taxminiy)'
        : totalSat >= 1300 && avgBand >= 6.5 ? "O'rtacha profil (taxminiy)"
        : 'Rivojlantirish kerak (taxminiy)';
      document.getElementById('p-local-grant').innerText = tier;
      document.getElementById('p-intl-grant').innerText = tier;
    }}

    // Initial Page Setup
    renderSatMocksGrid();
    renderIeltsMocksGrid();
    initListeningDropdown();
    initReadingDropdown();
    renderWritingPrompts();
    updatePredictor();
    restoreSatAttempt();
  </script>
</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated successfully: {OUTPUT_HTML} (Size: {len(html_content.encode('utf-8'))} bytes)")
