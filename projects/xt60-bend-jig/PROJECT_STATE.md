# XT60 bend jig project state

Last updated: `2026-08-22`

## Baseline

- Canonical project: `projects/xt60-bend-jig`.
- Requested repair baseline: `b0b79253373c7cf80943e99df8ab799958c50d49`.
- Repository workflow baselines integrated without overlap or loss:
  `a5e21e6760d383f900ee30e4457edfb13267e09d` and
  `1484955cc1cfa64164dbdd1ca1222be658933c8e`.
- Supported design: P13 four-plate, three-purchased-rod equal-travel mechanism.
- Authoritative source:
  `src/xt60_bend_jig/p13_four_plate_three_rod.py`, SHA-256
  `7927bc9bb0d0516faa5410200fc870df408fe16b282c2a226828e712ec801067`.

## Active iteration

- Current candidate fingerprint:
  `9f123ad24f46d60fcb89ae305455ba1a0c3b38d4738f82766ec91d02c1350db9`.
- Active iteration: `p13-r2-center-hole-fit-repair`; canonical handoff:
  `docs/iterations/p13-r2-center-hole-fit-repair/HANDOFF.md`.

## Current result

The user's printed "middle stick" is the separate printed shallow-D actuator
shaft (`OD5.60 / AF5.15 mm`). The failed "center hole" is the one repeated
printed interface formed by the matching D bores in `left_cam` and
`right_actuator`. It is not any of the three purchased-rod lanes, fixed C
journals, keeper, or caps.

The smallest source repair enlarged only the named shared cam-D-bore profile:
`cam_d_bore_od 5.70 -> 5.75 mm` and
`cam_d_bore_across_flat 5.25 -> 5.30 mm`. The shaft, three uncut
`OD4.00 x 50.00 mm` rods, architecture, motion/service contract, other fits,
and source-authored print orientation remain unchanged.

## Acceptance state

- CAD/source: accepted by independent critic, validator, and formal reviewer
  for the P13 R2 repaired-print candidate. Focused failing-before/passing-after
  evidence is recorded; the final relevant suite is `60 passed`.
- Written artifact/slicer: accepted for a repaired Snapmaker U1 PETG test
  print. Actual STEP solids, motion/service states, source/export parity,
  snapshots, exact production 3MF integrity/orientation, DfAM, and OrcaSlicer
  2.4.2 were checked. The unchanged thin caps and keeper retain documented
  generic DfAM/manufacturing risks.
- Physical: failed/pending. The latest printed P13 did not assemble at this
  interface. The repaired cams have not yet been printed, fitted, cycled, or
  used; no physical acceptance is claimed.

## Primary release and live review

- Release manifest: `releases/p13-petg-test/release-manifest.json`, SHA-256
  `406325612e34c5c6fce95d96a2fe074591fdf502f592f172c47d016df5a54356`.
- Production 3MF: `cad/p13_four_plate_three_rod/p13_print_kit.3mf`, SHA-256
  `588f11e47c89a64221e527085e560453d4e7e75a7b6ecc00cf448f7d22bf75a7`.
- Primary STEP: `cad/p13_four_plate_three_rod/p13_print_kit.step`, SHA-256
  `5237fe9bc908781ae5793c9ab004f4fc51d24720244b26846bb1dacba63256b7`.
- Tailscale CAD Viewer:
  <http://100.70.144.56:3245/Users/scottchu/.codex/worktrees/79caa408-e84c-4bfe-adfd-fa9ba1a1e186/design-projects/projects/xt60-bend-jig?file=cad%2Fp13_four_plate_three_rod%2Fp13_print_kit.step.py>

## Open risks

- Digital allowance is `0.15 mm` diametral on both D-profile controls, but a
  printed-to-printed fit remains sensitive to seam, elephant foot, shrinkage,
  and orientation.
- CAD lash and hub-wall margins pass but are small; printed play, torque
  transfer, hub cracking, wear, and heat response remain unknown.

## Next action

Reprint the two repaired cam plates, reuse the unchanged printed D shaft, and
first verify hand insertion through both stationary bores without forcing or
damage. If that passes, assemble in the certified service order and run the
complete dry-motion, retention, cycling, wire, heat, removal, cooled-angle, and
springback observation sequence before changing acceptance to physical.
