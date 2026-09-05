# OSW-02 repair-1 implementation receipt

**Status:** implementation candidate; focused deterministic checks and Vite build pass.

## Frozen input

Verified `inputs/MANIFEST.sha256` SHA-256:
`3cfed46383d2881ef0f2e6718e54dd2ab92cb41b2c69c8c6a712d6d21c68bfdf`.
The current authoritative SCAD SHA-256 is
`b5db326716df1f5cbff7135440cacac3cf0e61a67d9b0229a6e99261fa859f0e`.

## Repair scope

The module worker now obtains the Emscripten factory only through ESM default
import and verifies it is callable.  The UI immediately revokes Download on
control edits, reset, cancellation, preflight/compiler error, and stale state;
it enables the exact same byte buffer only after the current job id, result
identity, SCAD hash, and canonical dependency-lock fingerprint all match.
Old object URLs and Three resources are disposed.  STL bounds frame the camera;
a WebGL failure leaves generate/download controls usable.

Browser V1 rejects every non-smooth snapshot before worker creation. Diamond and
its four parameters remain visible, disabled, and labelled `pending optimization`.
The worker receives only the smooth job allowlist. Setup now verifies downloaded
and extracted staging assets before a vendor-to-backup then staging-to-vendor
rename sequence, so partial staging output is never usable as the vendor cache.

The reported `minimum_wall` critique was false: the recovered SCAD already uses
`minimum_wall` in its OD assertion. No CAD or SCAD change was made.

## Commands and results

```text
uv run pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
# PASS: 4 passed
npm run build:openscad-simulator --workspace projects/laifen-wave-case
# PASS: Vite 6.4.3, built in 498 ms
git diff --check -- projects/laifen-wave-case/preview/openscad-wasm-simulator projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py
# PASS
```

Vite emitted the expected local worker, locked OpenSCAD JS/WASM, CSS, and app
bundle. Its standard >500 kB bundle warning remains; no browser smoke was run.

## Candidate hashes

```text
e6aa6734b2d2efae5a896c3d1c5185cb00ef50eb043edd3cbfa7ba512611f113 src/main.mjs
fe77d55cc91f9e526559b307a70db3fa03aefe35a84c4c87cf5d4ee42f242f1a src/schema.mjs
ff49e6211a94b6b99c8eebf6a1b3cfc544bd438650cddb3b94919056189e3907 workers/openscad.worker.js
fd444d299420d6599040198fe507a76bcc062aadc80913c59912838a2a7d03b1 tests/test_openscad_wasm_simulator.py
```

## Limits

Real browser/WASM compilation, native mesh parity, mobile/accessibility capture,
CSP/network verification, private route delivery, slicer, and physical checks
remain for independent validation. No route, SCAD/CAD/STEP, or release asset was
changed by this repair.
