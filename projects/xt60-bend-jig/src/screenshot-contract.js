export const SCREENSHOT_PRESETS = Object.freeze({
  open: Object.freeze({ camera: "iso", state: Object.freeze({ angle: 0, locked: false }) }),
  forming: Object.freeze({ camera: "iso", state: Object.freeze({ angle: 80, locked: false }) }),
  locked: Object.freeze({ camera: "side", state: Object.freeze({ angle: 80, locked: true }) }),
  top: Object.freeze({ camera: "top", state: Object.freeze({ angle: 45, locked: false }) }),
});

export function screenshotPresetFromSearch(search = "") {
  const name = new URLSearchParams(String(search).replace(/^\?/, "")).get("shot");
  if (!name || !SCREENSHOT_PRESETS[name]) return null;
  return { name, camera: SCREENSHOT_PRESETS[name].camera, state: { ...SCREENSHOT_PRESETS[name].state } };
}
