# P2 R21 Three.js interaction fidelity recovery design

## Data boundary

`app.mjs` owns mutable UI state and calls frozen R10 `derive(state)`. On success it calls:

```js
buildScenePlan(descriptor, { presentation, view })
materializeScene(plan, THREE)
```

`buildScenePlan` is deterministic, finite, and JSON-serializable. It records named indexed geometry, material roles, transforms, and fit participation. `materializeScene` only adapts that plan to Three.js. Neither function accepts raw state. A source/call-graph test rejects state-shaped arguments and any field access outside descriptor and presentation/view options.

## Geometry corrections

- **Labels:** build browser glyph outlines from a local pinned typeface and measure their actual glyph bounds. Scale and extrude those outlines to descriptor `size`, `weight`, `orientation`, target, angle, axial position, and relief. Patch width/height equals measured glyph bounds plus descriptor patch margin; no text-length multiplier. The visible DOM readout reports the exact OpenSCAD font metadata separately.
- **Patterns:** place the ten required named functions in `scene/pattern-builders.mjs`. Each returns its own displacement/topology plan. Blunt diamonds have outward broad crowns; recessed diamonds have inward pockets. Knit uses paired loop cells; flowing and wave flutes have different axial paths; shallow helix has pitch-driven wraps; straight flutes remain axial; hex and quilt use distinct cells. Fade multiplies local amplitude/density by the descriptor envelope, and relief controls signed displacement while respecting descriptor wall/envelope limits.
- **Closures:** screw mode shows pitch-spaced helical engagement with runout and form height; bayonet mode shows countable lugs, receiving slots, and rising ramps with lock-angle travel. Exploded view exposes both mating sides while preserving coaxial alignment and pattern phase.
- **Drains and ends:** end meshes contain actual descriptor-driven holes, with high-contrast interior material and a top view that makes location/count clear. Flat, chamfer, rounded, and dome use distinct meridian geometry and bounds.
- **Sections:** sample polygon support densely enough that side counts 3, 4, 5, 6, 8, 12, and 32 remain legible in top view. Preserve the R10 rule that rotation is visually symmetric only at the truly circular limit.
- **Attachments:** implement separate builders for eyelet, captured rotating loop, separate clip/link pieces, tab with keyring bore, and spanning bridge handle. Their topology, attachment contact, and bounds must differ. Descriptor half selects the real body anchor; angle rotates the anchor; every active size/clearance changes relevant vertices or transforms.

## Camera and interaction

Use Three.js `OrbitControls` with damping disabled during deterministic tests. Canvas pointer events remain enabled above all layout layers. Controls target the combined model bounds center. Orbit, wheel, and touch update camera and render immediately.

`fitCamera(objects, camera, controls, viewport, margin)` computes a world-space `Box3` from every visible semantic object, including labels, patches, attachments, closures, and drain rims/interiors. It derives distance from vertical and horizontal FOV, applies at least 12% margin, updates near/far planes, and never recenters individual features out of frame. ISO/front/top buttons set documented normalized directions, retain the fit distance, update `controls.target`, and render. Refit after preset/model rebuild, presentation change, resize, and explicit reset; ordinary orbit does not snap back.

## Stable scene targets

Keep deterministic names such as `body.lower.mesh`, `body.upper.mesh`, `closure.screw.*`, `closure.bayonet.*`, `surface.pattern.<enum>`, `drains.bottom.hole-<n>`, `drains.top.hole-<n>`, `labels.<target>.glyph`, `labels.<target>.patch`, and `attachment.<mode>.*`. `scene/semantic-map.mjs` must contain all 84 R10 coverage rows and identify one primary target, active condition, descriptor source, evidence property, and oracle per row. Only `label.openScadFontFamily` may use truthful visible metadata as its primary target.

## Required files and tests

Implementation writes are limited to:

- `projects/laifen-wave-case/preview/p2-r21-threejs-interaction-fidelity-recovery/**`
- `projects/laifen-wave-case/tests/test_p2_r21_source_contract.mjs`
- `projects/laifen-wave-case/tests/test_p2_r21_descriptor_boundary.mjs`
- `projects/laifen-wave-case/tests/test_p2_r21_scene_invariants.mjs`
- `projects/laifen-wave-case/tests/test_p2_r21_family_geometry.mjs`
- `projects/laifen-wave-case/tests/test_p2_r21_ui_contract.mjs`
- `projects/laifen-wave-case/tests/test_p2_r21_browser.py`
- `projects/laifen-wave-case/scratch/r21-*/**`
- R21 implementation, candidate, evidence, validation, critique, review, and handoff records.

Test in this order:

1. Verify the frozen input manifest and transitive source/import bans.
2. Prove the descriptor-only boundary, deterministic scene plan, ten named direct-dispatch builders, glyph-metric label sizing, 84-row exact-one map, and inactive-field behavior.
3. Compare actual geometry stripped of names/text/readouts: vertices, indices, bounds, topology, materials, presence, and transforms for closures, every pattern/fade/relief family, drains, polygons, ends, labels, and all attachments.
4. Run the full six-context browser matrix. Each context performs genuine pointer orbit and zoom and asserts camera matrices plus image pixels change, fixed views work, all fit participants remain inside the canvas, controls/presets/tiers/transitions work, and errors/overflow are absent.
5. Freeze the candidate and caption-hidden screenshots, then route that exact fingerprint independently to validation, visual critique, and formal review.

R20, R10/core, P2 R3 live/service, continuity, P1 R7 CAD, OpenSCAD, exports, slicer, and physical namespaces are read-only.
