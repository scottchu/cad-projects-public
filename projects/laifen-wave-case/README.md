# Laifen Wave case and OpenSCAD container customizer

The editable model is the parametric OpenSCAD source at
[`openscad/laifen_case_customizer_v1.scad`](openscad/laifen_case_customizer_v1.scad).
The private browser customizer is live at
<https://mac-mini.duckbill-ionian.ts.net:8453/> with Smooth, Diamond, Ribs,
Rings and Spiral. Each textured pattern shows its own remembered controls
immediately below the selector. Top/Bottom drains remain independent, with
adjustable hole count. Generate previews the actual compiled mesh; Download
exports only the current STL.

The delivered R2 candidate passed independent source/state, written-mesh,
Chromium desktop/mobile and formal review gates. All six live files match the
reviewed build, and a fresh live generated/downloaded STL matches exactly.
See the [pattern-families delivery](docs/iterations/2026-09-06-pattern-families/DELIVERY.md)
and [handoff](docs/iterations/2026-09-06-pattern-families/HANDOFF.md).
Native Safari/iPhone, slicer and physical acceptance remain separate.

The Laifen defaults preserve the user-confirmed width contract: 39 mm crest
outer diameter with 30/31 mm body/cap bores. Relationship B uses separate body
and cap pieces, one shared seam-centred phase, the N33 valley-derived pattern,
and a 0.18 crest plateau for default Diamond. Drain count defaults to seven
per selected end; Top and Bottom can be selected independently, including both
or neither. Print layout places both openings upward.

The immutable printable STEP authority remains
[`cad/p1_r7_end_chamfer/print_layout.step`](cad/p1_r7_end_chamfer/print_layout.step),
SHA-256 `80fd95845b51da5266883614f9bf8eff60793a24d5c39b7321c9c6cb16d477a4`.
Git keeps this two-part print layout and the four distinct
`container_generator_v1` comparison releases. The redundant R7 body, cap and
closed-assembly STEP copies remain local and reproducible from tracked R7
source, but are excluded from Git to keep the first import below the review
payload threshold.

From the repository root, reproduce the browser dependencies and build with:

```sh
npm run setup:openscad-wasm --workspace laifen-wave-case
npm run build:openscad-simulator --workspace laifen-wave-case
```

Run the retained **FRESH-CLONE-RELEVANT** source, WASM and input checks with
(the historical LC-VAL-02 run contained 55 checks):

```sh
uv run --frozen --package laifen-wave-case pytest -q -p no:cacheprovider \
  projects/laifen-wave-case/tests/test_openscad_customizer.py \
  projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py \
  projects/laifen-wave-case/tests/test_vfr08_functional_repair.py \
  projects/laifen-wave-case/tests/test_container_generator_v1_parameters.py \
  projects/laifen-wave-case/tests/test_container_generator_v1_requirements.py \
  projects/laifen-wave-case/tests/test_container_generator_v1_preview_parameters.py \
  projects/laifen-wave-case/tests/test_container_generator_v1_step_equivalence.py::test_step_hashes_are_recorded_without_relaxing_geometry_or_scope
```

Two additional **LOCAL-FIXTURE-ONLY** written STEP regression checks consume
excluded local R7 body, cap and closed STEP fixtures. Run them only in a worktree
that still has those fixtures:

```sh
uv run --frozen --package laifen-wave-case pytest -q -p no:cacheprovider \
  projects/laifen-wave-case/tests/test_container_generator_v1_source_equivalence.py::test_frozen_p1_r7_remains_hash_clean_and_new_package_is_standalone \
  projects/laifen-wave-case/tests/test_container_generator_v1_step_equivalence.py::test_four_written_steps_are_valid_and_baseline_equivalent
```

Historical LC-VAL-02 recorded 55 fresh-clone-relevant tests and the two local-fixture-only
tests passing in the existing worktree; it did not execute a clean clone or
install. Later Smooth/Diamond browser and written-mesh gates are recorded in
the surface-pattern iteration; the earlier pending Diamond-browser status is
superseded. Native Safari/iPhone acceptance for the new families, native CAD
reconstruction, slicing, thread fit, drainage flow, strength and physical
acceptance remain separate. P1 R7 and earlier P2 R3 simulator records remain
historical evidence under [`docs/iterations/`](docs/iterations/).


### Historical desktop customizer gate (2026-09-05)

The desktop iteration introduced inside diameter, inside
height, body-wall thickness, and top/bottom thickness. Drain placement remains
visible; proportional lid height and export shape are under Container options.
The compiled STL is shown in 3D or a display-only Cutaway. Generate is explicit
after edits; Cancel, Reset dimensions, Reset view, and Download STL are distinct.
The first visit generates the unchanged smooth preset once. The existing screw
geometry needs a minimum advertised body wall of 4 mm; thinner everyday walls
require a separate mechanics change. That UI gate did not establish a physically
validated CAD release or change the deployed service at that time.

From the repository root:

```sh
node --test projects/laifen-wave-case/tests/node/desktop-customizer.test.mjs
uv run pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
npm run build:openscad-simulator --workspace laifen-wave-case
```

See `docs/iterations/2026-09-05-desktop-customizer/` for the design contract,
implementation receipt and independent acceptance status.

Historical artifact limitation: independent browser checks of the D39/H60/W4/T4 example
found four degenerate seam faces in its closed-container STL. Its separately
generated body, lid and print-layout samples were watertight. Source was
unchanged at that gate; this did not establish printability or physical acceptance. The
minimum advertised wall is 4 mm; 3 mm walls are unsupported. See the iteration's
[validation record](docs/iterations/2026-09-05-desktop-customizer/VALIDATION.md).
