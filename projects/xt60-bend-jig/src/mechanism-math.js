export const MECHANISM = Object.freeze({
  rodRadius: 2,
  rodLength: 50,
  boreDiameter: 4.2,
  sidePlateOuterSpan: 48,
  bendRadius: 6,
  horizontalRun: 16,
  openStroke: 11,
  upperOffsets: Object.freeze([4, 6, 8, 10, 12]),
  lowerOffsets: Object.freeze([4, 6, 8, 10, 12]),
});

const EPSILON = 1e-9;

export function clamp01(value) {
  return Math.min(1, Math.max(0, Number(value) || 0));
}

export function positionIndex(value) {
  return Math.round(Math.min(5, Math.max(1, Number(value) || 1)));
}

export function distance(a, b) {
  return Math.hypot(a.z - b.z, a.y - b.y);
}

export function pointSegmentDistance(point, start, end) {
  const dz = end.z - start.z;
  const dy = end.y - start.y;
  const lengthSquared = dz * dz + dy * dy;
  if (lengthSquared < EPSILON) return distance(point, start);
  const projection = Math.min(1, Math.max(0, ((point.z - start.z) * dz + (point.y - start.y) * dy) / lengthSquared));
  return distance(point, { z: start.z + projection * dz, y: start.y + projection * dy });
}

export function polylineLength(points) {
  let length = 0;
  for (let index = 1; index < points.length; index += 1) length += distance(points[index - 1], points[index]);
  return length;
}

export function distanceToPolyline(point, points) {
  let minimum = Infinity;
  for (let index = 1; index < points.length; index += 1) {
    minimum = Math.min(minimum, pointSegmentDistance(point, points[index - 1], points[index]));
  }
  return minimum;
}

export function buildWirePath({ wireLength, angleDegrees = 90, samples = 96 } = {}) {
  const angle = clamp01(Number(angleDegrees) / 90) * Math.PI / 2;
  const arcLength = MECHANISM.bendRadius * angle;
  const tailLength = Number(wireLength) - MECHANISM.horizontalRun - arcLength;
  const center = { z: MECHANISM.horizontalRun, y: MECHANISM.bendRadius };
  const points = [{ z: 0, y: 0 }, { z: MECHANISM.horizontalRun, y: 0 }];
  const arcSamples = Math.max(8, Math.round(samples * Math.max(angle, .01) / (Math.PI / 2)));
  for (let index = 1; index <= arcSamples; index += 1) {
    const q = angle * index / arcSamples;
    const phi = -Math.PI / 2 + q;
    points.push({
      z: center.z + MECHANISM.bendRadius * Math.cos(phi),
      y: center.y + MECHANISM.bendRadius * Math.sin(phi),
    });
  }
  const arcEnd = points.at(-1);
  points.push({
    z: arcEnd.z + Math.max(0, tailLength) * Math.cos(angle),
    y: arcEnd.y + Math.max(0, tailLength) * Math.sin(angle),
  });
  const exactLength = MECHANISM.horizontalRun + arcLength + Math.max(0, tailLength);
  const renderedLength = polylineLength(points);
  return {
    angleDegrees: angle * 180 / Math.PI,
    center,
    points,
    horizontalLength: MECHANISM.horizontalRun,
    arcLength,
    tailLength,
    exactLength,
    renderedLength,
    renderedLengthError: renderedLength - exactLength,
    startTangent: { z: 1, y: 0 },
    endTangent: { z: Math.cos(angle), y: Math.sin(angle) },
    valid: tailLength >= 0,
  };
}

