# Next agent

Read `PROJECT_STATE.md`, `docs/REQUIREMENTS.md`, `docs/EXPERIENCE.md`,
`docs/decisions/README.md`, and every file under the iteration named by
`docs/iterations/CURRENT` before changing this project.

## Resume point

- Active iteration: `p17-r2-three-rod-triangle-motion`.
- Contract: `P17-D09-R1`.
- Accepted digital candidate: `P17-I07-R1`; formal gate `P17-R07` ACCEPT.
- Exact independent fingerprint:
  `5965f4e88bc807a1e13ac38c7bc3b342cc285f24a9082c9975dd44000540cb87`.
- Candidate manifest SHA-256:
  `733f11d57aec71f9be8875a8d6ea3196fcc7c4076a673fc5de267c1253686c91`.
- Artifact provenance SHA-256:
  `19e9927cb9d17ef307e96b70eb06600ac5d691d0aa164568d7bddf46b741190c`.
- Source: `src/xt60_bend_jig/p17_r2_direct_counter_twist.py`.
- Tests: `tests/test_p17_r2_direct_counter_twist.py`.
- Full motion:
  `cad/p17_r2_direct_counter_twist/p17_r2_full_motion.step.py`.

Distinct `P17-C07`, `P17-V07`, and `P17-R07` passed the unchanged candidate
for digital CAD/source, ten written STEP exports, frozen visual evidence, and
Viewer transport/readiness only.

## Accepted mechanism

- Fixed: purple stepped axle at `A=(-29,17)`, both inner plates, both keepers.
- Moving: all three `OD4 x 50 mm` stainless rods and all six permanent caps.
- Rotating: left and right outer plates in opposite directions around
  `C=(1.75,6.25)`, with the right outer plate larger for force input.
- Guides: fixed-inner rod tracks are straight; side-local outer tracks and
  axle tracks are inverse-transform-derived for their respective rotations.
- Travel: OPEN to first contact at `23.53125 deg` to END at `24 deg`; the
  first-contact-to-END distance is a `0.25 mm` geometric preload proxy, not
  force proof.
- Removed: green grip tab, obsolete service window, old endpoint lock.
- Forbidden: stability bar, yoke, linkage, gear, extra center bar, replacement
  lock, or any claim that END is self-locking.

## Immediate task

Preserve the exact fingerprint. If the user authorizes printing, regenerate
the print package from source, run mesh/DfAM/slicer checks, and perform the
physical three-rod/cap/slot experiment described in `PROJECT_STATE.md` and the
active `HANDOFF.md`. Do not infer physical acceptance from CAD evidence.

Use only Python 3.12 through the root uv workspace. Use the singleton Viewer
managed by `~/.local/bin/cad-viewer`; do not start an ad-hoc competing server.

## Acceptance boundary

CAD/source, ten STEP exports, frozen visuals, and Viewer HTTP readiness are
accepted for `5965f4e...`. Interactive slider manipulation, mesh, DfAM,
slicer, 3MF, PETG fit, cap/keeper retention, force, wobble, wire damage,
springback, thermal behavior, endpoint retention, and self-lock are not
accepted.
