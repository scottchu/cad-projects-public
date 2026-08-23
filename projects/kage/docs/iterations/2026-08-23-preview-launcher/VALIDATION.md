# Preview launcher validation

## Independent validator receipt — KAGE-PREVIEW-004

- Validator provenance: `/root/kage_preview_validator`, validation/test role, distinct from design and implementation.
- Status: **failed** on the controlled real-launch gate; deterministic source/test gates passed.
- Candidate fingerprint before validation: `projects/kage/manifests/candidate.sha256` SHA-256 `715e85c7d189805102b2306f8544dd200dcf4d88e78b5434fb8ed69dae654307`, 802 rows.
- Candidate fingerprint after validation: unchanged at `715e85c7d189805102b2306f8544dd200dcf4d88e78b5434fb8ed69dae654307`, 802 rows; this mutable receipt is excluded from the candidate closure.
- Frozen inputs verified: preview `BRIEF.md` `8f33d9d913414fc20666674adbaff1d9e5171edd74225e4b0edf131c01e7b034`; preview `DESIGN.md` `6b287e139bd5dd25026213b557cadb530360dbec612087941ad657546dec87c3`; locked STEP `dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7`.
- Read-only status: source, tests, manifests, CAD/reference files, generated artifacts, Git, and PR state were not modified. This receipt is the validator's only write.

## Deterministic gates

All commands ran from the repository root on branch `codex/kage-retire-legacy-folders` unless stated otherwise.

1. Independent Python recomputation of the final-LF manifest, sorted/unique path set, intended-candidate closure, and each declared content hash: `802/802`; recomputed manifest SHA-256 `715e85c7d189805102b2306f8544dd200dcf4d88e78b5434fb8ed69dae654307`. Mutable evidence records and runtime debris including `__cadgen__` were excluded as declared.
2. `sh -n projects/kage/bin/preview-cad`: pass.
3. `[ -x projects/kage/bin/preview-cad ]` and `stat -f 'launcher_mode=%Lp' projects/kage/bin/preview-cad`: pass; mode `755`.
4. `uv run --package kage pytest projects/kage/tests/test_preview_cad.py -q`: pass, `7 passed`.
5. `uv run --package kage pytest projects/kage/tests -q`: pass, `14 passed`.
6. `uv run pytest tests/test_repository_structure.py -q`: pass, `12 passed`.
7. `git diff --check`: pass, no output.

## Controlled real launch

Preflight found no listener on port 3245:

- `lsof -nP -iTCP:3245 -sTCP:LISTEN -Fpnc`: no output.
- `curl -sS --max-time 3 -w '\nHTTP_STATUS=%{http_code}\n' 'http://127.0.0.1:3245/__cad/server?dir=<encoded-absolute-references-path>'`: connection refused, HTTP `000`.

From non-project working directory `/tmp`, the validator ran the absolute launcher path with stdout and stderr captured separately:

`/Users/scottchu/.codex/worktrees/b478a5e4-c0d0-4bb2-a265-df482c0a1937/design-projects/projects/kage/bin/preview-cad`

- Exit status: `1`.
- Exact stdout: empty.
- Exact stderr:

```text
preview-cad: starting CAD Viewer runtime 0.4.25 on port 3245
preview-cad: CAD Viewer did not become healthy within 20 polls
```

Post-failure `lsof -nP -iTCP:3245 -sTCP:LISTEN -Fpnc` was empty; no live Viewer or unknown listener remained.

### Finding KAGE-PREVIEW-VAL-001 — high

The required bundled-npm fallback fails in the actual environment when plain `npm` and `node` are absent from `PATH`. The launcher correctly selects `/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/npm`, but it invokes that executable without adding its directory to `PATH`. The bundled npm wrapper can start itself with its adjacent Node binary, while the Viewer package's `start` script is `node scripts/start-viewer.mjs`; that child bare `node` cannot resolve. Evidence: `command -v npm` and `command -v node` returned no path, both bundled executables exist, bundled npm reports version `11.17.0`, the selected runtime `package.json` declares the bare-`node` start script, and the launcher never created a listener.

Disposition: unresolved. Implementation must make bundled-node resolution explicit, add a hermetic regression that exercises a real npm-style child bare-`node` lookup rather than a self-contained npm stub, regenerate the candidate manifest, and return the changed fingerprint for independent rerun. No second live invocation was made against this failed candidate.

