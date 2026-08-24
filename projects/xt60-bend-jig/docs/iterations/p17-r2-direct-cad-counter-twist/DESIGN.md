# P17 R2 direct-CAD counter-twist design contract

Status: selected design candidate for implementation. `P17-D05` did not
implement, validate, critique, or approve CAD/source/artifacts.

Version correction: this is revision R2 of the P17 counter-twist product
design. The rejected P17 R1 simulator remains historical evidence, but its
failure does not create a new product-design `P` version.

## Coordinate system

- Units: millimeters.
- Assembly origin: center of the XT60 body envelope between the two fixed inner
  plates.
- `+X`: axial direction of rods and plate stack, left-to-right through the jig.
- `YZ`: motion/forming plane.
- `+Y`: horizontal wire-lead direction away from the XT60 body.
- `+Z`: upward from the bend plane.
- Outer plates rotate about local/world X axes. Inner plates are grounded by
  the stepped center axle and have zero rotation in every state.

All moving slots and holes are part-local geometry. Their world pose must be
derived from the actual solid occurrence transform. Fixed guide slots are fixed
geometry and must not move between open, mid, and locked STEP states.

## Architecture alternatives

### A1: two-hand direct counter-twist with rods as synchronizing followers

Each side has one fixed inner guide plate and one adjacent hand-operated outer
cam plate. A one-piece stepped center axle spans the assembly: a larger central
hex spacer sets the fixed-inner clear span and provides axial shoulders, two
smaller hex key sections pass through matching fixed-inner hex bores, and two
outer round journal sections support the independently rotating outer plates.
The axle grounds/supports the inner plates only; it does not couple the outer
plates. The user directly twists both outer plates by hand in opposite
directions. Three rigid rods span the jig; each rod's two end followers/caps
ride in complementary physical slots on the two outer plates while the rod also
passes through fixed straight guide slots in both inner plates. The fixed slots
define the allowed world `YZ` guide lines; the outer slots are
inverse-generated from those guide lines under the left/right plate rotations.

Kinematic proof sketch:

- Let rod `i` have desired world center `r_i(theta)` on a fixed guide line
  `L_i`, with `theta = 0` open and `theta = theta_lock` locked.
- Left outer rotation is `alpha_L = -theta`; right outer rotation is
  `alpha_R = +theta`.
- The left slot locus is the set
  `slot_L_i(theta) = R_x(-alpha_L(theta)) * (r_i(theta) - hub_L)`.
- The right slot locus is the set
  `slot_R_i(theta) = R_x(-alpha_R(theta)) * (r_i(theta) - hub_R)`.
- In generated STEP states, the actual world follower center is
  `hub_s + R_x(alpha_s(theta)) * slot_s_i(theta)`, which reconstructs the same
  `r_i(theta)` for both sides. This is a physical slot construction, not a
  scene-only sign flip.
- Because the rod is rigid and both ends reconstruct the same `YZ` point, rod
  skew should be zero within CAD tolerance. If the generated solids show skew,
  the candidate fails.

Disposition: selected. It is the smallest responsible CAD candidate because it
uses the user's real two-hand twist, keeps fixed inner geometry truly fixed,
avoids designing gears before the basic geometry is proven, and turns the
moving-hole/slot complaint into explicit part-local/world-transform tests.

### A2: grounded bevel/idler or differential linkage

A grounded carrier with bevel or spur/idler elements links the two outer plates
1:1 in opposite directions. This can reduce user coordination to one primary
input, but it introduces gear tooth geometry, bearing axes, carrier stiffness,
extra collision envelopes, backlash, printable tooth quality, lubrication/wear,
and a separate failure mode before the rod guide architecture is proven.

Disposition: rejected for P17 R2. Mechanically plausible, but not the smallest
responsible next CAD candidate. It remains a later option if two-hand direct
operation proves ergonomically unacceptable or if left/right synchronization
cannot be achieved through the rods and slots.

### A3: crossed links or equalizer between outer plates

Cross-links or bellcranks can enforce opposite rotation while keeping plate
slots simpler. The links need pivots, keepers, clearances outside the
soldering/removal envelope, and a stiffness/load path that may conflict with
the XT60 body and wires.

Disposition: rejected for P17 R2. Plausible but adds link hardware and service
constraints while the physical observations point first to axial span, rods,
caps, fixed/moving role confusion, and lock proof.

### A4: same-direction central D shaft with mirrored visualization

One shaft rotates both outer plates together and software or mirrored slot
drawings make the apparent motion look counter-twisted.

Disposition: rejected. It repeats the P13/P17 failure mode: a shared
same-direction shaft and/or scene-only sign flip cannot satisfy the user's
opposite hand-twist requirement.

## Selected CAD candidate

Use architecture A1: a two-hand direct counter-twist, four-principal-plate,
three-rigid-rod mechanism with grounded inner plates fixed by a one-piece
stepped center axle, six permanent rod-end follower caps, thin outer keepers,
and a right-side primary endpoint lock. Do not add three yoke/stability bars,
yoke socket features, or yoke tenons.

### Part roles and counts

Production parts:

- `left_inner_fixed_guide`: fixed PETG inner guide plate with hub/bearing boss,
  straight guide slots, a matching smaller-hex axle bore, and fixed
  lock/reaction features where needed.
- `right_inner_fixed_guide`: fixed PETG inner guide plate with hub/bearing boss,
  straight guide slots, a matching smaller-hex axle bore, and the grounded
  hard-stop/detent receiver for the primary right outer plate.
- `stepped_center_axle`: one-piece center bar/axle with a larger central hex
  spacer, two smaller hex key sections through the inner plates, two round
  outer journal sections for independent outer-plate rotation, and keeper
  grooves or shoulders. It sets the fixed-inner clear span and grounds the two
  inner plates without coupling either outer plate's rotation.
- `left_outer_secondary_cam`: hand-operated outer plate on the left inner hub,
  counter-rotating in the negative direction. It is larger than the inner
  plates but smaller than the primary side.
- `right_outer_primary_actuator`: hand-operated outer plate on the right inner
  hub, rotating in the positive direction. It has the larger grip/lever
  affordance and carries the endpoint lock lug/thumb release geometry.
