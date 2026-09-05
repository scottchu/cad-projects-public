# P2 R19 eleven-field semantic recovery brief

**Iteration:** `2026-09-03-p2-r19-eleven-field-semantic-recovery`  
**Design owner:** `DES-GCS-R19-01`  
**Status:** frozen design contract; implementation not started  
**Stopped predecessor:** R18 standalone renderer, 73/84

## Outcome

R19 keeps the R18 standalone architecture and repairs only the 11 fields enumerated below. It remains conceptual browser-preview evidence and makes no CAD, OpenSCAD, STEP/export, slicer, printability, fit, drainage-performance, physical, MakerWorld, publication, live-route, serving, or delivery claim.

## Residual ledger

| Field | Class | Required descriptor source |
| --- | --- | --- |
| `closure.matchPatternClosed` | geometry | `descriptor.closure.assembled.phaseMatchesPattern` plus assembled rotations |
| `closure.screw.leadRunoutTurns` | dimension-annotation | `descriptor.closure.primitive.lead`, `.pitch`, and `.protected` |
| `closure.screw.radialClearance` | dimension-annotation | `descriptor.closure.primitive.clearance` |
| `surface.reliefMode` | geometry | `descriptor.surface.relief.{insetDepth,outsetHeight,baseOD,crestOD,minimumResidualWall}` |
| `surface.envelope` | geometry | `descriptor.surface.field[*].{z,theta,weight,placed}` |
| `surface.coverage` | dimension-annotation | transition bounds derived from `descriptor.surface.field[*].{z,weight}` and `descriptor.constraints.height` |
| `surface.flute.duty` | geometry | flowing-flute cross-section from `descriptor.surface.field[*].{theta,z,raw,placed}` |
| `surface.spiral.softness` | geometry | helix edge profile from `descriptor.surface.field[*].{theta,z,raw,placed}` |
| `label.openScadFontFamily` | truthful-metadata | exact `descriptor.labels[*].openScadFontFamily` |
| `label.weight` | geometry | `descriptor.labels[*].weight` and glyph primitive |
| `label.angleDeg` | dimension-annotation | `descriptor.labels[*].theta` and body angular datum |

## Requirements

| ID | Requirement | Gate |
| --- | --- | --- |
| R19-01 | Write only R19 preview/tests/scratch/iteration records. R18 and earlier, frozen core, live, CAD, export, slicer, printer, physical, and continuity files are immutable. | path audit |
| R19-02 | Freeze and verify R18 contract, source, tests, stop receipt, and collecting audit. | input manifest |
| R19-03 | Preserve the standalone descriptor-only renderer and prohibit imports/calls into prior renderers. Preserve the transitive generic/hash witness ban. | dependency-closure audit |
| R19-04 | Preserve the full 84-row path/source/class map, ten explicit no-fallback pattern builders, exact-one active primary targets, zero duplicates, and zero unexpected inactive targets. | target/source audit |
| R19-05 | Repair all 11 listed fields as specified in `DESIGN.md`; no raw/effect hash or generic scalar witness may satisfy an oracle. | local-oracle audit |
| R19-06 | Preserve all other 73 official-pair passes and all polygon/family/UI/disclosure/nonzero-bbox/no-overflow behavior. Any new failure joins the complete grouped repair ledger. | full regression |
| R19-07 | The collecting audit must run all 84 rows, apply class-specific stripping, report every failure, and reach 84/84 before screenshots or browser work. Evidence stays at or below 1 MiB. | compact audit |
| R19-08 | After cheap PASS, capture normal and caption-hidden category sheets, then run Chromium, Firefox, and WebKit at `1280x900` and `390x844`. | sheets and 6-context matrix |
| R19-09 | Allow one initial attempt and at most two grouped repair cycles. Each cycle repairs the entire current list and reruns all 84 rows plus source/family/UI gates. | retry ledger |
| R19-10 | No live route, serving, delivery, or user-facing handoff until independent VAL, CRIT, and REV all PASS the same R19 candidate. | role join |

## Exact implementation scope

- `projects/laifen-wave-case/preview/p2-r19-eleven-field-semantic-recovery/**`
- `projects/laifen-wave-case/tests/test_p2_r19_target_contract.mjs`
- `projects/laifen-wave-case/tests/test_p2_r19_render_observability.mjs`
- `projects/laifen-wave-case/tests/test_p2_r19_visual_families.mjs`
- `projects/laifen-wave-case/tests/test_p2_r19_ui_contract.mjs`
- `projects/laifen-wave-case/tests/test_p2_r19_browser.py`
- `projects/laifen-wave-case/scratch/r19-*/**`
- R19 receipts and manifests under this iteration directory

The app may import frozen core derivation. The R19 renderer and its dependency closure consume only a complete descriptor and R19-local helpers/map.

## Roles

`IMP-GCS-R19-01A` owns the full 11-field cheap repair; `IMP-GCS-R19-01B` owns downstream sheets/browser/candidate freeze. Independent `VAL-GCS-R19-01` reruns provenance and deterministic/browser gates. Independent `CRIT-GCS-R19-01` judges caption-hidden clarity. `REV-GCS-R19-01` joins scope, evidence, and findings. Stop on scope expansion, prior/core/live/CAD edit need, inherited renderer code, a banned witness, map/ownership regression, incomplete audit, or repair exhaustion.
