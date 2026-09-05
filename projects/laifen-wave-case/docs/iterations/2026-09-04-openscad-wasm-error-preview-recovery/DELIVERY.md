# OSW-23 local delivery receipt

**Status:** PASS for private tailnet delivery of the reviewed smooth-only simulator.

## Delivered surface

- URL: <https://mac-mini.duckbill-ionian.ts.net:8448/openscad-simulator/>
- Handler: `/openscad-simulator -> http://127.0.0.1:8972/openscad-simulator` on HTTPS 8448.
- Existing port 8972 server and every pre-existing Tailscale handler were preserved.
- This is Tailscale Serve within the tailnet. Funnel/public hosting and MakerWorld integration were not enabled.

## Candidate and build

- Main: `1ea3f28d3bbd0653bc71f5db7996be473e68d0950b7d9a68a138a2c3103dfd90`.
- Worker: `fabd153527ec6c1aa0d5be9008679c7e2147d4559049149d8084b60795ec3845`.
- Focused test: `896e5e632fb82e05d682d91e0be3ee356b7b49fc2dd436b990d922ebd66b013c`.
- Formal review: `405b1575681015b8fd5bf1b99207c8b0015a780feb15d6756c042677562457f7`.
- `npm --workspace laifen-wave-case run setup:openscad-wasm`: PASS.
- `npm --workspace laifen-wave-case run build:openscad-simulator`: PASS, Vite 6.4.3, 499 ms.
- Served bundle aggregate: `71ef1860c7b284b712b018bb51b07850b2a16c2f7160d9ad66055f138cd8637a`.

## Delivery verification

- Loopback and tailnet index: HTTP 200.
- Referenced JavaScript and CSS: HTTP 200.
- OpenSCAD WASM: HTTP 200, `application/wasm`, 9,603,115 bytes.
- Served files match the final Vite `dist/` byte-for-byte.
- On the actual in-app Tailscale surface, default assembled generation completed with identity prefix `58895df4a50f`, enabled the exact STL download, displayed the compiled mesh, and showed Manifold/NoError diagnostics.

## Acceptance boundary

The browser/WASM smooth body, cap, and assembled outputs passed independent mesh/native parity, stale/download identity, compiler-error recovery, mobile, network, and formal-review gates. Diamond remains disabled pending performance work. This receipt does not change the P1 R7 build123d/STEP authority and does not claim slicer, printability, fit, or physical acceptance. No printer action was taken.
