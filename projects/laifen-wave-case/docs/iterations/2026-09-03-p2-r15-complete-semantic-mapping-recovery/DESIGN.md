# P2 R15 complete semantic mapping recovery design

## Selected approach

R15 keeps the R14 target discipline and changes the implementation strategy: repair by semantic group, then audit exhaustively. The first implementation attempt must address every known failing group before deciding whether to proceed. The latest compact exhaustive audit, not an individual unit-test failure, is the repair ledger.

R15 has no descriptor-gap authorization. The R14 audit showed 84/84 descriptor and semantic source deltas, valid active witness pairs, exact-one targets, 0 inactive default leaks, and polygon PASS. The broken layer is the adapter's local geometry/dimension mapping.

## Grouped semantic mapping fixes

| Group | Fields | Required mapping fix |
| --- | --- | --- |
| `screw-detail` | `closure.screw.formHeight`, `closure.screw.radialClearance` | Put both fields in a magnified screw profile target. `formHeight` changes crest/root tooth height and a vertical dimension bracket. `radialClearance` changes the visible male/female gap band and its bracket. The primary target must include the measured profile geometry, not an isolated dimension line. |
| `bayonet-detail` | `closure.bayonet.lockAngleDeg`, `closure.bayonet.rampRise`, `closure.bayonet.radialClearance` | Put all three in the bayonet detail target. `lockAngleDeg` changes an arc from entry lug to lock stop around a fixed datum. `rampRise` changes ramp endpoint height/slope plus a vertical bracket. `radialClearance` changes the lug/channel gap band. |
| `end-detail` | `ends.bottom.size`, `ends.top.size` | Enlarge top and bottom meridian profiles at one scale. Each size target includes the profile curve and a local dimension bracket whose endpoints move with descriptor size. |
| `surface-global` | `surface.envelope`, `surface.depth`, `surface.minWall`, `surface.axialPitch`, `surface.arcPitch`, `surface.coverage`, `surface.fadeMetric` | Use one shared unwrapped surface coordinate frame, but each field owns its own primary target. `envelope` changes active motif-region geometry for full/bottom/top/center. `coverage` changes active band length. `fadeMetric` changes geometry differently for depth fade versus density fade. `depth` changes relief amplitude. `minWall` changes residual-wall gauge. `axialPitch` and `arcPitch` change motif row/column spacing and anchored dimension brackets. |
| `pattern-knit` | `surface.stitch.tightness` | Render stitch loops from descriptor tightness so loop radius, spacing, or crossing angle changes in stripped geometry. |
| `pattern-flutes` | `surface.flute.count`, `surface.flute.duty`, `surface.flute.waveAmplitude`, `surface.flute.waveWavelength`, `surface.flute.wavePhase`, `surface.flute.waveDirection` | Render flutes as descriptor-derived ridge paths. `count` changes ridge count, `duty` changes ridge width versus gap, `waveAmplitude` changes lateral excursion, `waveWavelength` changes period and a period bracket, `wavePhase` shifts ridges against a fixed seam datum, and `waveDirection` mirrors handedness. |
| `pattern-spiral` | `surface.spiral.pitch`, `surface.spiral.bandWidth`, `surface.spiral.softness`, `surface.spiral.direction` | Render spiral bands with a fixed datum. `pitch` changes slope/spacing plus bracket, `bandWidth` changes band thickness, `softness` changes edge geometry or subdivision, and `direction` mirrors handedness. |
| `pattern-quilt` | `surface.quilt.grooveWidth`, `surface.quilt.edgeSoftness`, `surface.quilt.rotationDeg` | Render quilt cells as grooves and pillows. `grooveWidth` changes channel width, `edgeSoftness` changes rounded corner/control geometry, and `rotationDeg` rotates the lattice against a fixed datum with an angle annotation. |
| `drain-faces` | `ventDrain.linked`, `ventDrain.bottom.diameter`, `ventDrain.bottom.ringRadius`, `ventDrain.top.diameter`, `ventDrain.top.ringRadius` | Use paired top/bottom face targets. `linked` changes shared connector geometry and mirrored versus independent face records. Diameter fields change actual hole radii plus brackets. Ring-radius fields change hole-center radius from the face center plus radial brackets. |
| `label-detail` | `label.text`, `label.fontFamily`, `label.weight`, `label.relief`, `label.target`, `label.angleDeg`, `label.patch` | Use deterministic non-hash glyph/proxy geometry. `text` changes character strokes or glyph boxes from a small explicit glyph table. `fontFamily` changes stroke style or metrics by declared preview family. `weight` changes stroke/outline thickness. `relief` changes a raised/recessed section. `target` moves the label to lower/upper/both body regions. `angleDeg` moves a circumferential marker against a datum. `patch` adds/removes a real backplate shape. |
| `attachment-detail` | `attachment.mountAngleDeg` | Anchor attachment mode geometry to the section view and rotate the attachment anchor around a fixed body datum; include a changing angle arc. |
| `container-and-section` | `container.splitPercent` | Tie the percent annotation to the actual seam target. The dimension geometry must change with split position: bracket/tick endpoints follow the seam projection, and readable percent text is checked separately. |

## Preserved gates

- `label.openScadFontFamily` remains the only metadata target.
- All 84 fields must still have exactly one primary `data-field-target`.
- Source-ban stays strict for R15 source/tests.
- Polygon side counts `3..32` stay 30/30 unique; roundness `1` rotation remains expected-inactive.
- Closure/end/pattern/relief/label-mode/attachment/drain family topology passes are preserved, and `surface.envelope` must improve from 1/4 to 4/4 unique after stripping labels and metadata.
- The compact audit must remain <= 1 MB. The R14 audit was about 171 KB JSON and 201 KB total for JSON, summary, and script; R15 must stay compact enough to serve as reviewable evidence.

## Test plan

The implementation must run in this order:

1. Verify R15 frozen inputs and the R14 fingerprint.
2. Copy or build R15 namespace without modifying R14/R13/core/live/CAD files.
3. Run source-ban and target-map gates.
4. Run exact-one/active/inactive target gates.
5. Run the R15 compact exhaustive audit over all 84 fields and all preserved families.
6. Repair every failing group from that audit together, up to two grouped cycles after the initial attempt.
7. Proceed to human category sheets only after cheap 84/84 PASS and audit <= 1 MB.
8. Run six-context browser after sheets.
9. Freeze candidate only after cheap, sheet, and browser gates pass.

Browser and visual work is downstream evidence. It cannot waive a cheap semantic failure.

