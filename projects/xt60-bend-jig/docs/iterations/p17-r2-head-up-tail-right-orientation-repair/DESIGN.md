# P17-D10-R2 corrected head-up / tail-right design contract

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
This is workpiece-relative invariant `REQ-027`, not a camera/view choice.

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
`Y=22.235`. Recalculation against the corresponding accepted END vertices
gives `0.657609306503 mm` for upper-left and lower-right and
`0.657823586728 mm` for the middle vertex. D10-R1 therefore replaces only the
contradictory `0.65761 mm` maximum with `<=0.657824 mm`, the six-decimal
ceiling of the exact maximum. Implementation must derive and report this
regression rather than merely copy the bound. Every exact coordinate above is
unchanged. Legacy source-role mapping is `bottom -> upper-left`, `diagonal ->
upper-right/middle`, and `upright -> lower-right`.

This mapping is functional (`REQ-028`, `REQ-029`). OPEN is the outward UL-UR-
LR triangle with no identity swap or crossing. At CLAMPED/END, the middle rod
acts on the bend arc while upper-left/lower-right act on the vertical and
horizontal straight-leg features. The diagonal is a three-point wire wrap;
XT60 plastic is not a reaction member. “Locked” remains colloquial endpoint
wording only under `REQ-030`. Mirroring or reversing this topology requires
design reopening even if distances could otherwise be preserved.

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

Use D10-R2 virtual outer-rotation datum `C=(3.00,12.00)` and fixed
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

## D10-R2 two-sided outer support repair

At D10-R1 `C=(1.75,6.25)`, the left outer/bottom rail lost its `+normal`
reaction side and right outer/upright lost its `-normal` side. The inverse
locus curved back into its own radius-`2.075` swept capsule: missing material
extended to about `3.1/3.4 mm` at left OPEN/END and `2.7/4.1 mm` at right
OPEN/END. Fixed-inner support, contact, reconstruction, collision, service,
plate validity, and minimum web were not the cause.

A bounded primary-variable search changed only `C`:

```text
coarse domain:  C_y=-4..6, C_z=1..12, step 0.50
refined domain: C_y= 0..5, C_z=8..14, step 0.10
rail samples: 65 minimum; 129/257 on shortlisted clearance checks
required: material at slot radius +0.30 on both normals,
          rod/rod, axle/rod and plate-boundary web >=2.20,
          valid plates, regular rails and combined rank 3
selected: C=(3.00,12.00), 5.88430114797 from D10-R1 C
```

Fresh build123d evidence at the selected rounded datum:

```text
two-sided 0.20 OD probe at radius 2.075+0.30:
  minimum plate intersection = 0.100530964915 mm^3 (full probe volume)
all normal sides supported / all slot ends closed = true / true
outer rod-cutter gap left/right = 3.63098982454 / 5.88437374099
fixed-inner extended cutter gap = 6.10304832720
minimum axle analytic web = 2.90632582470
left/right axle-guide boundary web = 4.66173051860 / 6.16173051860
rail/axle reconstruction max = 5.69e-15 / 7.11e-15
combined Jacobian rank / max condition = 3 / 12.8216328305
maximum unintended motion intersection = 0
minimum XT60 clearance = 0.750000000000
completed-pigtail service gate = pass
```

The `0.30 mm` support requirement is not weakened. Implementation must probe
the continuous normal strip from swept-slot boundary through `+0.30 mm`, on
both sides of every outer rail at all 65 states including exact OPEN, contact,
and END. Any void, self-return cavity, or partial probe loss reopens design.
No rail may be trimmed away from the inverse-transform locus.

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

### D10-R1 conditioning adjudication

The inherited `crossing sine >=0.10` rule measured each fixed-line/outer-rail
pair as though that pair alone had to determine the rod pose. That is not a
necessary condition for this coupled three-rod architecture. At the exact D10
geometry the minimum individual diagnostic is `0.000667249` on left
upper-left and `0.001059948` on right lower-right, while exact reconstruction
is `7.94e-15 mm`, minimum web is `3.65059 mm`, and the combined normalized
constraint Jacobian remains rank 3 with condition number at most `13.58`.
The near-tangency therefore means one redundant local constraint contributes
little normal authority at that instant; it does not by itself create a cusp,
reversal, branch jump, or singular coupled mechanism. Raising the local sine
would force a needless change to the user-fixed topology or exact rod states.

D10-R1 removes only the individual crossing-sine pass threshold. Continue to
report its signed minimum as a diagnostic. Replace it with these
failure-relevant gates:

- every analytic local rail derivative
  `dq_s,i/dtheta = R(-alpha_s) * (dr_i/dtheta - alpha'_s*J*(r_i-C))`
  is finite and nonzero at exact endpoints and all samples;
- fixed-track progress is strictly monotonic,
  `d_i dot dr_i/dtheta = S/24 = 0.441053390592 mm/deg > 0`, with no sign
  reversal or endpoint dwell;
- each rail parameter remains continuous and one-to-one over `0..24 deg`,
  with no self-intersection, non-adjacent branch overlap, or branch switch;
- continuation of the complete coupled closure from each preceding sample
  reconstructs the intended rod centers within `0.05 mm`, remains full rank,
  and has normalized Jacobian condition number `<=1000` at exact OPEN,
  contact, END, and all intermediate samples.

These gates catch actual cusp, reversal, ambiguity, and coupled singularity.
They do not waive minimum web, actual-solid collision, two-sided support, or
endpoint checks.

### Math and constraints

- Recompute every OPEN/contact/END center, triangle area, side length,
  `theta_contact`, tangency offset, and rod travel from the equations.
- Prove the exact vertex mapping and right-vertical OPEN leg.
- Prove all rods travel monotonically by the same scalar `S*u`; left/right
  outer rotation signs are opposite.
- Recompute the accepted-END displacement regression and require
  `<=0.657824 mm` under the corresponding-vertex Euclidean-distance metric;
  expected maximum is `0.657823586728 mm` at the middle vertex.
- Rail reconstruction residual `<=0.05 mm`; regular nonzero rail derivatives;
  strictly monotonic fixed-track progress; no self-intersection, endpoint
  cusp, branch jump, reversal, or rank loss; normalized full-Jacobian
  condition `<=1000` at all samples. Individual crossing sine is reported as
  a diagnostic only and has no independent pass threshold.
- Exact counts: three rods, six permanent caps, two fixed inners, two rotating
  outers, one fixed axle, two keepers, zero added mechanisms.

### Actual solids and user regressions

- Valid positive-volume single plate solids with minimum remaining web
  `>=2.20 mm` and at least `0.30 mm` continuous actual two-sided material
  beside every outer rod track; verify strip continuity, not only one point.
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
