import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

export const HAND_ORDER = Object.freeze(["hour", "minute", "second"]);
export const TOWER_ANGLES_DEGREES = Object.freeze([60, 180, 300]);
export const CARRIER_BANDS_MM = Object.freeze({
  hour: Object.freeze([-1.50, 1.50]),
  minute: Object.freeze([4.05, 7.05]),
  second: Object.freeze([9.60, 12.60]),
});
export const GEAR_FACE_BANDS_MM = Object.freeze({
  hour: Object.freeze([-0.70, 1.40]),
  minute: Object.freeze([4.85, 6.95]),
  second: Object.freeze([10.40, 12.50]),
});
export const RACE_BANDS_MM = Object.freeze({
  hour: Object.freeze([-1.50, -0.70]),
  minute: Object.freeze([4.05, 4.85]),
  second: Object.freeze([9.60, 10.40]),
});
export const CONTACT_BANDS_MM = Object.freeze({
  hour: Object.freeze([-1.40, -0.80]),
  minute: Object.freeze([4.15, 4.75]),
  second: Object.freeze([9.70, 10.30]),
});
export const DIRECT_RACE_MM = Object.freeze({
  carrierRaceRadius: 131.60,
  toothTipRadius: 129.00,
  toothRootRadius: 132.50,
  rollerAxisRadius: 125.50,
  rollerHubDiameter: 6.00,
  rollerRunningDiameter: 12.10,
  rollerFlangeDiameter: 13.80,
  contactLandWidth: 0.60,
  nominalRadialGap: 0.05,
  radialCaptureOverlap: 0.80,
  axialRelief: 0.15,
  adjustableTowerAngle: 300,
  adjustableTowerRange: Object.freeze([-0.25, 0.25]),
});
export const MAX_BUFFER_PIXELS = 2_073_600;

const CARRIER_OUTER_RADIUS = 138.90;
const HAND_COLORS = Object.freeze({ hour: 0xe9633d, minute: 0xf0b54d, second: 0x255b62 });
const CAMERA_PRESETS = Object.freeze({
  assembled: { position: [244, -280, 198], target: [0, 0, 5.55] },
  cutaway: { position: [265, -230, 116], target: [0, 0, 5.55] },
  exploded: { position: [275, -300, 228], target: [0, 0, 5.55] },
});

export function geometryContract() {
  return {
    decision: "three-direct-gear-race-spinner-towers",
    separateGuideFeature: false,
    rollerContactSurface: "carrier-inner-root-land-below-tooth-face",
    carrierRaceRadiusMm: DIRECT_RACE_MM.carrierRaceRadius,
    toothTipRadiusMm: DIRECT_RACE_MM.toothTipRadius,
    toothRootRadiusMm: DIRECT_RACE_MM.toothRootRadius,
    rollerAxisRadiusMm: DIRECT_RACE_MM.rollerAxisRadius,
    rollerHubDiameterMm: DIRECT_RACE_MM.rollerHubDiameter,
    rollerRunningDiameterMm: DIRECT_RACE_MM.rollerRunningDiameter,
    rollerFlangeDiameterMm: DIRECT_RACE_MM.rollerFlangeDiameter,
    contactLandWidthMm: DIRECT_RACE_MM.contactLandWidth,
    nominalRadialGapMm: DIRECT_RACE_MM.nominalRadialGap,
    radialCaptureOverlapMm: DIRECT_RACE_MM.radialCaptureOverlap,
    axialReliefMm: DIRECT_RACE_MM.axialRelief,
    toothTipRollingAllowed: false,
    towerAnglesDegrees: [...TOWER_ANGLES_DEGREES],
    towerCount: TOWER_ANGLES_DEGREES.length,
    rollersPerTower: HAND_ORDER.length,
    rollerCount: TOWER_ANGLES_DEGREES.length * HAND_ORDER.length,
    independentlyRotatingRollers: true,
    fixedTowerAnglesDegrees: [60, 180],
    adjustableTowerAngleDegrees: DIRECT_RACE_MM.adjustableTowerAngle,
    adjustableTowerRangeMm: [...DIRECT_RACE_MM.adjustableTowerRange],
    carrierBandsMm: Object.fromEntries(HAND_ORDER.map((hand) => [hand, [...CARRIER_BANDS_MM[hand]]])),
    gearFaceBandsMm: Object.fromEntries(HAND_ORDER.map((hand) => [hand, [...GEAR_FACE_BANDS_MM[hand]]])),
    raceBandsMm: Object.fromEntries(HAND_ORDER.map((hand) => [hand, [...RACE_BANDS_MM[hand]]])),
    contactBandsMm: Object.fromEntries(HAND_ORDER.map((hand) => [hand, [...CONTACT_BANDS_MM[hand]]])),
    physicalValidation: "required-for-seam-bump-friction-wear-noise-and-adjustment",
  };
}

