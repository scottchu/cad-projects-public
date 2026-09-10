# P20 R2 corrected-sign focused implementation receipt

Date: `2026-08-26`

Status: **FIXED-ROD/RAIL CORRECTION USER-APPROVED IN THE COMPLETE P19-BASED
ASSEMBLY; INHERITED DIAGONAL WIRE USER-REJECTED.**

## Approved authority

- User-approved FRONT-YZ gate SHA-256:
  `e2d05a852889bef2e9c97a2e18878b475aef39b690fa884d6db6a1054d1da8d7`.
- Physical outer motion about the only rotation center `C=(0,0)`:
  left `+45 deg`, right `-45 deg`.
- Purple axle remains world-fixed at `A=(-15,-11)`.
- Exact local END points:
  - left `(-18.384776310850235,+2.828427124746188)`;
  - right `(-2.828427124746192,-18.384776310850235)`.
- White-rod outer rails/apertures: `0`.
- P19 inner white-rod rails remain delegated unchanged.

## Source result

The new P20 R2 module delegates preserved geometry to the exact P19 source and
owns only the authorized parameter/sign/outer-cut delta. One pure
`fixed_axle_local_center()` inverse-frame function generates both `33`-sample,
`7.90 mm` fixed-axle arc loci. The outer plate builder subtracts only that
side-specific arc and never loops over the three white rods.

The OPEN/MID/END wrappers and full-motion sidecar encode the corrected
physical sign. Only the focused both-rail review generator was written to STEP
in this task.

## Commands and results

Focused pure-math gate, run before BREP:

```text
uv run --package xt60-bend-jig pytest -q \
  projects/xt60-bend-jig/tests/test_p20_r2_fixed_rod_arc_rail.py \
  -k 'frozen_p19_delta_mask or inverse_frame_loci or approved_physical_twist_signs'
...                                                                      [100%]
3 passed
```

Independent printed pure-math witness from the production functions:

```text
left physical_deg 45.0
left END q=(-18.384776310850235,2.828427124746188)
left END reconstructed A=(-14.999999999999998,-11.000000000000000)
right physical_deg -45.0
right END q=(-2.828427124746192,-18.384776310850235)
right END reconstructed A=(-15.000000000000000,-11.000000000000000)
C (0.0, 0.0)
```

Focused STEP generation:

```text
uv run --package xt60-bend-jig python <cad-skill>/scripts/gen \
  projects/xt60-bend-jig/cad/p20_r2_fixed_rod_arc_rail/p20_r2_fixed_rail_review.step.py \
  --write --force
built .../p20_r2_fixed_rail_review.step.py
```

Focused STEP inspection:

```text
inspect refs .../p20_r2_fixed_rail_review.step --facts --planes --positioning
faces=398 edges=1170 occurrences=4

inspect validate .../p20_r2_fixed_rail_review.step
PASS - all solids valid, closed, and positive volume

inspect diff .../p20_r2_fixed_rail_review.step.py \
  .../p20_r2_fixed_rail_review.step --planes
topologyChanged=False, geometryChanged=False, bboxChanged=False, kindChanged=False
```

Phone snapshot:

```text
snapshot --input .../p20_r2_fixed_rail_review.step.py \
  --camera right --width 1200 --height 1600 --display solid
PASS 1200x1600 orthographic PNG; both complete rails visible
```

The first diagnostic snapshot used an unsuitable oblique framing and was
moved recoverably to
`/Users/scottchu/.Trash/p20-r2-superseded-snapshot-2026-08-26/` after the
right-orthographic view confirmed both rails.

## Frozen artifacts

- Focused STEP:
  `cad/p20_r2_fixed_rod_arc_rail/p20_r2_fixed_rail_review.step`
  SHA-256 `07c398b9b01233150dc4ca0805e2a7e2980f60fff302e1442654e0c3fb3f8f2c`.
- Authoritative P20 R2 source:
  `src/xt60_bend_jig/p20_r2_fixed_rod_arc_rail.py`
  SHA-256 `1b004ac07fbd3f8ff2f776b3219c5b98e50825b123e1ec3410683d61134baa73`.
- Complete P19-based assembly STEP:
  `cad/p20_r2_fixed_rod_arc_rail/p20_r2_full_motion.step`
  SHA-256 `715851b434ab2e17a7f6c29be0b21924fb99ed6e28c20be8b276399a5d1d6bca`.
- Phone snapshot:
  `docs/review/p20-r2-fixed-rod-arc-rail/p20_r2_fixed_rail_review_phone_right_20260827T020852Z.png`
  SHA-256 `b3a794cc8863f81d8e7796ff0094f10cef4baf8c251505d71f9dd310af129272`.

Original-resolution visual inspection found the blue/right plate's cyan rail
curving toward local END `(-2.828,-18.385)` and the green/left plate's purple
rail curving toward local END `(-18.385,+2.828)`. Both apertures and colored
centerline witnesses are fully exposed; neither is a round journal.

## User acceptance and next-task freeze

The user approved the fixed purple rod and both curved fixed-rod rails as seen
in the complete P19-based P20 R2 assembly. The following implementation facts
are frozen and may not change in the next wire task:

- `C=(0,0)` and world-fixed `A=(-15,-11)`;
- physical left `+45 deg`, right `-45 deg`;
- `qL(0)=qR(0)=(-15,-11)`;
- `qL(1)=(-18.384776310850235,+2.828427124746188)`;
- `qR(1)=(-2.828427124746192,-18.384776310850235)`;
- two `7.90 mm` curved fixed-axle rails; and
- zero white-rod outer rails/substitute apertures.

This is user approval of fixed-rod/rail/complete-assembly **presence**, not
acceptance of every inherited workpiece reference. The inherited P19 diagonal
wire is now **USER-REJECTED**. The next task must correct only that wire to an
exactly vertical leg, tangent `R6` quarter-circle arc, and exactly horizontal
leg, without altering any frozen fixed-rod fact above.

The defect escaped because P19 `build_workpiece_reference()` constructed the
wire from its END-derived diagonal datum and the P19 tests asserted the same
assumption. Their mutual consistency contradicted but did not exercise core
`REQ-002` and `REQ-017`, which require the functional fixed 90-degree bend.

No mesh, 3MF, slicing, print, white-rod outer rail, force, fit, manufacturing,
or physical-acceptance claim is made. The six known white-rod/solid-outer
collisions remain the intentional non-product boundary.
