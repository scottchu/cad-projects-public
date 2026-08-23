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
