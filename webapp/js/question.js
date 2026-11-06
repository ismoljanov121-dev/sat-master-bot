'use strict';
// The test screen. One runner serves SAT mocks, practice sets, the diagnostic and answer review.

const SCORE = { b: { Easy: -1, Medium: 0, Hard: 1 }, a: 1.3, guess: 0.2, mean: 500, sd: 110 };

function parseNumber(text) {
  const value = String(text == null ? '' : text).trim().replace(/\s/g, '').replace('−', '-').replace(',', '.');
  if (!/^-?(\d+(\.\d*)?|\.\d+)(\/\d+(\.\d*)?)?$/.test(value)) return null;
  if (value.includes('/')) {
    const [top, bottom] = value.split('/').map(Number);
    return bottom ? top / bottom : null;
  }
  return Number(value);
}

function isCorrect(question, value) {
  if (value == null || value === '') return false;
  if (question.type === 'spr') {
    const given = parseNumber(value);
    if (given == null) return false;
    return question.ans.some(answer => {
      const target = parseNumber(answer);
      return target != null && Math.abs(given - target) <= 1 / 2000;
    });
  }
  return value === question.cor;
}

// Same model as services/scoring.py, used only when the server cannot be reached.
function localSectionScore(items) {
  const grid = [];
  for (let t = -4.5; t <= 4.5001; t += 0.1) grid.push(t);
  const logs = grid.map(() => 0);
  items.forEach(([difficulty, type, correct]) => {
    const guess = type === 'mcq' ? SCORE.guess : 0;
    grid.forEach((theta, i) => {
      const p = guess + (1 - guess) / (1 + Math.exp(-SCORE.a * (theta - SCORE.b[difficulty])));
      logs[i] += Math.log(correct ? p : 1 - p);
    });
  });
  const peak = Math.max(...logs);
  const weights = logs.map((value, i) => Math.exp(-grid[i] * grid[i] / 2 + value - peak));
  const total = weights.reduce((a, b) => a + b, 0);
  const mean = weights.reduce((sum, w, i) => sum + w * grid[i], 0) / total;
  const clip = value => Math.min(800, Math.max(200, Math.round(value / 10) * 10));
  return { score: clip(SCORE.mean + SCORE.sd * mean) };
}

let run = null;

function currentQuestion() { return App.bank[run.ids[run.idx]]; }

function passageHTML(question) {
  const text = question.pas || '';
  const marks = (run.marks && run.marks[question.id]) || [];
  if (question.sec === 'm' || !marks.length) return rich(text);
  let html = '', position = 0;
  [...marks].sort((a, b) => a[0] - b[0]).forEach(([start, end]) => {
    if (start < position) return;
    html += esc(text.slice(position, start)) + `<mark>${esc(text.slice(start, end))}</mark>`;
    position = end;
  });
  return html + esc(text.slice(position));
}

function optionHTML(question, index) {
  const key = 'ABCD'[index];
  const chosen = run.answers[question.id];
  const checked = run.mode === 'review' || (run.checked && run.checked[question.id]);
  const out = (run.elim[question.id] || []).includes(key);
  let state = '';
  if (checked) {
    if (key === question.cor) state = 'right';
    else if (key === chosen) state = 'wrong';
  } else if (key === chosen) {
    state = 'sel';
  }
  const eliminator = run.elimOn && !checked
    ? `<button class="opt-x" data-act="qElim" data-key="${key}" aria-label="Variantni chizish">${icon('minus', true)}</button>` : '';
  return `<div class="opt ${state} ${out ? 'out' : ''}">
    <button class="opt-main" data-act="qPick" data-key="${key}"><span class="opt-key">${key}</span><span class="opt-text">${rich(question.opts[index])}</span></button>
    ${eliminator}</div>`;
}

function sprHTML(question) {
  const checked = run.mode === 'review' || (run.checked && run.checked[question.id]);
  const value = run.answers[question.id] || '';
  return `<div class="spr-box">
    <input id="spr-input" class="input" inputmode="text" autocomplete="off" placeholder="Javobni yozing" maxlength="8" value="${esc(value)}" ${checked ? 'disabled' : ''}>
    <div class="label">Butun son, o'nli kasr yoki oddiy kasr yozing: 12, 0.75, 3/4</div></div>`;
}

