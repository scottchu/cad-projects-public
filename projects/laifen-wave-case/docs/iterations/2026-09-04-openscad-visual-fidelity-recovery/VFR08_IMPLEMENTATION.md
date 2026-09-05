# VFR-08 implementation receipt

Status: **candidate generated; implementation evidence only**. This receipt does
not approve the candidate or replace independent critique, validation, or formal
review.

The frozen implementation input manifest was verified at SHA-256
`810506d1f3611a135ddbefdc5a37bda4957ec116d25d8934af83306aff9b8e38` (10/10
entries). The source baseline in that manifest was
`48b4ac84dc0cf4b8274200e9e2e13f145cfc01a5f721f975c37d1166c91ebd31`.

## Scoped changes

`openscad/laifen_case_customizer_v1.scad` contains exactly the prescribed
functional repair: both cylinders in `drain_pattern(h)` now use `center=false`
and the two existing caller translations remain unchanged; `print_layout()`
keeps the body placement and rotates only the cap with
`translate([-outer_diameter/2-3.5,0,cap_height]) rotate([180,0,0])`. Assembly
and standalone cap transforms remain unchanged. Source SHA-256 after the edit:
`ade77d3fcff4d5ba1c659838b4f9d24245584f0570834453b6e8c2b778047841`.

Focused source regressions were added in
`tests/test_vfr08_functional_repair.py` (SHA-256
`a7297933430d0e2f2135ff8c5a3ecde2fd573cff1ae90ef042d140bb66f96fa6`). The
command below passed 17 tests, including the existing customizer and WASM
simulator suites:

```text
uv run pytest projects/laifen-wave-case/tests/test_vfr08_functional_repair.py projects/laifen-wave-case/tests/test_openscad_customizer.py projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py
17 passed in 0.11s
```

## Generated evidence

Using the pinned `preview/openscad-wasm-simulator/vendor/openscad.js` and
`openscad.wasm`, the existing `scratch/vfr04-implementation/run-wasm-export.mjs`
runner generated 12 standalone meshes (diamond/smooth × none/bottom/top ×
body/cap), 2 print-layout meshes, and 1 depth-zero diamond body witness under
`scratch/vfr08-implementation/`. No browser, worker, service, slicer, STEP,
or printer path was changed.

`mesh-analysis.json` was produced by `analyze_meshes.py` using `trimesh` from
the root uv environment. All 15 meshes are one positive-volume watertight
component per standalone part, or two components for each layout; every
reported edge has incidence 2 and zero degenerate faces. Selected drained
pieces have seven distinct drain apertures and Euler characteristic -12:
smooth/diamond body-bottom and smooth/diamond cap-top all report `euler=-12`
and eight entities in a horizontal mid-floor section (one outer contour plus
seven drain contours). Unselected pieces report Euler 2. The selected body
floor cutter interval is `[-0.1,3.1]`; the selected cap interval is `[80.9,84.1]`.

The default layout meshes have bounds X `[-42.5,42.5]`, Y approximately
`[-19.5,19.5]`, Z `[0,144]`, with component bounds body `[3.5,42.5]` and cap
`[-42.5,-3.5]` and cap max Z `84`; this is the required 7 mm envelope gap.
The cap's local closed end maps to Z=0 and its local open rim maps to Z=84.
The depth-zero diamond body is byte-identical to the smooth bottom body in
the generated run, supporting the prescribed equivalence witness.

The complete scratch file/hash inventory is in
`scratch/vfr08-implementation/hashes.sha256`; mesh topology and dimensions are
in `mesh-analysis.json`.

## Boundary and next action

This is one implementation candidate with no repair cycle used. The evidence
does not establish support-free slicing, physical drainage, fit, strength,
thread wear, or user-facing browser visibility. Route this exact source and
scratch candidate to distinct independent critic and validator roles, then to
formal review. Any defect requiring changes outside the two prescribed masks
must reopen the VFR-08 contract.

## Focused record repair

The unused VFR-08 focused repair cycle corrected findings M1/L1 from the
independent validation record. The impossible self-entry was removed from
`scratch/vfr08-implementation/hashes.sha256`; no SCAD, test, mesh, browser,
service, or geometry file was touched. From the worktree root,

```text
shasum -a 256 -c projects/laifen-wave-case/scratch/vfr08-implementation/hashes.sha256
33/33 entries OK
```

The implementation receipt now records the verified focused-test hash
`a7297933430d0e2f2135ff8c5a3ecde2fd573cff1ae90ef042d140bb66f96fa6`.
Post-repair hashes are:

```text
sha256(hashes.sha256) = 09c35ffd92d87a1034fa70cc5cd03b6dcd5d6fb5fb1729db69ca1bc695793e20
```

The inventory digest is recorded after repair. This receipt deliberately omits
its own digest because a self-referential file hash cannot be stable.
