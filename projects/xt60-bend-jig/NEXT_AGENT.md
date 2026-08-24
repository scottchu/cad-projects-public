# Next agent

Read `PROJECT_STATE.md`, `docs/REQUIREMENTS.md`, `docs/EXPERIENCE.md`,
`docs/decisions/README.md`, and every file under the iteration named by
`docs/iterations/CURRENT` before changing this project.

## Resume point

- Active iteration: `p17-r2-lock-removal`.
- Contract: `P17-D08`.
- Accepted digital candidate: `P17-I06-R1`; formal gate `P17-R06` ACCEPT.
- Exact fingerprint:
  `20fc5068814e5c3f5d9c58fdaffbb98bb5dba0eb8b4dffabc7eea59ff3e0cba1`.
- Candidate manifest SHA-256:
  `be993fa2a713abc86895aad95eb670eeb342237ff1e2d8e4799289cf07ef2590`.
- Artifact provenance SHA-256:
  `d51bc72aafffead0360f3e037ac932b8d64dface19a2b00a803093ccaab4b047`.
- Source: `src/xt60_bend_jig/p17_r2_direct_counter_twist.py`.
- Tests: `tests/test_p17_r2_direct_counter_twist.py`.
- Focused motion:
  `cad/p17_r2_direct_counter_twist/p17_r2_fixed_axle_motion.step.py`.
- Full motion:
  `cad/p17_r2_direct_counter_twist/p17_r2_full_motion.step.py`.

Distinct `P17-C06-R1`, `P17-V06-R1`, and `P17-R06` all pass the unchanged candidate
for digital CAD/source, written STEP/export, and live preview delivery only.

## What is fixed and what moves

- Fixed: purple printed stepped axle, both keepers, both inner plates.
- Moving: all three white stainless forming rods and their caps.
- Rotating: left and right outer plates in opposite directions around `C`,
  constrained by mirrored guides around fixed eccentric axle `A` plus the
  unchanged white-rod contact network.
- Forbidden in this candidate: stability bar, yoke, boss, linkage, separate
  pivot, frame, shared outer coupling, decorative hole at `C`, or silent
  redesign of frozen white-rod paths/XT60 reference.
- Removed: the right-outer orange lock nose and the complete right-inner
  receiver; there is no replacement lock or endpoint-retention claim.
- Preserved: the green left-outer finger/force grip circled in the user's
  second screenshot; it is not lock geometry.

## Immediate task

Keep the exact fingerprint unchanged and collect the user's visual review from
the focused Viewer motion. The singleton service is already installed and is
managed through `~/.local/bin/cad-viewer`; do not launch an ad-hoc competing
Viewer. Exact page/artifact/descriptor/module/component readiness was accepted
by R06 and must be reverified if the path, backend, source, or artifact changes.

Do not proceed to mesh, 3MF, slicer, or a full print without explicit user
authorization. The physical stainless stock is `50.00 mm`, while the current
CAD rods remain `40.60 mm`; that mismatch is unresolved. The purple axle is
`34.90 mm` and reaches `1.45 mm` beyond each outer plate, but fit, stiffness,
and keeper retention remain physical unknowns.

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

CAD/source, nine STEP exports, and live preview are digitally accepted for
`20fc5068...`. Physical force, friction, fit, wobble, backlash, PETG tolerance,
keeper retention, endpoint retention, heat, wear, vibration, solder/removal
ergonomics, the 50 mm stock decision, mesh, DfAM, slicer, and 3MF remain
unaccepted.
