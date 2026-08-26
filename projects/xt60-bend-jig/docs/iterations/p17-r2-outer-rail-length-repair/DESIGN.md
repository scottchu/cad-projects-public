# P17-D12-R1 implementable rail/placement contract

All dimensions are millimetres in world `(Y,Z)`. `+Z` is XT60 head/up and
`+Y` is tails/wires/right, independent of camera orientation.

## 1. Frozen parameters

```text
A = (-29.000, 17.000)               fixed axle, unchanged
C = (  3.000, 12.000)               physical outer datum, unchanged
T = (-16.735,-14.935)               rigid complete-working-set translation
C_rel = C - T = (19.735,26.935)     functional relative datum
theta(u) = 24.00 u deg, 0 <= u <= 1
alpha_left = -theta; alpha_right = +theta
slot width = 4.15; slot radius = 2.075
```

`T` applies once to every rod state, XT60 body, bend/wire geometry, completed-
pigtail service geometry and derived working reference. It does not apply to
`A`, `C`, plate envelopes or keepers. D12 `T=(-7,-6.5)` is superseded.

Translated rod centers are:

| identity | OPEN | first contact | CLAMPED/END |
|---|---:|---:|---:|
| Rod 1 / `bottom` | `(-20.9852813742,9.500)` | `(-10.650,9.500)` | `(-10.400,9.500)` |
| middle / `diagonal` | `(5.500,9.500)` | `(-1.8081475452,2.1918524548)` | `(-1.9849242405,2.0150757595)` |
| Rod 2 / `upright` | `(5.500,-16.9852813742)` | `(5.500,-6.650)` | `(5.500,-6.400)` |

The common straight inner stroke remains `10.5852813742`; exact contact is
`theta=23.4331751998 deg`. Translation preserves every triangle area, edge,
track direction and workpiece-to-rod dimension.

The translated workpiece has bend center `B=(-0.500,3.500)`, radius `6.00`,
upward straight-leg reference `Y=-6.500`, rightward horizontal-leg reference
`Z=-2.500`, XT60 body center `(-6.500,22.500)`, and completed-pigtail extract
end `Y=17.265`.

## 2. Exact inverse rails and effective lengths

For translated rod center `r_i(u)=O_i+u(E_i-O_i)`, generate only the existing
inverse-transform centerline:

`q_s,i(u)=R[-alpha_s(u)] [r_i(u)-C]`, `0<=u<=1`.

Do not widen, layer, offset, branch, extend or redraw it.

| rod | side | `q(OPEN)` | `q(contact)` | `q(END)` |
|---|---|---:|---:|---:|
| Rod 1 | left | `(-23.985281374,-2.500)` | `(-11.530011605,-7.722132632)` | `(-11.224667525,-7.734134661)` |
| Rod 1 | right | `(-23.985281374,-2.500)` | `(-13.518407700,3.134510049)` | `(-13.258350740,3.166407373)` |
| middle | left | `(2.500,-2.500)` | `(-0.511096796,-10.911316197)` | `(-0.492720330,-11.149233536)` |
| middle | right | `(2.500,-2.500)` | `(-8.312089709,-7.087115475)` | `(-8.615189464,-7.094130833)` |
| Rod 2 | left | `(2.500,-28.985281374)` | `(9.710528727,-16.117634189)` | `(9.767817877,-15.792394813)` |
| Rod 2 | right | `(2.500,-28.985281374)` | `(-5.122906144,-18.106030284)` | `(-5.200090588,-17.826078028)` |

| rod | left OPEN-END | right OPEN-END | ratio | left contact-END | right contact-END | ratio |
|---|---:|---:|---:|---:|---:|---:|
| Rod 1 | `14.062509916` | `12.380157783` | `1.135891009` | `0.305583622` | `0.262009384` | `1.166307930` |
| middle | `9.452391469` | `12.332546705` | `1.304701222` | `0.238629650` | `0.303184826` | `1.270524536` |
| Rod 2 | `15.321870406` | `13.793481567` | `1.110805153` | `0.330249997` | `0.290400787` | `1.137221427` |

The maximum functional full-rail ratio is `1.304701222`, replacing the
rejected D12 maximum `2.012551004`; all three pass `<=1.50`. Rounded capsule
material outside `q(OPEN)` and `q(END)` is not counted as travel.

