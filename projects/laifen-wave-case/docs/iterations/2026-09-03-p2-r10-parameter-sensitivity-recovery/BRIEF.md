# P2 R10 parameter-sensitivity recovery brief

**Iteration:** `2026-09-03-p2-r10-parameter-sensitivity-recovery`  
**Design owner:** `DES-GCS-R10-02`  
**Status:** frozen recovery contract; implementation has not started  
**Failed predecessor:** R9 source fingerprint `d7cf4cb3c72aa012b1ad4be5f9e096023b51c51ed79ea60c0f5587ea37816eab`, independent `FAIL` + `BLOCK`

## Outcome

Build a descriptor-first browser intent model in `preview/p2-r10-parameter-sensitivity-recovery/`. Pure functions validate and derive a complete serializable visual descriptor. The renderer receives that descriptor alone. A machine-readable coverage map makes every visible parameter accountable to a derived property, a two-state sensitivity oracle, one visibility predicate, one SVG evidence target, and one future OpenSCAD flatten name.

## Requirements

| ID | Frozen requirement | Acceptance evidence |
| --- | --- | --- |
| R10-01 | Create only the new R10 source/test/evidence namespace; preserve R6–R9, P1 R7, and the live P2 R3 route/service. | scope and protected-hash checks |
| R10-02 | Keep the seven model groups Container, Closure, Ends, Surface, Vent & Drain, Label, Attachment. Add the R8 `surface.keepout` field omitted by R9. | schema inventory |
| R10-03 | Every schema record has nonempty label, help, unit, bounds, default, type, Basic/Advanced tier, visibility AST, derivation pointer, oracle, render target, and unique explicit flatten name. | coverage-schema equality test |
| R10-04 | Basic/Advanced grouping and all conditional visibility are exactly those in `DESIGN.md`. Inactive values are stored but ignored by validation, derivation, and rendering. | active-field matrix and poison tests |
| R10-05 | `derive(state)` returns exactly `{valid:false, errors, descriptor:null}` or `{valid:true, errors:[], descriptor}`. A valid descriptor is complete, deeply immutable, finite, and JSON-round-trippable. | result-shape and serialization tests |
| R10-06 | Renderer modules accept only a descriptor and serialize its ready primitives/annotations. They cannot import schema, presets, raw state, validators, geometry math, or pattern math. | import/static guard plus spy descriptor |
| R10-07 | Each active field changes its declared non-echo descriptor subtree and its named accessible SVG target under the prescribed valid A/B oracle. Generic raw-state echo cannot satisfy sensitivity. | full parameter delta matrix |
| R10-08 | Presets are immutable deep override patches. Every R8 shared field equals the frozen R8 preset value; derived E/P/K/split facts match. Split mm and percent are synchronized projections of one canonical millimetre value. | exact parity/projection fixtures |
| R10-09 | Rounded regular polygons use OD as maximum across corners; sides, roundness, and rotation each change sampled support at valid witnesses. | analytic extrema and sensitivity |
| R10-10 | Flat, chamfer, fillet, and spherical dome use unique pure meridian paths, profile-specific bounds, and same-scale comparison silhouettes. | curvature/path/bound tests and browser sheet |
| R10-11 | Screw proxy consumes pitch, 1/2/3 turns, lead/runout, form height, and clearance. Bayonet consumes lock angle, lug count, capture, ramp rise, and clearance. | per-field descriptor/SVG deltas |
| R10-12 | In assembled bayonet view both core pieces remain coaxial and axial. Shape alignment is unconditional; selected closed pattern phase aligns by the shared world/local transform. | plan + side transform oracle |
| R10-13 | Every surface has one distinct finite pure sampler and declared exact raw range. Knit, flowing, wave, soft wide helix, quilt, fade metric, envelope, relief, and keepout cannot alias or crash. | sampled-signature, periodicity, boundary, poison tests |
| R10-14 | Relief placement derives actual inset depth, outset height, datum/base OD, crest OD, minimum residual wall, and total envelope from the sampler range. | independent formula oracle |
| R10-15 | Labels are outward-readable and consume mode, safe text, angle, orientation, preview font, OpenSCAD-family disclosure, weight, size, target, axial position, relief, patch, and margin. Each target gets independent seam/end/closure/surface/attachment checks. | frame, safe-policy, collision, target and SVG tests |
| R10-16 | Drains create unique pure positions; count one is centered with radius zero; edge/pair/profile/attachment checks run per active end. SVG end faces use actual masks with holes for none/top/bottom/both. | analytic positions and DOM mask assertions |
| R10-17 | Every accessory has unique primitives and attachment semantics. Every active dimension changes its primitive data and computed bounds/envelope. | five mode matrices and bound parity |
| R10-18 | Invalid active input clears main/detail/comparison/readouts/envelopes and exposes linked accessible errors. Invalid inactive plugin values have no effect until activation. | transactional browser tests |
| R10-19 | UI copy uses “dimensionally proportional visual” and states that pixels are fit-to-view, not calibrated. The phrase “true scale” is absent. | source and browser text assertion |
| R10-20 | Named SVG groups and annotations support browser assertions; each parameter oracle records descriptor hash and canonical target-subtree hash. | Chromium/Firefox/WebKit evidence |
| R10-21 | No registry validator may be a no-op. Every validator has a nominal witness and a failing boundary witness that disappears when its plugin is inactive. | validator mutation/witness test |
| R10-22 | Implement pure functions and tests first, then descriptor snapshots/sensitivity, then renderer, then browser matrix. A failed cheap gate stops downstream work. | ordered receipt and command log |
| R10-23 | Preserve visual-only boundaries; make no OpenSCAD, CAD, STEP/export, slicer, print, fit, drainage, physical, or MakerWorld claim. | copy/scope review |

