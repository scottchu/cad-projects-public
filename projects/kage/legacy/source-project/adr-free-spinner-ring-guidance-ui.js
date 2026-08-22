(function () {
  "use strict";

  const $ = (id) => document.getElementById(id);
  const canvas = $("adrCanvas");
  const status = $("adrStatus");
  const STEPS = [
    ["carrier stack", "Start with the three carrier rings and their integral guide beads."],
    ["two fixed towers", "Install datum towers at 60° and 180°. Their positions do not adjust."],
    ["adjustable tower", "Add the 300° tower and set its radial position within ±0.25 mm."],
    ["nine rollers", "Load one independently rotating deep-grooved roller for H, M, and S at every tower."],
    ["preload check", "Confirm bead-only contact, axial relief, capture overlap, free rotation, and no gear-tooth contact."],
  ];
  let state = KageFreeSpinnerADR.normalizeState({ comparison: "proposed", arrangement: "assembled", assemblyStep: 4 });
  let scene;

  function setPressed(buttons, active) {
    buttons.forEach((button) => {
      const selected = button === active;
      button.classList.toggle("is-active", selected);
      button.setAttribute("aria-pressed", String(selected));
    });
  }

  function syncUI() {
    setPressed([$("comparisonProposed"), $("comparisonCurrent")], state.comparison === "proposed" ? $("comparisonProposed") : $("comparisonCurrent"));
    const arrangementButtons = [...document.querySelectorAll("[data-arrangement]")];
    setPressed(arrangementButtons, arrangementButtons.find((button) => button.dataset.arrangement === state.arrangement));
    const handButtons = [...document.querySelectorAll("[data-hand]")];
    setPressed(handButtons, handButtons.find((button) => button.dataset.hand === state.selectedHand));
    $("rotationInput").value = String(state.rotationDegrees);
    $("rotationReadout").textContent = `${Math.round(state.rotationDegrees)}°`;
    $("towerAdjustmentInput").value = state.adjustmentMm.toFixed(2);
    $("towerAdjustmentReadout").textContent = `${state.adjustmentMm >= 0 ? "+" : ""}${state.adjustmentMm.toFixed(2)} mm`;
    $("toggleLabels").checked = state.showLabels;
    $("toggleForces").checked = state.showForces;
    $("assemblyStepReadout").textContent = `Step ${state.assemblyStep} · ${STEPS[state.assemblyStep][0]}`;
    $("assemblyStepDetail").textContent = STEPS[state.assemblyStep][1];
    $("assemblyPrev").disabled = state.assemblyStep === 0;
    $("assemblyNext").disabled = state.assemblyStep === STEPS.length - 1;
    [...$("assemblyStepList").children].forEach((item, index) => item.classList.toggle("is-active", index <= state.assemblyStep));
    const proposed = state.comparison === "proposed";
    $("adrCanvasKicker").textContent = proposed ? "PROPOSED / THREE FREE-SPINNER TOWERS" : "CURRENT / CONTINUOUS KEEPER SYSTEM";
    $("adrCanvasTitle").textContent = proposed ? "Nine rollers guide three rings without touching gear teeth." : "Long rails, shoes, caps, and a spine consume the under-stack service zone.";
  }

  function update(patch) {
    state = scene ? scene.setState({ ...state, ...patch }) : KageFreeSpinnerADR.normalizeState({ ...state, ...patch });
    syncUI();
  }

  try {
    scene = KageFreeSpinnerADR.mount({
      canvas,
      parent: $("adrViewer"),
      initialState: state,
      onStateChange(nextState, contract) {
        state = nextState;
        status.textContent = `${contract.towerCount} towers · ${contract.rollerCount} independent rollers · CAD intent only`;
      },
    });
    status.textContent = "3 towers · 9 independent rollers · CAD intent only";
  } catch (error) {
    console.error(error);
    status.textContent = `3D unavailable · ${error.message}`;
  }

  $("comparisonProposed").addEventListener("click", () => update({ comparison: "proposed" }));
  $("comparisonCurrent").addEventListener("click", () => update({ comparison: "current" }));
  document.querySelectorAll("[data-arrangement]").forEach((button) => button.addEventListener("click", () => {
    update({ arrangement: button.dataset.arrangement });
    scene?.setCameraPreset(button.dataset.arrangement);
  }));
  document.querySelectorAll("[data-hand]").forEach((button) => button.addEventListener("click", () => update({ selectedHand: button.dataset.hand })));
  $("rotationInput").addEventListener("input", (event) => update({ rotationDegrees: Number(event.target.value) }));
  $("towerAdjustmentInput").addEventListener("input", (event) => update({ adjustmentMm: Number(event.target.value) }));
  $("toggleLabels").addEventListener("change", (event) => update({ showLabels: event.target.checked }));
  $("toggleForces").addEventListener("change", (event) => update({ showForces: event.target.checked }));
  $("assemblyPrev").addEventListener("click", () => update({ assemblyStep: state.assemblyStep - 1 }));
  $("assemblyNext").addEventListener("click", () => update({ assemblyStep: state.assemblyStep + 1 }));
  window.addEventListener("beforeunload", () => scene?.dispose(), { once: true });
  syncUI();
}());
