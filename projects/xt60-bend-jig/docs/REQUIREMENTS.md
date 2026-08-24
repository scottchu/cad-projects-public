# XT60 bend jig requirements and design contract

## Active P17 R2 version correction note

P17 R2 is the direct-CAD revision of the P17 counter-twist design after
physical P13 feedback and the user's `2026-08-24` rejection of the P17 R1
simulator artifact. The failed simulator evidence does not invalidate the P17
design version. The P13 requirements below remain historical evidence for the
supported P13 R2 candidate, but the active forward architecture is governed by
`REQ-009` through `REQ-021` and
`ADR-0003-p17-r2-direct-cad-counter-twist.md`.

P17 R2 explicitly supersedes old `REQ-003` for the active design: three uncut
`OD4.00 x 50.00 mm` rods are no longer frozen. Rod length must be re-derived
from inner clear span, plate stack, cap engagement, and axial running
clearance. P17 R2 also supersedes `REQ-008` removable right-cap wording: all six
rod-end caps are permanent.

P17-D02 further refines P17 R2 without a new `P` version: do not add
three-bar yoke/stability bars or yoke socket/tenon features. The active
architecture is four plates plus one stepped center axle.

P17-D03 further corrects P17 R2 numeric and assembly defaults without a new
`P` version: the fixed-inner hex bore must be large enough for the inner plate
to slide over the outer round journal before seating on the inner hex key. The
P17-D02 provisional `AF6` key/bore with `OD8` journal combination is
superseded as unassemblable.

P17-D06 is a focused correction inside P17 R2 after visual review of P17-I04.
The fixed member is the purple printed stepped center axle, not any white
`OD4.00 mm` stainless forming rod. The axle remains fixed to both inner plates
but is separated from the outer-plate rotation-center datum and moved farther
behind the XT60. Each outer plate receives its own mirrored arcuate axle-guide
slot. This does not authorize changes to the white rods, their existing guide
paths, the lock, caps, plate spacing, or the XT60 reference.

P17-D07 supersedes only D06's provisional fixed-axle datum
`A=(-18.00,17.00) mm`. Actual-solid implementation evidence showed that datum
cutting through the frozen upright inner guide and both frozen upright outer
cams, with negative required webs. The corrected datum is
`A=(-29.00,17.00) mm`; fixed/moving identities, outer rotation center, frozen
white-rod paths, lock, caps, stack, plate dimensions, mirrored-rail equations,
motion-review contract, and P17 R2 identity remain unchanged.

P17-D08 is a user-directed bounded correction inside P17 R2. The complete
current endpoint-lock geometry is removed: both the right-outer integral nose
and the right-inner receiver/ground-arm/bridge/catch assembly. No replacement
lock is authorized in this iteration. `REQ-016` and the endpoint-lock portion
of `CHOICE-005` are therefore suspended for the active intermediate candidate;
the `32 deg` pose is end-of-travel only and carries no hard-stop, detent,
over-center, or self-lock claim. The right outer remains the larger primary
force side. All axle, plate, rod, cap, guide, XT60, stack, and motion geometry
remain frozen. The green `left_outer_secondary_grip_block` circled in the
second supplied screenshot is a finger/force tab, not lock geometry, and must
remain unchanged in this repair.

## Historical P13 outcome and use sequence

Historical P13 flow: load two insulated XT60 pigtail wires, close one rotary
input to form and hold a fixed 90-degree path, solder while keeping the plastic
body unloaded, allow cooling, reopen the jig, and remove the completed pigtail
without damage. Active P17 R2 preserves the functional outcome but replaces the
single rotary input with two-hand direct counter-twist under `REQ-010`.

## Invariants

- `REQ-001`: Clamp and form only the two insulated wires; do not use the XT60 plastic body as the clamped load.
- `REQ-002`: The supported P13 outcome is a fixed 90-degree wire path.
- `REQ-003`: Use three purchased, uncut 304 stainless rods, each `OD4.00 x 50.00 mm`.
- `REQ-004`: P13 has four principal circular plates: two fixed guides and two synchronized cams.
- `REQ-005`: One rotary input gives all three rods equal scalar travel along their distinct straight guide directions.
- `REQ-006`: The mechanism must support loading, dry motion, soldering, cooling, service, and completed-pigtail removal.
- `REQ-007`: Geometry, placement, motion, STEP, and 3MF outputs remain source-derived and parametric.
- `REQ-008`: The production kit contains four principal plates, one D shaft, one keeper, three permanent left caps, and three removable right caps; purchased rods and proof-only geometry are excluded.

