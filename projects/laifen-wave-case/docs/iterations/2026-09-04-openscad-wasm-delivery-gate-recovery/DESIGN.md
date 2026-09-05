# OSW-16 delivery-gate recovery design contract

## Allowed delta

The worker may add `id` to every compiler diagnostic/error `postMessage` and a focused test may assert that contract. No other worker behavior changes. Validation may use a safe crafted SCAD/argv solely to force a real compiler error, then verify recovery with a subsequent valid smooth request; the production SCAD and UI remain byte-unchanged.

## Required gates

Run locally with a hard 180-second timeout per request. First complete the real-WASM cube preflight, then default smooth body, cap, and assembled requests on fresh module instances. For assembled, verify nonempty watertight mesh, one expected connected result, bounds/volume, native parity, exact result/download identity, and visible success state. Trigger the crafted compiler error and verify the visible error includes the matching active job id, no stale download/preview is offered, and a later valid request succeeds with a new identity. Check reset, cancellation, supersession, and stale-result suppression remain intact.

Backend diagnostics must remain explicit and accepted; unknown-feature warnings or ambiguous fallback are BLOCK. Smooth is the sole generated surface. This evidence is local runtime/mesh delivery only and does not approve CAD/source geometry, STEP changes, slicer/process readiness, printer action, or physical acceptance.
