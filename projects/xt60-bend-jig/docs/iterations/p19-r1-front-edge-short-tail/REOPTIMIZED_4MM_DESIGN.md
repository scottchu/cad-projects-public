# P19 R1 cycle-3 four-millimetre rail re-optimization

Status: **ONE 2D CANDIDATE FROZEN FOR INDEPENDENT CRITIQUE.** The cycle-2
`2 mm` candidate is superseded. This record does not authorize 3D CAD, STEP,
slicing, printing, force claims or physical acceptance.

Owner/role: `/root/p19_min_rail_optimizer`, mechanism/optimizer designer.
Frozen input: `REOPTIMIZE_4MM_INPUT.sha256`, verified `8/8` from repository
root. Baseline Git commit remains
`bcc16305ff112ba814bdf19ad544a5819127e902`.

## Recommended result

The `>=4.00 mm` requirement is feasible without reopening `C`, `A`, OPEN,
plate diameters, service geometry or topology and without extending any rail
past its physical inverse path.

- Keep OPEN unchanged.
- Translate the complete equal-pitch END diagonal by
  `delta_END=(+2.25Y,+3.00Z) mm` relative to repaired P19.
- Use equal/opposite outer rotation `-5.00 deg / +5.00 deg`.

All six inverse outer rod rails exceed `4.00 mm`. The shortest is the
right/upright rail at `4.212461 mm`; its complete OD4.15 capsule proxy is
`8.362461 mm` and aspect is `2.015051`, above the required `1.963855`.

## Coordinate frame, fixed objects and exact topology

Coordinates are millimetres in physical FRONT YZ. `+Y` is screen-right,
front/outward toward the short ESC tail and soldering tool. `+Z` is screen-up
toward the XT60 mating head.

- Outer rotation centre stays `C=(0.00,0.00)`.
- The real stepped axle stays `A=(-13.00,-9.00)`, left/behind, as one
  continuous `34.90 mm` X-axis structural member keyed through both fixed
  inner plates and journalled through both outer plates.
- Left outer law: `alpha_left(u)=-5.00u deg`.
- Right force-outer law: `alpha_right(u)=+5.00u deg`.
- Three uncut `OD4 x 50 mm` stainless rods, six permanent caps, four plates,
  fixed inner plates and opposite rotating outer plates remain invariant.

| rod identity | OPEN `(Y,Z)` | END `(Y,Z)` | world stroke |
|---|---:|---:|---:|
| `bottom` / upper-left | `(5.00,10.00)` | `(10.25,12.00)` | `5.618051 mm` |
| `diagonal` / upper-right | `(20.40,10.00)` | `(16.50,6.25)` | `5.410407 mm` |
| `upright` / lower-right | `(20.40,-5.00)` | `(22.75,0.50)` | `5.981012 mm` |

OPEN is still the exact ordered right angle
`(5,10) -> (20.4,10) -> (20.4,-5)`: the first leg is exactly horizontal and
the second exactly vertical. END is still one exact ordered equal-pitch
diagonal; both consecutive vectors are `(6.25,-5.75)`. The three identity
paths are continuous and non-crossing.

## Authoritative parametric rail law

For each named rod `i`, the fixed-inner/world path is

```text
p_i(u) = OPEN_i + u (END_i - OPEN_i),  0 <= u <= 1
```

Outer rod rails are only the exact inverse images of those paths:

```text
q_s,i(u) = R(-alpha_s(u)) p_i(u),  s in {left,right}
```

The fixed-axle outer guide remains

```text
qA_s(u) = R(-alpha_s(u)) A
```

Every rod rail uses the named `OD4.15 mm` cutter. The axle guide remains
`OD7.90 mm` around the `OD7.60 mm` journal. No endpoint padding, decorative
travel or manual rail extension was added. Each axle-guide centre arc is
`1.379804 mm`; axle-guide travel is not one of the six rod-rail gates.

## Bounded deterministic search

The first search varied only the three variables allowed before any reopening:

1. equal/opposite twist magnitude `theta`;
2. common END translation `delta_END_Y`;
3. common END translation `delta_END_Z`.

`C`, `A`, OPEN, END pitch/slope, plate hierarchy, cup/tool envelope and all
identities were frozen. The deterministic broad grid covered

```text
theta       = 5.0 .. 45.0 deg, 0.25-deg spacing
delta_END_Y = 0.0 .. 4.0 mm,   0.25-mm spacing
delta_END_Z = -5.0 .. 4.0 mm,  0.25-mm spacing
```

and the feasible low-angle family was refined over

```text
theta       = 4.5 .. 7.0 deg, 0.05-deg spacing
delta_END_Y = 2.0 .. 2.5 mm,  0.025-mm spacing
delta_END_Z = 2.75 .. 3.75 mm, 0.025-mm spacing
```

