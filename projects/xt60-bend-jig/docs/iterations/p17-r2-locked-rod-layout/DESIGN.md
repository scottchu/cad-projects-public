# P17-D13 exact locked rod-layout design

All dimensions are millimetres in world `(Y,Z)`. `+Y` is screen-right and
`+Z` is XT60 head/up. FRONT is authoritative; any OPPOSITE view is camera-
mirrored only.

## 1. Frozen parameters and equations

```text
I10 C = (3.000,12.000)              unchanged
D13 A = (-29.000,12.000)            only A.z changes
rod_track_delta = (+16.1869657526,+10.2949747468)
theta(u) = 24u deg                  0 <= u <= 1
alpha_left/right = -theta/+theta
contact u = 23.4331751998 / 24
rod slot width = 4.15
fixed axle guide width = 7.90
plates inner/left/right = 80/82/85 diameter
```

For each I10 rod state `r_i,I10(u)`, the only permitted new world locus is

`r_i,D13(u)=r_i,I10(u)+(DY,DZ)`.

Each inner track is the direct segment from its translated OPEN to END. Each
outer side-local rail must be derived, never manually redrawn:

`q_s,i(u)=R[-alpha_s(u)](r_i,D13(u)-C)`.

The fixed axle outer guide remains
`q_A,s(u)=R[-alpha_s(u)](A-C)`. No rod rail, axle guide or fixed track may be
translated as an old solid.

## 2. Exact world rod states

| identity | OPEN | first contact | END |
|---|---:|---:|---:|
| bottom | `(-4.7983156216,19.7949747468)` | `(5.5369657526,19.7949747468)` | `(5.7869657526,19.7949747468)` |
| diagonal | `(21.6869657526,19.7949747468)` | `(14.3788182074,12.4868272016)` | `(14.2020415121,12.3100505063)` |
| upright | `(21.6869657526,-6.6903066274)` | `(21.6869657526,3.6449747468)` | `(21.6869657526,3.8949747468)` |

All strokes remain `10.5852813742 mm` within floating-point rounding. END
centroid Z is

`(19.7949747468+12.3100505063+3.8949747468)/3 = 11.99999999997`.

Relative triangle edges, areas, rod identities and direct track directions
are preserved exactly because one common translation is applied.

## 3. Six analytically derived outer rails

Lengths below are the existing `33`-point centerline-polyline convention;
the continuous high-resolution values differ by at most `0.000320 mm`.
Contact-to-END values are endpoint chords, matching the I10 diagnostic.

| rod | side | local OPEN | local contact | local END | full length | contact-END |
|---|---|---:|---:|---:|---:|---:|
| bottom | left | `(-7.798315622,7.794974747)` | `(-0.772171194,8.160978996)` | `(-0.624481957,8.254624867)` | `7.501947709` | `0.174876127` |
| bottom | right | `(-7.798315622,7.794974747)` | `(5.427627746,6.143181878)` | `(5.716521765,5.987502678)` | `13.948259479` | `0.328170333` |
| diagonal | left | `(18.686965753,7.794974747)` | `(10.246743615,4.971795432)` | `(10.107465238,4.839525992)` | `9.319739289` | `0.192077253` |
| diagonal | right | `(18.686965753,7.794974747)` | `(10.633945738,-4.078443646)` | `(10.359683042,-4.273035529)` | `14.960368308` | `0.336282660` |
| upright | left | `(18.686965753,-18.690306627)` | `(20.468369138,-0.234522560)` | `(20.368003444,0.196364715)` | `19.287676670` | `0.442421876` |
| upright | right | `(18.686965753,-18.690306627)` | `(13.823129302,-15.097358455)` | `(13.774781917,-15.004982724)` | `6.279823509` | `0.104262867` |

| rod | full L/R ratio | contact-END L/R ratio | contact crossing L/R | minimum contact-to-END L/R |
|---|---:|---:|---:|---:|
| bottom | `1.859285084` | `1.876587387` | `8.260068/4.387453 deg` | `8.260068/4.387453 deg` |
| diagonal | `1.605234636` | `1.750767749` | `25.527730/14.276738 deg` | `24.860171/13.868000 deg` |
| upright | `3.071372411` | `4.243331211` | `10.761876/51.762854 deg` | `10.447053/50.913811 deg` |

These rails are numerically derivable but do not preserve the user-approved
I10 force/path balance. Crossing angles are frictionless geometry diagnostics,
not hand-force predictions.

## 4. Analytic plate and web feasibility

The check uses the frozen `4.15 mm` rod-slot and `7.90 mm` axle-guide cutter
radii, `33`-point derived polylines, the `80/82/85 mm` circular envelopes and
the `AF8.15` fixed-inner hex bore.

| gate | result | threshold | status |
|---|---:|---:|---|
| inner rod-slot boundary web | `11.495277132` | `>=2.20` | pass |
| inner hex boundary web | `3.294595306` | `>=2.20` | pass |
| inner axle/rod-track web | `18.645628384` | `>=2.20` | pass |
| inner rod-track pair web | `7.112219627` | `>=2.20` | pass |
| left rod-slot boundary web | `12.495277132` | `>=2.20` | pass |
| left axle-guide boundary web | `5.050000000` | `>=2.20` | pass |
| left axle/rod-rail web | `19.401033077` | `>=2.20` | pass |
| left rod-rail pair web | `3.632336547` | `>=2.20` | pass |
| right rod-slot boundary web | `13.995277132` | `>=2.20` | pass |
| right axle-guide boundary web | `6.550000000` | `>=2.20` | pass |
| right axle/rod-rail web | `16.036727644` | `>=2.20` | pass |
| right rod-rail pair web | `6.689064296` | `>=2.20` | pass |

