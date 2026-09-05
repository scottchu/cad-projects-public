# Frozen intake — P2 R5 cross-section generator

R5 supersedes R4 before implementation. Carry forward every R4 visual selector unchanged: screw/bayonet closure, end-profile family, closed seam phase matching, recessed diamond, knit stitch, micro flutes, rugged hex, envelopes/fades, optional accessories, visual-only labels and continuous core OD/no collar.

Add `crossSectionMode∈{round,regular_polygon}`, integer `sideCount` 3…32 (prominent presets 3,4,5,6,7,8), `cornerRoundness∈[0,1]`, and `sectionRotationDeg∈[0,360)`. Both core halves share one cross-section/frame. In assembled state closure must align both shape and pattern. Nominal OD is maximum across-corners diameter in polygon mode; all displayed core/accessory envelopes must state that interpretation and never silently grow.

The supplied `7DA5E007-FCC1-452B-94E8-32E1C0C7474E/1-Pasted-Image-1.jpg` is visual evidence only for cross-section/proportion interest. It imports no geometry, dimensions, topology, closure, texture, mesh, or manufacturing claim.

R4 implementation was interrupted before any candidate freeze. A new R5 implementer must inventory partial R4 paths and either quarantine them as non-candidate or start clean; no partial R4 file is authority. P1 R7, CAD/OpenSCAD/STEP/slicer/printer/MakerWorld claims, routes, services, and served P2 R3 copy remain forbidden.

`CEF85E27-66CF-4D60-9B0C-B3844C4D29FC/1-Pasted-Image-1.jpg` is visual evidence only for flowing vertical-groove character. It imports no geometry, dimensions, topology, texture mesh, or manufacturing claim. Add original `flowing_flutes`: a periodic groove field whose angular centerline is sinusoidally displaced over global Z. Reuse flute count/duty/depth and add only wave amplitude/wavelength plus phase/direction. Preserve global Z, closed angular phase matching, constant pitch/no Z scaling, and deterministic seam/sensitivity tests.
