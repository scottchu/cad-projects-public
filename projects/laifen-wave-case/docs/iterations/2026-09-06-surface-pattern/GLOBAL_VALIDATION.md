# SP-VAL-GLOBAL — whole-mesh intersection validation

## Verdict and frozen inputs

**PASS for the two previously open written-mesh gates.** The default Diamond
body, cap, assembled and print-layout STLs and the D39/H60/W4.4/T4/both/N17
Diamond print-layout STL contain no nonadjacent triangle intersections and no
geometric vertex-on-edge T-junctions at a `0.000001 mm` inspection tolerance.

The candidate is commit `8068fbd19b4fd526d6120e7dfd714e9aca217a9b`.
`inputs/candidate-03.sha256` has SHA-256
`412b5e389a85dbaa7ad730870f496639d8dcd2e2129de733b4da1ba1e031fc63`;
all 23 entries verified before and after this task. The five STL hashes match
the immutable values recorded in `VALIDATION.md`:

| Mesh | SHA-256 | Faces | Nonadjacent pairs tested | Intersections | T-junctions |
| --- | --- | ---: | ---: | ---: | ---: |
| Default body | `6789c6b1ade20b205646bcc2e5eb17d22b515e47c6e3fd1fd5688390376f60c8` | 55,772 | 1,787,588 | 0 | 0 |
| Default cap | `e9629eb47fc215a914d6579c77af945d96d935789a44a5cacb7557bd0dbcd514` | 40,510 | 1,522,713 | 0 | 0 |
| Default assembled | `5cfe2f06339bcc3df70dbc7072448789e5078aee9998a6599016298a148260fe` | 96,100 | 5,951,436 | 0 | 0 |
| Default print layout | `73dc750bd9bea35d1e65e4cd05ec7a56b1cc5cdd42faf8a1649455694d83062e` | 96,282 | 3,310,301 | 0 | 0 |
| Wide print layout | `4f42c45b9a847f5de188359cbe710b0d631450901a70173aec4f1e371c7d3041` | 80,098 | 4,487,993 | 0 | 0 |

## Independent method

The previous Python grid attempt was stopped after 95 seconds without a
verdict. This task replaced it with a dependency-free C++17 BVH certifier in
`/tmp/surface-pattern-global/mesh_certifier.cpp`. It parses the original STL
facets, assigns incidence only to coordinates equal within `1e-9 mm`, and
builds separate median-split AABB trees for faces and unique edges.

For faces, it exhaustively visits every BVH-overlapping pair, skips only pairs
sharing an incidence vertex, and applies both noncoplanar segment/triangle and
coplanar projected-triangle predicates. All spatial comparisons use the stated
`1e-6 mm` tolerance; orientation tolerances are scaled by edge length. This is
an actual triangle-pair test, not an inference from watertightness or two-use
edges. The assembled scan permitted only a cross-component contact where both
triangles were entirely on the known `z=135 mm` shoulder plane. It found zero
such allowed contacts, so the allowance did not suppress any reported pair.

For T-junctions, every canonical mesh vertex queries the complete edge BVH.
The test excludes only that vertex's own edge endpoints, requires its
projection to lie more than `1e-6 mm` from either endpoint, and measures the
3D point-to-segment distance. No nonincident vertex lies on an edge within the
inspection tolerance.

Detector fixtures guard against a silent all-pass implementation: two
properly adjacent triangles pass; a noncoplanar crossing fails with one
intersection; coplanar overlap fails with one intersection; and the explicit
T-junction fixture fails with one intersection and one T-junction. The full
five-mesh run completed in 2.43 seconds. Compiler warnings were empty under
Apple clang `-Wall -Wextra -pedantic`.

## Evidence and limits

Temporary evidence is under `/tmp/surface-pattern-global`:

- certifier source SHA-256
  `e8b032376cfd246ea30b8c5c8be39417cffdabb1834771f0ae3683ed9cca7d2d`;
- compiled certifier SHA-256
  `4eea40808e31019d216bd30faed659d2c5ce87a75ea67c4ef9dea56471b7ce14`;
- runner SHA-256
  `f4a9e685adb0e1eb4cf46dba38fbce33b17f5a472fc082fb204994965418d815`;
- machine-readable `receipt.json` SHA-256
  `91665069c635d4cb848baf3c41f3813726d507b3a8580da6eca6b9baba4faaa5`.

Reviewable replay source is retained at
`tests/mesh/surface-pattern-global/`. `CERTIFIER_INPUTS.sha256` has SHA-256
`da6ea9acc8e9ba2aad38cbffa3ede497a2dd5a4c79085a7cce30f29e5d6ba293`
and binds the Candidate 03 manifest, certifier, parameterized runner, fixture
generator, and README. The README gives the exact root-`uv` and `clang++`
commands. Its runner accepts all five STL paths explicitly and rejects bytes
whose hashes differ from this receipt, so it can use the current `/tmp`
evidence or externally restored copies. No binary, mesh, fixture, dependency,
or receipt is retained in the repository. The durable sources passed Python
syntax, warning-clean compilation, and the four fixture expectations; the five
large meshes were not redundantly rescanned during this durability step.

This certifies the five named written triangle meshes at the stated numeric
tolerance. It is not an exact-arithmetic theorem about continuous source, does
not inspect parameter combinations beyond the default and selected wide case,
and intentionally does not classify adjacent face pairs because the open
requirement was nonadjacent self-intersection. Prior validation separately
establishes closed topology, consistent winding, positive volume, zero
degenerate/duplicate faces, field accuracy, openings and protected geometry.
Browser, CAD/STEP, slicer and physical acceptance remain separate.

Exact commands, from the repository root:

```sh
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-06-surface-pattern/inputs/candidate-03.sha256
clang++ -O3 -std=c++17 -Wall -Wextra -pedantic /tmp/surface-pattern-global/mesh_certifier.cpp -o /tmp/surface-pattern-global/mesh_certifier
uv run python /tmp/surface-pattern-global/selftest.py
uv run python /tmp/surface-pattern-global/run_certification.py
shasum -a 256 /tmp/surface-pattern-global/{mesh_certifier.cpp,mesh_certifier,run_certification.py,receipt.json}
```

No product source, build, dependency, service, browser, CAD, mesh, printer or
existing joined validation record was modified. This task writes this global
validation record, temporary certifier evidence, and the reviewable durability
sources under `tests/mesh/surface-pattern-global/`.
