'use strict';
// Today screen, onboarding and app start.

const WEEKDAYS = ['Du', 'Se', 'Ch', 'Pa', 'Ju', 'Sh', 'Ya'];

function greeting() {
  const hour = new Date().getHours();
  if (hour < 5) return 'Xayrli tun';
  if (hour < 12) return 'Xayrli tong';
  return hour < 18 ? 'Xayrli kun' : 'Xayrli kech';
}

function taskRow(task, index) {
  return `<button class="task ${task.done ? 'done' : ''}" data-act="runPlanTask" data-index="${index}">
    <span class="tick">${icon('check', true)}</span>
    <span class="grow"><span class="h3">${esc(DOMAIN_NAMES[task.title] || task.title)}</span><br><span class="label">${esc(task.detail)}</span></span>
    <span class="label num">${task.minutes} daq</span></button>`;
}

function weekStrip(week) {
  return `<div class="week">${week.map((entry, index) => {
    const day = new Date(`${entry.day}T12:00:00`);
    const label = WEEKDAYS[(day.getDay() + 6) % 7];
    return `<div><i class="${entry.tests ? 'on' : ''} ${index === week.length - 1 ? 'today' : ''}"></i>${label}</div>`;
  }).join('')}</div>`;
}

function guestHome() {
  return `<div class="page stack"><div class="h1">IELTS & SAT Daily</div>
    <div class="card stack"><div class="h3">Telegram ichida oching</div>
      <p class="small muted">Natijalar, kunlik reja va AI tekshiruvi botdagi Mini App tugmasi orqali ishlaydi. Testlarni bu yerda ham ishlab ko'rishingiz mumkin, lekin ular saqlanmaydi.</p></div>
    <button class="btn primary block lg" data-act="tab" data-tab="sat">SAT mashqlari</button>
    <button class="btn block lg" data-act="tab" data-tab="ielts">IELTS mashqlari</button></div>`;
}

