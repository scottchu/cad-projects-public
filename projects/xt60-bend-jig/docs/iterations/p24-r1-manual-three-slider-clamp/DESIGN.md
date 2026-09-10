# P24 R1 manual three-slider clamp design

Date: `2026-08-29`  
Owner: `P24-DESIGN-01`  
Status: **REPAIR CYCLE 1 — CLOSED CONCEPTUAL LOAD/RELEASE LOOP; FIRST-INTENT CAD ONLY**

## Concept comparison

| Concept | Manual-motion separation | Accommodation of three inherited paths | Main concern | Decision |
|---|---|---|---|---|
| Common pressure cassette | Full: screw moves only a pressure plate after hand positioning | Three independent shoes float in separate generous YZ windows | Unknown friction/load sharing and bulky side envelope | **Selected** |
| P23 screw-driven Orange shoe | Fails: screw advances Orange | Blue/Green react while Orange is driven | Contradicts all-three-manual intent | Rejected and superseded |
| Plate-edge brake | Can be applied after hand positioning | Brakes plate edges indirectly rather than capturing each rod-end state | Edge flex, skew, rail interference and unclear three-rod state capture | Not selected |

The cassette is the smallest concept that separates manual forming from state
holding while preserving each rod's inherited rail authority.

## Architecture and labels

Each axial side has a stationary `side_frame_T3`, three separate
`<side>_<role>_floating_shoe_socket_ID4p20`, one
`<side>_common_pressure_plate_T3`, and one
`<side>_central_M6_like_smooth_screw_envelope_CONCEPT_ONLY`. Roles are exactly
`blue`, `orange`, and `green`; no carrier is shared between roles.

Repair cycle 1 gives that smooth screw envelope three explicit conceptual
interfaces: `<side>_frame_thread_reaction_contact_CONCEPT_ONLY`, an outboard
`<side>_screw_clamp_bearing_head`, and an inboard
`<side>_screw_captive_pullback_retainer`. The shaft remains a smooth M6-like
envelope, not modeled thread geometry. Its reacted frame passage is coaxial and
surface-contacting so the visible load path closes without positive-volume
penetration. The pressure plate has a clearance passage and is axially captive
between the larger head and retainer.

Each shoe has an inward-open blind cylindrical socket and an outboard flange.
The flange slides freely in its own frame relief window in `RELEASED_OPEN`.
The common plate spans all three flange backs. Closing the central screw moves
only that plate along X by `0.60`; the final rigid CAD pose places the plate in
simultaneous face contact with all three already-positioned flanges. The frame
provides the opposite sandwich face. Contact represents topology, not elastic
compression or a predicted normal force.

The conceptual clamp load loop is `frame reacted/threaded contact -> screw ->
outboard bearing head -> pressure plate -> three shoe flange backs -> three
shoe flange fronts -> side frame -> frame reacted/threaded contact`. On screw
reversal, the positive release loop is `screw -> inboard captive retainer ->
pressure plate outward`. The screw may translate only the pressure plate along
X. It has no contact or dependency that changes any rod or shoe YZ center.

Each shoe retains a role-colored outboard finger stem beyond the pressure
plate. Exposed stem length is at least `5.00` in both required states so the
user can directly perform Orange DOWN and Blue/Green BACK-TO-FRONT without the
pressure plate visually or physically masking the three inputs.

The three frame windows are envelopes around the complete inherited YZ
endpoint sweeps plus explicit preview clearance. Window geometry must be
derived from inherited centers, not hand-drawn replacement tracks. The windows
may overlap or merge into a generous open relief region if needed; guide rails
remain the only motion authority.

## Parameters and derived relations

| Name | Value / rule | Classification |
|---|---:|---|
| `rod_od`, `rod_length` | `4.00`, `50.00` | invariant purchased parts |
| `rod_end_x` | `+/-25.00` | derived from rod length |
| `outer_plate_face_x` | approximately `+/-21.00` | inherited reference |
| `shoe_engagement` | `3.70` | frozen available axial engagement |
| `shoe_socket_id` | `4.20` | first-design assumption |
| `shoe_socket_depth` | `4.00 = 3.70 + 0.30` | derived intent envelope |
| `released_axial_clearance` | `0.30` | frozen shoe/stack running clearance |
| `pressure_travel` | `0.60` along local inward X | frozen design choice |
| `pressure_plate_thickness` | `3.00` along X | frozen design choice |
| `side_frame_thickness` | `3.00` along X | frozen design choice |
| `relief_radial_clearance` | `>=0.50` beyond socket/shoe swept envelope | provisional first-CAD choice |
| `screw_envelope_diameter` | `6.00` smooth M6-like cylinder | conceptual only |
| `frame_reaction_contact_diameter` | `6.00`, coaxial surface contact with shaft | conceptual threaded/reaction interface only |
| `plate_capture_endplay` | `0.30` between inactive head/retainer face and plate | provisional visible lost motion |
| `finger_stem_exposure` | `>=5.00` beyond pressure-plate outboard face | first-intent access minimum |
| `screw_axis` | X, centered in a collision-free YZ region of the common plate | derived placement |

`shoe_center_yz(role,u) = inherited_rod_center_yz(role,u)` for both sides and
all sampled `u`. Clamp state is an independent variable and must not appear in
the inherited rod-center function. X mirroring changes only X placement and
handed labels; it never mirrors FRONT-YZ motion.

