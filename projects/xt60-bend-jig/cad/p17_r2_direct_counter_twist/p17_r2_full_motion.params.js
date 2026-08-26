// Full P17 R2 assembly motion review. White rods and permanent caps translate
// on their selected straight paths while the two outer plates rotate in
// opposite senses. Geometry travel is linear; animation time does not alter it.

const ORIGIN = Object.freeze([0.0, 3.0, 12.0]);
const AXIS = Object.freeze([1.0, 0.0, 0.0]);
const PATHS = Object.freeze({
  upright: Object.freeze({ open: [9.885, -12.6002813742], end: [9.885, -2.015] }),
  bottom: Object.freeze({ open: [-16.6002813742, 13.885], end: [-6.015, 13.885] }),
  diagonal: Object.freeze({ open: [9.885, 13.885], end: [2.4000757595, 6.4000757595] }),
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
    step: { path: "cad/p17_r2_direct_counter_twist/p17_r2_full_motion.step" },
    parameters: {
      open_to_end: {
        type: "number",
        label: "OPEN to END OF TRAVEL",
        unit: "normalized",
        min: 0.0,
        max: 1.0,
        step: 0.01,
        default: 0.0,
      },
    },
    features: FEATURES,
    animations: {
      open_end_open: {
        label: "OPEN - END - OPEN",
        durationSeconds: 6.0,
        loop: true,
        update({ elapsedSec, set }) {
          set("open_to_end", pingPong(elapsedSec));
        },
      },
    },
  },
  update({ params, effects }) {
    const travel = clamp01(params.open_to_end);
    const thetaDeg = 24.0 * travel;
    effects.transform("left_outer", {
      rotate: { axis: AXIS, origin: ORIGIN, angleDeg: -thetaDeg },
    });
    effects.transform("right_outer", {
      rotate: { axis: AXIS, origin: ORIGIN, angleDeg: thetaDeg },
    });
    for (const [name, path] of Object.entries(PATHS)) {
      const translation = [
        0.0,
        (path.end[0] - path.open[0]) * travel,
        (path.end[1] - path.open[1]) * travel,
      ];
      effects.transform(`${name}_rod`, { translate: translation });
      effects.transform(`left_${name}_cap`, { translate: translation });
      effects.transform(`right_${name}_cap`, { translate: translation });
    }
  },
};

export default definition;
