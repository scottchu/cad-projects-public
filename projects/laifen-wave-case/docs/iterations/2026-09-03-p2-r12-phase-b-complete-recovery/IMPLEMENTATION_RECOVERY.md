# IMP-GCS-R12-REC-01 implementation recovery

**Status:** implementation PASS; candidate frozen for independent validation, critique, and formal review. This receipt does not grant acceptance.

## Provenance and scope

- R12 frozen input manifest passed before edits: `frozen-inputs.sha256` validated the partial R10 core, exact Phase A/B tests, R11 audit inputs, and R12 intake.
- Frozen design fingerprint: `54a5623e9bbf4b391eebf5aaac803ac52ea386c58b84395368061adb4e106f3a`.
- Candidate manifest fingerprint: `51727da73c72db6e391f4f83014a54076dc2ffbdc5bc617f753c72a8fc1a2221`.
- Edits before Phase C were only `core/parameter-coverage.mjs` and `core/derive.mjs`. Phase C then created the permitted R10 renderer/UI and renderer/browser tests. No R6–R9 source, live route/service, CAD, OpenSCAD, STEP, slicer, print, or continuity record was changed.

## Recovered Phase B

- Direction witnesses use valid signed `+1/-1` pairs.
- Flow amplitude and quilt edge softness affect sampled geometry signatures; quilt rotation is consumed only by the quilt sampler.
- Flat-end sizes are normalized to zero before validation when the selected profile is flat.
- Render-ready label glyph data contains size and OpenSCAD font-family disclosure.
- Attachment mode coverage compares distinct valid modes and descriptor primitives/bounds encode mode identity.
- `splitPercent` remains a projection-only special case whose witness changes canonical split millimetres.

The R12 exhaustive audit records **84/84 PASS**, projection special **PASS**, and **58/58 inactive poison PASS** in `scratch/r12-phase-b-audit/`.

## Phase C implementation and validation

The R10 namespace now supplies a descriptor-only SVG renderer, dynamic Basic/Advanced control UI, accessible invalid-state clearing, named target groups, comparison/detail views, and visual-only copy. Renderer source imports no state, schema, validator, or geometry authority.

Executed commands, all passing:

```sh
node projects/laifen-wave-case/tests/test_p2_r10_schema_coverage.mjs
node projects/laifen-wave-case/tests/test_p2_r10_geometry.mjs
node projects/laifen-wave-case/tests/test_p2_r10_descriptor_sensitivity.mjs
node projects/laifen-wave-case/tests/test_p2_r10_renderer.mjs
node projects/laifen-wave-case/scratch/r12-phase-b-audit/audit.mjs
uv run --package laifen-wave-case python projects/laifen-wave-case/tests/test_p2_r10_browser.py
```

The browser test passed Chromium, Firefox, and WebKit at 1280×900 and 390×844, including named active targets and invalid-state clearing. A separate same-engine desktop/mobile check found no page overflow or page errors.

## Retry accounting and next action

Phase B used two focused repairs: a syntax correction followed by directional helix sampling. Phase C used two focused browser-test repairs: target-count semantics and reusable local test-server binding. Both phases finished within their stated ceilings.

Independent VAL and CRIT must verify candidate `51727…2221`; REV must join their receipts before any delivery activity. CAD, artifact, slicer, physical, and MakerWorld acceptance remain out of scope and unproven.
