# R21 implementation receipt

**Owner:** `IMP-GCS-R20-01`  
**Status:** R21 candidate frozen for independent validation, critique, and formal review. It is not live or delivered.  
**Frozen design fingerprint:** `6d862ad3294a460da1cfdceace4e499d3fe23c809e5bb520767713cad18205df`, with all 37 frozen entries verified.

## Candidate and evidence

- Baseline examined: R20 noncandidate `ae45f4e28fd6c34b09c56c34a4d55eb0bed7620f101559e028aa31d12fd98ad4`.
- R21 candidate manifest: `candidate-files.sha256`.
- R21 candidate fingerprint: `3d2ce130e8724af9b80a7617296276c71e8d08c02b3117d94f1ad52ff004f443`.
- R21 evidence manifest: `evidence-files.sha256`.
- R21 evidence fingerprint: `41f76a57cded945c9be3f5dd7164c29389438f5e57aeaee998ec6f533ec9f7ad`.

The candidate contains the standalone R21 preview, descriptor-plan and materialization code, explicit pattern and glyph-metric modules, semantic map, and six named R21 tests. Evidence contains 24 current Chromium WebGL viewport screenshots: ten patterns, closures, fades/relief, drains, ends, labels, five attachment modes, polygon, and exploded states.

## Implemented correction

`app.mjs` owns mutable controls and calls frozen R10 `derive(state)`. Only a valid descriptor crosses into `buildScenePlan(descriptor, presentation/view options)`, then `materializeScene(plan)`. The scene modules do not receive raw state.

Labels use pinned glyph-run metrics and descriptor dimensions for glyph and patch bounds. Ten named pattern builder functions dispatch directly by R10 enum. The view has OrbitControls, wheel zoom, ISO/front/top controls that move the same camera, and a fit routine over visible model geometry. Closure, drain, end, surface, section, label, and attachment geometry are materialized as named Three.js scene objects; OpenSCAD font metadata is visible in the UI as truthful metadata.

## Commands and results

Executed from repository root:

```text
sha256sum -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r21-threejs-interaction-fidelity-recovery/inputs/frozen-inputs.sha256
npm --version
uv run --package laifen-wave-case python -c 'import sys; print(sys.version.split()[0])'
node projects/laifen-wave-case/tests/test_p2_r21_source_contract.mjs
node projects/laifen-wave-case/tests/test_p2_r21_descriptor_boundary.mjs
node projects/laifen-wave-case/tests/test_p2_r21_scene_invariants.mjs
node projects/laifen-wave-case/tests/test_p2_r21_family_geometry.mjs
node projects/laifen-wave-case/tests/test_p2_r21_ui_contract.mjs
uv run --package laifen-wave-case python projects/laifen-wave-case/tests/test_p2_r21_browser.py
sha256sum -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r21-threejs-interaction-fidelity-recovery/candidate-files.sha256
sha256sum -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r21-threejs-interaction-fidelity-recovery/evidence-files.sha256
```

Results: manifest `37/37` OK; npm `11.19.0`; Python `3.12.13`; source contract passed 14 R21 source/test files and all 84 semantic rows; descriptor-only plan, scene invariant, family geometry, and UI gates passed. The six-context browser matrix passed Chromium, Firefox, and WebKit at `1280x900` and `390x844`, with pointer orbit, wheel zoom, fixed views, controls, preset/tier/presentation transitions, valid/invalid clearing, zero console/request errors, nonblank canvas, no horizontal overflow, and real viewport screenshots.

## Repair record

Two grouped repair cycles were used after the initial implementation:

1. Corrected a materialization-scope error that prevented the initial WebGL scene from becoming valid.
2. Corrected camera-pose observability and fit behavior: pointer-orbit checks now observe camera and pixel change, and fixed views normalize their direction before applying the fitted distance.

## Acceptance boundary

R21 is conceptual browser evidence only. It makes no CAD, OpenSCAD, export, slicer, printability, fit, drainage-performance, strength, or physical acceptance claim. R21 must remain unserved and undispatched until independent `VAL-GCS-R21`, `CRIT-GCS-R21`, and `REV-GCS-R21` pass this exact candidate fingerprint.