## 3. Force diagnostic

`phi` is the acute angle between an outer-rail tangent and its straight inner
track. `1/sin(phi)` is a frictionless geometric diagnostic, not hand force.

| rod | left minimum `phi` / multiplier | right minimum `phi` / multiplier | multiplier ratio |
|---|---:|---:|---:|
| Rod 1 | `25.758539 deg / 2.301075x` | `30.475993 deg / 1.971697x` | `1.167053` |
| middle | `25.431746 deg / 2.328638x` | `19.737418 deg / 2.961120x` | `1.271610` |
| Rod 2 | `33.527406 deg / 1.810493x` | `38.940400 deg / 1.591060x` | `1.137916` |

All terminal angles exceed D11's diagnostic `18 deg` reference. Real force,
friction, PETG wear/compliance and wire stiffness remain physical unknowns.

## 4. Actual-solid evidence for the selected candidate

Read-only evaluation of the current parametric source with only the candidate
translation substituted returned:

- inverse reconstruction `<=5.403e-15`; all four plates valid single solids;
- minimum actual rail/fixed-feature web `2.247514 >=2.20`; inner-hex boundary
  web `2.906326`; outer boundary web left/right `4.661731/6.161731`;
- minimum exact fixed-feature gap `2.247514`; axle, keepers, rods, caps,
  workpiece and service features clear;
- support endpoint material ratio `0.9999999999999983`; all normal sides,
  continuous swept-boundary-to-`+0.30` strips and closed ends pass; maximum
  boundary recession `0.005098333`;
- unintended motion intersection `0.0`, all guides/fixed hardware clear,
  minimum XT60 clearance `0.750000`;
- service clearance `0.933816 >=0.75`, zero service intersection;
- normalized condition `11.634573`, minimum sigma ratio `0.085951`, rank `3`.

The exact `1.0` ratio candidate is rejected evidence, not an alternative: web
`-0.304997`, fixed-feature gap `0`, and keeper/cap clearance fail. On the
`0.01 mm` analytic/solid frontier, `d=2.44` has web `2.193821` and fails;
`d=2.45` has web `2.202770` but only `0.002770` margin. Selected `d=2.50`
retains `0.047514` nominal margin with maximum ratio still only `1.304701`.

## 5. Implementation done gate

Implementation must replace the paused D12 translation, regenerate all derived
states/artifacts, and prove:

1. exact `T`, translated coordinates, rail endpoints and length tables above;
2. unchanged relative triangles/workpiece/inner tracks and continuous identity;
3. three `OD4 x 50` rods, six permanent caps, two fixed inners, two opposite
   outers, one axle, two keepers, and larger right outer plate;
4. `4.15` slots, occupied-segment `0.30` two-sided reaction material, closed
   ends, minimum web `>=2.20`, and no self-return/wobble cavity;
5. inverse reconstruction, no cusp/reversal/branch, rank/conditioning,
   collision, XT60/wire contact timing, service and source/STEP parity gates;
6. no added mechanism/part and no physical-force or self-lock claim.

## 6. P17-D12-R2 superseding numeric contract

This section supersedes Sections 1–4 only where they name the D12-R1
translation, absolute world coordinates, inverse-rail coordinates, length/
angle diagnostics, placement comparison or evidence values. Architecture,
equations and the implementation gates remain unchanged.

### 6.1 Placement and front-view check

```text
A = (-29.000,17.000)               unchanged physical axle
C = (  3.000,12.000)               unchanged physical outer datum
T = (-12.350,-10.550)              complete working set, applied once
C_rel = C - T = (15.350,22.550)
theta(u) = 24.00 u deg
alpha_left/right = -theta/+theta
```

The OPEN working-set box relative to plate datum `C` moves from I10 midpoint
`(-10.743,-15.743)` to `(-6.358,-11.358)`. The combined six-rail terminal box
moves from midpoint about `(-7.109,-12.909)` to `(-3.805,-9.593)`. Both are an
exact `(+4.385,+4.385)` screen-right/up correction of the underlying rigid
working set; rotation makes the six-rail box improvement non-rigid at its
individual extrema.

