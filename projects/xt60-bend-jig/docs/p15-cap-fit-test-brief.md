# P15 actual PETG cap-fit test

- Model: three separate removable-cap specimens; no mechanism dependency or modification.
- Units: millimetres.
- Coordinate convention: XY printer bed, closed end at Z=0, socket opening along +Z.
- Actual cap envelope: 7.00 mm OD x 3.80 mm high, matching P13.
- Socket candidates: 4.05, 4.10, and 4.15 mm from left to right.
- Retention geometry: 3.60 mm entry throat, 0.60 mm throat depth, 0.60 mm radial flex slit.
- Blind base: 0.80 mm continuous closed floor.
- Identification: one, two, or three shallow exterior notches opposite the slit map to 4.05, 4.10, and 4.15 mm respectively.
- Print orientation: all caps upright on their closed ends; no rod and no support geometry included.
- Primary artifact: `cad/p15_cap_fit_test/p15_cap_fit_test.step`.
- Secondary artifact: three-object, millimetre-unit, manifold and oriented `cad/p15_cap_fit_test/p15_cap_fit_test.3mf`.
- Validation: named parameters, three valid positive solids, 7.00 x 7.00 x 3.80 mm specimen envelopes, preserved 0.80 mm bases, non-overlapping stations, STEP/3MF round trips, mandatory isometric and top snapshots.
- Physical boundary: CAD verifies nominal geometry only. Print in the intended PETG profile and test the purchased Ø4 x 50 mm stainless rod; cap insertion force, retention, creep, and repeat removal remain physical acceptance tests.
