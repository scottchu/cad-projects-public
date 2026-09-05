# P2 R22 semantic geometry completion design

## Canonical registry

`app.mjs` calls frozen R10 `derive(state)`. On success, only `descriptor` and presentation/view options cross into R22:

```js
const registry = buildPlanRegistry(descriptor, { presentation });
const scene = materializeRegistry(registry, THREE);
```

`PlanObjectRegistry.register(record)` requires a stable unique `key`, semantic paths, primitive kind, finite positions, indices where faces exist, material parameters, transform, visibility, and local bounds. It returns the same record used for materialization and evidence. `finalize(semanticMap)` evaluates each descriptor-only `activeCondition`, rejects missing or duplicate targets, and rejects active paths without a real object. The materializer creates a same-name object for every visible registry record and recomputes world bounds.

The semantic map is derived beside object registration, not maintained as a disconnected alias table. An independent audit regenerates the expected 84 paths from R10 `PARAMETER_COVERAGE`, verifies exact equality, and for each official pair compares a stripped target snapshot containing only positions, indices, bounds, numeric material parameters, transforms, and presence.

Activity defaults to `descriptor.activeFieldIds.includes(path)`; mode-specific predicates further require the corresponding descriptor subtree/object. The two link predicates use effective-geometry equality exactly as defined in the brief. `container.splitPercent` is always active. Truthful OpenSCAD font metadata is rendered as a named WebGL glyph run whose geometry reflects its exact displayed value; it remains separate from product-label font selection and is excluded from caption-hidden product-family judgments.

## Shared body and seam construction

Sample section support and surface fields in global cylindrical coordinates `(theta, z)`. Build one canonical ring array at every global `z`, including a single seam array at `descriptor.constraints.splitZ`; lower and upper meshes copy that exact seam array. Both halves use the same outside-diameter support and relief envelope. Inner rings use descriptor wall/floor/minimum-wall constraints.

`container.floor` moves the bottom inner end plane and its side-wall connection. `surface.minWall` limits inward displacement and changes the local interior backing surface so the minimum residual wall equals the descriptor constraint when active. `closure.matchPatternClosed=true` applies one global pattern phase; false applies a deterministic upper phase offset above the seam keepout through a short blend, preserving the shared seam ring and coaxial axis.

Tests measure every corresponding seam vertex, lower/upper radial extents, nominal OD support, crest OD, wall separation, floor thickness, and split bounds. Maximum seam radial mismatch is `0.001 mm`.

## Real semantic geometry

- **Closure:** screw uses indexed helical male/female flank surfaces; pitch, turns, runout, form height, and radial clearance change helix vertices/bounds. Bayonet uses countable lugs, receiving slots, and indexed ramps; lock angle, count, capture, rise, and radial clearance change their geometry. Shapes remain unmistakable in exploded close view.
- **Patterns:** `pattern-builders.mjs` exports ten direct builders: `buildSmoothSurface`, `buildBluntDiamondSurface`, `buildRecessedDiamondSurface`, `buildKnitStitchSurface`, `buildStraightMicroFlutesSurface`, `buildFlowingFlutesSurface`, `buildRuggedHexSurface`, `buildShallowHelixSurface`, `buildWaveFlutesSurface`, and `buildQuiltedDiamondSurface`. Each computes its own cells/paths/displacement and indexed topology. Builders may share neutral section interpolation and triangulation utilities, but no pattern selector, generic sine sampler, or conditional fallback may generate multiple named families. Smooth has no feature topology; blunt has broad raised crowns; recessed has inward pockets; knit has paired loops; straight, flowing, and wave flutes have distinct path equations; rugged hex has hex cells; helix has pitch-driven continuous bands; quilt has groove-separated pillows.
- **Fade and relief:** full/bottom/top/center change actual feature extent or amplitude. `fadeMetric=depth` changes radial amplitude; `density` changes cell/path spacing and index count. Keepout removes/clips feature topology at ends and seam. Inset moves vertices inward, outset outward, and balanced spans both sides of the nominal support, with 3/3 geometry signatures and visible silhouette/depth differences.
- **Ends and drains:** build indexed end solids from the R10 meridian paths. Triangulate drain loops as holes in the applicable end face, with no cap triangles across apertures. None, bottom, top, and both must yield 4/4 different aperture topology and visible dark-through openings.
- **Labels and patch:** pinned per-glyph metrics produce indexed extruded glyphs. None has no glyph; inset penetrates inward; outset projects outward. Patch is a real raised/recessed backing surface sized from measured glyph bounds plus descriptor margin and uses sufficient relief/contrast to remain prominent. Target, angle, orientation, size, weight, position, text, preview font, patch, and relief change actual glyph/patch geometry or transform without string-length selection.
- **Attachments:** use distinct indexed builders for eyelet, captured rotating loop, separate clip/link, keyring tab with visible through-bore, and bridge handle. For every non-none mode, the five universal controls `openingWidth`, `openingHeight`, `memberThickness`, `pivotClearance`, and `standoff` alter actual geometry. `keyringHoleDiameter` alters the real bore/coupling feature wherever applicable and `bridgeSpan` alters real anchor spacing wherever applicable; if R10 exposes either control for a mode, the builder must supply a truthful geometric feature rather than ignore it. Mode, presentation, half, and angle change presence or real transforms.

