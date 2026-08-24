# Direct CAD Viewer handoff

## Implementation receipt

`KAGE-PREVIEW-DIRECT-002` is complete as implementation only.

- Baseline: branch `codex/simplify-cad-preview`, HEAD `9c1ae27b9a856cb19c0dfefd497e5133987e2bd4`.
- Frozen design receipt: `KAGE-PREVIEW-DIRECT-001`, design owner `/root/direct_viewer_design`.
- Implementation owner: `/root/direct_viewer_impl`.
- Candidate: `manifests/candidate.sha256` SHA-256 `f9651e45f78138553a252bd6eea68dd68a2eeae50aa94c26e1b580dee5254d3e`, 805 sorted unique final-LF rows; 805/805 content hashes pass.
- Frozen inputs: this iteration's `BRIEF.md` SHA-256 `16c52e943902d07fdcf464357f51b107708598e59bc7df2d34787440bd6f3997` and `DESIGN.md` SHA-256 `b927c83c1c84704e8a4e26d7d6bc6edd3a085abcda90db559eac38af8ea4e0a6`.
- Removed: root `bin/preview-cad`, root `tests/test_preview_cad_launcher.py`, and Kage `manifests/cad-viewer-runtime-0.4.25.sha256`.
- Updated: root `README.md` and `docs/CAD_WORKFLOW.md`; Kage `README.md`, `PROJECT_STATE.md`, `NEXT_AGENT.md`, `docs/iterations/CURRENT`, `tests/test_migration_integrity.py`, and `manifests/candidate.sha256`.
- Created: all five records in this iteration directory.
- Preserved: `.gitignore`'s `__cadgen__/` rule; every CAD/reference byte; reversible cleanup and Trash recovery state; retained branch; and CAD, slicer, and physical acceptance boundaries.
- Locked STEP verification: SHA-256 remains `dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7`.
- Live-process boundary: no Viewer was started, stopped, signaled, probed, or otherwise touched by implementation.

The active contract now uses the installed `cad-viewer` workflow directly. Page HTTP `200` and exact artifact HTTP `200`/JSON `ready` are both required before a ready link. After inspection, the general visual claim is limited to “the requested artifact rendered with no visible error state”; feature-specific claims must name the inspected features and views.

Residual risks are the installed-runtime drift, listener-conflict, and visual-evidence limitations recorded in `DESIGN.md`. They are workflow boundaries, not implementation acceptance; independent roles must assess them.

## Next gates

The initial critic required a focused repair; the original `f9651e45…` candidate must not advance. Distinct critic, validator, and formal reviewer roles must use the repaired candidate fingerprint recorded below. The validator alone performs the live direct-Viewer check and must record the exact page HTTP result, exact artifact HTTP/JSON state, and separate visual-inspection result. Startup or URL output alone supports no preview-readiness or visual claim. Implementation has not approved or committed the candidate.

## Focused implementation repair — KAGE-PREVIEW-DIRECT-002-R1

- Repaired candidate: `manifests/candidate.sha256` SHA-256 `da3bcedc68ed5324cf805f42ff0bca48cd1ccbcf89db7aa9207908b5df27f631`, 805 rows.
- Repaired frozen inputs: `BRIEF.md` SHA-256 `1e077da21ad8bd0721fe5d469b4563c4d486487e95c5ee4cad607b9d007fe72e`; `DESIGN.md` SHA-256 `1f19b9bb92cea1718de295460a8872a7e61f7317c22e434cfc744abda2168013`.
- `KPD-C-001` disposition: resolved. Before mutation, old-repository `main` was exactly `96b055d4b8d0b87f3e6132fa3d90b23b3be4ed84` and `refs/heads/kage/restart-20260822` was absent. Only that branch ref was restored with `git update-ref` at the exact commit. Post-check shows the branch at `96b055d…`, the sole registered worktree still on `main`, and the old worktree's pre-existing untracked paths unchanged.
- `KPD-C-002` disposition: resolved in every active/frozen direct-workflow instruction. The only general visual statement allowed after inspection is “the requested artifact rendered with no visible error state”; feature-specific claims must name the inspected features and views.
- `KPD-C-003` disposition: retained as a low runtime-documentation risk. Independent validation must record the exact installed-runtime artifact request and JSON result; it does not justify a repository launcher or runtime pin.
- Prior `REVIEW.md` and `VALIDATION.md` receipts remain unchanged history for `f9651e45…`; their results do not accept the repaired candidate.
- Live-process boundary: this repair did not start, stop, signal, probe, or otherwise touch either Viewer process.
- Deterministic repair gates: candidate serialization 805 sorted unique final-LF rows; 805/805 hashes pass; Kage tests 7 passed; repository-structure tests 12 passed; locked STEP hash unchanged; exact old-repository `main` and restored-branch refs pass; one-worktree invariant passes; active/frozen broad-claim scan passes; `git diff --check` passes.

## Final independent acceptance and delivery handoff

- Formal verdict: `KAGE-PREVIEW-DIRECT-005` accepted repaired candidate `da3bcedc68ed5324cf805f42ff0bca48cd1ccbcf89db7aa9207908b5df27f631`, 805 rows, after distinct design, implementation, critic, validator, and formal-review roles.
- Removal: `bin/preview-cad`, `tests/test_preview_cad_launcher.py`, and `manifests/cad-viewer-runtime-0.4.25.sha256` are absent. The installed `cad-viewer` skill is the sole runtime authority.
- Independent readiness evidence: the exact Kage review page returned HTTP `200`; the exact artifact-status request returned HTTP `200` with JSON `state == "ready"` on the directly started installed Viewer at `127.0.0.1:3246`, PID `24443`.
- Visual evidence: no browser binding was available, so no visual inspection was performed and no no-visible-error, feature-specific, or broader visual-quality claim is accepted.
- Finding dispositions: `KPD-C-001` and `KPD-C-002` are resolved; `KPD-C-003` is satisfied for the observed runtime by the validator's recorded exact request and JSON response. No blocking finding remains.
- Preservation: the locked STEP remains `dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7`; both Trash trees remain intact; `kage/restart-20260822` is restored and retained at `96b055d4b8d0b87f3e6132fa3d90b23b3be4ed84`; the old repository still has only its `main` worktree registered.
- Acceptance boundary: direct preview readiness only. Restart CAD/source, slicer/fabrication, physical print/assembly, and unperformed visual observation remain unaccepted.
- Root delivery: accepted candidate committed as `e7dbb5f9ec3c84e5ca457062be19c2f89307faa1` on `codex/simplify-cad-preview` and delivered through pull request [#6](https://github.com/scottchu/design-projects/pull/6). Retain the branch and Trash recovery state; `KAGE-EXP-001` remains the sole next design action.
