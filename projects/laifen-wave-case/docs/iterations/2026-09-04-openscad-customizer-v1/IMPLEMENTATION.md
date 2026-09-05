# OSC-02 implementation receipt

**Owner/role:** `/root/render_controls_impl_b`, OpenSCAD implementation.  
**Status:** repair 2 source, deterministic contract checks, and smooth CSG compilation PASS; mesh validation remains pending.  
**Frozen design input:** `inputs/MANIFEST.sha256`, SHA-256 `fe5b5ba5c69a19c67eff3e25e0884dbf187e2a65eaeb6dd9a6d03a6f4c89a5dd` (all five entries verified before editing).

## Delivered files

- `openscad/laifen_case_customizer_v1.scad` — self-contained Customizer source.
- `openscad/customizer_contract.py` — pure derivation and validation layer used by tests.
- `tests/test_openscad_customizer.py` — focused default, split round-trip, bounds, and source-contract tests.

The OpenSCAD source offers grouped controls for device/envelope, one canonical split source, thread, surface, exclusive drainage placement, and output selection. It provides true separate body and cap shells, an original helical male/female thread pair, a body-owned shoulder, internal cavities, seven-hole drain pattern, and constructive external chamfers on both closed ends. The surface choices are now exact-OD `smooth` and shallow crossing-helical-groove `diamond`; `minimum_wall` is an enforced constraint/readout rather than a false geometry driver. The default contract derives cavity 213 mm, engagement 6 mm, overlap 9 mm, body 144 mm, cap 84 mm, and closed length 219 mm while retaining OD39 and bores30/31.

## Repair 1

The female thread no longer uses a large clearance cylinder that swallows the helix. Its base void is `thread_root_radius + thread_clearance`, followed by a matching helical groove to the crest radius. Male and female active helices share the same 6 mm local interval, centered in the 9 mm overlap with 1.5 mm transition each side. The former subtractive closed-end body chamfer was removed; rotational outer profiles now construct both chamfers before cavity subtraction. The old sphere lattice was replaced with bounded crossing helical V-grooves, with 2 mm thread/end keepouts and a shared global phase.

## Repair 2

The cap root-clearance cylinder now spans the entire 9 mm closure overlap. The active female helical groove is separately placed only over the central 6 mm engagement interval, matching the body helix. A 0.4 mm 45-degree entry/elephant-foot relief widens only the mouth. Diamond skin now derives `groove_count` from `diamond_arc_pitch`, repeats both handed V-groove families around the circumference, uses the corrected per-repeat twist law, and derives phase from global Z; the cap receives `cap_close_z` as its global offset. The threaded-cap material guard is now 1.8 mm.

## Evidence

`uv run pytest projects/laifen-wave-case/tests/test_openscad_customizer.py -q` returned `5 passed`.

Using `/Volumes/OpenSCAD/OpenSCAD-2021.01.app/Contents/MacOS/OpenSCAD` with `surface_style="smooth"` compiled the body CSG in `0.37 s` and cap CSG in `0.28 s`, written only to `/tmp` as transient validation output.

`git diff --check` returned clean. SHA-256:

```text
774fd5c8e5be700a887bd7005f1212717bd4c4e86d8857f72c70bb2b31df0210  openscad/customizer_contract.py
7f5aa5a7adf854a6d23ba3c931e4ed4b4b8530dd48cfd12f32928b1cef743c89  openscad/laifen_case_customizer_v1.scad
a552de195421168fdc5b1270560e05a3e0b57bf93650f68d23ef5d25dac0c083  tests/test_openscad_customizer.py
```

## Limits / next action

The stable mounted OpenSCAD 2021.01 executable compiled smooth body/cap CSG, but no release STL was written. CLI STL manifold/bounds validation and default/change/reset snapshots were not run. No build123d source, reviewed STEP, slicer, printer, route, or continuity authority was modified. Independent critique and validation must inspect the exact source and run all four outputs before any printable claim.
