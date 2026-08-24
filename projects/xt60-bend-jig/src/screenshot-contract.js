export const SCREENSHOT_PRESETS = Object.freeze({
  open: Object.freeze({ camera: "iso", state: Object.freeze({ thetaRel: 0, locked: false }) }),
  mid: Object.freeze({ camera: "iso", state: Object.freeze({ thetaRel: 27, locked: false }) }),
  closed: Object.freeze({ camera: "side", state: Object.freeze({ thetaRel: 54, locked: false }) }),
  locked: Object.freeze({ camera: "side", state: Object.freeze({ thetaRel: 54, locked: true }) }),
});
export function screenshotPresetFromSearch(search = "") { const name = new URLSearchParams(String(search).replace(/^\?/, "")).get("shot"); return name && SCREENSHOT_PRESETS[name] ? { name, camera: SCREENSHOT_PRESETS[name].camera, state: { ...SCREENSHOT_PRESETS[name].state } } : null; }
