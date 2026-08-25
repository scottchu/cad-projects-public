# P17 R2 coupled three-rod triangle motion design

Status: selected and frozen for one bounded implementation/repair cycle.

## Coordinate convention and named geometry

- Units are millimetres.
- `X` is the common stainless-rod and four-plate-stack axis.
- Motion is in world `YZ`; `+Y` is away from the XT60 wire exit.
- XT60 reference body center is `(Y,Z)=(0,21)`, with world Y extent
  `[-4.05,+4.05]` and Z extent `[10.75,31.25]`.
- Purple fixed axle datum remains `A=(-29.00,17.00)`.
- Selected virtual outer-rotation datum is `C=(-1.74,13.22)`. `C` is a
  kinematic datum, not permission to add a centered bar or bore.
- Nominal bend center is `B=(12.80,15.00)` with bend radius `R_b=6.00`.
  Incoming wire centerline is `Z=B_z+R_b=21.00` along `+Y`; the quarter-circle
  turns downward to an outgoing `-Z` leg at `Y=B_y+R_b=18.80`.

Named constants:

```text
r_rod = 2.00
r_wire = 2.15
d_tangent = r_rod + r_wire = 4.15
wire_preload = 0.25       # geometric displacement proxy only
d_end = d_tangent - wire_preload = 3.90
contact_stroke = 3.7642135623730946
common_stroke S = contact_stroke + wire_preload
                = 4.014213562373095
theta_end = 24.00 deg
slot_width = 4.15
slot_endpoint_margin = 1.40
minimum_web = 2.20
```

## Selected OPEN, contact, and END triangles

Rod closure unit directions are fixed in world coordinates:

```text
d_upright  = (-1,  0)
d_bottom   = ( 0, -1)
d_diagonal = ( 1,  1) / sqrt(2)
```

The first-contact centers are derived from exact tangency to the two-wire
90-degree centerline:

| Rod | OPEN center `(Y,Z)` | First-contact center `(Y,Z)` | END center `(Y,Z)` |
|---|---:|---:|---:|
| upright | `(26.7142135624, 9.0000000000)` | `(22.9500000000, 9.0000000000)` | `(22.7000000000, 9.0000000000)` |
| bottom | `(6.8000000000, 28.9142135624)` | `(6.8000000000, 25.1500000000)` | `(6.8000000000, 24.9000000000)` |
| diagonal | `(11.4464466094, 13.6464466094)` | `(14.1081475452, 16.3081475452)` | `(14.2849242405, 16.4849242405)` |

The equations are:

```text
r_end,u = (B_y + R_b + d_end, B_z - R_b)
r_end,b = (B_y - R_b, B_z + R_b + d_end)
r_end,d = B + ((R_b - d_end)/sqrt(2)) * (1,1)

r_contact uses d_tangent in the same equations.
r_open,i = r_end,i - S * d_i
```

Triangle center areas and side lengths are design evidence, not wire pocket
areas:

| State | Area `mm^2` | `U-B` | `B-D` | `D-U` |
|---|---:|---:|---:|---:|
| OPEN | `105.7576208180` | `28.1629509039` | `15.9591407608` | `15.9591407608` |
| first contact | `12.3846671451` | `22.8395490323` | `11.4711540559` | `11.4711540559` |
| END | `7.39470457618` | `22.4859956417` | `11.2622196269` | `11.2622196269` |

At first contact, each rod-center to its intended wire-centerline feature is
exactly `4.15 mm`. END advances every rod `0.25 mm` on its own normal, giving
the `3.90 mm` geometric offset. This is “tight enough” in CAD only as a named
preload displacement proxy. Force and insulation response require a physical
wire test.

## Direct straight fixed tracks and counter-rotating outer rails

Use a linear geometric parameter. Easing may be applied to animation time, but
must never alter the CAD path:

```text
u(theta) = theta / theta_end, 0 <= theta <= theta_end
r_i(theta) = r_open,i + S * u(theta) * d_i
alpha_left(theta)  = -theta
alpha_right(theta) = +theta
q_s,i(theta) = R(-alpha_s(theta)) * (r_i(theta) - C)
```

Each fixed-inner guide is one closed capsule centered on the straight segment
from `r_open,i - 1.40*d_i` to `r_end,i + 1.40*d_i`. Therefore “inner plate
straight movement” is exactly correct for this selected contract.

Each outer rail is the swept narrow capsule about `q_s,i(theta)`. It is not a
circle unless that inverse-transform equation degenerates to one; no such
assumption is allowed. The purple-axle rail remains side-specific:

```text
q_s,A(theta) = R(-alpha_s(theta)) * (A - C)
```

World reconstruction must satisfy, for both sides and all rods:

```text
C + R(alpha_s(theta)) * q_s,i(theta) = r_i(theta)
C + R(alpha_s(theta)) * q_s,A(theta) = A
```

within `0.05 mm` on at least 65 samples including exact endpoints.

## Why `32 deg` is superseded by `24 deg`

The endpoint angle is a same-version geometry parameter, not a version. A
read-only 33-sample actual-cutter feasibility probe of the selected linear
path found `24 deg` retained positive right-side bottom/diagonal rail web
`2.6498620121 mm`; the left minimum was `3.6684788120 mm`. Larger angles make
the two swept rail cutters approach each other; `26 deg` falls to about
`2.19 mm`, below the `2.20 mm` gate. Therefore `theta_end=24 deg` is selected,
not left open for implementation search. Linear travel puts nominal first
contact at:

```text
theta_contact = 24 * contact_stroke / common_stroke
              = 22.5053112131 deg
```

The predecessor smoothstep is rejected because its zero endpoint derivative
creates an artificial dwell/near-singular endpoint without a real lock.

## Plate envelope and minimum material

Selected production targets:

