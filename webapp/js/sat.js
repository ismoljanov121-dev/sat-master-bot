'use strict';
// Digital SAT: adaptive mock flow, exam tools, and the SAT tab.

const MOCK_SAVE_KEY = 'sat_attempt_v3';
const STAGES = ['rw_m1', 'rw_m2', 'math_m1', 'math_m2'];
const STAGE_INFO = {
  rw_m1: { section: 'Reading & Writing', module: 1, minutes: 32 },
  rw_m2: { section: 'Reading & Writing', module: 2, minutes: 32 },
  math_m1: { section: 'Math', module: 1, minutes: 35 },
  math_m2: { section: 'Math', module: 2, minutes: 35 },
};
const ROUTE_THRESHOLD = 0.55;
const DOMAIN_NAMES = {
  'Craft and Structure': "So'z va matn tuzilishi",
  'Information and Ideas': "Axborot va g'oyalar",
  'Standard English Conventions': 'Grammatika qoidalari',
  'Expression of Ideas': "Fikrni ifodalash",
  Algebra: 'Algebra',
  'Advanced Math': 'Murakkab algebra',
  'Problem-Solving and Data Analysis': "Ma'lumotlar tahlili",
  'Geometry and Trigonometry': 'Geometriya va trigonometriya',
};

let mock = null;

function saveMock() {
  if (!mock || !run) return;
  store(MOCK_SAVE_KEY, {
    id: mock.id, stage: mock.stage, route: mock.route, modules: mock.modules, session: mock.session, deadline: run.deadline,
    idx: run.idx, answers: run.answers, flags: run.flags, elim: run.elim, marks: run.marks, times: run.times, notes: mock.notes,
  });
}

function clearMock() { store(MOCK_SAVE_KEY, undefined); }

const FORMULAS = [
  ['Doira yuzi', '\\(A=\\pi r^{2}\\)'], ['Aylana uzunligi', '\\(C=2\\pi r\\)'], ["To'rtburchak yuzi", '\\(A=\\ell w\\)'],
  ['Uchburchak yuzi', '\\(A=\\frac{1}{2}bh\\)'], ['Pifagor teoremasi', '\\(c^{2}=a^{2}+b^{2}\\)'],
  ['Maxsus uchburchak 30-60-90', '\\(x,\\ x\\sqrt{3},\\ 2x\\)'], ['Maxsus uchburchak 45-45-90', '\\(s,\\ s,\\ s\\sqrt{2}\\)'],
  ['Parallelepiped hajmi', '\\(V=\\ell wh\\)'], ['Silindr hajmi', '\\(V=\\pi r^{2}h\\)'], ['Shar hajmi', '\\(V=\\frac{4}{3}\\pi r^{3}\\)'],
  ['Konus hajmi', '\\(V=\\frac{1}{3}\\pi r^{2}h\\)'], ['Piramida hajmi', '\\(V=\\frac{1}{3}\\ell wh\\)'],
  ['Aylanadagi yoy darajasi', '\\(360^{\\circ}=2\\pi\\) radian'], ['Uchburchak burchaklari', '\\(180^{\\circ}\\)'],
];

function formulaSheet() {
  sheet(`<div class="stack"><div class="h2">Formulalar</div><div>
    ${FORMULAS.map(([name, formula]) => `<div class="formula-row"><span class="small">${esc(name)}</span><span>${rich(formula)}</span></div>`).join('')}
  </div></div>`);
}

// A small expression evaluator, so the calculator never needs eval().
function evaluate(source) {
  const text = source.replace(/×/g, '*').replace(/÷/g, '/').replace(/π/g, 'pi').replace(/√/g, 'sqrt').replace(/\s/g, '');
  let pos = 0;
  const peek = () => text[pos];
  function primary() {
    if (peek() === '(') {
      pos++;
      const value = sum();
      if (peek() === ')') pos++;
      return value;
    }
    if (peek() === '-') { pos++; return -power(); }
    const word = /^[a-z]+/.exec(text.slice(pos));
    if (word) {
      pos += word[0].length;
      if (word[0] === 'pi') return Math.PI;
      const fn = { sqrt: Math.sqrt, sin: x => Math.sin(x * Math.PI / 180), cos: x => Math.cos(x * Math.PI / 180), tan: x => Math.tan(x * Math.PI / 180), ln: Math.log, log: Math.log10 }[word[0]];
      if (!fn) throw new Error('word');
      return fn(primary());
    }
    const number = /^\d*\.?\d+/.exec(text.slice(pos));
    if (!number) throw new Error('number');
    pos += number[0].length;
    return Number(number[0]);
  }
  function power() {
    const base = primary();
    if (peek() === '^') { pos++; return base ** power(); }
    return base;
  }
  function product() {
    let value = power();
    while (peek() === '*' || peek() === '/' || peek() === '(' || /[a-z]/.test(peek() || '')) {
      if (peek() === '*') { pos++; value *= power(); }
      else if (peek() === '/') { pos++; value /= power(); }
      else value *= power();
    }
    return value;
  }
  function sum() {
    let value = product();
    while (peek() === '+' || peek() === '-') {
      if (text[pos++] === '+') value += product();
      else value -= product();
    }
    return value;
  }
  const result = sum();
  if (pos < text.length || !Number.isFinite(result)) throw new Error('syntax');
  return Math.round(result * 1e8) / 1e8;
}

