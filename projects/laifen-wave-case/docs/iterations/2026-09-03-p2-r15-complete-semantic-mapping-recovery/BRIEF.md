# P2 R15 complete semantic mapping recovery brief

**Iteration:** `2026-09-03-p2-r15-complete-semantic-mapping-recovery`  
**Design owner:** `DES-GCS-R15-01`  
**Status:** frozen design contract; implementation not started  
**Stopped predecessor:** R14 frozen fingerprint `ff0f85197408ec890f0a5870c641f778515d6fc468965b85e3147ca44dd9380f`

## Outcome and baseline

R15 repairs the stopped R14 noncandidate by completing semantic mappings for every failing stripped-geometry field before any browser work. The R14 compact exhaustive audit is the frozen defect authority: it found no descriptor gap, exact-one primary targets passed, polygon semantics passed, and family topology mostly passed; the remaining failure is that 42 field targets do not move in their stripped semantic geometry or dimension annotation.

R15 is conceptual browser-preview work only. It grants no CAD, OpenSCAD, STEP/export, slicer, printability, fit, drainage-performance, physical, MakerWorld, publication, live-route, or delivery acceptance.

## Frozen requirements

| ID | Requirement | Acceptance evidence |
| --- | --- | --- |
| R15-01 | Work only in the new R15 preview/test/docs/scratch namespace. R14, R13, frozen R12 core/schema/derive, live routes, CAD, OpenSCAD, STEP, slicer, printer, physical, and unrelated files are read-only. | pre/post path audit |
| R15-02 | Verify R14 frozen fingerprint `ff0f85197408ec890f0a5870c641f778515d6fc468965b85e3147ca44dd9380f`, then verify R15 frozen inputs. | `shasum -a 256` and `shasum -a 256 -c` receipts |
| R15-03 | Freeze R14 source/tests/stop receipt and `scratch/r14-exhaustive-audit/{audit.json,SUMMARY.md,audit.mjs}` as the defect baseline. | frozen-input manifest |
| R15-04 | Treat descriptor gap as false for this repair. No core/schema/derive change is authorized. | audit evidence and source path audit |
| R15-05 | Preserve source ban: no `.field-witness`, generic witness grids, value-hash-driven geometry/color/text, raw/effect hash badges, random IDs, timestamps, or raw-state renderer authority. | source-ban gate |
| R15-06 | Preserve exact-one primary target: 84/84 active fields must have one visible primary target, with 0 unexpected inactive target leaks and 0 duplicate primary targets. | target-contract and exhaustive audit |
| R15-07 | Repair the complete 42-field grouped list before evaluating browser readiness; do not stop after one field or one small subgroup. | implementation receipt and audit |
| R15-08 | Cheap gate must be 84/84 semantic PASS, source-ban PASS, target-map PASS, exact-one PASS, 0 unexpected inactive/duplicate targets, polygon PASS, family topology PASS, and compact audit size <= 1 MB before browser. | compact audit and ordered command receipt |
| R15-09 | Preserve polygon 30/30 uniqueness and expected inactive rotation symmetry at roundness `1`. | polygon regression |
| R15-10 | Preserve family topology passes: closure 2/2, ends 4/4, patterns 10/10, relief 3/3, label modes 3/3, attachments 6/6, drains 4/4. Repair envelope 4/4 alias. | stripped family gates |
| R15-11 | Only `label.openScadFontFamily` remains metadata-only. Every failing R15 repair target must be geometry or dimension annotation. | target-map audit |
| R15-12 | After cheap PASS, generate human-visible category sheets for sections, closures, ends, surface/envelope/fade/relief, labels, attachments, drains, and tier states. | sheet manifest and critique input |
| R15-13 | After sheet generation, run Chromium, Firefox, and WebKit at desktop `1280x900` and mobile `390x844`. | six-context browser evidence |
| R15-14 | Initial implementation attempt plus at most two grouped repair cycles. Each repair cycle addresses the latest grouped failure list from a fresh exhaustive audit. | retry ledger |
| R15-15 | No live route, served copy, delivery, or user-facing handoff before independent VAL, independent CRIT, and formal REV all PASS the same R15 candidate fingerprint. | formal review join |

## Required 42-field repair groups

