import assert from "node:assert/strict";
import test from "node:test";

import {
  allRodPoses,
  CAM,
  camLocalPoint,
  camProgressFromAngle,
  camSlotSamples,
  commonTravelFromAngle,
  contactGap,
  DEFAULT_CAM_STATE,
  distance2D,
  exteriorFaceAngleDegrees,
  profileCompatible,
  reconstructCamFollower,
  reduceCamState,
  RODS,
  rodPoseAtAngle,
  sampledCollisionReport,
  WIRE,
} from "../src/cam-contract.js";

test("contract freezes exactly three purchased 4 x 50 mm rods", () => {
  assert.deepEqual(RODS.map(rod => rod.id), ["upper", "lower", "forming"]);
  assert.equal(CAM.rodDiameter, 4);
  assert.equal(CAM.rodLength, 50);
  assert.equal(CAM.rodLength - CAM.sidePlateOuterSpan, 2);
});

test("all rods use identical monotonic common travel with no perpendicular drift", () => {
  let previous = -Infinity;
  for (let step = 0; step <= 160; step += 1) {
    const angle = CAM.maxAngleDegrees * step / 160;
    const commonTravel = commonTravelFromAngle(angle);
    assert.ok(commonTravel >= previous - 1e-12);
    previous = commonTravel;
    for (const rod of RODS) {
      const pose = rodPoseAtAngle(rod.id, angle);
      const delta = { z: pose.z - rod.open.z, y: pose.y - rod.open.y };
      const along = delta.z * rod.direction.z + delta.y * rod.direction.y;
      const perpendicular = delta.z * -rod.direction.y + delta.y * rod.direction.z;
      assert.ok(Math.abs(along - commonTravel) < 1e-9);
      assert.ok(Math.abs(perpendicular) < 1e-9);
    }
  }
});

test("closed dwell from 70 to 80 degrees leaves all rods fixed", () => {
  assert.equal(camProgressFromAngle(70), 1);
  assert.equal(camProgressFromAngle(80), 1);
  for (const rod of RODS) assert.ok(distance2D(rodPoseAtAngle(rod.id, 70), rodPoseAtAngle(rod.id, 80)) < 1e-9);
});

test("closed contacts are tangent and open gaps are eleven millimeters", () => {
  for (const rod of RODS) {
    assert.ok(Math.abs(contactGap(rod.id, 80)) < 1e-5, rod.id);
    assert.ok(contactGap(rod.id, 0) >= 10.999, rod.id);
  }
});

test("left and right rod endpoints have zero modeled skew", () => {
  for (let step = 0; step <= 160; step += 1) {
    for (const rod of allRodPoses(step / 2)) {
      assert.equal(rod.left.y, rod.right.y);
      assert.equal(rod.left.z, rod.right.z);
      assert.equal(rod.skew, 0);
    }
  }
});

test("outside-face cam angles mirror while both plates share one world shaft angle", () => {
  for (let step = 0; step <= 80; step += 1) {
    assert.equal(exteriorFaceAngleDegrees("left", step), -exteriorFaceAngleDegrees("right", step));
  }
});

test("each curved groove reconstructs its follower exactly", () => {
  for (const rod of RODS) {
    for (const sample of camSlotSamples(rod.id, 161)) {
      const local = camLocalPoint(rod.id, sample.angle);
      const world = reconstructCamFollower(local, sample.angle);
      const follower = rodPoseAtAngle(rod.id, sample.angle);
      assert.ok(distance2D(world, follower) < 1e-9);
    }
  }
});

test("lock freezes dial input and unlock permits reopening", () => {
  let state = reduceCamState(DEFAULT_CAM_STATE, { type: "CLOSE" });
  state = reduceCamState(state, { type: "LOCK" });
  assert.equal(state.angle, 80);
  assert.equal(reduceCamState(state, { type: "SET_ANGLE", value: 0 }), state);
  assert.equal(reduceCamState(state, { type: "OPEN" }), state);
  state = reduceCamState(state, { type: "UNLOCK" });
  assert.equal(reduceCamState(state, { type: "OPEN" }).angle, 0);
});

test("wire relation is exactly ninety degrees and profile is 12 AWG only", () => {
  assert.equal(WIRE.horizontalTangent.z * WIRE.verticalTangent.z + WIRE.horizontalTangent.y * WIRE.verticalTangent.y, 0);
  assert.equal(WIRE.bendAngleDegrees, 90);
  assert.equal(profileCompatible(4.3), true);
  assert.equal(profileCompatible(3.5), false);
});

test("sampled states contain no unintended rod-to-rod collisions", () => {
  const report = sampledCollisionReport(161);
  assert.deepEqual(report.collisions, []);
  assert.ok(report.minimumRodGap >= 0);
});
