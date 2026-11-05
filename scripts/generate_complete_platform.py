# -*- coding: utf-8 -*-
"""
Builds the comprehensive Fullscreen Mini App containing:
- 45 Full SAT Mocks (Catalog + Live Interactive Test Runner)
- 45 Full IELTS Academic Mocks (Catalog + Live Interactive Test Runner)
- 40 IELTS Listening questions with audio simulator
- 40 IELTS Reading questions with 3 passages
- 42 Writing Task 1 & 2 topics with Band 9 structures
- Score & University Grant Predictor
- Fullscreen Telegram WebApp mode (requestFullscreen + disableVerticalSwipes)
"""
import json
from pathlib import Path

BASE_DIR = Path(r"C:\Users\Otabek\.gemini\antigravity\scratch\sat-master-bot")
EXAM_BANK_FILE = BASE_DIR / "webapp" / "exam_bank.json"
OUTPUT_HTML = BASE_DIR / "webapp" / "index.html"

with open(EXAM_BANK_FILE, "r", encoding="utf-8") as f:
    bank_data = json.load(f)

json_str = json.dumps(bank_data, ensure_ascii=False)

html_content = f'''<!DOCTYPE html>
<html lang="uz" class="h-full">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>IELTS 8.5 & SAT 1500+ Full Mock Platform</title>
  <script src="https://telegram.org/js/telegram-web-app.js"></script>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');
    * {{
      font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
      -webkit-tap-highlight-color: transparent;
      touch-action: manipulation;
    }}
    html, body {{
      width: 100%;
      min-height: 100%;
      min-height: 100dvh;
      background-color: var(--tg-theme-bg-color, #090D16);
      color: var(--tg-theme-text-color, #F8FAFC);
    }}
    button, a, [onclick] {{
      touch-action: manipulation;
      cursor: pointer;
    }}
    input, select, textarea {{
      -webkit-user-select: auto !important;
      user-select: auto !important;
    }}
    code, .font-mono {{
      font-family: 'JetBrains Mono', monospace;
    }}
    .card-surface {{
      background: rgba(17, 24, 39, 0.90);
      border: 1px solid rgba(255, 255, 255, 0.08);
      backdrop-filter: blur(16px);
    }}
    .nav-active {{
      background: #2563EB !important;
      color: #FFFFFF !important;
      box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4);
    }}
    input[type=range] {{
      height: 6px;
      border-radius: 9999px;
    }}
    input[type=range]::-webkit-slider-thumb {{
      width: 20px;
      height: 20px;
      border-radius: 50%;
      background: #3B82F6;
      border: 2px solid #FFFFFF;
      box-shadow: 0 0 12px rgba(59, 130, 246, 0.6);
      cursor: pointer;
      -webkit-appearance: none;
    }}
    .tab-content {{
      display: none;
    }}
    .tab-content.active {{
      display: block;
    }}
    ::-webkit-scrollbar {{
      width: 4px;
      height: 4px;
    }}
    ::-webkit-scrollbar-thumb {{
      background: rgba(255, 255, 255, 0.15);
      border-radius: 4px;
    }}
  </style>
</head>
<body class="min-h-screen p-3 sm:p-5 pb-24 antialiased flex flex-col justify-between">

  <div class="max-w-3xl mx-auto w-full space-y-3.5">
    
    <!-- Top Header -->
    <div class="flex items-center justify-between pb-2 border-b border-slate-800">
      <div class="flex items-center gap-2.5">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-amber-500 flex items-center justify-center text-white text-lg font-bold shadow-lg shadow-blue-500/20">
          🎓
        </div>
        <div>
          <div class="flex items-center gap-1.5">
            <h1 class="text-sm font-extrabold text-white tracking-tight">IELTS & SAT Daily Hub</h1>
            <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">FULLSCREEN</span>
          </div>
          <p class="text-xs text-slate-400">45+ SAT & 45+ IELTS Full Mock Platform</p>
        </div>
      </div>
      <div class="flex items-center gap-1.5">
        <button onclick="requestAppFullscreen()" class="text-xs font-semibold px-2 py-1 rounded-lg bg-slate-800 border border-slate-700 text-slate-300 hover:text-white flex items-center gap-1" title="To'liq ekranga o'tish">
          <span>⛶ Kengaytirish</span>
        </button>
        <a href="https://t.me/ieltssat_daily" target="_blank" class="text-xs font-semibold px-2.5 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 hover:bg-blue-500/20 transition flex items-center gap-1">
          <span>@ieltssat_daily</span> ↗
        </a>
      </div>
    </div>

    <!-- Navigation Bar (6 Tabs) -->
    <div class="flex gap-1.5 overflow-x-auto pb-1 scrollbar-none text-xs font-bold">
      <button id="nav-sat-hub" onclick="switchMainTab('sat-hub')" class="nav-active px-3 py-2 rounded-xl bg-blue-600 text-white whitespace-nowrap transition">
        🎯 45 ta SAT Full Mock
      </button>
      <button id="nav-ielts-hub" onclick="switchMainTab('ielts-hub')" class="px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 whitespace-nowrap transition">
        🇬🇧 45 ta IELTS Full Mock
      </button>
      <button id="nav-listening" onclick="switchMainTab('listening')" class="px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 whitespace-nowrap transition">
        🎧 IELTS Listening
      </button>
      <button id="nav-reading" onclick="switchMainTab('reading')" class="px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 whitespace-nowrap transition">
        📖 IELTS Reading
      </button>
      <button id="nav-writing" onclick="switchMainTab('writing')" class="px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 whitespace-nowrap transition">
        ✍️ Writing Bank (42 ta)
      </button>
      <button id="nav-predict" onclick="switchMainTab('predict')" class="px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 whitespace-nowrap transition">
        📊 Ball Predictor
      </button>
    </div>

    <!-- ========================================================================= -->
    <!-- TAB 1: 45 FULL SAT MOCKS CATALOG & ACTIVE RUNNER -->
    <!-- ========================================================================= -->
    <div id="tab-sat-hub" class="tab-content active space-y-3.5">
      
      <!-- SAT Mocks Catalog View -->
      <div id="sat-catalog-view" class="space-y-3">
        <!-- Filter bar -->
        <div class="card-surface p-3 rounded-2xl space-y-2">
          <div class="flex items-center justify-between">
            <h3 class="text-xs font-bold text-white">🎯 Digital SAT Full Mock Tizimi (45 ta Test)</h3>
            <span class="text-[10px] font-bold text-amber-400 px-2 py-0.5 rounded bg-amber-500/10 border border-amber-500/20">College Board Standarti</span>
          </div>
          <div class="flex gap-1.5 overflow-x-auto pb-1 scrollbar-none text-xs font-semibold">
            <button onclick="filterSatMocks('all')" id="sat-f-all" class="py-1.5 px-3 rounded-xl bg-blue-600 text-white whitespace-nowrap">Barchasi (45)</button>
            <button onclick="filterSatMocks('bluebook')" id="sat-f-bb" class="py-1.5 px-3 rounded-xl bg-slate-800 text-slate-300 whitespace-nowrap">Bluebook Rasmiy (1–6)</button>
            <button onclick="filterSatMocks('princeton')" id="sat-f-pr" class="py-1.5 px-3 rounded-xl bg-slate-800 text-slate-300 whitespace-nowrap">Princeton Review (7–20)</button>
            <button onclick="filterSatMocks('cb_bank')" id="sat-f-cb" class="py-1.5 px-3 rounded-xl bg-slate-800 text-slate-300 whitespace-nowrap">Question Bank (21–35)</button>
            <button onclick="filterSatMocks('master')" id="sat-f-iv" class="py-1.5 px-3 rounded-xl bg-slate-800 text-slate-300 whitespace-nowrap">Ivy League Master (36–45)</button>
          </div>
        </div>

        <!-- Mocks List -->
        <div id="sat-mocks-grid" class="space-y-2.5">
          <!-- Rendered via JS -->
        </div>
      </div>

      <!-- SAT Active Interactive Test Runner View -->
      <div id="sat-runner-view" class="hidden space-y-3.5">
        <!-- Active Runner Top Bar -->
        <div class="card-surface p-3.5 rounded-2xl flex items-center justify-between">
          <div>
            <div class="flex items-center gap-1.5">
              <button onclick="exitSatRunner()" class="text-xs text-blue-400 hover:text-white font-bold">
                ← Barcha SAT Mocklarga Qaytish
              </button>
            </div>
            <h3 id="sat-runner-title" class="text-xs font-extrabold text-white mt-1"></h3>
          </div>
          <div class="flex items-center gap-2">
            <div class="text-right">
              <span class="text-[10px] text-slate-400 block">Qolgan vaqt:</span>
              <span id="sat-runner-timer" class="font-mono font-bold text-xs text-amber-400">45:00</span>
            </div>
            <button id="sat-btn-flag" onclick="toggleSatFlag()" class="p-2 rounded-xl bg-slate-800 text-slate-400 hover:text-amber-400 border border-slate-700 text-xs">
              🚩
            </button>
          </div>
        </div>

        <!-- Questions Nav Pills -->
        <div class="card-surface p-2.5 rounded-xl overflow-x-auto flex gap-1 scrollbar-none" id="sat-runner-pills">
          <!-- Injected via JS -->
        </div>

        <!-- Active Question Card -->
        <div id="sat-runner-card" class="card-surface p-4 sm:p-5 rounded-2xl space-y-4">
          <div id="sat-runner-passage" class="p-3.5 rounded-xl bg-slate-900 border border-slate-800 text-xs leading-relaxed text-slate-300"></div>
          
          <div class="space-y-1">
            <span id="sat-runner-domain" class="text-[10px] font-bold text-slate-400 uppercase tracking-wider"></span>
            <p id="sat-runner-stem" class="text-sm font-semibold text-white leading-snug"></p>
          </div>

          <div id="sat-runner-options" class="space-y-2"></div>

          <!-- Feedback & Explanation -->
          <div id="sat-runner-feedback" class="hidden p-3.5 rounded-xl bg-slate-900 border border-slate-800 space-y-2 text-xs">
            <div class="flex items-center gap-1.5 font-bold" id="sat-fb-status"></div>
            <p id="sat-fb-expl" class="text-slate-300 leading-relaxed"></p>
            <div id="sat-fb-hack" class="text-amber-400 text-[11px] font-medium pt-1 border-t border-slate-800"></div>
          </div>

          <!-- Controls -->
          <div class="flex items-center justify-between pt-2 border-t border-slate-800">
            <button onclick="prevSatRunnerQ()" id="sat-btn-prev" class="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-300 transition">
              ← Oldingisi
            </button>
            <button onclick="finishSatRunner()" class="px-3 py-2 rounded-xl bg-red-600/20 hover:bg-red-600/30 text-red-400 border border-red-500/30 text-xs font-bold transition">
              Testni Yakunlash
            </button>
            <button onclick="nextSatRunnerQ()" id="sat-btn-next" class="px-3.5 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white transition">
              Keyingisi →
            </button>
          </div>
        </div>

        <!-- Results Screen -->
        <div id="sat-runner-results" class="hidden card-surface p-5 rounded-2xl text-center space-y-4">
          <h3 class="text-base font-extrabold text-white">🎉 SAT Mock Natijalari</h3>
          <div class="grid grid-cols-3 gap-2">
            <div class="p-3 rounded-xl bg-slate-900 border border-slate-800">
              <span class="text-[10px] text-slate-400 uppercase block font-semibold">Reading & Writing</span>
              <span id="sat-rw-score" class="text-lg font-extrabold text-blue-400 font-mono">710</span>
              <span class="text-[10px] text-slate-500 block">/ 800</span>
            </div>
            <div class="p-3 rounded-xl bg-slate-900 border border-slate-800">
              <span class="text-[10px] text-slate-400 uppercase block font-semibold">Math 800</span>
              <span id="sat-m-score" class="text-lg font-extrabold text-amber-400 font-mono">770</span>
              <span class="text-[10px] text-slate-500 block">/ 800</span>
            </div>
            <div class="p-3 rounded-xl bg-slate-900 border border-slate-800">
              <span class="text-[10px] text-slate-400 uppercase block font-semibold">Umumiy Natija</span>
              <span id="sat-tot-score" class="text-lg font-extrabold text-emerald-400 font-mono">1480</span>
              <span class="text-[10px] text-slate-500 block">/ 1600</span>
            </div>
          </div>
          <p id="sat-score-desc" class="text-xs text-slate-300 leading-relaxed"></p>
          <button onclick="exitSatRunner()" class="py-2.5 px-5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs">
            Boshqa Mock Tanlash (45 ta)
          </button>
        </div>
      </div>

    </div>

    <!-- ========================================================================= -->
    <!-- TAB 2: 45 FULL IELTS ACADEMIC MOCKS CATALOG -->
    <!-- ========================================================================= -->
    <div id="tab-ielts-hub" class="tab-content space-y-3.5">
      <!-- Filter Bar -->
      <div class="card-surface p-3 rounded-2xl space-y-2">
        <div class="flex items-center justify-between">
          <h3 class="text-xs font-bold text-white">🇬🇧 Cambridge & BC Full Academic Mocks (45 ta)</h3>
          <span class="text-[10px] font-bold text-emerald-400 px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/20">Rasmiy Format</span>
        </div>
        <div class="flex gap-1.5 overflow-x-auto pb-1 scrollbar-none text-xs font-semibold">
          <button onclick="filterIeltsMocks('all')" id="ielts-f-all" class="py-1.5 px-3 rounded-xl bg-blue-600 text-white whitespace-nowrap">Barchasi (45)</button>
          <button onclick="filterIeltsMocks('cambridge_new')" id="ielts-f-cnew" class="py-1.5 px-3 rounded-xl bg-slate-800 text-slate-300 whitespace-nowrap">Cambridge 19–17 (1–12)</button>
          <button onclick="filterIeltsMocks('cambridge_mid')" id="ielts-f-cmid" class="py-1.5 px-3 rounded-xl bg-slate-800 text-slate-300 whitespace-nowrap">Cambridge 16–14 (13–24)</button>
          <button onclick="filterIeltsMocks('cambridge_old')" id="ielts-f-cold" class="py-1.5 px-3 rounded-xl bg-slate-800 text-slate-300 whitespace-nowrap">Cambridge 13–10 (25–40)</button>
          <button onclick="filterIeltsMocks('official_bc')" id="ielts-f-bc" class="py-1.5 px-3 rounded-xl bg-slate-800 text-slate-300 whitespace-nowrap">British Council (41–45)</button>
        </div>
      </div>

      <!-- IELTS Mocks List -->
      <div id="ielts-mocks-grid" class="space-y-2.5">
        <!-- Rendered via JS -->
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- TAB 3: IELTS LISTENING FULL TEST -->
    <!-- ========================================================================= -->
    <div id="tab-listening" class="tab-content space-y-3.5">
      <div class="card-surface p-4 rounded-2xl space-y-3">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <div class="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center justify-center text-sm font-bold">
              🎧
            </div>
            <div>
              <h3 class="text-xs font-bold text-white">IELTS Official Listening Test Simulator</h3>
              <p class="text-[11px] text-slate-400">4 Bo'lim • 40 ta Savol • Haqiqiy Imtihon Standarti</p>
            </div>
          </div>
          <button id="btn-audio-toggle" onclick="toggleAudioSim()" class="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition flex items-center gap-1">
            <span id="audio-icon">▶</span> <span id="audio-state-text">Audio O'ynatish</span>
          </button>
        </div>

        <div class="space-y-1.5">
          <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
            <div id="audio-progress" class="bg-gradient-to-r from-emerald-500 to-teal-400 h-full w-0 transition-all duration-300"></div>
          </div>
          <div class="flex justify-between text-[10px] text-slate-400 font-mono">
            <span id="audio-cur-time">00:00</span>
            <span id="audio-tot-time">30:00</span>
          </div>
        </div>

        <div class="grid grid-cols-4 gap-1.5 text-xs font-semibold">
          <button onclick="filterListeningSection(1)" id="l-sec-1" class="py-1.5 rounded-lg bg-blue-600 text-white text-center">Sec 1 (1–10)</button>
          <button onclick="filterListeningSection(2)" id="l-sec-2" class="py-1.5 rounded-lg bg-slate-800 text-slate-300 text-center">Sec 2 (11–20)</button>
          <button onclick="filterListeningSection(3)" id="l-sec-3" class="py-1.5 rounded-lg bg-slate-800 text-slate-300 text-center">Sec 3 (21–30)</button>
          <button onclick="filterListeningSection(4)" id="l-sec-4" class="py-1.5 rounded-lg bg-slate-800 text-slate-300 text-center">Sec 4 (31–40)</button>
        </div>
      </div>

      <div class="card-surface p-3 rounded-xl">
        <button onclick="toggleTapescript()" class="w-full flex justify-between items-center text-xs font-semibold text-slate-300">
          <span>📜 Tapescript & Audio Matnini Ko'rsatish</span>
          <span id="ts-arrow">▼</span>
        </button>
        <div id="tapescript-content" class="hidden mt-2 pt-2 border-t border-slate-800 text-xs text-slate-400 leading-relaxed space-y-2"></div>
      </div>

      <div id="listening-questions-container" class="space-y-2.5"></div>

      <div class="card-surface p-4 rounded-2xl flex items-center justify-between">
        <div>
          <span class="text-xs text-slate-400 block font-medium">Barcha javoblar kiritildimi?</span>
          <span id="listening-score-preview" class="text-xs font-bold text-white">40 tadan 0 ta yechildi</span>
        </div>
        <button onclick="gradeListeningTest()" class="py-2.5 px-4 rounded-xl bg-emerald-600 hover:bg-emerald-500 active:scale-95 text-white font-bold text-xs shadow-lg shadow-emerald-600/30 transition">
          Testni Tekshirish & Ballni Ko'rish ✅
        </button>
      </div>

      <div id="listening-res-modal" class="hidden card-surface p-5 rounded-2xl text-center space-y-3">
        <h3 class="text-base font-extrabold text-white">🎧 IELTS Listening Natijasi</h3>
        <div class="flex items-baseline justify-center gap-1.5 py-1">
          <span id="l-res-band" class="text-5xl font-extrabold text-emerald-400 font-mono">8.0</span>
          <span class="text-sm font-bold text-slate-500">/ 9.0</span>
        </div>
        <p id="l-res-details" class="text-xs text-slate-300 font-medium"></p>
        <button onclick="restartListeningTest()" class="py-2 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs text-white font-semibold">
          Qayta Topshirish
        </button>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- TAB 4: IELTS READING FULL TEST -->
    <!-- ========================================================================= -->
    <div id="tab-reading" class="tab-content space-y-3.5">
      <div class="grid grid-cols-3 gap-1.5 text-xs font-semibold">
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

      <div class="card-surface p-4 sm:p-5 rounded-2xl space-y-2.5 max-h-72 overflow-y-auto">
        <div class="flex items-center justify-between pb-1.5 border-b border-slate-800">
          <h3 id="reading-p-title" class="text-xs font-extrabold text-white tracking-tight"></h3>
          <span class="text-[10px] text-blue-400 font-bold px-2 py-0.5 rounded bg-blue-500/10">Academic Reading</span>
        </div>
        <div id="reading-p-text" class="text-xs text-slate-300 leading-relaxed space-y-2 whitespace-pre-line"></div>
      </div>

      <div id="reading-questions-container" class="space-y-2.5"></div>

      <div class="card-surface p-4 rounded-2xl flex items-center justify-between">
        <div>
          <span class="text-xs text-slate-400 block font-medium">IELTS Reading Balingiz</span>
          <span id="reading-score-preview" class="text-xs font-bold text-white">40 tadan 0 ta kiritildi</span>
        </div>
        <button onclick="gradeReadingTest()" class="py-2.5 px-4 rounded-xl bg-blue-600 hover:bg-blue-500 active:scale-95 text-white font-bold text-xs shadow-lg shadow-blue-600/30 transition">
          Reading Ballini Hisoblash 📖
        </button>
      </div>

      <div id="reading-res-modal" class="hidden card-surface p-5 rounded-2xl text-center space-y-3">
        <h3 class="text-base font-extrabold text-white">📖 IELTS Reading Natijasi</h3>
        <div class="flex items-baseline justify-center gap-1.5 py-1">
          <span id="r-res-band" class="text-5xl font-extrabold text-blue-400 font-mono">7.5</span>
          <span class="text-sm font-bold text-slate-500">/ 9.0</span>
        </div>
        <p id="r-res-details" class="text-xs text-slate-300 font-medium"></p>
        <button onclick="restartReadingTest()" class="py-2 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs text-white font-semibold">
          Qayta Topshirish
        </button>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- TAB 5: IELTS WRITING BANK (42 TOPICS) -->
    <!-- ========================================================================= -->
    <div id="tab-writing" class="tab-content space-y-3.5">
      <div class="card-surface p-3 rounded-2xl space-y-2">
        <div class="flex items-center justify-between">
          <h3 class="text-xs font-bold text-white">✍️ IELTS Writing Task 1 & 2 Banki</h3>
          <span class="text-[10px] font-bold text-amber-400 px-2 py-0.5 rounded bg-amber-500/10 border border-amber-500/20">42 ta Mavzu</span>
        </div>
        <div class="flex gap-1.5 overflow-x-auto pb-1 scrollbar-none text-xs font-semibold">
          <button onclick="filterWriting('all')" id="w-filter-all" class="py-1.5 px-3 rounded-xl bg-blue-600 text-white whitespace-nowrap">Barchasi (42)</button>
          <button onclick="filterWriting('t1')" id="w-filter-t1" class="py-1.5 px-3 rounded-xl bg-slate-800 text-slate-300 whitespace-nowrap">Task 1 (21 ta)</button>
          <button onclick="filterWriting('t2')" id="w-filter-t2" class="py-1.5 px-3 rounded-xl bg-slate-800 text-slate-300 whitespace-nowrap">Task 2 (21 ta)</button>
          <button onclick="filterWriting('opinion')" id="w-filter-op" class="py-1.5 px-3 rounded-xl bg-slate-800 text-slate-300 whitespace-nowrap">Opinion Essays</button>
          <button onclick="filterWriting('discussion')" id="w-filter-disc" class="py-1.5 px-3 rounded-xl bg-slate-800 text-slate-300 whitespace-nowrap">Discussion</button>
          <button onclick="filterWriting('solution')" id="w-filter-sol" class="py-1.5 px-3 rounded-xl bg-slate-800 text-slate-300 whitespace-nowrap">Problem/Solution</button>
        </div>
      </div>

      <div id="writing-cards-container" class="space-y-3"></div>
    </div>

    <!-- ========================================================================= -->
    <!-- TAB 6: SCORE & GRANT PREDICTOR -->
    <!-- ========================================================================= -->
    <div id="tab-predict" class="tab-content space-y-3.5">
      <div class="grid grid-cols-2 p-1 rounded-xl bg-slate-900 border border-slate-800 text-xs font-semibold">
        <button id="btn-ielts" onclick="switchPredictMode('ielts')" class="py-2 rounded-lg bg-blue-600 text-white shadow-md transition">
          🇬🇧 IELTS (Band 9)
        </button>
        <button id="btn-sat" onclick="switchPredictMode('sat')" class="py-2 rounded-lg text-slate-400 hover:text-white transition">
          🎯 Digital SAT (1600)
        </button>
      </div>

      <div class="card-surface p-5 rounded-2xl text-center space-y-2 relative overflow-hidden">
        <div class="absolute -top-12 -right-12 w-32 h-32 bg-blue-500/10 rounded-full blur-2xl pointer-events-none"></div>
        <span class="text-xs font-medium uppercase tracking-wider text-slate-400 block" id="hero-subtitle">
          Taxminiy IELTS Overall Balingiz
        </span>
        <div class="flex items-baseline justify-center gap-1.5 py-1">
          <span id="hero-score" class="text-5xl font-extrabold tracking-tight bg-gradient-to-r from-blue-400 via-indigo-300 to-white bg-clip-text text-transparent">
            7.5
          </span>
          <span id="hero-max" class="text-sm font-bold text-slate-500">/ 9.0</span>
        </div>
        <div class="flex items-center justify-center gap-2">
          <span id="hero-badge" class="inline-flex items-center gap-1 text-xs font-semibold px-3 py-1 rounded-full bg-emerald-500/15 text-emerald-400 border border-emerald-500/25">
            ✨ CEFR C1 (Advanced)
          </span>
        </div>
      </div>

      <div id="ielts-box" class="card-surface p-4 rounded-2xl space-y-3">
        <div>
          <div class="flex justify-between text-xs mb-1.5">
            <span class="font-semibold text-slate-300">🎧 Listening (To'g'ri javoblar soni)</span>
            <span id="txt-l" class="font-mono font-bold text-blue-400">33 / 40 (Band 7.5)</span>
          </div>
          <input type="range" min="10" max="40" value="33" id="rng-l" oninput="calcIelts()" class="w-full bg-slate-800 accent-blue-500">
        </div>
        <div class="pt-2 border-t border-slate-800">
          <div class="flex justify-between text-xs mb-1.5">
            <span class="font-semibold text-slate-300">📖 Reading (To'g'ri javoblar soni)</span>
            <span id="txt-r" class="font-mono font-bold text-blue-400">30 / 40 (Band 7.0)</span>
          </div>
          <input type="range" min="10" max="40" value="30" id="rng-r" oninput="calcIelts()" class="w-full bg-slate-800 accent-blue-500">
        </div>
        <div class="grid grid-cols-2 gap-2.5 pt-2 border-t border-slate-800">
          <div>
            <label class="block text-xs font-semibold text-slate-400 mb-1">✍️ Writing</label>
            <select id="sel-w" onchange="calcIelts()" class="w-full py-2 px-2.5 rounded-xl bg-slate-800 border border-slate-700 text-xs font-medium text-white focus:outline-none">
              <option value="5.5">Band 5.5</option>
              <option value="6.0">Band 6.0</option>
              <option value="6.5" selected>Band 6.5</option>
              <option value="7.0">Band 7.0</option>
              <option value="7.5">Band 7.5</option>
              <option value="8.0">Band 8.0</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-400 mb-1">🗣 Speaking</label>
            <select id="sel-s" onchange="calcIelts()" class="w-full py-2 px-2.5 rounded-xl bg-slate-800 border border-slate-700 text-xs font-medium text-white focus:outline-none">
              <option value="5.5">Band 5.5</option>
              <option value="6.0">Band 6.0</option>
              <option value="6.5">Band 6.5</option>
              <option value="7.0" selected>Band 7.0</option>
              <option value="7.5">Band 7.5</option>
              <option value="8.0">Band 8.0</option>
            </select>
          </div>
        </div>
      </div>

      <div id="sat-box" class="hidden card-surface p-4 rounded-2xl space-y-3">
        <div>
          <div class="flex justify-between text-xs mb-1.5">
            <span class="font-semibold text-slate-300">📐 SAT Math (200 - 800)</span>
            <span id="txt-sat-m" class="font-mono font-bold text-amber-400">740 / 800</span>
          </div>
          <input type="range" min="300" max="800" step="10" value="740" id="rng-sat-m" oninput="calcSat()" class="w-full bg-slate-800 accent-amber-500">
        </div>
        <div class="pt-2 border-t border-slate-800">
          <div class="flex justify-between text-xs mb-1.5">
            <span class="font-semibold text-slate-300">📝 Reading & Writing (200 - 800)</span>
            <span id="txt-sat-rw" class="font-mono font-bold text-amber-400">680 / 800</span>
          </div>
          <input type="range" min="300" max="800" step="10" value="680" id="rng-sat-rw" oninput="calcSat()" class="w-full bg-slate-800 accent-amber-500">
        </div>
      </div>

      <div class="card-surface p-4 rounded-2xl space-y-2.5">
        <div class="flex items-center justify-between pb-1 border-b border-slate-800">
          <h2 class="text-xs font-bold uppercase tracking-wider text-slate-300">🏛 Mos Universitetlar & Grantlar</h2>
          <span class="text-xs text-blue-400 font-medium">Uzbekistan & Global</span>
        </div>
        <div id="uni-container" class="space-y-2"></div>
      </div>

      <div class="grid grid-cols-2 gap-2.5">
        <button onclick="shareScore()" class="py-3 px-4 rounded-xl bg-blue-600 hover:bg-blue-700 active:scale-95 text-white font-bold text-xs flex items-center justify-center gap-1.5 shadow-lg shadow-blue-600/30 transition">
          <span>Telegramda Ulashish</span> 🚀
        </button>
        <button onclick="switchMainTab('sat-hub')" class="py-3 px-4 rounded-xl bg-amber-600 hover:bg-amber-700 active:scale-95 text-white font-bold text-xs flex items-center justify-center gap-1.5 shadow-lg shadow-amber-600/30 transition">
          <span>45 ta SAT Mockni Ko'rish</span> 🎯
        </button>
      </div>
    </div>

  </div>

  <!-- EMBEDDED EXAM BANK DATA & ENGINE -->
  <script>
    const EXAM_DATA = {json_str};

    // Fullscreen and Telegram Init
    function requestAppFullscreen() {{
      if (window.Telegram && window.Telegram.WebApp) {{
        const tg = window.Telegram.WebApp;
        tg.ready();
        tg.expand();
        if (tg.requestFullscreen) {{
          try {{ tg.requestFullscreen(); }} catch (e) {{}}
        }}
        if (tg.disableVerticalSwipes) {{
          try {{ tg.disableVerticalSwipes(); }} catch (e) {{}}
        }}
      }}
    }}

    requestAppFullscreen();

    // ==========================================
    // TAB SWITCHER
    // ==========================================
    function switchMainTab(tab) {{
      const tabs = ['sat-hub', 'ielts-hub', 'listening', 'reading', 'writing', 'predict'];
      tabs.forEach(t => {{
        const btn = document.getElementById('nav-' + t);
        const content = document.getElementById('tab-' + t);
        if (btn && content) {{
          if (t === tab) {{
            btn.className = 'nav-active px-3 py-2 rounded-xl bg-blue-600 text-white whitespace-nowrap transition';
            content.classList.add('active');
          }} else {{
            btn.className = 'px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 whitespace-nowrap transition';
            content.classList.remove('active');
          }}
        }}
      }});
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    // ==========================================
    // 1. SAT MOCKS HUB (45 FULL MOCKS)
    // ==========================================
    const satMocks = EXAM_DATA.sat_mocks || [];
    let activeSatCategory = 'all';

    function filterSatMocks(cat) {{
      activeSatCategory = cat;
      const cats = ['all', 'bb', 'pr', 'cb', 'iv'];
      cats.forEach(c => {{
        const btn = document.getElementById('sat-f-' + c);
        if (btn) {{
          if ((cat === 'all' && c === 'all') ||
              (cat === 'bluebook' && c === 'bb') ||
              (cat === 'princeton' && c === 'pr') ||
              (cat === 'cb_bank' && c === 'cb') ||
              (cat === 'master' && c === 'iv')) {{
            btn.className = 'py-1.5 px-3 rounded-xl bg-blue-600 text-white whitespace-nowrap';
          }} else {{
            btn.className = 'py-1.5 px-3 rounded-xl bg-slate-800 text-slate-300 whitespace-nowrap';
          }}
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
              ${{m.category_label}}
            </span>
            <span class="text-[10px] font-semibold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
              ${{m.status}}
            </span>
          </div>

          <h4 class="text-xs font-extrabold text-white">${{m.title}}</h4>
          <p class="text-[11px] text-slate-400">${{m.description}}</p>

          <div class="flex flex-wrap gap-2 text-[10px] text-slate-300 pt-1">
            <span class="px-2 py-0.5 rounded bg-slate-900 border border-slate-800">⏱ ${{m.duration}}</span>
            <span class="px-2 py-0.5 rounded bg-slate-900 border border-slate-800">📝 ${{m.total_questions}} ta savol</span>
            <span class="px-2 py-0.5 rounded bg-slate-900 border border-slate-800">🎯 ${{m.score_scale}}</span>
          </div>

          <div class="pt-2 border-t border-slate-800 flex justify-end">
            <button onclick="startSatMockTest('${{m.id}}')" class="py-2 px-4 rounded-xl bg-blue-600 hover:bg-blue-500 active:scale-95 text-white font-bold text-xs flex items-center gap-1.5 shadow-md shadow-blue-600/30 transition">
              <span>Testni Boshlash</span> 🚀
            </button>
          </div>
        </div>
      `).join('');
    }}

    // SAT Active Runner Logic
    let currentSatMock = null;
    let satRunnerQuestions = [];
    let satRunnerIdx = 0;
    const satRunnerAnswers = {{}};
    const satRunnerFlags = new Set();
    let satRunnerSeconds = 45 * 60;
    let satRunnerTimer = null;

    function startSatMockTest(mockId) {{
      const found = satMocks.find(m => m.id === mockId) || satMocks[0];
      currentSatMock = found;
      satRunnerQuestions = found.sample_test_questions || EXAM_DATA.sat_default_test || [];
      satRunnerIdx = 0;
      for (const k in satRunnerAnswers) delete satRunnerAnswers[k];
      satRunnerFlags.clear();
      satRunnerSeconds = 45 * 60;

      document.getElementById('sat-catalog-view').classList.add('hidden');
      document.getElementById('sat-runner-view').classList.remove('hidden');
      document.getElementById('sat-runner-card').classList.remove('hidden');
      document.getElementById('sat-runner-results').classList.add('hidden');

      document.getElementById('sat-runner-title').innerText = found.title;
      renderSatRunnerPills();
      loadSatRunnerQuestion(0);
      startSatRunnerTimer();
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    function exitSatRunner() {{
      if (satRunnerTimer) clearInterval(satRunnerTimer);
      document.getElementById('sat-runner-view').classList.add('hidden');
      document.getElementById('sat-catalog-view').classList.remove('hidden');
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    function startSatRunnerTimer() {{
      if (satRunnerTimer) clearInterval(satRunnerTimer);
      satRunnerTimer = setInterval(() => {{
        if (satRunnerSeconds > 0) {{
          satRunnerSeconds--;
          const m = Math.floor(satRunnerSeconds / 60);
          const s = satRunnerSeconds % 60;
          document.getElementById('sat-runner-timer').innerText = 
            `${{m.toString().padStart(2, '0')}}:${{s.toString().padStart(2, '0')}}`;
        }} else {{
          clearInterval(satRunnerTimer);
          finishSatRunner();
        }}
      }}, 1000);
    }}

    function renderSatRunnerPills() {{
      const nav = document.getElementById('sat-runner-pills');
      nav.innerHTML = satRunnerQuestions.map((q, idx) => {{
        const isAnswered = satRunnerAnswers[idx] !== undefined;
        const isFlagged = satRunnerFlags.has(idx);
        const isActive = idx === satRunnerIdx;
        let bg = 'bg-slate-800 text-slate-400';
        if (isActive) bg = 'bg-blue-600 text-white font-bold ring-2 ring-blue-400';
        else if (isFlagged) bg = 'bg-amber-500/20 text-amber-400 border border-amber-500/40';
        else if (isAnswered) bg = 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30';

        return `<button onclick="loadSatRunnerQuestion(${{idx}})" class="w-7 h-7 rounded-lg text-[11px] shrink-0 font-mono transition ${{bg}}">${{idx + 1}}</button>`;
      }}).join('');
    }}

    function loadSatRunnerQuestion(idx) {{
      satRunnerIdx = idx;
      renderSatRunnerPills();
      const q = satRunnerQuestions[idx];

      document.getElementById('sat-runner-domain').innerText = `${{q.section}} • ${{q.domain}} (${{q.difficulty}})`;
      document.getElementById('sat-runner-stem').innerText = q.question;

      const pBox = document.getElementById('sat-runner-passage');
      if (q.passage && q.passage.trim().length > 0) {{
        pBox.classList.remove('hidden');
        pBox.innerText = q.passage;
      }} else {{
        pBox.classList.add('hidden');
      }}

      // Flag
      const flagBtn = document.getElementById('sat-btn-flag');
      if (satRunnerFlags.has(idx)) {{
        flagBtn.className = 'p-2 rounded-xl bg-amber-500/20 text-amber-400 border border-amber-500/40 text-xs';
      }} else {{
        flagBtn.className = 'p-2 rounded-xl bg-slate-800 text-slate-400 hover:text-amber-400 border border-slate-700 text-xs';
      }}

      // Options
      const optBox = document.getElementById('sat-runner-options');
      const selected = satRunnerAnswers[idx];
      optBox.innerHTML = q.options.map(opt => {{
        const isSel = selected === opt.key;
        const optClass = isSel
          ? 'bg-blue-600/20 border-blue-500 text-white font-semibold'
          : 'bg-slate-900 border-slate-800 text-slate-300 hover:border-slate-700';
        return `
          <button onclick="selectSatRunnerAnswer('${{opt.key}}')" class="w-full p-3 rounded-xl border text-left text-xs transition flex items-start gap-2.5 ${{optClass}}">
            <span class="w-5 h-5 rounded-md flex items-center justify-center font-bold text-[10px] ${{isSel ? 'bg-blue-600 text-white' : 'bg-slate-800 text-slate-400'}}">
              ${{opt.key}}
            </span>
            <span class="flex-1">${{opt.text}}</span>
          </button>
        `;
      }}).join('');

      // Feedback
      const fbBox = document.getElementById('sat-runner-feedback');
      if (selected !== undefined) {{
        fbBox.classList.remove('hidden');
        const isCorrect = selected === q.correct;
        document.getElementById('sat-fb-status').innerHTML = isCorrect
          ? `<span class="text-emerald-400">✅ To'g'ri javob (${{q.correct}})!</span>`
          : `<span class="text-rose-400">❌ Noto'g'ri. To'g'ri javob: ${{q.correct}}</span>`;
        document.getElementById('sat-fb-expl').innerText = q.explanation || "College Board rasmiy tahlili.";
        document.getElementById('sat-fb-hack').innerText = q.strategy ? `⚡ SAT Strategiyasi: ${{q.strategy}}` : "";
      }} else {{
        fbBox.classList.add('hidden');
      }}

      document.getElementById('sat-btn-prev').disabled = idx === 0;
      document.getElementById('sat-btn-next').innerText = idx === satRunnerQuestions.length - 1 ? "Natijani Ko'rish →" : "Keyingisi →";
    }}

    function selectSatRunnerAnswer(key) {{
      satRunnerAnswers[satRunnerIdx] = key;
      loadSatRunnerQuestion(satRunnerIdx);
    }}

    function toggleSatFlag() {{
      if (satRunnerFlags.has(satRunnerIdx)) {{
        satRunnerFlags.delete(satRunnerIdx);
      }} else {{
        satRunnerFlags.add(satRunnerIdx);
      }}
      renderSatRunnerPills();
      loadSatRunnerQuestion(satRunnerIdx);
    }}

    function prevSatRunnerQ() {{
      if (satRunnerIdx > 0) loadSatRunnerQuestion(satRunnerIdx - 1);
    }}

    function nextSatRunnerQ() {{
      if (satRunnerIdx < satRunnerQuestions.length - 1) {{
        loadSatRunnerQuestion(satRunnerIdx + 1);
      }} else {{
        finishSatRunner();
      }}
    }}

    function finishSatRunner() {{
      if (satRunnerTimer) clearInterval(satRunnerTimer);
      let rwCorrect = 0;
      let mathCorrect = 0;

      satRunnerQuestions.forEach((q, idx) => {{
        if (satRunnerAnswers[idx] === q.correct) {{
          if (q.section === 'Reading & Writing') rwCorrect++;
          else mathCorrect++;
        }}
      }});

      const totalQ = satRunnerQuestions.length;
      const rwTotal = satRunnerQuestions.filter(q => q.section === 'Reading & Writing').length || 10;
      const mathTotal = totalQ - rwTotal || 10;

      const rwScore = Math.round(200 + (rwCorrect / rwTotal) * 600);
      const mathScore = Math.round(200 + (mathCorrect / mathTotal) * 600);
      const totalScore = rwScore + mathScore;

      document.getElementById('sat-runner-card').classList.add('hidden');
      document.getElementById('sat-runner-results').classList.remove('hidden');

      document.getElementById('sat-rw-score').innerText = rwScore;
      document.getElementById('sat-m-score').innerText = mathScore;
      document.getElementById('sat-tot-score').innerText = totalScore;

      document.getElementById('sat-score-desc').innerHTML = `
        <b>${{currentSatMock.title}}</b> yakunlandi.<br>
        Siz ${{totalQ}} ta savoldan <b>${{rwCorrect + mathCorrect}}</b> tasiga to'g'ri javob berdingiz.<br>
        • Reading & Writing: ${{rwCorrect}}/${{rwTotal}} (${{rwScore}} ball)<br>
        • Math: ${{mathCorrect}}/${{mathTotal}} (${{mathScore}} ball)
      `;
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    // ==========================================
    // 2. IELTS MOCKS HUB (45 FULL MOCKS)
    // ==========================================
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
            <button onclick="switchMainTab('listening')" class="py-1.5 px-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center gap-1 transition">
              <span>Listening</span> 🎧
            </button>
            <button onclick="switchMainTab('reading')" class="py-1.5 px-3 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs flex items-center gap-1 transition">
              <span>Reading</span> 📖
            </button>
            <button onclick="switchMainTab('writing')" class="py-1.5 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs border border-slate-700 transition">
              <span>Writing</span> ✍️
            </button>
          </div>
        </div>
      `).join('');
    }}

    // ==========================================
    // 3. IELTS LISTENING (40 QUESTIONS)
    // ==========================================
    const listeningData = EXAM_DATA.ielts_listening || [];
    let activeListeningSection = 1;
    const listeningAnswers = {{}};
    let audioPlaying = false;
    let audioTimer = null;
    let audioElapsed = 0;

    function toggleAudioSim() {{
      const btnIcon = document.getElementById('audio-icon');
      const btnText = document.getElementById('audio-state-text');
      const progressBar = document.getElementById('audio-progress');

      if (!audioPlaying) {{
        audioPlaying = true;
        btnIcon.innerText = "⏸";
        btnText.innerText = "Pauza";
        audioTimer = setInterval(() => {{
          audioElapsed++;
          const curM = Math.floor(audioElapsed / 60);
          const curS = audioElapsed % 60;
          document.getElementById('audio-cur-time').innerText = 
            `${{curM.toString().padStart(2, '0')}}:${{curS.toString().padStart(2, '0')}}`;
          const pct = Math.min(100, (audioElapsed / (30 * 60)) * 100);
          progressBar.style.width = pct + '%';
        }}, 1000);
      }} else {{
        audioPlaying = false;
        btnIcon.innerText = "▶";
        btnText.innerText = "Davom ettirish";
        clearInterval(audioTimer);
      }}
    }}

    function filterListeningSection(sec) {{
      activeListeningSection = sec;
      for (let i = 1; i <= 4; i++) {{
        const btn = document.getElementById('l-sec-' + i);
        if (i === sec) {{
          btn.className = 'py-1.5 rounded-lg bg-blue-600 text-white text-center';
        }} else {{
          btn.className = 'py-1.5 rounded-lg bg-slate-800 text-slate-300 text-center';
        }}
      }}
      renderListeningQuestions();
      updateTapescriptContent();
    }}

    function toggleTapescript() {{
      const content = document.getElementById('tapescript-content');
      const arrow = document.getElementById('ts-arrow');
      if (content.classList.contains('hidden')) {{
        content.classList.remove('hidden');
        arrow.innerText = '▲';
        updateTapescriptContent();
      }} else {{
        content.classList.add('hidden');
        arrow.innerText = '▼';
      }}
    }}

    function updateTapescriptContent() {{
      const container = document.getElementById('tapescript-content');
      const summaries = {{
        1: "<b>Section 1 Context & Transcript:</b><br>Officer: 'Good morning, University Housing Office, Sarah speaking.'<br>Student: 'Hello! I'm an incoming international student, Alex Turner (T-U-R-N-E-R). My contact number is 07892 451209. I need a flat near campus starting September 15th.'<br>Officer: 'We have 14 Meadowbank Road. Rent is £650 per month including water and WiFi. A security deposit of £400 is required...'",
        2: "<b>Section 2 Guide:</b><br>Coordinator: 'Welcome everyone to the Royal Botanical Gardens! The solar glasshouse opened in 2022. Volunteers assist visitors with trail maps and visitor inquiries. Please store your bags in the Staff Pavilion lockers. The Amazonian orchids are undergoing biological pest control...'",
        3: "<b>Section 3 Tutorial:</b><br>Prof. Vance: 'Welcome Mark and Chloe. Your focus on tidal stream turbines over offshore wind is solid because seawater is roughly 800 times denser than air, providing predictable baselines. Saltwater corrosion requires carbon fiber composites...'",
        4: "<b>Section 4 Academic Lecture:</b><br>Dr. Hughes: 'Working memory operates through three primary slave systems governed by the central executive. The phonological loop retains speech sounds for approximately 2 seconds before trace decay...'"
      }};
      container.innerHTML = summaries[activeListeningSection] || "";
    }}

    function renderListeningQuestions() {{
      const container = document.getElementById('listening-questions-container');
      const questions = listeningData.filter(q => q.section === activeListeningSection);

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
              <input type="text" value="${{savedAns}}" onchange="setListeningAnswer(${{q.num}}, this.value)" placeholder="Javobingizni yozing..." class="flex-1 py-1.5 px-3 rounded-lg bg-slate-900 border border-slate-700 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-500">
            </div>
          `;
        }}

        return `
          <div class="card-surface p-3.5 rounded-xl space-y-1.5" id="l-card-${{q.num}}">
            <div class="flex justify-between items-start">
              <span class="text-[11px] font-mono font-bold text-blue-400">Savol #${{q.num}}</span>
              <span class="text-[10px] uppercase font-semibold text-slate-500">${{q.type}}</span>
            </div>
            <p class="text-xs font-semibold text-white">${{q.text}}</p>
            ${{inputHtml}}
            <div id="l-expl-${{q.num}}" class="hidden text-[11px] text-slate-300 pt-1.5 border-t border-slate-800"></div>
          </div>
        `;
      }}).join('');

      updateListeningPreview();
    }}

    function setListeningAnswer(num, val) {{
      listeningAnswers[num] = val.trim();
      updateListeningPreview();
      renderListeningQuestions();
    }}

    function updateListeningPreview() {{
      const count = Object.keys(listeningAnswers).length;
      document.getElementById('listening-score-preview').innerText = `40 tadan ${{count}} ta kiritildi`;
    }}

    function gradeListeningTest() {{
      let correct = 0;
      listeningData.forEach(q => {{
        const user = (listeningAnswers[q.num] || "").toLowerCase().trim();
        const expected = q.ans.toLowerCase().trim();
        const isMatch = user === expected || (user.includes(expected) && expected.length > 2);
        const card = document.getElementById('l-card-' + q.num);
        const expl = document.getElementById('l-expl-' + q.num);

        if (isMatch) correct++;
        if (card) {{
          card.classList.remove('border-slate-800');
          card.classList.add(isMatch ? 'border-emerald-500/50' : 'border-rose-500/50');
        }}
        if (expl) {{
          expl.classList.remove('hidden');
          expl.innerHTML = isMatch
            ? `<span class="text-emerald-400 font-bold">✅ To'g'ri! (${{q.ans}})</span> • ${{q.expl}}`
            : `<span class="text-rose-400 font-bold">❌ To'g'ri javob: ${{q.ans}}</span> • ${{q.expl}}`;
        }}
      }});

      const band = rawToBand(correct);
      const modal = document.getElementById('listening-res-modal');
      modal.classList.remove('hidden');
      document.getElementById('l-res-band').innerText = band.toFixed(1);
      document.getElementById('l-res-details').innerText = 
        `Siz 40 ta savoldan ${{correct}} tasiga to'g'ri javob berdingiz! CEFR: ${{band >= 7.0 ? 'C1/C2 Yuqori Daraja' : 'B2 Tayyor'}}`;
      modal.scrollIntoView({{ behavior: 'smooth' }});
    }}

    function restartListeningTest() {{
      for (const k in listeningAnswers) delete listeningAnswers[k];
      document.getElementById('listening-res-modal').classList.add('hidden');
      renderListeningQuestions();
    }}

    // ==========================================
    // 4. IELTS READING (40 QUESTIONS)
    // ==========================================
    const readingData = EXAM_DATA.ielts_reading || [];
    let activeReadingPassage = 1;
    const readingAnswers = {{}};

    function switchReadingPassage(pNum) {{
      activeReadingPassage = pNum;
      for (let i = 1; i <= 3; i++) {{
        const btn = document.getElementById('btn-p' + i);
        if (i === pNum) {{
          btn.className = 'py-2 rounded-xl bg-blue-600 text-white text-center';
        }} else {{
          btn.className = 'py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 text-center';
        }}
      }}
      renderReadingPassage();
      renderReadingQuestions();
    }}

    function renderReadingPassage() {{
      const firstQ = readingData.find(q => q.passage_num === activeReadingPassage);
      if (firstQ) {{
        document.getElementById('reading-p-title').innerText = firstQ.passage_title;
        document.getElementById('reading-p-text').innerText = firstQ.passage_text;
      }}
    }}

    function renderReadingQuestions() {{
      const container = document.getElementById('reading-questions-container');
      const questions = readingData.filter(q => q.passage_num === activeReadingPassage);

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
              <input type="text" value="${{savedAns}}" onchange="setReadingAnswer(${{q.num}}, this.value)" placeholder="Bo'sh joyga so'z yozing..." class="flex-1 py-1.5 px-3 rounded-lg bg-slate-900 border border-slate-700 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-500">
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
    }}

    function setReadingAnswer(num, val) {{
      readingAnswers[num] = val.trim();
      updateReadingPreview();
      renderReadingQuestions();
    }}

    function updateReadingPreview() {{
      const count = Object.keys(readingAnswers).length;
      document.getElementById('reading-score-preview').innerText = `40 tadan ${{count}} ta kiritildi`;
    }}

    function gradeReadingTest() {{
      let correct = 0;
      readingData.forEach(q => {{
        const user = (readingAnswers[q.num] || "").toUpperCase().trim();
        const expected = q.ans.toUpperCase().trim();
        const isMatch = user === expected || (user.includes(expected) && expected.length > 2);
        const card = document.getElementById('r-card-' + q.num);
        const expl = document.getElementById('r-expl-' + q.num);

        if (isMatch) correct++;
        if (card) {{
          card.classList.remove('border-slate-800');
          card.classList.add(isMatch ? 'border-emerald-500/50' : 'border-rose-500/50');
        }}
        if (expl) {{
          expl.classList.remove('hidden');
          expl.innerHTML = isMatch
            ? `<span class="text-emerald-400 font-bold">✅ To'g'ri! (${{q.ans}})</span> • ${{q.expl}}`
            : `<span class="text-rose-400 font-bold">❌ To'g'ri javob: ${{q.ans}}</span> • ${{q.expl}}`;
        }}
      }});

      const band = rawToBand(correct);
      const modal = document.getElementById('reading-res-modal');
      modal.classList.remove('hidden');
      document.getElementById('r-res-band').innerText = band.toFixed(1);
      document.getElementById('r-res-details').innerText = 
        `Siz 40 ta savoldan ${{correct}} tasiga to'g'ri javob berdingiz! Taxminiy Reading Balingiz: Band ${{band.toFixed(1)}}`;
      modal.scrollIntoView({{ behavior: 'smooth' }});
    }}

    function restartReadingTest() {{
      for (const k in readingAnswers) delete readingAnswers[k];
      document.getElementById('reading-res-modal').classList.add('hidden');
      renderReadingQuestions();
    }}

    // ==========================================
    // 5. IELTS WRITING BANK (42 TOPICS)
    // ==========================================
    const writingT1 = EXAM_DATA.ielts_writing_t1 || [];
    const writingT2 = EXAM_DATA.ielts_writing_t2 || [];
    let activeWritingFilter = 'all';

    function filterWriting(filter) {{
      activeWritingFilter = filter;
      const filters = ['all', 't1', 't2', 'op', 'disc', 'sol'];
      filters.forEach(f => {{
        const btn = document.getElementById('w-filter-' + f);
        if (btn) {{
          if (f === filter || (filter === 'opinion' && f === 'op') || (filter === 'discussion' && f === 'disc') || (filter === 'solution' && f === 'sol')) {{
            btn.className = 'py-1.5 px-3 rounded-xl bg-blue-600 text-white whitespace-nowrap';
          }} else {{
            btn.className = 'py-1.5 px-3 rounded-xl bg-slate-800 text-slate-300 whitespace-nowrap';
          }}
        }}
      }});
      renderWritingCards();
    }}

    function renderWritingCards() {{
      const container = document.getElementById('writing-cards-container');
      let items = [];

      if (activeWritingFilter === 'all') {{
        items = [...writingT1.map(x => ({{...x, isT1: true}})), ...writingT2.map(x => ({{...x, isT1: false}}))];
      }} else if (activeWritingFilter === 't1') {{
        items = writingT1.map(x => ({{...x, isT1: true}}));
      }} else if (activeWritingFilter === 't2') {{
        items = writingT2.map(x => ({{...x, isT1: false}}));
      }} else if (activeWritingFilter === 'opinion') {{
        items = writingT2.filter(x => x.type.includes('Opinion') || x.type.includes('Agree')).map(x => ({{...x, isT1: false}}));
      }} else if (activeWritingFilter === 'discussion') {{
        items = writingT2.filter(x => x.type.includes('Discuss')).map(x => ({{...x, isT1: false}}));
      }} else if (activeWritingFilter === 'solution') {{
        items = writingT2.filter(x => x.type.includes('Problem')).map(x => ({{...x, isT1: false}}));
      }}

      container.innerHTML = items.map((w, idx) => `
        <div class="card-surface p-4 rounded-2xl space-y-2.5 border border-slate-800 hover:border-slate-700 transition">
          <div class="flex items-center justify-between">
            <span class="text-[10px] font-bold px-2 py-0.5 rounded ${{w.isT1 ? 'bg-indigo-500/20 text-indigo-400 border border-indigo-500/30' : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'}}">
              ${{w.isT1 ? 'Task 1: Academic Report' : 'Task 2: Academic Essay'}} • ${{w.type}}
            </span>
            <span class="text-[10px] text-slate-500 font-mono">#${{idx + 1}}</span>
          </div>

          <h4 class="text-xs font-bold text-white">${{w.title}}</h4>
          
          <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-300 leading-relaxed italic">
            "${{w.prompt}}"
          </div>

          <div class="space-y-1.5 text-xs text-slate-300">
            ${{w.isT1 ? `
              <div><b class="text-slate-400">Asosiy ko'rsatkichlar:</b> ${{w.key_features}}</div>
              <div><b class="text-slate-400">Band 9 Overview:</b> ${{w.overview}}</div>
            ` : `
              <div><b class="text-slate-400">Markaziy Fikr:</b> ${{w.stance}}</div>
              <div><b class="text-slate-400">Kuchli Dalillar:</b> ${{w.ideas}}</div>
            `}}
          </div>

          <div>
            <span class="text-[10px] font-bold uppercase text-slate-500 block mb-1">Band 9 Kollokatsiyalar:</span>
            <div class="flex flex-wrap gap-1">
              ${{w.band9_vocab.map(v => `
                <span class="text-[10px] px-2 py-0.5 rounded-md bg-blue-500/10 text-blue-300 border border-blue-500/20 font-medium">
                  ${{v}}
                </span>
              `).join('')}}
            </div>
          </div>

          <div class="pt-2 border-t border-slate-800 text-[11px] text-slate-400 leading-relaxed">
            <b class="text-emerald-400">Tuzilishi:</b> ${{w.isT1 ? w.structure : w.outline}}
          </div>
        </div>
      `).join('');
    }}

    // ==========================================
    // 6. SCORE PREDICTOR LOGIC
    // ==========================================
    let activePredictMode = 'ielts';
    let currentPredictScore = 7.5;

    function rawToBand(raw) {{
      if (raw >= 39) return 9.0;
      if (raw >= 37) return 8.5;
      if (raw >= 35) return 8.0;
      if (raw >= 33) return 7.5;
      if (raw >= 30) return 7.0;
      if (raw >= 27) return 6.5;
      if (raw >= 23) return 6.0;
      if (raw >= 20) return 5.5;
      if (raw >= 16) return 5.0;
      if (raw >= 13) return 4.5;
      return 4.0;
    }}

    function roundBand(val) {{
      const rem = val % 1;
      if (rem < 0.25) return Math.floor(val);
      if (rem < 0.75) return Math.floor(val) + 0.5;
      return Math.ceil(val);
    }}

    function switchPredictMode(mode) {{
      activePredictMode = mode;
      const ieltsBox = document.getElementById('ielts-box');
      const satBox = document.getElementById('sat-box');
      const btnIelts = document.getElementById('btn-ielts');
      const btnSat = document.getElementById('btn-sat');

      if (mode === 'ielts') {{
        ieltsBox.classList.remove('hidden');
        satBox.classList.add('hidden');
        btnIelts.className = 'py-2 rounded-lg bg-blue-600 text-white shadow-md transition';
        btnSat.className = 'py-2 rounded-lg text-slate-400 hover:text-white transition';
        calcIelts();
      }} else {{
        ieltsBox.classList.add('hidden');
        satBox.classList.remove('hidden');
        btnSat.className = 'py-2 rounded-lg bg-amber-600 text-white shadow-md transition';
        btnIelts.className = 'py-2 rounded-lg text-slate-400 hover:text-white transition';
        calcSat();
      }}
    }}

    function calcIelts() {{
      const l = parseInt(document.getElementById('rng-l').value);
      const r = parseInt(document.getElementById('rng-r').value);
      const w = parseFloat(document.getElementById('sel-w').value);
      const s = parseFloat(document.getElementById('sel-s').value);

      const bL = rawToBand(l);
      const bR = rawToBand(r);

      document.getElementById('txt-l').innerText = `${{l}} / 40 (Band ${{bL.toFixed(1)}})`;
      document.getElementById('txt-r').innerText = `${{r}} / 40 (Band ${{bR.toFixed(1)}})`;

      const avg = (bL + bR + w + s) / 4;
      currentPredictScore = roundBand(avg);

      document.getElementById('hero-subtitle').innerText = "Taxminiy IELTS Overall Balingiz";
      document.getElementById('hero-score').innerText = currentPredictScore.toFixed(1);
      document.getElementById('hero-max').innerText = "/ 9.0";

      let cefr = "B2 (Upper-Intermediate)";
      if (currentPredictScore >= 8.5) cefr = "C2 Native Master 🔥";
      else if (currentPredictScore >= 7.0) cefr = "C1 Advanced 🎯";
      else if (currentPredictScore >= 5.5) cefr = "B2 Upper-Intermediate";
      else cefr = "B1 Intermediate";

      document.getElementById('hero-badge').innerText = `✨ ${{cefr}}`;
      updateUnis(currentPredictScore, null);
    }}

    function calcSat() {{
      const m = parseInt(document.getElementById('rng-sat-m').value);
      const rw = parseInt(document.getElementById('rng-sat-rw').value);

      document.getElementById('txt-sat-m').innerText = `${{m}} / 800`;
      document.getElementById('txt-sat-rw').innerText = `${{rw}} / 800`;

      currentPredictScore = m + rw;

      document.getElementById('hero-subtitle').innerText = "Taxminiy Digital SAT Balingiz";
      document.getElementById('hero-score').innerText = currentPredictScore;
      document.getElementById('hero-max').innerText = "/ 1600";

      let pct = "O'rtacha Ball";
      if (currentPredictScore >= 1500) pct = "Top 1% Global Elita 🏆";
      else if (currentPredictScore >= 1400) pct = "Top 5% Nufuzli Grant 💎";
      else if (currentPredictScore >= 1250) pct = "Top 15% Kuchli Natija";
      document.getElementById('hero-badge').innerText = `✨ ${{pct}}`;
      updateUnis(null, currentPredictScore);
    }}

    function updateUnis(ielts, sat) {{
      const container = document.getElementById('uni-container');
      const items = [
        {{
          name: "Westminster International Univ. (WIUT)",
          req: "IELTS 5.5+ / SAT 1100+",
          eligible: (ielts >= 5.5 || sat >= 1100),
          tag: (ielts >= 5.5 || sat >= 1100) ? "Imtihonsiz Qabul ✅" : "Tayyorgarlik Kerak"
        }},
        {{
          name: "Yangi O'zbekiston Universiteti (New Uzbekistan)",
          req: "IELTS 7.0+ / SAT 1200+",
          eligible: (ielts >= 7.0 || sat >= 1200),
          tag: (ielts >= 7.0 || sat >= 1300) ? "100% Grant Imkoniyati 🎁" : "Kontrakt Ehtimoli"
        }},
        {{
          name: "Inha University in Tashkent (IUT)",
          req: "IELTS 5.5+ / SAT Math 650+",
          eligible: (ielts >= 5.5 || sat >= 1150),
          tag: (ielts >= 5.5 || sat >= 1150) ? "Matematika Imtihonisiz ✅" : "Ball Yetarli Emas"
        }},
        {{
          name: "AQSH & Yevropa To'liq Grantlari (Full Ride)",
          req: "IELTS 7.5+ / SAT 1450+",
          eligible: ((ielts && ielts >= 7.5) || (sat && sat >= 1450)),
          tag: ((ielts && ielts >= 7.5) || (sat && sat >= 1450)) ? "Full Scholarship Ehtimoli 🌟" : "1450+ SAT Maqsad"
        }}
      ];

      container.innerHTML = items.map(u => `
        <div class="p-2.5 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-between">
          <div>
            <span class="text-xs font-bold text-white block">${{u.name}}</span>
            <span class="text-[11px] text-slate-400">${{u.req}}</span>
          </div>
          <span class="text-[11px] font-semibold px-2 py-0.5 rounded-lg border ${{u.eligible ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 'bg-slate-800 text-slate-500 border-slate-700'}}">
            ${{u.tag}}
          </span>
        </div>
      `).join('');
    }}

    function shareScore() {{
      const msg = activePredictMode === 'ielts'
        ? `🔥 Mening IELTS taxminiy ballim: Band ${{currentPredictScore.toFixed(1)}}! Siz ham o'z balingizni @ieltssat_dailybot orqali hisoblang:`
        : `🔥 Mening Digital SAT taxminiy ballim: ${{currentPredictScore}} / 1600! Siz ham @ieltssat_dailybot orqali 45+ mock testlarni topshiring:`;
      const shareUrl = `https://t.me/share/url?url=https://t.me/ieltssat_daily&text=${{encodeURIComponent(msg)}}`;
      if (window.Telegram && window.Telegram.WebApp && window.Telegram.WebApp.openTelegramLink) {{
        window.Telegram.WebApp.openTelegramLink(shareUrl);
      }} else {{
        window.open(shareUrl, '_blank');
      }}
    }}

    // ==========================================
    // INITIALIZATION
    // ==========================================
    renderSatMocksGrid();
    renderIeltsMocksGrid();
    renderListeningQuestions();
    renderReadingPassage();
    renderReadingQuestions();
    renderWritingCards();
    calcIelts();
  </script>
</body>
</html>
'''

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated successfully: {OUTPUT_HTML} (Size: {len(html_content)} bytes)")