Every point derived all six outer curves from `q_s,i`, then rejected failures
of rail travel, capsule aspect, topology, identity, plate/rim/internal web,
tool keepout, short-tail direction, nonzero crossing or rank. Selection was
lexicographic:

1. all hard requirements;
2. robust sampled targets `min rail >=4.20`, inner-rim web `>=2.35`, outer
   internal web `>=3.50`;
3. minimum normalized deviation from cycle 2;
4. lower worst four-contact condition among the surviving compact shortlist.

No extra variable was reopened because this original three-variable space was
feasible. The frozen candidate was recomputed with `200,001` samples for arc,
chord, sagitta and crossing, `2,001`-point polylines for independent-parameter
web estimates, and `2,001` states per side for conditioning. No randomized
operation, CAD tessellation or image measurement enters the result.

## All six inverse rod rails

Full capsule proxy is `centre arc + 4.15 mm`; aspect is that value divided by
`4.15 mm`. Nominal diametral rod/rail gap is `0.15 mm`.

| outer plate / rod | centre arc | endpoint chord | sagitta | full capsule proxy | aspect | arc / nominal gap | minimum crossing |
|---|---:|---:|---:|---:|---:|---:|---:|
| left / `bottom` | `5.052562` | `5.045550` | `0.115213` | `9.202562` | `2.217485` | `33.68x` | `8.245 deg` |
| left / `diagonal` | `5.083225` | `5.076732` | `0.111205` | `9.233225` | `2.224874` | `33.89x` | `16.418 deg` |
| left / `upright` | `7.811007` | `7.803298` | `0.150220` | `11.961007` | `2.882170` | `52.07x` | **`2.193 deg`** |
| right / `bottom` | `6.353263` | `6.346184` | `0.129820` | `10.503263` | `2.530907` | `42.36x` | `6.528 deg` |
| right / `diagonal` | `6.239376` | `6.232702` | `0.124917` | `10.389376` | `2.503464` | `41.60x` | `13.246 deg` |
| right / `upright` | **`4.212461`** | `4.204717` | `0.110548` | **`8.362461`** | **`2.015051`** | `28.08x` | `4.088 deg` |

The `4 mm` gate is met by physical centre travel, not by cutter diameter or
an illustrated slot tail. The shortest rail exceeds the hard limit by
`0.212461 mm` and its aspect exceeds the hard proxy by `0.051196`.

The shallowest crossing is now left/upright `2.192572 deg`; this is nonzero
but worse than repaired P19's `2.752 deg` global minimum. The cycle-3 rail
length improvement therefore does not imply better force transfer. This is a
visible unresolved force/clearance/back-drive risk, not a pass-by-omission.

## Plate envelope and 2D web

Plate hierarchy remains:

- fixed inner: `OD54.40 mm`, radius `27.20 mm`;
- left secondary-grip outer: `OD54.70 mm`, radius `27.35 mm`;
- right primary-force outer: `OD55.00 mm`, radius `27.50 mm`.

The limiting rod-centre radius is `22.755494 mm` at the new END upright.

| estimate | minimum web |
|---|---:|
| fixed-inner rim | **`2.369506 mm`** |
| left-outer rim | `2.519506 mm` |
| right-force-outer rim | `2.669506 mm` |
| fixed-inner rail-to-rail | `4.326720 mm` |
| left-outer rail-to-rail | `3.632161 mm` |
| right-outer rail-to-rail | `4.185938 mm` |
| minimum outer axle-guide to rod rail | `19.840109 mm` |

Overall estimated minimum is the fixed-inner rim, `0.169506 mm` above the
required `2.20 mm`. These are 2D centreline/cutter estimates only. Exact BREP
must later include endpoint caps, AF8.15 hex corners, fillets and chamfers.

## Short-tail and solder-tool service

The END diagonal slope and wire-normal construction are unchanged. New
contact targets are

```text
F_bottom   = (12.890520,14.870131)
F_diagonal = (19.140520, 9.120131)
F_upright  = (25.390520, 3.370131)
```

The cup/tool centre is `(32.25,3.370131)`. The horizontal short-tail
centreline is `6.859480 mm`, `1.050000 mm` shorter than cycle 2.

- Complete tool keepout remains `8 x 8 mm`.
- Tool left edge remains `Y=28.25 mm`.
- Largest OD55 tangent remains `Y=27.50 mm`.
- Complete-tool outside clearance remains **`0.75 mm`**.
- Cup left edge remains `Y=29.25 mm`, `1.75 mm` outside the largest rim.
- XT60 head remains `+Z`; short tail and tool approach remain `+Y`.

