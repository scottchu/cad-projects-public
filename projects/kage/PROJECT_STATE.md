# Kage project state

## Baseline

- Authority: clean-restart document plus locked direct-gear reference, identified by `manifests/`.
- Current restart CAD candidate: none.
- Q3-R0: candidate/reference only.
- Current repository candidate: `manifests/candidate.sha256` SHA-256 `da3bcedc68ed5324cf805f42ff0bca48cd1ccbcf89db7aa9207908b5df27f631`, 805 rows.
- Reversible-cleanup acceptance remains recorded. The custom repository preview launcher is removed; preview now uses the installed `cad-viewer` workflow directly and requires separate page, artifact-readiness, and visual-evidence claims.

## Active iteration

`docs/iterations/2026-08-23-direct-cad-viewer/`

## Acceptance state

- CAD/source: accepted for migration integrity and GitHub delivery only; no restart CAD candidate or mechanism geometry is accepted.
- Written artifact/slicer: exact-byte preservation and structural STEP/3MF evidence accepted for migration only; slicer profile, orientation, brim footprint, and print release remain pending.
- Physical print/assembly: pending; no completed results set.
- Preview operation: the prior launcher acceptance is superseded. Direct Viewer readiness requires the exact page HTTP `200` and exact artifact HTTP `200` with JSON `state == "ready"`. After inspection, the general visual claim is limited to “the requested artifact rendered with no visible error state”; feature-specific claims must name the inspected features and views. This does not change the CAD, slicer, or physical acceptance states above.

## Next action

Migration delivery remains complete through migration commit `b1fe19dc674e811e0e1287fade3748f7f26b1126` and pull request [#2](https://github.com/scottchu/design-projects/pull/2). GitHub Projects are no longer used, and pull request #1 remains superseded by #2. Pull request [#5](https://github.com/scottchu/design-projects/pull/5) records the reversible legacy-path retirement and the now-superseded preview launcher. Formal review accepted the direct-Viewer workflow candidate `da3bcedc68ed5324cf805f42ff0bca48cd1ccbcf89db7aa9207908b5df27f631`; pull-request delivery is the remaining repository action. Both complete retired trees must remain under `/Users/scottchu/.Trash/kage-cleanup-2026-08-22`; both old active paths remain absent, the restart worktree remains unregistered, and branch `kage/restart-20260822` remains retained. Do not empty Trash. After delivery, the sole next design action remains `KAGE-EXP-001`.