let calcInput = '';
const CALC_KEYS = [
  ['sin(', 'cos(', 'tan(', '√(', 'C'], ['(', ')', '^', 'π', '⌫'],
  ['7', '8', '9', '÷', 'ln('], ['4', '5', '6', '×', 'log('], ['1', '2', '3', '-', '='], ['0', '.', ',', '+', 'ans'],
].map(row => row.filter(key => key !== ','));

function calculatorSheet() {
  const key = App.boot && App.boot.desmos_key;
  if (key) { desmosSheet(key); return; }
  const keys = CALC_KEYS.flat().map(k => {
    const kind = k === '=' ? 'eq' : (/[a-z√π^()⌫C]/.test(k) ? 'fn' : '');
    return `<button class="${kind}" data-act="calcKey" data-key="${esc(k)}">${esc(k)}</button>`;
  }).join('');
  sheet(`<div class="stack">
    <div class="between"><span class="h2">Kalkulyator</span><button class="btn soft sm" data-act="openDesmos">Desmos</button></div>
    <div class="calc-screen"><span id="calc-in" class="small muted">${esc(calcInput) || '&nbsp;'}</span><span id="calc-out" class="out">0</span></div>
    <div class="calc-keys">${keys}</div></div>`);
}

function desmosSheet(key) {
  sheet(`<div class="stack"><span class="h2">Grafik kalkulyator</span><div id="desmos" class="desmos-box"></div></div>`);
  const mountCalculator = () => { window.Desmos.GraphingCalculator(document.getElementById('desmos'), { keypad: true, expressions: true }); };
  if (window.Desmos) { mountCalculator(); return; }
  const script = document.createElement('script');
  script.src = `https://www.desmos.com/api/v1.10/calculator.js?apiKey=${encodeURIComponent(key)}`;
  script.onload = mountCalculator;
  document.head.appendChild(script);
}

function mathTools() {
  return [
    { id: 'calc', icon: 'calc', label: 'Kalkulyator', open: calculatorSheet },
    { id: 'formula', icon: 'sigma', label: 'Formulalar', open: formulaSheet },
  ];
}

