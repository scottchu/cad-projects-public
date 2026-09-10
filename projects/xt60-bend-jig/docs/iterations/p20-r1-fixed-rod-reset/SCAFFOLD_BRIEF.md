# P20 R1 no-outer-rod-rails scaffold brief

Status: **FROZEN EVIDENCE-ONLY SCAFFOLD CONTRACT; NOT A PRODUCT CANDIDATE**

Date: `2026-08-26`
Contract-opening HEAD: `5e58e37ad22ed9d2121417c245410c3dbda45a7b`
Product baseline: P19 R1 at
`b69b6ad12af611644987f026eef4940db9c7bb34`

## User clarification and sequential intent

The user explicitly clarified that P20 is a deliberate intermediate scaffold:

- do not add separate clearance holes or windows now;
- remove all six outer rod rails even though the retained rods will intersect
  the solid outer plates;
- those rod/outer-plate collisions are known, temporary, and expected;
- later, separately authorized iterations will add the three outer rod rails
  back one at a time;
- this step stops after removing the six rails, moving the fixed axle farther
  lower-left, applying `-45/+45 deg` outer-plate travel, and implementing the
  centered-equivalent fixed-axle guide.

This clarification changes the delivery class, not the prior analytic facts.
`DESIGN.md`, `DESIGN_CANDIDATE.sha256`, `DESIGN_CRITIQUE.md`, and the frozen
2D review image remain immutable evidence that six collisions exist. Their
former product-candidate BLOCKED conclusion is preserved. The scaffold may
advance only because the user now authorizes those collisions as an explicit
temporary construction state.

The user explicitly rejects solving or adding all three outer rails at once.
Each outer rail is coupled to its corresponding fixed-inner rail path, and
each outer rail also changes its neighboring outer rails' spacing, overlap,
material web, and collision conditions. The required future workflow is
therefore one-factor-at-a-time: freeze this axle-only scaffold first; later add
exactly one named outer rail; validate it against its corresponding inner path
and every already-present neighboring outer rail; freeze that result before
starting the next. A failed addition rolls back only that one rail. This task
does not choose the future rod order and stops before adding any outer rod
rail; order requires a later explicit gate.

## Exact scaffold geometry contract

- Physical FRONT remains world YZ: `+Z` mating-head/up and `+Y` short-tail,
  tool approach, outward/right.
- Start from exact P19 source geometry and retain its three rod identities,
  OPEN/END world paths, three fixed-inner rod paths in both inner plates,
  `OD4 x 50 mm` rod stock, six caps, plate bodies/stack, workpiece, service
  geometry, axle profile, and keeper geometry.
- Fixed stepped-axle datum is the independently checked design witness
  `A=(-15.00,-11.00) mm`, farther lower-left from P19 `A=(-13,-9)`.
- One shared state `u in [0,1]` gives
  `alpha_left(u)=-45u deg` and `alpha_right(u)=+45u deg`, exactly `90 deg`
  relative travel at END. Both inner plates and the axle remain fixed.
- Centered-equivalent outer frame is
  `T_s(q,u)=A+R(alpha_s(u))q`. The stationary axle is one constant local point
  `q_A=(0,0)` for both sides and all states. Each outer plate therefore uses
  the same centered round axle journal/guide at that local point, not a
  translated P19 arcuate guide.
- Remove the three white-rod rails from each outer plate, six total. Do not
  replace them with clearance holes, windows, slots, pockets, bores, or any
  other rod aperture in this scaffold.

## Exact delta mask

| Object | Authorized change now | Frozen / forbidden now |
|---|---|---|
| Left outer plate | Remove its three rod-rail cuts; replace its P19 fixed-axle arc only with the centered-equivalent round guide; rotate through `-45 deg`. | Any rod clearance aperture, re-added rod rail, plate-body/OD/thickness/grip change, new feature or part. |
| Right outer plate | Remove its three rod-rail cuts; replace its P19 fixed-axle arc only with the centered-equivalent round guide; rotate through `+45 deg`. | Any rod clearance aperture, re-added rod rail, plate-body/OD/thickness/force-side change, new feature or part. |
| Both inner plates | Move only the fixed-axle keyed bore/seat from `(-13,-9)` to `(-15,-11)`. | Any change to the three fixed-inner rod paths, plate bodies, roles, X placement, or world rotation. |
| Purple axle and keepers | Move their complete world YZ occurrences to `A=(-15,-11)`. | Source geometry, X-axis role, dimensions, stack engagement, or world rotation. |
| Three white rods and six caps | No geometry, identity, or P19 world-path change. | Reassignment, shortening, mirroring, crossing, or geometry used to hide the expected plate collisions. |
| Workpiece/service geometry | No change. | Moving or deleting XT60, wire/cup/tool/removal evidence to avoid collision reporting. |
| Later rail sequence | None in this step. | Adding back even one outer rod rail, choosing its order, optimizing it, or claiming evidence for a future iteration. |

## Required evidence and known collision disposition

- Source and written scaffold artifacts must prove exactly zero outer rod rails
  and zero substitute outer rod apertures, while preserving the three
  fixed-inner paths by role.
- Tests and reports must name the rod/solid-outer-plate collisions as expected,
  temporary scaffold evidence. They must not suppress, allow-list away, or
  summarize them as zero collision.
- The prior analytic OPEN result remains authoritative context: six named
  rod/plate collision pairs, approximately `40.212386 mm3` each and
  `241.274316 mm3` total. Implementation validation must measure the actual
  source/STEP scaffold and report its exact result; it must not assume numeric
  equality with the analytic proxy.
- The centered-equivalent transform, constant guide location, `-45/+45 deg`
  endpoints, fixed inner/axle identities, required rail absence, occurrence
  census, source/export parity, and visual labeling remain falsifiable gates.
- Any collision beyond the explicitly expected three rods against two outer
  plate solids is a blocker. Any hidden rod aperture, added rail, changed
  workpiece/service geometry, or product-acceptance wording is a blocker.

## Delivery and stop boundary

The result is an evidence-only, intentionally colliding sequential scaffold.
It is not a complete movable assembly, CAD-accepted product candidate,
print-ready part, or physical prototype. Formal review may accept only that
the exact scaffold conforms to this contract and truthfully exposes its known
collisions.

Stop after the scoped source/test/STEP/snapshot evidence and independent
critic, validator, and formal scaffold review. Do not create 3MF, slice,
print, add clearance holes, add back a rail, select the later rail order, add a
lock/part, optimize, or claim mechanism/product/physical acceptance.

Future one-rail iterations must each own a new immutable input/candidate
fingerprint. Their acceptance gate must trace the named outer rail to its
corresponding inner path, check all already-frozen neighboring outer rails,
and keep rollback bounded to the newly attempted rail.