- Three `OD4.00` stainless rods, length derived for P17 R2 rather than frozen to
  `50.00 mm`.
- Six permanent rod-end follower caps, one on each rod end. No cap is removable
  for service.
- Two thin outer keepers or keeper clips on the center axle, outside the outer
  plates, retaining the axial stack while preserving journal clearance.

Reference-only parts:

- XT60 body envelope, insulated wire envelopes, soldering iron keep-out, bend
  path, and removal sweeps. These are validation geometry, not production
  printed parts.

### Plate and center-axle support architecture

- The two inner plates are fixed to the stepped center axle and never rotate.
- The larger central hex spacer sets the inner clear span. Its left and right
  shoulder faces seat the inner faces of the two fixed inner plates.
- Smaller hex key sections pass through matching fixed-inner hex bores. They
  prevent inner-plate rotation and set angular alignment of fixed guide slots.
- Each outer plate is independently supported on its adjacent round journal
  section by a coaxial plastic-on-plastic bearing around the X axis.
- Thin outer keepers retain the stack axially outside the outer plates. They
  must not clamp the outer plates tightly; named axial clearance is required.
- The assembly order requires each fixed inner plate to slide over the outer
  round axle section before seating on the inner hex key. Therefore the round
  journal OD must be smaller than the fixed-inner hex bore's inscribed
  diameter, which for a regular hex bore is its across-flats dimension.
- There is no common D shaft between the two outer plates.
- There is no keyed or flat coupling between the center axle and either outer
  plate. The center axle grounds/supports the inner plates only.
- Source should express each outer plate as a separate revolute occurrence:
  `alpha_left(theta) = -theta`, `alpha_right(theta) = +theta`.
- Bearing/hub datums:
  - axle axis: world X through assembly origin unless implementation proves a
    better derived pivot is needed;
  - central hex spacer shoulder faces: fixed-inner span datums;
  - smaller hex key sections: fixed-inner rotational datums;
  - round journal sections: outer-plate revolute datums;
  - outer cam bearing bores: part-local round bores centered on the same axis;
  - axial running gaps: named parameters, not hidden literals.

Hex is selected over square for the fixed-inner key sections. A hex key gives
positive angular indexing like a square, but its 120-degree included corners
and six contact flats distribute bearing stress more gently in PETG than a
four-corner square key. It also gives more orientation choices for aligning
fixed guide-slot phases while avoiding the high corner stress and print-fit
sensitivity of square internal corners. Round bores are used only for the
outer plates, where rotation is required.

P17-D03 numeric correction: the P17-D02 provisional defaults
`center_axle_inner_hex_af = 6.00 mm` with `outer_journal_diameter = 8.00 mm`
are superseded inside P17 R2 because an `OD8` round journal cannot pass through
an `AF6` hex bore. Future implementation must preserve the slide-over assembly
invariant:

```text
outer_journal_diameter
  < fixed_inner_hex_bore_inscribed_diameter
  = fixed_inner_hex_bore_af
```

P17-D04 repair correction: the shared stepped pivot does not need to remain at
the XT60/jig geometric center. The repair must prefer an offset shared pivot
behind the XT60 connector body, opposite the `+Y` wire-exit/solder side,
provided all fixed guide lines and rotating outer cam slots are recalculated
around that new pivot. Do not translate the axle alone. The center axle, inner
hex bores, outer round bearing bores, fixed guide slots, outer cam slots, lock
stop/detent geometry, and snapshots must all use the same named pivot datum.

Coordinate/use orientation for P17-D04:

- `+Y` remains the outgoing-wire and solder-joint side.
- `-Y` is the behind-connector side.
- The stepped axle/keeper centerline must be behind the XT60 body on `-Y` and
  its pivot `Z` must stay inside the XT60 body's body-height projection in
  locked state.
- P17-D05 clarifies the user's "behind the XT60" intent: the pivot centerline
  must sit behind the body on `-Y`; the full X-spanning axle and outer keepers
  are not required to fit inside the XT60 body's narrow `X` width projection,
  because that would contradict the four-plate stack. Validation must not fail
  a candidate merely because `axle_bbox_x` or keeper `X` extents exceed the
  connector body width.
- The axle and keepers must have zero actual-solid intersection with the XT60
  body, solder joints, wires, heat-shrink, soldering-tool, release, and
  completed-pigtail service envelopes from open through locked.
- Minimum positive CAD clearance target from axle/keeper actual solids to those
  service envelopes is `0.75 mm`; values below `0.75 mm` require explicit
  design review before implementation handoff.

P17-D04 also rejects the current P17-I02 slot widths and cam-slot construction:
`fixed_slot_width = 4.90 mm` and `outer_slot_width = 7.55 mm` are too loose for
`OD4.00 mm` stainless rods and create visible nonfunctional bulk. Future CAD
must not use an oversized straight endpoint capsule as the cam slot. For every
rod, derive the actual continuous cam centerline/swept locus under the offset
shared pivot and cut a narrow curved slot around that centerline.

### Rod motion and complementary slot construction

Use three rod roles from the supported outcome, but re-derive their exact guide
lines:

- `upright_forming_rod`: shapes the vertical leg of the 90-degree bend.
- `bottom_support_rod`: supports the horizontal leg without loading XT60
  plastic.
- `diagonal_forming_rod`: drives the corner/bend transition.

For each rod, implementation must define:

- fixed guide line `L_i` in world `YZ`;
- open center `r_i(0)`;
- locked center `r_i(theta_lock)`;
- monotonic scalar travel `u_i(theta)` along `L_i`;
- follower radius and clearance;
- left and right outer slot loci generated by inverse transform from actual
  left/right rotations.

The implementation may start with the P13 role concepts for which rod forms,
supports, or locks the wire, but it must not copy P13 or P17 R1 simulator
numeric paths without derivation against the P17 R2 span, stack, lock, and
fixed-inner/outer-counter-twist constraints.

### Axial span and rod-length derivation

P13's `26.2 mm` inner clear span is rejected as excessive. P17 R2 derives the
inner clear span from the XT60 body width and side clearance:

