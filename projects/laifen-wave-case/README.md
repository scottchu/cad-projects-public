# Laifen Wave case and OpenSCAD container customizer

The current editable model is the parametric OpenSCAD source at
[`openscad/laifen_case_customizer_v1.scad`](openscad/laifen_case_customizer_v1.scad).
Its private browser customizer is live at
<https://mac-mini.duckbill-ionian.ts.net:8448/openscad-simulator/>. The browser
compiles that source with OpenSCAD WASM, previews the resulting mesh, and can
download an STL. Basic dimensions, the middle split, thread geometry, drains,
chamfer and the implemented surface controls come from the same parameter
schema. Diamond remains disabled in the public controls while its cancellation
and detailed browser geometry gates are unresolved.

The Laifen defaults preserve the user-confirmed width contract: 39 mm crest
outer diameter with 30/31 mm body/cap bores. Relationship B uses separate body
and cap pieces, one shared seam-centred phase, the N33 valley-derived pattern,
and a 0.18 crest plateau. Selected drainage is seven real holes at either the
top or bottom, and print layout places both openings upward.

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

Run the 55 focused **FRESH-CLONE-RELEVANT** source, WASM and retained-input checks with:

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

LC-VAL-02 recorded 55 fresh-clone-relevant tests and the two local-fixture-only
tests passing in the existing worktree; it did not execute a clean clone or
install. This is source, browser and written geometry evidence. Actual Safari use, Diamond browser completion, native CAD
reconstruction, slicing, thread fit, drainage flow, strength and physical
acceptance remain open. P1 R7 and the earlier P2 R3 simulator records remain
historical evidence under [`docs/iterations/`](docs/iterations/).
