# CAD Viewer singleton service validation (CVS-V02)

Validator: P17-V04/CVS-V02 independent live validator
Date: 2026-08-24
Worktree: `/Users/scottchu/.codex/worktrees/a373f6e6-90f4-4c0e-857b-643add242937/design-projects`
Branch: `codex/xt60-p17-r2-direct-cad`
HEAD: `cb020f6cf01876e01d1e6501fec8861a527aa248`

## Top status

FAIL.

The managed singleton service installed, migrated the legacy label, survived restart/crash/stop/foreign-port checks, and was left running on `127.0.0.1:3245`. However, the installed stable command `/Users/scottchu/.local/bin/cad-viewer` is a no-op for at least `status --json` and `start --json`: it exits 0 with zero stdout/stderr. This violates the explicit acceptance requirement that stable `~/.local/bin/cad-viewer status --json` works from a fresh shell.

Observed root cause: the stable shim invokes `/Users/scottchu/Library/Application Support/CADViewer/service/current/cli.mjs`; Node resolves that symlink to the content-addressed release path, so the CLI module's entrypoint guard comparing `process.argv[1]` with `import.meta.url` does not run `main()`.

No source/tests/design/CAD files were edited. Only this validation receipt was written in the repo. Authorized user-state install/launchd changes were performed.

## Frozen inputs and hashes

- Expected DESIGN hash: `9955f707...`; observed:
  - `9955f7078747aa280407f86febe7ed478bf63252bf660ba8f3fc183b253179a5  tools/cad-viewer-service/DESIGN.md`
- Expected candidate payload/install-manifest hash: `83e77c8735e32c49ea494ef90d76cc5d435614b2a9474efe4f64688ac4f634c0`; observed:
  - `83e77c8735e32c49ea494ef90d76cc5d435614b2a9474efe4f64688ac4f634c0  tools/cad-viewer-service/payload/install-manifest.json`
- Required instruction hashes recorded:
  - `22a4b39ab1439018f2570d0d90326f700f07647ae399a34655a8a5be347382c5  AGENTS.md`
  - `55eaba17c19970620d203fb187ef4cf95928498e9e3ede744ab7accebd603d7c  docs/CAD_WORKFLOW.md`
  - `fbe7f1f41b1f9f9f1a46e13cec1c5d9cd319a512ec6d13c9ac52c1f65417266a  cad-viewer/SKILL.md`
- Implementation file hashes recorded before live work:
  - `2ad373107d6579251358cb4572429ed101c4fff9c6b2f7e11cd787c0ed17c9ff  tools/cad-viewer-service/bin/cad-viewer`
  - `998bb2b6d0cce1354ceb245e721c53fdfd8054703b8b976cb67e39be28563484  tools/cad-viewer-service/payload/bin/cad-viewer`
  - `82d2d04d571a986bc43aabac064dd5cf3696e0d2428c7f0cac0a4f6a76e1659f  tools/cad-viewer-service/payload/cli.mjs`
  - `17d2ce9076bc17526c55101cc4f67352cf6277180899a1dd9390a520c59a6082  tools/cad-viewer-service/payload/config.mjs`
  - `ec583ddabd75b42fd4e9ccfdd1d1ba64f39570f303c9e8b46ebe18e0d094fdf2  tools/cad-viewer-service/payload/core.mjs`
  - `2d4025bd45ea0e3bd9bc03ad97ae51a4afe253cab948d1c223ce06b9eb63f74e  tools/cad-viewer-service/payload/install.mjs`
  - `4b93a4ac35c791c95b68c296893a2b143dfec61967a8604f808056d8471f25f5  tools/cad-viewer-service/payload/launch-viewer.mjs`
  - `52a18ae746d6e44a897f8b307e6eeb2819d0f746bd305c7833ffa6d8b90eeed5  tools/cad-viewer-service/payload/launchd/com.scottchu.cad-viewer.plist.template`
  - `5b5924a960093331e0524f7a054e29e573991bf88613797dffc76e14e410a6a1  tools/cad-viewer-service/tests/core.test.mjs`
  - `96adde00ccc98be4f209e03ecbde78c6f0384655ed979da70456ef12a2f2478d  tools/cad-viewer-service/tests/install.test.mjs`

I did not find a separate checked-in implementation receipt under `tools/` or `docs/`; the task handoff text was treated as the implementation receipt boundary.

## Read-only checks before live install

Commands:

```sh
/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node --test tools/cad-viewer-service/tests/*.test.mjs
/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node tools/cad-viewer-service/scripts/generate-install-manifest.mjs --check
/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node --check tools/cad-viewer-service/payload/cli.mjs
/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node --check tools/cad-viewer-service/payload/install.mjs
/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node --check tools/cad-viewer-service/payload/launch-viewer.mjs
plutil -lint <rendered plist fixture>
```

Results:

- Node tests: 16 passed, 0 failed.
- Manifest check: `install-manifest.json is current`.
- JS syntax checks: pass.
- Rendered plist lint: `OK`.

The checked-in tests cover manifest canonicality/modes/hashes, release switching, rollback helpers, stale lock behavior, runtime selection, source bans on Homebrew Python and pinned Viewer runtime, URL containment, and rendered plist validity.

## Pre-live state

- `launchctl print gui/501/com.scottchu.cad-viewer`: not found.
- `launchctl print gui/501/com.codex.cad-viewer`: running legacy submitted job.
- Legacy job:
  - label: `com.codex.cad-viewer`
  - job PID: `84510`
  - listener: PID `84559`, command `python3.12`, `127.0.0.1:3245`
  - legacy arguments included:
    - `VIEWER_CAD_PYTHON=/Users/scottchu/.codex/worktrees/a373f6e6-90f4-4c0e-857b-643add242937/design-projects/.venv/bin/python3`
    - plugin runtime `/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.25/skills/cad-viewer/scripts/viewer`
- Pre-existing `/__cad/server` responded HTTP 200; captured hash:
  - `f7ff3f68f84b5f25663fc6f1269d0d1b890f5956b96a1634b850f16af1e7e50c  /tmp/cvs-pre-server.json`
- Tailscale Serve pre-state:
  - command: `tailscale serve status --json`
  - exit: 0
  - bytes: 221
  - hash: `5037675750347d2e9d6e4fafe5dbf66912c59404bc28cb320cb3f3fc19069cef`

The legacy state matched the contract's narrow migration scope; no arbitrary PID was killed directly.

## Live installation and lifecycle evidence

### Start/install/migration

Command:

```sh
tools/cad-viewer-service/bin/cad-viewer start --json
```

Result: exit 0.

Key JSON:

- `state:"running"`
- `enabled:true`
- `loaded:true`
- `jobPid:91011`
- backend listener PID `91074`, command `python3.12`
- `payloadHash:"83e77c8735e32c49ea494ef90d76cc5d435614b2a9474efe4f64688ac4f634c0"`
- `payloadChanged:true`
- `migratedLegacy:true`

After migration:

- `com.codex.cad-viewer` no longer existed in `launchctl`.
- `com.scottchu.cad-viewer` existed as a LaunchAgent at `/Users/scottchu/Library/LaunchAgents/com.scottchu.cad-viewer.plist`.
- Page HTTP check: `http://127.0.0.1:3245/` returned HTTP 200, 1750 bytes.
- Server check: `http://127.0.0.1:3245/__cad/server` returned HTTP 200, 289 bytes, JSON including:
  - `app:"cad-viewer"`
  - `port:3245`
  - `pid:91074`
  - `url:"http://127.0.0.1:3245"`

Installed path checks:

- `current -> releases/83e77c8735e32c49ea494ef90d76cc5d435614b2a9474efe4f64688ac4f634c0`
- Installed release file hashes matched source manifest entries:
  - `998bb2b6...  bin/cad-viewer`
  - `82d2d04d...  cli.mjs`
  - `17d2ce90...  config.mjs`
  - `ec583dda...  core.mjs`
  - `2d4025bd...  install.mjs`
  - `4b93a4ac...  launch-viewer.mjs`
  - `52a18ae7...  launchd/com.scottchu.cad-viewer.plist.template`
  - `83e77c87...  install-manifest.json`
- Stable shim hash:
  - `998bb2b6d0cce1354ceb245e721c53fdfd8054703b8b976cb67e39be28563484  /Users/scottchu/.local/bin/cad-viewer`
- LaunchAgent plist hash:
  - `5242e7dbab90c2e53e636ab660bd5df254bf36e2ca0d835365e4fb2e8577075d  /Users/scottchu/Library/LaunchAgents/com.scottchu.cad-viewer.plist`
- Grep for this live worktree path in release/stable shim/plist produced no matches.
- Expected canonical Python was present in installed config and process environment:
  - `/Users/scottchu/Projects/personal/design-projects/.venv/bin/python3`
