import assert from "node:assert/strict";
import test from "node:test";

import {
  buildWirePath,
  distance,
  MECHANISM,
  solveMechanism,
  validateClosedMechanism,
} from "../src/mechanism-math.js";

const GAUGES = [
  { gauge: 12, diameter: 4.3 },
  { gauge: 14, diameter: 3.5 },
];

test("the closed centerline is an exact tangent-continuous 90 degree path", () => {
  const path = buildWirePath({ wireLength: 44, angleDegrees: 90, samples: 180 });
  assert.equal(path.angleDegrees, 90);
  assert.ok(path.valid);
  assert.ok(Math.abs(path.exactLength - 44) < 1e-9);
  assert.ok(Math.abs(path.renderedLength - 44) < .001, "the polyline consumed by Three.js must preserve length too");
  assert.deepEqual(path.startTangent, { z: 1, y: 0 });
  assert.ok(Math.abs(path.endTangent.z) < 1e-12);
  assert.ok(Math.abs(path.endTangent.y - 1) < 1e-12);
  assert.deepEqual(path.points[0], { z: 0, y: 0 });
  assert.equal(path.points[1].y, 0);
  const end = path.points.at(-1);
  const beforeEnd = path.points.at(-2);
  assert.ok(Math.abs(end.z - beforeEnd.z) < 1e-9, "the released leg must be vertical at 90 degrees");
});

test("all three rods are tangent to the wire rather than placed by eye", () => {
  for (const { diameter } of GAUGES) {
    for (let upperRodPosition = 1; upperRodPosition <= 5; upperRodPosition += 1) {
      for (let lowerRodPosition = 1; lowerRodPosition <= 5; lowerRodPosition += 1) {
        const { solved, checks } = validateClosedMechanism({
          upperRodPosition,
          lowerRodPosition,
          wireLength: 50,
          wireDiameter: diameter,
        });
        assert.ok(checks.upperRodTangent, JSON.stringify(solved.contactGaps));
        assert.ok(checks.lowerRodTangent, JSON.stringify(solved.contactGaps));
        assert.ok(checks.movingRodTangent, JSON.stringify(solved.contactGaps));
        assert.ok(checks.rodsDoNotOverlap, JSON.stringify(solved.rodSeparations));
      }
    }
  }
});

test("each calculated contact point is exactly one combined radius from its rod center", () => {
  const solved = solveMechanism({ wireLength: 50, wireDiameter: 4.3, clampAmount: 1, bendAmount: 1 });
  for (const name of ["upper", "lower", "moving"]) {
    assert.ok(Math.abs(distance(solved.rods[name], solved.contacts[name]) - solved.contactRadius) < 1e-12, name);
  }
  const radial = {
    z: solved.contacts.moving.z - solved.wire.center.z,
    y: solved.contacts.moving.y - solved.wire.center.y,
  };
  const cross = radial.z * solved.movingDirection.y - radial.y * solved.movingDirection.z;
  assert.ok(Math.abs(cross) < 1e-12, "moving contact normal must align with its 45 degree slot");
});

test("the moving rod follows one straight 45 degree slot and closes monotonically", () => {
  const samples = Array.from({ length: 11 }, (_, index) => solveMechanism({ wireLength: 44, clampAmount: index / 10 }));
  const direction = samples[0].movingDirection;
  assert.ok(Math.abs(direction.z + direction.y) < 1e-12);
  for (let index = 1; index < samples.length; index += 1) {
    const previous = distance(samples[index - 1].rods.moving, samples[index - 1].movingClosed);
    const current = distance(samples[index].rods.moving, samples[index].movingClosed);
    assert.ok(current < previous, `${current} must be below ${previous}`);
  }
  assert.ok(distance(samples.at(-1).rods.moving, samples.at(-1).movingClosed) < 1e-12);
});

test("wire arclength is conserved throughout the animated bend", () => {
  for (const wireLength of [34, 44, 54]) {
    for (let step = 0; step <= 20; step += 1) {
      const path = buildWirePath({ wireLength, angleDegrees: step * 4.5 });
      assert.ok(Math.abs(path.exactLength - wireLength) < 1e-9);
      assert.ok(Math.abs(path.renderedLength - wireLength) < .002);
    }
  }
});

test("both moving-rod ends have identical coordinates and zero skew", () => {
  for (let step = 0; step <= 20; step += 1) {
    const solved = solveMechanism({ wireLength: 44, clampAmount: step / 20 });
    assert.deepEqual(solved.synchronizedEnds.left, solved.synchronizedEnds.right);
    assert.equal(solved.synchronizedEnds.skew, 0);
  }
});

test("the purchased 50 mm rods span the modeled plates with a positive margin", () => {
  const solved = solveMechanism({ wireLength: 44 });
  assert.equal(MECHANISM.rodLength, 50);
  assert.equal(MECHANISM.sidePlateOuterSpan, 48);
  assert.equal(solved.rodSpanMargin, 2);
});

test("short-wire validation is derived from the selected upper reaction point", () => {
  const low = solveMechanism({ upperRodPosition: 1, wireLength: 40, wireDiameter: 4.3 });
  const high = solveMechanism({ upperRodPosition: 5, wireLength: 40, wireDiameter: 4.3 });
  assert.ok(high.minimumWireLength > low.minimumWireLength);
  assert.ok(low.wireLengthMargin > high.wireLengthMargin);
  assert.equal(validateClosedMechanism({ upperRodPosition: 5, wireLength: 34, wireDiameter: 4.3 }).checks.wireLongEnough, false);
});
