"use strict";

/*
 * KAGE keeps physical state and optical calculations independent from both its
 * Canvas2D fallback and locally bundled Three.js visualization. The same
 * contract can therefore drive the browser, CLI, tests and later CAD.
 */

const OPTICAL_DEFAULTS = Object.freeze({
  bodyDiameter: 260,
  bodyDepth: 35,
  wallGap: 45,
  shellThickness: 2,
  movementDepth: 15,
  movementEnvelopeWidth: 99,
  movementEnvelopeHeight: 99,
  hardwareOverallDepth: 34,
  mountingThickness: 2,
  p0HandWallDistance: 60,
  hourLength: 45,
  minuteLength: 70,
  secondLength: 85,
  hourWidth: 4.5,
  minuteWidth: 2.4,
  secondWidth: 0.8,
  secondEnabled: false,
  sourceHandDistance: 40,
  apertureDiameter: 1,
  pointIntensity: 78,
  pointTemperature: 2700,
  ledOffsetX: 0,
  ledOffsetY: 0,
  haloEnabled: false,
  haloTemperature: 2700,
  haloBrightness: 74,
  haloRadius: 195,
  haloSpread: 52,
  ringDiameter: 210,
  ambientLevel: 46,
  manualHour: 10,
  manualMinute: 10,
  manualSecond: 35,
  useRealTime: false,
  sweepMode: "sweep",
  showBody: false,
  showLabels: true,
  showRays: true,
  showDimensions: true,
  material: "warmWhite",
  surface: "smooth",
  movementType: "manual-concentric-ring-jig",
  view: "wall",
  stage: "p0"
});

const state = { ...OPTICAL_DEFAULTS };

const REFERENCE_FINAL_PRESET = Object.freeze({
  frontOccluderDiameter: 260,
  frontOccluderDepth: 12,
  rearPodDiameter: 150,
  rearPodDepth: 60,
  podFrontOverlap: 2,
  bodyDiameter: 260,
  bodyDepth: 70,
  wallGap: 45,
  movementDepth: 15,
  hardwareOverallDepth: 34,
  mountingThickness: 2,
  handPlaneToPodRear: 17.8,
  sourceHandDistance: 42,
  sourceZ: 104.8,
  wallZ: 0,
  sourceRecess: 10.2,
  rearOpeningDiameter: 120,
  movementEnvelopeWidth: 99,
  movementEnvelopeHeight: 99,
  apertureDiameter: 0.8,
  hourLength: 60,
  hourWidth: 9,
  hourShape: "leaf-kite",
  hourLengthMin: 58,
  hourLengthMax: 64,
  hourRootWidth: 4,
  hourMaxWidthPosition: 86,
  hourTipWidth: 1.5,
  minuteLength: 70,
  minuteShape: "blade",
  secondLength: 85,
  secondShape: "needle",
  secondEnabled: true,
  movementType: "quartz-driven-orbital-hands",
  fixedMaskZ: 60,
  fixedMaskPhysicalRadius: 55.5714285714,
  fixedMaskProjectedRadius: 130,
  requiredCarrierHideMargin: 5,
  minimumFullFieldAngle: 130,
  carrierOuterRadius: 47,
  hourPlaneZ: 61.2,
  minutePlaneZ: 62.8,
  secondPlaneZ: 64.4,
  hourCarrierInnerRadius: 38,
  hourCarrierOuterRadius: 48,
  minuteCarrierInnerRadius: 38,
  minuteCarrierOuterRadius: 48,
  secondCarrierInnerRadius: 38,
  secondCarrierOuterRadius: 48,
  exposedDriveRadius: 49.5,
  clearCenterDiameter: 36,
  carrierThickness: 1.2,
  carrierAxialGap: 0.4,
  carrierAxialPitch: 1.6,
  carrierStackDepth: 4.4,
  hourAxialOffset: 1.6,
  minuteAxialOffset: 0,
  secondAxialOffset: -1.6
});

const CONTROL_GROUPS = {
  bodyControls: [
    ["bodyDiameter", "Body diameter", 150, 400, 1, "mm"],
    ["bodyDepth", "Body depth", 15, 80, 1, "mm"],
    ["wallGap", "Body to wall", 10, 150, 1, "mm"],
    ["shellThickness", "Front shell", 1, 5, 0.1, "mm"],
    ["movementEnvelopeWidth", "Movement envelope width", 60, 120, 1, "mm"],
    ["movementEnvelopeHeight", "Movement envelope height", 60, 120, 1, "mm"],
    ["hardwareOverallDepth", "Quartz hardware overall (provisional)", 20, 45, 0.1, "mm"],
    ["mountingThickness", "Face / mounting thickness", 0.5, 9, 0.1, "mm"]
  ],
  clockControls: [
    ["movementDepth", "Quartz movement depth", 10, 30, 1, "mm"],
    ["hourLength", "Hour hand length", 20, 100, 1, "mm"],
    ["minuteLength", "Minute hand length", 30, 130, 1, "mm"],
    ["secondLength", "Second hand length", 40, 150, 1, "mm"],
    ["hourWidth", "Hour hand width", 0.5, 12, 0.1, "mm"],
    ["minuteWidth", "Minute hand width", 0.4, 6, 0.1, "mm"],
    ["secondWidth", "Second hand width", 0.2, 3, 0.1, "mm"]
  ],
  pointControls: [
    ["sourceHandDistance", "Effective source / aperture to hand", 5, 150, 1, "mm"],
    ["p0HandWallDistance", "P0 hand plane to wall", 30, 120, 1, "mm"],
    ["apertureDiameter", "Aperture diameter", 0.2, 5, 0.1, "mm"],
    ["pointIntensity", "Point LED intensity", 0, 100, 1, "%"],
    ["pointTemperature", "Point LED temperature", 2200, 4000, 50, "K"],
    ["ledOffsetX", "Horizontal LED offset", -60, 60, 1, "mm"],
    ["ledOffsetY", "Vertical LED offset", -60, 60, 1, "mm"]
  ],
  haloControls: [
    ["haloBrightness", "Halo brightness", 0, 100, 1, "%"],
    ["haloTemperature", "Halo temperature", 2200, 4000, 50, "K"],
    ["haloRadius", "Halo base radius", 100, 350, 1, "mm"],
    ["haloSpread", "Halo diffusion", 10, 100, 1, "%"],
    ["ringDiameter", "COB ring diameter", 100, 360, 1, "mm"]
  ]
};

const STAGES = {
  p0: {
    title: "Wired LED + fake blockers",
    description: "Start with one current-limited, heat-sunk wired point LED, a thin or flared aperture, and manually rotated fake blocker rings.",
    source: "WIRED POINT LED + APERTURE",
    note: "Use a constant-current driver, metal thermal path, opaque eye-safe baffle, and replaceable 0.8 / 1.0 / 1.5 mm apertures. Printed plastic is never the heatsink.",
    aim: "Can the real point source cast a readable shadow and useful wall pool?",
    parts: "Wired LED · driver · heatsink · aperture · fake blockers",
    pass: "Readable at three angles plus stable temperature and brightness",
    buy: "Buy only the wired LED bench parts",
    movement: "Manual concentric rings; no drive geometry",
    stack: ["Optional system", "No separate COB in P0", "later", "Primary optics", "Wired LED + fake blockers", "test"]
  },
  p1: {
    title: "Generic quartz timing experiment",
    description: "Keep the proven wired optics and replace the manual pivot with a generic center-shaft quartz movement and lightweight conventional hands.",
    source: "WIRED LED + REAL CLOCK",
    note: "Confirm torque, plane spacing, wobble, and full-day clearance before committing to the orbital blocker stack.",
    aim: "Does a real quartz movement preserve the proven shadow geometry?",
    parts: "P0 LED bench · generic quartz · lightweight hands",
    pass: "24-hour run with no collisions, stalls, drift, or visible wobble",
    buy: "Buy one movement only after P0 passes",
    movement: "Generic center-shaft quartz timing test",
    stack: ["Optional system", "No separate COB in P1", "later", "Timing experiment", "LED + conventional quartz hands", "prove"]
  },
  p2: {
    title: "Direct-shaft orbital clock",
    description: "A stock quartz movement sits toward the wall and directly drives separate second, minute, and hour blocker discs. The fixed mask hides their support envelope.",
    source: "POINT LED + ORBITAL BLOCKERS",
    note: "Prove source → second → minute → hour → fixed mask/quartz → wall before adding a separate halo circuit.",
    aim: "Does the final direct-shaft stack project three readable orbital shadows?",
    parts: "Proven LED · quartz · three blocker discs · fixed mask",
    pass: "All planes clear, supports stay masked, and 24-hour motion passes",
    buy: "Commit to final clock mechanics after P1",
    movement: "Stock quartz shafts → blocker discs; fixed mask; no gears",
    stack: ["Optional system", "No separate COB in P2", "later", "Final shadow stack", "LED → discs → mask/quartz → wall", "primary"]
  },
  p3: {
    title: "Conditional independent halo",
    description: "Keep the accepted P2 shadow stack unchanged. Add a separately dimmed COB halo only if the point LED cannot create the desired wall pool without softening the shadows.",
    source: "POINT LED + COB HALO",
    note: "The halo and shadow emitters remain separate circuits and separate optical systems.",
    aim: "Does an independent halo improve the wall field without washing out time?",
    parts: "Proven P2 clock · COB halo · diffuser · final body",
    pass: "Readable shadow at all dimmer settings with safe final temperatures",
    buy: "Commit to final parts last",
    movement: "Stock quartz shafts → single tapered orbital blocker blades; fixed mask; no gears",
    stack: ["Ambient system", "COB ring + diffuser", "soft", "Shadow stack", "LED → discs → fixed mask → quartz → wall", "primary"]
  }
};

const MATERIALS = {
  warmWhite: [232, 227, 215],
  sand: [202, 181, 148],
  stone: [164, 158, 149],
  oak: [190, 151, 102],
  charcoal: [52, 50, 46]
};

const LIGHTING_PRESETS = {
  morning: { ambientLevel: 72, haloBrightness: 48, pointIntensity: 58, haloTemperature: 3100 },
  evening: { ambientLevel: 46, haloBrightness: 74, pointIntensity: 78, haloTemperature: 2700 },
  warm: { ambientLevel: 34, haloBrightness: 82, pointIntensity: 82, haloTemperature: 2200 },
  gallery: { ambientLevel: 64, haloBrightness: 60, pointIntensity: 70, haloTemperature: 3500 },
  dark: { ambientLevel: 15, haloBrightness: 90, pointIntensity: 92, haloTemperature: 2500 }
};