function feedbackHTML(question) {
  const value = run.answers[question.id];
  const right = isCorrect(question, value);
  const note = (App.notes && App.notes[question.id]) || {};
  const answer = question.type === 'spr' ? question.ans[0] : question.cor;
  const title = right
    ? "To'g'ri"
    : (value ? `Javobingiz: ${esc(value)}. To'g'ri javob: ${esc(answer)}` : `Javob berilmagan. To'g'ri javob: ${esc(answer)}`);
  return `<div class="feedback ${right ? 'good' : 'bad'}">
    <div class="h3">${title}</div>
    <div class="body">${rich(note.exp)}</div>
    ${note.strat ? `<div class="strategy">${rich(note.strat)}</div>` : ''}</div>`;
}

function questionBody(question) {
  const showFeedback = run.mode === 'review' || (run.checked && run.checked[question.id]);
  const flagged = run.flags[question.id];
  const hasPassage = !!question.pas;
  const longText = (question.pas || '').length > 500;
  const head = `<div class="q-head">
      <span class="h3 num">${run.idx + 1}-savol <span class="muted">/ ${run.ids.length}</span></span>
      <span class="q-tools">
        ${question.type === 'mcq' && run.mode !== 'review' ? `<button class="q-tool blue ${run.elimOn ? 'on' : ''}" data-act="qElimMode">${icon('minus', true)}Chizish</button>` : ''}
        ${run.mode === 'exam' ? `<button class="q-tool ${flagged ? 'on' : ''}" data-act="qFlag">${icon('flag', true)}Belgilash</button>` : ''}
      </span></div>`;
  const textPane = hasPassage ? `<div id="q-passage" class="passage ${longText ? 'long' : ''}">${passageHTML(question)}</div>` : '';
  const answerPane = `${head}${figureHTML(question.fig)}<div class="stem">${rich(question.q)}</div>
    ${question.type === 'spr' ? sprHTML(question) : `<div class="opts">${question.opts.map((_, i) => optionHTML(question, i)).join('')}</div>`}
    ${showFeedback ? feedbackHTML(question) : ''}`;
  if (!hasPassage) return `<div class="exam-grid"><div class="exam-pane">${answerPane}</div></div>`;
  return `<div class="exam-grid split"><div class="exam-pane pane-text">${textPane}</div><div class="exam-pane">${answerPane}</div></div>`;
}

function timerHTML() {
  if (!run.deadline) return `<span class="timer off">${esc(run.subtitle || '')}</span>`;
  if (run.hideTimer) return '<span class="timer off">Vaqt yashirilgan</span>';
  const left = Math.max(0, Math.ceil((run.deadline - Date.now()) / 1000));
  const text = `${String(Math.floor(left / 60)).padStart(2, '0')}:${String(left % 60).padStart(2, '0')}`;
  return `<span class="timer ${left <= 300 ? 'low' : ''}">${text}</span>`;
}

function bottomHTML() {
  const question = currentQuestion();
  const last = run.idx === run.ids.length - 1;
  const position = `<button class="btn nav" data-act="qPalette">${icon('grid', true)}${run.idx + 1} / ${run.ids.length}</button>`;
  const prev = `<button class="btn" data-act="qMove" data-step="-1" ${run.idx === 0 ? 'disabled' : ''}>${icon('left', true)}</button>`;
  if (run.mode === 'practice') {
    const checked = run.checked[question.id];
    if (!checked) return `${position}<button class="btn primary" data-act="qCheck" ${run.answers[question.id] ? '' : 'disabled'}>Tekshirish</button>`;
    return `${position}<button class="btn primary" data-act="${last ? 'qFinish' : 'qMove'}" data-step="1">${last ? 'Yakunlash' : 'Keyingisi'}</button>`;
  }
  if (run.mode === 'review') {
    return `${prev}${position}<button class="btn primary" data-act="${last ? 'qFinish' : 'qMove'}" data-step="1">${last ? 'Yopish' : 'Keyingisi'}</button>`;
  }
  return `${prev}${position}<button class="btn primary" data-act="${last ? 'qFinish' : 'qMove'}" data-step="1">${last ? 'Yakunlash' : 'Keyingisi'}</button>`;
}

