'use strict';
// Profile, goals, referrals, joining a group exam, and the learning center panel.

function focusLabel(focus) { return { sat: 'SAT', ielts: 'IELTS', both: 'SAT va IELTS' }[focus] || 'Tanlanmagan'; }

views.profile = {
  tab: 'profile',
  async render() {
    if (!hasTelegramUser) {
      return `<div class="page stack"><div class="h1">Profil</div>
        <div class="card empty">Natijalar va reja saqlanishi uchun ilovani Telegram ichida oching.</div></div>`;
    }
    await refreshBoot();
    const { me, referral, staff } = App.boot;
    return `<div class="page stack"><div class="h1">${esc(me.first_name || 'Profil')}</div>
      <div class="grid2">
        <div class="card tight stat"><div class="label">Hozirgi seriya</div><div class="v">${me.streak} kun</div></div>
        <div class="card tight stat"><div class="label">Eng uzun seriya</div><div class="v">${me.best_streak} kun</div></div>
      </div>
      <div class="section-title">Maqsad</div>
      <div class="list">
        <button class="list-row" data-act="open" data-view="goals"><span class="tile">${icon('target')}</span>
          <span class="grow"><span class="h3">${esc(focusLabel(me.focus))}</span><br>
          <span class="label">${[me.target_sat ? `SAT ${me.target_sat}` : '', me.target_ielts ? `IELTS ${me.target_ielts}` : '', `kuniga ${me.daily_minutes} daqiqa`].filter(Boolean).join(' · ')}</span></span>
          <span class="chev">${icon('right', true)}</span></button>
        <div class="list-row"><span class="tile warn">${icon('bell')}</span>
          <span class="grow"><span class="h3">Eslatmalar</span><br><span class="label">Har kuni soat ${me.reminder_hour}:00 da</span></span>
          <button class="switch ${me.reminders_on ? 'on' : ''}" data-act="toggleReminders" aria-label="Eslatmalar"></button></div>
      </div>
      <div class="section-title">Do'stlarni taklif qilish</div>
      <div class="card stack">
        <div class="row"><span class="tile good">${icon('gift')}</span><span class="grow small">Do'stingiz havola orqali kelib mashq boshlasa, sizga <b>+1 AI tekshiruvi</b> beriladi.</span></div>
        <div class="grid3">
          <div class="stat"><div class="v">${referral.joined}</div><div class="label">Keldi</div></div>
          <div class="stat"><div class="v">${referral.active}</div><div class="label">Boshladi</div></div>
          <div class="stat"><div class="v">${referral.bonus}</div><div class="label">Bonus</div></div>
        </div>
        <button class="btn soft block" data-act="inviteFriend" data-link="${esc(referral.link)}">${icon('share', true)}Taklif havolasini yuborish</button>
      </div>
      <div class="section-title">O'quv markazi</div>
      <div class="list">
        <button class="list-row" data-act="enterCode"><span class="tile">${icon('key')}</span>
          <span class="grow"><span class="h3">Imtihon kodini kiritish</span><br><span class="label">O'qituvchi bergan 6 belgili kod</span></span>
          <span class="chev">${icon('right', true)}</span></button>
        ${staff ? `<button class="list-row" data-act="open" data-view="center"><span class="tile good">${icon('school')}</span>
          <span class="grow"><span class="h3">Markaz paneli</span><br><span class="label">Guruh imtihonlari va natijalar</span></span>
          <span class="chev">${icon('right', true)}</span></button>` : ''}
      </div>
      <p class="small muted center" style="padding:8px">Bu mustaqil mashq platformasi: College Board, Cambridge, British Council va IDP bilan aloqador emas va ular tomonidan tasdiqlanmagan. SAT va IELTS tegishli egalarining savdo belgilari.</p>
    </div>`;
  },
};

