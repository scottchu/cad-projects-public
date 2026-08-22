import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { allRodPoses, CAM, camProgressFromAngle, camSlotSamples, RODS, sharedCamAngleRadians, WIRE } from "./cam-contract.js";

const MAX_BUFFER_PIXELS = 2_073_600;
const SIDE_X = CAM.sidePlateOuterSpan / 2;
export const RENDER_GEOMETRY = Object.freeze({
  escPadCenterY: -5.55,
  escPadHeight: 0.7,
  escPadSurfaceY: -5.2,
  wireCenterY: -3.05,
  mechanismYOffset: -3.05,
  leadLength: 44,
});

export const CAMERA_PRESETS = Object.freeze({
  iso: Object.freeze({ position: [102, 67, 92], target: [0, 1, 15] }),
  side: Object.freeze({ position: [122, 3, 15], target: [0, 1, 15] }),
  top: Object.freeze({ position: [0.01, 132, 13], target: [0, -1, 13] }),
});

export function boundedBufferSize(cssWidth, cssHeight, devicePixelRatio = 1) {
  const width = Math.max(1, Math.round(Number(cssWidth) || 0));
  const height = Math.max(1, Math.round(Number(cssHeight) || 0));
  let dpr = Math.min(1.6, Math.max(1, Number(devicePixelRatio) || 1));
  if (width * height * dpr * dpr > MAX_BUFFER_PIXELS) dpr *= Math.sqrt(MAX_BUFFER_PIXELS / (width * height * dpr * dpr));
  return { width, height, dpr, bufferPixels: Math.floor(width * dpr) * Math.floor(height * dpr) };
}

function roundedBox(width, height, depth, radius, material) {
  const mesh = new THREE.Mesh(new RoundedBoxGeometry(width, height, depth, 4, radius), material);
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  return mesh;
}

function cylinderAlongX(radius, length, material, segments = 36) {
  const mesh = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, length, segments), material);
  mesh.rotation.z = Math.PI / 2;
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  return mesh;
}

function tubeFromPoints(points, radius, material, segments = 48) {
  const path = new THREE.CurvePath();
  for (let index = 1; index < points.length; index += 1) path.add(new THREE.LineCurve3(points[index - 1], points[index]));
  const mesh = new THREE.Mesh(new THREE.TubeGeometry(path, Math.max(1, segments), radius, 10, false), material);
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  return mesh;
}

function makeGuide(side, rod, materials) {
  const group = new THREE.Group();
  group.name = `${side < 0 ? "left" : "right"}-straight-guide-${rod.id}`;
  const x = side * (SIDE_X + 2.7);
  const start = new THREE.Vector3(x, rod.open.y + RENDER_GEOMETRY.mechanismYOffset, rod.open.z);
  const end = new THREE.Vector3(x, rod.closed.y + RENDER_GEOMETRY.mechanismYOffset, rod.closed.z);
  const rail = tubeFromPoints([start, end], 3.1, materials.guide, 12);
  rail.name = `${group.name}-body`;
  const channel = tubeFromPoints([start, end], 1.8, materials.guideChannel, 12);
  channel.name = `${group.name}-channel`;
  group.add(rail, channel);
  return group;
}

function makeCamPlate(side, materials) {
  const sideName = side < 0 ? "left" : "right";
  const group = new THREE.Group();
  group.name = `${sideName}-rotating-three-slot-cam-plate`;
  group.position.set(side * SIDE_X, CAM.center.y + RENDER_GEOMETRY.mechanismYOffset, CAM.center.z);

  const disk = cylinderAlongX(CAM.camPlateDiameter / 2, 2.8, materials.cam, 72);
  disk.name = `${sideName}-cam-plate-body`;
  group.add(disk);

  const faceX = side * 1.55;
  for (const rod of RODS) {
    const points = camSlotSamples(rod.id, 121).map(sample => new THREE.Vector3(faceX, sample.y, sample.z));
    const groove = tubeFromPoints(points, CAM.grooveWidth / 2, materials.groove, 120);
    groove.name = `${sideName}-curved-cam-slot-${rod.id}`;
    const centerline = tubeFromPoints(points, 0.34, materials.slotCenter, 120);
    centerline.name = `${sideName}-cam-slot-centerline-${rod.id}`;
    group.add(groove, centerline);
  }

  const hub = cylinderAlongX(CAM.shaftDiameter / 2 + 1.7, 4.2, materials.hub, 40);
  hub.name = `${sideName}-keyed-shaft-hub`;
  group.add(hub);
  return group;
}

