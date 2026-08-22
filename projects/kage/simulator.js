"use strict";

const HAND_META = Object.freeze({
  hour: Object.freeze({ color: "#3f8f87", tangentialWidth: 3.0 }),
  minute: Object.freeze({ color: "#e38b48", tangentialWidth: 2.0 }),
  second: Object.freeze({ color: "#d95d78", tangentialWidth: 1.2 }),
});

// Browser-side mirror of the manufactured P3 V3 contract.  A Python parity
// test compares every value below with p3_v3_stacked_three_motor_90deg_spec.py.
const P3_V3_REFERENCE = Object.freeze({
  architecture: "p3-v3-stacked-three-motor-90deg",
  sourceZ: 40.0,
  frameRadii: Object.freeze([141.0, 150.0]),
  carrierRadii: Object.freeze([130.5, 135.5]),
  carrierLayerBottoms: Object.freeze([2.8, 6.2, 9.6]),
  carrierLayerThickness: 3.0,
  carrierAxialGap: 0.4,
  finLaneRadii: Object.freeze({ hour: 138.1, minute: 136.5, second: 134.9 }),
  finBaseZ: Object.freeze({ hour: 2.8, minute: 6.2, second: 12.4 }),
  shadowOcclusionTopZ: Object.freeze({ hour: 5.8, minute: 9.2, second: 12.6 }),
  commonVisibleFinBaseZ: 12.6,
  finRadialThickness: 1.2,
  targetTipRadii: Object.freeze({ hour: 250.0, minute: 300.0, second: 350.0 }),
});

const PARAMETERS = Object.freeze({
  sourceZ: Object.freeze({ group: "optics", label: "LED distance from wall", variable: "sourceZ", units: "mm", meaning: "Axial point-source distance from the wall.", min: 30, max: 80, step: 0.5, default: 40, dependency: "Must remain beyond every fin tip.", affected: "LED, fin z positions, mask and cone", derivedOutput: "source plane and all axial fin heights", validation: "Reject nonpositive source distance; warn if field angle clips." }),
  hourTip: Object.freeze({ group: "fins", label: "Hour shadow tip radius", variable: "hourTip", units: "mm", meaning: "Projected hour-fin tip radius on the wall.", min: 225, max: 280, step: 1, default: 250, dependency: "Must remain beyond the projected hour-fin base.", affected: "hour fin height and wall shadow", derivedOutput: "hour fin tip z and visible shadow length", validation: "Clamped above its projected hour-fin base and the complete ring stack." }),
  minuteTip: Object.freeze({ group: "fins", label: "Minute shadow tip radius", variable: "minuteTip", units: "mm", meaning: "Projected minute-fin tip radius on the wall.", min: 270, max: 330, step: 1, default: 300, dependency: "Must remain beyond hour and the projected minute-fin base.", affected: "minute fin height and wall shadow", derivedOutput: "minute fin tip z and visible shadow length", validation: "Clamped at least 10 mm beyond hour." }),
  secondTip: Object.freeze({ group: "fins", label: "Second shadow tip radius", variable: "secondTip", units: "mm", meaning: "Projected second-fin tip radius and outer hand-shadow field.", min: 320, max: 400, step: 1, default: 350, dependency: "Must remain beyond minute and the projected second-fin base.", affected: "second fin height, wall shadow and light cone", derivedOutput: "second fin tip z and minimum field angle", validation: "Clamped at least 10 mm beyond minute; warns if the LED cone clips." }),
  finWidth: Object.freeze({ group: "fins", label: "Tangential fin width scale", variable: "finWidth", units: "×", meaning: "Scales the manufactured H/M/S widths of 3.0/2.0/1.2 mm together.", min: 0.8, max: 1.2, step: 0.05, default: 1, dependency: "Hour remains widest and second remains thinnest.", affected: "physical fin width and projected shadow width", derivedOutput: "per-hand wall-shadow width", validation: "Range-limited around the tested 0.4 mm-nozzle geometry." }),
  finThickness: Object.freeze({ group: "fins", label: "Fin radial thickness", variable: "finThickness", units: "mm", meaning: "Radial thickness of each constant-section upright fin.", min: 0.8, max: 1.6, step: 0.1, default: 1.2, dependency: "The CAD reference is three 0.4 mm nozzle lines.", affected: "fin radial footprint only", derivedOutput: "physical section and lane clearances", validation: "Warns below 1.2 mm or if the outboard lanes lose 0.4 mm clearance." }),
  ringGap: Object.freeze({ group: "fins", label: "Ring axial gap", variable: "ringGap", units: "mm", meaning: "Clear Z gap between the three 3.0 mm stacked carrier gears.", min: 0.2, max: 0.8, step: 0.1, default: 0.4, dependency: "Changes middle/top carrier planes while keeping the bottom datum fixed.", affected: "ring stack and minute/second fin bases", derivedOutput: "carrier layers, stack height and fin heights", validation: "Warns below the frozen 0.4 mm print/assembly gap." }),
  projectedMaskRadius: Object.freeze({ group: "body", label: "Central mask shadow", variable: "projectedMaskRadius", units: "mm", meaning: "Projected dark center radius used to hide fixed center hardware.", min: 110, max: 150, step: 1, default: 130, dependency: "Should remain inside the projected start of all three fins.", affected: "wall shadow and physical mask size", derivedOutput: "physical mask radius at mask plane", validation: "Warns if it covers any visible fin shadow." }),
  maskZ: Object.freeze({ group: "body", label: "Mask plane from wall", variable: "maskZ", units: "mm", meaning: "Wallward physical mask plane; distinct from the room-side glare cap.", min: 0.5, max: 2.0, step: 0.1, default: 1.5, dependency: "Must stay wallward of the bottom hour carrier at z=2.8 mm.", affected: "physical mask diameter", derivedOutput: "required physical mask radius", validation: "Clamped below the nearest fin base with 1.0 mm clearance." }),
  fieldFullAngle: Object.freeze({ group: "optics", label: "LED clear full angle", variable: "fieldFullAngle", units: "°", meaning: "Full useful wallward cone angle of the on-axis emitter; the optical solver uses half of this value.", min: 140, max: 180, step: 1, default: 180, dependency: "Must cover twice the source-axis half-angle to the outer second-hand shadow.", affected: "spotlight cone and vignetting warning", derivedOutput: "half-angle and available wall field", validation: "Clamp to 140..180 degrees; warn when less than 2 × atan(second tip / source z)." }),
  pointIntensity: Object.freeze({ group: "optics", label: "LED intensity", variable: "pointIntensity", units: "%", meaning: "Relative preview intensity; electrical power and thermal limits remain physical tests.", min: 10, max: 100, step: 1, default: 78, dependency: "Visual only; does not change geometric projection.", affected: "wall pool brightness and shadow contrast", derivedOutput: "preview luminance", validation: "Range-limited; never treated as electrical wattage." }),
  pointTemperature: Object.freeze({ group: "optics", label: "LED temperature", variable: "pointTemperature", units: "K", meaning: "Preview correlated color temperature of the wired point LED.", min: 2200, max: 4000, step: 50, default: 2700, dependency: "Color only; projection geometry is invariant.", affected: "LED and wall pool color", derivedOutput: "RGB preview color", validation: "Range-limited to warm-white study emitters." }),
  shellRadius: Object.freeze({ group: "body", label: "Frame outer radius", variable: "shellRadius", units: "mm", meaning: "Outer radius of the 300 mm structural frame used by the visualization.", min: 145, max: 165, step: 1, default: 150, dependency: "Must remain outside every fin lane.", affected: "frame diameter and side-section envelope", derivedOutput: "overall visualization diameter", validation: "Warns if it intersects the minute outboard fin lane." }),
  glareCapDiameter: Object.freeze({ group: "body", label: "Viewer glare cap", variable: "glareCapDiameter", units: "mm", meaning: "Room-side matte cap hiding direct LED glare; it is not the wall-side optical mask.", min: 18, max: 28, step: 1, default: 22, dependency: "Always placed 6 mm in front of the LED, never in its wallward cone.", affected: "room-side cap only", derivedOutput: "glare cap radius", validation: "Range-limited to the initial eye-shield study." }),
});

