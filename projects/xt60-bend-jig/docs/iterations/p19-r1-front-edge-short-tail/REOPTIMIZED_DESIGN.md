# P19 R1 option-2 minimum-travel re-optimized 2D design

Status: **ONE RECOMMENDED 2D CANDIDATE FROZEN FOR INDEPENDENT CRITIQUE.**
This is not authorization for 3D CAD, STEP, slicing, printing, or physical
acceptance.

Owner/role: `/root/p19_min_rail_optimizer`, mechanism/optimizer designer.
Frozen input: `REOPTIMIZE_INPUT.sha256`, verified `7/7` from the repository
root. Baseline remains Git commit
`bcc16305ff112ba814bdf19ad544a5819127e902` and the repaired P19 R1
front-edge candidate.

## Result

The user-selected option 2 is feasible without hand-extending any rail. Keep
the repaired OPEN triangle, fixed axle, rotation centre, plate hierarchy and
service envelope unchanged; translate the complete ordered END diagonal by
only `(+1.20 Y, -0.10 Z) mm` and increase equal/opposite outer rotation from
`10.0 deg` to `12.2 deg`.

This raises the shortest inverse-derived outer-rail centre travel from
`1.209836 mm` to `2.142936 mm`. All six rod rails clear the hard
`>=2.00 mm` requirement. The limiting 2D material web remains the unchanged
fixed-inner rim estimate `2.405845 mm`, above the required `2.20 mm`.

## Frozen coordinates and topology

Coordinates are millimetres in physical FRONT YZ: `+Y` is screen-right,
front/outward toward the short ESC tail and soldering tool; `+Z` is screen-up
toward the XT60 mating head.

- Outer rotation centre: `C=(0.00, 0.00)`.
- Real stepped X-axis axle: `A=(-13.00, -9.00)`, nominal X length
  `34.90 mm`, keyed through both fixed inner plates and journalled through both
  rotating outer plates.
- Left outer motion: `alpha_left(u)=-12.20u deg`.
- Right force-outer motion: `alpha_right(u)=+12.20u deg`.
- OPEN remains the exact ordered right angle
  `bottom -> diagonal -> upright`, with an exactly horizontal first leg and
  exactly vertical second leg.
- END remains one exact ordered, equal-pitch diagonal; both consecutive
  vectors remain `(6.25,-5.75)`.

| P18/P19 rod identity | OPEN `(Y,Z)` | END `(Y,Z)` | fixed-inner/world stroke |
|---|---:|---:|---:|
| `bottom` / upper-left | `(5.00,10.00)` | `(9.20,8.90)` | `4.341659 mm` |
| `diagonal` / upper-right | `(20.40,10.00)` | `(15.45,3.15)` | `8.451331 mm` |
| `upright` / lower-right | `(20.40,-5.00)` | `(21.70,-2.60)` | `2.729469 mm` |

Rod identities do not swap. The three straight fixed-inner/world paths are
continuous and non-crossing. Three uncut `OD4.00 x 50.00 mm` stainless rods,
six permanent caps, four plates, fixed inner plates and opposite rotating
outer plates remain unchanged.

## Deterministic rail law

The only authoritative fixed-inner/world centre path for rod `i` is

```text
p_i(u) = OPEN_i + u (END_i - OPEN_i),  0 <= u <= 1
```

Every outer rod rail is derived from that same physical path in its plate's
inverse frame:

```text
q_s,i(u) = R(-alpha_s(u)) p_i(u),  s in {left,right}
```

The fixed-axle outer guide remains independently inverse-derived from the
fixed real axle:

```text
qA_s(u) = R(-alpha_s(u)) A
```

No endpoint margin or decorative extension was added. The fixed-inner and
outer rod cutter remains `OD4.15 mm`; the axle guide remains `OD7.90 mm`
around its `OD7.60 mm` journal.

## Bounded search and objective

Only three numeric variables were searched:

1. common END translation `delta_end_Y`;
2. common END translation `delta_end_Z`;
3. common equal/opposite twist magnitude `theta`.

OPEN, C, A, rod identities, diagonal pitch, service direction, cup/tool
envelope and plate diameters were not optimizer variables. The deterministic
refinement grid was:

```text
theta       = 11.3 .. 12.8 deg in 0.1-deg steps
delta_end_Y = 1.20 .. 1.80 mm in 0.05-mm steps
delta_end_Z = -0.50 .. +0.50 mm in 0.10-mm steps
```

