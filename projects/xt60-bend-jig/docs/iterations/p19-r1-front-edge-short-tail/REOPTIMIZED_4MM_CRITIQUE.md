# P19 R1 cycle-3 four-millimetre independent 2D critique

Decision: **BLOCK USER 2D REVIEW OF THIS CANDIDATE.**

The six physical inverse rails meet the new `4.00 mm` length and capsule
aspect gates. The candidate is nevertheless blocked because its frozen wire
construction intersects the diagonal rod already in OPEN, so it does not
provide a credible unlocked insertion/removal state. The phone artifact also
overlaps required object and service labels. Neither failure requires 3D CAD
to falsify.

This is a 2D input critique only. It does not approve or reject future 3D CAD,
STEP, slicing, printing, force, fit, heat, self-locking, or physical
acceptance.

Owner/role: `/root/p17_optimizer_math_audit`, independent critic. No design,
CAD source, tests, STEP, artifact, or continuity file was changed by this
review.

## Frozen inputs and candidate

- `REOPTIMIZE_4MM_INPUT.sha256`: verified `8/8`; manifest SHA-256
  `ac9f534d2b5ae11a9ba8d7488c2262d13a5590e49a5c717d6b7ecaff72895403`.
- `REOPTIMIZED_4MM_DESIGN.md` SHA-256:
  `d6054dc2813015259634638af948be059d74e338f817292a0715a7ec13e3c49c`.
- `docs/review/p19-r1-front-edge-short-tail/reoptimized-4mm-gate.png`
  SHA-256:
  `1db9685ac7f3a738f52987e1382329572dd8386098c4f48b45ed5106a16f96ee`.
- Baseline: Git commit `bcc16305ff112ba814bdf19ad544a5819127e902`
  plus the exact cycle-2 evidence named by the verified manifest.

## Independent rail reproduction

I independently evaluated the frozen candidate from

```text
p_i(u) = OPEN_i + u (END_i - OPEN_i)
q_s,i(u) = R(-alpha_s(u)) p_i(u),  0 <= u <= 1
```

with `alpha_left=-5u deg`, `alpha_right=+5u deg`, `200,001`
centreline samples for arc/chord/sagitta/crossing and `2,001 x 2,001`
independent-parameter searches for 2D curve webs. An additional 101-state
inverse reconstruction check had maximum residual `7.33e-15 mm`.

| outer / rod | reproduced centre arc | capsule aspect | minimum crossing |
|---|---:|---:|---:|
| left / bottom | `5.052562102 mm` | `2.217484844` | `8.244929 deg` |
| left / diagonal | `5.083225349 mm` | `2.224873578` | `16.417614 deg` |
| left / upright | `7.811007031 mm` | `2.882170369` | **`2.192572 deg`** |
| right / bottom | `6.353263015 mm` | `2.530906751` | `6.527924 deg` |
| right / diagonal | `6.239375705 mm` | `2.503464025` | `13.245957 deg` |
| right / upright | **`4.212461442 mm`** | **`2.015050950`** | `4.088284 deg` |

Therefore all six exact inverse-derived rails pass centre travel
`>=4.00 mm`; the minimum margin is `0.212461442 mm`. Every full-capsule
aspect passes `>=1.963855`; the minimum margin is approximately `0.051196`.
No endpoint padding or manual rail extension is present.

OPEN vectors reproduce exactly as `(15.4,0)` then `(0,-15)`. END vectors
reproduce exactly as `(6.25,-5.75)` then `(6.25,-5.75)`. The named world
paths are separated and non-crossing, and identities remain `bottom`,
`diagonal`, `upright`.

## Envelope, web, axle, and closure

Independent OD4.15 cutter-envelope calculations reproduce:

- limiting rod-centre radius `22.755493842 mm`;
- fixed-inner rim web **`2.369506158 mm`**;
- left/right outer rim webs `2.519506158 / 2.669506158 mm`;
- fixed-inner rail-to-rail web `4.326719611 mm`;
- left/right outer rail-to-rail webs `3.632160752 / 4.185937908 mm`;
- minimum axle-guide-to-rod-rail web `19.840109320 mm`.

Thus `OD54.4 < OD54.7 < OD55.0` and the `>=2.20 mm` 2D web gate pass.
The limiting margin is only `0.169506 mm`; endpoint caps, exact AF8.15 key
corners, fillets and chamfers remain future exact-solid checks.

