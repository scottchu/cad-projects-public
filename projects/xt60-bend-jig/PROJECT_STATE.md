# XT60 bend jig project state

Last updated: `2026-08-24`

## Baseline and active iteration

- Canonical project: `projects/xt60-bend-jig`.
- Development baseline: `05e0152b045bd82a41ea07a715f2361606c1ec99`.
- Active iteration: `p17-r2-fixed-reaction-rod-motion`.
- Current design contract: `P17-D07`.
- Accepted digital candidate: `P17-I05`, formally accepted by `P17-R05`.
- Candidate fingerprint:
  `b4ad7e49b198c189c5a32fdeecef7cf231b0306ef26d2404ae662711b22ff5b5`.
- Candidate manifest SHA-256:
  `df92325baba8d39f8f511819c93467ac3cf8c5c4535bbde762755889acccddc8`.
- Artifact provenance SHA-256:
  `4de4d236f67729b142b0ae0752ef41fe3087a9c191890947695f7ff72dc4be37`.
- Canonical handoff:
  `docs/iterations/p17-r2-fixed-reaction-rod-motion/HANDOFF.md`.

This is still P17 R2. A product version represents an intentional product
baseline or architecture/interface change; an implementation correction,
Viewer/simulator result, snapshot, export, or validation rerun does not by
itself increment P or R.

## Accepted digital result

The exact P17-I05 candidate preserves the P17 four-plate architecture and
repairs the fixed-member identity one issue at a time:

- the fixed member is the purple printed one-piece stepped axle at
  `A=(-29.00,17.00) mm`;
- both inner plates and both keepers are world-fixed to that axle;
- all three white `OD4.00 mm` stainless rods remain moving forming/locking
  rods on their frozen paths;
- the two outer plates counter-rotate independently by `-theta/+theta` about
  `C=(-10.60,17.00) mm`;
- each outer plate has a mirrored `7.90 mm` arcuate guide around the eccentric
  fixed axle (`e=18.40 mm`);
- the old decorative opening at `C` is filled;
- no stability bar, yoke, boss, linkage, separate pivot part, frame, or shared
  outer coupling was added;
- legacy XT60 reference and white-rod-path issues were deliberately not
  redesigned in this focused repair.

## Independent evidence

- `P17-C05` distinct critic: pass/no blocker for the exact fingerprint.
- `P17-V05` distinct validator: pass for digital CAD/source and written
  STEP/export.
- `P17-R05` distinct formal reviewer: accept for digital CAD/export and live
  preview delivery with physical boundaries preserved.
- Focused regressions: `8 passed`; full focused test file: `31 passed`.
- Ten STEP exports: every `inspect validate` result was `ok:true` with
  `failureCount:0`; source/export occurrence, topology, and bounds parity
  passed.
- All ten STEP, four motion source/sidecar, eleven PNG, and two 72-frame GIF
  hashes matched provenance.
- Closure: 66 side/state rows, rank 3; maximum residual `3.43e-15 mm`;
  maximum perturbed pose error `7.31e-12`.
- Actual solids: exact frozen-feature gap `3.6500 mm`; minimum analytic web
  `3.84868 mm`; inner/left/right boundary webs
  `3.8946/7.650/9.150 mm`; sampled service clearance `19.1764973 mm`; all
  sampled unintended-intersection gates clear.
- Visual review confirmed fixed purple axle/keepers/inners, opposite outer
  rotation, moving white rods in the full assembly, filled `C`, and no added
  structure.

## Primary artifacts

- Focused visible motion:
  `cad/p17_r2_direct_counter_twist/p17_r2_fixed_axle_motion.step.py`.
- Full-assembly visible motion:
  `cad/p17_r2_direct_counter_twist/p17_r2_full_motion.step.py`.
- Open, mid, locked, exploded, print-kit, lock-closeup, cap coupon, center-axle
  coupon, and both motion STEP exports are under
  `cad/p17_r2_direct_counter_twist/`.
- Parametric authority:
  `src/xt60_bend_jig/p17_r2_direct_counter_twist.py`.
- Focused regression:
  `tests/test_p17_r2_direct_counter_twist.py`.

## Viewer delivery

- Per-user singleton service: `com.scottchu.cad-viewer` on
  `127.0.0.1:3245`.
- Stable lifecycle command: `~/.local/bin/cad-viewer`.
- Installed payload digest:
  `9ae1b0eb9651d7fbd589c50108cb8be08efbed31ed3d0ac55af25c9dcc61ab0e`.
- Canonical Viewer Python:
  `/Users/scottchu/Projects/personal/design-projects/.venv/bin/python3`.
- Exact focused Tailscale page returned HTTP `200`; exact artifact state was
  `ready`; its descriptor, motion module, and component GLB each returned HTTP
  `200` locally and through Tailscale.
- Viewer V02 failure and V03 repair/pass are preserved in
  `tools/cad-viewer-service/VALIDATION.md`.

## Acceptance boundary

- CAD/source: accepted for fingerprint `b4ad7e49...`.
- Written STEP/export: accepted for the ten provenance-recorded artifacts.
- Live preview: accepted for user visual review.
- Mesh/DfAM/slicer/3MF: not generated or accepted for this repair.
- Physical: not accepted. The `7.90 mm` guide around the `7.60 mm` axle
  journal leaves `0.150 mm` radial running clearance and `1.050 mm` keeper
  capture; PETG fit, friction, force, wobble, backlash, wear, retention,
  self-lock, heat, creep, vibration, solder ergonomics, and durability require
  physical evidence.

## Repository delivery

- Branch: `codex/xt60-p17-r2-direct-cad`.
- Pull request: <https://github.com/scottchu/design-projects/pull/8>.
- The unrelated user-modified legacy P13 `p13_print_kit.3mf` remains in the
  canonical main checkout and was not changed by this worktree.

## Next action

Deliver the exact focused Viewer URL for user visual review. Do not change the
accepted fingerprint while collecting feedback. If the user accepts this
fixed-axle step and authorizes printing, the smallest physical experiment is a
PETG axle-guide/keeper coupon before a full assembly. If the user instead
chooses the next visible issue, open a new bounded iteration without silently
changing white-rod paths or the XT60 reference in this accepted candidate.