- Backend process environment included:
  - `VIEWER_CAD_PYTHON=/Users/scottchu/Projects/personal/design-projects/.venv/bin/python3`

Observed ancestry:

```text
91074 91041 /Users/scottchu/Projects/personal/design-projects/.venv/bin/python3
91041 91040 /Users/scottchu/Projects/personal/design-projects/.venv/bin/python3
91040 91019 node
91019 91011 npm run start --host 127.0.0.1 --port 3245 --json
91011     1 /Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node
    1     0 /sbin/launchd
```

### Idempotent start

Commands:

```sh
tools/cad-viewer-service/bin/cad-viewer start --json
tools/cad-viewer-service/bin/cad-viewer start --json
```

Result: both exited 0 and reported:

- `state:"running"`
- `jobPid:91011`
- listener PID `91074`
- message: `CAD Viewer is already running with this payload; PID unchanged`

`lsof` showed one listener on `127.0.0.1:3245`.

### Restart

Command:

```sh
tools/cad-viewer-service/bin/cad-viewer restart --json
```

Result: exit 0.

- Before restart: job/backend `91011/91074`
- After restart: job/backend `91330/91400`
- `payloadChanged:false`
- `migratedLegacy:false`
- one listener on `127.0.0.1:3245`

### Crash recovery

Command:

```sh
launchctl kill SIGKILL gui/501/com.scottchu.cad-viewer
```

Result:

- Service temporarily reported `state:"starting"` while launchd throttle elapsed.
- Recovered without direct PID kill to:
  - job PID `91478`
  - backend PID `91535`
  - `state:"running"`
  - one listener on `127.0.0.1:3245`

### Stop/disabled

Command:

```sh
tools/cad-viewer-service/bin/cad-viewer stop --json
```

Result: exit 0.

- `state:"disabled"`
- `enabled:false`
- `loaded:false`
- no port owner
- `launchctl print-disabled gui/501` included `"com.scottchu.cad-viewer" => disabled`

Follow-up status exited 1 with `state:"disabled"`.

### Foreign-port safety

Fixture:

```sh
/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node -e '...listen(3245,"127.0.0.1")...'
```

Fixture PID: `91600`.

Command under test:

```sh
tools/cad-viewer-service/bin/cad-viewer start --json
```

Result: exit 2.

JSON:

```json
{"ok":false,"command":"start","state":"blocked","error":"Port 3245 is owned by an unmanaged process; it was left alive and service state was not enabled","portOwners":[{"pid":91600,"command":"node"}]}
```

Verified:

- Fixture PID `91600` remained alive.
- `launchctl print-disabled gui/501` still contained `"com.scottchu.cad-viewer" => disabled`.
- Status reported `state:"blocked"`, `enabled:false`, `loaded:false`.

The disposable fixture was removed by sending Ctrl-C only to the tool session that created it. The managed service was then restored with:

```sh
tools/cad-viewer-service/bin/cad-viewer start --json
```

Restored state:

- job PID `91660`
- backend PID `91723`
- `state:"running"`
- one listener on `127.0.0.1:3245`

## Stable installed command failure

Required check:

```sh
/bin/zsh -f -c '/Users/scottchu/.local/bin/cad-viewer status --json'
```

Observed:

```text
stable_status_exit=0
       0 /tmp/cvs-stable-status.out
       0 /tmp/cvs-stable-status.err
       0 total
```

Additional check:

```sh
/bin/zsh -f -c '/Users/scottchu/.local/bin/cad-viewer start --json'
```

Observed:

```text
stable_start_exit=0
       0 /tmp/cvs-stable-start.out
       0 /tmp/cvs-stable-start.err
       0 total
```

The same CLI works when invoked through the checked-in source shim because that path passes `--source-root` and does not go through the `current` symlink entrypoint mismatch:

```sh
tools/cad-viewer-service/bin/cad-viewer status --json
```

returned `state:"running"` with job PID `91660` and backend PID `91723`.

This is the release-blocking failure.

## Logs, URL, source independence, and Tailscale

Logs command through checked-in source:

```sh
tools/cad-viewer-service/bin/cad-viewer logs --lines 6 --json
```

Result: exit 0, stdout log tail included the npm start command and CAD Viewer URL; stderr log tail was empty.

URL command through checked-in source:

```sh
tools/cad-viewer-service/bin/cad-viewer url --workspace /Users/scottchu/.codex/worktrees/a373f6e6-90f4-4c0e-857b-643add242937/design-projects --file tools/cad-viewer-service/README.md --local --json
tools/cad-viewer-service/bin/cad-viewer url --workspace /Users/scottchu/.codex/worktrees/a373f6e6-90f4-4c0e-857b-643add242937/design-projects --file tools/cad-viewer-service/README.md --tailscale --json
```

Results:

- local: `http://127.0.0.1:3245/Users/scottchu/.codex/worktrees/a373f6e6-90f4-4c0e-857b-643add242937/design-projects?file=tools%2Fcad-viewer-service%2FREADME.md`
- tailscale: `https://mac-mini.duckbill-ionian.ts.net/Users/scottchu/.codex/worktrees/a373f6e6-90f4-4c0e-857b-643add242937/design-projects?file=tools%2Fcad-viewer-service%2FREADME.md`

Temp exact source copy check:

- Temp copy root: `/var/folders/p1/g0fbbwtx3jqcj7vdr2198_dc0000gn/T/tmp.kmRUs3KmDN`
- Copied manifest hash: `83e77c8735e32c49ea494ef90d76cc5d435614b2a9474efe4f64688ac4f634c0`
- Copied DESIGN hash: `9955f7078747aa280407f86febe7ed478bf63252bf660ba8f3fc183b253179a5`
- Command: `<temp>/tools/cad-viewer-service/bin/cad-viewer status --json`
- Result: exit 0, reported the live service running with job PID `91660`, backend PID `91723`.

Tailscale Serve after-state:

- command: `tailscale serve status --json`
- exit: 0
- bytes: 221
- hash: `5037675750347d2e9d6e4fafe5dbf66912c59404bc28cb320cb3f3fc19069cef`
- byte comparison with pre-state: equal (`cmp` exit 0)

No Tailscale route mutation was performed.

## Final live state

Final managed status through checked-in source:

```json
{"ok":true,"command":"status","state":"running","enabled":true,"loaded":true,"jobPid":91660,"ready":true,"runtime":{"path":"/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.25/skills/cad-viewer/scripts/viewer","version":"0.4.25","launchedAt":"2026-08-24T20:22:17.231Z","launcherPid":91660},"portOwners":[{"pid":91723,"command":"python3.12"}],"server":{"app":"cad-viewer","viewerVersion":"","serverMode":"serve","serverFeatures":["path-directory"],"backend":"local-fs","rootDir":"/Users/scottchu","rootPath":"/Users/scottchu","rootName":"scottchu","port":3245,"pid":91723,"stepArtifactGenerationAvailable":true,"url":"http://127.0.0.1:3245"},"errors":[]}
```

Final HTTP checks:

- `http://127.0.0.1:3245/`: HTTP 200, 1750 bytes.
- `http://127.0.0.1:3245/__cad/server`: HTTP 200, 289 bytes, app `cad-viewer`, port `3245`, backend PID `91723`.

Installed payload revalidated with `validatePayload(...)`:

```json
{"payloadHash":"83e77c8735e32c49ea494ef90d76cc5d435614b2a9474efe4f64688ac4f634c0","files":["bin/cad-viewer","cli.mjs","config.mjs","core.mjs","install.mjs","launch-viewer.mjs","launchd/com.scottchu.cad-viewer.plist.template"]}
```

Final service state requirement is satisfied only at the managed service level: the singleton is running on `127.0.0.1:3245`. The stable installed CLI requirement is not satisfied.

## Boundaries and limitations

- No source repair was attempted.
- No git/PR operation was performed.
- No plugin cache, CAD/project file, DESIGN, README, source, tests, or generated artifacts were edited.
- Live rollback was not forced because I found no explicit safe controlled failure hook in the implementation. Rollback behavior was validated only by the checked-in unit/static tests.
- Physical/CAD acceptance is out of scope; this receipt validates only the CAD Viewer singleton service behavior.

## Requirement coverage

