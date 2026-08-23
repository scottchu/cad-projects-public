# Validation

## KAGE-MIG-002 implementation self-check

Owner: `/root/kage_migration_impl`; this is not independent acceptance.

- `uv lock` — resolved 68 packages and added the Kage workspace package, pinned py-gearworks revision, and trimesh.
- `PATH=/Applications/ChatGPT.app/Contents/Resources/cua_node/bin:$PATH npm install --ignore-scripts` — root workspace install completed, 0 vulnerabilities; the first plain `npm install` attempt did not run because npm was absent from the shell PATH.
- `uv sync --all-packages --all-groups` — built/installed Kage in the shared root `.venv`.
- Initial `uv run --package kage pytest projects/kage/tests` — 67 passed, 7 failed because the retained CLI compatibility evaluator imported its Q4 spec. Focused repair copied the exact legacy spec and listed it as a project module; no CAD changed.
- Rerun `uv run --package kage pytest projects/kage/tests` — 74 passed.
- `uv run kage-clock upright-optics --json` — exit 0.
- `npm run --workspace kage build:three` and `npm run --workspace kage build:adr` with the bundled Node path — exit 0; regenerated bundle hashes equal the original hashes (`96d5ad09…`, `e211e6ad…`).
- `rsync -rcn --delete --exclude='.DS_Store' <source>/docs/ projects/kage/docs/legacy/source-docs/` and `cmp` on the original README — no differences.
- `rsync -rcn --from0 --files-from=/tmp/kage-legacy-source-files <source>/ projects/kage/legacy/source-project/` — no differences for the selected source-only set.
- Source authority manifest SHA-256: `c838df4fb1edaa4077330db1fb8e24808a065e8738d5646cd76b26077a707cdd`.
- Target authority manifest SHA-256: `1840122753c5d76b68076ae0def2bdf19bbcb0a601efec14bd31cb0c5bee3268`.
- KAGE-MIG-002 input manifest SHA-256: `777e1514e8d7acb1fccbcdfd305911dcbff486d5b219778940221846f1ec0bbb`.
- Frozen target-layout candidate: 796 sorted path/content lines in `manifests/candidate.sha256`; manifest SHA-256 `2901b2b7100492f8e75ff37c1d6a47e6bac5b686bb74e9db081c95f9127a7dd9`.
- Root locks after migration: `uv.lock` `bd6f17b6…`; `package-lock.json` `a5bfa9bb…`.

## Acceptance boundary before independent validation

- CAD/source: migration hashes and active runtime passed implementation self-check; no restart CAD candidate exists and independent KAGE-MIG-004 is pending.
- Written artifact/slicer: selected artifact bytes match source hashes; STEP/3MF structure, placement, quantity, footprint, and slicer acceptance remain for the independent validator. No print release is claimed.
- Physical print/assembly: pending; no completed physical-results JSON/photo set was found. Exactly one seam-coupon experiment is specified in `DESIGN.md`.

## KAGE-MIG-004 failed validator receipt — superseded candidate

- Owner: `/root/kage_migration_validator`; role: independent read-only validator.
- Candidate: `2901b2b7100492f8e75ff37c1d6a47e6bac5b686bb74e9db081c95f9127a7dd9`, verified before and after validation.
- All 796 candidate manifest rows matched.
- Active Kage suite: 75 passed; isolated Q3 suite: 9 passed; CLI smoke: passed; temporary JavaScript rebuild: byte parity passed.
- Locked STEP and Q3 STEP/3MF structure/parity checks: passed. This is structural artifact evidence only; slicer acceptance remains pending.
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest -p no:cacheprovider tests/test_repository_structure.py`: 10 passed, 1 failed.
- `VAL-001` MAJOR: `PROJECT_STATE.md` lacked the required `Baseline`, `Active iteration`, `Acceptance state`, and `Next action` headings.
- Snapshot was intentionally skipped because no visible geometry changed and all selected artifacts were byte-frozen. Physical acceptance remains pending.

## Repair-cycle disposition

`PROJECT_STATE.md` now uses the four required headings without changing the acceptance claims. Repair-cycle changes invalidate KAGE-MIG-004 on `2901b2b7…`; the full independent validator gate, including the repository structure test and exact candidate closure, must rerun on the repaired fingerprint.

## KAGE-MIG-002 focused repair cycle 1 self-check

Owner: `/root/kage_migration_impl`; this confirms repair mechanics only and is not independent acceptance.

- Repaired candidate: 798 exact-closure rows; manifest SHA-256 `81b98d4c043560512076b2599b7200e3ffe90a6e84a5300b25ac9941c5e57fb0`.
- `PYTHONDONTWRITEBYTECODE=1 uv run --package kage pytest -p no:cacheprovider projects/kage/tests` — 7 passed; normal scope is migration integrity only.
- `PYTHONDONTWRITEBYTECODE=1 uv run --package kage pytest -p no:cacheprovider projects/kage/compatibility-tests` — 68 passed; optional, non-normative compatibility scope.
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest -p no:cacheprovider tests/test_repository_structure.py` — 11 passed.
- Candidate manifest path order, exact-set closure, content hashes, exact exclusions, and `BRIEF.md` inclusion passed in the normal suite.
- `git diff --check` — passed.
- Runtime debris check under `projects/kage` — no cache, egg-info, local environment, or dependency-tree directories found.
- Authority/source fingerprint remains `c838df4fb1edaa4077330db1fb8e24808a065e8738d5646cd76b26077a707cdd`.
- Root lock hashes remain `uv.lock` `bd6f17b697f912ddbc338fb33a24c73ad2a91d9fd25e1dc09869202e368cb669` and `package-lock.json` `a5bfa9bb8ed1028deb0086c001c9c5eca714de9dc115b5da5426f97a8e4fa9a5`.
- No CAD/runtime source, selected artifact, or dependency/lock content changed in repair cycle 1.

