# KAGE B0 Q4-R3 integral half-lap base — design handoff

## Decision

Create a new successor namespace, `p3_v3_mvp_base_q4_r3_integral_half_lap`.
Do not edit, regenerate, or relabel Q4-R1 or Q4-R2.

The assembly has exactly four printed quadrant plates. Every radial seam is a
flush half-lap integral to those plates, fastened by two vertical M3 screws.
There are no clamps, bridges, dowels, pins, glue, or other printed parts.

Do not make all four seam precedences identical: that creates a closed
over/under cycle. Use three clockwise laps and reverse only service seam S41.
Q4 is the lower starter, Q1 is the upper closing plate, and all parts can be
assembled by straight downward moves without bending or simultaneous motion.

## Named geometry

| Parameter | Value |
|---|---:|
| `base_outer_radius_mm` | `150.00` |
| `base_inner_radius_mm` | `66.00` |
| `base_thickness_mm` | `2.50` |
| `quadrant_count` | `4` |
| `seam_angles_deg` | `45, 135, 225, 315` |
| `seam_gap_outside_lap_mm` | `0.10` |
| `half_lap_thickness_mm` | `1.25` |
| `lap_mating_z_mm` | `1.25` |
| `upper_lap_z_mm` | `1.25..2.50` |
| `lower_lap_z_mm` | `0.00..1.25` |
| `lap_tongue_radial_min_mm` | `70.00` |
| `lap_tongue_radial_max_mm` | `116.00` |
| `lap_tongue_radial_width_mm` | `46.00` |
| `lap_tongue_tip_tangent_mm` | `12.00` from seam centreline into receiver |
| `lap_receiver_radial_min_mm` | `69.80` |
| `lap_receiver_radial_max_mm` | `116.20` |
| `lap_receiver_tip_tangent_mm` | `12.30` |
| `lap_radial_clearance_per_end_mm` | `0.20` |
| `lap_tip_clearance_mm` | `0.30` |
| `lap_free_edge_chamfer_mm` | `0.20 x 45 deg` |
| `future_support_clear_radius_min_mm` | `118.00` |

Use local seam coordinates with `r` radial and `t` positive clockwise into the
receiving quadrant. The donor bulk seam face is at `t=-0.05`; its upper tongue
runs from `t=-0.05` through `t=12.00`. The receiver bulk starts at `t=+0.05`;
remove its upper half over the receiver envelope, leaving the lower land. The
nominal interface is therefore `46.00 x 11.95 mm` before holes, about
`531.5 mm^2` of mating area after the two D3.40 holes.

The receiver's worst plan corner is
`sqrt(116.20^2 + 12.30^2) = 116.85 mm`, so all lap geometry remains below
R118. The annulus outside R118 through R150 stays unchanged and reserved.

## Seam precedence and quadrant roles

`A > B` means A supplies the upper tongue and B supplies the lower receiver.

| Seam | Precedence |
|---|---|
| `S12` | `Q1 > Q2` |
| `S23` | `Q2 > Q3` |
| `S34` | `Q3 > Q4` |
| `S41_service_reversed` | `Q1 > Q4` |

Thus Q1 has two upper tongues, Q4 has two lower receivers, and Q2/Q3 each have
one upper tongue and one lower receiver. This single reversal is intentional;
it breaks the impossible four-member precedence cycle while keeping all four
joints geometrically identical after assembly.

## Fasteners

| Parameter | Value |
|---|---:|
| `screws_per_seam` | `2` |
| `screw_count_total` | `8` |
| `screw_axis_radii_mm` | `82.00, 104.00` |
| `screw_axis_tangent_mm` | `6.00` |
| `screw_center_spacing_radial_mm` | `22.00` |
| `plate_clearance_hole_diameter_mm` | `3.40` through both lap layers |
| `screw_standard` | `ISO 4762 M3 x 6`, fully threaded |
| `screw_head_max_diameter_mm` | `5.50` |
| `screw_head_max_height_mm` | `3.00` |
| `nut_standard` | `ISO 4032 M3` |
| `nut_nominal_af_mm` | `5.50` |
| `nut_max_across_corners_mm` | `6.35` |
| `nut_max_thickness_mm` | `2.40` |
| `hex_key_mm` | `2.50` |
| `top_driver_access_diameter_mm` | `8.00` |
| `bottom_nut_tool_access_diameter_mm` | `8.00` |

