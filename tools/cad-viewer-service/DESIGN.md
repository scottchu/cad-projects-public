# CAD Viewer singleton service contract (CVS-D01)

Status: CVS-D03 frozen and implementation-ready; supersedes CVS-D02
Baseline: `cb020f6cf01876e01d1e6501fec8861a527aa248`
Scope: user-level CAD Viewer service and controller only; no CAD source,
artifact, project, Tailscale, or Viewer-runtime edits.

## Outcome and invariants

One macOS LaunchAgent owns one CAD Viewer at `127.0.0.1:3245`. It survives the
terminal or ChatGPT session that invoked it, restarts after a crash, and starts
again at the next user login only when the user has left it enabled. The command
`cad-viewer stop` persists the disabled state across login until an explicit
`cad-viewer start` or `cad-viewer restart`.

The implementation must preserve these invariants:

1. The only managed label is `com.scottchu.cad-viewer` in domain `gui/$UID`.
2. The only bind address and port are `127.0.0.1:3245`; there is no alternate
   port fallback and no `0.0.0.0` binding.
3. Viewer Python is exactly
   `/Users/scottchu/Projects/personal/design-projects/.venv/bin/python3`, is
   passed as the absolute `VIEWER_CAD_PYTHON`, and must report Python 3.12.
   Missing or invalid Python is a hard, actionable failure; no interpreter is
   discovered or substituted.
4. Node and npm are exactly the executables under
   `/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/`. No PATH-based
   Node/npm lookup is allowed.
5. The Viewer runtime is selected afresh on every service start from installed
   paths matching
   `/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/*/skills/cad-viewer/scripts/viewer`.
6. The controller never kills a PID merely because it owns port 3245. Only
   `launchctl` may stop or restart the controller's own label (plus the one
   narrowly verified legacy migration described below).
7. The service does not create, modify, or remove any Tailscale Serve route.

## Selected architecture

Use a checked-in source payload to atomically install a checkout-independent
user payload plus a persistent user LaunchAgent. No installed path may refer to
a repository checkout or worktree:

- Checked-in source: `<invoked-checkout>/tools/cad-viewer-service/`; it may be
  any checkout/worktree and is only an installation/update source.
- Installed releases:
  `/Users/scottchu/Library/Application Support/CADViewer/service/releases/<payload-sha256>/`
- Atomic active link:
  `/Users/scottchu/Library/Application Support/CADViewer/service/current` ->
  `releases/<payload-sha256>`
- Stable user command: `/Users/scottchu/.local/bin/cad-viewer` is a copied,
  user-owned shim that invokes `service/current/cli.mjs`; it is not a symlink to
  repository source.
- LaunchAgent plist:
  `/Users/scottchu/Library/LaunchAgents/com.scottchu.cad-viewer.plist`
- Service target: `gui/$UID/com.scottchu.cad-viewer`
- Logs:
  `/Users/scottchu/Library/Logs/CADViewer/stdout.log` and `stderr.log`
- Runtime record (selected path/version and launch time):
  `/Users/scottchu/Library/Application Support/CADViewer/runtime.json`
- Install history/provenance:
  `/Users/scottchu/Library/Application Support/CADViewer/service/install-history/`

The checked-in `bin/cad-viewer` and installed stable shim are small zsh
entrypoints that `exec` the fixed bundled Node binary; their shebangs must not
discover Node. A repository-source invocation passes its adjacent payload root
to `cli.mjs`. The installed shim always invokes the active installed
`service/current/cli.mjs`. Thus an explicit `start` from newer checked-in source
self-updates the durable payload, while ordinary `~/.local/bin/cad-viewer start`
validates and reuses its current installed payload. Deleting the source
worktree afterward cannot affect the command or service.

The LaunchAgent directly invokes the fixed bundled Node binary with
`/Users/scottchu/Library/Application Support/CADViewer/service/current/launch-viewer.mjs`.
That launcher resolves the installed Viewer runtime, writes the runtime record
atomically, forces `VIEWER_CAD_PYTHON`, and spawns the fixed npm:

```text
/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/npm
  --prefix <resolved-runtime> run start --
  --host 127.0.0.1 --port 3245 --json
```

The launcher's PATH is the bundled Node directory followed only by macOS system
paths. It must not include Homebrew, pyenv, asdf, or another Python location.
Signals and the child exit status are propagated so launchd can supervise the
job correctly.

The plist is rendered from the active payload's checked-in template and
installed atomically after `plutil -lint`; its program path references only the
installed `current` link. It has `RunAtLoad=true`, `ProcessType=Interactive`, a 10-second
`ThrottleInterval`, and `KeepAlive={SuccessfulExit=false}`. A crash/non-zero
exit is restarted; `launchctl bootout` is the deliberate-stop mechanism. The
plist remains installed after stop.

### Install, update, and rollback

Every source payload includes a canonical `install-manifest.json` containing a
format version plus the SHA-256 and executable mode of every installable
relative path. It contains no absolute source path. `payload-sha256` is the
SHA-256 of its UTF-8, recursively key-sorted, compact JSON bytes with no final
newline. Symlinks, absolute paths, `..`, unlisted files, and a manifest that
includes itself are rejected. The exact manifest bytes are copied beside the
listed files in the release so the installed payload is independently
revalidatable; they are not an entry in their own file list.

Before lifecycle mutation, `start` (and `restart` when invoked from repository
source) performs this transaction:

1. Resolve the invoked source root without assuming the canonical checkout is
   current or clean. Rehash every listed source file and validate modes/schema.
2. Copy only the exact manifest and listed files into a user-private
   `releases/.staging-<pid>-<random>` directory without following symlinks.
   Rehash the copy, set declared modes, then atomically rename it to
   `releases/<payload-sha256>`. An existing same-hash release is reused only
   after full revalidation.
3. Record source absolute path, source Git commit when available, dirty/clean
   state, manifest hash, installed release hash, timestamp, and prior-current
   hash in a new immutable install-history JSON. Provenance is outside the
   content-addressed release and never changes its hash.