```text
xt60_body_width_x = 15.90 mm        invariant from physical requirement
xt60_side_clearance_each = 1.25 mm  design choice, initial CAD default
inner_clear_span = xt60_body_width_x + 2 * xt60_side_clearance_each
                 = 18.40 mm
```

`18.40 mm` is a P17 R2 design choice derived from the XT60 envelope and a named
clearance. It is not inherited from P17 R1's rejected `18.5 mm` simulator
number.
Valid range for implementation exploration: `17.90..19.50 mm`, with the lower
bound preserving at least `1.00 mm` side clearance per side and the upper bound
still reducing P13's surplus by more than half.

Provisional axial and center-axle defaults:

| Parameter | Class | Default | Range / rule |
|---|---|---:|---|
| `xt60_body_width_x` | invariant | `15.90` | measured requirement |
| `xt60_side_clearance_each` | design choice | `1.25` | `1.00..1.80` |
| `inner_clear_span` | derived constraint | `18.40` | computed |
| `inner_plate_thickness` | design choice | `3.20` | `3.00..3.60` |
| `outer_plate_thickness` | design choice | `3.20` | `3.00..3.80` |
| `inner_outer_running_gap` | physical unknown/design choice | `0.40` | `0.30..0.60`; printed rubbing pending |
| `cap_to_outer_running_gap` | physical unknown/design choice | `0.30` | `0.20..0.60` |
| `cap_rod_engagement` | physical unknown/design choice | `4.00` | coupon must test `3.50..4.50` |
| `center_axle_central_hex_af` | design choice | `10.00` | must clear XT60/wires; validate actual solids |
| `center_axle_inner_hex_key_af` | design choice | `8.00` | enough PETG web around inner bore |
| `fixed_inner_hex_bore_af` | physical unknown/design choice | `8.15` | must exceed key AF by named print clearance |
| `inner_hex_key_clearance_af` | physical unknown/design choice | `0.15` | `0.10..0.25`; coupon/fit pending |
| `outer_journal_diameter` | derived/design choice | `7.60` | must be `< fixed_inner_hex_bore_af`; bearing fit pending |
| `outer_bearing_bore_diameter` | physical unknown/design choice | `7.90` | derived from journal plus diametral clearance |
| `outer_journal_clearance_diametral` | physical unknown/design choice | `0.30` | `0.20..0.45` |
| `keeper_seat_length` | design choice | `1.20` | `1.00..1.60`; axle solid under keeper |
| `outer_keeper_thickness` | design choice | `1.20` | `1.00..1.60`; retained on actual seat/groove |
| `outer_keeper_outer_diameter` | design choice | `10.00` | D05 minimum print-ready default; see keeper wall repair below |
| `keeper_bore_diameter` | physical unknown/design choice | `7.55` | default `0.05 mm` diametral retention on `OD7.60` journal; coupon gated |
| `keeper_retention_interference_diametral` | physical unknown/design choice | `0.05` | coupon ladder must include `0.00,0.05,0.10`; no physical acceptance claim |
| `keeper_radial_wall_min` | derived DfAM check | `1.20` | minimum PETG wall at any retained keeper lobe after relief cuts |
| `keeper_axial_running_clearance` | physical unknown/design choice | `0.25` | `0.15..0.40` |
| `rod_length_target` | derived constraint | `40.60` | round formula below to a manufacturable length |
| `pivot_y` | design choice | `-10.60` | behind XT60 body, opposite `+Y` wire-exit side |
| `pivot_z` | design choice | `17.00` | inside XT60 body `XZ` shadow; clear service envelopes |
| `inner_plate_diameter` | design choice | `54.00` | resized only as needed for offset guide slots |
| `left_outer_secondary_grip_diameter` | design choice | `60.00` | must remain larger than inner plate |
| `right_outer_primary_grip_diameter` | design choice | `63.00` | quantified larger primary lever affordance |
| `fixed_slot_width` | physical unknown/design choice | `4.20` | replaces rejected `4.90`; slot-fit coupon gated |
| `outer_cam_slot_width` | physical unknown/design choice | `4.20` | replaces rejected `7.55`; slot-fit coupon gated |
| `slot_fit_coupon_widths` | physical unknown | `4.10,4.15,4.20,4.25,4.30` | straight and curved coupons for `OD4.00` rod |
| `slot_center_slop_nominal` | derived check | `±0.10` | `(4.20 - 4.00) / 2`; physical proof pending |

Rod-length formula:

```text
principal_stack_width =
  inner_clear_span
  + 2 * inner_plate_thickness
  + 2 * outer_plate_thickness
  + 2 * inner_outer_running_gap

rod_length_raw =
  principal_stack_width
  + 2 * cap_to_outer_running_gap
  + 2 * cap_rod_engagement

default =
  18.40 + 6.40 + 6.40 + 0.80 + 0.60 + 8.00
  = 40.60 mm
```

Center-axle stack formula:

```text
central_hex_length = inner_clear_span

per_side_center_axle_length =
  inner_plate_thickness
  + inner_outer_running_gap
  + outer_plate_thickness
  + keeper_axial_running_clearance
  + keeper_seat_length

center_axle_total_length =
  central_hex_length
  + 2 * per_side_center_axle_length

default =
  18.40 + 2 * (3.20 + 0.40 + 3.20 + 0.25 + 1.20)
  = 34.90 mm
```

Implementation should choose either a `40.60 mm` rod cut length or a nearby
standard/cut target after checking cap socket depth and plate stack
clearances. The center axle is a separate printed/mechanical element with a
default total length near `34.90 mm`; do not confuse it with the three rods.
The old `50.00 mm` rod freeze is not accepted for P17 R2 because it directly
conflicts with the photo-observed protrusion and reduced span.

Per side, the center axle must be segmented in this order:

```text
central spacer shoulder
→ inner hex key through the full fixed-inner plate thickness
→ round journal spanning the inner/outer running gap
  + full outer plate thickness
  + keeper axial running clearance
  + actual retained keeper seat
```

The round journal/seat is not allowed to stop at the outer plate face. The axle
solid must extend under the keeper so the keeper has real retained geometry.
The provisional keeper strategy is a permanent press-fit end ring captured on
a modeled end seat with a shallow retention groove or bead. A split/groove
keeper may replace it only if implementation models the groove, insertion
path, retention geometry, and minimum remaining axle wall. A floating ring
with no positive seat, groove, interference, or retention feature fails P17 R2.

