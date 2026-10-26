(() => {
  'use strict';
  const G = globalThis.RailGeometry;
  const $ = id => document.getElementById(id);
  const key = 'xt60-rail-customizer/v1';
  let profile = G.defaults(), progress = 0, mode = 'open', drag = null, playing = false;
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

  $('rod-controls').innerHTML = G.names.map((name, i) => `<fieldset class="rod"><legend><i class="swatch" style="background:${G.colors[i]}"></i>${name}</legend>${['open', 'end'].map(endpoint => `<div class="endpoint-row"><span>${endpoint.toUpperCase()}</span>${['Y', 'Z'].map((axis, j) => `<label>${axis}<input type="number" step="0.01" min="-60" max="60" data-rod="${i}" data-endpoint="${endpoint}" data-axis="${j}" aria-label="${name} ${endpoint.toUpperCase()} ${axis}"></label>`).join('')}</div>`).join('')}</fieldset>`).join('');
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
  function setMode(next) {
    stop(); mode = next; progress = next === 'open' ? 0 : 1;
    $('selected-hole').textContent = 'Drag a hole or use the coordinates.';
    document.querySelectorAll('[data-edit]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.edit === mode)));
    draw();
  }
  document.querySelectorAll('[data-edit]').forEach(button => { button.onclick = () => setMode(button.dataset.edit); });
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
    return G.paths(profile, frame).map((points, i) => `<path data-rail="${i}" d="${G.pathData(points)}" fill="none" stroke="${G.colors[i]}" stroke-width="${profile.slotDiameterMm}" stroke-linecap="round" stroke-linejoin="round" opacity="0.28"/><path d="${G.pathData(points)}" fill="none" stroke="${G.colors[i]}" stroke-width=".16" stroke-dasharray=".5 .4"/>`).join('');
  }
  function axleLayer(frame) {
    return `<path data-axle-rail d="${G.pathData(G.sample(u => G.axleLocal(profile, u, frame)))}" fill="none" stroke="#906cbe" stroke-width="${profile.axleGuideDiameterMm}" stroke-linecap="round" opacity=".22"/>${circle(G.axleLocal(profile, progress, frame), .75, 'fill="#75559e"')}<text class="svg-label" x="${G.axleLocal(profile, 0, frame)[0] - 2}" y="${-G.axleLocal(profile, 0, frame)[1] + 4.8}">fixed axle</text>`;
  }
  function rodMarkers(frame) {
    return profile.rods.map((rod, i) => circle(G.local(profile, rod, progress, frame), 2, `fill="#fffdf5" stroke="${G.colors[i]}" stroke-width=".5" data-current-rod="${i}"`)).join('');
  }
  function handles() {
    return ['open', 'end'].filter(e => e !== mode).concat(mode).map(endpoint => profile.rods.map((rod, i) => {
      const p = rod[endpoint], active = endpoint === mode;
      const handle = endpoint === 'open' ? '<circle r="1"/>' : '<path d="M0,-1.4L1.4,0L0,1.4L-1.4,0Z"/>';
      return `<g transform="translate(${p[0]},${-p[1]})" ${active ? `data-handle="${i}" tabindex="0" role="button" aria-label="${rod.name} ${endpoint.toUpperCase()} hole. Arrow keys move 0.1 mm; Shift moves 1 mm."` : 'pointer-events="none"'}><circle class="handle-target" r="3.1"/><g fill="${active ? G.colors[i] : '#f4f1e7'}" stroke="${G.colors[i]}" stroke-width=".3">${handle}</g>${active ? `<text class="svg-label" x="${i === 0 ? -8 : 2}" y="${endpoint === 'open' ? -2.8 : 3.8}">${rod.name} ${endpoint.toUpperCase()}</text>` : ''}</g>`;
    }).join('')).join('');
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
  function movePointer(event) {
    const matrix = editor.getScreenCTM();
    if (!matrix) return;
    const point = new DOMPoint(event.clientX, event.clientY).matrixTransform(matrix.inverse());
    profile.rods[drag.rod][mode] = [point.x, -point.y].map(n => Math.max(-60, Math.min(60, n)));
    syncInputs(); changed();
    $('selected-hole').textContent = `${G.names[drag.rod]} ${mode.toUpperCase()} (${profile.rods[drag.rod][mode].map(fmt).join(', ')}) mm`;
  }
  editor.addEventListener('pointerdown', event => {
    if (event.button !== 0) return;
    const target = event.target.closest('[data-handle]');
    if (!target) return;
    event.preventDefault(); stop();
    progress = mode === 'open' ? 0 : 1;
    drag = {rod: +target.dataset.handle, pointer: event.pointerId};
    editor.setPointerCapture(event.pointerId); movePointer(event);
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
    const target = event.target.closest('[data-handle]');
    const delta = {ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, 1], ArrowDown: [0, -1]}[event.key];
    if (!target || !delta) return;
    event.preventDefault(); stop();
    const index = +target.dataset.handle, step = event.shiftKey ? 1 : .1;
    profile.rods[index][mode] = profile.rods[index][mode].map((n, j) => Math.max(-60, Math.min(60, n + delta[j] * step)));
    syncInputs(); changed(); editor.querySelector(`[data-handle="${index}"]`).focus();
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
  $('reset').onclick = () => { stop(); profile = G.defaults(); progress = 0; mode = 'open'; syncInputs(); setMode('open'); persist(); drawDiagnostics(); $('profile-state').textContent = 'Recovered P20 profile'; status('Archived P20 default restored.'); };
  document.querySelectorAll('[data-export]').forEach(button => { button.onclick = () => {
    const frame = button.dataset.export;
    download(`xt60-${frame}-rails-mm.svg`, G.svg(profile, frame), 'image/svg+xml');
    status(`${frame} plate-local SVG downloaded in mm.`);
  }; });
  syncInputs(); draw(); drawDiagnostics();
})();
