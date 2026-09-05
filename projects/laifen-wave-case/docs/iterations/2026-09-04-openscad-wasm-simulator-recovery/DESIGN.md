# OSW-05 recovery design contract

## Scoped change

Change only the worker's real-WASM argv from `--enable=manifold` to `--enable=manifold --backend=Manifold`. Preserve all existing parameter-to-`-D` mappings, output modes, stale-job identity, cancellation, UI labels, and served paths. Do not alter OpenSCAD source, SCAD geometry, generated meshes, CSS, routes, or STEP.

## Gates

Before body/cap/assembled generation, the worker must compile a tiny known-good cube through the same real WASM module and argv. Record stdout, stderr, exit status, elapsed time, backend diagnostics, and whether a valid nonempty watertight cube mesh was produced. Apply a hard timeout to the cube and every case job; timeout must cancel the job, suppress stale downloads/previews, and retain diagnostics without leaving a false success state.

The native/WASM gate compares the selected smooth output's mesh validity, component count, bounds, volume, and deterministic parameter identity against the native OpenSCAD CLI result within declared tessellation tolerances. A successful cube does not prove case geometry. The case gate must separately cover default smooth body, cap, and assembled outputs; diamond remains disabled or separately bounded until it compiles under the practical ceiling. Any unsupported backend flag, compiler diagnostic, timeout, non-manifold result, or parity failure is a BLOCK and must be recorded.

## Evidence

Freeze the exact worker argv, dependency lock, WASM asset identity, cube report, compiler diagnostics, case reports, mesh parity report, cancellation/timeout trace, and served-byte checks. Independent validation must inspect the same frozen candidate. Formal review remains a distinct join. No printer or physical acceptance is implied.
