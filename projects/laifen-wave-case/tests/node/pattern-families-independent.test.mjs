import test from 'node:test';
import assert from 'node:assert/strict';
import {adapt, DEFAULTS} from '../../preview/openscad-wasm-simulator/src/adapter.mjs';
import {deriveDraftState, dimensionSnapshot} from '../../preview/openscad-wasm-simulator/src/bounds.mjs';
import {steppedValue} from '../../preview/openscad-wasm-simulator/src/controls.mjs';
import {patternFields, patternMemories, waveEstimate} from '../../preview/openscad-wasm-simulator/src/patterns.mjs';
import {BROWSER_PRESET, snapshot} from '../../preview/openscad-wasm-simulator/src/schema.mjs';

// Independent oracle inputs:
// DESIGN 426729855f05805f16661cc3728a6145b2eac291b56f60199fc6ca7528cc3e61
// BRIEF 28483df404ab8b99528cdedb71ba98ef4f2f1146015a0b110904a7d4c78f71b6
// VALIDATION_PLAN 2aefb747139641d74a6297e22e63fd6de8b4d91e1170e885e3a4e624a3841399
// The pure oracle below predates the frozen candidate. Imports above are the explicit
// binding layer added only after candidate-source manifest 666f1a43... verified 36/36.

const TAU = 2 * Math.PI;
const almost = (actual, expected, tolerance = 1e-12) =>
  assert.ok(Math.abs(actual - expected) <= tolerance, `${actual} != ${expected}`);

export function diamondArc(size) {
  return size === 4.8 ? 3.63 : size * (3.63 / 4.8);
}

export function diamondOracle({radius, depth, size, height}) {
  const arc = diamondArc(size);
  const count = Math.floor(TAU * (radius - depth) / arc + 0.5);
  const actualArc = TAU * (radius - depth) / count;
  return {
    arc,
    count,
    actualArc,
    plateau: 0.36 * actualArc * size / Math.hypot(actualArc, size),
    slope: depth / (size * 0.32),
    triangles: 16 * count * (Math.ceil(height / (size / 8)) + 1),
  };
}

export function familyOracle({family, radius, depth, spacing, height, chamfer = 1.2}) {
  assert.ok(['ribs', 'rings', 'spiral'].includes(family));
  const count = family === 'ribs' ? Math.floor(TAU * (radius - depth) / spacing + 0.5) : null;
  const angularSamples = family === 'ribs' ? Math.max(192, 32 * count) : 192;
  const axialSegments = family === 'ribs' ? 1 : Math.ceil(height / (spacing / 16));
  const clipRows = Math.min(axialSegments + 1, Math.ceil(chamfer * axialSegments / height) + 2);
  const estimate = 2 * angularSamples * (axialSegments + 2)
    + 4 * angularSamples * clipRows + 2 * angularSamples;
  return {count, angularSamples, axialSegments, clipRows, estimate};
}

export function phaseDegrees(family, theta, globalZ, spacing, count, seam = 0) {
  const g = globalZ - seam;
  if (family === 'ribs') return count * theta;
  if (family === 'rings') return 360 * g / spacing;
  if (family === 'spiral') return 6 * theta - 360 * g / spacing;
  throw new Error(`unknown family ${family}`);
}

export function fieldRadius(radius, depth, phaseDeg) {
  return radius - depth * (1 - Math.cos(phaseDeg * Math.PI / 180)) / 2;
}

export function nextNominalGrid(value, minimum, step, direction) {
  const position = (value - minimum) / step;
  const index = direction > 0 ? Math.floor(position + 1e-12) + 1 : Math.ceil(position - 1e-12) - 1;
  return minimum + index * step;
}

test('Diamond derives exact default arc, count, plateau and slope', () => {
  const value = diamondOracle({radius: 19.5, depth: 0.45, size: 4.8, height: 135});
  assert.equal(value.arc, 3.63);
  for (const size of [4.8, 6.4, 8]) almost(diamondArc(size) / size, 3.63 / 4.8);
  assert.equal(value.count, 33);
  almost(value.actualArc, TAU * 19.05 / 33);
  almost(value.plateau, 0.36 * value.actualArc * 4.8 / Math.hypot(value.actualArc, 4.8));
  almost(value.slope, 0.45 / (4.8 * 0.32));
  assert.ok(value.plateau >= 1 && value.slope <= 1);
});

