# Evaluation round 001

Verdict: ACCEPT for V0 physical prototype printing.

Evidence:
- 12/12 focused V0 tests and 127/127 repository tests passed.
- Six STEP files validate as closed, positive-volume solids; assembled/exploded contain exactly four occurrences.
- Direct BREP envelope is 90 × 90 × 41.769231 mm; STEP/source difference is below 1e-5 mm³.
- Dense 5° rotation sweep found no lower/body or carrier-pair collisions; hour/body overlap is confined to intended split-collet pads.
- Four STL and four named 3MF meshes are watertight, manifold, single-shell; Orca import passed.
- Snapshot review confirmed body + three annular carriers, three spokes and one rounded upright fin per carrier, correct Z order, stepped arbor, and support-free print poses.
- The 110 mm `inspect refs` extent is a tooling transform artifact; direct BREP, assembly descriptor, raw topology, and meshes all show 90 mm.

Physical-only gates: collet force/durability, journal fit, friction, wear, runout, rotational feel, real shadow quality, LED brightness and thermal safety.

Limitation: V0 is not compatible with a real quartz movement.

Route: done.

