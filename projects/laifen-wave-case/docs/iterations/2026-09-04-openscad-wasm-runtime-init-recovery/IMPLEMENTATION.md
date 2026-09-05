# OSW-10 runtime-init implementation receipt

Verified frozen input-manifest SHA-256:
`9a70964c5a4751e594b580e87965305695809c643efc0c4cd264727ea3524235`.

The sole runtime change is `noInitialRun:true` in the official Emscripten
factory options. It preserves the ESM import, `locateFile`, stdout/stderr
handlers, Manifold argv, job identity, and all non-worker artifacts. A focused
source regression requires the option adjacent to the existing loader options.

Commands actually run:

```text
uv run pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
# PASS: 4 passed
npm run build:openscad-simulator --workspace projects/laifen-wave-case
# PASS: Vite build in 517 ms
git diff --check -- worker + focused test
# PASS
```

Candidate hashes:

```text
b6e9d9d845d301ec21f528509fcd9cd650a53b5fe7bd162950cc4bc699588397 workers/openscad.worker.js
cc3276cca8c2ea0b27134fc570b9c8efb4a790468425ebb79d229c5542e1fca6 tests/test_openscad_wasm_simulator.py
```

No real-browser cube/body/cap/assembled smoke, mesh parity, served-byte,
route, slicer, printer, or physical validation was performed. Those remain
independent gates; module initialization alone is not acceptance.