## Derived constraints

- `CON-001`: `0 deg` is open, nominal first geometric wire contact is near `22 deg`, and `27 deg` is locked.
- `CON-002`: Nominal insulated wire OD is `4.30 mm`; rod radius is `2.00 mm`; wire radius is `2.15 mm`.
- `CON-003`: `wire_preload = 0.25 mm`, `contact_stroke = 3.7642135623730946 mm`, and `common_stroke = 4.014213562373095 mm` for the imported baseline.
- `CON-004`: The accepted source domain limits `wire_preload` to `0.00..0.40 mm` without renewed design review.
- `CON-005`: Principal plate and cap print orientations are authored in source; slicer-side flipping, negative Z, or `Lay on face` is not an accepted repair.
- `CON-006`: `4.15 mm` is the current evidence-backed sliding rod-hole reference and applies only after checking the bore's functional role.
- `CON-007`: The next center-hole repair must map the user's physical observation to one exact printed stick/shaft and mating hole, then change only the responsible source-controlled clearance with regression evidence.

## Design choices

- `CHOICE-001`: P13 uses no base or enclosing frame.
- `CHOICE-002`: The three rod roles are asymmetric: forming, supporting, and locking.
- `CHOICE-003`: PETG and a `0.4 mm` nozzle are the current physical prototype assumptions.

## Non-goals

- `NON-GOAL-001`: Adjustable bend angle.
- `NON-GOAL-002`: Decorative handle, replacement base, electronics, motor, or frame holder.
- `NON-GOAL-003`: Treating the XT60 envelope, wires, soldering tool, or purchased rods as printed production objects.
- `NON-GOAL-004`: Redesigning the architecture as part of the monorepo migration.
- `NON-GOAL-005`: Applying one larger diameter indiscriminately to all center, shaft, or rod bores.

## Physical unknowns

- `PHYS-001`: Exact identity and required clearance of the printed center-hole interface that rejected the user's middle stick.
- `PHYS-002`: Complete printed fit, binding, actuation effort, and repeated cycling after the center-hole repair.
- `PHYS-003`: Permanent and removable cap retention, service effort, and wear.
- `PHYS-004`: Wire holding force, insulation marking or damage, and XT60 body loading.
- `PHYS-005`: Soldering access and PETG stiffness, creep, cracking, or heat softening.
- `PHYS-006`: Completed-pigtail removal, cooled angle, and springback.

## Evidence mapping

| IDs | Evidence | Status |
|---|---|---|
| `REQ-001`–`REQ-008` | P13 brief, source, focused tests, STEP/3MF census | historical; migration rerun pending |
| `CON-001`–`CON-005` | P13 source, amendment, motion tests, artifact provenance | historical; migration rerun pending |
| `CON-006` | PETG rod-hole coupon observation | observed |
| `CON-007`, `PHYS-001` | Latest printed P13 fit observation; exact interface diagnosis pending | observed defect; unresolved |
| `PHYS-002`–`PHYS-006` | Repaired complete P13 PETG assembly and use trial | pending |

## Active P17 R2 requirements

- `REQ-009`: The two inner plates are fixed relative to one real grounded
  stepped center axle and have zero rotation in every open, mid, locked,
  service, and review state.
- `REQ-010`: The two outer plates are the hand-operated rotating elements and
  rotate in opposite directions as a real twist action. P17 R2 selects
  two-hand direct counter-twist rather than a geared/linkage synchronizer.
- `REQ-011`: P17 R2 must not use a scene-only sign flip, a shared same-direction
  actuator shaft, moving holes in fixed parts, Three.js, or simulator evidence
  as CAD authority. A source-declared, self-contained CAD Viewer parameter
  sidecar may pose already-authored rigid occurrences for review only; Python/
  build123d geometry and static generated STEP states remain authoritative.
- `REQ-012`: Both outer plates are larger than the inner plates. The primary
  force/actuator side must be slightly larger or provide a quantitatively
  larger grip/lever affordance.
- `REQ-013`: All six rod-end caps are permanent follower/retention caps. No cap
  is removable for service in the active P17 R2 production design.
- `REQ-014`: Permanent cap retention must not preserve rigid `ID3.90` on
  `OD4.00` interference as accepted. It requires a physically falsifiable
  coupon gate before physical acceptance.
- `REQ-015`: P17 R2 must re-derive inner clear span, axial stack, rod length, cap
  engagement, pivot/hub/shaft architecture, and follower interaction together.
  The active design may supersede uncut `50.00 mm` rods.
