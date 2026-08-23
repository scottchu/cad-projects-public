# Implementation log

Generator: `upright_fin_simulator`  
Status: implementation complete; pending independent evaluator verdict.

## Actions

- Added isolated frozen contract and build123d geometry modules for the V0
  fixture; preserved simulator and historical P0 fixture.
- Generated primary assembled/exploded STEP plus four individual STEP files
  with the CAD skill generator.
- Added exact source/math/geometry/motion/STEP/artifact tests.
- Ran the 5-degree dense relative-rotation BREP sweep. Lower carriers and all
  carrier pairs remain collision-free; the hour/body overlap stays limited to
  the three intended split-collet pads.
- Generated four manifold STL files and a named exactly-four-object 3MF. The
  first raw OCC STL pass exposed nonmanifold face seams; the exporter was
  corrected to emit the same welded validated exterior mesh as the 3MF.
- Verified actual OrcaSlicer loading.
- Ran CAD CLI validation on all six STEP files: every occurrence is closed,
  valid, and positive-volume.
- Generated and reviewed five mandatory assembly/exploded snapshots.

## Implementation results

- Exact printed part count: 4.
- Assembly STEP imported bounds: `90 × 90 × 41.769231 mm`; four solids.
- Individual bounds meet the frozen ±0.05 mm contract.
- Source/individual STEP bidirectional geometry difference: below `1e-5 mm³`.
- Export manifest remains `pending_independent_review`; implementation does not
  self-approve.

## Remaining physical gates

Force, friction, wear, runout, collet durability, LED heat safety, and real
shadow quality are unverified until a physical print. This fixture is not
compatible with a real quartz movement.

## Tooling note

`inspect validate` passes all six STEP artifacts. `inspect refs --facts` on the
assembled render package reports a `110.055 × 110.047 mm` occurrence extent,
while direct STEP import, source equality tests, and snapshots show the actual
assembly envelope is `90 × 90 mm`. This appears to be occurrence-transform
accounting in the render-package facts view and is left for the evaluator to
independently assess; the STEP BREP itself is frozen and tested.

## V0R1 compact representative-quartz export checkpoint

- Added an isolated V0R1 exporter without changing the accepted V0 package.
- Exported exactly four named secondary print objects: representative quartz
  body, hour carrier, minute carrier, and second carrier.
- Generated one welded STL per part and a named four-object 3MF at
  `models/v0r1_compact_quartz_fixture/print/`.
- Recorded source STEP, print meshes, primary assembly STEP, hashes, dimensions,
  and physical-test caveats in `v0r1_manifest.json`.
- Kept the manifest at `pending_independent_review`; implementation does not
  self-approve V0R1 or claim compatibility with a purchased quartz movement.
- Added the V0R1 print/assembly/optical/LED safety procedure under `docs/`.
