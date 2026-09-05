# VFR-06 implementation task

Status: ready after `inputs/VFR06_IMPLEMENTATION_INPUTS.sha256` is frozen.

Task ID: VFR-06-I. Owner role: sole source implementation owner. Implement
only the periodic knot-lattice and edge-owned-clipping architecture in
`VFR06_ARCHITECTURE_DECISION.md`, following gates V06-0 through V06-3P in the
declared order. The recorded B relationship and every protected dimension,
operation, threshold and smooth-path byte range are immutable.

Exclusive writes:

- `openscad/laifen_case_customizer_v1.scad`
- focused implementation assertions in `tests/test_openscad_customizer.py`
  and, only if required, one new focused VFR-06 test file
- new implementation probes and evidence under `scratch/vfr06-implementation/`
- passing body/cap candidate outputs under `openscad/generated_vfr06/`
- `VFR06_IMPLEMENTATION.md`

Read only: the Python contract oracle; browser schema, main, worker, HTML/CSS,
vendor/runtime and lock files; all prior evidence/artifacts; continuity files;
build123d/STEP and slicer namespaces. Do not enable Diamond controls, deploy,
modify services, publish, slice, upload or print.

Run V06-0, V06-1, V06-1 boundary/annulus, V06-1T, V06-2, V06-3B0, V06-3B,
V06-3C and V06-3P sequentially. Production SCAD must emit the arrays inspected
by the proof gates. Keep one initial candidate attempt plus one focused repair
total. A timeout or failed candidate gate consumes an attempt. If a second
candidate failure occurs, restore the frozen source/tests, retain noncandidate
evidence, and record the browser OpenSCAD Diamond path blocked under the
0.025 mm / 60 s contracts. Do not renew the budget or change architecture.

The implementation receipt must include verified input fingerprint; changed
paths and hashes; exact commands/timings; source-emitted topology and accuracy
evidence; body/cap worker results; protected-region/smooth regression; and
remaining risks. The implementer cannot approve its own candidate.
