# OpenSCAD Customizer V1 handoff

**Status:** design frozen; implementation not started  
**Owner:** OSC-01  
**Inputs:** `inputs/MANIFEST.sha256`

Implementation may write only a new self-contained OpenSCAD package under a future `openscad/` namespace, its focused tests, CLI validation reports, and snapshots. It must not edit `cad/container_generator_v1/`, P1 R7 artifacts, preview routes, or project requirements. Implementers must preserve the canonical split mode, formulas, closure shoulder, phase law, drainage modes, and deferred feature list in `DESIGN.md`.

Required independent roles are implementation, critique, validation, and formal review. Acceptance requires deterministic assertions, round-trip tests, CLI STL manifold/bounds checks, snapshots for default/change/reset, and an explicit comparison against the frozen parameter contract. OpenSCAD is the editable customizer target; this handoff does not authorize slicer, printer, or physical claims.