## URL and artifact evidence

- Local URL: none printed; page HTTP 200/root-marker gate not reached.
- `/__cad/server` app identity after launch: not reachable; gate not reached.
- Artifact GET/POST state: not reachable; `state == ready` not established.
- Tailscale URL/status: none printed, so no external fetch was attempted.
- Locked STEP hash after the failed launch: `dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7`, unchanged.

## Acceptance boundary

Preview-launcher acceptance is blocked by `KAGE-PREVIEW-VAL-001`. The passing hermetic tests do not override the failed real fallback path. This validation does not accept restart CAD/source, a fabrication or slicer artifact, or physical print/assembly behavior; the served STEP remains a locked historical reference only.

## R2 implementation self-check — KAGE-PREVIEW-002

The invalid Kage-local launcher/test was removed and superseded by root `bin/preview-cad` and `tests/test_preview_cad_launcher.py`. No live launch was run. The generic CLI validates workspace containment and optional checksum before listener actions; Kage remains a pinned consumer. Self-check: root focused tests passed (3), Kage suite passed after manifest regeneration, repository structure and shell syntax remain pending independent validation. This is implementation evidence only, not acceptance.

## Repair cycle 2 implementation self-check — KAGE-PREVIEW-002

Root rejected incomplete candidate `a489fbe8496ae2d8eaf4309c06bd3ec9339277e37b59fab9c7a4fd6934d81c9e` (805 rows): three root tests did not cover the frozen lifecycle and signaling contract, and the launcher did not safely establish process/API ownership or complete stale/owned cleanup. Repair cycle 2 supersedes that candidate; the earlier failed evidence above remains historical and does not transfer acceptance. The superseding implementation uses stateful executable stubs and state files without touching a real listener, process, Viewer cache, network, or reference artifact. This is implementation self-check evidence only; distinct critic, validator, and formal-review gates remain required on the final fingerprint.

- Final implementation candidate: `3d6609aa35269072f8bad57e45d85cf0463646a6201f761f30e7feb6000c539f`, 805 sorted unique final-LF rows.
- `sh -n bin/preview-cad` and executable-mode check: pass; mode `755`.
- `uv run pytest tests/test_preview_cad_launcher.py -q`: pass, `23 passed`.
- `uv run --package kage pytest projects/kage/tests -q`: pass, `7 passed` (active suite remains migration-integrity only).
- `uv run pytest tests/test_repository_structure.py -q`: pass, `12 passed`.
- `sha256sum -c projects/kage/manifests/cad-viewer-runtime-0.4.25.sha256`: pass, all six installed-runtime inputs `OK`.
- Independent candidate path/hash recomputation: pass, `805/805`; manifest SHA-256 `3d6609aa35269072f8bad57e45d85cf0463646a6201f761f30e7feb6000c539f`.
- `git diff --check`: pass.
- Frozen contract/reference recheck: `BRIEF.md` `a2ec89d957d34a167cd764cd18cf4e7b0826d1188f9717c348d9c9b49a749d7b`; `DESIGN.md` `4465830780883d0efd83f62c568450a1ace504fc6884fb862e2984924b1521ab`; locked STEP `dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7`.
- No live Viewer launch, port access, real process signal, cache mutation, commit, pull-request action, or acceptance action was performed.

## R2 independent validation rerun — KAGE-PREVIEW-004

- Validator provenance: `/root/kage_preview_validator`, independent validation/test role, distinct from design, implementation, critic, and formal review.
- Status: **passed** for repository-launcher and checksum-pinned Kage-consumer scope.
- Candidate fingerprint before validation: `projects/kage/manifests/candidate.sha256` SHA-256 `3d6609aa35269072f8bad57e45d85cf0463646a6201f761f30e7feb6000c539f`, 805 rows.
- Candidate fingerprint after validation: unchanged at `3d6609aa35269072f8bad57e45d85cf0463646a6201f761f30e7feb6000c539f`, 805 rows; this mutable receipt and generated `__cadgen__` cache are excluded from candidate closure.
- Frozen inputs verified: R2 `BRIEF.md` `a2ec89d957d34a167cd764cd18cf4e7b0826d1188f9717c348d9c9b49a749d7b`; R2 `DESIGN.md` `4465830780883d0efd83f62c568450a1ace504fc6884fb862e2984924b1521ab`; locked STEP `dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7`.
- Read-only status: source, tests, manifests, CAD/reference bytes, Git, and PR state were not modified. This appended receipt is the validator's only write. The healthy Viewer was intentionally left running.

