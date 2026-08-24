export const CAM = Object.freeze({
  rodDiameter: 4, rodLength: 50, primaryOuterDiameter: 64, secondaryOuterDiameter: 60,
  innerDiameter: 50, innerClearSpan: 18.5, xt60EnvelopeWidth: 15.9, totalStroke: 11,
  minAngleDegrees: 0, contactAngleDegrees: 44, maxAngleDegrees: 54,
  center: Object.freeze({ z: 13, y: 7 }),
});
const SQRT_HALF = Math.SQRT1_2;
const EPSILON = 1e-9;
export const WIRE = Object.freeze({ diameter: 4.3, radius: 2.15, bendRadius: 6, bendAngleDegrees: 90 });
export const RODS = Object.freeze([
  Object.freeze({ id: "upper", label: "Upper reaction rod", open: Object.freeze({ z: 6.85, y: 14 }), direction: Object.freeze({ z: 1, y: 0 }) }),
  Object.freeze({ id: "lower", label: "Lower reaction rod", open: Object.freeze({ z: 8, y: -15.15 }), direction: Object.freeze({ z: 0, y: 1 }) }),
  Object.freeze({ id: "forming", label: "Diagonal forming rod", open: Object.freeze({ z: 30.955308593052023, y: -8.955308593052022 }), direction: Object.freeze({ z: -SQRT_HALF, y: SQRT_HALF }) }),
]);
export const DEFAULT_CAM_STATE = Object.freeze({ thetaRel: 0, locked: false });
export function clamp(value, min, max) { return Math.max(min, Math.min(max, Number(value) || 0)); }
export function clampAngle(value) { return clamp(value, CAM.minAngleDegrees, CAM.maxAngleDegrees); }
export function smoothstep(value) { const x = clamp(value, 0, 1); return x * x * (3 - 2 * x); }
export function camProgressFromAngle(thetaRel) { return smoothstep(clampAngle(thetaRel) / CAM.maxAngleDegrees); }
export function commonTravelFromAngle(thetaRel) { return CAM.totalStroke * camProgressFromAngle(thetaRel); }
export function plateRotations(thetaRel) { const theta = clampAngle(thetaRel); return Object.freeze({ thetaRel: theta, left: -theta / 2, right: theta / 2, innerLeft: 0, innerRight: 0 }); }
export function sideRotationRadians(side, thetaRel) { const rotations = plateRotations(thetaRel); if (side === "left") return rotations.left * Math.PI / 180; if (side === "right") return rotations.right * Math.PI / 180; throw new Error(`Unknown side: ${side}`); }
export function reduceCamState(state = DEFAULT_CAM_STATE, action = {}) {
  switch (action.type) {
    case "SET_THETA": return state.locked ? state : { ...state, thetaRel: clampAngle(action.value) };
    case "OPEN": return state.locked ? state : { ...state, thetaRel: CAM.minAngleDegrees };
    case "CLOSE": return state.locked ? state : { ...state, thetaRel: CAM.maxAngleDegrees };
    case "LOCK": return { ...state, thetaRel: CAM.maxAngleDegrees, locked: true };
    case "UNLOCK": return { ...state, locked: false };
    case "TOGGLE_LOCK": return state.locked ? { ...state, locked: false } : { ...state, thetaRel: CAM.maxAngleDegrees, locked: true };
    case "RESET": return { ...DEFAULT_CAM_STATE };
    default: return state;
  }
}
export function rodById(id) { const rod = RODS.find(candidate => candidate.id === id); if (!rod) throw new Error(`Unknown rod: ${id}`); return rod; }
export function rodPoseAtAngle(id, thetaRel) { const rod = rodById(id); const commonTravel = commonTravelFromAngle(thetaRel); const z = rod.open.z + commonTravel * rod.direction.z; const y = rod.open.y + commonTravel * rod.direction.y; return { id, thetaRel: clampAngle(thetaRel), commonTravel, z, y, left: { x: -CAM.rodLength / 2, z, y }, right: { x: CAM.rodLength / 2, z, y }, skew: 0 }; }
export function allRodPoses(thetaRel) { return RODS.map(rod => rodPoseAtAngle(rod.id, thetaRel)); }
function rotateZY(point, angle) { const c = Math.cos(angle); const s = Math.sin(angle); return { z: point.z * c - point.y * s, y: point.z * s + point.y * c }; }
// Each side owns an inverse-transform slot, avoiding a visual-only sign flip.
export function sideLocalSlotPoint(rodId, side, thetaRel) { const pose = rodPoseAtAngle(rodId, thetaRel); return rotateZY({ z: pose.z - CAM.center.z, y: pose.y - CAM.center.y }, -sideRotationRadians(side, thetaRel)); }
export function reconstructSideFollower(localPoint, side, thetaRel) { const world = rotateZY(localPoint, sideRotationRadians(side, thetaRel)); return { z: world.z + CAM.center.z, y: world.y + CAM.center.y }; }
export function sideSlotSamples(rodId, side, sampleCount = 121) { const count = Math.max(2, Number(sampleCount) || 2); return Array.from({ length: count }, (_, index) => { const thetaRel = CAM.maxAngleDegrees * index / (count - 1); return { thetaRel, ...sideLocalSlotPoint(rodId, side, thetaRel) }; }); }
export function sampledSkew(thetaRel) { return RODS.map(rod => { const left = reconstructSideFollower(sideLocalSlotPoint(rod.id, "left", thetaRel), "left", thetaRel); const right = reconstructSideFollower(sideLocalSlotPoint(rod.id, "right", thetaRel), "right", thetaRel); return { id: rod.id, left, right, skew: Math.hypot(left.z - right.z, left.y - right.y) }; }); }
export function stationaryGuide(id) { const rod = rodById(id); return { id, open: { ...rod.open }, direction: { ...rod.direction } }; }
export function distance2D(a, b) { return Math.hypot(a.z - b.z, a.y - b.y); }
export function sampledCollisionReport(samples = 121) { let minimumRodGap = Infinity; const collisions = []; const count = Math.max(2, Number(samples) || 2); for (let index = 0; index < count; index += 1) { const theta = CAM.maxAngleDegrees * index / (count - 1); const rods = allRodPoses(theta); for (let first = 0; first < rods.length; first += 1) for (let second = first + 1; second < rods.length; second += 1) { const gap = distance2D(rods[first], rods[second]) - CAM.rodDiameter; minimumRodGap = Math.min(minimumRodGap, gap); if (gap < -EPSILON) collisions.push({ theta, first: rods[first].id, second: rods[second].id, gap }); } } return { collisions, minimumRodGap }; }
export function mechanismReadout(thetaRel) { const theta = clampAngle(thetaRel); const rotations = plateRotations(theta); const skew = sampledSkew(theta); return { rodCount: RODS.length, rodDiameter: CAM.rodDiameter, rodLength: CAM.rodLength, thetaRel: theta, camProgress: camProgressFromAngle(theta), commonTravel: commonTravelFromAngle(theta), ...rotations, modeledSkew: Math.max(...skew.map(item => item.skew)), closed: theta >= CAM.maxAngleDegrees }; }
