# P2 R13 renderer-fidelity recovery design

## Frozen architecture

R12 candidate `51727da73c72db6e391f4f83014a54076dc2ffbdc5bc617f753c72a8fc1a2221` is the immutable input, not an accepted visual candidate. Its pure Phase A/B facts remain authoritative: 83 schema fields plus canonical `container.splitPercent`, 84/84 descriptor sensitivity PASS, and 58/58 inactive-poison PASS. R13 creates a new preview namespace and imports the R12 core read-only. Rendering is a projection of the complete descriptor; it never reads raw state or substitutes labels for geometry.

Before source work, IMP must map every row below to an existing descriptor leaf. If any row lacks enough data for the specified observable, the result is `DESCRIPTOR_GAP`, with the missing path and smallest additive payload. That stops this contract. No core edit is pre-authorized, and no inferred/raw-state workaround is allowed.

## Named render surfaces and target rules

| Surface ID | Purpose |
| --- | --- |
| `r13-main-elevation` | proportional two-piece body, split, ends, pattern, labels and attached features |
| `r13-section-plan` | round/rounded-polygon support silhouette, angular placement and section dimensions |
| `r13-closure-detail` | screw or bayonet topology at the middle seam |
| `r13-end-detail` | same-scale bottom/top and four-profile meridian comparison |
| `r13-surface-map` | unwrapped derived surface field with axial/circumferential spacing and fade |
| `r13-relief-section` | inset/outset/balanced relief and residual-wall/keepout witnesses |
| `r13-drain-faces` | separately labelled top and bottom face masks |
| `r13-label-detail` | readable label, patch and relief/location witnesses |
| `r13-attachment-detail` | mode-specific attached/detached silhouette and dimensions |
| `r13-envelope-facts` | visible dimensional and disclosure metadata |
| `r13-controls` | schema-generated Basic/Advanced control surface |
| `r13-boundary` | persistent conceptual and scale disclosure |

Every active coverage row owns exactly one visible node `[data-field-target="<canonical path>"]` inside one named surface. Canonical visual hashes exclude `data-*`, target names, raw/effect hashes, comments, `<title>`, and hidden nodes. Geometry or style rows hash visible SVG geometry/style attributes; text rows hash rendered text/font attributes; the two justified metadata rows hash visible labelled output. A target must have a nonzero browser bounding box and may not be transparent, clipped out, marker-only, or accessibility-hidden. Whole-document hash deltas do not pass a field oracle.

`label.openScadFontFamily` is metadata because no OpenSCAD engine runs. `container.splitPercent` is projection metadata paired with the same visible seam as canonical millimetres. All other rows require a visible geometric, stylistic, or text-layout change.

## Exhaustive 84-field observability oracle

The A/B states are the valid witnesses from frozen `PARAMETER_COVERAGE`. Each row must change the named node's canonical meaningful-output hash while protected unrelated target hashes remain stable, except explicitly shared envelope/camera consequences.

