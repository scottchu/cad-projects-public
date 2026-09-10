# Iteration validation

## Environment

- Provenance: MIG-IMPLEMENT `/root/migrate_pill_click`, implementation checks only.
- Candidate fingerprint: `source-manifest.json` and `candidate.sha256`.
- Root: `/Users/scottchu/Projects/personal/design-projects`, root uv/Python 3.12 workspace.
- Read-only status: tests do not edit imported source/artifacts; tmp copies/caches may be created.

## Commands and results

All commands below ran at the root unless stated otherwise.

- `uv lock`: PASS, 70 packages; added pill-click 0.1.0 and networkx 3.6.1 only.
- `git diff -- uv.lock`: additions only: member pill-click and package blocks pill-click/networkx; existing package versions unchanged. Prior lock is `root-uv-lock.before.txt`.
- `uv sync --all-packages --all-groups`: PASS, built pill-click, installed pill-click/networkx; removed extraneous greenlet 3.5.5, playwright 1.62.0, pyee 13.0.1 from shared environment. No packaging repair needed.
- `uv lock --check`: PASS, 70 packages.
- `uv run --project projects/pill-click pytest projects/pill-click/tests --collect-only -q -p no:cacheprovider`: PASS, 241 tests collected across 21 files; no full-suite execution implied.
- `uv run --project projects/pill-click pytest projects/pill-click/tests/test_environment.py projects/pill-click/tests/test_p0_spec.py projects/pill-click/tests/test_p0_v2_spec.py projects/pill-click/tests/test_p0_v3_spec.py -q --maxfail=3 -p no:cacheprovider`: PASS, 26 checks.
- `uv run --project projects/pill-click pytest projects/pill-click/tests/test_p1_hollow_magnetic_dispenser_artifacts.py -q -k 'not loads_in_orca' -p no:cacheprovider`: PASS, 3 static package/normalizer checks; CLI-loading test deliberately deselected.

## Requirement evidence

MIG-001/003/004 map to `source-manifest.json`; MIG-002 to lock/sync/check;
MIG-005 to separate acceptance states. Continuity root tests and final hashes
are recorded in `HANDOFF.md` after final verification.

## Artifact paths and checksums

All imported files retain their original paths except README, whose preserved
copy is under legacy. `source-manifest.json` lists source/destination/hash and
explicit exclusions, plus external legacy spec. Models include P1/P2 STEP/3MF
and source entrypoints; no artifact was regenerated.

## Acceptance state

- CAD/source: migration parity and bounded checks only; full CAD acceptance pending.
- Written artifact/slicer: bytes preserved and P1 static 3MF checks pass; source/export parity and slicer not run.
- Physical: no new evidence; pending exact-baseline user validation and physical tests.

## Failures, repairs, and reruns

No test failure in the bounded executed set. Full historical CAD suite was not
run; therefore known/unknown historical failures remain unrepaired and unassessed.
Missing P0 exports and obsolete README plugin paths are preexisting gaps.

## Final implementation checks and environment restoration

- Root `tests/test_repository_structure.py`: 12 passed, 1 failed because existing
  `projects/xt60-bend-jig/PROJECT_STATE.md` lacks `## Baseline`. This out-of-scope
  document was not changed by the migration worker. Pill-click-only continuity
  structure checks passed.
- `node projects/pill-click/docs/iterations/2026-09-01-workspace-migration/check-migration.mjs`:
  PASS, 138 imported files and one isolated external legacy file.
- `git diff --check -- uv.lock`: PASS.
- To undo sync's unrelated environment removal, the implementation worker ran
  `uv pip install --offline --python /Users/scottchu/Projects/personal/design-projects/.venv/bin/python greenlet==3.5.5 playwright==1.62.0 pyee==13.0.1`.
  PASS; exact installed versions verified through the root interpreter's
  `importlib.metadata`. No browser binaries were downloaded and no further sync
  was performed. These packages remain undeclared, as they were before migration.
- Root lock after restoration:
  `b51844dc64d9fddd3d27d65cebd69b33183ad85fe642fc6fd78ecaece91e386f`.
  Before-lock:
  `bd6f17b697f912ddbc338fb33a24c73ad2a91d9fd25e1dc09869202e368cb669`.

## Independent validator receipt

Validator provenance: `/root/migration_validator`; read-only, no source/artifact edits.
Source manifest SHA-256:
`77901ecc9a718fe14f339587c7887132845f2b748f5a4ddddd2b2e9c1ad906e7`.
Candidate manifest SHA-256:
`cf03c7cbc037ff599f589daedd215569a7aba7136efa1fdb7fbd63c9e0bdd37c`.

Independent filesystem/hash enumeration verified all 139 original project files:
138 mapped files preserved, only the nested `uv.lock` excluded and its hash
recorded. Counts: 60 source files, 21 tests, 37 model files; original README
preserved in legacy. The older root spec is the only external legacy file and
matches its original hash. No nested environments/locks or symlinks were introduced.
All 142 candidate entries passed independent verification.

The validator reran `uv lock --check` (70 packages) and the five-file combination
of the four import/spec test files plus the P1 artifact test file listed above,
with `-k 'not loads_in_orca' --maxfail=3 -p no:cacheprovider`: 29 passed.
Drone archive parity: 107 files, 34 directories, zero links; all 106 tracked files
match original source Git HEAD blobs. The only extra is `.DS_Store`; original
untracked-content parity cannot be independently reconstructed after its move.

Conclusion: no blocking data loss; originals are safe to quarantine recoverably.
The checker verifies destination hashes if originals no longer exist; this is not
a claim that it re-compared absent originals. Quarantine manifests provide the
separate original-tree recovery evidence.

## Post-review original-tree quarantine

Parent recovery coordination moved `3d-print/design` and root `pill_click` into
`/Users/scottchu/.Trash/3d-print-cleanup-2026-09-01.V3MAHz/`. The complete before/after
manifests match (including directory and symlink entries). A separate post-move
Node/SHA-256 comparison checked all 138 included files against both their
quarantined originals and destination, the excluded nested lock against its
recorded hash, and the isolated external legacy spec in both locations: PASS.
The original retired paths are absent. The destination-only checker still passes
with source/candidate fingerprints unchanged. The recovery location contains
additional unmigrated projection-lamp work; do not discard it as a duplicate.
