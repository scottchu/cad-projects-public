# P2 R21 Three.js interaction fidelity recovery brief

**Owner:** `DES-GCS-R21-01`  
**Status:** frozen design contract; implementation not started  
**Baseline:** R20 candidate `ae45f4e28fd6c34b09c56c34a4d55eb0bed7620f101559e028aa31d12fd98ad4`, independently `FAIL`/`BLOCK`

## Required result

Build a new `preview/p2-r21-threejs-interaction-fidelity-recovery/` app that preserves R20's real Three.js viewport, same-diameter lower/upper pieces, assembled/exploded presentation, R10 Basic/Advanced schema and presets, and conceptual-only disclosure while correcting the exact R20 blockers.

1. `derive(state)` is the only state-to-model boundary. Scene planning and construction accept a valid R10 descriptor plus camera/presentation options; no scene or geometry function receives, imports, closes over, or reads raw form state. Invalid derivation clears the model and stale readouts atomically.
2. Label glyph and patch vertices, bounds, extrusion, placement, and fit derive only from descriptor dimensions and explicit glyph metrics. Neither source nor tests may use text/string length as a geometry selector. `openScadFontFamily` remains truthful visible metadata and never controls browser glyph geometry.
3. Ten named pattern builders are present and directly dispatched: `buildSmoothSurface`, `buildBluntDiamondSurface`, `buildRecessedDiamondSurface`, `buildKnitStitchSurface`, `buildStraightMicroFlutesSurface`, `buildFlowingFlutesSurface`, `buildRuggedHexSurface`, `buildShallowHelixSurface`, `buildWaveFlutesSurface`, and `buildQuiltedDiamondSurface`. There is no known-enum fallback.
4. OrbitControls must support pointer orbit and wheel/pinch zoom. A real interaction must change camera pose and rendered pixels. Compact ISO, front, and top buttons may provide repeatable views; they must move the same camera/controls target.
5. Camera fit uses the union of body, closure, label, patch, attachment, and drain geometry in assembled and exploded states, with a margin. Resize, preset, fixed-view, and rebuild paths refit or preserve a valid view without clipping.
6. Actual viewport geometry must make screw and bayonet; all ten patterns; fade bottom/top/center; inset/outset/balanced relief; none/bottom/top/both drains; representative polygon progression; flat/chamfer/rounded/dome ends; and each attachment mode visibly distinct without captions.
7. Attachment builders must produce distinct geometry for `integrated_lanyard_eyelet`, `captured_rotating_loop`, `separate_clip_link`, `keyring_tab`, and `bridge_handle`; `none` produces none. Half, angle, presentation, and active size/clearance fields change the actual attachment geometry or transform.

## Evidence and bans

Every active R10 field retains exactly one primary semantic scene target or the existing truthful metadata exception. Evidence comes from stable object names and actual vertex/index data, bounds, materials, presence, or transforms. Preserve R20's 84-field coverage, inactive-field behavior, polygon symmetry rule, and geometry invariants.

Ban imports from R20 or earlier renderers, raw-state scene construction, SVG proxy/cards, `.field-witness`, hash-derived or random visuals, field-name/string-length geometry, generic scalar witnesses, and evidence-only decoration. R21 may import the frozen R10 schema, derive, presets, coverage, and utilities.

## Acceptance

- Cheap gates first: frozen manifest, transitive source ban, descriptor-only call graph, ten named builders, label-metric ban, 84-field semantic coverage, and pure geometry invariants.
- Browser gate: Chromium, Firefox, and WebKit at `1280x900` and `390x844`; interact with real controls, orbit, zoom, fixed views, tier, preset, assembled/exploded, valid/invalid transitions, and representative family controls. Require zero console/request errors, nonblank WebGL pixels, camera/pixel change after orbit, no horizontal overflow, and no clipping.
- Current caption-hidden screenshots must cover closures, ten patterns, fades/relief, drains, polygons, ends, labels, attachments, assembled/exploded, and desktop/mobile composition. An independent visual critic evaluates these screenshots.
- Allow one initial implementation and at most two grouped repair cycles. If a gate still fails, stop and reopen design or reduce scope.
- R21 remains conceptual browser evidence. No CAD, OpenSCAD, STEP/mesh, slicer, physical, MakerWorld, or live-route claim. No live promotion before distinct `VAL-GCS-R21`, `CRIT-GCS-R21`, and `REV-GCS-R21` roles pass one fingerprint.
