# P2 R18 standalone semantic renderer brief

**Iteration:** `2026-09-03-p2-r18-standalone-semantic-renderer`  
**Design owner:** `DES-GCS-R18-REC-01`  
**Status:** frozen design contract; implementation not started  
**Rejected predecessor:** R17 candidate `5fe1228ca56d11f6e0d6d30c2c7e832118dcb3b67293cd79fbc475dc2da9a9c6`

## Outcome

R18 replaces the layered R17 adapter with one standalone, descriptor-only renderer. The goal is to retain R17's deterministic and browser passes while removing inherited generic witness logic and making the visual teaching surfaces understandable when captions are hidden.

R18 remains conceptual browser-preview evidence. It grants no CAD, OpenSCAD, STEP/export, slicer, printability, fit, drainage-performance, physical, MakerWorld, publication, live-route, served-copy, or delivery acceptance.

## Frozen requirements

| ID | Requirement | Gate |
| --- | --- | --- |
| R18-01 | Write only the R18 preview/tests/scratch/iteration namespace. R17 and prior iterations, frozen core, live routes, CAD, export, slicer, printer, physical, and continuity files are immutable inputs. | pre/post path audit |
| R18-02 | Freeze and verify the exact R17 candidate, implementation receipt/evidence, independent `VALIDATION.md`, independent `CRITIQUE.md`, and their evidence manifests. | R18 input manifest |
| R18-03 | `renderR18(descriptor)` is standalone: neither it nor any transitive dependency may import or invoke an R16/R17 renderer. Renderer dependencies may consume the complete descriptor and R18-local helpers/map only; they may not import schema, derive, presets, or raw state. | transitive import/source audit |
| R18-04 | Export exactly 84 unique map rows, one per frozen coverage path, each with `path`, resolvable `descriptorSource`, `targetClass`, `surface`, `oracle`, and visibility rule. Classes are geometry, dimension-annotation, or truthful-metadata; only `label.openScadFontFamily` is metadata. | 84/84 map audit |
| R18-05 | Preserve exactly one visible primary `data-field-target` for every active field, zero duplicate targets, and zero unexpected inactive targets. | collecting active-state audit |
| R18-06 | Scan the full R18 renderer dependency closure. Ban `.field-witness`, generic witness grids, crypto/hash-derived output, raw/effect hash badges, random/time output, enum-name length geometry, `pattern.length`, shared `raw.reduce`, and fallback pattern builders. | transitive source ban |
| R18-07 | Implement ten named, explicit, non-aliasing surface builders: `smooth`, `blunt_diamond`, `recessed_diamond`, `knit_stitch`, `straight_micro_flutes`, `flowing_flutes`, `rugged_hex`, `shallow_helix`, `wave_flutes`, and `quilted_diamond`. | source enumeration and stripped family audit |
| R18-08 | The dimension-only subgroups for `surface.flute.waveWavelength` and `surface.spiral.pitch` must change across their official pairs and be anchored to the corresponding motif geometry. A whole-target delta cannot mask a fixed bracket. | dimension-only hash and endpoint audit |
| R18-09 | Put truthful OpenSCAD font metadata outside label geometry. Use separate label mini-panels for mode, font plus weight, orientation, target, axial position, and patch; no panel may overlap another. | DOM/bbox and caption-hidden sheets |
| R18-10 | Use separate attachment mini-panels for mode, half, angle, and size. `attachHalf` moves the actual attachment; angle uses an anchored arc; size dimensions terminate on the actual attachment outline. | DOM/bbox and caption-hidden sheets |
| R18-11 | Make blunt and recessed diamonds read as opposite depths in the main surface panel: positive broad facets versus negative incised grooves/voids, with a clearly opposite section profile. | caption-hidden comparison |
| R18-12 | Preserve R17 passes: 84/84 semantic deltas, polygon 30/30 and roundness-1 symmetry, closure 2/2, ends 4/4, pattern 10/10, envelope 4/4, relief 3/3, label mode 3/3, attachment 6/6, drain 4/4, descriptor-source resolution, nonzero target boxes, Basic/Advanced tiering, invalid clearing, disclosure, and no horizontal overflow. | full regression audit |
| R18-13 | Run Chromium, Firefox, and WebKit at desktop `1280x900` and mobile `390x844` only after cheap gates pass. All six contexts require no errors, overflow, hidden focus, duplicate/leaked target, or zero-area active target. | browser matrix |
| R18-14 | Capture normal and caption-hidden category sheets. The independent critic must identify surface family/depth, label relationships, and attachment relationships from geometry without explanatory captions. | CRIT receipt |
| R18-15 | Allow one initial implementation plus at most two grouped repair cycles. Each cycle reruns the complete 84-row audit and all affected family/source checks. | retry ledger |
| R18-16 | No live route, serving, delivery, or user-facing handoff until independent VAL, independent CRIT, and formal REV all PASS the same frozen R18 candidate. | three-role join |

## Exact implementation scope

Implementation may create or edit only:

- `projects/laifen-wave-case/preview/p2-r18-standalone-semantic-renderer/**`
- `projects/laifen-wave-case/tests/test_p2_r18_target_contract.mjs`
- `projects/laifen-wave-case/tests/test_p2_r18_render_observability.mjs`
- `projects/laifen-wave-case/tests/test_p2_r18_visual_families.mjs`
- `projects/laifen-wave-case/tests/test_p2_r18_ui_contract.mjs`
- `projects/laifen-wave-case/tests/test_p2_r18_browser.py`
- `projects/laifen-wave-case/scratch/r18-*/**`
- R18 receipts and manifests under this iteration directory

The R18 app may import the frozen core to call `derive`; the renderer and its dependency closure receive only the returned descriptor. Copying code from R16/R17 or importing either prior renderer is forbidden.

## Ordered roles

| Task | Role | Done gate |
| --- | --- | --- |
| `IMP-GCS-R18-01A` | implementer, standalone cheap gates | standalone renderer, literal complete map, transitive ban, 84/84 semantic and family/dimension gates PASS |
| `IMP-GCS-R18-01B` | same implementer, visual/browser | normal plus caption-hidden sheets and six-context browser PASS; freeze candidate |
| `VAL-GCS-R18-01` | independent validator | verify candidate and rerun transitive, 84-row, dimension-only, semantic, family, UI, and six-context gates |
| `CRIT-GCS-R18-01` | independent critic | caption-hidden surface/label/attachment recognition PASS on the same candidate |
| `REV-GCS-R18-01` | formal reviewer | provenance, scope, requirement coverage, and VAL/CRIT disposition PASS |

Stop on prior/core/live/CAD mutation, a renderer import from R16/R17, any generic/hash witness, an incomplete/unresolvable map, a fixed dimension subgroup, an alias, an active-target ownership error, or repair-ceiling exhaustion.
