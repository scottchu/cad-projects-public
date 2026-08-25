# Next agent

Read `PROJECT_STATE.md`, `docs/REQUIREMENTS.md`, `docs/EXPERIENCE.md`,
`docs/decisions/README.md`, and every file under the iteration named by
`docs/iterations/CURRENT` before changing this project.

## Resume point

- Active iteration: `p17-r2-head-up-tail-right-orientation-repair`.
- Contract: `P17-D10-R2`.
- Accepted digital candidate: `P17-I08-R2`; formal gate `P17-R08` ACCEPT.
- Exact fingerprint:
  `f5bc383f6566adf0262a32630792621fd7e5436e780b1b2553b144eb49887ad5`.
- Source: `src/xt60_bend_jig/p17_r2_direct_counter_twist.py`.
- Tests: `tests/test_p17_r2_direct_counter_twist.py`.
- Full motion:
  `cad/p17_r2_direct_counter_twist/p17_r2_full_motion.step.py`.

Distinct `P17-C08`, `P17-V08`, and `P17-R08` accepted the unchanged candidate
for digital CAD/source, ten written STEP exports, frozen visual/motion evidence,
and the recorded acceptance boundaries only.

## Non-negotiable orientation/topology

- Front frame is workpiece-relative: `+Z` is XT60 head/up; `+Y` is tail/wires
  outward-right. Viewer camera pose cannot redefine it.
- OPEN is upper-left -> upper-right -> lower-right with the two right rods on
  one exact vertical leg.
- CLAMPED/END is upper-left -> middle -> lower-right on the accepted diagonal.
- Preserve the identity of all three rods across motion; no crossing or role
  swap. Mirroring/reversing requires an explicit design reopen.

## Accepted mechanism

- Fixed: purple stepped axle at `A=(-29,17)`, both inner plates, both keepers.
- Moving: all three `OD4 x 50 mm` stainless rods and all six permanent caps.
- Rotating: outer plates counter-rotate by `-theta/+theta` around
  `C=(3,12)`, with the right outer plate larger for force input.
- Guides: fixed-inner rod tracks are straight; side-local outer rod/axle rails
  are inverse-transform-derived.
- Travel: OPEN to first contact at `23.4331751998 deg` to END at `24 deg`;
  `0.25 mm` additional displacement is a geometry proxy, not force proof.
- Forbidden: stability bar, yoke, linkage, gear, grip block, replacement lock,
  or any claim that END is self-locking.

## Immediate task

Do not alter the accepted fingerprint during review. The exact persistent
singleton Viewer page is the review surface. If the user authorizes printing,
regenerate from source, run mesh/DfAM/slicer checks, then execute the physical
three-rod/cap/slot experiment in `PROJECT_STATE.md` and the active `HANDOFF.md`.

Use only Python 3.12 through the root uv workspace. Use the singleton Viewer
managed by `~/.local/bin/cad-viewer`; do not start an ad-hoc competing server.

## Acceptance boundary

CAD/source, ten STEP exports, frozen visuals, prescribed motion, and Viewer HTTP
readiness are accepted for `f5bc383f...`. Interactive slider manipulation,
mesh, DfAM, slicer, 3MF, PETG fit, cap/keeper retention, force, wobble, wire
damage, springback, thermal behavior, endpoint retention, and self-lock are not
accepted.
