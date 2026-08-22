# P14 standalone PETG rod-fit coupon

- Model: one-piece physical fit coupon; no mechanism dependency or modification.
- Units: millimetres.
- Coordinate convention: centered in XY, lower face at Z=0, +Z thickness.
- Overall body: 40 x 42 x 3 mm, with a 4 mm clipped upper-left traversal datum.
- Stations: 3 x 3 row-major grid, 14 mm pitch, labeled 4.00 through 4.40 mm in 0.05 mm increments.
- Physical control: 4.00 mm is the known too-tight press control; larger stations are ascending insertion candidates.
- Bore entrances: 0.28 mm radial x 0.28 mm axial chamfer at both faces, exactly 45 degrees.
- Cylindrical land: 2.44 mm between chamfers (minimum contract 2.40 mm).
- Material margins: measured from the widest chamfer entrance envelope; minimum ligament and outline edge wall must both be at least 3.00 mm.
- Label margin: actual build123d text bounds must retain at least 1.00 mm to the outline; the default layout retains approximately 1.544 mm.
- Labels: unique engraved numeric diameter directly below every bore; upper-left clip establishes start and traversal direction.
- Primary artifact: `cad/p14_rod_fit_coupon/p14_rod_fit_coupon.step`.
- Secondary artifact: one-object, millimetre-unit, manifold and oriented `cad/p14_rod_fit_coupon/p14_rod_fit_coupon.3mf`.
- Validation: focused source/BREP tests, STEP round trip, 3MF round trip, CAD CLI facts/planes/positioning and validate, top and isometric snapshots.
- Physical boundary: CAD checks do not establish the winning printed fit; print flat in the intended PETG profile and test the same rod without forcing it.