const PRESET_VISIBILITY = Object.freeze({
  structure: Object.freeze({ showQuartz: false, showShell: true, showPhysicalMask: true, showCarriers: true, showSourceHardware: true, showGlareCap: true, showProjectionRays: true, showHandShadows: true, showMaskShadow: true, showWallHalo: true, lightEnabled: true }),
  mechanism: Object.freeze({ showQuartz: false, showShell: false, showPhysicalMask: true, showCarriers: true, showSourceHardware: false, showGlareCap: false, showProjectionRays: false, showHandShadows: false, showMaskShadow: false, showWallHalo: false, lightEnabled: false }),
  optics: Object.freeze({ showQuartz: false, showShell: false, showPhysicalMask: true, showCarriers: true, showSourceHardware: true, showGlareCap: true, showProjectionRays: true, showHandShadows: true, showMaskShadow: true, showWallHalo: true, lightEnabled: true }),
});
const VISIBILITY_KEYS = Object.freeze(Object.keys(PRESET_VISIBILITY.structure));
function booleanControlAudit(label, variable, affectedGeometryRender) { return Object.freeze({ label, variable, units: "boolean", physicalMeaning: `Independently controls ${label.toLowerCase()}.`, min: false, max: true, allowed: [false, true], default: PRESET_VISIBILITY.structure[variable], dependency: "Independent; presets write this once but never retain authority.", affectedGeometryRender, derivedOutput: `${label} visibility or emission`, validationErrorBehavior: "Non-boolean values fall back to the declared default." }); }

const UI_CONTROL_AUDIT = Object.freeze({
  renderer: Object.freeze({ label: "Renderer", variable: "renderer", units: "enum", physicalMeaning: "Chooses interactive 3D or deterministic 2D presentation of one model.", min: null, max: null, allowed: ["3d","2d"], default: "3d", dependency: "3D requires WebGL2; falls back to 2D on failure.", affectedGeometryRender: "main viewport renderer", derivedOutput: "same scene in selected renderer", validationErrorBehavior: "Unknown values resolve to 3D; WebGL failure reports and falls back." }),
  cameraView: Object.freeze({ label: "Camera", variable: "cameraView", units: "enum", physicalMeaning: "Changes only the structural inspection camera.", min: null, max: null, allowed: ["assembly","wall","section","orbital"], default: "assembly", dependency: "Wall camera locks orbit; visibility remains independent.", affectedGeometryRender: "camera pose only", derivedOutput: "selected structural or optical composition", validationErrorBehavior: "Unknown values fall back to assembly." }),
  stackArrangement: Object.freeze({ label: "Stack arrangement", variable: "stackArrangement", units: "enum", physicalMeaning: "Shows the physical stack assembled or axially exploded.", min: null, max: null, allowed: ["assembled","exploded"], default: "assembled", dependency: "Exploded disables actual ray-traced shadow casting; analytic shadows remain nominal references.", affectedGeometryRender: "display Z only", derivedOutput: "assembled or exploded stack", validationErrorBehavior: "Unknown values fall back to assembled." }),
  opticalMode: Object.freeze({ label: "Optical mode", variable: "opticalMode", units: "enum", physicalMeaning: "Fixed hardware moves only the LED; solve targets is a design calculator that re-sizes fins.", min: null, max: null, allowed: ["fixedHardware","solveTargets"], default: "fixedHardware", dependency: "Fixed hardware is the physical simulation; solve targets is explicitly hypothetical.", affectedGeometryRender: "fin tip planes only in solve-target mode", derivedOutput: "projected shadow radii or solved fin heights", validationErrorBehavior: "Unknown values fall back to fixed hardware." }),
  timeSource: Object.freeze({ label: "Time source", variable: "timeSource", units: "enum", physicalMeaning: "Uses stored manual time or the local clock.", min: null, max: null, allowed: ["manual","realtime"], default: "manual", dependency: "Realtime disables but does not overwrite manual values.", affectedGeometryRender: "carrier and shadow rotations", derivedOutput: "manual or live angles", validationErrorBehavior: "Unknown values fall back to manual." }),
  ambienceMode: Object.freeze({ label: "Ambience", variable: "ambienceMode", units: "enum", physicalMeaning: "Switches the room presentation between daylight material reading and evening shadow contrast.", min: null, max: null, allowed: ["day","evening"], default: "day", dependency: "Does not alter optical dimensions, time or component visibility.", affectedGeometryRender: "wall, room exposure, halo and shadow presentation", derivedOutput: "daylight or evening room composition", validationErrorBehavior: "Unknown values fall back to day." }),
  showQuartz: booleanControlAudit("Quartz movement", "showQuartz", "quartz envelope only"),
  showShell: booleanControlAudit("Outer shell", "showShell", "open shell only"),
  showPhysicalMask: booleanControlAudit("Physical mask", "showPhysicalMask", "wall-side physical mask only"),
  showCarriers: booleanControlAudit("Orbital carriers + fins", "showCarriers", "three carrier groups only"),
  showSourceHardware: booleanControlAudit("LED hardware", "showSourceHardware", "LED mesh only"),
  showGlareCap: booleanControlAudit("Glare cap", "showGlareCap", "glare cap only"),
  showProjectionRays: booleanControlAudit("Projection rays", "showProjectionRays", "ray helper only"),
  showHandShadows: booleanControlAudit("Hand shadows", "showHandShadows", "three analytic hand shadows only"),
  showMaskShadow: booleanControlAudit("Mask shadow", "showMaskShadow", "analytic central mask shadow only"),
  showWallHalo: booleanControlAudit("Wall halo", "showWallHalo", "analytic wall halo only"),
  lightEnabled: booleanControlAudit("LED emission", "lightEnabled", "SpotLight and halo emission only"),
  manualHour: Object.freeze({ label: "Hour", variable: "manualHour", units: "h", physicalMeaning: "Manual clock hour used when real time is off.", min: 0, max: 23, allowed: null, default: 10, dependency: "Ignored while real-time mode is enabled.", affectedGeometryRender: "hour carrier angle", derivedOutput: "hour angle including minute fraction", validationErrorBehavior: "Clamp to 0..23." }),
  manualMinute: Object.freeze({ label: "Minute", variable: "manualMinute", units: "min", physicalMeaning: "Manual clock minute used when real time is off.", min: 0, max: 59, allowed: null, default: 10, dependency: "Ignored while real-time mode is enabled.", affectedGeometryRender: "minute and hour carrier angles", derivedOutput: "minute angle including second fraction", validationErrorBehavior: "Clamp to 0..59." }),
  manualSecond: Object.freeze({ label: "Second", variable: "manualSecond", units: "s", physicalMeaning: "Manual clock second used when real time is off.", min: 0, max: 59, allowed: null, default: 35, dependency: "Ignored while real-time mode is enabled.", affectedGeometryRender: "second, minute and hour carrier angles", derivedOutput: "second carrier angle", validationErrorBehavior: "Clamp to 0..59." }),
});