function goalsForm(me, finishLabel) {
  const minutes = [15, 30, 45, 60].map(value => `<button class="${me.daily_minutes === value ? 'on' : ''}" data-act="goalMinutes" data-value="${value}">${value}</button>`).join('');
  const hours = Array.from({ length: 17 }, (_, i) => i + 7).map(h => `<option value="${h}" ${me.reminder_hour === h ? 'selected' : ''}>${h}:00</option>`).join('');
  return `<div class="stack lg">
    <div class="field"><span class="h3">Nimaga tayyorlanyapsiz?</span>
      <div class="pick" id="goal-focus">${[['sat', 'target', 'Digital SAT'], ['ielts', 'book', 'IELTS Academic'], ['both', 'grid', 'Ikkalasi ham']].map(([value, name, label]) => (
        `<button class="${me.focus === value ? 'on' : ''}" data-act="goalFocus" data-value="${value}">${icon(name)}<span class="h3">${label}</span></button>`
      )).join('')}</div></div>
    <div class="field"><div class="between"><span class="h3">SAT maqsadi</span><span id="sat-val" class="h3 num">${me.target_sat || 1300}</span></div>
      <input id="goal-sat" type="range" min="800" max="1600" step="10" value="${me.target_sat || 1300}"></div>
    <div class="field"><div class="between"><span class="h3">IELTS maqsadi</span><span id="ielts-val" class="h3 num">${(me.target_ielts || 7).toFixed(1)}</span></div>
      <input id="goal-ielts" type="range" min="5" max="9" step="0.5" value="${me.target_ielts || 7}"></div>
    <div class="field"><span class="h3">Imtihon sanasi</span>
      <input id="goal-date" class="input" type="date" value="${esc(me.exam_date || '')}"><span class="label">Hali aniq bo'lmasa, bo'sh qoldiring.</span></div>
    <div class="field"><span class="h3">Kuniga necha daqiqa?</span><div class="pick cols" id="goal-minutes">${minutes}</div></div>
    <div class="field"><span class="h3">Eslatma vaqti</span><select id="goal-hour" class="input">${hours}</select></div>
    <button class="btn primary block lg" data-act="saveGoals">${esc(finishLabel)}</button></div>`;
}

function bindGoalInputs() {
  const sat = document.getElementById('goal-sat'), ielts = document.getElementById('goal-ielts');
  sat.addEventListener('input', () => { document.getElementById('sat-val').textContent = sat.value; });
  ielts.addEventListener('input', () => { document.getElementById('ielts-val').textContent = Number(ielts.value).toFixed(1); });
}

function readGoals() {
  const focus = document.querySelector('#goal-focus .on')?.dataset.value;
  const minutes = document.querySelector('#goal-minutes .on')?.dataset.value;
  const body = {
    target_sat: Number(document.getElementById('goal-sat').value),
    target_ielts: Number(document.getElementById('goal-ielts').value),
    exam_date: document.getElementById('goal-date').value || null,
    reminder_hour: Number(document.getElementById('goal-hour').value),
    onboarded: true,
  };
  if (focus) body.focus = focus;
  if (minutes) body.daily_minutes = Number(minutes);
  return body;
}

views.goals = {
  full: true,
  render() {
    const me = App.boot?.me || { daily_minutes: 30, reminder_hour: 19 };
    return `<div class="page flush stack lg"><div class="h1">Maqsadlarim</div>${goalsForm(me, 'Saqlash')}</div>`;
  },
  mount: bindGoalInputs,
};

function statusLabel(session) { return session.status === 'open' ? '<span class="chip good">Ochiq</span>' : '<span class="chip">Yopilgan</span>'; }

