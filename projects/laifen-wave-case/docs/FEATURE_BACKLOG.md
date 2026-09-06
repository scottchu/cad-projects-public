# Container feature backlog

Reconciled against delivered commit `191cb37119f9a4e4d23112ecd5bc0d18f0daec86`,
SCAD `497098afa555092a0ed85a3a7213cd270852aa76f9001e1478c209cd8469bc42`.
The user requests the original roadmap, one reviewed item at a time. This file
restores its order; a historical preview, enum or screenshot is not SCAD delivery.
Authority: [Foundation V1](iterations/2026-09-04-p2-foundation-v1/DESIGN.md),
[current source](../openscad/laifen_case_customizer_v1.scad), and the
[backlog gate](iterations/2026-09-06-pattern-backlog/BRIEF.md). Decisive historical
inputs are frozen in that gate's `inputs/design-extra.sha256`.

## V2 — original pattern order and source-based mapping

| Order / original item | Delivered mapping and remaining action |
| --- | --- |
| 1 Smooth baseline | Delivered Smooth has no sidewall displacement. Preserve exact geometry regression. |
| 2 Blunt diamond | Current Diamond covers this morphology: broad plateau centers at crest radius and depressed crossing grooves, from the actual `diamond_field`/`diamond_radius` equations. It does not reproduce every historical preview setting; do not add a duplicate merely to restore the old label. |
| 3 Recessed diamond | **Next distinct missing item.** Current Diamond centers are high; documented recessed centers are low with high crossing ridges. No delivered field has this pocket lattice. Run the isolated appearance comparison before source work. |
| 4 Knit stitch | Missing. Paired loop/stitch cells are absent from all five source fields. Historical registry/preview entries do not establish a working knit surface. |
| 5 Straight micro-flutes | Partial overlap with Ribs: both are axial. Ribs is a continuous circumferential cosine with rounded valleys and spacing4–16mm; historical micro-flutes specified narrow recesses, flat lands and duty/count controls. Compare appearance/scale later before deciding whether an extension is sufficient; no duplicate by name. |
| 6 Flowing flutes | Missing distinct axial meandering-flute family. Current Ribs is z-independent and Spiral has constant helical slope. Historical R9 flowing/wave paths alias, so that code cannot establish two completed motifs. |
| 7 Rugged hex | Missing: no delivered six-sided cell topology. Historical simplistic field/line renderers remain unvalidated intent evidence. |
| 8 Shallow helix | Partial overlap with Spiral: delivered six-start cosine ridges have vertical spacing s and per-ridge turn rise6s. Historical soft spiral exposed band width, softness, direction and turn pitch. Compare the intended band appearance before adding anything; six starts alone do not prove equivalence. |
| 9 Wave flutes | Missing distinctness contract and real source. Rings has no angular variation and forms horizontal bands; it is not an axial waving-flute field. Separate this later from Flowing flutes with a clear appearance gate. |
| 10 Quilted diamond | Missing pillow-and-groove treatment. Current Diamond has flat crowns and linear sides; neither it nor the three cosine fields implements the historical quilt groove/pillow/softness controls. |

Rings is an additional delivered family, outside the original ten-item list.
Source distinction matters: identical enum-name lengths caused aliasing in R16;
R17/R21 still failed crown/pocket recognition and explicit family geometry.
See [R4 field intent](iterations/2026-09-03-p2-r4-closure-pattern-selector/DESIGN.md)
and [R21 validation](iterations/2026-09-03-p2-r21-threejs-interaction-fidelity-recovery/VALIDATION.md).
No completion credit comes from the rejected renderers' ten names or pixel hashes.

## Foundation gaps retained separately from V2

| Original foundation relationship | Current delivery / remaining scope |
| --- | --- |
| Two coaxial pieces/common outside diameter, screw closure, cavity/end thickness | Delivered real source and browser controls; physical fit remains separate. |
| Outside-height/diameter input model and old broad ranges | Superseded by accepted inside dimensions, wall/end thickness and outside-size readouts. Do not restore duplicate dimension inputs or unsafe historical wall/diameter ranges. |
| Split distance/percentage from top, central seam | Source has distance/percentage; current UI has manual lid height or fixed proportional Auto. Explicit editable percentage and original25–75% teaching rule are not delivered UI requirements by default; revisit only as their own gate. |
| Round/polygon with side count | Round delivered; real polygon body/cap/closure integration remains missing. |
| Independent flat/chamfer/rounded top and bottom with size | Current common chamfer geometry is real; independent end families/sizes and rounded/flat choices remain missing. |
| Screw pitch,1/2/3 turns, clearance, depth and form controls | Actual screw source exists; everyday UI fixes these values. Exposing controls and adding rounded/trapezoidal form alternatives need dedicated fit/geometry gates. |
| Drain location/count/diameter/bolt circle | Top/Bottom independently, both/neither and count are delivered. Diameter and placement are source-derived/fixed in the everyday UI. Adjustable diameter/ring circle remain deferred. Current count means center plus ring, not the old preview's all-on-ring convention. |
| Assembled/exploded presentation | Assembled, Body, Lid and Print layout outputs exist; 3D/Cutaway are display modes. Exploded viewing remains absent and is not equivalent to Print layout. |

## V3–V8 — retained roadmap after individual V2 gates

| Phase | Status and complete retained scope |
| --- | --- |
| V3 Fade and relief | Full inward sidewall patterning and wall guards exist. Full/bottom/top/center coverage, depth/density fade, inset/outset/balanced placement and editable seam/end keepouts remain missing. Future relief modes must reconcile with the accepted crest OD and no-collar intent. |
| V4 Labels | Missing real source/UI: none/inset/outset, safe text, preview font, weight, size, relief, orientation, lower/upper/both target, angle, axial position, optional patch and margin. Future OpenSCAD font metadata stays distinct from actual rendered geometry. |
| V5 Attachments | Missing real source/UI: none, lanyard eyelet, captured loop, separate clip/link, keyring tab, bridge handle; fixed/separate presentation; lower/upper target, angle, opening/member/clearance/hole/span/standoff dimensions. Historical accessory annotations are not validated attachments. |
| V6 Alternative closure | Bayonet remains missing as real source: lock angle, lug count, capture, ramp rise, clearance and closed pattern phase. Historical closure accounting is not mating/strength proof. |
| V7 OpenSCAD parity/export | Partly delivered ahead of roadmap order: flattened source fields, deterministic browser compilation, full canonical job identity, actual STL outputs and bounded source/export/default parity. New foundation/V2–V6 features still need real source support, relevant presets and independent export validation; existing parity does not certify absent features. |
| V8 MakerWorld packaging | Deferred: documentation, presets, screenshots, metadata and package validation. Publication needs separate authorization; packaging does not imply physical acceptance. |

Next: [Current Diamond / Recessed diamond study](iterations/2026-09-06-pattern-backlog/DESIGN.md).
No photo is needed for the documented first proposal. If its sunken centers/high
crossings do not match the user's intent, request a close oblique, side-lit photo
of the intended surface. Appearance PASS selects one motif; then freeze a separate
real-source implementation gate. All later items stay queued, not concurrently built.
