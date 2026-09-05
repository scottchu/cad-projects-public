# UI recovery task

Task ID: `VFR-01U`

Owner role: implementation agent. This task changes presentation and diagnostic handling only; it does not change OpenSCAD geometry, parameters, output identity, worker compilation, or generated STL bytes.

Input manifest: `inputs/UI_RECOVERY_MANIFEST.sha256`

Manifest fingerprint: `4d09d530b31e1e74b0467edfb1d594abca9b33fd56280508c511f5c723fc0cd6`

## Objective and done gate

On mobile, keep the rendered canvas sticky at the top, keep the parameter panel below it independently scrollable, and keep the primary Generate action sticky and easy to reach. Show actionable failures as an accessible toast. Keep raw compiler logs in a collapsed details element. Filter the proven non-fatal OpenSCAD localization warning from the primary user surface while retaining it in raw details.

Done requires focused source tests, a successful production build, and browser evidence for mobile layout, successful generation, a real validation error toast, dismissal/focus behavior, and collapsed raw diagnostics. The user's actual Tailscale delivery surface must be checked after independent validation.

## Dependencies and scope

Dependencies: the frozen UI manifest above and the user's explicit mobile/toast requirements. This UI-only task is independent of VFR-02/VFR-03 geometry and pattern decisions.

Allowed writes: `preview/openscad-wasm-simulator/index.html`, `style.css`, `src/main.mjs`, and focused tests in `tests/test_openscad_wasm_simulator.py`. The implementation owner may write an implementation receipt under this iteration.

Forbidden: OpenSCAD source or schema geometry changes, worker protocol changes, generated CAD/artifact replacement, fake Three.js geometry, public hosting, MakerWorld, slicer, printer, and production registration.

## Role and ceilings

Implementation uses a balanced model at medium effort, one initial attempt and at most two focused repairs. Critique, validation, and formal review must use distinct identities after the candidate is frozen. Stop if the required layout would need geometry or worker-protocol changes.
