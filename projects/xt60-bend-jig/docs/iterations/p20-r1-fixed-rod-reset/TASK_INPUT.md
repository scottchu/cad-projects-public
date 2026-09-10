# P20 R1 fixed-rod reset task input

Date: `2026-08-26`

## Exact baseline

- Working branch: `codex/xt60-p20-r1-fixed-rod-reset`.
- Contract-opening commit: `e0474bd6f3475cc26c71a9e84148f78b606a1db4`.
- Product input baseline: merged P19 R1 commit
  `b69b6ad12af611644987f026eef4940db9c7bb34`.
- P19 candidate manifest:
  `docs/iterations/p19-r1-front-edge-short-tail/IMPLEMENTATION_CANDIDATE.sha256`.
- P19 candidate-manifest SHA-256:
  `e2492339de9037b6e2a84351699b693202e4585a32623305c616d97712b91677`.
- P19 source and focused test are the authoritative starting geometry and
  behavior. Earlier P17 experiments preserved in branch history are not P20
  design inputs and must not be mixed into this correction.

P19 remains traceable as the prior independently accepted digital CAD/STEP
fingerprint. The user's failure report supersedes P19 only as the active
forward product direction; it does not rewrite or erase its evidence.

## User request

The user's exact reset request was:

> P19 failed can you check
>
> feedback:
>
> - 3 rods outer plate rails vs inner plate rails - they overlaps too much
> - fixed rod doesn't even have enough rotation power
>
> start over -
>
> 1. Take P19 - remove all the 3 outer plate rails for 3 rods
> 2. Move the fixed rod outward to even more lower left
> 3. Change the fixed rod rotation 45 degree on each side so total is 90 degree
> 4. re-calculate the fix rod rotation rails path - the result of the rails
>    path should be identical as if the fixed rod is in the center point
> 5. STOP here

## Confirmed interpretation

The user explicitly answered `YES - go ahead` to this interpretation:

- Start over from P19 as the only product baseline; do not continue the prior
  repair direction.
- Remove all three rod-rail paths from each of the two outer plates: six outer
  rod rails total. Retain the three fixed-inner rod paths in both inner plates.
- Move the real purple fixed stepped rod/axle farther outward toward lower-left
  in physical FRONT YZ.
- The fixed axle remains fixed in world and keyed to the inner plates. The two
  outer plates receive equal and opposite `45 deg` travel, giving `90 deg`
  total relative twist.
- Rederive the two outer-plate fixed-axle guide paths. Their motion result must
  be equivalent to using the fixed rod as the rotation-center reference; they
  must not be translated copies of the old P19 arc.
- Preserve rod identities, P19 OPEN/END world topology, `+Z` mating-head/up,
  `+Y` solder-tail/tool/outward-right, the fixed-inner rod paths, rod stock and
  caps, and workpiece/service geometry unless the bounded design proves that an
  invariant is impossible.
- Stop after this correction and its required CAD/STEP verification. Do not
  create 3MF, slice, print, add a lock, or continue into optimization.

## Version decision

This opens `P20 R1`. Removing the outer plates' rod-guidance network, moving
the fixed reaction datum, and changing the relative twist from P19's `10 deg`
total to `90 deg` changes the mechanism architecture and external motion
contract. Under the user-confirmed P/R policy, that requires a new `P`
baseline rather than a P19 refinement.

## Open design facts that must not be guessed

- “Farther outward toward lower-left” is a directional constraint, not an
  authorized numeric coordinate.
- “Equivalent to the fixed rod being the center point” is a required motion
  result, but its exact transform, datums, and falsifiable equivalence checks
  must be derived by the P20 design role.
- Removal of all six outer rod rails may change constraint closure, support,
  force transfer, and plate integrity. The design role must expose those
  consequences before source implementation.

These facts keep the cheap FRONT-YZ intent/motion gate open. No P20 source,
test, BREP, STEP, Viewer, mesh, slicer, or print work is authorized until the
design role produces one exact candidate and the user confirms the resulting
2D orientation/topology/path gate.