const DEFAULT_STATE = Object.freeze({ ...Object.fromEntries(Object.entries(PARAMETERS).map(([key, item]) => [key, item.default])), ...Object.fromEntries(Object.entries(UI_CONTROL_AUDIT).map(([key, item]) => [key, item.default])) });
const state = { ...DEFAULT_STATE };
const MASK_FIN_CLEARANCE = 1.0;

function positive(name, value) { const number = Number(value); if (!(number > 0)) throw new Error(`${name} must be positive`); return number; }
function plane(sourceZ, z, allowWall = false) { const source = positive("source z", sourceZ); const point = Number(z); if (!(point >= (allowWall ? 0 : Number.EPSILON) && point < source)) throw new Error(`plane z must obey ${allowWall ? "0 <=" : "0 <"} z < source z`); return [source, point]; }
function projectedRadius(sourceZ, finRadius, pointZ) { const [source, point] = plane(sourceZ, pointZ); const radius = Number(finRadius); if (radius < 0) throw new Error("fin radius cannot be negative"); return radius * source / (source - point); }
function finZForProjectedRadius(sourceZ, finRadius, wallRadius) { const source = positive("source z", sourceZ); const radius = positive("fin radius", finRadius); const target = positive("projected radius", wallRadius); if (target <= radius) throw new Error("projected radius must exceed fin radius"); return source * (1 - radius / target); }
function finShadowInterval(sourceZ, finRadius, baseZ, tipZ) { if (!(Number(tipZ) > Number(baseZ))) throw new Error("fin tip z must exceed base z"); const startRadius = projectedRadius(sourceZ, finRadius, baseZ); const tipRadius = projectedRadius(sourceZ, finRadius, tipZ); return { startRadius, tipRadius, shadowLength: tipRadius - startRadius }; }
function projectedTangentialWidth(sourceZ, physicalWidth, pointZ) { const [source, point] = plane(sourceZ, pointZ); const width = Number(physicalWidth); if (width < 0) throw new Error("physical width cannot be negative"); return width * source / (source - point); }
function projectedMaskRadius(sourceZ, maskRadius, maskZ) { return projectedRadius(sourceZ, maskRadius, maskZ); }
function requiredMaskRadius(sourceZ, projectedRadiusValue, maskZ) { const [source, point] = plane(sourceZ, maskZ); const projected = Number(projectedRadiusValue); if (projected < 0) throw new Error("projected radius cannot be negative"); return projected * (source - point) / source; }
function coneRadius(sourceZ, projectedWallRadius, planeZ) { const [source, point] = plane(sourceZ, planeZ, true); const radius = Number(projectedWallRadius); if (radius < 0) throw new Error("wall radius cannot be negative"); return radius * (source - point) / source; }
function baffleClearRadius(distanceFromSource, halfAngleDegrees, margin) { const distance = Number(distanceFromSource), angle = Number(halfAngleDegrees), pad = Number(margin); if (distance < 0 || pad < 0 || !(angle > 0 && angle < 90)) throw new Error("invalid baffle geometry"); return distance * Math.tan(angle * Math.PI / 180) + pad; }
function radialEnvelopeClearance(innerEnvelope, outerEnvelope) { const [a0, a1] = innerEnvelope.map(Number), [b0, b1] = outerEnvelope.map(Number); if (Math.min(a0, b0) < 0 || a0 > a1 || b0 > b1) throw new Error("invalid radial envelope"); return b0 - a1; }
function projectPointToWall(source, point) { const [sx,sy,sz]=source.map(Number),[px,py,pz]=point.map(Number); plane(sz,pz); const scale=sz/(sz-pz); return {x:sx+scale*(px-sx),y:sy+scale*(py-sy),scale,sourceAxisOffsetWarning:Math.abs(sx)>1e-12||Math.abs(sy)>1e-12}; }
function carrierRadii(carrierPitch, hourRadius = 30) { const pitch = Number(carrierPitch), hour = Number(hourRadius); if (!(pitch > 0) || !(hour > 0)) throw new Error("carrier pitch and hour radius must be positive"); return { hour, minute: hour + pitch, second: hour + 2 * pitch }; }
function ledNearestFinGap(sourceZ, fins) { const source = positive("source z", sourceZ); const tipPlanes = Object.values(fins || {}).map(fin => Number(fin.tipZ)); if (!tipPlanes.length || tipPlanes.some(value => !Number.isFinite(value))) throw new Error("finite fin tip planes are required"); return source - Math.max(...tipPlanes); }
function opticalDepth(sourceZ, glareCapOffset = 6) { return positive("source z", sourceZ) + positive("glare cap offset", glareCapOffset); }
function formatClearanceReadout(clearances) { return `${Number(clearances.carrierHour).toFixed(2)} / ${Number(clearances.hourMinute).toFixed(2)} / ${Number(clearances.minuteFrame).toFixed(2)} mm`; }
function fullAngleToHalfAngle(fullAngleDegrees) {
  const audit = PARAMETERS.fieldFullAngle;
  const value = Number(fullAngleDegrees);
  const normalized = Number.isFinite(value) ? Math.max(audit.min, Math.min(audit.max, value)) : audit.default;
  return normalized / 2;
}

function clockAngles(input = state, now = new Date()) {
  const realtime = input.timeSource === "realtime";
  const hour = realtime ? now.getHours() : input.manualHour;
  const minute = realtime ? now.getMinutes() : input.manualMinute;
  const second = realtime ? now.getSeconds() + now.getMilliseconds() / 1000 : input.manualSecond;
  const minuteValue = minute + second / 60;
  const hourValue = (hour % 12) + minuteValue / 60;
  return { hourAngle: hourValue * Math.PI / 6, minuteAngle: minuteValue * Math.PI / 30, secondAngle: second * Math.PI / 30 };
}

function kelvinToRgb(kelvin) {
  const t = Math.max(10, Math.min(400, Number(kelvin) / 100)); let r, g, b;
  if (t <= 66) { r = 255; g = 99.4708025861 * Math.log(t) - 161.1195681661; b = t <= 19 ? 0 : 138.5177312231 * Math.log(t - 10) - 305.0447927307; }
  else { r = 329.698727446 * Math.pow(t - 60, -0.1332047592); g = 288.1221695283 * Math.pow(t - 60, -0.0755148492); b = 255; }
  return [r, g, b].map(value => Math.max(0, Math.min(255, Math.round(value))));
}

