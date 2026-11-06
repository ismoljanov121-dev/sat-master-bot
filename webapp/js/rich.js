'use strict';
// Formulas (KaTeX, loaded on first use) and SVG figures for questions.

const FORMULA = /\\\((.+?)\\\)/gs;
const KATEX_VERSION = '0.16.22';
let katexLoading = null;

function rich(text) {
  return String(text == null ? '' : text).split(FORMULA).map((part, index) => (
    index % 2 ? `<span class="m" data-tex="${esc(part)}">${esc(part)}</span>` : esc(part)
  )).join('');
}

function loadKatex() {
  if (window.katex) return Promise.resolve();
  if (!katexLoading) {
    katexLoading = new Promise((resolve, reject) => {
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = `/static/vendor/katex/katex.min.css?v=${KATEX_VERSION}`;
      document.head.appendChild(link);
      const script = document.createElement('script');
      script.src = `/static/vendor/katex/katex.min.js?v=${KATEX_VERSION}`;
      script.onload = resolve;
      script.onerror = () => { katexLoading = null; reject(new Error('katex')); };
      document.head.appendChild(script);
    });
  }
  return katexLoading;
}

async function typeset(root) {
  const nodes = [...root.querySelectorAll('.m[data-tex]')];
  if (!nodes.length) return;
  try { await loadKatex(); } catch (e) { return; }
  nodes.forEach(node => {
    if (!node.dataset.tex) return;
    window.katex.render(node.dataset.tex, node, { throwOnError: false });
    node.removeAttribute('data-tex');
  });
}

function niceStep(range, ticks = 5) {
  const rough = range / ticks;
  const power = 10 ** Math.floor(Math.log10(rough));
  const unit = rough / power;
  return (unit <= 1 ? 1 : unit <= 2 ? 2 : unit <= 5 ? 5 : 10) * power;
}

function plotFigure(fig) {
  const size = 340, pad = 18;
  const [x0, x1] = fig.xr, [y0, y1] = fig.yr;
  const sx = x => pad + (x - x0) / (x1 - x0) * (size - 2 * pad);
  const sy = y => size - pad - (y - y0) / (y1 - y0) * (size - 2 * pad);
  let grid = '', labels = '';
  for (let x = Math.ceil(x0); x <= x1; x++) {
    grid += `<line class="fig-grid" x1="${sx(x)}" y1="${sy(y0)}" x2="${sx(x)}" y2="${sy(y1)}"/>`;
    if (x && x % 2 === 0) labels += `<text class="fig-small" x="${sx(x)}" y="${sy(0) + 15}" text-anchor="middle">${x}</text>`;
  }
  for (let y = Math.ceil(y0); y <= y1; y++) {
    grid += `<line class="fig-grid" x1="${sx(x0)}" y1="${sy(y)}" x2="${sx(x1)}" y2="${sy(y)}"/>`;
    if (y && y % 2 === 0) labels += `<text class="fig-small" x="${sx(0) - 7}" y="${sy(y) + 4}" text-anchor="end">${y}</text>`;
  }
  const curves = (fig.fn || []).map(fn => {
    const value = fn.k === 'line' ? x => fn.m * x + fn.b : x => fn.a * (x - fn.h) ** 2 + fn.v;
    const points = [];
    for (let x = x0; x <= x1 + 1e-9; x += 0.1) {
      const y = value(x);
      if (y >= y0 - 0.5 && y <= y1 + 0.5) points.push(`${sx(x).toFixed(1)},${sy(y).toFixed(1)}`);
    }
    return `<polyline class="fig-line" points="${points.join(' ')}"/>`;
  }).join('');
  const dots = (fig.pts || []).map(([x, y]) => `<circle class="fig-dot" cx="${sx(x)}" cy="${sy(y)}" r="4"/>`).join('');
  return `<svg viewBox="0 0 ${size} ${size}" role="img" aria-label="Koordinata tekisligidagi grafik">${grid}
    <line class="fig-axis" x1="${sx(x0)}" y1="${sy(0)}" x2="${sx(x1)}" y2="${sy(0)}"/>
    <line class="fig-axis" x1="${sx(0)}" y1="${sy(y0)}" x2="${sx(0)}" y2="${sy(y1)}"/>
    <text class="fig-text" x="${sx(x1) - 2}" y="${sy(0) - 7}" text-anchor="end">x</text>
    <text class="fig-text" x="${sx(0) + 8}" y="${sy(y1) + 13}">y</text>
    ${labels}${curves}${dots}</svg>`;
}

function chartFrame(fig, width, height, left, bottom) {
  const top = 12, right = 12;
  const [x0, x1] = fig.xr, [y0, y1] = fig.yr;
  const sx = x => left + (x - x0) / (x1 - x0) * (width - left - right);
  const sy = y => height - bottom - (y - y0) / (y1 - y0) * (height - bottom - top);
  let marks = '';
  const yStep = niceStep(y1 - y0);
  for (let y = 0; y <= y1; y += yStep) {
    marks += `<line class="fig-grid" x1="${left}" y1="${sy(y)}" x2="${width - right}" y2="${sy(y)}"/>`;
    marks += `<text class="fig-small" x="${left - 6}" y="${sy(y) + 4}" text-anchor="end">${y}</text>`;
  }
  return { sx, sy, marks, top, right };
}

