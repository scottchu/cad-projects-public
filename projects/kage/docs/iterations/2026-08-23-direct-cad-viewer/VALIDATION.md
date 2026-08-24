# Direct CAD Viewer validation

## Implementation self-check

Completed against candidate SHA-256 `f9651e45f78138553a252bd6eea68dd68a2eeae50aa94c26e1b580dee5254d3e`, 805 rows:

1. Absence checks for `bin/preview-cad`, `tests/test_preview_cad_launcher.py`, and `projects/kage/manifests/cad-viewer-runtime-0.4.25.sha256`: pass.
2. Active-document scan for those obsolete launcher/runtime instructions across root README/CAD workflow and Kage README/state/next: pass, no matches.
3. Candidate serialization: pass, 805 sorted unique rows with final LF.
4. `shasum -a 256 -c projects/kage/manifests/candidate.sha256`: pass, 805/805.
5. `uv run --package kage pytest projects/kage/tests -q`: pass, 7 tests.
6. `uv run pytest tests/test_repository_structure.py -q`: pass, 12 tests.
7. Locked STEP SHA-256: pass, `dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7`.
8. `git diff --check`: pass.

No live Viewer action or acceptance was performed by the implementation role.

## Independent validation

Validator `/root/direct_viewer_validator` independently validated frozen candidate
SHA-256 `f9651e45f78138553a252bd6eea68dd68a2eeae50aa94c26e1b580dee5254d3e`
with 805 rows against baseline `9c1ae27b9a856cb19c0dfefd497e5133987e2bd4`.

### Deterministic gates

- Candidate serialization: 805 rows, path-sorted and unique, with final LF; manifest
  SHA-256 matched the assigned fingerprint.
- Candidate closure: `shasum -a 256 -c projects/kage/manifests/candidate.sha256`
  passed 805/805 content hashes.
- Removed-file checks passed for `bin/preview-cad`,
  `tests/test_preview_cad_launcher.py`,
  `projects/kage/manifests/cad-viewer-runtime-0.4.25.sha256`, and the obsolete
  Kage-local wrapper/test paths.
- Active-document scan across the root README/CAD workflow and Kage
  README/state/next records found no stale launcher or runtime-manifest instruction.
- `uv run --package kage pytest projects/kage/tests -q`: 7 passed.
- `uv run pytest tests/test_repository_structure.py -q`: 12 passed.
- `git diff --check`: passed.
- Locked STEP SHA-256 remained
  `dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7`.

### Direct installed-Viewer evidence

Port `3245` was already occupied by Viewer PID `92119`; it was not stopped,
signalled, or reused for this gate. The validator used the explicit free port
`3246`, as directed by the installed `cad-viewer` skill. The successful direct
startup command was:

```sh
PATH=/Applications/ChatGPT.app/Contents/Resources/cua_node/bin:/usr/bin:/bin:/usr/sbin:/sbin \
VIEWER_CAD_PYTHON=/Users/scottchu/.codex/worktrees/b478a5e4-c0d0-4bb2-a265-df482c0a1937/design-projects/.venv/bin/python \
npm --prefix scripts/viewer run start -- --host 127.0.0.1 --port 3246
```

It was run from the installed skill directory
`/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.25/skills/cad-viewer`.
Server metadata reported app `cad-viewer`, backend `local-fs`, port `3246`, PID
`24443`, and `stepArtifactGenerationAvailable: true`.

Exact workspace and file:

```text
workspace: /Users/scottchu/.codex/worktrees/b478a5e4-c0d0-4bb2-a265-df482c0a1937/design-projects/projects/kage/references
file: locked-direct-gear/p3_v3_direct_gear_race_assembled.step
```

Exact page request:

```text
http://127.0.0.1:3246/Users/scottchu/.codex/worktrees/b478a5e4-c0d0-4bb2-a265-df482c0a1937/design-projects/projects/kage/references?file=locked-direct-gear%2Fp3_v3_direct_gear_race_assembled.step
```

Result: HTTP `200`, 1750 response bytes.

Exact artifact-status request, issued with `curl -G --data-urlencode`:

```text
http://127.0.0.1:3246/__cad/artifact?dir=%2fUsers%2fscottchu%2f.codex%2fworktrees%2fb478a5e4-c0d0-4bb2-a265-df482c0a1937%2fdesign-projects%2fprojects%2fkage%2freferences&file=locked-direct-gear%2fp3_v3_direct_gear_race_assembled.step
```

Result: HTTP `200` with the exact response:

```json
{
  "state": "ready",
  "ref": "/__cad/asset?file=%2FUsers%2Fscottchu%2F.codex%2Fworktrees%2Fb478a5e4-c0d0-4bb2-a265-df482c0a1937%2Fdesign-projects%2Fprojects%2Fkage%2Freferences%2Flocked-direct-gear%2F__cadgen__%2Fmodels%2Fp3_v3_direct_gear_race_assembled.step&dir=%2FUsers%2Fscottchu%2F.codex%2Fworktrees%2Fb478a5e4-c0d0-4bb2-a265-df482c0a1937%2Fdesign-projects%2Fprojects%2Fkage%2Freferences&v=2b87-dkwnq5qdut34"
}
```