Install screws top-down and hold ordinary loose nuts below; there are no nut
pockets. The 2.50 mm assembled lap plus a 2.40 mm maximum nut consumes
4.90 mm of the 6.00 mm under-head length, leaving 1.10 mm, about 2.2 M3
threads, beyond the nut. The printed plate faces stay at Z0.00 and Z2.50.
Only hardware projects: the head reaches Z5.50, the nut reaches Z-2.40, and the
screw tip reaches Z-3.50.

At each screw axis the minimum tangential distance to a lap free edge is
6.00 mm: 4.30 mm after the D3.40 hole radius, 3.25 mm after the head radius,
and 2.82 mm after the nut circumradius. Minimum radial centre-to-lap-edge
distance is 12.00 mm. Both screws and both tool envelopes remain inside R118.
Tighten only finger-snug for this 1.25 mm printed bearing section.

## Assembly order

1. Place Q4 at final XY and Z on a flat support datum, with both lower lands
   exposed.
2. Lower Q3 vertically from at least Z+6 mm. Seat its S34 upper tongue on Q4.
3. Lower Q2 vertically. Seat its S23 upper tongue on Q3.
4. Lower Q1 vertically as the closing plate. Its two upper tongues seat
   simultaneously on Q2 at S12 and Q4 at reversed service seam S41.
5. Insert all eight M3x6 screws top-down, add the eight nuts below, leave all
   loose, then finger-tighten in seam order S34, S12, S23, S41 and finally the
   second screw at each seam in the same order.

No step requires a plate to pass under an installed tongue, flex, or move
simultaneously with another plate.

## Meaningful CAD acceptance tests

1. **Version and count:** Q4-R1 and Q4-R2 hashes remain unchanged. Q4-R3
   exports exactly four printable one-solid quadrant bodies and zero printed
   clamps, bridges, dowels, pins, or other bodies.
2. **Envelope and bed fit:** assembled annulus is exactly OD300, ID132 and
   2.50 mm plate thickness. Each actual quadrant AABB plus a 5.00 mm brim fits
   the U1 260 x 260 mm usable envelope.
3. **Four engaged half-laps:** every seam has positive projected overlap and
   at least `525 mm^2` actual coincident mating-face area after holes. Each has
   one upper 1.25 mm solid and one lower 1.25 mm solid, with two coaxial
   D3.40 through-holes.
4. **No plate collision:** actual BREP pairwise intersections are at most
   `1e-7 mm^3`; intended laps share faces at Z1.25 but never positive volume.
   Non-lap seam gaps are 0.10 mm.
5. **Flushness:** excluding fasteners, all four top faces are coplanar at
   Z2.50 and all four bottom faces at Z0.00 within 0.02 mm. Nominal top and
   bottom seam step are both zero.
6. **Fastener reality:** instantiate eight actual-envelope M3x6 heads, shafts,
   and M3 nuts. Assert 4.90 mm captured stack, 1.10 mm thread projection, no
   hardware/plate collision outside intended holes/bearing faces, and clear
   D8 x 25 top driver plus D8 x 10 bottom nut-tool cylinders.
7. **Edge distance and spacing:** for every seam assert the numeric hole,
   head, nut, and 22.00 mm radial centre-spacing margins stated above using
   actual solid boundaries, not only parameter arithmetic.
8. **Closed-loop assembly path:** collision-sweep Q3, Q2, then Q1 from Z+6 mm
   to final in 0.25 mm increments while prior plates remain fixed. Q1 must seat
   both S12 and S41 in the same downward move. Also assert the precedence graph
   is acyclic; the rejected all-clockwise graph must fail this test.
9. **Reserved zone:** intersect every lap feature, screw envelope, nut envelope,
   and tool-access envelope with R118..150 and require zero positive volume.

## Physical gate

CAD does not prove FDM half-lap seating, support-surface cleanup, 1.25 mm layer
bearing strength, screw-preload resistance, seam slip, or assembled flatness.
Print one complete four-quadrant Q4-R3 base before adding motor, rings, or other
mechanisms. Record whether all four laps hand-seat, whether the final Q1 closes
without force, top/bottom seam step, flatness on a known plane, and seam slip
after repeated handling.