## Required state behavior

### `RELEASED_OPEN`

- Inherited rod state is OPEN (`u=0`).
- Both pressure plates are retracted by exactly `0.60` from their clamped
  positions; smooth screw envelopes show the released position.
- Each inboard captive retainer has explicit zero-distance bearing contact
  with the pressure-plate inboard face; each outboard head has positive visible
  clearance. Screw-to-frame conceptual reaction distance is zero. Every named
  contact has zero positive-volume penetration.
- Six shoes are centered on their corresponding rod ends, with `ID4.20`
  sockets and `3.70` nominal engagement, but their flanges have no pressure-
  plate contact. The model must visibly communicate loose/free YZ following.
- Frame windows clear the inherited endpoint paths and do not contact rods.
- A user-readable outboard/oblique view must show all three colored stems
  extending at least `5.00` beyond the plate, their role labels/directions, the
  released plate gap, and the captive pull-back relation.

### `CLAMPED_END`

- The user has already placed inherited rod state at END (`u=1`) before clamp
  closure; the preview does not animate the clamp as the cause of END.
- Pressure plates alone move inward by `0.60` and touch all three shoe flange
  backs per side. Shoes remain at inherited END centers; rods receive zero
  clamp-derived YZ displacement.
- Each outboard screw head has explicit zero-distance bearing contact with the
  pressure-plate outboard face; each inboard retainer has positive visible
  clearance. Screw-to-frame conceptual reaction distance remains zero.
- Intentional zero-distance contacts are the screw/frame reaction,
  head/pressure-plate bearing, pressure plate/shoe and shoe/frame sandwich
  faces. No named pair may have positive-volume penetration. No holding-force,
  real-thread or self-lock conclusion follows.
- A user-readable oblique/cutaway view must distinguish the fixed frame,
  reacted screw, head-to-plate contact, three simultaneous shoe contacts and
  the still-exposed manual stems from the released view.

## Implementation rules and focused tests

1. Delegate every Blue/Orange/Green center to the current inherited P20/P23
   path function. Test nominal states, intermediate samples, determinism and
   equality of all production callers.
2. Test operation ordering: varying `clamp_progress` at fixed `u` may change
   only pressure-plate/screw X placements and head/retainer bearing selection;
   it must not change any rod or shoe YZ center. Plate travel remains exactly
   `0.60`; screw travel may additionally include the declared `0.30` capture
   endplay. The two delivered states are `(u=0, clamp=0)` and
   `(u=1, clamp=1)`.
3. Test exact rod count `3`, cap count `0`, shoe count `6`, pressure-plate
   count `2`, side-frame count `2`, screw-envelope count `2`, labels and
   X-mirror symmetry.
4. Test rod length/OD/endpoints, socket ID/depth, `3.70` engagement, `0.30`
   released axial clearance, `0.60` pressure travel and both `3.00`
   thicknesses from actual solids. Measure every role-colored finger stem at
   `>=5.00` exposed beyond the pressure plate in both states.
5. Analytically prove every sampled inherited rod/shoe swept envelope lies
   inside its relief window with at least the declared radial clearance.
6. Run hardware-inclusive actual-solid pairwise collision checks in both
   required states. Require zero distance and zero positive penetration at the
   frame/screw reaction in both states, retainer/plate in `RELEASED_OPEN`,
   head/plate in `CLAMPED_END`, and all six plate/shoe plus six shoe/frame END
   contacts. Require positive clearance at each inactive head/retainer face.
   No unintended positive-volume overlap is acceptable. Report inherited
   baseline collisions separately rather than hiding them.
7. Validate all modeled parts as closed positive-volume solids; verify
   source-to-written-STEP parity and exact state labels.
8. Snapshot and independently inspect both STEP states for rod identity,
   manual-vs-clamp causality, loose released shoes, simultaneous end-state
   contact, the closed load/release loops, relief windows and service
   obstruction. Supply the user-readable released outboard/oblique and clamped
   oblique/cutaway views specified above. This is first-intent evidence only.

## Risks and stop conditions

- A rigid common plate may touch one high shoe first; equal three-shoe force is
  not established without compliance or measured tolerances.
- Axial sandwich friction may be insufficient, may mark/wear shoes, or may
  require unacceptable torque. No coefficient or holding force is assumed.
- Shoes may cock, rattle, escape, bind in windows, or pull off the limited
  `3.70` engagement during handling.
- Side frames or plates may flex; the central load may bow the plate and
  produce unequal pressure.
- Tightening one axial side first may skew the assembly; synchronization and
  sequence remain physical questions.
- `ID4.20`, relief clearance, screw placement, thread geometry, assembly path,
  hand access, XT60/wire clearance, heat, creep and print orientation remain
  unvalidated.
- The smooth frame/screw contact depicts a conceptual threaded reaction only;
  thread form, fit, strength, torque, wear, retention and back-drive remain
  wholly unproved.

Stop implementation if any cassette feature must drive or redirect a rod,
change inherited path math, couple the shoes before clamp closure, or rely on
solid interpenetration to depict the `0.60` stroke. Also stop if either the
clamp load loop or positive pull-back loop is open, any required contact has
positive penetration, or the pressure plate masks a finger stem below `5.00`.
Reopen design instead.
