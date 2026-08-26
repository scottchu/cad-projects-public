// P19 R1 cycle-4 review motion. One normalized state drives both plates and
// all three physical rods; plate-owned inverse rails remain static geometry.

const ORIGIN = Object.freeze([0.0, 0.0, 0.0]);
const AXIS = Object.freeze([1.0, 0.0, 0.0]);
const THETA_END_DEG = 5.0;
const PATHS = Object.freeze({
  upright: Object.freeze({ open: [20.4, -9.1728142259], end: [22.052212035894, -3.477677650052] }),
  bottom: Object.freeze({ open: [5.0, 10.0], end: [9.552212035894, 8.022322349948] }),
  diagonal: Object.freeze({ open: [20.4, 10.0], end: [15.802212035894, 2.272322349948] }),
});

const FEATURES = {
  left_outer: { names: ["motion_full_rotating_left_outer"] },
  right_outer: { names: ["motion_full_rotating_right_outer"] },
};
for (const name of Object.keys(PATHS)) {
  FEATURES[`${name}_rod`] = { names: [`motion_full_${name}_rod`] };
  FEATURES[`left_${name}_cap`] = { names: [`motion_full_left_${name}_cap`] };
  FEATURES[`right_${name}_cap`] = { names: [`motion_full_right_${name}_cap`] };
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

function pingPong(elapsedSec, durationSec = 6.0) {
  const duration = Math.max(Number(durationSec) || 6.0, Number.EPSILON);
  const phase = (((Number(elapsedSec) || 0.0) % duration) + duration) % duration / duration;
  return phase <= 0.5 ? phase * 2.0 : (1.0 - phase) * 2.0;
}

const definition = {
  manifest: {
    schemaVersion: 1,
    step: { path: "cad/p19_r1_front_edge_short_tail/p19_r1_full_motion.step" },
    parameters: {
      open_to_end: {
        type: "number", label: "OPEN to END", unit: "normalized",
        min: 0.0, max: 1.0, step: 0.01, default: 0.0,
      },
    },
    features: FEATURES,
    animations: {
      open_end_open: {
        label: "OPEN - END - OPEN", durationSeconds: 6.0, loop: true,
        update({ elapsedSec, set }) { set("open_to_end", pingPong(elapsedSec)); },
      },
    },
  },
  update({ params, effects }) {
    const state = motionState(params.open_to_end);
    effects.transform("left_outer", { rotate: { axis: AXIS, origin: ORIGIN, angleDeg: state.alphaLeftDeg } });
    effects.transform("right_outer", { rotate: { axis: AXIS, origin: ORIGIN, angleDeg: state.alphaRightDeg } });
    for (const [name, translation] of Object.entries(state.rods)) {
      effects.transform(`${name}_rod`, { translate: translation });
      effects.transform(`left_${name}_cap`, { translate: translation });
      effects.transform(`right_${name}_cap`, { translate: translation });
    }
  },
};

export default definition;
