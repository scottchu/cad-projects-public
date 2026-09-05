# P1 R7 parametric-core refactor brief

**Owner:** `DES-CAD-FV1-01`  
**Status:** frozen design contract; implementation pending  
**Task type:** source-preserving build123d package refactor and STEP regeneration  
**Baseline:** immutable `cad/p1_r7_end_chamfer/`, reviewed candidate `8d3941772cca549846937dcad6ce4a05e06f5bba104c261668a0cf747c62b6a1`

## Outcome

Create `cad/container_generator_v1/` as a clearer parametric build123d package for the already printed first-version design. Reorganize the original P1 R7 source, expose and group only its existing truthful inputs, centralize all math in one pure derivation, preserve source-level joints/datums, and regenerate four default STEP artifacts. This is an adapter/refactor, not a redesign.

The user report selects P1 R7 as the physical-design baseline. Because the printed artifact and slicer identities and complete measurements were not supplied, physical acceptance remains partial and unbound to an exact digital candidate.

## Immutable default

- 39 mm crest OD; 30 mm body bore; 31 mm cap bore.
- 213 mm cavity from approximate device length 208 mm plus 5 mm allowance.
- 219 mm closed outside length; body/cap heights 144/84 mm.
- Existing right-hand B thread: pitch 2 mm, 6 mm effective engagement, 0.25 mm radial clearance, 0.5 mm height, 1.4 mm root wall, and existing lead/runout/taper/positive shoulder.
- Existing N33 procedural diamond skin, 4.8 mm axial pitch, 0.45 mm height, phase, plateau, and full seam continuity.
- Existing 1.20 mm 45-degree circular chamfer at both closed ends.
- Existing seven Ø3 mm drains at each floor: center plus six on radius 9 mm.
- Existing vertical print layout: both openings up, closed ends on the bed, 7 mm object-bounds separation.
- Existing part identities, geometry labels, joints/datums, assembly placement, and print-layout placement.

## Requirements

| ID | Requirement |
| --- | --- |
| `CV1-ORIGINAL` | Copy/refactor only the repository's original build123d P1 R7 source; do not use downloaded/reference mesh geometry. P1 R7 remains byte-unchanged. |
| `CV1-PARAMETERS` | Publish one machine-readable registry that classifies every current P1 R7 field as adjustable geometry, reference/readout-only, or locked design constant, with units/default/domain/effect. No exposed inert geometry control. |
| `CV1-DERIVE` | One pure `derive(params)` computes the complete immutable resolved record once. All builders, assemblies, manifests, and tests consume that record and may not duplicate equations. Invalid inputs stop before BREP construction. |
| `CV1-SOLIDS` | `body` and `cap` are valid positive closed solids with the same thread, shoulder, walls, floors, drains, chamfers, and skin as the default P1 R7 baseline. |
| `CV1-JOINTS` | Preserve named `shoulder`, `tip`, `full_thread_start`, `full_thread_end`, `skin_phase`, `bed`, `inner_floor`, and `screw_axis` datums/joint intent. Body is the fixed assembly root; cap motion derives from pitch and screw angle. |
| `CV1-OUTPUTS` | Generate exactly `body.step`, `cap.step`, `closed.step`, and `print_layout.step` from matching `.step.py` entrypoints in the new namespace. STEP is primary. |
| `CV1-EQUIVALENCE` | Default native solids and imported STEP occurrences must match P1 R7 geometry, volume, bounds, placements, topology roles, and key measurements under the tolerances in `DESIGN.md`. |
| `CV1-FDM` | Preserve the positive shoulder as closure stop; device/reference content never drives closure placement. Preserve openings-up vertical print poses and prove no new unsupported internal ceiling. |
| `CV1-BOUNDARY` | No STL/3MF before STEP PASS. No simulator, web/live route, OpenSCAD, alternate geometry family, slicer claim, or printer action. |

## Explicitly deferred

Wide-short proportions, generic split controls, round/polygon selection, alternate end profiles, drain location/count changes, new thread forms, additional patterns, fades, labels/text, attachments, bayonet, OpenSCAD, STL/3MF, slicing, MakerWorld, and live delivery are outside this refactor.

## Task DAG

| Task | Role/dependency | Deliverable and gate |
| --- | --- | --- |
| `IMP-CAD-CV1-01` | build123d implementer; this fingerprint | New package, focused tests, four STEP files, snapshots, candidate/evidence manifests, implementation receipt. |
| `VAL-CAD-CV1-01` | independent validator; frozen candidate | Reproduce math, actual-solid collision/equivalence, STEP validation/facts/measure/alignment, placements, and print layout. |
| `CRIT-CAD-CV1-01` | independent CAD/visual critic; frozen candidate | Review default body/cap, closed, section/thread/end/drain closeups, and print-layout snapshots for refactor drift and FDM risk. |
| `REV-CAD-CV1-01` | distinct formal reviewer; VAL and CRIT complete | Join one exact candidate and issue CAD/source and written-STEP PASS/BLOCK separately from slicer/physical state. |

One initial implementation plus at most two focused repair cycles is the ceiling. Any geometry-law change, new feature, baseline edit, unapproved tolerance relaxation, or third repair stops implementation and reopens design.
