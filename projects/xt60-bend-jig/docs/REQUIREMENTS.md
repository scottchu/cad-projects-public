# XT60 bend jig requirements and design contract

## Active P18 R1 compact counter-twist baseline

The user approved the P17 compact 2D gate and explicitly opened **P18 R1** on
`2026-08-26`. P18 preserves the four-plate, three-rod, one-stepped-axle
architecture and the accepted workpiece-relative topology, but changes the
product envelope, fixed-axle datum and total twist travel together. P17 remains
immutable history and input evidence; P18 is the active forward baseline.

- `REQ-031`: FRONT is world YZ: `+Z` is XT60 mating-head/up and `+Y` is the
  solder tail and both wires outward/right. Camera pose may not redefine it.
- `REQ-032`: OPEN remains upper-left -> upper-right -> lower-right with the two
  right rods on one exact vertical leg. END remains upper-left -> middle ->
  lower-right on the accepted diagonal. Rod identities never swap, cross,
  mirror or reverse.
- `REQ-033`: P18 uses three uncut `OD4.00 x 50.00 mm` stainless rods, six
  permanent caps, four plates and one one-piece stepped axle. No stability
  bar, yoke, linkage, gear, grip block or replacement lock is authorized.
- `REQ-034`: Both inner plates and the stepped axle are fixed. The two outer
  plates are hand-operated and counter-rotate by equal and opposite angles;
  the right force plate is slightly larger than the left outer plate.
- `REQ-035`: Fixed-inner rod tracks are straight. Every outer rod rail and
  both fixed-axle rails are deterministically inverse-transform-derived from
  one normalized motion parameter. Plate-owned holes/rails never animate
  independently.
- `REQ-036`: The virtual outer rotation datum `C` is not a centered pivot bore
  or physical member. The existing rod/slot/axle contact network supplies the
  prescribed CAD constraint; CAD motion is not a force or self-lock proof.
- `REQ-037`: P18 remains parametric STEP-first CAD. Source, tests, STEP,
  sidecar and snapshots are separate from mesh/slicer and physical evidence.
- `REQ-038`: END means prescribed clamped geometry only. It carries no
  hard-stop, detent, retention, over-center or self-lock claim.
- `REQ-039`: P18 must preserve loading, wire-only forming, cooling, extraction
  direction and completed-pigtail removal without using the XT60 body as the
  reaction load path.
- `REQ-040`: Full-assembly soldering-iron clearance is not digitally accepted
  in P18 R1 and remains a required service/physical gate.

### P18 R1 numeric and derived constraints

- `CON-031`: `theta_end=45 deg`, `alpha_left=-45u`,
  `alpha_right=+45u`, `u in [0,1]`.
- `CON-032`: `C=(0,0) mm`, fixed axle `A=(-9.5,-9.5) mm`, and accepted rigid
  placement `S=(-14.6869657526,-12.2949747468) mm` in FRONT YZ.
- `CON-033`: Plate diameters are inner `52.933 mm`, left outer `53.933 mm`
  and right force outer `54.933 mm`; required exact material web is
  `>=2.20 mm`.
- `CON-034`: Common stroke is `10.5852813742 mm`, geometric preload remains
  `0.25 mm`, `u_contact=0.976382299991634`, and
  `theta_contact=43.9372034996235 deg`.
- `CON-035`: Inner clear span is `18.40 mm`; principal plate stack is
  `32.00 mm`; cap engagement is `8.70 mm` per side; rod length is exactly
  `50.00 mm`.
- `CON-036`: The one-piece axle retains AF10 central spacer, AF8 keys, exact
  AF8.15 inner bores, OD7.60 journals, 7.90 mm outer running guides/bore and
  retained OD10/bore7.55 keepers. Total axle length is `34.90 mm`.
- `CON-037`: The AF8.15 bore is an actual regular hex; its circumradius is
  `8.15/sqrt(3)=4.705404693895 mm`. `AF/2` is not a radial-clearance proxy.
- `CON-038`: Dense four-contact closure must retain rank `3`, finite recorded
  conditioning, continuous rail branches and two-sided rod support throughout
  OPEN-to-END.
- `CON-039`: Actual-solid unintended intersections are zero except the named
  END wire preload allow-list; completed-pigtail removal clearance is at least
  `0.75 mm`.
- `CON-040`: The near-tangent diagonal rail interval remains a physical
  hand-force/friction/wedging/backlash risk even when the digital constraint
  and support gates pass.

### P18 R1 choices, non-goals and physical unknowns

- `CHOICE-012`: P18 R1 selects the accepted compact 45-degree candidate with
  a slightly larger right force plate and no added grip feature.
- `NON-GOAL-010`: Claiming full solder-tool access, acceptable hand torque,
  smoothness, retention, fit, heat, wear, back-drive or self-lock from CAD.
- `PHYS-014`: Hand force, friction, wedging, backlash and back-drive through
  the near-tangent portion of the 45-degree travel.
- `PHYS-015`: Full assembled soldering-iron access to both joints.
- `PHYS-016`: Permanent cap and keeper installation/retention and axle/hex fit.
- `PHYS-017`: Limiting-web robustness, PETG dimensional outcome, heat and wear.
- `PHYS-018`: Whether the `0.50 mm` force-side radius advantage is useful by
  hand without an added grip feature.
