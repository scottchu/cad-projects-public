# OSW-19 handoff

**Status:** OSW-22 formal review **PASS for local smooth-only delivery**  
**Owners:** OSW-20 implementation; OSW-21 validation; OSW-22 formal review

The final reviewed candidate is:

```text
1ea3f28d3bbd0653bc71f5db7996be473e68d0950b7d9a68a138a2c3103dfd90  src/main.mjs
fabd153527ec6c1aa0d5be9008679c7e2147d4559049149d8084b60795ec3845  workers/openscad.worker.js
896e5e632fb82e05d682d91e0be3ee356b7b49fc2dd436b990d922ebd66b013c  tests/test_openscad_wasm_simulator.py
```

OSW-18 and OSW-21 together close every OSW-15 delivery blocker. Default smooth
assembled generation has real-browser mesh/native parity and exact download
identity. Compiler diagnostics carry the active job id and remain visible. A
safe real parser failure revokes download, clears the old mesh to the initial
empty canvas, and is followed by successful generation with a new identity.
The final validation receipt is
`d663489027ab93eb13d8e4392f15df94f7a822eb9042657e3908654e163c79f3`;
its evidence-manifest fingerprint is
`6b3129dba28ff221806243ac020a89263e1b702c6c8dd712f8a20c50b03b523f`.

See `FORMAL_REVIEW.md` for the final join. Diamond remains disabled and outside
acceptance. Local delivery PASS does not authorize route mutation, MakerWorld,
public hosting, upload, publication, slicing, printer action, or physical-fit
claims. Browser mesh, CAD/STEP, slicer/process, and physical acceptance remain
separate.

## OSW-23 local delivery

Private tailnet delivery is live at <https://mac-mini.duckbill-ionian.ts.net:8448/openscad-simulator/>. The exact Vite bundle was copied to `scratch/presentation/openscad-simulator/`; served aggregate is `71ef1860c7b284b712b018bb51b07850b2a16c2f7160d9ad66055f138cd8637a`. Loopback and tailnet index/assets passed HTTP checks; WASM was served as `application/wasm`. The actual in-app tailnet page generated and displayed the default assembled STL with identity prefix `58895df4a50f`. Delivery receipt is `DELIVERY.md` and delivery-evidence fingerprint is `44e9a88a7ff9578dcb965f739544594f9096e10324ed3be101b9b8a9f72613aa`. Existing routes/services were preserved.
