# P19 R1 task input

Date: `2026-08-26`
Baseline Git commit: `bcc16305ff112ba814bdf19ad544a5819127e902`
Baseline design: `P18 R1 compact counter-twist`

## User-confirmed intent

- The actual use is soldering an XT60 onto short FPV-drone ESC leads. The
  design may not assume a long wire tail.
- FRONT is `+Y`/right and UP is `+Z`. The XT60 mating head stays up.
- Move the complete three-rod working triangle toward the upper-right/front
  plate boundary. The short tail must protrude beyond the right/front edge so
  soldering happens outside the plate envelope.
- Keep the clamp as close as possible to the solder joint/front edge; do not
  solve access by moving the clamp far away from the wire.
- Preserve the OPEN right-angle rod topology and END diagonal topology with
  rod identities unchanged.
- Preserve three uncut `OD4 x 50 mm` stainless rods, six permanent caps, four
  plates, fixed inner plates, and equal/opposite outer-plate twist.
- The old P18 inner/outer rail lengths are not invariants. Inner tracks may be
  shortened or curved. Outer rod rails may be shortened and must be
  deterministically inverse-derived from the selected rod paths.
- `45 deg` remains the twist upper limit, not a mandatory target if a smaller
  angle improves service access, rail length, force angle, or boundary web.
- Plate diameter target remains `50-55 mm`; `80 mm` is unacceptable.
- The fixed printed axle must remain a real X-axis structural member through
  the four-plate stack. Its exact YZ location must be shown explicitly in the
  2D gate and cannot appear as an unsupported/floating point.

## Required decision sequence

1. Produce a cheap front-view YZ 2D gate before 3D CAD.
2. Show OPEN, END, plate boundary, XT60, short-tail exit, soldering service
   corridor, fixed axle, and complete rod/rail swept envelopes.
3. Select the maximum-front candidate that preserves minimum material web,
   identity, non-crossing continuous paths, and usable force direction.
4. Freeze the accepted 2D parameters and only then implement 3D STEP-first
   CAD.

## Non-goals for the 2D gate

- No 3MF, slicing, printing, or physical-acceptance claim.
- No new stability bar, yoke, gear, linkage, grip block, or removable cap.
- No hand-edited outer rails; every outer rail is a deterministic transform of
  one named inner/world rod path and the outer-plate rotation law.

## User decision — re-optimization cycle 2

On `2026-08-26` the user selected option 2 after reviewing the isolated
short-outer-rail analysis: re-optimize before 3D with a hard minimum
`outer_rail_center_travel >= 2.00 mm` for every one of the six outer rod
rails. This is a bounded P19 R1 refinement, not a new product version.

The optimizer may vary only the numeric P19 2D motion parameters needed to
meet that constraint, including twist magnitude up to `45 deg`, rod OPEN/END
coordinates within the already-approved topology, and common working-region
placement. It must preserve the `50-55 mm` plate envelope, `>=2.20 mm` web,
complete outside-rim solder-tool keepout, fixed real axle, OD4.15 rail fit,
rod identities, non-crossing paths, exact OPEN right angle, exact END
diagonal, and deterministic inverse-derived outer rails. It may not satisfy
the constraint by hand-extending a rail beyond the physical rod path.

## User decision — re-optimization cycle 3 supersedes cycle 2

After viewing the cycle-2 result, the user rejected its shortest
`2.142936 mm` rail as visibly too short and explicitly set the minimum to
`4.00 mm`. The cycle-2 `REOPTIMIZED_DESIGN.md`,
`REOPTIMIZED_CRITIQUE.md`, and `reoptimized-option2-mintravel.png` are
superseded 2D evidence only. They are not the active P19 candidate and may not
authorize 3D.

The active hard gate is now:

```text
outer_rail_center_travel_i >= 4.00 mm  for all six rod rails
```

For the named `OD4.15 mm` rail cutter this also implies a complete capsule
length of at least `8.15 mm` and an aspect proxy of at least
`8.15 / 4.15 = 1.963855` without adding decorative endpoint travel.

### Cycle-3 per-object delta mask

- May change: equal/opposite twist magnitude up to `45 deg`; common END
  diagonal translation; if those variables alone are infeasible, the smallest
  common working-region translation or topology-preserving OPEN/END numeric
  adjustment identified by the optimizer.
- Must remain invariant: physical `+Z` head/up and `+Y` short-tail/tool/right;
  exact ordered OPEN right angle; exact ordered END equal-pitch diagonal; all
  three rod identities; non-crossing continuous paths; `C=(0,0)` unless a
  separately documented infeasibility proof requires reopening it; real
  stepped axle `A=(-13,-9)` through all four plates; three `OD4 x 50 mm`
  rods; six permanent caps; four plates; fixed inners; opposite rotating
  outers; `OD4.15` rod rails; plate OD hierarchy within `50-55 mm`; minimum
  estimated web `>=2.20 mm`; complete `8 x 8 mm` solder-tool keepout at least
  `0.75 mm` beyond the largest rim; short-tail service; deterministic inverse
  rail law; no added parts, grip, lock or self-lock claim.
