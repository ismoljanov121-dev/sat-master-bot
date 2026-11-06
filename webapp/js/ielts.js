'use strict';
// IELTS Listening and Reading test screens, and the IELTS tab.

const BANDS = {
  listening: [[39, 9], [37, 8.5], [35, 8], [32, 7.5], [30, 7], [26, 6.5], [23, 6], [18, 5.5], [16, 5], [13, 4.5], [10, 4], [8, 3.5], [6, 3], [4, 2.5], [3, 2], [2, 1.5], [1, 1]],
  reading: [[39, 9], [37, 8.5], [35, 8], [33, 7.5], [30, 7], [27, 6.5], [23, 6], [19, 5.5], [15, 5], [13, 4.5], [10, 4], [8, 3.5], [6, 3], [4, 2.5], [3, 2], [2, 1.5], [1, 1]],
};
const READING_MINUTES = 60;
const LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

let it = null;

function normalizeAnswer(value) {
  return String(value == null ? '' : value).trim().toLowerCase()
    .replace(/(\d),(?=\d{3}\b)/g, '$1')
    .replace(/(\d)(st|nd|rd|th)\b/g, '$1')
    .replace(/^(a|an|the)\s+/, '')
    .replace(/[.\s]+$/, '')
    .replace(/\s+/g, ' ');
}

function ieltsCorrect(question, value) {
  const given = normalizeAnswer(value);
  return !!given && [question.ans, ...(question.alts || [])].some(answer => normalizeAnswer(answer) === given);
}

function bandFor(correct, kind) {
  const row = BANDS[kind].find(([minimum]) => correct >= minimum);
  return row ? row[1] : 0;
}

function partOf(question) { return it.kind === 'reading' ? question.passage_num : question.sec; }
function partQuestions() { return it.test.questions.filter(q => partOf(q) === it.part); }

function answerControl(question) {
  const value = it.answers[question.num] || '';
  const locked = it.graded ? 'disabled' : '';
  if (question.type === 'tfng' || question.type === 'ynng') {
    const choices = question.type === 'tfng' ? ['TRUE', 'FALSE', 'NOT GIVEN'] : ['YES', 'NO', 'NOT GIVEN'];
    return `<div class="iq-opts">${choices.map(choice => (
      `<button class="${value === choice ? 'on' : ''}" data-act="iqSet" data-num="${question.num}" data-value="${choice}" ${locked}>${choice}</button>`
    )).join('')}</div>`;
  }
  if (question.type === 'mcq') {
    return `<div class="iq-opts col">${question.options.map(option => {
      const key = option[0];
      return `<button class="${value === key ? 'on' : ''}" data-act="iqSet" data-num="${question.num}" data-value="${key}" ${locked}>${esc(option)}</button>`;
    }).join('')}</div>`;
  }
  if (question.type === 'heading' || question.type === 'match') {
    const items = question.choices || it.test.headings?.[it.part] || [];
    return `<select class="input" data-num="${question.num}" ${locked}>
      <option value="">Tanlang</option>
      ${items.map(item => {
        const key = item.split('.')[0].trim();
        return `<option value="${esc(key)}" ${value === key ? 'selected' : ''}>${esc(item)}</option>`;
      }).join('')}</select>`;
  }
  return `<input class="input" data-num="${question.num}" value="${esc(value)}" placeholder="Javob" autocomplete="off" autocapitalize="off" ${locked}>`;
}

function questionCard(question) {
  let state = '', result = '';
  if (it.graded && !it.sealed) {
    const right = ieltsCorrect(question, it.answers[question.num]);
    state = right ? 'right' : 'wrong';
    result = `<div class="small ${right ? '' : ''}"><b>${right ? "To'g'ri" : `To'g'ri javob: ${esc(question.ans)}`}</b>${question.expl ? `. ${esc(question.expl)}` : ''}</div>`;
  }
  return `<div class="iq ${state}"><span class="n num">${question.num}-savol</span>
    <div>${esc(question.text)}</div>${answerControl(question)}${result}</div>`;
}

function headingsList() {
  const items = it.test.headings?.[it.part];
  if (!items) return '';
  return `<div class="card tight small"><div class="h3" style="margin-bottom:6px">Sarlavhalar ro'yxati</div>${items.map(esc).join('<br>')}</div>`;
}