## Exact implementation paths

Implementation may create only:

- `projects/laifen-wave-case/preview/p2-r10-parameter-sensitivity-recovery/**`
- `projects/laifen-wave-case/tests/test_p2_r10_schema_coverage.mjs`
- `projects/laifen-wave-case/tests/test_p2_r10_geometry.mjs`
- `projects/laifen-wave-case/tests/test_p2_r10_descriptor_sensitivity.mjs`
- `projects/laifen-wave-case/tests/test_p2_r10_renderer.mjs`
- `projects/laifen-wave-case/tests/test_p2_r10_browser.py`
- R10 role receipts/manifests and role-owned `projects/laifen-wave-case/scratch/r10-*/**`

No implementation path may be substituted or silently added. Tests are production-independent oracles: they may import public pure functions and descriptor/renderer entrypoints, but cannot copy production formulas wholesale or pass through source-text presence alone.

## Ordered task DAG and ceilings

| Task | Distinct owner and role | Dependency | Deliverable and done gate | Ceiling / stop |
| --- | --- | --- | --- | --- |
| IMP-GCS-R10-01A | implementation owner, pure model | R10 fingerprint | schema, predicates, presets, math, validators, first two tests | balanced/medium; initial + 2 repairs; stop on any cheap failure |
| IMP-GCS-R10-01B | same implementation workstream, descriptor | 01A PASS | `derive(state)`, descriptor snapshots, complete coverage/sensitivity test | balanced/medium; no renderer until all 83 fields and projections pass |
| IMP-GCS-R10-01C | same implementation workstream, renderer/UI | 01B PASS | descriptor-only SVG/UI and renderer/browser tests; frozen candidate | balanced/medium; no source outside namespace |
| VAL-GCS-R10-01 | independent validator, never IMP/CRIT | exact frozen candidate | deterministic, mutation, browser and accessibility receipt/evidence | strong/high; initial + 2 method repairs |
| CRIT-GCS-R10-01 | independent visual critic, never IMP/VAL | same candidate | recognition/comprehension receipt/evidence | strong/high; initial + 2 focused checks |
| REV-GCS-R10-01 | independent formal reviewer | exact candidate + VAL + CRIT | provenance join and requirement disposition | strong/high; PASS only if both independent gates pass |
| DEL-GCS-R10-01 | independent delivery packager | formal PASS | byte-pinned static package and receipt only | fast/low; no route/service action without separate authorization |

The implementation workstream gets one initial attempt and at most two focused repair cycles. If any material field family still fails after that ceiling, reopen the contract and reduce the active feature set; do not add another patch layer. A reduced candidate must hide and omit postponed controls rather than expose inert ones.

## Recovery disposition of every R9 independent finding

R10 must close all R9 VAL findings V01–V08 and CRIT P1 findings CR9-01–03, not merely reproduce visible controls. The descriptor/coverage contract in `DESIGN.md` binds: R9 schema/help/export/preset drift to schema metadata and exact parity fixtures; section/scale to support and camera descriptor oracles; closure/topology to coaxial side primitives plus separate phase annotations; patterns/fade/relief to distinct sampled signatures consumed by the renderer; labels to safe policy/frames/collision/patch primitives; drains to unique subtractive face masks; accessories to primitive/bounds parity; invalid state to descriptor-null. Critique-specific end comparison cards and pattern/fade adapter identities are named descriptor/SVG targets. A candidate that passes a raw-state or DOM-presence assertion without the declared descriptor and visual-target delta fails R10-07.
