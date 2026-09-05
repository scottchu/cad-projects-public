# P2 R14 semantic render adapter recovery brief

**Iteration:** `2026-09-03-p2-r14-semantic-render-adapter-recovery`  
**Design owner:** `DES-GCS-R14-REC-01`  
**Status:** frozen design contract; implementation not started  
**Rejected predecessor:** R13 candidate `9f79d2ca92c04a159ff8a79c5279dfa00fe9d0b5bb2c6f16d639be26bfc9c468`

## Outcome and baseline

Create a new R14 conceptual preview/test namespace that recovers the R13 semantic-render failure without changing the frozen R12 core, the rejected R13 candidate, or any live route. R13 produced useful visible structure, but independent validation found that many claimed field changes were generic hash witnesses, duplicate targets, or inert semantic geometry. R14 keeps the useful R13 passes and replaces the oracle with real semantic targets.

R14 is not CAD, OpenSCAD, STEP, slicer, print, MakerWorld, or physical evidence. It is a user-validation preview contract only.

## Frozen requirements

| ID | Requirement | Acceptance evidence |
| --- | --- | --- |
| R14-01 | Create only the R14 preview/test/docs/scratch namespace. Do not edit R13, R12 core/schema/derive, P2 R3 live route, CAD, OpenSCAD, STEP, slicer, printer, or continuity outside this iteration unless a later role is explicitly authorized. | pre/post path audit |
| R14-02 | Verify the R14 frozen-input manifest, then verify nested R13 candidate, implementation, validation, and critique manifests before implementation. | `shasum -a 256 -c` receipts |
| R14-03 | Renderer output must not use value hashes, effect hashes, raw-state echoes, random IDs, timestamps, or viewport-dependent semantic geometry. `.field-witness` is forbidden in source, DOM, CSS, and tests. | cheap source ban and DOM audit |
| R14-04 | Every active field has exactly one primary `[data-field-target="<canonical path>"]`. Support marks may use separate non-primary attributes, never duplicate `data-field-target`. | exact-one target gate |
| R14-05 | Each primary target class is `geometry`, `dimension-annotation`, or `metadata-badge`. The target map must declare field, class, surface, descriptor source, oracle, and allowed shared effects. | semantic target map gate |
| R14-06 | Metadata-only fields are limited to `label.openScadFontFamily`, justified because no OpenSCAD engine runs. `container.splitPercent` is a dimension annotation anchored to the seam, not metadata-only. | target-class audit |
| R14-07 | Geometry tests strip captions, text labels, metadata badges, hidden nodes, comments, and `data-*`, then measure geometry/style separately from metadata text. | stripped-geometry gates |
| R14-08 | Preserve R13's true passes: polygon side-count uniqueness, screw/bayonet topology, drain face modes, Basic/Advanced tiering, hidden-field behavior, invalid clearing, and conceptual/scale disclosure. | regression gates |
| R14-09 | Polygon rotation tests must not assert rotation deltas for circularized roundness `1`; use noncircular roundness for rotation witnesses or mark that state expected-inactive. | polygon oracle gate |
| R14-10 | Blunt and recessed diamond/relief families must differ in stripped geometry, not only color, caption, metadata, or witness marks. | paired stripped-family gate |
| R14-11 | All ten surface families plus envelope/fade/relief modes must be visibly distinct in geometry on a shared review area and in human-visible category sheets. | family uniqueness and sheet review |
| R14-12 | End and attachment views must be scaled and anchored so profile, mode, half, angle, opening, member, hole, bridge, clearance, and standoff changes are readable without captions. | dimension-target and UX capture gates |
| R14-13 | Cheap gates run before browser: source ban, target map, exact-one target, stripped-geometry observability, polygon, family, tier, disclosure, determinism, and invalid clearing. | ordered command receipt |
| R14-14 | Chromium, Firefox, and WebKit must pass at desktop `1280x900` and mobile `390x844` with no page errors, overflow, hidden-field focus, target loss, stale invalid output, or family alias. | six-context browser evidence |
| R14-15 | Initial implementation plus at most two focused repair cycles. Any candidate mutation changes the fingerprint and invalidates affected independent gates. | retry ledger |
| R14-16 | No live route, served copy, delivery, or user-facing handoff begins until independent VAL, independent CRIT, and formal REV all PASS the same candidate fingerprint. | formal review join |

## Exact implementation scope

Implementation may create or edit only:

- `projects/laifen-wave-case/preview/p2-r14-semantic-render-adapter-recovery/**`
- `projects/laifen-wave-case/tests/test_p2_r14_target_contract.mjs`
- `projects/laifen-wave-case/tests/test_p2_r14_render_observability.mjs`
- `projects/laifen-wave-case/tests/test_p2_r14_visual_families.mjs`
- `projects/laifen-wave-case/tests/test_p2_r14_ui_contract.mjs`
- `projects/laifen-wave-case/tests/test_p2_r14_browser.py`
- `projects/laifen-wave-case/scratch/r14-*/**`
- R14 role receipts and manifests under this iteration directory

The R14 app may import the frozen R12 schema, presets, parameter coverage, utilities, and `derive` read-only. It may copy R13 preview ideas into the new R14 namespace, but it must not modify R13 files. Renderer modules must consume descriptors or target-map entries; they must not become new schema or raw-state authorities.

## Ordered DAG and stop rules

| Task | Owner/role | Dependency | Deliverable / done gate | Stop |
| --- | --- | --- | --- | --- |
| IMP-GCS-R14-01A | implementation, cheap gates first | R14 design fingerprint and verified R13/R12 manifests | R14 target map, source-ban test, exact-one target test, stripped-geometry oracle harness | stop on manifest mismatch, descriptor gap, hash witness, duplicate target, or scope expansion |
| IMP-GCS-R14-01B | implementation, renderer | 01A PASS | R14 adapter preserving useful R13 geometry while making all active targets semantic | stop before browser on any cheap gate fail |
| IMP-GCS-R14-01C | implementation, browser sheets | 01B PASS | desktop/mobile category sheets and six-context browser PASS; frozen candidate manifest | stop on overflow, hidden focus, stale invalid output, target loss, alias, or retry exhaustion |
| VAL-GCS-R14-01 | independent validator | exact R14 candidate | read-only manifest verification, independent stripped-geometry 84-row audit, polygon/family/tier/browser rerun | PASS required |
| CRIT-GCS-R14-01 | independent critic | same candidate | human-visible desktop/mobile category-sheet critique focused on recognition | PASS required |
| REV-GCS-R14-01 | formal reviewer | candidate plus VAL and CRIT | provenance, scope, requirement traceability, findings disposition, final join | PASS only if VAL and CRIT PASS |

No later gate may waive an earlier cheap failure. A proven descriptor gap stops implementation and requires a separately refrozen contract; it is not permission to edit core schema or derive.

