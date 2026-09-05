# P2 R4 closure, pattern, and end-profile selector brief

**Iteration:** `2026-09-03-p2-r4-closure-pattern-selector`  
**Design role:** DES-GCS-R4-01  
**Baseline:** exact P2 R3 recovery candidate, preserving R7 CAD as a separate immutable baseline.

## Outcome and limits

Extend the browser visual-intent simulator into a generic two-piece container selector. A user can compare screw-thread and bayonet-twist-lock concepts, choose a distinctly recessed original diamond pattern, and compare flat/chamfer/fillet/dome closed ends. The result remains a visual/semantic simulator. It must not claim real thread or bayonet geometry, tolerance/fit, wall strength, drainage, CAD, OpenSCAD, STEP, slicing, printing, physical acceptance, or MakerWorld publication.

The two user images are visual-proportion evidence only. No supplied geometry, mesh, equations, dimensions, or product topology may be copied.

## Requirements

| ID | Requirement | Class | Evidence |
| --- | --- | --- | --- |
| R4-01 | Exactly two named exterior pieces meet at one configurable mid split; OD is continuous across that split. | invariant | source/scene and browser checks |
| R4-02 | Retain Laifen and wide-short presets plus H, OD, wall, floor, split mm/% controls and canonical raw split synchronization. | invariant | regression/browser trace |
| R4-03 | Add `closureMode ∈ {screw_thread,bayonet_twist_lock}`. | invariant | enum/domain test and controls |
| R4-04 | Screw mode retains pitch, turns 1/2/3, lead/runout, form-height reference, and screw radial clearance with current visual accounting. | invariant | math and DOM checks |
| R4-05 | Bayonet mode provides lock angle, lug count, axial capture, ramp rise, and bayonet radial clearance; default uses a 90-degree quarter turn. | invariant | math/domain/browser checks |
| R4-06 | Add original `recessed_diamond` using global theta/Z periodic math; keep constant pitch and phase at the split. | invariant | pure-math phase/pitch tests and visual review |
| R4-07 | Retain smooth, blunt diamond, shallow helix and wave/flute choices. | invariant | enum/visual checks |
| R4-08 | Add `endProfile ∈ {flat,chamfer,rounded_fillet,dome}`, linked or independent ends, and valid top/bottom sizes. | invariant | pure-math/domain/browser checks |
| R4-09 | Only closed external ends change for an end profile; circular cross-section, OD and middle seam remain unchanged. | invariant | delta/scene checks |
| R4-10 | Invalid parameters clear geometry, detail and scale and announce field-linked errors. | invariant | browser tests |
| R4-11 | Preserve mobile layout, accessibility semantics, true-scale relief and honestly labelled magnifier. | invariant | browser/visual review |
| R4-12 | No P1 R7, route, service, served P2 R3 copy, CAD/OpenSCAD/STEP/slicer/printer or MakerWorld change occurs in this iteration. | invariant | manifest/diff review |

## Roles, states, and non-goals

`lower-piece` and `upper-piece` are the only solid-looking scene groups. In assembled state their cylindrical sidewalls meet at `z = H-S`; exploded state separates these same two groups only. Closure bands, lugs, arrows, split scale and effective-engagement labels are non-solid annotations.

The lower external closed end is at global `z=0`; the upper external closed end is at global `z=H`. The seam is not an end profile and cannot change OD. `topEndSize` controls z=H and `bottomEndSize` controls z=0. Linked mode projects a single user size to both ends; independent mode preserves each raw value.

No device envelope, material, print orientation, drainage result, thread engagement, bayonet retention, collision, torque, fit, watertightness, mesh, or manufacturing claim is in scope.

## Iteration DAG

| ID | role/owner class | dependencies | exclusive writes | done gate / ceiling |
| --- | --- | --- | --- | --- |
| DES-GCS-R4-01 | design, strong/high | frozen P2 R3 inputs | this R4 brief/design/intake/manifest | one design pass plus one document repair |
| IMP-GCS-R4-01 | implementation, balanced/medium | frozen R4 design fingerprint | simulator source, test, implementation receipt/manifests | 14 min; initial + two focused repairs |
| VAL-GCS-R4-01 | independent validation, strong/high | frozen implementation candidate | validation receipt/evidence/scratch | 12 min; initial + two method repairs |
| CRIT-GCS-R4-01 | independent critique, strong/high | same candidate | critique receipt/evidence/scratch | 10 min; initial + two focused findings |
| REV-GCS-R4-01 | formal review, strong/high | VAL + CRIT PASS | review receipt/join only | 8 min; initial + two provenance repairs |
| DEL-GCS-R4-01 | private delivery, fast/low | formal PASS | isolated delivery copy/route receipt only | 6 min; one route retry |

VAL and CRIT may run in parallel after the candidate manifest freezes. A repair changes the candidate fingerprint and reruns affected independent gates. Stop if an implementation proposes copied reference geometry, a third exterior piece, a non-global pattern datum, changed P1 R7/CAD/route scope, or a printed-fit claim.

## Frozen amendment — phase, stitch, and envelope features

| ID | Requirement | Class | Evidence |
| --- | --- | --- | --- |
| R4-09A | `matchPatternClosed` defaults true and precompensates upper open phase from the final closure rotation; user-visible residual/readout permits comparison when off. | invariant | pure seam test + browser readout |
| R4-09B | Add original shallow `knit_stitch` global theta/Z field using arc/axial/depth and only `stitchTightness` as the new stitch control. | invariant | periodicity/sensitivity/seam tests |
| R4-09C | Add envelope enum full/bottom/top/center, normalized coverage and depth/density fade metric without changing pitch or Z-scaling. | invariant | boundary/monotonicity/pitch tests |
| R4-09D | Add original `straight_micro_flutes` with global angular pitch/count, duty/width, depth, envelope and closed-phase matching. | invariant | pure pattern/seam tests |
| R4-09E | Maintain one continuous maximum OD across both pieces: no raised seam collar and no thicker thread zone; do not add lanyard hardware. | invariant | scene/dimension inspection |
| R4-09F | Optional accessory selector reports maximum envelope outside the nominal core OD; captured/separate accessories are explicit extra body/part while core remains two pieces. | invariant | envelope/collision/browser tests |
| R4-09G | Add original global-periodic `rugged_hex` only as a visual pattern; make no print-in-place, support-free or physical claim. | invariant | pure pattern/domain tests |

These additions preserve the existing non-goals. No reference geometry is copied and visual phase matching never claims physical seam invisibility.
