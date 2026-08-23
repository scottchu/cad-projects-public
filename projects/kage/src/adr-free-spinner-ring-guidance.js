import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

export const HAND_ORDER = Object.freeze(["hour", "minute", "second"]);
export const TOWER_ANGLES_DEGREES = Object.freeze([60, 180, 300]);
export const CARRIER_BANDS_MM = Object.freeze({
  hour: Object.freeze([-1.5, 1.5]),
  minute: Object.freeze([4.05, 7.05]),
  second: Object.freeze([9.6, 12.6]),
});
export const GUIDANCE_MM = Object.freeze({
  guideBead: 0.8,
  nominalRadialGap: 0.05,
  radialCaptureOverlap: 0.8,
  axialRelief: Object.freeze([0.10, 0.15]),
  adjustableTowerAngle: 300,
  adjustableTowerRange: Object.freeze([-0.25, 0.25]),
});
export const MAX_BUFFER_PIXELS = 2_073_600;

const RING_INNER_RADIUS = 54;
const RING_OUTER_RADIUS = 72;
const GUIDE_BEAD_CENTER_RADIUS = 72.4;
const ROLLER_RUNNING_RADIUS = 3.95;
const ROLLER_AXIS_RADIUS = GUIDE_BEAD_CENTER_RADIUS + GUIDANCE_MM.guideBead / 2 + GUIDANCE_MM.nominalRadialGap + ROLLER_RUNNING_RADIUS;
const HAND_COLORS = Object.freeze({ hour: 0xe9633d, minute: 0xf0b54d, second: 0x255b62 });
const CAMERA_PRESETS = Object.freeze({
  assembled: { position: [122, -142, 112], target: [0, 0, 5.55] },
  cutaway: { position: [136, -116, 64], target: [0, 0, 5.55] },
  exploded: { position: [142, -154, 126], target: [0, 0, 5.55] },
});