function resultCard() {
  if (!it.graded) return '';
  if (it.band == null) {
    return `<div class="card score-hero"><div class="h2">Javoblaringiz saqlandi</div>
      <p class="small muted" style="margin-top:6px">Natija serverda hisoblanadi va Natijalar bo'limida chiqadi.</p></div>`;
  }
  return `<div class="card score-hero">
    <div class="eyebrow">Taxminiy band</div><div class="big">${it.band.toFixed(1)}</div>
    <div class="muted num">${it.correct} / ${it.test.questions.length} to'g'ri</div>
    ${it.savedId ? `<button class="btn soft sm" style="margin-top:12px" data-act="shareAttempt" data-id="${it.savedId}">${icon('share', true)}Ulashish</button>` : ''}
  </div>`;
}

function readingBody() {
  const passage = it.test.passages.find(p => p.num === it.part) || it.test.passages[0];
  const pane = it.pane || 'text';
  const tabs = `<div class="segmented" id="pane-tabs"><button class="${pane === 'text' ? 'on' : ''}" data-act="iqPane" data-pane="text">Matn</button>
    <button class="${pane === 'q' ? 'on' : ''}" data-act="iqPane" data-pane="q">Savollar</button></div>`;
  const wide = window.innerWidth >= 900;
  return `${wide ? '' : tabs}<div class="exam-grid split" style="margin-top:12px">
    <div class="exam-pane pane-text" ${!wide && pane !== 'text' ? 'hidden' : ''}>
      <div class="passage long"><b>${esc(passage.title)}</b>\n\n${esc(passage.text)}</div></div>
    <div class="exam-pane" ${!wide && pane !== 'q' ? 'hidden' : ''}>${resultCard()}${headingsList()}${partQuestions().map(questionCard).join('')}</div></div>`;
}

function audioFor(part) { return it.test.audio && it.test.audio[part]; }

function playerHTML() {
  const audio = audioFor(it.part);
  const speech = !audio && 'speechSynthesis' in window && typeof SpeechSynthesisUtterance !== 'undefined';
  if (!audio && !speech) {
    return `<div class="player"><div class="h3">Audio bu qurilmada ishlamaydi</div>
      <p class="small muted">Matnni o'qib mashq qilishingiz mumkin.</p>
      <button class="btn sm" data-act="iqScript">Matnni ko'rish</button></div>`;
  }
  return `<div class="player">
    <div class="row"><button id="play-btn" class="play-btn" data-act="iqPlay" aria-label="Tinglash">${icon('play')}</button>
      <div class="grow"><div class="h3">Section ${it.part}</div><div id="audio-state" class="label">${audio ? 'Tinglashga tayyor' : "Qurilma ovozi bilan o'qiladi"}</div></div>
      ${audio ? `<span id="audio-time" class="small muted num">00:00</span>` : ''}</div>
    ${audio ? `<audio id="audio" preload="metadata" src="${esc(audio.url)}"></audio>
      <input id="audio-seek" type="range" min="0" max="1000" value="0">
      <div class="between"><button class="btn sm" data-act="iqSkip" data-step="-10">-10s</button>
      <div class="row"><button class="btn sm" data-act="iqRate" data-rate="0.85">0.85x</button><button class="btn sm soft" data-act="iqRate" data-rate="1">1x</button></div>
      <button class="btn sm" data-act="iqSkip" data-step="10">+10s</button></div>` : ''}
  </div>`;
}

function scriptHTML() {
  if (!it.graded && !it.showScript) return '';
  return `<div class="card"><div class="eyebrow">Tapescript</div><div class="pre" style="margin-top:6px">${esc(it.test.scripts[it.part] || '')}</div></div>`;
}

function listeningBody() {
  return `<div class="exam-grid">${playerHTML()}${resultCard()}${partQuestions().map(questionCard).join('')}${scriptHTML()}</div>`;
}

function drawTest() {
  const main = document.getElementById('exam-main');
  if (!main) return;
  stopTestAudio();
  main.innerHTML = it.kind === 'reading' ? readingBody() : listeningBody();
  const parts = it.kind === 'reading' ? it.test.passages.map(p => p.num) : [1, 2, 3, 4];
  document.getElementById('exam-bottom').innerHTML = `
    <div class="segmented grow">${parts.map(n => `<button class="${n === it.part ? 'on' : ''}" data-act="iqPart" data-part="${n}">${n}</button>`).join('')}</div>
    ${it.graded ? `<button class="btn primary" style="flex:0 0 auto" data-act="iqClose">Yopish</button>`
      : `<button class="btn primary" style="flex:0 0 auto" data-act="iqGrade">Yakunlash</button>`}`;
  const count = Object.keys(it.answers).length;
  document.getElementById('exam-bar').style.width = `${count / it.test.questions.length * 100}%`;
  bindAudio();
}

