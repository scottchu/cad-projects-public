# XT60 bend jig project state

Last updated: `2026-08-22`

## Baseline

- Canonical project path: `projects/xt60-bend-jig`
- Migration source: `/Users/scottchu/Projects/personal/3d-print-xt60-restart/design/xt60-bend-jig`
- Source parent revision: `96b055d4b8d0b87f3e6132fa3d90b23b3be4ed84`; the legacy project directory itself was untracked.
- Authoritative P13 source: `src/xt60_bend_jig/p13_four_plate_three_rod.py`
- Source SHA-256 at import: `e424fac8064d35713ed15748bb8a0e1f966ef429b507ba4be5a5dc31cfc7c72b`
- Supported prototype: P13 four-plate, three-rod equal-travel mechanism.
- Earlier P0–P12 concepts and P14–P16 calibration coupons are retained as history or supporting evidence, not alternative current releases.

## Active iteration

- Iteration ID: `p13-r1-monorepo-migration`
- Iteration handoff: `docs/iterations/p13-r1-monorepo-migration/HANDOFF.md`
- Status: complete; the next agent must open `p13-r2-center-hole-fit-repair` before changing geometry.

## Acceptance state

- CAD/source: migrated P13 source reproduced in the root workspace. The 59 focused P13 tests pass, and the current print-kit, motion assembly, and 3.8 mm coupon solids pass topology/closure/orientation/positive-volume validation.
- Written artifact/slicer: current P13 STEP/3MF/provenance outputs were regenerated from source and passed 3MF manifold/orientation/lib3mf checks. Historical OrcaSlicer evidence was retained, but no fresh slicer acceptance is claimed after regeneration.
- Physical: failed center-hole fit on the latest print—the user's "middle stick" is too thick for the center hole. Exact interface identification and a focused source repair are pending in the next iteration; the rest of the complete P13 physical acceptance sequence also remains pending.

## Open risks and unknowns

- The initial complete Python run reported `396 passed, 8 skipped, 14 failed`. Seven P13 failures were cleared by generating the deliberately excluded current outputs; seven P2–P6 historical export tests still assume generated files that were absent from the transfer source and are not P13 migration regressions.
- The simulator contract suite and production bundle pass. Fresh browser visual review remains pending because no controllable in-app browser runtime was attached.
- Legacy `cadgen==0.4.15` is intentionally preserved for baseline reproduction while the installed CAD skill runtime is newer.
- "Middle stick" and "center hole" must be mapped to exact printed parts before changing a dimension; do not enlarge every rod or shaft bore.
- Printed actuation, PETG stiffness, creep, heat response, insulation marking, cap retention, removal, and cooled springback remain unknown.

## Next action

- Open `p13-r2-center-hole-fit-repair` in a fresh worktree. Identify the failed center interface, add a defect regression, enlarge only the responsible source-controlled hole, regenerate outputs, validate them, and provide a Tailscale CAD Viewer URL.
