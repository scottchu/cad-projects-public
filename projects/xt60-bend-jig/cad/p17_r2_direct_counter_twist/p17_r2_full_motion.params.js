// Full P17 R2 assembly motion review. White rods and permanent caps translate
// on their frozen paths while the two outer plates rotate in opposite senses.

const ORIGIN = Object.freeze([0.0, -10.60, 17.00]);
const AXIS = Object.freeze([1.0, 0.0, 0.0]);
const PATHS = Object.freeze({
  upright: Object.freeze({ open: [-12.0, 3.0], locked: [-18.0, 13.0] }),
  bottom: Object.freeze({ open: [-5.0, -12.0], locked: [8.0, -12.0] }),
  diagonal: Object.freeze({ open: [11.5, 9.0], locked: [3.0, 1.0] }),
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

function smoothstep01(value) {
  const t = clamp01(value);
  return t * t * (3.0 - 2.0 * t);
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
      open_to_lock: {
        type: "number",
        label: "OPEN to LOCK",
        unit: "normalized",
        min: 0.0,
        max: 1.0,
        step: 0.01,
        default: 0.0,
      },
    },
    features: FEATURES,
    animations: {
      open_lock_open: {
        label: "OPEN - LOCK - OPEN",
        durationSeconds: 6.0,
        loop: true,
        update({ elapsedSec, set }) {
          set("open_to_lock", pingPong(elapsedSec));
        },
      },
    },
  },
  update({ params, effects }) {
    const travel = clamp01(params.open_to_lock);
    const thetaDeg = 32.0 * travel;
    effects.transform("left_outer", {
      rotate: { axis: AXIS, origin: ORIGIN, angleDeg: -thetaDeg },
    });
    effects.transform("right_outer", {
      rotate: { axis: AXIS, origin: ORIGIN, angleDeg: thetaDeg },
    });
    const s = smoothstep01(travel);
    for (const [name, path] of Object.entries(PATHS)) {
      const translation = [
        0.0,
        (path.locked[0] - path.open[0]) * s,
        (path.locked[1] - path.open[1]) * s,
      ];
      effects.transform(`${name}_rod`, { translate: translation });
      effects.transform(`left_${name}_cap`, { translate: translation });
      effects.transform(`right_${name}_cap`, { translate: translation });
    }
  },
};

export default definition;
