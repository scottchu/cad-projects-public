# P17-D14 design contract and bounded infeasibility

## Coordinate and motion equations

Coordinates are world `(Y,Z)`, with screen right `+Y` and screen up `+Z`. For rod `i`,

`r_i(u) = O_i + u(E_i-O_i)`, `0 <= u <= 1`, and `theta(u)=24u deg`.

For physical plate angle `alpha_L=-theta`, `alpha_R=+theta`, the derived local rails are

`q_i,s(u) = R(-alpha_s(u)) (r_i(u)+D-C)`.

Reconstruction is `r_i(u)+D = C + R(alpha_s(u)) q_i,s(u)`. Numerical reconstruction residual in the pure-math search was below floating-point display precision and therefore below the `0.05 mm` gate by construction.

## Exact I10 guide table

| Rod | OPEN | CONTACT | END |
|---|---|---|---|
| bottom | `(-20.9852813742, 9.5000000000)` | `(-10.6500000000, 9.5000000000)` | `(-10.4000000000, 9.5000000000)` |
| diagonal | `(5.5000000000, 9.5000000000)` | `(-1.8081475452, 2.1918524548)` | `(-1.9849242405, 2.0150757595)` |
| upright | `(5.5000000000, -16.9852813742)` | `(5.5000000000, -6.6500000000)` | `(5.5000000000, -6.4000000000)` |

The common stroke is `10.5852813742 mm`; contact is at `u_c=23.4331751998/24 = 0.976382299991667`.

Workpiece remains: body center `(-6.5,22.5)`, bend center `B=(-0.5,3.5)`, vertical wire `Y=-6.5`, horizontal wire `Z=-2.5`, extraction endpoint `Y=17.265`.

## Why the joint search collapses

The intended contact centerline separation is `3.90 mm` at END (`2.15 mm` nominal insulated-wire radius plus `2.00 mm` rod radius minus `0.25 mm` preload).

- Bottom END is `Y=-10.4`; vertical wire is `Y=-6.5`. Thus `|-10.4+Dy-(-6.5)|=3.9`. Preserving the existing contact side/topology gives `Dy=0`.
- Upright END is `Z=-6.4`; horizontal wire is `Z=-2.5`. Thus `|-6.4+Dz-(-2.5)|=3.9`. Preserving the existing contact side/topology gives `Dz=0`.
- At `D=0`, diagonal END is `2.10 mm` from bend center. Relative to the `6.00 mm` bend centerline radius this is the same `3.90 mm` contact separation.

Therefore the only contact-feasible common translation is exactly `D=(0,0)`. D13's `(+16.1869657526,+10.2949747468)` is rejected independently of rail datum.

## Deterministic C search

Initial bounded box: `Cy in [-2,4] mm`, `Cz in [8,16] mm`, `0.25 mm` grid. Focused repair: `0.025 mm` grid in `+-0.30 mm` around the best coarse point. The pure-JavaScript search evaluated 813 coarse boundary-feasible points and 839 focused points using 129 samples per full rail and 33 samples over CONTACT-to-END.

If the inner-web gate were omitted, the numerical rail optimum was near `C=(4.000,9.550)`:

| Metric | D14 rail-only optimum |
|---|---:|
| worst full-path L/R ratio | `1.086832` |
| worst CONTACT-to-END ratio | `1.088179` |
| minimum crossing-angle diagnostic | `19.448050 deg` |
| minimum analytic boundary | `2.203773 mm` |

Per-rod values at that point:

| Rod | L/R full length mm | full ratio | L/R CONTACT-END length mm | CE ratio | min L/R crossing angle |
|---|---:|---:|---:|---:|---:|
| bottom | `13.474449 / 13.441391` | `1.002459` | `0.288784 / 0.287926` | `1.002979` | `29.627288 / 29.724818 deg` |
| diagonal | `10.359526 / 11.259062` | `1.086832` | `0.256727 / 0.277041` | `1.079126` | `21.062487 / 19.448050 deg` |
| upright | `14.350275 / 13.387809` | `1.071891` | `0.308918 / 0.283886` | `1.088179` | `30.786703 / 33.861605 deg` |

This is deliberately **not selected**, because the hard fixed-inner web fails for every `C`.

### Required comparison

| Evidence | `D` | `C` | worst full ratio | worst CONTACT-END ratio | minimum crossing diagnostic | Product state |
|---|---|---|---:|---:|---:|---|
| I10 accepted world loci | `(0,0)` | `(3,12)` | `1.304701` | `1.270525` | `19.737418 deg` | contact-correct reference |
| D13 rejected | `(+16.186966,+10.294975)` | `(3,12)` | `3.071372` | `4.243331` | `4.387453 deg` | body/wire collision and no END contact |
| D14 rail-only comparison | `(0,0)` | `(4,9.55)` | `1.086832` | `1.088179` | `19.448050 deg` | **not feasible: inner web fails** |

This is a Pareto tradeoff, not a hidden score: D14 strongly improves both rail ratios over I10 and D13, stays near the I10 crossing diagnostic, but consumes axle boundary margin and cannot clear the invariant inner web. Distance from the D13 datum is `sqrt(1^2+(-2.45)^2)=2.645751 mm`; distance from the D13 translation is `19.183 mm` because contact requires returning to `D=0`.

## Global hard blocker

The fixed axle uses the existing `8.15 mm` across-flats hex envelope, circumradius `8.15/sqrt(3)=4.705368 mm`. The inner running slot radius is `4.15/2=2.075 mm`. The closest point of the bottom inner path to `A=(-29,12)` is its OPEN endpoint:

`distance(A,O_bottom)=sqrt((8.0147186258)^2+(2.5)^2)=8.395577 mm`.

Available material web:

`8.395577 - 4.705405 - 2.075 = 1.615172 mm < 2.20 mm`.

This relation contains neither `C` nor an outer-rail term. Consequently no value of `C` can satisfy all frozen hard gates once contact forces `D=0`. This is a proof of infeasibility, not a failure to search far enough.

## Gates

| Gate | Result |
|---|---|
| FRONT orientation, topology, identities, stroke | PASS, frozen I10 |
| Exact END three-point contact/preload | PASS only at `D=(0,0)` |
| Pre-contact wire/body behavior | retained from accepted I10 world loci; downstream BREP regression still required |
| Rail derivation/reconstruction | PASS analytically by inverse-frame equation |
| Outer rail balance | strong rail-only point exists near `C=(4,9.55)` |
| boundary >=2.20 | rail-only point gives `2.203773 mm` |
| all pair webs >=2.20 | **FAIL: inner axle-bottom `1.615172 mm` for every C** |
| actual BREP/service/two-sided support | not run; downstream only and moot until hard analytic blocker is reopened |

Crossing angle is only a path-conditioning diagnostic. It is not hand force, self-locking, material deformation or physical proof.

## Smallest scope that must be reopened

Implementation must not begin. The user must authorize at least one of: move `A`, change the fixed-axle/hex guide envelope, or relax/move the exact workpiece contact interface. Expanding only the `C` search box cannot work.