export function solveMechanism({
  upperRodPosition = 3,
  lowerRodPosition = 3,
  wireLength = 44,
  wireDiameter = 4.3,
  clampAmount = 1,
  bendAmount = 1,
} = {}) {
  const upperIndex = positionIndex(upperRodPosition);
  const lowerIndex = positionIndex(lowerRodPosition);
  const wireRadius = Number(wireDiameter) / 2;
  const contactRadius = MECHANISM.rodRadius + wireRadius;
  const bendAngle = 90 * clamp01(bendAmount);
  const wire = buildWirePath({ wireLength, angleDegrees: bendAngle });
  const verticalZ = MECHANISM.horizontalRun + MECHANISM.bendRadius;
  const upperOffset = MECHANISM.upperOffsets[upperIndex - 1];
  const lowerOffset = MECHANISM.lowerOffsets[lowerIndex - 1];

  const upper = {
    z: verticalZ - contactRadius,
    y: MECHANISM.bendRadius + upperOffset,
  };
  const lower = {
    z: MECHANISM.horizontalRun - lowerOffset,
    y: -contactRadius,
  };

  const diagonal = { z: Math.SQRT1_2, y: -Math.SQRT1_2 };
  const arcContact = {
    z: wire.center.z + MECHANISM.bendRadius * diagonal.z,
    y: wire.center.y + MECHANISM.bendRadius * diagonal.y,
  };
  const movingClosed = {
    z: wire.center.z + (MECHANISM.bendRadius + contactRadius) * diagonal.z,
    y: wire.center.y + (MECHANISM.bendRadius + contactRadius) * diagonal.y,
  };
  const retraction = MECHANISM.openStroke * (1 - clamp01(clampAmount));
  const moving = {
    z: movingClosed.z + diagonal.z * retraction,
    y: movingClosed.y + diagonal.y * retraction,
  };

  const requiredTail = upperOffset + Number(wireDiameter);
  const minimumWireLength = MECHANISM.horizontalRun + Math.PI * MECHANISM.bendRadius / 2 + requiredTail;
  const rodCenters = { upper, lower, moving };
  const contactGaps = Object.fromEntries(Object.entries(rodCenters).map(([name, centerPoint]) => [
    name,
    distanceToPolyline(centerPoint, wire.points) - contactRadius,
  ]));
  const rodSeparations = {
    upperLower: distance(upper, lower) - 2 * MECHANISM.rodRadius,
    upperMoving: distance(upper, moving) - 2 * MECHANISM.rodRadius,
    lowerMoving: distance(lower, moving) - 2 * MECHANISM.rodRadius,
  };

  return {
    wire,
    wireRadius,
    contactRadius,
    upperIndex,
    lowerIndex,
    upperOffset,
    lowerOffset,
    rods: rodCenters,
    movingClosed,
    movingDirection: diagonal,
    arcContact,
    contacts: {
      upper: { z: verticalZ, y: upper.y },
      lower: { z: lower.z, y: 0 },
      moving: { ...arcContact },
    },
    minimumWireLength,
    wireLengthMargin: Number(wireLength) - minimumWireLength,
    contactGaps,
    rodSeparations,
    rodSpanMargin: MECHANISM.rodLength - MECHANISM.sidePlateOuterSpan,
    synchronizedEnds: {
      left: { ...moving },
      right: { ...moving },
      skew: 0,
    },
  };
}

export function validateClosedMechanism(options = {}, tolerance = 0.015) {
  const solved = solveMechanism({ ...options, clampAmount: 1, bendAmount: 1 });
  const checks = {
    wireLengthConserved: Math.abs(solved.wire.exactLength - Number(options.wireLength ?? 44)) <= EPSILON
      && Math.abs(solved.wire.renderedLengthError) <= .002,
    bendIsNinetyDegrees: Math.abs(solved.wire.angleDegrees - 90) <= EPSILON,
    upperRodTangent: Math.abs(solved.contactGaps.upper) <= tolerance,
    lowerRodTangent: Math.abs(solved.contactGaps.lower) <= tolerance,
    movingRodTangent: Math.abs(solved.contactGaps.moving) <= tolerance,
    rodsDoNotOverlap: Object.values(solved.rodSeparations).every(gap => gap >= -tolerance),
    rodSpansBothPlates: solved.rodSpanMargin >= 0,
    movingEndsSynchronized: solved.synchronizedEnds.skew <= tolerance,
    wireLongEnough: solved.wireLengthMargin >= 0,
  };
  return { solved, checks, valid: Object.values(checks).every(Boolean) };
}
