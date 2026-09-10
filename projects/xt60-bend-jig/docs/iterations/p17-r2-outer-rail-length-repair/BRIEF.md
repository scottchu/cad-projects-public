# P17-D12-R1 outer-rail effective-length repair

Status: `DESIGN FROZEN`; implementation and physical acceptance pending. This
is a P17 R2 numeric placement refinement, not a new version.

## User correction

The rejected D12 seed still showed one long and one short rail, especially
Rod 2 (`upright`, ratio `2.012551`). D12-R1 therefore optimizes the functional
OPEN-to-END centerline length on both outer plates. The functional length is
the locus occupied by the rod center for `0<=u<=1`; the `2.075 mm` rounded
slot ends outside the terminal centers are closed boundaries, not travel.

## Frozen R1 correction

- Fixed axle `A=(-29.00,17.00)` and physical outer datum `C=(3.00,12.00)` stay
  unchanged.
- Supersede D12 `T=(-7.00,-6.50)` with one complete-working-set translation
  `T=(-16.735,-14.935)` in world `(Y,Z)`.
- The functional relative datum becomes `C_rel=C-T=(19.735,26.935)`.
- Keep linear `beta(u)=24u deg` and left/right outer angles `-beta/+beta`.
- Keep the rail topology and `4.15 mm` section, straight inner-track directions
  and lengths, all relative rod triangles, identities, and XT60/wire-to-rod
  geometry unchanged.

The exact symmetric point `C_rel=(22.235,24.435)` gives three perfect `1.0`
ratios but fails actual-solid web (`-0.304997`) and fixed-feature/keeper
clearance. Along the smallest repair direction
`C_rel=(22.235-d,24.435+d)`, the `0.01 mm` frontier first reaches nominal
`2.20 mm` web at `d=2.45`; R1 selects `d=2.50` to retain `0.047514 mm`
digital margin. Its maximum rail-length ratio is `1.304701`, below the user
target `1.50`, and all actual-solid gates pass.

## Preserved architecture and claims

- Front frame remains `+Z` XT60 head/up and `+Y` tails/wires/right.
- OPEN remains upper-left / upper-right / lower-right with exact right vertical
  leg; END remains upper-left / middle / lower-right, with no role swap.
- Two fixed inner plates, two counter-rotating outers, larger right force plate,
  one axle, two keepers, three `OD4 x 50 mm` rods and six permanent caps.
- No bar, link, yoke, gear, added lock, layered rail, widened slot or new part.
- “Locked” means CLAMPED/END only. No self-lock, retention, hand-force or
  physical-fit claim is made before physical testing.

## P17-D12-R2 superseding placement repair

Status: `DESIGN FROZEN`; this section supersedes only the D12-R1 translation
and its six derived outer rails. It remains P17 R2.

The I10 review images show the entire rod/workpiece/rail working set too far
screen-left and down, leaving a large unused upper-right plate region. Front
view is fixed as `+Y` screen-right and `+Z` screen-up. R2 replaces
`T=(-16.735,-14.935)` with:

```text
T = (-12.350,-10.550)
delta from I10 = (+4.385,+4.385)  # right, up
C_rel = C - T = (15.350,22.550)
```

This is the largest responsible rounded balanced correction found in the final
bounded search. The analytic frontier `T=(-12.300,-10.500)` gains only another
`0.05 mm` per axis but leaves merely `0.0289 deg` above the final `8 deg`
crossing-angle diagnostic floor; R2 keeps `0.1668 deg` margin. A more aggressive
`T=(-12,-7)` is rejected because the diagonal falls to `2.968 deg`. The
up-biased `T=(-15.5,-9.275)` is rejected because minimum web is only
`1.282 < 2.20`.

R2 preserves physical `A=(-29,17)`, physical `C=(3,12)`, four plate envelopes,
all relative OPEN/contact/END triangles, all three straight inner tracks,
linear opposite `-24u/+24u` outer motion, `4.15` slots, all three OD4 x 50 rods,
six caps, larger right force side, service sequence and every part count. All
six outer rails must be regenerated from the inverse transform; no old rail
solid may be translated or reused.