`C=(0,0)` and real stepped axle `A=(-13,-9)` are unchanged. The artifact's
X section depicts one continuous `34.90 mm` structural member keyed through
both fixed inner plates and round-journalled through both opposite rotating
outer plates. It is not a floating point or a fourth stainless locking rod.

The normalized four-contact probe was independently rebuilt with row order
`fixed axle, upright, bottom, diagonal`, characteristic radius
`22.755493842 mm`, unit-row normalization, and `2,001` states per side. Rank
remained `3`; worst conditions were `10.629805` left and **`43.357683`**
right, both at END. The small difference from the design's last digits is
numeric eigensolver scale. Rank is not evidence of acceptable hand force,
stiffness, friction, or back-drive resistance.

The shallowest crossing is independently `2.192572 deg`. With the nominal
`0.15 mm` diametral rod/rail gap, the corresponding simple clearance-motion
proxy is `0.15/sin(2.192572 deg) = 3.92 mm`. That is nearly the entire new
minimum-travel target before this constraint necessarily takes load. This is
a severe physical-force/backlash risk, although it would be a documented
risk rather than the blocking 2D service contradiction by itself.

## Service and orientation

The numeric orientation is correct: XT60 mating head is `+Z/up`; short tail,
cup, FRONT and tool are `+Y/right`. The full `8 x 8 mm` tool keepout begins at
`Y=28.25 mm`, exactly `0.75 mm` outside the OD55 tangent at `Y=27.50 mm`.
The cup begins at `Y=29.25 mm`, `1.75 mm` outside the rim. The horizontal
short-tail centreline is `6.859480 mm`, closer to the joint than cycle 2.

However, applying the frozen combined rod/wire radius `4.15 mm` to the exact
wire line through `F_bottom=(12.890520,14.870131)` gives:

| rod | OPEN signed centre distance to wire line | OPEN surface clearance | first contact state |
|---|---:|---:|---:|
| bottom | `-8.926408 mm` | `+4.776408 mm` | `u=0.950263` |
| diagonal | `+1.500262 mm` | **`-2.649738 mm`** | already intersecting at `u=0` |
| upright | `-9.538703 mm` | `+5.388703 mm` | `u=0.955664` |

All three END signed distances remain approximately `-3.900000 mm`, giving
the selected `-0.250000 mm` END preload proxy. But the diagonal signed
distance evolves from `+1.500262` to `-3.900000 mm`, so its absolute distance
stays below `4.15 mm` for the entire motion and crosses the wire centreline.
It never has an unlocked clearance state. This is not merely early contact or
an unknown force coefficient; it geometrically contradicts OPEN service and
can prevent insertion/removal or demand impossible wire penetration.

## Visual delivery

The exact PNG was inspected at original resolution. The rail panels, numeric
table, risk line, orientation axes, and X-axis axle section are present.
However, the main FRONT gate is not ready for reliable phone review:

- the twist annotation overlaps `XT60 head +Z` at the top;
- `upright OPEN`, `upright END`, and `8 x 8 TOOL - fully outside` overlap each
  other and the rod markers;
- the resulting callout collision obscures the exact service relation that
  the user must approve.

This is a delivery blocker, not a request to change the numeric design.

## Findings and exact correction gate

1. **PASS — requested 4 mm rail and aspect gates.** All six inverse-derived
   centre arcs and capsule aspects independently pass.
2. **PASS — topology, identities, compact envelope, axle, direction, and
   projected tool keepout.** These remain within the frozen delta mask.
3. **BLOCK — OPEN service contradiction.** The diagonal rod already overlaps
   the frozen wire envelope by `2.649738 mm` in OPEN and never leaves it.
4. **BLOCK — visual review artifact.** Required labels collide in the exact
   FRONT area and prevent unambiguous phone review.
5. **SEVERE UNRESOLVED RISK — force/conditioning.** Crossing `2.192572 deg`
   and right-END condition about `43.36` are not proof of failure, but they
   make a force/clearance coupon or later physical test mandatory if a repaired
   2D candidate survives.

Before resubmission, the optimizer must add a hard OPEN service gate requiring
nonnegative rod-to-wire surface clearance for every named rod (preferably a
stated positive assembly margin), then find a feasible candidate without
manual rail extension or invariant regression. It must report all three OPEN
clearances/contact states, not only END preload and tail length. Re-render the
same exact candidate with separated leader labels outside the dense FRONT
geometry. No CAD, STEP, slicing, or print work is authorized by this repair.

**Final decision: BLOCK USER 2D REVIEW OF THIS CANDIDATE.**