P17-D05 keeper DfAM repair: the P17-I03 implementation used an annular keeper
with `outer_keeper_outer_diameter = outer_journal_diameter + 1.00 = 8.60 mm`
and `keeper_bore_diameter = 7.50 mm`, leaving only `0.55 mm` radial wall. That
is a digital print-readiness blocker for PETG. The smallest within-architecture
repair is to keep the two thin axial keepers but raise their retained-wall
default to:

```text
outer_journal_diameter = 7.60 mm
keeper_bore_diameter = 7.55 mm
outer_keeper_outer_diameter = 10.00 mm
keeper_radial_wall = (10.00 - 7.55) / 2 = 1.225 mm
```

The keeper must still be an actual retained geometry on the axle seat. If the
larger keeper OD reintroduces rod/cap/service collisions, implementation may
add local flats or scalloped reliefs on non-retention quadrants, but at least
two opposed retention lobes must preserve `keeper_radial_wall_min >= 1.20 mm`
and the candidate must rerun rod/cap/keeper/service collision checks. Physical
retention remains gated by a keeper coupon; CAD may only claim print-readiness
for wall and clearance geometry, not press-fit acceptance.

### Plate diameters and grip affordance

Use grip affordance, not inherited P17 diameters:

| Feature | Class | Default |
|---|---|---:|
| `inner_plate_diameter` | design choice | `48.00 mm` |
| `left_outer_secondary_grip_diameter` | design choice | `56.00 mm` |
| `right_outer_primary_grip_diameter` | design choice | `60.00 mm` |
| `right_primary_extra_lever_radius` | derived/design check | `(60 - 56) / 2 = 2.00 mm` |

Rationale: both outer plates exceed the inner plates for grip. The right side
is the primary force/actuator side because it carries the lock lug, thumb
release affordance, and larger lever radius; its larger diameter gives a
quantitative `2.00 mm` greater radius than the left outer side. Implementation
may replace diameter delta with an equal-or-better thumb tab, but must preserve
a quantified larger right-side grip/lever affordance.

### Permanent cap and follower strategy

All six caps are permanent rod-end follower heads. Do not use left/right
removable-service language.

Provisional strategy:

- Use a blind cylindrical rod socket with a lead-in chamfer and a controlled
  retention throat.
- Replace P13's rigid `ID3.90` on `OD4.00` assumption with a falsifiable coupon
  ladder for permanent PETG retention:
  - socket IDs: `3.96`, `4.00`, `4.04`, `4.08`, `4.12 mm`;
  - engagement depths: `3.50`, `4.00`, `4.50 mm`;
  - optional retention features: smooth bore, shallow annular groove, and
    heat-set/crimp witness variants if implementation can keep them printable.
- Initial CAD production default before coupon proof: `cap_socket_id = 4.04 mm`
  and `cap_rod_engagement = 4.00 mm`, classified as physical unknown. This is
  intentionally not a physical acceptance claim.
- The caps also act as outer slot follower heads; follower OD must exceed slot
  width enough to retain the rod axially while preserving cap-to-outer running
  clearance. The follower head must not bind against fixed inner slots.

Coupon gate:

- Print a dedicated P17 R2 permanent-cap retention coupon before relying on the
  production cap default.
- Pass gate only if six cap samples can be installed without cracking or
  hammering, cannot be removed by the defined hand pull, and still permit rod
  rotation/slot following as intended. Exact pull force remains pending unless
  measured with a gauge.

### Stepped center axle and reaction path

The fixed inner plates are joined and grounded by the one-piece stepped center
axle. The larger central hex spacer sets the inner clear span and its shoulders
seat both inner plates. The smaller hex key sections prevent the inner plates
from rotating relative to the axle. The right primary outer plate transmits
lock and forming torque into the right fixed inner plate, then through the
right hex bore, stepped center axle, and left hex bore to the left fixed inner
plate and the user's opposing hand or bench reaction. The XT60 plastic body is
only an envelope/clearance object and must not be a structural reaction member.

The center axle crosses the span near the XT60/wire envelope. Implementation
must include actual-solid collision and service checks for:

- central larger hex spacer vs XT60 body envelope;
- central larger hex spacer vs insulated wire envelopes in loading, locked,
  soldering, cooling, release, and removal states;
- inner hex key shoulders vs fixed guide slots and rod/follower paths;
- outer journal/keeper features vs outer plates, caps, and hand grip features.

Do not add yoke/stability bars, yoke sockets, or yoke tenons. Stiffness, PETG
hex-bore wear, bearing fit, keeper security, and print strength remain
physical unknowns.

Slide-over assembly sequence:

1. Start with the one-piece stepped center axle without outer keepers installed.
2. From each axle end, slide the fixed inner plate's hex bore over the round
   journal/keeper-seat section. This must clear because
   `outer_journal_diameter < fixed_inner_hex_bore_af`.
3. Seat each fixed inner plate on the matching inner hex key against the
   central spacer shoulder.
4. Add each outer plate onto its round journal with the named diametral
   running clearance.
5. Install the permanent keeper rings onto their modeled end seats/grooves,
   leaving `keeper_axial_running_clearance` so outer plates rotate freely.

Keeper installation and removal force are not CAD acceptance. P17 R2 requires
a keeper coupon or a real hardware keeper decision before physical acceptance.

### P17-D04 offset pivot and guide repair

Selected repair: offset the one-piece stepped center axle and shared pivot
behind the XT60 body rather than adding structure or shrinking the axle. The
provisional pivot is:

```text
pivot_y = -10.60 mm
pivot_z = 17.00 mm
```

This places the pivot centerline on the `-Y` behind-connector side, with pivot
`Z` inside the XT60 body-height projection, and away from the `+Y`
outgoing-wire/solder side. The full X-spanning axle/keepers may extend outside
the XT60 body `X` width while still requiring actual-solid service clearance.
With the current XT60 body half-depth `4.05 mm` in `Y`, central hex
circumradius about
`5.77 mm`, and keeper radius about `5.30 mm`, this gives approximate locked
behind-body `Y` clearances of:

```text
central_hex_corner_to_XT60_back_face_clearance_y ≈ 0.78 mm
keeper_to_XT60_back_face_clearance_y ≈ 1.25 mm
```

Implementation must verify these as actual-solid clearances, not as scalar
proxies. If the realized hex orientation increases the `Y` support radius, move
the pivot farther in `-Y` or reduce nonfunctional geometry while preserving the
slide-over and strength constraints.

All guide and slot geometry must be regenerated around the offset pivot. The
P17-D04 provisional guide-center table was superseded during P17-I03 because
actual-solid probing showed those provisional paths intersected the XT60 body.
P17-D05 retains the collision-free P17-I03 final guides below as the active
repair contract; future edits must preserve their collision-free role unless a
new actual-solid guide proof replaces them:

| Rod | Open world center `(Y,Z)` | Locked world center `(Y,Z)` | Intent |
|---|---:|---:|---|
| `upright_forming_rod` | `(-12.00, 3.00)` | `(-18.00, 13.00)` | vertical-leg forming while avoiding the body and offset axle/keeper keepout |
| `bottom_support_rod` | `(-5.00, -12.00)` | `(8.00, -12.00)` | lower support/front-side travel clear of behind-body axle |
| `diagonal_forming_rod` | `(11.50, 9.00)` | `(3.00, 1.00)` | corner-forming diagonal that stays outside axle/keeper keepout |

The fixed inner slot centerline for each rod is the straight line through these
world centers plus endpoint margin. The outer cam slot centerline is not that
straight line: for each side and each rod it is the continuous part-local locus

```text
cam_center_s_i(theta) =
  R_x(-alpha_s(theta)) * (rod_center_i(theta) - pivot_yz)
```

with `alpha_left(theta) = -theta` and `alpha_right(theta) = +theta`, sampled or
fit as a smooth curve tightly enough that reconstructed world rod-center error
is below `0.05 mm`. The cut slot is then a narrow swept slot around that curve.
Do not approximate the cam as one straight oversized capsule between endpoint
centers.

Default plate sizing for this offset is:

```text
inner_plate_diameter = 54.00 mm
left_outer_secondary_grip_diameter = 60.00 mm
right_outer_primary_grip_diameter = 63.00 mm
```

The inner diameter increase is justified only by the offset guide endpoint,
slot-width, and minimum web envelope. It is not a general size increase and
must be reduced if implementation proves a smaller plate preserves the same
clearances and webs. The right side remains the primary actuator with a
`1.50 mm` larger lever radius than the left.

### P17-D04 low-wobble slot and rail repair

Current `4.90 mm` fixed slots and `7.55 mm` outer slots are rejected. The
active repair default is:

```text
rod_diameter = 4.00 mm
fixed_slot_width = 4.20 mm
outer_cam_slot_width = 4.20 mm
nominal_center_slop = ±0.10 mm
```

This is a CAD default, not physical acceptance. It is derived from the existing
PETG rod-hole coupon where `4.15 mm` was the best sliding round-hole result,
with a small additional allowance for printed slot edges and curved cam paths.
The implementation must include a P17 R2 slot-fit coupon ladder before physical
acceptance:

```text
slot widths: 4.10, 4.15, 4.20, 4.25, 4.30 mm
coupon forms: straight fixed-guide slot and representative curved cam slot
rod: actual OD4.00 stainless rod
material/process: PETG, 0.4 mm nozzle, same orientation assumptions
```

Follower caps remain permanent axial retainers. They must not force the outer
cam slot width to the cap head diameter. If cap heads are used as anti-escape
flanges, they ride outside the plate face with named axial clearance; the rod
shank controls the low-wobble slot.

Nonfunctional visual bulk must be reduced:

- Do not add raised rails unless they perform a named strength or retention
  function.
- Slot walls/webs must meet `min_web_mm = 2.20 mm`; preferred local web is
  `2.40..3.20 mm`.
- Nonfunctional material outside slot webs should be relieved or blended where
  it is not needed for hub, grip, lock, or cap clearance.
- Any local wall above `4.00 mm` around a slot must be justified by a named
  load path, lock reaction, grip, or print-strength reason.

### Endpoint lock, hard stop, and back-drive argument

Selected lock concept:

- Right primary outer plate carries an integral lock lug and thumb-release
  tab.
- Right fixed inner plate carries a grounded hard-stop face and detent pocket.
- The last `2..4 deg` of travel enters an over-center/dwell region where the
  principal load-bearing slot tangent is shaped so the expected rod reaction
  normal produces closing torque into the hard stop rather than opening torque.
- The hard stop defines the locked angle; the detent keeps the plate seated
  against the stop during handling.
- The left outer plate is not independently latched. It is prevented from
  back-driving by the rigid rods, fixed inner guide slots, and the locked right
  primary outer slot. Validation must check that with the right primary locked,
  any small left rotation would require rod skew or follower penetration.

P17-D04 repair gate for `REQ-016`: the previous scalar
`lock_backdrive_evidence()` is not sufficient by itself. The repair candidate
must add actual stop/contact geometry that can be falsified on solids:

- Right fixed inner plate includes a receiver pocket with a closing hard-stop
  face and an opening-side detent/retaining shoulder.
- Right outer primary plate includes a lock nose/tab that enters the receiver
  during the final `2..4 deg` of travel.
- At `theta_lock`, closing-side hard-stop contact is either tangent within
  `0.05 mm` or represented by an allow-listed contact/interference volume no
  greater than the named stop preload.
- At `theta_lock`, the lock nose is captured past the opening-side shoulder by
  `over_center_capture = 0.30..0.60 mm`; default target `0.40 mm`.
- For an un-released opening perturbation of `1.0 deg` and `2.0 deg`, the
  swept lock nose must intersect the retaining shoulder before any rod center
  can move more than the nominal slot slop envelope.
- With a modeled release clearance applied, the same opening sweep must clear
  the retaining shoulder and not collide with rods, caps, axle, keepers, XT60,
  wires, solder joints, or service envelopes.