export function derivedClearances(adjustmentMm = 0) {
  const adjustment = THREE.MathUtils.clamp(Number(adjustmentMm) || 0, ...DIRECT_RACE_MM.adjustableTowerRange);
  const axis = DIRECT_RACE_MM.rollerAxisRadius + adjustment;
  return {
    adjustedAxisRadiusMm: axis,
    runningOuterRadiusMm: axis + DIRECT_RACE_MM.rollerRunningDiameter / 2,
    flangeOuterRadiusMm: axis + DIRECT_RACE_MM.rollerFlangeDiameter / 2,
    nominalRaceGapMm: DIRECT_RACE_MM.carrierRaceRadius - (DIRECT_RACE_MM.rollerAxisRadius + DIRECT_RACE_MM.rollerRunningDiameter / 2),
    toothTipHubClearanceMm: DIRECT_RACE_MM.toothTipRadius - (axis + DIRECT_RACE_MM.rollerHubDiameter / 2),
  };
}

export function boundedBufferSize(cssWidth, cssHeight, devicePixelRatio = 1) {
  const width = Math.max(1, Math.round(Number(cssWidth) || 0));
  const height = Math.max(1, Math.round(Number(cssHeight) || 0));
  let dpr = Math.min(1.5, Math.max(1, Number(devicePixelRatio) || 1));
  const requested = width * height * dpr * dpr;
  if (requested > MAX_BUFFER_PIXELS) dpr *= Math.sqrt(MAX_BUFFER_PIXELS / requested);
  const bufferWidth = Math.max(1, Math.floor(width * dpr));
  const bufferHeight = Math.max(1, Math.floor(height * dpr));
  return { cssWidth: width, cssHeight: height, dpr, bufferWidth, bufferHeight, bufferPixels: bufferWidth * bufferHeight };
}

export function normalizeState(input = {}) {
  const comparison = input.comparison === "legacy" ? "legacy" : "proposed";
  const arrangement = ["assembled", "cutaway", "exploded"].includes(input.arrangement) ? input.arrangement : "assembled";
  const selectedHand = [...HAND_ORDER, "all"].includes(input.selectedHand) ? input.selectedHand : "all";
  const adjustment = THREE.MathUtils.clamp(Number(input.adjustmentMm) || 0, ...DIRECT_RACE_MM.adjustableTowerRange);
  const rotationDegrees = ((Number(input.rotationDegrees) || 0) % 360 + 360) % 360;
  const assemblyStep = THREE.MathUtils.clamp(Math.round(Number(input.assemblyStep) || 0), 0, 4);
  return { comparison, arrangement, selectedHand, adjustmentMm: adjustment, rotationDegrees, showLabels: input.showLabels !== false, showForces: input.showForces !== false, assemblyStep };
}

export function comparisonVisibility(comparison) {
  const state = normalizeState({ comparison });
  return { directRaceRollers: state.comparison === "proposed", legacyKeepers: state.comparison === "legacy" };
}

export function assemblyVisibility(step) {
  const value = normalizeState({ assemblyStep: step }).assemblyStep;
  return { rings: true, fixedTowerFrames: value >= 1, adjustableTowerFrame: value >= 2, rollersOrKeepers: value >= 3, contactAnnotations: value >= 4 };
}

function material(color, options = {}) {
  return new THREE.MeshStandardMaterial({ color, roughness: options.roughness ?? 0.58, metalness: options.metalness ?? 0.02, side: THREE.DoubleSide, transparent: true, opacity: 1 });
}

