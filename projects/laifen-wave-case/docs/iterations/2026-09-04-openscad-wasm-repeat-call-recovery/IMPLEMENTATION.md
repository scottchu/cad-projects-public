# OSW-13 repeat-call implementation receipt

Verified frozen input-manifest SHA-256:
`dd111388da60cbdea439341c7fd7c264d506a2625c613df37e2bb3fee6a8859b`.

The worker now caches only the ESM factory import. `engine()` invokes that
factory with `noInitialRun:true` for each CLI call, giving the cube probe and
the case compile separate runtimes. It removes only obsolete
`--enable=manifold`; `--backend=Manifold`, diagnostics, input-first argv,
identity, and all UI/SCAD behavior remain unchanged.

Commands actually run:

```text
uv run pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
# PASS: 4 passed
npm run build:openscad-simulator --workspace projects/laifen-wave-case
# PASS: Vite build in 524 ms
git diff --check -- worker + focused test
# PASS
```

Candidate hashes:

```text
74dca2b782b6ca858a715e4dd1814016863effc3a5572835891cf3aff5290c9e workers/openscad.worker.js
049a71bc9a7f7c44ff87732771d06802cc3e6d55aca781a27479cdac809d72ff tests/test_openscad_wasm_simulator.py
```

No browser validation, UI/source/route/dependency/CAD output changes, or
physical claim was made. Real cube plus smooth body/cap/assembled validation,
backend-diagnostic capture, mesh parity, and stale/timeout delivery evidence
remain independent gates.
