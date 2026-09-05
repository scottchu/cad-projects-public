# VFR-08 implementation task

Implement only `VFR08_FUNCTIONAL_REPAIR_DESIGN.md`: shared drain cutters become
non-centered with the prescribed caller extents, and only `print_layout` rotates
the cap open-end-up at the prescribed placement. Add focused regressions and
regenerate exact body/cap/print-layout evidence under
`scratch/vfr08-implementation/`; write `VFR08_IMPLEMENTATION.md`.

Exclusive writes: authoritative SCAD, focused OpenSCAD tests, new VFR-08 scratch
evidence and receipt. Browser/UI/worker/vendor, prior evidence, continuity,
STEP/slicer/services/printer remain read only. One candidate plus one focused
repair. Preserve all VFR-07 B pattern/source geometry outside these masks.
Implementer does not approve its own result.