function annulus(innerRadius, outerRadius, depth, meshMaterial, segments = 180) {
  const shape = new THREE.Shape();
  shape.absarc(0, 0, outerRadius, 0, Math.PI * 2, false);
  const hole = new THREE.Path();
  hole.absarc(0, 0, innerRadius, 0, Math.PI * 2, true);
  shape.holes.push(hole);
  const geometry = new THREE.ExtrudeGeometry(shape, { depth, bevelEnabled: false, curveSegments: segments });
  geometry.translate(0, 0, -depth / 2);
  return new THREE.Mesh(geometry, meshMaterial);
}

function bandCenter(band) { return (band[0] + band[1]) / 2; }
function polar(radius, degrees, z = 0) {
  const angle = THREE.MathUtils.degToRad(degrees);
  return new THREE.Vector3(Math.cos(angle) * radius, Math.sin(angle) * radius, z);
}

function createCarrier(hand, index) {
  const group = new THREE.Group();
  const carrierBand = CARRIER_BANDS_MM[hand];
  const gearBand = GEAR_FACE_BANDS_MM[hand];
  const raceBand = RACE_BANDS_MM[hand];
  const center = bandCenter(carrierBand);
  const color = HAND_COLORS[hand];
  group.name = `${hand}-bare-260t-carrier-with-lower-root-race`;
  group.userData.hand = hand;
  group.userData.baseZ = center;

  const carrierMaterial = material(color);
  const carrier = annulus(DIRECT_RACE_MM.carrierRaceRadius, CARRIER_OUTER_RADIUS, carrierBand[1] - carrierBand[0], carrierMaterial);
  carrier.name = `${hand}-bare-carrier-body-r131p60-to-r138p90`;
  carrier.castShadow = true;
  group.add(carrier);

  // Zero-thickness highlight on the carrier's own lower inner cylinder. It is
  // a display surface, not an additional mechanical feature.
  const raceMaterial = material(0xf8dfa1, { roughness: 0.28 });
  const raceHeight = raceBand[1] - raceBand[0];
  const raceSurface = new THREE.Mesh(new THREE.CylinderGeometry(DIRECT_RACE_MM.carrierRaceRadius, DIRECT_RACE_MM.carrierRaceRadius, raceHeight, 180, 1, true), raceMaterial);
  raceSurface.geometry.rotateX(Math.PI / 2);
  raceSurface.position.z = bandCenter(raceBand) - center;
  raceSurface.name = `${hand}-carrier-inner-root-land-display-surface-r131p60`;
  group.add(raceSurface);

  const teeth = new THREE.Group();
  teeth.name = `${hand}-260t-tooth-envelope-separated-above-race`;
  const toothMaterial = material(0x332c25, { roughness: 0.72 });
  const toothHeight = gearBand[1] - gearBand[0];
  for (let toothIndex = 0; toothIndex < 260; toothIndex += 1) {
    const angle = toothIndex / 260 * Math.PI * 2;
    const tooth = new THREE.Mesh(new THREE.BoxGeometry(DIRECT_RACE_MM.toothRootRadius - DIRECT_RACE_MM.toothTipRadius, 1.08, toothHeight), toothMaterial);
    tooth.name = `${hand}-gear-tooth-${String(toothIndex + 1).padStart(3, "0")}`;
    tooth.position.set(Math.cos(angle) * ((DIRECT_RACE_MM.toothRootRadius + DIRECT_RACE_MM.toothTipRadius) / 2), Math.sin(angle) * ((DIRECT_RACE_MM.toothRootRadius + DIRECT_RACE_MM.toothTipRadius) / 2), bandCenter(gearBand) - center);
    tooth.rotation.z = angle;
    tooth.userData.angle = angle;
    teeth.add(tooth);
  }
  group.add(teeth);

  const lengths = [18, 24, 31];
  const widths = [5.2, 3.8, 2.4];
  const finMaterial = material(color, { roughness: 0.50 });
  const fin = new THREE.Mesh(new THREE.BoxGeometry(widths[index], lengths[index], 2.1), finMaterial);
  fin.name = `${hand}-outer-shadow-fin`;
  fin.position.y = CARRIER_OUTER_RADIUS + lengths[index] / 2;
  group.add(fin);

  group.position.z = center;
  group.userData.materials = [carrierMaterial, raceMaterial, toothMaterial, finMaterial];
  group.userData.teeth = teeth;
  return group;
}

