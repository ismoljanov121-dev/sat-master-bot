'use strict';
// Short practice sets, the mistake notebook and the diagnostic.

async function loadNotes() {
  if (!App.notes) App.notes = await loadData('sat_notes.json');
  return App.notes;
}

function randomIds(filter, count) {
  const pool = Object.values(App.bank).filter(filter);
  for (let i = pool.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [pool[i], pool[j]] = [pool[j], pool[i]];
  }
  return pool.slice(0, count).map(q => q.id);
}

function practiceItems() {
  return run.ids.filter(id => run.answers[id]).map(id => ({ q: id, a: run.answers[id], t: run.times[id] || 0 }));
}

async function finishPractice(mode, label) {
  const items = practiceItems();
  const correct = run.ids.filter(id => isCorrect(App.bank[id], run.answers[id])).length;
  const ids = [...run.ids];
  const answers = { ...run.answers };
  setExamGuard(false);
  if (!items.length) { leaveView(); return; }
  document.getElementById('app').innerHTML = loadingCards(2);
  const result = await submitAttempt({ kind: 'practice', mode, ref: label || '', items });
  if (result) {
    await refreshBoot();
    open('report', { id: result.id, report: result.report, review: { ids, answers } }, { replace: true });
  } else {
    open('report', { report: { kind: 'practice', title: 'Mashq', correct, total: ids.length, domains: [], offline: true }, review: { ids, answers } }, { replace: true });
  }
}

async function startSet(mode, ids, title, label) {
  if (!ids.length) { toast("Hozircha mos savol topilmadi."); return; }
  document.getElementById('app').innerHTML = loadingCards(2);
  await Promise.all([satBank(), loadNotes()]);
  const diagnostic = mode === 'diagnostic';
  startRun({
    mode: diagnostic ? 'exam' : 'practice',
    title, subtitle: diagnostic ? 'Diagnostika' : 'Mashq',
    ids,
    tools: mathToolsFor(ids),
    finishLabel: 'Yakunlash',
    exitMessage: "Mashqdan chiqasizmi? Ishlangan savollar saqlanadi.",
    onFinish: () => finishPractice(mode, label),
    onExit: () => { if (practiceItems().length) submitAttempt({ kind: 'practice', mode, ref: label || '', items: practiceItems() }); },
  });
}

function mathToolsFor(ids) {
  return ids.some(id => App.bank[id].sec === 'm') ? mathTools() : [];
}

async function startPractice({ section, domain, difficulty }) {
  await satBank();
  let ids;
  if (hasTelegramUser) {
    const query = new URLSearchParams({ count: '10' });
    if (section) query.set('section', section);
    if (domain) query.set('domain', domain);
    if (difficulty) query.set('difficulty', difficulty);
    ids = (await api(`practice?${query}`).catch(() => ({ ids: [] }))).ids;
  }
  if (!ids || !ids.length) {
    ids = randomIds(q => (!section || q.sec === section) && (!domain || q.dom === domain) && (!difficulty || q.dif === difficulty), 10);
  }
  startSet('domain', ids, DOMAIN_NAMES[domain] || 'Aralash mashq', domain);
}

async function startReview() {
  const notebook = await api('notebook').catch(() => null);
  if (!notebook || !notebook.due.length) { toast("Bugun takrorlanadigan savol yo'q."); return; }
  startSet('review', notebook.due.slice(0, 10), 'Xatolarni takrorlash', '');
}

async function startDiagnostic() {
  await satBank();
  let ids = hasTelegramUser ? (await api('diagnostic').catch(() => ({ ids: [] }))).ids : [];
  if (!ids.length) ids = randomIds(q => q.dif === 'Medium', 16);
  track('diagnostic_started');
  startSet('diagnostic', ids, 'SAT diagnostika', '');
}

function runTask(action) {
  if (action.type === 'diagnostic') startDiagnostic();
  else if (action.type === 'review') startReview();
  else if (action.type === 'practice') startPractice(action);
  else if (action.type === 'mock') { App.satTab = 'mock'; open('sat', {}, { reset: true }); }
  else if (action.type === 'reading') { App.ieltsTab = 'reading'; open('ielts', {}, { reset: true }); }
  else if (action.type === 'listening') { App.ieltsTab = 'listening'; open('ielts', {}, { reset: true }); }
  else if (action.type === 'writing') { App.ieltsTab = 'writing'; open('ielts', {}, { reset: true }); }
}

function accuracyTone(percent) {
  if (percent >= 75) return 'good';
  return percent >= 50 ? 'warn' : 'bad';
}