```text
front view (+Z up, +Y right)

                    +Z
                     ^
     I10 OPEN        |       D12-R2 OPEN
   UL------UR        |        UL------UR
            |        |                 |
            |        |                 |
            LR       |                 LR
     midpoint         |          midpoint
  (-10.743,-15.743)   |       (-6.358,-11.358)
                     +------------------------> +Y
                     C=(3,12), plate datum
```

Candidate comparison:

| candidate `T` | right/up from I10 | worst full/contact ratio | minimum contact angle | minimum web | disposition |
|---|---:|---:|---:|---:|---|
| `(-16.735,-14.935)` | `(0,0)` | `1.304701/1.270525` | `19.737 deg` | `2.247514` | rejected visual placement |
| `(-12.000,-7.000)` | `(+4.735,+7.935)` | `1.505677/1.634586` | `2.968 deg` | `4.577647` | rejected force diagnostic |
| `(-15.500,-9.275)` | `(+1.235,+5.660)` | `1.215214/1.264891` | `12.004 deg` | `1.282081` | rejected web |
| `(-13.775,-11.950)` | `(+2.960,+2.985)` | `1.317303/1.367694` | `12.024 deg` | `3.805457` | safe but insufficient visual correction |
| `(-12.300,-10.500)` | `(+4.435,+4.435)` | `1.410168/1.520188` | `8.029 deg` | `4.686526` | rejected marginal angle floor |
| **`(-12.350,-10.550)`** | **`(+4.385,+4.385)`** | **`1.405804/1.514484`** | **`8.167 deg`** | **`4.651876`** | **selected** |

### 6.2 World rod and workpiece coordinates

| identity | OPEN | first contact | CLAMPED/END |
|---|---:|---:|---:|
| Rod 1 / `bottom` | `(-16.6002813742,13.885)` | `(-6.265,13.885)` | `(-6.015,13.885)` |
| middle / `diagonal` | `(9.885,13.885)` | `(2.5768524548,6.5768524548)` | `(2.4000757595,6.4000757595)` |
| Rod 2 / `upright` | `(9.885,-12.6002813742)` | `(9.885,-2.265)` | `(9.885,-2.015)` |

Common inner stroke remains `10.5852813742`; contact remains
`theta=23.4331751998 deg`. Workpiece bend is `B=(3.885,7.885)`, XT60 body
center is `(-2.115,26.885)`, horizontal-leg reference is `Z=1.885`, upward-leg
reference is `Y=-2.115`, and completed-pigtail extract end is `Y=21.650`.

### 6.3 Six exact inverse rails

Use only `q_s,i(u)=R[-alpha_s(u)](r_i(u)-C)`.

| rod | side | `q(OPEN)` | `q(contact)` | `q(END)` |
|---|---|---:|---:|---:|
| Rod 1 | left | `(-19.600281374,1.885)` | `(-9.250489975,-1.954964251)` | `(-9.002310873,-1.944697650)` |
| Rod 1 | right | `(-19.600281374,1.885)` | `(-7.751239319,5.414031679)` | `(-7.468913728,5.388764025)` |
| middle | left | `(6.885,1.885)` | `(1.768424834,-5.144147816)` | `(1.729636322,-5.359796525)` |
| middle | right | `(6.885,1.885)` | `(-2.544921328,-4.807593845)` | `(-2.825752452,-4.871774181)` |
| Rod 2 | left | `(6.885,-24.600281374)` | `(11.990050357,-10.350465807)` | `(11.990174529,-10.002957801)` |
| Rod 2 | right | `(6.885,-24.600281374)` | `(0.644262237,-15.826508654)` | `(0.589346423,-15.603721376)` |

| rod | left full | right full | ratio | left contact-END | right contact-END | ratio |
|---|---:|---:|---:|---:|---:|---:|
| Rod 1 | `11.535632996` | `12.907013192` | `1.118882093` | `0.248395166` | `0.283457937` | `1.141157219` |
| middle | `9.201239566` | `12.139694820` | `1.319354282` | `0.219113381` | `0.288075639` | `1.314733212` |
| Rod 2 | `15.749176568` | `11.202968733` | `1.405803849` | `0.347511926` | `0.229458948` | `1.514484088` |

Contact-to-END `(left,right)` minimum crossing angles are Rod 1
`(21.081418,18.364978) deg`, middle `(10.768937,8.166759) deg`, and Rod 2
`(23.550019,37.317751) deg`. Corresponding frictionless geometric multipliers
are `(2.780139,3.173908)`, `(5.351923,7.039543)`, and
`(2.502819,1.649526)`. These are diagnostics only.

