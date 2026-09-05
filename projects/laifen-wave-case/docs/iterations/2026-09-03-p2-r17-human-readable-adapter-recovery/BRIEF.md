# P2 R17 human-readable adapter recovery brief

**Iteration:** `2026-09-03-p2-r17-human-readable-adapter-recovery`  
**Design owner:** `DES-GCS-R17-01`  
**Status:** frozen design contract; implementation not started  
**Rejected predecessor:** R16 candidate `14b625606e1abd2a705d1874b557d9a9ba9ad6cc368d306de5d42417c8362a5e`

## Outcome and baseline

R17 is a narrow semantic and human-readable adapter recovery over R16. R16 achieved 84/84 in its prescribed cheap audit and passed prescribed browser tests, but independent validation failed on stricter target-class, family-alias, descriptor-source, and browser-bounding-box checks. Independent critique also blocked the surface, label, and attachment cards as too caption-dependent or crowded. R17 fixes only those blockers and preserves all other R16 passes.

R17 is conceptual browser-preview evidence only. It grants no CAD, OpenSCAD, STEP/export, slicer, printability, fit, drainage-performance, physical, MakerWorld, publication, live-route, served-copy, or delivery acceptance.

## Frozen requirements

| ID | Requirement | Acceptance evidence |
| --- | --- | --- |
| R17-01 | Work only in the R17 preview/test/docs/scratch namespace. R16 and prior iterations, frozen R12 core/schema/derive, live routes, CAD, OpenSCAD, STEP, slicer, printer, physical, and unrelated files are read-only. | pre/post path audit |
| R17-02 | Freeze exact R16 candidate `14b625606e1abd2a705d1874b557d9a9ba9ad6cc368d306de5d42417c8362a5e`, implementation evidence, independent validation, independent critique, and their manifests. | frozen-input manifest |
| R17-03 | Preserve all R16 passes not named as blockers: source ban, exact-one targets, 84/84 active field coverage, no duplicate/inactive leaks, metadata-only OpenSCAD font, polygon 30/30, closure/end/envelope/relief/label-mode/attachment/drain topology, tiering, invalid clearing, disclosure, and six prescribed browser contexts. | regression and independent-style audit |
| R17-04 | Keep hash/witness ban: no `.field-witness`, generic witness grids, value-hash-driven geometry/color/text, raw/effect hash badges, random/timestamp semantic output, or renderer-side schema/derive authority. | source ban |
| R17-05 | Correct the four dimension targets: `container.rotationDeg`, `surface.flute.waveWavelength`, `surface.spiral.pitch`, and `attachment.mountAngleDeg` must include feature-anchored dimension geometry, not only geometry deltas. | target-class audit |
| R17-06 | Correct the nine invalid `descriptor.body` target-map source paths to existing descriptor leaves. This is declaration repair only; no descriptor gap exists. | descriptor-source audit |
| R17-07 | Distinguish stripped surface pattern aliases: `blunt_diamond` vs `shallow_helix`, and `knit_stitch` vs `wave_flutes`. Do not dispatch by enum-name length. | stripped family audit |
| R17-08 | Distinguish stripped drain modes `bottom` and `top` by end identity and hole placement geometry. | stripped family audit |
| R17-09 | Ensure nonzero browser bounding boxes for `ends.bottom.profile`, `label.mode`, and `attachment.mode` in Chromium, Firefox, and WebKit at `1280x900` and `390x844`. | strict six-context bbox audit |
| R17-10 | Surface, labels, and attachments must be human-readable without captions or overlap. The cards may use local teaching geometry and spacing, but must stay truthful to the descriptor. | human category sheets and critique |
| R17-11 | Separate the OpenSCAD font metadata banner from active label geometry. It remains truthful metadata only and must not dominate or occlude label geometry. | DOM/visual audit |
| R17-12 | Run full independent-style semantic, family, descriptor-source, and bbox audit before candidate freeze; then run strict six-context browser gate. | ordered receipt |
| R17-13 | Initial implementation plus at most two grouped repair cycles. Each cycle addresses all remaining blocker groups from the latest audit. | retry ledger |
| R17-14 | No live route, served copy, delivery, or user-facing handoff until independent VAL, independent CRIT, and formal REV all PASS the same R17 candidate fingerprint. | formal review join |

## Exact implementation scope

Implementation may create or edit only:

- `projects/laifen-wave-case/preview/p2-r17-human-readable-adapter-recovery/**`
- `projects/laifen-wave-case/tests/test_p2_r17_target_contract.mjs`
- `projects/laifen-wave-case/tests/test_p2_r17_render_observability.mjs`
- `projects/laifen-wave-case/tests/test_p2_r17_visual_families.mjs`
- `projects/laifen-wave-case/tests/test_p2_r17_ui_contract.mjs`
- `projects/laifen-wave-case/tests/test_p2_r17_browser.py`
- `projects/laifen-wave-case/scratch/r17-*/**`
- R17 role receipts and manifests under this iteration directory

R17 may copy R16 source into the new namespace as a starting point. R16 candidate files and evidence are immutable input. Frozen R12 core may be imported read-only.

## DAG and stop rules

| Task | Owner/role | Dependency | Done gate | Stop |
| --- | --- | --- | --- | --- |
| IMP-GCS-R17-01A | implementation, blocker repair | R17 design fingerprint and verified R16 inputs | R17 namespace, source ban, exact-one target pass, four dimension fixes, nine descriptor-source fixes, pattern/drain alias fixes, nonzero target geometry fixes | stop on scope expansion, prior/core/live/CAD edit, hash/witness mechanism, duplicate/inactive target, or descriptor-gap claim |
| IMP-GCS-R17-01B | implementation, independent-style audit/browser | 01A PASS | full independent-style audit PASS, strict six-context bbox/browser PASS, human category sheets, candidate manifest | stop on any blocker recurrence, browser error, overflow, hidden focus, zero bbox, overlap, or retry exhaustion |
| VAL-GCS-R17-01 | independent validator | exact R17 candidate | read-only manifest verification and independent rerun of semantic/family/source/bbox/browser gates | PASS required |
| CRIT-GCS-R17-01 | independent critic | same candidate | human clarity review of surface, labels, attachments, plus preserved categories | PASS required |
| REV-GCS-R17-01 | formal reviewer | candidate plus VAL and CRIT | provenance, scope, requirement traceability, and findings-disposition join | PASS only if VAL and CRIT PASS |

No candidate may be frozen until the independent-style audit and strict six-context bbox/browser gate both pass.