### Deterministic gates

All commands ran from the repository root on branch `codex/kage-retire-legacy-folders` unless stated otherwise.

1. Independent Python recomputation of manifest final LF, sorted/unique paths, intended-candidate closure, and every declared content hash: `805/805`; manifest SHA-256 `3d6609aa35269072f8bad57e45d85cf0463646a6201f761f30e7feb6000c539f`.
2. `sh -n bin/preview-cad`: pass.
3. `[ -x bin/preview-cad ]` and `stat -f 'launcher_mode=%Lp' bin/preview-cad`: pass; mode `755`.
4. `uv run pytest tests/test_preview_cad_launcher.py -q`: pass, `23 passed`.
5. `uv run --package kage pytest projects/kage/tests -q`: pass, `7 passed`.
6. `uv run pytest tests/test_repository_structure.py -q`: pass, `12 passed`.
7. `sha256sum -c projects/kage/manifests/cad-viewer-runtime-0.4.25.sha256`: pass, all six installed runtime paths `OK`.
8. `git diff --check`: pass, no output.

### Controlled live launch and endpoint evidence

Preflight `lsof -nP -iTCP:3245 -sTCP:LISTEN -Fpnc` returned no listener. The corresponding local `GET /__cad/server` probe was connection refused with HTTP `000`, so starting a new Viewer was safe.

From `/tmp`, the validator ran:

```text
/Users/scottchu/.codex/worktrees/b478a5e4-c0d0-4bb2-a265-df482c0a1937/design-projects/bin/preview-cad --sha256 dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7 /Users/scottchu/.codex/worktrees/b478a5e4-c0d0-4bb2-a265-df482c0a1937/design-projects/projects/kage/references locked-direct-gear/p3_v3_direct_gear_race_assembled.step
```

Exit status was `0`. Stdout contained exactly two lines:

```text
http://127.0.0.1:3245/Users/scottchu/.codex/worktrees/b478a5e4-c0d0-4bb2-a265-df482c0a1937/design-projects/projects/kage/references?file=locked-direct-gear%2Fp3_v3_direct_gear_race_assembled.step&cb=1787526470
https://mac-mini.duckbill-ionian.ts.net/Users/scottchu/.codex/worktrees/b478a5e4-c0d0-4bb2-a265-df482c0a1937/design-projects/projects/kage/references?file=locked-direct-gear%2Fp3_v3_direct_gear_race_assembled.step&cb=1787526470
```

Exact stderr:

```text
preview-cad: starting CAD Viewer runtime 0.4.25 from /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.25/skills/cad-viewer
preview-cad: workspace: /Users/scottchu/.codex/worktrees/b478a5e4-c0d0-4bb2-a265-df482c0a1937/design-projects/projects/kage/references
preview-cad: startup log: /var/folders/p1/g0fbbwtx3jqcj7vdr2198_dc0000gn/T//preview-cad-91977.log
```

Independent post-launch checks:

- `lsof` reported exactly one listener, PID `92119`, command `python3.12`, bound to `127.0.0.1:3245`.
- `GET /__cad/server?dir=<encoded-workspace>` returned HTTP `200`, `app: cad-viewer`, `pid: 92119`, and the exact Kage references root; API PID matched the sole listener.
- GET of the printed local URL returned HTTP `200` and contained `id="root"`.
- `GET /__cad/artifact?dir=<encoded-workspace>&file=<encoded-file>` returned HTTP `200` with `state: ready`.
- Separate GET of the printed external HTTPS URL returned HTTP `200`; the external URL contains no `:3245`.
- Locked STEP SHA-256 after launch remained `dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7`.

### Prior finding disposition

`KAGE-PREVIEW-VAL-001` is **resolved** by the superseding R2 candidate. The root launcher prepends the selected npm directory to the child environment's `PATH`; the real environment again had no plain `npm` or `node` on `PATH`, yet bundled npm successfully launched runtime 0.4.25 and completed every live readiness gate. The 23-test root suite includes a bundled-npm child bare-`node` regression.

### Acceptance boundary

