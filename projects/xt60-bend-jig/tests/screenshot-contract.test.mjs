import assert from "node:assert/strict";
import test from "node:test";

import { SCREENSHOT_PRESETS, screenshotPresetFromSearch } from "../src/screenshot-contract.js";

test("screenshot presets cover open forming locked and top states", () => {
  assert.deepEqual(Object.keys(SCREENSHOT_PRESETS), ["open", "forming", "locked", "top"]);
  assert.deepEqual(screenshotPresetFromSearch("?shot=locked"), { name: "locked", camera: "side", state: { angle: 80, locked: true } });
  assert.equal(screenshotPresetFromSearch("?shot=missing"), null);
});
