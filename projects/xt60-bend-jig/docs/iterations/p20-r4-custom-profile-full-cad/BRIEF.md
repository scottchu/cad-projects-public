# P20 R4 custom-profile full CAD preview brief

Date: `2026-08-27`

Status: **FROZEN FOR FULL-ASSEMBLY INTENT PREVIEW ONLY**

Owner/role: `/root/p20_final_design`, design contract owner. This role does
not implement or approve its own design.

## Outcome and boundary

Create the complete P20 assembly from the user's last accepted `GREEN 0 ·
BLUE→GREEN` 2D customizer default. The review artifact must be the whole jig,
not the Blue–Orange coupon and not P20 R3's zero-white-rod-outer-rail
intermediate. It must visibly contain four plates, three `OD4 x 50 mm` rods,
six caps, the fixed stepped axle and its two keepers, the XT60 reference and
the exact P20 R3 90-degree workpiece.

This iteration authorizes STEP-first CAD and review snapshots solely so the
user can verify the final-design topology, orientation, rails and full
assembly. It does **not** authorize mesh, 3MF, slicing, printing or physical
acceptance. The earlier Blue–Orange coupon is separate evidence and is not an
assembly baseline.

## Immutable input manifest

Manifest algorithm: the following lines are sorted by path, encoded UTF-8 with
one LF per line as `<sha256><two spaces><path>`. Aggregate SHA-256:
`4286336b7709980f7d9ec4d22bb3f54f262639b88d3b3a7a1dba36b9e48b0691`.

```text
1f7cae7260871f2ba54e663ebf24aaa01a5bdef69e5c0a40e6524736846558cc  /Users/scottchu/.codex/visualizations/2026/08/26/01a03fb3-e479-7562-b8ff-8baec6a79b6b/inner-outer-rails-3d.html
4b23ae3a0c65fb861e1215e95ba435b5747d2d3c4f085a6e07a925af37263f5c  projects/xt60-bend-jig/docs/EXPERIENCE.md
07e86ede330777bca4f1d9975604024aada7fdf7e3d7b261bc524135cfc3cc82  projects/xt60-bend-jig/docs/REQUIREMENTS.md
d07b20ce105c0d1b7fe3a5568ef2ed3b8ebb4524f72181f7e381f3d48600296a  projects/xt60-bend-jig/docs/iterations/p20-r3-wire-90deg/BRIEF.md
fc23e908385b482cd7b6b729d1c99ec20087e90dbde9f04e970564e4108c75aa  projects/xt60-bend-jig/docs/iterations/p20-r3-wire-90deg/IMPLEMENTATION.md
34be78a4d7a5a3905c25d5d8144e7a1580e52fcab0e3d85d3272e40466cea7fe  projects/xt60-bend-jig/docs/iterations/p20-r3-wire-90deg/ROD_CAP_PLATE_GAP_CONSTRAINT.md
41c06b8536fbf4e1bb2e9979d74de299232379b4b0ebf87ee81e93c63f581017  projects/xt60-bend-jig/src/xt60_bend_jig/p19_r1_front_edge_short_tail.py
1b004ac07fbd3f8ff2f776b3219c5b98e50825b123e1ec3410683d61134baa73  projects/xt60-bend-jig/src/xt60_bend_jig/p20_r2_fixed_rod_arc_rail.py
91107a87b4d36f6829c7175f2030a3e2c2911784b9495083af2033d561642b71  projects/xt60-bend-jig/src/xt60_bend_jig/p20_r3_wire_90deg.py
```

Baseline Git HEAD is `9698cf30e9ddb3e576c08179bfdd067446514c67`.

## Exact customizer profile

The canonical compact JSON has SHA-256
`7a8013c935c74df865b3bd861ec163a00725e86f0e27415489babd26cd85eeb0`.

```json
{"rods":[{"name":"bottom","startAngleDeg":118,"startRadiusMm":16,"archMm":0},{"name":"diagonal","startAngleDeg":45,"startRadiusMm":16,"archMm":0},{"name":"upright","startAngleDeg":-23,"startRadiusMm":16,"archMm":0}],"endOffset":{"yMm":-7.3241343806549555,"zMm":-2.77402040577638},"pathSteps":360,"archPeak":0.5,"curveBias":0,"innerPlateRadiusMm":20,"outerPlateRadiusMm":22.5,"fixedAxle":{"yMm":-10,"zMm":-10,"leftTravelDeg":45,"rightTravelDeg":-45,"guideWidthMm":7.9},"whiteRodCutterDiameterMm":4.15}
```

The shared END offset is applied to the three P19 END base points. All three
inner paths use the same pure path authority. Each outer path is its complete
inverse-frame image; no outer path may be shortened, replaced by an endpoint
hole or omitted.

## Frame and state topology

- Units: millimetres.
- Assembly axis/plate stack: `X`.
- FRONT plane: `YZ`; `+Z` is XT60 mating-head/up and `+Y` is wire-tail/outward-right.
- Outer rotation center: `C=(Y0,Z0)` for both sides.
- Fixed stepped axle: world-stationary `A=(Y-10,Z-10)`.
- OPEN/MID/END normalized state: `u=0/0.5/1`.
- Physical plate motion: left `+45u deg`, right `-45u deg` about `C`.
- The inner plates, stepped axle, keepers, XT60 and 90-degree workpiece remain
  world-fixed. Rod centers follow the inner trajectories. Outer-plate local
  cuts are inverse-derived so forward plate motion reconstructs the same rod
  world positions.

## Object census and axial stack

The full review assembly has exactly `18` labeled occurrences:

- four plates: left outer, left inner, right inner, right outer;
- three `OD4.00 x 50.00 mm` stainless rods;
- six permanent rod caps, one at each rod end;
- one stepped fixed axle and two permanent outer keepers;
- one XT60 reference and one two-conductor exact 90-degree workpiece.

For this preview, preserve the current P19/P20 R3 axial geometry exactly:
inner clear span `18.40`, plate thicknesses `3.20`, inner/outer running gap
`0.40`, left/right inner plate centers `X=-10.80/+10.80`, outer centers
`X=-14.40/+14.40`, rod length `50.00`, cap head length `9.05`, cap engagement
`8.70`, and axle length `34.90 mm`. The user's requirement to minimize cap
height and maximize clear plate gap is recorded in
`ROD_CAP_PLATE_GAP_CONSTRAINT.md`; no unapproved replacement target is invented
here. The preview must expose the existing caps and gap honestly.

## Rail ownership

- Both fixed inner plates: complete Blue and Orange `4.15 mm` rails; Green is
  an exact `4.15 mm` round bore because its inner center travel is numerically
  zero (`~2.1e-13 mm`).
- Left outer: complete inverse-derived Blue, Orange and Green `4.15 mm` paths,
  plus the fixed-axle `7.90 mm` inverse arc.
- Right outer: complete inverse-derived Blue, Orange and Green `4.15 mm`
  paths, plus the fixed-axle `7.90 mm` inverse arc.
- The previous transient suggestion to omit the left-Green outer path is not
  part of this exact profile. Removing it would require a separate motion,
  collision and support-path reopening.

## Explicit non-goals

- No coupon substitution or coupon result promoted to whole-jig acceptance.
- No cap shortening, rod shortening, plate-stack optimization or XT60 move.
- No rail deletion, one-at-a-time rail experiment, centered axle, lock,
  detent, yoke or support bar.
- No mesh, 3MF, slicing, upload, print, force/friction, heat, wear or physical
  claim.

## User intent gate

The required review surface is the full assembly in OPEN, MID and END plus an
exploded/axial view. The user must be able to answer one question: **Does this
complete assembly match the accepted 2D profile—correct orientation, all
three rods, all inner and outer paths, fixed rod/rails, caps, plate stack and
90-degree XT60 wire—before any manufacturing work continues?**