The repository-level preview launcher and Kage's checksum-pinned consumer invocation are independently validated on this machine. This validates only Viewer launch, ownership/identity, URL, and imported-artifact readiness. It does not accept restart CAD/source, fabrication or slicer output, or physical print/assembly behavior; the Kage STEP remains a locked historical reference.

## R3 implementation self-check — KAGE-PREVIEW-002

Independent critique invalidated R2 candidate `3d6609aa35269072f8bad57e45d85cf0463646a6201f761f30e7feb6000c539f` despite its controlled live pass: unconditional process-group `KILL`, stale-listener `KILL`, missing owned-leader generation revalidation, post-TERM API handling, and final listener-token equality were not safe enough for delivery. R3 preserves that live evidence only as history; none of its acceptance transfers to this candidate.

- Final R3 implementation candidate: `495265a08a78dcd5fd2639ab41e8e9ef0aa62595e106f1229b6fa7a6355ed60a`, 805 sorted unique final-LF rows.
- `sh -n bin/preview-cad` and executable-mode check: pass; mode `755`.
- Static production check for `-KILL`, `PRE_KILL`, `kill_wait`, `$KILL`, or `KILL=` action paths: pass; no match.
- `uv run pytest tests/test_preview_cad_launcher.py -q`: pass, `27 passed`.
- `uv run --package kage pytest projects/kage/tests -q`: pass, `7 passed` (active suite remains migration-integrity only).
- `uv run pytest tests/test_repository_structure.py -q`: pass, `12 passed`.
- `sha256sum -c projects/kage/manifests/cad-viewer-runtime-0.4.25.sha256`: pass, all six installed-runtime inputs `OK`.
- Independent candidate path/hash recomputation: pass, `805/805`; manifest SHA-256 `495265a08a78dcd5fd2639ab41e8e9ef0aa62595e106f1229b6fa7a6355ed60a`.
- `git diff --check`: pass.
- Frozen R3 contract/reference recheck: `BRIEF.md` `17c969e6c0b31c4cd82bcec454dce4c359221dd41b25b6e7043c94c779eb3f7f`; `DESIGN.md` `5beff97b9e3bd1c277bd1d59e3ee6bce508c398f394b752587e9d323908e0bdd`; locked STEP `dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7`.
- R3 regressions verify no signal for an absent, drifted, or never-captured owned leader; one group `TERM` only for an exact leader-generation match; no escalation when a stale listener persists; restart after post-TERM API loss and port release; and no URL stdout after final listener-token replacement.
- No live Viewer launch, port access, real process signal, cache mutation, commit, pull-request action, or acceptance action was performed for R3 implementation.

## Final R3 independent validation rerun — KAGE-PREVIEW-004

- Validator provenance: `/root/kage_preview_validator`, independent validation/test role, distinct from design, implementation, critic, and formal review.
- Status: **passed** for the final R3 repository-launcher and checksum-pinned Kage-consumer scope.
- Candidate fingerprint before validation: `projects/kage/manifests/candidate.sha256` SHA-256 `495265a08a78dcd5fd2639ab41e8e9ef0aa62595e106f1229b6fa7a6355ed60a`, 805 rows.
- Candidate fingerprint after validation: unchanged at `495265a08a78dcd5fd2639ab41e8e9ef0aa62595e106f1229b6fa7a6355ed60a`, 805 rows; mutable evidence and generated `__cadgen__` cache remain excluded from candidate closure.
- Frozen inputs verified: R3 `BRIEF.md` `17c969e6c0b31c4cd82bcec454dce4c359221dd41b25b6e7043c94c779eb3f7f`; R3 `DESIGN.md` `5beff97b9e3bd1c277bd1d59e3ee6bce508c398f394b752587e9d323908e0bdd`; locked STEP `dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7`.
- Read-only status: source, tests, manifests, CAD/reference bytes, Git, and PR state were not modified. This appended receipt is the validator's only write. The healthy Viewer was intentionally left running.

### Final deterministic gates

All commands ran from the repository root on branch `codex/kage-retire-legacy-folders` unless stated otherwise.

