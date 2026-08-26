# P20 R1 fixed-rod reset handoff

Date: `2026-08-26`

## Status

P20-DESIGN-01 completed its cheap analytic gate with disposition **BLOCKED**.
The centered-equivalent transform is mathematically valid, but removal of all
six outer white-rod rails makes every retained OD4 x 50 rod intersect both
solid outer plates at OPEN. No P20 source, test, CAD solid, STEP, Viewer
artifact, mesh, 3MF, slice, print, or physical acceptance exists.

P20-CRITIC-01 independently verified the exact design candidate and reproduced
the blocker. Its report is `DESIGN_CRITIQUE.md`, SHA-256
`fe5762cef497214c4da7291fc89e7f05ebcb0789f61c8912580110680860abfc`.

## Frozen provenance

- Branch: `codex/xt60-p20-r1-fixed-rod-reset`.
- Contract-opening HEAD:
  `e0474bd6f3475cc26c71a9e84148f78b606a1db4`.
- Product baseline: merged P19 R1
  `b69b6ad12af611644987f026eef4940db9c7bb34`.
- P19 candidate manifest SHA-256:
  `e2492339de9037b6e2a84351699b693202e4585a32623305c616d97712b91677`.
- P20 design input: `DESIGN_INPUT_MANIFEST.sha256`.

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

## Design gate result

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

## Next action

Do not start P20-IMPL-01. Ask the user whether to keep the strict no-outer-
aperture rule and close P20 as infeasible, or open a new intent contract that
changes at least one frozen object/topology. The smallest single-object
reopening to investigate is non-guiding outer-plate clearance apertures, but
none are authorized or designed by this handoff.