4. Atomically replace `current` using a relative `current.new` symlink plus
   rename; atomically copy/rename the stable shim; render/lint/atomically replace
   the plist. Save the prior current target until service acceptance completes.
5. Start/restart and run the normal readiness gate. On success, mark the new
   hash last-known-good. On failure, atomically restore the prior `current`,
   shim, and plist, restart the prior release, and verify its readiness. Report
   both failures if rollback also fails. With no prior release, disable and
   boot out the new service, leaving diagnostic logs and the failed release.

Installation is serialized by an atomically created directory lock at
`service/install.lock/` containing installer PID and process-start evidence. A
live competing writer is polled for at most 15 seconds, then the contender fails
without mutation. A dead/stale owner is atomically renamed out of the lock path
and reclaimed; a lock whose ownership cannot be proved stale is treated as
live. Interrupted
staging directories are never selected and are removed on the next successful
transaction. Retain the active release, last-known-good release, and one prior
release; garbage collection removes no active/rollback target and occurs only
after acceptance. `stop`, `status`, `logs`, and `url` never install or update.

### Runtime selection

The bundled Node resolver must:

1. enumerate only the exact cache glob above;
2. resolve symlinks and reject a candidate whose real path escapes
   `/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/`;
3. require readable `package.json`, `scripts/start-viewer.mjs`, and the npm
   `start` script;
4. parse `package.json.version` as SemVer and choose the highest stable version;
   if no stable version exists, choose the highest prerelease; break a version
   tie by lexicographically smallest real path;
5. fail without launching when there is no valid candidate.

This selection is dynamic; neither the plist nor controller may contain
`cad/0.4.25` or any other installed-version pin.

## Command contract

All commands support `--json` for one final machine-readable object. Human
output must say whether the service is running, stopped/disabled, blocked, or
misconfigured and must show the selected runtime when known.

### `cad-viewer start`

1. When invoked from checked-in source, resolve and fully validate that source
   payload without activating it. When invoked through the stable shim, fully
   validate the active installed payload and perform no source lookup.
2. Validate canonical Python, Python 3.12, bundled Node/npm, one valid Viewer
   runtime, the candidate/active payload's plist template, and writable user
   state/log directories.
3. Determine managed state and apply the narrowly verified one-time predecessor
   migration when applicable. Otherwise, if not loaded, check port 3245 before
   changing `current`, plist, shim, or enabled state. Any listener not
   proven to descend from the managed launchd job is a conflict: report its
   PID/command when readable, leave it alive, leave the service's prior enabled
   state unchanged, and return exit 2.
4. If the managed service is already healthy and the payload did not change,
   return success without changing its PID or spawning another process.
5. If validated invoked source differs, perform the atomic install/update
   transaction above. Otherwise retain the active installed payload.
6. Atomically refresh the installed plist and
   stable command, run `launchctl
   enable gui/$UID/com.scottchu.cad-viewer`, then `launchctl bootstrap gui/$UID
   <plist>` if unloaded or `launchctl kickstart -p <service-target>` if loaded.
7. Poll for up to 15 seconds. Success requires HTTP 200 from
   `http://127.0.0.1:3245/__cad/server`, JSON `app="cad-viewer"`, `port=3245`,
   and an API-reported backend PID whose parent chain reaches the launchd job
   PID. A bare page HTTP 200 is insufficient.

`start` is idempotent for the same payload. A changed, valid invoked-source
payload is an intentional update and must pass acceptance or roll back.

### `cad-viewer stop`

Run `launchctl disable <service-target>` first, then `launchctl bootout
<service-target>` when loaded. Treat an already-unloaded service as success.
Wait up to 10 seconds for the managed descendant to release port 3245. Never
kill a remaining listener; if a different process owns the port, report it as
unmanaged. Success requires the disabled override to be present in
`launchctl print-disabled gui/$UID`. Keep the plist installed.

### `cad-viewer restart`

An explicit restart means enabled and running afterward. If the service is
healthy, run `launchctl enable` followed by `launchctl kickstart -k -p` on only
the managed target, then apply the same 15-second readiness gate as `start`.
If unloaded or disabled, use `start` semantics. Never kill a port owner by PID.

### `cad-viewer status`

This command is read-only. It combines `launchctl print`, `launchctl
print-disabled`, the port owner, the `/__cad/server` payload, backend ancestry,
the runtime record, and canonical dependency checks. It reports exactly one of:

- `running`: enabled, loaded, and the managed backend passes the readiness gate;
- `starting`: loaded but still within launch throttling/startup;
- `stopped`: unloaded and not disabled;
- `disabled`: disabled override present and managed job unloaded;
- `blocked`: managed job cannot become ready, including a foreign port owner;
- `misconfigured`: canonical Python, bundled Node/npm, runtime, plist, or record
  violates this contract.

Exit codes are 0 for `running`, 1 for `stopped`/`disabled`, and 2 for all other
states. Status never equates an unmanaged CAD Viewer on port 3245 with a healthy
singleton. When facts overlap, classification precedence is `misconfigured`,
`blocked`, `running`, `starting`, `disabled`, then `stopped`.

### `cad-viewer logs`

`cad-viewer logs` shows the last 100 lines of both named log files with clear
headings. `--lines N` changes the count and `-f` follows both via `/usr/bin/tail
-F`. Missing logs are reported without creating or starting the service. Log
files and their parent directory are user-only writable; startup rotates either
file above 10 MiB to one `.1` file before bootstrap.

### `cad-viewer url`

The command requires `running` status, then prints both bases:

```text
local:     http://127.0.0.1:3245
tailscale: https://mac-mini.duckbill-ionian.ts.net
```

Optional `--workspace <absolute-directory>` and `--file <relative-path>` append
the correctly URL-encoded absolute workspace path and `?file=` selector. Both
paths must resolve inside the workspace and exist; generated models may name
their existing `.step.py` source. `--local` or `--tailscale` prints only that
URL. This command reads the existing Tailscale base as a fixed presentation
setting; it never runs or configures `tailscale serve`.

