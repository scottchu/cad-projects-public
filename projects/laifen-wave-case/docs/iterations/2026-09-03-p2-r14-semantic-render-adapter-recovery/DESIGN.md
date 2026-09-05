# P2 R14 semantic render adapter recovery design

## Selected recovery approach

R14 is a semantic adapter repair over the rejected R13 preview. It starts from a new namespace, imports the frozen R12 core read-only, and may reuse R13's useful visual structures only after removing the generic witness system. R14 must prove that every active field changes one declared semantic target, and that categorical families remain distinct after all labels and metadata are stripped.

The adapter has three explicit layers:

1. `target-map`: one row per active canonical field, declaring target class, surface, descriptor source, and oracle.
2. `renderer`: descriptor-to-SVG/DOM only, with no value-hash, source schema, preset, validation, or raw-state authority.
3. `tests`: cheap source ban, exact-one target audit, stripped-geometry field/family audits, UI/disclosure gates, then browser and human-visible sheets.

## Banned failure mechanisms

- No `field-witness`, `.field-witness`, generic witness grids, value-derived HSL, value-derived triangle/path dimensions, raw/effect hash badges, or hashed `JSON.stringify(value)` geometry/color/text.
- No target that passes only because its caption, field name, selected option text, hidden metadata, generated ID, or `data-*` changed.
- No field may have more than one primary `data-field-target`.
- No whole-surface or whole-document hash may stand in for a field oracle.

## Primary target classes

| Class | Allowed use | Test treatment |
| --- | --- | --- |
| `geometry` | visible object proxy, path, mask, glyph outline, attachment shape, hole, seam, wall, or body geometry | strip text/metadata and measure canonical geometry/style |
| `dimension-annotation` | visible dimension line, bracket, angle arc, datum marker, or callout anchored to the changed feature | strip text; measure line/arc/marker geometry and separately assert readable numeric text |
| `metadata-badge` | visible truthful fact where no geometry can be executed in this preview | test text truth and visibility; excluded from geometry-family hashes |

Only `label.openScadFontFamily` is metadata-only: the browser cannot execute OpenSCAD font geometry. `container.splitPercent` is a dimension annotation tied to the same seam projection as `container.splitFromTop`.

## Semantic target map

