// Focused review motion for the corrected P17 R2 fixed purple stepped axle.
// This is self-contained because the Viewer serves only the declared sidecar.

const ORIGIN = Object.freeze([0.0, -10.60, 17.00]);
const AXIS = Object.freeze([1.0, 0.0, 0.0]);

const FEATURES = Object.freeze({
  stepped_center_axle: { names: ["motion_fixed_stepped_center_axle"] },
  left_keeper: { names: ["motion_fixed_left_keeper"] },
  right_keeper: { names: ["motion_fixed_right_keeper"] },
  left_inner_fixed_guide: { names: ["motion_fixed_left_inner"] },
  right_inner_fixed_guide: { names: ["motion_fixed_right_inner"] },
  left_outer: { names: ["motion_rotating_left_outer"] },
  right_outer: { names: ["motion_rotating_right_outer"] },
  xt60_reference: { names: ["motion_fixed_xt60_reference"] },
});

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
    step: { path: "cad/p17_r2_direct_counter_twist/p17_r2_fixed_axle_motion.step" },
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
    const thetaDeg = 32.0 * clamp01(params.open_to_lock);
    effects.transform("left_outer", {
      rotate: { axis: AXIS, origin: ORIGIN, angleDeg: -thetaDeg },
    });
    effects.transform("right_outer", {
      rotate: { axis: AXIS, origin: ORIGIN, angleDeg: thetaDeg },
    });
  },
};

export default definition;
