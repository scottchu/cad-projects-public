# KAGE B0 Q4-R2 screw-only base — design handoff

Status: **DESIGN PROPOSAL — no CAD implementation authorized by this document**  
Date: 2026-08-19  
Successor namespace: `p3_v3_mvp_base_q4_r2_screw_only`  
Predecessor: locked `p3_v3_mvp_base_q4_r1`, preserved byte-for-byte

## Decision

Yes, the existing Q4-R1 underside bridge should become the screw-only clamp.
Keep one clamp per seam and one screw through each adjacent quadrant: four
clamps and eight M3 screws total.

Remove all steel/printed loose dowels, clamp press bores, dowel occurrences,
BOM rows, and dowel validation. Preserve the locked Q4-R1 quadrants exactly,
including their existing R78 round split hole and R108 radially relieved split
slot. Replace the clamp's two press bores with two short integral printed
locating bosses on those same axes. The two bosses, separated by 30 mm, locate
the seam and resist yaw; the screws supply clamp force only.

This is the smallest credible successor: existing Q4-R1 quadrant prints remain
usable, only the four clamps change, the captive-nut strategy stays, and there
are no new loose printed parts.

## Locked inputs

| Input | SHA-256 |
|---|---|
| `p3_v3_mvp_base_q4_r1_spec.py` | `9235d8f10d9802382d63981dd1cb95307013f49b03fbe723ae34891d7a35f35e` |
| `p3_v3_mvp_base_q4_r1_geometry.py` | `2c989ed42de710f3a133bd7c854e36b58bc508fcfc91559f35037621838228e9` |
| `p3_v3_mvp_base_q4_r1_validation.py` | `32a9674490b22e1de25e90b198859de409dc8b1e4f9f3da4584167590f2ba12b` |
| `models/p3_v3_mvp_base_q4_r1/p3_v3_mvp_base_q4_r1_assembled.step` | `e93ad8295c427210586c3cf72d7e7157b26d01f467f848f75186548ea1f2db33` |

Implementation, if separately approved, must create new R2 spec/geometry/
export/test files and `models/p3_v3_mvp_base_q4_r2_screw_only/`. It must not
edit, overwrite, or regenerate any Q4-R1 source or artifact.

## Frozen base and print envelope

Coordinates remain: XY clock plane, +Z front/viewer, base underside Z=0,
front Z=2.50.

| Parameter | Value |
|---|---:|
| `base_outer_diameter_mm` | `300.00` |
| `base_inner_diameter_mm` | `132.00` |
| `base_thickness_mm` | `2.50` |
| `quadrant_count` | `4` |
| `quadrant_angle_deg` | `90.00` |
| `seam_base_angle_deg` | `45.00` |
| `seam_relief_per_face_mm` | `0.05` |
| `seam_gap_nominal_mm` | `0.10` |
| `u1_bed_xy_mm` | `270.00` |
| `u1_edge_keepout_mm` | `5.00` per edge |
| `u1_usable_xy_mm` | `260.00` |
| `quadrant_brim_mm` | `5.00` per side |
| `future_support_clear_radius_mm` | `R118.00..150.00` |

Each quadrant is the exact locked Q4-R1 BREP, not a remodeled approximation.
Preserve its one-solid structure, D3.40 screw holes, R78 D4.15 round split
feature, R108 5.15-radial x4.15-tangential relieved split feature, and
front-face-down printing. The Q4-R1 measured maximum span with brim,
approximately 222.061 mm, remains below the 260 mm usable bed.

## Screw-only clamp with integral registration

One identical clamp is centered on every seam at R93. Its local X axis is
radial and local Y axis tangential.

| Named parameter | Value |
|---|---:|
| `clamp_count_total` | `4` |
| `clamp_radial_min_mm` | `69.00` |
| `clamp_radial_max_mm` | `117.00` |
| `clamp_radial_mm` | `48.00` |
| `clamp_tangential_mm` | `26.00` |
| `clamp_body_thickness_mm` | `5.00` |
| `integral_boss_count_per_clamp` | `2` |
| `integral_boss_axis_radii_mm` | `(78.00, 108.00)` |
| `integral_boss_diameter_mm` | `4.00` |
| `integral_boss_height_mm` | `2.40` above clamp top |
| `integral_boss_tip_chamfer_mm` | `0.20 x45deg` |
| `round_split_feature_diameter_mm` | `4.15`, inherited Q4-R1 |
| `relieved_split_feature_radial_mm` | `5.15`, inherited Q4-R1 |
| `relieved_split_feature_tangential_mm` | `4.15`, inherited Q4-R1 |
| `round_boss_diametral_clearance_mm` | `0.15` |
| `relieved_boss_radial_clearance_mm` | `1.15` |
| `relieved_boss_tangential_clearance_mm` | `0.15` |
| `boss_front_recess_mm` | `0.10` below base front face |

At assembly, the clamp body occupies Z=-5.00..0.00 and both integral bosses
occupy Z=0.00..2.40, ending 0.10 below the base front face. The R78 boss seats
in the round split feature and fixes radial/tangential translation. The R108
boss seats in the existing radial capsule: its 0.15 tangential clearance
controls yaw while its 1.15 radial relief absorbs printed radial shrink. Broad
clamp top faces contact both quadrant undersides and establish Z.

The integral bosses are printed as part of the one-solid clamp. They are
locators, not clamp-force members. Do not add serrations, new pockets,
dovetails, loose keys, printed threads, glue, or any part called a pin/dowel.
If fit fails physically, tune only the named boss diameter after a coupon; the
locked quadrant features remain unchanged and the complete four-piece base
still decides acceptance.

## M3 hardware and receivers

Use the user's common socket-head assortment:

- **8 x M3x6 ISO 4762 socket-head cap screws**, fully threaded;
- **8 x ISO 4032 M3 standard hex nuts**, nominal AF5.50, maximum thickness
  2.40;
- 2.5 mm hex key;
- **no dowels or pins of any kind**.

| Named parameter | Value |
|---|---:|
| `screw_count_per_clamp` | `2` |
| `screw_count_total` | `8` |
| `screw_axis_radius_mm` | `93.00` |
| `screw_tangent_offsets_mm` | `-7.00, +7.00`, inherited Q4-R1 |
| `base_screw_clearance_diameter_mm` | `3.40` |
| `m3_socket_head_max_diameter_mm` | `5.50` |
| `m3_socket_head_nominal_height_mm` | `3.00` |
| `nut_count_total` | `8` |
| `nut_pocket_af_mm` | `5.80` |
| `nut_pocket_depth_mm` | `2.70`, open at clamp top |
| `screw_tip_relief_diameter_mm` | `3.40` |
| `screw_tip_relief_depth_mm` | `1.30` below nut-pocket floor |
| `clamp_bottom_skin_mm` | `1.00` minimum |
| `driver_access_diameter_mm` | `8.00` |
| `driver_access_height_mm` | `25.00` above front face |

Each clamp has one captive nut for each screw. A screw passes from +Z through
one quadrant and threads into the nut in the common clamp; the other screw does
the same through the adjacent quadrant. At worst stack, M3x6 traverses 2.50
base +0.30 nut slack +2.40 nut =5.20, leaving 0.80 in the blind tip relief.
It therefore achieves the full 2.40 nut engagement without needing M3x8, whose
extra length would consume the 1.00 bottom skin. M3x5 is too short once the
0.30 nut slack is included.

The nut pockets and blind tip reliefs remain the exact Q4-R1 clamp cuts. Fuse
the two bosses where the old press bores were; they do not overlap either nut
pocket. Hardware reference solids are optional in print exports but mandatory
in the assembled validation STEP.

## Assembly order

1. Reuse or print the locked Q4-R1 Q1–Q4 front-face down with 5 mm brim. Print
   new C1–C4 clamps bottom-down; integral bosses and nut pockets face upward.
   No support in pockets or screw reliefs.
2. Load two ISO 4032 M3 nuts into each clamp from its open top. Confirm flat,
   nonspinning seating.
3. Support all four quadrants front-face up in their final XY positions with
   every seam accessible from below.
4. Insert C1, C2, and C3 upward from below into the inherited split features.
   Add one M3x6 screw through each adjacent quadrant and leave both loose.
5. Insert C4 upward from below as the last clamp while all four quadrants stay
   in final XY. Do not attach C4 to Q4 and lower Q4.
6. Confirm eight screws present and loose. Put the four clamp bottoms on a
   verified plane. Tighten finger-snug in C1, C3, C2, C4 order, repeating the
   sequence once. Do not use screw torque to force a boss into a pocket or pull
   an open seam closed.
7. Remove from the plane and measure free-state seam alignment and flatness.

The integral bosses remove pin purchasing, pin pressing, and loose-pin service;
all clamp insertion is straight upward and reversible with one hex key.

## Meaningful CAD tests only

Keep the successor suite compact; the following seven tests are sufficient.

1. **Four-piece bed fit and solidity.** Exactly Q1–Q4; each is one valid solid.
   Each actual oriented AABB plus 5 mm brim fits the 260 mm usable U1 square.
2. **Exact screw-only registry.** Exactly four printable clamps, eight integral
   bosses, eight screw interfaces, and eight nut receivers. There are zero
   loose pin/dowel occurrences, press bores, purchased pins, or dowel BOM rows.
   The inherited quadrant split features are classified as integral-boss
   receivers, never as hardware. A loose D4 occurrence or ninth screw fails.
3. **Screw stack and access.** Actual M3x6 shafts, ISO 4762 heads, ISO 4032 nuts,
   D3.40 base holes, captive pockets, and blind tip reliefs have intended
   clearance/engagement. All eight D8x25 driver cylinders are unobstructed.
   M3x5 must fail engagement and M3x8 must fail bottom-skin/tip containment.
4. **Actual-solid boss/receiver fit.** At all four seams the D4 integral bosses
   have zero unintended positive-volume intersection with the inherited round
   and relieved split receivers; named radial/tangential clearances are
   measured from actual faces. Clamp top faces contact both quadrant
   undersides, nut openings stay open, and every clamp/quadrant is one solid.
5. **Seam registration sensitivity.** Nominal assembled seam gap is 0.10 and
   front step is zero in CAD. Translate either adjoining quadrant 0.20 mm
   tangential, or rotate it 0.20 degrees about the base centre in separate
   negatives; the same boss/receiver evaluator must reject loss of
   clearance/contact or positive-volume interference. Bounding boxes alone do
   not count.
6. **Assembly path.** Prove straight-up C1–C3 and last-clamp C4 insertion with
   all four quadrants already in final XY. Reject the old Q4-with-attached-C4
   lowering path and any path requiring quadrant bending or screw preload.
7. **Reserved-zone clearance and locked isolation.** Actual clamp, integral
   boss, inherited receiver, screw, nut, and driver geometry stays below R118;
   R118..150 remains free for later support cartridges. Successor quadrant
   BREP digests equal Q4-R1 exactly, frozen Q4-R1 hashes remain unchanged, and
   every changed R2 output is under the new namespace.

CAD acceptance proves nominal registration geometry, access, solids, and
clearances. It does not prove printed boss fit, screw preload, seam slip,
free-state flatness, or handling durability. Those remain a new complete-base
physical gate; do not infer them from Q4-R1's dowel-based result.
