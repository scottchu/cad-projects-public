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
