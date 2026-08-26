# P17-D11 design and feasibility result

## Frozen geometry and coordinates

Front view is world `YZ`, `+Y` screen-right and `+Z` screen-up. Rod identity and
world centers remain exactly:

| rod | OPEN `(Y,Z)` mm | contact `(Y,Z)` mm | END `(Y,Z)` mm |
|---|---:|---:|---:|
| Rod 1 / `bottom` | `(-4.2502813742,24.435)` | `(6.085,24.435)` | `(6.335,24.435)` |
| middle / `diagonal` | `(22.235,24.435)` | `(14.9268524548,17.1268524548)` | `(14.7500757595,16.9500757595)` |
| Rod 2 / `upright` | `(22.235,-2.0502813742)` | `(22.235,8.285)` | `(22.235,8.535)` |

For rod `i`, `r_i(u)=O_i+u(E_i-O_i)`, `0<=u<=1`; the fixed inner
track is that direct straight segment. Let `J(y,z)=(-z,y)`, common outer
center `C`, outer magnitude `beta(u)`, and `sigma_left=-1`,
`sigma_right=+1`. Every outer rail is derived, never eyeballed:

`q_s,i(u) = R(-sigma_s beta(u)) [r_i(u)-C]`.

Its world-frame tangent is

`t_s,i = (E_i-O_i) - sigma_s beta'(u) J[r_i(u)-C]`,

with `beta'` in radians per unit `u`. The acute crossing angle `phi` is the
angle between `t_s,i` and the unit fixed-track direction. `sin(phi)` is only a
geometric useful-normal-component diagnostic; `1/sin(phi)` is not hand force.

## Quantified gates

The current middle rod has minimum terminal angle `21.43 deg` and left/right
diagnostic-multiplier ratio `1.37`. A deliberately modest comparable gate was
fixed before selection:

- on every rail over exact contact-to-END, `min(phi) >= 18.0 deg`, hence
  `1/sin(phi) <= 3.236`;
- for each rod, left/right worst-multiplier ratio `<=1.50`;
- for each rod, left/right contact-to-END rail-arclength ratio `<=1.50`;
- inverse reconstruction `<=0.05 mm`, minimum web `>=2.20 mm`, all four plates
  one valid solid, closed ends and continuous `0.30 mm` two-sided support;
- actual-solid unintended intersection `<=1e-7 mm3`, all plate guides and
  fixed hardware clear, D10 service clearance `>=0.75 mm`;
- rail derivative finite/nonzero, one-to-one/no branch jump, normalized
  constraint rank `3`, condition number `<=1000`.

Real friction, PETG compliance/wear, wire stiffness and hand torque remain
physical unknowns even after a digital pass.

## Baseline diagnosis

At frozen `C=(3,12)` and `beta(u)=24u deg`, END values reproduce the defect:

| rod | left angle / multiplier | right angle / multiplier | current full rail L/R lengths mm |
|---|---:|---:|---:|
| `bottom` | `14.56 deg / 3.98x` | `5.05 deg / 11.35x` | `5.582780 / 15.866822` |
| `diagonal` | `29.99 deg / 2.00x` | `21.43 deg / 2.74x` | `11.213927 / 14.536168` |
| `upright` | `4.45 deg / 12.88x` | `29.86 deg / 2.01x` | `19.041356 / 4.519826` |

For constant `beta'=24 deg`, common-`C` symmetry alone is contradictory:
bottom balance drives `C_z` toward `24.435`, while upright balance drives
`C_y` toward `22.235`. A `0.10 mm` grid over `C_y,C_z in [-10,40] mm`, filtered
by necessary `|C-A|<=35 mm` and maximum rod radius `<=36.7 mm`, found no point
meeting the gates. The best minimum angle was `14.094 deg` with maximum
side-multiplier ratio `4.022`; common `C` alone is rejected.

## Bounded nonlinear family and rejected frontier

The only reopened motion family was equal and opposite as required by
`REQ-023`:

`beta(u)=24[(1-lambda)u + lambda u^n] deg`,

