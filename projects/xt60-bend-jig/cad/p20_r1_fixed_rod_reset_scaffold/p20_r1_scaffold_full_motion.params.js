// P20 R1 evidence-only intentionally-colliding non-candidate scaffold.
// One normalized state rotates the two solid outer plates about axle A and
// preserves all three P19 world rod paths. There are deliberately no outer
// rod apertures in this scaffold.

const AXLE_ORIGIN = Object.freeze([0.0, -15.0, -11.0]);
const AXIS = Object.freeze([1.0, 0.0, 0.0]);
const THETA_END_DEG = 45.0;
const PATHS = Object.freeze({
  upright: Object.freeze({ open: [20.4, -9.1728142259], end: [22.052212035894, -3.477677650052] }),
  bottom: Object.freeze({ open: [5.0, 10.0], end: [9.552212035894, 8.022322349948] }),
  diagonal: Object.freeze({ open: [20.4, 10.0], end: [15.802212035894, 2.272322349948] }),
});

const FEATURES = {
  left_outer: { names: ["motion_full_rotating_left_outer__P20_scaffold"] },
  right_outer: { names: ["motion_full_rotating_right_outer__P20_scaffold"] },
};
for (const name of Object.keys(PATHS)) {
  FEATURES[`${name}_rod`] = { names: [`motion_full_${name}_rod__P20_scaffold`] };
  FEATURES[`left_${name}_cap`] = { names: [`motion_full_left_${name}_cap__P20_scaffold`] };
  FEATURES[`right_${name}_cap`] = { names: [`motion_full_right_${name}_cap__P20_scaffold`] };
}

function clamp01(value) {
  const number = Number(value);
  return Math.min(Math.max(Number.isFinite(number) ? number : 0.0, 0.0), 1.0);
}

function motionState(value) {
  const u = clamp01(value);
  const thetaDeg = THETA_END_DEG * u;
  const rods = {};
  for (const [name, path] of Object.entries(PATHS)) {
    rods[name] = [
      0.0,
      (path.end[0] - path.open[0]) * u,
      (path.end[1] - path.open[1]) * u,
    ];
  }
  return Object.freeze({
    u,
    thetaDeg,
    alphaLeftDeg: -thetaDeg,
    alphaRightDeg: thetaDeg,
    rods: Object.freeze(rods),
  });
}

function pingPong(elapsedSec, durationSec = 8.0) {
  const duration = Math.max(Number(durationSec) || 8.0, Number.EPSILON);
  const phase = (((Number(elapsedSec) || 0.0) % duration) + duration) % duration / duration;
  return phase <= 0.5 ? phase * 2.0 : (1.0 - phase) * 2.0;
}

const definition = {
  manifest: {
    schemaVersion: 1,
    status: "evidence-only intentionally-colliding non-candidate scaffold",
    step: { path: "cad/p20_r1_fixed_rod_reset_scaffold/p20_r1_scaffold_full_motion.step" },
    parameters: {
      open_to_end: {
        type: "number", label: "OPEN to END scaffold evidence", unit: "normalized",
        min: 0.0, max: 1.0, step: 0.01, default: 0.0,
      },
    },
    features: FEATURES,
    animations: {
      open_end_open: {
        label: "OPEN - END - OPEN scaffold evidence", durationSeconds: 8.0, loop: true,
        update({ elapsedSec, set }) { set("open_to_end", pingPong(elapsedSec)); },
      },
    },
  },
  update({ params, effects }) {
    const state = motionState(params.open_to_end);
    effects.transform("left_outer", { rotate: { axis: AXIS, origin: AXLE_ORIGIN, angleDeg: state.alphaLeftDeg } });
    effects.transform("right_outer", { rotate: { axis: AXIS, origin: AXLE_ORIGIN, angleDeg: state.alphaRightDeg } });
    for (const [name, translation] of Object.entries(state.rods)) {
      effects.transform(`${name}_rod`, { translate: translation });
      effects.transform(`left_${name}_cap`, { translate: translation });
      effects.transform(`right_${name}_cap`, { translate: translation });
    }
  },
};

export { motionState };
export default definition;
