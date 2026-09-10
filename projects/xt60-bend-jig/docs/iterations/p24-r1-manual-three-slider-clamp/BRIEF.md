# P24 R1 manual three-slider clamp brief

Date: `2026-08-29`  
Owner: `P24-DESIGN-01`  
Status: **DESIGN CONTRACT COMPLETE; FIRST-INTENT CAD ONLY; NOT PRINT AUTHORITY**

## Baseline and objective

P24 supersedes P23's screw-driven Orange architecture for forward design while
retaining P23 as rejected/superseded history. Preserve the current P20/P23
four-plate mechanism, inherited rod paths and rails, and all three purchased
`OD4.00 x 50.00 mm` rods. Remove the six tight caps. Add one X-mirrored
three-shoe clamp cassette at each rod end. The cassette holds a hand-reached
state; it does not create that state or drive any rod.

Units are millimetres. X is the rod axis; FRONT is world YZ; `+Z` is XT60
mating-head/up and `+Y` is wire-tail/outward. Rod ends remain `X=+/-25.00` and
outer plate faces are approximately `X=+/-21.00`.

## Use sequence

1. In `RELEASED_OPEN`, both cassettes are released. Their three independent
   shoes are loose in generous YZ relief windows and follow, but do not define,
   the inherited rod-end paths.
2. The user alone moves the mechanism: thumb pushes Orange DOWN; index and
   middle fingers push Blue and Green BACK-TO-FRONT. No screw, pressure plate,
   shoe or frame may advance any rod.
3. After the hand reaches inherited CLAMPED/END, tighten the central screw on
   each side. Each screw moves only its common pressure plate, which
   simultaneously sandwiches the three already-positioned shoe flanges against
   the side frame.
4. To release, retract both pressure plates before allowing the hand-driven
   mechanism to return toward OPEN.

## Invariants

- Rod identities, YZ paths, rail geometry and existing motion authority remain
  inherited and unchanged; no cassette feature may steer, synchronize or force
  a path.
- Orange is manually pushed DOWN. Blue and Green are manually pushed
  BACK-TO-FRONT. All three remain manually actuated.
- Both axial sides use X-mirrored modules with three independent rod-end shoes,
  one common pressure plate and one central screw envelope per side.
- Shoes are free in the released state and are compressed together only after
  the user reaches CLAMPED/END.
- Preserve rods exactly `OD4.00 x 50.00`, endpoints `X=+/-25.00`, approximate
  outer faces `X=+/-21.00`, available engagement `3.70`, assumed socket
  `ID4.20`, released axial clearance `0.30`, pressure travel `0.60`, pressure
  plate thickness `3.00`, and side-frame thickness `3.00`.
- The central screw is an M6-like smooth conceptual envelope only. It makes no
  thread, torque, retention, preload or holding-force claim.
- Required previews are exactly `RELEASED_OPEN` and `CLAMPED_END`. Generous YZ
  relief windows may surround inherited endpoint sweeps; they may not replace
  or constrain those sweeps.

## Delta mask

Allowed: remove six cap occurrences; add left/right mirrored side frames,
three independently floating socket shoes per side, common pressure plates,
central smooth screw/knob envelopes, pressure-plate X travel, relief windows,
labels and the two required preview compositions.

Forbidden: rod dimensions or identities; inherited rod-center math, YZ paths,
rails, plates, stepped axle, keepers, XT60/workpiece geometry or motion; any
screw-driven rod motion; cross-linking the three shoes; changing P23 history;
mesh, 3MF, slicing, print preparation or printer work.

## Non-goals and physical unknowns

This iteration does not prove holding force, friction coefficient, screw
threads, torque, back-drive resistance, equal pressure sharing, plate/frame
bending, shoe tilt or escape, socket fit, wear, creep, heat response, vibration,
two-side tightening sequence, assembly/service access, manufacturability or
printability. It does not repair inherited collisions or certify CLAMPED/END as
self-locking. `CLAMPED_END` names geometry and clamp intent only.