## State transitions

```text
first start / explicit start
  STOPPED or DISABLED --enable+bootstrap--> STARTING --readiness--> RUNNING

crash/non-zero exit
  RUNNING --launchd KeepAlive--> STARTING --readiness--> RUNNING

explicit stop
  RUNNING/STARTING --disable+bootout--> DISABLED

explicit restart
  RUNNING --enable+kickstart -k--> STARTING --> RUNNING
  DISABLED/STOPPED --start semantics--> STARTING --> RUNNING

foreign port / missing dependency
  STOPPED/DISABLED --preflight fails, no mutation--> BLOCKED or MISCONFIGURED
```

There is no transition that adopts or kills an arbitrary listener.

### One-time predecessor migration

The current ephemeral predecessor label `com.codex.cad-viewer` may be removed
only during the first successful `start`, and only when all of these checks
pass: `launchctl print gui/$UID/com.codex.cad-viewer` exists; its arguments
contain the installed text-to-cad CAD Viewer runtime, host `127.0.0.1`, and
canonical Viewer start command; and `/__cad/server` identifies `cad-viewer` with
a backend PID descending from that legacy job. The controller then uses only
`launchctl bootout gui/$UID/com.codex.cad-viewer`, never a PID signal, records
the migration, and proceeds. If any check fails, it is foreign: fail safely and
print manual diagnostics. Migration must never run again once the new label is
installed.

## Failure handling and security

- A missing canonical `.venv` instructs the operator to run `uv sync
  --all-packages --all-groups` from
  `/Users/scottchu/Projects/personal/design-projects`; it never creates a venv.
- A plugin or ChatGPT update is handled on the next restart by runtime
  re-resolution. A missing ChatGPT bundled Node/npm is a hard failure.
- A missing, deleted, dirty, or outdated repository checkout is irrelevant to
  an already installed command: only the content-addressed installed payload is
  executed. Updates occur only from an explicitly invoked, validated source.
- A startup loop is throttled to 10 seconds. `status` presents the last log
  lines and exact failed prerequisite rather than claiming readiness.
- All management is in the current user's `gui/$UID` domain; no sudo, system
  daemon, privileged port, or cross-user state is allowed.
- Bind remains loopback-only. CAD Viewer is unauthenticated and can serve local
  files selected by URL; remote access relies on the separately administered
  Tailscale trust boundary. The controller does not widen that boundary.
- The CLI must reject symlink/path traversal for runtime resolution and URL
  construction and quote every path without shell evaluation.

## Alternatives rejected

- `nohup`, a terminal background process, tmux, or an agent-owned exec session:
  lifecycle remains coupled to a shell/session and has no durable disabled
  state.
- A root LaunchDaemon: unnecessary privilege, wrong per-user GUI/login
  lifecycle, and broader filesystem exposure.
- A fixed plugin version in the plist: breaks after cache upgrades/removal.
- Port probing with automatic alternate ports or killing the occupant: breaks
  the stable Tailscale route and risks terminating unrelated work.
- launchd socket activation: the existing Viewer does not accept an inherited
  listening socket; an adapter adds failure modes without benefit.

## Acceptance tests

Tests may invoke checked-in source from an isolated worktree, but the installed
service must remain functional after that worktree is removed. Tests preserve
the existing external Tailscale route.

1. **Install/start:** from disabled or absent state, `cad-viewer start` reaches
   `running`; exact page and `/__cad/server` are HTTP 200 and the payload passes
   the managed ancestry gate.
2. **Singleton/idempotence:** two additional `start` calls preserve one launchd
   label, one listener, and the same managed job PID.
3. **Payload durability:** installation creates a hash-named release, `current`
   points to it, the stable command and plist contain no checkout/worktree path,
   and source/installed hashes match the manifest. Delete the source worktree;
   a new shell can still run every command and the service remains reachable.
4. **Crash recovery:** force a non-zero death through `launchctl kill` on the
   managed label; within 20 seconds launchd supplies a different PID and status
   returns `running`.
5. **Durable stop:** `stop` yields `disabled`, no managed listener, and
   `print-disabled` true. A fresh `bootstrap`/login-equivalent cannot start it;
   a later explicit `start` clears the override and restores readiness.
6. **Restart:** `restart` replaces the managed PID, restores readiness, and
   never changes host/port.
7. **Foreign-port safety:** while stopped, bind a disposable non-Viewer process
   to 3245. `start` returns 2, does not signal it, does not enable the service,
   and reports `blocked`. Remove the fixture and start normally.
8. **Interpreter gate:** process inspection shows backend execution through the
   exact canonical `.venv/bin/python3`; temporarily invalid configuration fails
   without Homebrew/system fallback.
9. **Dynamic runtime:** resolver unit fixtures prove SemVer, prerelease,
   tie-break, containment, and malformed-candidate rules; integration status
   records the installed selected version without a version pin in plist/code.
10. **Logs and URL:** logs show both streams and follow mode; local and Tailscale
    URLs are correctly encoded and load the same Viewer. Exact artifact
    readiness remains a separate per-artifact check.
11. **Tailscale non-mutation:** `tailscale serve status --json` is byte-equivalent
    before and after start/stop/restart.
12. **Hygiene:** no files change under `projects/`, the plugin cache, or any CAD
    source/artifact path.
13. **Atomic update:** invoke `start` from a newer valid source payload while the
    prior release runs. Verify copied hashes before `current` changes, one
    atomic current switch, service readiness, correct install-history
    provenance, and continued operation after deleting that source.
14. **Rollback:** inject failure after the atomic switch. Verify automatic
    restoration and readiness of the prior hash, no mixed-version payload, no
    broken stable shim/plist, and preserved failed-release diagnostics.
15. **Installer validators:** reject altered content, mode mismatch, traversal,
    symlink escape, malformed/noncanonical manifest, and interrupted staging;
    safely reclaim a provably stale lock and reject/times out a live or
    unverifiable concurrent lock without changing `current`.

## Frozen input manifest

