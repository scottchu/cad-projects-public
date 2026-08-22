export const P6 = Object.freeze({
  rodDiameter: 4,
  rodLength: 50,
  plateSize: 24,
  plateThickness: 3,
  fixedHoleDiameter: 3.9,
  serviceHoleDiameter: 4.2,
  fixedCapBore: 3.9,
  serviceCapBore: 4.1,
  capAcrossFlats: 8,
  capLength: 5,
  innerGap: 38,
  gaugeLength: 38,
  gaugeDepth: 8,
  gaugeHeight: 3,
});

export const ASSEMBLY_STEPS = Object.freeze([
  Object.freeze({ id: "exploded", short: "Parts", title: "Start at the rod ends", note: "Keep every printed part near the end where it will be installed." }),
  Object.freeze({ id: "fixed-plate", short: "Fixed plate", title: "Press the fixed plate on", note: "Push the Ø3.90 plate only 3 mm from the left rod end. Never drag it along the full 50 mm rod." }),
  Object.freeze({ id: "fixed-cap", short: "Fixed cap", title: "Lock the fixed side", note: "Press the Ø3.90 cap onto the same left end until it meets the plate." }),
  Object.freeze({ id: "service-plate", short: "Service plate", title: "Slide the loose plate on", note: "Feed the Ø4.20 service plate from the opposite rod end." }),
  Object.freeze({ id: "gauge-in", short: "38 mm gauge", title: "Set the 38 mm gap", note: "Lift the removable gauge between the inner plate faces and square both plates on a flat surface." }),
  Object.freeze({ id: "external-clamps", short: "Clamp", title: "Clamp both plates externally", note: "External clamps stop both plates rotating and lock the 38 mm spacing before the loose side is capped." }),
  Object.freeze({ id: "service-cap", short: "Service cap", title: "Retain the service side", note: "Fit the Ø4.10 cap on the right end after the plates are clamped. The cap stops outward escape; the clamps hold the gap." }),
  Object.freeze({ id: "gauge-out", short: "Remove gauge", title: "Remove the setup gauge", note: "Pull the gauge down and out. The external clamps now preserve the 38 mm spacing and squareness." }),
]);

export const DEFAULT_ASSEMBLY_STATE = Object.freeze({ step: 0, progress: 1 });

export function clamp01(value) {
  return Math.min(1, Math.max(0, Number(value) || 0));
}

export function smoothstep(value) {
  const t = clamp01(value);
  return t * t * (3 - 2 * t);
}

const FIXED_PLATE_X = -(P6.innerGap / 2 + P6.plateThickness / 2);
const SERVICE_PLATE_X = -FIXED_PLATE_X;
const FIXED_CAP_X = -(P6.innerGap / 2 + P6.plateThickness + P6.capLength / 2);
const SERVICE_CAP_X = -FIXED_CAP_X;

export const ASSEMBLED_POSITIONS = Object.freeze({
  fixedPlateX: FIXED_PLATE_X,
  servicePlateX: SERVICE_PLATE_X,
  fixedCapX: FIXED_CAP_X,
  serviceCapX: SERVICE_CAP_X,
});

const exploded = Object.freeze({
  fixedPlateX: -32,
  fixedCapX: -38,
  servicePlateX: 32,
  serviceCapX: 38,
  gaugeY: -10.5,
  gaugeZ: 24,
  fixedPlateTilt: -0.12,
  servicePlateTilt: 0.12,
  clampsZ: 34,
});

function stageTarget(step) {
  const index = Math.max(0, Math.min(ASSEMBLY_STEPS.length - 1, Math.floor(Number(step) || 0)));
  return {
    fixedPlateX: index >= 1 ? FIXED_PLATE_X : exploded.fixedPlateX,
    fixedCapX: index >= 2 ? FIXED_CAP_X : exploded.fixedCapX,
    servicePlateX: index >= 3 ? SERVICE_PLATE_X : exploded.servicePlateX,
    serviceCapX: index >= 6 ? SERVICE_CAP_X : exploded.serviceCapX,
    gaugeY: exploded.gaugeY,
    gaugeZ: index >= 4 && index < 7 ? 0 : exploded.gaugeZ,
    fixedPlateTilt: index >= 4 ? 0 : exploded.fixedPlateTilt,
    servicePlateTilt: index >= 4 ? 0 : exploded.servicePlateTilt,
    clampsZ: index >= 5 ? 0 : exploded.clampsZ,
    clampsEngaged: index >= 5,
    gaugeInstalled: index >= 4 && index < 7,
  };
}

function mix(a, b, t) { return a + (b - a) * t; }

export function assemblyPose(step = 0, progress = 1) {
  const index = Math.max(0, Math.min(ASSEMBLY_STEPS.length - 1, Math.floor(Number(step) || 0)));
  const from = stageTarget(Math.max(0, index - 1));
  const to = stageTarget(index);
  const t = index === 0 ? 1 : smoothstep(progress);
  return {
    step: index,
    fixedPlateX: mix(from.fixedPlateX, to.fixedPlateX, t),
    fixedCapX: mix(from.fixedCapX, to.fixedCapX, t),
    servicePlateX: mix(from.servicePlateX, to.servicePlateX, t),
    serviceCapX: mix(from.serviceCapX, to.serviceCapX, t),
    gaugeY: mix(from.gaugeY, to.gaugeY, t),
    gaugeZ: mix(from.gaugeZ, to.gaugeZ, t),
    fixedPlateTilt: mix(from.fixedPlateTilt, to.fixedPlateTilt, t),
    servicePlateTilt: mix(from.servicePlateTilt, to.servicePlateTilt, t),
    clampsZ: mix(from.clampsZ, to.clampsZ, t),
    clampsEngaged: index > 5 || (index === 5 && t >= 0.999),
    gaugeInstalled: index >= 4 && index < 7,
  };
}

export function assemblyMetrics(step = 0, progress = 1) {
  const pose = assemblyPose(step, progress);
  const gap = pose.servicePlateX - P6.plateThickness / 2 - (pose.fixedPlateX + P6.plateThickness / 2);
  return {
    ...P6,
    step: pose.step,
    gap,
    leftInsertionTravel: Math.abs(exploded.fixedPlateX - FIXED_PLATE_X),
    rightInsertionTravel: Math.abs(exploded.servicePlateX - SERVICE_PLATE_X),
    fixedInterference: P6.rodDiameter - P6.fixedHoleDiameter,
    serviceClearance: P6.serviceHoleDiameter - P6.rodDiameter,
    clampsEngaged: pose.clampsEngaged,
    gaugeInstalled: pose.gaugeInstalled,
  };
}