Each grid point sampled every inverse curve and rejected any point failing
the outer-rail travel, `2.20 mm` web, plate envelope, topology, identity,
outside-tool or nonzero force-crossing gates. A stricter screening margin of
`2.05 mm` rail travel and `2.25 mm` internal web was used. Of the refined grid
points, `510` survived that sampled robust screen.

The ranking objective minimized deviation from repaired P19 plus unnecessary
plate/rail/conditioning burden:

```text
J = 0.04(theta-10)^2
  + 0.70(delta_end_Y^2 + delta_end_Z^2)
  + 100 max(0, 2.12-min_rail_travel)
  + 100 max(0, 2.35-min_outer_internal_web)
  + 2 max(0, 4-min_crossing_deg)
```

The selected point was the lowest-scoring screened point and was then
recomputed using `200,001` samples for curve arc/chord/crossing quantities,
`2,001` independent-parameter samples for 2D curve-to-curve web estimates,
and `2,001` states per side for the four-contact conditioning probe. There is
no random seed, tessellation-dependent choice or manual rail edit.

## All six outer rod rails

Arc is the centreline travel of the authoritative inverse curve. Full swept
capsule length proxy is `arc + 4.15 mm`; nominal diametral rail gap is
`0.15 mm`.

| outer plate / rod | centre arc | endpoint chord | sagitta | full capsule proxy | arc / nominal gap | minimum path/rail crossing |
|---|---:|---:|---:|---:|---:|---:|
| left / `bottom` | **2.239287** | `2.207227` | `0.163207` | `6.389287` | `14.93x` | `13.698 deg` |
| left / `diagonal` | `7.052051` | `6.996000` | `0.383841` | `11.202051` | `47.01x` | `21.796 deg` |
| left / `upright` | `7.199993` | `7.174427` | `0.262415` | `11.349993` | `48.00x` | `9.120 deg` |
| right / `bottom` | `6.744079` | `6.709960` | `0.293265` | `10.894079` | `44.96x` | `4.205 deg` |
| right / `diagonal` | `11.252912` | `11.190345` | `0.512880` | `15.402912` | `75.02x` | `12.972 deg` |
| right / `upright` | **2.142936** | `2.142920` | `0.003391` | `6.292936` | `14.29x` | `35.347 deg` |

The shortest rail exceeds the hard limit by `0.142936 mm`. Both formerly
short rails now provide more than fourteen nominal diametral-clearance units
of centre travel. The right/upright curve still has very small sagitta and
will act like a short straight capsule in printed PETG; the minimum-travel
constraint improves travel but does not prove physical fit or force.

Each fixed-axle guide centre arc is `3.366722 mm` (`|A-C| * radians(12.2)`),
inverse-derived from the same plate law and not counted among the six rod
rails.

## Plate envelope and 2D web estimates

The hierarchy is unchanged:

- fixed inner plates: `OD54.40 mm`, radius `27.20 mm`;
- left secondary-grip outer: `OD54.70 mm`, radius `27.35 mm`;
- right primary-force outer: `OD55.00 mm`, radius `27.50 mm`.

The unchanged OPEN upper-right centre at `(20.4,10.0)` remains the maximum
rod-centre radius, `22.719155 mm`, so it still controls every rim estimate.

| estimate | minimum web |
|---|---:|
| fixed-inner rim | **2.405845 mm** |
| left-outer rim | `2.555845 mm` |
| right-force-outer rim | `2.705845 mm` |
| fixed-inner rail-to-rail | `4.283583 mm` |
| left-outer rail-to-rail | `3.707542 mm` |
| right-outer rail-to-rail | **2.531360 mm** |
| minimum outer axle-guide to rod rail | `19.314173 mm` |

Overall estimated minimum remains `2.405845 mm`, only `0.205845 mm` above
the requirement. These are centreline/cutter estimates, not exact BREP or
written-STEP evidence. Later implementation must measure complete endpoint
caps, the exact AF8.15 hex corners, fillets and chamfers.

## Service geometry

The repaired P19 conservative workpiece construction remains authoritative.
The END diagonal slope and normal are unchanged; translating the complete END
line gives wire contact targets:

```text
F_bottom   = (11.840520, 11.770131)
F_diagonal = (18.090520,  6.020131)
F_upright  = (24.340520,  0.270131)
```

The cup/tool centre is `(32.25,0.270131)`. The remaining short-tail
centreline from `F_upright` to the cup is reduced from `9.109480 mm` to
`7.909480 mm`, moving the working triangle closer to the short FPV ESC joint.

- Complete solder-tool keepout: `8 x 8 mm`.
- Tool left edge: `Y=28.25 mm`.
- Largest OD55 right tangent: `Y=27.50 mm`.
- Whole-tool outside clearance: **`0.75 mm`**.
- Cup left edge: `Y=29.25 mm`, or `1.75 mm` outside the largest rim.
- XT60 mating head remains `+Z`; short tail and tool approach remain `+Y`.

