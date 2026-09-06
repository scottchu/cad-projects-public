# DR-VAL-01 independent validation

Status: **PASS** for candidate DR-C1. Native Safari interaction remains a separate root-owned gate.

## Provenance and scope

- Frozen baseline: commit `7b9c960f1a2ef1e0b211c3cbd3f9c0c3a0ab42ef`.
- Baseline manifest SHA-256: `16128041328e85ec25bfbaf6c90e0dc937b310ebc9306745a98390c9fcaa8845`.
- Candidate manifest: `inputs/candidate-01.sha256`, SHA-256 `4a716d71c154bcba1264d556946613ec615c50217bba6331e36da8e9f1c67389`; every listed path passed `shasum -a 256 -c` before validation.
- Candidate SCAD SHA-256: `cf0983e84e738be87e31462c903afcf02646915cc1e4a9e8641b8edce05b5393`.
- Validator owned only this receipt and temporary `/tmp/drain-val-01` probes. No source, test, service, or browser state was changed.

## Evidence

### Build and focused contracts

- `npm run build:openscad-simulator --workspace laifen-wave-case`: PASS; Vite built 18 modules in 574 ms.
- `node --test projects/laifen-wave-case/tests/node/compact-controller.test.mjs projects/laifen-wave-case/tests/node/desktop-customizer.test.mjs`: PASS, 27/27. This covers all four checkbox mappings, no automatic compile on edit, active-work invalidation, invalid-draft preservation, and Bottom-only reset/default.
- `uv run pytest projects/laifen-wave-case/tests/test_openscad_customizer.py projects/laifen-wave-case/tests/test_vfr08_functional_repair.py projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py`: PASS, 16/16.
- `node projects/laifen-wave-case/openscad/run_math_probe.mjs`: PASS; all seven existing `VFR04_*` compiled witnesses were present.

The installed official OpenSCAD WASM matches the pinned lock:

- `openscad.js`: 124,567 bytes, SHA-256 `904a47f29e63afb597bedef747da3b457d8ea17cc793c462c6c8b444e918a62e`.
- `openscad.wasm`: 9,603,115 bytes, SHA-256 `f72ce246c02c0e501990837102be383326b153fd761774ebfacce5c80c5ecf26`.

### Actual compiled endpoint geometry

A temporary Node runner used that pinned factory and `--backend=Manifold` to compile the smooth browser preset as separate body and cap STLs for `none`, `top`, `bottom`, and `both`. It parsed actual STL triangles, audited every undirected mesh edge, calculated signed volumes, and performed three-direction point-in-solid tests at the center plus all six ring-hole centers halfway through each closed end.

| Drain mode | Body seven points | Body volume loss (mm3) | Cap seven points | Cap volume loss (mm3) |
| --- | --- | ---: | --- | ---: |
| `none` | all solid | 0 | all solid | 0 |
| `top` | all solid | 0 | all void | 147.839849 |
| `bottom` | all void | 148.334297 | all solid | 0 |
| `both` | all void | 148.334297 | all void | 147.839849 |

The expected faceted-cylinder losses were 148.334297 mm3 for the 3.00 mm body floor and 147.839849 mm3 for the unchanged cap's effective 2.99 mm floor (`cap` cavity overlap is 0.01 mm). Every result matched within 0.08 mm3. All eight outputs had zero non-two-count edges after 1e-5 mm vertex quantization, positive volume, and the expected bounds. `both/body` was canonically identical to `bottom/body`; `both/cap` was canonically identical to `top/cap`.

The SCAD diff adds `both` to exactly the four established drain conditions: smooth body, smooth cap, diamond body, and diamond cap. `closed_assembly()` and `print_layout()` continue to call those same body and cap modules, so the checked cutters propagate to assembled and layout output without a second implementation path. Diamond geometry was not recompiled because this bounded change only extends the existing cutter conditions and the requested validation preset was smooth.

### Default geometry parity

The frozen baseline and candidate were each compiled as the complete assembled smooth browser preset with Bottom-only drains. Their STL outputs were byte-identical:

