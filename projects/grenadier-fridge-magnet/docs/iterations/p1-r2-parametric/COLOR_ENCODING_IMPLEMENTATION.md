# P2-I3 export color repair receipt

Status: source/export repair complete; independent color and fresh visual review pending. Verified8 frozen input paths against ae01ca5e353d385e4ed5f7b73b38772cb2acb5b1672e2a57df1b6a27c9183861 before writes. Previous source/tests archived byte-for-byte under historical-connected-source. Connected artifact bytes remain untouched.

New candidate1f66199dfbd9b35780aee9cb93af0179277805085e9ac1bc61bbf2c9999b2fc0 binds18 paths in color-corrected-candidate-manifest.json. Per-part PBR baseColorFactor now receives floating linear RGB converted once from unchanged source sRGB palette; conflicting COLOR_0 attribute removed at the source exporter callback. Unreferenced old color buffer remains legal glTF; entire BIN chunk is unchanged. Default glTF opaque, metallic1, roughness1 and single-sided properties preserved explicitly. No renderer compensation or palette change.

Rationale supplied in frozen design: Three.js color-management documentation https://threejs.org/manual/en/color-management.html explains linear working-space vertex colors; Khronos glTF2 material semantics https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html specify linear baseColorFactor and COLOR_0 multipliers. Source code uses standard sRGB transfer with threshold0.04045 and inverse threshold0.0031308. Floating JSON material factors avoid UINT8 linear quantization, especially on dark blue/black.

Commands from repository root:
- `uv run pytest projects/grenadier-fridge-magnet/tests/test_parametric_magnet.py -q -k glb_linear` →1 passed. Covers all five actual colors, endpoints0/1, inverse tolerance1e-6, exact recovered8-bit palette, and absent double multiplication.
- `uv run python projects/grenadier-fridge-magnet/src/parametric_magnet.py --glb-only` →source regenerated only GLBs and version-local mesh report into p1-r2-color-corrected; no new STLs.
- Focused root-env decoder extracted each GLB JSON/BIN chunk. Entire binary chunks compared equal to connected originals. Nodes, accessors, bufferViews, named mesh identities, indices/POSITION accessor references and primitive memberships compared equal. Every actual material factor matched expected linear RGB to1e-15 and inverted/rounded to original palette bytes. Details: GLB/p1-r2-color-corrected/color-parity-report.json. These comparisons establish unchanged geometry, including backing bridges/heights/transforms; unrelated geometry regressions were not repeated.

New GLB paths/hashes:
- GLB/p1-r2-color-corrected/flat.glb — bb0b2d54dba75530fbcce067229393cea5534d065251a18a5c6c7c60b8c34e77
- GLB/p1-r2-color-corrected/relief.glb — 143d67d0365a8b7fd9fc7e2425ee925cf59b24527607b98e8f768880b3966638

Root and preview owner received immutable files/hashes for fresh front/oblique inspection. Encoding evidence does not prove appearance under arbitrary lighting, physical filament color, strength, slicing or text survival. No STEP/BREP, new manufacturing claims, printer or network action. Source and test namespace released; next action independent V3/C3 against this exact candidate.
