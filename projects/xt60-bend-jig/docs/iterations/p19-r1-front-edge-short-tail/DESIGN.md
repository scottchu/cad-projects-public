# P19 R1 front-edge short-tail 2D design gate — repair 1

Status: **REPAIRED CANDIDATE READY FOR INDEPENDENT CRITIC RECHECK; user 2D
acceptance and all 3D work remain blocked until that recheck passes.**

Owner/role: `/root/p19_kinematic_solver`, mechanism designer. Frozen baseline
commit: `bcc16305ff112ba814bdf19ad544a5819127e902`. The seven-entry
`DESIGN_INPUT_MANIFEST.sha256` passed; manifest SHA-256 is
`133ddcafbb153a33ad07be50ad9f3dda3a31d0df82d1446a00865ef7f64b404b`.
Focused repair input is `SERVICE_CRITIQUE.md` SHA-256
`eeeebf294dbd07b17856a4f2a24c8f3336d4a9c5da492f4aa6a45a283904fef5`.

## Frozen kinematics

Coordinates are millimetres in physical FRONT YZ: `+Y` is screen-right,
front/outward toward the short ESC tail; `+Z` is screen-up toward the XT60
mating head. Outer plates rotate about `C=(0.00,0.00)`. The real stepped
X-axis axle is at `A=(-13.00,-9.00)`, left/behind, keyed through both fixed
inner plates and journalled through both rotating outer plates. Its P18
nominal X length remains `34.90 mm`; A is not a virtual pivot or fourth rod.

- Left outer rotation: `alpha_left(u)=-10.00u deg`.
- Right force-outer rotation: `alpha_right(u)=+10.00u deg`.
- Three rods remain uncut `OD4.00 x 50.00 mm`, with six permanent caps.
- OPEN, END, C, A, topology, identity and service direction are unchanged by
  this repair.

| P18 rod identity / role | OPEN `(Y,Z)` | END `(Y,Z)` | inner stroke |
|---|---:|---:|---:|
| `bottom` / upper-left | `(5.00,10.00)` | `(8.00,9.00)` | `3.162 mm` |
| `diagonal` / upper-right | `(20.40,10.00)` | `(14.25,3.25)` | `9.132 mm` |
| `upright` / lower-right | `(20.40,-5.00)` | `(20.50,-2.50)` | `2.502 mm` |

OPEN is the exact ordered right angle `(5,10) -> (20.4,10) -> (20.4,-5)`.
END preserves the same identities on `Z=16.36-0.92Y`; the consecutive END
vectors are both `(6.25,-5.75)`, so no identity swaps or crossings occur.

## Plate hierarchy, tracks and deterministic rail law

The four plates retain the P18 size hierarchy:

- both fixed inner plates: `OD54.40 mm`, radius `27.20 mm`;
- left secondary-grip outer: `OD54.70 mm`, radius `27.35 mm`;
- right primary-force outer: `OD55.00 mm`, radius `27.50 mm` and largest.

Every OD4 rod track/rail uses the physically supported `OD4.15 mm` cutter
(`r=2.075 mm`). The separate fixed-axle outer guide retains P18
`OD7.90 mm` around its `OD7.60 mm` journal.

For each rod `i`, the only authoritative fixed-inner/world path is

`p_i(u)=OPEN_i+u(END_i-OPEN_i)`, `0<=u<=1`.

Inner rails are straight capsule sweeps of `p_i`. Every outer rail and axle
guide is inverse-derived, never hand-edited:

`q_s,i(u)=R(-alpha_s(u))p_i(u)` and
`qA_s(u)=R(-alpha_s(u))A`, `s in {left,right}`.

Outer rail endpoint/length values are unchanged from the frozen ±10-degree
law: left rod arcs `1.356/8.213/6.117 mm`, right rod arcs
`5.126/10.985/1.210 mm` in bottom/diagonal/upright order, and each axle-guide
arc is `2.760 mm`. The fingerprinted image shows the complete inner paths and
both side-specific inverse rail sweeps rather than endpoint-only sketches.

## Recomputed 2D web envelope

This is a centreline/cutter estimate, not exact BREP evidence. Each complete
inverse curve was sampled at 2,001 uniform u values; curve pairs were compared
at independent parameters. The limiting rod-centre radius is
`22.7191549 mm`. Rotation preserves this radius.

