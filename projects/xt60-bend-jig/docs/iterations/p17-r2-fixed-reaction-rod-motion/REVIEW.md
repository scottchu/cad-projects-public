# P17 R2 fixed stepped-axle guide review

Status: `P17-C05` and `P17-R05` pass for exact candidate fingerprint
`b4ad7e49b198c189c5a32fdeecef7cf231b0306ef26d2404ae662711b22ff5b5`.

## Critic gate `P17-C05`

Owner: `/root/p17_critic`, distinct from design, implementation, validation,
and formal review.

Verdict: pass/no blocker for the unchanged fingerprint. The critic
independently reconstructed all declared hashes, ran the focused `8 passed`
and full-file `31 passed` regressions, probed the 66 closure rows, validated
representative STEP exports, and inspected PNG/GIF motion evidence.

Confirmed:

- the fixed member is the purple printed stepped axle;
- both inner plates and keepers remain world-fixed;
- all three white stainless rods remain moving forming/locking rods;
- the blue/green outer plates counter-rotate about `C` through mirrored axle
  guides while `A` remains fixed;
- the old decorative hole at `C` is filled and no bar, yoke, boss, linkage, or
  shared outer coupling was added;
- legacy XT60/white-rod issues were not silently redesigned in this one-at-a-
  time repair.

Nonblocking physical risks: `7.90 mm` guide width around the `7.60 mm` journal
leaves `0.150 mm` radial running clearance, and keeper capture is `1.050 mm`.
PETG fit, friction, backlash, wear, force transmission, wobble, and retention
remain physical unknowns. The nominal local-rank closure proof is not a claim
that a pin and slot alone form a revolute joint.

## Formal review gate `P17-R05`

Owner: `/root/p17_formal_review`, distinct from critic, implementation, and
validation.

Verdict: ACCEPT the exact fingerprint for digital CAD/source, written
STEP/export, and live preview delivery. The reviewer verified the P17 hashes,
joined the C05 and V05 evidence, inspected the motion packet, and accepted the
singleton Viewer delivery including its preserved V02 failure and repaired V03
pass.

Acceptance does not include mesh, DfAM, slicer, 3MF, PETG print, keeper/cap
fit, force, strain, creep, heat, vibration, self-lock, wear, springback,
solder ergonomics, or completed physical assembly. Any source, test, motion
sidecar, STEP, or selected review-artifact change invalidates this exact
fingerprint and dependent gates.
