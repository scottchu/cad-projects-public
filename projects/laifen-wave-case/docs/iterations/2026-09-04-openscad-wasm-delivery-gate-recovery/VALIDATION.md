# OSW-18 independent delivery-gate validation

**Verdict:** BLOCK. The compiler and recovery path work, but a failed compile
continues to display the preceding mesh, violating the frozen no-stale-preview
gate. No application repair was made.

## Provenance

- Input manifest: `8f9eebed962dd85d2d4280df23c0f3c3b4150dad51773b38ab3ce432674d62f3`.
- Worker: `fabd153527ec6c1aa0d5be9008679c7e2147d4559049149d8084b60795ec3845`.
- Focused test: `ce4040064a4684eccd17abe42306aae39dfb1f74cca0d0917933715a0af2ceca`.

## Passing gates

- Setup/build passed; Vite 6.4.3 built in 501 ms. Focused Python tests passed,
  four tests.
- Real Chromium completed the cube preflight and default smooth assembled job
  in 1.514 s. In-app diagnostics visibly reported a top-level `manifold`,
  `Status: NoError`, genus 1, and zero CGAL cache bytes, with no backend warning.
- Browser assembled STL: 12,163,932 bytes, SHA-256
  `84eb922bea02774772f388a62d564c20d1c799447411f818199e061714ec6f64`;
  watertight, winding-consistent, bounds `[-19.5,-19.5,0]` to
  `[19.5,19.5,219]`, volume 107,031.967 mm3.
- Native parity had exact bounds/extents and relative volume delta `7.62e-7`.
  The three face-connected shells are one positive exterior plus two inward
  cavity boundaries; OpenSCAD reports one top-level manifold. Native body plus
  cap volume differs from assembled by only 0.000706 mm3, consistent with the
  intended shoulder contact and no material collision at mesh tolerance.
- In-memory result bytes and downloaded bytes/hashes matched exactly. The
  filename contains the full result identity
  `58895df4a50f984b3ba0c0c6c5398b47dfc2e53c93dcddb362020412ddcc93e4`.
- The safe injected parser error produced visible parser diagnostics and
  `OpenSCAD exited 1`. Every diagnostic and error event carried active job id 2.
  The app showed `Compiler error; no STL is available.`, removed the download
  href, and disabled download. A later valid request recovered successfully with
  new identity `05f4547efdf51955ea95430a8ee91aaa6d502ddf631175f6406d0c5c2b7340b3`.
- All requests remained on `127.0.0.1`; WASM responses were HTTP 200
  `application/wasm`. Port 8769 was stopped after validation.

## Blocking finding

**OSW18-B01 — stale preview remains after compiler failure (delivery BLOCK).**
The canvas screenshot bytes immediately before and after the real parser error
were identical. The previous successful assembled mesh therefore remains visibly
offered after the app states that no STL is available. Download revocation is
correct, but it does not satisfy the separate no-stale-preview requirement.

Evidence is under `scratch/openscad-wasm-validation/delivery-gate/` and bound by
`EVIDENCE.sha256`. This local runtime validation makes no slicer, printer, or
physical-fit claim.