function bindAudio() {
  const audio = document.getElementById('audio');
  if (!audio) return;
  const seek = document.getElementById('audio-seek');
  const clock = document.getElementById('audio-time');
  const status = document.getElementById('audio-state');
  const button = document.getElementById('play-btn');
  const format = s => `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(Math.floor(s % 60)).padStart(2, '0')}`;
  audio.addEventListener('timeupdate', () => {
    clock.textContent = format(audio.currentTime);
    if (audio.duration) seek.value = audio.currentTime / audio.duration * 1000;
  });
  const state = playing => { button.innerHTML = icon(playing ? 'pause' : 'play'); };
  audio.addEventListener('play', () => state(true));
  audio.addEventListener('pause', () => state(false));
  audio.addEventListener('error', () => { status.textContent = "Audio yuklanmadi. Internetni tekshiring."; });
  seek.addEventListener('change', () => { if (audio.duration) audio.currentTime = seek.value / 1000 * audio.duration; });
}

function stopTestAudio() {
  document.getElementById('audio')?.pause();
  if (window.speechSynthesis) window.speechSynthesis.cancel();
  it && (it.speaking = false);
}

function speakScript() {
  const parts = (it.test.scripts[it.part] || '').match(/[^.!?]+[.!?]*/g) || [];
  it.speaking = true;
  document.getElementById('play-btn').innerHTML = icon('pause');
  const say = index => {
    if (!it || !it.speaking || index >= parts.length) { stopTestAudio(); return; }
    const utterance = new SpeechSynthesisUtterance(parts[index].trim());
    utterance.lang = 'en-GB';
    utterance.onend = () => say(index + 1);
    window.speechSynthesis.speak(utterance);
  };
  say(0);
}

async function gradeTest() {
  stopTestAudio();
  stopIeltsTimer();
  if (!it.sealed) {
    it.correct = it.test.questions.filter(q => ieltsCorrect(q, it.answers[q.num])).length;
    it.band = bandFor(it.correct, it.kind);
  }
  it.graded = true;
  setExamGuard(false);
  haptic('good');
  it.pane = 'q';
  drawTest();
  document.getElementById('exam-timer').innerHTML = '<span class="timer off">Yakunlandi</span>';
  const result = await submitAttempt({
    kind: `ielts_${it.kind}`, ref: it.test.num, answers: it.answers,
    duration_s: Math.round((Date.now() - it.startedAt) / 1000), session: it.session || undefined,
  });
  if (result) {
    it.savedId = result.id;
    if (it.sealed) Object.assign(it, { correct: result.report.correct, band: result.report.band });
    drawTest();
    refreshBoot();
  }
}

let ieltsTimer = null;
function stopIeltsTimer() { clearInterval(ieltsTimer); ieltsTimer = null; }
function drawIeltsTimer() {
  const box = document.getElementById('exam-timer');
  if (!box || !it?.deadline) return;
  const left = Math.max(0, Math.ceil((it.deadline - Date.now()) / 1000));
  box.innerHTML = `<span class="timer ${left <= 300 ? 'low' : ''}">${String(Math.floor(left / 60)).padStart(2, '0')}:${String(left % 60).padStart(2, '0')}</span>`;
  if (left === 0) { stopIeltsTimer(); toast('Vaqt tugadi.'); gradeTest(); }
}

views.ieltsTest = {
  full: true,
  render() {
    const label = it.kind === 'reading' ? 'IELTS Reading' : 'IELTS Listening';
    return `<div class="exam"><div class="exam-top"><div class="exam-top-in">
        <button class="icon-btn" data-act="iqExit" aria-label="Chiqish">${icon('x')}</button>
        <div class="exam-title"><span class="eyebrow">${label}</span><span id="exam-timer"><span class="timer off">${esc(it.test.title)}</span></span></div>
        <span style="width:44px"></span></div><div class="exam-progress"><i id="exam-bar"></i></div></div>
      <div id="exam-main" class="exam-main"></div>
      <div class="exam-bottom"><div id="exam-bottom" class="exam-bottom-in"></div></div></div>`;
  },
  mount() {
    drawTest();
    if (it.deadline && !it.graded) {
      drawIeltsTimer();
      ieltsTimer = setInterval(drawIeltsTimer, 1000);
    }
  },
  onBack() { actions.iqExit(); },
  leave() { stopIeltsTimer(); stopTestAudio(); },
};

async function startIelts(kind, num, session, ticket) {
  const sealedTest = ticket?.exam?.test;
  const test = sealedTest || (await loadData('ielts.json'))[kind].find(item => item.num === Number(num));
  if (!test) return;
  const openLimit = kind === 'reading' ? Date.now() + READING_MINUTES * 60000 : 0;
  it = {
    kind, test, session, sealed: !!sealedTest, part: 1, answers: {}, graded: false, pane: 'text', startedAt: Date.now(),
    deadline: ticket ? Date.now() + ticket.seconds_left * 1000 : openLimit,
  };
  setExamGuard(true);
  track('ielts_started', `${kind}_${num}`);
  open('ieltsTest');
}

