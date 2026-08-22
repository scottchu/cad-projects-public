# Kage project state

## Baseline

- Authority: clean-restart document plus locked direct-gear reference, identified by `manifests/`.
- Current restart CAD candidate: none.
- Q3-R0: candidate/reference only.
- Migration candidate: repair cycle 1 frozen at `81b98d4c043560512076b2599b7200e3ffe90a6e84a5300b25ac9941c5e57fb0`; critic, validator, and formal-review gates passed.

## Active iteration

`docs/iterations/2026-08-22-r0-monorepo-migration/`

## Acceptance state

- CAD/source: accepted for migration integrity and GitHub delivery only; no restart CAD candidate or mechanism geometry is accepted.
- Written artifact/slicer: exact-byte preservation and structural STEP/3MF evidence accepted for migration only; slicer profile, orientation, brim footprint, and print release remain pending.
- Physical print/assembly: pending; no completed results set.

## Next action

Complete delivery without changing the candidate: obtain the CAD Viewer link for the locked STEP, create or link the GitHub Project item, commit and push the feature branch, and open the pull request. After delivery, KAGE-EXP-001 is the sole design experiment.
