# OSC-05 recovery handoff

**Status:** design frozen; implementation not started  
**Owner:** OSC-05  
**Baseline:** OSC-04 OpenSCAD Customizer V1 source and contract

Implement only the named `THREAD_EMBED_EPS` constructive-overlap correction, exact-OD round/smooth shell correction, and any bounded diamond compile adjustment required by `DESIGN.md`. Preserve source path, user-visible controls/defaults, selectors, formulas, closure shoulder, phase matching, drainage modes, and deferred feature list. Do not edit build123d/CAD/STEP, routes, slicer, printer, or prior iteration records.

The implementation worker must freeze source and focused tests, compile native OpenSCAD temporary STLs, validate watertight positive-volume outputs, and capture required snapshots before handing the same candidate to distinct critique and validation owners. One design revision is the maximum before implementation.