### 6.4 Read-only actual-solid result

The selected transient parameter substitution passed:

- inverse reconstruction `<=5.329e-15`; all four plates are valid single solids;
- minimum web `4.651875693 >=2.20`; outer left/right minima
  `6.671861290/6.760000860`; outer rod-cutter gaps
  `7.059616189/7.085231967`;
- minimum fixed-feature gap `4.947934776`; all axle/keeper/rod/cap/workpiece
  intersections are zero and the virtual `C` region remains material;
- endpoint support material ratio `0.9999999999999982`; all two-sided normal
  probes, continuous `0.30` strips and closed ends pass; maximum swept-boundary
  recession `0.005098333`;
- unintended motion intersection `0.0`, pre-contact wire intersection `0.0`,
  exact contact residual `<=7.30e-13`, all guides/hardware clear, and minimum
  XT60 clearance `0.750000`;
- rail regularity passes: minimum derivative `0.379349364 mm/deg`, minimum
  non-adjacent branch gap `0.142254162`, continuation residual `<=7.29e-15`
  and no branch jump;
- service clearance `0.933815921 >=0.75`, zero service intersection;
- conditioning rank `3`, minimum normalized sigma ratio `0.098033925`, maximum
  condition number `10.200550511`.

### 6.5 R2 implementation done gate

Implement only the new named `T`, update its exact invariant, regenerate all
dependent coordinates and all six inverse rails, then rerun the existing D12
source, constraint, actual-solid, support, collision/contact, service,
conditioning, STEP parity and visual gates. Add a direct regression for the
R2 right/up displacement and terminal rail table. Do not change `A`, `C`,
plate envelopes, relative triangles, track strokes, slot widths, motion law,
hardware/counts or claims. Physical force and fit remain unproven.

## 7. P17-D12-R3 superseding fixed-axle contract

This section supersedes only R2 references that freeze
`A=(-29.000,17.000)`. R2 `T=(-12.350,-10.550)`, `C=(3,12)`, all rod and
workpiece coordinates, all six inverse rod rails, plate envelopes, angles,
hardware and service motion are unchanged.

### 7.1 Bounded marked-band selection

The searched front-view region was `A-C: Y=+10..+20, Z=-5..+5`, corresponding
to world `A: Y=13..23, Z=7..17`. `+Y` is screen-right and `+Z` is up.

| point | distance from marked `A0=(17,12)` | minimum web | limiting result | disposition |
|---|---:|---:|---|---|
| `A0=(17.000,12.000)` | `0` | `-0.014196` | required material overlaps fixed/rod guide neighborhood | infeasible |
| `A=(19.000,11.000)` | `2.236068` | `2.221355` | only `0.021355` margin | rejected fragile frontier |
| **`A=(19.250,11.000)`** | **`2.462214`** | **`2.447634`** | **`0.247634` margin; all solid gates pass** | **selected** |
| `A=(20.000,12.000)` | `3.000000` | `2.786825` | passes but drifts away from marked diagonal band | not selected |

The review overlay is `/tmp/p17-d12-r3-fixed-axle-overlay.html`. It shows the
plate, `C`, crossed-out `A0`, selected `A`, OPEN and END rod triangles, XT60
head-up/tail-right workpiece and the marked center-right search band.

### 7.2 Exact fixed-axle guide rails

For each side, derive only the existing fixed-point inverse rail:

`q_A,s(u)=R[-alpha_s(u)](A-C)`, `0<=u<=1`.

`A-C=(16.25,-1.00)`, eccentricity `16.280740155 mm`, guide slot width
`7.90 mm`, analytic centerline length `6.819660489 mm`; the 33-point polyline
length is `6.819611800 mm`.

| side | `q_A(OPEN)` | `q_A(contact)` | `q_A(END)` |
|---|---:|---:|---:|
| left | `(16.250000,-1.000000)` | `(15.307452615,5.544762793)` | `(15.251850330,5.695924992)` |
| right | `(16.250000,-1.000000)` | `(14.512094177,-7.379811827)` | `(14.438377044,-7.523015908)` |

