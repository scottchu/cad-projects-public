# P25 R1 rear-loop / front-pusher clamp handoff

Date: `2026-09-05`

## Disposition

Frozen candidate `a1932fb19ffeb6d584153d1c201ebe24b2e06d6a` is formally
accepted only as a user-facing first-CAD preview. Candidate-manifest file
SHA-256 is
`88fdcd25585c35277d66a769b5c35208f8e5b8c7534d93efdbcb57493638a845`;
its `13/13` entries verify.

This is not manufacturing, slicing, printing, holding-force, spring or
physical-operation authority.

## Frozen operation and topology

1. Thumb manually pushes Orange DOWN.
2. Index and middle fingers manually push Blue and Green BACK-to-FRONT.
3. Only after all three rods reach inherited END, install/close both mirrored
   end modules.
4. Each rear yoke supports Blue and Green together; each hinged front bar
   contacts Orange only.
5. In the neutral latch path a positive barrier retains the bar. Deflecting the
   receiver `1.50 mm` creates the separate collision-free release path.

The three purchased rods remain exactly `OD4.00 x 50.00 mm`. Cap count and
P24 screw-cassette count are zero. P20 rod paths, plates and XT60 geometry are
unchanged.

## Evidence

- Focused P25 tests: `23/23 PASS`.
- Targeted P20 R4 + P24 + P25 tests: `42/42 PASS`.
- Neutral opening encounters a positive barrier from about `0.9 deg`; sampled
  `1..5 deg` positions all have positive-volume retention interference.
- With `1.50 mm` receiver actuation, the sampled `1..60 deg` release path has
  zero positive-volume collision; the `5 deg` gap is `0.737800 mm`.
- Locked tooth engagement projection is `1.20 mm`; the locked assembly has no
  positive-volume interpenetration.
- Three assembled STEP files reopen as `21/21` valid closed solids each;
  exploded STEP reopens as `8/8`. Source/export bounds and volume parity pass.
- Independent critique and validation pass. Formal review verdict is `ACCEPT`
  for first-CAD preview only; see `REVIEW.md`.

## Exact artifacts

- Source: `src/xt60_bend_jig/p25_r1_rear_loop_front_pusher_clamp.py`
- Latched: `cad/p25_r1_rear_loop_front_pusher_clamp/p25_r1_latched_end.step`
- Preclamp: `cad/p25_r1_rear_loop_front_pusher_clamp/p25_r1_preclamp_end.step`
- Released: `cad/p25_r1_rear_loop_front_pusher_clamp/p25_r1_released_clear.step`
- Exploded: `cad/p25_r1_rear_loop_front_pusher_clamp/p25_r1_modules_exploded.step`

## Open risks and next gate

- `opening_spring_*_UNVERIFIED` is only an envelope. Immediate pop-open,
  orientation-independent release and spring selection are unproven.
- Flexure force, strain, fatigue, creep and printed release-tab return are
  unproven.
- Holding force, preload, vibration resistance, axial retention without caps,
  fit/tolerance, wear, saddle/pad fidelity and two-side load equality are
  unproven.
- Inherited P20 RELEASED_OPEN Blue/XT60 collision remains
  `186.980487360803 mm3` and blocks complete-product acceptance.

After user Viewer PASS, the smallest next experiment is one single-side
latch/hinge coupon using the selected material/orientation, a real OD4 rod,
real OD2 hinge pin and actual opening bias. Test retention, approximately
`1.50 mm` release travel, right-side-up/sideways/upside-down opening and 20
cycles before considering a complete two-sided print.
