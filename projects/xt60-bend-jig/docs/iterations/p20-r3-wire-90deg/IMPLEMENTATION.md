# P20 R3 wire-only implementation receipt

Date: `2026-08-26`

Status: **IMPLEMENTED AND FOCUSED-DIGITAL VALIDATED; NOT PHYSICALLY ACCEPTED**

## Implementation

- New source delegates the full assembly to
  `p20_r2_fixed_rod_arc_rail.build_full_motion_open()`.
- It replaces exactly one occurrence,
  `motion_full_fixed_workpiece_reference`, with
  `p18_r1_compact_counter_twist.build_workpiece_reference()`.
- P18 accepted source SHA-256:
  `37a45b972afb534e695b6c334b72ec451f4d466aafedab12c22afd90b866440f`.
- The R3 source contains no `wire_line_point`, `wire_line_direction`, or
  `p19.build_workpiece_reference` reference.

## Focused tests

```text
uv run --package xt60-bend-jig pytest -q \
  projects/xt60-bend-jig/tests/test_p20_r3_wire_90deg.py
.....                                                                    [100%]
5 passed
```

The tests verify all three frozen P20 R2 hashes, identical P18/P20 XT60 body
coordinates, exact vertical/quarter-arc/horizontal topology, `90 deg`, absence
of diagonal-line inputs, and exact label/bounds/volume/solid-count/validity
signatures for every non-workpiece occurrence. Both assemblies contain `18`
occurrences; the sole changed signature is the workpiece.

## STEP validation

```text
scripts/gen .../p20_r3_full_motion.step.py --write
built

scripts/inspect refs .../p20_r3_full_motion.step --facts --planes --positioning
faces=343 edges=867 occurrences=18

scripts/inspect validate .../p20_r3_full_motion.step
PASS - all solids valid, closed, and positive volume

scripts/inspect diff .../p20_r3_full_motion.step.py \
  .../p20_r3_full_motion.step --planes
topologyChanged=False, geometryChanged=False, bboxChanged=False, kindChanged=False
```

## Visual review

The single `1200 x 1600` right-orthographic full-assembly snapshot focuses the
yellow workpiece while ghosting the complete mechanism. At original resolution
the vertical leg, tangent quarter-circle, and horizontal +Y tail are plainly
visible together with all plates, rails, rods, caps, axle, keepers and XT60
context. It is not an isolated wire-only handoff.

## Boundary

No broad collision sweep, mesh, slicing, print, force, fit, manufacturing, or
physical claim was performed. The zero-white-rod-outer-rail and known-collision
P20 R2 intermediate boundary remains unchanged.
