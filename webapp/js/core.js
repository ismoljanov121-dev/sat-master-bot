'use strict';
// App shell: Telegram integration, navigation, API access and small UI helpers.

const tg = window.Telegram && window.Telegram.WebApp;
const hasTelegramUser = !!(tg && tg.initData);

const App = { boot: null, session: null, params: new URLSearchParams(location.search) };
const views = {};
const actions = {};
const stack = [];
const dataCache = {};

function tgAtLeast(version) { return !!(tg && tg.isVersionAtLeast && tg.isVersionAtLeast(version)); }
function tgSafe(action) { try { action(); } catch (e) { console.warn('[tg]', e); } }

function esc(value) {
  return String(value == null ? '' : value).replace(/[&<>"']/g, ch => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]
  ));
}

function icon(name, small) { return `<svg class="i${small ? ' s' : ''}"><use href="#i-${name}"/></svg>`; }

function hexToRgba(hex, alpha) {
  const match = /^#?([0-9a-f]{6})$/i.exec(hex || '');
  if (!match) return null;
  const n = parseInt(match[1], 16);
  return `rgba(${n >> 16}, ${(n >> 8) & 255}, ${n & 255}, ${alpha})`;
}

function applyTheme() {
  const dark = tg && tg.colorScheme ? tg.colorScheme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
  const root = document.documentElement;
  root.dataset.theme = dark ? 'dark' : 'light';
  const p = (tg && tg.themeParams) || {};
  const set = (name, value) => (value ? root.style.setProperty(name, value) : root.style.removeProperty(name));
  set('--bg', p.secondary_bg_color);
  set('--surface', p.section_bg_color || p.bg_color);
  set('--text', p.text_color);
  set('--muted', p.hint_color);
  set('--accent', p.button_color);
  set('--accent-text', p.button_text_color);
  set('--accent-soft', hexToRgba(p.button_color, dark ? 0.18 : 0.11));
  if (tgAtLeast('6.1')) {
    const surface = p.section_bg_color || p.bg_color;
    if (surface) tgSafe(() => tg.setHeaderColor(surface));
    if (p.secondary_bg_color) tgSafe(() => tg.setBackgroundColor(p.secondary_bg_color));
  }
  if (tgAtLeast('7.10') && (p.section_bg_color || p.bg_color)) tgSafe(() => tg.setBottomBarColor(p.section_bg_color || p.bg_color));
}

const hapticMap = { tap: ['impact', 'light'], pick: ['selection'], good: ['notify', 'success'], bad: ['notify', 'error'], warn: ['notify', 'warning'] };
function haptic(kind) {
  if (!tgAtLeast('6.1') || !tg.HapticFeedback) return;
  const [type, style] = hapticMap[kind] || hapticMap.tap;
  tgSafe(() => {
    if (type === 'impact') tg.HapticFeedback.impactOccurred(style);
    else if (type === 'notify') tg.HapticFeedback.notificationOccurred(style);
    else tg.HapticFeedback.selectionChanged();
  });
}

function askConfirm(message, onYes, onNo) {
  const done = ok => { if (ok) onYes(); else if (onNo) onNo(); };
  if (tgAtLeast('6.2')) {
    try { tg.showConfirm(message, done); return; }
    catch (e) { if (/PopupOpened/.test(e.message)) return; }
  }
  done(window.confirm(message));
}

// Phones open in full screen by default. Elsewhere it is the student's choice, and the choice is remembered.
const FULLSCREEN_KEY = 'fullscreen';
const PHONE_PLATFORMS = ['android', 'android_x', 'ios'];
let fullscreenTapped = false;

function onPhone() { return !!tg && PHONE_PLATFORMS.includes(tg.platform); }
function canFullscreen() { return tgAtLeast('8.0') || !!document.documentElement.requestFullscreen; }
function isFullscreen() { return !!(tg && tg.isFullscreen) || !!document.fullscreenElement; }
function wantsFullscreen() { return recall(FULLSCREEN_KEY) ?? onPhone(); }

function browserFullscreen(on) {
  const change = on ? document.documentElement.requestFullscreen?.() : document.exitFullscreen?.();
  change?.catch(() => toast("Bu qurilmada to'liq ekran ishlamaydi."));
}

function setFullscreen(on) {
  if (document.fullscreenElement) browserFullscreen(on);
  else if (tgAtLeast('8.0')) tgSafe(() => (on ? tg.requestFullscreen() : tg.exitFullscreen()));
  else browserFullscreen(on);
}