| # | Field | Surface | Required A/B observable |
| ---: | --- | --- | --- |
| 1 | `container.height` | `r13-main-elevation` | body height/aspect and height dimension |
| 2 | `container.outerDiameter` | `r13-main-elevation` | body width/aspect and OD dimension |
| 3 | `container.splitFromTop` | `r13-main-elevation` | seam position and upper/lower lengths |
| 4 | `container.wall` | `r13-relief-section` | shell band thickness |
| 5 | `container.floor` | `r13-end-detail` | end-floor thickness |
| 6 | `container.crossSection` | `r13-section-plan` | circle versus regular-polygon silhouette |
| 7 | `container.sideCount` | `r13-section-plan` | facet/vertex count; every integer 3..32 unique |
| 8 | `container.cornerRoundness` | `r13-section-plan` | corner radius/curvature |
| 9 | `container.rotationDeg` | `r13-section-plan` | silhouette rotation against a fixed datum ray |
| 10 | `closure.mode` | `r13-closure-detail` | screw helix topology versus bayonet lug/ramp topology |
| 11 | `closure.matchPatternClosed` | `r13-main-elevation` | pattern phase continuity/mismatch across seam |
| 12 | `closure.screw.pitch` | `r13-closure-detail` | crest spacing and pitch dimension |
| 13 | `closure.screw.turns` | `r13-closure-detail` | complete turn count/engagement length |
| 14 | `closure.screw.leadRunoutTurns` | `r13-closure-detail` | tapered lead/runout extent |
| 15 | `closure.screw.formHeight` | `r13-closure-detail` | magnified crest height |
| 16 | `closure.screw.radialClearance` | `r13-closure-detail` | mating radial gap |
| 17 | `closure.bayonet.lockAngleDeg` | `r13-closure-detail` | lock-travel arc length/angle |
| 18 | `closure.bayonet.lugCount` | `r13-closure-detail` | discrete lug count |
| 19 | `closure.bayonet.capture` | `r13-closure-detail` | capture-slot axial depth |
| 20 | `closure.bayonet.rampRise` | `r13-closure-detail` | ramp vertical rise |
| 21 | `closure.bayonet.radialClearance` | `r13-closure-detail` | lug/channel radial gap |
| 22 | `ends.linked` | `r13-end-detail` | link connector plus mirrored versus independent top/bottom state |
| 23 | `ends.bottom.profile` | `r13-end-detail` | bottom meridian topology |
| 24 | `ends.bottom.size` | `r13-end-detail` | bottom profile height/radius dimension |
| 25 | `ends.top.profile` | `r13-end-detail` | top meridian topology |
| 26 | `ends.top.size` | `r13-end-detail` | top profile height/radius dimension |
| 27 | `surface.pattern` | `r13-surface-map` | family-specific field across a reviewable area |
| 28 | `surface.reliefMode` | `r13-relief-section` | inward, outward, or balanced placement about base wall |
| 29 | `surface.envelope` | `r13-surface-map` | full, bottom fade, top fade, or center band distribution |
| 30 | `surface.depth` | `r13-relief-section` | relief amplitude and dimension |
| 31 | `surface.minWall` | `r13-relief-section` | residual-wall limit band/gauge |
| 32 | `surface.axialPitch` | `r13-surface-map` | axial motif spacing |
| 33 | `surface.arcPitch` | `r13-surface-map` | circumferential motif spacing |
| 34 | `surface.coverage` | `r13-surface-map` | fade/band axial extent |
| 35 | `surface.fadeMetric` | `r13-surface-map` | amplitude fade versus density fade treatment |
| 36 | `surface.keepout` | `r13-main-elevation` | smooth seam/end exclusion-band width |
| 37 | `surface.stitch.tightness` | `r13-surface-map` | knit loop spacing/curvature |
| 38 | `surface.flute.count` | `r13-surface-map` | flute count/circumferential density |
| 39 | `surface.flute.duty` | `r13-surface-map` | ridge-to-gap width ratio |
| 40 | `surface.flute.waveAmplitude` | `r13-surface-map` | flowing-flute lateral amplitude |
| 41 | `surface.flute.waveWavelength` | `r13-surface-map` | flowing-flute period |
| 42 | `surface.flute.wavePhase` | `r13-surface-map` | field translation/phase |
| 43 | `surface.flute.waveDirection` | `r13-surface-map` | opposite meander handedness |
| 44 | `surface.spiral.pitch` | `r13-surface-map` | soft-spiral axial pitch |
| 45 | `surface.spiral.bandWidth` | `r13-surface-map` | spiral band width |
| 46 | `surface.spiral.softness` | `r13-surface-map` | spiral edge transition softness |
| 47 | `surface.spiral.direction` | `r13-surface-map` | opposite spiral handedness |
| 48 | `surface.quilt.grooveWidth` | `r13-surface-map` | quilt groove width |
| 49 | `surface.quilt.pillowHeight` | `r13-relief-section` | quilt pillow height |
| 50 | `surface.quilt.edgeSoftness` | `r13-surface-map` | quilt edge curvature/gradient |
| 51 | `surface.quilt.rotationDeg` | `r13-surface-map` | quilt lattice rotation |
| 52 | `ventDrain.mode` | `r13-drain-faces` | none/bottom/top/both enabled faces |
| 53 | `ventDrain.linked` | `r13-drain-faces` | link connector plus shared versus independent face records |
| 54 | `ventDrain.bottom.count` | `r13-drain-faces` | bottom visible hole count |
| 55 | `ventDrain.bottom.diameter` | `r13-drain-faces` | bottom hole diameter |
| 56 | `ventDrain.bottom.ringRadius` | `r13-drain-faces` | bottom hole-ring radius |
| 57 | `ventDrain.top.count` | `r13-drain-faces` | top visible hole count |
| 58 | `ventDrain.top.diameter` | `r13-drain-faces` | top hole diameter |
| 59 | `ventDrain.top.ringRadius` | `r13-drain-faces` | top hole-ring radius |
| 60 | `label.mode` | `r13-label-detail` | none/inset/outset geometry and relief cue |
| 61 | `label.text` | `r13-label-detail` | rendered safe text content |
| 62 | `label.fontFamily` | `r13-label-detail` | preview glyph font family |
| 63 | `label.openScadFontFamily` | `r13-envelope-facts` | visible labelled future-font metadata; no visual-geometry claim |
| 64 | `label.weight` | `r13-label-detail` | glyph stroke weight |
| 65 | `label.size` | `r13-label-detail` | glyph scale |
| 66 | `label.relief` | `r13-label-detail` | inset/outset depth/height section and dimension |
| 67 | `label.orientation` | `r13-label-detail` | horizontal versus vertical transform |
| 68 | `label.target` | `r13-main-elevation` | lower, upper, or both piece placement |
| 69 | `label.angleDeg` | `r13-section-plan` | circumferential marker/label angle against datum |
| 70 | `label.axialFromTargetEnd` | `r13-main-elevation` | axial label position from selected end |
| 71 | `label.patch` | `r13-label-detail` | actual patch absent/present |
| 72 | `label.patchMargin` | `r13-label-detail` | patch outline margin/size |
| 73 | `attachment.mode` | `r13-attachment-detail` | none plus five distinct mode silhouettes |
| 74 | `attachment.presentation` | `r13-attachment-detail` | attached versus visibly detached placement |
| 75 | `attachment.attachHalf` | `r13-main-elevation` | lower versus upper attachment location |
| 76 | `attachment.mountAngleDeg` | `r13-section-plan` | attachment angular marker/location |
| 77 | `attachment.common.openingWidth` | `r13-attachment-detail` | opening width dimension/geometry |
| 78 | `attachment.common.openingHeight` | `r13-attachment-detail` | opening height dimension/geometry |
| 79 | `attachment.common.memberThickness` | `r13-attachment-detail` | member thickness |
| 80 | `attachment.common.pivotClearance` | `r13-attachment-detail` | pivot/capture gap |
| 81 | `attachment.common.keyringHoleDiameter` | `r13-attachment-detail` | keyring-hole diameter |
| 82 | `attachment.common.bridgeSpan` | `r13-attachment-detail` | bridge span |
| 83 | `attachment.common.standoff` | `r13-attachment-detail` | body-to-attachment offset |
| 84 | `container.splitPercent` | `r13-envelope-facts` | visible percentage plus the same seam projection as canonical split mm |

