# P2 R22 semantic geometry completion brief

**Owner:** `DES-GCS-R22-01`  
**Status:** frozen design contract; implementation not started  
**Rejected baseline:** R21 candidate `3d2ce130e8724af9b80a7617296276c71e8d08c02b3117d94f1ad52ff004f443`

## Selected recovery

Create a standalone `preview/p2-r22-semantic-geometry-completion/`. Retain the proven R21 browser/orbit/camera/control behavior by reimplementing it in the R22 namespace. Replace R21's plan, semantic map, materializer, and all deficient model geometry. Do not import any R21 or earlier renderer.

The only model input is a valid frozen-R10 descriptor. One canonical plan-object registry must create each object and its evidence record together. Every semantic-map row names an exact registry key; aliases such as `*.active` or `*.primary` are forbidden unless an object with that literal key exists.

## Required gates

1. **Semantic resolution:** exactly 84 unique R10 coverage rows. Every row contains `path`, a descriptor-only `activeCondition`, exact `primaryTarget`, evidence class, and field-pair oracle. Every active target resolves to an actual plan object and then a same-name Three.js object: 84/84 rows, zero missing/duplicate/unexpected targets.
2. **Actual sensitivity:** the expected-active set is the 84 rows minus the two explicitly conditional link cases below. All 82/82 produce a delta after names, paths, DOM text, annotations, and metadata are stripped. Accepted deltas are vertex/index buffers, geometric bounds, material parameters, object presence, or transforms tied to the modeled feature. No hashes, captions, readouts, colors alone, or evidence-only decorations qualify.
3. **Link conditions:** `ends.linked` is geometry-inactive only when linked and unlinked effective top/bottom end descriptors are equal; otherwise toggling it must change the top end mesh. `ventDrain.linked` is geometry-inactive only in `both` mode when effective top/bottom drain descriptors are equal; otherwise toggling it must change the top end aperture mesh. These rows still resolve to the real affected end object. No other active row receives an inactivity exception.
4. **Seam and diameter:** assembled lower and upper exterior rings share the same canonical seam samples. Maximum paired radial mismatch is `<= 0.001 mm`; both halves preserve the same descriptor outside-diameter datum and crest envelope. Pattern phase changes blend above the seam keepout and never break the shared seam ring.
5. **Known omissions:** actual geometry must change for `container.floor`, `closure.matchPatternClosed`, `closure.screw.formHeight`, `closure.bayonet.radialClearance`, `surface.reliefMode`, `surface.minWall`, `surface.fadeMetric`, `surface.keepout`, `label.mode`, and every R10-active attachment common dimension. The official R10 pair for each is a mandatory regression.
6. **Families:** screw/bayonet are shape-distinct; ten patterns are topology-distinct; fade is 4/4; relief is 3/3; drains are 4/4 actual openings; labels are none/inset/outset 3/3; all six attachment modes including none are distinct. A keyring tab and its bore, and a prominent patch with margin, must be visible without captions.
7. **Human evidence:** representative meshes expose finite vertices, nondegenerate indexed faces, transforms, materials, and bounds. Current real-browser screenshots must establish the same distinctions without captions and without clipping.

## Preserved behavior and bans

Preserve descriptor-only construction, string-independent pinned glyph metrics, real OrbitControls and zoom, ISO/front/top views, fit over all visible objects, invalid-state clearing, R10 controls/presets/tiers, same-diameter two-piece form, assembled/exploded state, six Chromium/Firefox/WebKit desktop/mobile contexts, and the conceptual-only disclosure.

Ban SVG proxy/cards, `.field-witness`, hashes/randomness/string length as visuals, generic scalar witnesses, color-only semantic deltas, captions as acceptance evidence, raw form state below `derive`, prior-renderer imports, and no-op/first-fail audits. R22 may import only the frozen R10 schema, derive, presets, coverage, and utilities outside its own namespace.

R22 makes no CAD, OpenSCAD, STEP/mesh export, slicer, fit, printability, physical, MakerWorld, served-byte, or live-route claim. No live promotion before independent VAL, CRIT, and REV all pass the same candidate fingerprint.