- `REQ-016`: P17 R2 must include a real grounded reaction path and explicit
  endpoint hard-stop, detent, over-center, or equivalent lock architecture
  with a torque/back-drive geometry argument. Force, wear, creep, heat,
  vibration, and self-lock proof remain physical gates.
- `REQ-017`: The functional outcome remains clamping/forming insulated wires
  without loading the XT60 plastic body, targeting a fixed 90-degree bend, and
  allowing loading, motion, soldering, cooling, and completed-pigtail removal.
- `REQ-018`: P17 R2 remains a source-derived parametric STEP-first CAD workflow;
  generated STEP/mesh/3MF artifacts must come from source and must not be
  hand-edited.
- `REQ-019`: P17 R2 uses the original good four-plate plus one center-bar
  architecture. The center bar is a one-piece stepped center axle with a larger
  central hex spacer, two smaller inner-plate hex key sections, two outer round
  journal sections, and thin axial keepers.
- `REQ-020`: The stepped center axle grounds/supports the fixed inner plates
  only. It must not couple the left or right outer plate rotation; outer plates
  must rotate independently on round journal sections with named clearance.
- `REQ-021`: The stepped center axle and fixed-inner bores must support the
  user's assembly sequence: each fixed inner plate slides over the outer round
  axle section first, then seats on the inner hex key against the central
  spacer shoulder. Keeper geometry must be physically retained, not a floating
  ring.
- `REQ-022`: The purple printed stepped center axle is world-invariant and
  positively fixes both inner plates. The three white `OD4.00 mm` stainless
  rods remain moving forming/locking rods; none becomes a fixed reaction rod.
- `REQ-023`: The fixed axle is off the outer-plate geometric/rotation center
  and farther behind the XT60 on `-Y`. Each outer plate has a dedicated
  side-specific arcuate guide slot for the axle, with left and right loci
  mirrored so the permitted open-to-lock rotations have equal magnitude and
  opposite sign.
- `REQ-024`: A fixed pin in one curved slot is not by itself a complete planar
  revolute constraint. P17 R2 must not claim that the axle slot alone forces
  pure twist. Full mechanism closure must use the already-existing rod/slot
  contact network or an independently approved integral pivot feature; D06
  must not add stability bars or new separate parts.
- `REQ-025`: The focused fixed-axle review artifact must provide visible
  open-to-lock motion with fixed inner plates and axle, opposite-moving outer
  plates, and stationary physical slot geometry. Review animation is evidence
  of the prescribed rigid transforms only, not proof of force, constraint
  closure, self-lock, or physical fit.
- `REQ-026`: The active P17 R2 intermediate candidate must contain no current
  lock nose, receiver, ground arm, axial bridge, hard stop, flexure, lead-in
  ramp, retaining shoulder, release tab, lock-only artifact, or lock evidence
  API. The `0..32 deg` trajectory remains for motion review but its endpoint is
  not a locked state. A future lock requires a separate user-authorized design
  step. The green left-secondary finger/force grip tab is explicitly retained.

## Active P17 R2 derived constraints

- `CON-008`: XT60 body width across the reduced inner span is `15.90 mm`.
- `CON-009`: Initial P17 R2 inner clear span is derived as
  `15.90 mm + 2 * xt60_side_clearance_each`; the P17 R2 design default is
  `18.40 mm` with `xt60_side_clearance_each = 1.25 mm`.
- `CON-010`: P17 R2 rod length is derived from inner clear span, two inner plate
  thicknesses, two outer plate thicknesses, two inner/outer running gaps, two
  cap/outer running gaps, and two cap engagement depths.
- `CON-011`: The existing PETG rod-hole coupon applies only to sliding
  rod-hole/slot roles: `4.05` very tight, `4.10` tight hand push/pull, `4.15`
  best sliding, `4.20` looser, and `4.25` loose/wobble.
- `CON-012`: Permanent cap sockets use their own coupon ladder and cannot claim
  physical acceptance from the sliding rod-hole coupon.
- `CON-013`: For every rod and state, the left and right outer slot transforms
  must reconstruct the same world `YZ` rod center on the fixed guide line; rod
  skew must be zero within CAD tolerance.
- `CON-014`: The center axle central larger hex spacer length equals the
  fixed-inner clear span and its axial shoulders seat the two inner plates.
- `CON-015`: Smaller hex key sections pass through matching fixed-inner hex
  bores. Hex is selected over square because it gives positive indexing with
  more contact flats, lower PETG corner stress, and easier angular alignment.