function createRelievedRollerGeometry(hand) {
  const [z0, z1] = CARRIER_BANDS_MM[hand];
  const [contact0, contact1] = CONTACT_BANDS_MM[hand];
  const lower0 = z0 - 0.65;
  const lower1 = z0 - 0.15;
  const upper0 = z1 + 0.15;
  const upper1 = z1 + 0.65;
  const rHub = DIRECT_RACE_MM.rollerHubDiameter / 2;
  const rLand = DIRECT_RACE_MM.rollerRunningDiameter / 2;
  const rFlange = DIRECT_RACE_MM.rollerFlangeDiameter / 2;
  const profile = [
    [lower0, rHub], [lower0, rFlange], [lower1, rFlange], [lower1, rHub],
    [contact0, rHub], [contact0, rLand], [contact1, rLand], [contact1, rHub],
    [upper0, rHub], [upper0, rFlange], [upper1, rFlange], [upper1, rHub],
  ].map(([z, radius]) => new THREE.Vector2(radius, z));
  const geometry = new THREE.LatheGeometry(profile, 64);
  geometry.rotateX(Math.PI / 2);
  geometry.computeVertexNormals();
  return geometry;
}

function createTower(angleDegrees, towerIndex) {
  const tower = new THREE.Group();
  const adjustable = angleDegrees === DIRECT_RACE_MM.adjustableTowerAngle;
  tower.name = adjustable ? `tower-${towerIndex + 1}-adjustable-300deg` : `tower-${towerIndex + 1}-fixed-${angleDegrees}deg`;
  tower.userData.angleDegrees = angleDegrees;
  tower.userData.adjustable = adjustable;
  tower.userData.baseRadius = DIRECT_RACE_MM.rollerAxisRadius;

  const frame = new THREE.Group();
  frame.name = `${tower.name}-compact-unibody-frame`;
  const frameMaterial = material(adjustable ? 0xe9633d : 0x36322d, { roughness: 0.74 });
  const pin = new THREE.Mesh(new THREE.CylinderGeometry(2, 2, 25, 24), frameMaterial);
  pin.geometry.rotateX(Math.PI / 2);
  pin.position.z = 7.5;
  pin.name = `${tower.name}-d4x25-axle`;
  frame.add(pin);
  const foot = new THREE.Mesh(new THREE.BoxGeometry(13, 8, 2.3), frameMaterial);
  foot.position.z = -5.2;
  foot.name = `${tower.name}-m3-mount-foot-envelope`;
  frame.add(foot);

  const rollers = new THREE.Group();
  rollers.name = `${tower.name}-three-relieved-asymmetric-rollers`;
  HAND_ORDER.forEach((hand) => {
    const rollerMaterial = material(HAND_COLORS[hand], { roughness: 0.34 });
    const roller = new THREE.Mesh(createRelievedRollerGeometry(hand), rollerMaterial);
    roller.name = `tower-${towerIndex + 1}-${hand}-relieved-carrier-race-roller`;
    roller.castShadow = true;
    roller.userData.hand = hand;
    rollers.add(roller);
  });
  tower.add(frame, rollers);
  tower.userData.frame = frame;
  tower.userData.rollers = rollers;
  tower.userData.material = frameMaterial;
  tower.position.copy(polar(DIRECT_RACE_MM.rollerAxisRadius, angleDegrees));
  return tower;
}

function createLegacyKeepers() {
  const group = new THREE.Group();
  group.name = "legacy-multipart-under-stack-keeper-system";
  const legacyMaterial = material(0x686157, { roughness: 0.82 });
  HAND_ORDER.forEach((hand) => {
    [60, 180, 300].forEach((angle, index) => {
      const keeper = new THREE.Mesh(new THREE.BoxGeometry(13, 9, 5.5), legacyMaterial);
      keeper.name = `${hand}-legacy-keeper-${index + 1}`;
      keeper.position.copy(polar(141, angle, bandCenter(CARRIER_BANDS_MM[hand])));
      keeper.rotation.z = THREE.MathUtils.degToRad(angle);
      group.add(keeper);
    });
  });
  group.userData.material = legacyMaterial;
  return group;
}

