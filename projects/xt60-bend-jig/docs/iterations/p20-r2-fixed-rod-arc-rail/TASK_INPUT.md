# P20 R2 fixed-rod arc-rail task input

Date: `2026-08-26`

## Exact provenance

- Working branch: `codex/xt60-p20-r1-fixed-rod-reset`.
- Contract-opening clean HEAD:
  `a48c5697f9126dbb6934d764e48f2a01f6a01475`.
- Product input baseline: merged P19 R1
  `b69b6ad12af611644987f026eef4940db9c7bb34`.
- P19 source, focused tests, accepted candidate manifest, design, validation,
  and formal review are the only product-design inputs.
- P20 R1 remains immutable rejected history. Its scaffold correctly records
  zero white-rod outer rails and `A=(-15,-11)`, but it used a
  constant round journal by changing the effective outer-plate rotation center
  to `A`. The user rejected it because the requested fixed-rod rotation rail
  was missing.

## User correction

The user asked where the rail was, then clarified that the task was to retain
and recalculate the purple fixed-rod rotation rail. They explicitly rejected
the P20 R1 interpretation in which that rail became a round journal and asked
to correct it now.

The corrected task is:

1. Start from P19.
2. Remove exactly the three white-rod outer rails from each outer plate, six
   total; retain all three inner-plate rod rails.
3. Move the purple fixed rod/axle farther lower-left, using the already
   reviewed witness `A=(-15,-11)` unless a cheap analytic design gate proves
   that witness invalid for the corrected kinematics.
4. Keep P19's virtual outer rotation center `C=(0,0)`, the fixed axle world
   stationary, and both inner plates fixed.
5. Rotate the physical left outer plate `+45 deg` and physical right outer
   plate `-45 deg` about `C`, exactly `90 deg` relative.
6. Recompute a true curved fixed-rod rotation rail in each outer plate from
   the P19 inverse-frame locus about `C`; never replace it with a round journal
   or rotate the plate about `A`.
7. Prove both rails reconstruct the same stationary world axle at every
   sampled state and make the curved rails plainly visible in review media.
8. Stop after corrected implementation and its required evidence.

The user explicitly approved the corrected FRONT-YZ sign gate at
`/tmp/p20_r2_corrected_twist_center_gate.png`, SHA-256
`e2d05a852889bef2e9c97a2e18878b475aef39b690fa884d6db6a1054d1da8d7`.
That approval supersedes all earlier P20 R2 sign assumptions.

## Sequential white-rod rationale

No white-rod outer rail is added in P20 R2. The user will add those rails one
at a time in later iterations because each outer rail is coupled to its
corresponding inner-plate rail path and because each added outer rail affects
the spacing, overlap, material web, and collision behavior of its neighbor.
Simultaneous multi-rail design would hide which interaction caused a failure.

## Acceptance boundary

This remains a deliberately colliding, non-product intermediate: with all six
white-rod outer rails absent, the three rods intersect both solid outer plates.
Those six known collisions must remain visible and separately reported. They
do not authorize substitute holes, white-rod rails, rod changes, or product,
manufacturing, print, or physical-acceptance claims.