- `CON-016`: The center axle crosses the inner span and must be checked as an
  actual solid against XT60 body, wire, soldering, release, and completed
  pigtail removal envelopes.
- `CON-017`: Thin outer keepers retain the center-axle/plate stack axially but
  must leave named running clearance so outer plates rotate freely.
- `CON-018`: The round journal OD must be smaller than the fixed-inner hex
  bore's inscribed diameter. For a regular hex bore, the inscribed diameter is
  the across-flats dimension, so `outer_journal_diameter <
  fixed_inner_hex_bore_af`.
- `CON-019`: P17-D03 coherent provisional defaults are:
  `center_axle_central_hex_af = 10.00 mm`,
  `center_axle_inner_hex_key_af = 8.00 mm`,
  `fixed_inner_hex_bore_af = 8.15 mm`,
  `outer_journal_diameter = 7.60 mm`,
  `outer_bearing_bore_diameter = 7.90 mm`,
  `outer_journal_clearance_diametral = 0.30 mm`,
  `keeper_seat_length = 1.20 mm`,
  `outer_keeper_thickness = 1.20 mm`, and
  `keeper_axial_running_clearance = 0.25 mm`, subject to named print
  clearances and minimum wall checks.
- `CON-020`: Per side, the center axle segment after the central shoulder is
  the inner hex key through the full fixed-inner plate thickness, followed by a
  round section spanning the inner/outer running gap, full outer plate
  thickness, keeper axial running clearance, and the actual retained keeper
  seat.
- `CON-021`: The axle solid must extend under the keeper. Each keeper must be a
  modeled retained feature such as a permanent press-fit ring on a real
  seat/groove or a modeled split/groove keeper with insertion and retention
  geometry.
- `CON-022`: The outer bearing bore is derived from round journal OD plus named
  diametral running clearance; it must not be derived from the fixed-inner hex
  key AF.
- `CON-023`: P17-D02's provisional center-axle numeric table is superseded
  inside P17 R2 wherever it conflicts with `CON-018` through `CON-022`.
- `CON-024`: P17-D06 separates two world `YZ` datums. The existing outer
  rotation center remains `C = (-10.60, 17.00) mm`; the fixed stepped-axle
  center is corrected by P17-D07 to `A = (-29.00, 17.00) mm`. The default
  eccentricity is `e = |A - C| = 18.40 mm`. D06's provisional
  `A=(-18.00,17.00)` / `e=7.40` is rejected as geometrically infeasible.
- `CON-025`: With normalized travel `t in [0,1]`, `theta = 32 deg * t`,
  `alpha_left = -theta`, and `alpha_right = +theta`. The fixed-axle guide
  centerline in each outer plate's local `YZ` frame is
  `q_s(theta) = R(-alpha_s(theta)) * (A - C)`. Reconstruction must satisfy
  `C + R(alpha_s(theta)) * q_s(theta) = A` within `0.05 mm` at open, mid,
  locked, and intermediate samples.
- `CON-026`: The dedicated axle-guide slot width defaults to
  `fixed_axle_guide_slot_width = outer_journal_diameter + 0.30 mm = 7.90 mm`.
  It is a continuous swept arc over `0..32 deg` with closed capsule ends and
  at least 33 centerline samples. The left and right local loci are mirror
  images, not one copied same-direction slot.
- `CON-027`: The axle, both inner plates, their hex bores, and both keepers
  have identical world transforms for every review state. Only the two outer
  plate occurrences receive viewer-time rotations about `C`.
- `CON-028`: The centered outer bearing bore at `C` is not retained as an
  empty or decorative hole in the focused geometry. A future integral
  pivot boss/bore at `C` requires an explicit design decision; this design
  relies on the unchanged existing rod/slot network for eventual mechanism
  closure and keeps that closure claim pending independent validation.
- `CON-029`: At the D07 datum, analytic minimum web to the frozen feature set
  must be at least `2.20 mm`; the selected scan result is `3.849 mm`. Exact
  BREP cutter/feature distance must also be at least `2.20 mm`; the selected
  result is `3.650 mm`. Inner, left-outer, and right-outer boundary webs are
  respectively `3.8946`, `7.650`, and `9.150 mm`.
- `CON-030`: Across 33 samples from `0..32 deg`, axle/outer,
  keeper/outer, axle/white-rod, and keeper/cap unintended intersection volumes
  must remain zero. Nominal diametral axle-guide clearance is `0.30 mm`
  (`0.15 mm` radial), and the `OD10.00 mm` keeper over a `7.90 mm` slot gives
  `1.05 mm` radial axial-capture overlap; physical retention remains pending.

