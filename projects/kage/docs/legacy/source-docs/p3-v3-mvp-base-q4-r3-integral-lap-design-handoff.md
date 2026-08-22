# KAGE B0 Q4-R3 integral-lap base — design handoff

## Decision

Create a new `p3_v3_mvp_base_q4_r3_integral_lap` successor. Preserve Q4-R1 and
Q4-R2 unchanged. The assembly has exactly four printed parts: Q1–Q4. There are
no clamps, bridges, dowels, pins, inserts, or glue.

Use an alternating A/B half-lap, not four identical clockwise tabs. Q1 and Q3
are A parts and carry an integral underside tongue at both radial seams. Q2 and
Q4 are B parts and carry a matching underside-open rebate at both seams. This
is the smallest credible no-bending topology: Q1/Q3 are placed first and Q2/Q4
lower vertically over their tongues. Four identical clockwise over/under parts
create a cyclic final insertion and are rejected for the MVP unless a later
actual-solid motion proof demonstrates a simpler path.

Each seam uses two through-bolts. The BOM is eight M3 screws and eight M3 nuts.
Do not reduce this to one screw plus an unproven printed hook.

## Frozen envelope

| Named parameter | Value |
|---|---:|
| `base_outer_radius_mm` | `150.00` |
| `base_inner_radius_mm` | `66.00` |
| `base_thickness_mm` | `2.50` |
| `quadrant_count` | `4` |
| `seam_base_angle_deg` | `45.00` |
| `quadrant_angle_deg` | `90.00` |
| `seam_gap_nominal_mm` | `0.10` outside the lap |
| `future_support_clear_radius_min_mm` | `118.00` |
| `u1_bed_xy_mm` | `270.00` |
| `u1_edge_keepout_mm` | `5.00` |
| `quadrant_brim_mm` | `5.00` per side |

No joint feature or fastener hole may enter R118..150. The base material itself
continues through that annulus as before.

## Integral half-lap geometry

Use seam-local coordinates: `r` is radius and `t` is perpendicular to the
nominal radial seam, positive into the B quadrant. Assembly datum is the base
underside at Z=0 and front/top face at Z=2.50.

| Named parameter | Value |
|---|---:|
| `joint_role_a_quadrants` | `Q1, Q3` |
| `joint_role_b_quadrants` | `Q2, Q4` |
| `lap_radial_min_mm` | `70.00` |
| `lap_radial_max_mm` | `116.00` |
| `lap_radial_span_mm` | `46.00` |
| `tongue_overlap_depth_mm` | `10.00` into B |
| `receiver_rebate_depth_mm` | `10.30` from seam |
| `receiver_radial_clearance_per_side_mm` | `0.20` |
| `receiver_tip_clearance_mm` | `0.30` |
| `tongue_thickness_mm` | `1.25` |
| `receiver_roof_thickness_mm` | `1.25` |
| `lap_interface_z_mm` | `1.25` |
| `nominal_polymer_top_step_mm` | `0.00` |

Each A tongue occupies R70.00..116.00, crosses the nominal seam, extends
10.00 mm into B, and occupies Z=0.00..1.25. It is fused directly to the A
quadrant and is not a separate body. Each B rebate is open to the underside and
to the seam, spans R69.80..116.20, extends 10.30 mm into B, and removes
Z=0.00..1.25. The remaining B roof occupies Z=1.25..2.50. In the final assembly
the tongue top and roof underside have coincident seating faces at Z=1.25;
there is no intended positive-volume overlap.

The largest candidate joint corner is below R117, leaving at least 1.0 mm
radial margin to the R118 support keepout. Confirm this from actual solids, not
only parameter arithmetic.

Print Q1/Q3 underside-down so both tongues are bed-supported. Print Q2/Q4
front/top-down so both receiver roofs are bed-supported. No joint support
material is permitted on a seating face.

## Fasteners

| Named parameter | Value |
|---|---:|
| `screws_per_seam` | `2` |
| `screw_count_total` | `8` |
| `nut_count_total` | `8` |
| `screw_axis_radii_mm` | `82.00, 104.00` |
| `screw_axis_tangent_into_b_mm` | `5.00` |
| `clearance_hole_diameter_mm` | `3.40` through both layers |
| `screw_standard` | `ISO 4762 M3x6`, fully threaded |
| `nut_standard` | `ISO 4032 M3`, 5.5 mm AF, 2.4 mm max thick |
| `driver_hex_mm` | `2.50` |
| `tightening` | finger-snug only |

