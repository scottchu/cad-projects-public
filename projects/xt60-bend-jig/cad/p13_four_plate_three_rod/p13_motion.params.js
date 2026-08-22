// Review-only P13 rigid-motion sidecar. This file is deliberately standalone:
// the CAD Viewer serves only the module declared by p13_motion.step.py.

export const MOTION_CONSTANTS = Object.freeze({
  lockedAngleDeg: 27.0,
  riseEndDeg: 22.0,
  contactStroke: 3.7642135623730946,
  wirePreload: 0.25,
  commonStroke: 4.014213562373095,
  shaftOrigin: Object.freeze([0.0, -2.096372644586, 27.903627355414]),
  shaftAxis: Object.freeze([1.0, 0.0, 0.0]),
  lockedCenters: Object.freeze({
    upright: Object.freeze([-3.9, 42.0]),
    bottom: Object.freeze([12.0, 26.1]),
    diagonal: Object.freeze([4.51507575950825, 34.51507575950825]),
  }),
  guideDirections: Object.freeze({
    upright: Object.freeze([1.0, 0.0]),
    bottom: Object.freeze([0.0, 1.0]),
    diagonal: Object.freeze([-Math.SQRT1_2, -Math.SQRT1_2]),
  }),
});

const ROD_NAMES = Object.freeze(["upright", "bottom", "diagonal"]);

function clamp01(value) {
  const number = Number(value);
  return Math.min(Math.max(Number.isFinite(number) ? number : 0.0, 0.0), 1.0);
}

function smoothstep01(value) {
  const t = clamp01(value);
  return 3.0 * t * t - 2.0 * t * t * t;
}

export function solveMotion(motion) {
  const normalizedMotion = clamp01(motion);
  const thetaDeg = MOTION_CONSTANTS.lockedAngleDeg * normalizedMotion;
  const travel = thetaDeg <= MOTION_CONSTANTS.riseEndDeg
    ? MOTION_CONSTANTS.contactStroke * smoothstep01(thetaDeg / MOTION_CONSTANTS.riseEndDeg)
    : MOTION_CONSTANTS.contactStroke + MOTION_CONSTANTS.wirePreload * smoothstep01(
      (thetaDeg - MOTION_CONSTANTS.riseEndDeg)
      / (MOTION_CONSTANTS.lockedAngleDeg - MOTION_CONSTANTS.riseEndDeg),
    );
  const remaining = MOTION_CONSTANTS.commonStroke - travel;
  const centers = {};
  const translations = {};

  for (const name of ROD_NAMES) {
    const locked = MOTION_CONSTANTS.lockedCenters[name];
    const guide = MOTION_CONSTANTS.guideDirections[name];
    const openCenter = [
      locked[0] - guide[0] * MOTION_CONSTANTS.commonStroke,
      locked[1] - guide[1] * MOTION_CONSTANTS.commonStroke,
    ];
    const center = [
      locked[0] - guide[0] * remaining,
      locked[1] - guide[1] * remaining,
    ];
    centers[name] = center;
    translations[name] = [0.0, center[0] - openCenter[0], center[1] - openCenter[1]];
  }

  return {
    motion: normalizedMotion,
    thetaDeg,
    travel,
    centers,
    translations,
    shaftOrigin: [...MOTION_CONSTANTS.shaftOrigin],
    shaftAxis: [...MOTION_CONSTANTS.shaftAxis],
  };
}

export function loopMotion(elapsedSeconds, durationSeconds = 6.0) {
  const duration = Math.max(Number(durationSeconds) || 6.0, Number.EPSILON);
  const elapsed = Number.isFinite(Number(elapsedSeconds)) ? Number(elapsedSeconds) : 0.0;
  const phase = ((elapsed % duration) + duration) % duration / duration;
  return phase <= 0.5 ? 2.0 * phase : 2.0 * (1.0 - phase);
}

export const FEATURE_NAMES = Object.freeze({
  fixed_left_plate: "motion_fixed_left_plate",
  fixed_right_plate: "motion_fixed_right_plate",
  fixed_shaft_keeper: "motion_fixed_shaft_keeper",
  fixed_workpiece: "motion_fixed_workpiece",
  rotating_left_cam: "motion_rotating_left_cam",
  rotating_right_actuator: "motion_rotating_right_actuator",
  rotating_shaft: "motion_rotating_shaft",
  upright_rod: "motion_upright_rod",
  upright_left_cap: "motion_upright_left_cap",
  upright_right_cap: "motion_upright_right_cap",
  bottom_rod: "motion_bottom_rod",
  bottom_left_cap: "motion_bottom_left_cap",
  bottom_right_cap: "motion_bottom_right_cap",
  diagonal_rod: "motion_diagonal_rod",
  diagonal_left_cap: "motion_diagonal_left_cap",
  diagonal_right_cap: "motion_diagonal_right_cap",
});

const FEATURES = Object.fromEntries(Object.entries(FEATURE_NAMES).map(([id, name]) => [
  id,
  { label: id.replaceAll("_", " "), names: [name] },
]));

function applyMotion(effects, motion) {
  const solved = solveMotion(motion);
  const rotate = {
    rotate: {
      axis: solved.shaftAxis,
      origin: solved.shaftOrigin,
      angleDeg: solved.thetaDeg,
    },
  };
  effects.transform("rotating_left_cam", rotate);
  effects.transform("rotating_right_actuator", rotate);
  effects.transform("rotating_shaft", rotate);

  for (const name of ROD_NAMES) {
    const translate = { translate: solved.translations[name] };
    effects.transform(`${name}_rod`, translate);
    effects.transform(`${name}_left_cap`, translate);
    effects.transform(`${name}_right_cap`, translate);
  }
}

const definition = {
  manifest: {
    schemaVersion: 1,
    step: {
      path: "cad/p13_four_plate_three_rod/p13_motion.step",
    },
    parameters: {
      motion: {
        type: "number",
        label: "OPEN to LOCK",
        description: "Review-only motion: OPEN, first wire contact at 22 degrees, then 0.25 mm preload at LOCK.",
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
        description: "Six-second exact ping-pong: OPEN, contact, 0.25 mm wire preload, LOCK, then release.",
        durationSeconds: 6.0,
        loop: true,
        update({ elapsedSec, set }) {
          set("motion", loopMotion(elapsedSec, 6.0));
        },
      },
    },
  },
  update({ params, effects }) {
    applyMotion(effects, params.motion);
  },
};

export default definition;