The CVS-D02 input manifest is the newline-delimited path-and-content list below,
in this exact order. Its SHA-256 is
`f7fa47e6eccefe9a7247c9f840c2fffb18aec0747493b6c7fcaa506091be772d`.

```text
651d6e177946976015f6b0a9f5231556c300f1b9bf0b37c1c2cfb9ee8e039327  tools/cad-viewer-service/DESIGN.md@CVS-D01
22a4b39ab1439018f2570d0d90326f700f07647ae399a34655a8a5be347382c5  AGENTS.md
fbe7f1f41b1f9f9f1a46e13cec1c5d9cd319a512ec6d13c9ac52c1f65417266a  /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.25/skills/cad-viewer/SKILL.md
```

CVS-D02 also incorporates the observed implementation fact that the service
source exists only in a disposable worktree while the canonical checkout is
dirty/outdated and lacks it; therefore no checkout path is a valid installed
runtime dependency. Any input change invalidates this contract and requires
design review before implementation. The installed Viewer runtime itself is
deliberately dynamic and is validated at each launch rather than frozen here.

---

# CVS-D03: automatic recovery across Viewer cache refreshes

Status: frozen and implementation-ready
Baseline commit: `df9af826385db3f625917eca15a6d64273d8fd5f`
Scope: repair only the singleton service's runtime supervision, readiness, and
explicit lifecycle recovery. All CVS-D02 ownership, installation, stop,
security, and Tailscale invariants remain in force.

## Observed failure and corrected persistence guarantee

The installed LaunchAgent, controller payload, listener, and backend remained
alive after the plugin cache advanced from CAD Viewer `0.4.25` to `0.4.26` and
deleted the selected `0.4.25` runtime. `/__cad/server` still returned HTTP 200,
but the Viewer SPA path returned HTTP 404 because the live backend continued to
serve frontend files from the deleted runtime. The old `runtime.json` then made
the stable `start` and `restart` commands report `misconfigured` before they
could restart the managed job. Manual relocation of `runtime.json` recovered
the service, but manual state surgery is not an acceptable lifecycle step.

"Persistent" therefore means the stable command, one LaunchAgent, fixed port,
and review URL survive the invoking ChatGPT or shell session and automatically
recover to the newest valid installed Viewer runtime after plugin-cache
turnover. It does not mean a private copy of the Viewer runtime is retained.
Recovery is contingent on at least one valid runtime eventually existing under
the frozen cache root; if the cache contains none, launchd retries with bounded
throttling and the stable command reports the missing prerequisite. The URL
does not change, although a cache refresh may cause a bounded interruption and
the browser may need to reload after recovery.

## Selected repair

Keep the dynamic plugin-cache architecture. Do not copy the Viewer runtime into
`Application Support/CADViewer`: doing so would introduce a second runtime
installation, duplicate a large and evolving Python/JS asset tree, and require
a new update/provenance contract. The smaller robust repair is an owned-child
supervisor in the already installed `launch-viewer.mjs`, plus lifecycle
commands that treat an obsolete runtime record as recoverable state.

### Runtime and page supervision

After selecting a runtime, atomically replacing `runtime.json`, and spawning
the fixed npm child, the launcher must supervise that exact selection for its
entire lifetime:

1. Re-run the existing contained SemVer runtime selection every 2 seconds. A
   missing/invalid selected path, no valid candidate, or a newly preferred
   path/version is a refresh event. Selecting a newer valid runtime while the
   old one still exists is intentional; it prevents the service from remaining
   pinned until the old cache directory is later removed.
2. Establish operational health within 15 seconds and then continue checking
   both the base Viewer page and `/__cad/server`. Health requires base-page HTTP
   200 plus server HTTP 200 with `app="cad-viewer"`, `port=3245`, and an integer
   backend PID. `/__cad/server` alone is no longer sufficient. Two consecutive
   HTTP failures are required before recycling so a single transient request
   does not create a restart loop. A runtime-selection change or disappearance
   is filesystem evidence and may recycle immediately.
3. On a refresh event, log the old path/version and exact reason, cancel further
   checks, and terminate only the npm `ChildProcess` created by this launcher.
   First send `SIGTERM`; after 5 seconds an implementation may send `SIGKILL`
   only through that owned child handle. It must never signal a PID discovered
   from the port, HTTP API, `runtime.json`, or process table. Wait for the owned
   child exit, then exit the launcher non-zero using a dedicated refresh exit
   code so `KeepAlive={SuccessfulExit=false}` re-runs the same installed
   launcher. A refresh-requested child exit must not be re-propagated as a
   terminating signal to the launcher.
4. The next launch performs normal dynamic selection and atomically overwrites
   the stale runtime record; if no valid candidate exists yet, preflight exits
   non-zero and launchd's existing 10-second throttle retries. No cache path is
   pinned into the plist, installed payload, or controller.

The launcher must not exit while an owned npm child is still known to be live.
The lifecycle fixture must prove that recycling never creates two simultaneous
listeners. If npm termination can orphan the backend, implementation stops and
reopens this design instead of adding port-PID killing.

### Readiness and explicit command recovery

The controller's `running` and startup-acceptance gates are superseded as
follows:

- Service readiness requires both base-page HTTP 200 and the existing valid,
  managed `/__cad/server` response/ancestry gate. A backend API with a missing
  SPA is `blocked` unless a harder configuration error takes precedence.
- Dependency inspection must separate hard prerequisites from runtime-record
  observations. Missing canonical Python, bundled Node/npm, active payload, or
  a current valid runtime remains a hard error. A missing, malformed, or stale
  `runtime.json` is a status diagnostic but is recoverable by `start` and
  `restart`; those commands must not require deleting or renaming it first.
- `status` remains read-only and reports `misconfigured` when a loaded job's
  record cannot be matched to the currently selected valid runtime. Its JSON
  must expose the record issue separately from hard dependency errors so the
  recovery path is evident.
