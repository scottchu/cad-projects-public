# OSW-09 runtime-init recovery design contract

## Single allowed change

Change the worker's factory invocation to include `noInitialRun: true` (alongside the existing options). Add a focused source/test assertion that the property is present and true. Do not change `callMain`, argv ordering, `--enable=manifold --backend=Manifold`, parameter-to-`-D` mapping, timeout, cancellation, stale-job identity, UI, SCAD, dependency lock, generated meshes, routes, or STEP.

## Acceptance gates

The real module must initialize without `Requested GUI mode` or abort diagnostics. Before any case generation, run the same tiny-cube real-WASM smoke with a hard timeout and capture stdout/stderr, exit status, elapsed time, and backend diagnostics. Then run the existing default smooth body/cap/assembled gates using the exact worker path. Compare native/WASM mesh validity, watertightness, component count, bounds, volume, and parameter identity within the pre-existing tolerances. A cube pass alone is insufficient. Any initialization abort, timeout, diagnostic mismatch, stale result, or mesh parity failure is BLOCK.

This recovery does not approve diamond generation, CAD/source changes, STEP changes, slicer/process readiness, printer action, or physical acceptance. Freeze the one-line source delta, focused test, cube/body reports, and served-byte evidence for independent review.