const $ = (id) => document.getElementById(id);
const clamp = (value, min, max) => Math.max(min, Math.min(max, value));
const round = (value, digits = 1) => Number(value.toFixed(digits));

function handToWallDistance(s = state) {
  // The hand plane sits directly in front of the quartz movement.
  if (s.movementType === "quartz-driven-orbital-hands") return s.minutePlaneZ - s.wallZ;
  return s.stage === "p0" ? s.p0HandWallDistance : s.wallGap + s.movementDepth;
}

function controlAvailability(stage) {
  return { p0HandWallDistance: stage === "p0" };
}

function projectionModel(s = state) {
  if (s.movementType === "quartz-driven-orbital-hands") {
    const direct = directShaftDiscModel(s);
    const minute = direct.carriers.minute;
    const pivotFactor = 1 - minute.M;
    return {
      L: minute.L,
      D: direct.sourceWall,
      handWall: minute.W,
      magnification: minute.M,
      penumbra: minute.penumbra,
      pivotX: pivotFactor * s.ledOffsetX,
      pivotY: pivotFactor * s.ledOffsetY,
      hourLength: direct.carriers.hour.projectedTip,
      minuteLength: minute.projectedTip,
      secondLength: direct.carriers.second.projectedTip,
      hourWidth: direct.carriers.hour.projectedWidth,
      minuteWidth: minute.projectedWidth,
      secondWidth: direct.carriers.second.projectedWidth,
      perPlane: direct.carriers,
      projectedMaskRadius: direct.projectedMaskRadius,
      requiredFullFieldAngle: direct.requiredFullFieldAngle
    };
  }
  const L = Math.max(0.1, s.sourceHandDistance);
  const handWall = handToWallDistance(s);
  const D = L + handWall;
  const magnification = D / L;
  // Finite-source approximation: source diameter × hand-to-wall / source-to-hand.
  const penumbra = s.apertureDiameter * handWall / L;
  const pivotX = (1 - magnification) * s.ledOffsetX;
  const pivotY = (1 - magnification) * s.ledOffsetY;
  return {
    L, D, handWall, magnification, penumbra, pivotX, pivotY,
    hourLength: s.hourLength * magnification,
    minuteLength: s.minuteLength * magnification,
    secondLength: s.secondLength * magnification,
    hourWidth: s.hourWidth * magnification,
    minuteWidth: s.minuteWidth * magnification,
    secondWidth: s.secondWidth * magnification
  };
}

function directShaftDiscModel(s = state) {
  const sourceZ = s.sourceZ ?? REFERENCE_FINAL_PRESET.sourceZ;
  const wallZ = s.wallZ ?? REFERENCE_FINAL_PRESET.wallZ;
  const sourceWall = sourceZ - wallZ;
  const maskZ = s.fixedMaskZ ?? REFERENCE_FINAL_PRESET.fixedMaskZ;
  const maskPhysicalRadius = s.fixedMaskPhysicalRadius ?? REFERENCE_FINAL_PRESET.fixedMaskPhysicalRadius;
  const projectedMaskRadius = maskPhysicalRadius * sourceWall / (sourceZ - maskZ);
  const definitions = {
    hour: { planeZ: s.hourPlaneZ, tip: s.hourLength, width: s.hourWidth, shape: s.hourShape || "leaf-kite" },
    minute: { planeZ: s.minutePlaneZ, tip: s.minuteLength, width: s.minuteWidth, shape: s.minuteShape || "blade" },
    second: { planeZ: s.secondPlaneZ, tip: s.secondLength, width: s.secondWidth, shape: s.secondShape || "needle" }
  };
  const carriers = {};
  Object.entries(definitions).forEach(([name, disc]) => {
    const L = sourceZ - disc.planeZ;
    const W = disc.planeZ - wallZ;
    const M = sourceWall / L;
    const projectedCarrier = s.carrierOuterRadius * M;
    const projectedTip = disc.tip * M;
    const hideMargin = projectedMaskRadius - projectedCarrier;
    const halfAngle = Math.atan(disc.tip / L) * 180 / Math.PI;
    carriers[name] = {
      ...disc,
      L, W, D: sourceWall, M,
      penumbra: s.apertureDiameter * W / L,
      projectedCarrier,
      projectedTip,
      projectedWidth: disc.width * M,
      visibleLength: Math.max(0, projectedTip - projectedMaskRadius),
      hideMargin,
      carrierHidden: hideMargin >= s.requiredCarrierHideMargin,
      fullFieldAngle: halfAngle * 2,
      shaftInterface: `${name} shaft / bore must be measured`
    };
  });
  const podClearRadius = (s.rearOpeningDiameter ?? REFERENCE_FINAL_PRESET.rearOpeningDiameter) / 2;
  const second = carriers.second;
  const podRearZ = 45;
  const requiredClearRadiusAtPodRear = second.tip * (sourceZ - podRearZ) / second.L;
  const minimumPodEndZ = sourceZ - podClearRadius * second.L / second.tip;
  return {
    movementType: "quartz-driven-orbital-hands",
    driveMechanism: "stock quartz concentric shafts directly drive three single tapered orbital blocker blades",
    hollowCenter: false,
    printedGears: false,
    wallZ, sourceZ, sourceWall, maskZ, maskPhysicalRadius,
    projectedMaskRadius,
    maskMagnification: sourceWall / (sourceZ - maskZ),
    carrierOuterRadius: s.carrierOuterRadius,
    carriers,
    worstHideMargin: Math.min(...Object.values(carriers).map(carrier => carrier.hideMargin)),
    requiredFullFieldAngle: Math.max(...Object.values(carriers).map(carrier => carrier.fullFieldAngle)),
    flaredPodClearance: {
      podClearRadius,
      podRearZ,
      requiredClearRadiusAtPodRear,
      minimumPodEndZ,
      continuousPodClearsCone: podClearRadius >= requiredClearRadiusAtPodRear,
      podMustEndBeforeConeExpands: podClearRadius < requiredClearRadiusAtPodRear
    },
    stack: ["viewer shell + metal heatsink", "point LED + thin/flared aperture", "second disc", "minute disc", "hour disc", "fixed mask + quartz face", "quartz case", "45 mm air gap", "wall"]
  };
}

function orbitalCarrierModel(s = state) {
  const sourceZ = s.sourceZ ?? REFERENCE_FINAL_PRESET.sourceZ;
  const wallZ = s.wallZ ?? REFERENCE_FINAL_PRESET.wallZ;
  const D = sourceZ - wallZ;
  const maskZ = s.fixedMaskZ ?? REFERENCE_FINAL_PRESET.fixedMaskZ;
  const maskRadius = s.fixedMaskPhysicalRadius ?? REFERENCE_FINAL_PRESET.fixedMaskPhysicalRadius;
  const occluderRadius = maskRadius * D / (sourceZ - maskZ);
  const aperture = s.apertureDiameter;
  const definitions = {
    hour: { inner: s.hourCarrierInnerRadius, outer: s.hourCarrierOuterRadius, tip: s.hourLength, width: s.hourWidth, offset: s.hourAxialOffset, planeZ: s.hourPlaneZ, shape: s.hourShape || "leaf-kite" },
    minute: { inner: s.minuteCarrierInnerRadius, outer: s.minuteCarrierOuterRadius, tip: s.minuteLength, width: s.minuteWidth, offset: s.minuteAxialOffset, planeZ: s.minutePlaneZ, shape: s.minuteShape || "blade" },
    second: { inner: s.secondCarrierInnerRadius, outer: s.secondCarrierOuterRadius, tip: s.secondLength, width: s.secondWidth, offset: s.secondAxialOffset, planeZ: s.secondPlaneZ, shape: s.secondShape || "needle" }
  };
  const carriers = {};
  Object.entries(definitions).forEach(([name, c]) => {
    const L = sourceZ - c.planeZ;
    const W = c.planeZ - wallZ;
    const M = D / L;
    const projectedTip = c.tip * M;
    const projectedDriveRadius = s.exposedDriveRadius * M;
    const hideMargin = occluderRadius - projectedDriveRadius;
    const failureFlags = {
      donutShadow: hideMargin < 0,
      collision: s.carrierAxialGap < .4,
      vignetting: aperture / 2 >= s.clearCenterDiameter / 2,
      glare: aperture > 1,
      pivotDrift: false,
      centralObstruction: s.clearCenterDiameter / 2 > c.inner
    };
    carriers[name] = {
      ...c, L, W, D, M,
      penumbra: aperture * W / L,
      projectedTip,
      visibleLength: Math.max(0, projectedTip - occluderRadius),
      projectedDriveRadius,
      hideMargin,
      failureFlags
    };
  });
  return {
    movementType: s.movementType,
    occluderRadius,
    clearCenterDiameter: s.clearCenterDiameter,
    carrierThickness: s.carrierThickness,
    axialGap: s.carrierAxialGap,
    axialPitch: s.carrierAxialPitch,
    stackDepth: s.carrierStackDepth,
    carriers,
    worstHideMargin: Math.min(...Object.values(carriers).map(carrier => carrier.hideMargin))
  };
}

function movementStudyModel(s = state) {
  // Movement Studies is globally reachable, including from initial P0. Always
  // evaluate it from a complete primary reference geometry instead of leaking
  // stage-local defaults into the orbital contract.
  const complete = s.movementType === "quartz-driven-orbital-hands"
    ? { ...REFERENCE_FINAL_PRESET, ...s }
    : { ...s, ...REFERENCE_FINAL_PRESET };
  return directShaftDiscModel({
    ...complete,
    stage: "p3",
    movementType: "quartz-driven-orbital-hands"
  });
}

function haloModel(s = state) {
  // Independent from the point-source model: wall spacing broadens and softens
  // the COB ring while brightness falls with distance.
  const diffusion = s.haloSpread / 100;
  const radius = s.haloRadius + s.wallGap * (0.12 + diffusion * 0.22);
  const edgeSoftness = 0.12 + diffusion * 0.34 + s.wallGap / 600;
  const distanceFalloff = 1 / (1 + Math.max(0, s.wallGap - 10) / 130);
  return { radius, diameter: radius * 2, edgeSoftness, effectiveBrightness: s.haloBrightness * distanceFalloff };
}

function pointLightModel(s = state) {
  const projection = projectionModel(s);
  return {
    rgb: kelvinToRgb(s.pointTemperature),
    intensity: s.pointIntensity / 100,
    fieldRadius: projection.secondLength * 1.22,
    pivotX: projection.pivotX,
    pivotY: projection.pivotY
  };
}