| Parameter | Target |
|---|---:|
| fixed inner diameter | `70.00` |
| left outer diameter | `72.00` |
| right force outer diameter | `75.00` |
| inner/outer thickness | retain `3.20 / 3.20` |
| sliding rod slot width | `4.15` |
| fixed axle outer-guide width | retain `7.90` |

The right outer has `1.50 mm` more lever radius than the left. The separate
green left grip block is redundant and must be removed; no replacement tab is
added.

A read-only build123d feasibility probe using `C`, the selected tracks, 33
outer samples, and no obsolete service-window cutter produced valid single
solids: inner volume `11729.6349114 mm^3`, left outer
`12102.0219310 mm^3`, right outer `13201.8375575 mm^3`. Minimum exact outer
rod-cutter separation was `3.6684788120 mm` left and `2.6498620121 mm` right;
minimum axle-guide to rod-guide cutter separation exceeded `25.90 mm`.

The old fixed-inner completed-pigtail window is incompatible with this real
wire-contact triangle: its actual cutter overlaps the bottom track by
`85.6964735519 mm^3` and the diagonal track by `14.0678087543 mm^3`. Remove
that obsolete plate window in this bounded implementation. Do not replace it
with bars or bulk. The completed pigtail stays inside the `18.40 mm` central X
span during `+Y` removal; actual-solid service sweep must prove this before
acceptance.

## 50 mm rods, permanent caps, and wobble

Retain the current principal four-plate stack width:

```text
W_stack = 18.40 + 2*3.20 + 2*0.40 + 2*3.20 = 32.00
cap_to_outer_gap = 0.30 per side
cap_engagement = (50.00 - 32.00 - 2*0.30)/2 = 8.70 per side
cap_closed_end_wall = 0.35
cap_length >= 8.70 + 0.35 = 9.05
```

Do not lengthen only the current cap solid; that collides with the current
socket/end definition. Rebuild each permanent cap as a stepped blind socket:

- proximal sliding guide: `ID4.15`, depth `4.70`;
- distal retention zone: depth `4.00`, nominal candidate `ID4.04`, with the
  existing coupon ladder controlling the eventual production choice;
- closed end wall at least `0.35`; total cap length at least `9.05`;
- follower OD remains at least `6.60`, leaving at least `1.225 mm` radial wall
  at the `ID4.15` guide.

All six caps remain permanent. CAD cannot select retention force.

The `4.15` moving slot gives nominal radial center play
`(4.15-4.00)/2=0.075 mm`. Across the two fixed-inner planes separated by
`21.60 mm`, a conservative opposite-edge difference of `0.15 mm` gives rod
angular wobble `atan(0.15/21.60)=0.3979 deg`. Acceptance target is no more than
`0.40 deg` nominal CAD skew and no more than `0.15 mm` diametral guide play;
printed curved-slot fit remains physical.

## Closure, conditioning, and no-floating gates

For each rod, the fixed-line/outer-rail crossing determinant is proportional
to `d_i dot (r_i-C)`. The selected contract has minimum absolute values
greater than `9.6 mm`; normalized crossing sine from the analytic path remains
above `0.45`. Implementation must preserve:

- fixed/outer rail crossing sine `>=0.25` at every sampled state;
- full normalized constraint Jacobian full rank, with
  `sigma_min/sigma_max >= 1e-3` (condition number `<=1000`) at OPEN, first
  contact, END, and all sampled intermediate states;
- no endpoint-only rank loss, sign reversal, branch jump, or false jam;
- positive two-sided material beside every rod slot normal at both fixed inner
  plates and both outer plates;
- each rod center at least `1.40 mm` from each fixed capsule centerline end at
  OPEN and END;
- coincident left/right YZ centers and zero modeled rod skew.

## Validation gates

### Object collision

- Actual `OD4 x 50` rod solids against XT60 body at 65 states: zero
  intersection and clearance `>=0.75 mm`. The design probe found minimum
  `0.75 mm` at the bottom rod and zero intersection.
- Actual rods against the selected two-wire straight/arc/vertical solids:
  zero before first contact; intended tangency allow-listed at contact; only
  named `0.25 mm` displacement proxy at END.
- Zero unintended rod/axle, rod/keeper, cap/keeper, rod/plate, cap/plate, and
  plate/plate collision through motion.
- Completed pigtail loading, solder, cooling, reversal, and `+Y` removal sweep
  through the central X span has zero unintended collision.

### Math

- Recompute all three triangles, areas, side lengths, tangency offsets,
  contact angle, `50 mm` cap engagement, inverse rails, and reconstruction;
  tests must derive values rather than assert duplicated literals.
- Reject smoothstep or any geometry law with zero endpoint derivative.
- Prove monotonic `S*u` travel and counter-rotation signs.

### Constraint

- Exact counts: three rods, six permanent caps, two fixed inner plates, two
  independently rotating outer plates, one fixed purple axle, two axle
  keepers, zero added bars/linkages.
- Valid single plate solids, closed slot ends, minimum `2.20 mm` web, fixed
  slot `4.15`, plate diameters `70/72/75`, right lever larger.
- Positive two-sided support and normalized endpoint conditioning pass.

### User requirement

- No floating rod, no moving hole in a fixed plate, no same-direction outer
  motion, no centered replacement bar, no green left grip block, no current
  service-window collision, and no lock/self-lock wording.
- The exact OPEN/contact/END motion must be visually reviewable in CAD Viewer;
  screenshots do not replace the deterministic gates.

## Physical unknowns

Cap insertion/retention, printed straight/curved slot fit, hand torque,
insulation marking, actual preload force, wire springback, 90-degree cooled
angle, PETG heat/creep/wear, axle stiffness, and repeated cycling remain
physical tests. CAD acceptance must not be reported as physical acceptance.
