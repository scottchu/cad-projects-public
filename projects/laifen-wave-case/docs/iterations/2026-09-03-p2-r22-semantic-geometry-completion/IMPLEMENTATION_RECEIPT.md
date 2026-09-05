# R22 implementation receipt

**Owner:** `IMP-GCS-R22-01`  
**Status:** candidate frozen for independent VAL, CRIT, and REV only; it is not served or delivered.  
**Frozen design fingerprint:** `6647642d1876112a7bf7daad13bd7b05295ff2b011d55af764f23467f510efbc` (`40/40` frozen inputs verified).

## Candidate and evidence

- Candidate manifest: `candidate-files.sha256`
- Candidate fingerprint: `226d8688ba80285a084c25a66a1fb1f140138cecf1253fa30ce738a94cb1803a`
- Evidence manifest: `evidence-files.sha256`
- Evidence fingerprint: `9b6144a70de42ca39a3cdec48442c61c6d976033934a2bf5034e95c2da821bed`

R22 contains a descriptor-only canonical plan registry, indexed body/end/pattern/closure/drain/label/attachment meshes, same-name Three.js materialization, and the standalone R22 UI shell. It contains no `semantic.*` proxy records. The evidence manifest includes the compact gate result and caption-hidden Chromium screenshots under `scratch/r22-scene-sheets/`.

## Validation

Executed from the repository root:

```text
sha256sum -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r22-semantic-geometry-completion/inputs/frozen-inputs.sha256
node projects/laifen-wave-case/tests/test_p2_r22_source_contract.mjs
node projects/laifen-wave-case/tests/test_p2_r22_registry_contract.mjs
node projects/laifen-wave-case/tests/test_p2_r22_parameter_sensitivity.mjs
node projects/laifen-wave-case/tests/test_p2_r22_mesh_invariants.mjs
node projects/laifen-wave-case/tests/test_p2_r22_family_geometry.mjs
node projects/laifen-wave-case/tests/test_p2_r22_ui_contract.mjs
uv run --package laifen-wave-case python projects/laifen-wave-case/tests/test_p2_r22_browser.py
sha256sum -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r22-semantic-geometry-completion/candidate-files.sha256
sha256sum -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r22-semantic-geometry-completion/evidence-files.sha256
```

Results: source contract passed; registry reports `84/84` unique rows and actual indexed mesh targets; stripped positions/indices/material/transform audit reports `82/82`, with only `ends.linked` and `ventDrain.linked` inactive under exact effective-geometry equality; canonical shared seam mismatch is `0 mm`; ten indexed pattern meshes are distinct; closure, relief, drains, attachments, Basic/Advanced UI, and descriptor invalid state passed. Chromium, Firefox, and WebKit each passed desktop `1280x900` and mobile `390x844`, including pointer orbit and wheel camera/pixel deltas, fixed views, controls, nonblank canvas, overflow, errors, and requests.

## Repair record and limits

One grouped repair was used. It replaced the initial generic `semantic.*` cubes with real descriptor-driven mesh records and changed the sensitivity test to strip names, paths, metadata, and DOM text before comparison. No second repair was needed.

This remains conceptual browser evidence only. It makes no CAD, OpenSCAD, STEP/mesh export, slicer, fit, printability, physical, or live-route claim. Independent validation and visual critique are still required for this exact fingerprint.