function shadowOpacity(s = state) {
  // No System-B photons means no projected hand shadow. Keep the mapping
  // bounded and monotonic so intensity remains physically legible.
  return clamp(s.pointIntensity / 100, 0, 1) * .72;
}

function shadowSharpness(p = projectionModel()) {
  if (p.penumbra < 0.75) return ["SHARP", "clean edge"];
  if (p.penumbra < 1.6) return ["ACCEPTABLE", "slight feather"];
  if (p.penumbra < 3.2) return ["SOFT", "visible penumbra"];
  return ["TOO BLURRY", "prototype aperture"];
}

function clockAngles(nowMs = performance.now()) {
  let hour = state.manualHour;
  let minute = state.manualMinute;
  let second = state.manualSecond;
  // Manual time is a fixed design input. Fractional motion belongs only to a
  // real clock; otherwise the hand sweeps within one second and snaps back at
  // every performance-timer boundary.
  let fraction = 0;

  if (state.useRealTime) {
    const now = new Date();
    hour = now.getHours();
    minute = now.getMinutes();
    second = now.getSeconds();
    fraction = state.sweepMode === "sweep" ? now.getMilliseconds() / 1000 : 0;
  }
  const secondValue = second + fraction;
  const minuteValue = minute + secondValue / 60;
  const hourValue = (hour % 12) + minuteValue / 60;
  return {
    hour, minute, second,
    hourAngle: hourValue * Math.PI / 6,
    minuteAngle: minuteValue * Math.PI / 30,
    secondAngle: secondValue * Math.PI / 30
  };
}

function kelvinToRgb(kelvin) {
  const t = clamp(kelvin, 1000, 40000) / 100;
  let r, g, b;
  if (t <= 66) {
    r = 255;
    g = 99.4708025861 * Math.log(t) - 161.1195681661;
    b = t <= 19 ? 0 : 138.5177312231 * Math.log(t - 10) - 305.0447927307;
  } else {
    r = 329.698727446 * Math.pow(t - 60, -0.1332047592);
    g = 288.1221695283 * Math.pow(t - 60, -0.0755148492);
    b = 255;
  }
  return [clamp(Math.round(r), 0, 255), clamp(Math.round(g), 0, 255), clamp(Math.round(b), 0, 255)];
}

function rgba(rgb, alpha) { return `rgba(${rgb[0]},${rgb[1]},${rgb[2]},${alpha})`; }

function formatValue(value, unit, step) {
  const digits = step < 1 ? 1 : 0;
  return `${Number(value).toFixed(digits)} ${unit}`;
}

function normalizedCanvasCssSize(width, height) {
  return {
    width: Math.max(1, Math.round(Number(width) || 0)),
    height: Math.max(1, Math.round(Number(height) || 0))
  };
}

function heroCanvasLayout(width) {
  const normalizedWidth = Math.max(1, Math.round(Number(width) || 0));
  return normalizedCanvasCssSize(normalizedWidth, normalizedWidth * 5 / 6);
}

function canvasMetrics(canvas) {
  const rect = canvas.getBoundingClientRect();
  const dpr = Math.min(2, window.devicePixelRatio || 1);
  const { width, height } = normalizedCanvasCssSize(rect.width, rect.height);
  if (canvas.width !== Math.round(width * dpr) || canvas.height !== Math.round(height * dpr)) {
    canvas.width = Math.round(width * dpr);
    canvas.height = Math.round(height * dpr);
  }
  const ctx = canvas.getContext("2d");
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  return { ctx, width, height, dpr };
}

function roundedRectPath(ctx, x, y, w, h, r) {
  const radius = Math.min(r, w / 2, h / 2);
  ctx.beginPath();
  ctx.moveTo(x + radius, y);
  ctx.arcTo(x + w, y, x + w, y + h, radius);
  ctx.arcTo(x + w, y + h, x, y + h, radius);
  ctx.arcTo(x, y + h, x, y, radius);
  ctx.arcTo(x, y, x + w, y, radius);
  ctx.closePath();
}

function drawWallBackground(ctx, width, height) {
  const light = state.ambientLevel / 100;
  const base = Math.round(122 + light * 105);
  const gradient = ctx.createLinearGradient(0, 0, width, height);
  gradient.addColorStop(0, `rgb(${base + 8},${base + 5},${base - 2})`);
  gradient.addColorStop(.55, `rgb(${base},${base - 5},${base - 13})`);
  gradient.addColorStop(1, `rgb(${base - 9},${base - 14},${base - 22})`);
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, width, height);

  ctx.save();
  ctx.globalAlpha = .055;
  for (let y = 2; y < height; y += 5) {
    const shift = (y * 13) % 9;
    ctx.fillStyle = y % 10 ? "#fff" : "#6c6255";
    for (let x = shift; x < width; x += 17) ctx.fillRect(x, y, 1, 1);
  }
  ctx.restore();
}

function drawHalo(ctx, cx, cy, scale) {
  if (!state.haloEnabled || state.haloBrightness <= 0) return;
  const halo = haloModel();
  const radius = halo.radius * scale;
  const rgb = kelvinToRgb(state.haloTemperature);
  const alpha = clamp(halo.effectiveBrightness / 100, 0, 1);
  const g = ctx.createRadialGradient(cx, cy, Math.max(1, radius * .08), cx, cy, radius * 1.38);
  g.addColorStop(0, rgba(rgb, .18 * alpha));
  g.addColorStop(.18, rgba(rgb, .62 * alpha));
  g.addColorStop(.5, rgba(rgb, .42 * alpha));
  g.addColorStop(.72, rgba(rgb, .16 * alpha));
  g.addColorStop(1, rgba(rgb, 0));
  ctx.fillStyle = g;
  ctx.fillRect(cx - radius * 1.45, cy - radius * 1.45, radius * 2.9, radius * 2.9);

  const ringRadius = state.ringDiameter * scale / 2;
  const ring = ctx.createRadialGradient(cx, cy, Math.max(0, ringRadius - radius * .24), cx, cy, ringRadius + radius * .28);
  ring.addColorStop(0, rgba(rgb, 0));
  ring.addColorStop(.42, rgba(rgb, .05 * alpha));
  ring.addColorStop(.56, rgba(rgb, .16 * alpha));
  ring.addColorStop(1, rgba(rgb, 0));
  ctx.fillStyle = ring;
  ctx.fillRect(cx - radius, cy - radius, radius * 2, radius * 2);
}

function drawPointIllumination(ctx, cx, cy, scale) {
  const light = pointLightModel();
  if (light.intensity <= 0) return;
  const x = cx + light.pivotX * scale;
  const y = cy + light.pivotY * scale;
  const radius = Math.max(18, light.fieldRadius * scale);
  // System B is a directed point-source pool, not the rear COB halo. It remains
  // visible and tunable even when the ambient halo system is disabled.
  const g = ctx.createRadialGradient(x, y, radius * .05, x, y, radius);
  g.addColorStop(0, rgba(light.rgb, .24 * light.intensity));
  g.addColorStop(.42, rgba(light.rgb, .18 * light.intensity));
  g.addColorStop(.76, rgba(light.rgb, .07 * light.intensity));
  g.addColorStop(1, rgba(light.rgb, 0));
  ctx.fillStyle = g;
  ctx.fillRect(x - radius, y - radius, radius * 2, radius * 2);
}

function drawShadowHand(ctx, cx, cy, angle, length, width, blur, alpha, scale, extraOffset = 0) {
  const dx = Math.sin(angle) * length * scale;
  const dy = -Math.cos(angle) * length * scale;
  ctx.save();
  ctx.lineCap = "round";
  ctx.strokeStyle = `rgba(33,27,22,${alpha})`;
  ctx.lineWidth = Math.max(.65, width * scale);
  ctx.shadowColor = `rgba(35,27,21,${Math.min(.8, alpha + .15)})`;
  ctx.shadowBlur = Math.max(.25, blur * scale * 1.2);
  ctx.beginPath();
  ctx.moveTo(cx + extraOffset, cy);
  ctx.lineTo(cx + dx + extraOffset, cy + dy);
  ctx.stroke();
  ctx.restore();
}

function drawBody(ctx, cx, cy, scale) {
  if (!state.showBody) return;
  const radius = state.bodyDiameter * scale / 2;
  const rgb = MATERIALS[state.material];
  ctx.save();
  ctx.shadowColor = "rgba(25,20,15,.25)";
  ctx.shadowBlur = Math.max(10, state.wallGap * scale * .35);
  ctx.shadowOffsetY = Math.max(3, state.wallGap * scale * .08);
  const g = ctx.createRadialGradient(cx - radius * .32, cy - radius * .4, radius * .05, cx, cy, radius);
  g.addColorStop(0, rgba(rgb.map(v => Math.min(255, v + 18)), .97));
  g.addColorStop(.72, rgba(rgb, .98));
  g.addColorStop(1, rgba(rgb.map(v => Math.max(0, v - 26)), .98));
  ctx.fillStyle = g;
  ctx.beginPath();
  ctx.arc(cx, cy, radius, 0, Math.PI * 2);
  ctx.fill();
  ctx.shadowColor = "transparent";
  ctx.clip();
  if (state.surface === "rings") {
    ctx.strokeStyle = "rgba(55,45,34,.08)";
    ctx.lineWidth = .55;
    for (let r = 12; r < radius; r += 5) { ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.stroke(); }
  } else if (state.surface === "radial") {
    ctx.strokeStyle = "rgba(55,45,34,.065)";
    ctx.lineWidth = .5;
    for (let a = 0; a < Math.PI * 2; a += Math.PI / 32) {
      ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + Math.cos(a) * radius, cy + Math.sin(a) * radius); ctx.stroke();
    }
  } else if (state.surface === "wabi") {
    ctx.fillStyle = "rgba(62,50,38,.06)";
    for (let i = 0; i < 100; i += 1) {
      const a = i * 2.399, r = radius * Math.sqrt((i + 1) / 101);
      ctx.beginPath(); ctx.arc(cx + Math.cos(a) * r, cy + Math.sin(a) * r, .6 + (i % 4) * .25, 0, Math.PI * 2); ctx.fill();
    }
  }
  ctx.restore();
  ctx.save();
  ctx.strokeStyle = "rgba(255,255,255,.38)";
  ctx.lineWidth = 1;
  ctx.beginPath(); ctx.arc(cx, cy, radius - .5, 0, Math.PI * 2); ctx.stroke();
  ctx.restore();
}

