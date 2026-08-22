import assert from "node:assert/strict";
import test from "node:test";
import { readFile } from "node:fs/promises";

import { CAM, mechanismReadout, reduceCamState } from "../src/cam-contract.js";
import { boundedBufferSize, CAMERA_PRESETS, RENDER_GEOMETRY, wirePathPoints } from "../src/scene.js";

test("browser surface exposes only the three-cam mechanism controls", async () => {
  const html = await readFile(new URL("../index.html", import.meta.url), "utf8");
  for (const id of ["mechanismCanvas", "angleSlider", "lockButton", "cycleButton", "travelReadout", "bendReadout"]) assert.match(html, new RegExp(`id=["']${id}["']`));
  assert.match(html, /Three-rod cam bender/);
  assert.match(html, /3 × Ø4×50 · 6 CAM SLOTS · 1 SHAFT/);
  assert.doesNotMatch(html, /setup gauge|external clamps|P6 two-plate/i);
  assert.doesNotMatch(html, /(?:src|href)=["']https?:\/\//);
});

test("scene declares the approved architecture and FPV workpiece", async () => {
  const source = await readFile(new URL("../src/scene.js", import.meta.url), "utf8");
  for (const token of [
    "three-rods-two-mirrored-cams-one-shared-shaft", "single-shared-keyed-cam-shaft",
    "curved-cam-slot", "straight-guide", "bottom-esc-board-with-power-pads",
    "flight-controller-above-esc", "red-horizontal-to-vertical-lead",
    "black-horizontal-to-vertical-lead", "xt60-connector-following-bent-leads",
    "stationary-split-shaft-brake-grounded-to-left-frame", "shaft-brake-shoe-closes-without-rotating",
  ]) assert.match(source, new RegExp(token));
  assert.doesNotMatch(source, /assemblyPose|optional-removable-38mm-setup-gauge|external-clamp|lockPin/);
});

test("camera contract is ISO SIDE TOP and render buffer is bounded", () => {
  assert.deepEqual(new Set(Object.keys(CAMERA_PRESETS)), new Set(["iso", "side", "top"]));
  assert.ok(boundedBufferSize(2400, 1800, 3).bufferPixels <= 2_073_600);
});

test("lock-anywhere freezes the current angle", () => {
  let state = reduceCamState({ angle: 43.5, locked: false }, { type: "LOCK" });
  assert.deepEqual(state, { angle: 43.5, locked: true });
  state = reduceCamState(state, { type: "SET_ANGLE", value: 0 });
  assert.equal(state.angle, 43.5);
  state = reduceCamState(state, { type: "UNLOCK" });
  assert.deepEqual(state, { angle: 43.5, locked: false }, "unlock must not jump the mechanism");
  assert.equal(mechanismReadout(CAM.maxAngleDegrees).commonTravel, 11);
});

test("app blocks every mechanism motion command while locked", async () => {
  const source = await readFile(new URL("../src/app.js", import.meta.url), "utf8");
  assert.match(source, /if \(state\.locked\) return false;/);
  assert.match(source, /cycleButton\.disabled = state\.locked \|\| cycleRunning/);
  assert.match(source, /angleSlider\.disabled = state\.locked/);
  assert.match(source, /resetButton\.disabled = state\.locked/);
  assert.match(source, /if \(state\.locked\) return;[\s\S]*Object\.assign\(state, DEFAULT_CAM_STATE\)/);
});

test("rendered wires touch the ESC pad surface and retain 44 mm arclength", () => {
  assert.ok(Math.abs(RENDER_GEOMETRY.wireCenterY - 4.3 / 2 - RENDER_GEOMETRY.escPadSurfaceY) < 1e-12);
  for (const angle of [0, Math.PI / 4, Math.PI / 2]) {
    const points = wirePathPoints(angle);
    assert.ok(Math.abs(points[0].y - 4.3 / 2 - RENDER_GEOMETRY.escPadSurfaceY) < 1e-12);
    let length = 0;
    for (let index = 1; index < points.length; index += 1) length += points[index].distanceTo(points[index - 1]);
    assert.ok(Math.abs(length - RENDER_GEOMETRY.leadLength) < .004, `${angle}: ${length}`);
  }
  const closed = wirePathPoints(Math.PI / 2);
  const tail = closed.at(-1).clone().sub(closed.at(-2)).normalize();
  assert.ok(Math.abs(tail.z) < 1e-12 && Math.abs(tail.y - 1) < 1e-12);
});

test("mobile CSS establishes safe areas, 44 px controls, and overflow containment", async () => {
  const css = await readFile(new URL("../styles.css", import.meta.url), "utf8");
  for (const token of ["safe-area-inset-top", "safe-area-inset-right", "safe-area-inset-bottom", "safe-area-inset-left"]) assert.match(css, new RegExp(token));
  assert.match(css, /html, body \{[^}]*max-width: 100%[^}]*overflow-x: hidden/s);
  assert.match(css, /\.camera-toolbar button \{[^}]*min-width: 44px[^}]*min-height: 44px/s);
  assert.match(css, /\.button-quiet \{[^}]*min-width: 44px[^}]*min-height: 44px/s);
  assert.match(css, /\.drive-actions button, \.lock-button \{[^}]*min-width: 44px[^}]*min-height: 44px/s);
  assert.match(css, /@media \(max-width: 340px\)/);
});
