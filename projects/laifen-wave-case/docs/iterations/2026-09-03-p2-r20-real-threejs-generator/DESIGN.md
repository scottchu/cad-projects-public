# P2 R20 real Three.js generator design

## Selected architecture

R20 replaces SVG proxy cards with a standalone Three.js generator. The R20 app imports the frozen R10 core for controls, presets, validation, and descriptor derivation, then passes valid descriptors into an R20-only scene builder. The scene builder owns all R20 geometry and must not import any prior renderer or target map.

Recommended file split:

- `preview/p2-r20-real-threejs-generator/index.html`: canvas host, controls container, readout, disclosure.
- `preview/p2-r20-real-threejs-generator/app.mjs`: R10 schema controls, presets, tier filtering, invalid-state handling, browser wiring.
- `preview/p2-r20-real-threejs-generator/scene/build-scene.mjs`: pure descriptor-to-Three.js scene builder plus evidence summary.
- `preview/p2-r20-real-threejs-generator/scene/geometry.mjs`: deterministic mesh helpers for sections, closures, ends, patterns, drains, labels, attachments, dimensions, and exploded offsets.
- `preview/p2-r20-real-threejs-generator/scene/semantic-map.mjs`: all R10 field paths mapped to named scene objects and invariant checks.
- `preview/p2-r20-real-threejs-generator/style.css`: compact responsive controls/readout; no proxy-card layout.

R20 may use Three.js primitives, `BufferGeometry`, `ShapeGeometry`, `ExtrudeGeometry`, `Line`, `LineLoop`, `Group`, `Mesh`, sprites/canvas textures for safe label text, and measurement helper lines/arcs when they are anchored to scene features. Measurement helpers are allowed only as truthful annotations of geometry already present in the scene.

## Source and evidence boundary

The transitive R20 source gate scans every `.mjs`, `.js`, `.html`, and `.css` file under `preview/p2-r20-real-threejs-generator/` and every R20 test/audit script. It must reject imports from prior preview renderers/maps, `<svg` proxy output, `.field-witness`, `crypto`, SHA/hash helpers, `JSON.stringify`-based rendering evidence, `Math.random`, timestamps, `field.path.length`, `pattern.length`, raw/string length as geometry selectors, shared `raw.reduce` aggregate witnesses, and universal scalar fallback builders.

Frozen R10 core is allowed as an import source but remains read-only. R20 must not use R10 descriptor `effects` digests as visible geometry, colors, text, or acceptance evidence.

## Scene object contract

The scene builder returns `{scene, root, evidence}`. `root.name` is `p2-r20-real-threejs-generator`. Every semantic object has a stable `name`, `userData.path` for the R10 field paths it supports, `userData.source` pointing to the descriptor subtree, and `userData.kind` set to `geometry`, `dimension-annotation`, or `truthful-metadata`. The evidence summary records object name, field path, vertex count, bounding box, world transform, material role, and relevant measured value.

Primary scene groups:

| Group | Required named objects and invariants |
| --- | --- |
| Body | `body.lower.mesh`, `body.upper.mesh`, `body.innerWall.reference`, `body.floor.reference`, `body.split.plane`, `body.split.percent.annotation`; bounds reflect descriptor height/OD/split/wall/floor. |
| Section | `section.crossShape.loop`, `section.sideMarkers`, `section.rotation.datum`; side count 3-32 yields distinct loop vertices, corner roundness changes vertex interpolation, roundness-1 rotation has no false geometry delta. |
| Closure | `closure.screw.*` for helix pitch/turns/runout/form/clearance and `closure.bayonet.*` for lugs, ramps, capture, lock angle, clearance; only the active closure mode is primary, with inactive comparison objects marked non-primary if shown. |
| Ends | `ends.bottom.profile`, `ends.top.profile`, `ends.bottom.size.annotation`, `ends.top.size.annotation`; flat/chamfer/rounded/dome produce distinct geometry and nonzero bounds. |
| Surface | `surface.pattern.<name>`, `surface.fade.<envelope>`, `surface.relief.<mode>`, and field-specific lines/meshes for depth, minWall, axialPitch, arcPitch, coverage, keepout, stitch, flute, spiral, and quilt controls. Ten pattern builders are explicit functions with no fallback for a known enum. |
| Drains | `drains.bottom.*`, `drains.top.*`; mode none/bottom/top/both controls actual face placement, count, diameter, and ring radius. |
| Labels | `labels.lower.glyph`, `labels.upper.glyph`, `labels.patch.*`, `labels.angle.annotation`, `labels.position.annotation`, `labels.font.preview`, `metadata.openscadFont.value`; OpenSCAD metadata is a separate truthful text object whose target text equals the descriptor value. |
| Attachments | `attachment.<mode>.geometry`, `attachment.half.anchor`, `attachment.angle.annotation`, `attachment.opening.annotation`, `attachment.member.annotation`, `attachment.clearance.annotation`; attach half moves the actual anchor between lower/upper bodies. |
| UI evidence | `readout`, `status`, `controls`, `preset`, `tier`, and disclosure elements are DOM evidence, not scene substitutes. |

## Explicit pattern builders

The implementation must define ten named builders and dispatch by enum without a generic fallback for known values:

1. `buildSmoothSurface`
2. `buildBluntDiamondSurface`
3. `buildRecessedDiamondSurface`
4. `buildKnitStitchSurface`
5. `buildStraightMicroFlutesSurface`
6. `buildFlowingFlutesSurface`
7. `buildRuggedHexSurface`
8. `buildShallowHelixSurface`
9. `buildWaveFlutesSurface`
10. `buildQuiltedDiamondSurface`

Blunt versus recessed must differ by actual depth/normal direction and silhouette or material treatment. Knit versus wave must differ by stitch loops versus longitudinal wave flutes. Shallow helix versus flutes must differ by helical band direction and pitch-driven wrap.

## Tests and evidence

Required implementation tests:

- `tests/test_p2_r20_source_contract.mjs`: source/import ban, R10 import allowed, no prior renderer/map import, no SVG proxy/witness-card architecture, semantic map covers all R10 field paths.
- `tests/test_p2_r20_scene_invariants.mjs`: descriptor-to-scene object names, mesh vertex counts, bounds, transforms, split/exploded state, polygon behavior, closure, ends, surface, drains, labels, attachments.
- `tests/test_p2_r20_family_geometry.mjs`: explicit pattern/fade/end/drain/closure/label/attachment family differences using object geometry with labels and metadata ignored.
- `tests/test_p2_r20_ui_contract.mjs`: controls, tiers, presets, invalid clearing, readout, disclosure, and no hidden focus leaks.
- `tests/test_p2_r20_browser.py`: Chromium/Firefox/WebKit desktop/mobile real-control interaction, console/request error checks, responsive canvas bbox, and screenshot capture.
- `scratch/r20-independent-style-audit/audit.mjs`: compact independent-style audit summarizing field coverage, source ban, object evidence, family geometry, and browser preconditions. JSON output must remain under 1 MiB.

Candidate freeze requires all local tests, the compact audit, the six-context browser gate, and screenshot sheets to pass. The implementation receipt must report the design fingerprint, candidate manifest SHA-256, evidence manifest SHA-256, exact commands, repair-cycle count, changed paths, and unresolved acceptance gaps.

## Formal acceptance chain

R20 cannot be treated as delivered or live until distinct independent VAL, CRIT, and formal REV roles all PASS the same R20 candidate fingerprint. VAL must inspect scene-object evidence and browser behavior. CRIT must use current screenshots with captions hidden where required. REV must join the frozen design, candidate, validation, critique, source, evidence manifests, and acceptance boundary.
