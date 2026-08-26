# P19 R1 re-optimized option-2 independent 2D critique

Decision: **ACCEPT FOR USER 2D REVIEW ONLY.**

This decision does not approve 3D CAD, STEP, slicing, printing, force,
self-locking, fit, solder-tool access in X, or physical acceptance. The user
may review this exact 2D candidate; it must not advance automatically to 3D.

Owner/role: `/root/p17_optimizer_math_audit`, independent kinematic and
service critic. No design, CAD source, tests, STEP, or continuity files were
changed by this review.

## Frozen inputs and candidate

- `REOPTIMIZE_INPUT.sha256`: verified `7/7`; manifest SHA-256
  `854d9dd121f4eea2cedd12efd101a8acf0584626fe27efe5b1211b787a86b07a`.
- `REOPTIMIZED_DESIGN.md` SHA-256:
  `291f155ce85f5fb5acab41ff4bc1287c05e47c6ac8edc884160497f95e1198e5`.
- `docs/review/p19-r1-front-edge-short-tail/reoptimized-option2-mintravel.png`
  SHA-256:
  `d256073709c3ce518f19a22931eb52db4a1cbbb7ecc1496e2358158a42daf508`.
- Baseline: Git commit `bcc16305ff112ba814bdf19ad544a5819127e902` plus
  the exact accepted P19 repair-1 input set named by the verified manifest.

## Independent reproduction

I independently evaluated the frozen candidate, rather than trusting the
reported table. For every rod `i`, I used

```text
p_i(u) = OPEN_i + u (END_i - OPEN_i)
q_s,i(u) = R(-alpha_s(u)) p_i(u),  0 <= u <= 1
```

with `alpha_left=-12.2u deg`, `alpha_right=+12.2u deg`, `200,001`
centreline samples for arc/chord/crossing checks, and `2,001 x 2,001`
independent-parameter searches for pairwise 2D webs. The maximum inverse
reconstruction residual over an additional 101-state sample was
`7.23e-15 mm`.

| outer / rod | independently reproduced centre travel | minimum crossing |
|---|---:|---:|
| left / bottom | `2.239287176 mm` | `13.698385 deg` |
| left / diagonal | `7.052050993 mm` | `21.796485 deg` |
| left / upright | `7.199992845 mm` | `9.120120 deg` |
| right / bottom | `6.744079368 mm` | `4.204535 deg` |
| right / diagonal | `11.252912415 mm` | `12.971800 deg` |
| right / upright | `2.142936368 mm` | `35.346603 deg` |

All six authoritative centre travels therefore pass `>=2.00 mm`; the minimum
margin is `0.142936368 mm`. No rail is hand-extended. The reproduced
right/upright perpendicular sagitta is only `0.003391347 mm`, confirming that
it is a real inverse-derived curve but will print as an almost straight short
capsule.

The fixed OPEN vectors are exactly `(15.4,0)` then `(0,-15)`. The END vectors
are exactly `(6.25,-5.75)` then `(6.25,-5.75)`. The named straight world paths
remain separated and non-crossing; identities remain `bottom`, `diagonal`,
and `upright` with no reassignment.

Independent cutter-envelope checks reproduced:

- maximum rod-centre radius `22.719154914 mm`;
- fixed-inner rim web `2.405845086 mm`;
- left-outer rim web `2.555845086 mm`;
- right-outer rim web `2.705845086 mm`;
- fixed-inner rail-to-rail web `4.283582733 mm`;
- left-outer rail-to-rail web `3.707542135 mm`;
- right-outer rail-to-rail web `2.531360165 mm`;
- minimum axle-guide-to-rod-rail web `19.314173464 mm`.

Thus the distinct hierarchy `OD54.4 < OD54.7 < OD55.0`, OD4.15 rod cutters,
and the `>=2.20 mm` 2D web gate pass. The overall limiting estimate remains
the fixed-inner rim at `2.405845086 mm`; the re-optimization consumes
`1.348667862 mm` of repair-1 minimum outer internal web but does not violate
the gate.

The normalized four-contact probe was independently rebuilt using row order
`fixed axle, upright, bottom, diagonal`, characteristic radius
`22.719154914 mm`, unit-row normalization, and `2,001` states per side. Rank
remained `3`; reproduced worst conditions were `7.476604` left and `4.322525`
right, both at END. The tiny `1.7e-5` difference from the design's left
condition is numerical-eigensolver scale and does not alter disposition.

## Service, orientation, and fixed axle

- The artifact visibly and numerically preserves physical FRONT orientation:
  XT60 mating head `+Z/up`; solder cups, short tail, tool and FRONT are
  `+Y/right`.
- The complete `8 x 8 mm` tool keepout begins at `Y=28.25 mm`, exactly
  `0.75 mm` beyond the OD55 tangent at `Y=27.50 mm`. Because the entire
  rectangle has `Y>=28.25 mm`, the whole FRONT keepout—not only its centre—is
  outside the largest rim.
- The cup starts at `Y=29.25 mm`; the translated short-tail centreline is
  `7.909480 mm`, `1.20 mm` shorter than repair 1 and in the requested outward
  direction.
- `A=(-13,-9)` remains a real fixed stepped axle at the left/behind location.
  The artifact's X section shows one continuous `34.90 mm` member through all
  four plates, keyed at both fixed inners and round-journalled at both rotating
  outers; it is not a floating marker or a fourth stainless locking rod.
- Opposite outer motions remain equal and opposite. The inner plates and axle
  remain fixed.

The translated wire line preserves the selected `-0.25 mm` END geometric
preload proxy for all three named rods. However, independently recomputed
first geometric contacts are approximately `u=0.8771` bottom, `u=0.0408`
diagonal, and `u=0.9055` upright. The diagonal therefore begins nominal wire
contact much earlier than in repair 1 (`u≈0.1185`) and far earlier than the
other two rods. This is a material force/deformation risk, not a 2D topology
failure; the user should see it before any 3D authorization.

## Findings and disposition

1. **PASS — requested rail-length repair.** All six inverse-derived outer
   rails independently clear `2.00 mm`; the exact shortest is
   `2.142936368 mm`.
2. **PASS — topology and identity.** OPEN remains the requested ordered right
   angle, END remains the requested ordered diagonal, and all three identities
   are continuous and non-crossing.
3. **PASS — compact envelope and service direction.** Plate diameters remain
   within `50–55 mm`; the complete tool keepout remains outside the rim; the
   working triangle moved toward the short-tail joint without moving OPEN,
   C, or A.
4. **PASS WITH SMALL MARGIN — 2D material.** The limiting estimated web is
   only `0.205845 mm` above the requirement. Exact BREP endpoint caps, AF8.15
   key corners, fillets and chamfers are not yet measured.
5. **WARNING — near-straight limiting rail.** Right/upright has adequate
   centre travel but only `0.003391 mm` sagitta. PETG clearance, endpoint
   loading and retention remain unproven.
6. **WARNING — force balance/contact timing.** The diagonal's very early
   nominal contact and the right/bottom `4.205 deg` minimum crossing can still
   produce friction, wire deformation, wedging or high hand torque. Rank and
   conditioning do not prove usable clamp force or self-locking.
7. **WARNING — service proof remains 2D FRONT only.** The image proves the
   requested direction and projected envelopes, not X-separated solder-iron
   access, heat clearance, cap/keeper interference, or a removable workpiece.

**Final decision: ACCEPT FOR USER 2D REVIEW ONLY.** Show the exact hashed PNG
and the warnings above. If the user freezes it, the next authorized gate must
measure exact solids and X-separated service before any print recommendation.
