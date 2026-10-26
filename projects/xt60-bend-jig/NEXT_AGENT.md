# Next agent

Current task is the [offline rail customizer recovery](docs/iterations/2026-10-26-rail-customizer-recovery/HANDOFF.md).
Start there, then its BRIEF, DESIGN, VALIDATION and REVIEW. Open
`preview/xt60-rail-customizer.html`; edit `preview/rail-customizer/` and rebuild
with the documented npm command. Both OPEN and END editing are required.
P19 stays the accepted digital baseline. P25 state below is preserved mechanism
history, not the active simulator task. Do not regenerate CAD for this recovery.

## Preserved P25 restart route

Read `PROJECT_STATE.md`, `docs/REQUIREMENTS.md`, `docs/EXPERIENCE.md`,
`docs/decisions/README.md`, then every file under
`docs/iterations/p25-r1-rear-loop-front-pusher-clamp/` before changing this
project. Also read the delivery records under
`../../docs/iterations/2026-09-10-local-work-delivery/`.

## Exact resume point

- Prior mechanism iteration: `p25-r1-rear-loop-front-pusher-clamp`.
- Frozen first-CAD candidate: `a1932fb19ffeb6d584153d1c201ebe24b2e06d6a`.
- Candidate-manifest file SHA-256:
  `88fdcd25585c35277d66a769b5c35208f8e5b8c7534d93efdbcb57493638a845`
  (`13/13`).
- Formal disposition: user-facing first-CAD preview only. It is not a print
  candidate or physical acceptance.
- P19 R1 remains the latest accepted digital mechanism baseline. P17-P24 are
  preserved history with the exact status in their own records; they are not
  parallel current iterations.

## Preserve

- Manual force topology: Orange DOWN; Blue and Green BACK-to-FRONT; clamps act
  only at inherited END.
- Two mirrored P25 modules, Blue+Green rear yoke, Orange-only front bar,
  `OD4 x 50 mm` rods, zero caps, zero screw cassette, and inherited P20
  paths/plates/XT60 geometry.
- The P20 R4 print-kit source hash guard and its two known historical drift
  failures. Do not weaken the guard or relabel the old fingerprint as current.
- Separate source/CAD, written-artifact, slicer, and physical acceptance.

## Next smallest action

Complete delivery-candidate review without regenerating CAD. Product work then
awaits explicit user PASS/FAIL on P25. A later physical gate, if authorized, is
one single-side latch/hinge coupon with a real OD4 rod, OD2 hinge pin, and real
opening bias; do not proceed directly to a complete print.