export function geometryContract() {
  return {
    decision: "three-free-spinner-towers",
    towerAnglesDegrees: [...TOWER_ANGLES_DEGREES],
    towerCount: TOWER_ANGLES_DEGREES.length,
    rollersPerTower: HAND_ORDER.length,
    rollerCount: TOWER_ANGLES_DEGREES.length * HAND_ORDER.length,
    independentlyRotatingRollers: true,
    fixedTowerAnglesDegrees: [60, 180],
    adjustableTowerAngleDegrees: GUIDANCE_MM.adjustableTowerAngle,
    adjustableTowerRangeMm: [...GUIDANCE_MM.adjustableTowerRange],
    carrierBandsMm: Object.fromEntries(HAND_ORDER.map((hand) => [hand, [...CARRIER_BANDS_MM[hand]]])),
    guideBeadMm: GUIDANCE_MM.guideBead,
    nominalRadialGapMm: GUIDANCE_MM.nominalRadialGap,
    radialCaptureOverlapMm: GUIDANCE_MM.radialCaptureOverlap,
    axialReliefMm: [...GUIDANCE_MM.axialRelief],
    rollerContactSurface: "integral-smooth-guide-bead",
    gearTeethContactAllowed: false,
    continuousKeeperRailInProposedDesign: false,
    physicalValidation: "required-for-friction-wear-fit-and-noise",
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
  const comparison = input.comparison === "current" ? "current" : "proposed";
  const arrangement = ["assembled", "cutaway", "exploded"].includes(input.arrangement) ? input.arrangement : "assembled";
  const selectedHand = [...HAND_ORDER, "all"].includes(input.selectedHand) ? input.selectedHand : "all";
  const adjustment = THREE.MathUtils.clamp(Number(input.adjustmentMm) || 0, ...GUIDANCE_MM.adjustableTowerRange);
  const rotationDegrees = ((Number(input.rotationDegrees) || 0) % 360 + 360) % 360;
  const assemblyStep = THREE.MathUtils.clamp(Math.round(Number(input.assemblyStep) || 0), 0, 4);
  return {
    comparison,
    arrangement,
    selectedHand,
    adjustmentMm: adjustment,
    rotationDegrees,
    showLabels: input.showLabels !== false,
    showForces: input.showForces !== false,
    assemblyStep,
  };
}

export function comparisonVisibility(comparison) {
  const normalized = normalizeState({ comparison });
  return { proposedRollers: normalized.comparison === "proposed", currentKeepers: normalized.comparison === "current" };
}

export function assemblyVisibility(step) {
  const value = normalizeState({ assemblyStep: step }).assemblyStep;
  return {
    rings: true,
    fixedTowerFrames: value >= 1,
    adjustableTowerFrame: value >= 2,
    rollersOrKeepers: value >= 3,
    guidanceAnnotations: value >= 4,
  };
}

function createAnnulus(innerRadius, outerRadius, depth, material, segments = 128) {
  const shape = new THREE.Shape();
  shape.absarc(0, 0, outerRadius, 0, Math.PI * 2, false);
  const hole = new THREE.Path();
  hole.absarc(0, 0, innerRadius, 0, Math.PI * 2, true);
  shape.holes.push(hole);
  const geometry = new THREE.ExtrudeGeometry(shape, { depth, bevelEnabled: false, curveSegments: segments });
  geometry.translate(0, 0, -depth / 2);
  return new THREE.Mesh(geometry, material);
}

function makeMaterial(color, options = {}) {
  return new THREE.MeshStandardMaterial({ color, roughness: options.roughness ?? 0.58, metalness: options.metalness ?? 0.02, side: THREE.DoubleSide, transparent: true, opacity: 1 });
}

function handBandCenter(hand) {
  const band = CARRIER_BANDS_MM[hand];
  return (band[0] + band[1]) / 2;
}

function createRing(hand, index) {
  const group = new THREE.Group();
  group.name = `${hand}-carrier-with-integral-guide-bead`;
  group.userData.hand = hand;
  group.userData.baseZ = handBandCenter(hand);
  const color = HAND_COLORS[hand];
  const ringMaterial = makeMaterial(color);
  const ring = createAnnulus(RING_INNER_RADIUS, RING_OUTER_RADIUS, 3, ringMaterial);
  ring.name = `${hand}-carrier-band-${CARRIER_BANDS_MM[hand][0]}-to-${CARRIER_BANDS_MM[hand][1]}mm`;
  ring.castShadow = true;
  ring.receiveShadow = true;
  group.add(ring);

  const beadMaterial = makeMaterial(0xf5dd9a, { roughness: 0.36 });
  const bead = new THREE.Mesh(new THREE.TorusGeometry(GUIDE_BEAD_CENTER_RADIUS, GUIDANCE_MM.guideBead / 2, 12, 160), beadMaterial);
  bead.name = `${hand}-integral-smooth-guide-bead-0p8mm`;
  bead.castShadow = true;
  group.add(bead);

  const teeth = new THREE.Group();
  teeth.name = `${hand}-internal-gear-teeth-never-roller-contact`;
  const toothMaterial = makeMaterial(0x342c25, { roughness: 0.72 });
  const toothCount = 52 + index * 4;
  for (let toothIndex = 0; toothIndex < toothCount; toothIndex += 1) {
    const angle = toothIndex / toothCount * Math.PI * 2;
    const tooth = new THREE.Mesh(new THREE.BoxGeometry(2.7, 1.45, 2.55), toothMaterial);
    tooth.name = `${hand}-internal-gear-tooth-${String(toothIndex + 1).padStart(2, "0")}`;
    tooth.position.set(Math.cos(angle) * 52.7, Math.sin(angle) * 52.7, 0);
    tooth.rotation.z = angle;
    tooth.castShadow = true;
    tooth.userData.angle = angle;
    teeth.add(tooth);
  }
  group.add(teeth);

  const finMaterial = makeMaterial(index === 2 ? 0x255b62 : color, { roughness: 0.52 });
  const lengths = [26, 34, 42];
  const widths = [5.2, 3.8, 2.4];
  const fin = new THREE.Mesh(new THREE.BoxGeometry(widths[index], lengths[index], 2.15), finMaterial);
  fin.name = `${hand}-outer-upright-shadow-fin`;
  fin.position.y = RING_OUTER_RADIUS + lengths[index] / 2 - 2;
  fin.castShadow = true;
  group.add(fin);

  group.position.z = group.userData.baseZ;
  group.userData.materials = [ringMaterial, beadMaterial, toothMaterial, finMaterial];
  group.userData.teeth = teeth;
  return group;
}

function createSpoolGeometry() {
  const profile = [
    [-1.75, 4.8], [-1.25, 4.8], [-1.0, ROLLER_RUNNING_RADIUS], [-0.72, 3.35],
    [0.72, 3.35], [1.0, ROLLER_RUNNING_RADIUS], [1.25, 4.8], [1.75, 4.8],
  ].map(([y, radius]) => new THREE.Vector2(radius, y));
  const geometry = new THREE.LatheGeometry(profile, 48);
  geometry.rotateX(Math.PI / 2);
  geometry.computeVertexNormals();
  return geometry;
}

function polarPosition(radius, degrees, z = 0) {
  const angle = THREE.MathUtils.degToRad(degrees);
  return new THREE.Vector3(Math.cos(angle) * radius, Math.sin(angle) * radius, z);
}

function createTower(angleDegrees, towerIndex) {
  const tower = new THREE.Group();
  const adjustable = angleDegrees === GUIDANCE_MM.adjustableTowerAngle;
  tower.name = adjustable ? `tower-${towerIndex + 1}-adjustable-300deg` : `tower-${towerIndex + 1}-fixed-${angleDegrees}deg`;
  tower.userData.angleDegrees = angleDegrees;
  tower.userData.adjustable = adjustable;

  const frame = new THREE.Group();
  frame.name = `${tower.name}-compact-frame`;
  const frameMaterial = makeMaterial(adjustable ? 0xe9633d : 0x36322d, { roughness: 0.74 });
  const post = new THREE.Mesh(new THREE.CylinderGeometry(2.4, 2.8, 22, 24), frameMaterial);
  post.geometry.rotateX(Math.PI / 2);
  post.name = `${tower.name}-single-polished-pin-envelope`;
  post.position.z = 5.55;
  post.castShadow = true;
  frame.add(post);
  const foot = new THREE.Mesh(new THREE.BoxGeometry(10, 7, 2.2), frameMaterial);
  foot.name = `${tower.name}-compact-mount-foot`;
  foot.position.z = -5.1;
  frame.add(foot);

  const rollers = new THREE.Group();
  rollers.name = `${tower.name}-three-independent-rollers`;
  const rollerGeometry = createSpoolGeometry();
  HAND_ORDER.forEach((hand) => {
    const material = makeMaterial(HAND_COLORS[hand], { roughness: 0.34 });
    const roller = new THREE.Mesh(rollerGeometry, material);
    roller.name = `tower-${towerIndex + 1}-${hand}-independent-deep-grooved-roller`;
    roller.position.z = handBandCenter(hand);
    roller.castShadow = true;
    roller.userData.hand = hand;
    roller.userData.material = material;
    rollers.add(roller);
  });
  tower.add(frame, rollers);
  tower.userData.frame = frame;
  tower.userData.rollers = rollers;
  tower.userData.baseRadius = ROLLER_AXIS_RADIUS;
  tower.userData.material = frameMaterial;
  tower.position.copy(polarPosition(ROLLER_AXIS_RADIUS, angleDegrees));
  return tower;
}

function createKeeperSystem() {
  const group = new THREE.Group();
  group.name = "current-bulky-continuous-keeper-rails-shoes-caps-spines";
  const material = makeMaterial(0x666057, { roughness: 0.82 });
  HAND_ORDER.forEach((hand, index) => {
    const rail = new THREE.Mesh(new THREE.TorusGeometry(74.7, 2.35, 12, 96, Math.PI * 1.55), material);
    rail.name = `${hand}-continuous-under-stack-keeper-rail`;
    rail.position.z = handBandCenter(hand) - 2.6;
    rail.rotation.z = THREE.MathUtils.degToRad(39 + index * 4);
    group.add(rail);
    [60, 180, 300].forEach((angle, keeperIndex) => {
      const shoe = new THREE.Mesh(new THREE.BoxGeometry(12, 8, 5.5), material);
      shoe.name = `${hand}-keeper-shoe-${keeperIndex + 1}`;
      shoe.position.copy(polarPosition(75.5, angle, handBandCenter(hand)));
      shoe.rotation.z = THREE.MathUtils.degToRad(angle);
      group.add(shoe);
    });
  });
  const spine = new THREE.Mesh(new THREE.BoxGeometry(8, 40, 22), material);
  spine.name = "current-bulky-keeper-spine-and-cap";
  spine.position.set(-78, 0, 5.5);
  group.add(spine);
  group.userData.material = material;
  return group;
}

function createLabel(text, color = "#2b2924") {
  const canvas = document.createElement("canvas");
  canvas.width = 384;
  canvas.height = 80;
  const context = canvas.getContext("2d");
  context.clearRect(0, 0, canvas.width, canvas.height);
  context.fillStyle = "rgba(250,247,239,.94)";
  context.beginPath();
  context.roundRect(2, 2, 380, 76, 18);
  context.fill();
  context.fillStyle = color;
  context.font = "600 27px system-ui, sans-serif";
  context.textAlign = "center";
  context.textBaseline = "middle";
  context.fillText(text, 192, 41);
  const texture = new THREE.CanvasTexture(canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  const sprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: texture, transparent: true, depthTest: false }));
  sprite.scale.set(42, 8.75, 1);
  sprite.userData.texture = texture;
  return sprite;
}