- Idempotent `start` may preserve the PID only when payload, page, server,
  ancestry, and runtime record all match the currently preferred runtime. If
  the managed job is loaded but any of those runtime/page conditions fail,
  `start` must use managed `launchctl kickstart -k -p` and the normal readiness
  gate even when the controller payload hash is unchanged. `restart` already
  has that forced managed-restart meaning.
- The replacement launcher overwrites `runtime.json` atomically. Recovery must
  neither remove the active content-addressed service release nor reinstall it
  solely because the plugin runtime changed.

Foreign-port behavior is unchanged: neither automatic supervision nor an
explicit command adopts, signals, or replaces an unmanaged listener. Explicit
`stop` remains durable and must not be defeated by the supervisor or launchd.

## Authorized implementation surface

The implementer may change only the following source/test/documentation areas
for this repair:

- `payload/launch-viewer.mjs`: make direct execution import-safe/testable; add
  the fixed runtime/page supervisor, owned-child recycle, and refresh exit path.
  Dependency injection may exist only as an internal exported function used by
  tests; no production CLI flag or environment variable may override host,
  port, cache root, Node/npm, or Python.
- `payload/cli.mjs`: require base-page plus server readiness, separate
  runtime-record diagnostics from hard prerequisites, and force managed
  recovery when the selected runtime/record/page does not match.
- `payload/core.mjs` and `payload/config.mjs`: only small pure helpers and fixed
  supervision constants needed by the above behavior.
- `tests/core.test.mjs` and one focused new launcher/runtime-refresh test file:
  cover runtime-record matching, page/API readiness, supervisor recycling, and
  owned-child/no-duplicate behavior with isolated temporary runtimes and a
  fixture port. Do not add a production configuration override to make testing
  easier.
- `payload/install-manifest.json`: regenerate from the reviewed payload; update
  `scripts/generate-install-manifest.mjs` only if a new installable module is
  strictly necessary.
- `README.md`: state the corrected cache-refresh guarantee, bounded outage, and
  no-manual-runtime-record recovery commands.
- `VALIDATION.md`: independent validator appends evidence only after source and
  tests are frozen.

The plist template, stable shim, label, port, canonical Python, bundled
Node/npm, content-addressed installer, stop semantics, and Tailscale settings
are frozen unless deterministic evidence proves the repair impossible within
this surface. That condition is a design stop, not implicit authorization to
expand scope.

## Failure-driven regression and lifecycle gates

All prior CVS-D02/CVS-V03 gates remain required. The following failures are new
release blockers:

1. **Resolver turnover fixture:** in an isolated cache, launch from valid
   `0.4.25`; make valid `0.4.26` available and remove `0.4.25`. Prove the same
   production selection logic chooses `0.4.26` without a version pin.
2. **SPA-disappearance fixture:** while the supervised child and API fixture
   remain alive, make its page return 404 or remove its selected runtime. Prove
   the supervisor detects the exact failure that escaped the old API-only gate,
   signals only its owned child, exits non-zero, and a supervised second launch
   reaches the new runtime.
3. **No duplicate listener:** sample the fixture listener throughout turnover;
   the listener count is never greater than one, the old child is gone before
   the next launcher becomes ready, and no discovered port PID is signaled.
4. **Stale-record stable CLI recovery:** snapshot the real user runtime record,
   replace it with a syntactically valid `0.4.25` record whose path is absent
   while `0.4.26` is valid, then run the installed stable `cad-viewer start
   --json`. Without moving/removing the stale record manually, it must replace
   the managed job PID, atomically write the selected `0.4.26` record, and
   return `running`. Restore only if the test aborts before normal recovery.
5. **Explicit restart recovery:** repeat the stale-record condition with
   `restart --json`; it must recover through the same managed target. Both
   commands must remain blocked if no valid current runtime exists.
6. **Exact service health:** after each automatic and explicit recovery, the
   base page and `/__cad/server` are HTTP 200, server identity/port/ancestry are
   valid, the selected runtime record exists, and exactly one listener owns
   `127.0.0.1:3245`. An exact project preview page and its artifact endpoint are
   then checked separately before a preview URL is handed to the user.
7. **Durable stop and foreign port:** stop during/after a turnover leaves the
   disabled override present and no managed retry. A foreign 3245 fixture is
   never killed, adopted, or displaced by automatic or explicit recovery.
8. **Persistence boundaries:** installed release, stable command, and plist
   contain no worktree path or runtime version. Tailscale Serve status is
   byte-identical before/after. No project, CAD, plugin-cache, or alternate venv
   file is changed by the production repair.

The automatic fixture may use a temporary cache and fixture port through an
imported internal supervisor API. Live validation uses the fixed production
port and actual stable CLI but must not delete or modify installed plugin-cache
contents.

## Stops and residual risks

Stop and reopen design if the repair requires a private Viewer-runtime copy, a
second LaunchAgent/listener, an alternate port, a Tailscale mutation, an
interpreter fallback, a production test override, edits inside the plugin
cache, or signaling any process not created by the launcher. Also stop if the
owned npm child cannot be retired without leaving a backend listener, or if the
page health check causes a reproducible restart loop under a valid runtime.

Residual risks accepted for this bounded repair:

- A cache refresh can produce a short outage bounded by the 2-second detector,
  owned-child shutdown, launchd throttle, and 15-second startup gate.
- With no valid installed runtime, persistence cannot provide a page; the
  service remains diagnostic/retrying until the external plugin installation
  supplies one.
- A valid higher SemVer runtime is trusted under the existing contained-runtime
  rules. This repair does not add cryptographic provenance for plugin cache
  contents.
- Polling adds small ongoing filesystem/HTTP work. Two-failure HTTP debounce
  limits transient churn; runtime-selection changes remain immediate.

## CVS-D03 frozen input manifest

The design input is the exact newline-delimited manifest at
`/tmp/cvs-runtime-refresh-design-input-manifest.txt`, verified SHA-256:

`8b0669b2f0d2801eaa1206839401fe07e9b535ba595fe8c932fb768cf68c008c`