## Closure and conditioning

The normalized four-contact probe uses row order
`fixed axle, upright, bottom, diagonal`, pose coordinates
`deltaY, deltaZ, alpha`, characteristic radius `22.755494 mm`, and unit row
normalization after rotation-column scaling.

| outer plate | minimum rank over 2,001 states | worst normalized condition | state |
|---|---:|---:|---:|
| left | `3` | `10.629803` | END (`u=1`) |
| right | `3` | **`43.357104`** | END (`u=1`) |

Rank remains three, but conditioning is materially worse than cycle 2,
especially on the right. This is only nominal local centreline closure. It
does not establish usable hand torque, stiffness, friction, self-lock,
back-drive resistance or physical fit.

## Delta versus superseded cycle 2

| item | superseded 2 mm candidate | cycle-3 4 mm candidate | delta |
|---|---:|---:|---:|
| twist magnitude per side | `12.2 deg` | `5.0 deg` | `-7.2 deg` |
| OPEN | frozen | unchanged | `0` |
| END common delta vs repaired P19 | `(+1.20,-0.10)` | `(+2.25,+3.00)` | `(+1.05,+3.10)` |
| shortest left rail | `2.239287` | `5.052562` | `+2.813275 mm` |
| shortest right rail | `2.142936` | `4.212461` | `+2.069525 mm` |
| minimum capsule aspect | `1.516371` | `2.015051` | `+0.498680` |
| overall estimated web | `2.405845` | `2.369506` | `-0.036339 mm` |
| minimum outer internal web | `2.531360` | `3.632161` | `+1.100801 mm` |
| left/right worst condition | `7.4766 / 4.3225` | `10.6298 / 43.3571` | materially worse |
| shortest crossing | `4.205 deg` | `2.193 deg` | worse |
| short-tail centreline | `7.909480` | `6.859480` | `-1.050000 mm` |
| tool outside clearance | `0.75` | `0.75` | unchanged |
| plate ODs | `54.4/54.7/55.0` | unchanged | `0` |

Cycle 3 solves the user-visible short-rail problem with real inverse travel
and gives more rail-to-rail material, but it does so by increasing physical
rod strokes while reducing the plate twist angle. That tradeoff worsens the
local force angle and right-side conditioning and must be independently
challenged before user review.

## Requirement disposition

| requirement | cycle-3 2D result |
|---|---|
| Six outer rod rails each `>=4.00 mm` | **PASS**, minimum `4.212461 mm` |
| Capsule aspect each `>=1.963855` | **PASS**, minimum `2.015051` |
| No manual outer-rail extension | **PASS**, all are exact inverse curves |
| Physical `+Z` head/up and `+Y` tail/tool/right | **PASS** |
| OPEN exact ordered right angle | **PASS**, unchanged |
| END exact ordered equal-pitch diagonal | **PASS** |
| Identity/non-crossing | **PASS** |
| `C=(0,0)` and real axle `A=(-13,-9)` through four plates | **PASS**, unchanged |
| Fixed inners/opposite rotating outers, twist `<=45 deg` | **PASS**, `±5 deg` |
| Three OD4 x 50 rods and six permanent caps | **PASS**, unchanged |
| OD4.15 rail cutter | **PASS** |
| ODs `50-55`, inner < left outer < right force outer | **PASS** |
| Estimated web `>=2.20 mm` | **PASS**, minimum `2.369506 mm` |
| Whole `8 x 8` tool keepout `>=0.75 mm` outside rim | **PASS**, exactly `0.75 mm` |
| Short-tail service and clamp near front | **PASS for 2D direction**, `6.859480 mm` |
| Rank-three local closure | **PASS**, rank `3` throughout samples |
| Usable force/conditioning | **UNRESOLVED RISK**, `2.193 deg`, condition `43.36` |
| No added part/grip/lock/self-lock claim | **PASS** |
| Exact solids, X service cone, print fit/force/heat | **NOT YET PROVEN** |

## Review boundary and physical risks

The phone PNG must show OPEN, END, fixed real axle, complete tool/cup
envelopes, short-tail route, all six inverse rails and an X-section proving
that A is one member through all four plates.

Review artifact:
`docs/review/p19-r1-front-edge-short-tail/reoptimized-4mm-gate.png`.

Independent critique must reproduce the exact six travel/aspect gates, web,
service, topology, inverse law, crossing and conditioning before this may be
shown as the active 2D gate. Later 3D/physical work must separately resolve
the marginal rim margin, shallow left/upright crossing, poor right END
conditioning, PETG rail fit, hand force, back-drive, cap/keeper clearance,
wire deformation, heat and the X-separated solder-tool cone.
