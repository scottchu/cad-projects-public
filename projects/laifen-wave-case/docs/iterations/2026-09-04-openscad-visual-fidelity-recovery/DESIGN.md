# Design

## Decision record

The recovery proceeds through the staged DAG in `BRIEF.md`. The current screenshot is treated as evidence of a visual-fidelity gap and diagnostic presentation defect. It is not evidence that the user supplied the wrong dimensions, and it is not permission to redesign before the intent gate.

## Architecture constraints

1. OpenSCAD WASM owns case solids, component boundaries, texture, seams, and all downloadable closed geometry.
2. The viewer consumes the generated OpenSCAD result. Any seam visible only for display is a separate presentation layer and must be tagged display-only, component-aware, and non-exporting.
3. Three.js presentation code must not displace, warp, or synthesize the case surface to make a screenshot look plausible.
4. The manifold benchmark must measure the current diamond pattern before changing `groove_count`, radii, plateau, or seam offsets. The `N34`/`N33` and collar values are explicitly pending verification.
5. Mobile layout uses a sticky canvas region, an independently scrolling parameter region, and a sticky Generate control whose focus and keyboard behavior remain usable.
6. Toasts expose status through an accessible live region and focus-safe dismissal. Raw logs are hidden in collapsed details and remain available for debugging.
7. Localization diagnostics are classified. Non-fatal localization notices are filtered or demoted in the primary UI; genuine generation/geometry errors retain severity, visible text, and raw details.

## Required evidence by stage

- VFR-02: read-only measurements, source/artifact parity, and immutable fingerprint.
- VFR-03: a small 2D gate that teaches fixed versus adjustable relationships and captures an explicit user pass/fail.
- VFR-04: focused pure-math and geometry checks, component/collision and seam checks, source-to-export parity, accessible UI checks, and a visual review on the actual delivery surface.

## Scope controls

No production file is changed by this documentation step. No public upload, MakerWorld publication, printer command, or registration is allowed by this iteration. If VFR-02 or VFR-03 fails, downstream 3D implementation stops until the contract is reopened and refrozen.

