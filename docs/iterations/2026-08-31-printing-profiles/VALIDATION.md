# Printing profiles — main-port validation

Root baseline before edits: `uv run pytest tests/test_repository_structure.py
projects/kage/tests` -> 18 passed, 1 failed. The inherited failure is main's XT60
PROJECT_STATE missing `## Baseline`; no unrelated heading repair is in scope.
All seven Kage integrity tests passed before edits.

Independent validation is complete; formal review accepted docs-only PR delivery
with the inherited failure disclosed. No CAD/slicer/physical test is claimed by
this documentation-only task. The independent receipt below is unchanged.

## PRINT-PR-VALIDATE independent receipt

Owner `/root/printing_pr_validate`, distinct validation role. **PASS with the
documented inherited baseline failure.** Verified on branch
`codex/project-printing-profiles` at baseline
`b69b6ad12af611644987f026eef4940db9c7bb34`.

- Frozen candidate: 29-row `CANDIDATE.sha256`, SHA-256
  `7c8d7afe1e78855abb6df035912b2174eb915505bb439fb34014d456d28027bc`;
  `shasum -a 256 -c .../CANDIDATE.sha256` matched all 29 paths before and after
  the checks. The receipt itself is excluded from that immutable manifest.
- `uv run pytest tests/test_repository_structure.py -k printing_profiles`:
  **1 passed, 12 deselected**.
- `uv run pytest tests/test_repository_structure.py projects/kage/tests`:
  **19 passed, 1 failed**. The sole failure is exactly the recorded pre-existing
  `projects/xt60-bend-jig/PROJECT_STATE.md` missing `## Baseline`; it is outside
  this port and no repair was made.
- `uv run --package kage pytest projects/kage/tests`: **7 passed**.
  `uv run python` used Python 3.12.13 from this checkout's root `.venv`.
- `git diff --check` passed. A local-Markdown resolver checked 32 changed/new
  local links; all targets exist.
- Compared to the baseline Kage integrity manifest (805 rows), the 806-row
  candidate has exactly one added row, `projects/kage/PRINTING_PROFILE.md`, and
  exactly one changed row, `docs/CAD_WORKFLOW.md`; no row was removed and every
  other original row is byte-preserved.
- Scope inspection found no changes to `AGENTS.md`, dependencies/locks,
  `CURRENT`, CAD/source, frozen contracts, tests other than the allowlisted root
  profile test, or CAD/mesh/STEP/3MF artifacts. The main P19 XT60 profile names
  no P20--P24 dependency; P19 remains the stated authority. Existing untracked
  `projects/kage/kage.egg-info/` was excluded and preserved.

Coverage: editable per-project profiles, shared-profile policy/template links,
P19-main binding, Kage-manifest preservation, focused structure/profile check,
and Kage integrity coverage all pass. This validates documentation and
repository preservation only; no CAD, export, slicer, printer, or physical
acceptance is claimed. Next: formal reviewer joins this receipt with the
independent critic receipt on the unchanged fingerprint.

## PRINT-PR-IMPL self-check

Owner `/root/printing_docs`; implementation evidence only, not independent approval.
Candidate: `CANDIDATE.sha256`, 29 path-sorted rows, SHA-256
`7c8d7afe1e78855abb6df035912b2174eb915505bb439fb34014d456d28027bc`.

- `uv run pytest tests/test_repository_structure.py -k printing_profiles`:
  1 passed, 12 deselected.
- `uv run pytest tests/test_repository_structure.py`: 12 passed, 1 failed;
  same baseline missing XT60 `## Baseline` heading, no new failure.
- `uv run --package kage pytest projects/kage/tests`: 7 passed.
- `git diff --check`: passed.
- `shasum -a 256 -c docs/iterations/2026-08-31-printing-profiles/CANDIDATE.sha256`:
  29/29 matched. The manifest includes frozen contracts, output policy/profiles/
  test, relevant main requirements/experience and protected authority manifests.

Kage integrity snapshot: `a49cdaf17eed504e7aba262d844499efba6da3ed6874fbfafa76ea43d9f7306f`,
806 rows. Exactly one old row changed (shared CAD policy) and one new profile row
was added; no old CAD/source/reference hash changed. This is not a transfer of
historical mechanism or physical acceptance.

Three shared/Kage core files are byte-identical to the original implementation;
only the new XT60 profile is adapted to main P19. Root-policy diffs contain only
printing-profile additions. No original-worktree write, Git index/ref change,
source/model/artifact operation or unrelated heading/test repair was performed.
