# XT60 bend jig project state

Last updated: `2026-08-25`

## Baseline and active iteration

- Canonical project: `projects/xt60-bend-jig`.
- Active iteration: `p17-r2-three-rod-triangle-motion`.
- Current design contract: `P17-D09-R1`.
- Accepted digital candidate: `P17-I07-R1`, formally accepted by `P17-R07`.
- Independent candidate fingerprint:
  `5965f4e88bc807a1e13ac38c7bc3b342cc285f24a9082c9975dd44000540cb87`.
- Candidate manifest SHA-256:
  `733f11d57aec71f9be8875a8d6ea3196fcc7c4076a673fc5de267c1253686c91`.
- Artifact provenance SHA-256:
  `19e9927cb9d17ef307e96b70eb06600ac5d691d0aa164568d7bddf46b741190c`.
- Canonical handoff:
  `docs/iterations/p17-r2-three-rod-triangle-motion/HANDOFF.md`.

This remains P17 R2. A product version identifies an intentional product
baseline, mechanism architecture, or external-interface change. A focused
repair, Viewer/simulation outcome, export, snapshot, or validation rerun does
not by itself increment P or R.

## Accepted digital result

P17-I07-R1 is the source-derived four-plate, three-rod counter-twist candidate:

- exactly three moving `OD4.00 x 50.00 mm` stainless rods and six permanent
  stepped blind caps;
- both inner plates, both keepers, and the purple stepped axle at
  `A=(-29.00,17.00) mm` remain world-fixed;
- the left and right outer plates rotate independently by `-theta/+theta`
  about `C=(1.75,6.25) mm`, with the right force side larger;
- all fixed-inner rod guides are direct straight tracks; all six outer rod
  rails and both axle rails are derived by inverse transform, not redrawn;
- the numeric OPEN, first-contact, and END triangles use `S_open=12.80 mm`,
  first contact at `23.53125 deg`, and END at `24 deg`;
- the plate diameters are `80/82/85 mm`, moving slots are `4.15 mm`, and the
  geometric END preload proxy is `0.25 mm` on each insulated wire;
- the redundant green grip and obsolete inner service-window cutter are
  removed; there is no stability bar, yoke, linkage, gear, centered
  replacement bar, lock, or self-lock feature;
- the five-waypoint completed-pigtail service path is explicit and was checked
  with actual solids after reverse opening.

The production source retains legacy internal `locked`/`theta_lock_deg` names
only for compatibility; they mean END of prescribed travel and do not claim
retention.

## Independent evidence

- `P17-C07`: PASS/no blocker or major finding for the exact fingerprint.
- `P17-V07`: PASS for CAD source, ten written STEP exports, frozen visual
  evidence, and singleton Viewer HTTP readiness.
- `P17-R07`: ACCEPT for delivery of the unchanged candidate.
- Focused tests: `18 passed` through the root `uv` environment.
- All ten written STEP exports validated with zero geometry failures and
  passed source/export topology, occurrence, bounds, and volume parity.
- Across 65 motion states: minimum rail crossing sine `0.10202`, maximum
  normalized constraint condition `9.64043`, rank `3`, minimum actual web
  `2.66759 mm`, and zero unintended intersections.
- The full service sweep evaluated `4004` actual-solid poses and retained
  `0.84675 mm` minimum clearance with zero intersection.
- Frozen OPEN/contact/END/opposite snapshots and the 72-frame motion GIF were
  visually inspected. The opposite END view can visually merge two caps, but
  source and occurrence evidence independently prove three rods and six caps.

## Primary artifacts

- Parametric authority:
  `src/xt60_bend_jig/p17_r2_direct_counter_twist.py`.
- Focused regression:
  `tests/test_p17_r2_direct_counter_twist.py`.
- Full motion:
  `cad/p17_r2_direct_counter_twist/p17_r2_full_motion.step.py`.
- Focused motion:
  `cad/p17_r2_direct_counter_twist/p17_r2_fixed_axle_motion.step.py`.
- OPEN, contact, midpoint, END, exploded, print-kit, cap coupon, axle coupon,
  and both motion STEP exports are under
  `cad/p17_r2_direct_counter_twist/`.

## Viewer delivery

- Singleton per-user service: `com.scottchu.cad-viewer` on
  `127.0.0.1:3245`, managed by `~/.local/bin/cad-viewer`.
- Installed self-healing payload digest:
  `4e89ad3d2efce80b2381e439c43af0623245d1c2443fca5ea0fb24b10bb72988`.
- CAD Python is the repository root uv interpreter; no project-local Python
  environment is permitted.
- The exact local and Tailscale pages, artifact endpoint, assembly descriptor,
  singular `open_to_end` module, all ten GLBs, and all six static assets
  returned HTTP `200`; the artifact reported `state: ready`.
- Live browser slider manipulation was not independently exercised. Frozen
  GIF motion and Viewer transport/readiness are accepted separately.

## Acceptance boundary

- CAD/source: accepted for exact fingerprint `5965f4e...`.
- Written STEP/export: accepted for the ten provenance-recorded exports.
- Frozen visual and Viewer transport/readiness: accepted.
- Mesh/DfAM/slicer/3MF: not generated or accepted for P17-I07-R1.
- Physical: not tested or accepted. PETG slot fit, permanent-cap and keeper
  retention, hand torque, real preload/holding force, wobble, insulation
  marking/safety, soldering heat, cooled bend angle, springback, creep, wear,
  vibration, endpoint retention, and self-lock remain physical gates.

## Repository delivery

- Branch: `codex/xt60-p17-r2-direct-cad`.
- Pull request: <https://github.com/scottchu/design-projects/pull/8>.
- The unrelated user-modified legacy P13 `p13_print_kit.3mf` in the canonical
  main checkout remains outside this worktree and must not be overwritten.

## Next action

Do not change the accepted fingerprint while reviewing it. The smallest next
experiment is a user-authorized P17-I07-R1 print package followed by the
documented three-rod/cap/slot physical test. Record first contact, END effort,
rod wobble, wire marks, XT60 reaction, cap/keeper retention, removal path, and
cooled bend angle. Do not claim a physical lock: this candidate intentionally
contains none.