function createAnnotations(towers) {
  const labels = new THREE.Group();
  labels.name = "guidance-dimension-labels";
  HAND_ORDER.forEach((hand, index) => {
    const label = createLabel(`${hand.toUpperCase()}  ${CARRIER_BANDS_MM[hand][0].toFixed(2)} → ${CARRIER_BANDS_MM[hand][1].toFixed(2)} mm`);
    label.name = `${hand}-carrier-band-label`;
    label.position.set(-38, 88, handBandCenter(hand) + index * 2.5);
    labels.add(label);
  });
  towers.forEach((tower, index) => {
    const label = createLabel(index === 2 ? "T3 · ADJUST ±0.25" : `T${index + 1} · FIXED`, index === 2 ? "#c34b2d" : "#2b2924");
    label.name = `tower-${index + 1}-label`;
    label.position.copy(polarPosition(95, tower.userData.angleDegrees, 18 + index * 1.6));
    labels.add(label);
  });
  const forces = new THREE.Group();
  forces.name = "roller-preload-force-arrows";
  towers.forEach((tower, index) => {
    const angle = THREE.MathUtils.degToRad(tower.userData.angleDegrees);
    const direction = new THREE.Vector3(-Math.cos(angle), -Math.sin(angle), 0).normalize();
    const origin = polarPosition(95, tower.userData.angleDegrees, handBandCenter("minute"));
    const arrow = new THREE.ArrowHelper(direction, origin, 17, index === 2 ? 0xe9633d : 0x9dad43, 4.5, 2.8);
    arrow.name = `tower-${index + 1}-radial-capture-force-arrow`;
    forces.add(arrow);
  });
  return { labels, forces };
}

