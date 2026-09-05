# P2 R20 real Three.js generator brief

**Owner:** `DES-GCS-R20-REC-01`  
**Status:** frozen design contract only; implementation not started.  
**Iteration:** `2026-09-03-p2-r20-real-threejs-generator`

## Problem

R19 preserved an 84-row mapping shape but still failed as a visual recovery because it used SVG proxy/witness cards and generic scalar mechanisms. Independent validation failed at 48/84 class-specific rows, found ten failed local oracles, family aliases, a polygon symmetry regression, malformed SVG paths, and blank teaching panels. Independent critique blocked label panels, attachment panels, polygon readability, and end-profile clarity. R20 must reset the preview architecture to a real Three.js scene with measurable objects instead of per-field witness drawings.

## Required result

Build a standalone R20 preview with one real Three.js main viewport. The scene must import frozen R10 `DEFAULT_STATE`, `FIELD_SCHEMA`, `MODULE_SCHEMA`, `visible`, `derive`, and presets/read helpers as needed, then build scene geometry from the R10 descriptor. The main evidence is named Three.js objects, mesh vertices, bounds, transforms, material groups, and screenshots from real browser interaction.

The viewport must contain actual scene objects for:

- two-piece lower/upper body meshes driven by descriptor height, OD, wall/floor/split, split percent, exploded state, and camera fit;
- round and regular-polygon sections, including side count, corner roundness, and rotation, with roundness-1 rotation treated as visually symmetric/inactive;
- screw and bayonet closure objects, including pitch/turns/runout/form/clearance and lock angle/lug/capture/ramp/clearance;
- linked/independent bottom/top end profiles and sizes;
- all ten surface patterns and all fade/envelope controls, including recognizably different blunt/recessed, knit/wave, and helix/flute topology;
- top/bottom/both/none drains with counts, diameters, and ring radii at the correct end faces;
- safe browser label geometry, patch geometry, label target/orientation/angle/position/relief/size/weight, and a separate truthful OpenSCAD font metadata object outside label geometry;
- all attachment modes, presentation, attach half, mount angle, and common size/clearance dimensions;
- compact controls, preset selection, tier visibility, readout, invalid-state clearing, and a visible conceptual-only disclosure.

## Non-goals

Do not generate or edit CAD, OpenSCAD, STEP, STL, 3MF, slicer files, print settings, printer state, MakerWorld assets, publication state, or the P2 R3 live route. Do not import R16/R17/R18/R19 renderers or reuse R19 SVG proxy/witness-card architecture. Do not use per-field witness hashes, field-name length, string-length selectors, random colors, hash colors, `.field-witness`, or universal scalar fallback geometry as evidence.

## Acceptance gates before a candidate

1. Frozen manifest verification passes.
2. Static source gate confirms all R20 transitive source files avoid prior renderers, SVG proxy/witness cards, value-hash mechanisms, field-name length mechanisms, generic scalar reducers, randomness, timestamps, and `.field-witness`.
3. Scene semantic map covers every active/conditional R10 field path with a named object, geometry source, bounds/transform invariant, or truthful metadata invariant. No map row may be satisfied by a value hash or by text-only evidence except `label.openScadFontFamily`.
4. Pure core and scene invariant tests pass across presets and official field pairs: mesh vertices/bounds/transforms/named object facts must change for the intended field and stay stable for unrelated invariant checks.
5. Surface families, end families, drain modes, closure modes, attachment modes, label modes, and polygon side counts are visually and geometrically distinct under stripped object/scene evidence. Roundness-1 polygon rotation is expected symmetric.
6. Browser gate passes Chromium, Firefox, and WebKit at desktop and mobile sizes using real controls: no console errors, no request failures, canvas nonzero, viewport responsive, readout/disclosure visible, invalid state clears the scene, presets/tier controls work, and screenshots are captured from the Three.js viewport.
7. Caption-hidden screenshot review surfaces exist for the actual Three.js scene states: patterns/fades, labels, attachments, polygon/end/drain preservation, and closure. The sheets must be human-visible screenshots of the real scene, not SVG cards.

## Retry and stop limits

One initial implementation plus at most two grouped repair cycles are allowed. Stop on any need to edit prior/core/live/CAD/export/slicer/physical state, any source-ban failure that cannot be repaired in scope, any R10 schema/derive edit need, any per-field witness/hash mechanism, missing scene coverage for an R10 field, browser failure after two grouped repairs, or evidence that requires a live route before independent VAL, CRIT, and formal REV all PASS the same candidate fingerprint.
