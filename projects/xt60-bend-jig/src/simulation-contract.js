import { MECHANISM, positionIndex, solveMechanism, validateClosedMechanism } from "./mechanism-math.js";

export const PHASES = Object.freeze(["loaded", "positioned", "clamped", "soldering", "cooling", "released"]);

export const PHASE_LABELS = Object.freeze({
  loaded: "Wire loaded",
  positioned: "Supports positioned",
  clamped: "Forming rod closed",
  soldering: "Soldering",
  cooling: "Holding / cooling",
  released: "Released",
});

export const PHASE_NOTES = Object.freeze({
  loaded: "The lead is straight and its arclength is fixed. The diagonal forming rod is fully retracted.",
  positioned: "The upper and lower reaction rods are locked at the selected tangent points.",
  clamped: "Both ends of the forming rod translate together through parallel 45° guide slots.",
  soldering: "The solver reports tangency at all three rods and a 90° centerline bend.",
  cooling: "The forming rod stays at the mathematically closed position while the joint cools.",
  released: "The rod retracts along the same straight slot; only the springback estimate changes the wire angle.",
});

export const WIRE_GAUGES = Object.freeze({
  12: Object.freeze({ label: "12 AWG", diameter: 4.3 }),
  14: Object.freeze({ label: "14 AWG", diameter: 3.5 }),
});

export const DEFAULT_STATE = Object.freeze({
  phase: "clamped",
  phaseProgress: 1,
  upperRodPosition: 3,
  lowerRodPosition: 3,
  wireLength: 44,
  springback: 12,
  wireGauge: 12,
});

export function clamp(value, min = 0, max = 1) {
  return Math.min(max, Math.max(min, Number(value) || 0));
}

export function smoothstep(value) {
  const x = clamp(value);
  return x * x * (3 - 2 * x);
}

export function phasePose(phase, phaseProgress = 1, springback = 10) {
  const t = smoothstep(phaseProgress);
  const retention = 1 - clamp(springback, 0, 100) / 100;
  switch (phase) {
    case "loaded": return { clamp: 0, heat: 0, bend: 0, retention: 0 };
    case "positioned": return { clamp: 0, heat: 0, bend: 0, retention: 0 };
    case "clamped": return { clamp: t, heat: 0, bend: t, retention: 0 };
    case "soldering": return { clamp: 1, heat: t, bend: 1, retention: 0 };
    case "cooling": return { clamp: 1, heat: 1 - t, bend: 1, retention: t * retention };
    case "released": return { clamp: 1 - t, heat: 0, bend: 1 - t * (1 - retention), retention };
    default: return { clamp: 0, heat: 0, bend: 0, retention: 0 };
  }
}

export function mechanismSolution(state = DEFAULT_STATE, pose = phasePose(state.phase, state.phaseProgress, state.springback)) {
  const wire = WIRE_GAUGES[state.wireGauge] || WIRE_GAUGES[12];
  return solveMechanism({
    upperRodPosition: state.upperRodPosition,
    lowerRodPosition: state.lowerRodPosition,
    wireLength: state.wireLength,
    wireDiameter: wire.diameter,
    clampAmount: pose.clamp,
    bendAmount: pose.bend,
  });
}

export function bendMetrics(state = DEFAULT_STATE) {
  const wire = WIRE_GAUGES[state.wireGauge] || WIRE_GAUGES[12];
  const validation = validateClosedMechanism({
    upperRodPosition: state.upperRodPosition,
    lowerRodPosition: state.lowerRodPosition,
    wireLength: state.wireLength,
    wireDiameter: wire.diameter,
  });
  const solved = validation.solved;
  const springback = clamp(state.springback, 0, 100);
  const retainedAngle = 90 - springback * .35;

  let severity = "ok";
  let message = "PASS: 3/3 tangencies, 90.0° bend, conserved wire length, zero modeled end skew.";
  if (!validation.checks.wireLongEnough) {
    severity = "danger";
    message = `FAIL: ${Number(state.wireLength).toFixed(0)} mm is too short for upper position ${solved.upperIndex}; minimum ${solved.minimumWireLength.toFixed(1)} mm.`;
  } else if (!validation.valid) {
    severity = "danger";
    const failed = Object.entries(validation.checks).filter(([, pass]) => !pass).map(([name]) => name).join(", ");
    message = `FAIL: ${failed}.`;
  } else if (solved.wireLengthMargin < 4) {
    severity = "warning";
    message = `PASS WITH LOW MARGIN: only ${solved.wireLengthMargin.toFixed(1)} mm remains above the upper reaction contact.`;
  }

  return {
    rodCount: 3,
    rodDiameter: MECHANISM.rodRadius * 2,
    rodLength: MECHANISM.rodLength,
    boreDiameter: MECHANISM.boreDiameter,
    clearance: MECHANISM.boreDiameter - MECHANISM.rodRadius * 2,
    wireDiameter: wire.diameter,
    bendRadius: MECHANISM.bendRadius,
    minimumWireLength: solved.minimumWireLength,
    wireLength: Number(state.wireLength),
    wireLengthMargin: solved.wireLengthMargin,
    closedTravel: MECHANISM.openStroke,
    retainedAngle,
    springback,
    upperIndex: positionIndex(state.upperRodPosition),
    lowerIndex: positionIndex(state.lowerRodPosition),
    contactGaps: solved.contactGaps,
    maxContactError: Math.max(...Object.values(solved.contactGaps).map(Math.abs)),
    renderedLengthError: Math.abs(solved.wire.renderedLengthError),
    closedBendAngle: solved.wire.angleDegrees,
    modeledEndSkew: solved.synchronizedEnds.skew,
    rodSpanMargin: solved.rodSpanMargin,
    validation: validation.checks,
    severity,
    message,
  };
}