function domainRow(item, attributes = '') {
  const percent = item.total ? Math.round(item.correct / item.total * 100) : null;
  return `<button class="list-row" ${attributes}>
    <span class="grow stack sm">
      <span class="between"><span class="h3">${esc(DOMAIN_NAMES[item.domain] || item.domain)}</span>
        <span class="small muted num">${percent == null ? "Ma'lumot yo'q" : `${percent}%`}</span></span>
      <span class="bar ${percent == null ? '' : accuracyTone(percent)}"><i style="width:${percent || 0}%"></i></span>
    </span><span class="chev">${icon('right', true)}</span></button>`;
}

async function practiceTab() {
  const mastery = (App.boot && App.boot.mastery) || Object.entries({
    rw: ['Craft and Structure', 'Information and Ideas', 'Standard English Conventions', 'Expression of Ideas'],
    m: ['Algebra', 'Advanced Math', 'Problem-Solving and Data Analysis', 'Geometry and Trigonometry'],
  }).flatMap(([section, list]) => list.map(domain => ({ section, domain, correct: 0, total: 0 })));
  const group = section => mastery.filter(d => d.section === section).map(d => (
    domainRow(d, `data-act="pickPractice" data-section="${d.section}" data-domain="${esc(d.domain)}"`)
  )).join('');
  return `<button class="card row" data-act="quickPractice" style="text-align:left;width:100%">
      <span class="tile">${icon('spark')}</span>
      <span class="grow"><span class="h3">Tezkor mashq</span><br><span class="label">Aralash 10 savol, taxminan 12 daqiqa</span></span>
      <span class="chev">${icon('right', true)}</span></button>
    <div class="section-title">Reading & Writing</div><div class="list">${group('rw')}</div>
    <div class="section-title">Math</div><div class="list">${group('m')}</div>`;
}

async function notebookTab() {
  if (!hasTelegramUser) return `<div class="card empty">Xatolar daftari Telegram ichida ishlaydi.</div>`;
  const [data] = await Promise.all([api('notebook').catch(() => null), satBank()]);
  if (!data) return `<div class="card empty">Ma'lumotni yuklab bo'lmadi.</div>`;
  const upcoming = data.items.length - data.due.length;
  const rows = data.items.slice(0, 30).map(item => {
    const question = App.bank[item.q];
    const when = data.due.includes(item.q) ? '<span class="chip warn">Bugun</span>' : `<span class="chip">${esc(item.due.slice(5))}</span>`;
    return `<div class="list-row"><span class="grow"><span class="h3">${esc(DOMAIN_NAMES[question.dom] || question.dom)}</span><br>
      <span class="label">${esc(question.dif)} · ${item.wrong} marta xato</span></span>${when}</div>`;
  }).join('');
  return `<div class="grid3">
      <div class="card tight stat"><div class="v">${data.due.length}</div><div class="label">Bugun</div></div>
      <div class="card tight stat"><div class="v">${upcoming}</div><div class="label">Keyinroq</div></div>
      <div class="card tight stat"><div class="v">${data.resolved}</div><div class="label">O'zlashtirildi</div></div>
    </div>
    <button class="btn primary block lg" data-act="startReview" ${data.due.length ? '' : 'disabled'}>${icon('repeat', true)}Takrorlashni boshlash</button>
    <p class="small muted" style="padding:0 4px">Xato savol 1 kundan keyin qaytadi. To'g'ri ishlasangiz, 3 va 7 kundan keyin yana so'raladi, shundan so'ng o'zlashtirilgan hisoblanadi.</p>
    ${rows ? `<div class="list">${rows}</div>` : `<div class="card empty">Hozircha xatolar yo'q. Mashq yoki mock ishlang.</div>`}`;
}

Object.assign(actions, {
  quickPractice() { startPractice({}); },
  startReview() { startReview(); },
  startDiagnostic() { startDiagnostic(); },
  pickPractice(el) {
    const { section, domain } = el.dataset;
    const levels = [['', 'Aralash'], ['Easy', 'Oson'], ['Medium', "O'rta"], ['Hard', 'Qiyin']];
    sheet(`<div class="stack"><div class="h2">${esc(DOMAIN_NAMES[domain] || domain)}</div>
      <p class="muted small">Qiyinlikni tanlang. Har mashqda 10 ta savol va darhol izoh bo'ladi.</p>
      <div class="list">${levels.map(([value, label]) => `<button class="list-row" data-act="beginPractice" data-section="${section}" data-domain="${esc(domain)}" data-difficulty="${value}">
        <span class="grow h3">${label}</span><span class="chev">${icon('right', true)}</span></button>`).join('')}</div></div>`);
  },
  beginPractice(el) {
    closeSheet();
    startPractice(el.dataset);
  },
});