export function wirePathPoints(angleRadians, x = 0) {
  const horizontalRun = 16;
  const arcLength = WIRE.bendRadius * angleRadians;
  const tail = Math.max(0, RENDER_GEOMETRY.leadLength - horizontalRun - arcLength);
  const baseY = RENDER_GEOMETRY.wireCenterY;
  const points = [new THREE.Vector3(x, baseY, 0), new THREE.Vector3(x, baseY, horizontalRun)];
  const samples = 18;
  for (let index = 1; index <= samples; index += 1) {
    const q = angleRadians * index / samples;
    const phi = -Math.PI / 2 + q;
    points.push(new THREE.Vector3(x, baseY + WIRE.bendCenter.y + WIRE.bendRadius * Math.sin(phi), WIRE.bendCenter.z + WIRE.bendRadius * Math.cos(phi)));
  }
  const end = points.at(-1);
  points.push(new THREE.Vector3(x, end.y + tail * Math.sin(angleRadians), end.z + tail * Math.cos(angleRadians)));
  return points;
}

function makeBoard(width, depth, material, name) {
  const group = new THREE.Group();
  group.name = name;
  const board = roundedBox(width, 2.2, depth, 1.3, material);
  group.add(board);
  return group;
}

function makeXt60(materials) {
  const group = new THREE.Group();
  group.name = "xt60-connector-following-bent-leads";
  const body = roundedBox(16, 10, 11, 2, materials.xt60);
  body.name = "xt60-yellow-body";
  group.add(body);
  for (const x of [-4.2, 4.2]) {
    const socket = cylinderAlongX(1.8, 0.8, materials.socket, 24);
    socket.position.set(x, 0, -5.55);
    group.add(socket);
  }
  return group;
}

