# IMP-GCS-01 implementation receipt

**Status:** candidate frozen for independent validation and critique; no delivery route was changed.

Repair 1 replaces attempt 1 after the validator/critic HOLD findings. Attempt-1 source/test bytes are retained in `scratch/generic-container-impl/attempt1-source/`. Repair 1 adds strict field-domain validation, suppresses all derived visual geometry when invalid, replaces hoop meshes with LineSegments brackets, and gives both existing piece groups closed-end visual discs.

Verified frozen input fingerprint: `aea717d84cc31b67b345ed9367f6c5ae72b2a370291aa55e75ce1662238574df`.

The isolated P2 R2 page stores canonical raw millimetre split `S`; percent is only a raw-number adapter with endpoint rounding containment. `deriveContainer()` implements dynamic `E`, `P`, `K`, feasibility, bore/wall and preset derivation. The renderer has exactly two global-Z clipped exterior BufferGeometry meshes meeting at one seam. Thread information is external rings plus a line marker, with the marker group attached to the lower piece in exploded view; it is never an opaque tube.

The interface exposes all schema controls, 1/2/3 turns, both required presets, semantic live state, errors/warnings, global-Z readouts, true-scale main relief and explicitly labelled detail magnifier. It makes no fabrication/fit/print claims.

Validation run:

- `node projects/laifen-wave-case/tests/test_generic_container_simulator.mjs` passed: presets, E/P, turns, H=261/311 percent endpoints, infeasibility, global-Z phase, pinned dependency and scene semantics.
- Root Python Playwright Chromium smoke passed at desktop and 412px phone widths: makeup preset, turns, exploded view and screenshots in `scratch/generic-container-impl/`.
- Local temporary HTTP served the page for smoke only. No static route/service was edited.

Known limit: this visual simulator has no actual thread solid or print/CAD evidence; downstream review must inspect the exact candidate manifest before delivery is considered.
