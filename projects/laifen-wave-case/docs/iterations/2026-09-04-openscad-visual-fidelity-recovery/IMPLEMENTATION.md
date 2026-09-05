# VFR-01U implementation receipt

## Owner and provenance

- Owner identity: `/root/openscad_mobile_toast_impl`, implementation role.
- Frozen input: `inputs/UI_RECOVERY_MANIFEST.sha256`.
- Verified manifest fingerprint before edits: `4d09d530b31e1e74b0467edfb1d594abca9b33fd56280508c511f5c723fc0cd6`.

## Changed paths

- `preview/openscad-wasm-simulator/index.html`
- `preview/openscad-wasm-simulator/style.css`
- `preview/openscad-wasm-simulator/src/main.mjs`
- `tests/test_openscad_wasm_simulator.py`
- This receipt.

## Implementation

The mobile grid now presents a sticky canvas first, followed by a separately scrollable parameter panel and a sticky, full-width Generate action. Raw compiler output is retained in collapsed `details`. A concise assertive toast presents validation, compiler, result-verification, and timeout failures; dismissing it returns focus to Generate. Non-fatal localization diagnostics are retained in raw details and do not produce the primary diagnostic status, while other diagnostics and compiler errors remain visible through concise status/toast text.

No OpenSCAD source, schema geometry, worker protocol, output identity, generated artifact, or STL bytes were changed.

## Validation and handoff

Focused source checks and the production build were attempted earlier in this task; the focused pytest run reported `5 passed` and the Vite production build completed. Further shell verification was stopped because the root reported EMFILE pressure. This implementation owner does not approve the candidate.

Independent validation must still exercise the mobile layout, a successful generation, a genuine validation-error toast, dismissal/focus restoration, collapsed raw diagnostics, and the actual Tailscale delivery surface. CAD, artifact/slicer, and physical acceptance remain unchanged and out of scope.

## Repair cycle 1

For critique candidate `09eb7635454e890130c609e9ef5e85ac0e9155dd019359baf284436eaece305e`, validation toasts now reuse the specific validation text already set in status and add concise recovery guidance. Raw diagnostics now append a real newline. Focus-safe dismissal, geometry, schema, worker, output identity, and STL bytes are unchanged. Focused assertions cover both repairs. This implementation owner does not approve the repaired candidate.

Wording correction: the toast now says “Adjust that value and try again.” It no longer claims that a field has been highlighted.
