// P18 R1 review motion. Plate-owned rails remain rigid with each plate.
// Inner plates, keepers, axle, XT60 and workpiece never receive transforms.

const ORIGIN = Object.freeze([0.0, 0.0, 0.0]);
const AXIS = Object.freeze([1.0, 0.0, 0.0]);
const PATHS = Object.freeze({
  upright: Object.freeze({ open: [7.0, -18.9852813742], end: [7.0, -8.4] }),
  bottom: Object.freeze({ open: [-19.4852813742, 7.5], end: [-8.9, 7.5] }),
  diagonal: Object.freeze({ open: [7.0, 7.5], end: [-0.4849242405, 0.0150757595] }),
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

function pingPong(elapsedSec, durationSec = 6.0) {
  const duration = Math.max(Number(durationSec) || 6.0, Number.EPSILON);
  const phase = (((Number(elapsedSec) || 0.0) % duration) + duration) % duration / duration;
  return phase <= 0.5 ? phase * 2.0 : (1.0 - phase) * 2.0;
}

const definition = {
  manifest: {
    schemaVersion: 1,
    step: { path: "cad/p18_r1_compact_counter_twist/p18_r1_full_motion.step" },
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
    const travel = clamp01(params.open_to_end);
    const thetaDeg = 45.0 * travel;
    effects.transform("left_outer", { rotate: { axis: AXIS, origin: ORIGIN, angleDeg: -thetaDeg } });
    effects.transform("right_outer", { rotate: { axis: AXIS, origin: ORIGIN, angleDeg: thetaDeg } });
    for (const [name, path] of Object.entries(PATHS)) {
      const translation = [0.0, (path.end[0] - path.open[0]) * travel, (path.end[1] - path.open[1]) * travel];
      effects.transform(`${name}_rod`, { translate: translation });
      effects.transform(`left_${name}_cap`, { translate: translation });
      effects.transform(`right_${name}_cap`, { translate: translation });
    }
  },
};

export default definition;