views.center = {
  full: true,
  async render() {
    const data = await api('teacher').catch(() => null);
    if (!data) return `<div class="page flush"><div class="card empty">Markaz paneli sizga ochiq emas.</div></div>`;
    App.teacher = data;
    const stats = data.stats ? `<div class="grid3">
      <div class="card tight stat"><div class="v">${data.stats.users}</div><div class="label">O'quvchi</div></div>
      <div class="card tight stat"><div class="v">${data.stats.active_week}</div><div class="label">7 kunda faol</div></div>
      <div class="card tight stat"><div class="v">${data.stats.mocks}</div><div class="label">Mock</div></div></div>` : '';
    const rows = data.sessions.map(item => `<button class="list-row" data-act="open" data-view="centerSession" data-code="${item.code}">
      <span class="grow"><span class="h3">${esc(item.title)}</span><br><span class="label num">Kod ${item.code} · ${item.results} natija</span></span>
      ${statusLabel(item)}<span class="chev">${icon('right', true)}</span></button>`).join('');
    return `<div class="page flush stack"><div class="h1">Markaz paneli</div>${stats}
      <button class="btn primary block lg" data-act="newSession">Yangi guruh imtihoni</button>
      ${rows ? `<div class="list">${rows}</div>` : '<div class="card empty">Hali imtihon ochilmagan.</div>'}</div>`;
  },
};