The axle, both inner hex bores and both keepers remain one fixed world frame at
`A=(19.25,11.00)` for OPEN, mid, contact and END. Only the outer plates rotate
around unchanged `C`; do not move `C`, embed `A` into moving plate transforms,
or modify any stainless-rod rail.

### 7.3 Axial retention and actual-solid evidence

Keeper/axle dimensions remain: journal `OD7.60`, guide `7.90`, keeper bore
`7.55`, keeper OD `10.00`, seat and keeper thickness `1.20`, axial running
clearance `0.25`, and radial keeper capture `1.05`. Three OD4 x 50 rods retain
`8.70 mm` cap engagement per side; all six cap/keeper collisions are zero.

Read-only transient evaluation with only `A` substituted returned:

- all four plates valid; minimum web `2.447634348 >=2.20`, inner boundary web
  `19.013855151`, outer fixed-guide web left/right
  `3.117105554/3.774308649`, and outer boundary web
  `20.769259845/22.269259845`;
- exact fixed-feature gap `3.040481243`; axle guide radial clearance `0.15`;
- 132 actual-solid fixed-guide support probes have minimum material ratio
  `0.9999999999999987`; both sides remain continuously supported from the
  swept boundary through `+0.30 mm` at all 33 states per plate;
- 65-state maximum unintended and pre-contact intersections `0.0`; axle,
  keepers, rods, caps, plates, XT60 and wires clear; exact wire-contact timing
  and `0.750000 mm` XT60 clearance remain unchanged;
- fixed axle/keeper to XT60/service minimum `1.213238136`; completed-pigtail
  service sweep minimum `0.933815921`, BREP intersection `0.0`;
- fixed occurrences are identical in every state; conditioning rank `3`,
  minimum normalized sigma ratio `0.110413741`, maximum condition
  `9.056843781`.

### 7.4 R3 implementation done gate

Change only named `fixed_axle_center_y/z` and its exact invariant; regenerate
the two inner hex bores, two fixed-axle outer rails, axle and two keepers from
the selected `A`. Add exact A/rail endpoint, marked-band placement, fixed-frame,
web/support, keeper, collision/service and source/STEP parity regressions.
Prove the six stainless-rod rails and every R2 working-set coordinate/hash are
unchanged. Stop if minimum web, continuous support, clearance, collision,
service or fixed-frame gates fail. No physical fit or retention claim.

## 8. P17-D12-R4b final fixed-axle contract

This section supersedes Section 7 and every later quick-preview/restoration
checkpoint only where they select a fixed-axle datum. D12-R2 working-set
geometry and all six stainless-rod rails remain frozen. This is still P17 R2.

### 8.1 User-selected true center-right datum

Front view is world `YZ`: `+Y` is screen-right and `+Z` is screen-up. XT60
mating head is up; its solder tail and both wires exit right. `FRONT` uses that
physical frame. `OPPOSITE` is explicitly a mirrored camera view only; it must
not be used to reinterpret coordinates, exchange left/right parts, swap rod
identities or reverse the prescribed `-theta/+theta` outer motion.

```text
C = (3.000,12.000)                 unchanged physical rotation datum
A = (30.000,12.000)                frozen fixed purple axle
A - C = (27.000,0.000)
eccentricity |A-C| = 27.000000000
delta from temporary A=(-29,17) = (+59.000,-5.000)
height above horizontal wire reference Z=1.885 = 10.115000
```

Supersession is explicit:

| datum | disposition |
|---|---|
| R3 `A=(19.25,11)` | rejected by user: visually occupies/squeezes the stainless-rod working area |
| temporary `A=(-29,17)` | restoration baseline only; rejected as far-left, not center-right |
| R4 `A=(24,20)` | rejected by root visual inspection as upper-right rather than true center-right |
| **R4b `A=(30,12)`** | **selected after exact contact-sheet review: true center-right and outside the rod/cap swept area** |

The bounded same-height comparison was:

| candidate | relative to `C` | fixed hardware to rod/cap | minimum web | outer boundary L/R | fixed service clearance | disposition |
|---|---:|---:|---:|---:|---:|---|
| `A=(28,12)` | `(25,0)` | `9.912810052` | `10.294595306` | `12.05/13.55` | `2.965` | passes; more inward |
| **`A=(30,12)`** | **`(27,0)`** | **`11.903129708`** | **`8.294595306`** | **`10.05/11.55`** | **`2.965`** | **selected visual/clearance balance** |
| `A=(32,12)` | `(29,0)` | `13.895189794` | `6.294595306` | `8.05/9.55` | `2.965` | passes; unnecessarily outward |