function scatterFigure(fig) {
  const width = 360, height = 290, left = 44, bottom = 44;
  const { sx, sy, marks } = chartFrame(fig, width, height, left, bottom);
  const xStep = niceStep(fig.xr[1] - fig.xr[0], 6);
  let xMarks = '';
  for (let x = 0; x <= fig.xr[1]; x += xStep) {
    xMarks += `<text class="fig-small" x="${sx(x)}" y="${height - bottom + 16}" text-anchor="middle">${x}</text>`;
  }
  const dots = fig.pts.map(([x, y]) => `<circle class="fig-dot" cx="${sx(x)}" cy="${sy(y)}" r="4.5"/>`).join('');
  const [m, b] = fig.fit;
  const fit = `<line class="fig-line" x1="${sx(fig.xr[0])}" y1="${sy(m * fig.xr[0] + b)}" x2="${sx(fig.xr[1])}" y2="${sy(m * fig.xr[1] + b)}"/>`;
  return `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Nuqtali diagramma">${marks}${xMarks}
    <line class="fig-axis" x1="${left}" y1="${height - bottom}" x2="${width - 12}" y2="${height - bottom}"/>
    <line class="fig-axis" x1="${left}" y1="12" x2="${left}" y2="${height - bottom}"/>
    ${fit}${dots}
    <text class="fig-small" x="${(width + left) / 2}" y="${height - 8}" text-anchor="middle">${esc(fig.xl)}</text>
    <text class="fig-small" transform="translate(12 ${(height - bottom) / 2}) rotate(-90)" text-anchor="middle">${esc(fig.yl)}</text></svg>`;
}

function barFigure(fig) {
  const width = 360, height = 270, left = 44, bottom = 34;
  const top = Math.max(...fig.vals) * 1.15;
  const { sy, marks } = chartFrame({ xr: [0, 1], yr: [0, top] }, width, height, left, bottom);
  const slot = (width - left - 12) / fig.vals.length;
  const bars = fig.vals.map((value, i) => {
    const x = left + slot * i + slot * 0.18;
    return `<rect class="fig-bar" x="${x}" y="${sy(value)}" width="${slot * 0.64}" height="${sy(0) - sy(value)}" rx="3"/>
      <text class="fig-small" x="${x + slot * 0.32}" y="${height - bottom + 16}" text-anchor="middle">${esc(fig.labels[i])}</text>`;
  }).join('');
  return `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Ustunli diagramma">${marks}${bars}
    <line class="fig-axis" x1="${left}" y1="${sy(0)}" x2="${width - 12}" y2="${sy(0)}"/>
    <text class="fig-small" transform="translate(12 ${(height - bottom) / 2}) rotate(-90)" text-anchor="middle">${esc(fig.yl)}</text></svg>`;
}

function tableFigure(fig) {
  const head = fig.head.map(cell => `<th>${esc(cell)}</th>`).join('');
  const rows = fig.rows.map(row => `<tr>${row.map(cell => `<td class="num">${esc(cell)}</td>`).join('')}</tr>`).join('');
  return `<div class="table-wrap"><table class="data"><thead><tr>${head}</tr></thead><tbody>${rows}</tbody></table></div>`;
}

function triangleFigure(fig) {
  const width = 340, height = 250, pad = 38;
  const xs = fig.pts.map(p => p[0]), ys = fig.pts.map(p => p[1]);
  const minX = Math.min(...xs), maxX = Math.max(...xs), minY = Math.min(...ys), maxY = Math.max(...ys);
  const scale = Math.min((width - 2 * pad) / (maxX - minX), (height - 2 * pad) / (maxY - minY));
  const offX = (width - (maxX - minX) * scale) / 2, offY = (height - (maxY - minY) * scale) / 2;
  const pts = fig.pts.map(([x, y]) => [offX + (x - minX) * scale, height - offY - (y - minY) * scale]);
  const cx = pts.reduce((sum, p) => sum + p[0], 0) / 3, cy = pts.reduce((sum, p) => sum + p[1], 0) / 3;
  const toward = (p, distance) => {
    const dx = cx - p[0], dy = cy - p[1], length = Math.hypot(dx, dy);
    return [p[0] + dx / length * distance, p[1] + dy / length * distance];
  };
  let labels = (fig.ang || []).map((text, i) => {
    const [x, y] = toward(pts[i], 34);
    return text ? `<text class="fig-text" x="${x}" y="${y + 5}" text-anchor="middle">${esc(text)}</text>` : '';
  }).join('');
  labels += (fig.sides || []).map((text, i) => {
    if (!text) return '';
    const a = pts[i], b = pts[(i + 1) % 3];
    const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2;
    const dx = mx - cx, dy = my - cy, length = Math.hypot(dx, dy) || 1;
    return `<text class="fig-text" x="${mx + dx / length * 16}" y="${my + dy / length * 16 + 5}" text-anchor="middle">${esc(text)}</text>`;
  }).join('');
  let corner = '';
  if (fig.right !== undefined) {
    const p = pts[fig.right], a = pts[(fig.right + 1) % 3], b = pts[(fig.right + 2) % 3];
    const unit = (from, to, length) => {
      const d = Math.hypot(to[0] - from[0], to[1] - from[1]);
      return [(to[0] - from[0]) / d * length, (to[1] - from[1]) / d * length];
    };
    const [ax, ay] = unit(p, a, 14), [bx, by] = unit(p, b, 14);
    corner = `<path class="fig-thin" d="M${p[0] + ax} ${p[1] + ay} L${p[0] + ax + bx} ${p[1] + ay + by} L${p[0] + bx} ${p[1] + by}"/>`;
  }
  return `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Uchburchak">
    <polygon class="fig-shape" points="${pts.map(p => p.join(',')).join(' ')}"/>${corner}${labels}</svg>`;
}

