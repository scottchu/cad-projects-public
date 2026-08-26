# P19 R1 independent outer-short-rail analysis

Owner/role: `/root/p18_validator`, independent diagnostic only

Date: 2026-08-26

Decision: **both short rails are mathematically valid but physically
marginal short capsules. Neither is equivalent to a round clearance hole at
the nominal `0.15 mm` diametral gap.** The right/upright rail is the more
hole-like of the two and its curvature is below nominal radial play, but its
finite `1.210 mm` center travel and useful Jacobian row remain real.

No design, source, test, STEP, continuity or acceptance state was changed.

## Frozen input verification

`RAIL_ANALYSIS_INPUT.sha256` SHA-256:
`cd860b9eadec18a04464c30723414014356b8811626cf5ce5afbb32404c5d2fa`.

`sha256sum -c` returned `OK` for all 3/3 declared inputs:

- `DESIGN.md`:
  `169583198638b23201b5c47835a66537551f87a837e78c21bb519161e3704fb7`
- `SERVICE_CRITIQUE.md`:
  `52d27a315bd3a19f5985b429b5915df370939ea2647dc2d0f822bf2521255475`
- `design-repair1-b2597076bc82.png`:
  `b2597076bc821aec78cc3557c24edd9bf77f5c720a48a0975e56c5c6dbd8e675`

## Deterministic calculation

The calculation was run from repository root through `uv run python`. Curve
quantities used a fixed uniform grid of `200,001` points including both
endpoints. Jacobian quantities used `2,001` states. No randomized operation,
CAD tessellation or image measurement was used.

For rod `i`, let `d_i=END_i-OPEN_i`, `p_i(u)=OPEN_i+u d_i`, and let `J`
rotate a YZ vector by +90 degrees. The plate-local inverse rail and derivative
are

```text
q_s,i(u)  = R(-alpha_s(u)) p_i(u)
q'_s,i(u) = R(-alpha_s(u)) [d_i - alpha'_s J p_i(u)]
```

with `alpha_left=-10u deg` and `alpha_right=+10u deg`. The reported center
travel is `integral_0^1 |q'(u)|du`; endpoint chord is `|q(1)-q(0)|`.
Sagitta is the maximum perpendicular deviation of `q(u)` from its endpoint
chord. Crossing angle is the acute line angle between world rod path `d_i`
and the current world-transformed rail tangent `R(alpha_s)q'_s`.

For a swept OD4.15 cutter, two useful envelope measures are reported:

```text
straight end-to-end envelope = endpoint chord + 4.15
center-travel envelope        = center arc + 4.15
aspect proxy                  = (center arc + 4.15) / 4.15
```

The command embedded those equations and the frozen points directly and
printed JSON for both target/comparison pairs. A second deterministic loop
formed the same normalized four-contact Jacobian law used by P18/P19: row
order `fixed axle, upright, bottom, diagonal`; pose coordinates
`deltaY, deltaZ, alpha`; rotation scaled by characteristic radius
`22.719154913861 mm`; each row normalized before SVD.

## Rail-length results

Angles below are line angles measured from +Y toward +Z; tangent direction is
unoriented, so angles differing by 180 degrees are identical.

| quantity | left / bottom short | left / diagonal comparison | right / upright short | right / diagonal comparison |
|---|---:|---:|---:|---:|
| world rod stroke (mm) | 3.162278 | 9.131539 | 2.501999 | 9.131539 |
| outer-rail center arc (mm) | **1.356484** | 8.212906 | **1.209836** | 10.984581 |
| endpoint chord (mm) | **1.339631** | 8.169534 | **1.208652** | 10.939344 |
| arc/chord | 1.012580 | 1.005309 | 1.000980 | 1.004135 |
| maximum sagitta (mm) | **0.092171** | 0.364835 | **0.023139** | 0.431092 |
| chord + OD4.15 (mm) | 5.489631 | 12.319534 | 5.358652 | 15.089344 |
| arc + OD4.15 (mm) | **5.506484** | 12.362906 | **5.359836** | 15.134581 |
| cutter aspect proxy | **1.3269** | 2.9790 | **1.2915** | 3.6469 |
| nominal gap / center arc | **11.06%** | 1.83% | **12.40%** | 1.37% |
| nominal radial play / arc | **5.53%** | 0.91% | **6.20%** | 0.68% |
| average `|q'|/|d|` | 0.42896 | 0.89940 | 0.48355 | 1.20293 |
| min/max instantaneous `|q'|/|d|` | 0.3988 / 0.4690 | 0.8712 / 0.9325 | 0.4513 / 0.5244 | 1.1820 / 1.2278 |

The short appearance is therefore genuine and deterministic: opposite plate
rotation cancels roughly half of the corresponding world rod displacement.
It is not a sampling or drawing error. The longer diagonal comparisons have
roughly 6-9 times more center travel and 2.2-2.8 times the swept-cutter aspect.

## Tangent and crossing results

| rail | rod/world line angle | plate-local tangent OPEN / END | world rail tangent OPEN / END | crossing OPEN / END | minimum |
|---|---:|---:|---:|---:|---:|
| left/bottom | 161.565° | 174.205° / 25.497° | 174.205° / 15.497° | 12.640° / 33.932° | **12.640° at OPEN** |
| left/diagonal comparison | 47.663° | 21.998° / 42.400° | 21.998° / 32.400° | 25.665° / 15.263° | 15.263° at END |
| right/upright | 87.709° | 53.923° / 62.671° | 53.923° / 72.671° | 33.787° / 15.038° | **15.038° at END** |
| right/diagonal comparison | 47.663° | 66.868° / 48.852° | 66.868° / 58.852° | 19.205° / 11.189° | 11.189° at END |

