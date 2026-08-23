# Migration handoff

Status: formal review accepted candidate `81b98d4c043560512076b2599b7200e3ffe90a6e84a5300b25ac9941c5e57fb0` for Kage migration integrity and GitHub delivery only. Delivery is complete on pull request [#2](https://github.com/scottchu/design-projects/pull/2), linked to GitHub Project [Notebook](https://github.com/users/scottchu/projects/1). Pull request #1 was closed automatically by the branch rename and is superseded. Candidate `2901b2b7…` remains superseded; source authority remains `c838df4fb1edaa4077330db1fb8e24808a065e8738d5646cd76b26077a707cdd`.

Next action: keep the candidate unchanged and run only `KAGE-EXP-001`. The locked assembled STEP is available in CAD Viewer at [this review link](https://mac-mini.duckbill-ionian.ts.net/Users/scottchu/.codex/worktrees/068351f6-bce2-42b2-bc1d-0cdf3c6e680e/design-projects/projects/kage?file=references%2Flocked-direct-gear%2Fp3_v3_direct_gear_race_assembled.step).

## Implementation result

- Added the installed historical Kage simulator/optics compatibility runtime, one normal migration-integrity test module, four optional compatibility modules, root-workspace metadata, exact continuity records, legacy indexes, 60 byte-preserved legacy doc files, 667 byte-preserved source/history files, one locked STEP, and the Q3-R0 11-file candidate packet.
- Updated only root `uv.lock` and `package-lock.json` outside `projects/kage`.
- Excluded local environments, dependency trees, caches, logs, rollback duplication, screenshots/renders, and bulk generated CAD/media. A boundary audit caught and removed 210 unintended generated STEP copies from the initial text-file selection because STEP is text-encoded.
- One focused repair added the exact legacy Q4 spec required by the retained CLI compatibility evaluator after the first active test run reported seven import failures.
- Exact commands and results are in `VALIDATION.md`; selected-path hashes and counts are in `manifests/`.

## Repair-cycle findings

KAGE-MIG-003 verified 796/796 candidate rows before reporting `CRIT-001` through `CRIT-004`; KAGE-MIG-004 verified the same candidate and all requested artifact/runtime checks before repository structure failed 1 of 11 on `VAL-001`. Their concise receipts and repair dispositions are in `REVIEW.md` and `VALIDATION.md`. Both gates are invalidated by this repair and must rerun.

On repaired candidate `81b98d4c…`, `/root/kage_migration_critic` independently passed read-only with all `CRIT-001..004` resolved and no new high/medium finding. `/root/kage_migration_validator` independently passed read-only with 798/798 rows, normal 7, compatibility 68, repository structure 11, and `VAL-001` resolved; unchanged hashes carry the prior artifact-structure evidence without promoting slicer or physical acceptance. `/root/kage_migration_formal_review` verified 798/798 and accepted migration integrity/GitHub delivery only, writing only `REVIEW.md`.

## Sole next experiment

`KAGE-EXP-001` begins only after migration acceptance by authoring—not claiming to possess or print—a minimal restart-namespace two-half Q3 seam coupon and focused geometry/export test bound to `KAGE-DC-001/002`. Inherited, unaccepted controls are: `3 + 3 mm` lap, `R70–124` band, donor/receiver tangent half-widths `13.0/13.2 mm`, `0.2 mm` plan clearance, and four `Ø3.3 mm` holes at `R76/R118`, tangent offsets `±7 mm`. Then generate explicit STEP/3MF; verify two solids, lap/hole dimensions, and U1 footprint; print both PETG halves on U1/0.4 mm with identical profile/orientation; assemble four M3 fasteners finger-snug; wait one hour; measure without sanding/forcing. Pass only for gap `0.05–0.30 mm`, step `≤0.25 mm`, flatness deviation `≤0.50 mm`, and no crack, forced fit, or visible bow. Exact edge: `KAGE-DC-001/002 → author coupon source+regression → CAD/export validation → physical coupon → base-adoption decision`. No coupon exists or was generated during migration.

## Receipt ledger

| Task | Owner | Status | Fingerprint/evidence | Next action |
|---|---|---|---|---|
| KAGE-MIG-001 | `/root/kage_migration_design` | complete, read-only | source authority `c838df4f…`; receipt summarized in `BRIEF.md` | implementation |
| KAGE-MIG-002 | `/root/kage_migration_impl` | repair cycle 1 complete | repaired `81b98d4c…`; focused checks in `VALIDATION.md` | delivery |
| KAGE-MIG-003 | `/root/kage_migration_critic` | passed, read-only | `81b98d4c…`; `CRIT-001..004` resolved, no new high/medium | formal join complete |
| KAGE-MIG-004 | `/root/kage_migration_validator` | passed, read-only | `81b98d4c…`; 798/798, 7/68/11 tests, `VAL-001` resolved | formal join complete |
| KAGE-MIG-005 | `/root/kage_migration_formal_review` | accepted migration integrity/delivery only | `81b98d4c…`; 798/798; only `REVIEW.md` changed | GitHub delivery |
| KAGE-MIG-006 | `/root` | delivered | commit `b1fe19d…`; PR #2; Project Notebook; CAD Viewer HTTP 200 | `KAGE-EXP-001` |

## 2026-08-22 cleanup note

The former Notebook Project item for PR #2 was removed and the repository was unlinked on 2026-08-22. GitHub Projects are no longer used. The delivery-time linkage above remains historical.

## Final delivery cleanup extension — KAGE-CLEAN-002

Implementation owner `/root/kage_cleanup_impl` used monorepo baseline `7ca4d99ded0c0ccb0f67c0ee56494aa932596da1` and the unchanged reviewed 798-row candidate fingerprint `81b98d4c043560512076b2599b7200e3ffe90a6e84a5300b25ac9941c5e57fb0`.

The inventory agent concluded **SAFE TO RETIRE** with one recoverable quarantine copy because both legacy trees were byte-identical and all declared migration selections were preserved. The independent preservation auditor concluded **FAIL for permanent deletion** but **CONDITIONAL PASS for reversible Trash quarantine** because three mockup PNGs, two unique rollback parametric sources, and four catalog STEP inputs were intentionally excluded from `projects/kage`. The resolution was to move both complete trees intact to unique Trash children, never empty Trash, unregister only the now-clean restart worktree, and retain its branch.

Both former active paths are absent. The complete trees now remain recoverable at:

- `/Users/scottchu/.Trash/kage-cleanup-2026-08-22/original-japandi-shadow-clock-simulator`
- `/Users/scottchu/.Trash/kage-cleanup-2026-08-22/restart-japandi-shadow-clock-simulator`

Each quarantine child contains 25,227 regular files, 4 symlinks, and 3,054 directories. Each locked-reference assembled STEP hashes to `dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7`; each active direct-gear assembled STEP hashes to `e523eeaac4c0054b4fc06a33869e123248014a7892c4f582898c99765cd0b7a4`. Normal `git worktree remove /Users/scottchu/Projects/personal/3d-print-kage-restart` succeeded without `--force`; the worktree is no longer registered, and retained branch `kage/restart-20260822` remains at `96b055d4b8d0b87f3e6132fa3d90b23b3be4ed84`.

Rollback: do not empty the quarantine. Restore the original child only if its exact old destination is absent. To restore the restart child, first recreate `/Users/scottchu/Projects/personal/3d-print-kage-restart` from retained branch `kage/restart-20260822`, then move the child beneath that worktree's `design/` directory; stop if any destination exists.

This cleanup changes no CAD, source, tests, artifacts, manifests, locks, branch contents, or acceptance layer. Distinct critic and validator reruns passed on integrated commit `f29a93c4473e9c61002018f3161d79550cc8dd9e`; formal review `KAGE-CLEAN-005` accepted reversible path retirement and worktree deregistration only, with no remaining finding. Do not empty Trash. After delivery, the sole next design action remains `KAGE-EXP-001`.

| Cleanup task | Owner | Final status | Evidence |
|---|---|---|---|
| `KAGE-CLEAN-001` | `/root/kage_cleanup_inventory`, `/root/kage_cleanup_preservation_audit` | complete, read-only | byte parity plus reversible-only preservation boundary |
| `KAGE-CLEAN-002` | `/root/kage_cleanup_impl` | complete | two intact Trash moves; normal worktree removal; no permanent deletion |
| `KAGE-CLEAN-003` | `/root/kage_cleanup_critic` | passed, read-only | no remaining critical/high/medium/low finding |
| `KAGE-CLEAN-004` | `/root/kage_cleanup_validator` | passed, read-only | 798/798; Kage 7; repository 12; full quarantine parity |
| `KAGE-CLEAN-005` | `/root/kage_cleanup_formal_review` | accepted | reversible cleanup only; `REVIEW.md` |