### Visual gate and verdict

The Browser runtime was read and attempted against the exact page, but no browser
binding was available (`agent.browsers.list()` returned an empty list). Therefore
no loaded-page screenshot or visual inspection was possible. The validator makes
no claim that the render looks good and does not claim that a visible render-error
state was ruled out by sight.

Verdict for this fingerprint: **PASS for direct preview readiness** because the
mandatory exact page and exact artifact-state gates both passed. **Visual quality:
not validated**; a later agent may describe the render visually only after inspecting
the page or a snapshot and finding no visible render-error state. This operational
verdict does not accept restart CAD, source geometry, slicer behavior, or physical
print/assembly behavior.

The validator's Viewer process was left running on `127.0.0.1:3246`, PID `24443`.
Only this `VALIDATION.md` record was changed by the validator.

## Focused independent rerun — KAGE-PREVIEW-DIRECT-004-R1

Validator `/root/direct_viewer_validator` reran the invalidated gates against repaired
candidate SHA-256
`da3bcedc68ed5324cf805f42ff0bca48cd1ccbcf89db7aa9207908b5df27f631`,
805 rows. The earlier `f9651e45…` receipt above remains history and does not accept
this repaired fingerprint.

### Repaired-candidate gates

- Candidate fingerprint and row count matched the assignment; paths are sorted and
  unique, the file has a final LF, and all 805/805 content hashes passed.
- Removed-file and stale active launcher/runtime-manifest scans passed.
- The active/frozen direct-workflow instruction scan found none of the broad phrases
  `render looks good`, `render is visually good`, or `visually good`.
- `uv run --package kage pytest projects/kage/tests -q`: 7 passed.
- `uv run pytest tests/test_repository_structure.py -q`: 12 passed.
- `git diff --check`: passed.
- Locked STEP SHA-256 remained
  `dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7`.
- In `/Users/scottchu/Projects/personal/3d-print`, both `refs/heads/main` and
  `refs/heads/kage/restart-20260822` resolved exactly to
  `96b055d4b8d0b87f3e6132fa3d90b23b3be4ed84`. `git worktree list --porcelain`
  reported exactly one registered worktree, at that old repository root, on
  `refs/heads/main`. This independently closes the repaired branch-retention gate.

### Direct installed-Viewer recheck

The existing direct installed-Viewer process remained healthy on `127.0.0.1:3246`,
PID `24443`, with app `cad-viewer`, backend `local-fs`, and
`stepArtifactGenerationAvailable: true`. It was not stopped or signalled.

Exact page request:

```text
http://127.0.0.1:3246/Users/scottchu/.codex/worktrees/b478a5e4-c0d0-4bb2-a265-df482c0a1937/design-projects/projects/kage/references?file=locked-direct-gear%2Fp3_v3_direct_gear_race_assembled.step
```

Result: HTTP `200`, 1750 response bytes.

Exact artifact-status request:

```text
http://127.0.0.1:3246/__cad/artifact?dir=%2fUsers%2fscottchu%2f.codex%2fworktrees%2fb478a5e4-c0d0-4bb2-a265-df482c0a1937%2fdesign-projects%2fprojects%2fkage%2freferences&file=locked-direct-gear%2fp3_v3_direct_gear_race_assembled.step
```

Result: HTTP `200` with the exact response:

```json
{
  "state": "ready",
  "ref": "/__cad/asset?file=%2FUsers%2Fscottchu%2F.codex%2Fworktrees%2Fb478a5e4-c0d0-4bb2-a265-df482c0a1937%2Fdesign-projects%2Fprojects%2Fkage%2Freferences%2Flocked-direct-gear%2F__cadgen__%2Fmodels%2Fp3_v3_direct_gear_race_assembled.step&dir=%2FUsers%2Fscottchu%2F.codex%2Fworktrees%2Fb478a5e4-c0d0-4bb2-a265-df482c0a1937%2Fdesign-projects%2Fprojects%2Fkage%2Freferences&v=2b87-dkwnq5qdut34"
}
```

No visual inspection was performed in this focused rerun. The browser gate remains
unavailable from the earlier attempt, so this receipt makes no no-visible-error,
feature-specific, or broader visual-quality claim.

Verdict for repaired fingerprint `da3bcedc…`: **PASS for direct preview readiness**.
The exact page and artifact gates passed, the repaired branch-retention invariant
passed, and the visual-claim wording repair passed. Visual observation remains not
validated. This does not accept restart CAD, source geometry, slicer behavior, or
physical print/assembly behavior. The Viewer remains running on port `3246`.