function normalizedState(input = state) {
  const next = { ...input };
  for (const [key, audit] of Object.entries(PARAMETERS)) {
    const value = Number(next[key] ?? audit.default);
    next[key] = Number.isFinite(value) ? Math.max(audit.min, Math.min(audit.max, value)) : audit.default;
  }
  for (const key of ["renderer", "cameraView", "stackArrangement", "opticalMode", "timeSource", "ambienceMode"]) {
    const audit = UI_CONTROL_AUDIT[key];
    next[key] = audit.allowed.includes(next[key]) ? next[key] : audit.default;
  }
  for (const key of VISIBILITY_KEYS) next[key] = typeof next[key] === "boolean" ? next[key] : UI_CONTROL_AUDIT[key].default;
  next.manualHour = Math.max(0, Math.min(23, Number(next.manualHour ?? UI_CONTROL_AUDIT.manualHour.default) || 0));
  next.manualMinute = Math.max(0, Math.min(59, Number(next.manualMinute ?? UI_CONTROL_AUDIT.manualMinute.default) || 0));
  next.manualSecond = Math.max(0, Math.min(59, Number(next.manualSecond ?? UI_CONTROL_AUDIT.manualSecond.default) || 0));
  const baseZ = finBasePlanes(next.ringGap);
  if (next.opticalMode === "solveTargets") {
    const commonTop = commonVisibleFinBaseZ(next.ringGap);
    const minimumTargetForVisibleBlade = radius => projectedRadius(next.sourceZ, radius, commonTop + 0.20);
    next.hourTip = Math.max(next.hourTip, minimumTargetForVisibleBlade(P3_V3_REFERENCE.finLaneRadii.hour));
    next.minuteTip = Math.max(next.minuteTip, minimumTargetForVisibleBlade(P3_V3_REFERENCE.finLaneRadii.minute), next.hourTip + 10);
    next.secondTip = Math.max(next.secondTip, minimumTargetForVisibleBlade(P3_V3_REFERENCE.finLaneRadii.second), next.minuteTip + 10);
  }
  const nearestFinBase = Math.min(...Object.values(baseZ));
  const maximumSafeMaskZ = Math.min(PARAMETERS.maskZ.max, nearestFinBase - MASK_FIN_CLEARANCE);
  next.maskZ = Math.max(PARAMETERS.maskZ.min, Math.min(next.maskZ, maximumSafeMaskZ));
  return next;
}

function applyPreset(input, presetName) {
  const preset = PRESET_VISIBILITY[presetName];
  if (!preset) throw new RangeError(`Unknown visibility preset: ${presetName}`);
  return { ...input, ...preset };
}

function finBasePlanes(ringGap = P3_V3_REFERENCE.carrierAxialGap) {
  const gap = Number(ringGap);
  if (!(gap >= 0)) throw new Error("ring axial gap cannot be negative");
  const pitch = P3_V3_REFERENCE.carrierLayerThickness + gap;
  return {
    hour: P3_V3_REFERENCE.carrierLayerBottoms[0],
    minute: P3_V3_REFERENCE.carrierLayerBottoms[0] + pitch,
    second: P3_V3_REFERENCE.carrierLayerBottoms[0] + 2 * pitch + P3_V3_REFERENCE.carrierLayerThickness - 0.2,
  };
}

function commonVisibleFinBaseZ(ringGap = P3_V3_REFERENCE.carrierAxialGap) {
  const gap = Number(ringGap);
  if (!(gap >= 0)) throw new Error("ring axial gap cannot be negative");
  return P3_V3_REFERENCE.carrierLayerBottoms[0]
    + 3 * P3_V3_REFERENCE.carrierLayerThickness
    + 2 * gap;
}

function buildModel(input = state) {
  const s = normalizedState(input);
  const radii = { ...P3_V3_REFERENCE.finLaneRadii };
  const basePlanes = finBasePlanes(s.ringGap);
  const commonTop = commonVisibleFinBaseZ(s.ringGap);
  const fins = {};
  for (const [name, meta] of Object.entries(HAND_META)) {
    const radius = radii[name];
    const baseZ = basePlanes[name];
    const referenceTipZ = finZForProjectedRadius(P3_V3_REFERENCE.sourceZ, radius, P3_V3_REFERENCE.targetTipRadii[name]);
    const tipZ = s.opticalMode === "fixedHardware" ? referenceTipZ : finZForProjectedRadius(s.sourceZ, radius, s[`${name}Tip`]);
    const target = projectedRadius(s.sourceZ, radius, tipZ);
    if (!(tipZ > commonTop)) throw new Error(`${name} target does not clear the complete carrier stack`);
    const carrierBaseZ = name === "hour" ? basePlanes.hour : name === "minute" ? basePlanes.minute : basePlanes.minute + P3_V3_REFERENCE.carrierLayerThickness + s.ringGap;
    const carrierTopZ = carrierBaseZ + P3_V3_REFERENCE.carrierLayerThickness;
    const interval = finShadowInterval(s.sourceZ, radius, carrierTopZ, tipZ);
    const stemWidth = meta.tangentialWidth * s.finWidth;
    fins[name] = {
      orientation: "constant-radius-rectangular-axial-upright-fin",
      carrierInnerRadius: P3_V3_REFERENCE.carrierRadii[0],
      carrierOuterRadius: P3_V3_REFERENCE.carrierRadii[1],
      carrierBaseZ,
      carrierThickness: P3_V3_REFERENCE.carrierLayerThickness,
      radius, baseZ, tipZ, height: tipZ - baseZ,
      shadowOcclusionTopZ: carrierTopZ,
      visibleBaseZ: commonTop,
      visibleHeight: tipZ - commonTop,
      projectedStart: interval.startRadius, projectedTip: interval.tipRadius, projectedLength: interval.shadowLength,
      stemWidth, crownWidth: stemWidth, crownHeight: tipZ - baseZ, crownStyle: "flat",
      projectedBaseWidth: projectedTangentialWidth(s.sourceZ, stemWidth, carrierTopZ),
      projectedCrownBaseWidth: 0,
      projectedTipWidth: projectedTangentialWidth(s.sourceZ, stemWidth, tipZ),
    };
  }
  const topFootprintOuter = radii.second + s.finThickness / 2;
  const clearanceCarrierHour = radii.minute - s.finThickness / 2 - topFootprintOuter;
  const clearanceHourMinute = radii.hour - s.finThickness / 2 - (radii.minute + s.finThickness / 2);
  const clearanceMinuteFrame = P3_V3_REFERENCE.frameRadii[0] - (radii.hour + s.finThickness / 2);
  if (Math.min(clearanceCarrierHour, clearanceHourMinute, clearanceMinuteFrame) < -1e-9) throw new Error("derived outboard fin lanes intersect");
  const maskPhysicalRadius = requiredMaskRadius(s.sourceZ, s.projectedMaskRadius, s.maskZ);
  const fieldHalfAngle = fullAngleToHalfAngle(s.fieldFullAngle);
  const outerProjectedTip = Math.max(...Object.values(fins).map(fin => fin.projectedTip));
  const requiredFieldHalfAngle = Math.atan(outerProjectedTip / s.sourceZ) * 180 / Math.PI;
  const requiredFieldFullAngle = requiredFieldHalfAngle * 2;
  const shellLipZ = 0;
  const nearestFinGap = ledNearestFinGap(s.sourceZ, fins);
  const warnings = [];
  if (s.projectedMaskRadius >= Math.min(...Object.values(fins).map(fin => fin.projectedStart))) warnings.push("Central mask overlaps a visible fin-shadow start.");
  if (s.fieldFullAngle < requiredFieldFullAngle) warnings.push(`LED cone is too narrow for the ${outerProjectedTip.toFixed(0)} mm outer shadow radius.`);
  if (s.finThickness < P3_V3_REFERENCE.finRadialThickness) warnings.push("Fin radial thickness is below the frozen three-line 1.2 mm CAD value.");
  if (s.ringGap < P3_V3_REFERENCE.carrierAxialGap) warnings.push("Ring axial gap is below the frozen 0.4 mm print/assembly value.");
  if (Math.min(clearanceCarrierHour, clearanceHourMinute, clearanceMinuteFrame) < 0.4) warnings.push("Outboard fin lane clearance is below 0.4 mm.");
  if (Number(input.maskZ ?? PARAMETERS.maskZ.default) > s.maskZ + 1e-9) warnings.push("Mask plane moved wallward to preserve 1.0 mm fin-base clearance.");
  if (nearestFinGap < 12) warnings.push("LED is too close to the nearest fin for emitter/heatsink/aperture packaging.");
  if (s.maskZ >= Math.min(...Object.values(fins).map(fin => fin.baseZ))) warnings.push("Mask plane must stay wallward of every upright-fin base.");
  return { architecture: P3_V3_REFERENCE.architecture, opticalMode: s.opticalMode, flatXYBladesAllowed: false, wallZ: 0, sourceZ: s.sourceZ, opticalDepth: opticalDepth(s.sourceZ), glareCapOffset: 6, maskZ: s.maskZ, maskFinClearance: Math.min(...Object.values(fins).map(fin => fin.baseZ)) - s.maskZ, projectedMaskRadius: s.projectedMaskRadius, maskPhysicalRadius, finProfileScale: s.finWidth, finTangentialWidth: s.finWidth, finRadialThickness: s.finThickness, ringGap: s.ringGap, commonVisibleFinBaseZ: commonTop, carrierLayerThickness: P3_V3_REFERENCE.carrierLayerThickness, carrierLayers: { hour: [basePlanes.hour, basePlanes.hour + 3], minute: [basePlanes.minute, basePlanes.minute + 3], second: [basePlanes.minute + 3 + s.ringGap, basePlanes.minute + 6 + s.ringGap] }, carrierRadii: radii, carrierAnnulus: [...P3_V3_REFERENCE.carrierRadii], frameRadii: [...P3_V3_REFERENCE.frameRadii], nearestFinGap, fieldFullAngle: s.fieldFullAngle, fieldHalfAngle, shellRadius: s.shellRadius, shellLipZ, glareCapDiameter: s.glareCapDiameter, requiredFieldFullAngle, requiredFieldHalfAngle, clearances: { carrierHour: clearanceCarrierHour, hourMinute: clearanceHourMinute, minuteFrame: clearanceMinuteFrame, topCarrierEdge: P3_V3_REFERENCE.carrierRadii[1] - topFootprintOuter }, fins, warnings };
}

