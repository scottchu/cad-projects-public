# CAD Viewer singleton service

This controller installs and manages one per-user macOS LaunchAgent named
`com.scottchu.cad-viewer`. The service owns only `127.0.0.1:3245`, survives the
shell or ChatGPT session that started it, and remains disabled across logins
after an explicit stop.

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
