'use strict';
// IELTS Task 1 visuals: line graphs, bar charts, pie charts, tables, flow charts and maps. The AI gets the same data.

const VIZ_SLOTS = 5;
const VIZ_CHAR = 6.4;
const VIZ_NOTE = "Ma'lumotlar mashq uchun tuzilgan, real statistika emas.";

function vizSlot(index) { return `k${index % VIZ_SLOTS + 1}`; }
function vizNumber(value) { return String(Number(value.toFixed(4))); }

function vizLegend(names, shape) {
  if (names.length < 2) return '';
  return `<div class="viz-legend">${names.map((name, index) => `<span><i class="viz-key ${shape} ${vizSlot(index)}"></i>${esc(name)}</span>`).join('')}</div>`;
}

// The scale always starts at a round number and includes every value, so the axis can be read off directly.
function vizScale(part, values) {
  const floor = part.min ?? 0;
  const step = niceStep(Math.max(...values) - floor, 5);
  const top = Math.ceil(Math.max(...values) / step) * step;
  const ticks = [];
  for (let value = floor; value <= top + step / 1000; value += step) ticks.push(Number(value.toFixed(6)));
  return { floor, top, ticks };
}

function vizGrid(frame) {
  return frame.ticks.map(value => `<line class="fig-grid" x1="${frame.left}" y1="${frame.y(value)}" x2="${frame.width - frame.right}" y2="${frame.y(value)}"/>
    <text class="fig-small" x="${frame.left - 6}" y="${frame.y(value) + 4}" text-anchor="end">${vizNumber(value)}</text>`).join('');
}

function vizFrame(part) {
  const width = 360, height = 240, top = 12, left = 40;
  const line = part.kind === 'line';
  const totals = line || !part.stacked
    ? part.series.flatMap(item => item.values)
    : part.categories.map((_, index) => part.series.reduce((sum, item) => sum + item.values[index], 0));
  const scale = vizScale(part, totals);
  const longest = Math.max(...part.series.map(item => item.name.length));
  const direct = line && part.series.length > 1 && part.series.length <= 4 && longest <= 13;
  // Long category names that would touch their neighbours go on two alternating rows.
  const word = line ? 0 : Math.max(...part.categories.flatMap(name => name.split(' ').map(piece => piece.length)));
  const stagger = !line && word * VIZ_CHAR > (width - left - 12) / part.categories.length;
  const right = direct ? 12 + longest * 6.6 : stagger ? 30 : 12;
  const bottom = line ? 26 : 38;
  const y = value => height - bottom - (value - scale.floor) / (scale.top - scale.floor) * (height - bottom - top);
  const frame = { ...scale, width, height, top, left, right, bottom, y, direct, stagger };
  if (line) {
    const [first, last] = [part.x[0], part.x[part.x.length - 1]];
    frame.points = part.x.map(value => left + 6 + (value - first) / (last - first) * (width - left - right - 12));
  } else {
    const slot = (width - left - right) / part.categories.length;
    frame.slot = slot;
    frame.points = part.categories.map((_, index) => left + slot * (index + 0.5));
  }
  return frame;
}

