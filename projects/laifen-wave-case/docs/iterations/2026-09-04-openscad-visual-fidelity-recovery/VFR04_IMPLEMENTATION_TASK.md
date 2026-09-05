# VFR-04 implementation task

Status: ready after a frozen implementation manifest is recorded.

## Objective

Implement the user-approved B relationship in the OpenSCAD WASM customizer: two separate body/cap roles, N33 at defaults derived from valley radius, a meaningful default plateau half-fraction of 0.18, one shared seam-centered phase, and diamond texture continuing to both sides of the middle seam.

Follow `VFR04_DESIGN.md`. Preserve the exact smooth branch and protected dimensions, threads, bores, floors, drains, chamfers, output transforms, browser job identity, mobile layout, toast/raw-diagnostic behavior, and 180-second watchdog.

## Exclusive implementation writes

- `openscad/laifen_case_customizer_v1.scad`
- `openscad/customizer_contract.py`
- `preview/openscad-wasm-simulator/src/schema.mjs`
- `preview/openscad-wasm-simulator/src/main.mjs`
- `preview/openscad-wasm-simulator/index.html`
- `preview/openscad-wasm-simulator/style.css`
- `preview/openscad-wasm-simulator/workers/openscad.worker.js` only if required by measured evidence
- `tests/test_openscad_customizer.py`
- `tests/test_openscad_wasm_simulator.py`
- optional `tests/test_openscad_diamond_field.py`
- new explicit candidate artifacts under `openscad/generated_vfr04/`
- scratch evidence under `scratch/vfr04-implementation/`
- implementation receipt `docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/VFR04_IMPLEMENTATION.md`

No other source, CAD, prior artifact, service, Tailscale, MakerWorld, printer, or continuity file may change in this task.

## Done gate

Run the staged G1-G5 checks prescribed by `VFR04_DESIGN.md`. Stop downstream work if a cheap gate fails. Only enable the browser diamond selector after real pinned WASM Manifold body and cap outputs are each nonempty, watertight, one-component and within the stated timing/triangle budgets. Generate and record actual body, cap, assembled and print-layout candidate files plus source/parameter/hashes/metrics when the gates pass. Preserve smooth output geometry as a regression oracle. Run focused pytest and Vite build. Inspect the actual locally served browser result on desktop and 390 x 844 mobile.

Use one initial attempt plus at most two focused repair cycles. A timeout consumes an attempt. Do not extend the UI timeout, silently reduce requested geometry, fake the pattern in Three.js, or change protected internals to force a pass. Physical/slicer/STEP acceptance remains outside this OpenSCAD candidate.