- SHA-256: `b1b9db18e21cafed5237afb90e57831b72246c6ac2e4b4c88f736738fd0cf169`.
- 39,904 triangles; volume 106,957.799815 mm3; bounds `[-19.5,-19.5,0]` to `[19.5,19.5,219]`; zero non-two-count edges.
- The authoritative SCAD and browser source defaults remain `bottom`; the source default surface remains `diamond`.

## Requirement coverage and limits

- DR-01: source exposes a `Drain holes` fieldset with independently labeled native Top and Bottom checkboxes; `.check-row` has a 44 px minimum height. Focused interaction tests pass. Native Safari appearance and touch-row behavior are root-owned evidence.
- DR-02: PASS for authoritative smooth body/cap geometry in all four states, including simultaneous end voids for `both`; shared-module routing and the four condition-only SCAD edits cover assembled, print-layout, and diamond paths.
- DR-03: PASS in focused Node and Python contracts. All validators accept exactly `none/top/bottom/both`; edits invalidate active work without compiling; reset is Bottom-only; invalid dimension errors survive checkbox edits.
- DR-04: PASS for compiled actual-end openings and exact frozen-baseline smooth-default parity. No slicer or physical acceptance was claimed.

No blocking findings. The stylesheet was expanded from minified form while adding the checkbox-row rules, which enlarges the textual diff; the build and focused behavior checks found no related functional regression.

## Root-owned live browser and delivery evidence

Root validated the frozen DR-C1 build in native Safari without worker browser interaction:

- At 1440 x 900, the initial state was Top off and Bottom on. Root independently exercised `both`, Top-only, and `none`; checkbox edits marked the preview stale and never compiled automatically.
- Explicit Generate from `both` completed with `Preview up to date`. Reset restored Top off and Bottom on, cleared the mesh, and did not auto-generate.
- At 390 x 700, both 44 px checkbox rows remained readable and reachable by scrolling; explicit Generate from `both` completed.
- Evidence images: `/tmp/container-drain-validation/{desktop-default,desktop-both,desktop-top,desktop-none,desktop-both-generated,reset-bottom,mobile-both-generated}.png`.
- A later attempt to add an invalid-dimension browser check stopped before any action because CUA reported that the user had changed Safari. Invalid-draft preservation is therefore supported by the 27-test Node gate above, with no additional browser claim.

Safari downloaded `/Users/scottchu/Downloads/container-assembled-3d4c353de77c.stl`: 12,810,713 bytes, SHA-256 `e56f4a377bbe7dc74c7b1ad9b1c77e386daa751293bdee667ad6be7722656058`. Independent identity recomputation from the candidate SCAD bytes, stable pinned dependency lock, and `{...BROWSER_PRESET, drainage_mode: "both"}` produced full identity `3d4c353de77c4d654e59ccfcf453439d1c31a4cbce5b9189c8e5146bfb995052`; its filename prefix and assembled output mode exactly match the download.

Root also compared all six files served by the existing private 8453 preview against the rebuilt local `dist` files using bounded `curl --fail --silent --show-error --max-time 20` requests. Every response was byte-identical:

| Built/served asset | Bytes | SHA-256 |
| --- | ---: | --- |
| `index.html` | 6,933 | `323e96e77fe8fc14f7e6077fc11df9142e614e168673a73fe61b6214ef211a97` |
| `index-Bmck2Ywj.css` | 5,322 | `1e46f000a5298380ca3a0b123e6ac90ba0cfc512bb8cd914c3c49de8b2225a9e` |
| `index-C0Hjou4v.js` | 540,118 | `c2f52289f176d8dfb904251a1bffc025870efae2c78c609e82d77350f8508457` |
| `openscad-CutNEzGH.js` | 124,567 | `904a47f29e63afb597bedef747da3b457d8ea17cc793c462c6c8b444e918a62e` |
| `openscad-DIKIGOy4.wasm` | 9,603,115 | `f72ce246c02c0e501990837102be383326b153fd761774ebfacce5c80c5ecf26` |
| `openscad.worker-Csx1v_-i.js` | 1,823 | `cf543214d381e56ac230d6853810786ae70c52977d408e64695db595574fd46e` |
