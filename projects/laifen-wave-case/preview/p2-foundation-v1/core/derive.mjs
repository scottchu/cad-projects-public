const finite = value => typeof value === "number" && Number.isFinite(value);
const clone = value => structuredClone(value);
const freeze = value => {
  if (value && typeof value === "object" && !Object.isFrozen(value)) {
    Object.values(value).forEach(freeze);
    Object.freeze(value);
  }
  return value;
};

export const DEFAULT_INPUTS = freeze({
  H: 120, OD: 60, W: 2.4, F: 3,
  splitMode: "percent", splitValue: 50,
  section: "round", N: 6,
  bottomStyle: "chamfer", bottomSize: 1.2,
  topStyle: "chamfer", topSize: 1.2,
  P: 2, T: 2, C: 0.25, D: 0.45, threadForm: "symmetric trapezoid",
  drainLocation: "bottom", Q: 7, d: 3, BCD: 20,
  presentation: "assembled",
});

const enumValues = {
  splitMode: ["percent", "distance"], section: ["round", "polygon"],
  bottomStyle: ["flat", "chamfer", "rounded"], topStyle: ["flat", "chamfer", "rounded"],
  threadForm: ["symmetric trapezoid", "rounded"], drainLocation: ["none", "top", "bottom"],
  presentation: ["assembled", "exploded"],
};
const numericBounds = {
  H: [40, 300], OD: [20, 160], W: [.8, 8], F: [.8, 12],
  P: [.8, 6], T: [1, 3], C: [.1, .6], D: [.2, 1.5], Q: [1, 16], d: [.8, 10],
};
const error = (errors, path, message) => errors.push({path, message});
const numberOrDefault = (raw, key) => raw[key] === undefined ? DEFAULT_INPUTS[key] : Number(raw[key]);

function normalized(raw = {}) {
  const source = {...DEFAULT_INPUTS, ...raw};
  const state = {};
  for (const key of Object.keys(DEFAULT_INPUTS)) {
    state[key] = Object.hasOwn(numericBounds, key) || ["splitValue", "N", "bottomSize", "topSize", "BCD"].includes(key)
      ? numberOrDefault(source, key) : source[key];
  }
  if (state.section === "round") state.N = DEFAULT_INPUTS.N;
  if (state.bottomStyle === "flat") state.bottomSize = 0;
  if (state.topStyle === "flat") state.topSize = 0;
  if (state.drainLocation === "none") {
    state.Q = DEFAULT_INPUTS.Q; state.d = DEFAULT_INPUTS.d; state.BCD = DEFAULT_INPUTS.BCD;
  } else if (state.Q === 1) state.BCD = 0;
  return state;
}

const endPath = (style, size, R, top = false) => {
  const sign = top ? -1 : 1;
  if (style === "flat") return [{r:R, z:0}, {r:R, z:0}];
  if (style === "chamfer") return [{r:R-size, z:0}, {r:R, z:sign*size}];
  return Array.from({length:9}, (_, i) => {
    const t = Math.PI * i / 16;
    return {r:R-size+size*Math.sin(2*t), z:sign*(size-size*Math.cos(2*t))};
  });
};

