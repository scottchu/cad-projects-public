# Next agent

Read `PROJECT_STATE.md`, `docs/REQUIREMENTS.md`, `docs/EXPERIENCE.md`,
`docs/decisions/README.md`, and every file under the iteration named by
`docs/iterations/CURRENT` before changing this project.

## Resume point

- Active iteration: `p13-r2-center-hole-fit-repair`.
- Final digital candidate fingerprint:
  `9f123ad24f46d60fcb89ae305455ba1a0c3b38d4738f82766ec91d02c1350db9`.
- Authoritative P13 source:
  `src/xt60_bend_jig/p13_four_plate_three_rod.py`, SHA-256
  `7927bc9bb0d0516faa5410200fc870df408fe16b282c2a226828e712ec801067`.
- Canonical evidence: iteration `VALIDATION.md`, `REVIEW.md`, and `HANDOFF.md`.
- Production 3MF:
  `cad/p13_four_plate_three_rod/p13_print_kit.3mf`, SHA-256
  `588f11e47c89a64221e527085e560453d4e7e75a7b6ecc00cf448f7d22bf75a7`.

## Immediate task

Do not redesign or further enlarge the fit before physical evidence. Reprint
the repaired `left_cam` and `right_actuator` plates and test them with the
unchanged printed shallow-D shaft. Record whether the shaft passes through both
bores by hand without forcing, binding, visible damage, or unacceptable play.
If that focused fit passes, complete the documented P13 assembly, dry-motion,
retention, cycling, wire, heat, removal, cooled-angle, and springback sequence.
Append the observations to `docs/EXPERIENCE.md` and update all three acceptance
layers. If it fails, open a new iteration and preserve this one as history.

## Preserve and do not assume

- Preserve the four-plate/three-purchased-rod architecture, fixed 90-degree
  outcome, three uncut `OD4 x 50 mm` rods, role-specific rod fits, service
  order, and source-defined print orientation.
- The repair changed only the two shared cam D-bore controls to
  `OD5.75 / AF5.30 mm`; the shaft remains `OD5.60 / AF5.15 mm`.
- The final relevant digital suite is `60 passed`; digital acceptance is not
  physical proof.
- Unchanged thin caps and keeper retain conservative generic DfAM warnings and
  should be inspected during the repaired print.
- Use only the root `uv` and npm workspaces. Never edit generated CAD by hand
  or modify legacy source directories.

## Live CAD review

The Viewer was independently confirmed over Tailscale at:

<http://100.70.144.56:3245/Users/scottchu/.codex/worktrees/79caa408-e84c-4bfe-adfd-fa9ba1a1e186/design-projects/projects/xt60-bend-jig?file=cad%2Fp13_four_plate_three_rod%2Fp13_print_kit.step.py>

Viewer restart and artifact-resolution commands are recorded in the active
iteration's `VALIDATION.md` if the current process is no longer running.
