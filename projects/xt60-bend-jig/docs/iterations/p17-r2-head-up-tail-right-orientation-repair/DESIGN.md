# P17-D10 corrected head-up / tail-right design contract

Status: selected numeric contract; source and artifact implementation pending.

## Coordinate and workpiece contract

All dimensions are millimetres. Stainless rods run on `X`; front-view motion
is world `YZ`, where `+Y` is right and `+Z` is up.

The nominal OD4.30 wire centerline is a `└`:

```text
bend center B = (16.235, 18.435)
bend radius R = 6.000
vertical leg:   Y = 10.235, extending upward (+Z)
horizontal leg: Z = 12.435, extending right (+Y)
quarter arc: left tangent (10.235,18.435) to bottom tangent (16.235,12.435)
```

The XT60 mating head is on the upward leg; both solder tails leave right. The
two wires share this `YZ` definition and remain separated only along `X`.

With rod radius `2.00` and wire radius `2.15`, first tangency is at offset
`d_t=4.15`. END uses `d_e=3.90`, exactly `0.25` further geometric travel as a
preload proxy; it is not a force claim.

## Exact rod states and mapping

Closure unit directions are:

```text
d_UL = (+1, 0)
d_UR = (-1,-1)/sqrt(2)
d_LR = (0,+1)
common OPEN-to-END stroke S = 10.5852813742
```

| Continuous rod identity | OPEN `(Y,Z)` | first contact `(Y,Z)` | END `(Y,Z)` |
|---|---:|---:|---:|
| upper-left -> upper-left | `(-4.2502813742,24.4350000000)` | `(6.0850000000,24.4350000000)` | `(6.3350000000,24.4350000000)` |
| upper-right -> middle | `(22.2350000000,24.4350000000)` | `(14.9268524548,17.1268524548)` | `(14.7500757595,16.9500757595)` |
| lower-right -> lower-right | `(22.2350000000,-2.0502813742)` | `(22.2350000000,8.2850000000)` | `(22.2350000000,8.5350000000)` |

Derived center-triangle evidence:

| State | Area `mm^2` | side lengths `mm` in UL-UR, UR-LR, LR-UL order |
|---|---:|---:|
| OPEN | `350.7350647343` | `26.4852813742, 26.4852813742, 37.4558441227` |
| first contact | `12.3846671450` | `11.4711540559, 11.4711540559, 22.8395490323` |
| END | `7.39470457605` | `11.2622196269, 11.2622196269, 22.4859956417` |

The OPEN right leg is exact: upper-right and lower-right both have
`Y=22.235`. The corrected END centers move no more than the supplied
`0.65761 mm` correction bound from the corresponding accepted END vertices;
implementation must derive and report this regression rather than merely copy
the bound. Legacy source-role mapping is `bottom -> upper-left`, `diagonal ->
upper-right/middle`, and `upright -> lower-right`.

## Contact derivation and geometric law

For each rod `i`:

```text
r_contact,i = r_end,i - 0.25*d_i
r_open,i    = r_end,i - S*d_i
u(theta)    = theta / 24,  0 <= theta <= 24 deg
r_i(theta)  = r_open,i + S*u(theta)*d_i
theta_contact = 24*(S-0.25)/S = 23.4331751998 deg
```

At first contact each rod is `4.15` from its intended straight or arc wire
feature. At END it is `3.90`. Reject geometric smoothstep: any ease belongs
only to Viewer time-to-angle presentation and must not alter `r_i(theta)`.

## Fixed-inner tracks and opposite outer rails

Each fixed-inner track is a stationary, closed `4.15 mm` capsule on the direct
straight segment from OPEN to END, extended `1.40 mm` beyond both endpoints
along `d_i`. Both fixed inner plates use the identical world `YZ` tracks; no
hole or rail moves with animation.

Retain the accepted virtual outer-rotation datum `C=(1.75,6.25)` and fixed
axle `A=(-29.00,17.00)`. For side `s`:

```text
alpha_left(theta)  = -theta
alpha_right(theta) = +theta
q_s,i(theta) = R(-alpha_s(theta)) * (r_i(theta)-C)
q_s,A(theta) = R(-alpha_s(theta)) * (A-C)
```

The six rod rails and two axle rails are swept closed capsules about those
part-local loci. Reconstruction must satisfy
`C + R(alpha_s)*q_s,i = r_i` and `C + R(alpha_s)*q_s,A = A` within `0.05 mm`
at exact OPEN, contact, END, and at least 65 total samples. A rail is not
assumed circular; only the fixed-axle locus is circular by construction.

## Preserved geometry and bounded implementation

Preserve the accepted `80/82/85 mm` inner/left-outer/right-force-outer plate
diameters, `3.20 mm` thicknesses, `18.40 mm` clear span, `32.00 mm` principal
stack, `4.15 mm` rod slots, larger right lever, green-grip absence, and the
complete fixed axle/keeper geometry. Preserve all three `50.00 mm` rods,
`8.70 mm` cap engagement per side, stepped blind caps at least `9.05 mm` long,
and six permanent-cap occurrences. If the corrected rails cannot meet the
existing `2.20 mm` minimum web or actual-solid gates inside these envelopes,
STOP and return to design; implementation may not enlarge slots or add parts.

## Focused gates

### Math and constraints

- Recompute every OPEN/contact/END center, triangle area, side length,
  `theta_contact`, tangency offset, and rod travel from the equations.
- Prove the exact vertex mapping and right-vertical OPEN leg.
- Prove all rods travel monotonically by the same scalar `S*u`; left/right
  outer rotation signs are opposite.
- Recompute the accepted-END displacement regression and require the supplied
  `<=0.65761 mm` bound under the task's corresponding-vertex metric.
- Rail reconstruction residual `<=0.05 mm`; no endpoint cusp, branch jump,
  tangent jam, sign reversal, or rank loss. Preserve normalized full-Jacobian
  condition `<=1000` and crossing sine `>=0.10` at all samples.
- Exact counts: three rods, six permanent caps, two fixed inners, two rotating
  outers, one fixed axle, two keepers, zero added mechanisms.

### Actual solids and user regressions

- Valid positive-volume single plate solids with minimum remaining web
  `>=2.20 mm` and positive two-sided material beside every rod track.
- Zero unintended rod/plate, rod/axle, rod/keeper, cap/plate, cap/keeper,
  plate/plate, XT60-body, and non-contact wire intersections through at least
  65 states including exact OPEN/contact/END.
- Before contact, wire intersection is zero; contact is allow-listed only at
  the three intended features; END contains only the named `0.25 mm`
  displacement proxy and never uses the XT60 plastic as reaction geometry.
- The OPEN snapshot must visibly show upper-left plus an upper-right/lower-
  right vertical pair. END must visibly retain the upper-left-to-lower-right
  diagonal and the user-fixed `└` workpiece orientation.
- Revalidate loading, reverse-to-OPEN, and rigid completed-pigtail removal
  against final rods, caps, plates, axle, keepers, XT60 body, joint, and both
  wires. Require zero intersection and `>=0.75 mm` clearance on a continuous
  path sampled at least 1001 times per segment. The prior service path is a
  test seed, not assumed valid; failure returns to design.
- Regression absence: no floating rod, no moving fixed-inner hole, no same-
  direction outer rotation, no green grip tab, no bar/yoke/link/gear/new lock,
  and no self-lock language.

## Acceptance boundary

Passing these gates can accept CAD/source, written STEP, prescribed motion,
and visual orientation. It cannot accept physical cap fit, wire holding force,
insulation safety, hand torque, PETG behavior, heat, wear, springback, or the
cooled bend angle.
