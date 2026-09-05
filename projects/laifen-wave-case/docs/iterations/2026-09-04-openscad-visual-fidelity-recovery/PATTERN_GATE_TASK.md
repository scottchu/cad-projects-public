# VFR-03 pattern intent gate task

Task ID: `VFR-03`

Input manifest: `inputs/PATTERN_GATE_MANIFEST.sha256`, fingerprint `9f1a0b9871916a956979cb6ea6142a7b6f11a33a5d4fff2fac0388933c517fa0`.

Build a cheap, mobile-first, 2D unwrapped seam strip. It must show only the two frozen alternatives from `BENCHMARK.md`: A is current OpenSCAD N34 with 2 mm body and 11 mm cap smooth collars; B is preserved R7 N33, valley-derived, `0.18` crest plateau, shared phase, and pattern reaching both sides of the seam. Label body, cap, seam, fixed facts, and what the user must inspect. Provide one obvious A/B control and the exact pass/fail question from the benchmark. A seam highlight may be toggled for inspection but may not imply geometry.

Allowed writes: `preview/openscad-pattern-gate/**` and `docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/PATTERN_GATE_IMPLEMENTATION.md`. No 3D OpenSCAD/CAD/source/schema/worker changes, no STL generation, no public hosting, and no printer action. The gate must use deterministic SVG/HTML math rather than an image of someone else's design.

Done: mobile and desktop page renders, A/B visibly differ, labels and exact numeric relationships are readable, no external assets or requests, and the implementer receipt names files and limitations. User pass/fail remains open; the gate does not approve VFR-04.
