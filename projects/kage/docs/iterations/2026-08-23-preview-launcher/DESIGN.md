# Kage preview launcher design

## Selected architecture

Use one repository-level standalone POSIX-shell executable, `bin/preview-cad`, with strict mode and small testable functions. Its exact interface is `bin/preview-cad [--sha256 EXPECTED] <workspace-dir> <file-relative-to-workspace>` and it runs from any cwd. Reject a Python console-script plus bin-wrapper: shell is the native boundary for process ownership, environment and signal control, while a Python package entry point would add an avoidable installed-command/venv dependency around a launcher that must diagnose that very venv. It resolves the repository root from its own location, resolves and validates the two user paths, then discovers the newest semantic-version CAD Viewer cache at runtime. It sets `VIEWER_CAD_PYTHON=<repo>/.venv/bin/python` and starts Viewer from the validated workspace. It has no Kage-specific path, SHA-256, or hostname.

Before any port probe, Viewer discovery subprocess, or process action, canonicalize the workspace and requested file. Require a nonempty workspace directory and nonempty relative file argument; reject absolute file paths, lexical `..` components, non-regular files, and resolved files outside the workspace (including symlink escape). The generic launcher accepts any installed Viewer-supported artifact or generator source. A supplied `--sha256` must be an exact lowercase 64-hex digest and match the resolved file before any process action; omission is valid for normal generic use. Kage's consumer command is documentation/validation only and always uses its locked STEP plus `--sha256 dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7`.

The launcher treats port ownership as a state machine:

```text
no listener -> start current Viewer -> API/page health -> POST build -> ready URLs
healthy Viewer -> reuse -> POST build -> ready URLs
identified stale Viewer -> revalidate exact token/API/page -> TERM/wait token disappearance or port free -> start -> health/build -> URLs
owned failed start -> revalidate leader token -> TERM group only if exact -> bounded observe -> fail
unknown/PID-token-drift listener -> fail safely, no signal
```

`/__cad/server` is the identity endpoint, not a bare TCP or HTML response, but it cannot prove the SPA bundle exists: a cached imported artifact may still report `ready` after the Viewer cache's `dist/` has been removed. Therefore identity is followed by a GET of the exact generic workspace review-page URL (with encoded workspace/file and cache-buster), requiring HTTP 200 and stable Viewer shell marker `id="root"`, before the required build POST.

For a reusable/stale pre-existing listener, capture `CURRENT_TOKEN` as its listener PID, `ps` start time, and normalized command only after API/page identity succeeds. An API-identified listener failing the page probe is stale, but it may be signaled only if the same token and API/page identity are confirmed immediately before `TERM`. Once TERM is sent, API loss is expected: wait boundedly for the **same token** to vanish or for the port to become free, then start a new Viewer. Never KILL a pre-existing listener.

For a Viewer started by this invocation, create a new process group and immediately capture the group leader's PID, `ps` start time, and normalized command. Its failed readiness cleanup is deliberately weaker: re-read that exact leader token; absent/drifted means no signal, matched means one TERM to the verified owned group followed by bounded observation. Never KILL, including after timeout, because PGID reuse cannot be excluded. After any accepted reuse/restart and before output, artifact-ready is insufficient: re-read the listener token and require it equals `CURRENT_TOKEN`; token replacement fails with no URL stdout.

Launch readiness is bounded and has no background success path. The script uses `curl --fail-with-body` where available (or a documented compatible fallback), `lsof` only for evidence/PID discovery, and percent-encodes `dir`/`file` query values. All subprocess variables are passed as positional arguments or environment values, never interpolated into `eval`/shell fragments.