### 8.2 Unchanged working set and derived fixed-axle guides

The only allowed fixed-axle outer guide equation remains

`q_A,s(u)=R[-alpha_s(u)](A-C)`, for `0<=u<=1`,

with `alpha_left=-24u deg` and `alpha_right=+24u deg`. The guide width remains
`7.90 mm`; do not draw or reuse an eyeballed arc.

| side | `q_A(OPEN)` | `q_A(contact)` | `q_A(END)` |
|---|---:|---:|---:|
| left | `(27.000000,0.000000)` | `(24.773161951,10.737338915)` | `(24.665727356,10.981889363)` |
| right | `(27.000000,0.000000)` | `(24.773161951,-10.737338915)` | `(24.665727356,-10.981889363)` |

Each guide has analytic arc length `11.309733553 mm`; its frozen `33`-point
sampled polyline is `11.309652808 mm`. The axle, both inner hex bores and both
keepers occupy one fixed world frame at `A=(30,12)` in OPEN, mid, contact and
END. Only the outer plates counter-rotate about unchanged `C`.

D12-R2 `T=(-12.350,-10.550)`, the head-up/tail-right workpiece, all three
OD4x50 rod world paths, three direct straight inner tracks and six inverse
rod rails are unchanged. Their source-derived digest is exactly
`a13a2cb0deef4c08b20bbd690b8cc74e377cd0f750810c0f86781ed1d09a1e58`.

### 8.3 Read-only deterministic evidence

Transient evaluation changing only `A` returned:

- `65` motion states: axle/outer, keeper/outer, axle/rod, keeper/cap and
  XT60/wire/service intersections are all zero;
- minimum axle-to-white-rod clearance `12.464846008 mm`, keeper-to-cap
  clearance `11.903129708 mm`, and combined hardware-to-rod/cap clearance
  `11.903129708 mm`;
- minimum analytic web `8.294595306 mm`, inner-hex boundary web
  `8.294595306 mm`, left/right outer fixed-guide web
  `12.012572604/14.178129708 mm`, outer boundary web `10.05/11.55 mm`, and
  exact frozen-feature gap `12.012572604 mm`;
- axle-guide radial clearance `0.15 mm` and keeper radial capture `1.05 mm`;
- `132` fixed-guide support probes have minimum material ratio
  `0.9999999999999996`; all support strips are continuous from the swept
  boundary through `+0.30 mm`;
- minimum fixed axle/keeper to XT60/wire/service clearance `2.965 mm`;
- completed-pigtail service sweep minimum `0.933815921 mm`, BREP intersection
  `0.0`, pass;
- conditioning rank `3`, minimum normalized sigma ratio `0.101441491`, maximum
  condition number `9.857899236`, pass;
- fixed occurrence evidence covers `65` uniform states plus exact contact and
  reports every axle/keeper frame world-invariant.

These results are CAD/math evidence only. They do not establish printed
keeper press fit, PETG creep/wear, cap retention, rod wobble, friction, hand
force, wire-holding force, self-locking or physical product acceptance.

### 8.4 R4b implementation done gate

Implementation must:

1. verify the immutable R4b implementation manifest before writes;
2. promote the named datum to final `A=(30,12)` and regenerate only its two
   inner bores, two outer fixed-axle guides, axle and two keepers;
3. prove `C`, D12-R2 `T`, workpiece, rod identities/states, straight inner
   tracks and the six-rail digest above are unchanged;
4. prove the exact guide endpoints/lengths, fixed-world invariant, minimum
   `2.20 mm` web, continuous `+0.30 mm` two-sided support, plate boundary,
   keeper engagement, collision, service and conditioning gates;
5. regenerate every dependent source-authored artifact and show FRONT and
   explicitly mirrored OPPOSITE review packets without camera-semantic drift;
6. obtain independent critique, validation and formal review before claiming
   digital acceptance; keep physical acceptance explicitly open.

No source may move a stainless rod, alter any of its six rails, change a plate
envelope or motion law, add a part/mechanism/lock, or reuse the rejected R3/R4
datum. Stop and reopen design if any frozen gate fails.