export function deriveV1(raw = {}) {
  const state = normalized(raw), errors = [];
  for (const [key, [min, max]] of Object.entries(numericBounds)) {
    if (!finite(state[key]) || state[key] < min || state[key] > max) error(errors, key, `${key} must be a finite value from ${min} to ${max}.`);
  }
  for (const [key, values] of Object.entries(enumValues)) {
    if (!values.includes(state[key])) error(errors, key, `${key} has an invalid selection.`);
  }
  if (!Number.isInteger(state.T)) error(errors, "T", "T must be an integer turn count.");
  if (state.section === "polygon" && (!Number.isInteger(state.N) || state.N < 3 || state.N > 32)) error(errors, "N", "N must be an integer from 3 to 32 for a polygon.");
  const R = state.OD / 2;
  const AF = state.section === "polygon" ? state.OD * Math.cos(Math.PI / state.N) : null;
  const ID = (AF ?? state.OD) - 2 * state.W;
  const usableHeight = state.H - 2 * state.F;
  const U = state.splitMode === "percent" ? state.H * state.splitValue / 100 : state.splitValue;
  const splitPercent = 100 * U / state.H;
  const splitZ = state.H - U;
  const E = state.P * state.T;
  const residualThreadWall = state.W - state.D;
  if (!finite(state.splitValue) || (state.splitMode === "percent" && (state.splitValue < 25 || state.splitValue > 75))) error(errors, "splitValue", "Split percentage must be from 25 to 75.");
  if (state.splitMode === "distance" && (!finite(state.splitValue) || state.splitValue < state.H*.25 || state.splitValue > state.H*.75)) error(errors, "splitValue", "Split distance must keep the seam from 25% to 75% from the top.");
  if (ID < 4) error(errors, "W", "Clear ID must be at least 4 mm.");
  if (!(usableHeight > 0)) error(errors, "F", "Usable cavity height must be positive.");
  if (!(U >= state.F + E + 2 && state.H-U >= state.F + E + 2)) error(errors, "splitValue", "Both pieces need floor, screw engagement, and 2 mm keepout.");
  if (!(residualThreadWall >= .8)) error(errors, "D", "Thread residual wall must be at least 0.8 mm.");
  if (!(state.C < state.D)) error(errors, "C", "Radial clearance must be smaller than thread depth.");
  for (const [styleKey, sizeKey, length] of [["bottomStyle", "bottomSize", splitZ], ["topStyle", "topSize", U]]) {
    if (state[styleKey] !== "flat" && (!finite(state[sizeKey]) || state[sizeKey] < .2 || state[sizeKey] > Math.min(state.F, state.OD/8) || state[sizeKey] > length)) error(errors, sizeKey, "End size must fit its floor envelope and piece length.");
  }
  const Rb = state.BCD / 2;
  let drainPositions = [];
  if (state.drainLocation !== "none") {
    if (!finite(state.BCD) || state.BCD < 0) error(errors, "BCD", "Drain bolt-circle diameter must be non-negative.");
    if (state.Q === 1 && state.BCD !== 0) error(errors, "BCD", "One drain is centered, so BCD is zero.");
    if (Rb + state.d/2 + 1.2 > ID/2) error(errors, "BCD", "Drain edge and web exceed the clear cavity.");
    if (state.Q > 1 && 2*Rb*Math.sin(Math.PI/state.Q)-state.d < 1.2) error(errors, "BCD", "Drain holes need at least 1.2 mm web.");
    drainPositions = Array.from({length:state.Q}, (_, i) => ({x:state.Q === 1 ? 0 : Rb*Math.cos(2*Math.PI*i/state.Q), y:state.Q === 1 ? 0 : Rb*Math.sin(2*Math.PI*i/state.Q), r:state.d/2}));
  }
  if (errors.length) return freeze({valid:false, errors, descriptor:null});
  const radialSegments = state.section === "round" ? 64 : state.N;
  const end = (style, size, top) => ({style, size, path:endPath(style, size, R, top)});
  const explodeGap = Math.max(12, E + 6);
  const descriptor = {
    version:"p2-foundation-v1", inputs:state,
    R, ID, AF, usableHeight, U, splitPercent, splitZ, lowerLength:splitZ, upperLength:U,
    commonOutsideDiameter:state.OD, cavity:{bottomZ:state.F, topZ:state.H-state.F, radius:ID/2},
    section:{kind:state.section, N:state.N, radialSegments},
    ends:{bottom:end(state.bottomStyle, state.bottomSize, false), top:end(state.topStyle, state.topSize, true)},
    screw:{pitch:state.P, turns:state.T, engagement:E, radialClearance:state.C, diametralClearance:2*state.C, depth:state.D, form:state.threadForm, residualThreadWall},
    drains:{location:state.drainLocation, count:state.drainLocation === "none" ? 0 : state.Q, diameter:state.drainLocation === "none" ? 0 : state.d, BCD:state.drainLocation === "none" ? 0 : state.BCD, positions:drainPositions},
    pieces:{lower:{z:0, length:splitZ}, upper:{z:state.presentation === "exploded" ? explodeGap : 0, length:U}},
    presentation:state.presentation, bounds:{min:{x:-R,y:-R,z:0}, max:{x:R,y:R,z:state.H+(state.presentation === "exploded" ? explodeGap : 0)}},
    plans:{lowerShell:{z0:0,z1:splitZ}, upperShell:{z0:splitZ,z1:state.H}, seamZ:splitZ, maleThread:{z0:splitZ-E,z1:splitZ}, femaleThread:{z0:splitZ,z1:splitZ+E}},
  };
  return freeze({valid:true, errors:[], descriptor:freeze(clone(descriptor))});
}