- `CON-041`: The next physical correction requires exactly `28.40 mm` clear
  span between the fixed inner plates, `10.00 mm` wider than P20 R4.
- `CON-042`: Preserve the purchased three `OD4.00 x 50.00 mm` stainless rods
  and the `0.30 mm` cap-to-outer gap. The printed stepped axle becomes
  `44.90 mm`; the wider stack leaves `3.70 mm` available cap engagement per
  side, pending physical retention validation.
- `CON-043`: Permanent cap distal socket is `ID4.10 mm` on nominal `OD4.00 mm`
  stock; actual installation force and retention remain a physical gate.
- `PHYS-019`: Confirm the reprinted cap is looser but still retained, and that
  the assembled fixed-inner clear span is usable; this does not close other
  physical defects.

## Active P24 R1 manual three-slider clamp contract

- `REQ-044`: The three purchased rods remain exactly `OD4.00 x 50.00 mm` and
  retain their inherited identities, paths and rails. P24 uses zero legacy
  permanent caps.
- `REQ-045`: The user alone creates mechanism motion: thumb pushes Orange
  DOWN; index and middle fingers push Blue and Green BACK-to-FRONT. All three
  are independent manual inputs.
- `REQ-046`: The new clamp acts only after all three rods reach inherited END.
  Clamp progress may move only pressure/screw geometry along X and may never
  change rod or shoe YZ centers.
- `REQ-047`: Each axial side uses three independent floating socket shoes,
  one common pressure plate, one reaction frame and one captive central screw.
  No shared shoe carrier may steer or synchronize the three rods.
- `REQ-048`: The conceptual screw must close both endpoint loops: head-to-plate
  compression for CLAMPED and captive-retainer-to-plate pull-back for RELEASED,
  with frame reaction and no positive-volume penetration.
- `CON-044`: Preserve `3.70 mm` nominal shoe engagement, `ID4.20 mm` sockets,
  `0.60 mm` pressure-plate travel, `0.30 mm` inactive captive endplay and at
  least `5.00 mm` finger-stem exposure.
- `NON-GOAL-011`: P24 R1 does not prove a helical thread, torque, preload,
  holding force, equal load sharing, anti-jam release, manufacturability,
  printability or physical acceptance.
- `PHYS-020`: Resolve the inherited OPEN Blue/XT60 collision and then validate
  real thread/fit, holding, two-side tightening, shoe rattle/cocking, release,
  assembly and service paths before any print-candidate claim.

P18 R1 evidence authority is
`docs/iterations/p18-r1-compact-counter-twist/`; its formal review accepts
the frozen CAD and six STEP artifacts only. Mesh, 3MF, slicing, printing and
physical acceptance remain pending.

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

P17-D09-R1 supersedes the frozen-rod-path and provisional rod-length portions
of D08 for the active candidate. All three stainless rods are now explicitly
`OD4.00 x 50.00 mm`; numeric OPEN, first-contact, and END triangles are
defined together; fixed-inner rod tracks are straight; the two outer plates
counter-rotate through inverse-transform-derived side-local rails; and the
right force side remains larger. The green grip and obsolete service window
are removed. The purple axle stays fixed at `A=(-29,17)`. No stability bar,
yoke, linkage, gear, replacement lock, or self-lock claim is authorized. This
focused mechanism repair remains P17 R2.

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
- `REQ-027`: P17 workpiece orientation uses a workpiece-relative front frame,
  independent of Viewer camera pose: `+Z` is XT60 mating-head/up and `+Y` is
  solder-tail/both-wires/right. This frame may not be mirrored, reversed, or
  reinterpreted by camera orientation without explicit design reopening.
- `REQ-028`: OPEN/UNLOCKED rod topology is upper-left, upper-right, and
  lower-right, with upper-right and lower-right on one exact right vertical
  leg. These are outward/retracted positions of the same three rod identities
  along their contact normals. Rod roles may not swap or cross; both fixed
  inner plates use direct stationary straight guide lines.
- `REQ-029`: CLAMPED/END rod topology converges upper-left -> middle ->
  lower-right on one diagonal. The middle rod addresses the bend arc and the
  two end rods address the two straight-leg contact features, creating a
  three-point wire wrap while XT60 plastic is absent from the reaction/load
  path. These functional roles survive later numeric refinement.
- `REQ-030`: “Locked” is only colloquial shorthand for CLAMPED/END geometry.
  It carries no hard-stop, retention, detent, over-center, or self-lock claim.
  Requirements `REQ-027` through `REQ-030` may not be mirrored or reversed by
  a numeric refinement; that requires explicit design reopening.

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
| `TRI-REQ-01`–`TRI-REQ-10` | `docs/iterations/p17-r2-three-rod-triangle-motion/BRIEF.md`, `DESIGN.md`, P17-I07-R1 source/tests/artifacts, `REVIEW.md`, `VALIDATION.md` | P17-R07 digitally accepted |
| `REQ-009`–`REQ-026` | P17-I07-R1 source, tests, ten STEP exports, frozen visuals, P17-C07/P17-V07/P17-R07 | accepted for digital CAD/export/Viewer readiness |
| `REQ-013`, `REQ-014`, `PHYS-007` | Future permanent-cap coupon | pending physical |
| `PHYS-008`–`PHYS-012` | Future PETG assembly and use tests | pending physical |
