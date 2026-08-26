# P19 R1 cycle-4 OPEN-upright minimum reopening

Status: **FEASIBLE ANALYTIC 2D CANDIDATE; READY FOR INDEPENDENT
P19-CRIT-04 REVIEW.** This record authorizes review of one exact 2D candidate
only. It does not authorize CAD implementation until the independent critic
accepts it, and it makes no claim about hand force, friction, backlash,
self-locking, printing or physical acceptance.

Owner/role: `/root/p19_min_rail_optimizer`, mechanism/optimizer designer.
Frozen manifest:
`REOPTIMIZE_4MM_OPEN_UPRIGHT_INPUT.sha256`, SHA-256
`65923a3ca0861b79e3f36861479f06f80b08c043fec5c790d7065560a48d9143`;
all seven declared content entries verified from the repository root.

## Frozen geometry and inverse law

Coordinates are millimetres in physical FRONT YZ: `+Y` is the short-tail,
tool/front/right direction and `+Z` is mating-head/up.

```text
C = (0,0)
A = (-13,-9), one continuous stepped X axle through all four plates

OPEN_bottom   = ( 5.000000000, 10.000000000)
OPEN_diagonal = (20.400000000, 10.000000000)
OPEN_upright  = (20.400000000, -5.000000000-d)

END_i = END0_i + (deltaY,deltaZ)
END0 = [(8,9), (14.25,3.25), (20.5,-2.5)]
p_i(u) = OPEN_i + u(END_i-OPEN_i), shared 0 <= u <= 1
alpha_left(u)  = -theta*u
alpha_right(u) = +theta*u
q_s,i(u) = R(-alpha_s(u)) p_i(u)
```

The OPEN top leg remains exactly horizontal and its right leg remains exactly
vertical. END keeps the repeated pitch `(6.25,-5.75)`. Identities remain
`bottom, diagonal, upright`; the three world paths are continuous and
non-crossing. Both sides reconstruct the same physical world point from the
same shared `u`; no outer rail is padded or hand-extended.

`C`, `A`, plate ODs `54.4/54.7/55.0`, three uncut OD4x50 rods, six permanent
caps, fixed inners, OD4.15 rail cutters, short-tail/tool direction and all
other cycle-4 invariants remain unchanged. The purple axle is an X-axis
structural member through all four plates, not a floating fourth rod.

## Bounded optimizer and minimum proof

Only the authorized values were searched:

```text
5.0 <= theta <= 45.0 deg
0 <= d <= 5.45 mm
0 <= deltaY <= 9.10947953 mm
-1.045238580701 <= x <= +1.081431993941 mm
x = n dot (deltaY,deltaZ)
n = (5.75,6.25)/hypot(6.25,5.75)
```

The objective was lexicographic: first satisfy every hard gate, then minimize
`d`; only after that prefer service margin, web and conditioning. Deterministic
coarse screening across the full bounds was followed by multi-start constrained
refinement. The minimum lies on four active bounds/equalities:

1. `theta=5 deg`, the frozen non-degenerate lower limit;
2. `x=+0.331431993941`, the new `0.75 mm` OPEN-clear service boundary;
3. left/bottom inverse centre arc `=4.000000000 mm`;
4. right/upright inverse centre arc `=4.000000000 mm`.

At fixed `theta` and `x`, the first equality uniquely solves `deltaY`; the
right/upright rail equality then uniquely solves `d`. Searches started from the prior
`d=5.4 mm` witness and from the other rail-active branch converged to the same
minimum branch. Raising theta or moving x inside the service interval makes
the minimum feasible `d` larger. High-resolution quadrature and continuous
curve-distance refinement produced the values below.

## Selected exact candidate

```text
theta  = 5.000000000 deg per outer plate
d      = 4.172814226 mm downward
deltaY = +1.552212036 mm
deltaZ = -0.977677650 mm
x      = +0.331431994 mm
```

| identity | OPEN `(Y,Z)` | END `(Y,Z)` |
|---|---:|---:|
| `bottom` | `(5.000000,10.000000)` | `(9.552212,8.022322)` |
| `diagonal` | `(20.400000,10.000000)` | `(15.802212,2.272322)` |
| `upright` | `(20.400000,-9.172814)` | `(22.052212,-3.477678)` |

The exact OPEN vectors are `(15.4,0)` and `(0,-19.172814226)`. The END
vectors are both `(6.25,-5.75)`. The characteristic radius for the normalized
closure probe is `22.719154914 mm`.

## Six exact inverse outer rails

Centre arcs use adaptive quadrature of `|q'_s,i(u)|`; chords use the exact
endpoints. Capsule aspect is `(centre arc + 4.15)/4.15`.

| outer / rod | centre arc | chord | capsule aspect | minimum crossing |
|---|---:|---:|---:|---:|
| left / `bottom` | `4.000000000` | `3.993644065` | `1.963855422` | `0.753626 deg` at OPEN |
| left / `diagonal` | `8.012433561` | `8.001136834` | `2.930706882` | `6.317446 deg` at END |
| left / `upright` | `7.864158837` | `7.856482742` | `2.894978033` | **`0 deg` at `u=0.527104459`** |
| right / `bottom` | `5.944910144` | `5.938566246` | `2.432508468` | `0.506324 deg` at OPEN |
| right / `diagonal` | `10.157688046` | `10.146318684` | `3.447635674` | `4.966200 deg` at END |
| right / `upright` | `4.000000000` | `3.992179578` | `1.963855422` | **`0 deg` at `u=0.527104459`** |