Install every screw from the B/front side through the 1.25 mm B roof and
1.25 mm A tongue; hold the loose nut below the A tongue with a 5.5 mm wrench.
Do not add a printed nut carrier or thin the 1.25 mm tongue with a nut pocket.
The 2.50 mm polymer stack plus 2.40 mm maximum nut consumes 4.90 mm of the
6.00 mm under-head length and leaves 1.10 mm, approximately two M3 threads,
beyond the nut. Standard socket heads project about 3.0 mm above the otherwise
flush front surface; this isolated hardware projection is accepted for the
MVP. No washer is specified.

## Assembly order

1. Support the parts in final XY on blocks that leave all eight nuts accessible
   from below. Place Q1 and Q3 at Z=0; they do not overlap each other.
2. Lower Q2 vertically at its final XY. Its two underside-open rebates seat
   simultaneously over the Q1 and Q3 tongues. Start its four screws and nuts
   loose.
3. Lower Q4 vertically in the same way over the remaining Q1 and Q3 tongues.
   Start its four screws and nuts loose.
4. Confirm the 300 mm OD and 132 mm ID are continuous and all four non-lap seam
   gaps are 0.10 mm nominal. Tighten in a cross pattern: Q2 inner, Q4 outer,
   Q2 outer, Q4 inner, then repeat on the opposite ends; stop at finger-snug.

No step requires bending, snapping, in-plane trapping, or passing one solid
through another. Q2 and Q4 must each have a collision-free straight-Z path
from at least 5.0 mm above final position.

## CAD acceptance tests

1. **Part registry:** exactly four printable one-solid parts Q1–Q4; zero clamp,
   bridge, dowel, pin, insert, or other printed occurrence.
2. **All-seam engagement:** actual-solid contact/near-contact probes confirm one
   46 x 10 mm half-lap at each of four seams and the A/B ownership above.
3. **No collision:** pairwise final-position intersections are at most
   `1e-7 mm^3`; coincident Z=1.25 seating faces are allowed, positive-volume
   plate overlap is not.
4. **Closed-loop path:** sweep actual Q2 and Q4 solids independently from
   Z=+5.0 mm to Z=0 in steps no larger than 0.25 mm with Q1/Q3 fixed; require
   zero positive-volume collision until final seating. No bending is modeled.
5. **Hardware:** eight actual M3x6 socket-head axes pass both layers, remain
   wrench/driver accessible, engage the full nut, and expose 0.8..1.4 mm beyond
   the nut. Reject M3x5 for insufficient guaranteed protrusion and M3x8 for
   unnecessary exposed tip.
6. **Registration negative:** after seating but before hardware deformation,
   reject a 0.50 mm radial shift or 0.50 mm cross-seam shift using actual tongue,
   rebate, seam-face, and screw-envelope geometry.
7. **Flatness:** all four nominal polymer front faces share Z=2.50 within
   0.02 mm and the lap creates 0.00 mm nominal polymer step. Report socket-head
   projection separately; do not hide it in the flatness metric.
8. **Keepout and outline:** OD is 300.00 mm, ID is 132.00 mm, all joint cuts,
   tongues, and holes stay below R118, and the R118..150 support annulus has no
   new joint void.
9. **Bed fit and printability:** actual oriented AABB of every one-solid quadrant
   plus 5.0 mm brim on every side fits the 260 x 260 mm usable U1 envelope;
   require the stated Q1/Q3 underside-down and Q2/Q4 front-down orientations and
   no support on lap faces.
10. **Version isolation:** no Q4-R1 or Q4-R2 source, artifact, or digest changes.

## Physical gate

Print and assemble this four-part base before adding a motor, rings, light, or
electronics. CAD does not prove layer-dependent lap fit, seam slip under hand
load, screw pull-through in 1.25 mm material, nut loosening, or assembled
flatness. The physical MVP passes only if all four vertical drops seat by hand,
the plate lies flat after finger-tightening, and repeated handling does not let
any seam visibly shift.
