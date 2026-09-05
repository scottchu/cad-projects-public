# Container generator v1

This standalone build123d package is a source-organization refactor of the
immutable `cad/p1_r7_end_chamfer/` baseline. It copies the P1 R7 procedural
surface, thread, runout, end-trim, Boolean, datum, assembly, and placement laws;
it does not import that package at runtime and adds no geometry family.

`PARAMETER_SPECS` in `parameters.py` is the machine-readable registry. Create a
selected immutable `Parameters` record with `preset('laifen_wave_r7', ...)`,
then call `derive(parameters)` exactly once. Geometry builders accept only the
resulting frozen `Resolved` record.

From the repository root, run the cheap gates first and generate the four STEP
artifacts only after they pass:

```sh
uv run pytest projects/laifen-wave-case/tests/test_container_generator_v1_parameters.py projects/laifen-wave-case/tests/test_container_generator_v1_requirements.py -q
uv run python projects/laifen-wave-case/cad/container_generator_v1/generate.py
```

The four primary pairs are `body.step.py`/`body.step`,
`cap.step.py`/`cap.step`, `closed.step.py`/`closed.step`, and
`print_layout.step.py`/`print_layout.step`. No mesh output is part of this
package. STEP and physical acceptance remain separate.