function observableSignature(input = state) {
  const model = buildModel(input);
  const angles = clockAngles(input, new Date(2026, 7, 11, 12, 34, 56, 0));
  return { renderer: input.renderer, cameraView: input.cameraView, stackArrangement: input.stackArrangement, opticalMode: model.opticalMode, timeSource: input.timeSource, ambienceMode: input.ambienceMode, ...Object.fromEntries(VISIBILITY_KEYS.map(key => [key, input[key]])), sourceZ: model.sourceZ, opticalDepth: model.opticalDepth, maskPhysicalRadius: model.maskPhysicalRadius, finWidth: model.finProfileScale, finThickness: model.finRadialThickness, ringGap: model.ringGap, hourRadius: model.carrierRadii.hour, minuteRadius: model.carrierRadii.minute, secondRadius: model.carrierRadii.second, nearestFinGap: model.nearestFinGap, fieldFullAngle: model.fieldFullAngle, fieldHalfAngle: model.fieldHalfAngle, shellRadius: model.shellRadius, shellLipZ: model.shellLipZ, glareCapDiameter: model.glareCapDiameter, intensity: input.pointIntensity, temperature: input.pointTemperature, hourBase: model.fins.hour.baseZ, hourTip: model.fins.hour.tipZ, minuteTip: model.fins.minute.tipZ, secondTip: model.fins.second.tipZ, hourWidth: model.fins.hour.projectedBaseWidth, minuteWidth: model.fins.minute.projectedBaseWidth, secondWidth: model.fins.second.projectedBaseWidth, clearance: model.clearances.hourMinute, hourAngle: angles.hourAngle, minuteAngle: angles.minuteAngle, secondAngle: angles.secondAngle };
}

function snapshot() { return { model: buildModel(state), angles: clockAngles(state), cameraView: state.cameraView, stackArrangement: state.stackArrangement, timeSource: state.timeSource, ambienceMode: state.ambienceMode, useRealTime: state.timeSource === "realtime", ...Object.fromEntries(VISIBILITY_KEYS.map(key => [key, state[key]])), secondEnabled: true, pointIntensity: state.pointIntensity, pointRgb: kelvinToRgb(state.pointTemperature) }; }

let threeScene = null;
let twoDFrame = 0;
let twoDClockTimer = 0;
let pageVisible = typeof document === "undefined" ? true : !document.hidden;
const $ = id => document.getElementById(id);

function buildRangeControls() {
  const targets = { optics: $("opticsControls"), fins: $("finControls"), body: $("bodyControls") };
  for (const [key, audit] of Object.entries(PARAMETERS)) {
    const label = document.createElement("label"); label.className = "range-control"; label.dataset.parameter = key;
    label.innerHTML = `<span class="range-label"><span>${audit.label}</span><output id="out-${key}">${audit.default} ${audit.units}</output></span><input id="param-${key}" type="range" min="${audit.min}" max="${audit.max}" step="${audit.step}" value="${audit.default}" aria-label="${audit.label}"><small>${audit.meaning}</small>`;
    targets[audit.group].appendChild(label);
    label.querySelector("input").addEventListener("input", event => { state[key] = Number(event.target.value); syncNormalizedState(); renderAll(); });
  }
}

function syncNormalizedState() {
  Object.assign(state, normalizedState(state));
  for (const [key, audit] of Object.entries(PARAMETERS)) {
    const input = $(`param-${key}`), output = $(`out-${key}`); if (!input || !output) continue;
    input.value = state[key]; output.textContent = `${Number(state[key]).toFixed(audit.step < 1 ? 1 : 0)} ${audit.units}`;
  }
  for (const key of ["hourTip", "minuteTip", "secondTip"]) {
    const input = $(`param-${key}`);
    if (input) input.disabled = state.opticalMode === "fixedHardware";
  }
}

function sideSectionLayout(model, logicalWidth = 420, logicalHeight = 240) {
  const left = 40, right = logicalWidth - 24, top = 22, axisY = 178;
  const radialMax = Math.max(model.shellRadius, model.maskPhysicalRadius) + 6;
  const radialScale = Math.max(.75, (axisY - top) / radialMax);
  const axialMax = model.sourceZ + 6;
  const axialScale = (right - left) / axialMax;
  const x = z => left + Number(z) * axialScale;
  const y = radius => axisY - Number(radius) * radialScale;
  return { logicalWidth, logicalHeight, left, right, top, axisY, radialMax, radialScale, axialMax, axialScale, x, y };
}

function estimatedTextBox(text, x, baselineY, fontSize = 8, padding = 1) {
  const width = String(text).length * fontSize * 0.62 + padding * 2;
  return { x: x - padding, y: baselineY - fontSize - padding, width, height: fontSize + padding * 2 };
}