function createLabel(text, color = "#2b2924") {
  const canvas = document.createElement("canvas");
  canvas.width = 384;
  canvas.height = 80;
  const context = canvas.getContext("2d");
  context.fillStyle = "rgba(250,247,239,.94)";
  context.beginPath();
  context.roundRect(2, 2, 380, 76, 18);
  context.fill();
  context.fillStyle = color;
  context.font = "600 25px system-ui, sans-serif";
  context.textAlign = "center";
  context.textBaseline = "middle";
  context.fillText(text, 192, 41);
  const texture = new THREE.CanvasTexture(canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  const sprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: texture, transparent: true, depthTest: false }));
  sprite.scale.set(63, 13, 1);
  sprite.userData.texture = texture;
  return sprite;
}

function createAnnotations(towers) {
  const labels = new THREE.Group();
  labels.name = "direct-race-contact-labels";
  HAND_ORDER.forEach((hand, index) => {
    const label = createLabel(`${hand.toUpperCase()} RACE  ${RACE_BANDS_MM[hand][0].toFixed(2)} → ${RACE_BANDS_MM[hand][1].toFixed(2)} mm`);
    label.position.set(-55, 174, bandCenter(CARRIER_BANDS_MM[hand]) + index * 3.5);
    labels.add(label);
  });
  const forces = new THREE.Group();
  forces.name = "carrier-race-capture-arrows";
  towers.forEach((tower, index) => {
    const angle = THREE.MathUtils.degToRad(tower.userData.angleDegrees);
    const origin = polar(160, tower.userData.angleDegrees, bandCenter(CARRIER_BANDS_MM.minute));
    const direction = new THREE.Vector3(-Math.cos(angle), -Math.sin(angle), 0).normalize();
    forces.add(new THREE.ArrowHelper(direction, origin, 24, index === 2 ? 0xe9633d : 0x9dad43, 6, 3.8));
  });
  return { labels, forces };
}

function setOpacity(materials, opacity) {
  materials.forEach((item) => { item.opacity = opacity; item.depthWrite = opacity >= 0.99; });
}

function disposeTree(root) {
  root.traverse((object) => {
    object.geometry?.dispose?.();
    const materials = Array.isArray(object.material) ? object.material : [object.material];
    materials.filter(Boolean).forEach((item) => { item.map?.dispose?.(); item.dispose?.(); });
    object.userData?.texture?.dispose?.();
  });
}

