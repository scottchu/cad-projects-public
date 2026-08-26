# P19 R1 cycle-3 four-millimetre focused repair 1

Status: **INFEASIBLE IN THE FROZEN THREE-VARIABLE SPACE.** The rejected
cycle-3 candidate is not repaired by changing only equal/opposite twist and a
common END translation. No 3D CAD, STEP, slicing, printing, force claim or
physical acceptance is authorized by this result.

Owner/role: `/root/p19_min_rail_optimizer`, mechanism/optimizer designer.
Frozen input: `REOPTIMIZE_4MM_INPUT.sha256`, verified `8/8` from the
repository root. The independent critique input is
`REOPTIMIZED_4MM_CRITIQUE.md`; its reviewed design fingerprint was
`d6054dc2813015259634638af948be059d74e338f817292a0715a7ec13e3c49c`.

## Corrected repair gate

The critic's service correction is applied as follows:

- all three named rods must have nonnegative rod-to-wire surface clearance at
  OPEN `u=0`;
- first contact state is reported for each rod;
- END may retain the selected `-0.250 mm` preload proxy;
- the wire line is re-derived from each candidate's END equal-pitch diagonal,
  rather than frozen at the rejected candidate's translated location.

The physical direction remains `+Z` mating-head/up and `+Y` short-tail,
tool/front/right. The complete triangle may not move backward relative to
repair 1, so `delta_END_Y >= 0`. The available short-tail centreline must stay
nonnegative. This is the numeric expression of the frozen front-edge/short-tail
service requirement; allowing negative `delta_END_Y` would solve a different
product direction by moving the clamp away from the short solder joint.

## Frozen geometry and equations

All coordinates are millimetres in FRONT YZ.

```text
C = (0,0)
A = (-13,-9), one real X-axis stepped axle through all four plates

OPEN_bottom   = ( 5.00, 10.00)
OPEN_diagonal = (20.40, 10.00)
OPEN_upright  = (20.40, -5.00)

END0_bottom   = ( 8.00,  9.00)
END0_diagonal = (14.25,  3.25)
END0_upright  = (20.50, -2.50)

END_i = END0_i + (deltaY,deltaZ)
p_i(u) = OPEN_i + u(END_i-OPEN_i)
alpha_left(u)  = -theta*u
alpha_right(u) = +theta*u
q_s,i(u) = R(-alpha_s(u)) p_i(u)
```

OPEN remains the exact ordered right angle `upper-left -> upper-right ->
lower-right`; END remains an exact ordered equal-pitch diagonal with both
vectors `(6.25,-5.75)`. Rod identities do not swap or cross. Every outer rail
is the exact inverse curve `q_s,i`; no rail is extended by hand.

The END pitch fixes the wire normal

```text
n = (5.75,6.25) / hypot(6.25,5.75)
  = (0.67705653,0.73593101)
F_bottom = END_bottom + 3.90*n
```

and the combined rod/wire radius is `4.15 mm`. With
`x = n dot (deltaY,deltaZ)`, the three OPEN signed centre distances are

```text
s_OPEN = (-5.19523858, +5.23143199, -5.80753318) - x.
```

Therefore simultaneous nonnegative OPEN clearance has exactly three allowed
projection branches:

```text
x <= -9.95753318
or -1.04523858 <= x <= +1.08143199
or x >= +9.38143199.
```

## Bounded search and infeasibility pressure

Only the already-authorized variables were searched:

```text
0.10 <= theta <= 45.00 deg
0.00 <= deltaY <= 9.109480 mm
-1.04523858 <= x <= +1.08143199 for the central OPEN-clear branch
deltaZ = (x - nY*deltaY) / nZ
```

The plate/rim gate bounds every rod centre to
`27.20 - 2.075 - 2.20 = 22.925 mm`. A constrained extremum over all three END
centres and `deltaY >= 0` gives

```text
minimum reachable x = -5.71218825
maximum reachable x = +9.25407914.
```

