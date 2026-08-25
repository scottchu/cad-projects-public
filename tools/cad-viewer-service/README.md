# CAD Viewer singleton service

This controller installs and manages one per-user macOS LaunchAgent named
`com.scottchu.cad-viewer`. The service owns only `127.0.0.1:3245`, survives the
shell or ChatGPT session that started it, and remains disabled across logins
after an explicit stop.

The installed launcher re-resolves the contained Viewer plugin runtime every
two seconds. When the plugin cache adds a preferred version, removes the
selected version, or leaves the API alive while the Viewer page disappears,
the launcher drains the complete npm/Node/Python tree inside its dedicated,
owned process group before it exits nonzero and lets launchd start the same
singleton on the current valid runtime. A persistent Node group anchor prevents
PID/PGID reuse during TERM/KILL proof; port and process-table observations are
quiescence checks and are never signal authority. The URL remains fixed; a
cache turnover can cause a short interruption and an open browser may need a
reload. No private runtime copy is retained, so at least one valid installed
Viewer runtime must exist in the plugin cache.

The frozen lifecycle and safety contract is in `DESIGN.md`. In particular, the
service always uses the canonical repository uv environment at
`/Users/scottchu/Projects/personal/design-projects/.venv/bin/python3`; it never
discovers or falls back to a system, Homebrew, pyenv, or project-local Python.

## First use

From any checkout or worktree containing this reviewed source payload, run:

```sh
tools/cad-viewer-service/bin/cad-viewer start
```

The first successful start validates `payload/install-manifest.json`, installs
a content-addressed release under `~/Library/Application Support/CADViewer`,
and atomically copies the stable `~/.local/bin/cad-viewer` shim. Neither that
shim nor the LaunchAgent refers back to the source checkout. Subsequent
lifecycle commands are:

```sh
cad-viewer status
cad-viewer restart
cad-viewer stop
cad-viewer logs --lines 100
cad-viewer url --workspace /absolute/workspace --file relative/model.step.py
```

`start` and `restart` recover a missing, malformed, or stale `runtime.json`
without manually renaming or deleting that record. `status` remains read-only
and reports the record issue separately from hard dependency failures. Service
readiness requires both the base Viewer page and the managed
`/__cad/server` API; an API-only response is not considered healthy.

Every command accepts `--json`. In JSON follow mode, `logs -f --json` buffers a
bounded tail and emits one final object when interrupted.

If canonical Python is missing or incomplete, repair the single root
environment from the canonical repository instead of creating another one:

```sh
uv sync --all-packages --all-groups
```

## Deterministic checks

Use the Node executable bundled with ChatGPT; no npm install is required:

```sh
NODE=/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node
"$NODE" --test tools/cad-viewer-service/tests/*.test.mjs
"$NODE" tools/cad-viewer-service/scripts/generate-install-manifest.mjs --check
"$NODE" --check tools/cad-viewer-service/payload/cli.mjs
"$NODE" --check tools/cad-viewer-service/payload/install.mjs
"$NODE" --check tools/cad-viewer-service/payload/launch-viewer.mjs
```