function saveInput(el) {
  const num = el.dataset.num;
  if (!num || !it) return;
  const value = el.value.trim();
  if (value) it.answers[num] = value;
  else delete it.answers[num];
  document.getElementById('exam-bar').style.width = `${Object.keys(it.answers).length / it.test.questions.length * 100}%`;
}
document.addEventListener('input', event => { if (event.target.closest?.('.iq')) saveInput(event.target); });
document.addEventListener('change', event => { if (event.target.closest?.('.iq')) saveInput(event.target); });

Object.assign(actions, {
  iqSet(el) {
    if (it.graded) return;
    const { num, value } = el.dataset;
    if (it.answers[num] === value) delete it.answers[num];
    else it.answers[num] = value;
    haptic('pick');
    const box = el.closest('.iq');
    const question = it.test.questions.find(q => String(q.num) === num);
    box.outerHTML = questionCard(question);
    document.getElementById('exam-bar').style.width = `${Object.keys(it.answers).length / it.test.questions.length * 100}%`;
  },
  iqPart(el) { it.part = Number(el.dataset.part); it.pane = it.graded ? 'q' : 'text'; window.scrollTo(0, 0); drawTest(); },
  iqPane(el) { it.pane = el.dataset.pane; window.scrollTo(0, 0); drawTest(); },
  iqScript() { it.showScript = true; drawTest(); },
  iqPlay() {
    const audio = document.getElementById('audio');
    if (audio) {
      if (audio.paused) audio.play().catch(() => { document.getElementById('audio-state').textContent = "Audio yuklanmadi."; });
      else audio.pause();
    } else if (it.speaking) {
      stopTestAudio();
      document.getElementById('play-btn').innerHTML = icon('play');
    } else {
      speakScript();
    }
  },
  iqSkip(el) {
    const audio = document.getElementById('audio');
    if (audio) audio.currentTime = Math.max(0, audio.currentTime + Number(el.dataset.step));
  },
  iqRate(el) {
    const audio = document.getElementById('audio');
    if (audio) audio.playbackRate = Number(el.dataset.rate);
    el.parentElement.querySelectorAll('button').forEach(b => b.classList.toggle('soft', b === el));
  },
  iqGrade() {
    const empty = it.test.questions.length - Object.keys(it.answers).length;
    askConfirm(empty ? `${empty} ta savol bo'sh. Testni yakunlaysizmi?` : 'Testni yakunlaysizmi?', gradeTest);
  },
  iqClose() { leaveView(); },
  iqExit() {
    if (it.graded) { leaveView(); return; }
    askConfirm("Testdan chiqasizmi? Javoblar saqlanmaydi.", () => { setExamGuard(false); leaveView(); });
  },
  startIelts(el) { startIelts(el.dataset.kind, el.dataset.num, null); },
  ieltsTab(el) { App.ieltsTab = el.dataset.tab2; draw(); },
});

function testRows(kind, tests) {
  return tests.map(test => {
    const words = kind === 'reading' ? test.passages.reduce((sum, p) => sum + p.text.split(/\s+/).length, 0) : 0;
    const label = kind === 'reading'
      ? `3 ta matn · 40 savol · ${words > 1800 ? "to'liq uzunlik" : 'qisqa matnlar'}`
      : '4 bo\'lim · 40 savol';
    return `<button class="list-row" data-act="startIelts" data-kind="${kind}" data-num="${test.num}">
      <span class="tile ${kind === 'reading' ? '' : 'good'}">${icon(kind === 'reading' ? 'file' : 'head')}</span>
      <span class="grow"><span class="h3">${esc(test.title)}</span><br><span class="label">${esc(label)}</span></span>
      <span class="chev">${icon('right', true)}</span></button>`;
  }).join('');
}

views.ielts = {
  tab: 'ielts',
  async render() {
    const tab = App.ieltsTab || 'reading';
    const button = (key, label) => `<button class="${tab === key ? 'on' : ''}" data-act="ieltsTab" data-tab2="${key}">${label}</button>`;
    let body;
    if (tab === 'writing') body = await writingTab();
    else {
      const data = await loadData('ielts.json');
      body = `<div class="list">${testRows(tab, data[tab])}</div>`;
    }
    return `<div class="page stack"><div class="h1">IELTS Academic</div>
      <div class="segmented">${button('reading', 'Reading')}${button('listening', 'Listening')}${button('writing', 'Writing')}</div>${body}</div>`;
  },
};