## UI and screenshot evidence

Recreate R21's proven one-viewport shell in R22: compact R10 controls, Basic/Advanced, presets, assembled/exploded, OrbitControls, wheel/pinch zoom, ISO/front/top, responsive fit, readout, and disclosure. Fit includes every registry object. Do not reuse R21 modules.

Browser evidence runs Chromium, Firefox, and WebKit at `1280x900` and `390x844`. Every context performs real orbit/zoom/fixed-view/control/preset/tier/presentation/invalid-state interactions and asserts camera and pixel change, a nonblank canvas, no console/request errors, no overflow, and positive canvas margins for all fit objects.

Caption-hidden current screenshots cover closures, ten patterns, four fades, three relief modes, four drains, label modes/patch, attachment modes including keyring, ends, polygons, and assembled/exploded desktop/mobile. The critic must judge geometry with identical neutral materials where color could mask aliasing.

## Implementation tests and order

Write only:

- `projects/laifen-wave-case/preview/p2-r22-semantic-geometry-completion/**`
- `projects/laifen-wave-case/tests/test_p2_r22_source_contract.mjs`
- `projects/laifen-wave-case/tests/test_p2_r22_registry_contract.mjs`
- `projects/laifen-wave-case/tests/test_p2_r22_parameter_sensitivity.mjs`
- `projects/laifen-wave-case/tests/test_p2_r22_mesh_invariants.mjs`
- `projects/laifen-wave-case/tests/test_p2_r22_family_geometry.mjs`
- `projects/laifen-wave-case/tests/test_p2_r22_ui_contract.mjs`
- `projects/laifen-wave-case/tests/test_p2_r22_browser.py`
- `projects/laifen-wave-case/scratch/r22-*/**`
- R22 candidate/evidence and role receipts under this iteration.

Order: frozen manifest and source ban; registry/84-row activity/target resolution; complete collecting 82-pair sensitivity audit; seam/OD and mesh invariants; family geometry under neutral material; UI; six browser contexts; screenshot sheets; candidate freeze. Audits always collect every failure and emit compact JSON below 1 MiB. No browser run begins while a cheap gate fails.

## Task DAG and ceiling

| Task | Owner/role | Depends on | Done gate and writes |
|---|---|---|---|
| `DES-GCS-R22-01` | architect | rejected R21 + frozen R10 | These five frozen contract files only. |
| `IMP-GCS-R22-01` | implementer | design fingerprint | R22 preview/tests/scratch/implementation receipt; all cheap and browser gates pass; candidate/evidence frozen. |
| `VAL-GCS-R22-01` | independent validator | frozen candidate | Rehashes inputs/candidate/evidence; independently verifies 84/84 targets, 82/82 deltas, seam/OD, meshes, families, and 6/6 browser contexts. |
| `CRIT-GCS-R22-01` | independent visual critic | same candidate | Reviews fresh caption-hidden screenshots for shape distinction, visibility, and clipping. |
| `REV-GCS-R22-01` | independent formal reviewer | VAL PASS + CRIT PASS | Joins exact manifests and boundaries; issues PASS/FAIL. |

Each role has a distinct identity. The implementer receives one initial attempt and at most two grouped repair cycles against complete VAL/CRIT findings. Every repair creates a new candidate and reruns all cheap gates before browser work. A third repair is forbidden; reopen design or reduce exposed features. R21/R10/live/CAD/OpenSCAD remain read-only throughout.