## Family-recognition and UI gates

- Polygon deterministic gate renders every integer `3..32`; all 30 silhouette hashes must be unique. It separately checks at least three roundness values and two non-equivalent rotations for sides 3, 4, 5, 6, 8, 12, and 32. Browser captures may sample those seven side counts after the exhaustive gate passes.
- Categorical family hashes must be pairwise unique for two closure modes, four end profiles, ten patterns, four envelopes, three relief modes, three label modes, six attachment states including none, and four drain modes. A unique caption with aliased geometry fails.
- Basic default has exactly the 14 active Basic controls. Advanced default has those 14 plus the 13 active relevant Advanced controls. The browser must confirm `[hidden]{display:none!important}`, computed `display:none`, no focus/tab stop, and accessibility omission for hidden fields. Mode changes exercise screw/bayonet, linked ends, pattern plugins, drain ends/linking, label disabled/enabled, and attachment disabled/enabled.
- Every visual surface is deterministic: two renders of the same frozen descriptor are byte-identical after canonicalization. No date, randomness, viewport-dependent semantic geometry, or unstable generated IDs enter hashes.
- Invalid state clears `r13-main-elevation`, section, closure, end, surface, relief, drains, label, attachment, comparison, facts, and any cached markup in one transaction.

## Ordered verification and stop rules

1. Verify `inputs/frozen-inputs.sha256`, then verify the nested R12 candidate, implementation, validation, and critique manifests.
2. Rerun frozen R12 Phase A/B and compact audit in a temporary output mirror. Any core/hash/result drift stops R13.
3. Run target-contract, 84-field render-observability, polygon/family uniqueness, UI visibility, disclosure, determinism, and invalid-clearing tests. No browser starts until every cheap gate passes.
4. Run Chromium, Firefox, and WebKit at 1280×900 and 390×844. Capture the major relationship sheet and inspect rendered pixels plus accessibility/DOM evidence.
5. Freeze the candidate. Independent VAL and CRIT run read-only in parallel on the same fingerprint; REV is their join.

Stop immediately on a manifest mismatch, descriptor gap, core edit, target alias, any result below 84/84, polygon alias within 3..32, categorical family alias, ineffective Basic/Advanced state, missing conceptual disclosure, stale invalid output, browser error/overflow/hidden focus, scope expansion, or retry exhaustion. No later gate may waive an earlier failure. No live route exists in this iteration.

## User-confirmable review gate after formal PASS

The review sheet must teach four small relationships before any integrated delivery: (1) fixed two-piece coaxial/middle-split topology versus adjustable proportions/section; (2) screw versus bayonet action and their active tuning; (3) end plus pattern/fade/relief identity; and (4) label/attachment/drain placement. Each panel states what is fixed, what is adjustable, what to inspect, and asks an explicit pass/fail recognition question. User confirmation validates intent only and does not promote the artifact to CAD, export, slicer, or physical evidence.