function vizLine(part, index) {
  const frame = vizFrame(part);
  const lines = part.series.map((item, position) => {
    const points = item.values.map((value, at) => `${frame.points[at].toFixed(1)},${frame.y(value).toFixed(1)}`).join(' ');
    const dots = item.values.map((value, at) => `<circle class="viz-dot ${vizSlot(position)}" cx="${frame.points[at].toFixed(1)}" cy="${frame.y(value).toFixed(1)}" r="4"/>`).join('');
    return `<polyline class="viz-line ${vizSlot(position)}" points="${points}"/>${dots}`;
  }).join('');
  const ends = part.series.map(item => ({ name: item.name, y: frame.y(item.values[item.values.length - 1]) })).sort((a, b) => a.y - b.y);
  const roomy = ends.every((end, at) => !at || end.y - ends[at - 1].y >= 14);
  const labels = frame.direct && roomy ? ends.map(end => (
    `<text class="fig-small" x="${frame.points[frame.points.length - 1] + 9}" y="${end.y + 4}">${esc(end.name)}</text>`
  )).join('') : '';
  const ticks = part.x.map((value, at) => (
    `<text class="fig-small" x="${frame.points[at].toFixed(1)}" y="${frame.height - 8}" text-anchor="middle">${esc(value)}</text>`
  )).join('');
  return `<div class="figure viz-figure">${vizLegend(part.series.map(item => item.name), 'line')}
    <svg class="viz-plot" data-part="${index}" tabindex="0" viewBox="0 0 ${frame.width} ${frame.height}" role="img" aria-label="${esc(part.title)}">
      ${vizGrid(frame)}<line class="fig-axis" x1="${frame.left}" y1="${frame.y(frame.floor)}" x2="${frame.width - frame.right}" y2="${frame.y(frame.floor)}"/>
      <line class="viz-cross" hidden y1="${frame.top}" y2="${frame.y(frame.floor)}"/>${lines}${labels}${ticks}</svg>
    <div class="viz-readout small muted">Qiymatni ko'rish uchun grafikka bosing.</div></div>`;
}

// Square at the baseline, 4px round at the data end.
function vizColumn(x, y, width, height, className, round) {
  const r = Math.min(4, width / 2, height);
  const path = round
    ? `M${x} ${y + height}V${y + r}Q${x} ${y} ${x + r} ${y}H${x + width - r}Q${x + width} ${y} ${x + width} ${y + r}V${y + height}Z`
    : `M${x} ${y + height}V${y}H${x + width}V${y + height}Z`;
  return `<path class="viz-fill ${className}" d="${path}"/>`;
}

function vizCategoryLabel(text, x, y) {
  const lines = text.includes(' ') ? text.split(' ') : [text];
  return `<text class="fig-small" text-anchor="middle" y="${y}">${lines.map((line, index) => (
    `<tspan x="${x}" dy="${index ? 13 : 0}">${esc(line)}</tspan>`
  )).join('')}</text>`;
}

function vizBar(part, index) {
  const frame = vizFrame(part);
  const single = part.series.length === 1;
  const groups = part.categories.map((category, at) => {
    const center = frame.points[at];
    let marks = '';
    if (part.stacked) {
      const width = Math.min(24, frame.slot * 0.6);
      let base = 0;
      const last = part.series.reduce((found, item, position) => (item.values[at] > 0 ? position : found), 0);
      part.series.forEach((item, position) => {
        const value = item.values[at];
        if (!value) return;
        const top = frame.y(base + value), bottom = frame.y(base);
        marks += vizColumn(center - width / 2, top, width, Math.max(0.5, bottom - top - (base ? 2 : 0)), vizSlot(position), position === last);
        base += value;
      });
      marks += `<text class="fig-small strong" x="${center}" y="${frame.y(base) - 5}" text-anchor="middle">${vizNumber(base)}</text>`;
    } else {
      const gap = 2;
      const width = Math.min(24, (frame.slot * 0.84 - gap * (part.series.length - 1)) / part.series.length);
      const span = width * part.series.length + gap * (part.series.length - 1);
      part.series.forEach((item, position) => {
        const value = item.values[at];
        const x = center - span / 2 + position * (width + gap);
        marks += vizColumn(x, frame.y(value), width, frame.y(0) - frame.y(value), vizSlot(position), true);
        if (single) marks += `<text class="fig-small strong" x="${x + width / 2}" y="${frame.y(value) - 5}" text-anchor="middle">${vizNumber(value)}</text>`;
      });
    }
    return marks + vizCategoryLabel(category, center, frame.height - frame.bottom + 16 + (frame.stagger && at % 2 ? 13 : 0));
  }).join('');
  return `<div class="figure viz-figure">${vizLegend(part.series.map(item => item.name), 'box')}
    <svg class="viz-plot" data-part="${index}" tabindex="0" viewBox="0 0 ${frame.width} ${frame.height}" role="img" aria-label="${esc(part.title)}">
      ${vizGrid(frame)}<line class="fig-axis" x1="${frame.left}" y1="${frame.y(frame.floor)}" x2="${frame.width - frame.right}" y2="${frame.y(frame.floor)}"/>
      <line class="viz-cross" hidden y1="${frame.top}" y2="${frame.y(frame.floor)}"/>${groups}</svg>
    <div class="viz-readout small muted">Qiymatni ko'rish uchun diagrammaga bosing.</div></div>`;
}

