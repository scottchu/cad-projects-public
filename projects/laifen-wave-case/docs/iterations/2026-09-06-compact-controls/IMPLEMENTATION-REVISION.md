# MC-IMP-02 — coherent draft-state implementation

Status: implementation complete; independent Safari, critique, validation and
formal review remain pending. Verified `RULES-REVISION.md` SHA-256
`53f9dd990507ec640f615cac30dbc466e1ecff325494886af2535c96e586a6ca`,
`inputs/rules-revision.sha256` SHA-256
`75b16b2f8d2e59847ef2689266d5b3b634cfae75cdd57ecd8e1b34eaf5b920be`,
and rejected-C4 input manifest `dd9dfcbe25d7946207d009ddb8e2ee1a499442b6d712202bed31f7fe192d0d1d`
(20/20 paths OK) before editing.

`deriveDraftState(raw,lastValidDimensions)` is now the controller's only owner
of direct/coupled issues, field/form error projections, all slider intervals and
source-labeled rules, summary, generation values, Generate eligibility and the
next complete last-valid snapshot. Any dimension issue pauses every dimension
slider and derives its displayed rule from the unchanged whole last-valid
snapshot. Coupled issues have deterministic participant sets and one live form
error association. Selector errors block Generate without pausing valid
dimension sliders. The controller no longer calls `adapt()`, uses no
`editedKey`, and accepts range input only from an enabled interval.

Changed application/test paths: `index.html`, `src/bounds.mjs`, new
`src/controller.mjs`, `src/controls.mjs`, `src/main.mjs`,
`tests/node/desktop-customizer.test.mjs`, and new
`tests/node/compact-controller.test.mjs`. This receipt is the only documentation
write. SCAD, schema, worker, dependency lock, CSS/layout, adapter, lifecycle and
services were not changed by MC-IMP-02. Preserved hashes: SCAD `ade77d3f...`,
schema `89406233...`, worker `fabd1535...`, dependency lock `6d4a6b00...`.

Commands run from repository root:

- `npm exec --workspace laifen-wave-case -- node --test tests/node/desktop-customizer.test.mjs tests/node/compact-controller.test.mjs` — PASS, 25/25.
- `uv run pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q` — PASS, 4/4.
- `node --check` for `bounds.mjs`, `controller.mjs`, and `main.mjs` — PASS.
- `git diff --check` for the bounded app/test paths — PASS.

Integrated fake-DOM checks cover defaults, literal blank/70 retention, global
slider pause and last-valid labels, selector stability, deterministic manual and
Auto coupled issues with all participants, Auto recovery, same-final-state
order independence, enabled slider synchronization without generation,
Generate values, edit-during-generation invalidation, and reset without
generation. Existing generation epoch, exact Blob and late-result tests remain
passing. No build was run because `dist` is the live preview input; root owns the
post-freeze build and Safari checks. No CAD, mesh, slicer or physical acceptance
is claimed.