1. Independent Python recomputation of manifest final LF, sorted/unique paths, intended-candidate closure, and every declared content hash: `805/805`; manifest SHA-256 `495265a08a78dcd5fd2639ab41e8e9ef0aa62595e106f1229b6fa7a6355ed60a`.
2. `sh -n bin/preview-cad`: pass.
3. `[ -x bin/preview-cad ]` and `stat -f 'launcher_mode=%Lp' bin/preview-cad`: pass; mode `755`.
4. Static `rg -n -- '-KILL' bin/preview-cad` negative check: pass; production contains no `-KILL` path.
5. `uv run pytest tests/test_preview_cad_launcher.py -q`: pass, `27 passed`.
6. Focused node-id rerun covering matched-owned-group `TERM` only, absent/drifted/never-captured owned generation tokens, final listener-token replacement, and post-TERM API loss followed by port release: pass, `7 passed`.
7. `uv run --package kage pytest projects/kage/tests -q`: pass, `7 passed`.
8. `uv run pytest tests/test_repository_structure.py -q`: pass, `12 passed`.
9. `sha256sum -c projects/kage/manifests/cad-viewer-runtime-0.4.25.sha256`: pass, all six installed runtime paths `OK`.
10. `git diff --check`: pass, no output.

The focused lifecycle evidence specifically passed:

- `test_matched_owned_startup_failure_sends_group_term_only`;
- both cases of `test_owned_leader_absent_or_drifted_at_cleanup_gets_no_signal`;
- `test_owned_leader_never_captured_gets_no_signal`;
- `test_final_listener_token_replacement_suppresses_both_urls`;
- `test_post_term_api_loss_then_port_free_starts_current_runtime`.

### Controlled live reuse and endpoint evidence

Preflight found exactly one listener on port 3245: PID `92119`, command `python3.12`, bound to `127.0.0.1:3245`. `GET /__cad/server?dir=<encoded-workspace>` returned `app: cad-viewer`, `pid: 92119`, and the exact Kage references root. The API PID matched the sole listener. Its generation record before reuse was:

```text
Sun Aug 23 19:07:53 2026 /Users/scottchu/.codex/worktrees/b478a5e4-c0d0-4bb2-a265-df482c0a1937/design-projects/.venv/bin/python -m server_py.server --host 127.0.0.1 --port 3245
```

From `/tmp`, the validator ran:

```text
/Users/scottchu/.codex/worktrees/b478a5e4-c0d0-4bb2-a265-df482c0a1937/design-projects/bin/preview-cad --sha256 dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7 /Users/scottchu/.codex/worktrees/b478a5e4-c0d0-4bb2-a265-df482c0a1937/design-projects/projects/kage/references locked-direct-gear/p3_v3_direct_gear_race_assembled.step
```

Exit status was `0`. Exact stderr was `preview-cad: reusing healthy CAD Viewer PID 92119`. Stdout contained exactly two lines:

```text
http://127.0.0.1:3245/Users/scottchu/.codex/worktrees/b478a5e4-c0d0-4bb2-a265-df482c0a1937/design-projects/projects/kage/references?file=locked-direct-gear%2Fp3_v3_direct_gear_race_assembled.step&cb=1787527287
https://mac-mini.duckbill-ionian.ts.net/Users/scottchu/.codex/worktrees/b478a5e4-c0d0-4bb2-a265-df482c0a1937/design-projects/projects/kage/references?file=locked-direct-gear%2Fp3_v3_direct_gear_race_assembled.step&cb=1787527287
```

Independent post-reuse checks:

- the sole listener remained PID `92119` with the same start time and command, so no replacement occurred;
- `GET /__cad/server` returned HTTP `200`, `app: cad-viewer`, and matching PID `92119`;
- GET of the printed local URL returned HTTP `200` and contained `id="root"`;
- `GET /__cad/artifact?dir=<encoded-workspace>&file=<encoded-file>` returned HTTP `200` with `state: ready`;
- separate GET of the printed external HTTPS URL returned HTTP `200`, and the URL contains no `:3245`;
- locked STEP SHA-256 remained `dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7`;
- candidate manifest SHA-256 remained `495265a08a78dcd5fd2639ab41e8e9ef0aa62595e106f1229b6fa7a6355ed60a`, 805 rows.

No signal was sent during this validation; the existing healthy Viewer was reused and left running.

### Final acceptance boundary

The final R3 repository-level preview launcher and Kage's checksum-pinned consumer invocation are independently validated on this machine. This validates only process-safety behavior, Viewer reuse/identity, URL output, and imported-artifact readiness. It does not accept restart CAD/source, fabrication or slicer output, or physical print/assembly behavior; the Kage STEP remains a locked historical reference.