with integer `n` and `0<=lambda<1`. It preserves `beta(0)=0`, `beta(1)=24`,
strict monotonicity, exact world rod states, and opposite plate angles. No new
part or lock is introduced.

The strongest fully evaluated frontier used `C=(2.5,15.7) mm`, `n=22`,
`lambda=0.85`. It gives `beta(contact)=15.572772 deg`, start slope
`3.6 deg/u`, END slope `452.4 deg/u`, and these dense analytic results:

| rod | side | min contact-to-END angle | worst multiplier | contact-to-END length mm | full rail length mm |
|---|---|---:|---:|---:|---:|
| `bottom` | left | `27.4129 deg` | `2.1720x` | `1.17081` | `10.92919` |
| `bottom` | right | `18.1489 deg` | `3.2104x` | `1.62979` | `14.42055` |
| `diagonal` | left | `56.0055 deg` | `1.2061x` | `1.67948` | `12.64735` |
| `diagonal` | right | `44.4652 deg` | `1.4276x` | `1.99096` | `15.21349` |
| `upright` | left | `18.6753 deg` | `3.1230x` | `3.33007` | `19.30443` |
| `upright` | right | `21.2820 deg` | `2.7551x` | `2.86124` | `14.03262` |

Its worst multiplier ratio is `1.4781`; worst contact-path ratio is `1.3920`.
Inverse reconstruction is numerical zero, all four plates are valid solids,
and minimum web is `2.234605 mm`. It is nevertheless rejected: actual-solid
motion reports `0.014479844 mm3` unintended intersection and
`allPlateGuidesClear=false`; endpoint and continuous two-sided-support gates
also fail. Increasing the rail sampling density to mask that failure was
aborted as an unbounded Boolean-cost workaround and is not an accepted fix.

A smaller frozen-`C` candidate (`n=20`, `lambda=0.80`) cleared workpiece motion
but reduced left web to `1.917015 mm` and failed support. A nearby repair
`C=(2.5,15.7)`, `n=20`, `lambda=0.90` still had only `2.101477 mm` web and
`0.012642150 mm3` unintended intersection. Both are rejected.

## Decision and exact reopening needed

The frozen states do not mathematically forbid better force balance, but the
allowed `80/82/85 mm` plate/support envelope prevents the tested balanced rails
from being physically cut as valid supported guides. Therefore P17-D11 stops
without an implementation candidate. The smallest next design task must reopen
exactly one envelope variable (outer plate diameter/profile or the common
center/axle envelope beyond this bounded search), then repeat the same gates.
It must not widen the `4.15 mm` slots, move the world triangles, change the
fixed inner tracks, add structure, or claim measured force.

## R1 bounded outer-envelope repair

R1 searched the same equation family while allowing `C` and the left/right
outer radial envelope to be derived. Inner diameter remained `80 mm`; right
remained larger than left. A common diameter increase was tested first because
it is the smallest envelope change; independent increases are needed only if
the derived left/right requirements exceed the existing right-side advantage.

The strongest low-curvature R1 candidate is `C=(-0.5,21.0) mm` with unchanged
`A=(-29,17) mm` and
`beta(u)=24[0.30u+0.70u^12] deg` (left `-beta`, right `+beta`). It preserves
the exact frozen rod states and fixed tracks. Start/END slopes are
`7.2/208.8 deg/u`.

Dense contact-to-END results are: minimum crossing angle `25.1682 deg`, worst
multiplier ratio `1.47442`, and worst path ratio `1.42916`. The 65-point
actual swept-rail solid gives left/right minimum web
`2.229227/5.756361 mm`, four valid plate solids, `0.0 mm3` unintended
intersection, `0.75 mm` XT60 clearance, zero precontact wire intersection,
and all plate guides/fixed hardware clear. Nonlinear prescribed-pose maximum
residual is `1.12e-15 mm`; normalized rank is `3` and maximum condition number
is `952.565` (`<=1000`).

The derived circular diameter needed for `2.20 mm` radial web is only
`73.301702 mm`. Existing `82 mm` left and `85 mm` right plates exceed it by
`8.698/11.698 mm`; shared growth `delta=0` is sufficient. Independent growth
is neither necessary nor useful.