| Group | Count | Fields |
| --- | ---: | --- |
| `screw-detail` | 2 | `closure.screw.formHeight`, `closure.screw.radialClearance` |
| `bayonet-detail` | 3 | `closure.bayonet.lockAngleDeg`, `closure.bayonet.rampRise`, `closure.bayonet.radialClearance` |
| `end-detail` | 2 | `ends.bottom.size`, `ends.top.size` |
| `surface-global` | 7 | `surface.envelope`, `surface.depth`, `surface.minWall`, `surface.axialPitch`, `surface.arcPitch`, `surface.coverage`, `surface.fadeMetric` |
| `pattern-knit` | 1 | `surface.stitch.tightness` |
| `pattern-flutes` | 6 | `surface.flute.count`, `surface.flute.duty`, `surface.flute.waveAmplitude`, `surface.flute.waveWavelength`, `surface.flute.wavePhase`, `surface.flute.waveDirection` |
| `pattern-spiral` | 4 | `surface.spiral.pitch`, `surface.spiral.bandWidth`, `surface.spiral.softness`, `surface.spiral.direction` |
| `pattern-quilt` | 3 | `surface.quilt.grooveWidth`, `surface.quilt.edgeSoftness`, `surface.quilt.rotationDeg` |
| `drain-faces` | 5 | `ventDrain.linked`, `ventDrain.bottom.diameter`, `ventDrain.bottom.ringRadius`, `ventDrain.top.diameter`, `ventDrain.top.ringRadius` |
| `label-detail` | 7 | `label.text`, `label.fontFamily`, `label.weight`, `label.relief`, `label.target`, `label.angleDeg`, `label.patch` |
| `attachment-detail` | 1 | `attachment.mountAngleDeg` |
| `container-and-section` | 1 | `container.splitPercent` |

## Exact implementation scope

Implementation may create or edit only:

- `projects/laifen-wave-case/preview/p2-r15-complete-semantic-mapping-recovery/**`
- `projects/laifen-wave-case/tests/test_p2_r15_target_contract.mjs`
- `projects/laifen-wave-case/tests/test_p2_r15_render_observability.mjs`
- `projects/laifen-wave-case/tests/test_p2_r15_visual_families.mjs`
- `projects/laifen-wave-case/tests/test_p2_r15_ui_contract.mjs`
- `projects/laifen-wave-case/tests/test_p2_r15_browser.py`
- `projects/laifen-wave-case/scratch/r15-*/**`
- R15 role receipts and manifests under this iteration directory

R15 may copy R14 source into the R15 namespace as a starting point, but R14 remains immutable input. R15 may import the frozen R12 core read-only. R15 must not edit R14 tests to make them pass; it must create R15 tests and a R15 exhaustive audit.

## Ordered DAG

| Task | Owner/role | Dependency | Done gate | Stop |
| --- | --- | --- | --- | --- |
| IMP-GCS-R15-01A | implementation, full grouped cheap repair | R15 design fingerprint and verified inputs | R15 namespace, source ban, target map, exact-one gate, full grouped 42-field semantic repair, compact exhaustive audit | stop on scope expansion, source-ban fail, descriptor-gap claim, duplicate/inactive target, audit >1 MB, or cheap result below 84/84 after repair ceiling |
| IMP-GCS-R15-01B | implementation, visual/browser after cheap PASS | 01A 84/84 PASS | human category sheets and six-context browser PASS; frozen candidate manifest | stop on browser errors, overflow, hidden focus, stale invalid output, target loss, or sheet incomprehensibility |
| VAL-GCS-R15-01 | independent validator | exact R15 candidate | read-only manifest verification, independent 84/84 exhaustive audit, source/family/polygon/tier/browser rerun | PASS required |
| CRIT-GCS-R15-01 | independent critic | same R15 candidate | human sheet and desktop/mobile recognition critique | PASS required |
| REV-GCS-R15-01 | formal reviewer | candidate plus VAL and CRIT | scope, provenance, requirement traceability, and findings-disposition join | PASS only if VAL and CRIT PASS |

No browser work, screenshot, candidate freeze, or delivery work may begin until the cheap audit is 84/84 with 0 unexpected inactive/duplicate targets.

