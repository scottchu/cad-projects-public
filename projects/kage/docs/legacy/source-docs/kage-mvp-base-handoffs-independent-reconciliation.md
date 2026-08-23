# KAGE MVP base handoffs — independent reconciliation

Status: **REVISE — accept the base-first gate, not either handoff unchanged**  
Date: 2026-08-19  
Scope: read-only design review; no CAD modified

Reviewed inputs:

- `p3-v3-mvp-base-q4-r0-design-handoff.md`, SHA-256
  `3ff2073e1eb5247ee1cc1ab7c0001ad1cc885b6d350d1c78ba097406de10b67a`;
- `kage-mvp-track-b-hard-mechanics-handoff.md`, SHA-256
  `e623675bf6d068957b65aa55bef159dba0423e3f9808992085e99c272682fb63`.

## Verdict

The Q4-R0 base-first boundary is correct. Track B's B1 is not the first MVP
gate because it combines four independent unknowns: base closure, ring
closure, roller guidance, and pinion mesh. Split them so a failure has one
owner:

1. B0: four-quadrant base only;
2. B1-P: one complete ring, rim-pushed on three supports;
3. B1-D: add one base-mounted manual pinion;
4. B2: passive three-ring stack.

Q4-R0 should not be released exactly as written. Eight separate bridges and
16 screw/nut pairs are unnecessary for the B0 question, add eight printed
height stacks to the coplanarity problem, and place an outer bridge at R138 in
the annulus later support cartridges will need.

## Exact Q4-R0.1 revision

Keep these values:

- OD 300.00, R150 outer, R66 inner, thickness 2.50;
- four 90-degree quadrants cut from one full source annulus;
- 0.05 relief per opposed seam face, 0.10 nominal total seam gap;
- M3x6 button-head screws, ISO 4032 M3 nuts, D4x6 steel dowels;
- D3.40 screw clearance, 5.80 AF x2.70-deep top-open nut pockets;
- D3.95 bridge press bores, 3.50 press engagement;
- 4.15-wide base slip feature, 2.50 engagement;
- D8 x25 driver-access cylinders;
- 270 bed, 5 edge keepout, 260 usable square, 5 brim per side.

Change the following:

| Parameter | Q4-R0.1 value |
|---|---:|
| `seam_base_angle_deg` | `45.00` |
| `bridge_count_per_seam` | `1` |
| `bridge_count_total` | `4` |
| `bridge_radial_extent_mm` | `R69.00..117.00` |
| `bridge_radial_mm` | `48.00` |
| `bridge_tangential_mm` | `26.00` |
| `bridge_thickness_mm` | `5.00` |
| `screw_axis_radius_mm` | `93.00` |
| `screw_tangent_offsets_mm` | `-7.00, +7.00` |
| `round_dowel_axis_radius_mm` | `78.00` |
| `relief_dowel_axis_radius_mm` | `108.00` |
| `relief_split_slot_radial_x_tangent_mm` | `5.15 x 4.15` capsule |
| `m3_screw_count_total` | `8` |
| `m3_nut_count_total` | `8` |
| `d4_dowel_count_total` | `8` |
| `future_support_clear_annulus_mm` | `R118.00..150.00` |

The bridge carries one screw on each side of the seam and two seam-centred
dowels. The R78 dowel uses the round D4.15 split slip bore. The R108 dowel uses
a radial capsule, 5.15 overall radial by 4.15 tangential, so it still controls
tangential yaw but allows +/-0.50 radial print/shrink mismatch. This is a
round-plus-relieved registration pair, not two rigid pins fighting a closed
four-seam tolerance loop.

Each nut pocket remains open at the bridge top. Under it, use a blind D3.40 tip
relief 1.30 deep from the pocket floor, leaving 1.00 minimum bridge bottom
skin. Do not use an unexplained through relief: M3x6 needs only 0.80 to 1.10 of
tip space after the 2.50 base, 0.00 to 0.30 pocket slack, and 2.40 nut.

This revision reduces the base from 52 assembled items to 32:

- four base quadrants;
- four bridges;
- eight screws;
- eight nuts;
- eight dowels.

It retains two-point seam registration and one clamp into each adjacent
quadrant at every seam. It also reduces the coplanarity references from eight
independent bridge bottoms to four.

## Geometry and bed checks

The original 37.5-degree bed calculation is correct:

- clean quadrant maximum: 210.317215 x109.821746;
- with 5 brim per side: 220.317215 x119.821746;
- both are below the 260 usable-bed limit.

The revised 45-degree seam also fits without a packing trick:

- clean quadrant maximum: 212.132034 x103.330952;
- with 5 brim per side: 222.132034 x113.330952;
- remaining margin is at least 37.867966 on the limiting usable-bed axis.

Use 45 degrees because, for the later station angles 0, 60, 180, and 300, it
increases the minimum seam-centre separation from 7.5 to 15 degrees. More
importantly, all base joinery ends at R117, leaving R118..150 continuously free
for later through-bolted roller and pinion cartridges. Do not guess their hole
pattern in B0; B1 must define it before claiming that the same physical B0
print can be reused.

## Assembly access and coplanarity

Assembly access is valid only in the bare-base state. All eight screw axes must
retain the stated D8 x25 +Z driver envelope. Future B1 parts must either leave
those envelopes accessible or be removable before base service.

Assemble with the four bridge bottoms on a verified plane, tighten in a
cross-seam sequence, remove the assembly from that plane, wait one hour, and
then measure the functional front face free-standing. Fixture-constrained
flatness is not a pass. CAD must have all bridge seat tops coplanar and every
quadrant front datum coplanar, but printed free-state front deviation remains
the existing 0.50 physical gate.

Each quadrant must be exactly one connected positive-volume solid after seam
relief and all split holes/slots. A compound with two solids is RED even if its
AABB, area, or assembled union is correct.

## Later B1 interface boundary

The revised joinery reserves rather than designs the B1 interface:

- no bridge, nut pocket, dowel, screw axis, or driver keepout may enter
  R118..150;
- keep solid printable base material at the station sectors centred on
  0, 60, 180, and 300 degrees;
- B1 owns the exact through-hole/slot pattern, backing plates, and radial
  adjustment geometry;
- B1 support loads must use through-bolts/backing features, not printed threads
  in the 2.50 base;
- B1 must recheck seam, bridge, tool, and support clearances as actual solids.

Therefore Q4-R0.1 is a reusable CAD architecture, but the first B0 print is not
automatically a reusable B1 article until the support-hole pattern exists.

## Track B reconciliation

Track B's tooth-profile warning and single-source roller requirement are sound,
but both belong after B0. Its four-quadrant moving ring is not accepted merely
because the base uses four quadrants. Ring segment count must be chosen from
actual 270-bed slicer envelopes and tooth-phase risk; do not double moving-ring
seams unless two halves demonstrably fail the bed contract.

Likewise, the pinion must not enter the passive guidance gate. First rim-push a
complete ring across every support seam event; then add the rigidly
base-mounted hand pinion and attribute any new force peak to mesh.

## Release decision

**REVISE, then ACCEPT for CAD implementation of B0 only.** The implementation
may proceed when Q4-R0.1 owns the exact values above, keeps each quadrant one
solid, and includes one deliberate negative for coplanarity/registration. Do
not release B1-P CAD until the full printed B0 passes free-state flatness,
last-seam closure, vertical self-weight dwell, and three assembly cycles.