function drawProjectedMaskShadow(ctx, cx, cy, scale, s = state) {
  if (s.movementType !== "quartz-driven-orbital-hands") return;
  const direct = directShaftDiscModel(s);
  ctx.save();
  ctx.fillStyle = "rgba(22,18,15,.94)";
  ctx.shadowColor = "rgba(35,27,21,.32)";
  ctx.shadowBlur = Math.max(1, projectionModel(s).penumbra * scale);
  ctx.beginPath();
  ctx.arc(cx, cy, direct.projectedMaskRadius * scale, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();
}

function drawWallView(ctx, width, height, nowMs) {
  drawWallBackground(ctx, width, height);
  const p = projectionModel();
  const halo = haloModel();
  const clock = clockAngles(nowMs);
  const longestShadow = state.secondEnabled ? p.secondLength : p.minuteLength;
  const sceneDiameter = Math.max(halo.diameter * 1.18, longestShadow * 2.25, state.bodyDiameter * 1.35);
  const scale = Math.min(width, height) * .78 / sceneDiameter;
  const cx = width * .5;
  const cy = height * .49;
  drawHalo(ctx, cx, cy, scale);
  drawPointIllumination(ctx, cx, cy, scale);

  const px = cx + p.pivotX * scale;
  const py = cy + p.pivotY * scale;
  const opacity = shadowOpacity();
  drawShadowHand(ctx, px, py, clock.hourAngle, p.hourLength, p.hourWidth, p.penumbra, opacity, scale);
  drawShadowHand(ctx, px, py, clock.minuteAngle, p.minuteLength, p.minuteWidth, p.penumbra, opacity * .94, scale);
  if (state.secondEnabled) drawShadowHand(ctx, px, py, clock.secondAngle, p.secondLength, p.secondWidth, p.penumbra, opacity * .76, scale);

  ctx.save();
  ctx.fillStyle = `rgba(31,25,20,${opacity * .75})`;
  ctx.shadowColor = "rgba(35,27,21,.35)";
  ctx.shadowBlur = Math.max(1, p.penumbra * scale);
  ctx.beginPath(); ctx.arc(px, py, Math.max(2, p.hourWidth * scale * .72), 0, Math.PI * 2); ctx.fill();
  ctx.restore();
  // The fixed z=60 mask creates the central wall shadow whether or not the
  // viewer-side decorative shell is displayed.
  drawProjectedMaskShadow(ctx, px, py, scale);
  drawBody(ctx, cx, cy, scale);
}

function drawLabel(ctx, text, x, y, align = "left", color = "rgba(246,239,225,.72)") {
  if (!state.showLabels) return;
  ctx.save();
  ctx.font = "8px Avenir Next, Helvetica, Arial, sans-serif";
  ctx.textAlign = align;
  ctx.fillStyle = color;
  ctx.fillText(text.toUpperCase(), x, y);
  ctx.restore();
}

function drawDimension(ctx, x1, y1, x2, y2, label) {
  if (!state.showDimensions) return;
  ctx.save();
  ctx.strokeStyle = "rgba(240,196,132,.46)";
  ctx.fillStyle = "rgba(247,218,176,.75)";
  ctx.lineWidth = .75;
  ctx.setLineDash([2, 3]);
  ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
  ctx.setLineDash([]);
  const a = Math.atan2(y2 - y1, x2 - x1);
  for (const [x, y, direction] of [[x1, y1, 1], [x2, y2, -1]]) {
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x + Math.cos(a + .55) * 5 * direction, y + Math.sin(a + .55) * 5 * direction);
    ctx.lineTo(x + Math.cos(a - .55) * 5 * direction, y + Math.sin(a - .55) * 5 * direction);
    ctx.closePath(); ctx.fill();
  }
  ctx.font = "8px Avenir Next, Helvetica, Arial, sans-serif";
  ctx.textAlign = "center";
  ctx.fillText(label, (x1 + x2) / 2, (y1 + y2) / 2 - 7);
  ctx.restore();
}

function drawSectionView(ctx, width, height, large = false) {
  const bg = ctx.createLinearGradient(0, 0, width, height);
  bg.addColorStop(0, "#23201b");
  bg.addColorStop(1, "#151310");
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, width, height);
  const p = projectionModel();
  const isP0 = state.stage === "p0";
  const isReferenceBody = state.movementType === "quartz-driven-orbital-hands";
  const isDirect = state.movementType === "quartz-driven-orbital-hands";
  const isOrbitalComparison = state.movementType === "annular-orbital-hollow-center";
  const margin = large ? 54 : 28;
  const total = isP0 ? p.L + p.handWall : state.bodyDepth + state.wallGap + 10;
  const sx = (width - margin * 2) / Math.max(90, total);
  const wallX = width - margin;
  const handX = wallX - p.handWall * sx;
  const apertureX = handX - p.L * sx;
  const sourceX = apertureX;
  const bodyBackX = wallX - state.wallGap * sx;
  const bodyFrontX = bodyBackX - state.bodyDepth * sx;
  const midY = height * .5;
  const bodyH = Math.min(height * .67, state.bodyDiameter * (large ? .56 : .43));
  const top = midY - bodyH / 2;
  const bottom = midY + bodyH / 2;

  // Wall and its diffuse halo.
  ctx.fillStyle = "#d7d0c4";
  ctx.fillRect(wallX, 14, Math.max(8, width - wallX - margin * .2), height - 28);
  if (state.haloEnabled) {
    const hr = Math.min(bodyH * .48, 90);
    const haloRgb = kelvinToRgb(state.haloTemperature);
    const hg = ctx.createLinearGradient(wallX - hr, 0, wallX + 4, 0);
    hg.addColorStop(0, rgba(haloRgb, 0));
    hg.addColorStop(.75, rgba(haloRgb, .22));
    hg.addColorStop(1, rgba(haloRgb, .55));
    ctx.fillStyle = hg;
    ctx.fillRect(wallX - hr, top - 14, hr + 5, bodyH + 28);
  }

  // P0 is a separate wired LED breadboard, not a 40 mm optical path forced inside
  // the future 35 mm shell. Later stages show the enclosure.
  ctx.save();
  ctx.strokeStyle = "#d8cdb9";
  ctx.lineWidth = Math.max(2, state.shellThickness * .85);
  ctx.fillStyle = "rgba(225,215,197,.08)";
  if (isP0) {
    ctx.beginPath();
    ctx.moveTo(sourceX - 7, bottom - 18);
    ctx.lineTo(handX + 10, bottom - 18);
    ctx.stroke();
    for (const x of [sourceX, handX]) {
      ctx.beginPath(); ctx.moveTo(x, bottom - 18); ctx.lineTo(x, bottom - 7); ctx.stroke();
    }
    drawLabel(ctx, "open adjustable jig", (sourceX + handX) / 2, bottom - 2, "center");
  } else if (isReferenceBody) {
    const frontDepthPx = REFERENCE_FINAL_PRESET.frontOccluderDepth * sx;
    const podStartX = bodyFrontX + (REFERENCE_FINAL_PRESET.frontOccluderDepth - REFERENCE_FINAL_PRESET.podFrontOverlap) * sx;
    const podH = bodyH * REFERENCE_FINAL_PRESET.rearPodDiameter / REFERENCE_FINAL_PRESET.frontOccluderDiameter;
    const podTop = midY - podH / 2;
    roundedRectPath(ctx, bodyFrontX, top, frontDepthPx, bodyH, Math.min(7, frontDepthPx * .35));
    ctx.fill(); ctx.stroke();
    const direct = directShaftDiscModel(state);
    const podEndX = wallX - direct.flaredPodClearance.minimumPodEndZ * sx;
    const openingHalf = podH * REFERENCE_FINAL_PRESET.rearOpeningDiameter / REFERENCE_FINAL_PRESET.rearPodDiameter / 2;
    ctx.fillRect(podStartX, podTop, podEndX - podStartX, midY - openingHalf - podTop);
    ctx.strokeRect(podStartX, podTop, podEndX - podStartX, midY - openingHalf - podTop);
    ctx.fillRect(podStartX, midY + openingHalf, podEndX - podStartX, podTop + podH - (midY + openingHalf));
    ctx.strokeRect(podStartX, midY + openingHalf, podEndX - podStartX, podTop + podH - (midY + openingHalf));
    drawLabel(ctx, "Ø260 × 12 decorative room shell", bodyFrontX, top - 10, "left");
    drawLabel(ctx, `Ø150 pod ends by z${direct.flaredPodClearance.minimumPodEndZ.toFixed(1)}`, podEndX, podTop - 10, "right");
    drawLabel(ctx, "open/flared optical field through blockers + mask", (apertureX + handX) / 2, midY + 19, "center", "rgba(246,193,126,.78)");
  } else {
    roundedRectPath(ctx, bodyFrontX, top, Math.max(20, bodyBackX - bodyFrontX), bodyH, 10);
    ctx.fill(); ctx.stroke();
  }
  ctx.restore();

  const movementW = Math.max(13, state.movementDepth * sx);
  const movementH = isReferenceBody ? bodyH * state.movementEnvelopeHeight / state.bodyDiameter : bodyH * .27;
  if (isDirect) {
    const model = directShaftDiscModel(state);
    const carriers = [
      ["second", model.carriers.second, "#f6d6a8"],
      ["minute", model.carriers.minute, "#f0bd78"],
      ["hour", model.carriers.hour, "#d8a061"]
    ];
    carriers.forEach(([name, carrier, color]) => {
      const planeX = wallX - carrier.planeZ * sx;
      const ringHalf = bodyH * model.carrierOuterRadius / state.bodyDiameter;
      const blockerTip = bodyH * carrier.tip / state.bodyDiameter;
      ctx.strokeStyle = color;
      ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(planeX, midY - ringHalf); ctx.lineTo(planeX, midY + ringHalf); ctx.stroke();
      ctx.lineWidth = name === "hour" ? 4 : name === "minute" ? 2.5 : 1.2;
      ctx.beginPath(); ctx.moveTo(planeX, midY - ringHalf); ctx.lineTo(planeX, midY - blockerTip); ctx.stroke();
    });
    const maskX = wallX - model.maskZ * sx;
    const maskHalf = bodyH * model.maskPhysicalRadius / state.bodyDiameter;
    ctx.strokeStyle = "#151310";
    ctx.lineWidth = Math.max(3, 2 * sx);
    ctx.beginPath(); ctx.moveTo(maskX, midY - maskHalf); ctx.lineTo(maskX, midY + maskHalf); ctx.stroke();
    drawLabel(ctx, "fixed mask Ø111.14 / projects Ø260", maskX, midY - maskHalf - 9, "center");

    const quartzX = wallX - 60 * sx;
    const quartzW = 15 * sx;
    ctx.fillStyle = "#665d52";
    ctx.strokeStyle = "rgba(228,214,190,.45)";
    ctx.lineWidth = 1;
    roundedRectPath(ctx, quartzX, midY - movementH * .38, quartzW, movementH * .76, 3);
    ctx.fill(); ctx.stroke();
    drawLabel(ctx, "stock quartz / wall side", quartzX + quartzW / 2, midY + movementH / 2 + 18, "center");
    drawLabel(ctx, "3 direct-shaft blocker discs / separate planes", handX, midY + movementH / 2 + 17, "center");
  } else if (isOrbitalComparison) {
    ctx.strokeStyle = "#d8a061";
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(handX, midY - movementH / 2); ctx.lineTo(handX, midY + movementH / 2); ctx.stroke();
    drawLabel(ctx, "comparison-only hollow-center carrier", handX, midY + movementH / 2 + 17, "center");
  } else {
    ctx.fillStyle = "#786d5e";
    roundedRectPath(ctx, handX - movementW, midY - movementH / 2, movementW, movementH, 3);
    ctx.fill();
    const movementLabel = isP0 || state.stage === "p1" ? "manual concentric rings" : isReferenceBody ? "movement architecture study zone" : "generic quartz movement";
    drawLabel(ctx, movementLabel, handX - movementW, midY + movementH / 2 + 13);
  }

  // Blocker plane and wired point source.
  ctx.strokeStyle = "#e5ad6b";
  ctx.lineWidth = 2;
  ctx.beginPath(); ctx.moveTo(handX, midY - bodyH * .23); ctx.lineTo(handX, midY + bodyH * .23); ctx.stroke();
  ctx.fillStyle = "#f1a454";
  ctx.shadowColor = "#ee9c4e"; ctx.shadowBlur = 10;
  ctx.beginPath(); ctx.arc(sourceX, midY, 3.2, 0, Math.PI * 2); ctx.fill();
  ctx.shadowColor = "transparent";
  drawLabel(ctx, "wired point led + aperture", sourceX, midY - 25, "center");
  drawLabel(ctx, isDirect ? "nominal minute blocker plane" : "hand plane", handX, top - 10, "center");

  // Rays communicate M=D/L. They converge at source/aperture then spread to wall.
  if (state.showRays) {
    ctx.save();
    ctx.strokeStyle = "rgba(239,151,77,.55)";
    ctx.lineWidth = .8;
    ctx.setLineDash([4, 3]);
    const raySource = sourceX;
    const handHalf = bodyH * .16;
    const wallHalf = handHalf * p.magnification;
    for (const sign of [-1, 1]) {
      ctx.beginPath();
      ctx.moveTo(raySource, midY);
      ctx.lineTo(handX, midY + sign * handHalf);
      ctx.lineTo(wallX, midY + sign * wallHalf);
      ctx.stroke();
    }
    ctx.restore();
  }

  // Rear COB system remains visibly separate.
  if (state.haloEnabled) {
    ctx.strokeStyle = "#f1c47f";
    ctx.lineWidth = 5;
    ctx.beginPath(); ctx.moveTo(bodyBackX - 2, top + bodyH * .15); ctx.lineTo(bodyBackX - 2, top + bodyH * .28); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(bodyBackX - 2, bottom - bodyH * .28); ctx.lineTo(bodyBackX - 2, bottom - bodyH * .15); ctx.stroke();
    drawLabel(ctx, "cob + diffuser", bodyBackX - 6, bottom + 16, "right", "rgba(248,209,149,.8)");
  }
  drawLabel(ctx, "wall", wallX + 8, 30, "left", "rgba(47,42,35,.68)");
  drawDimension(ctx, handX, bottom + 17, wallX, bottom + 17, `${p.handWall} mm hand → wall`);
  drawDimension(ctx, apertureX, top + 18, handX, top + 18, `L ${state.sourceHandDistance} mm`);
  if (isReferenceBody) {
    drawDimension(ctx, bodyFrontX, bottom + 34, bodyFrontX + REFERENCE_FINAL_PRESET.frontOccluderDepth * sx, bottom + 34, "12 mm decorative shell");
    drawDimension(ctx, bodyBackX - REFERENCE_FINAL_PRESET.rearPodDepth * sx, bottom + 49, bodyBackX, bottom + 49, "60 mm rear pod");
    drawDimension(ctx, bodyBackX, bottom + 64, wallX, bottom + 64, "45 mm wall gap");
  }
}

