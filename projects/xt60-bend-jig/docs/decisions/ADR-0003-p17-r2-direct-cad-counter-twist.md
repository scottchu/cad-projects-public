# ADR-0003: P17 R2 direct-CAD counter-twist continuation

- Status: accepted
- Date: `2026-08-24`
- Supersedes: `ADR-0001` as the active forward architecture after P13
  physical feedback; P17 R1 simulator artifact as evidence
- Superseded by:

## Context

The supported P13 four-plate/three-rod prototype reached digital acceptance but
physical feedback exposed architecture-level issues: excessive middle spacing,
rod protrusion, uncertain rod length, all caps must be permanent, two caps were
too tight on nominal rods, fixed inner plates must never rotate, outer hand
plates must counter-rotate, and the named `LOCKED` pose did not prove a real
lock.

The follow-up P17-D02 user correction requires the original good four-plate
plus one center-bar architecture. P17 R2 must not add three yoke/stability bars
or yoke socket/tenon features.

The follow-up P17-D03 numeric/assembly correction supersedes P17-D02's
provisional `AF6` fixed-inner hex key/bore with `OD8` round journal. That
combination is unassemblable because the fixed inner plate must slide over the
outer round journal before seating on the inner hex key.

P17 R1 attempted to review the counter-twist design with a simulator first, but
the user rejected that simulator artifact on `2026-08-24` because holes or
slots appeared to move with animation and directed the project to skip
simulation. The failed simulator artifact does not invalidate the P17 design
version. It rejects the simulator evidence and its provisional geometry only.

## Alternatives considered

- Preserve P13 and only adjust rod/cap lengths. Rejected because the feedback
  changes fixed/moving roles, cap permanence, lock proof, and span/rod
  derivation together.
- Repair or continue the P17 R1 simulator. Rejected by user direction.
- Use a geared or linked counter-rotation mechanism immediately. Mechanically
  plausible, but larger than needed for this direct-CAD revision and adds gear or
  link hardware risks before the rod/slot/center-axle stack is proven.
- Use two-hand direct counter-twist with independently supported outer plates,
  fixed inner guide slots, rigid rods, and complementary physical outer slots.
- Use three yoke/stability bars or yoke socket/tenon features to ground the
  inner plates. Rejected by explicit user correction; it adds unwanted support
  structure and diverges from the good four-plate plus one center-bar
  architecture.

## Decision

Continue P17 as R2 direct STEP-first CAD for a two-hand direct counter-twist
mechanism. The active architecture is four plates plus one stepped center axle.
The center axle has a larger central hex spacer that sets the fixed-inner clear
span and provides axial shoulders, smaller hex key sections through matching
fixed-inner hex bores, outer round journal sections for independent outer-plate
rotation, and thin outer keepers. The axle grounds/supports the inner plates
only; it must not couple outer rotation. Three rigid rods and six permanent
follower caps move along fixed guide lines through complementary outer slots.
The right outer plate is the primary actuator side and must provide a
quantitatively larger grip/lever affordance plus endpoint
hard-stop/detent/over-center lock geometry.

Within that decision, P17-D03 sets a required slide-over invariant:
`outer_journal_diameter < fixed_inner_hex_bore_af`. Coherent provisional
defaults are central spacer hex `AF10`, inner key `AF8`, fixed-inner hex bore
about `AF8.15`, round journal about `OD7.60`, and outer bearing bore about
`7.90`, all subject to named print clearances and minimum wall checks. Per
side, the center axle extends from central shoulder through full fixed-inner
hex-key engagement, running gap, full outer-plate journal overlap, keeper
clearance, and an actual keeper seat. Keepers must be retained geometry, not
floating rings.

P17 R2 supersedes P13's `50.00 mm` uncut-rod freeze, removable-cap wording, and
accepted `ID3.90` permanent-cap interference. P17 R2 must re-derive inner clear
span, center-axle stack, rod length, cap engagement, journal/keeper clearances,
and lock path together.

## Consequences

This keeps the P17 R2 CAD candidate focused on the user's physical
mechanism concerns rather than simulator repair or premature link/gear
hardware. It requires stronger CAD tests for actual part-local slot geometry,
fixed transforms, opposite rotations, rod skew, center-axle/XT60/wire
collisions, cap count/retention geometry, journal clearance, keeper retention,
and lock contact. CAD still cannot prove physical cap retention, lock force,
heat response, wear, vibration resistance, springback, or printed fit.

Version policy applied: `P` increments only for a core product-design
baseline, architecture, or interface change. `R` increments for same-design
geometry, fit, manufacturing, or implementation refinement. Simulator, STEP,
3MF, slicer, and physical status are independent evidence layers and never
alone bump `P`.

## Evidence

- `docs/iterations/p17-r2-direct-cad-counter-twist/BRIEF.md`
- `docs/iterations/p17-r2-direct-cad-counter-twist/DESIGN.md`
- `docs/EXPERIENCE.md`
- Supplied photos with hashes recorded in the P17 R2 brief and experience log