function drawQuestion() {
  const main = document.getElementById('exam-main');
  if (!main) return;
  main.innerHTML = questionBody(currentQuestion());
  document.getElementById('exam-bottom').innerHTML = bottomHTML();
  const answered = run.ids.filter(id => run.answers[id]).length;
  document.getElementById('exam-bar').style.width = `${answered / run.ids.length * 100}%`;
  typeset(main);
  run.enteredAt = Date.now();
  const input = document.getElementById('spr-input');
  if (input) input.addEventListener('input', () => setAnswer(input.value.trim()));
}

function recordTime() {
  if (!run || !run.enteredAt) return;
  const id = run.ids[run.idx];
  run.times[id] = (run.times[id] || 0) + Math.round((Date.now() - run.enteredAt) / 1000);
  run.enteredAt = Date.now();
}

function setAnswer(value) {
  const id = run.ids[run.idx];
  if (value) run.answers[id] = value;
  else delete run.answers[id];
  run.onChange?.();
  document.getElementById('exam-bottom').innerHTML = bottomHTML();
  const answered = run.ids.filter(q => run.answers[q]).length;
  document.getElementById('exam-bar').style.width = `${answered / run.ids.length * 100}%`;
}

function moveTo(index) {
  recordTime();
  run.idx = Math.min(run.ids.length - 1, Math.max(0, index));
  run.onChange?.();
  window.scrollTo(0, 0);
  drawQuestion();
}

function tick() {
  if (!run || !run.deadline) return;
  const box = document.getElementById('exam-timer');
  if (box) box.innerHTML = timerHTML();
  if (Date.now() >= run.deadline) {
    stopTimer();
    run.onTimeUp?.();
  }
}

let timerId = null;
function stopTimer() { clearInterval(timerId); timerId = null; }
function startTimer() {
  stopTimer();
  if (run.deadline) timerId = setInterval(tick, 1000);
}
document.addEventListener('visibilitychange', () => { if (!document.hidden) tick(); });

views.runner = {
  full: true,
  render() {
    const tools = (run.tools || []).map(tool => `<button class="icon-btn" data-act="tool" data-tool="${tool.id}" aria-label="${esc(tool.label)}">${icon(tool.icon)}</button>`).join('');
    return `<div class="exam">
      <div class="exam-top"><div class="exam-top-in">
        <button class="icon-btn" data-act="qExit" aria-label="Chiqish">${icon('x')}</button>
        <div class="exam-title" ${run.deadline ? 'data-act="qTimer"' : ''}>
          <span class="eyebrow">${esc(run.title)}</span><span id="exam-timer">${timerHTML()}</span>
        </div>
        ${tools || '<span style="width:44px"></span>'}
      </div><div class="exam-progress"><i id="exam-bar"></i></div></div>
      <div id="exam-main" class="exam-main"></div>
      <div class="exam-bottom"><div id="exam-bottom" class="exam-bottom-in"></div></div>
    </div>`;
  },
  mount() {
    drawQuestion();
    startTimer();
    document.addEventListener('selectionchange', onPassageSelection);
  },
  onBack() { actions.qExit(); },
  leave() {
    recordTime();
    stopTimer();
    document.removeEventListener('selectionchange', onPassageSelection);
    hideHighlightButton();
  },
};

function selectionOffsets() {
  const selection = document.getSelection();
  const box = document.getElementById('q-passage');
  if (!selection || selection.isCollapsed || !box || !box.contains(selection.anchorNode) || !box.contains(selection.focusNode)) return null;
  const range = selection.getRangeAt(0);
  const before = range.cloneRange();
  before.selectNodeContents(box);
  before.setEnd(range.startContainer, range.startOffset);
  const start = before.toString().length;
  return [start, start + range.toString().length];
}

function hideHighlightButton() { document.getElementById('hl-pop')?.remove(); }

function onPassageSelection() {
  if (!run || run.mode === 'review' || currentQuestion().sec === 'm') return;
  const offsets = selectionOffsets();
  hideHighlightButton();
  if (!offsets || offsets[1] <= offsets[0]) return;
  const pop = document.createElement('div');
  pop.id = 'hl-pop';
  pop.className = 'hl-pop';
  pop.innerHTML = `<button class="btn primary sm" data-act="qHighlight">Ajratish</button>`;
  run.pendingMark = offsets;
  document.body.appendChild(pop);
}