function sideSectionAnnotations(model, layout) {
  const finColors = { hour: "#8fc5b5", minute: "#e7a96e", second: "#d88794" };
  const finX = { hour: 62, minute: 138, second: 214 };
  const finLabels = Object.entries(model.fins).map(([name, fin]) => {
    const textValue = `${name === "hour" ? "H" : name === "minute" ? "M" : "S"} r${fin.radius.toFixed(1)}`;
    const x = finX[name], baselineY = 202;
    const textBox = estimatedTextBox(textValue, x, baselineY);
    return { name, text: textValue, color: finColors[name], x, baselineY, swatch: { x: x - 13, y: baselineY - 8, width: 8, height: 8 }, bbox: { x: x - 13, y: textBox.y, width: textBox.x + textBox.width - (x - 13), height: Math.max(textBox.height, 9) }, leaderEnd: { x: x - 9, y: baselineY - 5 } };
  });
  const dimensions = { bbox: { x: 245, y: 3, width: 164, height: 52 } };
  const legendItems = [["H",finColors.hour],["M",finColors.minute],["S",finColors.second],["wall","#e2dbd0"],["mask","#81786e"],["LED","#ffd08a"],["glare cap","#d7cec1"]];
  let legendX = 40;
  const legend = legendItems.map(([name, color]) => {
    const textBox = estimatedTextBox(name, legendX + 11, 225);
    const item = { name, color, swatch: { x: legendX, y: 218, width: 8, height: 8 }, textX: legendX + 11, baselineY: 225, bbox: { x: legendX, y: Math.min(218, textBox.y), width: textBox.x + textBox.width - legendX, height: Math.max(226, textBox.y + textBox.height) - Math.min(218, textBox.y) } };
    legendX += name.length * 5 + 31;
    return item;
  });
  const geometry = Object.entries(model.fins).map(([name, fin]) => {
    const half = model.finRadialThickness * layout.radialScale / 2;
    return { name, x: layout.x(fin.baseZ), y: layout.y(fin.radius) - half, width: layout.x(fin.tipZ) - layout.x(fin.baseZ), height: half * 2 };
  });
  geometry.push({ name: "mask", x: layout.x(model.maskZ) - 2.5, y: layout.y(model.maskPhysicalRadius), width: 5, height: model.maskPhysicalRadius * layout.radialScale });
  geometry.push({ name: "led", x: layout.x(model.sourceZ) - 4, y: layout.y(0) - 4, width: 8, height: 8 });
  geometry.push({ name: "glare", x: layout.x(model.sourceZ + 6) - 2.5, y: layout.y(model.glareCapDiameter / 2), width: 5, height: layout.y(0) - layout.y(model.glareCapDiameter / 2) });
  return { finLabels, dimensions, legend, geometry };
}

function drawSideSection(canvas = $("sectionCanvas")) {
  const logicalWidth = 420, logicalHeight = 240, dpr = Math.min(2, globalThis.devicePixelRatio || 1);
  if (canvas.width !== Math.round(logicalWidth * dpr) || canvas.height !== Math.round(logicalHeight * dpr)) { canvas.width = Math.round(logicalWidth * dpr); canvas.height = Math.round(logicalHeight * dpr); }
  const ctx = canvas.getContext("2d"), model = buildModel(state), layout = sideSectionLayout(model, logicalWidth, logicalHeight);
  const { x, y, left, right, top, axisY, radialScale } = layout, annotations = sideSectionAnnotations(model, layout);
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, logicalWidth, logicalHeight); ctx.fillStyle = "#1c1916"; ctx.fillRect(0, 0, logicalWidth, logicalHeight);
  const line = (x0,y0,x1,y1,color,width=1,dash=[]) => { ctx.save();ctx.strokeStyle=color;ctx.lineWidth=width;ctx.setLineDash(dash);ctx.beginPath();ctx.moveTo(x0,y0);ctx.lineTo(x1,y1);ctx.stroke();ctx.restore(); };
  const label = (textValue, tx, ty, color="#e8dfd2", align="left") => { ctx.fillStyle=color;ctx.font="8px system-ui";ctx.textAlign=align;ctx.fillText(textValue,tx,ty); };

  if (state.showProjectionRays) {
    line(x(model.sourceZ), y(0), x(0), y(model.fins.hour.projectedStart), "rgba(245,187,106,.46)", 1.2);
    line(x(model.sourceZ), y(0), x(0), y(model.fins.second.projectedTip), "rgba(245,187,106,.62)", 1.2);
    for (const fin of Object.values(model.fins)) line(x(model.sourceZ), y(0), x(0), y(fin.projectedTip), "rgba(245,187,106,.25)", .8, [3,3]);
  }

  line(x(0), top, x(0), axisY + 3, "#e2dbd0", 3);
  line(left, axisY, right, axisY, "rgba(226,219,208,.34)", 1);
  label("wall z0", x(0)+4, top+8, "#f1e9dc"); label("radius r", left+4, top-5, "#bfb3a4"); label("z / wall → viewer", right, axisY+13, "#bfb3a4", "right");

  if (state.showShell) { line(x(model.shellLipZ), y(model.shellRadius), x(model.sourceZ+4), y(model.shellRadius), "rgba(238,232,221,.48)", 5); label("shell", x(model.shellLipZ), y(model.shellRadius)-5, "#d8d0c5"); }
  if (state.showQuartz) { ctx.fillStyle="#4e4943";ctx.fillRect(x(3)-2,y(29),4,29*radialScale);label("quartz",x(3)+5,y(27),"#aaa097"); }
  if (state.showPhysicalMask) { ctx.fillStyle="#81786e";ctx.fillRect(x(model.maskZ)-2.5,y(model.maskPhysicalRadius),5,model.maskPhysicalRadius*radialScale);line(x(model.maskZ),y(model.maskPhysicalRadius),x(model.maskZ)+11,y(model.maskPhysicalRadius)-7,"#c8beb0");label("physical mask",x(model.maskZ)+13,y(model.maskPhysicalRadius)-7,"#ded5c8"); }

  const colors = { hour: "#8fc5b5", minute: "#e7a96e", second: "#d88794" };
  if (state.showCarriers) for (const [name, fin] of Object.entries(model.fins)) {
    const cy = y(fin.radius), h = Math.max(3, model.finRadialThickness * radialScale), baseWidth = Math.max(3, 1.2 * layout.axialScale);
    ctx.fillStyle=colors[name];ctx.globalAlpha=.72;ctx.fillRect(x(fin.baseZ)-baseWidth/2,cy-h/2,baseWidth,h);ctx.globalAlpha=1;
    ctx.fillStyle=colors[name];ctx.globalAlpha=.28;ctx.fillRect(x(fin.baseZ),cy-h/2,Math.max(1,x(fin.shadowOcclusionTopZ)-x(fin.baseZ)),h);ctx.globalAlpha=1;
    ctx.fillStyle=colors[name];ctx.fillRect(x(fin.shadowOcclusionTopZ),cy-h/2,Math.max(1,x(fin.tipZ)-x(fin.shadowOcclusionTopZ)),h);
  }

  if (state.showSourceHardware) { ctx.fillStyle=state.lightEnabled?"#ffd08a":"#766e65";ctx.beginPath();ctx.arc(x(model.sourceZ),y(0),4,0,Math.PI*2);ctx.fill();line(x(model.sourceZ),y(0),x(model.sourceZ)-12,y(0)-10,"#ffd08a");label("LED / point source",x(model.sourceZ)-14,y(0)-11,"#ffdba5","right"); }
  if (state.showGlareCap) { const capX=x(model.sourceZ+6),capTop=y(model.glareCapDiameter/2);ctx.fillStyle="#d7cec1";ctx.fillRect(capX-2.5,capTop,5,y(0)-capTop);line(capX,capTop,capX-18,capTop-8,"#d7cec1");label("viewer glare cap",capX-20,capTop-9,"#e5ddd2","right"); }

  const dimX=252, dimY=13;ctx.fillStyle="rgba(245,239,229,.08)";ctx.fillRect(annotations.dimensions.bbox.x,annotations.dimensions.bbox.y,annotations.dimensions.bbox.width,annotations.dimensions.bbox.height);
  label(`S source-wall: ${model.sourceZ.toFixed(1)} mm`,dimX,dimY,"#eee4d7");
  label(`Ring gap: ${model.ringGap.toFixed(2)} mm`,dimX,dimY+11,"#eee4d7");
  label(`Radii H/M/S: ${model.carrierRadii.hour.toFixed(1)} / ${model.carrierRadii.minute.toFixed(1)} / ${model.carrierRadii.second.toFixed(1)} mm`,dimX,dimY+22,"#eee4d7");
  label(`LED → nearest fin: ${model.nearestFinGap.toFixed(1)} mm`,dimX,dimY+33,"#eee4d7");

  if (state.showCarriers) for (const item of annotations.finLabels) { const fin=model.fins[item.name];line(x(fin.tipZ),y(fin.radius),item.leaderEnd.x,item.leaderEnd.y,item.color,.8);ctx.fillStyle=item.color;ctx.fillRect(item.swatch.x,item.swatch.y,item.swatch.width,item.swatch.height);label(item.text,item.x,item.baselineY,item.color); }
  for(const item of annotations.legend){ctx.fillStyle=item.color;ctx.fillRect(item.swatch.x,item.swatch.y,item.swatch.width,item.swatch.height);label(item.name,item.textX,item.baselineY,"#cfc5b7");}
}

