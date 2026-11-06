'use strict';
// Score reports, answer review and the results tab.

const SECTION_LABELS = { rw: 'Reading & Writing', math: 'Math' };
const ROUTE_LABELS = { hard: 'Qiyin modul', easy: 'Oson modul' };
const DIFFICULTY_LABELS = { Easy: 'Oson', Medium: "O'rta", Hard: 'Qiyin' };

function percent(part) { return part.total ? Math.round(part.correct / part.total * 100) : 0; }

function domainBars(domains) {
  return domains.map(item => {
    const value = percent(item);
    return `<div class="domain"><div class="between"><span class="h3">${esc(DOMAIN_NAMES[item.domain] || item.domain)}</span>
      <span class="small muted num">${item.correct} / ${item.total}</span></div>
      <div class="bar ${accuracyTone(value)}"><i style="width:${value}%"></i></div></div>`;
  }).join('');
}

function stepButtons(steps) {
  return (steps || []).map((step, index) => `<button class="list-row" data-act="reportStep" data-index="${index}">
    <span class="tile">${icon(step.action.type === 'review' ? 'repeat' : 'target')}</span>
    <span class="grow h3">${esc(step.text)}</span><span class="chev">${icon('right', true)}</span></button>`).join('');
}

function satReportBody(report) {
  const delta = report.previous != null ? report.score - report.previous : null;
  const sections = Object.entries(report.sections).map(([key, part]) => `<div class="card tight stat">
    <div class="label">${SECTION_LABELS[key]}</div><div class="v">${part.score}</div>
    ${part.low ? `<div class="label num">${part.low} – ${part.high}</div>` : ''}
    <div class="label num">${part.correct} / ${part.total} to'g'ri</div>
    <div class="label">${ROUTE_LABELS[part.route] || ''}</div></div>`).join('');
  const levels = Object.entries(report.difficulty || {}).sort((a, b) => Object.keys(DIFFICULTY_LABELS).indexOf(a[0]) - Object.keys(DIFFICULTY_LABELS).indexOf(b[0]));
  return `<div class="card score-hero">
      <div class="eyebrow">${esc(report.title)}</div>
      <div class="big">${report.score}</div>
      ${report.low ? `<div class="muted num">Taxminiy oraliq: ${report.low} – ${report.high}</div>` : ''}
      ${delta != null ? `<div style="margin-top:8px"><span class="chip ${delta >= 0 ? 'good' : 'bad'} num">${delta >= 0 ? '+' : ''}${Math.round(delta)} oldingi mockka nisbatan</span></div>` : ''}
    </div>
    <div class="grid2">${sections}</div>
    ${report.domains?.length ? `<div class="section-title">Mavzular bo'yicha</div><div class="card">${domainBars(report.domains)}</div>` : ''}
    ${levels.length ? `<div class="section-title">Qiyinlik bo'yicha</div><div class="grid3">${levels.map(([name, part]) => `<div class="card tight stat">
      <div class="label">${DIFFICULTY_LABELS[name]}</div><div class="v">${percent(part)}%</div><div class="label num">${part.correct} / ${part.total}</div></div>`).join('')}</div>` : ''}
    ${report.pacing?.avg_s ? `<div class="section-title">Vaqt</div><div class="card stack sm"><div class="between"><span>O'rtacha bir savolga</span><span class="h3 num">${report.pacing.avg_s} soniya</span></div>
      <div class="small muted">${esc(report.pacing.tip)}</div></div>` : ''}`;
}

function practiceReportBody(report) {
  const value = percent(report);
  return `<div class="card score-hero"><div class="eyebrow">${esc(report.title)}</div>
      <div class="big">${report.correct} / ${report.total}</div><div class="muted num">${value}% to'g'ri</div></div>
    ${report.kind === 'diagnostic' ? `<div class="card small muted">16 ta savol aniq ball chiqarish uchun kam, shuning uchun bu yerda ball emas, mavzular bo'yicha holat ko'rsatiladi.</div>` : ''}
    ${report.domains?.length ? `<div class="section-title">Mavzular bo'yicha</div><div class="card">${domainBars(report.domains)}</div>` : ''}`;
}

views.report = {
  full: true,
  render({ id, report, review }) {
    App.reportSteps = report.steps || [];
    const body = report.kind === 'sat_mock' ? satReportBody(report) : practiceReportBody(report);
    const offline = !report.offline ? '' : `<div class="card tight small">${hasTelegramUser
      ? "Internet yo'q, shuning uchun bu taxminiy hisob. Natija ulanish tiklanganda saqlanadi."
      : "Natija saqlanmadi. Natijalaringiz saqlanishi uchun testni Telegram ichida oching."}</div>`;
    return `<div class="page flush stack">${offline}${body}
      ${App.reportSteps.length ? `<div class="section-title">Keyingi qadamlar</div><div class="list">${stepButtons(App.reportSteps)}</div>` : ''}
      <div class="grid2">
        ${review ? `<button class="btn soft" data-act="reviewAnswers">${icon('eye', true)}Tahlil</button>` : ''}
        ${id ? `<button class="btn" data-act="shareAttempt" data-id="${id}">${icon('share', true)}Ulashish</button>` : ''}
      </div>
      <button class="btn block" data-act="reportDone">Yopish</button>
      <p class="small muted center">Ball taxminiy. Bu rasmiy College Board natijasi emas.</p></div>`;
  },
  onBack() { actions.reportDone(); },
};

async function reviewAnswers(review) {
  document.getElementById('app').innerHTML = loadingCards(2);
  await Promise.all([satBank(), loadNotes()]);
  const ids = review.ids.filter(id => App.bank[id]);
  startRun({ mode: 'review', title: 'Tahlil', subtitle: `${ids.length} savol`, ids, answers: review.answers, onFinish: leaveView });
}

function lineChart(points) {
  const width = 340, height = 160, pad = 26;
  const values = points.flatMap(p => [p.low ?? p.score, p.high ?? p.score]);
  const min = Math.min(...values) - 30, max = Math.max(...values) + 30;
  const x = i => pad + (points.length === 1 ? (width - 2 * pad) / 2 : i / (points.length - 1) * (width - 2 * pad));
  const y = v => height - pad - (v - min) / (max - min) * (height - 2 * pad);
  const line = points.map((p, i) => `${x(i).toFixed(1)},${y(p.score).toFixed(1)}`).join(' ');
  const band = points.length > 1 && points[0].low != null
    ? `<polygon fill="var(--accent-soft)" stroke="none" points="${points.map((p, i) => `${x(i)},${y(p.high)}`).join(' ')} ${[...points].reverse().map((p, i) => `${x(points.length - 1 - i)},${y(p.low)}`).join(' ')}"/>` : '';
  const dots = points.map((p, i) => `<circle class="fig-dot" cx="${x(i)}" cy="${y(p.score)}" r="4"/>
    <text class="fig-small" x="${x(i)}" y="${y(p.score) - 10}" text-anchor="middle">${Math.round(p.score)}</text>`).join('');
  return `<svg class="chart" viewBox="0 0 ${width} ${height}" role="img" aria-label="Natijalar grafigi">${band}<polyline class="fig-line" points="${line}"/>${dots}</svg>`;
}

const ATTEMPT_ICONS = { sat_mock: 'target', practice: 'spark', diagnostic: 'target', ielts_reading: 'file', ielts_listening: 'head' };

function attemptRow(item) {
  const value = item.kind === 'sat_mock' ? Math.round(item.score)
    : item.kind.startsWith('ielts') ? Number(item.score).toFixed(1) : `${item.correct}/${item.total}`;
  return `<button class="list-row" data-act="openAttempt" data-id="${item.id}">
    <span class="tile">${icon(ATTEMPT_ICONS[item.kind] || 'file')}</span>
    <span class="grow"><span class="h3">${esc(item.title)}</span><br><span class="label num">${esc(item.day)}</span></span>
    <span class="h3 num">${value}</span><span class="chev">${icon('right', true)}</span></button>`;
}

function goalCard(boot, latestMock) {
  const target = boot.me.target_sat;
  if (!latestMock) return '';
  const score = Math.round(latestMock.score);
  const gap = target ? target - score : null;
  return `<div class="card stack sm">
    <div class="between"><span class="eyebrow">Hozirgi taxminiy SAT</span>${target ? `<span class="chip accent num">Maqsad ${target}</span>` : ''}</div>
    <div class="row" style="align-items:baseline"><span class="h1 num" style="font-size:34px">${score}</span>
      ${latestMock.low ? `<span class="muted num small">${Math.round(latestMock.low)} – ${Math.round(latestMock.high)}</span>` : ''}</div>
    ${target ? `<div class="bar"><i style="width:${Math.min(100, (score - 400) / (target - 400) * 100)}%"></i></div>
      <div class="small muted">${gap > 0 ? `Maqsadgacha ${gap} ball qoldi` : 'Maqsadga yetdingiz'}</div>` : ''}</div>`;
}

views.results = {
  tab: 'results',
  async render() {
    if (!hasTelegramUser) return `<div class="page"><div class="card empty">Natijalar Telegram ichida saqlanadi.</div></div>`;
    const [list] = await Promise.all([api('attempts').catch(() => ({ attempts: [] })), refreshBoot()]);
    const boot = App.boot;
    const attempts = list.attempts;
    const mocks = attempts.filter(a => a.kind === 'sat_mock').reverse().slice(-8);
    const latest = kind => attempts.find(a => a.kind === kind);
    const reading = latest('ielts_reading'), listening = latest('ielts_listening');
    if (!attempts.length) {
      return `<div class="page stack"><div class="h1">Natijalar</div><div class="card empty">Birinchi testni ishlang, natijalar shu yerda paydo bo'ladi.</div>
        <button class="btn primary block" data-act="tab" data-tab="sat">Testni boshlash</button></div>`;
    }
    const known = boot.mastery.filter(d => d.total);
    return `<div class="page stack"><div class="h1">Natijalar</div>
      ${goalCard(boot, mocks[mocks.length - 1])}
      ${mocks.length > 1 ? `<div class="card stack sm"><div class="h3">SAT mock natijalari</div>${lineChart(mocks)}</div>` : ''}
      ${reading || listening ? `<div class="grid2">
        ${reading ? `<div class="card tight stat"><div class="label">IELTS Reading</div><div class="v">${Number(reading.score).toFixed(1)}</div></div>` : ''}
        ${listening ? `<div class="card tight stat"><div class="label">IELTS Listening</div><div class="v">${Number(listening.score).toFixed(1)}</div></div>` : ''}</div>` : ''}
      ${known.length ? `<div class="section-title">Mavzular bo'yicha aniqlik</div><div class="card">${domainBars(known)}</div>` : ''}
      <div class="section-title">Oxirgi urinishlar</div><div class="list">${attempts.slice(0, 15).map(attemptRow).join('')}</div></div>`;
  },
};

async function shareAttempt(id) {
  const share = await api('share', { method: 'POST', body: { attempt: id } }).catch(() => null);
  if (!share) { toast("Ulashib bo'lmadi."); return; }
  const story = tgAtLeast('7.8') && ['android', 'ios'].includes(tg.platform);
  sheet(`<div class="stack"><div class="h2">Natijani ulashish</div>
    <p class="small muted">Do'stingiz havola orqali kelib mashq boshlasa, sizga qo'shimcha AI tekshiruvi beriladi.</p>
    ${story ? `<button class="btn primary block lg" data-act="shareStory" data-image="${esc(share.image)}" data-link="${esc(share.link)}">Story'ga joylash</button>` : ''}
    <button class="btn ${story ? '' : 'primary'} block lg" data-act="shareChat" data-link="${esc(share.link)}" data-text="${esc(share.text)}">Telegram'da yuborish</button></div>`);
}

