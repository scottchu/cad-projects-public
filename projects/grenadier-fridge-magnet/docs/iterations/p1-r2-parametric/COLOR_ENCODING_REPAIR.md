# P2-D3 — GLB color encoding repair

## Defect and authority
Independent critique reports deep-blue plate rendered cyan despite approved deep-blue palette. Root inspected exporter: raw palette sRGB bytes passed to vertex colors, while glTF COLOR_0 is a linear multiplier. This is an export representation defect; source palette and geometry remain approved intent. Geometry-passing connected candidate is preserved; its screen color acceptance is blocked. Root supplied official technical evidence: https://threejs.org/manual/en/color-management.html and Khronos glTF2 COLOR_0 linear multiplier semantics. No physical filament-color inference is made.

## Frozen repair
Keep PALETTE bytes unchanged. At the GLB export boundary convert every RGB component from normalized sRGB c to linear L exactly once: L=c/12.92 for c<=0.04045; otherwise L=((c+0.055)/1.055)^2.4. Apply to all five visible classes and black backing. Alpha stays unchanged. Do not apply an additional conversion if using a library API that already accepts sRGB and converts to linear internally; inspect written GLB to prove one conversion. Never alter original palette to compensate for an incorrect renderer.

Prefer FLOAT32 linear COLOR_0 accessors, or per-part constant glTF material baseColorFactor floating-point linear RGB with neutral white/no COLOR_0 multiplier. Constant material route must use one class color per named part and remove conflicting vertex-color multiplication. Preserve appearance intent of opacity and material properties. If exporter only permits normalized UINT8 linear color, explicitly quantify inverse-sRGB channel error for EACH actual palette color and document quantization; do not call that exact-byte fidelity. Do not silently accept substantial shadow/blue error to save implementation effort; float path is preferred.

Inverse transfer: c=12.92L for L<=0.0031308; otherwise c=1.055*L^(1/2.4)-0.055. Test every actual palette RGB plus endpoint values0/1; floating result after inverse must match normalized source within1e-6, and rounded8-bit output must equal original palette bytes. This test checks encoding, not lighting or physical printing.

## Per-object delta and output boundary
Allowed: export color representation and focused color tests. Forbidden: vertex positions, triangle indices, winding/topology, height parameters, geometry memberships/part identities, scene transforms, original PNG/SVG/palette, semantic masks or backing mask. No slicing/printing/network changes. Archive current source and preserve connected GLB originals before writing exporter repair. Use new export namespace p1-r2-color-corrected and new candidate manifest; historical connected candidate remains reviewable.

## Acceptance
Decode actual GLB color accessors/material factors independently and prove expected linear palette exactly once; verify unchanged geometry buffer data, primitive memberships and node transforms against connected candidate (serialization offsets may differ). Inspect fresh front/oblique render: original plate remains deep blue and pale glass distinct, with known viewer color management. Record deterministic color evidence separately from lighting-dependent screenshots and physical filament color. No need to rerun unrelated geometry construction if unchanged buffers are proven.

## Role and handoff
P2-D3 owner /root/parametric_magnet_design, export contract only,60second timebox, no CAD/export code. P2-I3 source/export repair depends on this frozen manifest; distinct independent critique/validation must check new candidate. This reopens color representation after geometry repair, not another topology attempt or artwork change. No user size/color-choice gate is needed.