The implementation should create a tiny root test fixture/stub harness rather than mock shell builtins globally, at `tests/test_preview_cad_launcher.py`. Environment overridable names such as `PREVIEW_CAD_VIEWER_GLOB`, `PREVIEW_CAD_NPM`, `PREVIEW_CAD_CURL`, `PREVIEW_CAD_LSOF`, `PREVIEW_CAD_PS`, `PREVIEW_CAD_KILL`, `PREVIEW_CAD_SLEEP`, `PREVIEW_CAD_PORT`, and `PREVIEW_CAD_TAILSCALE_HOST` make discovery, generation tokens, and process paths observable. Production defaults remain the contract values. Fixtures must include cache paths with whitespace and semantic versions, a current-runtime provenance capture, and no actual listener/network/cache mutation. They must test that only a matched owned leader receives TERM, no path sends negative KILL, a final listener-token replacement suppresses stdout, and API disappearance after a matched stale-listener TERM does not block restart once its token disappears/port is free. A test-only no-launch/fixture root is acceptable only when the real default remains unchanged and no environment override is needed for ordinary use.

The candidate manifest for review must be a final-LF, path-sorted SHA-256 list covering the frozen contract sections, root launcher/root test/root docs, root workspace metadata used by launch, Kage consumer README/iteration/integrity/manifest, locked STEP/README, and current Viewer skill file hash/path. `__cadgen__` is explicitly excluded as generated runtime output; its contents are neither implementation input nor integrity evidence.

Document the generic CLI and its checksum semantics in root `README.md`; this is necessary because the command is a repository surface. `docs/ARCHITECTURE.md` does not need a change unless implementation establishes a durable repository-wide tool-directory contract beyond this one documented command; do not broaden architecture policy merely to describe usage. Kage `README.md` documents only its pinned consumer invocation and non-acceptance boundary.

## Rejected alternatives

1. **Hardcoded Viewer cache path/version.** Rejected because the 0.4.21 cache was removed while an old process stayed alive; the launcher must follow installed runtime upgrades.
2. **A Kage-owned launcher or default project cwd.** Rejected because the utility must serve any repository workspace and a project root can expose unrelated `cadgen.py` shadowing; launch from the validated caller workspace only.
3. **Escalating cleanup to KILL.** Rejected: PID/PGID reuse means neither stale nor owned failed-start cleanup can establish safe KILL ownership. Matched tokens permit TERM only.
4. **TCP/HTTP 200 as readiness.** Rejected because it accepts a stale or static server that cannot build the STEP artifact.
5. **Mandatory checksum for every generic preview.** Rejected because it would block ordinary generated/source preview. Optional `--sha256` pins immutable consumers such as Kage before action.
6. **Viewer-only UI build.** Rejected because the required proof is an artifact in state `ready`, not only a reachable SPA.
7. **Checking in `__cadgen__` artifacts.** Rejected because they are generated cache, vary with runtime, and must not mutate the frozen migration closure.

## Risks and boundaries

- PID/PGID reuse remains a race after `lsof`; stable leader/listener generation tokens reduce it to a safe no-signal failure. Revalidate exact tokens immediately before TERM; never KILL.
- The Viewer API is installed-runtime behavior, not a stable Kage API; dynamic discovery/provenance capture plus contract tests localize any future version incompatibility.
- User-controlled path resolution is a security and correctness boundary. Validate containment and optional checksum before every external action; report deterministic rejection without probing port 3245.
- A successful preview proves only the viewer can parse/render the selected artifact. For Kage, that remains a historical imported STEP and proves no mechanism, print, slicer, fit, or physical behavior.
- Tailscale reachability is environment-dependent. Printing a deterministic HTTPS Tailscale Serve URL after local readiness is allowed; local URL readiness is required, while remote reachability is a warning/evidence result and never authorizes unsafe repair.
- The Viewer API and generated cache can become inconsistent with the SPA after runtime-cache removal. The page-shell probe is the focused regression boundary for that defect; artifact state alone is intentionally insufficient.
- A listener can be replaced between artifact-ready and URL output. Final equality with `CURRENT_TOKEN` is the required output guard; it is not enough that a different healthy Viewer now occupies the port.
