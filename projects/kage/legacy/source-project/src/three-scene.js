import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

const MAX_BUFFER_PIXELS = 2_073_600;
const CAMERA_DISTANCE_LIMITS = Object.freeze({ min: 65, max: 1600, far: 2500 });
const REFERENCE_Z = Object.freeze({ wall: 0, mask: 1.5, hour: 2.8, minute: 6.2, second: 9.6, source: 40, glareCap: 46 });
const ORDER = Object.freeze(["wall", "mask", "hour", "minute", "second", "source", "glareCap"]);
const CAMERA_PRESETS = Object.freeze({
  assembly: { label: "P3 V3 STACKED ASSEMBLY", position: [270, 205, 245], target: [0, 0, 7] },
  wall: { label: "WALL SHADOW", position: [0, 0, 650], target: [0, 0, 0] },
  section: { label: "SIDE SECTION", position: [360, 4, 74], target: [0, 0, 7] },
  orbital: { label: "STACKED FIN CLOSE-UP", position: [205, 145, 96], target: [0, 0, 9] },
});

function blockerRotation(clockAngleRadians) { return -clockAngleRadians; }
function blockerWorldTip(clockAngleRadians, tipRadius) { return { x: Math.sin(clockAngleRadians) * tipRadius, y: Math.cos(clockAngleRadians) * tipRadius }; }
function displayZ(baseZ, explodedOffset, exploded) { return Number(baseZ) + (exploded ? Number(explodedOffset) || 0 : 0); }
function fullAngleToHalfAngle(fullAngleDegrees) {
  const value = Number(fullAngleDegrees);
  const normalized = Number.isFinite(value) ? Math.max(140, Math.min(180, value)) : 180;
  return normalized / 2;
}

function boundedBufferSize(cssWidth, cssHeight, devicePixelRatio = 1) {
  const width = Math.max(1, Math.round(Number(cssWidth) || 0));
  const height = Math.max(1, Math.round(Number(cssHeight) || 0));
  let dpr = Math.min(1.5, Math.max(1, Number(devicePixelRatio) || 1));
  const requested = width * height * dpr * dpr;
  if (requested > MAX_BUFFER_PIXELS) dpr *= Math.sqrt(MAX_BUFFER_PIXELS / requested);
  const bufferWidth = Math.max(1, Math.floor(width * dpr));
  const bufferHeight = Math.max(1, Math.floor(height * dpr));
  return { cssWidth: width, cssHeight: height, dpr, bufferWidth, bufferHeight, bufferPixels: bufferWidth * bufferHeight };
}

function defaultFin(name) {
  const defaults = {
    hour: { radius: 138.1, carrierInnerRadius: 130.5, carrierOuterRadius: 135.5, carrierBaseZ: 2.8, carrierThickness: 3, baseZ: 2.8, shadowOcclusionTopZ: 5.8, tipZ: 17.904, projectedStart: 161.520467836, projectedTip: 250, stemWidth: 3, crownWidth: 3, crownHeight: 15.104, crownStyle: "flat", projectedBaseWidth: 3.50877193, projectedTipWidth: 5.434782609 },
    minute: { radius: 136.5, carrierInnerRadius: 130.5, carrierOuterRadius: 135.5, carrierBaseZ: 6.2, carrierThickness: 3, baseZ: 6.2, shadowOcclusionTopZ: 9.2, tipZ: 21.8, projectedStart: 177.272727273, projectedTip: 300, stemWidth: 2, crownWidth: 2, crownHeight: 15.6, crownStyle: "flat", projectedBaseWidth: 2.597402597, projectedTipWidth: 4.395604396 },
    second: { radius: 134.9, carrierInnerRadius: 130.5, carrierOuterRadius: 135.5, carrierBaseZ: 9.6, carrierThickness: 3, baseZ: 12.4, shadowOcclusionTopZ: 12.6, tipZ: 24.582857143, projectedStart: 196.934306569, projectedTip: 350, stemWidth: 1.2, crownWidth: 1.2, crownHeight: 12.182857143, crownStyle: "flat", projectedBaseWidth: 1.751824818, projectedTipWidth: 3.113417346 },
  };
  return defaults[name];
}