| Field | Class | Primary target |
| --- | --- | --- |
| `container.height` | geometry | main body height and height dimension |
| `container.outerDiameter` | geometry | main body width and OD dimension |
| `container.splitFromTop` | geometry | seam location and upper/lower segment lengths |
| `container.wall` | geometry | relief-section wall band thickness |
| `container.floor` | geometry | end-floor slab thickness |
| `container.crossSection` | geometry | section silhouette kind |
| `container.sideCount` | geometry | regular-polygon support path with 3..32 unique sides |
| `container.cornerRoundness` | geometry | noncircular rounded-corner path curvature |
| `container.rotationDeg` | dimension-annotation | datum ray plus rotated noncircular polygon; roundness `1` is expected-inactive |
| `closure.mode` | geometry | screw helix proxy versus bayonet lug/ramp proxy |
| `closure.matchPatternClosed` | geometry | seam-phase continuity/misalignment on object skin |
| `closure.screw.pitch` | dimension-annotation | crest-spacing witness anchored to screw path |
| `closure.screw.turns` | geometry | visible engagement-turn count and length |
| `closure.screw.leadRunoutTurns` | geometry | tapered lead/runout extent |
| `closure.screw.formHeight` | dimension-annotation | magnified thread-form height |
| `closure.screw.radialClearance` | dimension-annotation | mating radial gap |
| `closure.bayonet.lockAngleDeg` | dimension-annotation | lock-travel arc |
| `closure.bayonet.lugCount` | geometry | discrete lug count |
| `closure.bayonet.capture` | dimension-annotation | capture-slot axial depth |
| `closure.bayonet.rampRise` | dimension-annotation | ramp-rise height |
| `closure.bayonet.radialClearance` | dimension-annotation | lug/channel clearance gap |
| `ends.linked` | geometry | linked connector plus mirrored versus independent end state |
| `ends.bottom.profile` | geometry | bottom meridian profile path |
| `ends.bottom.size` | dimension-annotation | bottom end size callout anchored to profile |
| `ends.top.profile` | geometry | top meridian profile path |
| `ends.top.size` | dimension-annotation | top end size callout anchored to profile |
| `surface.pattern` | geometry | family-specific motif field across shared unwrapped area |
| `surface.reliefMode` | geometry | inset/outset/balanced relief cross-section |
| `surface.envelope` | geometry | full/bottom/top/center coverage distribution |
| `surface.depth` | dimension-annotation | relief amplitude |
| `surface.minWall` | dimension-annotation | residual-wall gauge |
| `surface.axialPitch` | dimension-annotation | axial motif spacing |
| `surface.arcPitch` | dimension-annotation | circumferential motif spacing |
| `surface.coverage` | geometry | coverage extent |
| `surface.fadeMetric` | geometry | amplitude-fade versus density-fade treatment |
| `surface.keepout` | geometry | smooth seam/end exclusion bands |
| `surface.stitch.tightness` | geometry | knit loop spacing/curvature |
| `surface.flute.count` | geometry | flute count/density |
| `surface.flute.duty` | geometry | ridge-to-gap ratio |
| `surface.flute.waveAmplitude` | geometry | flowing-flute lateral amplitude |
| `surface.flute.waveWavelength` | dimension-annotation | flowing-flute period |
| `surface.flute.wavePhase` | geometry | field translation/phase |
| `surface.flute.waveDirection` | geometry | handedness reversal |
| `surface.spiral.pitch` | dimension-annotation | spiral axial pitch |
| `surface.spiral.bandWidth` | dimension-annotation | spiral band width |
| `surface.spiral.softness` | geometry | spiral edge softness |
| `surface.spiral.direction` | geometry | spiral handedness |
| `surface.quilt.grooveWidth` | dimension-annotation | quilt groove width |
| `surface.quilt.pillowHeight` | geometry | pillow-height relief section |
| `surface.quilt.edgeSoftness` | geometry | quilt edge curvature |
| `surface.quilt.rotationDeg` | dimension-annotation | quilt lattice rotation |
| `ventDrain.mode` | geometry | none/bottom/top/both face masks |
| `ventDrain.linked` | geometry | shared versus independent face records |
| `ventDrain.bottom.count` | geometry | bottom hole count |
| `ventDrain.bottom.diameter` | dimension-annotation | bottom hole diameter |
| `ventDrain.bottom.ringRadius` | dimension-annotation | bottom hole-ring radius |
| `ventDrain.top.count` | geometry | top hole count |
| `ventDrain.top.diameter` | dimension-annotation | top hole diameter |
| `ventDrain.top.ringRadius` | dimension-annotation | top hole-ring radius |
| `label.mode` | geometry | none/inset/outset label relief proxy |
| `label.text` | geometry | deterministic non-hash glyph-outline/proxy geometry derived from safe text; readable support text is not the oracle |
| `label.fontFamily` | geometry | font-specific glyph silhouette or metric proxy; caption-only font text fails |
| `label.openScadFontFamily` | metadata-badge | visible future-font metadata only |
| `label.weight` | geometry | glyph stroke/weight geometry |
| `label.size` | dimension-annotation | glyph scale |
| `label.relief` | dimension-annotation | inset/outset relief depth |
| `label.orientation` | geometry | horizontal versus vertical transform |
| `label.target` | geometry | lower/upper/both placement on main body |
| `label.angleDeg` | dimension-annotation | circumferential label-angle marker |
| `label.axialFromTargetEnd` | dimension-annotation | axial placement from selected end |
| `label.patch` | geometry | patch absent/present shape |
| `label.patchMargin` | dimension-annotation | patch margin around label |
| `attachment.mode` | geometry | none plus five distinct attachment silhouettes |
| `attachment.presentation` | geometry | attached versus detached placement |
| `attachment.attachHalf` | geometry | lower versus upper mounted relationship |
| `attachment.mountAngleDeg` | dimension-annotation | angular placement marker around section |
| `attachment.common.openingWidth` | dimension-annotation | opening width |
| `attachment.common.openingHeight` | dimension-annotation | opening height |
| `attachment.common.memberThickness` | dimension-annotation | member thickness |
| `attachment.common.pivotClearance` | dimension-annotation | pivot/capture clearance gap |
| `attachment.common.keyringHoleDiameter` | dimension-annotation | keyring hole diameter |
| `attachment.common.bridgeSpan` | dimension-annotation | bridge span |
| `attachment.common.standoff` | dimension-annotation | body-to-attachment offset |
| `container.splitPercent` | dimension-annotation | seam percentage annotation tied to split projection |

## Required oracles

Cheap gates must run before browser work:

- Source ban scans R14 preview source/CSS/tests for `.field-witness`, `field-witness`, renderer-side crypto/hash imports, value-derived HSL, and hashed value-to-geometry helpers.
- Target-map gate proves every active field has one declared primary target, one class, one surface, and one descriptor source.
- Exact-one DOM gate renders every official A/B pair and asserts exactly one visible primary target per active field, with nonzero browser bounding box and no hidden/transparent/off-viewBox target.
- Stripped geometry gate removes labels, captions, metadata badges, `data-*`, comments, hidden nodes, and generated IDs before hashing or measuring geometry/style.
- Metadata gate separately checks `label.openScadFontFamily` text truth and visibility.
- Polygon gate verifies side counts `3..32` at noncircular roundness, corner-roundness deltas, and rotation deltas only for noncircular support. Roundness `1` may confirm circular symmetry but must not be used to claim rotation sensitivity.
- Family gates require stripped-geometry uniqueness for closure modes, end profiles, all ten surface families, envelope modes, relief modes, label modes, attachment states, and drain modes.
- Blunt/recessed gate specifically compares the diamond families with all text/color/metadata removed.
- Human-visible sheets are required for sections, closures, ends, patterns, fade/relief, labels, attachments, drains, and desktop/mobile tier states.

## Visual repair directives

- Preserve the R13 true polygon construction for side-count uniqueness, but repair the rotation oracle.
- Preserve screw/bayonet, drain, tier, invalid-clearing, and disclosure behavior as regressions.
- Replace generic pattern cells with family-specific motifs: smooth is visually empty/smooth; blunt diamond has raised broad facets; recessed diamond has cut channels or negative relief; knit, flutes, spiral, hex, helix, wave, and quilt use recognizably different strokes or geometry.
- Enlarge end profile paths and show top/bottom at one shared scale.
- Enlarge attachment proxies, anchor attached states to clear body datums, separate detached presentation clearly, and make half/angle/dimension annotations local to the attachment.
- Keep persistent adjacent text: `Conceptual descriptor preview only - not CAD, OpenSCAD, or a printable/exportable model.` Keep fit-to-view/not-calibrated separate.
