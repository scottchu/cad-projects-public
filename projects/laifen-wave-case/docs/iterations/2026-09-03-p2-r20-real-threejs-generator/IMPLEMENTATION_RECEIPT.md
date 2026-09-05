# R20 implementation receipt

**Owner:** `IMP-GCS-R20-01`  
**Status:** candidate frozen for independent validation, critique, and review; not live or delivered.  
**Frozen design fingerprint:** `d2097cf93f9ee295dfe86fa687c6cfa5f698890ff089027dbebadc4ffdcd2378` (all 57 entries verified from repository root).

## Candidate

- Candidate manifest: `candidate-files.sha256`
- Candidate fingerprint: `ae45f4e28fd6c34b09c56c34a4d55eb0bed7620f101559e028aa31d12fd98ad4`
- Evidence manifest: `evidence-files.sha256`
- Evidence fingerprint: `05f2f3b1e722e2b8027a8e098d8903bb7458a37a5111ed1e65c6859c46941187`
- Candidate scope: R20 preview (HTML, app, CSS, pure geometry recipe, Three.js scene builder, semantic map) and five R20 tests only.

## Implemented evidence surface

The standalone R20 page imports frozen R10 schema, derivation, presets, and utilities plus Three.js through its import map. It creates named lower/upper mesh geometry, cross-section geometry, ends, closure geometry, pattern lines, drain cylinders, glyph/patch planes, attachment geometry, and truthful font metadata. The renderer returns object-level evidence with names, paths, vertices, bounds, world transforms, and material roles.

The compact control surface has preset and Basic/Advanced tiers, validates through R10 before building a scene, clears the scene for invalid state, and contains the required conceptual-only disclosure. It does not import a prior renderer or map and contains no SVG proxy viewport.

## Validation

Executed from repository root:

```text
sha256sum -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r20-real-threejs-generator/inputs/frozen-inputs.sha256
node projects/laifen-wave-case/tests/test_p2_r20_source_contract.mjs
node projects/laifen-wave-case/tests/test_p2_r20_scene_invariants.mjs
node projects/laifen-wave-case/tests/test_p2_r20_family_geometry.mjs
node projects/laifen-wave-case/tests/test_p2_r20_ui_contract.mjs
node projects/laifen-wave-case/scratch/r20-independent-style-audit/audit.mjs
uv run python projects/laifen-wave-case/tests/test_p2_r20_browser.py
```

Results: manifest `57/57` OK; source contract passed with 12 R20 source/test/audit files and 168 active pair mappings; scene invariant, family geometry, UI, and compact audit passed; compact audit reports `84/84` coverage and zero banned-source hits. The browser test passed Chromium, Firefox, and WebKit at desktop and mobile viewports, including visible control interaction, valid and invalid state handling, zero console/request failures, responsive nonzero canvas, disclosure/readout, no horizontal overflow, and five actual Three.js viewport screenshots.

Screenshot evidence is in `scratch/r20-scene-sheets/` for surface/fade, labels, attachment, polygon/end/drain, and closure with captions hidden. I visually inspected the polygon/end/drain and label captures after the passing browser run.

## Repair record

Two grouped repair cycles were used after the initial implementation:

1. Corrected the source-test filesystem target and made recessed diamonds geometrically distinct from blunt diamonds.
2. Corrected the Three.js drain-array syntax and browser control interaction through collapsed modules; the final browser evidence also uses a visible label angle and asserts actual named scene objects.

## Acceptance boundary and remaining gaps

This is conceptual browser evidence only. It makes no CAD, OpenSCAD, export, slicer, printability, fit, drainage-performance, strength, font-parity, or physical acceptance claim. Independent VAL, CRIT, and formal REV must each pass this exact candidate fingerprint before any live-route, served-byte, delivery, CAD, export, or print action.
