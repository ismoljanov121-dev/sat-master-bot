'use strict';
// IELTS Writing: prompts, the essay editor and AI feedback.

const TARGET_WORDS = { 1: 150, 2: 250 };
const WRITING_MINUTES = { 1: 20, 2: 40 };
const CRITERIA_NAMES = {
  task: 'Topshiriq bajarilishi', coherence: "Izchillik va bog'liqlik", lexical: "Lug'at boyligi", grammar: 'Grammatika',
};
const WRITING_ERRORS = {
  too_short: "Insho juda qisqa. Tekshirish uchun kamida 40 so'z yozing.",
  too_long: "Insho juda uzun. 700 so'zgacha yozing.",
  limit_reached: "Bugungi bepul tekshiruvlar tugadi. Ertaga yana urinib ko'ring yoki do'stingizni taklif qiling.",
  ai_busy: "AI hozir band. Bir ozdan keyin qayta urinib ko'ring. Tekshiruvingiz sarflanmadi.",
  ai_failed: "Tekshirib bo'lmadi. Qayta urinib ko'ring. Tekshiruvingiz sarflanmadi.",
  ai_disabled: 'AI tekshiruvi hozircha yoqilmagan.',
  network: "Internet bilan aloqa yo'q.",
};

let writer = null;

function wordCount(text) { return (text.match(/[A-Za-z0-9'’-]+/g) || []).length; }

async function writingTab() {
  const task = App.writingTask || 2;
  const data = await loadData('ielts_writing.json');
  const list = task === 1 ? data.task1 : data.task2;
  const ai = App.boot?.ai;
  const history = hasTelegramUser ? await api('writing').catch(() => null) : null;
  const button = (value, label) => `<button class="${task === value ? 'on' : ''}" data-act="writingTask" data-task="${value}">${label}</button>`;
  const past = history?.items?.length
    ? `<div class="section-title">Oldingi tekshiruvlar</div><div class="list">${history.items.slice(0, 5).map(item => `
        <button class="list-row" data-act="openSubmission" data-id="${item.id}">
          <span class="tile good"><span class="h3 num">${Number(item.band).toFixed(1)}</span></span>
          <span class="grow"><span class="h3">Task ${item.task}</span><br><span class="label num">${item.word_count} so'z</span></span>
          <span class="chev">${icon('right', true)}</span></button>`).join('')}</div>` : '';
  return `<div class="card row"><span class="tile">${icon('spark')}</span>
      <span class="grow"><span class="h3">AI tekshiruvi</span><br>
      <span class="label">${ai ? `Bugun ${history?.remaining ?? ai.remaining} ta tekshiruv qoldi` : 'Telegram ichida ishlaydi'}</span></span></div>
    <div class="segmented">${button(1, 'Task 1')}${button(2, 'Task 2')}</div>
    ${past}
    <div class="section-title">Mavzular</div>
    <div class="list">${list.map(item => `<button class="list-row" data-act="openWriting" data-id="${item.id}">
      <span class="grow"><span class="h3">${esc(item.title)}</span><br><span class="label">${esc(item.type)}</span></span>
      <span class="chev">${icon('right', true)}</span></button>`).join('')}</div>`;
}

function draftKey(id) { return `essay_${id}`; }

function counterHTML(words, target) {
  const tone = words >= target ? 'good' : words >= target * 0.7 ? 'warn' : '';
  return `<span class="chip ${tone} num">${words} / ${target} so'z</span>`;
}

views.writing = {
  full: true,
  async render({ id }) {
    const data = await loadData('ielts_writing.json');
    const prompt = [...data.task1, ...data.task2].find(item => item.id === id);
    const task = id.startsWith('w1') ? 1 : 2;
    const text = recall(draftKey(id)) || '';
    writer = { id, task, prompt, startedAt: null };
    const remaining = App.boot?.ai?.remaining;
    return `<div class="exam"><div class="exam-top"><div class="exam-top-in">
        <button class="icon-btn" data-act="back" aria-label="Orqaga">${icon('left')}</button>
        <div class="exam-title"><span class="eyebrow">IELTS Writing Task ${task}</span><span id="w-timer"><span class="timer off">${WRITING_MINUTES[task]} daqiqa tavsiya etiladi</span></span></div>
        ${examFullscreenButton()}
        <button class="icon-btn" data-act="writingTimer" aria-label="Taymer">${icon('clock')}</button></div></div>
      <div class="exam-main"><div class="exam-grid">
        <div class="card stack sm"><span class="eyebrow">${esc(prompt.type)}</span><div class="pre">${esc(prompt.prompt)}</div>
          <button class="btn sm" data-act="writingGuide" style="align-self:flex-start">Reja va iboralar</button></div>
        <textarea id="essay" class="input" rows="14" spellcheck="false" placeholder="Inshoingizni shu yerga yozing">${esc(text)}</textarea>
      </div></div>
      <div class="exam-bottom"><div class="exam-bottom-in">
        <span id="w-count">${counterHTML(wordCount(text), TARGET_WORDS[task])}</span>
        <button id="w-submit" class="btn primary" data-act="submitEssay">${icon('spark', true)}Tekshirish${remaining != null ? ` (${remaining})` : ''}</button>
      </div></div></div>`;
  },
  mount() {
    const box = document.getElementById('essay');
    box.addEventListener('input', () => {
      store(draftKey(writer.id), box.value);
      document.getElementById('w-count').innerHTML = counterHTML(wordCount(box.value), TARGET_WORDS[writer.task]);
    });
  },
  leave() { clearInterval(writer?.timer); },
};

function feedbackView(data) {
  const criteria = Object.entries(data.criteria).map(([name, part]) => `<div class="domain">
      <div class="between"><span class="h3">${esc(CRITERIA_NAMES[name])}</span><span class="h3 num">${Number(part.band).toFixed(1)}</span></div>
      <div class="bar"><i style="width:${part.band / 9 * 100}%"></i></div>
      <div class="small muted">${esc(part.comment)}</div></div>`).join('');
  const mistakes = (data.mistakes || []).map(item => `<div class="mistake">
      <div><s>${esc(item.quote)}</s></div><div><b>${esc(item.fix)}</b></div><div class="small muted">${esc(item.why)}</div></div>`).join('');
  const short = data.words < data.target
    ? `<div class="card tight small"><b>Hajm yetarli emas:</b> ${data.words} so'z yozilgan, kamida ${data.target} so'z kerak.</div>` : '';
  return `<div class="page flush stack">
    <div class="card score-hero"><div class="eyebrow">Taxminiy band</div><div class="big">${Number(data.band).toFixed(1)}</div>
      <p class="small muted" style="margin-top:6px">AI bahosi rasmiy natija emas, mashq uchun yo'l-yo'riq.</p></div>
    ${short}
    <div class="card"><div class="pre">${esc(data.summary)}</div></div>
    <div class="section-title">Mezonlar</div><div class="card">${criteria}</div>
    ${data.strengths?.length ? `<div class="section-title">Yaxshi tomonlar</div><div class="card stack sm">${data.strengths.map(item => `<div class="row small">${icon('check', true)}<span>${esc(item)}</span></div>`).join('')}</div>` : ''}
    ${mistakes ? `<div class="section-title">Asosiy xatolar</div><div class="card">${mistakes}</div>` : ''}
    ${data.improved_paragraph ? `<div class="section-title">Yaxshilangan abzas</div><div class="passage">${esc(data.improved_paragraph)}</div>` : ''}
    ${data.next_steps?.length ? `<div class="section-title">Keyingi qadamlar</div><div class="card stack sm">${data.next_steps.map(item => `<div class="small">${esc(item)}</div>`).join('')}</div>` : ''}
    <button class="btn block" data-act="back">Yopish</button></div>`;
}

views.writingResult = {
  full: true,
  render({ data }) { return feedbackView(data); },
};

Object.assign(actions, {
  writingTask(el) { App.writingTask = Number(el.dataset.task); draw(); },
  openWriting(el) { open('writing', { id: el.dataset.id }); },
  async openSubmission(el) {
    const data = await api(`writing/${el.dataset.id}`).catch(() => null);
    if (data) open('writingResult', { data });
  },
  writingGuide() {
    sheet(`<div class="stack"><div class="h2">Reja va foydali iboralar</div><div class="pre small">${esc(writer.prompt.guide)}</div></div>`);
  },
  writingTimer() {
    if (writer.timer) return;
    const deadline = Date.now() + WRITING_MINUTES[writer.task] * 60000;
    const box = document.getElementById('w-timer');
    const draw = () => {
      const left = Math.max(0, Math.ceil((deadline - Date.now()) / 1000));
      box.innerHTML = `<span class="timer ${left <= 120 ? 'low' : ''}">${String(Math.floor(left / 60)).padStart(2, '0')}:${String(left % 60).padStart(2, '0')}</span>`;
      if (!left) { clearInterval(writer.timer); toast('Vaqt tugadi.'); }
    };
    draw();
    writer.startedAt = Date.now();
    writer.timer = setInterval(draw, 1000);
    toast('Taymer boshlandi.');
  },
  async submitEssay() {
    if (!hasTelegramUser) { toast('AI tekshiruvi Telegram ichida ishlaydi.'); return; }
    const text = document.getElementById('essay').value;
    const button = document.getElementById('w-submit');
    button.disabled = true;
    button.innerHTML = `<span class="spinner"></span>AI o'qimoqda`;
    const minutes = writer.startedAt ? Math.round((Date.now() - writer.startedAt) / 60000) : 0;
    try {
      const data = await api('writing', { method: 'POST', body: { prompt_id: writer.id, text, minutes } });
      store(draftKey(writer.id), undefined);
      haptic('good');
      refreshBoot();
      open('writingResult', { data }, { replace: true });
    } catch (e) {
      haptic('bad');
      toast(WRITING_ERRORS[e.code] || "Xatolik yuz berdi. Qayta urinib ko'ring.");
      button.disabled = false;
      button.innerHTML = `${icon('spark', true)}Tekshirish`;
    }
  },
});