function draw2D() {
  const canvas = $("heroCanvas2d"), rect = canvas.getBoundingClientRect(), dpr = Math.min(2, window.devicePixelRatio || 1), width = Math.max(1, Math.round(rect.width)), height = Math.max(1, Math.round(rect.height));
  if (canvas.width !== width * dpr || canvas.height !== height * dpr) { canvas.width = width * dpr; canvas.height = height * dpr; }
  const ctx = canvas.getContext("2d"); ctx.setTransform(dpr,0,0,dpr,0,0); ctx.clearRect(0,0,width,height);
  if (state.cameraView !== 'wall') { drawSideSection($("sectionCanvas")); ctx.drawImage($("sectionCanvas"), 0, 0, width, height); return; }
  const model = buildModel(state), cx = width / 2, cy = height / 2, scale = Math.min(width,height) * .42 / Math.max(...Object.values(model.fins).map(fin=>fin.projectedTip)), rgb = kelvinToRgb(state.pointTemperature), intensity = state.pointIntensity / 100, evening=state.ambienceMode==="evening";
  ctx.fillStyle=evening?"#777168":"#dcd5ca";ctx.fillRect(0,0,width,height);
  if (state.showWallHalo && state.lightEnabled) { const glow = ctx.createRadialGradient(cx,cy,5,cx,cy,model.fins.second.projectedTip*scale*1.2); glow.addColorStop(0,`rgba(${rgb.join(",")},${.5*intensity})`); glow.addColorStop(1,`rgba(${rgb.join(",")},0)`); ctx.fillStyle=glow;ctx.fillRect(0,0,width,height); }
  const angles=clockAngles(state);
  if (state.showHandShadows) { for(const [name,fin] of Object.entries(model.fins)){const angle=angles[`${name}Angle`],a={x:Math.sin(angle),y:-Math.cos(angle)};ctx.strokeStyle=evening?"rgba(30,25,21,.68)":"rgba(30,25,21,.24)";ctx.lineCap=name==="second"?"butt":"round";ctx.lineWidth=Math.max(1,fin.projectedBaseWidth*scale);ctx.beginPath();ctx.moveTo(cx+a.x*fin.projectedStart*scale,cy+a.y*fin.projectedStart*scale);ctx.lineTo(cx+a.x*fin.projectedTip*scale,cy+a.y*fin.projectedTip*scale);ctx.stroke();} }
  if (state.showMaskShadow) { ctx.fillStyle="rgba(25,21,18,.9)";ctx.beginPath();ctx.arc(cx,cy,model.projectedMaskRadius*scale,0,Math.PI*2);ctx.fill(); }
  if(state.showGlareCap){ctx.fillStyle="#25231f";ctx.beginPath();ctx.arc(cx,cy,state.glareCapDiameter*.5*scale,0,Math.PI*2);ctx.fill();}
}

function updateReadouts() {
  const model=buildModel(state); $("sourceReadout").textContent=`${model.sourceZ.toFixed(1)} mm`; $("insetScale").textContent=`LED ${model.sourceZ.toFixed(0)} mm`;
  $("shadowReadout").textContent=`${state.stackArrangement==="exploded"?"NOMINAL SHADOW REFERENCE · ":""}H ${model.fins.hour.projectedStart.toFixed(0)}–${model.fins.hour.projectedTip.toFixed(0)} · M ${model.fins.minute.projectedStart.toFixed(0)}–${model.fins.minute.projectedTip.toFixed(0)} · S ${model.fins.second.projectedStart.toFixed(0)}–${model.fins.second.projectedTip.toFixed(0)} mm`;
  $("maskReadout").textContent=`r${model.projectedMaskRadius.toFixed(1)} / physical r${model.maskPhysicalRadius.toFixed(1)}`;
  $("pitchReadout").textContent=`Ring axial gap: ${model.ringGap.toFixed(2)} mm`;
  $("radiiReadout").textContent=`Radii H/M/S: ${model.carrierRadii.hour.toFixed(1)} / ${model.carrierRadii.minute.toFixed(1)} / ${model.carrierRadii.second.toFixed(1)} mm`;
  $("sourceGapReadout").textContent=`LED → nearest fin: ${model.nearestFinGap.toFixed(1)} mm`;
  $("opticalDepthReadout").textContent=`LED + glare cap depth: ${model.opticalDepth.toFixed(1)} mm`;
  $("clearanceReadout").textContent=formatClearanceReadout(model.clearances);
  $("coneRequiredReadout").textContent=`Required LED full angle: ${model.requiredFieldFullAngle.toFixed(1)}°`;
  $("coneMarginReadout").textContent=`Full-angle margin: ${(state.fieldFullAngle-model.requiredFieldFullAngle).toFixed(1)}°`;
  $("warnings").textContent=model.warnings.join(" ");
}

