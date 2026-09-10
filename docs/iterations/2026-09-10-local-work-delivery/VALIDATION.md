# Independent delivery validation

Date: `2026-09-10`

Task / role: `M3`, `/root/delivery_validation`, independent validator. This
role did not implement or approve CAD changes. It wrote this receipt only;
tests used the root Python 3.12 environment and temporary/runtime outputs.

## Verdict

**PASS for the bounded preservation and integration delivery.** The final
candidate preserves the declared branch, recovery-snapshot, Pill Click and
drone inputs with verified provenance, retains modern-main policy and package
versions, and passes the focused supported test gates. This verdict does not
promote any preserved experiment to a new CAD, written-artifact, slicer or
physical acceptance state.

The repository structure command remains non-green because modern main already
lacks the active Laifen iteration's `VALIDATION.md`. The historical P20 R4
print-kit SHA guard also continues to fail exactly as documented. Neither
failure was weakened or repaired as part of this source-preserving delivery.

## Frozen candidate and provenance

- Final `CANDIDATE.sha256`: `529/529` entries verified; manifest SHA-256
  `97357dfeadd1023c178f27e02b02429bf725053fda3f884ae7aa69714dda0210`.
- Final `M2-SOURCE-ARTIFACT-FREEZE.sha256`: `703/703` entries verified before
  return; manifest SHA-256
  `4afc5f670dacd9625ed4f939e17ad4e16d196f007fef67790df8103093a0583d`.
- `PROVENANCE.tsv` SHA-256:
  `ae4e416eb3b2fbcd692e439b24c724f15bab7c089b4685eb3e31fb677569f6cd`.
  Independent enumeration checked all `547` rows: `109` source-commit Git
  blobs at `a883404`, `437` recovery-snapshot files, the one ignored original
  Pill Click review job, `531` declared destination files and `16` explicit
  exclusions. There were zero source, destination or exact-import hash errors.
- Original source checkout HEAD remained
  `a8834040afe401637d36e94bd8fdd9e1d9874d35`; recovery `manifest.json`
  remained
  `37c87c541c9bcc8793ea1bc1387c8b1d977ec39d090af962acc98c9cb603cbc1`.
- The initially omitted ignored file
  `projects/pill-click/models/p1_hollow_magnetic_dispenser/p1_review_job.json`
  was caught by the migration checker, restored byte-for-byte from the original
  checkout, explicitly staged, and refrozen. Its SHA-256 is
  `02b48475b4922f9f332b1a9a6a9fb0efe653529106fe34931e9adb0e221a1518`.

## Commands and results

All commands ran from the isolated candidate root.

- `uv run python --version` and `.venv/bin/python3 --version`: Python
  `3.12.13` through the repository root environment.
- `uv lock --check`: PASS, `74` packages.
- Structural comparison of `uv.lock` with `cf8ec46:uv.lock`: only
  `pill-click 0.1.0` and `networkx 3.6.1` were added; no packages were removed
  and no existing versions changed.
- `git diff --exit-code -- package-lock.json`: PASS.
- The exact README-supported P13 ten-node pytest command: `10/10` PASS.
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest -q -p no:cacheprovider`
  over P20 R4 full CAD, P24 and P25 test files: `42/42` PASS.
- The separate historical
  `projects/xt60-bend-jig/tests/test_p20_r4_print_kit_3mf.py`: `1` passed,
  `2` failed as expected. Both failures preserve the parent-source guard:
  current P20 R4 source
  `d4c9d5bc428d3e426df1e80099ceef33b1de820fa8af6b4f5a569e97d2480d58`
  differs from frozen guard
  `3eb9187ec7ad9205a2a1ced5e15e5a87a2a5a24e6c76282193ed086fb776d5b8`.
- Pill Click bounded five-file command with
  `-k 'not loads_in_orca' --maxfail=3 -p no:cacheprovider`: `29/29` PASS.
- `node .../check-migration.mjs`: PASS; `138` included, `1` excluded and `1`
  external legacy input; preserved source/candidate manifest fingerprints
  `77901ecc...` / `cf03c7cb...`.
- `npm test --workspaces --if-present`: PASS; XT60 `26/26` Node tests and
  Kage's declared build-backed test scripts completed.
- `npm run build --workspaces --if-present`: PASS; XT60 bundle built.
- `uv run pytest -q -p no:cacheprovider tests/test_repository_structure.py`:
  `10` passed, `1` failed at
  `test_workspace_members_externalize_project_continuity`. A Git-tree check
  proves `cf8ec46` already points Laifen at
  `2026-09-06-pattern-reference-intake` without that iteration's
  `VALIDATION.md`; `git diff --exit-code cf8ec46 --
  tests/test_repository_structure.py projects/laifen-wave-case` passed. This is
  unchanged modern-main debt outside delivery scope.
- Focused `git diff --check` over newly authored/reconciled README, XT60
  continuity, lock and delivery-record paths: PASS. A broad check reports
  whitespace already embedded in byte-preserved STEP/archive/history files;
  those bytes were intentionally left unchanged.
- Bound Workbench policy manifest at revision
  `1d7f4fcd65e04136bb6bad24e90015ca36d97f2f` independently hashes to the
  binding value
  `b95f77ef16d317366d1c93f7ff76dee92c0e69976ce55facec10512e23b6c3cf`.

## Historical manifest checks

- P25 candidate: `13/13` current geometry/source/artifact rows pass; manifest
  file SHA-256 remains `88fdcd25585c35277d66a769b5c35208f8e5b8c7534d93efdbcb57493638a845`.
- P24 candidate: `12/12` pass. P20 R3 candidate: `12/12` pass. P20 R1 scaffold
  candidate: `20/20` pass.
- P25 design inputs pass `11/16`; its five drifted rows are reconciled current
  continuity/profile files. The scaffold input manifest passes `14/18`; its
  four drifted rows are modern policy/requirements/experience files. The
  frozen candidate manifests themselves remain unchanged and self-verifying.
- P20 R4 parent passes `20/30` historical rows and child passes `8/14`.
  Mismatches are the documented later source/export/provenance drift plus one
  absent external visualization input. Their historical labels and hashes were
  preserved rather than rewritten to make a false current fingerprint.

## Acceptance boundary and remaining risks

This validation covers source/history preservation, integration, focused
regression checks and provenance. No CAD or production artifact was regenerated,
so a new snapshot and CAD Viewer handoff do not apply. No DfAM, slicing, printer,
force, fit, fatigue, wear or physical validation was performed. P25 remains a
first-CAD preview, P19 remains the accepted digital baseline, and the documented
P20 collision/thin-web and print-kit provenance gaps remain open.
