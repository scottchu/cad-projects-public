# OSW-01 handoff

**Status:** design frozen; implementation not started.  
**Authority:** `BRIEF.md`, `DESIGN.md`, and `inputs/MANIFEST.sha256`.

The next task is OSW-02 implementation. It may create only the isolated
`preview/openscad-wasm-simulator/` app, its focused tests, a dependency lock, and
an implementation receipt inside this iteration. It must not edit the frozen
OpenSCAD/Python contracts, CAD/STEP artifacts, prior previews, routes, services,
project state, or this design contract.

The candidate source is the recovered SCAD
`b5db326716df1f5cbff7135440cacac3cf0e61a67d9b0229a6e99261fa859f0e`
with test `4e1eea50a2e1fa71b1f420abf2693f2eb96c4ce51d9f4467a39086681dbb5f4e`.
It inherits OSC-07 smooth PASS evidence `d4323bae…` and evidence manifest
`6e6d01b2…`. Browser V1 is smooth-only. Diamond controls are visible, disabled,
and labelled `pending optimization`; a diamond request must be rejected before
worker startup. Do not spend an implementation or validation retry compiling
diamond and do not create a visual substitute.

OSW-02 starts with the verified setup script for the official playground-pinned
`OpenSCAD-2025.03.25.wasm24456-WebAssembly-web.zip`: 2,947,329 bytes, SHA-256
`0968af31b9c9b3bba68d9031de1695ccae51c32231a1aab4ef27b18c86379f3b`.
It must not build OpenSCAD WASM or commit the ZIP or 9,603,115-byte
`openscad.wasm`. It stops before app code if the download, archive, members,
installed hashes, or license provenance cannot be verified against official
`openscad-playground` commit
`012111f06bb6d8dac2b8d30318512494d87d6932`. It also stops if the browser build
requires threading/cross-origin isolation, if the source copy is not
byte-identical, or if real WASM generation cannot preserve the exact
parameter/output job contract.

After OSW-02 freezes a candidate, distinct critic and validator owners inspect
the same fingerprint. The formal reviewer joins their receipts. Only then may a
distinct delivery owner add the isolated private `/openscad-simulator/` mapping.
No role in this chain may claim CAD, STEP, slicer, printability, fit, physical,
MakerWorld, public-hosting, or publication acceptance.

The first user-facing validation should be cheap and concrete: generate a wide,
short smooth container, move the seam once by distance and once by equivalent
percentage, then generate one-turn and two-turn thread cases. Explain which
piece is fixed, which input moves the seam, and that every result is a newly
compiled STL. Ask the user whether those four relationships match the intended
container. Also show the disabled diamond controls and explain that optimization
must pass a later performance gate before they can compile or download.
