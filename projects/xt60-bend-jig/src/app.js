import { CAM, DEFAULT_CAM_STATE, mechanismReadout, reduceCamState } from "./cam-contract.js";
import { mount } from "./scene.js";
import { screenshotPresetFromSearch } from "./screenshot-contract.js";

const elements = Object.fromEntries([
  "mechanismCanvas", "sceneTitle", "sceneDescription", "resetButton", "lockReadout", "angleSlider",
  "angleReadout", "openButton", "cycleButton", "closeButton", "lockButton", "travelReadout",
  "progressReadout", "skewReadout", "bendReadout",
].map(id => [id, document.getElementById(id)]));
const cameraButtons = [...document.querySelectorAll("[data-camera]")];
const screenshotPreset = screenshotPresetFromSearch(globalThis.location?.search || "");
const reducedMotion = globalThis.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches ?? false;

export const state = { ...DEFAULT_CAM_STATE, ...(screenshotPreset?.state || {}) };
let scene = null;
let runToken = 0;
let cycleRunning = false;

function copyFor(readout) {
  if (state.locked) return { title: `SHAFT LOCKED AT ${readout.angle.toFixed(1)}°`, description: `The index lock holds both cam plates and all three rods at ${readout.commonTravel.toFixed(2)} mm common travel.` };
  if (readout.closedDwell) return { title: "90° FORMING POSITION", description: "All three rods are at their tangent endpoints. The final 10° of dial rotation is a closed dwell." };
  if (readout.camProgress > .01) return { title: "ALL THREE RODS MOVING", description: "Six followers track two mirrored cam plates while straight guides prevent sideways drift." };
  return { title: "MECHANISM OPEN", description: "All three rods are retracted. The ESC is below the flight controller and both leads begin horizontal." };
}

export function render() {
  const readout = mechanismReadout(state.angle);
  const copy = copyFor(readout);
  elements.sceneTitle.textContent = copy.title;
  elements.sceneDescription.textContent = copy.description;
  elements.angleReadout.textContent = `${readout.angle.toFixed(1)}°`;
  elements.angleSlider.value = String(readout.angle);
  elements.angleSlider.disabled = state.locked;
  elements.resetButton.disabled = state.locked;
  elements.openButton.disabled = state.locked || readout.angle === CAM.minAngleDegrees;
  elements.closeButton.disabled = state.locked || readout.angle === CAM.maxAngleDegrees;
  elements.cycleButton.disabled = state.locked || cycleRunning;
  elements.lockReadout.textContent = state.locked ? "LOCKED" : "UNLOCKED";
  elements.lockReadout.classList.toggle("is-locked", state.locked);
  elements.lockButton.textContent = state.locked ? "Unlock shared shaft" : "Lock shaft here";
  elements.lockButton.classList.toggle("is-locked", state.locked);
  elements.lockButton.setAttribute("aria-pressed", String(state.locked));
  elements.travelReadout.textContent = readout.commonTravel.toFixed(2);
  elements.progressReadout.textContent = `${(readout.camProgress * 100).toFixed(0)}%`;
  elements.skewReadout.textContent = readout.modeledSkew.toFixed(3);
  elements.bendReadout.textContent = `${(readout.camProgress * 90).toFixed(1)}°`;
  scene?.update(state);
}

function setState(action) {
  Object.assign(state, reduceCamState(state, action));
  render();
}

function cancelCycle() {
  runToken += 1;
  cycleRunning = false;
  elements.cycleButton.disabled = false;
  elements.cycleButton.textContent = "Run bend";
}

function animateAngle(from, to, duration, token) {
  return new Promise(resolve => {
    if (reducedMotion) { state.angle = to; render(); resolve(); return; }
    const started = performance.now();
    function tick(now) {
      if (token !== runToken) { resolve(); return; }
      const raw = Math.min(1, (now - started) / duration);
      const eased = raw * raw * (3 - 2 * raw);
      state.angle = from + (to - from) * eased;
      render();
      if (raw < 1) requestAnimationFrame(tick); else resolve();
    }
    requestAnimationFrame(tick);
  });
}

export async function runCycle() {
  if (state.locked) return false;
  const token = ++runToken;
  cycleRunning = true;
  state.locked = false;
  state.angle = 0;
  elements.cycleButton.disabled = true;
  elements.cycleButton.textContent = "Bending…";
  render();
  await animateAngle(0, CAM.maxAngleDegrees, 1700, token);
  if (token === runToken) {
    cycleRunning = false;
    state.locked = true;
    elements.cycleButton.disabled = false;
    elements.cycleButton.textContent = "Replay bend";
    render();
  }
  return true;
}

elements.angleSlider.addEventListener("input", event => { cancelCycle(); setState({ type: "SET_ANGLE", value: event.currentTarget.value }); });
elements.openButton.addEventListener("click", () => { cancelCycle(); setState({ type: "OPEN" }); });
elements.closeButton.addEventListener("click", () => { cancelCycle(); setState({ type: "CLOSE" }); });
elements.lockButton.addEventListener("click", () => { cancelCycle(); setState({ type: "TOGGLE_LOCK" }); });
elements.cycleButton.addEventListener("click", runCycle);
elements.resetButton.addEventListener("click", () => {
  if (state.locked) return;
  cancelCycle();
  Object.assign(state, DEFAULT_CAM_STATE);
  scene?.setCamera("iso");
  cameraButtons.forEach(button => { const active = button.dataset.camera === "iso"; button.classList.toggle("is-active", active); button.setAttribute("aria-pressed", String(active)); });
  render();
});
cameraButtons.forEach(button => button.addEventListener("click", () => {
  cameraButtons.forEach(peer => { const active = peer === button; peer.classList.toggle("is-active", active); peer.setAttribute("aria-pressed", String(active)); });
  scene?.setCamera(button.dataset.camera);
}));

try {
  scene = mount({ canvas: elements.mechanismCanvas });
  if (screenshotPreset) {
    scene.setCamera(screenshotPreset.camera, true);
    cameraButtons.forEach(button => { const active = button.dataset.camera === screenshotPreset.camera; button.classList.toggle("is-active", active); button.setAttribute("aria-pressed", String(active)); });
    document.documentElement.dataset.screenshotPreset = screenshotPreset.name;
  }
  render();
} catch (error) {
  elements.sceneTitle.textContent = "3D PREVIEW UNAVAILABLE";
  elements.sceneDescription.textContent = error.message;
  elements.cycleButton.disabled = true;
}

globalThis.addEventListener("beforeunload", () => scene?.dispose());