// Labels sit outside the slices. On each side they are pushed apart, so small neighbouring slices stay readable.
function vizPieLabels(labels, height) {
  ['left', 'right'].forEach(side => {
    const group = labels.filter(item => item.side === side).sort((a, b) => a.y - b.y);
    group.forEach((item, at) => { if (at && item.y - group[at - 1].y < 16) item.y = group[at - 1].y + 16; });
    const overflow = group.length ? group[group.length - 1].y - (height - 8) : 0;
    if (overflow > 0) group.forEach(item => { item.y -= overflow; });
  });
}

function vizPie(part) {
  const width = 360, height = 216, cy = 108, labelGap = 16;
  const total = part.slices.reduce((sum, slice) => sum + slice.value, 0);
  let start = -Math.PI / 2;
  const wedges = part.slices.map(slice => {
    const sweep = slice.value / total * Math.PI * 2;
    const wedge = { start, end: start + sweep, middle: start + sweep / 2, large: sweep > Math.PI ? 1 : 0, text: `${slice.name} ${slice.value}%` };
    start += sweep;
    return { ...wedge, side: Math.cos(wedge.middle) >= 0 ? 'right' : 'left' };
  });
  // The pie moves over and shrinks if it must, because a label is never allowed to run off the edge.
  const room = side => Math.max(0, ...wedges.filter(item => item.side === side).map(item => item.text.length * VIZ_CHAR));
  const leftRoom = room('left'), rightRoom = room('right');
  const radius = Math.min(74, (width - leftRoom - rightRoom - 2 * labelGap - 16) / 2);
  const cx = leftRoom + labelGap + radius + (width - leftRoom - rightRoom - 2 * labelGap - 2 * radius) / 2;
  const labels = [];
  const slices = wedges.map((item, position) => {
    const point = (value, r) => [cx + r * Math.cos(value), cy + r * Math.sin(value)];
    const [x1, y1] = point(item.start, radius), [x2, y2] = point(item.end, radius);
    const [ax, ay] = point(item.middle, radius + 2), [bx, by] = point(item.middle, radius + 12);
    labels.push({ ax, ay, bx, y: by + 4, side: item.side, text: item.text });
    return `<path class="viz-slice ${vizSlot(position)}" d="M${cx.toFixed(2)} ${cy}L${x1.toFixed(2)} ${y1.toFixed(2)}A${radius} ${radius} 0 ${item.large} 1 ${x2.toFixed(2)} ${y2.toFixed(2)}Z"/>`;
  }).join('');
  vizPieLabels(labels, height);
  const texts = labels.map(item => {
    const x = item.side === 'right' ? cx + radius + labelGap : cx - radius - labelGap;
    return `<path class="viz-leader" d="M${item.ax.toFixed(1)} ${item.ay.toFixed(1)}L${(item.side === 'right' ? x - 3 : x + 3).toFixed(1)} ${(item.y - 4).toFixed(1)}"/>
      <text class="fig-small strong" x="${x.toFixed(1)}" y="${item.y.toFixed(1)}" text-anchor="${item.side === 'right' ? 'start' : 'end'}">${esc(item.text)}</text>`;
  }).join('');
  return `<div class="figure viz-figure"><svg viewBox="0 0 ${width} ${height}" role="img" aria-label="${esc(part.title)}">${slices}${texts}</svg></div>`;
}