function setMaterialsOpacity(materials, opacity) {
  materials.forEach((material) => {
    material.opacity = opacity;
    material.depthWrite = opacity >= 0.99;
  });
}

function disposeTree(root) {
  root.traverse((object) => {
    object.geometry?.dispose?.();
    const materials = Array.isArray(object.material) ? object.material : [object.material];
    materials.filter(Boolean).forEach((material) => {
      material.map?.dispose?.();
      material.dispose?.();
    });
    object.userData?.texture?.dispose?.();
  });
}

export function mount(options = {}) {
  const canvas = options.canvas;
  const parent = options.parent || canvas?.parentElement;
  if (!canvas || !parent) throw new Error("Free-spinner ADR requires a canvas and bounded parent");

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false, powerPreference: "high-performance" });
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.03;
  renderer.setClearColor(0xd9d1c2, 1);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0xd9d1c2);
  scene.fog = new THREE.Fog(0xd9d1c2, 250, 560);
  const camera = new THREE.PerspectiveCamera(34, 1, 0.1, 1000);
  const controls = new OrbitControls(camera, canvas);
  controls.enableDamping = true;
  controls.dampingFactor = 0.075;
  controls.minDistance = 92;
  controls.maxDistance = 430;
  controls.enablePan = false;

  const assembly = new THREE.Group();
  assembly.name = "free-spinner-ring-guidance-adr-assembly";
  scene.add(assembly);
  const rings = HAND_ORDER.map(createRing);
  const proposed = new THREE.Group();
  proposed.name = "proposed-three-free-spinner-towers-no-continuous-keeper";
  const towers = TOWER_ANGLES_DEGREES.map(createTower);
  towers.forEach((tower) => proposed.add(tower));
  const currentKeepers = createKeeperSystem();
  const annotations = createAnnotations(towers);
  assembly.add(...rings, proposed, currentKeepers, annotations.labels, annotations.forces);

  const plinth = new THREE.Mesh(new THREE.CylinderGeometry(102, 106, 7, 96), makeMaterial(0x9f7654, { roughness: 0.82 }));
  plinth.geometry.rotateX(Math.PI / 2);
  plinth.position.z = -10;
  plinth.name = "decorative-reference-plinth-not-guidance";
  plinth.receiveShadow = true;
  assembly.add(plinth);

  const floor = new THREE.Mesh(new THREE.PlaneGeometry(620, 620), new THREE.MeshStandardMaterial({ color: 0xe8e2d7, roughness: 1, side: THREE.DoubleSide }));
  floor.position.set(0, 0, -14);
  floor.receiveShadow = true;
  scene.add(floor);
  scene.add(new THREE.HemisphereLight(0xfff8e8, 0x655c50, 2.2));
  const key = new THREE.DirectionalLight(0xffe0ad, 5.5);
  key.position.set(-95, -120, 210);
  key.castShadow = true;
  key.shadow.mapSize.set(1024, 1024);
  scene.add(key);
  const rim = new THREE.DirectionalLight(0xbce5db, 3.2);
  rim.position.set(160, 55, 105);
  scene.add(rim);

  let state = normalizeState(options.initialState);
  let destroyed = false;
  let frameRequested = false;

  function requestRender() {
    if (destroyed || frameRequested) return;
    frameRequested = true;
    requestAnimationFrame(() => {
      frameRequested = false;
      controls.update();
      renderer.render(scene, camera);
    });
  }

  function setCameraPreset(arrangement, immediate = false) {
    const preset = CAMERA_PRESETS[arrangement] || CAMERA_PRESETS.assembled;
    camera.position.fromArray(preset.position);
    controls.target.fromArray(preset.target);
    controls.update();
    if (immediate) renderer.render(scene, camera);
    else requestRender();
  }

  function applyState(nextState) {
    state = normalizeState({ ...state, ...nextState });
    const visibility = comparisonVisibility(state.comparison);
    const step = assemblyVisibility(state.assemblyStep);
    proposed.visible = visibility.proposedRollers;
    currentKeepers.visible = visibility.currentKeepers && step.rollersOrKeepers;

    const explodeOffsets = state.arrangement === "exploded" ? [-9, 0, 9] : [0, 0, 0];
    rings.forEach((ring, index) => {
      const hand = HAND_ORDER[index];
      ring.position.z = ring.userData.baseZ + explodeOffsets[index];
      ring.rotation.z = THREE.MathUtils.degToRad(state.rotationDegrees * [1, 0.62, 1.37][index]);
      const selected = state.selectedHand === "all" || state.selectedHand === hand;
      setMaterialsOpacity(ring.userData.materials, selected ? (state.arrangement === "cutaway" ? 0.76 : 1) : 0.16);
      ring.userData.teeth.children.forEach((tooth) => {
        const frontCut = Math.cos(tooth.userData.angle) > 0.28;
        tooth.visible = !(state.arrangement === "cutaway" && frontCut);
      });
      ring.visible = step.rings;
    });

    towers.forEach((tower, towerIndex) => {
      const radius = tower.userData.baseRadius + (tower.userData.adjustable ? state.adjustmentMm : 0);
      tower.position.copy(polarPosition(radius, tower.userData.angleDegrees));
      tower.userData.frame.visible = tower.userData.adjustable ? step.adjustableTowerFrame : step.fixedTowerFrames;
      tower.userData.rollers.visible = step.rollersOrKeepers;
      tower.userData.rollers.children.forEach((roller, handIndex) => {
        const hand = HAND_ORDER[handIndex];
        roller.position.z = handBandCenter(hand) + explodeOffsets[handIndex];
        roller.rotation.z = THREE.MathUtils.degToRad(-state.rotationDegrees * [1, 0.62, 1.37][handIndex]);
        roller.material.opacity = state.selectedHand === "all" || state.selectedHand === hand ? 1 : 0.16;
        roller.material.depthWrite = roller.material.opacity >= 0.99;
      });
      tower.userData.material.opacity = tower.userData.adjustable ? 1 : 0.82;
    });

    currentKeepers.children.forEach((part) => {
      const handIndex = HAND_ORDER.findIndex((hand) => part.name.startsWith(hand));
      if (handIndex >= 0 && part.name.includes("keeper")) part.position.z += explodeOffsets[handIndex] - (part.userData.lastExplodeOffset || 0);
      if (handIndex >= 0) part.userData.lastExplodeOffset = explodeOffsets[handIndex];
    });
    annotations.labels.visible = state.showLabels && step.guidanceAnnotations;
    annotations.forces.visible = state.showForces && step.guidanceAnnotations && visibility.proposedRollers;
    options.onStateChange?.(state, geometryContract());
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
    getState: () => ({ ...state }),
    setState: applyState,
    setCameraPreset,
    resize,
    dispose() {
      destroyed = true;
      resizeObserver.disconnect();
      controls.removeEventListener("change", requestRender);
      controls.dispose();
      disposeTree(scene);
      renderer.dispose();
    },
  };
}

export { CAMERA_PRESETS };
