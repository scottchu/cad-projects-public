# P20 R2 true fixed-rod arc-rail design gate

Status: **PASS — analytic design only; ready for independent critique.**

Owner/role: `/root/p20_r2_arc_designer`, independent mechanism/rail designer.
This record does not authorize source, BREP, STEP, white-rod outer rails, or a
physical claim.

## Frozen provenance

- Branch: `codex/xt60-p20-r1-fixed-rod-reset`.
- Contract-opening HEAD: `a48c5697f9126dbb6934d764e48f2a01f6a01475`.
- Product baseline: P19 R1
  `b69b6ad12af611644987f026eef4940db9c7bb34`.
- Input manifest SHA-256:
  `07847a8fec788ece8c9f421225ca1301810cf619713904a7da867dfcc6674a55`.
- All `20/20` declared local and `git:<commit>:<path>` entries were
  independently recomputed and matched.

## CAD brief

- Task type: bounded P19 source modification design; no implementation in this
  task.
- Units/frame: millimetres in physical FRONT YZ; `+Z` mating-head/up and `+Y`
  solder-tail/tool/outward-right. X is the plate-stack and axle axis.
- Fixed geometry: virtual outer-plate center `C=(0,0)` and world-stationary
  purple axle `A=(-15,-11)`.
- Motion: shared `u in [0,1]`; physical left outer `alpha_L=+45u deg`, physical
  right outer `alpha_R=-45u deg`, both about `C`; inner plates and axle do not
  move.
- Required feature: exactly one true curved fixed-axle rail in each outer
  plate; no white-rod outer cut of any kind.
- Preserved feature: all three P19 white-rod inner rails in each inner plate.
- Validation target: inverse reconstruction, exact arc geometry, cutter fit,
  rim/feature web, axial keeper/support, and visible phone gate.

## One pure inverse-frame authority

For either side, implementation must delegate to one pure function equivalent
to:

```python
def fixed_axle_local(side, u, C, A, theta_deg):
    alpha = (+1 if side == "left" else -1) * theta_deg * u
    return C + rotate(A - C, -alpha)
```

Thus

```text
q_s(u) = C + R(-alpha_s(u)) (A-C)
T_s(q,u) = C + R(alpha_s(u)) (q-C)
T_s(q_s(u),u) = A
```

The last equality follows from `R(alpha)R(-alpha)=I`; it is exact, not a
sampled approximation. A constant circle at `A` would instead give
`T_s(A,u)=R(alpha_s)A`, which moves in world because `A != C`. Rotating the
plate about `A` is the rejected P20 R1 interpretation.

## Exact loci

`|A-C| = sqrt(346) = 18.601075237738 mm`. The two rails are opposite 45-degree
arcs of that circle in their respective plate-local frames.

| `u` | left local `q_L=(Y,Z)` mm | right local `q_R=(Y,Z)` mm | maximum reconstructed-world residual |
|---:|---:|---:|---:|
| `0.00` | `(-15.000000,-11.000000)` | `(-15.000000,-11.000000)` | `0` |
| `0.25` | `(-16.857773,-7.862283)` | `(-12.565786,-13.714993)` | `3.56e-15 mm` |
| `0.50` | `(-18.067711,-4.422423)` | `(-9.648675,-15.902926)` | `0` |
| `0.75` | `(-18.583317,-0.812612)` | `(-6.360772,-17.479719)` | `1.78e-15 mm` |
| `1.00` | `(-18.384776,+2.828427)` | `(-2.828427,-18.384776)` | `1.78e-15 mm` |

Each side has:

| quantity | exact relation | value |
|---|---:|---:|
| radius | `sqrt(346)` | `18.601075238 mm` |
| included angle | `pi/4` | `45 deg` |
| centerline arc | `r*pi/4` | `14.609250329 mm` |
| endpoint chord | `2r sin(pi/8)` | `14.236646635 mm` |
| whole-arc sagitta | `r(1-cos(pi/8))` | `1.415922543 mm` |

The local curves meet only at their common OPEN point `A`; they are not one
translated curve. They are mirror-related about the radial line through `A`:
`q_L(u)=R(-45u)A` and `q_R(u)=R(+45u)A`; each plate-local rail turns opposite
to its physical outer-plate rotation.

## Cutter width, sampling, and fit

P19's axle is `OD7.60 mm` and its accepted outer bearing/guide intent is
`0.30 mm` diametral running clearance. Therefore the fixed-axle rail cutter is
exactly `7.90 mm` wide, retaining `0.15 mm` radial clearance per side. It must
not reuse the white-rod `4.15 mm` cutter.

Preserve P19's odd `33` fixed-guide center samples (`32` equal chord
intervals). At 45 degrees this gives:

- angular interval `1.40625 deg`;
- maximum chord-to-circle sagitta `0.001400627 mm`;
- conservative minimum journal radial clearance
  `0.150000-0.001401 = 0.148599 mm`.