function fullscreenButton() {
  if (!canFullscreen()) return '';
  return `<button class="icon-btn" data-act="toggleFullscreen" aria-label="To'liq ekran">${icon(isFullscreen() ? 'shrink' : 'expand')}</button>`;
}

// A phone's exam screen is already full, so the button there would only take room from the title.
function examFullscreenButton() { return onPhone() ? '' : fullscreenButton(); }

function syncFullscreen() {
  const on = isFullscreen();
  document.querySelectorAll('[data-act="toggleFullscreen"]').forEach(el => {
    if (el.classList.contains('switch')) el.classList.toggle('on', on);
    else el.innerHTML = icon(on ? 'shrink' : 'expand');
  });
}

// Telegram refuses on some clients. A tap still counts as a user gesture, so the browser can take over.
function onFullscreenFailed(event) {
  if (event?.error === 'UNSUPPORTED' && fullscreenTapped) browserFullscreen(true);
  fullscreenTapped = false;
}

function setExamGuard(enabled) {
  if (!tgAtLeast('6.2')) return;
  tgSafe(() => (enabled ? tg.enableClosingConfirmation() : tg.disableClosingConfirmation()));
}

let toastTimer = null;
function toast(message) {
  document.querySelectorAll('.toast').forEach(el => el.remove());
  const el = document.createElement('div');
  el.className = 'toast';
  el.textContent = message;
  document.body.appendChild(el);
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.remove(), 2600);
}

function store(key, value) {
  try {
    if (value === undefined) localStorage.removeItem(key);
    else localStorage.setItem(key, JSON.stringify(value));
  } catch (e) {}
}

function recall(key) {
  try { return JSON.parse(localStorage.getItem(key)); } catch (e) { return null; }
}

class ApiError extends Error {
  constructor(code, status, data = {}) { super(code); this.code = code; this.status = status; this.data = data; }
}

// The server refuses students who have not joined the channel yet. Their results wait in the queue.
const CHANNEL_FALLBACK = 'https://t.me/ieltssat_daily';
const isQueueable = (e) => e.code === 'network' || e.status === 401 || e.code === 'not_subscribed';

async function api(path, options = {}) {
  if (!hasTelegramUser) throw new ApiError('no_user', 0);
  let response;
  try {
    response = await fetch(`/api/v1/${path}`, {
      method: options.method || 'GET',
      headers: { 'X-Telegram-Init-Data': tg.initData, 'Content-Type': 'application/json' },
      body: options.body ? JSON.stringify(options.body) : undefined,
    });
  } catch (e) {
    throw new ApiError('network', 0);
  }
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new ApiError(data.error || 'server_error', response.status, data);
  return data;
}

async function loadData(name) {
  if (!dataCache[name]) {
    const version = (window.DATA_VERSIONS || {})[name] || '';
    dataCache[name] = fetch(`/static/data/${name}?v=${version}`).then(r => {
      if (!r.ok) throw new Error(name);
      return r.json();
    }).catch(e => { delete dataCache[name]; throw e; });
  }
  return dataCache[name];
}

async function satBank() {
  if (!App.bank) {
    const list = await loadData('sat_bank.json');
    App.bank = Object.fromEntries(list.map(q => [q.id, q]));
  }
  return App.bank;
}

// Finished tests survive a lost connection: they wait here and go out on the next launch.
const QUEUE_KEY = 'pending_attempts';
async function submitAttempt(body) {
  try {
    return await api('attempts', { method: 'POST', body });
  } catch (e) {
    if (isQueueable(e)) {
      store(QUEUE_KEY, [...(recall(QUEUE_KEY) || []), body]);
      const messages = {
        network: "Internet yo'q. Natija saqlab qo'yildi va keyinroq yuboriladi.",
        not_subscribed: "Natija saqlandi. Kanalga obuna bo'lgach, Mini App'ni qayta oching.",
      };
      toast(messages[e.code] || "Sessiya eskirdi. Natija saqlandi, Mini App'ni qayta oching.");
    }
    return null;
  }
}

async function flushQueue() {
  const pending = recall(QUEUE_KEY) || [];
  if (!pending.length) return;
  const remaining = [];
  for (const body of pending) {
    try { await api('attempts', { method: 'POST', body }); }
    catch (e) { if (isQueueable(e)) remaining.push(body); }
  }
  store(QUEUE_KEY, remaining.length ? remaining : undefined);
}

