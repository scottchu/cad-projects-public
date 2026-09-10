# P23 R1 handoff

Date: `2026-08-29`

Disposition: **ACCEPTED FOR USER REVIEW AS AN EVIDENCE-ONLY FIRST-DESIGN
INTENT PREVIEW; NOT PRINT AUTHORITY**

## What this candidate shows

- The six individual rod caps are removed.
- One mirrored side yoke is installed at each X end of the unchanged three
  `OD4 x 50 mm` purchased rods.
- Green reacts in a fixed blind socket, Blue follows its inherited path in a
  retained follower, and Orange moves in a retained rectangular keyed shoe.
- Each side has one fused screw-with-knob context and a captive T-head relation
  that represents positive pull-back toward OPEN without gravity.
- OPEN-to-CLAMPED Orange travel is `12.150910844187 mm`; both sides use the
  same nominal `2.00 mm` pitch and `6.075455422093` turns.

## Frozen repair-cycle-1 candidate

```text
5f92bda26ef931f5a614c02c5b72756b4b39987878f7a1b5db19e49160607a52  src/xt60_bend_jig/p23_r1_mirrored_screw_clamps.py
22596c141bbf2cf7614b9ae8948c68064613e2c1f5935899cfb43104fb4fb7f3  tests/test_p23_r1_mirrored_screw_clamps.py
69c20491b6ee8aac79587c325b418807e9f05afdd2288580da947a1c4a5f7a50  cad/p23_r1_mirrored_screw_clamps/p23_r1_open.step
a4a3133d4ae2bda76b6f67f3ee11e2d648ee0c6c58e84f065b2f8b1cb0933978  cad/p23_r1_mirrored_screw_clamps/p23_r1_clamped.step
9be75b7f1a2b7358a593b675ac0bd7aaebc486e9dc96ba12a6655e57ad8f582c  docs/iterations/p23-r1-mirrored-screw-clamps/VALIDATION.md
7fc620d8baaf3170918f7f05adfb45a5efbe979eb40b90e7ca2e437d59a75850  docs/iterations/p23-r1-mirrored-screw-clamps/REVIEW.md
```

Focused tests pass `11/11`. Both written STEP files contain `20` valid,
closed, positive-volume occurrences. P23-only module collision probes pass at
OPEN, CLAMPED and sampled intermediate states.

Fresh snapshots were forced from the exact written STEP hashes after stale
snapshot-cache evidence was rejected:

```text
3d219b72d85817f69565c4db8f15932acfa2d9b9f37566f6b69e04a436edf6a4  /private/tmp/p23-r1-final-snapshots/open_iso_20260829T161022Z.png
6e1692953b9bda8d3825d250faf52d0652dbfd84c8564513a326d16b522a0e0d  /private/tmp/p23-r1-final-snapshots/clamped_iso_20260829T161024Z.png
```

## Acceptance boundary and next gate

This candidate is not manufacturable or printable authority. OPEN still has
the inherited XT60-reference/Blue-rod overlap of `186.980487360803 mm3`.
Actual thread geometry and tolerance, left/right synchronization, torque,
back-drive holding, wear, binding, wobble, assembly and completed-pigtail
service paths remain unproved.

The next gate is user confirmation of the two side clamps, screw direction,
rod roles and OPEN/CLAMPED relationship. Do not slice or print. After user
intent confirmation, open a separate bounded correction for synchronization
and the inherited XT60/Blue interface before print-readiness work.