That is the smallest frozen sampling choice and is analytically sufficient.
Implementation must still fail closed unless each cut plate is one valid solid
and its exact axle/rail intersection is zero across at least the same 33
states. Pure-math reconstruction tolerance is `1e-10 mm`; sampled center
points must lie on radius `sqrt(346)` within `1e-12 mm`; written geometry must
not be accepted from this analytic result alone.

## Web and interaction gates

The rail is an annular capsule centered on radius `sqrt(346)`, with cutter
radius `3.95 mm`. Its exact outer-rim radial webs are:

| gate | result | threshold | decision |
|---|---:|---:|---:|
| left outer OD54.70 | `27.35-r-3.95 = 4.798925 mm` | `>=2.20` | PASS |
| right outer OD55.00 | `27.50-r-3.95 = 4.948925 mm` | `>=2.20` | PASS |
| inner OD54.40 to moved AF8.15 hex corner | `27.20-r-8.15/sqrt(3) = 3.893520 mm` | `>=2.20` | PASS |

The fixed rail cannot split either outer disk: its inner radial edge remains
`r-3.95 = 14.651075 mm` from `C`, and the outer ligament is continuous for
the full arc including round endpoint caps.

A deterministic `1001 x 1001` closed-domain sweep, followed by continuous
boundary minimization, checked the complete synchronized motion. The grid
Lipschitz bound is under `0.040 mm`; the values below subtract that bound and
the complete cutter/body radii, so they are conservative surface clearances:

| compared with moving fixed-axle rail | minimum conservative surface clearance |
|---|---:|
| any current `OD4` white rod | `>18.469 mm` |
| any retained `4.15 mm` inner-rail path, projected in YZ over all states | `>18.394 mm` |

Therefore the corrected purple rail does not substitute for, touch, or merge
with any white-rod path. The six required rod/solid-outer-plate collisions
remain because the white-rod outer cut count is exactly zero.

The left and right purple rail apertures overlap in a YZ projection near the
common axle, as they must for one continuous axle. They are in different
outer plates: the actual plate X intervals are `[-16.0,-12.8]` and
`[12.8,16.0] mm`, leaving `25.6 mm` between their nearest faces. Thus there is
no same-solid neighboring-rail web interaction and no 3D cutter overlap.

## Axial support and keeper implications

- The stepped axle remains one `34.90 mm` X member.
- Each outer plate is `3.20 mm` thick; journal overlap remains the full
  `3.20 mm` thickness.
- The permanent `OD10.00 / ID7.55` keepers retain `1.05 mm` radial capture
  beyond the `7.90 mm` rail and preserve the `0.25 mm` axial running gap.
- The curved slot provides passage/contact for the fixed journal, not a new
  centered bearing and not complete mechanism closure. With all white-rod
  outer rails absent, this intentionally colliding intermediate is neither a
  free-motion product nor a force/torque proof.

## Requirement coverage and decision

| requirements | analytic result |
|---|---|
| `REQ-01..03` | exact P19 input; six white-rod outer rails absent; six inner rails retained |
| `REQ-04..07` | `A=(-15,-11)`, `C=(0,0)`, physical left/right `+45/-45`, two true inverse-frame arcs PASS |
| `REQ-08` | repaired phone gate exposes both full arcs, both MID states, OPEN-to-END arrows, six retained inner rails, and explicitly rejects the round hole |
| `REQ-09` | no unlisted object or service change authorized |
| `REQ-10` | six known rod/solid-outer collisions retained, no purple-rail interaction found |
| `REQ-11` | design stops before source/BREP/STEP |

**Design decision: PASS the exact two-arc analytic candidate to independent
critique.** The next worker may implement only after that critique accepts this
fingerprint. The first future white-rod outer rail and its sequencing remain
explicitly out of scope.

### Focused repair after independent critique

The independent critique at SHA-256
`43c98d108c1713e2efd54172fe275b3dafb7d74fa17421b1d170244368794b21`
accepted every equation, numeric locus, cutter, sampling, web, interaction,
stack and known-collision result, but blocked the old candidate fingerprint
`c38fe2158b150efa946f92a6d110b56be2806a1c4dd7d933f8b50666c2a2860f`
because its frozen phone gate omitted MID markers and directional arrows and
said only `x3` retained inner rails.

The user subsequently approved a corrected physical-sign gate: left outer
`+45 deg`, right outer `-45 deg`, both about `C`. The inverse rail directions
and the left/right locus columns above were swapped accordingly; radius,
width, sampling, web and collision boundaries are unchanged. The approved
PNG SHA-256 is
`e2d05a852889bef2e9c97a2e18878b475aef39b690fa884d6db6a1054d1da8d7`.

Approved phone gate:
`docs/review/p20-r2-fixed-rod-arc-rail/p20_r2_corrected_twist_center_gate.png`.
