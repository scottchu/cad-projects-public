# Next agent

Read `PROJECT_STATE.md`, `docs/REQUIREMENTS.md`, `docs/EXPERIENCE.md`,
`docs/decisions/README.md`, and every file under the iteration named by
`docs/iterations/CURRENT` before changing this project.

## Resume point

- Active iteration: `p17-r2-direct-cad-counter-twist`.
- Current contract: `P17-D05`.
- Accepted digital candidate: `P17-I04`.
- Exact fingerprint:
  `24f5d7524303671a914eec18148b7cee0a8a297cca1403b2c2c68c714fdefabb`.
- Candidate manifest:
  `cad/p17_r2_direct_counter_twist/p17-r2-candidate-manifest.json`, SHA-256
  `c5fbeaaee626ad3adafb4f2cb5ca195c27e84683c4c4db9b2b27e25fa5241ae2`.
- Source:
  `src/xt60_bend_jig/p17_r2_direct_counter_twist.py`.
- Tests:
  `tests/test_p17_r2_direct_counter_twist.py`.
- Artifact provenance:
  `cad/p17_r2_direct_counter_twist/p17-r2-artifact-provenance.json`.
- Canonical implementation and decision history:
  `docs/iterations/p17-r2-direct-cad-counter-twist/HANDOFF.md`.

Independent `P17-C04`, `P17-V04`, and formal `P17-R04` all pass the exact
fingerprint for CAD/source and written STEP/export only.

## Immediate task

Repository delivery is open as PR #8:
<https://github.com/scottchu/design-projects/pull/8>, from branch
`codex/xt60-p17-r2-direct-cad`; accepted-candidate commit `ff1351e`. Review and
merge it without changing the accepted fingerprint. The exact Tailscale Viewer
page and final locked artifact were verified HTTP `200` / state `ready` on
`2026-08-24`; reverify only if the backend, path, or artifact changes. Do not
redesign or increment the P-version for delivery-only work.

If PR #8 is merged and the user asks to proceed toward printing, run the
smallest falsifiable physical workflow first:

1. create/validate the mesh or 3MF only from authoritative source;
2. perform DfAM and slicer validation with the actual printer/material profile;
3. print the straight/curved `4.10..4.30 mm` slot ladder plus cap and keeper
   fit coupons;
4. record actual rod fit, wobble, cap insertion, keeper retention, and PETG
   latch force before a full assembly print.

## Preserve

- P17 R2 identity and the recorded version semantics. Simulation status is an
  evidence layer, not a version trigger.
- Four plates: inner pair fixed, outer pair independently counter-rotating.
- One offset stepped axle: central spacer and inner hex keys, outer round
  journals, retained keepers.
- Pivot behind XT60 on `-Y`, away from solder/wire/service envelopes.
- `4.20 mm` continuous curved production slots and coupon ladder; never restore
  the rejected `4.90/7.55 mm` loose slots.
- Larger right force plate, six permanent caps, real release path, service
  windows, and dogleg pigtail removal.
- No yoke/stability bars, shared outer coupling, simulator sidecar, or
  unnecessary new structure.
- Parametric source is authoritative; never hand-edit STEP/mesh/3MF outputs.

## Acceptance boundary

- CAD/source and the eight written STEP files: accepted for fingerprint
  `24f5d752...`.
- Viewer: only claim ready after exact page HTTP `200` and exact artifact state
  `ready` are verified in the current session.
- Mesh/DfAM/slicer/3MF: pending.
- Physical: pending. Do not describe flexure lock, keeper/cap retention, slot
  fit, wobble, heat, wear, vibration, solder/removal ergonomics, springback, or
  self-lock as proven.

The canonical `main` checkout contains a user-modified legacy P13
`p13_print_kit.3mf`. It is unrelated to P17 R2 and must remain untouched.
