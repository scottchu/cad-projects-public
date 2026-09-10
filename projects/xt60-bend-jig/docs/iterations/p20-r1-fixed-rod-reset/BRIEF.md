# P20 R1 fixed-rod reset brief

Status: **FROZEN INTENT CONTRACT; NUMERIC DESIGN GATE OPEN**

## Outcome and use sequence

Start from the exact P19 R1 product baseline and correct only the rail/rotation
architecture identified by the user. The jig must retain the P19 workpiece
orientation, rod identities, OPEN/END world arrangement, short-tail soldering
service, four-plate stack, real fixed stepped axle, and purchased rod/cap
system. The accepted candidate removes the outer plates' rod rails, moves the
fixed axle farther lower-left, and gives the two outer plates `45 deg` of
equal/opposite travel each while the axle and inner plates remain fixed.

## Coordinate frame and state topology

- Units are millimetres and degrees.
- Physical FRONT is world YZ: `+Z` is XT60 mating-head/up; `+Y` is the short
  solder tail, tool approach, outward/right.
- The real purple stepped axle lies along X, remains fixed in world, and keys
  both inner plates. It is not one of the three white `OD4 x 50 mm` rods.
- P19 rod identities remain `bottom`, `diagonal`, and `upright`. Their exact
  P19 OPEN/END world paths and ordered right-angle-to-diagonal topology remain
  frozen unless the design role proves the bounded correction impossible and
  returns for a separately authorized reopening.
- One normalized state `u in [0,1]` drives the full mechanism. At END,
  `alpha_left=-45 deg` and `alpha_right=+45 deg`, for `90 deg` relative twist.

## Requirements

- `P20-REQ-01`: Use merged P19 R1 at
  `b69b6ad12af611644987f026eef4940db9c7bb34` as the only product input
  baseline and preserve its evidence as history.
- `P20-REQ-02`: Neither outer plate may contain a guide rail for any of the
  three white rods. Required absence is six outer rod rails total.
- `P20-REQ-03`: Preserve the three P19 fixed-inner rod paths, cut identically
  into both fixed inner plates, with their existing rod identities and world
  motion.
- `P20-REQ-04`: Move the real fixed stepped axle datum farther outward toward
  lower-left in FRONT YZ. Its exact coordinate is a design output and requires
  a user-confirmable 2D gate before implementation.
- `P20-REQ-05`: Both outer plates rotate through the complete shared state by
  equal magnitude and opposite sign, `-45/+45 deg`, yielding exactly `90 deg`
  relative travel. The axle and both inner plates remain world-invariant.
- `P20-REQ-06`: Derive one side-specific fixed-axle guide path in each outer
  plate from a single deterministic pure-math transform. The paths must
  produce the same motion result as treating the fixed axle as the
  rotation-center reference and may not be translated or hand-edited copies
  of the P19 guide arc.
- `P20-REQ-07`: Preserve physical `+Z/+Y` orientation, exact rod identities,
  P19 OPEN/END world topology, non-crossing paths, three uncut
  `OD4.00 x 50.00 mm` rods, six permanent caps, and four plates.
- `P20-REQ-08`: Preserve P19 workpiece, wire, cup, XT60, tool-service,
  completed-pigtail service, axle stock/profile, keeper, plate-stack, and
  plate-body geometry unless exact evidence proves the bounded correction
  impossible. An impossibility result stops and requests a new contract; it
  does not silently widen scope.
- `P20-REQ-09`: Stop after the bounded correction passes required CAD, STEP,
  visual, independent validation, and formal review gates. No mesh, 3MF,
  slicing, printing, new lock, new part, or further optimization is in scope.

## Derived constraints and evidence targets

- `P20-CON-01`: The design role must define the new fixed-axle datum, reference
  center(s), plate-local frames, state transform, and centered-equivalence
  equation explicitly. All production callers must delegate to that one pure
  function.
- `P20-CON-02`: At nominal and boundary states, the two side-local guide paths
  must reconstruct the same stationary world axle datum within declared CAD
  tolerance, with deterministic repeatability and left/right sign symmetry.
- `P20-CON-03`: Source and written STEP must prove zero outer rod-rail
  occurrences and the preserved fixed-inner rod-path occurrences by role, not
  only by total solid count or screenshot.
- `P20-CON-04`: Actual-solid checks must cover OPEN, representative mid-states,
  END, hardware-inclusive collisions, minimum material web, rod support,
  completed-pigtail removal, workpiece/tool service, axle/keeper capture, and
  the full `90 deg` relative motion.
- `P20-CON-05`: Tests must separately cover the pure transform, nominal and
  boundary inputs, determinism, inverse/reconstruction equivalence, production
  caller parity, user-required absence/presence, and source/export parity.
- `P20-CON-06`: A failing 2D math, topology, closure, collision, service, or
  material gate stops BREP/export work. No evidence-only solid is a product
  candidate unless the user separately authorizes it.

## Per-object delta masks

| Object | Authorized change | Frozen / forbidden change |
|---|---|---|
| Left outer plate | Delete its three white-rod rails; replace only its fixed-axle guide with the newly derived side-local path. | Plate body, OD, thickness, grip identity, X placement, new holes/rails/parts, or a translated P19 axle arc. |
| Right outer plate | Delete its three white-rod rails; replace only its fixed-axle guide with the newly derived side-local path. | Plate body, OD, thickness, force-side identity, X placement, new holes/rails/parts, or a translated P19 axle arc. |
| Left and right inner plates | Move only the fixed-axle keyed bore/seat as required by the new axle datum. | The three fixed-inner white-rod paths, plate bodies, orientation, role, or rotation. |
| Purple stepped axle and keepers | Move their complete world YZ occurrence together to the accepted new datum. | Axle/keeper source geometry, X-axis role, dimensions, stack engagement, world rotation, or conversion into a white rod. |
| Three white rods and six caps | No geometry or identity change; retain P19 world OPEN/END paths. | Reassignment, shortening, mirroring, crossing, cap change, or outer-plate rod guidance. |
| Workpiece/service geometry | No change. | Moving the XT60, wire/cup/tool keepouts, changing service direction, or weakening removal clearance to make the mechanism fit. |
| Motion law | Change outer endpoint angles to `-45/+45 deg`; derive the new fixed-axle guide relation. | Independent side states, same-direction rotation, moving inners/axle, hand-padded paths, or motion beyond the confirmed `90 deg` relative range. |

## Ambiguity and derived-design boundary

The frozen user intent determines direction, identities, topology, relative
travel, allowed objects, and required outcome. It does not determine a numeric
lower-left coordinate or the mathematical construction of centered-equivalent
guide paths. P20-DESIGN-01 owns those two derivations and must show them in a
cheap FRONT-YZ diagram with OPEN/mid/END states, plate boundaries, fixed axle,
both guide paths, all three inner rod paths, workpiece/service envelopes, and
motion arrows. The user must confirm that exact gate before P20-IMPL-01 begins.

If no candidate satisfies this brief without changing a frozen object, the
correct output is a bounded infeasibility report and the smallest proposed
reopening. It is not permission to redesign.

## Acceptance boundary

CAD/STEP acceptance requires the four core evidence categories—actual-solid
collision, math, constraints, and user requirements—plus applicable motion,
service, source/export parity, snapshots, independent critic, independent
validator, and distinct formal review. Hand force, torque, friction, wedging,
backlash, PETG fit, strength, heat, wear, cap/keeper retention, and real
soldering usability remain physical unknowns even if digital gates pass.
