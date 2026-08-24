import assert from "node:assert/strict";
import test from "node:test";
import { SCREENSHOT_PRESETS, screenshotPresetFromSearch } from "../src/screenshot-contract.js";
test("P17 screenshot presets cover open counter-twist mid closed and locked", () => { assert.deepEqual(Object.keys(SCREENSHOT_PRESETS), ["open", "mid", "closed", "locked"]); assert.deepEqual(screenshotPresetFromSearch("?shot=locked"), { name: "locked", camera: "side", state: { thetaRel: 54, locked: true } }); assert.equal(screenshotPresetFromSearch("?shot=missing"), null); });