## Four-contact closure and conditioning

The dimensionless four-contact probe uses row order
`fixed axle, upright, bottom, diagonal`, pose coordinates
`deltaY, deltaZ, alpha`, characteristic radius `22.719155 mm`, and unit-row
normalization after rotation-column scaling. It sampled `2,001` states per
side.

| outer plate | minimum rank | worst normalized condition | state |
|---|---:|---:|---:|
| left | `3` | `7.476587` | END (`u=1`) |
| right | `3` | `4.322530` | END (`u=1`) |

This proves only local nominal centreline closure. It does not prove hand
torque, friction, self-lock, back-drive resistance, print fit, rail pressure,
wire safety or usable clamp force.

## Delta versus repaired P19 candidate

| item | repair 1 | option-2 candidate | delta |
|---|---:|---:|---:|
| twist magnitude per side | `10.0 deg` | `12.2 deg` | `+2.2 deg` |
| OPEN coordinates | frozen | unchanged | `0` |
| END common placement | baseline | `+1.20Y,-0.10Z` | small rigid END translation |
| shortest left rail | `1.356484 mm` | `2.239287 mm` | `+0.882803 mm` |
| shortest right rail | `1.209836 mm` | `2.142936 mm` | `+0.933100 mm` |
| min outer internal web | `3.880027 mm` | `2.531360 mm` | `-1.348667 mm`, still passes |
| overall estimated web | `2.405845 mm` | `2.405845 mm` | unchanged |
| worst normalized condition | `10.1768` | `7.4766` | improved globally |
| short-tail centreline | `9.109480 mm` | `7.909480 mm` | `-1.200000 mm` |
| tool outside clearance | `0.75 mm` | `0.75 mm` | unchanged |
| plate diameters | `54.4/54.7/55.0` | unchanged | `0` |

The tradeoff is explicit: the six-rail travel requirement consumes some
right-outer rail-to-rail web and slightly worsens left-side END conditioning,
while improving the previous global conditioning maximum and moving the
clamp closer to the short-tail joint.

## Requirement disposition

| requirement | 2D result |
|---|---|
| Six outer rod rails each `>=2.00 mm` centre travel | **PASS**, minimum `2.142936 mm` |
| No hand-extended rail | **PASS**, all are `q_s,i(u)` inverse transforms |
| `+Z` head/up; `+Y` tail/tool/right | **PASS** |
| OPEN exact ordered right angle | **PASS**, unchanged |
| END exact ordered diagonal | **PASS**, equal pitch preserved |
| Rod identities unchanged/non-crossing | **PASS** |
| Fixed real X-axis axle left/behind | **PASS**, `A=(-13,-9)` unchanged |
| Fixed inner / opposite rotating outer plates | **PASS**, `±12.2 deg` |
| Rotation no more than `45 deg` | **PASS** |
| `3 x OD4 x 50 mm`, six permanent caps | **PASS**, unchanged contract |
| OD4.15 rod-rail cutter | **PASS** |
| Plate ODs `50-55`, inner < left outer < right force outer | **PASS**, `54.4 < 54.7 < 55.0` |
| Estimated 2D web `>=2.20 mm` | **PASS**, minimum `2.405845 mm` |
| Complete `8 x 8` tool keepout at least `0.75 mm` outside rim | **PASS**, exactly `0.75 mm` |
| Short-tail/cup service with clamp near front | **PASS for 2D direction**, tail `7.909480 mm` |
| Four-contact local closure | **PASS**, rank `3` throughout sampled states |
| No new part, lock, grip or stability bar | **PASS** |
| Exact solids / X-separated tool cone / print force and fit | **NOT YET PROVEN**; later gates only |

## Review artifact and remaining risks

Phone-viewable artifact:
`docs/review/p19-r1-front-edge-short-tail/reoptimized-option2-mintravel.png`.
It shows the exact OPEN/END placement, fixed real axle, outside tool/cup
envelopes, short-tail route and both complete inverse outer-rail families.

Remaining physical risks are the marginal `0.205845 mm` 2D web margin, the
right/upright rail's nearly straight `0.003391 mm` sagitta, printed PETG bore
scatter, friction/back-drive, required hand torque, endpoint loading, cap and
keeper clearance, heat exposure, short ESC-wire deformation, exact X service
cone and true clamp force. Independent 2D critique must reproduce this exact
candidate before the user is asked to freeze it for 3D.