The worst full and contact-to-END left/right length ratios are respectively
`1.405804` and `1.514484`. The latter intentionally exceeds the preferred
`1.50` by `0.014484` because visible placement is the user-prioritized defect.
Minimum contact-to-END crossing angle is `8.166759 deg`; this is only a
frictionless geometry diagnostic. No physical hand-force, clamp-force,
self-lock or retention claim is authorized.

## P17-D12-R3 superseding fixed-axle placement repair

Status: `DESIGN FROZEN`; this section supersedes only the fixed purple axle
datum, its two inner hex bores, two outer fixed-axle guide rails and two keeper
locations. R2 working-set `T`, all six stainless-rod rails and every moving
state remain unchanged. This remains P17 R2.

The user-marked target is the central-right diagonal empty band, not the old
far-left axle position and not the upper-right rim. The nominal band target
`A0=(17,12)` (`A0-C=(14,0)`) is infeasible: minimum required web is
`-0.014196 mm`. The nearest nominal pass `A=(19,11)` has only
`0.021355 mm` margin above the `2.20 mm` gate and is rejected as
threshold-fragile. Freeze:

```text
C = (3.000,12.000)                 unchanged
A = (19.250,11.000)                selected fixed purple axle
A - C = (16.250,-1.000)
delta from I11 A=(-29,17) = (+48.250,-6.000)
distance from marked A0 = 2.462214
```

The selected point follows the marked down-right band while remaining central,
not at the plate rim. It is `9.115 mm` above the horizontal solder-tail/wire
reference `Z=1.885`, placing the axle on the head/back side of that corridor.

Both fixed-axle rail centerlines are `6.819660489 mm` analytic arc length.
Minimum web is `2.447634 mm`; minimum exact feature gap is `3.040481 mm`;
fixed axle/keeper to XT60/service clearance is `1.213238 mm`. All actual-solid
axle, keeper, plate, cap, rod, XT60/wire and service collision gates pass.
Fixed-frame invariance and conditioning pass. No part, plate, slot width,
motion law, workpiece, rod rail, lock or physical-force claim changes.

## P17-D12-R4b final fixed-axle placement

Status: `DESIGN FROZEN`; implementation, independent review and physical
acceptance remain pending. This supersedes the rejected R3 datum
`A=(19.25,11)`, temporary far-left restore `A=(-29,17)` and upper-right R4
preview `A=(24,20)`. It remains a focused P17 R2 placement repair.

Root visual inspection selected the true center-right point below because it
uses the empty horizontal band without occupying or squeezing the stainless-
rod working area:

```text
C = (3.000,12.000)                 unchanged outer-rotation datum
A = (30.000,12.000)                frozen fixed purple axle datum
A - C = (27.000,0.000)
```

Only `A`, the two inner fixed hex bores, the two inverse-frame outer
fixed-axle guides and the two keepers are reopened. D12-R2 `T`, XT60/workpiece,
OPEN/contact/END rod states, straight inner tracks and all six stainless-rod
rails remain exact geometric inputs with digest
`a13a2cb0deef4c08b20bbd690b8cc74e377cd0f750810c0f86781ed1d09a1e58`.

Front-view truth remains `+Z` head/up and `+Y` tail/wires/right. `FRONT` is
authoritative; `OPPOSITE` is only a mirrored review view and must not reverse
the physical coordinate convention, rod identities or motion signs.

Read-only actual-solid evidence clears the frozen axle/keeper envelope from
all rods and caps through `65` motion states by at least `11.903129708 mm`.
Minimum web is `8.294595306 mm`, minimum XT60/wire/service clearance is
`2.965 mm`, fixed-guide support is continuous through `+0.30 mm`, and all
unintended intersections are zero. The axle and keepers remain fixed in world
coordinates across every state plus exact contact.

No physical PETG fit, keeper retention, wear, hand force, wire-holding force,
self-lock or printed acceptance is claimed. No rod, rail, plate envelope,
slot width, motion law, bar, yoke, linkage, gear, added lock or new part is
authorized by this repair.
