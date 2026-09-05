# OSW-06 Manifold worker recovery receipt

Verified frozen manifest SHA-256:
`0123a62c15f2e173ac65ddebb8a95b6e6b4ac3df447cfc60068230fb874a17a0`.

The worker now invokes each real OpenSCAD compile with both
`--enable=manifold` and `--backend=Manifold`. Before every case compile it
writes and compiles `cube([1,1,1]);` through that exact backend argument set,
rejects nonzero/empty output, and posts backend, elapsed milliseconds, byte
count, and exit status for diagnostics. The permitted main-thread recovery adds
a 180000 ms timer tied to the assigned job id. On expiry it increments the id,
terminates the worker through `stop()`, revokes/disables Download, and labels
the stale result as timed out. `stop()` clears the timer on result, error,
cancellation, supersession, and reset; reset also supersedes an active id. No
schema, SCAD, CAD, route, or release asset changed.

Commands run:

```text
uv run pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
# PASS: 4 passed
npm run build:openscad-simulator --workspace projects/laifen-wave-case
# PASS: Vite build in 512 ms
git diff --check -- .../workers/openscad.worker.js .../test_openscad_wasm_simulator.py
# PASS
```

Hashes:

```text
16e2906186858596107527b091f555645e34ae5edf28b51beaa80e91e265d42d src/main.mjs
6938e8d9f1fdfdeff6606084c621db890263644d9b42ff6a649b8bfdac3070d4 workers/openscad.worker.js
40780e6ac959b91a0fa79639680d4c510703a8efe092907e9f6de931321a5f09 tests/test_openscad_wasm_simulator.py
```

No browser/WASM smoke was run in this implementation step. A real cube and
smooth-case browser run, timeout trace, backend diagnostics, mesh parity, and
served-byte checks remain independent validation gates.