views.centerSession = {
  full: true,
  async render({ code }) {
    const data = await api(`teacher/sessions/${code}`).catch(() => null);
    if (!data) return `<div class="page flush"><div class="card empty">Topilmadi.</div></div>`;
    const { session } = data;
    const rows = data.students.map((student, index) => `<tr><td class="num">${index + 1}</td><td>${esc(student.name)}</td>
      <td class="num">${student.score == null ? '—' : Math.round(student.score * 10) / 10}</td><td class="num">${student.correct}/${student.total}</td><td class="num">${student.minutes}</td></tr>`).join('');
    const topics = data.topics.slice(0, 4).map(item => `<div class="domain"><div class="between"><span class="h3">${esc(DOMAIN_NAMES[item.domain] || item.domain)}</span>
      <span class="small muted num">${percent(item)}%</span></div><div class="bar ${accuracyTone(percent(item))}"><i style="width:${percent(item)}%"></i></div></div>`).join('');
    const open = session.status === 'open';
    return `<div class="page flush stack"><div class="h2">${esc(session.title)}</div>
      <div class="code-display">${session.code}</div>
      <div class="between"><span class="small muted">O'quvchilar botga <b>/mock ${session.code}</b> deb yozadi</span>${statusLabel(session)}</div>
      <div class="grid2"><div class="card tight stat"><div class="label">Topshirganlar</div><div class="v">${data.count}</div></div>
        <div class="card tight stat"><div class="label">O'rtacha ball</div><div class="v">${data.average ?? '—'}</div></div></div>
      ${topics ? `<div class="section-title">Guruhning zaif mavzulari</div><div class="card">${topics}</div>` : ''}
      <div class="section-title">Natijalar</div>
      ${rows ? `<div class="card table-wrap"><table class="data"><thead><tr><th>#</th><th>O'quvchi</th><th>Ball</th><th>To'g'ri</th><th>Daqiqa</th></tr></thead><tbody>${rows}</tbody></table></div>` : '<div class="card empty">Hali natija yo\'q.</div>'}
      ${open ? `<button class="btn primary block" data-act="shareSession" data-code="${session.code}" data-title="${esc(session.title)}">${icon('share', true)}Guruhga havola yuborish</button>` : ''}
      <div class="grid2"><button class="btn soft" data-act="exportSession" data-code="${session.code}" ${data.count ? '' : 'disabled'}>CSV yuklash</button>
        ${open ? `<button class="btn danger" data-act="closeExam" data-code="${session.code}">Imtihonni yopish</button>` : ''}</div></div>`;
  },
};

async function joinByCode(code) {
  try {
    const { session } = await api('sessions/join', { method: 'POST', body: { code } });
    App.session = session;
    closeSheet();
    open('sessionStart', { session }, { reset: true });
  } catch (e) {
    toast(e.status === 404 ? "Kod topilmadi yoki imtihon yopilgan." : "Ulanib bo'lmadi.");
  }
}

views.sessionStart = {
  full: true,
  render({ session }) {
    return `<div class="page flush"><div class="break">
      <span class="tile">${icon('school')}</span><div class="h1">${esc(session.title)}</div>
      <p class="muted">Guruh imtihoni. Natijangiz o'qituvchingizga ko'rinadi.</p>
      <button class="btn primary block lg" data-act="beginSession">Imtihonni boshlash</button>
      <button class="btn block" data-act="tab" data-tab="home">Keyinroq</button></div></div>`;
  },
};

Object.assign(actions, {
  goalFocus(el) { el.parentElement.querySelectorAll('button').forEach(b => b.classList.toggle('on', b === el)); haptic('pick'); },
  goalMinutes(el) { el.parentElement.querySelectorAll('button').forEach(b => b.classList.toggle('on', b === el)); haptic('pick'); },
  async saveGoals() {
    const body = readGoals();
    if (!body.focus) { toast('Avval imtihonni tanlang.'); return; }
    if (!hasTelegramUser) { open('home', {}, { reset: true }); return; }
    try {
      await api('profile', { method: 'POST', body });
      await refreshBoot();
      haptic('good');
      if (stack.length > 1) leaveView();
      else open('home', {}, { reset: true });
    } catch (e) {
      toast("Saqlab bo'lmadi. Qayta urinib ko'ring.");
    }
  },
  async toggleReminders(el) {
    const value = !App.boot.me.reminders_on;
    el.classList.toggle('on', value);
    App.boot.me.reminders_on = value;
    await api('profile', { method: 'POST', body: { reminders_on: value } }).catch(() => toast("Saqlab bo'lmadi."));
  },
  inviteFriend(el) { shareLink(el.dataset.link, "Men bu yerda SAT va IELTS'ga bepul tayyorlanyapman. Sen ham qo'shil!"); },
  enterCode() {
    sheet(`<div class="stack"><div class="h2">Imtihon kodi</div>
      <input id="code-input" class="input code" maxlength="6" autocomplete="off" autocapitalize="characters" placeholder="ABC123">
      <button class="btn primary block lg" data-act="submitCode">Kirish</button></div>`);
    document.getElementById('code-input').focus();
  },
  submitCode() {
    const code = document.getElementById('code-input').value.trim();
    if (code) joinByCode(code);
  },
  beginSession() {
    const session = App.session;
    if (session.kind === 'sat_mock') startMock(session.ref, session.code);
    else startIelts(session.kind.replace('ielts_', ''), session.ref, session.code);
  },
  newSession() {
    const options = App.teacher.catalog.map(item => `<option value="${esc(item.kind)}|${esc(item.ref)}">${esc(item.title)}</option>`).join('');
    sheet(`<div class="stack"><div class="h2">Yangi guruh imtihoni</div>
      <div class="field"><span class="label">Imtihon</span><select id="session-exam" class="input">${options}</select></div>
      <div class="field"><span class="label">Nomi (ixtiyoriy)</span><input id="session-title" class="input" maxlength="80" placeholder="Masalan: 11-A guruh, 1-mock"></div>
      <button class="btn primary block lg" data-act="createSession">Yaratish</button></div>`);
  },
  async createSession() {
    const [kind, ref] = document.getElementById('session-exam').value.split('|');
    const title = document.getElementById('session-title').value;
    try {
      const { session } = await api('teacher/sessions', { method: 'POST', body: { kind, ref, title } });
      closeSheet();
      open('centerSession', { code: session.code });
    } catch (e) {
      toast("Yaratib bo'lmadi.");
    }
  },
  shareSession(el) {
    const bot = App.boot?.bot_username;
    shareLink(`https://t.me/${bot}?start=s_${el.dataset.code}`, `${el.dataset.title}: imtihonga shu havola orqali kiring.`);
  },
  async exportSession(el) {
    try {
      await api(`teacher/sessions/${el.dataset.code}/export`, { method: 'POST' });
      toast('CSV fayl bot chatiga yuborildi.');
    } catch (e) {
      toast("Yuborib bo'lmadi.");
    }
  },
  closeExam(el) {
    askConfirm("Imtihonni yopasizmi? Yangi o'quvchilar kira olmaydi.", async () => {
      await api(`teacher/sessions/${el.dataset.code}/close`, { method: 'POST' }).catch(() => {});
      draw();
    });
  },
});