It freezes the recovered current `runtime.json`, the retained stale `0.4.25`
record, this service's pre-CVS-D03 docs/source/tests, and the baseline commit.
Any change to those inputs before implementation invalidates this contract and
requires a new design fingerprint.

---

# CVS-D03-R1: anchored owned-process-group shutdown amendment

Status: frozen and implementation-ready; supersedes only the D03 direct-child
termination clauses
Baseline candidate: CVS-I04 payload
`2ddeecf807fc53904db4f9b9eefbf69e12134e21c785a51a481c0da2dca73b4b`
Trigger: formal rejection `CVS-R04-F01`

All D03 runtime selection, page-plus-API health, stale-record recovery,
single-label/port, interpreter, content-addressed install, foreign-port,
durable-stop, and Tailscale contracts remain unchanged. This amendment replaces
only the unsafe assumption that terminating the direct npm child terminates the
Viewer process tree.

## Proven failure

The real topology is launcher -> npm -> Node start shim -> canonical uv Python
launcher -> canonical uv Python backend. On a reviewer-owned port, `SIGTERM` to
the direct npm child terminated npm but left the Python backend listening for
more than six seconds. The direct-child fixture in CVS-I04 did not represent
this topology. Therefore the launcher must own and retire a kernel-enforced
process boundary containing the complete spawned tree before it exits or lets
launchd start a replacement.

## Selected macOS ownership boundary

Use one persistent Node group-anchor process, launched by the LaunchAgent's
parent launcher with Node `spawn(..., {detached:true})`. On POSIX/macOS this
creates a new session and process group whose leader PID and PGID are the anchor
PID. The launchd-owned parent launcher remains outside that group. The anchor
then spawns the fixed bundled npm with `detached:false`, so npm and its Node and
Python descendants inherit the dedicated PGID.

The anchor is an internal mode of the installed launcher module, not a second
service, daemon, listener, plist, or user command. It must not accept a
production environment variable or public CLI option that changes paths,
runtime, host, port, Node/npm, or Python. Test dependency injection remains an
import-only API.

Ownership is established before npm is allowed to start:

1. The parent creates a private IPC channel and spawns the anchor detached. It
   records the returned `ChildProcess`, PID, and macOS process-start evidence.
2. The anchor verifies through `/bin/ps` that its PID equals its PGID, installs
   handlers that keep it alive during `SIGTERM`, `SIGINT`, and `SIGHUP`, and
   sends an IPC readiness message containing its PID/PGID and a parent-issued
   one-use random nonce.
3. The parent accepts the boundary only when the IPC handle, nonce, child PID,
   recorded start evidence, and a fresh `ps` PID/PGID observation all match.
   Only then does it instruct the anchor over IPC to spawn npm.
4. The anchor sends npm-started and npm-exit events over the same IPC channel.
   It deliberately remains alive after npm exit until the parent completes
   group quiescence and sends the final direct IPC release.

No unrelated process can be adopted into this group: the group is a new
session created from the owned anchor, and only its descendants inherit it.
Process-table and `lsof` reads are allowed solely to prove membership and
quiescence. No PID learned from those reads, the HTTP API, runtime record, or
port owner may ever be a signal target.

## TERM/KILL and quiescence protocol

Automatic runtime refresh, two-failure SPA refresh, npm/worker failure, an
explicit stop, and a launchd restart all use the same one-shot group-drain
state machine:

1. Stop health polling and reject a second concurrent drain request.
2. Immediately before the first group signal, prove the anchor remains the
   same live `ChildProcess` with the frozen PID, start evidence, and
   `PGID == anchor PID`. If this proof fails, do not signal a numeric group and
   do not exit into a replacement; report an unsafe-ownership failure.
3. Send `SIGTERM` once to the negative, proven PGID. This is the only non-direct
   signal scope and reaches the anchor, npm, Node shim, and both canonical
   Python processes simultaneously. The anchor's handler keeps the group ID
   allocated while descendants drain.
4. For up to 5 seconds, poll the dedicated PGID. Success means the anchor is the
   only remaining group member and no member of that group listens on the
   managed port. Never infer success from npm exit alone.
5. On graceful success, send a final message over the original IPC handle that
   lets only the known anchor exit. Wait for its `ChildProcess` exit, confirm
   the PGID no longer exists, and confirm the managed port is free before the
   parent launcher exits.
6. If descendants remain after 5 seconds, re-prove that the anchor is still the
   same live leader, then send `SIGKILL` once to the negative PGID. That syscall
   includes the anchor. After it, never signal that PGID again; only poll until
   the group is absent and the port is free. Allow 5 additional seconds for
   this final quiescence proof.

The persistent anchor closes the PGID-reuse race: before TERM or KILL, its live
PID reserves the group identity. After group KILL there is no second group
signal, so a later PGID reuse cannot be targeted. A check-then-signal sequence
without a live anchor is forbidden. A plain detached npm group is rejected
because npm can exit early and remove the ownership anchor while Python remains.

Port quiescence is a gate, not authority. If the owned group is gone but a
foreign process has acquired port 3245, the parent must not signal it and must
not start a replacement into it. The parent remains loaded in a blocked
post-drain wait, periodically checking only for the port to become free. Once
free, automatic refresh may exit with code 75 so launchd restarts it. A durable
stop may always end this empty parent; it must not re-enable the label.

If group membership cannot be read, the anchor vanishes before a required
signal, a descendant escapes the PGID, group/port quiescence cannot be proven,
or the actual production topology does not inherit the anchor PGID, the repair
is rejected. Do not fall back to recursive PID discovery, port-owner killing,
or optimistic launcher exit.

## Launcher and launchd lifecycle

- **Automatic refresh:** drain the group, prove group and port quiescence, then
  exit the parent with refresh code 75. `KeepAlive` restarts only after that
  exit, so the new runtime cannot overlap the old listener.
- **Natural npm/worker failure:** the anchor reports the event but remains
  alive. The parent drains any remaining group members, proves quiescence, then
  exits non-zero so launchd may recover. Npm exit is never itself the drain
  completion event.
