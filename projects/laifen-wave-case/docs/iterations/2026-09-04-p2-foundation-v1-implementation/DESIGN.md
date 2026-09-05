# P2 Foundation V1 implementation design

## Data boundary

Use the pipeline `form state -> deriveV1(state) -> descriptor -> buildScene(descriptor)`. `deriveV1` is pure and deterministic. Freeze or clone the valid descriptor at the boundary so a scene caller cannot observe later form mutations. The renderer and derived-value readout receive only that descriptor. They may choose camera or clipping presentation but may not calculate model dimensions from controls or DOM values.

R10 `schema.mjs`, `derive.mjs`, `presets.mjs`, `parameter-coverage.mjs`, and `utils.mjs` are frozen references for naming and prior math. Create a deliberately smaller V1 schema and derivation in the new namespace; do not import R10 state with excluded families or any prior renderer.

The descriptor must name and serialize at least:

- input-normalized `H`, `OD`, `W`, `F`, split mode/value, section and active `N`, two end records, screw record, drain record, and presentation;
- derived `R`, `ID`, polygon `AF` when active, `usableHeight`, `U`, `splitPercent`, `splitZ`, lower/upper lengths, engagement `E`, diametral clearance, residual thread wall, end paths, drain positions, piece transforms, and total bounds;
- stable scene-object plans with dimensions sufficient to build every mesh without raw state.

Inactive inputs are normalized and ignored: `N` in round mode; end size for a flat end; all drain dimensions for `none`; bolt circle for count one; the unselected percent/mm split projection. Invalid input returns a null descriptor, and `buildScene` must reject null or incomplete descriptors.

## Stable IDs

DOM regions are `v1-app`, `v1-controls`, `v1-viewport`, `v1-derived`, `v1-errors`, and `v1-disclosure`. Controls use `v1-H`, `v1-OD`, `v1-W`, `v1-F`, `v1-splitMode`, `v1-splitValue`, `v1-section`, `v1-N`, `v1-bottomStyle`, `v1-bottomSize`, `v1-topStyle`, `v1-topSize`, `v1-P`, `v1-T`, `v1-C`, `v1-D`, `v1-threadForm`, `v1-drainLocation`, `v1-Q`, `v1-d`, `v1-BCD`, and `v1-presentation`.

Every materialized Three.js object has exactly one of these names:

| Name | Actual evidence |
| --- | --- |
| `v1.lower.shell` | Lower outside and cavity wall geometry, including its floor and seam edge. |
| `v1.upper.shell` | Upper outside and cavity wall geometry, including its floor and seam edge. |
| `v1.end.bottom` | Bottom flat/chamfer/rounded profile surface. |
| `v1.end.top` | Top flat/chamfer/rounded profile surface. |
| `v1.closure.maleThread` | Triangulated helical male surface attached to the lower piece. |
| `v1.closure.femaleThread` | Triangulated mating internal surface attached to the upper piece. |
| `v1.drains.bottom` | Through-floor hole walls and triangulated floor-with-holes when bottom is active. |
| `v1.drains.top` | Through-floor hole walls and triangulated floor-with-holes when top is active. |
| `v1.seam` | Descriptor-positioned seam edge used only as a neutral inspection line. |

Missing inactive drain groups are correct. All other names must resolve to nonempty `BufferGeometry` in a valid state; captions, badges, helper lines, hashes, colors, and hidden witness objects do not count as geometry evidence.

## Geometry construction

Generate lower and upper hollow meshes directly from outside and inside section rings. For round sections, use sufficient radial segments for smooth inspection; for regular polygons, preserve exactly `N` sides and `OD` as across-corners size. Index outer wall, inner wall, seam rim, and closed-end surfaces with consistent normals. At assembly, both exterior supports have maximum radius `OD/2`, their axes coincide, and the radial mismatch at the seam is at most `0.001 mm`.

End geometry uses the descriptor's actual flat, chamfer, or quarter-round path and stays within its floor envelope. The choices must remain visibly distinct in a radial cutaway and must change vertex positions, normals, and bounds where applicable.

Build male and female thread surfaces from one descriptor helix. Pitch sets axial advance, integer turns set winding count, and `E=P*T` sets engagement length. Depth changes radial profile geometry; `symmetric trapezoid` and `rounded` use distinct sampled cross-sections. Radial clearance changes the actual radial separation between mating surfaces. Integrate the surfaces with the lower spigot and upper internal wall; a drawn helix, line, texture, or unattached ribbon alone does not satisfy the closure requirement.

Build selected drain floors as triangulated faces with genuine holes and cylindrical hole walls through thickness `F`. `Q=1` is centered. For `Q>1`, use the derived bolt-circle positions. `none` produces no drain mesh or hole. Top and bottom choices modify only the selected piece.

Assembled transforms place both pieces at their shared datum. Exploded translates the upper piece only along `+Z` by a descriptor-derived gap while preserving identity and orientation. `v1-view-assembled`, `v1-view-exploded`, `v1-view-open`, and `v1-view-cutaway` are accessible view presets. Open focuses the exploded seam mouths; cutaway applies a real clipping plane to the existing scene. Inspection controls never mutate dimensions.

## UI and readout

Use one large 3D viewport with controls grouped as Body, Split, Ends, Screw, Drain, and View. Hide and disable inactive controls. Report at least clear ID, usable height, upper/lower lengths, synchronized split percent/mm, engagement, diametral clearance, residual thread wall, and drain feasibility from the descriptor. Display this exact disclosure: `Conceptual, dimensionally proportional preview. Not CAD; no printability, fit, strength, drainage, export, or physical validation.`

Fit the camera to current scene bounds in every presentation and after resize. Orbit/pan/zoom and reset must work with pointer, wheel, keyboard-focusable buttons, and touch. Avoid clipping at the smallest supported mobile viewport.

## Risk-driven tests

1. `tests/test_p2_foundation_v1_derive.mjs`: nominal equations, percent/mm split equivalence, round/polygon ID, all bounds and cross-field constraints, deterministic serialization, null descriptor on invalid input, and zero influence from every inactive control.
2. `tests/test_p2_foundation_v1_source_contract.mjs`: only the UI calls `deriveV1`; scene/readout modules receive descriptors; source bans raw-state access in scene modules, SVG proxy/witness/hash decorations, old renderer imports, CDN dependencies, and writes/imports from quarantined R13-R22.
3. `tests/test_p2_foundation_v1_scene.mjs`: named objects, finite indexed vertices, normals/indices/bounds, same-OD/seam tolerance, hollow cavities/floors, split and exploded transforms, actual parameter deltas, distinct ends/thread forms, radial clearance, genuine drain holes, inactive absence, and null-descriptor refusal.
4. `tests/test_p2_foundation_v1_browser.py`: real control interaction and derived readout; invalid recovery; assembled/exploded/open/cutaway; orbit/zoom/reset; resize and no clipping. Exercise Chromium desktop/mobile plus Firefox and WebKit desktop. Capture assembled, open, exploded, and cutaway evidence on desktop and mobile for the critic.

Tests must fail for the credible defect they name. A serialized descriptor change without a corresponding required mesh/material/presence/transform change cannot pass scene sensitivity evidence.

## Acceptance

The implementer freezes source and test paths in `candidate-files.sha256` and evidence in `evidence-files.sha256`. The candidate then remains immutable while independent validator and critic inspect the same hash. Formal review passes only when both reports pass and all `FV1-*` requirements trace to evidence. No live promotion occurs before that chain passes.
