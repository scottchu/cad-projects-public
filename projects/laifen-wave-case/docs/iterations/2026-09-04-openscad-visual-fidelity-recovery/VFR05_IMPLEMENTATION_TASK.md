# VFR-05 implementation task

Status: ready after its implementation manifest is frozen.

Implement only the direct role-specific annular-solid architecture in `VFR05_ARCHITECTURE.md`. Replace global string-search indexing and full-height cavity/chamfer Booleans for positive-depth diamond body/cap with bounded template indexing, conforming n-2 triangulation, and direct closed boundaries that preserve the existing exterior field, inner bore, floor, shoulder, neck and cap cavity steps. Retain only the existing thread and drain operations identified by the architecture.

Exclusive writes: `openscad/laifen_case_customizer_v1.scad`, focused assertions in `tests/test_openscad_customizer.py` if necessary, new evidence under `scratch/vfr05-implementation/`, passing body/cap candidates under `openscad/generated_vfr05/`, and `VFR05_IMPLEMENTATION.md`. The Python oracle and all browser/UI/worker files are read-only. No continuity, prior artifact, CAD/STEP, slicer, Tailscale, public, or printer change.

Run the architecture timing probes first, then G1, G2, G3 body and cap in order. One implementation attempt plus one focused repair. A timeout consumes an attempt. Do not enable browser controls or run G4/G5 in this task. Stop on changed B field, threshold relaxation, topology/ligament/internal regression, or second timing failure.