export function mount({ canvas, onReady } = {}) {
  if (!canvas?.parentElement) throw new Error("A bounded canvas is required");
  const reducedMotion = globalThis.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches ?? false;
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false, powerPreference: "high-performance" });
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.08;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.setClearColor(0xd5d2c8, 1);

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0xd5d2c8);
  scene.fog = new THREE.Fog(0xd5d2c8, 125, 210);
  const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 400);
  const controls = new OrbitControls(camera, canvas);
  controls.enableDamping = !reducedMotion;
  controls.dampingFactor = 0.075;
  controls.enablePan = false;
  controls.minDistance = 52;
  controls.maxDistance = 175;
  controls.maxPolarAngle = Math.PI * 0.51;

  const materials = {
    steel: new THREE.MeshStandardMaterial({ color: 0xbcc8c8, roughness: 0.2, metalness: 0.9 }),
    cam: new THREE.MeshPhysicalMaterial({ color: 0x2e7650, roughness: 0.5, metalness: 0.04, transparent: true, opacity: 0.26, depthWrite: false, side: THREE.DoubleSide }),
    groove: new THREE.MeshStandardMaterial({ color: 0x101713, roughness: 0.82 }),
    slotCenter: new THREE.MeshBasicMaterial({ color: 0xffcb3d }),
    guide: new THREE.MeshStandardMaterial({ color: 0x244031, roughness: 0.62 }),
    guideChannel: new THREE.MeshStandardMaterial({ color: 0x75877b, roughness: 0.55 }),
    hub: new THREE.MeshStandardMaterial({ color: 0x17231c, roughness: 0.42, metalness: 0.35 }),
    follower: new THREE.MeshStandardMaterial({ color: 0xebb52c, roughness: 0.38, metalness: 0.2 }),
    shaft: new THREE.MeshStandardMaterial({ color: 0x555f5d, roughness: 0.24, metalness: 0.8 }),
    dial: new THREE.MeshStandardMaterial({ color: 0x151a16, roughness: 0.5 }),
    lock: new THREE.MeshStandardMaterial({ color: 0xf1bd2c, roughness: 0.38 }),
    esc: new THREE.MeshStandardMaterial({ color: 0x202421, roughness: 0.76 }),
    fc: new THREE.MeshStandardMaterial({ color: 0x353a36, roughness: 0.68 }),
    pad: new THREE.MeshStandardMaterial({ color: 0xd6a636, roughness: 0.3, metalness: 0.72 }),
    red: new THREE.MeshStandardMaterial({ color: 0xd83e36, roughness: 0.6 }),
    black: new THREE.MeshStandardMaterial({ color: 0x171918, roughness: 0.68 }),
    xt60: new THREE.MeshStandardMaterial({ color: 0xe7a91f, roughness: 0.52 }),
    socket: new THREE.MeshStandardMaterial({ color: 0x343934, roughness: 0.38, metalness: 0.55 }),
    carbon: new THREE.MeshStandardMaterial({ color: 0x171a18, roughness: 0.7, metalness: 0.18 }),
  };

  const mechanism = new THREE.Group();
  mechanism.name = "three-rods-two-mirrored-cams-one-shared-shaft";
  scene.add(mechanism);

  const camPlates = [-1, 1].map(side => makeCamPlate(side, materials));
  mechanism.add(...camPlates);
  for (const side of [-1, 1]) for (const rod of RODS) mechanism.add(makeGuide(side, rod, materials));

  const shaft = cylinderAlongX(CAM.shaftDiameter / 2, 68, materials.shaft, 40);
  shaft.name = "single-shared-keyed-cam-shaft";
  const shaftWorldY = CAM.center.y + RENDER_GEOMETRY.mechanismYOffset;
  shaft.position.set(0, shaftWorldY, CAM.center.z);
  mechanism.add(shaft);

  const dial = new THREE.Group();
  dial.name = "single-left-hand-dial";
  dial.position.set(-36, shaftWorldY, CAM.center.z);
  const dialBody = cylinderAlongX(8.2, 6, materials.dial, 40);
  dial.add(dialBody);
  const dialMarker = roundedBox(6.2, 2.2, 2.2, .5, materials.lock);
  dialMarker.position.set(-3.3, 6.3, 0);
  dial.add(dialMarker);
  mechanism.add(dial);

  const brake = new THREE.Group();
  brake.name = "stationary-split-shaft-brake-grounded-to-left-frame";
  brake.position.set(-30.5, shaftWorldY, CAM.center.z);
  const brakeAnchor = roundedBox(11, 4, 5, .8, materials.guide);
  brakeAnchor.name = "fixed-brake-anchor-to-side-mechanism";
  brakeAnchor.position.x = 5.2;
  brake.add(brakeAnchor);
  for (const rotation of [0, Math.PI]) {
    const geometry = new THREE.TorusGeometry(4.3, 1.25, 12, 32, Math.PI * .86);
    geometry.rotateY(Math.PI / 2);
    geometry.rotateX(rotation);
    const half = new THREE.Mesh(geometry, materials.guide);
    half.name = "fixed-split-brake-half";
    brake.add(half);
  }
  const brakeShoe = roundedBox(4.4, 2.4, 6.2, .7, materials.lock);
  brakeShoe.name = "shaft-brake-shoe-closes-without-rotating";
  brakeShoe.position.y = 6.2;
  brake.add(brakeShoe);
  mechanism.add(brake);

  const rodMeshes = new Map();
  const followerMeshes = new Map();
  for (const rod of RODS) {
    const mesh = cylinderAlongX(CAM.rodDiameter / 2, CAM.rodLength, materials.steel, 44);
    mesh.name = `moving-purchased-rod-${rod.id}-diameter4-length50`;
    mechanism.add(mesh);
    rodMeshes.set(rod.id, mesh);
    const followers = [-1, 1].map(side => {
      const follower = new THREE.Mesh(new THREE.SphereGeometry(2.55, 24, 16), materials.follower);
      follower.name = `${side < 0 ? "left" : "right"}-cam-follower-${rod.id}`;
      follower.position.x = side * 25.1;
      mechanism.add(follower);
      return follower;
    });
    followerMeshes.set(rod.id, followers);
  }

  const fpv = new THREE.Group();
  fpv.name = "fpv-frame-with-bottom-esc-power-stack";
  scene.add(fpv);
  const armA = roundedBox(80, 2.6, 10, 2, materials.carbon); armA.rotation.y = Math.PI / 4; armA.position.set(0, -13, -12);
  const armB = roundedBox(80, 2.6, 10, 2, materials.carbon); armB.rotation.y = -Math.PI / 4; armB.position.set(0, -13, -12);
  fpv.add(armA, armB);
  const esc = makeBoard(36, 30, materials.esc, "bottom-esc-board-with-power-pads"); esc.position.set(0, -7, -15); fpv.add(esc);
  const fc = makeBoard(32, 27, materials.fc, "flight-controller-above-esc"); fc.position.set(0, -1, -15); fpv.add(fc);
  for (const x of [-14, 14]) for (const z of [-25, -5]) {
    const post = new THREE.Mesh(new THREE.CylinderGeometry(1.8, 1.8, 6, 20), materials.follower);
    post.position.set(x, -4, z);
    fpv.add(post);
  }
  for (const x of [-4.2, 4.2]) { const pad = roundedBox(6.2, RENDER_GEOMETRY.escPadHeight, 5, .6, materials.pad); pad.name = `bottom-esc-${x < 0 ? "negative" : "positive"}-solder-pad`; pad.position.set(x, RENDER_GEOMETRY.escPadCenterY, -1.8); fpv.add(pad); }

  const wireMeshes = [
    { x: -4.2, material: materials.black, name: "black-horizontal-to-vertical-lead", mesh: null },
    { x: 4.2, material: materials.red, name: "red-horizontal-to-vertical-lead", mesh: null },
  ];
  const xt60 = makeXt60(materials);
  scene.add(xt60);

  const ground = new THREE.Mesh(new THREE.PlaneGeometry(250, 220), new THREE.MeshStandardMaterial({ color: 0xc4c1b8, roughness: 1 }));
  ground.rotation.x = -Math.PI / 2; ground.position.y = -15; ground.receiveShadow = true; scene.add(ground);
  const grid = new THREE.GridHelper(190, 19, 0x8c918b, 0xa5a59d); grid.position.y = -14.9; grid.material.opacity = .2; grid.material.transparent = true; scene.add(grid);
  scene.add(new THREE.HemisphereLight(0xfffae9, 0x536057, 2.45));
  const key = new THREE.DirectionalLight(0xffedd0, 4.1); key.position.set(-65, 92, 72); key.castShadow = true; key.shadow.mapSize.set(1536, 1536); scene.add(key);
  const rim = new THREE.DirectionalLight(0xb9e0ce, 1.7); rim.position.set(70, 35, -55); scene.add(rim);

  let disposed = false;
  let resizeKey = "";
  let cameraTween = null;

  function setCamera(name = "iso", instant = false) {
    const preset = CAMERA_PRESETS[name] || CAMERA_PRESETS.iso;
    const targetPosition = new THREE.Vector3(...preset.position);
    const targetLook = new THREE.Vector3(...preset.target);
    if (instant || reducedMotion) { camera.position.copy(targetPosition); controls.target.copy(targetLook); controls.update(); cameraTween = null; return; }
    cameraTween = { fromPosition: camera.position.clone(), fromTarget: controls.target.clone(), targetPosition, targetLook, start: performance.now(), duration: 420 };
  }

  function update(state = {}) {
    const angle = Number(state.angle) || 0;
    const angleRadians = sharedCamAngleRadians(angle);
    const progress = camProgressFromAngle(angle);
    camPlates.forEach(plate => { plate.rotation.x = -angleRadians; });
    dial.rotation.x = -angleRadians;
    brakeShoe.position.y = state.locked ? 3.6 : 6.2;

    for (const pose of allRodPoses(angle)) {
      const worldY = pose.y + RENDER_GEOMETRY.mechanismYOffset;
      const mesh = rodMeshes.get(pose.id); mesh.position.set(0, worldY, pose.z);
      followerMeshes.get(pose.id).forEach(follower => { follower.position.y = worldY; follower.position.z = pose.z; });
    }

    const bendAngle = progress * Math.PI / 2;
    for (const wire of wireMeshes) {
      const points = wirePathPoints(bendAngle, wire.x);
      const replacement = tubeFromPoints(points, WIRE.radius, wire.material, 80);
      replacement.name = wire.name;
      if (wire.mesh) { scene.remove(wire.mesh); wire.mesh.geometry.dispose(); }
      wire.mesh = replacement;
      scene.add(replacement);
    }
    const end = wirePathPoints(bendAngle, 0).at(-1);
    xt60.position.set(0, end.y + Math.sin(bendAngle) * 6, end.z + Math.cos(bendAngle) * 6);
    xt60.rotation.x = -bendAngle;
  }

  function resize() {
    const rect = canvas.parentElement.getBoundingClientRect();
    const next = boundedBufferSize(rect.width, rect.height, globalThis.devicePixelRatio || 1);
    const keyValue = `${next.width}:${next.height}:${next.dpr.toFixed(3)}`;
    if (keyValue === resizeKey) return;
    resizeKey = keyValue; renderer.setPixelRatio(next.dpr); renderer.setSize(next.width, next.height, false); camera.aspect = next.width / next.height; camera.updateProjectionMatrix();
  }

  function draw(time) {
    if (disposed) return;
    resize();
    if (cameraTween) { const raw = Math.min(1, (time - cameraTween.start) / cameraTween.duration); const t = raw * raw * (3 - 2 * raw); camera.position.lerpVectors(cameraTween.fromPosition, cameraTween.targetPosition, t); controls.target.lerpVectors(cameraTween.fromTarget, cameraTween.targetLook, t); if (raw >= 1) cameraTween = null; }
    controls.update(); renderer.render(scene, camera);
  }

  const resizeObserver = new ResizeObserver(resize); resizeObserver.observe(canvas.parentElement);
  setCamera("iso", true); update({ angle: 0, locked: false }); renderer.setAnimationLoop(draw); onReady?.();

  function dispose() {
    disposed = true; renderer.setAnimationLoop(null); resizeObserver.disconnect(); controls.dispose();
    scene.traverse(object => { object.geometry?.dispose?.(); if (Array.isArray(object.material)) object.material.forEach(material => material.dispose()); else object.material?.dispose?.(); });
    renderer.dispose();
  }
  return { update, setCamera, dispose };
}