- Read AGENTS/CAD workflow/CAD Viewer skill/design/source/tests: done.
- Verify DESIGN and candidate payload hashes before live work: pass.
- Run unit/static/manifest/plutil/code checks: pass.
- Capture pre-state labels/port/process/Tailscale/repo hashes: pass.
- Migrate only narrow legacy `com.codex.cad-viewer`: pass; migration done by implementation, no arbitrary PID kill.
- Verify content-addressed release/current/stable shim/plist: partial pass; paths and hashes pass, stable shim execution fails.
- Verify no worktree path in installed release/shim/plist: pass.
- Verify exact canonical Python and dynamic runtime: pass.
- Verify page and `/__cad/server` HTTP 200 and ancestry: pass.
- Idempotent start twice preserves one label/listener/PID: pass through checked-in source.
- Restart changes managed PID and returns ready: pass through checked-in source.
- Crash recovery through `launchctl kill` on managed label: pass.
- Durable stop/disabled then explicit start: pass through checked-in source.
- Foreign-port safety: pass.
- Source independence: pass via temp exact source copy; installed stable path fails execution.
- Exercise logs/url: pass through checked-in source.
- Atomic rollback: static/unit coverage only; no live hook found.
- Tailscale Serve byte-for-byte/hash unchanged: pass.
- Final state new singleton running: pass for launchd/runtime; fail for stable CLI operability.

## Required repair before acceptance

Fix the installed stable CLI entrypoint so `/Users/scottchu/.local/bin/cad-viewer <command> --json` actually runs `main()` when invoked through `/Users/scottchu/Library/Application Support/CADViewer/service/current/cli.mjs`. A focused regression should assert non-empty JSON output from the stable shim path, not only from the checked-in `--source-root` shim.

---

# CVS-V03 focused live revalidation

Validator: P17-V04/CVS-V03 independent focused live validator
Date: 2026-08-24
Worktree: `/Users/scottchu/.codex/worktrees/a373f6e6-90f4-4c0e-857b-643add242937/design-projects`
Branch: `codex/xt60-p17-r2-direct-cad`
HEAD: `cb020f6cf01876e01d1e6501fec8861a527aa248`

## CVS-V03 top status

PASS for the repaired live singleton service gate.

The V02 stable-shim blocker is repaired: `/Users/scottchu/.local/bin/cad-viewer` now executes from a fresh `/bin/zsh -f` and emits non-empty valid JSON for `status`, `start`, `restart`, `logs`, and `url`. The final service was left running on `127.0.0.1:3245`.

Observation: `status --json` emits valid JSON but does not include a payload/current digest field. The current repaired digest was proven by the checked-in install command, stable `start --json`, stable `restart --json`, `current` symlink target, and installed payload validation. If the contract requires the `status` JSON object itself to include the digest, that is a residual API/documentation gap; it did not block this focused repair gate because the stable CLI operability failure was fixed and the installed current digest is independently proven.

## Frozen inputs

- Repaired payload/install-manifest digest expected and observed:
  - `9ae1b0eb9651d7fbd589c50108cb8be08efbed31ed3d0ac55af25c9dcc61ab0e  tools/cad-viewer-service/payload/install-manifest.json`
- Prior CVS-V02 validation receipt hash expected and observed before appending this section:
  - `4f4a0f209770a6255ab5a5a67c8f43577a1e97b38a0039624220beda7e4d9282  tools/cad-viewer-service/VALIDATION.md`

## Static checks

Commands:

```sh
/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node --test tools/cad-viewer-service/tests/*.test.mjs
/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node tools/cad-viewer-service/scripts/generate-install-manifest.mjs --check
/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node --check tools/cad-viewer-service/payload/cli.mjs
/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node --check tools/cad-viewer-service/payload/install.mjs
/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node --check tools/cad-viewer-service/payload/launch-viewer.mjs
plutil -lint <rendered plist fixture>
```

Results:

- Node tests: 17 passed, 0 failed.
- New relevant regression present and passing: `copied stable shim invokes CLI through symlinked current release path`.
- Manifest check: `install-manifest.json is current`.
- JS syntax checks: pass.
- Rendered plist lint: pass.

## Pre-install live state

Before installing the repaired payload, the V02 managed service was running:

- source status exit: 0
- job PID: `91660`
- backend PID: `91723`
- listener: `127.0.0.1:3245`
- Tailscale Serve pre-state:
  - exit: 0
  - bytes: 221
  - hash: `5037675750347d2e9d6e4fafe5dbf66912c59404bc28cb320cb3f3fc19069cef`

## Repaired payload install

Command:

```sh
tools/cad-viewer-service/bin/cad-viewer start --json
```

Result: exit 0.

Key JSON:

- `state:"running"`
- `enabled:true`
- `loaded:true`
- `jobPid:92535`
- backend PID: `92608`
- `payloadHash:"9ae1b0eb9651d7fbd589c50108cb8be08efbed31ed3d0ac55af25c9dcc61ab0e"`
- `payloadChanged:true`
- `migratedLegacy:false`

## Stable command checks from fresh shell

All stable command checks used `/bin/zsh -f -c '/Users/scottchu/.local/bin/cad-viewer ... --json'`.

### Stable status

Command:

```sh
/Users/scottchu/.local/bin/cad-viewer status --json
```

Result:

- exit: 0
- stdout bytes: 662
- stderr bytes: 0
- JSON parsed successfully
- `state:"running"`
- job PID: `92535`
- backend PID: `92608`

As noted above, this status JSON did not include a payload/current digest field.

### Stable idempotent start

Command:

```sh
/Users/scottchu/.local/bin/cad-viewer start --json
```

Result:

- exit: 0
- stdout bytes: 817
- stderr bytes: 0
- JSON parsed successfully
- `state:"running"`
- job PID remained `92535`
- backend PID remained `92608`
- `payloadHash:"9ae1b0eb9651d7fbd589c50108cb8be08efbed31ed3d0ac55af25c9dcc61ab0e"`
- message: `CAD Viewer is already running with this payload; PID unchanged`
- `lsof` showed one listener on `127.0.0.1:3245`

### Stable restart

Command:

```sh
/Users/scottchu/.local/bin/cad-viewer restart --json
```

Result:

- exit: 0
- stdout bytes: 823
- stderr bytes: 0
- JSON parsed successfully
- before restart: job/backend `92535/92608`
- after restart: job/backend `92716/92779`
- `payloadHash:"9ae1b0eb9651d7fbd589c50108cb8be08efbed31ed3d0ac55af25c9dcc61ab0e"`
- `payloadChanged:false`
- `migratedLegacy:false`
- `lsof` showed one listener on `127.0.0.1:3245`

### Stable logs

Command:

```sh
/Users/scottchu/.local/bin/cad-viewer logs --lines 6 --json
```

Result:

- exit: 0
- stdout bytes: 449
- stderr bytes: 0
- JSON parsed successfully
- `state:"snapshot"`
- stdout log tail present, including npm start command and CAD Viewer URL
- stderr log tail empty

### Stable url

Command:

```sh
/Users/scottchu/.local/bin/cad-viewer url --workspace /Users/scottchu/.codex/worktrees/a373f6e6-90f4-4c0e-857b-643add242937/design-projects --file tools/cad-viewer-service/README.md --local --json
```

Result:

- exit: 0
- stdout bytes: 222
- stderr bytes: 0
- JSON parsed successfully
- `state:"running"`
- local URL:
  - `http://127.0.0.1:3245/Users/scottchu/.codex/worktrees/a373f6e6-90f4-4c0e-857b-643add242937/design-projects?file=tools%2Fcad-viewer-service%2FREADME.md`

## Final runtime integrity

HTTP checks:

- `http://127.0.0.1:3245/`: HTTP 200, 1750 bytes.
- `http://127.0.0.1:3245/__cad/server`: HTTP 200, 289 bytes.
- server JSON included:
  - `app:"cad-viewer"`
  - `port:3245`
  - backend PID `92779`
  - `url:"http://127.0.0.1:3245"`

Launchd/process checks:

- `launchctl print gui/501/com.scottchu.cad-viewer`: running LaunchAgent.
- `launchctl print gui/501/com.codex.cad-viewer`: not found.
- one listener on `127.0.0.1:3245`: PID `92779`, command `python3.12`.
- process ancestry:

```text
92779 92745 /Users/scottchu/Projects/personal/design-projects/.venv/bin/python3
92745 92744 /Users/scottchu/Projects/personal/design-projects/.venv/bin/python3
92744 92724 node
92724 92716 npm run start --host 127.0.0.1 --port 3245 --json
92716     1 /Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node
    1     0 /sbin/launchd
```

Backend environment check:

- `VIEWER_CAD_PYTHON=/Users/scottchu/Projects/personal/design-projects/.venv/bin/python3`

Installed digest/path checks:

- `current -> releases/9ae1b0eb9651d7fbd589c50108cb8be08efbed31ed3d0ac55af25c9dcc61ab0e`
- installed manifest hash:
  - `9ae1b0eb9651d7fbd589c50108cb8be08efbed31ed3d0ac55af25c9dcc61ab0e  /Users/scottchu/Library/Application Support/CADViewer/service/releases/9ae1b0eb9651d7fbd589c50108cb8be08efbed31ed3d0ac55af25c9dcc61ab0e/install-manifest.json`
- stable shim hash:
  - `998bb2b6d0cce1354ceb245e721c53fdfd8054703b8b976cb67e39be28563484  /Users/scottchu/.local/bin/cad-viewer`
