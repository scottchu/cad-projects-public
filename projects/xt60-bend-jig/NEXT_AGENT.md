# Next agent

Read `PROJECT_STATE.md`, `docs/REQUIREMENTS.md`, `docs/EXPERIENCE.md`,
`docs/decisions/README.md`, and every file under the iteration named by
`docs/iterations/CURRENT` before changing this project.

## Resume point

- Active iteration: `p17-r2-balanced-rail-search`.
- Current design result: `P17-D14` bounded infeasibility; no implementation
  candidate.
- Prior review-only contract/candidate: `P17-D13` / `P17-I13`.
- Exact review fingerprint:
  `590e05f90e865f499af83c59350039ce20afc9ccd33bcad1975024aa3fba4b8c`.
- `P17-C13`, `P17-V13`, and `P17-R13`: fidelity/evidence accepted, product and
  merge/release blocked.
- Last accepted mainline candidate: `P17-I08-R2`, fingerprint `f5bc383f...`.
- Source: `src/xt60_bend_jig/p17_r2_direct_counter_twist.py`.
- Tests: `tests/test_p17_r2_direct_counter_twist.py`.
- Full motion:
  `cad/p17_r2_direct_counter_twist/p17_r2_full_motion.step.py`.

Read every file under `docs/iterations/p17-r2-balanced-rail-search/` and the
prior `docs/iterations/p17-r2-locked-rod-layout/` before acting.
The D13 source faithfully materializes the user's frozen rod delta and is
intentionally not product-acceptable: OPEN intersects XT60 and wire, while END
loses all three forming contacts. Do not mistake passing fidelity/export tests
or Viewer readiness for product acceptance.

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

Do not implement the D14 rail-only comparison `C=(4,9.55)`. P17-V14 confirmed
that exact END contact forces `D=(0,0)`, where fixed `A=(-29,12)` leaves only
`1.615172394712 mm` axle/hex-to-bottom-inner-slot web against the `2.20 mm`
gate; this failure is independent of `C`.

Obtain one explicit user scope decision before a new design search: allow the
fixed axle `A` to move, change the fixed-axle/hex guide envelope, or supersede
the exact workpiece/contact placement. Preserve XT60 orientation, rod topology
and identities unless explicitly reopened. Do not merge, slice, print or
release D13/D14 evidence.

Use only Python 3.12 through the root uv workspace. Use the singleton Viewer
managed by `~/.local/bin/cad-viewer`; do not start an ad-hoc competing server.

## Acceptance boundary

D13 implementation fidelity, ten STEP review exports, static/motion packet, and
Viewer HTTP readiness are accepted only as evidence. Product/mechanical/physical
acceptance and PR merge are formally rejected. Interactive slider manipulation,
mesh, DfAM, slicer, 3MF, PETG fit, cap/keeper retention, force, wobble, wire
damage, springback, thermal behavior, endpoint retention, and self-lock remain
unaccepted.
