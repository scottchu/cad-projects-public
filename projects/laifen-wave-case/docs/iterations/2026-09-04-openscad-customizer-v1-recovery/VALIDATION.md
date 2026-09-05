# OSC-07 independent recovery validation

**Owner/role:** `/root/render_controls_validate_b`, independent OpenSCAD and mesh validator.  
**Recovery input manifest:** `22e3b909bf3a3fbac3d1f85bdd2056ea95c3a3c584d9904a9c9a1bf2b0f9aa3b`.  
**Smooth candidate:** **PASS**.  
**Diamond texture:** **PERFORMANCE BLOCK** under the required 60-second body/cap limits.  
**Physical acceptance:** not tested.

## Provenance

The recovery manifest verified all frozen pre-repair inputs. As expected, `shasum -c` identifies only the repaired source and updated regression test as changed from that baseline. Their current identities and the implementation receipt agree:

```text
b5db326716df1f5cbff7135440cacac3cf0e61a67d9b0229a6e99261fa859f0e  openscad/laifen_case_customizer_v1.scad
4e1eea50a2e1fa71b1f420abf2693f2eb96c4ce51d9f4467a39086681dbb5f4e  tests/test_openscad_customizer.py
774fd5c8e5be700a887bd7005f1212717bd4c4e86d8857f72c70bb2b31df0210  openscad/customizer_contract.py
1bee085787d7cca85ac898873a34a94675a289bb2109ce1d0b43b0230df35709  recovery/IMPLEMENTATION.md
```

The engine was `/Volumes/OpenSCAD/OpenSCAD-2021.01.app/Contents/MacOS/OpenSCAD`, version `2021.01`.

## Source and compilation gates

```text
uv run pytest projects/laifen-wave-case/tests/test_openscad_customizer.py -q
...... [100%]
```

All four default smooth selectors compiled successfully: body `7.52 s`, cap `4.03 s`, assembled `15.64 s`, and print layout `14.77 s`. OpenSCAD reported `Simple: yes` for each.

A changed short-wide probe also compiled all four selectors with `device_length=60`, `axial_allowance=5`, `outer_diameter=50`, `body_bore=40`, `cap_bore=41`, `split_distance_from_top=30`, `thread_pitch=2.5`, `thread_turns=1.5`, `drainage_mode="top"`, and `surface_style="smooth"`. Times were body `3.24 s`, cap `7.24 s`, assembled `14.84 s`, and print layout `13.12 s`.

## Smooth mesh result

`trimesh.load_mesh(..., process=True)` confirms:

| Output | Extents (mm) | Watertight | Components | Positive volume | Result |
| --- | --- | --- | ---: | --- | --- |
| default body | `39 x 39 x 144` | yes | 1 | yes, `68998.710 mm3` | PASS |
| default cap | `39 x 39 x 84` | yes | 1 | yes, `38033.176 mm3` | PASS |
| default assembled | `39 x 39 x 219` | yes | 3 closed oriented shells | yes, `107031.885 mm3` | PASS as assembly review output |
| default print layout | `85 x 39 x 144` | yes | exactly 2 | both positive volumes | PASS |
| changed body | `50 x 50 x 47.75` | yes | 1 | yes | PASS |
| changed cap | `50 x 50 x 30` | yes | 1 | yes | PASS |
| changed print layout | `107 x 50 x 47.75` | yes | exactly 2 | both positive volumes | PASS |

The assembled STL contains the intentionally coincident closed body and cap as separate moving parts and nested oriented cavity shells. Every component is closed; the body and cap selectors and print layout provide the actual printable one-part/two-part outputs. Full component details are recorded in `openscad/generated_v1_recovery/mesh-validation.json`.

## Closed-state contact

An OpenSCAD CGAL intersection of the actual source body and cap translated to `cap_close_z` completed in `15.42 s`. Its bounds are `[-19.5,-19.5,135]..[19.5,19.5,135]` and its volume is exactly `0.0 mm3`. The intersection collapses to the `z=135` shoulder-stop plane. This is intended coincident shoulder contact, not volumetric collision. The planar STL is necessarily non-manifold; `collision-validation.json` records that boundary separately from the valid body/cap solids.

## Contract checks

- usable cavity: `208 + 5 = 213 mm`
- closed outside length: `213 + 2 x 3 = 219 mm`
- active thread: `2 mm pitch x 3 turns = 6 mm`
- closure overlap: `6 + 3 = 9 mm`
- body/cap heights: `144 / 84 mm`; cap close datum: `z=135 mm`
- body radial device clearance: `(30-29)/2 = 0.5 mm/side`
- cap radial device clearance: `(31-29)/2 = 1.0 mm/side`
- nominal total end clearance: `213-208 = 5 mm`
- default drains: bottom only, seven holes (center plus six radial)
- changed probe drains: top only
- both closed ends use the `end_chamfer=1.2 mm` constructive profile; source asserts keep it below the `3 mm` floor

## Diamond performance boundary

The required hard benchmarks used independent 60-second subprocess timeouts. Default diamond body timed out at `60.0621 s`; cap timed out at `60.0338 s`. Neither wrote an STL. This is a texture performance block and does not invalidate the passing smooth candidate.

## Evidence and limits

`openscad/generated_v1_recovery/` contains JSON mesh/compile/collision receipts and 900 x 900 smooth PNGs for assembled, body, cap, and print layout. No release STL, route, slicer artifact, printer action, or physical acceptance was created. Smooth source/CAD validation passes; users must still export/slice the exact chosen parameters and physically validate thread cycling and fit.

`openscad/generated_v1_recovery/VALIDATION_ARTIFACTS.sha256` binds the evidence and has SHA-256 `6e6d01b20f2b29fba73ca4097322f0e880e3c6d970325eb0e528d11a209737f3`.
