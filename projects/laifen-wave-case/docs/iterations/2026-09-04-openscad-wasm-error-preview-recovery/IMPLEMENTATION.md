# OSW-20 error-preview implementation receipt

Verified frozen input-manifest SHA-256:
`57a3aec931bca2ca55ebfb94755d9f34526f18eb5b3cbc43bde46113a7f82be1`.

`stop()` now invokes the existing idempotent `disposeMesh()` before it revokes
Download. Generation start, worker error, cancellation, supersession, reset,
and timeout already use `stop()`, so each clears the old scene object and
releases geometry/material before a new job or error state. A valid result then
creates one newly owned mesh after existing identity validation.

Commands run:

```text
uv run pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
# PASS: 4 passed
npm run build:openscad-simulator --workspace projects/laifen-wave-case
# PASS: Vite build in 520 ms
git diff --check -- main + focused test
# PASS
```

Hashes:

```text
1ea3f28d3bbd0653bc71f5db7996be473e68d0950b7d9a68a138a2c3103dfd90 src/main.mjs
896e5e632fb82e05d682d91e0be3ee356b7b49fc2dd436b990d922ebd66b013c tests/test_openscad_wasm_simulator.py
```

No real-browser error/recovery validation, mesh, route, slicer, printer, or
physical validation was run. Those remain separate gates.
