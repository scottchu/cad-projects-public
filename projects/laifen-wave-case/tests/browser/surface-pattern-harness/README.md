# Surface-pattern late-result browser harness

This validator-only page reuses the frozen candidate's actual controller,
lifecycle, schema, SCAD, worker, dependency lock, and pinned OpenSCAD runtime.
Its worker wrapper forwards normal events and holds only a genuine completed
STL result. The visible sequence delivers that exact result after actual
Cancel, then repeats it across a newer-job ownership boundary. PASS requires
unchanged status, render, Blob, and download state for stale results and exact
held/view/Blob SHA-256 identity for the accepted newest result.

From the repository root, verify the durable harness inputs and generate an
isolated Candidate 03 copy:

```sh
shasum -a 256 -c projects/laifen-wave-case/tests/browser/surface-pattern-harness/HARNESS_INPUTS-02.sha256
repo_root="$PWD"
node projects/laifen-wave-case/tests/browser/surface-pattern-harness/generate.mjs \
  "$repo_root" \
  "$repo_root/projects/laifen-wave-case/docs/iterations/2026-09-06-surface-pattern/inputs/candidate-03.sha256" \
  412b5e389a85dbaa7ad730870f496639d8dcd2e2129de733b4da1ba1e031fc63 \
  /tmp/laifen-surface-pattern-harness
cd /tmp/laifen-surface-pattern-harness
"$repo_root/.venv/bin/python3" -m http.server 8461 --bind 127.0.0.1
```

Open
`http://127.0.0.1:8461/projects/laifen-wave-case/preview/openscad-wasm-simulator/index.html`.
Confirm the page names manifest `412b5e38...`, then follow its numbered buttons.
Wait for each genuine-result PASS before clicking the next button. This manual
browser sequence is required; syntax or unit tests do not establish it. In the
supersession sequence, wait for Worker 3 genuine result PASS before clicking
**Deliver job 2 late**. The harness then snapshots the quiescent newest-job
state immediately before delivering the held older result and compares it with
the state immediately afterward.

The generated directory is disposable and must stay outside the repository.
Do not copy the vendor, meshes, logs, generated page, or screenshots back into
the project.
