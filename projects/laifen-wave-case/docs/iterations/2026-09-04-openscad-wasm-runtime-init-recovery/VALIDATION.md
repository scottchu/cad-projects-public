# OSW-11 independent real-browser/WASM validation

**Owner/role:** `/root/render_controls_validate_b`, independent runtime validator.  
**Frozen recovery manifest:** `9a70964c5a4751e594b580e87965305695809c643efc0c4cd264727ea3524235`.  
**Candidate:** worker `b6e9d9d845d301ec21f528509fcd9cd650a53b5fe7bd162950cc4bc699588397`, test `cc3276cca8c2ea0b27134fc570b9c8efb4a790468425ebb79d229c5542e1fca6`.  
**Verdict:** **BLOCK** — initialization is repaired and the internal cube command succeeds, but the same module aborts on the required case compile; requested Manifold enablement is also reported unknown.

## Provenance and deterministic gates

The manifest verifies the exact pre-repair worker/test baseline, dependency lock, prior validation, and authoritative SCAD. The current changed worker/test hashes match OSW-10, and the SCAD remains `b5db326716df1f5cbff7135440cacac3cf0e61a67d9b0229a6e99261fa859f0e`.

`npm --workspace laifen-wave-case run setup:openscad-wasm` passed. `npm --workspace laifen-wave-case run build:openscad-simulator` passed with Vite 6.4.3 in `517 ms`. The focused suite passed:

```text
uv run pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
.... [100%]
```

## Real-browser result

The built app was served only from `http://127.0.0.1:8767/`. Headless Chromium loaded the page, module worker, official OpenSCAD JavaScript, and official 9.6 MB WASM. Every observed request used `127.0.0.1`; the WASM response was HTTP 200 with `Content-Type: application/wasm`.

`noInitialRun:true` prevents the former empty-argument GUI auto-run. The worker's first explicit `callMain` completed the one-millimetre cube in `17.7 ms`, returned exit code `0`, logged a six-facet convex PolySet, and reported `1,443` STL bytes. This proves module initialization and a nonempty internal cube export. The worker sends only cube metadata, not the bytes, so independent watertight inspection of that cube is not available.

The same diagnostics also contain:

```text
WARNING: Ignoring request to enable unknown feature 'manifold'.
Could not initialize localization (application path is '/').
```

The localization warning did not prevent the cube. The unknown-feature warning means the requested Manifold enablement is not confirmed by this official WASM build and is a backend provenance mismatch under the recovery design.

Immediately after the successful probe, the worker posted the case `compiling` stage and called the same module again for the smooth body. It failed before rendering:

```text
program has already aborted!
```

The UI reached `Compiler error; no STL is available.` after `0.147 s` total. No case result identity, body bytes, blob, preview, download, or cap job existed.

## Dependency stop and remaining gates

The cube-before-case sequence executed, but the first case gate failed. Therefore the validator correctly stopped before cap generation, 180-second comparisons, trimesh/native parity, exact display/download identity, stale-download revocation, reset/cancel, diamond rejection, and mobile 390 px checks. None may be inferred from static tests.

No STL was available for mesh or native comparison. This is a runtime lifecycle failure: the official module handles the probe's first `callMain`, then rejects the second `callMain` in the same worker.

## Cleanup and next action

The isolated server was stopped and port `8767` has no listener. No application source, routes, CAD/SCAD, release STL, slicer artifact, printer action, or physical acceptance state changed.

Evidence under `scratch/openscad-wasm-validation/runtime-init/` includes the exact validator, full worker/network record, command list, and server access record. `EVIDENCE.sha256` binds those files and has SHA-256 `d8b4262c5ff640b1a072529a2efe849f569e75d814a1c9af1e24b9202ed2804c`. The next design must avoid two sequential `callMain` invocations on one aborted/terminated Emscripten runtime while preserving a real cube gate, and it must resolve the unsupported `manifold` feature diagnostic before backend parity can pass.