Thus the two extreme OPEN-clear branches are analytically excluded before any
rail search: `-5.71218825 > -9.95753318` and
`+9.25407914 < +9.38143199`. Only the central branch can preserve the plate
and front/short-tail constraints.

The central branch was searched deterministically in three stages:

1. full bounded grid: `theta=0.5..45 deg` by `0.25 deg`,
   `deltaY=0..9 mm` by `0.25 mm`, and `x` across the complete central interval
   by `0.10 mm`;
2. fixed-seed, multi-start continuous refinement with hard penalties for any
   rail `<4.00 mm`, inner/rim web `<2.20 mm`, or OPEN service violation;
3. active-boundary continuation across the complete central `x` interval,
   solving the two limiting travel equations
   `arc(left,bottom)=4.00` and `arc(right,upright)=4.00` at each projection.

The objective was to maximize the minimum left/right outer rail-to-rail web,
after satisfying all hard gates. The boundary continuation is monotone worse
away from the lower service boundary: limiting web decreases from
`1.405771 mm` at `x=-1.045239` to `0.510 mm` near `x=+0.933060` and continues
downward. No searched point reaches the required `2.20 mm`.

## Least-deficit witness (not a feasible design)

The global limiting witness is included so the failure is falsifiable. It is
not a candidate for 3D.

```text
theta = 9.88676759 deg per side
delta_END = (+1.48091079Y, -2.78273217Z)
x = -1.04523858
short-tail centreline = 7.62856874 mm
```

| rod identity | OPEN `(Y,Z)` | witness END `(Y,Z)` |
|---|---:|---:|
| `bottom` | `(5.000000,10.000000)` | `(9.480911,6.217268)` |
| `diagonal` | `(20.400000,10.000000)` | `(15.730911,0.467268)` |
| `upright` | `(20.400000,-5.000000)` | `(21.980911,-5.282732)` |

### Six exact inverse rails

Arc values were recomputed with `200,001` states. Full capsule aspect is
`(arc+4.15)/4.15`.

| outer / rod | centre arc | chord | capsule aspect | minimum crossing |
|---|---:|---:|---:|---:|
| left / `bottom` | `4.000000` | `3.969847` | `1.963855` | `0.000035 deg` |
| left / `diagonal` | `8.512810` | `8.461490` | `3.051279` | `8.766345 deg` |
| left / `upright` | `4.180355` | `4.173276` | `2.007314` | `63.093173 deg` |
| right / `bottom` | `7.744884` | `7.715237` | `2.866237` | `0.000018 deg` |
| right / `diagonal` | `13.209021` | `13.156401` | `4.182897` | `5.556764 deg` |
| right / `upright` | `4.000000` | `3.993576` | `1.963855` | `69.166679 deg` |

All six travel/aspect gates pass at the witness, but two crossings are
effectively tangent. That is an additional severe force/backlash risk, not a
way to waive the web failure.

### Web and service

| check | result |
|---|---:|
| fixed-inner rim | `2.405845 mm` |
| left/right outer rim | `2.555845 / 2.705845 mm` |
| fixed-inner rail-to-rail | `3.039674 mm` minimum |
| left outer rail-to-rail | `4.287073 mm` minimum |
| right outer rail-to-rail | **`1.405771 mm` minimum** |
| right diagonal-upright required web | `2.200000 mm` |
| right diagonal-upright deficit | **`0.794229 mm`** |
| axle-guide to rod-rail | `20.147505 mm` minimum |
| whole `8 x 8` tool outside OD55 tangent | `0.750000 mm` |

The right diagonal-upright pair is the decisive failure. Its closest cutter
envelopes leave only `1.405771 mm` of material; the frozen requirement is
`2.20 mm`.

OPEN wire states are now explicit:

| rod | OPEN signed centre distance | OPEN surface clearance | first contact `u` |
|---|---:|---:|---:|
| `bottom` | `-4.150000 mm` | `0.000000 mm` | `0.000000` (touching at OPEN) |
| `diagonal` | `+6.276671 mm` | `+2.126671 mm` | `0.208975` |
| `upright` | `-4.762295 mm` | `+0.612295 mm` | `0.710076` |