- Forbidden repair: manually extending any outer rail beyond the exact
  inverse image of its physical rod path.

## User decision — cycle 4 implementation authorization

On `2026-08-26` the user authorized CAD implementation after confirming that
the left and right outer plates must traverse the entire motion with one
shared normalized state and equal-magnitude opposite rotation. The cycle-3
bounded search proved that the original OPEN coordinates cannot satisfy all
six `>=4.00 mm` outer-rail travels, OPEN wire clearance, and `>=2.20 mm`
internal web simultaneously. The smallest ranked reopening is therefore
authorized before source implementation:

- change only `OPEN_upright_Z` downward by the minimum optimizer-selected
  amount needed to recover all hard gates;
- keep `OPEN_bottom=(5,10)` and `OPEN_diagonal=(20.4,10)` fixed, so the OPEN
  top leg stays horizontal and the right leg stays exactly vertical;
- keep `C=(0,0)`, `A=(-13,-9)`, the three rod identities, equal-pitch END
  diagonal, plate ODs `54.4/54.7/55.0`, complete tool keepout, short-tail
  direction, real four-plate stepped axle, three `OD4 x 50` rods, six
  permanent caps and every other cycle-3 invariant fixed;
- require one shared `u in [0,1]` for the entire motion, with
  `alpha_left(u)=-theta*u`, `alpha_right(u)=+theta*u`, and the same physical
  world paths `p_i(u)` reconstructed by both sides at every sampled state;
- retain all six physical inverse rail centre travels `>=4.00 mm`, OD4.15
  cutters, estimated/BREP web `>=2.20 mm`, non-crossing identities, credible
  OPEN wire insertion clearance and END contact/preload.

This authorizes source-first P19 CAD only after the corrected cheap analytic
gate passes. A failing analytic gate must stop CAD generation rather than be
materialized as a product candidate.

### Cycle-4 non-degeneracy gate

The first cycle-4 limit proof showed that minimizing only the upright OPEN
change has an unattained infimum at `theta=0 deg`. That limit makes both outer
plates stationary, collapses the fixed-axle guide to a point and violates the
counter-twist mechanism intent despite satisfying nominal rail length. It is
therefore excluded as a degenerate non-mechanism.

The implementation candidate must additionally satisfy:

- `5.0 deg <= theta <= 45.0 deg` per outer plate;
- rank `3` throughout the sampled motion;
- worst normalized four-contact condition `<=15.0`.

An exact cycle-4 tangent proof supersedes the provisional crossing-angle hard
gate: for a straight world rod path and its exact inverse rotating-plate rail,
any closest-point state inside `u in [0,1]` produces a zero instantaneous
path/rail crossing angle independent of twist magnitude. Crossing must still
be reported with its exact state, but it is a physical friction/backlash/force
unknown rather than a candidate blocker when the complete three-rod contact
system retains rank `3` and condition `<=15.0`.

The first non-degenerate minimum placed the diagonal rod exactly tangent to
the nominal wire envelope at OPEN (`0.000 mm` surface clearance). Exact
tangency is not credible loading/removal clearance once printed and wire-OD
tolerances are considered. The source-implementation candidate therefore
requires at least `0.75 mm` OPEN surface clearance for each of the three named
rods while retaining the selected END contact/preload construction.

The former provisional `0.50 mm` allowance is superseded. Independent
removal validation proved that the seated removal-path endpoint inherits that
same `0.50 mm` diagonal-wire clearance, so no continuous waypoint path can
meet the repository's `0.75 mm` completed-pigtail removal gate without first
raising the OPEN geometric clearance itself.

## P19-REPAIR-01 — completed-pigtail removal path

Independent validation of implementation fingerprint
`83a56c9fa8a498f43510ba25529b9e7fe296d0469b4fe5cf4704e783ddb901da`
found that the inherited rigid completed-pigtail removal waypoints collide
with the diagonal rod. Both finite bent-wire occurrences intersect it by
approximately `47.259 mm3`. The aggregate compound evidence also incorrectly
reported zero volume despite the pairwise collisions.

The authorized smallest implementation repair is therefore:

- freeze all accepted product geometry and motion: OPEN/END rods, six rails,
  `C`, `A`, plate ODs, axle, caps, XT60/wire shapes, tool/cup service and STEP
  assembly geometry;
- rederive only the completed-pigtail rigid-removal waypoints/pose sequence;
- require pairwise actual-solid minimum clearance `>=0.75 mm` against every
  OPEN production solid throughout the complete path;
- make the evidence aggregation report the limiting named pair, pose,
  distance and positive-volume intersection correctly;
- rerun the affected service tests plus candidate manifest/STEP parity checks.

The bounded waypoint-only repair proved infeasible because the seated start
pose had only `0.50 mm` diagonal-wire clearance. Product geometry is therefore
explicitly reopened only enough to enforce the superseding `0.75 mm` OPEN
clearance above; all other cycle-4 variables and invariants remain frozen.

These are analytic candidate-selection guards, not claims of physical hand
force, friction, backlash, stiffness or self-locking. Those remain physical
validation gaps.
