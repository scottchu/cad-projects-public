# OSW-22 final independent review

**Owner/role:** `/root/openscad_wasm_formal_review`, distinct formal reviewer  
**Verdict:** **PASS for local smooth-only delivery**

## Provenance join

The reviewed files match the assigned fingerprints:

```text
57a3aec931bca2ca55ebfb94755d9f34526f18eb5b3cbc43bde46113a7f82be1  inputs/MANIFEST.sha256
1ea3f28d3bbd0653bc71f5db7996be473e68d0950b7d9a68a138a2c3103dfd90  src/main.mjs
fabd153527ec6c1aa0d5be9008679c7e2147d4559049149d8084b60795ec3845  workers/openscad.worker.js
896e5e632fb82e05d682d91e0be3ee356b7b49fc2dd436b990d922ebd66b013c  tests/test_openscad_wasm_simulator.py
d663489027ab93eb13d8e4392f15df94f7a822eb9042657e3908654e163c79f3  VALIDATION.md
6b3129dba28ff221806243ac020a89263e1b702c6c8dd712f8a20c50b03b523f  scratch/openscad-wasm-validation/error-preview-recovery/EVIDENCE.sha256
```

All 12 entries in the OSW-21 evidence manifest verify. Focused review reruns
also passed:

```text
uv run pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
# 4 passed
npm run build:openscad-simulator --workspace projects/laifen-wave-case
# PASS, Vite 6.4.3, 520 ms
```

## Prior blocker closure

- **Assembled output:** OSW-18 produced the default smooth assembled STL in a
  real Chromium run. It is watertight and winding-consistent, has exact
  `39 x 39 x 219 mm` bounds, and matches native bounds/extents with relative
  volume delta `7.62e-7`. In-memory and downloaded bytes match at SHA-256
  `84eb922bea02774772f388a62d564c20d1c799447411f818199e061714ec6f64`.
- **Compiler error and recovery:** OSW-21 repeats the current-candidate sequence
  valid assembled -> safe real parser error -> valid assembled recovery. The
  error is visible, download is disabled with no href, and the later request
  completes with a new identity.
- **Visible diagnostics:** the unchanged OSW-17 worker includes the active job
  id on every compiler log. OSW-21 records job id 2 on every error-run log and
  error event, and the browser screenshot shows the parser diagnostics in the
  application.
- **Stale preview disposal:** `stop()` now calls the existing idempotent
  `disposeMesh()` path, which removes the scene object and disposes its geometry
  and material. Generation start, error, cancellation, supersession, reset, and
  timeout all use that path. The real error canvas differs from the prior
  assembled canvas and exactly matches the initial empty canvas; recovery then
  installs one new mesh.

Visual review of the bound assembled-success, compiler-error, and
recovery-success screenshots agrees with the structured evidence: success
shows the current mesh and diagnostics, error shows an empty viewer with the
failure state and diagnostics, and recovery shows a newly generated mesh.

## Disposition and limits

No P1 or higher finding remains against the two recovery contracts. The exact
candidate is sufficient for local static delivery. Backend diagnostics identify
the Manifold result without the obsolete unknown-feature warning, and all
recorded requests stay on `127.0.0.1` with correct WASM MIME.

This PASS is smooth-only. Diamond remains disabled, labelled pending
optimization, and rejected before worker creation. This review does not approve
MakerWorld integration, public hosting, private-route mutation, upload,
publication, slicing, printer action, or physical fit. Browser runtime and mesh
transport pass for the reviewed local candidate; CAD/STEP, slicer/process, and
physical acceptance remain separate states.
