# Direct CAD Viewer review

No independent critic or formal-review verdict has been issued for this candidate. Implementation evidence is not approval.

## Independent critic receipt — KAGE-PREVIEW-DIRECT-003

**Verdict: CHANGES REQUIRED.** The direct-Viewer simplification and false-positive readiness gate are structurally sound, but the frozen candidate does not yet satisfy every declared preservation and claim-precision condition.

- Critic owner: `/root/direct_viewer_critic`, distinct from design and implementation.
- Baseline inspected: `9c1ae27b9a856cb19c0dfefd497e5133987e2bd4` on `codex/simplify-cad-preview`.
- Verified candidate: `projects/kage/manifests/candidate.sha256` SHA-256 `f9651e45f78138553a252bd6eea68dd68a2eeae50aa94c26e1b580dee5254d3e`, 805 rows; paths are sorted and unique and all 805 content hashes pass.
- Locked imported STEP remains SHA-256 `dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7`.

### Findings

1. **MEDIUM — KPD-C-001 — the declared retained cleanup branch is absent.** `BRIEF.md`, `HANDOFF.md`, `PROJECT_STATE.md`, and `NEXT_AGENT.md` preserve or assert branch `kage/restart-20260822`, but `git -C /Users/scottchu/Projects/personal/3d-print show-ref --verify refs/heads/kage/restart-20260822` fails. The intended commit `96b055d4b8d0b87f3e6132fa3d90b23b3be4ed84` remains reachable as that repository's `main`, so this is not data loss; it is a false current-state claim and a failed explicit preservation invariant. Restore the retained branch ref to the recorded commit, then reverify it before acceptance.
2. **MEDIUM — KPD-C-002 — “looks good” is broader than the evidence required.** Root and Kage active documentation permits “the render looks good” or “visually good” after only confirming that no render-error state is visible. That observation proves only that the requested artifact loaded without a visible render error; it does not establish visual correctness or geometry quality. This wording recreates the user's objection at a narrower layer even though CAD acceptance is separately bounded. Replace these claims with the exact observation, such as “the requested artifact rendered with no visible error state”; reserve any broader visual assessment for the actual inspected features and views.
3. **LOW — KPD-C-003 — the readiness endpoint is policy-defined but not skill-documented.** The installed `cad-viewer` skill documents startup and review-link construction but not the artifact-status request. The current runtime exposes `GET /__cad/artifact?dir=<absolute-workspace>&file=<relative-file>` with `ready | needs-build | generating | error`. The independent validator should record the exact request used and its JSON result so the evidence is reproducible for this installed runtime. This does not justify restoring a repository launcher or pinning the plugin runtime.

### Passing review points

- The tracked launcher, its root test suite, and the Kage runtime-pin manifest are deleted; only ignored Python bytecode from the removed test remains as disposable runtime debris.
- Active root and Kage instructions no longer invoke the custom launcher. References in the superseded preview-launcher iteration remain clearly historical and are correctly preserved rather than rewritten.
- The direct call contract matches the installed skill: use the imported `.step`, resolve `projects/kage/references` absolutely, and select `locked-direct-gear/p3_v3_direct_gear_race_assembled.step` relative to that workspace.
- Page HTTP `200`, exact artifact JSON `state == "ready"`, and a separate visual observation are distinct gates. Startup or a printed URL alone cannot satisfy preview readiness, and preview evidence is not promoted to CAD, slicer, or physical acceptance.
- Both Trash quarantine trees remain present with 25,227 files each; both old active paths are absent and the obsolete restart worktree is unregistered. `.gitignore` still excludes `__cadgen__/`. The only failed recovery invariant observed is KPD-C-001.

### Commands and results

- `sha256sum projects/kage/manifests/candidate.sha256` — exact frozen fingerprint above.
- `sha256sum -c projects/kage/manifests/candidate.sha256` — 805/805 rows pass.
- candidate path-order/uniqueness check — pass.
- `uv run --package kage pytest projects/kage/tests -q` — 7 passed.
- `uv run pytest tests/test_repository_structure.py -q` — 12 passed.
- `git diff --check` — pass.
- launcher/runtime-pin absence and active-reference audit — pass, with superseded iteration records retained as history.
- cleanup presence/path/worktree audit — pass except for the missing retained branch described in KPD-C-001.

No Viewer was started, stopped, signaled, probed, or visually inspected by the critic. The validator remains the sole owner of live Viewer evidence. Route the two medium findings through the smallest implementation repair, regenerate the candidate fingerprint, and rerun critic and validator gates on the repaired candidate before formal review.

## Focused critic recheck — KAGE-PREVIEW-DIRECT-003-R1

**Verdict: PASS.** Candidate `da3bcedc68ed5324cf805f42ff0bca48cd1ccbcf89db7aa9207908b5df27f631` resolves both prior medium findings. No critical, high, or medium finding remains in critic scope.