P17-D05 lock repair supersedes the P17-I03 seated-receiver geometry without
changing the P17 R2 architecture. P17-C03/P17-V03 found that the right outer
lock nose collides with the right inner retaining shoulder during normal
closing at `20, 24, 28, 30, 31 deg`, while the same shoulder is needed to block
unreleased opening. The next implementation must use the same real right
inner/right outer parts and the same seated receiver occurrence for all checks;
do not validate against an imaginary shifted receiver or a separate alternate
part.

Smallest selected lock repair:

- Replace the blunt opening-side retaining shoulder with an integrated
  one-way pocket in the right inner receiver: a closing-side lead-in ramp,
  a zero-penetration throat, a hard-stop face at `theta_lock`, and an
  opening-side undercut/catch after the nose has passed the throat.
- Simplify the current orange twin-arm receiver into one compact grounded
  receiver rib where possible. Merge any redundant outboard arm/bridge into
  the load path between the fixed-inner hub/web and the hard-stop/shoulder.
  Keep only geometry that contributes to stop reaction, shoulder retention,
  user release, or printable web strength.
- The release state must be modeled as the same receiver with an actual
  user-operable compliant relief feature or thumb-accessible deflection path
  on the right inner/outer pair. A parameter such as
  `lock_receiver_release_shift` is allowed only if the source also models the
  connected flexure/tab clearance envelope and proves that the shifted
  shoulder remains part of the same seated receiver solid.
- Keep `theta_lock = 32 deg`, `over_center_capture = 0.30..0.60 mm` with
  default `0.40 mm`, and hard-stop contact tolerance `<= 0.05 mm` unless a
  smaller dimensional repair proves otherwise.

Required lock states and done gates:

| State | Receiver condition | Required result |
|---|---|---|
| Closing sweep `0..31.8 deg` including `20,24,28,30,31` | seated, unreleased | lock nose passes the lead-in/throat with zero solid intersection and `>=0.20 mm` clearance to the retaining shoulder except intentional hard-stop approach |
| Locked `32 deg` | seated, unreleased | hard-stop face is tangent/within `0.05 mm`; lock nose is captured past the opening-side shoulder by `0.30..0.60 mm`; no shoulder penetration |
| Over-close `33 deg` | seated, unreleased | only the hard stop may be an allow-listed contact/interference; rods/caps/keeper/body remain clear |
| Unreleased opening `31,30 deg` | seated, unreleased | the nose is blocked by the opening-side catch before any rod center moves beyond nominal slot slop; the blocker is the same seated receiver solid |
| Released opening `32 -> 30 deg` | same receiver, modeled release deflected | lock nose clears the shoulder and all production/service envelopes without using an alternate receiver location |

This is a geometric endpoint-lock proof only. If the implementation cannot
achieve hard-stop contact plus positive over-center/detent capture on the
existing right inner/outer plates without adding a new linkage or frame, then
`REQ-016` must remain digitally unresolved and be returned to design instead of
claiming a lock from torque signs alone.

Back-drive argument to prove digitally:

- For each load-bearing rod at lock, compute the slot tangent and normal in
  world coordinates.
- Resolve a nominal wire reaction direction into torque about the right hub.
- The summed torque must be non-opening or must be reacted by hard-stop
  contact before any follower can retreat along its guide line.
- Separately compute the lock-nose opening sweep against the fixed retaining
  shoulder. The over-center/detent geometry is the primary back-drive block;
  rod-slot torque signs are supporting evidence, not a substitute for contact.
- CAD can prove contact geometry and sign under nominal directions only. Actual
  force, friction, vibration, creep, heat softening, wear, and self-lock remain
  physical proof pending.

### Use sequence

1. Open both outer plates by counter-twisting to `theta = 0`.
2. Insert XT60 pigtail wires into the fixed inner clearance envelope without
   loading the plastic body.
3. Counter-twist both outer plates toward lock; rods move along fixed guide
   slots and form the wires toward a fixed 90-degree path.
4. Seat the right primary lock lug against the fixed hard stop/detent.
5. Solder while the center axle, fixed inner plates, and locked right primary
   path react load.
6. Allow cooling.
7. Thumb-release the right primary detent.
8. Counter-twist both outer plates back to the open service state so all rods
   withdraw from the completed-pigtail extraction corridor.
9. Remove the completed pigtail through the modeled service window/trajectory;
   do not validate removal while the jig remains locked or partially closed
   unless a future design explicitly supports that extra capability.

P17-D05 completed-pigtail removal repair: P17-V03 showed the current
completed-pigtail removal envelope colliding with both fixed inner plates in
all sampled states and with the diagonal rod at early opening states. This is
a real production collision until a modeled service trajectory clears it.

The active service contract is:

- Removal is only allowed after release and full return to the open service
  state. The user action sequence must explicitly release the right lock and
  open both outer plates before extraction.
- Both fixed inner plates need a real production `completed_pigtail_window`,
  not a reference-only overlay. The starting default is a rounded front-side
  through-window projected in each inner plate from world `Y=4.50 mm` to the
  front disk edge and centered around `Z=22.50 mm`, with
  `completed_pigtail_window_width_z = 8.00 mm`. The implementer may tune this
  only by actual-solid removal-envelope proof and must preserve named minimum
  webs around fixed slots, the hex hub, and the lock receiver.
- The removal trajectory is a two-stage service sweep in the released-open
  state: first lift/clear the completed pigtail into the window centerline so
  the service envelope lower bound stays above the diagonal rod by at least
  `0.75 mm`, then translate along `+Y` until the solder joints, heat shrink,
  and outgoing wires are outside the plate stack. If the implementation uses a
  different dogleg, it must be persisted as named waypoints and actual swept
  solids.
- The removal envelope must include XT60 body, solder joints, outgoing wires,
  heat-shrink, and realistic hand/tool clearance where that clearance is part
  of extraction. A collision may not be dismissed as "reference-only" if that
  solid represents the produced pigtail or a required service path.
- Mid/locked removal is not a supported user operation for P17 R2. Validation
  should still prove that mid/locked states do not intersect the stored
  workpiece/service keep-outs during soldering and cooling, but completed
  pigtail extraction clearance is required in the released-open service state.

### Source namespace and STEP targets

