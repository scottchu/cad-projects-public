# VFR-01U private delivery receipt

## Delivered surface

- Private route: <https://mac-mini.duckbill-ionian.ts.net:8448/openscad-simulator/>
- Served directory: `scratch/presentation/openscad-simulator/`
- Candidate manifest fingerprint: `9f01d5eca03a58263a7716c57f39979128520021a670f59ab960f8a6e2778ebd`.
- Served bytes: `DELIVERY_UI_BUNDLE.sha256`.
- Existing HTTPS 8448 route and loopback port 8972 service were retained; no Tailscale Serve reset, public Funnel, or new service was created.

## Exact-byte validation

The production `dist/` tree was copied to the existing served directory. All six served files match the built local bytes. HTTPS returned `200` for the HTML, JavaScript, CSS, worker, OpenSCAD runtime, and WASM; the WASM response remained `application/wasm` and `9,603,115` bytes.

## Delivery-surface interaction

The exact Tailscale route was exercised in Chromium with a temporary `390 x 844` mobile emulation and then restored to the normal viewport.

- Computed mobile layout: preview `position: sticky`; parameter form `overflow-y: auto`; action group `position: sticky`; raw diagnostic details closed.
- Invalid `outer_diameter=30`: status `OD must retain minimum wall`; toast `OD must retain minimum wall. Adjust that value and try again.`; focus moved to Dismiss; raw details stayed closed.
- Dismissal returned focus to Generate.
- Restored `outer_diameter=39`: `Complete 58895df4a50f`; download enabled; toast hidden; raw details closed.
- Raw diagnostics retained the known localization warning, used real line breaks, contained no literal backslash-n separators, and did not promote the warning into the primary status/toast surface.

## Acceptance boundary

VFR-01U is accepted for the private UI delivery only. It did not change OpenSCAD geometry, schema, worker protocol, output identity, or generated STL bytes. Diamond visual fidelity remains blocked on the VFR-03 intent gate. CAD/STEP, slicer, MakerWorld/public hosting, printer actions, and physical acceptance are unchanged and outside this receipt.