KAGE-MIG-003 and KAGE-MIG-004 must both rerun on `81b98d4c…`. Artifact/slicer structural evidence and all physical claims remain at their previous pending boundaries until those independent gates return.

## Repaired-candidate independent receipts

- Critic `/root/kage_migration_critic`, read-only: passed candidate `81b98d4c…`; `CRIT-001..004` resolved with no new high or medium finding.
- Validator `/root/kage_migration_validator`, read-only: passed the same candidate before/after with 798/798 manifest rows; normal suite 7 passed, optional compatibility 68 passed, repository structure 11 passed, and `VAL-001` resolved. Because source/artifact hashes are unchanged, prior written STEP/3MF structural evidence carries forward; slicer acceptance does not.
- Formal reviewer `/root/kage_migration_formal_review`: verified 798/798 and accepted migration integrity and GitHub delivery only. Its sole write was the candidate-excluded `REVIEW.md`.

## Final acceptance boundary

- CAD/source: migration integrity accepted; no restart CAD candidate, mechanism, fit, collision, motion, service, or manufacturing design accepted.
- Written artifact/slicer: exact-byte preservation and structural evidence accepted for migration; slicer profile, orientation, brim footprint, and print release pending.
- Physical print/assembly: pending; no completed physical-results set exists.

## Delivery receipt

