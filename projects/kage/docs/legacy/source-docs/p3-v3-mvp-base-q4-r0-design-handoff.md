# KAGE P3 V3 MVP base Q4-R0 — design handoff

Status: **DESIGN PROPOSAL — approval required; no CAD implementation or print release**  
Date: **2026-08-19**  
Successor namespace: `p3_v3_mvp_base_q4_r0`

## Decision

Validate the hard stationary mechanic first: four printable base quadrants must
assemble into one true 300 mm base. This successor contains only four base
quadrants, eight underside bridge joiners, and optional hardware reference
bodies. It contains no motor, tower, ring, fin, LED, electronics, or legacy
mounting-hole geometry.

This is a new, isolated successor. It must not overwrite the locked mechanism,
I3-R1, or the incomplete I3-R2 release namespace. A fit coupon may qualify
clearances, but only the complete four-quadrant base can pass this MVP.

## Inspected inputs and hashes

Repository commit: `2f5fac86a8f3f8cc23fbc5ca8ae9a37d531d607a`.

| Input | SHA-256 |
|---|---|
| `p3_v3_locked_parametric_repair_r1_i1_geometry.py` | `2683f001810d3b4b7b6b80672580ea654d00c8d40f3fb9340adb0d82711e53bb` |
| `p3_v3_locked_parametric_repair_r1_i1_spec.py` | `9200958d8f2d23fafdae8398b0384ed984f444733c558eb98e2d489a18a468f4` |
| `models/p3_v3_locked_parametric_repair_r1_i1_fixed_tower_retention/p3_v3_r1_i1_fixed_tower_retention_assembled.step` | `8bc30cab75f83380b6b53fb967b935a9198b36f814368ce53826e574f9649724` |
| `p3_v3_phase3_i3_r1_real_joinery_spec.py` | `1a5a35c526bd3b52e0383b9199e28e0798a77e6c123cc1cf3f3e8464df331c60` |
| `p3_v3_phase3_i3_r1_real_joinery_geometry.py` | `183ba5004cdcb6cec0a209cb6b2c8fff23d74a755ba164c25d944ccca485eb1f` |
| `models/p3_v3_phase3_i3_r1_real_joinery/assembled_nominal.step` | `ffa82c10617018c3ea986651a7e594ab799de8732a5ad294e2c7070966ed0f22` |
| `docs/p3-v3-phase3-i3-r2-verified-release-localized-handoff.md` | `b39376240fa9c3a88440592070d55d7caca7f9bb59b1032e7d8608c8dbf74ec8` |

## Measured conflicts in the current/prior geometry

1. The locked rear chassis is `R66..R145 x 2.50`, so the assembled base is
   `290.00 x 290.00 x 2.50`, not 300 mm. The existing 300 mm datum belongs to
   other stationary rings at R150.
2. The locked cardinal quadrants are each `145 x 145 x 2.50` and one solid,
   but have no base retention. Their seams at 0/90/180/270 degrees also land on
   accepted motor/tower axes at 0 and 180 degrees.
3. I3-R1 moves stationary seams to `37.5 + 90*k` degrees. Its measured rear
   quadrant maximum XY span is `203.306642 mm`, but every replacement quadrant
   contains **two disconnected solids**, inherited from clipping already-split
   cardinal quadrants instead of sectioning one full base solid.
4. I3-R1 reconstructs only the original `R145` base, so its four-quadrant
   compound remains exactly `[-145,-145]..[145,145]` in XY.
5. The I3-R1 rear bridge is `12R x 18T x 4Z`. Its nut cut runs from 0.20 to
   2.20 mm above the bridge bottom, leaving a measured `1.80 mm` roof at the
   assembly face and a `0.20 mm` bottom skin. The nominal 5.70 mm nut cannot be
   loaded through the 3.40 mm screw bore; the documented +Z loading order is
   therefore not represented by the actual source geometry.
6. Reusing the old R85/R120 join axes with the locked mount holes leaves only
   `0.0605 mm` edge clearance between one D4 split socket and a motor hole, and
   `0.8407 mm` between one M3 join screw and a tower hole. Those values are not
   robust ligaments.