- **Explicit `restart` or recovery `start`:** `kickstart -k` asks launchd to
  terminate the old parent. Its signal handler completes the same group drain
  before re-raising the launchd signal. Launchd then starts one replacement;
  the CLI applies the existing page/API/ancestry readiness gate.
- **Explicit `stop`:** the CLI still disables the label before `bootout`. The
  signaled parent drains the group and port before exiting; the disabled
  override prevents the non-zero/signal exit from relaunching it. Already
  stopped/disabled behavior is unchanged.
- **Abrupt parent crash:** the LaunchAgent remains the owning job. Acceptance
  must prove `launchctl kill SIGKILL` does not strand the detached group before
  launchd replaces it. If macOS launchd does not reap the detached descendants
  in this topology, the detached-anchor architecture is invalid and design
  must reopen.

The plist may add a fixed `ExitTimeOut` of 15 seconds so launchd permits the
5-second TERM window, one KILL, and final quiescence before killing the parent.
No other plist ownership/lifecycle field may change. Existing CLI readiness and
port-release waits may be lengthened only enough to cover this 15-second drain;
they may not add alternate ports or PID killing.

## Exact authorized implementation delta

The repair owner may modify:

- `payload/launch-viewer.mjs` for the internal anchor mode, IPC handshake,
  dedicated-group spawn, membership proof, unified group drain, and parent
  lifecycle integration;
- `payload/config.mjs` only for fixed handshake/drain/exit-time constants;
- `payload/cli.mjs` only if readiness/stop waits must cover the fixed drain;
- `payload/launchd/com.scottchu.cad-viewer.plist.template` only to add the
  fixed 15-second `ExitTimeOut`;
- `tests/runtime-refresh.test.mjs` and at most one new test helper under
  `tests/` for the anchored-group and production-topology regressions;
- `tests/core.test.mjs` only for a pure ownership/quiescence helper if needed;
- `scripts/generate-install-manifest.mjs` and
  `payload/install-manifest.json` only to enumerate/hash a strictly necessary
  new installed module;
- `README.md` for the externally visible process-tree persistence guarantee;
- `VALIDATION.md` for a new independent validation receipt.

`core.mjs`, installer/rollback behavior, stable shims, labels, bind address,
port, canonical Python, bundled Node/npm, cache resolver, Tailscale base, and
all CAD/project files remain frozen unless the repair hits an explicit design
stop.

## Mandatory regressions and live gates

1. **Actual production topology on reviewer port:** use the real selected Viewer
   runtime, exact bundled npm, canonical uv Python, production arguments and
   environment, but a reviewer-owned free loopback port. Start it through the
   real anchor/supervisor. Prove page/API readiness and observe one anchor PGID
   shared by npm, Node shim, Python launcher, and Python backend while the
   parent launcher has a different PGID.
2. **TERM turnover:** trigger the supervisor's runtime-refresh path without
   editing the real plugin cache. Sample process-group membership and listener
   count throughout. The Python backend must disappear, the old group and port
   must be quiescent before the supervisor returns refresh code 75, and a real
   replacement may start on the same port only afterward. Listener count must
   never exceed one.
3. **KILL escalation and PGID race:** use a reviewer-owned anchored descendant
   that ignores TERM. Prove the anchor stays live through the grace interval,
   the group receives exactly one KILL, no later signal targets that PGID, the
   group becomes absent, and an unrelated process remains alive. Include a
   negative test in which anchor provenance changes/fails: no group signal and
   no replacement is permitted.
4. **SPA/API turnover:** preserve the existing 0.4.25 -> 0.4.26 and SPA-404
   triggers, but run their shutdown assertion through the anchored group rather
   than a direct single-process child.
5. **Launchd restart/crash:** on the installed candidate, `restart` and
   `launchctl kill SIGKILL` each return to one managed listener with a new job
   PID and no old-PGID member/orphan. Capture membership before and after.
6. **Durable stop:** stable `stop` leaves the disabled override, no anchor group,
   no npm/Node/Python descendant, and no listener after at least one launchd
   throttle interval. A later explicit start restores exactly one group.
7. **Foreign-port race:** after an owned group drains, bind a reviewer-owned
   fixture before replacement. Prove the parent does not signal/adopt it and no
   Viewer replacement starts until the fixture releases the port.
8. **Immutable boundaries:** verify the candidate through the installed stable
   command, content-addressed payload, exact Viewer page/API and project
   artifact readiness. Plugin-cache inventory and Tailscale Serve JSON must be
   byte-identical before/after; no project or alternate venv changes.

Tests may inspect `ps`, `lsof`, and group membership. They may signal the
reviewer-owned group created by the same fixture. They must never signal the
production service during the reviewer-port regression or use a discovered
port PID as signal authority.

## Rejected alternatives and residual risk

Rejected:

- direct npm TERM/KILL: formally proven to orphan Python;
- recursive PPID enumeration and per-PID signaling: descendants can reparent
  between discovery and signal and a reused PID can target unrelated work;
- signaling the backend PID from `lsof`, `/__cad/server`, `runtime.json`, or
  `ps`: observation is not ownership;
- a detached npm group without a persistent anchor: early npm exit reopens the
  PGID ownership/reuse race;
- relying only on launchd's undocumented descendant cleanup or repeatedly
  self-kickstarting from the launcher: neither proves old-port quiescence before
  replacement;
- a second daemon, alternate port, proxy, self-contained Viewer copy, or
  Tailscale change: unnecessary architecture expansion.

Residual risk is limited to abrupt kernel/launchd behavior outside the graceful
protocol. It is accepted only if the installed `launchctl kill SIGKILL` gate
proves macOS reaps the detached group without orphaning. Failure of that gate,
or any escaped production descendant, is a release blocker and reopens design.

## D03-R1 frozen input

The exact manifest `/tmp/cvs-r04-design-repair-input-manifest.txt` was verified
entry-by-entry. Its SHA-256 is:

`825d40f959283c3e33a4fa7c3717166a4ae406b1ca9af9aa70b70cbb8cbf1e82`