views.home = {
  tab: 'home',
  async render() {
    if (!hasTelegramUser) return guestHome();
    if (!App.boot) await refreshBoot();
    if (!App.boot) return `<div class="page stack"><div class="card empty">Ma'lumotni yuklab bo'lmadi. Internetni tekshiring.</div>
      <button class="btn primary block" data-act="retryBoot">Qayta urinish</button></div>`;
    const { me, plan, summary, week, due } = App.boot;
    App.planTasks = plan.tasks;
    const left = plan.days_left;
    const resume = typeof resumeCard === 'function' ? resumeCard() : '';
    const latest = summary.latest.sat_mock;
    const allDone = plan.total && plan.done === plan.total;
    return `<div class="page stack">
      <div class="between"><div><div class="label">${greeting()}</div><div class="h1">${esc(me.first_name || "O'quvchi")}</div></div>
        <span class="row" style="gap:2px"><span class="chip ${me.streak ? 'warn' : ''} num">${icon('flame', true)}${me.streak} kun</span>${fullscreenButton()}</span></div>
      ${!me.onboarded ? `<button class="card row" data-act="open" data-view="onboarding" style="text-align:left;width:100%">
        <span class="tile">${icon('target')}</span><span class="grow"><span class="h3">Maqsadingizni belgilang</span><br><span class="label">Sizga mos kunlik reja tuzamiz</span></span>
        <span class="chev">${icon('right', true)}</span></button>` : ''}
      ${resume}
      ${left != null && left >= 0 ? `<div class="card tight between"><span class="small muted">Imtihongacha</span><span class="h3 num">${left} kun</span></div>` : ''}
      <div class="between" style="padding:4px 4px 0"><span class="section-title" style="padding:0">Bugungi reja</span>
        ${plan.total ? `<span class="label num">${plan.done} / ${plan.total}</span>` : ''}</div>
      ${plan.tasks.length ? `<div class="list">${plan.tasks.map(taskRow).join('')}</div>` : `<div class="card empty">Bugungi reja bo'sh. Mashq yoki mock tanlang.</div>`}
      ${allDone ? `<div class="card tight row"><span class="tile good">${icon('check')}</span><span class="small">Bugungi rejani bajardingiz. Barakalla!</span></div>` : ''}
      <div class="card stack sm"><div class="between"><span class="h3">Bu hafta</span><span class="label num">${summary.answered} savol ishlangan</span></div>${weekStrip(week)}</div>
      <div class="grid2">
        <button class="card tight stat" data-act="tab" data-tab="results" style="text-align:left"><div class="label">So'nggi SAT</div><div class="v">${latest ? Math.round(latest.score) : '—'}</div></button>
        <button class="card tight stat" data-act="goNotebook" style="text-align:left"><div class="label">Takrorlash</div><div class="v">${due}</div></button>
      </div>
      <button class="btn block" data-act="enterCode">${icon('key', true)}Imtihon kodini kiritish</button></div>`;
  },
  async mount() {
    if (App.boot && App.bootStale) { App.bootStale = false; await refreshBoot(); }
  },
};

views.onboarding = {
  full: true,
  render() {
    const me = App.boot?.me || { daily_minutes: 30, reminder_hour: 19 };
    return `<div class="page flush stack lg"><div class="stack sm"><div class="h1">Xush kelibsiz</div>
      <p class="muted">Bir daqiqada maqsadingizni belgilang, biz har kuni nima qilishni ko'rsatamiz.</p></div>
      ${goalsForm(me, 'Boshlash')}</div>`;
  },
  mount: bindGoalInputs,
};

function channelHandle(url) {
  return `@${String(url).replace(/\/+$/, '').split('/').pop()}`;
}

// Shown instead of the app until the student joins the channel. The server enforces the same rule.
views.channelGate = {
  full: true,
  render() {
    const handle = esc(channelHandle(App.gate ? App.gate.channel : CHANNEL_FALLBACK));
    return `<div class="page stack lg"><div class="stack sm"><div class="h1">Kanalga obuna bo'ling</div>
      <p class="muted">Bot va Mini App ${handle} kanali a'zolari uchun bepul. Kanalda har kuni SAT va IELTS so'zlari, savollar va maslahatlar chiqadi.</p>
      <p class="small muted">Obuna bo'lgach, pastdagi tekshirish tugmasini bosing.</p></div>
      <button class="btn primary block lg" data-act="openChannel">Kanalga o'tish</button>
      <button class="btn block lg" data-act="recheckChannel">Obuna bo'ldim, tekshirish</button></div>`;
  },
};

Object.assign(actions, {
  runPlanTask(el) { runTask(App.planTasks[Number(el.dataset.index)].action); },
  goNotebook() { App.satTab = 'notebook'; open('sat', {}, { reset: true }); },
  async retryBoot() { await refreshBoot(); draw(); },
  openChannel() {
    const url = (App.gate && App.gate.channel) || CHANNEL_FALLBACK;
    haptic('tap');
    if (tgAtLeast('6.1')) tgSafe(() => tg.openTelegramLink(url));
    else window.open(url, '_blank');
  },
  async recheckChannel(el) {
    el.disabled = true;
    await refreshBoot();
    el.disabled = false;
    if (App.gate) {
      toast("Obuna hali ko'rinmayapti. Bir necha soniyadan keyin qayta urinib ko'ring.");
      return;
    }
    flushQueue();
    routeStart();
  },
});

async function startApp() {
  startTelegram();
  document.getElementById('app').innerHTML = loadingCards(3);
  await refreshBoot();
  flushQueue();
  await routeStart();
}

async function routeStart() {
  if (App.gate) {
    open('channelGate', {}, { reset: true });
    return;
  }
  const tab = App.params.get('tab');
  const session = App.params.get('session');
  if (session) {
    await open('home', {}, { reset: true });
    joinByCode(session);
    return;
  }
  if (tab === 'center') {
    await open('profile', {}, { reset: true });
    open('center');
    return;
  }
  if (App.boot && !App.boot.me.onboarded) {
    await open('home', {}, { reset: true });
    open('onboarding');
    return;
  }
  open('home', {}, { reset: true });
}

startApp();