function sceneContract(snapshot = {}) {
  const model = snapshot.model || {};
  const fins = model.fins || {};
  const normalizeFin = name => ({ ...defaultFin(name), ...(fins[name] || {}) });
  const fieldFullAngle = Number.isFinite(Number(model.fieldFullAngle)) ? Math.max(140, Math.min(180, Number(model.fieldFullAngle))) : 180;
  return {
    architecture: model.architecture || "p3-v3-stacked-three-motor-90deg",
    axisConvention: "wall z=0; +Z points toward room/viewer",
    sourceZ: model.sourceZ ?? REFERENCE_Z.source,
    maskZ: model.maskZ ?? REFERENCE_Z.mask,
    maskPhysicalRadius: model.maskPhysicalRadius ?? 125.125,
    projectedMaskRadius: model.projectedMaskRadius ?? 130,
    fins: { hour: normalizeFin("hour"), minute: normalizeFin("minute"), second: normalizeFin("second") },
    finProfileScale: model.finProfileScale ?? 1,
    finTangentialWidth: model.finTangentialWidth ?? 1,
    finRadialThickness: model.finRadialThickness ?? 1.2,
    fieldFullAngle,
    fieldHalfAngle: fullAngleToHalfAngle(fieldFullAngle),
    shellRadius: model.shellRadius ?? 150,
    shellLipZ: model.shellLipZ ?? 0,
    glareCapDiameter: model.glareCapDiameter ?? 22,
  };
}

function createAnnulus(innerRadius, outerRadius, thickness, material, segments = 96) {
  const shape = new THREE.Shape();
  shape.absarc(0, 0, outerRadius, 0, Math.PI * 2, false);
  const hole = new THREE.Path();
  hole.absarc(0, 0, innerRadius, 0, Math.PI * 2, true);
  shape.holes.push(hole);
  const geometry = new THREE.ExtrudeGeometry(shape, { depth: thickness, bevelEnabled: false, curveSegments: segments });
  geometry.translate(0, 0, -thickness / 2);
  return new THREE.Mesh(geometry, material);
}

function createFinGeometry(profile, height, radialThickness) {
  const stem = Math.max(0.05, profile.stemWidth);
  const shape = new THREE.Shape();
  shape.moveTo(-stem / 2, 0);
  shape.lineTo(stem / 2, 0);
  shape.lineTo(stem / 2, height);
  shape.lineTo(-stem / 2, height);
  shape.closePath();
  const geometry = new THREE.ExtrudeGeometry(shape, { depth: radialThickness, bevelEnabled: false, curveSegments: 12 });
  geometry.rotateX(Math.PI / 2);
  geometry.translate(0, radialThickness / 2, 0);
  geometry.computeVertexNormals();
  return geometry;
}

function createShadowGeometry(startRadius, tipRadius, baseWidth, tipWidth) {
  const shape = new THREE.Shape();
  shape.moveTo(-baseWidth / 2, startRadius);
  shape.lineTo(baseWidth / 2, startRadius);
  shape.lineTo(tipWidth / 2, tipRadius);
  shape.lineTo(-tipWidth / 2, tipRadius);
  shape.closePath();
  const geometry = new THREE.ExtrudeGeometry(shape, { depth: .32, bevelEnabled: false });
  geometry.translate(0, 0, -.16);
  return geometry;
}

function makeLine(points, color = 0xf0a65d, opacity = 0.5) {
  const geometry = new THREE.BufferGeometry().setFromPoints(points);
  return new THREE.LineSegments(geometry, new THREE.LineBasicMaterial({ color, transparent: true, opacity }));
}