Object.assign(actions, {
  reportDone() {
    const fromTab = stack.length > 1;
    if (fromTab) leaveView();
    else open('home', {}, { reset: true });
  },
  reportStep(el) { runTask(App.reportSteps[Number(el.dataset.index)].action); },
  reviewAnswers() { reviewAnswers(current().params.review); },
  shareAttempt(el) { shareAttempt(el.dataset.id); },
  shareStory(el) {
    tgSafe(() => tg.shareToStory(el.dataset.image, { text: 'IELTS & SAT Daily', widget_link: { url: el.dataset.link, name: 'Mashq qilish' } }));
    closeSheet();
  },
  shareChat(el) { shareLink(el.dataset.link, el.dataset.text); closeSheet(); },
  async openAttempt(el) {
    const data = await api(`attempts/${el.dataset.id}`).catch(() => null);
    if (!data) return;
    if (data.kind.startsWith('ielts')) {
      const report = data.report;
      sheet(`<div class="stack center"><div class="h2">${esc(data.title)}</div>
        <div class="score-hero"><div class="big">${Number(report.band).toFixed(1)}</div><div class="muted num">${report.correct} / ${report.total} to'g'ri</div></div>
        <div class="stack" style="text-align:left">${(report.types || []).map(part => `<div class="between small"><span>${esc(part.label)}</span><span class="num">${part.correct} / ${part.total}</span></div>`).join('')}</div></div>`);
      return;
    }
    const answers = Object.fromEntries(data.answers.map(row => [row.question_id, row.chosen]));
    open('report', { id: data.id, report: data.report, review: { ids: data.answers.map(row => row.question_id), answers } });
  },
});
