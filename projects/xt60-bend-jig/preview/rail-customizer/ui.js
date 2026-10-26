(() => {
  'use strict';
  const G = globalThis.RailGeometry;
  const $ = id => document.getElementById(id);
  const key = 'xt60-rail-customizer/v1';
  let profile = G.defaults(), progress = 0, drag = null, playing = false;
  let frameRequest = 0, diagnosticTimer = 0, bound = 30;
  const scalarKeys = ['leftTravelDeg', 'rightTravelDeg', 'innerRadiusMm', 'outerRadiusMm', 'slotDiameterMm'];
  const fmt = n => n.toFixed(2);
  const status = message => { $('status').textContent = message; };
  function persist() {
    try { localStorage.setItem(key, JSON.stringify(profile)); }
    catch { status('Browser storage unavailable. Use Save JSON to keep your changes.'); }
  }
  try {
    const saved = localStorage.getItem(key);
    if (saved) { profile = G.validate(JSON.parse(saved)); $('profile-state').textContent = 'Restored browser profile'; }
  } catch { status('Stored profile unavailable or invalid. Recovered default loaded.'); }

  $('rod-controls').innerHTML = G.names.map((name, i) => `<fieldset class="rod"><legend><i class="swatch" style="background:${G.colors[i]}"></i>${name}</legend>${['open', 'end', 'bendMm'].map(endpoint => `<div class="endpoint-row"><span>${endpoint === 'bendMm' ? 'CURVE' : endpoint.toUpperCase()}</span>${['Y', 'Z'].map((axis, j) => `<label>${axis}<input type="number" step="0.01" min="-60" max="60" data-rod="${i}" data-endpoint="${endpoint}" data-axis="${j}" aria-label="${name} ${endpoint === 'bendMm' ? 'curve offset' : endpoint.toUpperCase()} ${axis}"></label>`).join('')}</div>`).join('')}</fieldset>`).join('');
  function syncInputs() {
    document.querySelectorAll('[data-rod]').forEach(input => { input.value = fmt(profile.rods[+input.dataset.rod][input.dataset.endpoint][+input.dataset.axis]); });
    scalarKeys.forEach(name => { $(name).value = profile[name]; });
    $('axle-note').textContent = `Rod stock Ø4 × 50 mm. Fixed axle at (${fmt(profile.axle[0])}, ${fmt(profile.axle[1])}), guide Ø${fmt(profile.axleGuideDiameterMm)} mm. Rotation center at (0, 0).`;
  }
  function changed() {
    $('profile-state').textContent = 'Edited profile · kinematic experiment';
    persist(); draw();
    clearTimeout(diagnosticTimer);
    diagnosticTimer = setTimeout(drawDiagnostics, 140);
  }
  document.querySelectorAll('[data-rod]').forEach(input => {
    input.addEventListener('change', () => {
      if (!input.checkValidity() || input.value === '' || !Number.isFinite(input.valueAsNumber)) { status('Hole coordinates must be numbers between −60 and 60 mm.'); syncInputs(); return; }
      stop(); profile.rods[+input.dataset.rod][input.dataset.endpoint][+input.dataset.axis] = input.valueAsNumber;
      status(''); changed();
    });
  });
  scalarKeys.forEach(name => {
    $(name).addEventListener('change', () => {
      const input = $(name);
      if (!input.checkValidity() || input.value === '' || !Number.isFinite(input.valueAsNumber)) { status(`Enter ${name} between ${input.min} and ${input.max}.`); syncInputs(); return; }
      stop(); profile[name] = input.valueAsNumber; status(''); changed();
    });
  });
  const circle = (p, r, extra) => `<circle cx="${p[0]}" cy="${-p[1]}" r="${r}" ${extra}/>`;
  function grid() {
    let result = '';
    for (let v = Math.ceil(-bound / 5) * 5; v <= bound; v += 5) {
      result += `<path d="M${v},${-bound}V${bound}M${-bound},${v}H${bound}" stroke="${v === 0 ? '#9aa698' : '#c8cdbf'}" stroke-width="${v === 0 ? 0.12 : 0.06}"/>`;
    }
    return result;
  }
  function backdrop(radius) {
    return `${grid()}<circle r="${radius}" fill="#f4f1e7" fill-opacity="0.8" stroke="#72816e" stroke-width="0.16"/><path d="M-0.7,0H0.7M0,-0.7V0.7" stroke="#586855" stroke-width=".15"/>`;
  }
  function railLayer(frame) {
    return G.paths(profile, frame).map((points, i) => `<path data-rail="${i}" d="${G.pathData(points)}" fill="none" stroke="${G.colors[i]}" stroke-width="${profile.slotDiameterMm}" stroke-linecap="round" stroke-linejoin="round" opacity="0.28"/><path d="${G.pathData(points)}" fill="none" stroke="${G.colors[i]}" stroke-width=".16" stroke-dasharray=".5 .4"/>${frame === 'inner' ? `<path data-line="${i}" d="${G.pathData(points)}" fill="none" stroke="transparent" stroke-width="${Math.max(4, profile.slotDiameterMm)}" stroke-linecap="round" pointer-events="stroke" tabindex="0" role="button" aria-label="Move entire ${G.names[i]} path. Arrow keys move 0.1 mm; Shift moves 1 mm."/>` : ''}`).join('');
  }
  function axleLayer(frame) {
    return `<g pointer-events="none"><path data-axle-rail d="${G.pathData(G.sample(u => G.axleLocal(profile, u, frame)))}" fill="none" stroke="#906cbe" stroke-width="${profile.axleGuideDiameterMm}" stroke-linecap="round" opacity=".22"/>${circle(G.axleLocal(profile, progress, frame), .75, 'fill="#75559e"')}<text class="svg-label" x="${G.axleLocal(profile, 0, frame)[0] - 2}" y="${-G.axleLocal(profile, 0, frame)[1] + 4.8}">fixed axle</text></g>`;
  }
  function rodMarkers(frame) {
    return profile.rods.map((rod, i) => circle(G.local(profile, rod, progress, frame), 2, `fill="#fffdf5" stroke="${G.colors[i]}" stroke-width=".5" pointer-events="none" data-current-rod="${i}"`)).join('');
  }
  function handles() {
    return profile.rods.map((rod, i) => {
      const separated = Math.hypot(rod.end[0] - rod.open[0], rod.end[1] - rod.open[1]) < 5;
      return ['open', 'end', 'curve'].map(kind => {
        const point = kind === 'curve' ? G.world(rod, .5) : rod[kind];
        const needsLeader = kind === 'curve' ? Math.min(...[rod.open, rod.end].map(p => Math.hypot(p[0] - point[0], p[1] - point[1]))) < 5 : separated;
        const anchor = needsLeader ? [point[0] + (kind === 'open' ? -4 : kind === 'end' ? 4 : 0), point[1] + (kind === 'curve' ? 5 : 0)] : point;
        const shape = kind === 'end' ? '<path d="M0,-1.3L1.3,0L0,1.3L-1.3,0Z"/>' : kind === 'curve' ? '<circle r=".8" stroke="#fffdf5" stroke-width=".3"/>' : '<circle r="1"/>';
        const label = kind === 'curve' ? 'curve dot' : `${kind.toUpperCase()} hole`;
        return `${needsLeader ? `<path d="M${point[0]},${-point[1]}L${anchor[0]},${-anchor[1]}" stroke="${G.colors[i]}" stroke-width=".15" stroke-dasharray=".4 .3" pointer-events="none"/>` : ''}<g transform="translate(${anchor[0]},${-anchor[1]})" data-handle="${i}" data-kind="${kind}" tabindex="0" role="button" aria-label="${rod.name} ${label}. Arrow keys move 0.1 mm; Shift moves 1 mm."><circle class="handle-target" r="2.6"/><g fill="${G.colors[i]}" stroke="${G.colors[i]}" stroke-width=".3">${shape}</g><text class="svg-label" x="${kind === 'open' && i === 0 ? -7 : 1.8}" y="${kind === 'end' ? 3.2 : -2}">${kind === 'open' ? rod.name + ' O' : kind === 'end' ? 'E' : 'curve'}</text></g>`;
      }).join('');
    }).join('');
  }
  function draw() {
    if (!drag) bound = G.viewBound(profile);
    for (const id of ['editor', 'left-view', 'right-view']) $(id).setAttribute('viewBox', `${-bound} ${-bound} ${bound * 2} ${bound * 2}`);
    $('editor').innerHTML = `${backdrop(profile.innerRadiusMm)}${railLayer('inner')}${axleLayer('inner')}${rodMarkers('inner')}${handles()}<text class="svg-label" x="${bound - 9}" y="-1">+Y →</text><text class="svg-label" x="1" y="${-bound + 3}">+Z ↑</text>`;
    for (const frame of ['left', 'right']) $(frame + '-view').innerHTML = `${backdrop(profile.outerRadiusMm)}${railLayer(frame)}${axleLayer(frame)}${rodMarkers(frame)}`;
    $('progress').value = Math.round(progress * 1000);
    const state = progress === 0 ? 'OPEN' : progress === 1 ? 'END' : progress === .5 ? 'MID' : 'TRAVEL';
    $('state-label').textContent = `${state} · ${Math.round(progress * 100)}%`;
    $('angles').textContent = `Left ${fmt(profile.leftTravelDeg * progress)}° · Right ${fmt(profile.rightTravelDeg * progress)}°`;
  }
  function drawDiagnostics() {
    const rows = ['inner', 'left', 'right'].map(frame => {
      const d = G.diagnostics(profile, frame);
      if (frame !== 'inner') $(frame + '-metrics').textContent = G.names.map((name, i) => `${name} ${fmt(d.lengths[i])}`).join(' · ') + ' mm travel';
      return `<div class="check ${d.rim < 2.2 || d.minWeb < 2.2 ? 'warning' : 'good'}"><b>${frame === 'inner' ? 'Fixed inner' : frame === 'left' ? 'Left outer' : 'Right outer'}</b><p>Rim ${fmt(d.rim)} mm · sampled web ${fmt(d.minWeb)} mm<br>Closest rails: ${d.closest}${d.rim < 2.2 || d.minWeb < 2.2 ? '<br>Warning: below 2.20 mm target.' : '<br>No sampled rim/web warning.'}</p></div>`;
    });
    $('diagnostics').innerHTML = (profile.slotDiameterMm < 4 ? '<p class="warning">Slot diameter is smaller than the Ø4 mm rod.</p>' : '') + rows.join('');
  }
  const editor = $('editor');
  function pointerPoint(event) {
    const matrix = editor.getScreenCTM();
    if (!matrix) return null;
    const point = new DOMPoint(event.clientX, event.clientY).matrixTransform(matrix.inverse());
    return [point.x, -point.y];
  }
  function translate(rod, delta) {
    const limited = delta.map((n, j) => Math.max(-60 - Math.min(rod.open[j], rod.end[j]), Math.min(60 - Math.max(rod.open[j], rod.end[j]), n)));
    return {open: rod.open.map((n, j) => n + limited[j]), end: rod.end.map((n, j) => n + limited[j])};
  }
  function movePointer(event) {
    const point = pointerPoint(event); if (!point) return;
    const delta = point.map((n, j) => n - drag.pointerStart[j]);
    const rod = profile.rods[drag.rod];
    if (drag.kind === 'line') Object.assign(rod, translate(drag.startRod, delta));
    else {
      const key = drag.kind === 'curve' ? 'bendMm' : drag.kind;
      rod[key] = drag.startRod[key].map((n, j) => Math.max(-60, Math.min(60, n + delta[j])));
    }
    syncInputs(); changed();
    $('selected-hole').textContent = `${G.names[drag.rod]} · ${drag.kind === 'line' ? 'moving entire path' : drag.kind === 'curve' ? 'shaping curve' : drag.kind.toUpperCase() + ' endpoint'}`;
  }
  editor.addEventListener('pointerdown', event => {
    if (event.button !== 0) return;
    const target = event.target.closest('[data-handle], [data-line]');
    if (!target) return;
    event.preventDefault(); stop();
    const kind = target.dataset.kind || 'line', rod = +(target.dataset.handle ?? target.dataset.line);
    if (kind !== 'line') progress = kind === 'open' ? 0 : kind === 'end' ? 1 : .5;
    drag = {rod, kind, pointer: event.pointerId, pointerStart: pointerPoint(event), startRod: structuredClone(profile.rods[rod])};
    editor.setPointerCapture(event.pointerId); draw();
  });
  editor.addEventListener('pointermove', event => { if (drag && drag.pointer === event.pointerId) movePointer(event); });
  function finishDrag(event) {
    if (!drag || drag.pointer !== event.pointerId) return;
    drag = null; draw();
    clearTimeout(diagnosticTimer); drawDiagnostics();
  }
  editor.addEventListener('pointerup', finishDrag);
  editor.addEventListener('pointercancel', finishDrag);
  editor.addEventListener('lostpointercapture', finishDrag);
  editor.addEventListener('keydown', event => {
    const target = event.target.closest('[data-handle], [data-line]');
    const delta = {ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, 1], ArrowDown: [0, -1]}[event.key];
    if (!target || !delta) return;
    event.preventDefault(); stop();
    const index = +(target.dataset.handle ?? target.dataset.line), kind = target.dataset.kind || 'line', step = event.shiftKey ? 1 : .1;
    if (kind === 'line') Object.assign(profile.rods[index], translate(profile.rods[index], delta.map(n => n * step)));
    else {
      const key = kind === 'curve' ? 'bendMm' : kind;
      profile.rods[index][key] = profile.rods[index][key].map((n, j) => Math.max(-60, Math.min(60, n + delta[j] * step)));
    }
    syncInputs(); changed(); editor.querySelector(kind === 'line' ? `[data-line="${index}"]` : `[data-handle="${index}"][data-kind="${kind}"]`).focus();
  });
  function stop() { playing = false; cancelAnimationFrame(frameRequest); $('play').textContent = 'Play motion'; $('play').setAttribute('aria-pressed', 'false'); }
  $('progress').oninput = () => { stop(); progress = +$('progress').value / 1000; draw(); };
  document.querySelectorAll('[data-state]').forEach(button => { button.onclick = () => { stop(); progress = +button.dataset.state; draw(); }; });
  $('play').onclick = () => {
    if (playing) { stop(); return; }
    playing = true; $('play').textContent = 'Pause motion'; $('play').setAttribute('aria-pressed', 'true');
    const initial = performance.now(), startProgress = progress === 1 ? 0 : progress;
    function tick(now) {
      if (!playing) return;
      progress = Math.min(1, startProgress + (now - initial) / 4000);
      draw();
      if (progress < 1) frameRequest = requestAnimationFrame(tick); else stop();
    }
    frameRequest = requestAnimationFrame(tick);
  };
  document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); });
  function download(filename, body, type) {
    const url = URL.createObjectURL(new Blob([body], {type}));
    const anchor = document.createElement('a'); anchor.href = url; anchor.download = filename;
    document.body.append(anchor); anchor.click(); anchor.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  $('save').onclick = () => { download('xt60-rail-profile.json', JSON.stringify(G.validate(profile), null, 2) + '\n', 'application/json'); status('Profile JSON downloaded.'); };
  $('load').onclick = () => { stop(); $('file').click(); };
  $('file').onchange = async () => {
    const file = $('file').files[0]; if (!file) return;
    try {
      if (file.size > 100000) throw new Error('Choose a profile JSON smaller than 100 KB.');
      const loaded = G.validate(JSON.parse(await file.text()));
      stop(); profile = loaded; progress = 0; syncInputs(); changed();
      $('profile-state').textContent = 'Loaded profile · kinematic experiment'; status('Profile loaded.');
    } catch (error) { status(`Load failed: ${error.message} Current profile kept.`); }
    $('file').value = '';
  };
  $('reset').onclick = () => { stop(); profile = G.defaults(); progress = 0; syncInputs(); draw(); persist(); drawDiagnostics(); $('selected-hole').textContent = 'Drag an endpoint, path or curve dot.'; $('profile-state').textContent = 'Recovered P20 profile'; status('Archived P20 default restored.'); };
  document.querySelectorAll('[data-export]').forEach(button => { button.onclick = () => {
    const frame = button.dataset.export;
    download(`xt60-${frame}-rails-mm.svg`, G.svg(profile, frame), 'image/svg+xml');
    status(`${frame} plate-local SVG downloaded in mm.`);
  }; });
  syncInputs(); draw(); drawDiagnostics();
})();
