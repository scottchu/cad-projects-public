# OSW-04 independent real-browser validation

**Owner/role:** `/root/render_controls_validate_b`, independent browser/WASM validator.  
**Frozen input manifest:** `3cfed46383d2881ef0f2e6718e54dd2ab92cb41b2c69c8c6a712d6d21c68bfdf`; every entry passed `shasum -c`.  
**Verdict:** **BLOCK** — the official browser engine loads, but a default smooth body did not complete within the bounded real-browser attempts, so no STL/download/preview acceptance chain exists.

## Candidate identity

The inspected files match the implementation receipt:

```text
e6aa6734b2d2efae5a896c3d1c5185cb00ef50eb043edd3cbfa7ba512611f113  src/main.mjs
fe77d55cc91f9e526559b307a70db3fa03aefe35a84c4c87cf5d4ee42f242f1a  src/schema.mjs
ff49e6211a94b6b99c8eebf6a1b3cfc544bd438650cddb3b94919056189e3907  workers/openscad.worker.js
fd444d299420d6599040198fe507a76bcc062aadc80913c59912838a2a7d03b1  tests/test_openscad_wasm_simulator.py
b5db326716df1f5cbff7135440cacac3cf0e61a67d9b0229a6e99261fa859f0e  openscad/laifen_case_customizer_v1.scad
```

## Deterministic gates

`npm --workspace laifen-wave-case run setup:openscad-wasm` completed with the pinned vendor cache. `npm --workspace laifen-wave-case run build:openscad-simulator` passed with Vite 6.4.3 in `514 ms`, emitting the local worker, `openscad-CutNEzGH.js`, and `openscad-DIKIGOy4.wasm`. The standard bundle-size warning was non-blocking.

```text
uv run pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
.... [100%]
```

These checks establish source structure, dependency integrity, preflight behavior, and build output. They do not execute the real compiler.

## Real-browser result

An isolated Python loopback server served only the built `dist` directory at `http://127.0.0.1:8764/`. Headless Chromium loaded the page, built application assets, module worker, official OpenSCAD JavaScript, and 9.6 MB WASM file successfully; the server recorded HTTP 200 requests for each local asset.

The validator selected `output_mode="body"` with the browser's smooth preset and clicked **Generate STL**. The first attempt remained short of `Complete` until Playwright's `180000 ms` timeout. It produced no STL. A single focused retry widened only the wait window; the job was still compiling after approximately 160 seconds when the parent directed the validator to stop and finalize. It also produced no STL. No further retries were made.

The access log for both attempts contained only `127.0.0.1` requests to `/`, the built CSS/main bundle, local worker, local OpenSCAD JS, and local WASM. Because the browser sequence did not reach its final evidence write, this is supporting server evidence rather than the planned complete request assertion. The WASM response MIME capture was likewise not retained.

## Unreached browser acceptance gates

The body compile is a blocking dependency for all result-specific checks. Therefore the following remain unproven in a real browser:

- smooth body and cap completion from the authoritative `.scad`
- visible parsed STL preview and camera bounds framing
- exact-byte browser download, body/cap trimesh inspection, and native hash/bounds comparison
- stale download revocation after parameter edits and reset recovery
- diamond rejection before worker creation
- cancellation, supersession, compiler/preflight error recovery
- mobile 390 x 844 overflow/layout behavior
- complete external-request assertion and WASM MIME evidence

Static implementation tests cover many of these states, but they cannot replace the missing real-worker result.

## Cleanup and status boundary

The isolated port `8764` was stopped and verified to have no listener. No Tailscale route, existing service, application source, SCAD/CAD, STL release, continuity record, slicer artifact, printer, or physical acceptance state was changed.

Evidence lives under `scratch/openscad-wasm-validation/`: the exact Playwright validator, command list, and structured failure record. `EVIDENCE.sha256` binds those files and has SHA-256 `96dad614ab7ed16d73a51cee526d80b9d9cce6a9f7d687c93e67193ac08ef0f3`. The next action is to profile or reduce the browser smooth compile workload before repeating one cold body and one warm cap result; interaction and mobile gates should resume only after the first real STL completes.