- Candidate manifest: exact SHA-256 above, 805 sorted unique rows, 805/805 content hashes pass.
- `KPD-C-001`: resolved. `/Users/scottchu/Projects/personal/3d-print` now has `refs/heads/kage/restart-20260822` exactly at `96b055d4b8d0b87f3e6132fa3d90b23b3be4ed84`. That repository has exactly one registered worktree, the original path on `main`; the retired restart worktree remains absent and unregistered. Both Trash quarantine trees remain present with 25,227 files each, and both old active paths remain absent.
- `KPD-C-002`: resolved. The root README/CAD workflow, Kage README/state/next records, and frozen direct-workflow brief/design use only the factual general observation “the requested artifact rendered with no visible error state.” Every broader feature-specific visual claim must identify its inspected features and views. No active/frozen “looks good” or “visually good” instruction remains.
- `KPD-C-003`: remains a low, non-blocking runtime-documentation risk. The installed skill is still the runtime authority and no repository launcher or runtime pin was restored. The validator must record the exact current-runtime artifact-status request and JSON response; prior validation evidence belongs to the superseded `f9651e45…` candidate and cannot accept this repaired fingerprint.
- Removal and active-instruction audit: `bin/preview-cad`, `tests/test_preview_cad_launcher.py`, and `projects/kage/manifests/cad-viewer-runtime-0.4.25.sha256` remain absent. Active instructions use the installed Viewer directly with the imported `.step`, absolute workspace, and workspace-relative file. Historical launcher records remain explicitly superseded history.
- Acceptance boundaries: preview page readiness, artifact readiness, and any visual observation remain separate from restart CAD, written-artifact/slicer, and physical print/assembly acceptance. Locked STEP SHA-256 remains `dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7`; `.gitignore` continues to exclude `__cadgen__/`.
- Focused deterministic evidence: Kage migration suite 7 passed; repository-structure suite 12 passed; candidate path order/uniqueness passed; `git diff --check` passed.

No Viewer or preview process was started, stopped, signaled, probed, or visually inspected during this recheck. Critic approval is limited to the repaired repository candidate and preservation/claim contracts; independent validation and formal-review gates remain separate.

## Formal independent-review join — KAGE-PREVIEW-DIRECT-005

**Verdict: ACCEPTED.** Repaired candidate
`da3bcedc68ed5324cf805f42ff0bca48cd1ccbcf89db7aa9207908b5df27f631`,
805 rows, may advance to root continuity and pull-request delivery. No critical,
high, medium, or other blocking finding remains.

- Formal reviewer: `/root/direct_viewer_formal_review`, distinct from design
  `/root/direct_viewer_design`, implementation `/root/direct_viewer_impl`, critic
  `/root/direct_viewer_critic`, and validator `/root/direct_viewer_validator`.
- Provenance and closure: baseline is
  `9c1ae27b9a856cb19c0dfefd497e5133987e2bd4`; the manifest fingerprint matched,
  its 805 paths were sorted and unique with final LF, and all 805/805 content hashes
  passed. The locked STEP remained
  `dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7`.
- Scope: `bin/preview-cad`, its root test suite, the Kage runtime-version pin, and
  obsolete Kage wrapper/test paths are absent. Active instructions use the installed
  `cad-viewer` workflow directly with the absolute Kage references workspace and the
  imported STEP selected relative to it. The Viewer runtime/source was not modified.
- `KPD-C-001` is resolved: `main` and retained branch
  `kage/restart-20260822` both resolve to
  `96b055d4b8d0b87f3e6132fa3d90b23b3be4ed84`; the old repository has exactly one
  registered worktree on `main`; both quarantine trees remain present with 25,227
  files each; and the retired active paths remain absent.
- `KPD-C-002` is resolved: active and frozen instructions permit only the factual
  general visual observation “the requested artifact rendered with no visible error
  state,” and require named features/views for any broader visual claim.
- `KPD-C-003` is satisfied for this installed runtime by the validator's exact
  evidence. The exact review page returned HTTP `200`; the exact
  `GET /__cad/artifact?dir=<absolute-workspace>&file=<relative-file>` request returned
  HTTP `200` and JSON `state == "ready"`. Inspection of the installed runtime also
  confirms this GET route and its `ready | needs-build | generating | error` state
  machine. Startup or URL production alone is not accepted evidence.
- Independent deterministic receipts join cleanly: critic PASS on the repaired
  fingerprint; validator PASS with 7 Kage tests, 12 repository-structure tests,
  candidate closure, removal scans, branch-retention checks, locked-STEP preservation,
  and `git diff --check` passing. The formal reviewer reran only read-only manifest,
  preservation, instruction, and endpoint-contract adjudication; it did not rerun the
  test suites or touch a Viewer process.
- Acceptance boundary: direct preview readiness is accepted for the exact locked
  historical STEP only. No loaded-page screenshot or visual inspection was available,
  so there is no no-visible-error or feature-specific visual claim. This accepts no
  restart CAD geometry, slicer/fabrication behavior, or physical print/assembly result.

Residual non-blocking risks are installed-runtime/API drift after upgrades, future
listener conflicts, and the still-pending visual observation. Root delivery must keep
the exact readiness wording and evidence boundary, update mutable continuity/handoff
records without changing the frozen candidate inputs, deliver through a non-`main`
branch and pull request, leave both Trash trees intact, and retain
`kage/restart-20260822`. The next design action remains `KAGE-EXP-001`.