7. The I3-R2 handoff still declares no CAD implementation, and its artifact
   root currently contains only a README. It cannot be treated as a current
   printable base.

## Frozen Q4-R0 parameters

Coordinates: assembly origin at circle center; XY is the base plane; base
underside is `Z=0`; +Z is the visible/front direction. Units are millimetres.

| Named parameter | Value |
|---|---:|
| `base_outer_diameter_mm` | `300.00` |
| `base_outer_radius_mm` | `150.00` |
| `base_inner_radius_mm` | `66.00` |
| `base_thickness_mm` | `2.50` |
| `quadrant_count` | `4` |
| `quadrant_angle_deg` | `90.00` |
| `seam_base_angle_deg` | `37.50` |
| `seam_relief_per_face_mm` | `0.05` |
| `seam_gap_nominal_mm` | `0.10` |
| `u1_bed_xy_mm` | `270.00` |
| `u1_edge_keepout_mm` | `5.00` per edge |
| `u1_usable_xy_mm` | `260.00` |
| `quadrant_brim_mm` | `5.00` per side |
| `joiner_radii_mm` | `(75.00, 138.00)` |
| `joiner_radial_mm` | `12.00` |
| `joiner_tangential_mm` | `26.00` |
| `joiner_thickness_mm` | `5.00` |
| `screw_tangent_offset_mm` | `7.00` |
| `base_screw_clearance_diameter_mm` | `3.40` |
| `m3_screw_length_mm` | `6.00` |
| `m3_button_head_max_diameter_mm` | `5.50` |
| `m3_hex_nut_nominal_af_mm` | `5.50` |
| `m3_hex_nut_max_thickness_mm` | `2.40` |
| `nut_pocket_af_mm` | `5.80` |
| `nut_pocket_depth_mm` | `2.70`, open at joiner top/assembly face |
| `dowel_nominal_diameter_mm` | `4.00` |
| `dowel_length_mm` | `6.00` |
| `joiner_press_bore_diameter_mm` | `3.95` |
| `joiner_press_engagement_mm` | `3.50` blind from joiner top |
| `base_split_slip_bore_diameter_mm` | `4.15` |
| `base_split_slip_engagement_mm` | `2.50` through base |
| `driver_access_diameter_mm` | `8.00` |
| `driver_access_height_mm` | `25.00` above base top |
| `bad_fixture_outer_joiner_shim_mm` | `0.50` |
| `legacy_mount_voids_enabled` | `False` |

The four quadrants must be cut from one source-owned full annulus, then relieved
at their opposed seam faces. Do not re-segment a compound of older quadrants.
Each output quadrant must be exactly one connected, positive-volume solid.

The two joiner radii replace R85/R120. Against the old, deliberately excluded
mount-hole pattern, the nearest calculated edge clearance becomes `8.370 mm`
instead of `0.0605 mm`; this is reservation evidence only, not approval of a
future motor/tower layout.

## Join and retention design

Each of four seams receives two identical underside bridges, for eight total.
Every bridge has one M3 screw axis on each side of the seam and one centered D4
registration pin. One screw therefore clamps each adjacent quadrant to the
same bridge. The two radially separated pins constrain seam yaw; the closed
four-seam loop and screw clearances constrain in-plane translation. Flat bridge
top faces seat both quadrant undersides and establish Z.

The common-hardware build uses 16 M3x6 ISO 7380-1 button-head screws, 16 ISO
4032 M3 hex nuts, and 8 D4x6 steel dowel pins. Hardware reference solids are
optional CAD children but the screws/nuts and qualified alignment pins are
required for the physical retention test. Printed D4 calibration pins may be
used only for initial fit; they do not pass the final retention gate.

Derived minimums at nominal dimensions:

