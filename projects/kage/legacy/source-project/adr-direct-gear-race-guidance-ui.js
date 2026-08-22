(function () {
  "use strict";

  const $ = (id) => document.getElementById(id);
  const canvas = $("adrCanvas");
  const status = $("adrStatus");
  const STEPS = [
    ["bare carrier rings", "Start with the three bare 260T carrier rings. Their smooth lower inner cylinders are the running races."],
    ["two fixed towers", "Install datum towers at 60° and 180°. Their positions do not adjust."],
    ["adjustable tower", "Add the 300° tower and set its radial position within ±0.25 mm."],
    ["nine relieved rollers", "Load one asymmetric relieved roller for H, M, and S at every tower."],
    ["contact check", "Confirm carrier-only race contact, tooth clearance, axial relief, and free rotation."],
  ];
  let state = KageDirectGearRaceADR.normalizeState({ comparison: "proposed", arrangement: "assembled", assemblyStep: 4 });
  let scene;

  function setPressed(buttons, active) {
    buttons.forEach((button) => {
      const selected = button === active;
      button.classList.toggle("is-active", selected);
      button.setAttribute("aria-pressed", String(selected));
    });
  }

  function syncUI() {
    setPressed([$("comparisonProposed"), $("comparisonLegacy")], state.comparison === "proposed" ? $("comparisonProposed") : $("comparisonLegacy"));
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
    $("adrCanvasKicker").textContent = proposed ? "PROPOSED / CARRIER ITSELF IS THE RACE" : "LEGACY / MULTIPART KEEPER SYSTEM";
    $("adrCanvasTitle").textContent = proposed ? "Nine relieved rollers capture three bare carrier rings below the teeth." : "Separate keeper components occupy the same service zone.";
  }

  function update(patch) {
    state = scene ? scene.setState({ ...state, ...patch }) : KageDirectGearRaceADR.normalizeState({ ...state, ...patch });
    syncUI();
  }

  try {
    scene = KageDirectGearRaceADR.mount({
      canvas,
      parent: $("adrViewer"),
      initialState: state,
      onStateChange(nextState, contract, clearances) {
        state = nextState;
        status.textContent = `${contract.rollerCount} rollers · ${clearances.nominalRaceGapMm.toFixed(2)} mm nominal gap · CAD intent only`;
      },
    });
    status.textContent = "9 rollers · 0.05 mm nominal gap · CAD intent only";
  } catch (error) {
    console.error(error);
    status.textContent = `3D unavailable · ${error.message}`;
  }

  $("comparisonProposed").addEventListener("click", () => update({ comparison: "proposed" }));
  $("comparisonLegacy").addEventListener("click", () => update({ comparison: "legacy" }));
  document.querySelectorAll("[data-arrangement]").forEach((button) => button.addEventListener("click", () => { update({ arrangement: button.dataset.arrangement }); scene?.setCameraPreset(button.dataset.arrangement); }));
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