function vizTable(part) {
  return `<div class="figure viz-figure"><div class="table-wrap"><table class="data viz-data"><thead><tr>${part.head.map(cell => `<th>${esc(cell)}</th>`).join('')}</tr></thead>
    <tbody>${part.rows.map(row => `<tr>${row.map((cell, at) => `<td class="${at ? 'num' : ''}">${esc(cell)}</td>`).join('')}</tr>`).join('')}</tbody></table></div></div>`;
}

function vizStep(step) {
  return `<div class="flow-step"><div class="h3">${esc(step.label)}</div>${step.note ? `<div class="small muted">${esc(step.note)}</div>` : ''}</div>`;
}

function vizSteps(steps) { return steps.map(vizStep).join('<div class="flow-arrow"></div>'); }

function vizFlow(part) {
  const branches = part.branches ? `<div class="flow-arrow"></div><div class="flow-split">${part.branches.map(branch => `<div class="flow-path">
      <div class="eyebrow center">${esc(branch.name)}</div>${vizSteps(branch.steps)}</div>`).join('')}</div>` : '';
  const after = part.after ? `<div class="flow-arrow"></div>${vizSteps(part.after)}` : '';
  const loop = part.loop ? `<div class="flow-loop small muted">${icon('repeat', true)}<span>${esc(part.loop)}</span></div>` : '';
  return `<div class="figure viz-figure flow">${vizSteps(part.steps)}${branches}${after}${loop}</div>`;
}

function vizMapText(text, x, y, className = 'viz-map-text') {
  const lines = text.split('|');
  return `<text class="${className}" text-anchor="middle" y="${y}">${lines.map((line, index) => (
    `<tspan x="${x}" dy="${index ? 13 : 0}">${esc(line)}</tspan>`
  )).join('')}</text>`;
}

const VIZ_MAP_ITEMS = {
  water: item => `<polygon class="viz-water" points="${item.points.map(p => p.join(',')).join(' ')}"/>
    ${item.label ? vizMapText(item.label, item.at[0], item.at[1], 'viz-map-text water') : ''}`,
  area(item) {
    const lines = item.label ? item.label.split('|').length : 0;
    return `<rect class="viz-area ${item.tone || ''}" x="${item.x}" y="${item.y}" width="${item.w}" height="${item.h}" rx="3"/>
      ${item.label ? vizMapText(item.label, item.x + item.w / 2, item.y + item.h / 2 + 4 - (lines - 1) * 6.5) : ''}`;
  },
  road: item => `<polyline class="viz-road ${item.thin ? 'thin' : ''}" points="${item.points.map(p => p.join(',')).join(' ')}"/>
    ${item.label ? vizMapText(item.label, item.at[0], item.at[1], 'viz-map-text small') : ''}`,
  rail: item => `<polyline class="viz-rail" points="${item.points.map(p => p.join(',')).join(' ')}"/>
    ${vizMapText(item.label, item.at[0], item.at[1], 'viz-map-text small')}`,
  route: item => `<polyline class="viz-route ${item.tone} ${item.tunnel ? 'tunnel' : ''}" points="${item.points.map(p => p.join(',')).join(' ')}"/>`,
  groyne: item => `<polyline class="viz-groyne" points="${item.points.map(p => p.join(',')).join(' ')}"/>`,
  wall: item => `<polyline class="viz-wall" points="${item.points.map(p => p.join(',')).join(' ')}"/>`,
  gate: item => `<polyline class="viz-gate" points="${item.points.map(p => p.join(',')).join(' ')}"/>`,
  dot: item => `<circle class="viz-pin" cx="${item.x}" cy="${item.y}" r="5"/>${vizMapText(item.label, item.x, item.y + 19)}`,
  text: item => vizMapText(item.label, item.x, item.y, 'viz-map-text small'),
};