Conclusion: all six outer rod rails, three inner tracks and two axle guides are
analytically constructible without crossing a circular plate boundary or the
`2.20 mm` feature-web gate. This is not an actual-BREP support/collision pass.

## 5. Product-interface blocker

The I10 workpiece is frozen:

```text
XT60 body center = (-6.5,22.5), Y size 8.1, Z size 20.5
body YZ rectangle = [-10.55,-2.45] x [12.25,32.75]
bend B = (-0.5,3.5)
vertical wire centerline Y = -6.5
horizontal wire centerline Z = -2.5
extract endpoint Y = 17.265
```

At OPEN, the translated bottom rod center
`(-4.7983156216,19.7949747468)` is inside that XT60 body rectangle. Because the
rod is OD4 and spans the central X region, the locked candidate has an actual
rod/body collision; the 2D centerline-to-body distance is `0` and the signed
rod clearance is `-2.000 mm`. This violates the no-XT60-plastic-load product
requirement before any detailed service sweep.

It also collides with the frozen vertical-wire envelope at OPEN: the centerline
separation is
`|-4.7983156216-(-6.5)|=1.7016843784 mm`, against required non-intersection
distance `2.00+2.15=4.15 mm`. Nominal radial overlap is therefore
`2.4483156216 mm`. This is a hard object-collision result, not a force
diagnostic.

The former END wire contact is also gone:

- bottom to vertical-wire centerline: `12.286965753 mm`, leaving
  `8.136965753 mm` surface gap after the `2.00+2.15 mm` radii;
- upright to horizontal-wire centerline: `6.394974747 mm`, leaving
  `2.244974747 mm` surface gap;
- the diagonal rod is likewise translated away from the frozen bend, so the
  original three-point contact/preload state cannot exist.

Therefore the locked layout does not merely require a service-risk test: it
fails the primary workpiece interface analytically. Actual-solid generation is
not authorized because it would only materialize a known invalid product.

Separately, the length ratios and crossing-angle results in Section 3 diagnose
poor path/leverage balance. They are a user-intent gate and a frictionless
force proxy, not collision evidence and not a physical hand-force proof. The
hard stop already follows independently from rod/body collision, OPEN
rod/wire collision and missing END contact.

## 6. Cheap 2D before/after overlay

Gray is exact I10; red is the user-locked D13 common rod delta. The gold XT60
body and brown wire reference stay fixed. The red bottom OPEN point is visibly
inside the XT60 body.

<svg viewBox="0 0 760 500" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="I10 and D13 rod layout overlay">
  <rect width="760" height="500" fill="#f8fafc"/>
  <circle cx="395" cy="260" r="200" fill="none" stroke="#94a3b8" stroke-width="2"/>
  <text x="400" y="252" font-size="13">C=(3,12)</text>
  <rect x="259" y="43" width="41" height="103" rx="5" fill="#f5c04a" opacity="0.75" stroke="#9a6700"/>
  <text x="210" y="32" font-size="13">fixed XT60 body</text>
  <path d="M280 240 L280 355 Q280 385 310 385 L520 385" fill="none" stroke="#9a6700" stroke-width="8" stroke-linecap="round"/>
  <g fill="none" stroke="#64748b" stroke-width="3" stroke-dasharray="7 5">
    <path d="M207 273 L313 273"/><path d="M472 273 L397 348"/><path d="M472 438 L472 332"/>
  </g>
  <g fill="#64748b"><circle cx="207" cy="273" r="7"/><circle cx="472" cy="273" r="7"/><circle cx="472" cy="438" r="7"/><circle cx="313" cy="273" r="7"/><circle cx="397" cy="348" r="7"/><circle cx="472" cy="332" r="7"/></g>
  <text x="115" y="287" fill="#475569" font-size="13">I10</text>
  <g fill="none" stroke="#dc2626" stroke-width="3">
    <path d="M369 170 L475 170"/><path d="M634 170 L559 244"/><path d="M634 335 L634 229"/>
  </g>
  <g fill="#dc2626"><circle cx="369" cy="170" r="8"/><circle cx="634" cy="170" r="8"/><circle cx="634" cy="335" r="8"/><circle cx="475" cy="170" r="8"/><circle cx="559" cy="244" r="8"/><circle cx="634" cy="229" r="8"/></g>
  <text x="650" y="185" fill="#dc2626" font-size="13">D13</text>
  <line x1="350" y1="145" x2="305" y2="105" stroke="#dc2626" stroke-width="2"/>
  <text x="360" y="140" fill="#dc2626" font-size="13">bottom OPEN intersects body</text>
  <text x="20" y="480" font-size="12" fill="#475569">front YZ overlay; +Y right, +Z up; diagram preserves coordinates but is not an artifact validation</text>
</svg>

## 7. Acceptance and stop gates

Implementation is not dependency-ready. It may begin only after an explicit
user-authorized correction resolves all three blockers without silently
weakening the locked coordinate contract:

1. zero actual rod/cap intersection with XT60 body through OPEN/contact/END;
2. restored three-point wire contact/preload or an explicitly superseding
   product interface;
3. an accepted rail/path balance target and contact crossing-angle floor;
4. actual-solid plate validity, continuous `+0.30 mm` two-sided support,
   collision, service, conditioning and source/STEP parity;
5. unchanged P17 R2 architecture and explicit physical-unknown boundary.

Physical cap/keeper fit, PETG wear, rod wobble, hand force, wire marking,
thermal behavior, springback, endpoint retention and self-lock remain unknown.
