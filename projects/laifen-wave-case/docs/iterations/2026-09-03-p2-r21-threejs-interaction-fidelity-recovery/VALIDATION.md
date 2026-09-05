# R21 independent validation — VAL-GCS-R21-01

## Verdict

**FAIL.** The candidate is frozen correctly and its real Three.js interaction/browser layer passes in all six required contexts. It does not satisfy the R21 semantic scene contract: the 84-row map does not encode activity, most declared primary targets do not exist, 13 active controls have no actual geometry or pixel effect, the two body halves do not meet continuously at the split, and several required visual families alias or use generic substitutes.

## Frozen provenance

- Candidate manifest SHA-256: `3d2ce130e8724af9b80a7617296276c71e8d08c02b3117d94f1ad52ff004f443`
- Frozen design/input manifest SHA-256: `6d862ad3294a460da1cfdceace4e499d3fe23c809e5bb520767713cad18205df`
- Implementation evidence manifest SHA-256: `41f76a57cded945c9be3f5dd7164c29389438f5e57aeaee998ec6f533ec9f7ad`
- Every entry in all three manifests rehashed successfully before validation.

## Passing evidence

- The five prescribed cheap gates pass: source contract, descriptor boundary, scene invariants, family geometry, and UI contract.
- Scene modules accept the descriptor/plan boundary and contain no raw form-state read. No prohibited prior-renderer import, SVG proxy, random/hash visual, or string-length geometry selector was found.
- All ten required function names exist and are directly enumerated in `PATTERN_BUILDERS`; an unknown enum throws.
- Glyph width comes from pinned per-glyph metrics rather than a string-length multiplier. The OpenSCAD font remains visible DOM metadata and is not used for browser glyph geometry.
- Stripped plan/materialization signatures distinguish 10/10 pattern enums, two closure modes, four fade envelopes, four end profiles, all polygon side counts 3..32, and all five attachment modes plus `none`. Roundness-one rotation symmetry passes for 3, 4, 5, 6, 8, 12, and 32 sides.
- The independent browser matrix passes 6/6: Chromium `151.0.7922.34`, Firefox `153.0`, and WebKit `26.5`, each at `1280x900` and `390x844`. Pointer drag and wheel zoom independently change camera pose and rendered pixels; front/top/ISO move the same camera and change pixels. Preset and assembled/exploded transitions work. Invalid height clears evidence, readout, and font metadata atomically, then recovers. Basic/Advanced expose 14/27 currently active controls. No page, console, or request errors and no horizontal overflow occurred.
- The independent pixel mask found no clipping. Minimum assembled margins were 173 px desktop and 61 px mobile; exploded margins were 133 px desktop and 46 px mobile after excluding the four-pixel CSS canvas border.
- The conceptual-only disclosure remains visible in every browser context.

## Blocking findings

### Critical — 84-field semantic contract does not resolve to the scene

`scene/semantic-map.mjs` has 84 unique path rows, but none has the contract-required active condition. Literal primary-target resolution succeeds for only 16/84 rows: 68 rows name aliases such as `closure.primary`, `surface.pattern.active`, `drains.active`, `labels.active.glyph`, and `attachment.active.geometry`, none of which is an object created by `buildScenePlan`.

After stripping names, paths, readouts, and metadata, pair observability passes 69/84 directly. Treating `ends.linked` and `ventDrain.linked` as the two expected no-delta link-state cases raises this to 71/84. These 13 active fields still produce neither a materialized-evidence delta nor a rendered-pixel delta where independently probed:

- `container.floor`
- `closure.matchPatternClosed`
- `closure.screw.formHeight`
- `closure.bayonet.radialClearance`
- `surface.reliefMode`
- `surface.minWall`
- `surface.fadeMetric`
- `surface.keepout`
- `label.mode`
- `attachment.common.openingHeight`
- `attachment.common.pivotClearance`
- `attachment.common.keyringHoleDiameter`
- `attachment.common.bridgeSpan`

The semantic-map cardinality is therefore 84/84, but actual target/activity conformance is 0/84 and actual pair observability is 71/84 after the two expected inactive cases.

### Critical — the lower/upper split is not continuous

The body sampler restarts its local ring index on each half. At the common split plane, corresponding lower and upper radii differ by as much as `0.1049382 mm`. Their sampled outer-radius spans also differ: lower `30.0000018..30.5294969 mm`, upper `30.0000018..30.4387532 mm`. This fails the same-diameter/phase-continuity requirement and is consistent with `closure.matchPatternClosed` having no effect.

