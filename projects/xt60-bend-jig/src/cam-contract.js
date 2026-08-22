export const CAM = Object.freeze({
  rodDiameter: 4,
  rodLength: 50,
  sidePlateOuterSpan: 48,
  shaftDiameter: 5,
  followerDiameter: 3,
  grooveWidth: 3.4,
  camPlateDiameter: 56,
  totalStroke: 11,
  minAngleDegrees: 0,
  activeAngleDegrees: 70,
  maxAngleDegrees: 80,
  center: Object.freeze({ z: 13, y: 7 }),
});

const SQRT_HALF = Math.SQRT1_2;
const EPSILON = 1e-9;

export const WIRE = Object.freeze({
  diameter: 4.3,
  radius: 2.15,
  bendRadius: 6,
  bendAngleDegrees: 90,
  bendCenter: Object.freeze({ z: 16, y: 6 }),
  horizontalTangent: Object.freeze({ z: 1, y: 0 }),
  verticalTangent: Object.freeze({ z: 0, y: 1 }),
});

export const RODS = Object.freeze([
  Object.freeze({
    id: "upper",
    label: "Upper reaction rod",
    contact: Object.freeze({ z: 22, y: 14 }),
    closed: Object.freeze({ z: 17.85, y: 14 }),
    open: Object.freeze({ z: 6.85, y: 14 }),
    direction: Object.freeze({ z: 1, y: 0 }),
  }),
  Object.freeze({
    id: "lower",
    label: "Lower reaction rod",
    contact: Object.freeze({ z: 8, y: 0 }),
    closed: Object.freeze({ z: 8, y: -4.15 }),
    open: Object.freeze({ z: 8, y: -15.15 }),
    direction: Object.freeze({ z: 0, y: 1 }),
  }),
  Object.freeze({
    id: "forming",
    label: "Diagonal forming rod",
    contact: Object.freeze({ z: 20.242640687119286, y: 1.7573593128807152 }),
    closed: Object.freeze({ z: 23.177134, y: -1.177134 }),
    open: Object.freeze({ z: 30.955308593052023, y: -8.955308593052022 }),
    direction: Object.freeze({ z: -SQRT_HALF, y: SQRT_HALF }),
  }),
]);

export const DEFAULT_CAM_STATE = Object.freeze({ angle: 0, locked: false });

export function clamp(value, min, max) {
  return Math.max(min, Math.min(max, Number(value) || 0));
}

export function clampAngle(value) {
  return clamp(value, CAM.minAngleDegrees, CAM.maxAngleDegrees);
}

export function smoothstep(value) {
  const x = clamp(value, 0, 1);
  return x * x * (3 - 2 * x);
}

export function camProgressFromAngle(angleDegrees) {
  return smoothstep(clampAngle(angleDegrees) / CAM.activeAngleDegrees);
}

export function commonTravelFromAngle(angleDegrees) {
  return CAM.totalStroke * camProgressFromAngle(angleDegrees);
}

export function reduceCamState(state = DEFAULT_CAM_STATE, action = {}) {
  switch (action.type) {
    case "SET_ANGLE":
      return state.locked ? state : { ...state, angle: clampAngle(action.value) };
    case "OPEN":
      return state.locked ? state : { ...state, angle: CAM.minAngleDegrees };
    case "CLOSE":
      return state.locked ? state : { ...state, angle: CAM.maxAngleDegrees };
    case "LOCK":
      return { ...state, locked: true };
    case "UNLOCK":
      return { ...state, locked: false };
    case "TOGGLE_LOCK":
      return { ...state, locked: !state.locked };
    case "RESET":
      return { ...DEFAULT_CAM_STATE };
    default:
      return state;
  }
}

export function rodById(id) {
  const rod = RODS.find(candidate => candidate.id === id);
  if (!rod) throw new Error(`Unknown rod: ${id}`);
  return rod;
}

