# CAD Viewer singleton service contract (CVS-D01)

Status: CVS-D02 frozen and implementation-ready; supersedes CVS-D01
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