The corrected logical namespace for P17 R2 source and regenerated artifacts is
`p17_r2_direct_counter_twist`. This documentation-only correction did not
rename the pre-correction `p18_direct_counter_twist` implementation files or
generated artifacts, because CAD/source/test/artifact mutation is out of scope
for `P17-D03`.

Future source/artifact relabel or regeneration should use a new P17 R2
namespace rather than editing P13:

- Source module: `src/xt60_bend_jig/p17_r2_direct_counter_twist.py`.
- Tests: focused P17 R2 tests under `projects/xt60-bend-jig/tests/`.
- CAD directory: `cad/p17_r2_direct_counter_twist/`.
- Primary STEP/state targets:
  - `p17_r2_open.step.py`
  - `p17_r2_mid.step.py`
  - `p17_r2_locked.step.py`
  - `p17_r2_exploded.step.py`
  - `p17_r2_print_kit.step.py`
  - `p17_r2_permanent_cap_coupon.step.py`
- Secondary 3MF only after STEP/source validation passes:
  - `p17_r2_print_kit.3mf`
  - `p17_r2_permanent_cap_coupon.3mf`

## Validation targets for implementation

The test plan is risk-driven; test names may differ, but coverage must be
traceable.

Core BREP/object-collision checks:

- open/mid/locked actual-solid assemblies have no unintended intersections;
- expected hard-stop/detent contacts are explicitly allow-listed;
- rods/caps do not collide with the center axle, inner plates, outer plates,
  XT60 body envelope, solder access keep-outs, or removal sweeps;
- center axle central hex spacer, smaller hex key sections, round journals, and
  keepers do not collide with XT60/wire/service envelopes or rod/follower
  paths;
- offset center axle and keepers have zero intersection and at least `0.75 mm`
  positive clearance to XT60 body, solder joints, outgoing wires,
  heat-shrink/service envelopes, soldering-tool keep-out, release sweep, and
  completed-pigtail removal sweep in open, mid, and locked states;
- the pivot centerline is behind the XT60 body on `-Y`, the pivot `Z` is
  inside the connector body projection, and the axle/keepers are away from the
  `+Y` wire-exit/solder-joint side; full axle/keeper `X` extents are allowed
  to exceed the XT60 body width because of the four-plate stack;
- lock closing sweep at `0,4,8,12,16,20,24,28,30,31,31.5,31.8,32 deg`
  uses the seated, unreleased receiver and has zero unintended lock-nose to
  shoulder collision before lock;
- locked, over-close, unreleased-opening, and released-opening lock states use
  the same actual receiver occurrence and prove hard-stop contact, retained
  after-lock blocking, and user-operable release clearance without an imaginary
  shifted receiver;
- fixed inner plates can slide over the round journal/keeper-seat sections
  before seating on the hex keys;
- follower heads remain captured in their outer slots without binding against
  fixed inner slots;
- insertion, opening, locking, soldering, cooling, release, and completed
  pigtail removal paths are represented by actual solids/envelopes;
- completed-pigtail removal is proven as a real released-open service
  trajectory through modeled inner-plate windows and clear of the diagonal rod,
  fixed inner plates, rods/caps, axle/keepers, XT60 body, solder joints,
  outgoing wires, heat-shrink, and required tool/hand envelopes by at least
  `0.75 mm`.

Math and kinematic checks:

- fixed inner transforms are identical across open/mid/locked states;
- center axle transform is identical across open/mid/locked states;
- one named `pivot_yz` datum drives center axle, inner hex bores, outer bearing
  bores, fixed guide slot construction, outer cam slot construction, lock
  stop/detent geometry, and snapshots;
- fixed inner hex bores remain rotationally aligned to the center axle hex key
  sections;
- left/right outer angles are equal magnitude and opposite sign;
- every outer slot world reconstruction maps to the fixed guide line for its
  rod at every tested state;
- left and right rod-end centers are coincident in `YZ` and rod skew is zero
  within tolerance;
- outer cam slots are swept from the actual continuous part-local centerline
  under the offset pivot, with reconstructed rod-center error below `0.05 mm`;
- rod center slop envelope from slot width is reported; default CAD slop is
  `±0.10 mm`, with binding/slop physical proof pending the slot coupon;
- no moving hole/slot is defined in world space without applying the owning
  part transform;
- locked slot tangents and hard-stop contact normals support the nominal
  back-drive argument without claiming actual force.

Constraint checks:

- inner clear span is derived from XT60 width plus named clearance and is less
  than half of P13's `10.3 mm` surplus over the XT60 body;
- axial stack, center-axle length, rod length, keeper clearance, and cap
  engagement formulas match generated solids;
- `fixed_slot_width = 4.90 mm` and `outer_slot_width = 7.55 mm` are rejected
  values and must fail as active P17 R2 defaults;
- fixed and outer cam slot widths are named low-wobble values close to
  `OD4.00 mm`, defaulting to `4.20 mm` until PETG slot coupons supersede them;
- generated cam slots are curved swept slots around the derived cam
  centerline, not oversized straight endpoint capsules;
- slot-fit coupon contains straight and curved slots at `4.10, 4.15, 4.20,
  4.25, 4.30 mm`;
- nonfunctional rail/wall bulk around slots is reduced while preserving named
  minimum printable webs; local slot walls above `4.00 mm` require a named
  structural/load-path justification;
- center axle has exactly one larger central hex spacer, two smaller hex key
  sections, two round journal sections, and two thin outer keepers;
- round journal OD is smaller than the fixed-inner hex bore inscribed diameter
  and the modeled assembly path proves that the inner plates can pass over the
  round sections before engaging the hex keys;
- inner hex key AF, fixed-inner hex bore AF, journal OD, outer bearing bore,
  keeper seat length, keeper ring thickness, and keeper axial clearance are
  named parameters with domain checks;
- each round journal spans the running gap, the full outer plate thickness,
  keeper axial clearance, and an actual retained keeper seat;
- each keeper is positively retained by modeled press fit/seat/groove or a
  real modeled split/groove keeper; floating keeper rings fail validation;
- keeper print-readiness checks prove `keeper_radial_wall_min >= 1.20 mm` at
  retained lobes after any collision-relief flats/scallops and include a
  physical keeper-retention coupon ladder before any print acceptance claim;
- outer plates rotate on round journal sections only and are not keyed to the
  axle;
