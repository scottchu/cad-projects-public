/* Recovered P20 R4 rail equations. Classic script also imported by Node tests. */
(() => {
  'use strict';
  const names = ['Blue', 'Orange', 'Green'];
  const colors = ['#3c8edb', '#dd7d28', '#27946a'];
  const rad = Math.PI / 180;
  const baseEnds = [[9.552212035894, 8.022322349948], [15.802212035894, 2.272322349948], [22.052212035894, -3.477677650052]];
  const rotate = ([y, z], degrees) => {
    const a = degrees * rad;
    return [y * Math.cos(a) - z * Math.sin(a), y * Math.sin(a) + z * Math.cos(a)];
  };
  function defaults() {
    return {
      schema: 'xt60-rail-customizer/v1', units: 'mm',
      rods: names.map((name, i) => ({name,
        open: rotate([16, 0], [118, 45, -23][i]), bendMm: [0, 0],
        end: [baseEnds[i][0] - 7.3241343806549555, baseEnds[i][1] - 2.77402040577638]})),
      leftTravelDeg: 45, rightTravelDeg: -45,
      innerRadiusMm: 20, outerRadiusMm: 22.5, slotDiameterMm: 4.15,
      axle: [-10, -10], axleGuideDiameterMm: 7.9
    };
  }
  function validate(value) {
    const fail = message => { throw new Error(message); };
    if (!value || value.schema !== 'xt60-rail-customizer/v1' || value.units !== 'mm') fail('Choose an XT60 rail profile with schema v1 and mm units.');
    const finite = (n, min, max, label) => {
      if (typeof n !== 'number' || !Number.isFinite(n) || n < min || n > max) fail(`${label} must be a number from ${min} to ${max}.`);
      return n;
    };
    const point = (p, label) => {
      if (!Array.isArray(p) || p.length !== 2) fail(`${label} needs [Y, Z] coordinates.`);
      return p.map(n => finite(n, -60, 60, label));
    };
    if (!Array.isArray(value.rods) || value.rods.length !== 3) fail('The profile needs exactly Blue, Orange and Green rods.');
    const result = {schema: value.schema, units: 'mm', rods: value.rods.map((rod, i) => {
      if (!rod || rod.name !== names[i]) fail('Keep the rod order Blue, Orange, Green.');
      return {name: rod.name, open: point(rod.open, `${rod.name} OPEN`), end: point(rod.end, `${rod.name} END`), bendMm: rod.bendMm === undefined ? [0, 0] : point(rod.bendMm, `${rod.name} curve offset`)};
    })};
    for (const key of ['leftTravelDeg', 'rightTravelDeg']) result[key] = finite(value[key], -180, 180, key);
    for (const key of ['innerRadiusMm', 'outerRadiusMm']) result[key] = finite(value[key], 5, 60, key);
    for (const key of ['slotDiameterMm', 'axleGuideDiameterMm']) result[key] = finite(value[key], 0.1, 15, key);
    result.axle = point(value.axle, 'Fixed axle');
    return result;
  }
  function world(rod, u) {
    return rod.open.map((v, j) => v + (rod.end[j] - v) * u + 4 * u * (1 - u) * (rod.bendMm?.[j] ?? 0));
  }
  const travel = (p, frame) => frame === 'left' ? p.leftTravelDeg : frame === 'right' ? p.rightTravelDeg : 0;
  const local = (p, rod, u, frame) => rotate(world(rod, u), -travel(p, frame) * u);
  const axleLocal = (p, u, frame) => rotate(p.axle, -travel(p, frame) * u);
  const sample = fn => Array.from({length: 361}, (_, i) => fn(i / 360));
  const paths = (p, frame) => p.rods.map(rod => sample(u => local(p, rod, u, frame)));
  function viewBound(p) {
    // The linear endpoint norm plus bend norm bounds the complete bowed path;
    // the bump weight is in 0..1 and rotation preserves norm.
    return Math.max(27, p.innerRadiusMm + 5, p.outerRadiusMm + 5,
      ...p.rods.flatMap(rod => [rod.open, rod.end].map(v => Math.hypot(...v) + Math.hypot(...(rod.bendMm ?? [0, 0])) + p.slotDiameterMm / 2 + 7)),
      Math.hypot(...p.axle) + p.axleGuideDiameterMm / 2 + 7);
  }
  const length = points => points.slice(1).reduce((sum, v, i) => sum + Math.hypot(v[0] - points[i][0], v[1] - points[i][1]), 0);
  function sampledGap(a, b, diameterA, diameterB = diameterA) {
    let minSquared = Infinity;
    for (const pa of a) for (const pb of b) {
      const d = (pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2;
      if (d < minSquared) minSquared = d;
    }
    return Math.sqrt(minSquared) - (diameterA + diameterB) / 2;
  }
  function diagnostics(p, frame) {
    const rails = paths(p, frame);
    const radius = frame === 'inner' ? p.innerRadiusMm : p.outerRadiusMm;
    const axlePath = sample(u => axleLocal(p, u, frame));
    let rim = Math.min(...rails.flatMap(rail => rail.map(v => radius - Math.hypot(...v) - p.slotDiameterMm / 2)));
    // Conservative radial envelope of the archived AF8.15 fixed-inner hex bore.
    if (frame === 'inner') rim = Math.min(rim, radius - Math.hypot(...p.axle) - 8.15 / Math.sqrt(3));
    const gaps = [];
    for (let a = 0; a < 3; a++) for (let b = a + 1; b < 3; b++) {
      gaps.push({label: `${names[a]} / ${names[b]}`, gap: sampledGap(rails[a], rails[b], p.slotDiameterMm)});
    }
    if (frame !== 'inner') {
      rim = Math.min(rim, ...axlePath.map(v => radius - Math.hypot(...v) - p.axleGuideDiameterMm / 2));
      for (let i = 0; i < 3; i++) gaps.push({label: `${names[i]} / axle`, gap: sampledGap(rails[i], axlePath, p.slotDiameterMm, p.axleGuideDiameterMm)});
    }
    gaps.sort((a, b) => a.gap - b.gap);
    return {lengths: rails.map(length), rim, minWeb: gaps[0].gap, closest: gaps[0].label};
  }
  const pathData = points => points.map((p, i) => `${i ? 'L' : 'M'}${p[0].toFixed(6)},${(-p[1]).toFixed(6)}`).join(' ');
  function svg(p, frame) {
    p = validate(p);
    if (!['inner', 'left', 'right'].includes(frame)) throw new Error('Unknown plate frame.');
    const radius = frame === 'inner' ? p.innerRadiusMm : p.outerRadiusMm;
    const rails = paths(p, frame);
    const axle = sample(u => axleLocal(p, u, frame));
    const bound = Math.max(radius, ...rails.flat().map(v => Math.max(Math.abs(v[0]), Math.abs(v[1])) + p.slotDiameterMm / 2), ...axle.map(v => Math.max(Math.abs(v[0]), Math.abs(v[1])) + p.axleGuideDiameterMm / 2)) + 3;
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${2 * bound}mm" height="${2 * bound}mm" viewBox="${-bound} ${-bound} ${2 * bound} ${2 * bound}"><title>XT60 ${frame} plate-local rail study — mm, +Y right, +Z up</title><desc>361 samples. Colored strokes are complete slot envelopes. Inner axle is a reference only. Kinematic study, not manufacturing-approved CAD.</desc><circle cx="0" cy="0" r="${radius}" fill="#f3f0e8" stroke="#555" stroke-width="0.15"/>${rails.map((rail, i) => `<path d="${pathData(rail)}" fill="none" stroke="${colors[i]}" stroke-width="${p.slotDiameterMm}" stroke-linecap="round" stroke-linejoin="round"/>`).join('')}<path d="${pathData(axle)}" fill="none" stroke="#916cc3" stroke-width="${p.axleGuideDiameterMm}" stroke-linecap="round" opacity="0.55"${frame === 'inner' ? ' stroke-dasharray="0.4 0.4"' : ''}/></svg>`;
  }
  globalThis.RailGeometry = Object.freeze({names, colors, defaults, validate, rotate, world, travel, local, axleLocal, sample, paths, viewBound, length, sampledGap, diagnostics, pathData, svg});
})();