function createCarrier(name, color) {
  const group = new THREE.Group();
  group.name = `${name}-constant-radius-carrier`;
  const material = new THREE.MeshStandardMaterial({ color, roughness: 0.68, metalness: name === "minute" ? .22 : .03, side: THREE.DoubleSide });
  const ring = createAnnulus(.1, 1, 1.2, material);
  ring.name = `${name}-hidden-carrier-ring`;
  ring.castShadow = true;
  group.add(ring);
  const fin = new THREE.Mesh(createFinGeometry(defaultFin(name), 1, 1.6), material);
  fin.name = `${name}-constant-section-upright-fin`;
  fin.castShadow = true;
  group.add(fin);
  group.userData = { name, ring, fin, material, baseZ: 0, ringKey: "", finKey: "" };
  return group;
}

function createShadow(name, color) {
  const group = new THREE.Group();
  group.name = `${name}-projected-profile-shadow`;
  const material = new THREE.MeshBasicMaterial({ color, transparent: true, opacity: .48, depthWrite: false, side: THREE.DoubleSide });
  const mesh = new THREE.Mesh(createShadowGeometry(defaultFin(name).projectedStart, defaultFin(name).projectedTip, defaultFin(name).projectedBaseWidth, defaultFin(name).projectedTipWidth), material);
  mesh.name = `${name}-shadow-only-no-mechanics`;
  group.add(mesh);
  group.userData = { mesh, material, geometryKey: "" };
  return group;
}