async function refreshBoot() {
  if (!hasTelegramUser) return null;
  try {
    App.boot = await api('bootstrap');
    App.gate = null;
  } catch (e) {
    if (e.code === 'not_subscribed') App.gate = { channel: (e.data && e.data.channel) || CHANNEL_FALLBACK };
    else console.warn('bootstrap', e);
  }
  return App.boot;
}

// Navigation. Views are { render(params), mount(root, params), tab, full }.
function current() { return stack[stack.length - 1]; }

function updateChrome() {
  const entry = current();
  const view = entry && views[entry.name];
  const bar = document.getElementById('tabbar');
  bar.hidden = !view || !!view.full;
  bar.querySelectorAll('button').forEach(b => b.classList.toggle('on', !!view && b.dataset.tab === view.tab));
  if (tgAtLeast('6.1')) {
    const canGoBack = stack.length > 1 || !!document.querySelector('#overlay .sheet');
    tgSafe(() => (canGoBack ? tg.BackButton.show() : tg.BackButton.hide()));
  }
}

async function draw() {
  const entry = current();
  const view = views[entry.name];
  const root = document.getElementById('app');
  const html = await view.render(entry.params);
  if (current() !== entry) return;
  root.innerHTML = html;
  typeset(root);
  if (view.mount) await view.mount(root, entry.params);
  updateChrome();
}

async function open(name, params = {}, options = {}) {
  if (views[current()?.name]?.leave) views[current().name].leave();
  if (options.replace) stack.pop();
  if (options.reset) stack.length = 0;
  stack.push({ name, params });
  window.scrollTo(0, 0);
  await draw();
}

function goBack() {
  if (closeSheet()) return;
  const view = views[current()?.name];
  if (view && view.onBack) { view.onBack(); return; }
  leaveView();
}

function leaveView() {
  if (stack.length <= 1) return;
  views[current().name].leave?.();
  stack.pop();
  window.scrollTo(0, 0);
  draw();
}

function sheet(html) {
  const overlay = document.getElementById('overlay');
  overlay.innerHTML = `<div class="scrim" data-act="closeSheet"></div><div class="sheet"><div class="grabber"></div>${html}</div>`;
  typeset(overlay);
  updateChrome();
  return overlay.querySelector('.sheet');
}

function closeSheet() {
  const overlay = document.getElementById('overlay');
  if (!overlay.firstChild) return false;
  overlay.innerHTML = '';
  updateChrome();
  return true;
}

function loadingCards(count = 3) {
  return `<div class="page stack">${'<div class="skeleton"></div>'.repeat(count)}</div>`;
}

function shareLink(url, text) {
  const link = `https://t.me/share/url?url=${encodeURIComponent(url)}&text=${encodeURIComponent(text)}`;
  if (tgAtLeast('6.1')) tgSafe(() => tg.openTelegramLink(link));
  else window.open(link, '_blank');
}

function externalLink(url) {
  if (tg && tg.openLink) tgSafe(() => tg.openLink(url));
  else window.open(url, '_blank');
}

function track(name, meta) {
  if (hasTelegramUser) api('events', { method: 'POST', body: { name, meta } }).catch(() => {});
}

Object.assign(actions, {
  tab(el) {
    haptic('pick');
    open(el.dataset.tab, {}, { reset: true });
  },
  closeSheet() { closeSheet(); },
  back() { goBack(); },
  toggleFullscreen() {
    const on = !isFullscreen();
    store(FULLSCREEN_KEY, on);
    fullscreenTapped = on;
    haptic('tap');
    setFullscreen(on);
  },
  open(el) { open(el.dataset.view, { ...el.dataset }); },
});

document.addEventListener('click', event => {
  const el = event.target.closest('[data-act]');
  if (!el) return;
  const handler = actions[el.dataset.act];
  if (handler) handler(el, event);
});

function startTelegram() {
  applyTheme();
  document.addEventListener('fullscreenchange', syncFullscreen);
  if (!tg) return;
  tgSafe(() => tg.ready());
  tgSafe(() => tg.expand());
  if (tgAtLeast('7.7')) tgSafe(() => tg.disableVerticalSwipes());
  tgSafe(() => tg.onEvent('fullscreenChanged', syncFullscreen));
  tgSafe(() => tg.onEvent('fullscreenFailed', onFullscreenFailed));
  if (tgAtLeast('8.0') && wantsFullscreen()) tgSafe(() => tg.requestFullscreen());
  tgSafe(() => tg.onEvent('themeChanged', applyTheme));
  if (tgAtLeast('6.1')) tgSafe(() => tg.BackButton.onClick(goBack));
}
