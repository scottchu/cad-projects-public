# P2 R2 generic threaded-container simulator brief

**Iteration:** `2026-09-03-p2-r2-generic-container-simulator`
**Design owner:** DES-MW-02
**Frozen CAD baseline:** reviewed P1 R7 candidate `8d3941772cca549846937dcad6ce4a05e06f5bba104c261668a0cf747c62b6a1`; it remains immutable.

## Supersession and outcome

P2 R1 remains intact as evidence of the original Laifen-only intent gate. Its fixed 84 mm split range and fixed R7 thread description cannot represent a short/wide container or user-selected 1/2-turn threads, so P2 R2 replaces it before implementation and delivery. No P2 R1 source exists to migrate.

P2 R2 specifies a language-neutral parametric contract for an HTML/Three.js visual simulator now and an OpenSCAD generator later. It represents two closed-end container pieces separated at a mid-body seam. It supports a long slender reference case and a wide short jar without claiming printable thread geometry.

## Stable requirements

| ID | Requirement | Acceptance evidence |
| --- | --- | --- |
| GCS-01 | The schema works for a generic threaded container, not just one named product. | Both supplied presets derive valid geometry/readouts. |
| GCS-02 | Store only `split_from_top_mm`; percent is an exact affine input/output adapter from the closed upper outer-end datum. | Round-trip/boundary tests use unrounded numeric state. |
| GCS-03 | The assembled global frame is `z=0` at the lower closed outer end and `z=H` at the upper closed outer end. | Semantic labels and math tests. |
| GCS-04 | Users can select 1, 2, or 3 effective thread turns; `engagement_mm=thread_pitch_mm*thread_turns`. | Preset and turn-change math tests. |
| GCS-05 | Split bounds derive from current height, floor, full thread band and smooth keepouts; infeasible settings state the exact inequality failure. | Boundary/infeasible tests and visible message. |
| GCS-06 | Assembled exterior pieces share one seam plane and have no co-planar exterior overlap. Thread information is not a hidden third tube. | Render structure and scene-graph assertions. |
| GCS-07 | The four current patterns are available, use fixed physical axial/arc pitch, derive circumferential count, use global Z before clipping, and phase-match at the seam. | Pure-field and scene-clipping tests. |
| GCS-08 | Main view preserves true relief scale; a labelled magnifier may enlarge a shallow pattern only while declaring its scale and requested depth. | DOM/readout and visual review. |
| GCS-09 | Display all status meaning in text and semantic state, including errors, warnings and assembled/exploded thread-band markers. | Accessibility/DOM tests. |
| GCS-10 | Future delivery is a new private static route only, leaving all existing routes and services untouched. | Route-specific local/private readiness check plus user-surface gate. |

This visual contract does not supersede P1 requirements for the Laifen object, including its original CAD, physical measurement, thread test, slicer, and print acceptance requirements.

## Intent gate and exclusions

The simulator lets the user choose a preset, edit the height/diameter/thread/split/pattern controls, compare assembled and exploded views, and answer: *Does this show the intended two-piece container, thread location, and chosen number of turns for the selected use?* A pass confirms only visual/topology intent.

Excluded: CAD solids, triangle meshes for fabrication, actual helical thread profile, tolerance claims, printability, strength, watertightness, fit, drainage effectiveness, slicer/print, MakerWorld publication, static-service mutation, and edits outside this iteration.

## Planned implementation and delivery paths

Only a later implementation role may create:

- `preview/p2-r2-generic-container-simulator/index.html`
- `preview/p2-r2-generic-container-simulator/app.js`
- `preview/p2-r2-generic-container-simulator/style.css`
- `preview/p2-r2-generic-container-simulator/math.js`
- `tests/test_generic_container_simulator.mjs`

The intended delivery is `https://mac-mini.duckbill-ionian.ts.net:8448/container-simulator`, via existing loopback 8972/private 8448 static service. Delivery may add only that isolated route after review. It must preserve `/laifen-chamfer`, `/laifen-full`, `/laifen-full-section`, the CAD Viewer 3249/private 8449 service and public 3245. HTTP success is not evidence that the user can understand the page on their device.

## Frozen material-task DAG

| ID | Role / owner class | Inputs/dependency | Exclusive writes | Done gate and ceiling |
| --- | --- | --- | --- | --- |
| DES-GCS-01 | design, Terra/high | this frozen baseline | P2 R2 BRIEF/DESIGN/inputs | Contract, manifest and parameter examples complete; 12 min, 10k output, initial + two doc repairs. |
| IMP-GCS-01 | implementation, Terra/medium | DES manifest fingerprint | new P2 R2 preview source and one new test | Pure schema/derivation, accessible controls, true-scale render, all presets; 22 min, 14k output, initial + two focused repairs. |
| VAL-GCS-01 | independent validation, Sol/high | frozen implementation candidate | P2 R2 `VALIDATION.md`, evidence manifests and `scratch/generic-container-validation/` | Run math/DOM/render tests against exact candidate; 14 min, 9k output, initial + two method repairs. Read-only implementation. |
| CRIT-GCS-01 | independent critique, Terra/high | same exact candidate | P2 R2 `CRITIQUE.md` and `scratch/generic-container-critique/` | Challenge topology, preset coherence, thread semantics, phase, mobile/accessibility and misleading relief; 12 min, 8k output, initial + two focused findings. Read-only implementation. |
| REV-GCS-01 | formal review, Sol/high | VAL + CRIT receipts | P2 R2 `REVIEW.md` and review manifest/receipt | Check scope, provenance, requirement coverage and finding dispositions; 8 min, 6k output, initial + two provenance repairs. |
| DEL-GCS-01 | private delivery, fast/low | formal PASS | route-specific service configuration and readiness receipt | Add/check only `/container-simulator`; local/private 200 then record need for user-device check. 8 min, one repair. |

No more than three workers may run. VAL and CRIT may run in parallel only after IMP freezes its candidate. REV joins them. Any source-candidate change invalidates only downstream manifests which name it. Stop and return to design if dynamic bounds, canonical conversion, non-overlapping exterior, or global-Z phase cannot be maintained. Each worker returns status, verified fingerprint, changed paths, commands/results, requirement coverage, findings, unresolved risks and next action.
