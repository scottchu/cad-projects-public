# P2 R19 eleven-field semantic recovery design

## Selected approach

Copy R18 into the R19 namespace, keep its standalone renderer and explicit pattern table, and replace only the 11 residual target builders. The renderer receives a descriptor only. Every local builder below owns its field's one primary target and reads the named descriptor values directly.

## Exact local mappings

| Field | Mapping and falsifiable oracle |
| --- | --- |
| `closure.matchPatternClosed` | Draw a fixed seam datum and lower/upper motif phase rays in an assembled closure panel. Use `phaseMatchesPattern`: true makes the two motif rays coincident; false gives the upper ray a visibly different phase while both halves remain coaxial. The stripped phase-ray path set must differ for the official boolean pair. |
| `closure.screw.leadRunoutTurns` | Draw the actual screw helix with a tapered runout at each end. Let runout axial length be `primitive.lead * primitive.pitch`; the helix amplitude ramps between root and crest across that span. An anchored axial bracket shares the taper endpoints. Both helix and dimension-only subgroups must differ for the official pair. |
| `closure.screw.radialClearance` | Draw magnified male and female screw profiles. Their normal gap is `primitive.clearance` at a fixed pixels/mm scale. A clearance bracket terminates on the two profile edges; its endpoint distance and the visible gap must change for the official pair. |
| `surface.reliefMode` | Draw one body-wall section and the actual relief excursion about its base line. Inset uses `insetDepth` inward, outset uses `outsetHeight` outward, and balanced shows both when present; use `baseOD`, `crestOD`, and `minimumResidualWall` for the section limits. All relief modes must remain distinct after captions/text/data attributes are removed. |
| `surface.envelope` | Render an unwrapped field mask at each sampled `(theta,z)`, using `weight` for motif amplitude/occupancy and `placed` for relief. Full, bottom fade, top fade, and center band therefore produce different axial masks without reading an enum string or hash. Require 4/4 stripped envelope geometry. |
| `surface.coverage` | From sorted `(z,weight)` rows, locate the unsaturated-to-saturated transition by linear interpolation; for center mode use both symmetric transitions. Draw a bracket from the relevant end/center datum to those actual transition bounds and render the same weighted mask. The dimension-only endpoints must change for the official coverage pair. |
| `surface.flute.duty` | In the flowing-flute builder, select a deterministic mid-height row, sort by `theta`, and draw its radial cross-section from the row's `raw/placed` values. Use interpolated zero/mid-level crossings as ridge/channel edges so the ridge-to-channel geometry changes with the descriptor field. No enum length, fixed span, or shared aggregate is allowed. |
| `surface.spiral.softness` | In the shallow-helix builder, take a deterministic cross-band slice normal to the traced helix and draw the sampled `raw/placed` edge profile. Locate 25% and 75% normalized crossings by interpolation; use that transition width for the band-edge curve. The profile/control geometry must differ for the official softness pair. |
| `label.openScadFontFamily` | Put one accessible metadata output outside every label SVG/geometry panel. Its normalized text must equal `labels[*].openScadFontFamily` exactly and differ for the official pair. It is tested by exact metadata value, never by stripped geometry or a badge/hash. |
| `label.weight` | Parse the descriptor weight and construct closed glyph-stroke outlines with half-thickness proportional to that numeric weight in the font/weight mini-panel. The outline coordinates, not only text/style metadata, must differ for 400 versus 700. |
| `label.angleDeg` | In a plan panel, place and tangentially rotate the actual glyph/patch at `theta` around a fixed body center. Draw a dimension arc from the seam datum to that radial anchor. The glyph/patch transform and dimension-only arc endpoint must differ for the official pair. |

## Class-specific collecting audit

Run all 84 rows and collect every failure before returning status.

- Geometry targets: remove all text, captions, metadata nodes, and `data-*` attributes, then compare normalized SVG geometry for the official pair.
- Dimension targets: perform the geometry comparison and separately compare the named `[data-dimension-for="path"]` subgroup; its endpoints must touch/project to the feature named in the table.
- `label.openScadFontFamily`: locate its sole metadata target as a general DOM element, assert exact normalized descriptor text for each side, and assert the two values differ. Do not force it through a `<g>` geometry extractor.
- For every official state, count exactly one visible primary target for each active field, no duplicate, and no target for an inactive field. The 73 R18 passing rows remain mandatory.

## Order and stop rules

1. Verify R19 frozen inputs and the R18 stop chain.
2. Create the R19 namespace and run transitive source/import, full-map, exact-one, and inactive gates.
3. Implement all 11 local builders before running the complete 84-row collecting audit.
4. Run ten-pattern, polygon, closure/end/envelope/relief/label/attachment/drain, tier, invalid-clearing, disclosure, and nonzero-area regressions.
5. Only after 84/84 PASS and evidence <=1 MiB, capture normal and caption-hidden sheets.
6. Run Chromium/Firefox/WebKit at desktop and mobile, then freeze one candidate.

One initial attempt plus two grouped repairs is the ceiling. Every repair starts from the full current failure list and reruns steps 2 through 4. If any cheap failure remains after repair two, stop and refreeze or reduce features; browser evidence cannot waive it.
