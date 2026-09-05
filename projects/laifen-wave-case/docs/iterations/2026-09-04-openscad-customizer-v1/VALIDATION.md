# OSC-04 independent validation receipt

**Owner/role:** `/root/render_controls_validate_b`, independent OpenSCAD CLI, mesh, and collision validator.  
**Verdict:** **BLOCK** — the parameter contract and changed smooth probe work, but the default body is not a printable manifold solid and the default diamond set exceeds the compile ceiling.  
**Frozen input:** `inputs/MANIFEST.sha256`, SHA-256 `fe5b5ba5c69a19c67eff3e25e0884dbf187e2a65eaeb6dd9a6d03a6f4c89a5dd`; all five entries passed `shasum -c` before validation.  
**Stable engine:** `/Volumes/OpenSCAD/OpenSCAD-2021.01.app/Contents/MacOS/OpenSCAD`, version `2021.01`.

## Candidate identity

The candidate source and implementation records match exactly:

```text
7f5aa5a7adf854a6d23ba3c931e4ed4b4b8530dd48cfd12f32928b1cef743c89  openscad/laifen_case_customizer_v1.scad
774fd5c8e5be700a887bd7005f1212717bd4c4e86d8857f72c70bb2b31df0210  openscad/customizer_contract.py
a552de195421168fdc5b1270560e05a3e0b57bf93650f68d23ef5d25dac0c083  tests/test_openscad_customizer.py
```

## Commands and results

The focused source/contract gate passed:

```text
uv run pytest projects/laifen-wave-case/tests/test_openscad_customizer.py -q
5 passed
```

All CLI exports used the stable mounted executable. The four selectors were exercised with commands of this form:

```text
/Volumes/OpenSCAD/OpenSCAD-2021.01.app/Contents/MacOS/OpenSCAD \
  -o /tmp/laifen-osc04.<run>/<case>-<style>-<mode>.stl \
  -D 'surface_style="<style>"' -D 'output_mode="<mode>"' \
  projects/laifen-wave-case/openscad/laifen_case_customizer_v1.scad
```

Default smooth completed: body `7.75 s`, cap `4.30 s`, assembled `18.36 s`, and print layout `16.19 s`. The changed probe used `device_length=60`, `axial_allowance=5`, `outer_diameter=50`, `body_bore=40`, `cap_bore=41`, `split_mode="distance"`, `split_distance_from_top=30`, `thread_pitch=2.5`, `thread_turns=1.5`, `drainage_mode="top"`, and `surface_style="smooth"`; body completed in `3.38 s`, cap in `7.42 s`, assembled in `15.77 s`, and print layout in `14.06 s`. All source assertions accepted that probe.

Default diamond body required `429.09 s` and cap `228.73 s`. Body alone exceeded the five-minute task ceiling. Diamond assembled was terminated at `253.90 s`; print layout was not started. The requested complete release STL family therefore was not generated. No STL was promoted into `openscad/generated_v1/`.

## Mesh evidence

`trimesh.load_mesh(..., process=True)` produced the full recorded measurements in `openscad/generated_v1/mesh-validation.json`.

| Output | Bounds / extents (mm) | Watertight | Components | Volume (mm3) | Result |
| --- | --- | --- | ---: | ---: | --- |
| default smooth body | `39 x 39 x 144` | no | 25 | 68998.830 | BLOCK |
| default smooth cap | `39 x 39 x 84` | yes | 1 | 38033.057 | pass |
| default smooth assembled | `39 x 39 x 219` | no | 27 | 107031.876 | BLOCK |
| default smooth print layout | `85 x 39 x 144` | no | 26 | 107031.877 | BLOCK |
| default diamond body | `39 x 39 x 144` | no | 25 | 66608.563 | BLOCK |
| default diamond cap | `39 x 39 x 84` | yes | 1 | 36747.743 | pass |
| changed smooth body | `50 x 50 x 47.75` | yes | 1 | 33845.679 | pass |
| changed smooth cap | `50 x 50 x 30` | yes | 1 | 22004.155 | pass |
| changed smooth print layout | `107 x 50 x 47.75` | yes | 2 | 55849.859 | pass |

The default body’s 25 disconnected/non-manifold components occur in both smooth and diamond exports, so the defect is not attributable only to the optional skin. OpenSCAD also reported `Simple: no`, multiple volumes, and “may not be a valid 2-manifold” for the default body-derived outputs. The short-wide probe demonstrates that the controls can derive and compile a different valid smooth body/cap pair, but it does not cure the default release candidate.

## Collision/contact and analytic budgets

Trimesh had no installed boolean backend. A separate temporary OpenSCAD wrapper evaluated the actual source solids at the closed datum:

```scad
intersection() {
    body_shell();
    translate([0, 0, cap_close_z]) cap_shell();
}
```

The resulting temporary intersection occupied `z=135..142.5 mm`, contained `0.000419 mm3`, was non-watertight, and split into 336 numerical/coincident fragments. This is below the `0.001 mm3` reporting threshold for meaningful bulk collision, but it is not evidence of clean thread clearance because the source body and intersection are non-manifold. The exact receipt is `openscad/generated_v1/collision-validation.json`.

The analytic contract is internally consistent:

- cavity `208 + 5 = 213 mm`
- active thread engagement `2 x 3 = 6 mm`
- closure overlap `6 + 3 = 9 mm`
- closed length `213 + 2 x 3 = 219 mm`
- body/cap heights `144 / 84 mm`, with cap close datum at `z=135 mm`
- device radial clearance for `D=29 mm`: body `(30-29)/2 = 0.5 mm/side`; cap `(31-29)/2 = 1.0 mm/side`
- total nominal end clearance `213-208 = 5 mm`, above the requested 3 mm minimum

The seven-hole selector is source-observable as one center plus six radial holes. Default `bottom` subtracts it from the body floor; the changed `top` probe subtracts it from the cap floor. This validates selection logic and generation only, not drainage performance.

## Visual evidence

The following 900 x 900 OpenSCAD snapshots were generated from the smooth candidate because the diamond release path was stopped:

- `openscad/generated_v1/default-smooth-assembled.png`
- `openscad/generated_v1/default-smooth-body.png`
- `openscad/generated_v1/default-smooth-cap.png`
- `openscad/generated_v1/default-smooth-print_layout.png`
- `openscad/generated_v1/default-smooth-section.png`

`openscad/generated_v1/VALIDATION_ARTIFACTS.sha256` binds the JSON and PNG evidence; its SHA-256 is `6f6e29fb4818fb645d826679deb424f71fd94b0282a934273bd3db94db4c692b`.

The assembled view shows the expected constant 39 mm outside diameter and mid-body seam. The print layout shows separate upright body/cap objects. The CGAL-rendered half section exposes the continuous cavity, the two end floors, and the seam/overlap region. These views are visual evidence only; they do not override the manifold failure.

## Status boundaries and next action

- **Source/math:** PASS for the frozen contract and changed-parameter derivation.
- **OpenSCAD selection/compilation:** PASS for all smooth selectors and the changed probe; BLOCK for the complete default diamond family due runtime ceiling.
- **Written mesh:** BLOCK because the default body, assembled, and print layout are non-watertight multi-component meshes.
- **Collision/contact:** no meaningful bulk overlap measured, but BLOCK for acceptance because the participating body/intersection topology is non-manifold.
- **Slicing and physical acceptance:** not tested. The earlier printed build123d case does not accept this separate OpenSCAD candidate.

Repair the default body so the male thread and shell export as one watertight component, then repeat the four smooth selectors before re-benchmarking a reduced-cost diamond implementation. Release STLs remain withheld until those gates pass.