- Feature branch `migrate-kage` contains migration commit `b1fe19dc674e811e0e1287fade3748f7f26b1126`.
- Pull request [#2](https://github.com/scottchu/design-projects/pull/2) records the review provenance, acceptance boundaries, unresolved risks, and next action. Pull request #1 was closed automatically by the branch rename and is superseded.
- PR #2 is an item in GitHub Project [Notebook](https://github.com/users/scottchu/projects/1).
- The locked STEP and all four selected Q3-R0 STEP/3MF review URLs returned HTTP 200 from the Tailscale CAD Viewer.
- These delivery-only continuity edits are excluded from `manifests/candidate.sha256`; the reviewed candidate remains `81b98d4c043560512076b2599b7200e3ffe90a6e84a5300b25ac9941c5e57fb0`.

Migration delivery is complete. Candidate-changing edits require the independent gates to rerun; the sole next design action is `KAGE-EXP-001`.

## 2026-08-22 cleanup note

The former Notebook Project item for PR #2 was removed and the repository was unlinked on 2026-08-22. GitHub Projects are no longer used. The delivery-time linkage above remains historical.

## KAGE-CLEAN-002 implementation self-check

Owner: `/root/kage_cleanup_impl`; this is a final delivery cleanup extension and not independent acceptance.

- Preflight: both exact legacy trees existed with 25,227 regular files, 4 symlinks, 3,054 directories, and `5.4G` reported size each. The quarantine target was absent.
- Preflight hashes: both locked-reference STEP copies were `dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7`; both active assembled STEP copies were `e523eeaac4c0054b4fc06a33869e123248014a7892c4f582898c99765cd0b7a4`.
- Created `/Users/scottchu/.Trash/kage-cleanup-2026-08-22` and used two exact `mv` operations to place the full trees at the uniquely named children recorded in `HANDOFF.md`. No copy, `rm`, permanent deletion, or Trash emptying occurred.
- Post-move counts: 25,227 regular files, 4 symlinks, and 3,054 directories in each quarantine child; both checked STEP hashes reproduced exactly.
- Both old active Kage paths are absent.
- The restart worktree was clean after its Kage subtree moved. Normal `git worktree remove /Users/scottchu/Projects/personal/3d-print-kage-restart` passed without `--force`.
- The restart path is absent; the old repository worktree list now contains only `/Users/scottchu/Projects/personal/3d-print` on `main`.
- `git show-ref --verify refs/heads/kage/restart-20260822` passed at `96b055d4b8d0b87f3e6132fa3d90b23b3be4ed84`.
- Unrelated pre-existing untracked paths in `/Users/scottchu/Projects/personal/3d-print` remain untouched.
- Reviewed candidate and source/artifact evidence remained unchanged; no CAD/source/test/artifact/manifest/lock path was edited.
- `sha256sum projects/kage/manifests/candidate.sha256` — `81b98d4c043560512076b2599b7200e3ffe90a6e84a5300b25ac9941c5e57fb0`; `sha256sum -c --quiet` passed all 798 rows.
- `sha256sum projects/kage/references/locked-direct-gear/p3_v3_direct_gear_race_assembled.step` — unchanged at `dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7`.
- `PYTHONDONTWRITEBYTECODE=1 uv run --package kage pytest -p no:cacheprovider projects/kage/tests` — 7 passed.
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest -p no:cacheprovider tests/test_repository_structure.py` — 11 passed.
- `git diff --check` — passed.

### Excluded-file preservation evidence

The following quarantine-relative paths and full SHA-256 values were verified in both complete quarantine children, `original-japandi-shadow-clock-simulator` and `restart-japandi-shadow-clock-simulator`:

| Quarantine-relative path | SHA-256 |
|---|---|
| `docs/mockups/base-joint-options.png` | `bcc8028ea0619611602f50b9f3e7d5f9673e03f68cd9310ee0948b2804c43a67` |
| `docs/mockups/wide-centered-step-lap-detail.png` | `87f1955a639a2c4532139804ffef0b63de423d44f75071a47b9e37089e3008b7` |
| `docs/mockups/wide-centered-step-lap-detail-v2.png` | `6af988227f76877ca7b1fe59d13cd5977344e1d4ee3287c1ff06933fa1145f2d` |
| `rollback/p3_v3_direct_gear_race_guidance_r2_pre_independent_review_20260819T103455Z/source/p3_v3_direct_gear_race_guidance_r2_export.py` | `b96cf2077383723eec2a5f8e004b43a64ac5409d1f63495f7b6c2bd54193cca5` |
| `rollback/p3_v3_direct_gear_race_guidance_r2_pre_independent_review_20260819T103455Z/source/p3_v3_direct_gear_race_guidance_r2_geometry.py` | `11007fbaebbb3c636179dcecab58a4d21273a21365ca5d4780938be1aba30cdd` |
| `models/p3_v3_motor_station_assembly_sim/purchased/iso4762_socket_head_cap_screw_m2x4.step` | `089b80213c239f50cc036eccf16def39078fbaa68e10f10fd82c46753bcc42e6` |
| `models/p3_v3_motor_station_assembly_sim/purchased/iso4762_socket_head_cap_screw_m3x8.step` | `be8177f1dad3e8a1c447c7d791171442352dd1668687bb6f27cf981b843f63a4` |
| `models/parts/miter_gear_1to1_m0_8_16t.step` | `00c7386f24c0f89cf603dd5f276f1106ca2fd3e270a3039449a7f33d00ffaf25` |
| `models/parts/miter_gear_1to1_m1_0_16t.step` | `9a9f41db33b4880777dcf34dca9505bb687c6ab0965fe422b156c85e694994a8` |

Cleanup acceptance covers recoverable path retirement and worktree registration only. CAD/source acceptance remains migration-only; written artifact/slicer status is unchanged; physical print/assembly remains pending. Distinct critic, validator, and formal review are required before calling the cleanup accepted.

## KAGE-CLEAN-002 delivery integration

The cleanup documentation commit was rebased onto `origin/main` at `172af588c68cb6fc633c9c58e2b3abf7a6eac43a`. The four continuity files conflicted only because main had concurrently recorded removal of the former GitHub Project linkage; conflict resolution preserved that current policy note together with the complete cleanup receipt. No CAD, source, test, artifact, manifest, lock, or external quarantine content changed during integration. The focused independent gates must recheck this integrated commit before formal review.