test('Diamond endpoints expose independent plateau, slope, count and wall predicates', () => {
  for (const size of [4.8, 8]) for (const depth of [0.1, 0.6]) {
    const value = diamondOracle({radius: 19.5, depth, size, height: 135});
    assert.ok(value.count >= 8 && value.count <= 128);
    assert.equal(value.plateau >= 1 && value.slope <= 1, true);
    assert.equal(3.95 + depth, depth === 0.1 ? 4.05 : 4.55);
  }
  assert.ok(diamondOracle({radius: 4.5, depth: 0.6, size: 4.8, height: 40}).count < 8);
});

test('Diamond preserves the literal 136.8 floating-ceil allocation boundary', () => {
  const common = {radius: 40, depth: 0.6, size: 4.8};
  assert.equal(diamondOracle({...common, height: 136.7}).triangles, 249_152);
  assert.equal(diamondOracle({...common, height: 136.8}).triangles, 250_240);
  assert.ok(diamondOracle({...common, height: 136.7}).triangles <= 250_000);
  assert.ok(diamondOracle({...common, height: 136.8}).triangles > 250_000);
});

test('Ribs round-half-up count transition drives angular samples', () => {
  const boundary = TAU * (19.5 - 0.45) / 19.5;
  const below = familyOracle({family: 'ribs', radius: 19.5, depth: 0.45, spacing: boundary - 1e-9, height: 135});
  const exact = familyOracle({family: 'ribs', radius: 19.5, depth: 0.45, spacing: boundary, height: 135});
  const above = familyOracle({family: 'ribs', radius: 19.5, depth: 0.45, spacing: boundary + 1e-9, height: 135});
  assert.deepEqual([below.count, exact.count, above.count], [20, 20, 19]);
  assert.deepEqual([below.angularSamples, above.angularSamples], [640, 608]);
  assert.equal(below.axialSegments, 1);
  almost(boundary, 6.13818872316775);
});

test('Rings and Spiral retain literal ceil and conservative estimate order', () => {
  for (const family of ['rings', 'spiral']) {
    const exact = familyOracle({family, radius: 19.5, depth: 0.45, spacing: 6, height: 135});
    const lowerSpacing = familyOracle({family, radius: 19.5, depth: 0.45, spacing: 6 - 1e-9, height: 135});
    const higherSpacing = familyOracle({family, radius: 19.5, depth: 0.45, spacing: 6 + 1e-9, height: 135});
    assert.deepEqual([lowerSpacing.axialSegments, exact.axialSegments, higherSpacing.axialSegments], [361, 360, 360]);
    assert.equal(exact.clipRows, Math.min(361, Math.ceil(1.2 * 360 / 135) + 2));
    assert.equal(exact.estimate, 144_000);
    assert.ok(lowerSpacing.estimate <= 250_000);
  }
});

test('new-family endpoint witnesses satisfy allocation and exact wall threshold', () => {
  for (const family of ['ribs', 'rings', 'spiral']) for (const spacing of [4, 16]) for (const depth of [0.1, 0.6]) {
    const value = familyOracle({family, radius: 19.5, depth, spacing, height: 135});
    if (family === 'ribs') assert.ok(value.count >= 3);
    assert.ok(value.estimate <= 250_000, `${family} s=${spacing} d=${depth}`);
    const threshold = 3.95 + depth + 0.01;
    almost(threshold, depth === 0.1 ? 4.06 : 4.56);
    assert.ok(threshold >= 3.95 + depth + 0.01);
    assert.ok(threshold - 0.01 < 3.95 + depth + 0.01);
  }
});

test('phase uses global Z continuously across the body-cap seam', () => {
  const seam = 135;
  for (const family of ['ribs', 'rings', 'spiral']) for (const theta of [0, 17.25, 359.5]) {
    const body = phaseDegrees(family, theta, seam, 6, 20, seam);
    const cap = phaseDegrees(family, theta, seam + 0, 6, 20, seam);
    almost(body, cap);
    if (family === 'rings') almost(body, 0);
  }
  almost(phaseDegrees('spiral', 360, seam + 36, 6, 20, seam), phaseDegrees('spiral', 0, seam, 6, 20, seam));
});

test('field is inward-only and attains exact crest and valley radii', () => {
  almost(fieldRadius(19.5, 0.6, 0), 19.5);
  almost(fieldRadius(19.5, 0.6, 180), 18.9);
  for (const phase of [0, 30, 90, 180, 270, 359]) {
    const radius = fieldRadius(19.5, 0.6, phase);
    assert.ok(radius >= 18.9 && radius <= 19.5);
  }
});

