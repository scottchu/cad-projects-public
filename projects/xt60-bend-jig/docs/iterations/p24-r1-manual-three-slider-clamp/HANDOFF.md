# P24 R1 manual three-slider clamp handoff

Date: `2026-08-30`

## Disposition

P24 R1 is formally accepted only for user review of first-design intent. It
is not manufacturing, slicing, printing, holding-force or physical-operation
authority.

Candidate fingerprint:
`628e365a8b4a08017fbaeebe2bd44d8e5d7b9c57b4e2af21936ba3bdaeae9b91`.
The exact twelve-line manifest is `CANDIDATE.sha256`.

## Intended operation

1. With both side cassettes released, the thumb manually pushes Orange DOWN.
2. Index and middle fingers manually push Blue and Green BACK-to-FRONT.
3. Only after all three rods reach the inherited END pose, each central screw
   moves its common pressure plate axially and sandwiches the three independent
   shoe flanges against the side frame.
4. Reversing each captive screw positively pulls its pressure plate outward
   before the three shoes return along their inherited paths.

The clamp never defines or drives rod YZ motion. Purchased rods remain exactly
`OD4.00 x 50.00 mm`; legacy cap count is zero.

## Evidence

- Focused tests: `13 passed`.
- Both written STEP files: `24` valid, closed, positive-volume occurrences.
- P24-only and P24-versus-context positive-volume collisions: zero in both
  required states.
- Pressure-plate travel: `0.60 mm`; inactive captive endplay: `0.30 mm`.
- Finger-stem exposure: `5.30 mm` released and `5.90 mm` clamped.
- Independent critique: `PASS`, report SHA-256
  `4659e18a775c3394ec5062ef9e209e8dc09085ac298b7519939fc57cc3925abf`.
- Independent validation: `PASS`, report SHA-256
  `45d640bd6f408a7cbd84b6392255ac363bf1342b394936864ff7d0d0ce9f19f8`.
- Formal review: `ACCEPT` for first-design intent only, report SHA-256
  `7c17d2b501d5d81bb66deb632c356357ffe7fe85a356c92a13ffec82dc5d96b5`.

## Review surfaces

- Operation image:
  `cad/p24_r1_manual_three_slider_clamp/p24_r1_operation_annotated.png`.
- Clamp contact image:
  `cad/p24_r1_manual_three_slider_clamp/p24_r1_clamped_contact_annotated.png`.
- RELEASED Viewer source:
  `cad/p24_r1_manual_three_slider_clamp/p24_r1_released_open.step.py`.
- CLAMPED Viewer source:
  `cad/p24_r1_manual_three_slider_clamp/p24_r1_clamped_end.step.py`.

CAD Viewer artifact status was verified `ready` for both generator sources on
`127.0.0.1:3245` before handoff.

## Open blockers and next gate

- Inherited `RELEASED_OPEN` Blue/XT60 intersection remains exactly
  `186.98048736080332 mm3`; this blocks whole-assembly collision and print
  acceptance.
- Real thread geometry, torque, holding force, load sharing, frame/plate
  bending, shoe fit/cocking/rattle, assembly path, two-side tightening order,
  anti-jam release, printability and physical behavior remain unproven.
- Next gate is the user's explicit PASS/FAIL on the operation, shape and side
  cassette concept. Do not slice or print from P24 R1 before that review and a
  separately authorized physical/manufacturing iteration.

## Later printing-profile pointer — 2026-08-31

See [PRINTING_PROFILE.md](../../../PRINTING_PROFILE.md) and the separate
[repository-policy handoff](../../../../../docs/iterations/2026-08-31-printing-profiles/HANDOFF.md).
Only documentation/profile concerns were added. P24 CANDIDATE, frozen BRIEF and
DESIGN, source, tests and artifacts are unchanged; first-intent-only acceptance
and the inherited print blockers above remain in force.