function noteSheet() {
  const id = currentQuestion().id;
  const marks = (run.marks[id] || []).length;
  sheet(`<div class="stack"><span class="h2">Izoh</span>
    <textarea id="note-text" class="input" rows="4" placeholder="Bu savol uchun qaydingiz">${esc((mock?.notes || {})[id] || '')}</textarea>
    <p class="small muted">Matndan so'zni ajrating va chiqqan tugmani bosing: u sariq rangda belgilanadi.</p>
    ${marks ? `<button class="btn" data-act="clearMarks">Belgilashlarni o'chirish</button>` : ''}
    <button class="btn primary" data-act="saveNote">Saqlash</button></div>`);
}

function readingTools() {
  return [{ id: 'note', icon: 'note', label: 'Izoh', open: noteSheet }];
}

function enterStage(stage, saved) {
  mock.stage = stage;
  const info = STAGE_INFO[stage];
  const ids = mock.modules[stage];
  const last = stage === 'math_m2';
  const state = saved || { answers: mock.answers, flags: mock.flags, elim: mock.elim, marks: mock.marks, times: mock.times };
  return startRun({
    mode: 'exam',
    title: `${info.section} · Modul ${info.module}`,
    ids,
    idx: saved?.idx || 0,
    answers: state.answers, flags: state.flags, elim: state.elim, marks: state.marks, times: state.times,
    deadline: saved?.deadline || Date.now() + info.minutes * 60000,
    tools: stage.startsWith('math') ? mathTools() : readingTools(),
    finishLabel: last ? 'Imtihonni yakunlash' : 'Modulni yakunlash',
    exitMessage: "Chiqsangiz, javoblar saqlanadi va keyinroq davom ettirasiz. Vaqt to'xtamaydi.",
    onChange: saveMock,
    onFinish: confirmFinishStage,
    onTimeUp: finishStage,
  }, { replace: current()?.name === 'satBreak' });
}

function confirmFinishStage() {
  const empty = run.ids.filter(id => !run.answers[id]).length;
  const message = empty
    ? `${empty} ta savol bo'sh qoldi. Yakunlangach, bu modulga qaytib bo'lmaydi. Davom etasizmi?`
    : "Modulni yakunlaysizmi? Yakunlangach, bu modulga qaytib bo'lmaydi.";
  askConfirm(message, finishStage);
}

function routeFor(section) {
  const ids = mock.modules[`${section}_m1`];
  const correct = ids.filter(id => isCorrect(App.bank[id], run.answers[id])).length;
  return correct / ids.length >= ROUTE_THRESHOLD ? 'hard' : 'easy';
}

function finishStage() {
  recordTime();
  stopTimer();
  Object.assign(mock, { answers: run.answers, flags: run.flags, elim: run.elim, marks: run.marks, times: run.times });
  const index = STAGES.indexOf(mock.stage);
  if (mock.stage.endsWith('m1')) {
    const section = mock.stage.split('_')[0];
    mock.route[section] = routeFor(section);
    mock.modules[`${section}_m2`] = mock.data[section][`m2_${mock.route[section]}`];
  }
  if (index === STAGES.length - 1) {
    finishMock();
    return;
  }
  mock.stage = STAGES[index + 1];
  mock.nextStage = STAGES[index + 1];
  run.deadline = 0;
  saveMock();
  open('satBreak', {}, { replace: true });
}

views.satBreak = {
  full: true,
  render() {
    const info = STAGE_INFO[mock.nextStage];
    const count = mock.modules[mock.nextStage].length;
    const newSection = mock.nextStage === 'math_m1';
    return `<div class="page flush"><div class="break">
      <span class="tile good">${icon('check')}</span>
      <div class="h1">${newSection ? "Reading & Writing yakunlandi" : 'Modul yakunlandi'}</div>
      <p class="muted">${newSection ? "Xohlasangiz, bir oz dam oling. Vaqt keyingi tugmani bosganingizda boshlanadi." : "Vaqt keyingi tugmani bosganingizda boshlanadi."}</p>
      <div class="card" style="width:100%"><div class="h3">${esc(info.section)}, Modul ${info.module}</div><div class="label num">${count} savol · ${info.minutes} daqiqa</div></div>
      <button class="btn primary block lg" data-act="nextStage">Boshlash</button>
      <button class="btn block" data-act="back">Keyinroq davom ettirish</button>
    </div></div>`;
  },
  onBack() {
    askConfirm("Imtihondan chiqasizmi? Javoblar saqlanadi, keyinroq shu joydan davom ettirasiz.", () => {
      setExamGuard(false);
      leaveView();
    });
  },
};

function mockPayload() {
  const items = [];
  STAGES.forEach(stage => mock.modules[stage].forEach(id => {
    const answer = mock.answers[id];
    if (answer || mock.times[id]) items.push({ q: id, a: answer || '', t: mock.times[id] || 0 });
  }));
  return { kind: 'sat_mock', ref: mock.id, route: mock.route, session: mock.session || undefined, items };
}

function localMockReport() {
  const sections = {};
  [['rw', 'rw'], ['math', 'm']].forEach(([key, sec]) => {
    const ids = STAGES.filter(s => s.startsWith(key)).flatMap(s => mock.modules[s]);
    const rows = ids.map(id => [App.bank[id].dif, App.bank[id].type, isCorrect(App.bank[id], mock.answers[id])]);
    sections[key] = { ...localSectionScore(rows), correct: rows.filter(r => r[2]).length, total: rows.length, route: mock.route[key] };
  });
  return { kind: 'sat_mock', title: mock.title, score: sections.rw.score + sections.math.score, sections, domains: [], offline: true };
}

async function finishMock() {
  setExamGuard(false);
  document.getElementById('app').innerHTML = loadingCards(2);
  const result = await submitAttempt(mockPayload());
  clearMock();
  const ids = STAGES.flatMap(stage => mock.modules[stage]);
  const review = { ids, answers: { ...mock.answers } };
  if (result) {
    App.boot && Object.assign(App.boot, { me: result.me, due: result.due });
    refreshBoot();
    open('report', { id: result.id, report: result.report, review }, { replace: true });
  } else {
    open('report', { report: localMockReport(), review }, { replace: true });
  }
  haptic('good');
  mock = null;
}

async function loadMock(mockId, session) {
  const mocks = await loadData('sat_mocks.json');
  await satBank();
  const data = mocks.find(item => item.id === mockId);
  if (!data) throw new Error(mockId);
  return {
    id: data.id, title: data.title, data, stage: 'rw_m1', session: session || null, route: { rw: null, math: null },
    modules: { rw_m1: data.rw.m1, rw_m2: [], math_m1: data.math.m1, math_m2: [] },
    answers: {}, flags: {}, elim: {}, marks: {}, times: {}, notes: {},
  };
}

async function startMock(mockId, session) {
  document.getElementById('app').innerHTML = loadingCards(2);
  try {
    mock = await loadMock(mockId, session);
  } catch (e) {
    toast("Testni yuklab bo'lmadi. Internetni tekshiring.");
    draw();
    return;
  }
  setExamGuard(true);
  track('mock_started', mockId);
  enterStage('rw_m1');
}

async function resumeMock(saved) {
  mock = await loadMock(saved.id, saved.session);
  Object.assign(mock, { route: saved.route, modules: saved.modules, notes: saved.notes || {},
    answers: saved.answers, flags: saved.flags, elim: saved.elim, marks: saved.marks, times: saved.times });
  setExamGuard(true);
  if (!saved.deadline) {
    mock.nextStage = saved.stage;
    mock.stage = saved.stage;
    open('satBreak', {});
    return;
  }
  await enterStage(saved.stage, saved);
  if (Date.now() >= saved.deadline) {
    toast('Modul vaqti tugagan edi.');
    finishStage();
  }
}

Object.assign(actions, {
  nextStage() { enterStage(mock.nextStage); },
  startMock(el) {
    const saved = recall(MOCK_SAVE_KEY);
    const begin = () => { clearMock(); startMock(el.dataset.id, App.session?.ref === el.dataset.id ? App.session.code : null); };
    if (saved) askConfirm("Tugallanmagan imtihon bor. Yangisini boshlasangiz, u o'chadi. Davom etasizmi?", begin);
    else begin();
  },
  resumeMock() { resumeMock(recall(MOCK_SAVE_KEY)); },
  calcKey(el) {
    const key = el.dataset.key;
    const out = document.getElementById('calc-out');
    if (key === 'C') { calcInput = ''; out.textContent = '0'; }
    else if (key === '⌫') calcInput = calcInput.slice(0, -1);
    else if (key === '=') {
      try { const value = evaluate(calcInput); out.textContent = value; App.calcLast = value; }
      catch (e) { out.textContent = 'Xato'; }
    } else calcInput += key === 'ans' ? (App.calcLast ?? '') : key;
    document.getElementById('calc-in').textContent = calcInput || ' ';
  },
  openDesmos() { externalLink('https://www.desmos.com/calculator'); },
  saveNote() {
    mock.notes[currentQuestion().id] = document.getElementById('note-text').value;
    saveMock();
    closeSheet();
  },
  clearMarks() {
    delete run.marks[currentQuestion().id];
    saveMock();
    closeSheet();
    drawQuestion();
  },
  satTab(el) { App.satTab = el.dataset.tab2; draw(); },
});

function resumeCard() {
  const saved = recall(MOCK_SAVE_KEY);
  if (!saved) return '';
  const answered = Object.keys(saved.answers || {}).length;
  return `<button class="card row" data-act="resumeMock" style="text-align:left;width:100%">
    <span class="tile warn">${icon('clock')}</span>
    <span class="grow"><span class="h3">Tugallanmagan imtihon</span><br><span class="label">${answered} ta javob saqlangan. Davom ettirish</span></span>
    <span class="chev">${icon('right', true)}</span></button>`;
}

async function satMocksTab() {
  const mocks = await loadData('sat_mocks.json');
  let scores = {};
  if (hasTelegramUser) {
    const list = await api('attempts').catch(() => ({ attempts: [] }));
    list.attempts.filter(a => a.kind === 'sat_mock').reverse().forEach(a => { scores[a.ref] = a.score; });
  }
  const rows = mocks.map(item => `<button class="list-row" data-act="startMock" data-id="${esc(item.id)}">
      <span class="tile">${item.num}</span>
      <span class="grow"><span class="h3">${esc(item.title)}</span><br><span class="label">98 savol · 2 soat 14 daqiqa</span></span>
      ${scores[item.id] ? `<span class="chip good num">${Math.round(scores[item.id])}</span>` : ''}
      <span class="chev">${icon('right', true)}</span></button>`).join('');
  return `${resumeCard()}
    <div class="card tight small muted">Har bir mock ikki bo'limdan iborat: Reading & Writing va Math. Ikkinchi modulning qiyinligi birinchi moduldagi natijangizga qarab tanlanadi.</div>
    <div class="list">${rows}</div>`;
}

views.sat = {
  tab: 'sat',
  async render() {
    const tab = App.satTab || 'mock';
    const body = tab === 'mock' ? await satMocksTab() : tab === 'practice' ? await practiceTab() : await notebookTab();
    const button = (key, label) => `<button class="${tab === key ? 'on' : ''}" data-act="satTab" data-tab2="${key}">${label}</button>`;
    return `<div class="page stack">
      <div class="h1">Digital SAT</div>
      <div class="segmented">${button('mock', 'Mock')}${button('practice', 'Mashq')}${button('notebook', 'Xatolar')}</div>
      ${body}</div>`;
  },
};
