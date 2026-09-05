# P2 R20 real Three.js generator handoff

**Status:** frozen design contract written; implementation not started.  
**Owner:** `DES-GCS-R20-REC-01`.

R20 is a structural reset after rejected R19 candidate `566aa6bc8c0aa57f1aeea341805a48db7d54c2078a48cebc4f9204a685e2fc74`. The implementer must build a new R20-only Three.js generator from the frozen R10 descriptor, not another SVG witness-card renderer.

Exact implementer write scope:

- `projects/laifen-wave-case/preview/p2-r20-real-threejs-generator/**`
- `projects/laifen-wave-case/tests/test_p2_r20_source_contract.mjs`
- `projects/laifen-wave-case/tests/test_p2_r20_scene_invariants.mjs`
- `projects/laifen-wave-case/tests/test_p2_r20_family_geometry.mjs`
- `projects/laifen-wave-case/tests/test_p2_r20_ui_contract.mjs`
- `projects/laifen-wave-case/tests/test_p2_r20_browser.py`
- `projects/laifen-wave-case/scratch/r20-*/**`
- R20 receipts and manifests under this iteration directory

Allowed reads include AGENTS, CAD workflow/continuity, R10 core schema/derive/presets, R6 Three.js source, R3 live/delivery records, and R19 candidate/evidence/failure records. Forbidden writes include R10 core, R6, R3, R19/prior iterations, current live route/served bytes, CAD/OpenSCAD/STEP/export/slicer/printer/physical/MakerWorld/publication state, and unrelated project files.

Stop before candidate freeze unless the full source contract, scene invariant, family geometry, UI, compact independent-style audit, screenshot-sheet, and six-context browser gates pass. Stop immediately on any need for a prior/core/live/CAD/export/slicer/physical edit, any prior-renderer import, any per-field witness/hash mechanism, any SVG proxy-card substitution for the main viewport, any missing R10 field coverage, any generic fallback that satisfies a field by scalar/string length, or retry exhaustion.

Initial implementation plus at most two grouped repair cycles are allowed. No live route, served copy, delivery, CAD/OpenSCAD/STEP/slicer/print, MakerWorld, or physical acceptance is authorized before independent validation, independent critique, and formal review all PASS one R20 candidate fingerprint.

Frozen input manifest: `inputs/frozen-inputs.sha256`, 57 entries, SHA-256/design fingerprint `d2097cf93f9ee295dfe86fa687c6cfa5f698890ff089027dbebadc4ffdcd2378`.
