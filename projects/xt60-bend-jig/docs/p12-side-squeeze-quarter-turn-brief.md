# P12 — side-squeeze quarter-turn XT60 jig

P12 is a new compact architecture successor to P11. P11 remains unchanged as
the validated four-disc reference. P12 reuses the accepted role-specific rod
kinematics and the assumed XT60/wire envelope, but replaces the four complete
discs and bottom base with a small open frame.

## Coordinate and workpiece contract

- Units are millimetres. Rod axes are X; wire forming occurs in YZ.
- Preserve the P11 default workpiece: two 4.30 mm leads, bend radius 6.0,
  D1 7.0, and the documented assumed XT60 envelope.
- Preserve exactly three purchased 304 stainless rods, each `Ø4 x 50 mm`.
- Preserve the P11 motion laws and contact order:
  forming completes at 20 degrees, support at 27 degrees, locking at
  32 degrees, followed by a true 32..35 degree dwell.

## Compact architecture

- No bottom plate and no complete circular principal plate.
- Two fixed skeleton cheek plates, each 4.0 mm thick, separated by a clear
  26.0 mm span.
- One 3.0 mm skeleton cam outside the right cheek with 0.30 mm running gap.
- The left cheek uses 4.4 mm datum guide slots. The right cheek uses 4.9 mm
  follower guide slots. The one right cam contains the three independently
  derived inverse slots and the 4.4 mm locked endpoint pockets.
- Cheek and cam material follows the required slot, hub, connector, detent and
  stop envelopes with only local structural web. It must not be replaced by a
  hidden complete disc.
- One rear/top spine joins the cheeks through two clearance-fit blind tongues.
  The spine front face sits 0.10 mm behind the assumed XT60 rear face and acts
  as the connector datum. A narrow rearward tongue provides a bench-clamp land.
- The frame load path is rods -> cheek webs -> rear spine -> clamp tongue.

## One-action lock

- A keyed shaft and integral finger lever rotate the skeleton cam 0..35 degrees.
- A fixed Ø2 stop pin follows a 2.2 mm cam channel with a positive 35-degree
  hard endpoint.
- A fixed Ø2 detent nose engages 2.4 mm OPEN and LOCK pockets in the cam hub.
- The 32..35-degree kinematic dwell prevents additional rod displacement while
  the lever enters the LOCK detent. Printed detent force and true force-based
  over-centre behaviour remain physical tests; CAD proves only geometry.

## Assembly and release

- Rods insert from the right through cam and both cheek guides.
- Three 3.9 mm blind circular caps retain the left ends.
- Three Ø7 x 2.9 mm circular C-clips with 4.10 mm throats retain the right ends
  and remove sideways before the rods are withdrawn.
- The printed shaft inserts from the left and receives a removable circular
  C-keeper on its right neck.
- Intended UX: clamp rear tongue -> OPEN -> place pigtail against spine datum ->
  rotate lever to LOCK -> solder -> cool -> flick to OPEN -> remove retainers
  and rods if the fixed soldered pigtail prevents intact lifting.

## Outputs

- Authoritative source:
  `src/xt60_bend_jig/p12_side_squeeze_quarter_turn.py`.
- Tests:
  `tests/test_p12_side_squeeze_quarter_turn.py`.
- Generated STEP entries under `cad/p12_side_squeeze_quarter_turn/`:
  loaded open, loaded closed, solder access, exploded, and print kit.

## Acceptance

- P11 source and artifacts remain untouched.
- Three rods follow the frozen P11 centres and motion laws at every tested pose.
- Dense pose sampling shows zero rod overlap with either cheek or the cam.
- Cam, stop, detent, spine tongues, retainers and shaft are geometrically
  assemblable at OPEN and LOCK.
- The primary frame has no bottom plate, keeps the soldering side open, and is
  materially smaller than P11's four full discs and base.
- STEP source/export parity, positive closed solids, non-overlapping print-kit
  layout, and mandatory snapshots pass.
- Printed fit, detent feel, tongue retention, cam torque, wire deformation,
  springback, heat exposure and real soldering ergonomics remain physical gates.
