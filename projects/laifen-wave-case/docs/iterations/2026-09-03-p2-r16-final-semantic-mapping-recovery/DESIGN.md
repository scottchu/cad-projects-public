# P2 R16 final semantic mapping recovery design

## Selected approach

R16 keeps the R15 renderer discipline and makes a residual-only semantic repair. The implementer should copy the R15 preview/tests into the R16 namespace, then patch only the local target mappings/render geometry needed for the 14 residual fields. A full collecting audit decides readiness; first-failure unit tests or one-field repair stops are not sufficient.

## Residual mapping fixes

| Group | Fields | Required local semantic mapping |
| --- | --- | --- |
| `container` | `container.sideCount` | Bind the primary target to the section polygon path only. The A/B oracle measures vertex/facet geometry for side-count deltas with captions and dimensions stripped. Preserve the 30/30 polygon uniqueness behavior. |
| `closure-clearance` | `closure.screw.radialClearance`, `closure.bayonet.radialClearance` | Use feature-anchored radial clearance bands. Screw clearance is the visible male/female thread-profile gap. Bayonet clearance is the lug/channel gap. Each primary target includes both the gap feature and a dimension bracket whose endpoints move with clearance. |
| `surface` | `surface.reliefMode`, `surface.minWall`, `surface.fadeMetric`, `surface.keepout` | Relief mode changes cross-section placement around the wall centerline. Minimum wall changes the residual-wall gauge and wall feature. Fade metric changes geometry by using amplitude fade for depth mode and motif count/spacing for density mode. Keepout changes patterned-area bounds near seam/end. |
| `labels` | `label.mode`, `label.openScadFontFamily`, `label.orientation`, `label.target`, `label.axialFromTargetEnd`, `label.patchMargin` | Label mode changes real inset/outset/none relief geometry. OpenSCAD font is the only metadata badge and must vary truthfully. Orientation rotates glyph/proxy geometry. Target moves actual label geometry to lower/upper/both. Axial position moves label geometry and an anchored dimension. Patch margin changes patch outline size and a margin bracket. |
| `attachment` | `attachment.attachHalf` | Move actual attachment geometry, not just a marker, between lower and upper body regions. The primary target should include the body datum and attachment shape so the stripped geometry changes. |

## Preserved behavior

- Do not change source schema, derive, presets, parameter coverage, R15, R14, R13, live routes, CAD, OpenSCAD, STEP, slicer, printer, or physical records.
- Preserve the 70 existing passing semantic fields and their family topology unless a full 84/84 collecting audit proves the result.
- Preserve source ban and exact-one target gates.
- Preserve no-hash rendering: no value hash to geometry/color/text, no `.field-witness`, no raw/effect hash badge.
- Preserve polygon roundness-1 expected symmetry, closure topology, pattern 10/10, envelope/fade/relief checks, drains, labels, attachments, tiering, invalid clearing, conceptual disclosure, and scale disclosure.

## Required gate order

1. Verify frozen inputs and R15 fingerprint.
2. Create R16 namespace only.
3. Run source-ban and exact-one target gates.
4. Run the collecting audit over all 84 fields.
5. If failures remain, repair the whole residual set from that audit; use at most two full-group cycles after the initial attempt.
6. Require 84/84 PASS, 0 duplicate targets, 0 unexpected inactive targets, source-ban PASS, and audit <= 1 MB before any browser or category-sheet work.
7. Generate human category sheets.
8. Run Chromium, Firefox, and WebKit at 1280x900 and 390x844.
9. Freeze candidate only after all cheap, sheet, and browser gates pass.

R16 remains a conceptual preview until independent validation, independent critique, and formal review all pass one exact candidate fingerprint.

