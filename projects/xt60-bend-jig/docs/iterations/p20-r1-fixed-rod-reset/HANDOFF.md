# P20 R1 fixed-rod reset handoff

Date: `2026-08-26`

## Status

The exact **evidence-only, non-candidate scaffold** is complete and formally
accepted for scaffold conformance only. Candidate manifest SHA-256 is
`59ad1459f3abcdbb3a8771f3fa10ad461471594d47dbb723781ea3597f9395c9`,
verified `20/20`. It is intentionally colliding and is not a movable,
manufacturable, printable, or physically accepted mechanism.

P20-CRITIC-01 independently verified the exact design candidate and reproduced
the blocker. Its report is `DESIGN_CRITIQUE.md`, SHA-256
`fe5762cef497214c4da7291fc89e7f05ebcb0789f61c8912580110680860abfc`.
Those records remain immutable prior blocked proof; the new scaffold contract
does not rewrite them.

## Frozen provenance

- Branch: `codex/xt60-p20-r1-fixed-rod-reset`.
- Contract-opening HEAD:
  `e0474bd6f3475cc26c71a9e84148f78b606a1db4`.
- Scaffold-contract-opening HEAD:
  `5e58e37ad22ed9d2121417c245410c3dbda45a7b`.
- Product baseline: merged P19 R1
  `b69b6ad12af611644987f026eef4940db9c7bb34`.
- P19 candidate manifest SHA-256:
  `e2492339de9037b6e2a84351699b693202e4585a32623305c616d97712b91677`.
- P20 design input: `DESIGN_INPUT_MANIFEST.sha256`.
- Active scaffold input: `SCAFFOLD_INPUT_MANIFEST.sha256`.

P19 evidence remains immutable history. The user's reported rail overlap and
insufficient effective rotation supersede P19 for forward product design.

## Frozen correction

- Remove all three white-rod rails from each outer plate, six total.
- Retain the three fixed-inner rod paths in both inner plates.
- Move the real purple fixed axle farther lower-left in FRONT YZ.
- Keep the axle and inner plates fixed; rotate left/right outer plates
  `-45/+45 deg` using one shared state, `90 deg` relative total.
- Rederive the two outer-plate fixed-axle guide paths so the motion result is
  centered-equivalent to the fixed axle, never a translated P19 arc.
- Preserve P19 orientation, rod identities and world topology, rod/cap stock,
  plate/workpiece/service geometry, and all unlisted objects unless exact
  design evidence proves impossibility and returns for authorization.
- Stop after the bounded correction and required verification. No 3MF,
  slicing, printing, lock, extra part, or further optimization.

## Prior blocked product gate

- Design-coordinate witness: `A=(-15.00,-11.00)`, one P19 rod radius farther
  in each required lower-left direction from `(-13,-9)`. It passes
  conservative plate/bore web and retained-inner-track clearance gates, but is
  not an implementation candidate because topology fails.
- Centered-equivalent outer frame:
  `T_s(q,u)=A+R(alpha_s(u))q`, with `alpha_left=-45u` and
  `alpha_right=+45u`. The fixed axle is local `(0,0)` on both sides for all
  states, so both outer guide loci are one identical constant round journal.
- Independent critique notes one representation nuance: naming `A` as the
  local frame origin is sufficient but not mandatory; the physical invariant
  is rotation about `A` with one constant plate-local axle point.
- Exact P19 X intervals put every rod `[-25,+25]` through the left outer slab
  `[-16,-12.8]` and right outer slab `[12.8,16]`.
- At OPEN all rod sections are wholly inside both plate rims. The analytic
  intersection is `40.212386 mm^3` per rod/plate pair, `241.274316 mm^3`
  across six pairs.
- Authority: `DESIGN.md` and
  `docs/review/p20-r1-fixed-rod-reset/p20-r1-fixed-rod-reset-2d-gate.svg`.
- Hand torque, force transfer, friction, backlash, fit, heat, wear, retention,
  and real soldering ergonomics remain physical unknowns.

## Active scaffold clarification

- Implement exactly zero outer rod rails and zero substitute clearance holes,
  windows, slots, pockets, or bores.
- Preserve the known six rod/solid-outer-plate collisions as deliberate,
  temporary, individually reported scaffold evidence.
- Use `A=(-15,-11)`, centered constant axle guides, fixed inner plates/axle,
  and shared `-45/+45 deg` outer motion.
- Do not call the result a complete movable assembly or accepted product.
- Adding the three outer rod rails back one at a time belongs to future,
  separately authorized iterations; no rail order or geometry is in scope now.
- Stop after independent scaffold critique, validation, and formal conformance
  review. No 3MF, slicing, printing, or next-rail work.

## Completed scaffold evidence

- Implementation receipt SHA-256:
  `b14be60cb9999738168f59f5c80642c36b8cb1ceee6ddcce1e8e1777189b7c36`.
- Focused repair restored static service occurrences, made collision
  evaluation fail closed, and replaced opaque motion-like media with
  transparent annotated static collision evidence.
- P20 tests `8/8`; combined P19+P20 regression `16/16`.
- OPEN/mid/END source states have `19` top-level occurrences; written STEP
  expands the service compound to `22` leaf occurrences. Full-motion has
  `18` occurrences. All four STEP artifacts validate and match source.
- Independent critic recheck SHA-256:
  `6531dea20ed5d4d744259f5c6a4c8896d2c0ec929ff47395a5757f0282d10819`,
  verdict `PASS`.
- Independent validator recheck SHA-256:
  `73312ac348745ce6a1a513283e752094bc826f1effcda028961f43d3b23a10b0`,
  verdict `PASS`.
- Formal scaffold review SHA-256:
  `3f57e45432591b13ed7fcc71011185534c18107f099ac251b93c5dc6ee131130`,
  verdict `ACCEPT` for scaffold conformance only.

## Next action

**STOP.** Do not dispatch the superseded product-candidate tasks or add any
outer rail. A future rail requires separate user authorization, a new
immutable manifest, and a contract for exactly one named rail only.
