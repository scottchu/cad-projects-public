# PF-DES pilot topology assessment

Verdict: **reject the current CSG pilot; return to the prescribed direct-shell
topology for the focused repair.** Do not advance this candidate to the UI.

Read source SHA-256
`b800269748da4e35ebc6a0f2d438e17d776762e824bc05b3fc9f0a2e39fcf90c`,
its exact diff against `c181dda780a3b9c407ebe3419702419254266792`,
PILOT_IMPLEMENTATION.md, and the retained compiler script. The script's
device_length55 correctly represents UI inside height60 with axial_allowance5;
outside height is66 and body_thread_z40.7 for the25.3mm cap.

The implementation replaced prescribed direct profile/zipper construction with
a192-angle raw exterior, CSG intersection against the existing envelope, and
generic shell Boolean operations. It suppresses the external shoulder collar.
This is an explicit algorithm deviation, not prior compliance with DESIGN.md.

In principle a native CSG intersection can own an actual chamfer intersection,
preserve protected96-sample bores and remove the need for a bespoke zipper.
It would need original written-mesh topology, seam, protected-feature and field
error evidence before being accepted as an alternative. The existing96-facet
envelope additionally clips crest peaks along the straight wall: its maximum
radial deficit is `R*(1-cos(pi/96))`, approximately0.02142mm at R40 and0.01050mm
at pilot R19.6. This effect belongs in any such alternative's error budget.

That conditional alternative is superseded by the independent pilot failure
reported by root during this assessment: body8055 intersections/151 T-junctions,
39 non-two-use edges/52 degenerates/12 duplicates; cap2513 intersections,
695 T-junctions/275 degenerates; assembly19015 intersections/966 T-junctions.
The validator's PILOT_VALIDATION receipt owns the exact commands, artifacts,
interpretation and provenance; these reported results are not this role's tests.
Compilation success does not outweigh these actual written-mesh failures.

Restore the prescribed direct exterior/profile construction, owned chamfer
intersection subdivisions and96-sample inner-profile zipper. Preserve the
same small pilot tuple and rerun failed topology gates before parity or broad
UI work. Do not repair STL files or weaken certification to accept this pilot.
Do not assume CSG clipping alone is the diagnosed cause: face orientation,
boundary ownership and integration may also contribute; the implementation
owner must inspect source topology while making the bounded repair.

New-family ligament and allocation assertions are also absent from this pilot;
they remain required before any arbitrary-parameter exposure. No geometry
contract was amended by this assessment. Existing DESIGN geometry and pilot
requirements remain active; this document changes no source, artifact or live build.