function mount(options = {}) {
  const canvas = options.canvas;
  const parent = options.parent || canvas?.parentElement;
  if (!canvas || !parent) throw new Error("Kage Three.js requires a canvas and bounded parent");
  if (typeof WebGL2RenderingContext === "undefined") throw new Error("WebGL2 is unavailable");

  const reducedMotion = options.reducedMotion ?? globalThis.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches ?? false;
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false, powerPreference: "high-performance" });
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.1;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.setClearColor(0xd8d0c2, 1);

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0xd8d0c2);
  const camera = new THREE.PerspectiveCamera(36, 1, .5, CAMERA_DISTANCE_LIMITS.far);
  const controls = new OrbitControls(camera, canvas);
  controls.enableDamping = !reducedMotion;
  controls.dampingFactor = .075;
  controls.enablePan = false;
  controls.enableZoom = true;
  controls.zoomSpeed = 1.1;
  controls.minDistance = CAMERA_DISTANCE_LIMITS.min;
  controls.maxDistance = CAMERA_DISTANCE_LIMITS.max;

  const environmentGroup = new THREE.Group();
  const mechanicsGroup = new THREE.Group();
  const sourceGroup = new THREE.Group();
  const shellGroup = new THREE.Group();
  const helperGroup = new THREE.Group();
  const shadowGroup = new THREE.Group();
  environmentGroup.name = "limewash-room-context";
  mechanicsGroup.name = "hidden-orbital-mechanics";
  sourceGroup.name = "wallward-point-source-and-room-glare-cap";
  shellGroup.name = "engineering-shell-envelope";
  helperGroup.name = "optical-cone-rays";
  shadowGroup.name = "wall-shadow-only-presentation";
  scene.add(environmentGroup, shadowGroup, mechanicsGroup, sourceGroup, shellGroup, helperGroup);

  const wallMaterial = new THREE.MeshStandardMaterial({ color: 0xded8cd, roughness: .98, side: THREE.DoubleSide });
  const wall = new THREE.Mesh(new THREE.PlaneGeometry(760, 700), wallMaterial);
  wall.name = "limewash-wall-z-zero";
  wall.position.z = 0;
  wall.receiveShadow = true;
  environmentGroup.add(wall);
  const floorMaterial = new THREE.MeshStandardMaterial({ color: 0xcabda8, roughness: .98, side: THREE.DoubleSide });
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(760, 320), floorMaterial);
  floor.name = "restrained-floor-context";
  floor.rotation.x = -Math.PI / 2;
  floor.position.set(0, -190, 78);
  environmentGroup.add(floor);
  const ambient = new THREE.AmbientLight(0xfff8ec, 2.2);
  ambient.name = "non-shadow-casting-room-fill";
  ambient.castShadow = false;
  const hemisphere = new THREE.HemisphereLight(0xfff8e8, 0x6a5f52, 1.25);
  hemisphere.name = "non-shadow-casting-daylight-fill";
  hemisphere.castShadow = false;
  environmentGroup.add(ambient, hemisphere);

  const charcoal = new THREE.MeshStandardMaterial({ color: 0x262521, roughness: .88, metalness: .02 });

  const quartz = new THREE.Mesh(new THREE.BoxGeometry(56, 56.7, 16), new THREE.MeshStandardMaterial({ color: 0x38342f, roughness: .78 }));
  quartz.name = "quartz-envelope-hidden-behind-mask";
  quartz.position.z = -8;
  mechanicsGroup.add(quartz);
  const mask = new THREE.Mesh(new THREE.CylinderGeometry(1, 1, 1.4, 72), charcoal);
  mask.geometry.rotateX(Math.PI / 2);
  mask.name = "wall-side-physical-mask";
  mask.position.z = REFERENCE_Z.mask;
  mask.castShadow = true;
  mechanicsGroup.add(mask);
  const carriers = { hour: createCarrier("hour", 0xec6a3a), minute: createCarrier("minute", 0xb99355), second: createCarrier("second", 0x292722) };
  mechanicsGroup.add(carriers.hour, carriers.minute, carriers.second);

  const led = new THREE.Mesh(new THREE.SphereGeometry(2, 24, 14), new THREE.MeshBasicMaterial({ color: 0xffd29a }));
  led.name = "single-on-axis-wallward-led";
  led.position.z = REFERENCE_Z.source;
  sourceGroup.add(led);
  const spot = new THREE.SpotLight(0xffc886, 5200, 0, THREE.MathUtils.degToRad(75), .2, 1.1);
  spot.name = "only-shadow-casting-light-wide-angle-wallward-point-source";
  spot.position.z = REFERENCE_Z.source;
  spot.target.position.set(0, 0, 0);
  spot.castShadow = true;
  spot.shadow.mapSize.set(1024, 1024);
  spot.shadow.camera.near = .5;
  spot.shadow.camera.far = 70;
  spot.shadow.bias = -.00015;
  spot.shadow.normalBias = .01;
  sourceGroup.add(spot, spot.target);
  const glareCap = new THREE.Mesh(new THREE.CylinderGeometry(1, 1, 3.2, 64), charcoal);
  glareCap.geometry.rotateX(Math.PI / 2);
  glareCap.name = "room-side-glare-cap-not-wall-mask";
  glareCap.position.z = REFERENCE_Z.glareCap;
  sourceGroup.add(glareCap);

  const shell = new THREE.Mesh(new THREE.CylinderGeometry(1, 1, 1, 72, 1, true), new THREE.MeshStandardMaterial({ color: 0xeee8dd, roughness: .85, transparent: true, opacity: .13, side: THREE.DoubleSide, depthWrite: false }));
  shell.geometry.rotateX(Math.PI / 2);
  shell.name = "opaque-shell-ends-before-ray-cone";
  shellGroup.add(shell);
  const rays = makeLine([146.774, 200, 250, 300].flatMap(radius => [new THREE.Vector3(0, 0, 40), new THREE.Vector3(radius, 0, .4)]));
  rays.name = "source-to-wall-projection-rays";
  helperGroup.add(rays);

  const wallMask = new THREE.Mesh(new THREE.CylinderGeometry(50, 50, .35, 72), new THREE.MeshBasicMaterial({ color: 0x1c1916, transparent: true, opacity: .72, depthWrite: false }));
  wallMask.geometry.rotateX(Math.PI / 2);
  wallMask.name = "projected-central-mask-shadow";
  wallMask.position.z = .22;
  wallMask.renderOrder = 3;
  const wallHaloMaterial = new THREE.ShaderMaterial({
    transparent: true, depthWrite: false,
    uniforms: { haloColor: { value: new THREE.Color(0xffc886) }, haloIntensity: { value: .34 } },
    vertexShader: "varying vec2 vUv; void main(){vUv=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}",
    fragmentShader: "varying vec2 vUv; uniform vec3 haloColor; uniform float haloIntensity; void main(){float d=length((vUv-.5)*2.0);float core=1.0-smoothstep(.05,.55,d);float aura=1.0-smoothstep(.28,1.0,d);float a=(core*.20+aura*.40)*haloIntensity;gl_FragColor=vec4(haloColor,a);}",
  });
  const wallHalo = new THREE.Mesh(new THREE.PlaneGeometry(700, 700), wallHaloMaterial);
  wallHalo.name = "single-calculated-wall-halo-no-source-mechanics";
  wallHalo.position.z = .11;
  wallHalo.renderOrder = 1;
  shadowGroup.add(wallHalo, wallMask);
  const shadows = { hour: createShadow("hour", 0x2e2923), minute: createShadow("minute", 0x27231f), second: createShadow("second", 0x211f1c) };
  shadowGroup.add(shadows.hour, shadows.minute, shadows.second);

  const baseObjects = new Map([[quartz, -8], [mask, REFERENCE_Z.mask], [carriers.hour, REFERENCE_Z.hour], [carriers.minute, REFERENCE_Z.minute], [carriers.second, REFERENCE_Z.second], [led, REFERENCE_Z.source], [spot, REFERENCE_Z.source], [glareCap, REFERENCE_Z.glareCap]]);
  const explodedOffsets = new Map([[quartz, -12], [mask, 0], [carriers.second, 8], [carriers.minute, 17], [carriers.hour, 26], [led, 40], [spot, 40], [glareCap, 54]]);

  let currentView = "assembly", currentArrangement = "assembled", currentSnapshot = null, lastRawSnapshot = null;
  let disposed = false, loopActive = false, needsRender = true, visible = !document.hidden, intersecting = true, continuous = false, externallyActive = true;
  let settledFrames = 0, lastSize = null, resizeCount = 0, renderCount = 0, animationLoopCount = 0, tickTimer = 0;

  function resize() {
    if (disposed) return false;
    const next = boundedBufferSize(parent.clientWidth, parent.clientHeight, globalThis.devicePixelRatio || 1);
    if (lastSize && next.cssWidth === lastSize.cssWidth && next.cssHeight === lastSize.cssHeight && Math.abs(next.dpr - lastSize.dpr) < 1e-6) return false;
    lastSize = next;
    renderer.setPixelRatio(next.dpr);
    renderer.setSize(next.cssWidth, next.cssHeight, false);
    camera.aspect = next.cssWidth / next.cssHeight;
    camera.updateProjectionMatrix();
    resizeCount += 1;
    needsRender = true;
    return true;
  }

  function setActualShadowCasting(enabled) {
    mask.castShadow = enabled;
    Object.values(carriers).forEach(carrier => carrier.traverse(child => { if (child.isMesh) child.castShadow = enabled; }));
    spot.castShadow = enabled && spot.visible;
  }
  function applyExplode(exploded) {
    baseObjects.forEach((base, object) => { object.position.z = displayZ(base, explodedOffsets.get(object), exploded); });
    spot.target.position.z = 0;
    setActualShadowCasting(!exploded);
  }
  function setView(name = "assembly", immediate = false) {
    const preset = CAMERA_PRESETS[name] || CAMERA_PRESETS.assembly;
    currentView = CAMERA_PRESETS[name] ? name : "assembly";
    camera.position.fromArray(preset.position);
    controls.target.fromArray(preset.target);
    controls.enableRotate = currentView !== "wall";
    if (lastRawSnapshot) update(lastRawSnapshot);
    camera.updateMatrixWorld();
    controls.update();
    needsRender = true;
    if (!immediate) ensureLoop();
    options.onViewChange?.(currentView, { arrangement: currentArrangement });
    return currentView;
  }

  function updateCarrier(name, data, angle, thickness) {
    const carrier = carriers[name];
    if (!carrier || !data) return;
    const height = Math.max(.1, data.tipZ - data.baseZ);
    const ringKey = `${data.carrierInnerRadius}:${data.carrierOuterRadius}:${data.carrierThickness}`;
    if (carrier.userData.ringKey !== ringKey) {
      carrier.userData.ring.geometry.dispose();
      carrier.userData.ring.geometry = createAnnulus(data.carrierInnerRadius, data.carrierOuterRadius, data.carrierThickness, carrier.userData.material).geometry;
      carrier.userData.ringKey = ringKey;
    }
    const profile = { stemWidth: data.stemWidth, crownWidth: data.crownWidth, crownHeight: data.crownHeight, crownStyle: data.crownStyle };
    const finKey = `${height}:${thickness}:${profile.stemWidth}:${profile.crownWidth}:${profile.crownHeight}:${profile.crownStyle}`;
    if (carrier.userData.finKey !== finKey) {
      carrier.userData.fin.geometry.dispose();
      carrier.userData.fin.geometry = createFinGeometry(profile, height, thickness);
      carrier.userData.finKey = finKey;
    }
    const carrierCenterZ = data.carrierBaseZ + data.carrierThickness / 2;
    carrier.userData.fin.position.set(0, data.radius, data.baseZ - carrierCenterZ);
    carrier.rotation.z = blockerRotation(angle);
    carrier.userData.baseZ = carrierCenterZ;
    baseObjects.set(carrier, carrierCenterZ);

    const shadow = shadows[name];
    const shadowKey = `${data.projectedStart}:${data.projectedTip}:${data.projectedBaseWidth}:${data.projectedTipWidth}`;
    if (shadow.userData.geometryKey !== shadowKey) {
      shadow.userData.mesh.geometry.dispose();
      shadow.userData.mesh.geometry = createShadowGeometry(data.projectedStart, data.projectedTip, data.projectedBaseWidth, data.projectedTipWidth);
      shadow.userData.geometryKey = shadowKey;
    }
    shadow.rotation.z = blockerRotation(angle);
  }

  function applyAmbience(mode, snapshot) {
    const evening = mode === "evening";
    scene.background.set(evening ? 0x6d675e : 0xd8d0c2);
    renderer.setClearColor(evening ? 0x6d675e : 0xd8d0c2, 1);
    wallMaterial.color.set(evening ? 0x8b857b : 0xded8cd);
    floorMaterial.color.set(evening ? 0x655d53 : 0xcabda8);
    ambient.intensity = evening ? .55 : 2.2;
    hemisphere.intensity = evening ? .38 : 1.25;
    renderer.toneMappingExposure = evening ? 1.0 : 1.12;
    const enabled = snapshot.lightEnabled === true;
    const intensity = Math.max(0, Number(snapshot.pointIntensity ?? 78) / 100);
    wallHaloMaterial.uniforms.haloIntensity.value = enabled ? intensity * (evening ? 1.0 : .27) : 0;
    Object.values(shadows).forEach(shadow => { shadow.userData.material.opacity = evening ? .62 : .26; });
    wallMask.material.opacity = evening ? .68 : .26;
  }

  function update(snapshot, nowMs = performance.now()) {
    if (!snapshot || disposed) return;
    lastRawSnapshot = snapshot;
    currentSnapshot = sceneContract(snapshot);
    const c = currentSnapshot, angles = snapshot.angles || {};
    updateCarrier("hour", c.fins.hour, angles.hourAngle || 0, c.finRadialThickness);
    updateCarrier("minute", c.fins.minute, angles.minuteAngle || 0, c.finRadialThickness);
    updateCarrier("second", c.fins.second, angles.secondAngle || 0, c.finRadialThickness);
    const wallOnly = currentView === "wall";
    mechanicsGroup.visible = !wallOnly;
    sourceGroup.visible = !wallOnly;
    shellGroup.visible = !wallOnly;
    helperGroup.visible = !wallOnly;
    quartz.visible = snapshot.showQuartz === true;
    mask.visible = snapshot.showPhysicalMask === true;
    carriers.hour.visible = snapshot.showCarriers === true;
    carriers.minute.visible = snapshot.showCarriers === true;
    carriers.second.visible = snapshot.showCarriers === true && snapshot.secondEnabled !== false;
    led.visible = snapshot.showSourceHardware === true;
    glareCap.visible = snapshot.showGlareCap === true;
    shell.visible = snapshot.showShell === true;
    rays.visible = snapshot.showProjectionRays === true;
    shadows.hour.visible = snapshot.showHandShadows === true;
    shadows.minute.visible = snapshot.showHandShadows === true;
    shadows.second.visible = snapshot.showHandShadows === true && snapshot.secondEnabled !== false;
    wallMask.visible = snapshot.showMaskShadow === true;
    wallHalo.visible = snapshot.showWallHalo === true;
    spot.visible = snapshot.lightEnabled === true;

    mask.scale.set(c.maskPhysicalRadius, c.maskPhysicalRadius, 1);
    baseObjects.set(mask, c.maskZ);
    wallMask.scale.setScalar(c.projectedMaskRadius / 50);
    led.position.x = spot.position.x = Number(snapshot.ledOffsetX) || 0;
    led.position.y = spot.position.y = Number(snapshot.ledOffsetY) || 0;
    baseObjects.set(led, c.sourceZ);
    baseObjects.set(spot, c.sourceZ);
    spot.angle = THREE.MathUtils.degToRad(c.fieldHalfAngle);
    spot.intensity = snapshot.lightEnabled === true ? Math.max(0, Number(snapshot.pointIntensity ?? 78) / 100 * 5200) : 0;
    const rgb = snapshot.pointRgb || [255, 205, 145];
    spot.color.setRGB(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255, THREE.SRGBColorSpace);
    led.material.color.copy(spot.color);
    wallHaloMaterial.uniforms.haloColor.value.copy(spot.color);
    glareCap.scale.set(c.glareCapDiameter / 2, c.glareCapDiameter / 2, 1);
    baseObjects.set(glareCap, c.sourceZ + 6);

    const shellLength = Math.max(2, c.sourceZ + 4 - c.shellLipZ);
    shell.scale.set(c.shellRadius, c.shellRadius, shellLength);
    shell.position.z = c.shellLipZ + shellLength / 2;
    rays.geometry.dispose();
    rays.geometry = new THREE.BufferGeometry().setFromPoints([c.fins.hour.projectedStart, c.fins.hour.projectedTip, c.fins.minute.projectedTip, c.fins.second.projectedTip].flatMap(radius => [new THREE.Vector3(0, 0, c.sourceZ), new THREE.Vector3(radius, 0, .4)]));
    currentArrangement = snapshot.stackArrangement === "exploded" ? "exploded" : "assembled";
    applyExplode(currentArrangement === "exploded");
    applyAmbience(snapshot.ambienceMode, snapshot);
    continuous = !reducedMotion && snapshot.useRealTime === true;
    syncTickTimer(snapshot);
    needsRender = true;
    ensureLoop();
    options.onFrame?.(nowMs);
  }

  function syncTickTimer(snapshot = lastRawSnapshot) {
    const shouldTick = snapshot?.useRealTime === true && reducedMotion && externallyActive && visible && intersecting && !disposed;
    if (shouldTick && !tickTimer) tickTimer = setInterval(() => { if (options.getSnapshot) update(options.getSnapshot(performance.now())); }, 1000);
    else if (!shouldTick && tickTimer) { clearInterval(tickTimer); tickTimer = 0; }
  }
  function drawFrame(nowMs) {
    if (disposed || !externallyActive || !visible || !intersecting) return;
    if (continuous && options.getSnapshot) update(options.getSnapshot(nowMs), nowMs);
    const changed = controls.update();
    if (needsRender || changed || continuous) { resize(); renderer.render(scene, camera); renderCount += 1; needsRender = false; settledFrames = 0; }
    else if (++settledFrames > 6) stopLoop();
  }
  function ensureLoop() { if (!disposed && externallyActive && !loopActive && visible && intersecting) { loopActive = true; animationLoopCount += 1; renderer.setAnimationLoop(drawFrame); } }
  function stopLoop() { if (loopActive) { renderer.setAnimationLoop(null); loopActive = false; } }
  function invalidate() { needsRender = true; settledFrames = 0; ensureLoop(); }
  function setActive(active) { externallyActive = Boolean(active); syncTickTimer(); if (externallyActive) invalidate(); else stopLoop(); }
  const onVisibility = () => { visible = !document.hidden; syncTickTimer(); if (visible) invalidate(); else stopLoop(); };
  const onContextLost = event => { event.preventDefault(); stopLoop(); options.onError?.(new Error("WebGL context was lost")); };
  document.addEventListener("visibilitychange", onVisibility);
  canvas.addEventListener("webglcontextlost", onContextLost, false);
  controls.addEventListener("change", invalidate);
  const onWindowResize = () => { if (resize()) invalidate(); };
  const resizeObserver = typeof ResizeObserver === "function" ? new ResizeObserver(onWindowResize) : null;
  if (resizeObserver) resizeObserver.observe(parent); else globalThis.addEventListener?.("resize", onWindowResize);
  const intersectionObserver = typeof IntersectionObserver === "function" ? new IntersectionObserver(entries => { intersecting = entries.some(entry => entry.isIntersecting); syncTickTimer(); if (intersecting) invalidate(); else stopLoop(); }, { rootMargin: "120px" }) : null;
  intersectionObserver?.observe(parent);

  function debug() {
    const names = [], shadowCastingLights = [];
    scene.traverse(object => { if (object.name) names.push(object.name); if (object.isLight && object.castShadow) shadowCastingLights.push(object.name); });
    return { revision: THREE.REVISION, view: currentView, arrangement: currentArrangement, ambienceMode: lastRawSnapshot?.ambienceMode, architecture: currentSnapshot?.architecture, objectNames: names, shadowCastingLights, buffer: lastSize, resizeCount, renderCount, animationLoopCount, loopActive, tickTimerActive: Boolean(tickTimer), visibility: { showQuartz: quartz.visible, showShell: shell.visible, showPhysicalMask: mask.visible, showCarriers: carriers.hour.visible && carriers.minute.visible, showSourceHardware: led.visible, showGlareCap: glareCap.visible, showProjectionRays: rays.visible, showHandShadows: shadows.hour.visible && shadows.minute.visible, showMaskShadow: wallMask.visible, showWallHalo: wallHalo.visible, lightEnabled: spot.visible && spot.intensity > 0, haloEmittedIntensity: wallHaloMaterial.uniforms.haloIntensity.value }, castShadow: { spot: spot.castShadow, mask: mask.castShadow, hourFin: carriers.hour.userData.fin.castShadow, ambient: ambient.castShadow, hemisphere: hemisphere.castShadow }, camera: { position: camera.position.toArray(), target: controls.target.toArray(), minDistance: controls.minDistance, maxDistance: controls.maxDistance, far: camera.far, zoomEnabled: controls.enableZoom, matrixFinite: camera.matrixWorld.elements.every(Number.isFinite) } };
  }
  function dispose() {
    if (disposed) return;
    disposed = true;
    if (tickTimer) clearInterval(tickTimer);
    stopLoop();
    document.removeEventListener("visibilitychange", onVisibility);
    canvas.removeEventListener("webglcontextlost", onContextLost, false);
    controls.removeEventListener("change", invalidate);
    controls.dispose();
    resizeObserver?.disconnect();
    if (!resizeObserver) globalThis.removeEventListener?.("resize", onWindowResize);
    intersectionObserver?.disconnect();
    const geometries = new Set(), materials = new Set();
    scene.traverse(object => { if (object.geometry) geometries.add(object.geometry); if (object.material) (Array.isArray(object.material) ? object.material : [object.material]).forEach(material => materials.add(material)); });
    geometries.forEach(geometry => geometry.dispose());
    materials.forEach(material => material.dispose());
    renderer.dispose();
  }

  setView("assembly", true);
  resize();
  invalidate();
  return Object.freeze({ available: true, update, setView, resetView: () => setView(currentView), setActive, resize, invalidate, debug, dispose, get canvas() { return canvas; } });
}

export { MAX_BUFFER_PIXELS, CAMERA_DISTANCE_LIMITS, REFERENCE_Z, ORDER, CAMERA_PRESETS, boundedBufferSize, blockerRotation, blockerWorldTip, displayZ, fullAngleToHalfAngle, sceneContract, createFinGeometry, mount };