## Active P17 R2 design choices

- `CHOICE-004`: P17 R2 uses two-hand direct counter-twist rather than a geared
  or linked synchronizer.
- `CHOICE-005`: The right outer plate is the primary force/actuator side
  because it carries the larger grip/lever affordance and endpoint lock.
- `CHOICE-006`: Initial P17 R2 defaults use `48.00 mm` inner plates, `56.00 mm`
  left secondary outer plate, and `60.00 mm` right primary outer plate; these
  are P17 R2 design choices, not inherited P17 R1 simulator numbers.
- `CHOICE-007`: Initial permanent-cap CAD default is a separate coupon-driven
  socket strategy, provisionally around `4.04 mm` socket ID and `4.00 mm`
  engagement, pending physical coupon proof.
- `CHOICE-008`: P17-D02 selects a one-piece stepped center axle instead of
  three yoke/stability bars or a yoke socket/tenon frame.
- `CHOICE-009`: Initial center-axle defaults are central hex spacer across
  flats `8.00 mm`, inner key hex across flats `6.00 mm`, outer journal diameter
  `8.00 mm`, diametral journal clearance `0.30 mm`, keeper thickness
  `1.00 mm`, and keeper running clearance `0.25 mm`. Superseded by P17-D03
  because the `AF6` / `OD8` slide-over path is impossible.
- `CHOICE-010`: P17-D03 uses coherent provisional center-axle defaults from
  `CON-019` and a permanent press-fit keeper ring on a real end seat/groove as
  the smallest responsible retained-keeper strategy. Keeper retention remains
  physically gated.
- `CHOICE-011`: P17-D08 preserves the larger right primary actuator for force
  affordance but removes its current endpoint lock. Internal legacy endpoint
  names may remain narrowly for generation compatibility; user-visible motion
  wording must say `open_to_end` and must not imply self-lock.

## Active P17 R2 non-goals

- `NON-GOAL-006`: Repairing or continuing the P17 simulator.
- `NON-GOAL-007`: Claiming physical lock force, self-lock, retention, heat,
  wear, vibration, wire holding force, or springback from CAD evidence.
- `NON-GOAL-008`: Preserving P13 rod length, cap interference, or locked-pose
  assumptions without re-derivation.
- `NON-GOAL-009`: Adding yoke/stability bars, yoke sockets, or yoke tenons to
  P17 R2.

## Active P17 R2 physical unknowns

- `PHYS-007`: Permanent cap installation force, retention, cracking, wear, and
  thermal response.
- `PHYS-008`: Plastic-on-plastic hub friction, backlash, wear, and creep.
- `PHYS-009`: Center-axle hex fit, shoulder seating, keeper retention,
  keeper installation force, journal friction, stiffness, and real hand/bench
  reaction behavior.
- `PHYS-010`: Lock detent force, self-lock, vibration resistance, release
  effort, and thermal creep.
- `PHYS-011`: Wire holding force, insulation marking, soldering heat exposure,
  cooled bend angle, and springback.
- `PHYS-012`: Exact best rod length for the re-derived stack and cap
  engagement.
- `PHYS-013`: A future endpoint retention architecture and its force,
  back-drive, release, vibration, heat, creep, and wear behavior remain
  unselected after P17-D08 removes the current lock.

## Active P17 R2 evidence mapping

| IDs | Evidence | Status |
|---|---|---|
| `REQ-009`–`REQ-021`, `CON-008`–`CON-023` | `docs/iterations/p17-r2-direct-cad-counter-twist/BRIEF.md`, `DESIGN.md`, `ADR-0003` | prior design contract; P17-I04 visually rejected |
| `REQ-022`–`REQ-025`, `CON-024`–`CON-030` | `docs/iterations/p17-r2-fixed-reaction-rod-motion/BRIEF.md`, `DESIGN.md`, supplied Viewer screenshots, D07 BREP search evidence | active D07 focused repair contract |
| `REQ-026`, `CHOICE-011`, `PHYS-013` | `docs/iterations/p17-r2-lock-removal/BRIEF.md`, `DESIGN.md`, two supplied annotated Viewer screenshots | P17-D08 design complete; implementation pending |
| `REQ-009`–`REQ-025` | Future repaired P17 R2 source, tests, STEP/artifact validation, critic, and formal review | pending |
| `REQ-013`, `REQ-014`, `PHYS-007` | Future permanent-cap coupon | pending physical |
| `PHYS-008`–`PHYS-012` | Future PETG assembly and use tests | pending physical |