function vizMap(part) {
  const width = 340, height = part.height || 220;
  const compass = `<g transform="translate(${width - 16} ${height - 22})"><path class="viz-compass" d="M0 -11L5 3H-5Z"/><text class="viz-map-text small" text-anchor="middle" y="14">N</text></g>`;
  return `<div class="figure viz-figure"><svg viewBox="0 0 ${width} ${height}" role="img" aria-label="${esc(part.facts)}">
    <rect class="viz-land" width="${width}" height="${height}"/>${part.items.map(item => VIZ_MAP_ITEMS[item.t](item)).join('')}${compass}</svg></div>`;
}

const VIZ_KINDS = { line: vizLine, bar: vizBar, pie: vizPie, table: vizTable, flow: vizFlow, map: vizMap };

// The same numbers as a table, for screen readers and for anyone who cannot tell the colors apart.
function vizDataTable(part) {
  let head, rows;
  if (part.kind === 'line' || part.kind === 'bar') {
    const labels = part.kind === 'line' ? part.x : part.categories;
    head = ['', ...part.series.map(item => item.name)];
    rows = labels.map((label, at) => [label, ...part.series.map(item => vizNumber(item.values[at]))]);
  } else if (part.kind === 'pie') {
    head = ['', '%'];
    rows = part.slices.map(slice => [slice.name, slice.value]);
  } else {
    return '';
  }
  return `<details class="viz-details"><summary class="small muted">Raqamlar jadvali</summary><div class="table-wrap"><table class="data viz-data">
    <thead><tr>${head.map(cell => `<th>${esc(cell)}</th>`).join('')}</tr></thead>
    <tbody>${rows.map(row => `<tr>${row.map((cell, at) => `<td class="${at ? 'num' : ''}">${esc(cell)}</td>`).join('')}</tr>`).join('')}</tbody></table></div></details>`;
}

function visualHTML(visual) {
  if (!visual) return '';
  const parts = visual.parts.map((part, index) => `<figure class="viz-part"><figcaption class="h3">${esc(part.title)}</figcaption>
    ${VIZ_KINDS[part.kind](part, index)}${vizDataTable(part)}</figure>`).join('');
  return `<div class="viz">${parts}<p class="small muted">${VIZ_NOTE}</p></div>`;
}

function vizShowValues(svg, part, frame, at) {
  const cross = svg.querySelector('.viz-cross');
  cross.removeAttribute('hidden');
  cross.setAttribute('x1', frame.points[at]);
  cross.setAttribute('x2', frame.points[at]);
  const box = svg.parentElement.querySelector('.viz-readout');
  box.textContent = '';
  const label = part.kind === 'line' ? part.x[at] : part.categories[at];
  const head = document.createElement('b');
  head.textContent = String(label);
  box.append(head);
  part.series.forEach((item, position) => {
    const row = document.createElement('span');
    const key = document.createElement('i');
    key.className = `viz-key line ${vizSlot(position)}`;
    const value = document.createElement('b');
    value.textContent = vizNumber(item.values[at]);
    row.append(key, value, ` ${part.series.length > 1 ? item.name : ''}`);
    box.append(row);
  });
  svg.dataset.at = at;
}

// A tap or a hover picks the nearest position, and the arrow keys walk through the same positions.
function mountVisual(root, visual) {
  if (!visual) return;
  root.querySelectorAll('.viz-plot').forEach(svg => {
    const part = visual.parts[Number(svg.dataset.part)];
    const frame = vizFrame(part);
    const pick = event => {
      const rect = svg.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width * frame.width;
      let nearest = 0;
      frame.points.forEach((point, at) => { if (Math.abs(point - x) < Math.abs(frame.points[nearest] - x)) nearest = at; });
      vizShowValues(svg, part, frame, nearest);
    };
    svg.addEventListener('pointerdown', pick);
    svg.addEventListener('pointermove', pick);
    svg.addEventListener('keydown', event => {
      const step = { ArrowRight: 1, ArrowLeft: -1 }[event.key];
      if (!step) return;
      event.preventDefault();
      const at = Math.min(frame.points.length - 1, Math.max(0, (svg.dataset.at ? Number(svg.dataset.at) : -step) + step));
      vizShowValues(svg, part, frame, at);
    });
  });
}