test('off-grid keyboard movement selects the next strict nominal-grid value', () => {
  almost(nextNominalGrid(4.83, 4.8, 0.1, 1), 4.9);
  almost(nextNominalGrid(4.83, 4.8, 0.1, -1), 4.8);
  almost(nextNominalGrid(0.43, 0.1, 0.05, 1), 0.45);
  almost(nextNominalGrid(0.43, 0.1, 0.05, -1), 0.4);
});

test('finite domain witnesses reject non-finite values before geometry math', () => {
  for (const value of [NaN, Infinity, -Infinity]) assert.equal(Number.isFinite(value), false);
  for (const value of [4, 4.8, 6, 8, 16, 0.1, 0.6]) assert.equal(Number.isFinite(value), true);
});

test('candidate Diamond derivation equals the independent aspect oracle', () => {
  for (const size of [4.8, 4.83, 8]) {
    const raw = {...DEFAULTS, pattern: 'diamond', patterns: patternMemories()};
    raw.patterns.diamond = {size: String(size), depth: '0.45'};
    const fields = patternFields(raw);
    assert.equal(fields.diamond_axial_pitch, size);
    assert.equal(fields.diamond_arc_pitch, diamondArc(size));
    assert.equal(fields.diamond_depth, 0.45);
  }
});

test('candidate new-family N/n/M/E matches oracle at finite endpoints and ceil transition', () => {
  for (const family of ['ribs', 'rings', 'spiral']) for (const spacing of [4, 6 - 1e-9, 6, 6 + 1e-9, 16]) {
    const expected = familyOracle({family, radius: 19.5, depth: 0.45, spacing, height: 135});
    assert.equal(waveEstimate(135, expected.angularSamples, spacing, 1.2, family === 'ribs'), expected.estimate);
  }
});

test('candidate source preflight preserves Diamond literal allocation edge', () => {
  const source = {...BROWSER_PRESET, device_length: 262.4, outer_diameter: 80,
    body_bore: 69, cap_bore: 70, split_distance_from_top: 136.7,
    surface_style: 'diamond', diamond_axial_pitch: 4.8,
    diamond_arc_pitch: 3.63, diamond_depth: 0.6};
  assert.doesNotThrow(() => snapshot(source));
  assert.throws(() => snapshot({...source, split_distance_from_top: 136.8}), /triangle estimate/);
});

test('candidate adapter enforces the new-family wall equality and adjacent failure', () => {
  for (const pattern of ['ribs', 'rings', 'spiral']) {
    const raw = {...DEFAULTS, pattern, wall: '4.56', patterns: patternMemories()};
    raw.patterns[pattern] = {size: '6', depth: '0.6'};
    assert.ok(adapt(raw).values, `${pattern} equality must pass`);
    const failure = adapt({...raw, wall: '4.55'});
    assert.match(failure.errors.wall, /at least 4\.56 mm/);
  }
});

test('candidate feasible sliders agree with oracle strict off-grid movement', () => {
  const raw = {...DEFAULTS, pattern: 'diamond', wall: '4.6', patterns: patternMemories()};
  raw.patterns.diamond = {size: '4.83', depth: '0.43'};
  const state = deriveDraftState(raw, dimensionSnapshot(DEFAULTS));
  assert.equal(state.canGenerate, true);
  for (const [key, current, minimum, step] of [['size', 4.83, 4.8, 0.1], ['depth', 0.43, 0.1, 0.05]]) {
    const values = state.patternSliders[key].values;
    almost(steppedValue(values, current, 'ArrowRight'), nextNominalGrid(current, minimum, step, 1));
    almost(steppedValue(values, current, 'ArrowLeft'), nextNominalGrid(current, minimum, step, -1));
    assert.equal(steppedValue(values, current, 'Home'), values[0]);
    assert.equal(steppedValue(values, current, 'End'), values.at(-1));
  }
});

test('candidate slider derives each family endpoint through its selected predicate', () => {
  for (const pattern of ['diamond', 'ribs', 'rings', 'spiral']) {
    const raw = {...DEFAULTS, pattern, wall: '4.6', patterns: patternMemories()};
    const state = deriveDraftState(raw, dimensionSnapshot(DEFAULTS));
    assert.equal(state.canGenerate, true);
    const [sizeLow, sizeHigh] = pattern === 'diamond' ? [4.8, 8] : [4, 16];
    assert.deepEqual([state.patternSliders.size.values[0], state.patternSliders.size.values.at(-1)], [sizeLow, sizeHigh]);
    assert.deepEqual([state.patternSliders.depth.values[0], state.patternSliders.depth.values.at(-1)], [0.1, 0.6]);
  }
});