Neither short rail owns the shallowest crossing in the complete candidate:
both minima are larger than the already recorded `2.752/3.101 deg` global
side minima. Their main risk is low travel relative to clearance, not tangent
singularity.

The right/upright sagitta (`0.023 mm`) is only 31% of nominal radial play
(`0.075 mm`). Its curved inverse path will therefore behave physically much
like a **short straight capsule**, even though it is not a round hole. The
left/bottom sagitta (`0.092 mm`) is only 23% larger than nominal radial play,
so its curvature is also weakly resolved.

## Clearance sensitivity

The bands below are deterministic what-if gaps, not measurements of a printed
part. `0.05 mm` represents a tight realized diametral gap, `0.15 mm` the CAD
nominal, and `0.30 mm` a loose realized gap. Center radial play is half the
diametral gap. The last column uses the conservative local amplification
`(gap/2)/sin(min crossing)`.

| rail | diametral gap | gap / arc | arc / gap | radial play / sagitta | crossing-amplified path uncertainty |
|---|---:|---:|---:|---:|---:|
| left/bottom | 0.05 | 3.69% | 27.13x | 0.27x | 0.114 mm |
| left/bottom | 0.15 | 11.06% | 9.04x | 0.81x | 0.343 mm |
| left/bottom | 0.30 | 22.12% | 4.52x | 1.63x | 0.685 mm |
| right/upright | 0.05 | 4.13% | 24.20x | 1.08x | 0.096 mm |
| right/upright | 0.15 | 12.40% | 8.07x | 3.24x | 0.289 mm |
| right/upright | 0.30 | 24.80% | 4.03x | 6.48x | 0.578 mm |

At nominal gap, each rail still has more than eight diametral-clearance units
of center travel, so neither is kinematically swallowed by a round clearance
hole. At a loose `0.30 mm` realized gap, only about four units remain and the
curvature is entirely below radial play; both then become meaningfully
marginal guides. Actual PETG bore shrinkage, ovality, surface roughness and
rod straightness may instead make them tight. CAD cannot select between those
two physical outcomes.

## Four-contact/Jacobian contribution

The target rows are not decorative. Raw rows are derivatives of signed local
normal residual with respect to `(deltaY mm, deltaZ mm, alpha rad)`:

| target row | OPEN | END |
|---|---|---|
| left/bottom | `(-0.100970,-0.994889,-3.964751)` | `(0.267182,-0.963646,-10.113809)` |
| right/upright | `(-0.808224,0.588876,7.971932)` | `(-0.954611,0.297856,3.719514)` |

Full four-contact closure remains rank 3 throughout `2,001` states. Removing
either short-rail row also leaves rank 3, so neither is the sole algebraic
source of closure; the fourth row supplies redundancy and conditioning.

| side / target | full condition OPEN / END | condition without target OPEN / END | full worst | worst without target |
|---|---:|---:|---:|---:|
| left / bottom | 2.897 / 5.841 | 3.398 / 5.413 | 5.841 at END | 5.413 at END |
| right / upright | 5.260 / 10.177 | 6.370 / 24.291 | 10.177 at END | 24.291 at END |

The left/bottom row is modestly redundant near END: removing it barely
changes minimum normalized singular value (`0.256590` full versus `0.254873`
without it). The right/upright row is materially useful: at END it raises the
minimum normalized singular value from `0.057047` to `0.154955` and reduces
condition from `24.291` to `10.177`. Treating the right/upright feature as an
unconstrained round hole would therefore discard useful support even though
the remaining three rows are still formally rank 3.

## Classification and recommendation

### Left outer / bottom

**Mathematically valid; physically marginal short rail.** It has finite,
monotonic center travel, a nonzero `12.64 deg` minimum crossing, and a real
constraint row. Its `1.327` cutter aspect and nominal gap equal to 11.1% of
travel explain why it looks loose/short. It is not effectively round at the
CAD nominal, but its intended curvature becomes poorly distinguished if the
realized diametral gap approaches `0.30 mm`.

### Right outer / upright

**Mathematically valid; more physically marginal, but still not a round
hole.** It is the shortest at `1.210 mm`, has aspect `1.292`, and nominal gap
is 12.4% of travel. Its sagitta is already below nominal radial play, so the
curve behaves like a short straight capsule. Nevertheless its center travel
is 8.07 times the nominal diametral gap and its Jacobian row strongly improves
END conditioning; replacing its meaning with a round clearance hole is not
supported by the math.

### Next evidence

Do not change the accepted 2D kinematics solely because the rails look short.
Carry both into exact 3D as the deterministic inverse sweeps, retain OD4.15 as
the named CAD cutter, and make the smallest falsifiable physical gate a paired
short-rail coupon printed in the intended PETG orientation with the real OD4
rod. Measure realized diametral play and hand force for the left/bottom and
right/upright lengths. If the coupon is loose or binds, adjust the shared
rod/slot fit parameter from measured evidence; do not hand-extend one rail or
change its trajectory independently.