All three reach the selected `-0.250000 mm` END preload proxy. OPEN no longer
contains the critic's diagonal-rod penetration, but the limiting witness has
no positive assembly margin on `bottom`.

The four-contact probe retains rank `3` through `2,001` states. Worst
normalized conditions are `39.7594` left and `4.6084` right, both at END.
Together with the near-zero crossing angles, this is not evidence of usable
hand force, stiffness, friction or back-drive resistance.

## Delta versus the rejected cycle-3 candidate

| item | rejected cycle 3 | least-deficit witness | effect |
|---|---:|---:|---|
| twist per side | `5.000000 deg` | `9.886768 deg` | increased |
| END common delta | `(+2.25,+3.00)` | `(+1.480911,-2.782732)` | service repair |
| shortest rail | `4.212461 mm` | `4.000000 mm` | still meets hard gate |
| OPEN min clearance | `-2.649738 mm` | `0.000000 mm` | penetration removed |
| minimum outer web | `3.632161 mm` | `1.405771 mm` | now fails by `0.794229` |
| short-tail centreline | `6.859480 mm` | `7.628569 mm` | `+0.769089 mm` longer |
| shallowest crossing | `2.192572 deg` | `0.000018 deg` | materially worse |
| worst condition | `43.36` right | `39.76` left | still severe |

## Decision and smallest next variable

There is no corrected candidate in the frozen `theta + common END
translation` space. The 4 mm rail requirement, OPEN service clearance,
front/short-tail direction, OD54.4/54.7/55.0 plates and `2.20 mm` web cannot
all be satisfied simultaneously.

The ranked smallest numeric reopenings that could plausibly recover the
missing right diagonal-upright web are:

1. **Reopen only `OPEN_upright_Z`, downward.** This preserves the exact OPEN
   vertical leg, ordered right-angle topology, all identities, END equal pitch,
   `C`, `A`, plates and service direction. At the limiting witness the closest
   pair is right-diagonal at `u=0.996` versus upright at OPEN `u=0`; their
   centre distance is `5.555771 mm`, while `6.350000 mm` is required for an
   OD4.15 pair plus `2.20 mm` web. Holding that witness fixed gives a geometric
   lower bound of approximately **`1.357388 mm` downward** on
   `OPEN_upright_Z`. The new OPEN upright radius would still leave about
   `3.757 mm` fixed-inner rim web before re-optimization. This is the most
   local plausible reopening, but it is not a solved candidate: the six rails,
   OPEN contacts, crossing and conditioning must all be re-optimized.
2. **Reopen one common END-pitch scale `lambda` while preserving its direction
   and equal-pitch identity.** At the witness, a static first estimate is
   `delta_lambda=-0.100262`, shortening each `8.492644 mm` pitch by about
   **`0.851485 mm`**. This can move the right-diagonal END away from upright
   OPEN, but it changes both diagonal and upright END coordinates and the
   derived wire/contact line, so it is broader than option 1 and must be
   recomputed rather than applied as a patch.
3. **Reopen rotation centre `C` only if the two shape parameters fail.** At
   `theta=9.8868 deg`, an END rail point responds to a centre shift by at most
   `2 sin(theta/2) = 0.17236` times that shift. Recovering the static
   `0.794229 mm` centre-distance deficit therefore needs at least about
   **`4.61 mm` of optimally directed C motion** before considering other
   constraints. It also perturbs all six rails and the axle guide, so it is a
   materially broader repair.

Increasing plate OD alone cannot repair this failure because the decisive
constraint is rail-to-rail web, not rim web. Allowing common negative
`delta_END_Y` can create numerical solutions only by moving the clamp backward
and lengthening the short tail, contradicting the frozen product direction;
it is not a valid option here. None of the ranked quantities is an authorized
design change or a feasibility claim. A new bounded repair task must select
one variable, re-optimize, and independently review it. Until then the active
P19 2D candidate remains blocked.

Review artifact:
`docs/review/p19-r1-front-edge-short-tail/reoptimized-4mm-repair1-infeasible.png`.
