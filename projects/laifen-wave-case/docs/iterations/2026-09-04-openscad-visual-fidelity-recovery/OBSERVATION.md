# Observation

Iteration: `2026-09-04-openscad-visual-fidelity-recovery`

## Evidence received

- The live OpenSCAD WASM route works and can produce a preview/downloadable result.
- The supplied screenshot does not resemble the printed/reference Laifen case: it reads as a plain, smooth, fused-looking cylinder rather than a component-aware case with the expected diamond/texture and seam.
- The screenshot includes raw red localization diagnostics in the user-facing surface.
- The user explicitly wants to continue the OpenSCAD WASM approach.
- The target mobile interaction is a fixed or sticky canvas at the top, independently scrollable parameters below, and an easy-to-reach sticky `Generate` action.

## Source-level hypotheses to verify

These are hypotheses for the benchmark and intent gate, not accepted causes:

- `groove_count` uses crest radius `N34`.
- Preserved `R7` uses valley radius `N33` and plateau `0.18`.
- The texture leaves a broad smooth collar: the body stops 2 mm before the seam and the cap begins 11 mm above the seam.

The values above must be checked against the read-only current diamond manifold before implementation. They do not authorize changing production source.

## Evidence boundary

This record describes visual and interaction evidence only. It does not establish geometric correctness, printability, physical assembly, or acceptance of any implementation. No MakerWorld/public release, printer action, or production registration is in scope.

## Open questions for VFR-02/VFR-03

- Which existing current-diamond manifold geometry and parameters are authoritative?
- Which seam and diamond relationships must be visible in a cheap 2D gate for the user to pass intent?
- Which diagnostics are localization warnings versus real errors, and what accessible wording should each retain?