| owner / risk | estimated web |
|---|---:|
| fixed inner rim, `R27.20`, rod cutter `r2.075` | `2.405845 mm` |
| left outer rim, `R27.35`, rod cutter `r2.075` | `2.555845 mm` |
| right force-outer rim, `R27.50`, rod cutter `r2.075` | `2.705845 mm` |
| inner rail-to-rail minimum | `4.342644 mm` |
| left outer rail-to-rail minimum | `3.880027 mm` |
| right outer rail-to-rail minimum | `4.001896 mm` |
| minimum outer axle-guide to rod rail | `19.485198 mm` |
| left/right axle-guide to rim | `7.588612 / 7.738612 mm` |

Overall estimated minimum is the fixed-inner rim at `2.405845 mm`, only
`0.205845 mm` above the required `2.20 mm`. This maximum-front result is
explicitly marginal. Implementation must measure exact BREP and written STEP
webs including endpoint caps, AF8.15 hex corners, fillets and chamfers. A
failure may only move the whole frozen path set inward by the measured deficit
plus `0.20 mm`; it may not silently change topology or identities.

## Actual workpiece, contacts and outside-rim solder service

The repaired gate supersedes the old illustrative tail with a conservative
front-view workpiece envelope:

- insulated wire diameter: P18 `OD4.30 mm`;
- END wire centreline contact targets are a straight offset of the END rod
  line by `3.90 mm` along normal `(0.6770565,0.7359310)`:
  `F_bottom=(10.6405,11.8701)`, `F_diagonal=(16.8905,6.1201)`, and
  `F_upright=(23.1405,0.3701)`;
- a vertical ESC leg continues from `F_bottom` toward `+Z`, the formed diagonal
  connects the three targets, and a horizontal short tail continues from
  `F_upright` toward `+Y` to the XT60 solder cup;
- two real cup occurrences are separated in X in the four-plate stack; their
  coincident FRONT envelope is the conservative P18 actual-joint projection,
  `6.00 mm` wide in Y by `4.00 mm` long in Z, centred at
  `(Y,Z)=(32.25,0.3701)`;
- the XT60 body is outside/right of the plate with the cup at its lower end and
  mating head toward `+Z`; two short wire contacts enter the two cups from
  `-Y`. The remaining centreline length from `F_upright` to cup centre is
  `9.1095 mm`.

The existing conservative solder-tool front keepout is `8.00 x 8.00 mm`,
centred on the cup/tool centre at `Y=32.25`. Its left edge is `Y=28.25`, which
is exactly `0.75 mm` beyond the largest-plate tangent `Y=27.50`. Thus the
entire tool envelope—not merely its centreline—stays outside the OD55 plate.
The actual cup envelope itself begins at `Y=29.25`, `1.75 mm` outside that rim.
The nearest END rod surface to the cup rectangle is estimated at `6.793 mm`.

With combined rod/wire radius `4.15 mm`, the fixed-wire envelope gives OPEN
surface clearances `1.792/1.081/1.879 mm` for
bottom/diagonal/upright. Linear-path first geometric contacts occur at
`u≈0.8296/0.1185/0.8717`, and each named END rod has the explicitly selected
`-0.250 mm` geometric preload proxy. The non-simultaneous first contacts mean
the flexible wire deforms progressively; this is not a force or stress proof
and must be challenged in the critic recheck and later actual-solid/physical
validation.

## Force-direction and local constraint evidence

The image draws world rod-travel arrows, both hand-rotation arrows, and local
rail-tangent arrows. Critic-independent calculations identify the shallowest
rod/rail crossing as `2.752 deg` on the left `upright` at END and `3.101 deg`
on the right `bottom` at OPEN. These are non-zero but remain friction,
clearance-amplification and back-drive risks.

A 2,001-state normalized four-contact Jacobian probe, using the same
fixed-axle plus three inverse rod-rail normal constraints and P18 row
normalization, returned rank `3` throughout. Worst normalized condition is
`5.8409` left and `10.1768` right, both at END. This is local kinematic closure
evidence only; hand torque, rail pressure, wire damage, wedging and usable
force remain physical unknowns.

## Review artifact and acceptance boundary

The phone-format repair artifact is
`docs/review/p19-r1-front-edge-short-tail/design-repair1-b2597076bc82.png`.
Its full SHA-256 is
`b2597076bc821aec78cc3557c24edd9bf77f5c720a48a0975e56c5c6dbd8e675`;
the filename carries the first 12 hex characters.

This repair addresses plate hierarchy, measured rail fit, whole-tool service
clearance, explicit cup/wire contacts, force/tangent visibility, complete rail
sweeps and the real X-spanning axle inset. It does **not** establish exact
solids, collision/service cones in X, single-solid plates, cap/keeper clearance,
thermal safety, print fit, strength, retention, friction or physical usability.
No P19 source, test, STEP, slicer or continuity change is authorized until the
independent critic accepts this repaired 2D direction.
