# P2 R16 final semantic mapping recovery brief

**Iteration:** `2026-09-03-p2-r16-final-semantic-mapping-recovery`  
**Design owner:** `DES-GCS-R16-REC-01`  
**Status:** frozen design contract; implementation not started  
**Stopped predecessor:** R15 frozen fingerprint `550dfb50af2b9ea950471d114ac9485a9ec507742225e6dcb80c219f88b15301`

## Outcome and baseline

R16 is the final narrow semantic-mapping recovery over R15. R15 stopped before browser work with source-ban/exact-one gates passing and a collecting audit at **70/84 PASS**. The repair set is exactly 14 fields. There is no authorization to redesign the 70 passing mappings or to touch prior iterations, core derivation, live routes, or CAD/export/physical layers.

R16 is conceptual browser-preview evidence only and cannot make CAD, OpenSCAD, STEP/export, slicer, printability, fit, drainage-performance, physical, MakerWorld, publication, live-route, or delivery claims.

## Frozen requirements

| ID | Requirement | Acceptance evidence |
| --- | --- | --- |
| R16-01 | Work only in the new R16 preview/test/docs/scratch namespace. R15/R14/R13, frozen R12 core/schema/derive, live routes, CAD, OpenSCAD, STEP, slicer, printer, physical, and unrelated files are read-only. | pre/post path audit |
| R16-02 | Verify R15 frozen fingerprint `550dfb50af2b9ea950471d114ac9485a9ec507742225e6dcb80c219f88b15301` and R16 frozen inputs before implementation. | hash receipts |
| R16-03 | Freeze R15 contract, noncandidate receipt, current collecting audit, R15 source/tests, and the reproduced 70/84 residual list as the baseline. | frozen-input manifest and command receipt |
| R16-04 | Preserve the 70 passing semantic mappings. Do not use a broad rewrite that invalidates unrelated passing fields unless the full collecting audit remains 84/84. | collecting audit |
| R16-05 | Preserve source ban and target discipline: no `.field-witness`, no value-hash-driven geometry/color/text, no raw/effect hash badges, no random/timestamp semantic output, exactly one primary target per active field, 0 duplicates, 0 unexpected inactive targets. | source-ban and exact-one gates |
| R16-06 | Repair exactly the residual 14 fields listed below with geometry or anchored dimension annotations, except `label.openScadFontFamily`, which remains truthful metadata. | target-map and collecting audit |
| R16-07 | Full collecting audit must be **84/84 PASS** and <= 1 MB before browser, category sheets, screenshots, candidate freeze, or delivery work. | audit result and size check |
| R16-08 | After cheap PASS, create human-visible category sheets, then run Chromium, Firefox, and WebKit at desktop `1280x900` and mobile `390x844`. | sheet and six-context evidence |
| R16-09 | Initial implementation plus at most two full-group repair cycles. Each cycle repairs the complete current residual list, not one field at a time. | retry ledger |
| R16-10 | No live route, served copy, or user-facing delivery before independent VAL, independent CRIT, and formal REV all PASS the same R16 candidate fingerprint. | formal review join |

## Exact residual map

| Field | Required target class | Fix requirement |
| --- | --- | --- |
| `container.sideCount` | geometry | Polygon-only section geometry changes vertex/facet count; no caption, text, or dimension-only pass. |
| `closure.screw.radialClearance` | dimension-annotation | Gap band between screw profiles and anchored radial dimension both change. |
| `closure.bayonet.radialClearance` | dimension-annotation | Lug/channel clearance band and anchored radial dimension both change. |
| `surface.reliefMode` | geometry | Inset/outset/balanced cross-section changes actual relief placement about the wall. |
| `surface.minWall` | dimension-annotation | Residual-wall gauge and measured wall feature move with descriptor minimum wall. |
| `surface.fadeMetric` | geometry | Depth fade changes relief amplitude while density fade changes motif count/spacing; stripped geometry differs. |
| `surface.keepout` | geometry | Smooth seam/end exclusion regions change actual visible patterned-area bounds. |
| `label.mode` | geometry | None/inset/outset changes actual label relief/engrave geometry. |
| `label.openScadFontFamily` | metadata-badge | Visible metadata badge truthfully varies with descriptor value; it remains the only metadata target. |
| `label.orientation` | geometry | Actual glyph/proxy geometry rotates horizontal versus vertical. |
| `label.target` | geometry | Label geometry moves to lower, upper, or both body regions. |
| `label.axialFromTargetEnd` | dimension-annotation | Label position and anchored axial dimension move from the selected target end. |
| `label.patchMargin` | dimension-annotation | Patch geometry and local margin bracket change together. |
| `attachment.attachHalf` | geometry | Actual attachment geometry moves between lower and upper body regions. |

## Exact implementation scope

Implementation may create or edit only:

- `projects/laifen-wave-case/preview/p2-r16-final-semantic-mapping-recovery/**`
- `projects/laifen-wave-case/tests/test_p2_r16_target_contract.mjs`
- `projects/laifen-wave-case/tests/test_p2_r16_render_observability.mjs`
- `projects/laifen-wave-case/tests/test_p2_r16_visual_families.mjs`
- `projects/laifen-wave-case/tests/test_p2_r16_ui_contract.mjs`
- `projects/laifen-wave-case/tests/test_p2_r16_browser.py`
- `projects/laifen-wave-case/scratch/r16-*/**`
- R16 role receipts and manifests under this iteration directory

R16 may copy R15 source into the R16 namespace as a starting point, but R15 remains immutable input. R16 may import frozen R12 core read-only.

## DAG and stop rules

| Task | Owner/role | Dependency | Done gate | Stop |
| --- | --- | --- | --- | --- |
| IMP-GCS-R16-01A | implementation, residual semantic repair | R16 design fingerprint and verified inputs | R16 namespace, source ban, exact-one gate, complete 14-field repair, collecting audit 84/84 <=1 MB | stop on prior/core/live/CAD edit, source-ban fail, duplicate/inactive target, hash witness, or <84/84 after repair ceiling |
| IMP-GCS-R16-01B | implementation, visual/browser | 01A PASS | category sheets and six browser contexts PASS; candidate manifest frozen | stop on sheet unreadability, browser error, overflow, hidden focus, target loss, or stale invalid output |
| VAL-GCS-R16-01 | independent validator | exact candidate | read-only hash/scope verification and independent 84/84 rerun | PASS required |
| CRIT-GCS-R16-01 | independent critic | same candidate | human sheet and desktop/mobile recognition critique | PASS required |
| REV-GCS-R16-01 | formal reviewer | candidate plus VAL and CRIT | provenance, scope, requirement coverage, and findings join | PASS only if VAL and CRIT PASS |

No browser/category-sheet work can start until the full collecting audit is 84/84 and <= 1 MB.