Object.assign(actions, {
  qPick(el) {
    const question = currentQuestion();
    if (run.mode === 'review' || (run.checked && run.checked[question.id])) return;
    const key = el.dataset.key;
    if ((run.elim[question.id] || []).includes(key)) run.elim[question.id] = run.elim[question.id].filter(k => k !== key);
    haptic('pick');
    setAnswer(run.answers[question.id] === key ? '' : key);
    run.onChange?.();
    document.querySelectorAll('.opts').forEach(box => {
      box.innerHTML = question.opts.map((_, i) => optionHTML(question, i)).join('');
      typeset(box);
    });
  },
  qElim(el) {
    const question = currentQuestion();
    const list = run.elim[question.id] || [];
    const key = el.dataset.key;
    run.elim[question.id] = list.includes(key) ? list.filter(k => k !== key) : [...list, key];
    if (run.answers[question.id] === key) delete run.answers[question.id];
    run.onChange?.();
    drawQuestion();
  },
  qElimMode() { run.elimOn = !run.elimOn; drawQuestion(); },
  qFlag() {
    const id = currentQuestion().id;
    if (run.flags[id]) delete run.flags[id];
    else run.flags[id] = 1;
    haptic('tap');
    run.onChange?.();
    drawQuestion();
  },
  qMove(el) { moveTo(run.idx + Number(el.dataset.step)); },
  qTimer() { run.hideTimer = !run.hideTimer; document.getElementById('exam-timer').innerHTML = timerHTML(); },
  qHighlight() {
    const id = currentQuestion().id;
    run.marks[id] = [...(run.marks[id] || []), run.pendingMark];
    hideHighlightButton();
    document.getSelection()?.removeAllRanges();
    run.onChange?.();
    document.getElementById('q-passage').innerHTML = passageHTML(currentQuestion());
  },
  qCheck() {
    const question = currentQuestion();
    recordTime();
    run.checked[question.id] = true;
    haptic(isCorrect(question, run.answers[question.id]) ? 'good' : 'bad');
    drawQuestion();
    document.querySelector('.feedback')?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  },
  qPalette() {
    const cells = run.ids.map((id, index) => {
      let state = '';
      if (run.mode === 'review' || (run.checked && run.checked[id])) state = isCorrect(App.bank[id], run.answers[id]) ? 'right' : 'wrong';
      else if (run.answers[id]) state = 'done';
      return `<button class="${state} ${index === run.idx ? 'cur' : ''} ${run.flags[id] ? 'flag' : ''}" data-act="qJump" data-index="${index}">${index + 1}</button>`;
    }).join('');
    const empty = run.ids.filter(id => !run.answers[id]).length;
    const finish = run.mode === 'exam'
      ? `<button class="btn primary block lg" data-act="qFinish">${esc(run.finishLabel || 'Yakunlash')}</button>` : '';
    sheet(`<div class="stack">
      <div class="between"><span class="h2">Savollar</span><span class="chip ${empty ? 'warn' : 'good'}">${empty ? `${empty} ta bo'sh` : 'Hammasi belgilangan'}</span></div>
      <div class="legend"><span><i class="done"></i>Javob berilgan</span><span><i></i>Bo'sh</span><span><i class="flag"></i>Belgilangan</span></div>
      <div class="palette">${cells}</div>${finish}</div>`);
  },
  qJump(el) { closeSheet(); moveTo(Number(el.dataset.index)); },
  qFinish() {
    closeSheet();
    recordTime();
    run.onFinish?.();
  },
  qExit() {
    if (run.mode === 'review') { leaveView(); return; }
    askConfirm(run.exitMessage || "Mashqdan chiqasizmi?", () => { setExamGuard(false); run.onExit?.(); leaveView(); });
  },
  tool(el) { run.tools.find(tool => tool.id === el.dataset.tool)?.open(); },
});

function startRun(config, options) {
  run = {
    mode: 'exam', idx: 0, answers: {}, flags: {}, elim: {}, marks: {}, times: {}, checked: {}, elimOn: false, ...config,
  };
  return open('runner', {}, options);
}
