# XT60 bend jig project state

Last updated: `2026-08-24`

## Baseline and active iteration

- Canonical project: `projects/xt60-bend-jig`.
- Development baseline: `05e0152b045bd82a41ea07a715f2361606c1ec99`.
- Active iteration: `p17-r2-lock-removal`.
- Current design contract: `P17-D08`.
- Accepted digital candidate: `P17-I06-R1`, formally accepted by `P17-R06`.
- Candidate fingerprint:
  `20fc5068814e5c3f5d9c58fdaffbb98bb5dba0eb8b4dffabc7eea59ff3e0cba1`.
- Candidate manifest SHA-256:
  `be993fa2a713abc86895aad95eb670eeb342237ff1e2d8e4799289cf07ef2590`.
- Artifact provenance SHA-256:
  `d51bc72aafffead0360f3e037ac932b8d64dface19a2b00a803093ccaab4b047`.
- Canonical handoff:
  `docs/iterations/p17-r2-lock-removal/HANDOFF.md`.

This is still P17 R2. A product version represents an intentional product
baseline or architecture/interface change; an implementation correction,
Viewer/simulator result, snapshot, export, or validation rerun does not by
itself increment P or R.

## Accepted digital result

The exact P17-I06-R1 candidate preserves the accepted P17 four-plate
architecture and removes the rejected current lock one issue at a time:

- the fixed member is the purple printed one-piece stepped axle at
  `A=(-29.00,17.00) mm`;
- both inner plates and both keepers are world-fixed to that axle;
- all three white `OD4.00 mm` stainless rods remain moving forming rods on
  their frozen paths;
- the two outer plates counter-rotate independently by `-theta/+theta` about
  `C=(-10.60,17.00) mm`;
- each outer plate has a mirrored `7.90 mm` arcuate guide around the eccentric
  fixed axle (`e=18.40 mm`);
- the old decorative opening at `C` is filled;
- the orange right-outer lock nose and its right-inner receiver counterpart
  are completely removed, with no replacement catch, stop, bridge, bar, or
  linkage;
- the green left-outer finger/force grip remains; it is not lock geometry;
- `32 deg` is end-of-travel only and the Viewer exposes one `open_to_end`
  control, with no retention or self-lock claim;
- the physical stainless stock is `50.00 mm`, while the current CAD rod target
  remains `40.60 mm`; deciding whether to use uncut stock is still pending;
- the purple axle remains `34.90 mm`, spanning the `32.00 mm` plate stack plus
  `1.45 mm` each side for keeper clearance/seat;
- no stability bar, yoke, boss, linkage, separate pivot part, frame, or shared
  outer coupling was added;
- legacy XT60 reference and white-rod-path issues were deliberately not
  redesigned in this focused repair.

## Independent evidence

- `P17-C06-R1` distinct critic: pass/no blocker for the exact fingerprint.
- `P17-V06-R1` distinct validator: pass for digital CAD/source and written
  STEP/export.
- `P17-R06` distinct formal reviewer: accept for digital CAD/export and live
  preview delivery with physical boundaries preserved.
- Full focused test file: `33 passed`.
- Nine retained STEP exports: every `inspect validate` result was `ok:true` with
  `failureCount:0`; source/export occurrence, topology, and bounds parity
  passed.
- All nine STEP and seven selected PNG/GIF hashes matched provenance; the
  semantic repair left every STEP and visual hash byte-identical.
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
- Open, mid, legacy-named `locked` (end-of-travel), exploded, print-kit, cap
  coupon, center-axle coupon, and both motion STEP exports are under
  `cad/p17_r2_direct_counter_twist/`.
- The obsolete lock-closeup generator/export was deleted.
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

- CAD/source: accepted for fingerprint `20fc5068...`.
- Written STEP/export: accepted for the nine provenance-recorded artifacts.
- Live preview: accepted for user visual review.
- Mesh/DfAM/slicer/3MF: not generated or accepted for this repair.
- Physical: not accepted. The `7.90 mm` guide around the `7.60 mm` axle
  journal leaves `0.150 mm` radial running clearance and `1.050 mm` keeper
  capture; PETG fit, friction, force, wobble, backlash, wear, retention,
  endpoint retention, heat, creep, vibration, solder ergonomics, and durability
  require physical evidence. The physical `50.00 mm` rod-stock decision also
  remains open.

## Repository delivery

- Branch: `codex/xt60-p17-r2-direct-cad`.
- Pull request: <https://github.com/scottchu/design-projects/pull/8>.
- The unrelated user-modified legacy P13 `p13_print_kit.3mf` remains in the
  canonical main checkout and was not changed by this worktree.

## Next action

Deliver the exact focused Viewer URL for user visual review. Do not change the
accepted fingerprint while collecting feedback. The next one-at-a-time design
decision is separate: keep the green force grip or remove it, decide whether
the physical `50.00 mm` stainless stock must remain uncut, or physically test
the `34.90 mm` axle/keeper engagement. Do not combine those decisions or
silently change rod paths, axle geometry, or the XT60 reference.
