# Foundation V1 implementation receipt

**Owner and role:** `IMP-GCS-FV1-01`, implementation only  
**Status:** candidate frozen; awaiting independent validation and visual critique  
**Frozen design fingerprint:** `46a37b6d61973c8b3287b67fa5b3c91b9df515e04e7f332c27cda6ab1edcb024`  
**Accepted gate fingerprint:** `535ec0f9eb5bce77c409c12576ab4b9bdf2b66b930a6a477d22276f46d659dfa`  
**Candidate manifest SHA-256:** `1f4caa5befa635f5a31ee1933b220a02572d6e685183960819e30af0479866a6`  
**Evidence manifest SHA-256:** `4be67f810e87678fbc562559ff8cab56dc55e41160a572855856267ef3936702`

## Scope and implementation

All 15 frozen inputs verified with `shasum -a 256 -c .../inputs/frozen-inputs.sha256` before writing. The candidate is a new `preview/p2-foundation-v1/` real Three.js application. `deriveV1(inputs)` is the only form-state boundary; it freezes a serializable V1 descriptor consumed by the scene and readout.

The scene has indexed lower and upper hollow shell meshes, independent actual end geometry, descriptor-based mating helical thread surfaces, selected-floor hole geometry, same-OD seam, and assembled/exploded transforms. The viewport supplies orbit, pan, zoom, reset, open-mouth, and clipping-plane cutaway inspection. The UI contains only the accepted V1 controls and derived readout, with invalid input clearing its descriptor and scene model.

Changed candidate paths are all entries in `candidate-files.sha256`: six V1 source files and the four prescribed focused tests. Evidence is limited to the manifest, four command logs, compact mesh facts, and eight current Chromium desktop/mobile screenshots under `scratch/p2-foundation-v1-implementation/`.

## Validation run by implementer

The following commands were run from the repository root; their exact success output is retained in the evidence directory.

```sh
node projects/laifen-wave-case/tests/test_p2_foundation_v1_derive.mjs
node projects/laifen-wave-case/tests/test_p2_foundation_v1_source_contract.mjs
node projects/laifen-wave-case/tests/test_p2_foundation_v1_scene.mjs
uv run python projects/laifen-wave-case/tests/test_p2_foundation_v1_browser.py
```

All passed. The browser test exercised Chromium, Firefox, and WebKit at `1280x900` and `390x844`; it checks real control-driven changes, invalid recovery with a cleared descriptor, all inspection views, keyboard reset, pointer orbit, wheel zoom, and the exact V1 disclosure. It wrote `desktop-{assembled,open,exploded,cutaway}.png` and `mobile-{assembled,open,exploded,cutaway}.png`.

## Requirement coverage

| Requirement | Implementation evidence |
| --- | --- |
| `FV1-DERIVE`, `FV1-BOUNDARY` | derivation and source-contract tests |
| `FV1-BODY`, `FV1-SCREW`, `FV1-END-DRAIN` | indexed geometry/sensitivity scene test and `mesh-facts.json` |
| `FV1-VIEW`, `FV1-UI` | cross-browser interaction test and desktop/mobile screenshots |
| `FV1-SCOPE` | source-contract test and candidate manifest |

## Focused repair count and limits

One focused repair was made during the initial attempt: Three.js extruded floor geometry can be non-indexed, so the geometry builder normalizes it to indexed geometry before merging/materialization. All cheap gates were rerun afterwards. No other repair cycle was used.

This is only a conceptual, dimensionally proportional preview. It has no CAD, printability, thread-fit, strength, drainage-performance, export, slicer, or physical-acceptance evidence. The implementation role has not independently validated, critiqued, reviewed, served, or promoted this candidate. Next action is read-only `VAL-GCS-FV1-01` and `CRIT-GCS-FV1-01` against this exact candidate manifest.
