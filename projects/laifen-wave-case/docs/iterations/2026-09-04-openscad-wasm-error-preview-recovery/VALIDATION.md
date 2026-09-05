# OSW-21 independent error-preview validation

**Verdict:** PASS for the frozen focused recovery candidate. This inherits the
unchanged OSW-18 assembled/native mesh evidence and makes no slicer, printer, or
physical-fit claim.

## Provenance

- Input manifest: `57a3aec931bca2ca55ebfb94755d9f34526f18eb5b3cbc43bde46113a7f82be1`.
- Main module: `1ea3f28d3bbd0653bc71f5db7996be473e68d0950b7d9a68a138a2c3103dfd90`.
- Focused test: `896e5e632fb82e05d682d91e0be3ee356b7b49fc2dd436b990d922ebd66b013c`.
- Unchanged worker: `fabd153527ec6c1aa0d5be9008679c7e2147d4559049149d8084b60795ec3845`.

## Evidence

- Setup and production build passed; Vite 6.4.3 built in 511 ms. The focused
  Python suite passed four tests, including the idempotent `disposeMesh()` path,
  scene removal, and geometry/material disposal assertions.
- Real Chromium assembled generation passed in 1.548 s with identity
  `58895df4a50f984b3ba0c0c6c5398b47dfc2e53c93dcddb362020412ddcc93e4`.
  The 12,163,932-byte in-memory STL and download matched exactly at SHA-256
  `84eb922bea02774772f388a62d564c20d1c799447411f818199e061714ec6f64`.
- The safe real parser failure displayed `Compiler error; no STL is available.`
  and visible parser diagnostics. All compiler log and error events carried the
  matching active job id 2. Download was disabled and its href removed.
- The error canvas differed from the prior successful mesh and was byte-identical
  to the initial empty canvas, proving no old mesh remained visible. The harness
  does not expose live WebGL resource counts; source plus focused tests prove the
  geometry/material disposal calls, while the canvas gate proves scene removal.
- A subsequent valid request completed and installed a new mesh with new identity
  `05f4547efdf51955ea95430a8ee91aaa6d502ddf631175f6406d0c5c2b7340b3`.
- Every browser request remained on `127.0.0.1`; every WASM response was HTTP 200
  `application/wasm`. The only console output was WebGL `ReadPixels` performance
  warnings. The isolated server was stopped and port 8770 had no listener.

Evidence is under `scratch/openscad-wasm-validation/error-preview-recovery/`
and bound by `EVIDENCE.sha256`.
