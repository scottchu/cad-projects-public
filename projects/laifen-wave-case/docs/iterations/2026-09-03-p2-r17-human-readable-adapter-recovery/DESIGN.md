# P2 R17 human-readable adapter recovery design

## Selected approach

R17 keeps the R16 no-hash, exact-one, descriptor-only renderer contract and fixes the independent blockers directly. The implementation should copy R16 into a R17 namespace, correct target-map declarations, then patch only the named targets and three human clarity cards. A full independent-style audit, not the prescribed R16 tests alone, is the candidate gate.

## Blocker mapping

| Blocker | Exact fix |
| --- | --- |
| `container.rotationDeg` | Add an angle arc and fixed datum ray in the primary target, anchored to the rotated polygon path. The target remains dimension-annotation and must not pass by polygon geometry alone. |
| `surface.flute.waveWavelength` | Fix the case-sensitive selector/path issue and include a local period bracket whose endpoints move with wavelength and are anchored to the flute wave path. |
| `surface.spiral.pitch` | Fix the lowercase `pitch` selector/path issue and include a spiral pitch bracket/normal spacing dimension anchored to the diagonal band geometry. |
| `attachment.mountAngleDeg` | Add a local body datum and angle arc from datum to attachment anchor; rotated attachment geometry alone is insufficient. |
| Nine `descriptor.body` rows | Replace nonexistent source declarations: height -> `descriptor.constraints.height`; outerDiameter -> `descriptor.envelopes.baseOD`; splitFromTop -> `descriptor.constraints.splitFromTop`; wall -> `descriptor.constraints.wall`; floor -> `descriptor.constraints.floor`; crossSection -> `descriptor.section.kind`; sideCount -> `descriptor.section.support`; cornerRoundness -> `descriptor.section.support`; rotationDeg -> `descriptor.section.rotationDeg`. |
| Pattern aliases | Use explicit per-enum motif builders. `blunt_diamond` uses broad raised diamond facets; `shallow_helix` uses diagonal helical bands. `knit_stitch` uses loop/crossing stitch geometry; `wave_flutes` uses sinusoidal vertical flute ridges. Equal enum-name length must not produce equal geometry. |
| Drain bottom/top alias | Encode end identity in stripped geometry: bottom holes live on the bottom face geometry and top holes live on the top face geometry, with distinct end placement or orientation surviving text removal. |
| Zero-height default boxes | For `ends.bottom.profile`, `label.mode`, and `attachment.mode`, make default/none/flat states area-bearing visible geometry in every engine: a flat end slab, an empty-but-visible label zone, and an empty-but-visible attachment datum/pocket. |
| Surface card clarity | Spread motif samples and envelope/fade/relief examples so the family identity survives when captions are ignored. Avoid overlapping dimension marks and use separate local subareas for pattern identity versus fade/relief. |
| Label card clarity | Move the OpenSCAD metadata badge outside the active label-geometry group. Give glyph/proxy, patch, target placement, orientation, and axial dimension separate local space so none occlude each other. |
| Attachment card clarity | Give mode, half, angle, and size annotations separate local hierarchy; one dominant attachment proxy plus one local dimension should be readable per state. |

## Preserved behavior

- Preserve all R16 passes outside the blocker list.
- Preserve exact-one primary `data-field-target` ownership and 0 duplicate/inactive target leaks.
- Preserve OpenSCAD font as the only metadata target.
- Preserve polygon side-count uniqueness and roundness-1 expected rotation symmetry.
- Preserve conceptual-only and scale disclosures, Basic/Advanced behavior, invalid clearing, and no horizontal overflow.
- Preserve CAD/export/physical separation.

## Required gates

1. Verify R17 frozen inputs and R16 candidate/evidence manifests.
2. Create R17 namespace only.
3. Run source-ban and exact-one target gates.
4. Run an independent-style audit that includes target-class enforcement, descriptor-source existence, stripped family uniqueness, drain bottom/top distinction, and strict target bbox rules.
5. Run prescribed R17 semantic/family/UI gates.
6. Run strict Chromium/Firefox/WebKit desktop/mobile browser bbox gate for all active primary targets, including `ends.bottom.profile`, `label.mode`, and `attachment.mode`.
7. Create human category sheets for surface, labels, and attachments plus preserved categories.
8. Freeze candidate only after all gates pass.

Use one initial implementation plus at most two grouped repair cycles. No live route or delivery work is authorized before independent validation, critique, and formal review pass.