export function rodPoseAtAngle(id, angleDegrees) {
  const rod = rodById(id);
  const commonTravel = commonTravelFromAngle(angleDegrees);
  const z = rod.open.z + commonTravel * rod.direction.z;
  const y = rod.open.y + commonTravel * rod.direction.y;
  return {
    id,
    angle: clampAngle(angleDegrees),
    camProgress: camProgressFromAngle(angleDegrees),
    commonTravel,
    z,
    y,
    left: { x: -CAM.rodLength / 2, z, y },
    right: { x: CAM.rodLength / 2, z, y },
    skew: 0,
  };
}

export function allRodPoses(angleDegrees) {
  return RODS.map(rod => rodPoseAtAngle(rod.id, angleDegrees));
}

export function sharedCamAngleRadians(angleDegrees) {
  return clampAngle(angleDegrees) * Math.PI / 180;
}

export function exteriorFaceAngleDegrees(side, angleDegrees) {
  const angle = clampAngle(angleDegrees);
  if (side === "left") return angle;
  if (side === "right") return -angle;
  throw new Error(`Unknown side: ${side}`);
}

function rotateZY(point, angle) {
  const c = Math.cos(angle);
  const s = Math.sin(angle);
  return { z: point.z * c - point.y * s, y: point.z * s + point.y * c };
}

export function camLocalPoint(rodId, angleDegrees) {
  const pose = rodPoseAtAngle(rodId, angleDegrees);
  const relative = { z: pose.z - CAM.center.z, y: pose.y - CAM.center.y };
  return rotateZY(relative, -sharedCamAngleRadians(angleDegrees));
}

export function reconstructCamFollower(localPoint, angleDegrees) {
  const world = rotateZY(localPoint, sharedCamAngleRadians(angleDegrees));
  return { z: world.z + CAM.center.z, y: world.y + CAM.center.y };
}

export function camSlotSamples(rodId, sampleCount = 161) {
  const count = Math.max(2, Number(sampleCount) || 2);
  return Array.from({ length: count }, (_, index) => {
    const angle = CAM.minAngleDegrees + (CAM.maxAngleDegrees - CAM.minAngleDegrees) * index / (count - 1);
    return { angle, ...camLocalPoint(rodId, angle) };
  });
}

export function stationaryGuide(id) {
  const rod = rodById(id);
  return { id, open: { ...rod.open }, closed: { ...rod.closed }, direction: { ...rod.direction } };
}

export function distance2D(a, b) {
  return Math.hypot(a.z - b.z, a.y - b.y);
}

export function contactGap(id, angleDegrees) {
  const rod = rodById(id);
  const pose = rodPoseAtAngle(id, angleDegrees);
  return distance2D(pose, rod.contact) - (CAM.rodDiameter / 2 + WIRE.diameter / 2);
}

export function profileCompatible(wireDiameter) {
  return Math.abs(Number(wireDiameter) - WIRE.diameter) <= EPSILON;
}

export function sampledCollisionReport(samples = 161) {
  let minimumRodGap = Infinity;
  const collisions = [];
  const count = Math.max(2, Number(samples) || 2);
  for (let index = 0; index < count; index += 1) {
    const angle = CAM.maxAngleDegrees * index / (count - 1);
    const rods = allRodPoses(angle);
    for (let first = 0; first < rods.length; first += 1) {
      for (let second = first + 1; second < rods.length; second += 1) {
        const gap = distance2D(rods[first], rods[second]) - CAM.rodDiameter;
        minimumRodGap = Math.min(minimumRodGap, gap);
        if (gap < -EPSILON) collisions.push({ angle, first: rods[first].id, second: rods[second].id, gap });
      }
    }
  }
  return { collisions, minimumRodGap };
}

export function mechanismReadout(angleDegrees) {
  const angle = clampAngle(angleDegrees);
  return {
    rodCount: RODS.length,
    rodDiameter: CAM.rodDiameter,
    rodLength: CAM.rodLength,
    angle,
    camProgress: camProgressFromAngle(angle),
    commonTravel: commonTravelFromAngle(angle),
    leftExteriorAngle: exteriorFaceAngleDegrees("left", angle),
    rightExteriorAngle: exteriorFaceAngleDegrees("right", angle),
    modeledSkew: Math.max(...allRodPoses(angle).map(rod => rod.skew)),
    closedDwell: angle >= CAM.activeAngleDegrees,
  };
}
