# XT60 bend jig project state

Last updated: `2026-08-24`

## Baseline and active iteration

- Canonical project: `projects/xt60-bend-jig`.
- Development baseline: `05e0152b045bd82a41ea07a715f2361606c1ec99`.
- Active iteration: `p17-r2-direct-cad-counter-twist`.
- Current design contract: `P17-D05`.
- Accepted digital candidate: `P17-I04`.
- Candidate fingerprint:
  `24f5d7524303671a914eec18148b7cee0a8a297cca1403b2c2c68c714fdefabb`.
- Frozen D05 design manifest:
  `64c6db4496520007f4b31c0050809fad29ce949e34e7c806a387107c099946cd`.
- Persisted candidate manifest:
  `cad/p17_r2_direct_counter_twist/p17-r2-candidate-manifest.json`, SHA-256
  `c5fbeaaee626ad3adafb4f2cb5ca195c27e84683c4c4db9b2b27e25fa5241ae2`.
- Canonical handoff:
  `docs/iterations/p17-r2-direct-cad-counter-twist/HANDOFF.md`.

P17 R1 simulator evidence remains rejected. The direct-CAD work is P17 R2;
simulator failure did not invalidate or increment the product version.

## Accepted digital result

The exact P17-I04 candidate preserves the original four-plate plus one-center-
axle architecture and implements:

- two fixed inner guide plates keyed to one stepped hex/round axle;
- two independently counter-rotating outer plates on round journals;
- a larger right primary force plate;
- an offset pivot behind the XT60 body on `-Y`, with the pivot `Z` inside the
  body projection and actual axle/keeper clearance from solder, wire,
  heat-shrink, tool, and removal envelopes;
- true continuous part-local curved cam tracks at `4.20 mm` nominal width for
  `OD4.00 mm` stainless rods, rather than the rejected `4.90/7.55 mm` loose
  endpoint slots;
- six permanent blind-socket caps, straight/curved slot-fit coupons, cap-fit
  coupons, and keeper-retention coupons;
- `OD10.00 / bore7.55` keepers with `1.225 mm` radial wall;
- a same-solid right-inner flexure receiver with closing ramp, throat, hard
  stop, undercut catch, and thumb release;
- fixed-inner service windows and a released-open dogleg extraction path for a
  completed XT60 pigtail;
- no yoke, stability frame/bar, shared outer coupling, or simulator sidecar.

## Independent evidence

- `P17-C04` critic: pass/no blocker for the exact fingerprint.
- `P17-V04` validator: pass for CAD/source and all eight written STEP exports.
- `P17-R04` distinct formal review: pass with bounded acceptance for CAD/source
  and STEP/export only.
- Fingerprint reconstruction: 30 declared paths checked, zero mismatches.
- Focused plus parameter regression: `29 passed`.
- Eight STEP files: topology validation `ok:true`, `failureCount:0`.
- Dense source BREP checks:
  - normal close receiver/nose unintended intersection: `0.0 mm^3`;
  - completed-pigtail dogleg production intersection: zero;
  - minimum service/removal clearance: `0.7764973081 mm`;
  - 65-state keeper/cap maximum intersection: `0.0 mm^3`;
  - minimum keeper/cap gap: `0.1034375039 mm`;
  - cam reconstruction and rod skew: numerical zero;
  - source/export maximum bounds delta: numerical zero.
- Eight final snapshots were generated and inspected, including a distinct
  tight lock close-up.

Formal evidence is recorded in the active iteration `REVIEW.md`,
`VALIDATION.md`, `HANDOFF.md`, and
`cad/p17_r2_direct_counter_twist/p17-r2-artifact-provenance.json`.

## Primary artifacts

- Locked assembly:
  `cad/p17_r2_direct_counter_twist/p17_r2_locked.step`.
- Open, mid, locked, exploded, print-kit, permanent-cap/slot coupon,
  center-axle/keeper coupon, and lock-closeup STEP files are all under
  `cad/p17_r2_direct_counter_twist/`.
- Parametric authority:
  `src/xt60_bend_jig/p17_r2_direct_counter_twist.py`.
- Focused regression:
  `tests/test_p17_r2_direct_counter_twist.py`.

## Acceptance boundary

- CAD/source: accepted for candidate `24f5d752...`.
- Written STEP/export: accepted for the eight recorded artifacts.
- Viewer availability: verified on `2026-08-24`; the exact Tailscale page
  returned HTTP `200` and the final locked STEP returned artifact state
  `ready`.
- Mesh/DfAM/slicer/3MF: not generated or accepted for P17 R2.
- Physical: not accepted. No P17 R2 PETG print or assembly proves slot fit,
  wobble, cap/keeper retention, latch force, release effort, heat, creep, wear,
  vibration, self-lock, solder ergonomics, removal ergonomics, or springback.

## Repository delivery

- Branch: `codex/xt60-p17-r2-direct-cad`.
- Accepted-candidate commit: `ff1351e`.
- Pull request: <https://github.com/scottchu/design-projects/pull/8>.
- The unrelated user-modified legacy P13 `p13_print_kit.3mf` remains outside
  this worktree and was not changed by P17 R2 delivery.

## Open risks

- The closing and release paths depend on modeled PETG flexure. Rigid geometry
  alone intersects during pass-in; real strain, force, creep, heat, vibration,
  and long-term self-lock behavior require physical testing.
- The keeper/cap digital gap is only `0.1034375039 mm`; rubbing and tolerance
  sensitivity remain physical unknowns.
- `4.20 mm` slot fit and real rod wobble/wear require the printed straight and
  curved coupon ladder on the actual rods.
- Permanent cap and keeper press fits require coupon selection before a full
  print.
- No mesh, DfAM, slicer, or printer-profile evidence exists yet.

## Next action

Review and merge PR #8 without changing the accepted design fingerprint. After
delivery, the smallest physical next experiment is the slot/cap/keeper coupon
set before any full assembly print.
