# P2 R18 standalone semantic renderer design

## Architecture

`app.mjs` may call the frozen `derive(state)`. It passes either the complete descriptor to `renderR18(descriptor)` or clears all visual output for an invalid result. The R18 renderer imports only R18-local rendering helpers and the R18 target map. It never imports a prior renderer, schema, derive, presets, or raw state.

`target-map.mjs` must contain exactly 84 records and no nine-row overlay. Its path set must equal the frozen `PARAMETER_COVERAGE` path set with no missing, extra, or duplicate path. Every `descriptorSource` must resolve for the field's active official pair. Every active row owns exactly one primary target. Geometry and dimension tests remove text, badges, metadata, and `data-*` attributes before comparing output. `label.openScadFontFamily` alone uses a separate exact-value metadata oracle.

The source-ban test starts at `app.mjs` and `render/renderer.mjs`, resolves every static local import recursively, and scans the resulting closure. It rejects imports containing `p2-r16` or `p2-r17`, renderer-side core imports, and every mechanism named in R18-06. A passing wrapper cannot hide a banned imported implementation.

## Ten explicit surface builders

Use an exhaustive builder table keyed by these exact ten values. No default/fallback builder is allowed; an unknown value is an error.

| Pattern | Required stripped geometry |
| --- | --- |
| `smooth` | area-bearing plain surface datum with no relief motif |
| `blunt_diamond` | broad filled/faceted diamonds projecting above the base section |
| `recessed_diamond` | incised diamond channels with open/negative centers and an inward section notch visibly opposite to blunt facets |
| `knit_stitch` | paired loop paths with visible crossings and row offset |
| `straight_micro_flutes` | straight, narrow, parallel axial ridges |
| `flowing_flutes` | continuous sinusoidal axial ridges with field-derived amplitude, phase, direction, and period |
| `rugged_hex` | staggered closed hexagonal cells with thick shared edges |
| `shallow_helix` | sparse diagonal bands whose traced centerline advances axially around circumference |
| `wave_flutes` | alternating wave ridges with a topology distinct from flowing axial flutes |
| `quilted_diamond` | rounded pillow diamonds separated by paired groove paths |

Builders consume `descriptor.surface`, including sampled `{theta,z,raw,weight,placed}` records and relief/envelope values. Each builder uses its own named topology and deterministic sample transform. No builder may use enum spelling/length or a common scalar aggregate to manufacture distinction.

For `surface.flute.waveWavelength`, the flowing-flute builder first constructs its visible ridge trace from the descriptor field. The dimension subgroup must use two consecutive same-phase crossings or crests from that trace; its endpoints and span therefore change with the official wavelength pair. For `surface.spiral.pitch`, the helix builder traces one band through increasing theta and unwraps it; the dimension subgroup connects corresponding band points one full turn apart. Its axial span is the traced pitch and changes with the official pair. Tests compare only each `[data-dimension-for=...]` subgroup after stripping text/data attributes, then verify both endpoints touch or project onto the owning feature. Fixed sample-row spacing is forbidden.

## Label and attachment teaching layout

OpenSCAD font metadata is a sibling metadata panel outside the label SVG/card. It displays the normalized `descriptor.labels[*].openScadFontFamily` value exactly, has its own accessible heading, and cannot overlap or count as label geometry. It is the only truthful-metadata target.

The label card uses six disjoint, named mini-panels with independent view boxes or nonintersecting bounding boxes:

1. `label-mode-panel`: none shows only the surface datum; inset cuts glyph/patch inward; outset projects it outward.
2. `label-font-weight-panel`: glyph outlines change by preview font family and actual stroke/outline thickness changes by weight.
3. `label-orientation-panel`: the same glyph and patch rotate between horizontal and vertical around a fixed anchor.
4. `label-target-panel`: a full lower/upper body diagram places the actual glyph/patch on lower, upper, or both halves.
5. `label-position-panel`: an end-anchored bracket terminates at the actual label anchor and moves with axial position.
6. `label-patch-panel`: patch presence and margin change the real patch outline around a fixed glyph bound.

The attachment card likewise uses four nonoverlapping mini-panels:

1. `attachment-mode-panel`: one dominant explicit silhouette for each of the six modes.
2. `attachment-half-panel`: the same actual attachment moves across the seam between lower and upper anchors.
3. `attachment-angle-panel`: the actual attachment rotates from a fixed body datum and owns the angle arc.
4. `attachment-size-panel`: opening, member, clearance, hole, bridge, and standoff dimensions terminate on the actual silhouette.

Every mini-panel remains visible and area-bearing for its default/none state. A field's primary target stays inside the panel teaching that field; panels may share descriptor-derived geometry but may not duplicate primary ownership.

## Gates and artifacts

Run in this order:

1. Verify the R18 frozen manifest and the nested R17 candidate/evidence manifests.
2. Run the transitive import/source ban and exact 84-row map/source/class audit.
3. Run the complete collecting audit: 84/84 active field deltas, exact-one ownership, zero duplicate/unexpected inactive targets, dimension-only wavelength/pitch deltas, and compact evidence at or below 1 MiB.
4. Run polygon and all family topology regressions, including ten explicit pattern builders and strong blunt/recessed stripped difference.
5. Run UI tests for Basic/Advanced grouping, invalid clearing, disclosure, metadata separation, panel nonintersection, and accessibility.
6. Capture category sheets for container, closure, ends, surface, drains, labels, attachments, and tier/invalid states. Capture a second surface/label/attachment set with explanatory headings, captions, legends, and metadata hidden while retaining geometry and dimension strokes.
7. Run Chromium, Firefox, and WebKit at `1280x900` and `390x844` with nonzero active targets, no overflow, no hidden focus, and no page/console/request error.
8. Freeze a candidate only after all prior gates pass.

The initial attempt must implement the whole standalone architecture. At most two later repair cycles may address the complete latest failure groups; every cycle reruns steps 2 through 5 before browser work. If the ceiling is exhausted, stop and reopen or reduce the feature set.