function circleFigure(fig) {
  const size = 260, c = size / 2, r = 92;
  const point = deg => [c + r * Math.cos(deg * Math.PI / 180), c - r * Math.sin(deg * Math.PI / 180)];
  let extra;
  if (fig.arc) {
    const [ax, ay] = point(0), [bx, by] = point(fig.arc);
    const large = fig.arc > 180 ? 1 : 0;
    extra = `<path class="fig-thin" d="M${c} ${c} L${ax} ${ay}"/><path class="fig-thin" d="M${c} ${c} L${bx} ${by}"/>
      <path class="fig-line" d="M${ax} ${ay} A${r} ${r} 0 ${large} 0 ${bx} ${by}"/>
      <text class="fig-text" x="${c + 26}" y="${c - 8}">${fig.arc}°</text>
      <text class="fig-text" x="${(c + ax) / 2}" y="${c + 18}" text-anchor="middle">${esc(fig.r)}</text>`;
  } else {
    const [ax, ay] = point(20);
    extra = `<path class="fig-thin" d="M${c} ${c} L${ax} ${ay}"/>
      <text class="fig-text" x="${(c + ax) / 2}" y="${(c + ay) / 2 - 8}" text-anchor="middle">${esc(fig.r)}</text>`;
  }
  return `<svg viewBox="0 0 ${size} ${size}" role="img" aria-label="Aylana">
    <circle class="fig-shape" cx="${c}" cy="${c}" r="${r}"/>${extra}
    <circle class="fig-dot" cx="${c}" cy="${c}" r="3.500"/>
    <text class="fig-text" x="${c - 14}" y="${c + 5}">${esc(fig.center || '')}</text></svg>`;
}

function rectFigure(fig) {
  const width = 340, height = 230, pad = 40;
  const scale = Math.min((width - 2 * pad) / fig.w, (height - 2 * pad) / fig.h);
  const w = fig.w * scale, h = fig.h * scale, cut = fig.cut * scale;
  const x = (width - w) / 2, y = (height - h) / 2;
  const path = `M${x} ${y} H${x + w - cut} V${y + cut} H${x + w} V${y + h} H${x} Z`;
  return `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Shakl">
    <path class="fig-shape" d="${path}"/>
    <text class="fig-text" x="${x + w / 2}" y="${y + h + 22}" text-anchor="middle">${fig.w}</text>
    <text class="fig-text" x="${x - 12}" y="${y + h / 2 + 5}" text-anchor="end">${fig.h}</text>
    <text class="fig-text" x="${x + w - cut / 2}" y="${y - 6}" text-anchor="middle">${fig.cut}</text></svg>`;
}

function parallelFigure(fig) {
  return `<svg viewBox="0 0 340 210" role="img" aria-label="Parallel to'g'ri chiziqlar">
    <line class="fig-thin" x1="26" y1="62" x2="314" y2="62"/><line class="fig-thin" x1="26" y1="150" x2="314" y2="150"/>
    <line class="fig-line" x1="118" y1="194" x2="222" y2="18"/>
    <text class="fig-text" x="318" y="58" text-anchor="end">m</text><text class="fig-text" x="318" y="146" text-anchor="end">n</text>
    <text class="fig-text" x="205" y="84">${esc(fig.a)}</text><text class="fig-text" x="160" y="140">${esc(fig.b)}</text></svg>`;
}

const FIGURES = {
  plot: plotFigure, scatter: scatterFigure, bar: barFigure, table: tableFigure,
  tri: triangleFigure, circle: circleFigure, rect: rectFigure, parallel: parallelFigure,
};

function figureHTML(fig) {
  if (!fig || !FIGURES[fig.t]) return '';
  return `<div class="figure">${FIGURES[fig.t](fig)}</div>`;
}
