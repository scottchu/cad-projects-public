import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import '../preview/rail-customizer/geometry.js';
const G = globalThis.RailGeometry;
const near = (a, b, tolerance = 1e-8) => assert.ok(Math.abs(a - b) <= tolerance, `${a} != ${b}`);

test('recovered default matches preserved P20 R4 source at all sampled states', () => {
  const source = readFileSync(new URL('../src/xt60_bend_jig/p20_r4_custom_profile_full_cad.py', import.meta.url), 'utf8');
  const points = name => {
    const section = source.split(`${name}: dict`)[1].split('}')[0];
    return [...section.matchAll(/PointYZ\(([-.\d]+), ([-.\d]+)\)/g)].map(m => [+m[1], +m[2]]);
  };
  const open = points('OPEN_POINTS'), end = points('END_POINTS'), p = G.defaults();
  assert.equal(open.length, 3); assert.equal(end.length, 3);
  for (let i = 0; i < 3; i++) for (let n = 0; n <= 360; n++) {
    const u = n / 360;
    const expected = open[i].map((v, j) => v + (end[i][j] - v) * u);
    G.world(p.rods[i], u).forEach((v, j) => near(v, expected[j]));
    for (const [frame, sign] of [['left', 1], ['right', -1]]) {
      const angle = sign * 45 * u * Math.PI / 180;
      const actual = G.local(p, p.rods[i], u, frame);
      near(actual[0], expected[0] * Math.cos(angle) + expected[1] * Math.sin(angle));
      near(actual[1], -expected[0] * Math.sin(angle) + expected[1] * Math.cos(angle));
    }
  }
  near(G.length(G.paths(p, 'inner')[2]), 0);
});

test('both inverse plate frames reconstruct edited world paths and fixed axle', () => {
  const p = G.defaults(); p.rods[0].open = [-30, 18]; p.rods[2].end = [5, -13];
  p.leftTravelDeg = 120; p.rightTravelDeg = -75;
  for (const frame of ['left', 'right']) for (const u of [0, .125, .5, .875, 1]) {
    for (const rod of p.rods) G.rotate(G.local(p, rod, u, frame), G.travel(p, frame) * u).forEach((v, j) => near(v, G.world(rod, u)[j]));
    G.rotate(G.axleLocal(p, u, frame), G.travel(p, frame) * u).forEach((v, j) => near(v, p.axle[j]));
  }
});

test('sampled web reproduces the archived coupon witness and exposes unsafe default', () => {
  const p = G.defaults(), [blue, orange] = G.paths(p, 'left');
  near(G.sampledGap(blue, orange, 4.15), 1.7150733085690888, 1e-10);
  // Historical design records this conservative axle-hex rim warning to 3 decimals.
  near(G.diagnostics(p, 'inner').rim, 1.152, 1e-3);
  assert.ok(G.diagnostics(p, 'left').minWeb < 2.2);
});

test('profile import round-trips all endpoints and rejects corrupt or unsupported data', () => {
  const p = G.defaults(); p.rods[1].open = [-20, 30]; p.rods[2].end = [60, -60];
  assert.deepEqual(G.validate(JSON.parse(JSON.stringify(p))), p);
  for (const mutate of [p => {p.schema = 'other';}, p => {p.units = 'inch';}, p => {p.rods.pop();}, p => {p.rods[0].open[0] = null;}, p => {p.rods[1].end = [Infinity, 0];}, p => {p.rods[0].name = '<script>';}, p => {p.leftTravelDeg = 181;}, p => {p.slotDiameterMm = 0;}]) {
    const bad = structuredClone(p); mutate(bad); assert.throws(() => G.validate(bad));
  }
});

test('SVG exports preserve mm scale, full paths and local frames', () => {
  const p = G.defaults();
  for (const frame of ['inner', 'left', 'right']) {
    const svg = G.svg(p, frame);
    assert.match(svg, /width="[\d.]+mm" height="[\d.]+mm"/);
    for (const rail of G.paths(p, frame)) assert.ok(svg.includes(G.pathData(rail)));
    assert.equal((svg.match(/stroke-width="4.15"/g) || []).length, 3);
    assert.match(svg, /not manufacturing-approved CAD/);
  }
  assert.throws(() => G.svg(p, 'wrong'));
});

test('viewport encloses rotated extreme diagonal endpoints and complete slot envelopes', () => {
  const p = G.defaults();
  p.rods[0].open = [60, 60]; p.rods[0].end = [60, 60];
  p.rods[1].open = [-60, 60]; p.rods[1].end = [-60, -60];
  p.leftTravelDeg = 180; p.rightTravelDeg = -180; p.axle = [-60, 60];
  p.rods[0].bendMm = [60, -60]; p.rods[1].bendMm = [-60, 60];
  const bound = G.viewBound(p);
  for (const frame of ['inner', 'left', 'right']) {
    for (const rail of G.paths(p, frame)) for (const point of rail) {
      for (const coord of point) assert.ok(Math.abs(coord) + p.slotDiameterMm / 2 < bound);
    }
    for (const point of G.sample(u => G.axleLocal(p, u, frame))) for (const coord of point) assert.ok(Math.abs(coord) + p.axleGuideDiameterMm / 2 < bound);
  }
});

test('curve dot determines midpoint while preserving endpoints and both inverse frames', () => {
  const p = G.defaults(), rod = p.rods[0]; rod.bendMm = [3, -5];
  assert.deepEqual(G.world(rod, 0), rod.open);
  G.world(rod, 1).forEach((v, j) => near(v, rod.end[j]));
  G.world(rod, .5).forEach((v, j) => near(v, (rod.open[j] + rod.end[j]) / 2 + rod.bendMm[j]));
  for (const frame of ['left', 'right']) for (let n = 0; n <= 360; n++) {
    const u = n / 360;
    G.rotate(G.local(p, rod, u, frame), G.travel(p, frame) * u).forEach((v, j) => near(v, G.world(rod, u)[j]));
  }
  const delta = [7, -2], shifted = {...rod, open: rod.open.map((v, j) => v + delta[j]), end: rod.end.map((v, j) => v + delta[j])};
  for (const u of [0, .25, .5, .75, 1]) G.world(shifted, u).forEach((v, j) => near(v, G.world(rod, u)[j] + delta[j]));
  for (const frame of ['inner', 'left', 'right']) assert.ok(G.svg(p, frame).includes(G.pathData(G.paths(p, frame)[0])));
});

test('legacy profiles migrate to zero bend and new curves survive JSON', () => {
  const old = G.defaults(); old.rods.forEach(rod => delete rod.bendMm);
  assert.deepEqual(G.validate(old), G.defaults());
  const current = G.defaults(); current.rods[2].bendMm = [-4.5, 7.25];
  assert.deepEqual(G.validate(JSON.parse(JSON.stringify(current))), current);
  for (const bad of [null, [1], [0, Infinity], [61, 0]]) {
    const p = G.defaults(); p.rods[0].bendMm = bad; assert.throws(() => G.validate(p));
  }
});
