# Kage project state

## Baseline

- Authority: clean-restart document plus locked direct-gear reference, identified by `manifests/`.
- Current restart CAD candidate: none.
- Q3-R0: candidate/reference only.
- Current repository candidate: `manifests/candidate.sha256` SHA-256 `495265a08a78dcd5fd2639ab41e8e9ef0aa62595e106f1229b6fa7a6355ed60a`, 805 rows.
- Reversible-cleanup and repository-wide preview-launcher critic, validator, and formal-review gates passed. Kage owns only the checksum-pinned historical-reference consumer; the launcher is the root `bin/preview-cad` tool for all projects.

## Active iteration

`docs/iterations/2026-08-23-preview-launcher/`

## Acceptance state

- CAD/source: accepted for migration integrity and GitHub delivery only; no restart CAD candidate or mechanism geometry is accepted.
- Written artifact/slicer: exact-byte preservation and structural STEP/3MF evidence accepted for migration only; slicer profile, orientation, brim footprint, and print release remain pending.
- Physical print/assembly: pending; no completed results set.
- Preview operation: accepted for the reusable repository launcher and Kage's checksum-pinned locked STEP only. This does not change the CAD, slicer, or physical acceptance states above.

## Next action

Migration delivery remains complete through migration commit `b1fe19dc674e811e0e1287fade3748f7f26b1126` and pull request [#2](https://github.com/scottchu/design-projects/pull/2). GitHub Projects are no longer used, and pull request #1 remains superseded by #2. Pull request [#5](https://github.com/scottchu/design-projects/pull/5) is the authorized delivery vehicle for both the formally accepted reversible legacy-path retirement and the repository-wide preview launcher. Both complete retired trees must remain under `/Users/scottchu/.Trash/kage-cleanup-2026-08-22`; both old active paths remain absent, the restart worktree remains unregistered, and branch `kage/restart-20260822` remains retained. Do not empty Trash. After delivery, the sole next design action remains `KAGE-EXP-001`.