function renderAll() { updateReadouts(); drawSideSection(); if(state.renderer==="3d"&&threeScene) threeScene.update(snapshot()); else draw2D(); }
function syncTwoDClockTimer() { const shouldTick=state.timeSource==="realtime"&&state.renderer==="2d"&&pageVisible; if(shouldTick&&!twoDClockTimer)twoDClockTimer=setInterval(renderAll,1000); else if(!shouldTick&&twoDClockTimer){clearInterval(twoDClockTimer);twoDClockTimer=0;} }
function setCameraView(cameraView) { if(!UI_CONTROL_AUDIT.cameraView.allowed.includes(cameraView)) return; state.cameraView=cameraView; document.querySelectorAll("[data-camera-view]").forEach(button=>{const active=button.dataset.cameraView===cameraView;button.classList.toggle("is-active",active);button.setAttribute("aria-pressed",String(active));}); const labels={assembly:["STACKED MOTOR ASSEMBLY","Three same-radius geared carriers: hour bottom/outer lane, minute middle/middle lane, second top/on-ring lane."],wall:["WALL SHADOW","Analytic point-source projection using the exact manufactured fin planes."],section:["LIVE OPTICAL SECTION","Wall → stacked fins → centered point LED → room-side glare cap."],orbital:["STACKED FIN CLOSE-UP","Constant-section fins rise beyond the complete 300 mm carrier stack."]}; $("viewTitle").textContent=labels[cameraView][0];$("viewDescription").textContent=labels[cameraView][1];threeScene?.setView(cameraView);renderAll(); }
function setStackArrangement(stackArrangement) { if(!UI_CONTROL_AUDIT.stackArrangement.allowed.includes(stackArrangement)) return; state.stackArrangement=stackArrangement; document.querySelectorAll("[data-arrangement]").forEach(button=>{const active=button.dataset.arrangement===stackArrangement;button.classList.toggle("is-active",active);button.setAttribute("aria-pressed",String(active));}); renderAll(); }
function setRenderer(renderer) { state.renderer=renderer==="2d"?"2d":"3d"; const three=state.renderer==="3d"&&threeScene; threeScene?.setActive(Boolean(three)); $("heroCanvas3d").classList.toggle("is-hidden",!three);$("heroCanvas2d").classList.toggle("is-hidden",three); document.querySelectorAll("[data-arrangement],#reset3dButton").forEach(control=>{control.disabled=!three;}); ["3d","2d"].forEach(name=>{const button=$(name==="3d"?"renderer3dButton":"renderer2dButton"),active=state.renderer===name;button.classList.toggle("is-active",active);button.setAttribute("aria-pressed",String(active));});$("threeStatus").textContent=three?"THREE.JS r176 · DRAG TO ORBIT · SCROLL TO ZOOM":"2D: DECOR/WALL SHOW FACE + SHADOW · INSPECTION SHOWS SECTION";syncTwoDClockTimer();renderAll(); }

function wireUI() {
  document.querySelectorAll("[data-camera-view]").forEach(button=>button.addEventListener("click",()=>setCameraView(button.dataset.cameraView)));
  document.querySelectorAll("[data-arrangement]").forEach(button=>button.addEventListener("click",()=>setStackArrangement(button.dataset.arrangement)));
  document.querySelectorAll("[data-time-source]").forEach(button=>button.addEventListener("click",()=>setTimeSource(button.dataset.timeSource)));
  document.querySelectorAll("[data-optical-mode]").forEach(button=>button.addEventListener("click",()=>setOpticalMode(button.dataset.opticalMode)));
  $("renderer3dButton").addEventListener("click",()=>setRenderer("3d")); $("renderer2dButton").addEventListener("click",()=>setRenderer("2d")); $("reset3dButton").addEventListener("click",()=>threeScene?.resetView());
  $("presetSelect").addEventListener("change",event=>{if(!event.target.value)return;Object.assign(state,applyPreset(state,event.target.value));event.target.value="";syncVisibilityInputs();renderAll();});
  document.querySelectorAll("[data-preset]").forEach(button=>button.addEventListener("click",()=>{Object.assign(state,applyPreset(state,button.dataset.preset));syncVisibilityInputs();renderAll();}));
  document.querySelectorAll("[data-visibility]").forEach(input=>input.addEventListener("change",()=>{state[input.dataset.visibility]=input.checked;renderAll();}));
  [["manualHour",23],["manualMinute",59],["manualSecond",59]].forEach(([id,max])=>$(id).addEventListener("input",event=>{state[id]=Math.max(0,Math.min(max,Number(event.target.value)||0));renderAll();}));
  $("collapseInsetButton").addEventListener("click",()=>{const inset=$("opticalInset"),collapsed=inset.classList.toggle("is-collapsed");$("collapseInsetButton").textContent=collapsed?"+":"−";$("collapseInsetButton").setAttribute("aria-expanded",String(!collapsed));});
  $("resetButton").addEventListener("click",()=>{Object.assign(state,DEFAULT_STATE);$("presetSelect").value="";$("manualHour").value=10;$("manualMinute").value=10;$("manualSecond").value=35;syncVisibilityInputs();syncNormalizedState();setOpticalMode("fixedHardware");setTimeSource("manual");setStackArrangement("assembled");setCameraView("assembly");setRenderer("3d");});
  syncVisibilityInputs();
}

function syncVisibilityInputs() { document.querySelectorAll("[data-visibility]").forEach(input=>{input.checked=state[input.dataset.visibility];}); }
function setOpticalMode(opticalMode) { if(!UI_CONTROL_AUDIT.opticalMode.allowed.includes(opticalMode))return;state.opticalMode=opticalMode;document.querySelectorAll("[data-optical-mode]").forEach(button=>{const active=button.dataset.opticalMode===opticalMode;button.classList.toggle("is-active",active);button.setAttribute("aria-pressed",String(active));});syncNormalizedState();renderAll(); }
function setTimeSource(timeSource) { if(!UI_CONTROL_AUDIT.timeSource.allowed.includes(timeSource))return;state.timeSource=timeSource;document.querySelectorAll("[data-time-source]").forEach(button=>{const active=button.dataset.timeSource===timeSource;button.classList.toggle("is-active",active);button.setAttribute("aria-pressed",String(active));});["manualHour","manualMinute","manualSecond"].forEach(id=>{$(id).disabled=timeSource==="realtime";});syncTwoDClockTimer();renderAll(); }

function mount() {
  buildRangeControls(); syncNormalizedState(); wireUI();
  try { if (!globalThis.KageThreeScene?.mount) throw new Error("local Three.js bundle did not load"); threeScene=globalThis.KageThreeScene.mount({canvas:$("heroCanvas3d"),parent:$("heroVisual"),getSnapshot:snapshot,onError:error=>{threeScene=null;setRenderer("2d");$("threeStatus").textContent=`3D unavailable: ${error.message}`;}}); globalThis.KageThreeRuntime=threeScene; setCameraView("assembly"); setRenderer("3d"); }
  catch(error){threeScene=null;setRenderer("2d");$("threeStatus").textContent=`3D unavailable: ${error.message}`;}
  const resizeObserver=typeof ResizeObserver==="function"?new ResizeObserver(()=>{if(state.renderer==="2d")draw2D();drawSideSection();}):null;resizeObserver?.observe($("heroVisual"));
  document.addEventListener("visibilitychange",()=>{pageVisible=!document.hidden;syncTwoDClockTimer();});
  window.addEventListener("beforeunload",()=>{if(twoDClockTimer)clearInterval(twoDClockTimer);twoDClockTimer=0;threeScene?.dispose();},{once:true});
  renderAll(); syncTwoDClockTimer();
}

const API=Object.freeze({ P3_V3_REFERENCE,HAND_META,PARAMETERS,PRESET_VISIBILITY,VISIBILITY_KEYS,UI_CONTROL_AUDIT,MASK_FIN_CLEARANCE,defaults:DEFAULT_STATE,applyPreset,projectedRadius,finZForProjectedRadius,finShadowInterval,projectedTangentialWidth,projectedMaskRadius,requiredMaskRadius,coneRadius,baffleClearRadius,radialEnvelopeClearance,projectPointToWall,carrierRadii,finBasePlanes,commonVisibleFinBaseZ,ledNearestFinGap,opticalDepth,formatClearanceReadout,fullAngleToHalfAngle,clockAngles,normalizedState,buildModel,sideSectionLayout,sideSectionAnnotations,observableSignature,kelvinToRgb });
if(typeof globalThis!=="undefined")globalThis.KageSimulator=API;
if(typeof module!=="undefined"&&module.exports)module.exports=API;
if(typeof document!=="undefined"){if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",mount);else mount();}
