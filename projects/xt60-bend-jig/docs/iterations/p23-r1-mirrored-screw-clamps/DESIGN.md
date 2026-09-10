# P23 R1 first-preview design contract

Date: `2026-08-29`  
Owner: `P23-DESIGN-01`  
Status: **SELECTED FOR EVIDENCE-ONLY INTENT CAD; NOT PRINT AUTHORITY**

## Verified input fingerprint

The six entries frozen in `BRIEF.md` were verified exactly, including the
supplied image: `6/6` SHA-256 matches. The image is inspiration only.

## Selected architecture

Use two X-mirrored **side yokes**, one outside each outer plate. Each yoke
captures Green in a fixed reaction socket, captures Blue in its inherited
straight-path follower channel, and carries a non-rotating Orange shoe in a
straight guide. One captive printed screw per side pushes and positively pulls
the Orange shoe. Left and right screws have equal pitch and equal nominal
travel; indexed knobs make equal-turn operation visible.

A rigid fixed-seat Blue/Green bridge is rejected because their separation
changes from `30.1645 mm` at OPEN to `16.9853 mm` at CLAMPED. An axle-mounted
yoke is deferred because it would unnecessarily reopen the stepped-axle stack
for this first intent preview.

## Datums, roles and parameters

- Units: millimetres. X is the rod axis; FRONT is YZ; `+Z` is mating-head/up;
  `+Y` is wire-tail/outward. Left/right modules mirror across `X=0` only.
- Immutable rods: three purchased `OD4.00 x 50.00 mm`; rod ends are `X=±25.00`.
- Preserve inherited four plates, stepped axle, all YZ rod paths and rails.
  Remove six individual caps; no other inherited geometry changes here.
- Corrected outer-plate outer faces are `X=±21.00`. Yoke inner faces are
  `X=±21.30`, preserving `0.30 mm` running gap; yoke thickness is `6.00`, so
  outer faces are `X=±27.30`.
- Rod-end sockets: `ID4.15`, nominal depth `4.00`, axial end clearance `0.30`,
  closed outboard wall `2.00`. Green socket is integral to the yoke; Blue is
  captured by a follower pocket; Orange is captured by the translating shoe.
  Each pocket wraps the rod end rather than applying end-face pressure only.
- General yoke wall target: `2.40`; local shoe/follower wall around an OD4
  socket: `2.00` radial minimum. Preview sliding clearance is `0.20` per side.
- Orange shoe nominal section: `9.00 x 6.00`; it is anti-rotation guided and
  uses a captive mushroom-head screw nose so screw reversal pulls it back to
  OPEN instead of relying on gravity.
- Printed screw: single-start trapezoidal `major Ø10.00`, `pitch 2.00`,
  nominal minor `Ø8.00`, nut engagement `10.00`, usable translation `13.00`,
  knob `Ø18 x 6`. Left/right handedness may mirror, but pitch magnitude and
  translation remain identical; each knob receives 12 index marks and a
  visible `CLAMP` arrow.

## OPEN and CLAMPED states

The preview uses the inherited world-YZ centers exactly:

| Rod | OPEN `(Y,Z)` | CLAMPED `(Y,Z)` | Travel |
|---|---:|---:|---:|
| Blue | `(-7.511545, 14.127161)` | `(2.228078, 5.248302)` | `13.179317` |
| Orange | `(11.313708, 11.313708)` | `(8.478078, -0.501698)` | `12.150911` |
| Green | `(14.728078, -6.251698)` | unchanged | `0.000000` |

Orange shoe center is `O(s)=O_OPEN+s*(-0.23336776,-0.97238855)`,
`0 <= s <= 12.150911`. At `2.00 mm` pitch, full nominal travel is
`6.07546` screw turns. Both sides must show the same `s`; the preview must
include OPEN zero marks and a CLAMPED endpoint mark. Blue remains passive and
follows its inherited channel; the screw does not redefine Blue or Green.

## Assembly and operation intent

1. Assemble the inherited four plates, axle, keepers and three rods without
   the six caps; place the mechanism at OPEN.
2. Set both Blue followers and Orange shoes to their OPEN marks, then install
   the mirrored yokes over the six rod ends.
3. Alternate equal indexed turns on left and right screws. The captive shoes
   move Orange toward CLAMPED while the inherited plate/rail system carries
   Blue and Green on their frozen paths.
4. Stop at both CLAMPED marks. Reverse equal turns to pull both Orange shoes
   back to OPEN; no gravity-assisted release is part of the intended use.

## Focused preview gates and risks

- Preview gates: exact rod identities and endpoints; mirrored equal-pitch
  screws; equal Orange travel; visible Green/Blue reaction capture; visible
  blind outer walls on all six rod-end pockets; zero rod-length or YZ-path
  change; OPEN/CLAMPED assemblies with no unintended solid overlap.
- Major risks left open: unequal user turns may skew Orange; screw friction may
  not hold against back-drive; yoke/rod capture may flex, slip or wear; Blue
  follower may bind; printed thread and snap clearances are unproven; actual
  force, torque, heat, wobble, retention and release effort require later
  physical tests.
- This contract authorizes an intent STEP preview only. It does not authorize
  mesh, 3MF, slicing, printing, or physical-acceptance claims.