- LaunchAgent plist hash:
  - `5242e7dbab90c2e53e636ab660bd5df254bf36e2ca0d835365e4fb2e8577075d  /Users/scottchu/Library/LaunchAgents/com.scottchu.cad-viewer.plist`
- installed payload revalidated:

```json
{"payloadHash":"9ae1b0eb9651d7fbd589c50108cb8be08efbed31ed3d0ac55af25c9dcc61ab0e","files":["bin/cad-viewer","cli.mjs","config.mjs","core.mjs","install.mjs","launch-viewer.mjs","launchd/com.scottchu.cad-viewer.plist.template"]}
```

No worktree reference was found in the installed repaired release, stable shim, or LaunchAgent plist.

Tailscale Serve after-state:

- exit: 0
- bytes: 221
- hash: `5037675750347d2e9d6e4fafe5dbf66912c59404bc28cb320cb3f3fc19069cef`
- byte comparison with pre-state: equal (`cmp` exit 0)

No Tailscale Serve route was mutated.

## Source independence

Temp exact source copy:

- path: `/var/folders/p1/g0fbbwtx3jqcj7vdr2198_dc0000gn/T/tmp.DQyMqWNYV5`
- copied install manifest hash:
  - `9ae1b0eb9651d7fbd589c50108cb8be08efbed31ed3d0ac55af25c9dcc61ab0e`
- copied pre-append validation hash:
  - `4f4a0f209770a6255ab5a5a67c8f43577a1e97b38a0039624220beda7e4d9282`
- command:
  - `<temp>/tools/cad-viewer-service/bin/cad-viewer status --json`
- result:
  - exit 0
  - valid JSON
  - `state:"running"`
  - job PID `92716`
  - backend PID `92779`

## Final state

The final service is running:

- label: `com.scottchu.cad-viewer`
- job PID: `92716`
- backend PID: `92779`
- URL: `http://127.0.0.1:3245`
- repaired payload digest: `9ae1b0eb9651d7fbd589c50108cb8be08efbed31ed3d0ac55af25c9dcc61ab0e`

No implementation/source repair was performed during CVS-V03. The only repository write was appending this CVS-V03 section to `tools/cad-viewer-service/VALIDATION.md`.

---

# CVS-V04 runtime-refresh live validation

Validator: `viewer_refresh_validator` independent live validator
Date: 2026-08-24
Worktree: `/Users/scottchu/.codex/worktrees/a373f6e6-90f4-4c0e-857b-643add242937/design-projects`
Branch: `codex/xt60-p17-r2-direct-cad`
HEAD: `df9af826385db3f625917eca15a6d64273d8fd5f`

## Top status

PASS for CVS-D03/CVS-I04.

The singleton installed payload digest
`2ddeecf807fc53904db4f9b9eefbf69e12134e21c785a51a481c0da2dca73b4b`,
the stable installed command recovered stale, missing, and malformed
`runtime.json` through both `start` and `restart` without manual relocation,
and all deterministic turnover/SPA/no-duplicate fixtures passed. The final
service is running on the preferred Viewer `0.4.26`, the exact XT60 page and
artifact assets are ready through localhost and Tailscale, and Tailscale Serve
plus the plugin cache remained unchanged.

No implementation, tests, plugin-cache files, Tailscale configuration, or XT60
project files were edited. The only repository write by this validator is this
appended CVS-V04 receipt.

## Frozen input and candidate fingerprint

The required validation manifest was verified before work:

```sh
shasum -a 256 /tmp/cvs-i04-validation-input-manifest.txt
while read -r expected file_path; do
  actual=$(shasum -a 256 "$file_path" | awk '{print $1}')
  test "$actual" = "$expected"
done < /tmp/cvs-i04-validation-input-manifest.txt
```

Result:

- manifest SHA-256 matched
  `5e711a7d77b14adcb58b7b6b18e6298625778d4fd611946bf368cdde4929e82b`;
- every declared path-and-content entry matched;
- candidate install manifest/digest matched
  `2ddeecf807fc53904db4f9b9eefbf69e12134e21c785a51a481c0da2dca73b4b`;
- design hash matched
  `c85df5480e90493294be5413d61315225f9e06f7861c62fa6ba005314b5d3a51`;
- launcher hash matched
  `eadccd3899b6940e142acd3f3fe7c9b9797c575fb0f3c54995ac6f3e00917140`;
- focused runtime-refresh test hash matched
  `aea656530898fb11ff06f211da509dae28cdb5a25391211e8ba34a2971aa0f2b`.

## Deterministic checks

Commands:

```sh
/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node --test tools/cad-viewer-service/tests/*.test.mjs
/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node tools/cad-viewer-service/scripts/generate-install-manifest.mjs --check
/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node --check tools/cad-viewer-service/payload/cli.mjs
/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node --check tools/cad-viewer-service/payload/install.mjs
/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node --check tools/cad-viewer-service/payload/launch-viewer.mjs
```

Results:

- Node tests: 23 passed, 0 failed;
- resolver-turnover fixture: pass, selecting newly available higher stable
  runtime after retiring the older fixture runtime;
- owned-child turnover/no-duplicate fixture: pass, listener sample count never
  exceeded one and the unrelated fixture process remained alive;
- SPA-disappearance fixture: pass, two page failures recycled the owned child
  while the API remained healthy;
- install manifest: current;
- all syntax checks: pass.

The runtime-turnover tests used isolated temporary caches and fixture ports.
The installed plugin cache was never modified.

## Pre-state and installation

Before installation, the prior digest `9ae1b0eb...` service was running on
Viewer `0.4.26` with job/backend PIDs `13895/14002`, one listener on
`127.0.0.1:3245`, base page HTTP `200`, and `/__cad/server` HTTP `200`.

Pre-state boundaries:

- plugin-cache file-content inventory digest:
  `736d6b4796367849185c0dd990d60d22c7bc578bfe2fea97704134e4f0aeca46`;
- Tailscale Serve JSON: 221 bytes, SHA-256
  `5037675750347d2e9d6e4fafe5dbf66912c59404bc28cb320cb3f3fc19069cef`;
- repository status contained only the frozen CVS-I04 candidate changes; no
  XT60 project diff existed.

Install command:

```sh
tools/cad-viewer-service/bin/cad-viewer start --json
```

Result: exit `0`, `state:"running"`, `payloadChanged:true`, installed/current
digest `2ddeecf807fc53904db4f9b9eefbf69e12134e21c785a51a481c0da2dca73b4b`,
job/backend PIDs `24938/25050`, preferred/runtime-record version `0.4.26`,
base page HTTP `200`, server API HTTP `200`, and one listener.

Installed integrity:

- `current -> releases/2ddeecf807fc53904db4f9b9eefbf69e12134e21c785a51a481c0da2dca73b4b`;
- installed manifest SHA-256:
  `2ddeecf807fc53904db4f9b9eefbf69e12134e21c785a51a481c0da2dca73b4b`;
- stable shim SHA-256:
  `998bb2b6d0cce1354ceb245e721c53fdfd8054703b8b976cb67e39be28563484`;
- LaunchAgent plist SHA-256:
  `5242e7dbab90c2e53e636ab660bd5df254bf36e2ca0d835365e4fb2e8577075d`;
- installed `validatePayload(...)` returned the same payload hash and the exact
  seven manifest-listed payload files;
- no disposable worktree path or pinned `cad/0.4.25`/`cad/0.4.26` runtime path
  was found in the installed release, stable shim, or plist.

## Stable CLI, canonical Python, and ancestry

Fresh-shell stable command:

```sh
/bin/zsh -f -c 'cd /tmp && /Users/scottchu/.local/bin/cad-viewer status --json'
/Users/scottchu/.local/bin/cad-viewer start --json
```

Both exited `0` with valid JSON. The idempotent `start` preserved job/backend
PIDs `24938/25050` and reported one listener.

The canonical interpreter reported Python `3.12.13` at:

`/Users/scottchu/Projects/personal/design-projects/.venv/bin/python3`

The backend environment contained the exact same `VIEWER_CAD_PYTHON`. Observed
ancestry was:

```text
backend python -> start_viewer python -> node start-viewer.mjs -> owned npm ->
installed launch-viewer.mjs -> launchd
```

No Homebrew, system, pyenv, worktree-local, or project-local Python was used.

## Runtime-record recovery matrix

For each case, the current `runtime.json` was first copied to an isolated
temporary backup. A failing recovery path would have restored that backup and
run the managed stable `restart`; no emergency restoration was needed.

The stale record used a syntactically valid absent Viewer `0.4.25` path while
the real preferred `0.4.26` runtime remained untouched.

Commands under test:

```sh
/Users/scottchu/.local/bin/cad-viewer status --json
/Users/scottchu/.local/bin/cad-viewer start --json
/Users/scottchu/.local/bin/cad-viewer restart --json
```