export function mount(options = {}) {
  const canvas = options.canvas;
  const parent = options.parent || canvas?.parentElement;
  if (!canvas || !parent) throw new Error("Direct gear-race ADR requires a canvas and bounded parent");
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false, powerPreference: "high-performance" });
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.02;
  renderer.setClearColor(0xd9d1c2, 1);
  renderer.shadowMap.enabled = true;
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0xd9d1c2);
  scene.fog = new THREE.Fog(0xd9d1c2, 440, 900);
  const camera = new THREE.PerspectiveCamera(34, 1, 0.1, 1600);
  const controls = new OrbitControls(camera, canvas);
  controls.enableDamping = true;
  controls.dampingFactor = 0.075;
  controls.minDistance = 175;
  controls.maxDistance = 760;
  controls.enablePan = false;

  const assembly = new THREE.Group();
  assembly.name = "direct-gear-race-guidance-adr-assembly";
  const rings = HAND_ORDER.map(createCarrier);
  const proposed = new THREE.Group();
  proposed.name = "proposed-three-towers-direct-on-carrier-lower-root-land";
  const towers = TOWER_ANGLES_DEGREES.map(createTower);
  towers.forEach((tower) => proposed.add(tower));
  const legacyKeepers = createLegacyKeepers();
  const annotations = createAnnotations(towers);
  assembly.add(...rings, proposed, legacyKeepers, annotations.labels, annotations.forces);
  scene.add(assembly);

  const floor = new THREE.Mesh(new THREE.PlaneGeometry(950, 950), material(0xe8e2d7, { roughness: 1 }));
  floor.position.z = -14;
  floor.receiveShadow = true;
  scene.add(floor, new THREE.HemisphereLight(0xfff8e8, 0x655c50, 2.2));
  const key = new THREE.DirectionalLight(0xffe0ad, 5.5);
  key.position.set(-190, -240, 410);
  key.castShadow = true;
  scene.add(key);
  const rim = new THREE.DirectionalLight(0xbce5db, 3.2);
  rim.position.set(320, 110, 210);
  scene.add(rim);

  let state = normalizeState(options.initialState);
  let destroyed = false;
  let frameRequested = false;
  function requestRender() {
    if (destroyed || frameRequested) return;
    frameRequested = true;
    requestAnimationFrame(() => { frameRequested = false; controls.update(); renderer.render(scene, camera); });
  }
  function setCameraPreset(arrangement, immediate = false) {
    const preset = CAMERA_PRESETS[arrangement] || CAMERA_PRESETS.assembled;
    camera.position.fromArray(preset.position);
    controls.target.fromArray(preset.target);
    controls.update();
    if (immediate) renderer.render(scene, camera); else requestRender();
  }
  function applyState(nextState) {
    state = normalizeState({ ...state, ...nextState });
    const visibility = comparisonVisibility(state.comparison);
    const step = assemblyVisibility(state.assemblyStep);
    proposed.visible = visibility.directRaceRollers;
    legacyKeepers.visible = visibility.legacyKeepers && step.rollersOrKeepers;
    const explode = state.arrangement === "exploded" ? [-11, 0, 11] : [0, 0, 0];
    rings.forEach((ring, index) => {
      const hand = HAND_ORDER[index];
      ring.position.z = ring.userData.baseZ + explode[index];
      ring.rotation.z = THREE.MathUtils.degToRad(state.rotationDegrees * [1, 0.62, 1.37][index]);
      const selected = state.selectedHand === "all" || state.selectedHand === hand;
      setOpacity(ring.userData.materials, selected ? (state.arrangement === "cutaway" ? 0.78 : 1) : 0.16);
      ring.userData.teeth.children.forEach((tooth) => { tooth.visible = !(state.arrangement === "cutaway" && Math.cos(tooth.userData.angle) > 0.28); });
      ring.visible = step.rings;
    });
    towers.forEach((tower, towerIndex) => {
      const radius = tower.userData.baseRadius + (tower.userData.adjustable ? state.adjustmentMm : 0);
      tower.position.copy(polar(radius, tower.userData.angleDegrees));
      tower.userData.frame.visible = tower.userData.adjustable ? step.adjustableTowerFrame : step.fixedTowerFrames;
      tower.userData.rollers.visible = step.rollersOrKeepers;
      tower.userData.rollers.children.forEach((roller, handIndex) => {
        const hand = HAND_ORDER[handIndex];
        roller.position.z = explode[handIndex];
        roller.rotation.z = THREE.MathUtils.degToRad(-state.rotationDegrees * [1, 0.62, 1.37][handIndex]);
        roller.material.opacity = state.selectedHand === "all" || state.selectedHand === hand ? 1 : 0.16;
        roller.material.depthWrite = roller.material.opacity >= 0.99;
      });
      tower.userData.material.opacity = tower.userData.adjustable ? 1 : 0.82;
    });
    annotations.labels.visible = state.showLabels && step.contactAnnotations;
    annotations.forces.visible = state.showForces && step.contactAnnotations && visibility.directRaceRollers;
    options.onStateChange?.(state, geometryContract(), derivedClearances(state.adjustmentMm));
    requestRender();
    return { ...state };
  }
  function resize() {
    const rect = parent.getBoundingClientRect();
    const next = boundedBufferSize(rect.width, rect.height, globalThis.devicePixelRatio || 1);
    renderer.setPixelRatio(next.dpr);
    renderer.setSize(next.cssWidth, next.cssHeight, false);
    camera.aspect = next.cssWidth / next.cssHeight;
    camera.updateProjectionMatrix();
    requestRender();
  }
  const resizeObserver = new ResizeObserver(resize);
  resizeObserver.observe(parent);
  controls.addEventListener("change", requestRender);
  setCameraPreset(state.arrangement, true);
  applyState(state);
  resize();
  return {
    getState: () => ({ ...state }), setState: applyState, setCameraPreset, resize,
    dispose() { destroyed = true; resizeObserver.disconnect(); controls.removeEventListener("change", requestRender); controls.dispose(); disposeTree(scene); renderer.dispose(); },
  };
}

export { CAMERA_PRESETS };
