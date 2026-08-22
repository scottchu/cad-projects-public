# P13 R1 monorepo migration handoff

## Current status

The controlled source and release import, workspace adaptation, and deterministic migration validation are complete.

## Completed work

- Added the repository project-continuity contract and templates.
- Imported authoritative source, tests, design history, scripts, selected releases, and curated review evidence.
- Excluded local environments, nested locks, Node installs, caches, broad logs, build output, CAD render packages, and stale binaries.
- Preserved legacy summaries unchanged under `docs/legacy/`.
- Added current-state, requirements, experience, decisions, migration, and release records.
- Recorded the user's latest physical result: the middle stick is too thick for the center hole.
- Resolved the shared root Python and npm workspaces without nested locks or environments.
- Regenerated the complete explicit P13 STEP set, current production/coupon 3MF files, and provenance from migrated source.
- Passed 59 focused P13 tests, solid validation for the print kit, motion assembly, and 3.8 mm coupon, and visual review of deterministic ISO snapshots.
- Passed 6 repository-structure tests, 26 simulator contract tests, and the simulator production build.

## Changed paths

- Repository rules and templates under `docs/` and `AGENTS.md`.
- New project under `projects/xt60-bend-jig/`.
- Root `uv.lock` and `package-lock.json` will change during dependency registration.

## Artifacts

See `releases/p13-petg-test/release-manifest.json`. It distinguishes imported historical hashes from current regenerated hashes.

## Unresolved risks and physical unknowns

- Fresh simulator browser review remains pending because no controllable in-app browser runtime was attached.
- Fresh slicer validation remains pending; retained OrcaSlicer results apply only to the historical corrected production 3MF.
- Seven P2–P6 historical tests assume generated exports that were absent in the source tree. They are outside the supported P13 baseline and were not repaired by importing stale outputs.
- The exact printed center interface must be identified before resizing.
- Complete P13 physical validation remains pending.

## Next smallest action

- Create `p13-r2-center-hole-fit-repair`, map the user's physical terms to the exact mating parts, and add the concrete fit regression before changing the responsible hole parameter.

## Restart instructions

Read `PROJECT_STATE.md`, `NEXT_AGENT.md`, the completed migration iteration, and `docs/EXPERIENCE.md`. Do not guess the failed center interface or modify the old project directories. The repaired iteration must hand back a Tailscale CAD Viewer URL.