It freezes the rejected CVS-I04 implementation, CVS-D03 contract, CVS-V04
evidence, and CVS-R04 formal rejection. Any input change before implementation
invalidates this amendment and requires a new task fingerprint.

---

# CVS-D03-R2: plugin-cache evidence-boundary clarification

Status: frozen clarification; no implementation delta
Candidate remains:
`4e89ad3d2efce80b2381e439c43af0623245d1c2443fca5ea0fb24b10bb72988`
Trigger: `CVS-V04-R1-F01`

This clarification does not change the D03/D03-R1 service architecture,
runtime selection, process-group ownership, lifecycle behavior, installed
payload, or user-facing persistence guarantee. It corrects an overbroad
validation phrase that treated interpreter-generated Python bytecode as though
it were authored plugin/package content.

## Decision

The immutable plugin-cache gate distinguishes two inventories:

1. **Authored/package inventory:** every regular file under the exact
   text-to-cad cache root except the narrowly classified bytecode files below.
   This includes all Python source, JavaScript, JSON, package metadata, lock
   files, HTML/CSS, GLB/assets, shell files, native libraries, `.pyd` files,
   legacy `.pyc`/`.pyo` outside `__pycache__`, and any other regular file.
2. **Interpreter-ephemeral inventory:** only a regular file whose relative path
   contains a path component exactly equal to `__pycache__` and whose basename
   ends exactly in `.pyc` or `.pyo`.

The tighter rule is intentional. Do not exempt all files beneath
`__pycache__`, do not use the broader `*.py[cod]` glob, and specifically do not
exempt `.pyd`: a native extension is distributed package content, not Python
bytecode cache. A `.pyc` outside `__pycache__` also remains protected because it
may be deliberately packaged legacy bytecode.

Executing the selected runtime with the canonical Python may add or refresh
the narrow ephemeral set through normal imports. That is not an authored-code
mutation and is permitted evidence-layer activity. The service still must not
delete, restore, normalize, edit, or intentionally precompile plugin-cache
contents. No validator may clean bytecode before or after a run merely to make
digests match.

## Canonical reproducible inventory

The pre- and post-validation inventories must be generated by the same
path-safe procedure:

1. Resolve the cache root once with `realpath`; walk it without following
   symlinks and include every regular file found by `lstat`.
2. Express each path relative to that resolved root with `/` separators.
   Reject a path that escapes the root. Sort entries by the UTF-8 bytes of the
   relative path under `LC_ALL=C`; do not depend on filesystem enumeration
   order.
3. Classify with path components and basename, not substring matching. The
   ephemeral predicate is exactly:
   `components.includes("__pycache__") && /\.(?:pyc|pyo)$/.test(basename)`.
4. For each authored/package entry record canonical fields
   `{path, sha256, size, mode}`. Serialize the complete sorted array as compact,
   recursively key-sorted UTF-8 JSON with no final newline and SHA-256 those
   exact bytes. The authored pre/post digest and every entry must match.
5. Record the ephemeral entries separately with the same fields. Preserve both
   complete pre/post lists and emit explicit added, deleted, and content-changed
   path lists with old/new hashes. Ephemeral differences are permitted but may
   not be hidden inside one aggregate digest.
6. Record symlinks separately as sorted `{path,target}` entries and require the
   pre/post symlink topology to match. No non-regular entry may be used to hide
   an authored-file change.

Mtime is diagnostic only and cannot prove content identity. The authored
SHA-256 manifest is the authority. A validation passes this boundary only when
the authored/package manifest and symlink topology are identical and every
regular-file delta belongs to the exact ephemeral predicate. Any added,
removed, or changed `.py`, JS, JSON, asset, package file, `.pyd`, legacy
bytecode, or unknown `__pycache__` content remains a release blocker.

## Effect on CVS-V04-R1 and formal review

This is a contract clarification, not an implementation repair. It does not
authorize `PYTHONDONTWRITEBYTECODE`, `-B`, a redirected pycache prefix, a cache
cleanup, a plugin edit, or a new service payload. The candidate digest remains
`4e89ad3d...`.

The CVS-V04-R1 mechanical results remain usable: 28 deterministic tests, the
actual bundled npm/canonical-Python topology, anchored TERM/KILL drain,
restart, record recovery, managed SIGKILL, durable stop, foreign-port safety,
exact page/artifact readiness, Tailscale identity, and project boundary all
refer to this unchanged candidate. Its recorded validation-window cache delta
contains exactly eleven files, each beneath an exact `__pycache__` component
and ending in `.pyc`; no authored/package delta was reported. Under the
clarified classification, that observed delta is interpreter-ephemeral and is
not by itself a release blocker.

Formal review must still check the eleven paths against the exact predicate and
confirm the receipt contains no other regular-file delta. If the reviewer
requires fresh aggregate proof because the prior run retained only the broad
digest, perform a focused evidence rerun of the same candidate using the
canonical two-inventory procedure. Reuse the prior lifecycle/mechanical gates;
do not repeat unrelated XT60 or rod work. The focused rerun may naturally
create or refresh bytecode, must list it, and must not delete or restore cache
files afterward.

## Stops

Reopen or reject if:

- any authored/package entry or symlink differs pre/post;
- a changed file fails the exact `__pycache__` plus `.pyc/.pyo` predicate;
- the evidence has only broad aggregate digests and cannot identify the changed
  paths;
- passing requires deleting/restoring plugin-cache content or changing the
  runtime environment;
- candidate payload `4e89ad3d...` changes before formal review.

This background evidence clarification is independent of, and must not block,
the XT60 rod design work.

## D03-R2 frozen input

The exact manifest
`/tmp/cvs-v04-r1-cache-boundary-design-input-manifest.txt` was verified
entry-by-entry. Its SHA-256 is:

`acf136318f88772be71aba116e63e544c95a2675bdab4acb08fb875a43bade5a`

It freezes the D03-R1 design, unchanged `4e89ad3d...` candidate launcher and
payload, runtime-refresh regression, and CVS-V04-R1 validator receipt.