All six centre travels pass `>=4.00 mm`; the left/bottom and right/upright
rails are exactly active. All six capsule aspects pass `>=1.963855`.

The zero upright crossing is exact, not a sampling defect. For a straight
world path `p(u)=O+uv`, the inverse-rail tangent transformed back into world
coordinates is `w_s=v-alpha'_s Jp`. Therefore

```text
cross(v,w_s) = -alpha'_s * (v dot p(u))
u* = -(O dot v)/|v|^2.
```

Here `u*=0.527104459` lies inside the motion, so both upright rails are
tangent to the physical upright path at that state regardless of the sign of
the outer rotation. This remains a severe friction/backlash/force-transfer
risk, but the superseding input treats it as a physical unknown, not a scalar
2D blocker, because the complete four-contact system retains rank three with
the required condition bound.

## Web, boundary and axle evidence

Pair order below is `bottom-diagonal / bottom-upright / diagonal-upright`.
Values are surface web after subtracting both OD4.15 cutter radii.

| plate / rail family | three pair webs | minimum |
|---|---:|---:|
| fixed inner | `4.161276 / 12.835288 / 4.342644` | `4.161276 mm` |
| left outer | `4.309452 / 12.835288 / 4.342644` | `4.309452 mm` |
| right outer | `3.922383 / 12.835288 / 4.342644` | `3.922383 mm` |

| check | result |
|---|---:|
| fixed-inner rim web | `2.405845 mm` |
| left-outer rim web | `2.555845 mm` |
| right-outer rim web | `2.705845 mm` |
| minimum conservative axle-guide to rod-rail web | `21.715109 mm` |
| whole 8x8 tool outside OD55 tangent | `0.750000 mm` |
| cup left edge outside largest rim | `1.750000 mm` |

The global estimated 2D material minimum is the fixed-inner rim at
`2.405845 mm`, passing `>=2.20 mm` by `0.205845 mm`. Endpoint caps, exact
stepped-axle key corners, fillets and chamfers remain future exact-solid
checks; this 2D result does not claim BREP clearance.

## OPEN service, contact and short tail

The wire line is re-derived from the selected END geometry with
`F_bottom=END_bottom+3.9n`. All three END signed centre distances are
`-3.900000 mm`, retaining the selected `-0.250000 mm` preload proxy.

| rod | OPEN signed centre distance | OPEN surface clearance | first contact |
|---|---:|---:|---:|
| `bottom` | `-5.526671 mm` | `+1.376671 mm` | `u=0.846312` |
| `diagonal` | `+4.900000 mm` | `+0.750000 mm` | `u=0.085227` |
| `upright` | `-9.209869 mm` | `+5.059869 mm` | `u=0.952918` |

The available short-tail centreline is `7.557267 mm`; the complete tool and
cup stay outside the right/front rim. Every named rod now has at least the
new hard `0.75 mm` OPEN surface clearance. The diagonal rod is the limiting
assembly-margin state and first contacts only after motion begins.

## Closure and condition

The normalized four-contact probe uses row order
`fixed axle, upright, bottom, diagonal`, pose coordinates
`deltaY, deltaZ, alpha`, rotation-column scale `22.719154914 mm`, and unit row
normalization. Continuous refinement around the sampled extrema gives:

| outer plate | minimum rank over 5,001 states | worst condition | state |
|---|---:|---:|---:|
| left | `3` | `7.436099` | END |
| right | `3` | **`13.007766`** | END |

The right condition gate now has `1.992234` margin. Rank/condition are nominal local
centreline-closure evidence only and do not establish usable torque, force,
stiffness, friction or back-drive resistance.

## Delta versus cycle-3 focused repair witness

| item | cycle-3 repair witness | selected cycle-4 candidate |
|---|---:|---:|
| twist per side | `9.886768 deg` | `5.000000 deg` |
| OPEN upright Z | `-5.000000 mm` | `-9.172814 mm` |
| common END delta | `(+1.480911,-2.782732)` | `(+1.552212,-0.977678)` |
| shortest rail | `4.000000 mm` | `4.000000 mm` |
| minimum outer rail-to-rail web | **`1.405771 mm` fail** | `3.922383 mm` pass |
| minimum OPEN clearance | `0.000000 mm` | `0.750000 mm` |
| short-tail centreline | `7.628569 mm` | `7.557267 mm` |
| worst condition | `39.7594` | `13.0078` |

The authorized `OPEN_upright_Z` reopening recovers the internal web and
conditioning failures without moving `C`, `A`, the plate diameters, the OPEN
top leg, the two other OPEN rods or any identity.

## Decision boundary and unresolved risks

This is one deterministic, feasible analytic 2D candidate. It preserves the
user's direction, exact OPEN/END topology, shared motion state, opposite
twist, fixed real X axle, rod/cap count, compact plate hierarchy, minimum
4 mm physical rail travel, estimated web and short-tail/tool service.

P19-CRIT-04 must independently reproduce the exact manifest, six inverse
rails, service/contact states, web, rank/condition and the phone artifact
before source-first CAD may start. The primary physical risks are the exact
upright tangency, the `0.75 mm` diagonal OPEN margin, nominal OD4.15/PETG fit,
hand force, backlash, flex, heat access and whether `7.557267 mm` of short-tail
service is sufficient in the actual ESC assembly. No 3D, STEP, 3MF, slicing,
printing or physical acceptance is claimed here.

Review artifact:
`docs/review/p19-r1-front-edge-short-tail/open-upright-minimum-gate.png`.