Results:

| Record state | `status` diagnostic | `start` | `restart` |
|---|---|---|---|
| stale valid `0.4.25` | exit `2`, `misconfigured`, explicit preferred-runtime mismatch | exit `0`, recovered to `0.4.26` | exit `0`, recovered to `0.4.26` |
| missing | exit `2`, `misconfigured`, `runtime.json is missing` | exit `0`, recovered to `0.4.26` | exit `0`, recovered to `0.4.26` |
| malformed | exit `2`, `misconfigured`, JSON parse issue | exit `0`, recovered to `0.4.26` | exit `0`, recovered to `0.4.26` |

Every recovery replaced the managed job PID, atomically rewrote a valid
preferred `runtime.json`, returned page/API readiness, and left exactly one
listener. No test required the user to rename or delete the record manually.

## Managed crash, durable stop, and foreign-port safety

Crash command:

```sh
launchctl kill SIGKILL gui/501/com.scottchu.cad-viewer
```

Result: launchd replaced job PID `26752` with `26943`; within two 2-second
polls the stable status returned `running`, backend PID `26980`, and one
listener.

Durable stop command:

```sh
/Users/scottchu/.local/bin/cad-viewer stop --json
```

Result: exit `0`, `state:"disabled"`, label unloaded, disabled override
present, no listener after three seconds, and follow-up status remained
disabled.

A validator-owned Node fixture then listened on `127.0.0.1:3245`. Stable
`start --json` exited `2` with `state:"blocked"`; the fixture PID remained
alive and retained the port, while the managed label remained disabled. Only
the validator-owned fixture was then sent `SIGTERM`. Stable `start --json`
restored the singleton to running state.

No discovered port PID or unrelated process was signaled by the service.

## Exact XT60 preview and assets

Exact source:

`projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist/p17_r2_fixed_axle_motion.step.py`

Exact Tailscale review URL:

`https://mac-mini.duckbill-ionian.ts.net/Users/scottchu/.codex/worktrees/a373f6e6-90f4-4c0e-857b-643add242937/design-projects?file=projects%2Fxt60-bend-jig%2Fcad%2Fp17_r2_direct_counter_twist%2Fp17_r2_fixed_axle_motion.step.py`

Results on both localhost and Tailscale:

- exact page: HTTP `200`, 1750 bytes;
- exact `/__cad/artifact?dir=<worktree>&file=<source>`: HTTP `200`,
  `state:"ready"`;
- `assembly.json`: HTTP `200`, 6268 bytes, schema `2`, package schema `3`,
  `assembly-package`, 6 components, 8 occurrences;
- params module: HTTP `200`, 2201 bytes, SHA-256
  `7f5e6906bf73a019b2908430d0d58d348aeac0528a087d57ffede7fb62c346e7`;
- component `3bb3ae3413a94ba0.glb`: HTTP `200`,
  `model/gltf-binary`, 137340 bytes, `glTF` magic.

Local and Tailscale response hashes matched for every checked asset. The
artifact's directory package ref itself returned `404`, as expected for a
directory rather than an asset; readiness is proven by the actual descriptor,
module, and component paths.

## Final boundaries and state

Final process inventory contains exactly one managed chain and listener:

```text
27430 launch-viewer.mjs
27439 npm run start --host 127.0.0.1 --port 3245
27459 node scripts/start-viewer.mjs --host 127.0.0.1 --port 3245
27460 canonical uv python -m server_py.start_viewer ...
27521 canonical uv python -m server_py.server ...
```

The legacy `com.codex.cad-viewer` label is absent. No orphan npm, launcher,
Python backend, or second `3245` listener was found.

Final immutable boundary checks:

- plugin-cache file-content inventory digest remained exactly
  `736d6b4796367849185c0dd990d60d22c7bc578bfe2fea97704134e4f0aeca46`;
- Tailscale Serve JSON remained byte-identical, 221 bytes, SHA-256
  `5037675750347d2e9d6e4fafe5dbf66912c59404bc28cb320cb3f3fc19069cef`;
- `git diff --name-only -- projects/xt60-bend-jig` was empty;
- repository changes before this receipt were exactly the frozen CVS-I04
  service candidate;
- final runtime record selects Viewer `0.4.26` and launcher PID `27430`;
- final service state is `running`, job/backend PIDs `27430/27521`, base page
  and server API HTTP `200`, with one listener on `127.0.0.1:3245`.

## Findings, coverage, and next action

- Release blockers: none.
- High/medium/low defects: none found in the scoped CVS-D03 repair.
- Accepted residuals: a real plugin-cache turnover can still create the bounded
  short outage defined by CVS-D03; no valid installed runtime remains an
  external prerequisite; the package-directory ref is not itself an asset.
- Requirement coverage: all requested deterministic, installed-payload,
  stable-CLI, record-recovery, page/API, ancestry, idempotence, restart, crash,
  durable-stop, foreign-port, source-independence, exact-preview, Tailscale,
  plugin-cache, project-boundary, and final-running-state gates passed.
- Next action: independent formal review of candidate digest
  `2ddeecf807fc53904db4f9b9eefbf69e12134e21c785a51a481c0da2dca73b4b`
  and this CVS-V04 receipt.

---

# CVS-R04 runtime-refresh formal review

Reviewer: `viewer_refresh_reviewer` independent formal reviewer
Date: 2026-08-24
Worktree: `/Users/scottchu/.codex/worktrees/a373f6e6-90f4-4c0e-857b-643add242937/design-projects`
Branch: `codex/xt60-p17-r2-direct-cad`
Baseline HEAD: `df9af826385db3f625917eca15a6d64273d8fd5f`

## Formal decision

**REJECT. Do not release or merge CVS-I04.**

The candidate passes its checked-in deterministic suite and the installed
singleton is currently healthy, but the central automatic-turnover safety gate
is false for the real Viewer process topology. Sending `SIGTERM` only to the
owned npm `ChildProcess` exits npm while leaving its Python backend listening.
This is the exact stop condition identified by CVS-D03: if npm termination can
orphan the backend, the design must reopen rather than ship or add port-PID
killing.

## Frozen fingerprint verification

The required review manifest was verified before review:

```text
ca45e2c461bc414485dbfbcb94f53f9a845abe300c090c151cbe0d3d1b112eee  /tmp/cvs-v04-review-input-manifest.txt
```

Every path-and-content entry matched. The reviewed candidate payload digest is:

```text
2ddeecf807fc53904db4f9b9eefbf69e12134e21c785a51a481c0da2dca73b4b  tools/cad-viewer-service/payload/install-manifest.json
```

The design, launcher, focused-test, and validator-receipt hashes also matched
the manifest (`c85df548...`, `eadccd389...`, `aea656530...`, and
`b235de3e...`, respectively).

## Release-blocking finding

**CVS-R04-F01 — Critical / release blocker: automatic refresh orphans the real
Viewer backend.**

Implementation evidence:

- `payload/launch-viewer.mjs:100-105` signals only the direct npm child and
  considers termination complete as soon as that child exits.
- `payload/launch-viewer.mjs:126-129` then returns refresh exit code `75`, so
  launchd can start a replacement while descendants from the prior npm command
  still own the port.
- `tests/runtime-refresh.test.mjs:87-140` substitutes a direct Node HTTP server
  for the owned child. That fixture has no npm -> Node -> Python descendant
  chain and therefore cannot prove the D03 no-orphan gate for the production
  topology.

Independent read-only fixture command: start the actual Viewer `0.4.26` using
the same bundled npm, canonical root-uv Python, arguments, and environment as
production, but on reviewer-owned temporary port `33425`; wait for page HTTP
200; send `SIGTERM` directly to the returned npm `ChildProcess`; sample the
listener for six seconds; finally clean up only the reviewer-owned detached
process group.

Observed result:

```json
{"phase":"ready","isReady":true,"npmPid":30116,"owners":["p30142"]}
{"phase":"after-direct-npm-sigterm","childExit":null,"childSignal":"SIGTERM","owners":["p30142"]}
{"phase":"cleanup","owners":[]}
```

The npm child had terminated (`signalCode:"SIGTERM"`), but backend PID `30142`
still listened after the six-second observation window. Cleanup removed that
reviewer-owned fixture, and the production singleton on port `3245` was not
mutated.

Impact: on real cache turnover or the two-failure SPA path, the launcher can
exit while its backend remains alive. A launchd retry then encounters the old
listener, so the service can fail to adopt the new runtime and can enter a
blocked/retry condition. It also violates the one-listener/no-orphan and
"launcher must not exit while an owned backend is live" requirements.

## Other reviewed evidence

The following scoped checks passed and are not the reason for rejection:

- review manifest and all entries: exact match;
- Node suite: 23 passed, 0 failed;
- install manifest: current;
- CLI and launcher syntax: pass;
- installed stable `status --json`: running, preferred/record runtime `0.4.26`;
- one production listener on `127.0.0.1:3245`, with ancestry through the
  canonical `/Users/scottchu/Projects/personal/design-projects/.venv/bin/python3`;
- installed digest: exact `2ddeecf8...` candidate;
- local and Tailscale exact XT60 page: HTTP 200 with byte-identical responses;
- local and Tailscale exact artifact query: HTTP 200, `state:"ready"`, with
  byte-identical responses;
- Tailscale Serve JSON SHA-256 remained
  `5037675750347d2e9d6e4fafe5dbf66912c59404bc28cb320cb3f3fc19069cef`;
- no worktree path or runtime-version pin was found in the installed payload,
  stable shim, or plist.

The CVS-V04 stale/missing/malformed record matrix, stable lifecycle behavior,
foreign-port protection, page-plus-API readiness, plugin-cache boundary, and
exact-preview evidence are credible for those individual gates. They do not
exercise the internal supervisor's real npm descendant shutdown and therefore
cannot override CVS-R04-F01.

## Acceptance gaps and next action

Reopen the runtime-refresh design before implementation. The revised design
must define an ownership-safe way to retire the complete spawned Viewer process
tree without signaling any discovered or foreign PID, and it must add a
regression that uses the real npm -> Node -> canonical Python launcher/backend
topology. That regression must prove the old listener is gone before the
launcher exits or any replacement starts, with listener count never above one.
Do not solve this by killing a PID obtained from the port, HTTP API,
`runtime.json`, or process table.

No implementation, lifecycle state, Tailscale configuration, plugin-cache
content, or XT60 project file was changed by this review. The only repository
write is this appended CVS-R04 receipt.

---

# CVS-V04-R1 anchored-group repair validation

Validator: `viewer_refresh_validator` independent repair validator
Date: 2026-08-24
Worktree: `/Users/scottchu/.codex/worktrees/a373f6e6-90f4-4c0e-857b-643add242937/design-projects`
Branch: `codex/xt60-p17-r2-direct-cad`
HEAD: `df9af826385db3f625917eca15a6d64273d8fd5f`

## Top status

**REJECT for release because the frozen plugin-cache byte-identity boundary
failed.**

The R1 repair does fix the critical CVS-R04-F01 process-ownership defect. The
installed launchd parent remained outside a dedicated anchor PGID; the anchor,
npm, Node shim, canonical uv-Python launcher/backend, and deeper artifact
workers inherited that PGID. Restart, runtime-record recovery, external TERM,
and direct managed-label SIGKILL all removed the old listener and ultimately
drained the complete old PGID with no escaped descendant. Listener count never
exceeded one.

However, the plugin-cache file-content inventory changed from
`736d6b4796367849185c0dd990d60d22c7bc578bfe2fea97704134e4f0aeca46`
before validation to
`d94b69d9df99ff1923de32864fc261f01f94bd45c48907a7f01fc07480c457e3`
after validation. The files written during the validation window are eleven
auto-generated `__pycache__/*.pyc` files under the Viewer `0.4.26` runtime.
No authored plugin source or package file was observed with a validation-window
mtime, but CVS-D03-R1 requires the complete plugin-cache inventory to remain
byte-identical and does not exempt bytecode caches. The gate therefore fails.

The cache was not deleted, restored, or otherwise modified by the validator
after detecting the mismatch. The final singleton and exact XT60 preview were
left running and ready.

## Frozen input and candidate fingerprint

Commands:

```sh
shasum -a 256 /tmp/cvs-r1-independent-validation-input-manifest.txt
while read -r expected file_path; do
  actual=$(shasum -a 256 "$file_path" | awk '{print $1}')
  test "$actual" = "$expected"
done < /tmp/cvs-r1-independent-validation-input-manifest.txt
```

Results:

- manifest SHA-256 matched
  `0c010985f9958fc81334af5d8007efcff2f01b4491fce483cc88f6bd0206736d`;
- every manifest entry matched before validation;
- candidate payload/install-manifest digest matched
  `4e89ad3d2efce80b2381e439c43af0623245d1c2443fca5ea0fb24b10bb72988`;
- D03-R1 design hash matched
  `10869a27bc4d938f330647dfbf8477727a6e1a943af2c3c3c1dd1034ed730d02`;
- launcher hash matched
  `ab17131a164890d062f5538b80f511074d9e6522adfcc95e72408a7bb8a1f596`;
- runtime-refresh regression hash matched
  `3e9f55be9bad49e1b5c360767a9574105a80a0e5aece8d094f9919b77b7f2d9d`;
- anchor fixture hash matched
  `04d648681ffb1e45112885576b4a7c76e2c794f23d412ba379daaed43cc0d80b`;
- pre-append validation receipt hash matched
  `0b92684913119ba7079c78b996ebf1acf5f2ca117b206d011900cd79c6c30480`.

## Deterministic and real-topology tests

Commands:

```sh
/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node --test tools/cad-viewer-service/tests/*.test.mjs
/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node tools/cad-viewer-service/scripts/generate-install-manifest.mjs --check
/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node --check tools/cad-viewer-service/payload/cli.mjs
/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node --check tools/cad-viewer-service/payload/install.mjs
/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node --check tools/cad-viewer-service/payload/launch-viewer.mjs
plutil -lint <rendered checked-in plist fixture>
```

Results:

- 28 tests passed, 0 failed;
- install manifest current; syntax checks and rendered plist passed;
- anchored runtime turnover drained the complete fixture group before
  replacement;
- two SPA failures used anchored drain while the API remained healthy;
- stubborn descendants received exactly one TERM and one KILL; failed anchor
  provenance sent no group signal and an unrelated process stayed alive;
- foreign post-drain listener was observed but never signaled or adopted;
- external lifecycle signal used the same group drain;
- abrupt fixture-parent death disconnected IPC and emergency-drained the group;
- actual bundled npm plus canonical uv-Python topology on reviewer port
  `56096` stayed inside one anchor PGID, fully drained, released the backend,
  and allowed a later replacement without listener overlap.

The resolver, SPA, stubborn-group, foreign-port, and actual-production-topology
tests used isolated caches/ports or the read-only installed Viewer runtime. No
test intentionally edited the real plugin cache.

## Install, stable command, and production topology

Install command:

```sh
tools/cad-viewer-service/bin/cad-viewer start --json
```

Result: exit `0`, `state:"running"`, `payloadChanged:true`, payload digest
`4e89ad3d2efce80b2381e439c43af0623245d1c2443fca5ea0fb24b10bb72988`,
job/backend PIDs `45808/45887`, Viewer `0.4.26`, and one listener.

Installed integrity:

- `current -> releases/4e89ad3d2efce80b2381e439c43af0623245d1c2443fca5ea0fb24b10bb72988`;
- installed manifest hash matched the candidate digest;
- stable shim SHA-256 remained
  `998bb2b6d0cce1354ceb245e721c53fdfd8054703b8b976cb67e39be28563484`;
- installed plist SHA-256 was
  `b9dd71abe9d1fadc00389fd61bac1d07c3fa3d77a9223484092f5276af52c9f3`
  and contained fixed `ExitTimeOut=15`;
- installed `validatePayload(...)` returned the exact seven listed files and
  the candidate digest;
- fresh `/bin/zsh -f` stable status from `/tmp` returned valid running JSON;
- no disposable worktree path or pinned `0.4.25`/`0.4.26` runtime path was
  found in the installed release, stable shim, or plist.

Initial R1 production topology:

```text
PID    PGID   PPID  role
45808  45808     1  launchd-owned parent launcher
45816  45816 45808  persistent owned group anchor
45819  45816 45816  bundled npm
45840  45816 45819  Node start-viewer shim
45841  45816 45840  canonical uv-Python start_viewer
45887  45816 45841  canonical uv-Python backend/listener
```

The parent PGID was distinct. All worker-chain members shared anchor PGID
`45816`, and the backend environment contained exactly:

`VIEWER_CAD_PYTHON=/Users/scottchu/Projects/personal/design-projects/.venv/bin/python3`

## Idempotence, restart, and runtime-record recovery

Stable idempotent `start --json` preserved job/backend PIDs `45808/45887`.

Stable `restart --json` changed job/anchor/backend from
`45808/45816/45887` to `46103/46111/46193`. After return, the old PGID had no
members, the three old PIDs were absent, and exactly one listener remained.

The stale/missing/malformed recovery matrix was repeated for both stable
`start` and stable `restart`. Each invalid record first produced read-only
`status` exit `2` with the appropriate diagnostic. All six recovery commands
then exited `0`, returned Viewer `0.4.26`, drained the old PGID completely,
left all tracked old PIDs absent, and exposed one listener:

```text
stale start       46103/46111/46193 -> job 46602
stale restart     46602/46610/46701 -> job 46861
missing start     46861/46869/46931 -> job 47089
missing restart   47089/47097/47162 -> job 47301
malformed start   47301/47309/47372 -> job 47585
malformed restart 47585/47593/47707 -> job 47871
```

No emergency runtime-record restoration was required.

## Direct managed-launcher SIGKILL challenge

Command:

```sh
launchctl kill SIGKILL gui/501/com.scottchu.cad-viewer
```

Before SIGKILL, job/anchor/backend were `47871/47879/47941`. The old anchor
PGID contained the anchor, npm, Node shim, two canonical uv-Python server
processes, and eight deeper worker/resource-tracker/spawn descendants. Every
observed descendant had PGID `47879`; none escaped the owned group.

At 100 ms sampling resolution:

- old listener was already absent at the first sample;
- old PGID emergency-drained completely by sample `33` (about 3.3 seconds);
- all tracked old PIDs were absent and no old-PGID member remained;
- launchd created replacement parent `48271` and anchor `48289`;
- replacement backend/listener was `48532`;
- maximum simultaneous listener count was one.

The replacement parent began while the emergency anchor was still draining,
but the old backend/listener was already gone. The anchor reserved the old
PGID until its descendants quiesced; by accepted final recovery the complete
old PGID was absent. No numeric PID discovered from `ps`, `lsof`, the server
API, or the port was used as signal authority.

This directly challenges the former CVS-R04-F01 topology. Unlike the rejected
direct-npm scheme, no Python backend survived the old group.

## External TERM, durable stop, and foreign listener

External managed-label TERM:

```sh
launchctl kill SIGTERM gui/501/com.scottchu.cad-viewer
```

Old job/anchor/backend `49468/49476/49539` drained by sample `2` before new
job `49956` appeared; the replacement listener `50227` appeared at sample
`16`. The old PGID and old PIDs were absent, and listener count never exceeded
one.

Durable stop:

```sh
/Users/scottchu/.local/bin/cad-viewer stop --json
sleep 12
/Users/scottchu/.local/bin/cad-viewer status --json
```

Immediate stop returned exit `0`, disabled state, and no listener, although its
embedded status snapshot still reported the terminating job as loaded/not
ready. After more than one 10-second launchd throttle interval, the label was
unloaded, the disabled override remained, old PGID/PIDs were absent, and the
port was free. This immediate loaded snapshot is informational; durable state
passed.

A validator-owned Node fixture PID `49404` then bound `127.0.0.1:3245`.
Stable `start --json` exited `2` as blocked, left the fixture alive and owning
the port, and left the managed label disabled. Only the validator-owned fixture
was sent TERM. Stable `start --json` then restored one managed group/listener.

## Exact XT60 preview

Exact source:

`projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist/p17_r2_fixed_axle_motion.step.py`

Exact Tailscale URL:

`https://mac-mini.duckbill-ionian.ts.net/Users/scottchu/.codex/worktrees/a373f6e6-90f4-4c0e-857b-643add242937/design-projects?file=projects%2Fxt60-bend-jig%2Fcad%2Fp17_r2_direct_counter_twist%2Fp17_r2_fixed_axle_motion.step.py`

Both localhost and Tailscale returned:

- exact page HTTP `200`, 1750 bytes;
- `/__cad/server` HTTP `200`, valid `cad-viewer`, port `3245`;
- exact artifact HTTP `200`, `state:"ready"`;
- `assembly.json` HTTP `200`, 6268 bytes, schema `2`, package schema `3`, six
  components and eight occurrences;
- params module HTTP `200`, 2201 bytes, SHA-256
  `7f5e6906bf73a019b2908430d0d58d348aeac0528a087d57ffede7fb62c346e7`;
- component `3bb3ae3413a94ba0.glb` HTTP `200`, 137340 bytes,
  `model/gltf-binary`, `glTF` magic.

Local and Tailscale content hashes matched for every checked route/asset.
Final post-lifecycle page and artifact checks again returned HTTP `200` and
`state:"ready"`.

## Release-blocking immutable-boundary finding

**CVS-V04-R1-F01 — High / release blocker: real runtime writes Python bytecode
inside the plugin cache.**

Boundary commands:

```sh
find /Users/scottchu/.codex/plugins/cache/text-to-cad/cad -type f -print0 |
  xargs -0 shasum -a 256 | shasum -a 256
tailscale serve status --json
git diff --name-only -- projects/xt60-bend-jig
```

Results:

- pre plugin-cache digest:
  `736d6b4796367849185c0dd990d60d22c7bc578bfe2fea97704134e4f0aeca46`;
- post plugin-cache digest:
  `d94b69d9df99ff1923de32864fc261f01f94bd45c48907a7f01fc07480c457e3`;
- Tailscale Serve remained byte-identical, 221 bytes, SHA-256
  `5037675750347d2e9d6e4fafe5dbf66912c59404bc28cb320cb3f3fc19069cef`;
- XT60 project diff remained empty;
- repository status before this receipt exactly matched the frozen R1
  candidate paths.

Files with validation-window mtimes are exactly these eleven bytecode caches;
hash, timestamp, size, and path are recorded below:

```text
d19b070eaa6adf8deb128848fe2fd179ca7e78ccc6295cf5d7e581bb33407170  2026-08-24 21:58:48 EDT  3422  .../cadgen/__pycache__/color.cpython-312.pyc
aab25a07072066da0c816db434be6c4d8bcf2f2890c27eda836cb9a95700d8d5  2026-08-24 21:57:29 EDT  9731  .../cadgen/__pycache__/dxf_artifact.cpython-312.pyc
3d434931508aaf602023e7877a965f23b9a5609d185b65bbb5a41a22e56a2807  2026-08-24 21:57:30 EDT  10441 .../cadgen/__pycache__/implicit_artifact.cpython-312.pyc
e58c33ec7125ebb8492680e404cf008ac476a9537b68e80b4f605af3b8df0488  2026-08-24 21:57:30 EDT  12038 .../cadgen/__pycache__/implicit_export.cpython-312.pyc
ac4fb55ee3d2c5396e09eace1405630ed3d8eb73ca267428310041adceea21da  2026-08-24 21:57:30 EDT  18583 .../cadgen/__pycache__/step_export_target.cpython-312.pyc
2fc99cebf204b40b58b5d2afd5fd0e8f8de28aed611c2516e6005dae26780147  2026-08-24 21:57:30 EDT  34174 .../cadgen/_internal/__pycache__/component_package.cpython-312.pyc
79c4985b327ccd01e969332d3e1eac6be3b6bfe8dcb88fabcd39873cbe3133fd  2026-08-24 21:58:49 EDT  9165  .../cadgen/_internal/__pycache__/legacy_artifacts.cpython-312.pyc
404adbcf96003f554c1831e3d2e9fa5591af3b08d10c94c208fa8ea9c9a3ca5f  2026-08-24 21:57:30 EDT  1818  .../cadgen/_internal/__pycache__/stl.cpython-312.pyc
e3b75b7e1239bd432bfbc679dbc4c88ea92b0c1cf475be63d6fbf78c94c45ba6  2026-08-24 21:57:30 EDT  27663 .../cadgen/_internal/__pycache__/threemf.cpython-312.pyc
08b497d98173a2ae199f1de0b809a83adaa60b64e3a43c693d307fd79e342afb  2026-08-24 21:57:29 EDT  8112  .../server_py/__pycache__/worker.cpython-312.pyc
e2a57584ad16a2b0a635052bbffc28a1e0ea81cf0428a82943cf4813f0a1fbef  2026-08-24 21:57:29 EDT  11782 .../server_py/__pycache__/worker_client.cpython-312.pyc
```

Each `...` prefix above expands to:

`/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.26/skills/cad-viewer/scripts/viewer/packages/cadgen/src/`

except the final two, whose prefix is:

`/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.26/skills/cad-viewer/scripts/viewer/`

No authored `.py`, JavaScript, package, manifest, or runtime source file had a
validation-window mtime. This distinguishes the auto-generated bytecode from
authored plugin code but does not waive the frozen byte-identity requirement.

## Final state and next action

Final state is deliberately healthy and reviewable:

```text
49956 PGID 49956 launchd-owned parent
49964 PGID 49964 owned anchor
49967 PGID 49964 npm
49990 PGID 49964 Node start shim
50005 PGID 49964 canonical uv-Python launcher
50227 PGID 49964 canonical uv-Python backend/listener
```

Stable status is `running`, Viewer/runtime record is `0.4.26`, page and server
API are ready, and one listener owns `127.0.0.1:3245`. No old PGID, orphan npm,
Node shim, Python backend, or second listener remains.

Requirement coverage:

- former CVS-R04-F01 complete-tree ownership/drain: pass;
- actual PGID topology and no escaped descendants: pass;
- idempotence, restart, record matrix, SIGKILL, TERM, durable stop, foreign
  listener, exact preview, Tailscale, and XT60 project boundaries: pass;
- plugin-cache byte identity: **fail / release blocker**.

Next action: repair the runtime/validation environment so Python bytecode is
not written into the plugin cache, then validate from an explicitly frozen
cache inventory. Do not delete or normalize the current plugin cache as part
of this receipt. Independent formal review remains blocked until that gate
passes.

---

# CVS-R04-R1 anchored-group formal rereview

Reviewer: `viewer_refresh_reviewer` independent formal reviewer
Date: 2026-08-24
Worktree: `/Users/scottchu/.codex/worktrees/a373f6e6-90f4-4c0e-857b-643add242937/design-projects`
Branch: `codex/xt60-p17-r2-direct-cad`
Baseline HEAD: `df9af826385db3f625917eca15a6d64273d8fd5f`

## Formal decision

**ACCEPT CVS-D03-R1/R2 candidate**
`4e89ad3d2efce80b2381e439c43af0623245d1c2443fca5ea0fb24b10bb72988`.

The anchored process group fixes the former `CVS-R04-F01` orphan-backend
blocker. The parent authorizes exactly one detached anchor through its original
`ChildProcess` and private nonce-bearing IPC channel; the anchor's live PID,
PGID, and process-start evidence reserve the numeric group before either TERM
or KILL. The real npm -> Node -> canonical uv-Python topology inherits that
group, and the validator's installed restart, TERM, and direct managed-label
SIGKILL challenges found no surviving backend, escaped descendant, duplicate
listener, or second group signal after KILL.

CVS-D03-R2 is accepted as a narrow evidence-boundary clarification, not an
unsafe waiver. It does not change the candidate or service environment. It
continues to protect every authored/package file, native extension, asset,
legacy bytecode outside `__pycache__`, and symlink, while classifying only
interpreter-created `.pyc`/`.pyo` beneath an exact `__pycache__` path component
as ephemeral. It forbids cleanup, restoration, precompilation, redirected
pycache, or authored plugin edits.

## Frozen fingerprint

The required formal-review manifest was verified before review:

```text
5f0b15da97095741523919c4db44e887d4e75ef7b8eae918da5c362e5bbbd518  /tmp/cvs-r04-r1-formal-review-input-manifest.txt
```

Every entry matched, including:

- DESIGN: `ebd6944efa36ae3851571d3d460edb0eb130093d03607be0c19d9cd08cb4709a`;
- pre-rereview VALIDATION receipt: `8773f12764cf51694403d7518e17170d7e80312e7a29e1a62f735a5936dc9b65`;
- installed-payload manifest/candidate:
  `4e89ad3d2efce80b2381e439c43af0623245d1c2443fca5ea0fb24b10bb72988`;
- launcher: `ab17131a164890d062f5538b80f511074d9e6522adfcc95e72408a7bb8a1f596`;
- runtime-refresh tests:
  `3e9f55be9bad49e1b5c360767a9574105a80a0e5aece8d094f9919b77b7f2d9d`;
- anchor fixture:
  `04d648681ffb1e45112885576b4a7c76e2c794f23d412ba379daaed43cc0d80b`.

No candidate byte changed during rereview.

## Process ownership and lifecycle review

Source review confirmed:

- the anchor is spawned detached and verified before npm starts;
- TERM is sent only to the negative, freshly re-proven owned PGID;
- graceful completion requires the anchor to be the sole remaining member and
  no owned listener, followed by IPC release and group absence;
- escalation re-proves the still-live anchor, sends exactly one group KILL,
  then performs observation only, closing the PGID-reuse signaling race;
- process table and port observations are quiescence evidence, never signal
  authority;
- an ownership-proof failure returns the parent to a non-replacement safety
  hold rather than killing a discovered PID;
- parent IPC loss invokes the anchor's emergency group drain;
- the plist's only lifecycle amendment is fixed `ExitTimeOut=15`.

The full deterministic suite was independently rerun: **28 passed, 0 failed**.
It includes anchored turnover, SPA/API failure, stubborn-child TERM/KILL,
failed-provenance/no-signal, foreign post-drain listener, external lifecycle
signal, abrupt parent death, and the real bundled-npm/canonical-Python topology
on reviewer port `58102`. The real group was absent and its port free before a
replacement started; sampled listener count never exceeded one.

CVS-V04-R1 additionally proves the installed launchd behavior:

- stable restart and all six stale/missing/malformed start/restart recoveries
  drained old PGIDs;
- direct `launchctl kill SIGKILL` removed the old listener by the first 100 ms
  sample and drained the full old PGID in about 3.3 seconds;
- launchd's replacement could coexist briefly only with the old ownership
  anchor, never with the old backend/listener; maximum listeners was one;
- external TERM drained before replacement; durable stop remained disabled
  beyond a throttle interval; foreign-port start remained blocked without
  killing or adopting the fixture.

Current read-only production evidence still matches the candidate: parent PID
`49956` is in PGID `49956`; anchor PID `49964`, npm `49967`, Node shim `49990`,
canonical uv-Python launcher `50005`, and backend/listener `50227` are all in
the distinct owned PGID `49964`. One listener owns `127.0.0.1:3245`.

## D03-R2 cache-boundary evidence

All eleven CVS-V04-R1 cache deltas were reconstructed to their full relative
paths and checked independently. Every item is a regular file, contains an
exact `__pycache__` component, ends in `.pyc`, and still matches the receipt's
recorded SHA-256. No item is `.pyd`, source, package metadata, asset, legacy
bytecode, or unknown content. The eleven-file list therefore satisfies the
exact D03-R2 ephemeral predicate.

Because the prior validator retained only a broad pre/post digest, this review
also performed the authorized focused two-inventory rerun. It resolved the
cache root once, used `lstat` without following symlinks, byte-sorted relative
paths, applied the exact component-and-basename predicate, and serialized
canonical `{path,sha256,size,mode}` arrays. The complete evidence is preserved
at:

```text
/tmp/cvs-r04-r1-cache-pre-authored.json
/tmp/cvs-r04-r1-cache-post-authored.json
/tmp/cvs-r04-r1-cache-pre-ephemeral.json
/tmp/cvs-r04-r1-cache-post-ephemeral.json
/tmp/cvs-r04-r1-cache-pre-symlinks.json
/tmp/cvs-r04-r1-cache-post-symlinks.json
```

The focused interval included all 28 tests, stable installed status, local and
Tailscale exact pages, and the exact local artifact request. Results:

```text
authored entries: 1120 -> 1120
authored digest: 6f6c374dbb1aa648d1fb2f2e180df9f04961ef9722ce149d77e2eb1ccac8caf8 -> identical
ephemeral entries: 128 -> 128
ephemeral digest: eff743cac3ff22b23778207560ab4ef96fd7cc6e28b9ba7917d66e52dd57085e -> identical
symlink entries: 0 -> 0
symlink digest: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 -> identical
authored added/deleted/changed: 0/0/0
ephemeral added/deleted/changed: 0/0/0
symlink added/deleted/changed: 0/0/0
```

No plugin-cache file was deleted, restored, normalized, edited, or
precompiled. This fresh aggregate proof closes the evidentiary weakness in the
original broad-digest-only receipt.

## Remaining boundary evidence

- installed current manifest is exact candidate `4e89ad3d...`;
- stable shim remains `998bb2b6...`;
- installed plist remains `b9dd71ab...` and lints successfully;
- install manifest is current; launcher and CLI syntax pass;
- exact XT60 page is HTTP 200 locally and through Tailscale;
- exact XT60 artifact is HTTP 200 with `state:"ready"`;
- Tailscale Serve JSON remains byte-identical with SHA-256
  `5037675750347d2e9d6e4fafe5dbf66912c59404bc28cb320cb3f3fc19069cef`;
- `git diff --name-only -- projects/xt60-bend-jig` is empty;
- the root uv Python remains the sole Viewer interpreter.

## Findings and residual risks

Release blockers: none. No high, medium, or low defect was found in the scoped
candidate.

Accepted residuals remain those documented by D03/D03-R1: cache turnover can
cause a bounded short outage; at least one valid Viewer runtime must exist;
polling adds small ongoing work; and an unprovable ownership/quiescence state
fails safe by retaining the parent instead of permitting a replacement. An
abrupt parent SIGKILL can briefly overlap the replacement parent/anchor with
the old emergency anchor, but the validated old listener is gone first and the
listener count remains at most one.

Next action: the exact candidate may proceed to delivery. This review does not
provide physical or CAD-design acceptance and does not authorize unrelated
XT60 changes.

No production lifecycle, Tailscale setting, plugin-cache content, XT60 project
file, or implementation file was changed by this rereview. Its only repository
write is this appended CVS-R04-R1 receipt.