The candidate still fails mandatory two-sided support: slot ends are closed,
but minimum outer endpoint material ratio is `0.0`, and
`allOuterEndpointProbesFull`, `allOuterSupportStripsContinuous`, and
`allNormalSidesSupported` are false. Failures occur on internal swept-path
normals, including right `upright` samples 27-60 and left
`diagonal`/`bottom` through contact/END. Those probes fall into another
portion of the rail cutter, not beyond the disk perimeter. Enlarging either
plate cannot restore material removed internally by the slot.

Therefore the exact variables reopened by R1 cannot close the final gate.
Changing rail topology/motion family or reducing the `0.30 mm` support rule is
a different authorization. R1 remains BLOCKED; this candidate must not be
implemented.

## R2 final bounded `C1` motion-law repair

R2 used one deterministic two-segment law, representing physical plate angle
against rod travel rather than Viewer easing. Named free parameters are the
terminal ramp width `h` and END slope `p`; the early slope is derived:

`m0 = [24 - 0.5 h p] / [1 - 0.5 h]`.

For `0<=u<=1-h`, `beta(u)=m0 u`. For `1-h<u<=1`, with
`q=u-(1-h)`,

`beta(u)=m0 u + (p-m0) q^2/(2h)`.

This is continuous and `C1`; `beta'(u)=m0` then ramps linearly to `p`.
Only cases with `m0>0` were admitted, so there is no dwell, cusp, reversal or
branch. Endpoints remain exactly `beta(0)=0`, `beta(1)=24 deg`; plates use
`-beta/+beta` at every `u`.

The bounded grid was `C_y=-12..3 mm`, `C_z=10..26 mm` in `1 mm` steps,
`h=0.10..0.40` in `0.05` steps, and `p=80..240 deg/u` in `20 deg/u` steps.
Dense contact-to-END sampling found `1,785` candidates passing angle,
multiplier-ratio and path-ratio gates. Rail polylines used 129 travel samples
for shortlist web ranking. No gate was weakened.

### Shortlist A — full actual-solid evaluation

- `C=(1,23) mm`, `h=0.10`, `p=240 deg/u`,
  `m0=12.631578947 deg/u`;
- `beta(contact)=18.965877697 deg`;
- minimum angle `18.233709 deg`, multiplier ratio `1.370194`, path ratio
  `1.423042`;
- minimum web `3.097874 mm` left and `6.389507 mm` right; all four plates are
  single valid solids and inverse residual is `8.38e-15 mm`;
- actual motion: `0.0 mm3` unintended intersection, guides/hardware clear,
  `0.75 mm` XT60 clearance, zero precontact wire intersection;
- service passes at `0.933816 mm` analytic / `1.25 mm` BREP clearance;
- nonlinear prescribed-pose rank `3`, maximum condition `73.397`.

It fails support: minimum outer endpoint material ratio `0.0`, normal-side,
endpoint-probe and continuous-strip booleans all false. Slot ends themselves
remain closed.

### Shortlist B — smoother focused support check

- `C=(1,22) mm`, `h=0.20`, `p=200 deg/u`,
  `m0=4.444444444 deg/u`;
- `beta(contact)=19.549160145 deg`;
- minimum angle `20.647251 deg`, multiplier ratio `1.497973`, path ratio
  `1.488114`;
- minimum web `2.902259 mm` left and `5.941184 mm` right; all plates valid.

Despite the broader, lower-acceleration ramp, minimum outer endpoint material
ratio remains `0.0`; normal-side, endpoint-probe and continuous-strip gates
remain false. Maximum detected swept-boundary recession is only `0.040087 mm`,
confirming the decisive failure is another internally swept rail region, not
the disk perimeter.

R2 therefore proves that this low-complexity monotone motion family can satisfy
force, web, collision and conditioning but cannot preserve the required
two-sided material under the frozen world tracks and slot width. The final
design status is BLOCKED. P17-I09 must not start. Any next move requires a new
user-authorized architectural constraint change, not another hidden repair.