### High — pattern functions are named wrappers, not ten direct topology builders

All ten exported functions call one `sample(descriptor, kind, phase)` helper. Actual construction occurs later in one `surfaceLines` conditional; blunt diamond, recessed diamond, flowing flutes, rugged hex, and quilted diamond fall through to the same sine formula with only descriptor signature, phase, and color differences. The browser produces 10/10 distinct pixel hashes, but the contract requires each named builder to return its own displacement/topology plan. The inspected caption-free sheet shows colored circumferential line variants rather than the specified diamond pockets/crowns, knit loops, hex cells, and quilt cells.

### High — required visual families alias

- Relief: inset, outset, and balanced are byte-identical in both stripped evidence and canvas pixels (`1/3` unique).
- Drains: plan evidence distinguishes all four modes, but canvas pixels distinguish only `2/4`; `none` equals `bottom`, and `top` equals `both`. Source creates separate dark cylinders rather than holes in the end meshes.
- Labels: `none` differs from an active label, but inset and outset are byte-identical (`2/3` unique). The label is a zero-depth `PlaneGeometry`; descriptor glyph depth/extrusion is not materialized.

### High — active attachment dimensions are ignored

The five attachment modes themselves are visually and structurally distinct, but only 18/35 mode-by-common-field probes affect actual materialized geometry. The 17 failures are:

- eyelet: opening height, pivot clearance, keyring-hole diameter, bridge span;
- captured loop: pivot clearance, keyring-hole diameter, bridge span;
- separate clip/link: opening height, pivot clearance, keyring-hole diameter, bridge span;
- keyring tab: pivot clearance, bridge span;
- bridge handle: opening width, opening height, pivot clearance, keyring-hole diameter.

All seven common fields remain active in the UI for every non-none attachment, so these are semantic omissions rather than inactive-field cases.

## Family and browser coverage

| Gate | Result |
|---|---:|
| Semantic map rows/unique paths | 84/84 |
| Rows with active-condition contract | 0/84 |
| Declared targets resolving to actual plan objects | 16/84 |
| Observable pairs, including two expected inactive link cases | 71/84 |
| Pattern pixel/evidence families | 10/10, but topology contract fails |
| Closure pixel/evidence families | 2/2 |
| Fade pixel/evidence families | 4/4 |
| Relief pixel/evidence families | 1/3 |
| Drain pixel families | 2/4 |
| Polygon representative pixel/evidence families | 7/7 |
| End pixel/evidence families | 4/4 |
| Label mode pixel/evidence families | 2/3 |
| Attachment mode pixel/evidence families | 6/6 including none |
| Attachment common-field deltas | 18/35 |
| Browser/viewport contexts | 6/6 operational PASS |

## Commands

Run from the repository root:

```text
shasum -a 256 projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r21-threejs-interaction-fidelity-recovery/{candidate-files,evidence-files}.sha256 projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r21-threejs-interaction-fidelity-recovery/inputs/frozen-inputs.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r21-threejs-interaction-fidelity-recovery/inputs/frozen-inputs.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r21-threejs-interaction-fidelity-recovery/candidate-files.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r21-threejs-interaction-fidelity-recovery/evidence-files.sha256
node projects/laifen-wave-case/tests/test_p2_r21_source_contract.mjs
node projects/laifen-wave-case/tests/test_p2_r21_descriptor_boundary.mjs
node projects/laifen-wave-case/tests/test_p2_r21_scene_invariants.mjs
node projects/laifen-wave-case/tests/test_p2_r21_family_geometry.mjs
node projects/laifen-wave-case/tests/test_p2_r21_ui_contract.mjs
node projects/laifen-wave-case/scratch/r21-validation/independent-audit.mjs
uv run --package laifen-wave-case python projects/laifen-wave-case/scratch/r21-validation/independent-browser.py
```

The supplied browser test was not used because it writes into the frozen implementation-evidence screenshot directory. The independent equivalent writes only under `scratch/r21-validation/`.

## Acceptance boundary

This result validates only the conceptual browser candidate. It provides no CAD, OpenSCAD, export, slicer, printability, fit, strength, drainage-performance, or physical acceptance. R21 must not be promoted live on this evidence.
