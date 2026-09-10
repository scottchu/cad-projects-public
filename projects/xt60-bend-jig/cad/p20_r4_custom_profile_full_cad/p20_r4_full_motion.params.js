// P20 R4 complete intent-preview motion. Source geometry is OPEN; one shared
// normalized state rotates the two outers oppositely and translates rods/caps.

const ORIGIN = Object.freeze([0.0, 0.0, 0.0]);
const AXIS = Object.freeze([1.0, 0.0, 0.0]);
const PATHS = Object.freeze({
  bottom: Object.freeze({ open: [-7.511545005, 14.127161486], end: [2.228077655, 5.248301944] }),
  diagonal: Object.freeze({ open: [11.313708499, 11.313708499], end: [8.478077655, -0.501698056] }),
  upright: Object.freeze({ open: [14.728077655, -6.251698056], end: [14.728077655, -6.251698056] }),
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

function state(value) {
  const u = clamp01(value);
  const rods = {};
  for (const [name, path] of Object.entries(PATHS)) {
    rods[name] = [0.0, (path.end[0] - path.open[0]) * u, (path.end[1] - path.open[1]) * u];
  }
  return { u, leftDeg: 45.0 * u, rightDeg: -45.0 * u, rods };
}

function pingPong(elapsedSec, durationSec = 8.0) {
  const duration = Math.max(Number(durationSec) || 8.0, Number.EPSILON);
  const phase = (((Number(elapsedSec) || 0.0) % duration) + duration) % duration / duration;
  return phase <= 0.5 ? phase * 2.0 : (1.0 - phase) * 2.0;
}

export default {
  manifest: {
    schemaVersion: 1,
    step: { path: "cad/p20_r4_custom_profile_full_cad/p20_r4_full_motion.step" },
    parameters: {
      open_to_end: {
        type: "number", label: "OPEN to END · preview only", unit: "normalized",
        min: 0.0, max: 1.0, step: 0.01, default: 0.0,
      },
    },
    features: FEATURES,
    animations: {
      open_end_open: {
        label: "OPEN · MID · END · OPEN", durationSeconds: 8.0, loop: true,
        update({ elapsedSec, set }) { set("open_to_end", pingPong(elapsedSec)); },
      },
    },
  },
  update({ params, effects }) {
    const current = state(params.open_to_end);
    effects.transform("left_outer", { rotate: { axis: AXIS, origin: ORIGIN, angleDeg: current.leftDeg } });
    effects.transform("right_outer", { rotate: { axis: AXIS, origin: ORIGIN, angleDeg: current.rightDeg } });
    for (const [name, translation] of Object.entries(current.rods)) {
      effects.transform(`${name}_rod`, { translate: translation });
      effects.transform(`left_${name}_cap`, { translate: translation });
      effects.transform(`right_${name}_cap`, { translate: translation });
    }
  },
};
