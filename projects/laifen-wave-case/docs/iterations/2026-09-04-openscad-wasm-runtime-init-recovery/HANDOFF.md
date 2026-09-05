# OSW-09 runtime-init recovery handoff

**Status:** OSW-11 independent browser validation BLOCK  
**Owner:** OSW-10 implementation; validated independently by `/root/render_controls_validate_b`

Implement only `factory({noInitialRun: true, ...existingOptions})` in the worker and its focused assertion. Preserve the prior OSW-08 candidate and all UI, SCAD, routes, dependency bytes, and existing manifold/backend argv. Use the tiny-cube preflight before body/case generation, with hard timeout and compiler diagnostics.

Implemented only the factory option and focused assertion. Candidate worker SHA-256 is
`b6e9d9d845d301ec21f528509fcd9cd650a53b5fe7bd162950cc4bc699588397`;
focused test SHA-256 is
`cc3276cca8c2ea0b27134fc570b9c8efb4a790468425ebb79d229c5542e1fca6`.
OSW-11 proves that `noInitialRun:true` repairs module initialization: the real
cube command returns code 0 and reports 1,443 STL bytes in 17.7 ms. The same
module then rejects the smooth-body second `callMain` with
`program has already aborted!`; no case STL exists. Diagnostics also state
`Ignoring request to enable unknown feature 'manifold'`, so requested backend
provenance is unresolved. See `VALIDATION.md` and
`scratch/openscad-wasm-validation/runtime-init/`.

Reopen runtime design around the single-use Emscripten `callMain` lifecycle and
the unsupported feature flag. Keep body/cap, mesh parity, download identity,
mobile, slicer, printer, and physical claims blocked until one frozen candidate
passes the full real-browser chain.
