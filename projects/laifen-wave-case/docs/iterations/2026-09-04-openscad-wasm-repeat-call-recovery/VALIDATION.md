# OSW-14 independent validation receipt

**Verdict:** PASS for the frozen browser/WASM candidate.  This receipt makes no
claim about diamond generation, slicing, printing, or physical fit.

## Provenance

- Frozen manifest SHA-256: `dd111388da60cbdea439341c7fd7c264d506a2625c613df37e2bb3fee6a8859b`.
- Worker SHA-256: `74dca2b782b6ca858a715e4dd1814016863effc3a5572835891cf3aff5290c9e`.
- Focused test SHA-256: `049a71bc9a7f7c44ff87732771d06802cc3e6d55aca781a27479cdac809d72ff`.
- OpenSCAD source SHA-256: `b5db326716df1f5cbff7135440cacac3cf0e61a67d9b0229a6e99261fa859f0e`.

## Results

- `npm --workspace laifen-wave-case run setup:openscad-wasm`: PASS.
- `npm run build:openscad-simulator --workspace projects/laifen-wave-case`:
  PASS with Vite 6.4.3 in 511 ms.
- `uv run pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q`:
  PASS, four tests.
- Real Chromium against an isolated production build: cube preflight PASS;
  default smooth body PASS in 0.381 s; default smooth cap PASS in 0.303 s.
  Each compile used a fresh worker runtime and remained well below the 180 s
  limit.
- Backend diagnostics: both case compiles reported `Top level object is a 3D
  object (manifold)`, `Status: NoError`, genus 0, and zero CGAL cache bytes.
  No unknown-feature or fallback warning appeared.  This is positive evidence
  that `--backend=Manifold` was accepted.
- Browser body STL: 6,381,466 bytes, SHA-256
  `28e1cf21cba70b2c31d1dcbf11842fde9cb7bad71556b8c7fcd58c39260989e3`;
  watertight, winding-consistent, one component, bounds
  `[-19.5,-19.5,0]..[19.5,19.5,144]`, volume 68,998.661 mm3.
- Browser cap STL: 5,763,428 bytes, SHA-256
  `646efb49c116b47b49521872c0e35af724053f9fbaa619c412aca40009e0b7d0`;
  watertight, winding-consistent, one component, bounds
  `[-19.5,-19.5,0]..[19.5,19.5,84]`, volume 38,033.306 mm3.
- Native OpenSCAD comparison: exact bounds and extents matched.  Relative volume
  delta was `7.05e-7` for the body and `3.41e-6` for the cap.  Native meshes were
  also watertight, winding-consistent single components.
- Result/download identity: body and cap downloaded bytes exactly matched the
  in-memory result bytes and SHA-256.  Filenames embedded the full result
  identity.
- UI state gates: an edited parameter marked the result stale and revoked the
  link; reset restored the default value/output and left download disabled;
  cancellation terminated the active workers and revoked download; crafted
  diamond input was rejected before a worker was created.
- Preview: desktop body/cap and 390 px mobile screenshots visibly contain the
  compiled meshes.  The mobile document and body widths both remained 390 px,
  with canvas and download control visible.
- Network: every request stayed on `127.0.0.1`; all WASM responses were HTTP 200
  with `application/wasm`.  The isolated server was stopped and port 8768 had no
  listener after validation.

## Evidence and limits

Evidence is in `scratch/openscad-wasm-validation/repeat-call/`, bound by
`EVIDENCE.sha256`.  The harness's immediate pre-animation canvas byte comparison
returned false, while the later captured desktop and mobile screenshots visibly
show the generated models; this is a harness sampling limitation, not a missing
preview.  The only browser console messages were WebGL `ReadPixels` performance
warnings.  Physical acceptance remains open.