- nut-pocket radial wall: `(12 - 5.80/cos(30deg))/2 = 2.651 mm`;
- nut-to-dowel ligament: `7 - 5.80/(2*cos(30deg)) - 3.95/2 = 1.676 mm`;
- tangential end wall: `13 - 7 - 5.80/(2*cos(30deg)) = 2.651 mm`;
- nut axial slack: `2.70 - 2.40 = 0.30 mm`;
- dowel diametral slip: `4.15 - 4.00 = 0.15 mm`;
- M3x6 tip beyond a 2.50 mm base plus 2.40 mm nut: `1.10 mm`, contained
  inside the 5.00 mm bridge and its through screw relief.

## Print orientation and assembly order

- Print every quadrant flat with its visible/front datum face on the bed. The
  critical front plane is therefore one common first-layer datum. Use a 5 mm
  brim; no quadrant needs support. The measured clean-annulus bounds are:
  Q1/Q3 `210.317215 x 109.821746 x 2.50`, Q2/Q4 the swapped XY spans. With
  brim, the maximum reserved span is `220.317215 mm`, within the 260 mm usable
  U1 envelope.
- Print each bridge bottom-down with the nut pockets and blind dowel bore open
  upward. No support or trapped nut pocket is allowed.
- Qualify one nut pocket and both dowel fits before printing the complete set;
  this coupon never substitutes for the full-base test.
- Press one D4x6 pin 3.50 mm into each bridge and load both M3 nuts from the
  open top. Loosely attach every bridge to the clockwise quadrant using one
  screw per bridge. Lower the adjacent quadrant onto the exposed pin halves,
  add the remaining screws, and close the four-seam loop.
- Set all eight bridge bottoms on one verified flat reference surface and
  tighten from +Z in an alternating seam/inner-outer sequence. The 8 mm x
  25 mm driver cylinders must remain unobstructed.

## Meaningful acceptance tests only

1. **Bed envelope:** actual-solid AABB plus 5 mm brim for each of Q1..Q4 is
   inside `[5,5]..[265,265]` on the U1. Each quadrant is one valid solid.
2. **300 mm datum and runout:** assembled source bounds are
   `[-150,-150,0]..[150,150,2.5]` for the base and radial samples on every
   quadrant outer arc equal `150.00 +/-0.02` in CAD. Physical OD measured at
   0/45/90/135 degrees is `300.00 +/-0.50`, with max-minus-min no more than
   `0.50`.
3. **Seams:** every adjacent-quadrant BREP intersection is at most `1e-7 mm3`.
   Normal face distance sampled at R66, R75, R138, and R150 is
   `0.10 +/-0.02` in CAD. Physical gaps must be `0.05..0.30` with no overlap
   or forced bowing.
4. **Z coplanarity:** all four CAD front datum faces share `Z=2.50` within
   `0.02`; all bridge seats share `Z=0`. Physical seam step is at most `0.25`
   and overall front-face deviation under a straightedge is at most `0.50`.
5. **Joiner fit and engagement:** measure all 16 screw-axis pairs and eight
   dowel-axis pairs for coaxiality; verify D3.40 clearance, 2.70-deep open nut
   pockets, at least 2.40 nut engagement, 3.50 press engagement, 2.50 slip
   engagement, 0.15 diametral dowel slip, and the three minimum ligaments above.
   Actual bridge/quadrant contact is required on both sides of every seam.
6. **Retention and access:** all 16 D8 x25 driver-access cylinders are free of
   printed geometry. After ten lift/place cycles holding a different quadrant
   each cycle, no seam may disengage and tests 2-5 must still pass.
7. **Deliberate bad-fixture negative:** rerun the production placement checks
   with a 0.50 mm shim under the outer bridge of seam 4 (or the identical CAD
   placement override). The same evaluator must fail Z coplanarity and at least
   one dowel-axis/seat-contact check. A validator that passes this fixture is
   rejected.

## Boundary and approval gate

CAD can prove geometry, envelope, clearances, axis alignment, and the deliberate
negative. It cannot prove U1 first-layer flatness, PETG/PLA shrinkage, press-fit
quality, clamp preload, creep, or handling durability. Print the complete base
before calling the four-to-one mechanic proven.

On approval, implementation should create new spec/geometry/export/test files
and `models/p3_v3_mvp_base_q4_r0/`; it must not modify any inspected predecessor
or generated predecessor artifact.
