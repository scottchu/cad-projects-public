# R20 independent validation — VAL-GCS-R20-01

## Verdict

**FAIL.** The frozen candidate and implementation-evidence fingerprints match, and the prescribed static/recipe gates pass, but the candidate violates the R20 source contract and the required six-context browser matrix was not completed. The recipe-level 84/84 result therefore does not establish actual WebGL observability for all 84 fields.

## Frozen provenance

- Candidate manifest SHA-256: `ae45f4e28fd6c34b09c56c34a4d55eb0bed7620f101559e028aa31d12fd98ad4`
- Implementation evidence manifest SHA-256: `05f2f3b1e722e2b8027a8e098d8903bb7458a37a5111ed1e65c6859c46941187`
- Frozen-input manifest SHA-256: `d2097cf93f9ee295dfe86fa687c6cfa5f698890ff089027dbebadc4ffdcd2378`
- Every listed file in all three manifests rehashed successfully before validation.

## Independent results

The following frozen tests/audits passed:

- `test_p2_r20_source_contract.mjs`: 12 source files and 168 active pair mappings.
- `test_p2_r20_scene_invariants.mjs`: PASS.
- `test_p2_r20_family_geometry.mjs`: PASS.
- `test_p2_r20_ui_contract.mjs`: PASS.
- supplied compact independent style audit: coverage 84/84, source hits 0.
- validator recipe audit: 84/84 pair deltas pass after applying the two declared inactive cases (`ends.linked`, `ventDrain.linked`).
- validator family checks: 10/10 pattern recipe signatures distinct; polygon side counts 3..32 yield 30/30 distinct signatures; roundness-one rotation symmetry passes 7/7; lower and upper bodies each have 912 sampled vertices and matching seam points; four end profiles and four drain modes produce their expected recipe families.
- The compact validator audit is below the 1 MB evidence ceiling.

Source inspection confirms real Three.js imports (`three` plus a `0.160.1` import map), with no import of the prior renderer/semantic map, no SVG main-scene proxy, and no crypto/hash/random/timestamp/effect-digest witness in candidate source.

## Blocking findings

1. **Banned string-derived geometry exists.** `scene/build-scene.mjs` sizes label planes with `label.size * label.text.length * .62` and patch planes with `l.size * l.text.length * .72`. R20 explicitly bans label/string length as a geometry selector. These are hidden generic witnesses even though they are attached to visible Three.js meshes.

2. **The scene builder is not descriptor-only.** `semanticRecipe(descriptor, state)` and `buildScene(descriptor, state, ...)` consume raw state throughout geometry construction. The selected R20 architecture requires the WebGL scene to be built from the canonical descriptor plus presentation options.

3. **The ten explicit pattern builders are absent.** None of `buildSmoothSurface`, `buildBluntDiamondSurface`, `buildRecessedDiamondSurface`, `buildKnitStitchSurface`, `buildStraightMicroFlutesSurface`, `buildFlowingFlutesSurface`, `buildRuggedHexSurface`, `buildShallowHelixSurface`, `buildWaveFlutesSurface`, or `buildQuiltedDiamondSurface` exists. Pattern behavior is routed through one conditional displacement function, so the named source-level pattern contract is unmet despite ten distinct sampled recipe signatures.

4. **The six-context browser acceptance gate is unproven.** The independent harness exercised the complete representative control sequence in Chromium desktop and produced three caption-hidden WebGL screenshots, then stopped during the fourth screenshot setup because selecting `chamfer` transiently makes the existing zero size invalid before the size control is set. The run ended before emitting its context receipt, invalid-clearing result, or any Firefox/WebKit/mobile result. Consequently zero of the required six contexts can be accepted from this run. The three screenshots are partial evidence only.

5. **Actual WebGL field coverage remains materially uncertain.** Source inspection shows recipe-only names which are not attached to the scene evidence, including `body.split.percent.annotation`, `closure.matchPatternClosed`, `surface.fade.*`, end-size annotations, label-angle annotations, and several attachment annotations. `metadata.openscadFont.value` is present in the recipe, but its value is not exposed by scene evidence and no OpenSCAD font value is rendered in the DOM. All non-none attachment modes instantiate the same torus family, while `pivotClearance`, `keyringHoleDiameter`, and `bridgeSpan` are listed as paths without participating in that geometry. These gaps require actual scene-object evidence, not recipe hashes, before the 84-field gate can pass.

## Commands

Run from repository root:

```text
shasum -a 256 projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r20-real-threejs-generator/{candidate-files,evidence-files}.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r20-real-threejs-generator/{candidate-files,evidence-files}.sha256
node projects/laifen-wave-case/tests/test_p2_r20_source_contract.mjs
node projects/laifen-wave-case/tests/test_p2_r20_scene_invariants.mjs
node projects/laifen-wave-case/tests/test_p2_r20_family_geometry.mjs
node projects/laifen-wave-case/tests/test_p2_r20_ui_contract.mjs
node projects/laifen-wave-case/scratch/r20-independent-style-audit/audit.mjs
node projects/laifen-wave-case/scratch/r20-validation/independent-audit.mjs
uv run --package laifen-wave-case python projects/laifen-wave-case/scratch/r20-validation/independent-browser.py
```

The final browser command did not complete and is recorded as a failed validation gate. No candidate, test, live, CAD, OpenSCAD, slicer, core, or continuity file was edited.