## Frozen input manifest

Paths are repository-relative except the two accessible supplied images.

```text
7d7cd580914ce231af11f6156eac1f9dd9f3ae0a474997230baa518a0f610bd1  projects/xt60-bend-jig/docs/REQUIREMENTS.md
54dec75dd5291a4b63b4589cbd61ab403b334a088007d62ab25723dce1a5c3b7  projects/xt60-bend-jig/docs/EXPERIENCE.md
e5f303deaafde4eea78a930ba41c32d97895830244929a114ab1526a3e225019  projects/xt60-bend-jig/docs/iterations/p23-r1-mirrored-screw-clamps/BRIEF.md
f78d26ab0ee09727b07b13616d1b3109a26106f8000f83b5d4a439bdbe48249a  projects/xt60-bend-jig/docs/iterations/p23-r1-mirrored-screw-clamps/DESIGN.md
6852e7fa9ffa39c1495de12df8bf5e5d1ed48ed00dc839dc8094853695eb9298  projects/xt60-bend-jig/docs/iterations/p23-r1-mirrored-screw-clamps/HANDOFF.md
5f92bda26ef931f5a614c02c5b72756b4b39987878f7a1b5db19e49160607a52  projects/xt60-bend-jig/src/xt60_bend_jig/p23_r1_mirrored_screw_clamps.py
aa6b1e00798261ba23a7ddf4f3732d7c47eab60c8271dcb0af1f2f82f6b499ec  /tmp/codex-remote-attachments/01a04e04-6017-7180-b4ff-d6f1035122d2/A60F73F3-477B-4B0B-94E1-34EB29E222D1/1-Pasted-Image-1.jpg
42b47a1abb0782c82e577d7b0e1989f5fbe117a41fd66f3dd5f2fca900791536  /tmp/codex-remote-attachments/01a04e02-3966-7582-b901-eabed005b369/D4FA1FE8-D8DF-4973-B810-D7F054981B97/1-Pasted-Image-1.jpg
```

Any changed manifest byte invalidates dependent P24 gates. The images preserve
inspiration/intent only and supply no dimensions.

## Output paths

- Design records: this `BRIEF.md` and sibling `DESIGN.md`.
- Planned source/test: `src/xt60_bend_jig/p24_r1_manual_three_slider_clamp.py`
  and `tests/test_p24_r1_manual_three_slider_clamp.py`.
- Planned CAD: `cad/p24_r1_manual_three_slider_clamp/` containing explicit
  `p24_r1_released_open.step.py/.step` and
  `p24_r1_clamped_end.step.py/.step` targets.
- Planned independent evidence: sibling `CRITIQUE.md`, `VALIDATION.md`,
  `REVIEW.md`, candidate manifest and snapshots. None exists by this task.

## Task DAG

| ID | Role / owner | Depends on | Exclusive writes | Done gate | Status |
|---|---|---|---|---|---|
| `P24-DESIGN-01` | mechanism designer | frozen inputs | `BRIEF.md`, `DESIGN.md` | selected numeric intent contract, tests and risks | complete |
| `P24-IMPLEMENT-01` | implementer | DESIGN-01 | P24 source, tests, CAD artifacts | both labeled STEP states generated from frozen source | pending |
| `P24-CRITIC-01` | independent critic | IMPLEMENT-01 | `CRITIQUE.md` | operation/topology findings on exact candidate | pending |
| `P24-VALIDATE-01` | independent validator | IMPLEMENT-01 | `VALIDATION.md` | math, constraints, solids, collisions and parity checked | pending |
| `P24-REVIEW-01` | formal reviewer | CRITIC-01, VALIDATE-01 | `REVIEW.md` | first-intent-only disposition on one fingerprint | pending |

Implementer, critic, validator and reviewer must be distinct identities. One
initial implementation plus at most two focused repairs; no downstream print
work is in scope.
