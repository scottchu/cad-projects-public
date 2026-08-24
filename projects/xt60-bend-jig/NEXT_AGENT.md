# Next agent

Read `PROJECT_STATE.md`, `docs/REQUIREMENTS.md`, `docs/EXPERIENCE.md`,
`docs/decisions/README.md`, and every file under the iteration named by
`docs/iterations/CURRENT` before changing this project.

## Resume point

- Active iteration: `p17-r2-fixed-reaction-rod-motion`.
- Contract: `P17-D07`.
- Accepted digital candidate: `P17-I05`; formal gate `P17-R05` ACCEPT.
- Exact fingerprint:
  `b4ad7e49b198c189c5a32fdeecef7cf231b0306ef26d2404ae662711b22ff5b5`.
- Candidate manifest SHA-256:
  `df92325baba8d39f8f511819c93467ac3cf8c5c4535bbde762755889acccddc8`.
- Artifact provenance SHA-256:
  `4de4d236f67729b142b0ae0752ef41fe3087a9c191890947695f7ff72dc4be37`.
- Source: `src/xt60_bend_jig/p17_r2_direct_counter_twist.py`.
- Tests: `tests/test_p17_r2_direct_counter_twist.py`.
- Focused motion:
  `cad/p17_r2_direct_counter_twist/p17_r2_fixed_axle_motion.step.py`.
- Full motion:
  `cad/p17_r2_direct_counter_twist/p17_r2_full_motion.step.py`.

Distinct `P17-C05`, `P17-V05`, and `P17-R05` all pass the unchanged candidate
for digital CAD/source, written STEP/export, and live preview delivery only.

## What is fixed and what moves

- Fixed: purple printed stepped axle, both keepers, both inner plates.
- Moving: all three white stainless forming/locking rods and their caps.
- Rotating: left and right outer plates in opposite directions around `C`,
  constrained by mirrored guides around fixed eccentric axle `A` plus the
  unchanged white-rod contact network.
- Forbidden in this candidate: stability bar, yoke, boss, linkage, separate
  pivot, frame, shared outer coupling, decorative hole at `C`, or silent
  redesign of frozen white-rod paths/XT60 reference.

## Immediate task

Keep the exact fingerprint unchanged and collect the user's visual review from
the focused Viewer motion. The singleton service is already installed and is
managed through `~/.local/bin/cad-viewer`; do not launch an ad-hoc competing
Viewer. Claim readiness only after exact page HTTP `200`, exact artifact state
`ready`, and descriptor/module/component assets HTTP `200` are reverified if
the path, backend, or artifact changes.

Do not proceed to mesh, 3MF, slicer, or a full print without explicit user
authorization. If authorized, test a PETG axle-guide/keeper coupon first: the
nominal radial running clearance is only `0.150 mm` and keeper capture is
`1.050 mm`.

## Preserve

- P17 R2 version identity; simulation/viewer/export status is evidence, not a
  version trigger.
- Four plates; inner pair fixed; outer pair independently counter-rotating.
- Purple printed stepped axle as the fixed reaction member at
  `A=(-29.00,17.00)`; outer rotation datum `C=(-10.60,17.00)`.
- All three white rods remain moving on the frozen P17 paths.
- Parametric source remains authoritative; never hand-edit STEP/mesh/3MF.
- Legacy P13 user-modified `p13_print_kit.3mf` in canonical main remains
  untouched.

## Acceptance boundary

CAD/source, ten STEP exports, and live preview are digitally accepted for
`b4ad7e49...`. Physical force, friction, fit, wobble, backlash, PETG tolerance,
keeper retention, self-lock, heat, wear, vibration, solder/removal ergonomics,
mesh, DfAM, slicer, and 3MF remain unaccepted.