function drawOrbitalView(ctx, width, height) {
  const bg = ctx.createLinearGradient(0, 0, width, height);
  bg.addColorStop(0, "#201d19");
  bg.addColorStop(1, "#11100e");
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, width, height);
  const model = movementStudyModel();
  const clock = clockAngles(performance.now());
  const cx = width > 680 ? width * .34 : width * .5;
  const cy = width > 680 ? height * .49 : height * .39;
  const scale = Math.min((width > 680 ? width * .52 : width * .76) / 260, height * .63 / 260);
  const colors = { hour: "#d59354", minute: "#efb974", second: "#f7d8aa" };
  const angles = { hour: clock.hourAngle, minute: clock.minuteAngle, second: clock.secondAngle };
  ctx.fillStyle = "rgba(246,211,166,.88)";
  ctx.font = "9px Avenir Next, Helvetica, Arial, sans-serif";
  ctx.fillText("PRIMARY / STOCK QUARTZ SHAFTS DIRECTLY DRIVE SINGLE ORBITAL BLOCKER BLADES", 20, 26);

  // The large room-side shell is cosmetic. It never participates in the mask
  // projection calculation.
  ctx.fillStyle = "rgba(211,198,176,.09)";
  ctx.strokeStyle = "rgba(224,212,192,.35)";
  ctx.lineWidth = 1.5;
  ctx.beginPath(); ctx.arc(cx, cy, 75 * scale, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

  ["hour", "minute", "second"].forEach((name, index) => {
    const carrier = model.carriers[name];
    ctx.save();
    ctx.strokeStyle = colors[name];
    ctx.globalAlpha = .7 + index * .1;
    ctx.lineWidth = Math.max(1.2, 1.2 * scale);
    ctx.setLineDash(index === 0 ? [] : index === 1 ? [5, 3] : [2, 3]);
    ctx.beginPath(); ctx.arc(cx, cy, model.carrierOuterRadius * scale, 0, Math.PI * 2); ctx.stroke();
    ctx.setLineDash([]);
    const angle = angles[name];
    const sx0 = cx + Math.sin(angle) * model.carrierOuterRadius * scale;
    const sy0 = cy - Math.cos(angle) * model.carrierOuterRadius * scale;
    const tx = cx + Math.sin(angle) * carrier.tip * scale;
    const ty = cy - Math.cos(angle) * carrier.tip * scale;
    ctx.lineWidth = Math.max(1.2, carrier.width * scale);
    ctx.lineCap = "round";
    ctx.beginPath(); ctx.moveTo(sx0, sy0); ctx.lineTo(tx, ty); ctx.stroke();
    ctx.restore();
  });

  // This fixed mask is a real part between the source and wall. Unlike the
  // Ø260 room shell it actually produces the central wall shadow.
  ctx.fillStyle = "#0d0c0b";
  ctx.strokeStyle = "rgba(244,185,114,.72)";
  ctx.lineWidth = 1.5;
  ctx.beginPath(); ctx.arc(cx, cy, model.maskPhysicalRadius * scale, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  drawLabel(ctx, "fixed mask Ø111.14 at z60 → wall shadow Ø260", cx, cy + 68 * scale, "center", "rgba(245,202,150,.85)");

  ctx.fillStyle = "rgba(227,218,201,.035)";
  ctx.strokeStyle = "rgba(239,231,216,.7)";
  ctx.lineWidth = 2;
  ctx.beginPath(); ctx.arc(cx, cy, 130 * scale, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  drawLabel(ctx, "Ø260 × 12 decorative room shell / not the mask", cx, cy - 130 * scale - 12, "center");
  drawLabel(ctx, "Ø150 rear pod", cx, cy + 75 * scale + 14, "center");

  const panelX = width > 680 ? width * .68 : 20;
  const panelY = width > 680 ? height * .23 : height * .75;
  ctx.fillStyle = "rgba(245,238,226,.74)";
  ctx.font = "9px Avenir Next, Helvetica, Arial, sans-serif";
  ctx.fillText("DIRECT-SHAFT DISC PLANES — BORES REMAIN ADJUSTABLE", panelX, panelY - 20);
  ["second", "minute", "hour"].forEach((name, index) => {
    const carrier = model.carriers[name];
    const y = panelY + index * 44;
    ctx.fillStyle = colors[name];
    roundedRectPath(ctx, panelX, y, 74, 8, 4); ctx.fill();
    ctx.fillStyle = "rgba(244,237,225,.84)";
    ctx.font = "9px Avenir Next, Helvetica, Arial, sans-serif";
    ctx.fillText(`${name.toUpperCase()}  z ${carrier.planeZ.toFixed(1)}  L ${carrier.L.toFixed(1)}  M ${carrier.M.toFixed(3)}  visible ${carrier.visibleLength.toFixed(1)} mm`, panelX, y + 24);
  });
  drawDimension(ctx, panelX, panelY + 122, panelX + 74, panelY + 122, "3.2 mm stack / 1.6 mm pitch");
  ctx.fillStyle = "rgba(197,181,158,.7)";
  ctx.font = "8px Avenir Next, Helvetica, Arial, sans-serif";
  ctx.fillText(`WORST HIDE MARGIN ${model.worstHideMargin.toFixed(2)} mm`, panelX, panelY + 150);
  ctx.fillStyle = "rgba(246,211,166,.88)";
  ctx.fillText("ROOM → WALL STACK", panelX, panelY + 184);
  ctx.strokeStyle = "rgba(239,185,118,.65)";
  ctx.lineWidth = 1.5;
  ctx.beginPath(); ctx.moveTo(panelX, panelY + 205); ctx.lineTo(panelX + 150, panelY + 205); ctx.stroke();
  ctx.fillStyle = "#6f6559";
  roundedRectPath(ctx, panelX + 4, panelY + 193, 40, 24, 4); ctx.fill();
  ctx.fillStyle = "#efa85d";
  ctx.beginPath(); ctx.arc(panelX + 66, panelY + 205, 4, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = "rgba(234,225,211,.72)";
  ctx.font = "8px Avenir Next, Helvetica, Arial, sans-serif";
  ctx.fillText("ROOM · SHELL/HEATSINK → LED → SEC/MIN/HR → MASK → QUARTZ → GAP → WALL", panelX, panelY + 232);
  ctx.fillText(`MASK Rwall ${model.projectedMaskRadius.toFixed(1)} mm · FIELD ${model.requiredFullFieldAngle.toFixed(1)}° / 130°`, panelX, panelY + 246);
}

function drawExplodedView(ctx, width, height) {
  const bg = ctx.createLinearGradient(0, 0, width, height);
  bg.addColorStop(0, "#d8d0c3"); bg.addColorStop(1, "#aaa092");
  ctx.fillStyle = bg; ctx.fillRect(0, 0, width, height);
  const stageParts = {
    p0: [
      ["WIRED POINT LED", .34, "light"], ["METAL HEATSINK", .45, "block"], ["THIN / FLARED APERTURE", .52, "small"],
      ["3 FAKE BLOCKERS", .68, "carrier"], ["OPEN TEST JIG", .72, "block"], ["WALL", 1.05, "wall"]
    ],
    p1: [
      ["POINT LED", .34, "light"], ["APERTURE", .48, "small"], ["CLOCK HANDS", .68, "hands"],
      ["GENERIC QUARTZ", .58, "block"], ["TEST JIG", .72, "block"], ["WALL", 1.05, "wall"]
    ],
    p2: [
      ["POINT LED + FLARED APERTURE", .38, "light"], ["SECOND / MINUTE / HOUR DISCS", .66, "carrier"],
      ["FIXED MASK + QUARTZ", .5, "small"], ["45 mm GAP", .54, "block"], ["WALL", 1.05, "wall"]
    ],
    p3: [
      ["Ø260 DECORATIVE SHELL + HEATSINK", 1, "shell"], ["POINT LED + FLARED APERTURE", .38, "light"],
      ["SECOND / MINUTE / HOUR DISCS", .66, "carrier"], ["FIXED Ø111 MASK + QUARTZ FACE", .5, "small"],
      ["STOCK QUARTZ CASE", .58, "block"], ["45 mm OPEN GAP", .54, "block"], ["WALL", 1.05, "wall"]
    ]
  };
  const parts = stageParts[state.stage];
  const horizontal = width > 620;
  const spacing = horizontal ? Math.min(62, (width - 100) / parts.length) : Math.min(46, (height - 90) / parts.length);
  const baseX = horizontal ? 55 : width * .5;
  const baseY = horizontal ? height * .5 : 45;
  const baseR = Math.min(horizontal ? height * .27 : width * .21, 105);
  parts.forEach(([label, ratio, kind], i) => {
    const x = horizontal ? baseX + i * spacing : baseX;
    const y = horizontal ? baseY + Math.sin(i * .8) * 10 : baseY + i * spacing;
    const r = baseR * ratio;
    ctx.save();
    ctx.translate(x, y);
    ctx.transform(1, 0, -.18, .72, 0, 0);
    ctx.shadowColor = "rgba(38,31,24,.18)"; ctx.shadowBlur = 10; ctx.shadowOffsetY = 7;
    if (kind === "wall") {
      ctx.fillStyle = "#eee9de"; ctx.fillRect(-r * .2, -r, r * .38, r * 2);
    } else if (kind === "block") {
      ctx.fillStyle = "#6b6257"; roundedRectPath(ctx, -r * .35, -r * .35, r * .7, r * .7, 5); ctx.fill();
    } else if (kind === "hands") {
      ctx.strokeStyle = "#332d26"; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(0, -r); ctx.moveTo(0, 0); ctx.lineTo(r * .7, r * .1); ctx.stroke();
    } else if (kind === "carrier") {
      ctx.strokeStyle = "#855b37"; ctx.lineWidth = 4; ctx.beginPath(); ctx.arc(0, 0, r * .58, 0, Math.PI * 2); ctx.stroke();
      ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(0, -r * .58); ctx.lineTo(0, -r); ctx.stroke();
    } else if (kind === "tunnel") {
      ctx.strokeStyle = "#b17a46"; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(-r, 0); ctx.lineTo(r, 0); ctx.stroke();
    } else if (kind === "pod") {
      ctx.fillStyle = "rgba(230,220,203,.55)"; ctx.beginPath(); ctx.arc(0, 0, r, 0, Math.PI * 2); ctx.fill();
    } else if (kind === "small") {
      ctx.fillStyle = "#b17a46"; ctx.beginPath(); ctx.arc(0, 0, r * .25, 0, Math.PI * 2); ctx.fill();
    } else {
      ctx.strokeStyle = kind === "light" ? "#f0aa56" : "#e6dfd1";
      ctx.lineWidth = kind === "shell" ? 12 : 5;
      ctx.beginPath(); ctx.arc(0, 0, r, 0, Math.PI * 2); ctx.stroke();
    }
    ctx.restore();
    ctx.save();
    ctx.font = "7px Avenir Next, Helvetica, Arial, sans-serif";
    ctx.fillStyle = "rgba(45,39,32,.7)";
    ctx.textAlign = horizontal ? "center" : "left";
    ctx.fillText(label, horizontal ? x : x + baseR + 16, horizontal ? height - 30 - (i % 2) * 12 : y + 3);
    ctx.restore();
  });
  ctx.fillStyle = "rgba(48,40,32,.55)";
  ctx.font = "9px Avenir Next, Helvetica, Arial, sans-serif";
  ctx.fillText("PRINT / SOURCE / MECHANISM / HALO / WALL", 24, 27);
}

let threeScene = null;
let rendererMode = "3d";
const THREE_VIEW_LABELS = Object.freeze({
  wall: "WALL SHADOW",
  section: "ASSEMBLY CUTAWAY",
  exploded: "EXPLODED ASSEMBLY",
  orbital: "ORBITAL MECHANICS"
});
const DEFAULT_THREE_VIEW = "section";

function syncVisualizationViewButtons(view) {
  document.querySelectorAll(".view-tab").forEach(button => button.classList.toggle("is-active", button.dataset.view === view));
  document.querySelectorAll("[data-three-view]").forEach(button => {
    const active = button.dataset.threeView === view;
    button.classList.toggle("is-active", active);
    button.setAttribute("aria-pressed", String(active));
  });
}

function selectVisualizationView(view, shouldRender = true) {
  if (!THREE_VIEW_LABELS[view]) return;
  state.view = view;
  syncVisualizationViewButtons(view);
  threeScene?.setView(view);
  $("threeModeLabel").textContent = rendererMode === "3d" ? THREE_VIEW_LABELS[view] : "CANVAS2D DIAGRAM";
  updateStageContext();
  if (shouldRender) renderAll();
}

function threeSceneSnapshot(nowMs = performance.now()) {
  const model = movementStudyModel(state);
  return {
    model,
    angles: clockAngles(nowMs),
    stage: state.stage,
    secondEnabled: state.secondEnabled,
    showBody: state.showBody,
    showRays: state.showRays,
    useRealTime: state.useRealTime,
    sweepMode: state.sweepMode,
    pointIntensity: state.pointIntensity,
    pointRgb: kelvinToRgb(state.pointTemperature),
    ledOffsetX: state.ledOffsetX,
    ledOffsetY: state.ledOffsetY,
    carrierOuterRadius: model.carrierOuterRadius
  };
}

function updateThreeDescription(snapshot = threeSceneSnapshot()) {
  const z = snapshot.model;
  $("threeDescription").textContent = `Wall z ${z.wallZ.toFixed(1)} millimetres; fixed mask z ${z.maskZ.toFixed(1)}; hour, minute, and second blocker planes z ${z.carriers.hour.planeZ.toFixed(1)}, ${z.carriers.minute.planeZ.toFixed(1)}, and ${z.carriers.second.planeZ.toFixed(1)}; point LED and aperture z ${z.sourceZ.toFixed(1)} toward the room.`;
}

function setRendererMode(requestedMode, reason = "") {
  const canUseThree = Boolean(threeScene?.available);
  rendererMode = requestedMode === "3d" && canUseThree ? "3d" : "2d";
  const threeCanvas = $("heroCanvas3d");
  const twoCanvas = $("heroCanvas2d");
  $("threeCameraToolbar").classList.toggle("renderer-hidden", rendererMode !== "3d");
  threeCanvas.classList.toggle("renderer-hidden", rendererMode !== "3d");
  twoCanvas.classList.toggle("renderer-hidden", rendererMode === "3d");
  [["renderer3dButton", "3d"], ["renderer2dButton", "2d"]].forEach(([id, mode]) => {
    const active = rendererMode === mode;
    $(id).classList.toggle("is-active", active);
    $(id).setAttribute("aria-pressed", String(active));
  });
  $("renderer3dButton").disabled = !canUseThree;
  $("reset3dButton").disabled = rendererMode !== "3d";
  const status = $("threeStatus");
  $("threeModeLabel").textContent = rendererMode === "3d" ? THREE_VIEW_LABELS[state.view] : "CANVAS2D DIAGRAM";
  status.classList.toggle("is-ready", rendererMode === "3d");
  status.classList.toggle("is-error", !canUseThree);
  status.textContent = rendererMode === "3d"
    ? `${state.view === "exploded" ? "SCHEMATIC EXPLODE · SHADOWS DISABLED" : "THREE.JS r176 · DRAG TO ORBIT · SCROLL TO ZOOM"}`
    : reason || (canUseThree ? "CANVAS2D FALLBACK / PRECISION DIAGRAM" : "3D UNAVAILABLE · CANVAS2D FALLBACK ACTIVE");
  if (rendererMode === "3d") {
    stopTwoDLoop();
    threeScene.setView(state.view);
    threeScene.update(threeSceneSnapshot());
  } else {
    startTwoDLoop();
    renderHero();
  }
}

function mountThreeRenderer() {
  const retireThreeRenderer = error => {
    const failedScene = threeScene;
    threeScene = null;
    globalThis.KageThreeRuntime = null;
    failedScene?.dispose();
    setRendererMode("2d", `3D interrupted: ${error.message}. Canvas2D fallback active.`);
  };
  try {
    const runtime = globalThis.KageThreeScene;
    if (!runtime?.mount) throw new Error("local Three.js bundle did not load");
    threeScene = runtime.mount({
      canvas: $("heroCanvas3d"),
      parent: $("heroVisual"),
      getSnapshot: threeSceneSnapshot,
      onFrame: updateTimeReadout,
      onError: retireThreeRenderer,
      onViewChange: (view, detail) => {
        if (rendererMode !== "3d") return;
        $("threeModeLabel").textContent = THREE_VIEW_LABELS[view];
        $("threeStatus").textContent = detail.exploded
          ? "SCHEMATIC EXPLODE · SHADOWS DISABLED"
          : "THREE.JS r176 · DRAG TO ORBIT · SCROLL TO ZOOM";
      }
    });
    globalThis.KageThreeRuntime = threeScene;
    state.view = DEFAULT_THREE_VIEW;
    syncVisualizationViewButtons(state.view);
    updateThreeDescription();
    setRendererMode("3d");
  } catch (error) {
    threeScene = null;
    setRendererMode("2d", `3D unavailable: ${error.message}. Canvas2D fallback active.`);
  }
}

function renderHero(nowMs = performance.now()) {
  if (rendererMode === "3d" && threeScene) {
    const snapshot = threeSceneSnapshot(nowMs);
    threeScene.update(snapshot, nowMs);
    updateThreeDescription(snapshot);
    return;
  }
  const canvas = $("heroCanvas2d");
  const { ctx, width, height } = canvasMetrics(canvas);
  ctx.clearRect(0, 0, width, height);
  if (state.view === "section") drawSectionView(ctx, width, height, true);
  else if (state.view === "exploded") drawExplodedView(ctx, width, height);
  else if (state.view === "orbital") drawOrbitalView(ctx, width, height);
  else drawWallView(ctx, width, height, nowMs);
}

function renderSection() {
  const canvas = $("sectionCanvas");
  const { ctx, width, height } = canvasMetrics(canvas);
  ctx.clearRect(0, 0, width, height);
  drawSectionView(ctx, width, height, false);
}

function buildRangeControls() {
  Object.entries(CONTROL_GROUPS).forEach(([containerId, definitions]) => {
    const container = $(containerId);
    container.textContent = "";
    if (containerId === "haloControls") {
      const toggle = document.createElement("label");
      toggle.className = "check-row";
      toggle.innerHTML = '<input id="haloEnabled" type="checkbox" checked><i></i><span>Halo enabled (independent COB system)</span>';
      container.append(toggle);
    }
    definitions.forEach(([key, label, min, max, step, unit]) => {
      const row = document.createElement("div");
      row.className = "range-control";
      row.innerHTML = `<div class="range-heading"><label for="control-${key}">${label}</label><output id="output-${key}">${formatValue(state[key], unit, step)}</output></div><input id="control-${key}" data-key="${key}" data-unit="${unit}" data-step="${step}" type="range" min="${min}" max="${max}" step="${step}" value="${state[key]}">`;
      container.append(row);
    });
  });
}

function updateRangeUI(input) {
  const min = Number(input.min), max = Number(input.max), value = Number(input.value);
  input.style.setProperty("--fill", `${(value - min) / (max - min) * 100}%`);
  const output = $(`output-${input.dataset.key}`);
  if (output) output.value = formatValue(value, input.dataset.unit, Number(input.dataset.step));
}

function prototypeWarnings(s = state) {
  const p = projectionModel(s);
  const halo = haloModel(s);
  const warnings = [];
  const direct = s.movementType === "quartz-driven-orbital-hands" ? directShaftDiscModel(s) : null;
  if (p.secondLength > halo.radius && s.haloEnabled && s.stage === "p3") warnings.push(["Shadow exceeds halo", "warn"]);
  if (s.secondLength > 115 || s.secondWidth > 1.4) warnings.push(["Second hand may load movement", "warn"]);
  if (s.sourceHandDistance < 10) warnings.push(["LED too close to hand plane", "warn"]);
  if (s.apertureDiameter < .5) warnings.push(["Tiny aperture may cut brightness", "warn"]);
  if (s.bodyDepth < s.movementDepth + 5) warnings.push(["Body shallow for movement", "warn"]);
  if (Math.max(s.movementEnvelopeWidth, s.movementEnvelopeHeight) > 114) warnings.push(["Movement envelope crowds Ø120 rear opening", "warn"]);
  if (s.mountingThickness >= 7.7) warnings.push(["Mounting thickness exceeds provisional 7.7 mm bushing", "warn"]);
  if (s.stage !== "p0" && s.stage !== "p3" && s.sourceHandDistance > s.bodyDepth - s.movementDepth - s.shellThickness) warnings.push(["Point-source path exceeds shell depth", "warn"]);
  if (direct && direct.worstHideMargin < s.requiredCarrierHideMargin) warnings.push(["Carrier/support shadow escapes fixed mask", "warn"]);
  if (direct && direct.requiredFullFieldAngle > s.minimumFullFieldAngle) warnings.push(["Optical cone exceeds 130° field", "warn"]);
  if (direct && direct.carriers.second.L < 30) warnings.push(["Source is too close to frontmost disc", "warn"]);
  if (direct && direct.flaredPodClearance.podMustEndBeforeConeExpands) warnings.push([`Continuous Ø150 pod vignettes; open by z${direct.flaredPodClearance.minimumPodEndZ.toFixed(1)} mm`, "warn"]);
  if (direct && (Math.abs(s.ledOffsetX) > .5 || Math.abs(s.ledOffsetY) > .5)) warnings.push(["LED/arbor axes exceed 0.5 mm alignment", "warn"]);
  warnings.push(["Verify LED thermal clearance from PLA", "warn"]);
  if (s.ringDiameter >= s.bodyDiameter - 8) warnings.push(["COB ring crowds shell edge", "warn"]);
  if (Math.abs(s.ledOffsetX) > 30 || Math.abs(s.ledOffsetY) > 30) warnings.push(["Large source offset shifts clock pivot", "warn"]);
  if (!warnings.length) warnings.push(["No obvious geometry conflict", "good"]);
  return warnings;
}

function renderMetrics() {
  const p = projectionModel();
  const halo = haloModel();
  const [sharpness, note] = shadowSharpness(p);
  const projectedDiameter = (state.secondEnabled ? p.secondLength : p.minuteLength) * 2;
  $("headerMagnification").textContent = `${p.magnification.toFixed(2)}×`;
  $("metricMagnification").textContent = `${p.magnification.toFixed(2)}×`;
  $("metricPenumbra").textContent = `${p.penumbra.toFixed(2)} mm`;
  $("metricSharpness").textContent = sharpness;
  $("metricSharpnessNote").textContent = note;
  $("projectedDiameterLabel").textContent = state.stage === "p0" ? `${Math.round(p.minuteLength)} mm · expected` : `${Math.round(projectedDiameter)} mm`;
  $("sectionGapBadge").textContent = `${state.wallGap} mm gap`;

  const dimensions = [
    ["Outer body", state.bodyDiameter, "mm"],
    ["Body depth", state.bodyDepth, "mm"],
    ["Wall gap", state.wallGap, "mm"],
    ["Source → hand (L)", p.L, "mm"],
    ["Hand → wall", p.handWall, "mm"],
    ["Source → wall (D)", p.D, "mm"],
    ["Point aperture", state.apertureDiameter, "mm"],
    ["Front shell", state.shellThickness, "mm"],
    ["Movement envelope W", state.movementEnvelopeWidth, "mm"],
    ["Movement envelope H", state.movementEnvelopeHeight, "mm"],
    ["Quartz overall (provisional)", state.hardwareOverallDepth, "mm"],
    ["Mounting thickness", state.mountingThickness, "mm"],
    ["COB ring", state.ringDiameter, "mm"],
    ["Projected clock", projectedDiameter, "mm"],
    ["Halo diameter", halo.diameter, "mm"],
    ["Hour shadow", p.hourLength, "mm"],
    ["Minute shadow", p.minuteLength, "mm"],
    ["Second shadow", p.secondLength, "mm"],
    ["Pivot translation", Math.hypot(p.pivotX, p.pivotY), "mm"]
  ];
  if (state.movementType === "quartz-driven-orbital-hands") {
    const direct = directShaftDiscModel(state);
    dimensions.push(
      ["Fixed mask physical Ø", direct.maskPhysicalRadius * 2, "mm"],
      ["Fixed mask wall Ø", direct.projectedMaskRadius * 2, "mm"],
      ["Worst carrier hide margin", direct.worstHideMargin, "mm"],
      ["Required full light field", direct.requiredFullFieldAngle, "deg"],
      ["Hour blocker z", direct.carriers.hour.planeZ, "mm"],
      ["Minute blocker z", direct.carriers.minute.planeZ, "mm"],
      ["Second blocker z", direct.carriers.second.planeZ, "mm"]
    );
  }
  $("dimensionsGrid").innerHTML = dimensions.map(([label, value, unit]) => `<div class="dimension-item"><span>${label}</span><b>${round(value, 1)}</b><small>${unit}</small></div>`).join("");

  const warnings = prototypeWarnings();
  $("warningsGrid").innerHTML = warnings.map(([label, type]) => `<div class="warning-chip ${type === "good" ? "good" : type === "info" ? "info" : ""}">${label}</div>`).join("");
  const bad = warnings.some(([, type]) => type === "warn");
  $("prototypeStatus").classList.toggle("has-warning", bad);
  $("prototypeStatus").querySelector("span").textContent = bad ? "Review flagged geometry" : "Concept looks viable";
}

function updateTimeReadout(nowMs = performance.now()) {
  const c = clockAngles(nowMs);
  $("sceneTime").textContent = `${String(c.hour).padStart(2, "0")}:${String(c.minute).padStart(2, "0")}:${String(c.second).padStart(2, "0")}`;
}

function applyStage(stageKey) {
  state.stage = stageKey;
  const stage = STAGES[stageKey];
  document.querySelectorAll(".stage-card").forEach(button => button.classList.toggle("is-active", button.dataset.stage === stageKey));
  $("stageDescription").textContent = stage.description;
  $("stageNote").textContent = stage.note;
  if (stageKey === "p0") {
    // Wired LED breadboard defaults. L is aperture plane to fake blockers.
    Object.assign(state, {
      sourceHandDistance: 40,
      wallGap: 45,
      movementDepth: 15,
      p0HandWallDistance: 60,
      hourLength: 45,
      minuteLength: 70,
      secondLength: 85,
      apertureDiameter: 1,
      secondEnabled: false,
      haloEnabled: false,
      movementType: "manual-concentric-ring-jig",
      useRealTime: false,
      showBody: false
    });
  } else if (stageKey === "p1") {
    Object.assign(state, { sourceHandDistance: 18, apertureDiameter: .8, haloEnabled: false, useRealTime: true, showBody: true, movementType: "standard-center-shaft-quartz", secondEnabled: true });
  } else if (stageKey === "p2") {
    Object.assign(state, REFERENCE_FINAL_PRESET, { stage: "p2", haloEnabled: false, useRealTime: true, showBody: true });
  } else if (stageKey === "p3") {
    Object.assign(state, REFERENCE_FINAL_PRESET, { stage: "p3", haloEnabled: true, useRealTime: true, showBody: true });
  }
  if (rendererMode === "3d") {
    state.view = DEFAULT_THREE_VIEW;
    syncVisualizationViewButtons(state.view);
    threeScene?.setView(state.view);
  }
  syncAllInputs();
  updateStageContext();
  renderAll();
}

function updateStageContext() {
  const stage = STAGES[state.stage];
  $("stageDescription").textContent = stage.description;
  $("stageNote").textContent = stage.note;
  $("visualKicker").textContent = `${state.stage.toUpperCase()} / ${stage.source}`;
  $("visualTitle").textContent = state.view === "wall" ? stage.title : state.view === "section" ? "Room-side source to wall" : state.view === "orbital" ? "Direct-shaft quartz stack" : "Parts before commitment";
  $("stageAim").textContent = stage.aim;
  $("stageParts").textContent = stage.parts;
  $("stagePass").textContent = stage.pass;
  $("stageMovement").textContent = stage.movement;
  $("stageBuy").textContent = stage.buy;
  const [haloTitle, haloDetail, haloState, shadowTitle, shadowDetail, shadowState] = stage.stack;
  $("stackHaloTitle").textContent = haloTitle;
  $("stackHaloDetail").textContent = haloDetail;
  $("stackHaloState").textContent = haloState;
  $("stackShadowTitle").textContent = shadowTitle;
  $("stackShadowDetail").textContent = shadowDetail;
  $("stackShadowState").textContent = shadowState;
  const p0DistanceInput = $("control-p0HandWallDistance");
  const p0DistanceAvailable = controlAvailability(state.stage).p0HandWallDistance;
  p0DistanceInput.disabled = !p0DistanceAvailable;
  p0DistanceInput.closest(".range-control").hidden = !p0DistanceAvailable;
  $("visualCaption").querySelector("span").textContent = state.stage === "p0" ? "P0 target / minute shadow" : "Projected shadow diameter";
  if (state.stage === "p0") $("projectedDiameterLabel").textContent = `${Math.round(projectionModel().minuteLength)} mm · expected`;
}

function renderAll() {
  renderMetrics();
  updateTimeReadout();
  renderSection();
  renderHero();
  if (rendererMode === "2d") startTwoDLoop();
}

function syncAllInputs() {
  document.querySelectorAll('input[type="range"][data-key]').forEach(input => {
    input.value = state[input.dataset.key];
    updateRangeUI(input);
  });
  $("haloEnabled").checked = state.haloEnabled;
  $("useRealTime").checked = state.useRealTime;
  $("manualHour").value = state.manualHour;
  $("manualMinute").value = state.manualMinute;
  $("manualSecond").value = state.manualSecond;
  $("showBody").checked = state.showBody;
  $("showLabels").checked = state.showLabels;
  $("showRays").checked = state.showRays;
  $("showDimensions").checked = state.showDimensions;
  $("surfaceTreatment").value = state.surface;
  document.querySelectorAll("[data-sweep]").forEach(button => button.classList.toggle("is-active", button.dataset.sweep === state.sweepMode));
  document.querySelectorAll("[data-material]").forEach(button => button.classList.toggle("is-active", button.dataset.material === state.material));
}

function wireInteractions() {
  document.querySelectorAll('input[type="range"][data-key]').forEach(input => {
    updateRangeUI(input);
    input.addEventListener("input", () => {
      state[input.dataset.key] = Number(input.value);
      updateRangeUI(input);
      renderAll();
    });
  });
  $("haloEnabled").addEventListener("change", event => { state.haloEnabled = event.target.checked; renderAll(); });
  $("useRealTime").addEventListener("change", event => { state.useRealTime = event.target.checked; renderAll(); });
  [["manualHour", "manualHour", 0, 23], ["manualMinute", "manualMinute", 0, 59], ["manualSecond", "manualSecond", 0, 59]].forEach(([id, key, min, max]) => {
    $(id).addEventListener("input", event => { state[key] = clamp(Number(event.target.value) || 0, min, max); renderAll(); });
  });
  [["showBody", "showBody"], ["showLabels", "showLabels"], ["showRays", "showRays"], ["showDimensions", "showDimensions"]].forEach(([id, key]) => {
    $(id).addEventListener("change", event => { state[key] = event.target.checked; renderAll(); });
  });
  $("surfaceTreatment").addEventListener("change", event => { state.surface = event.target.value; renderAll(); });
  document.querySelectorAll("[data-sweep]").forEach(button => button.addEventListener("click", () => {
    state.sweepMode = button.dataset.sweep; syncAllInputs(); renderAll();
  }));
  document.querySelectorAll("[data-material]").forEach(button => button.addEventListener("click", () => {
    state.material = button.dataset.material; syncAllInputs(); renderAll();
  }));
  document.querySelectorAll("[data-stage]").forEach(button => button.addEventListener("click", () => applyStage(button.dataset.stage)));
  document.querySelectorAll(".view-tab").forEach(button => button.addEventListener("click", () => {
    selectVisualizationView(button.dataset.view);
  }));
  document.querySelectorAll("[data-three-view]").forEach(button => button.addEventListener("click", () => {
    selectVisualizationView(button.dataset.threeView);
  }));
  $("renderer3dButton").addEventListener("click", () => setRendererMode("3d"));
  $("renderer2dButton").addEventListener("click", () => setRendererMode("2d"));
  $("reset3dButton").addEventListener("click", () => threeScene?.resetView());
  document.querySelectorAll("[data-preset]").forEach(button => button.addEventListener("click", () => {
    Object.assign(state, LIGHTING_PRESETS[button.dataset.preset]);
    document.querySelectorAll("[data-preset]").forEach(item => item.classList.toggle("is-active", item === button));
    syncAllInputs(); renderAll();
  }));
  $("resetButton").addEventListener("click", () => {
    Object.assign(state, OPTICAL_DEFAULTS);
    document.querySelectorAll("[data-stage]").forEach(button => button.classList.toggle("is-active", button.dataset.stage === "p0"));
    selectVisualizationView(rendererMode === "3d" ? DEFAULT_THREE_VIEW : "wall", false);
    syncAllInputs(); updateStageContext(); renderAll();
  });
}

let lastAnimatedFrame = 0;
let twoDAnimationFrame = 0;
let twoDTickTimer = 0;
const reduceMotionMedia = typeof matchMedia === "function" ? matchMedia("(prefers-reduced-motion: reduce)") : { matches: false };
function animationLoop(nowMs) {
  if (rendererMode !== "2d" || !state.useRealTime || state.sweepMode !== "sweep" || reduceMotionMedia.matches) {
    twoDAnimationFrame = 0;
    return;
  }
  if (nowMs - lastAnimatedFrame > 30) {
    if (state.view === "wall") renderHero(nowMs);
    updateTimeReadout(nowMs);
    lastAnimatedFrame = nowMs;
  }
  twoDAnimationFrame = requestAnimationFrame(animationLoop);
}

function startTwoDLoop() {
  const continuous = state.useRealTime && state.sweepMode === "sweep" && !reduceMotionMedia.matches;
  if (continuous) {
    if (twoDTickTimer) { clearInterval(twoDTickTimer); twoDTickTimer = 0; }
    if (!twoDAnimationFrame) twoDAnimationFrame = requestAnimationFrame(animationLoop);
    return;
  }
  if (twoDAnimationFrame) { cancelAnimationFrame(twoDAnimationFrame); twoDAnimationFrame = 0; }
  if (state.useRealTime && !twoDTickTimer) {
    twoDTickTimer = setInterval(() => { renderHero(); updateTimeReadout(); }, 1000);
  } else if (!state.useRealTime && twoDTickTimer) {
    clearInterval(twoDTickTimer);
    twoDTickTimer = 0;
  }
}

function stopTwoDLoop() {
  if (twoDAnimationFrame) cancelAnimationFrame(twoDAnimationFrame);
  if (twoDTickTimer) clearInterval(twoDTickTimer);
  twoDAnimationFrame = 0;
  twoDTickTimer = 0;
}

function init() {
  buildRangeControls();
  wireInteractions();
  syncAllInputs();
  updateStageContext();
  renderAll();
  const observedCanvasSizes = new WeakMap();
  let pendingResizeFrame = 0;
  const onResize = entries => {
    let dimensionsChanged = false;
    entries.forEach(entry => {
      const nextSize = normalizedCanvasCssSize(entry.contentRect.width, entry.contentRect.height);
      const previousSize = observedCanvasSizes.get(entry.target);
      if (!previousSize || previousSize.width !== nextSize.width || previousSize.height !== nextSize.height) {
        observedCanvasSizes.set(entry.target, nextSize);
        dimensionsChanged = true;
      }
    });
    if (!dimensionsChanged || pendingResizeFrame) return;
    pendingResizeFrame = requestAnimationFrame(() => {
      pendingResizeFrame = 0;
      renderAll();
    });
  };
  if (typeof ResizeObserver === "function") {
    const resizeObserver = new ResizeObserver(onResize);
    resizeObserver.observe($("heroVisual"));
    resizeObserver.observe($("sectionCanvas"));
  } else {
    window.addEventListener("resize", () => renderAll(), { passive: true });
  }
  mountThreeRenderer();
}

const KageModel = Object.freeze({
  defaults: OPTICAL_DEFAULTS,
  referenceFinalPreset: REFERENCE_FINAL_PRESET,
  stages: STAGES,
  projectionModel,
  directShaftDiscModel,
  orbitalCarrierModel,
  movementStudyModel,
  haloModel,
  pointLightModel,
  shadowOpacity,
  drawProjectedMaskShadow,
  clockAngles,
  shadowSharpness,
  prototypeWarnings,
  handToWallDistance,
  controlAvailability,
  threeSceneSnapshot,
  normalizedCanvasCssSize,
  heroCanvasLayout
});

if (typeof globalThis !== "undefined") globalThis.KageModel = KageModel;
if (typeof module !== "undefined" && module.exports) module.exports = KageModel;
if (typeof document !== "undefined") {
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
}