- six permanent caps exist, two per rod, with no removable cap objects or
  service-removal wording in production names;
- all sliding rod holes/slots use the printed coupon evidence only in sliding
  roles; permanent cap sockets use a separate coupon contract;
- minimum ligaments, webs, slot edge distances, inner hex-bore walls, round
  journal bearing walls, keeper roots, and lock-lug roots meet named PETG
  defaults;
- source/export parity verifies STEP occurrence counts, labels, transforms,
  and bounds.

User-requirement absence checks:

- no simulator, animation sidecar, Three.js, or JS motion dependency;
- no shared same-direction actuator shaft;
- no shared keyed/flat coupling from the center axle to either outer plate;
- no moving hole in a fixed inner plate;
- no cap marked removable/service;
- no P17 R1 simulator dimensions or geometry copied as authority;
- no yoke/stability bars, yoke sockets, or yoke tenons;
- no center axle left at the geometric origin without an explicit service
  clearance proof;
- no oversized `4.90 mm` / `7.55 mm` production slot defaults;
- no straight endpoint-capsule cam-slot shortcut;
- no XT60 plastic body load path.

Manufacturing and visual checks:

- STEP inspect `refs --facts --planes --positioning` and `validate` for every
  primary target;
- CAD snapshots for open, mid, locked, exploded, lock closeup, cap coupon, and
  print kit;
- CAD Viewer handoff after artifacts exist, requiring page HTTP `200` plus
  `/__cad/artifact` HTTP `200` and `state == "ready"` before review readiness;
- DfAM checks on the print kit and cap coupon before any slicer/3MF claim;
- slicer proof only after print artifacts are generated from the validated
  source and STEP state.

## Candidate manifest and deterministic fingerprint contract

P17-D05 requires the next implementation to persist the exact candidate
manifest and fingerprint payload. The P17-I03 receipt's prose-only
"canonical JSON" description is insufficient because independent validation
could not reconstruct the fingerprint from a checked-in JSON payload.

Write these files from source/provenance generation before critique or
validation:

- `projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist/p17-r2-candidate-manifest.json`
- `projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist/p17-r2-candidate-fingerprint.json`

Canonical JSON rules:

- UTF-8 JSON object.
- Keys sorted recursively.
- Compact separators `,` and `:` with no insignificant whitespace.
- Exactly one trailing newline in the written file.
- Arrays sorted by `path`, then `kind` where both exist.
- No timestamp, machine-local path, absolute path, scratch path, or wall-clock
  field may appear in `p17-r2-candidate-fingerprint.json`.

`p17-r2-candidate-manifest.json` schema:

```json
{
  "schema": "xt60-bend-jig.p17-r2.candidate-manifest.v1",
  "project": "projects/xt60-bend-jig",
  "iteration": "p17-r2-direct-cad-counter-twist",
  "candidate_id": "assigned implementation task id, e.g. P17-I04 or P17-I03-repair",
  "baseline_commit": "git baseline used by the implementer",
  "frozen_doc_manifest_sha256": "sha256 of decision-bearing docs used by implementation",
  "fingerprint_payload_path": "projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist/p17-r2-candidate-fingerprint.json",
  "candidate_fingerprint_sha256": "sha256 of the canonical fingerprint payload file bytes",
  "inputs": [
    {"path": "relative/repo/path", "sha256": "64 lowercase hex", "kind": "requirement|design|source-input|test-input|provenance-input"}
  ],
  "outputs": [
    {"path": "relative/repo/path", "sha256": "64 lowercase hex", "kind": "source|test|step|snapshot|provenance|coupon|manifest"}
  ],
  "excluded": [
    {"path": "relative/repo/path-or-glob", "reason": "mutable orchestration, ignored cache, scratch, or non-decision record"}
  ],
  "commands": [
    {"cmd": "exact command string", "result": "concise result"}
  ]
}
```

`p17-r2-candidate-fingerprint.json` schema is the deterministic subset:

```json
{
  "schema": "xt60-bend-jig.p17-r2.candidate-fingerprint.v1",
  "project": "projects/xt60-bend-jig",
  "iteration": "p17-r2-direct-cad-counter-twist",
  "candidate_id": "same as manifest",
  "baseline_commit": "same as manifest",
  "frozen_doc_manifest_sha256": "same as manifest",
  "inputs": [
    {"path": "relative/repo/path", "sha256": "64 lowercase hex", "kind": "requirement|design|source-input|test-input|provenance-input"}
  ],
  "outputs": [
    {"path": "relative/repo/path", "sha256": "64 lowercase hex", "kind": "source|test|step|snapshot|provenance|coupon|manifest"}
  ]
}
```

Fingerprint formula:

```text
candidate_fingerprint_sha256 =
  SHA256(bytes of p17-r2-candidate-fingerprint.json written by the canonical
  JSON rules above)
```

Required reproducibility command from repo root:

```sh
LC_ALL=C shasum -a 256 \
  projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist/p17-r2-candidate-fingerprint.json
```

The validator must be able to recompute the same SHA-256 from the persisted
file without reading a prose receipt. If candidate files change, regenerate
both manifest files and invalidate critique/validation/review gates that used
the previous fingerprint.

## Physical unknowns

- Permanent cap installation force, retention, cracking, wear, and heat
  response.
- Plastic-on-plastic hub friction, backlash, wear, and creep.
- Center-axle hex-bore fit, shoulder seating, keeper retention, bearing
  clearance, stiffness, and real hand/bench reaction behavior.
- Whether the offset behind-body pivot preserves actual soldering/cooling and
  completed-pigtail removal ergonomics.
- Whether `4.20 mm` printed straight/curved slots give acceptable low-wobble
  running clearance for the actual `OD4.00 mm` stainless rods.
- Lock detent force, self-lock, vibration resistance, release effort, and
  thermal creep.
- Wire holding force, insulation marking, soldering heat exposure, cooled bend
  angle, and springback.
- Whether a `40.50..40.60 mm` rod length is best ordered/cut for the real
  stack and cap engagement.

## Design-owner boundary

This design record is not CAD/source validation, artifact/slicer acceptance, or
physical acceptance. It is the contract for a separate implementation owner.
