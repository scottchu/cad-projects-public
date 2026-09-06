# PF-PILOT-VAL — independent feasibility validation

## Verdict

**FAIL; stop the Spiral pilot before protected-feature and parity work.** All
three exact written artifacts fail the first required geometry gate. This
verdict is independent of whether the design later permits envelope CSG: the
returned STL meshes themselves contain nonadjacent intersections, geometric
T-junctions and degenerate faces. Body and assembled also contain non-two-use
edges and duplicate faces. No browser, service, product build, source,
dependency, slicer or printer action was performed.

## Frozen inputs

- SCAD SHA-256:
  `b800269748da4e35ebc6a0f2d438e17d776762e824bc05b3fc9f0a2e39fcf90c`.
- `PILOT_IMPLEMENTATION.md` SHA-256:
  `5c343732811a3f166c163c2e1a14ab414c1052dad8192457cbc76b94a908803f`.
- Body SHA-256:
  `71914b7d35dd75d0807b41309fb72bf7420e352bdd63eeb0fe2d27aca8be06fc`.
- Cap SHA-256:
  `c33e58dab14d5f525a664f1cfb48e470ceb03ef0cd8839d3d69003e5beeab4e9`.
- Assembled SHA-256:
  `a7008ef90eb992640ee94398b5ebcfb89abb884955636e2078346d4b02a77428`.

All five hashes matched before inspection. The certifier source was the
durable surface-pattern global certifier, SHA-256
`e8b032376cfd246ea30b8c5c8be39417cffdabb1834771f0ae3683ed9cca7d2d`.
Apple clang produced the previously proven identical binary SHA-256
`4eea40808e31019d216bd30faed659d2c5ce87a75ea67c4ef9dea56471b7ce14`
with an empty warnings file.

## Actual mesh results

The exhaustive BVH checks used `1e-6 mm`; assembled allowed the intended
global seam plane at `z=38.7 mm`, but zero findings qualified for that narrow
allowance.

| Artifact | Faces | Components | Nonadjacent intersections | Geometric T-junctions | Non-two-use edges | Degenerates | Duplicate faces | Signed volume mm³ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Body | 97,212 | 1 | 8,055 | 151 | 39 | 52 | 12 | -19,547.909457 |
| Cap | 67,146 | 1 | 2,513 | 695 | 0 | 275 | 0 | -11,671.256489 |
| Assembled | 163,264 | 1 | 19,015 | 966 | 136 | 265 | 10 | -31,218.608636 |

All magnitudes are nonzero, but all three are oppositely oriented. The same
probe reports positive `65,263.241380 mm³` for the accepted Diamond body, with
zero degenerates and non-two-use edges, so the sign is not a probe convention.
Body edge multiplicity is 38 edges used four times and one used six times;
assembled has 136 edges used four times. Cap's two-use topology does not rescue
its intersections, T-junctions, degenerates or orientation.

## Concrete counterexample

Body faces 1355 and 69245 share no exact vertex. Face 1355 has vertex
`P=(-13.418874328679,-13.801372613179,0.856475376740)`. `P` lies strictly
inside face 69245 with barycentric coordinates
`(0.607459346714,0.323303111833,0.069237541453)`; every coordinate is positive.
Face 69245's vertices are:

```text
(-13.602737440185,-13.602737440185,0.837175774800)
(-13.174884090956,-14.066680580317,0.883338664819)
(-12.945048109564,-14.305259670971,0.900363979543)
```

This is an actual nonincident vertex in another triangle's interior, providing
both a geometric T-junction and a nonadjacent intersection witness in the Body
STL. It is not inferred from edge counts.

## Commands and evidence

From the repository root:

```sh
clang++ -O3 -std=c++17 -Wall -Wextra -pedantic \
  projects/laifen-wave-case/tests/mesh/surface-pattern-global/mesh_certifier.cpp \
  -o /tmp/pattern-families-validation/mesh_certifier
/tmp/pattern-families-validation/mesh_certifier \
  /tmp/pattern-families-pilot/spiral-body.stl 0.000001
/tmp/pattern-families-validation/mesh_certifier \
  /tmp/pattern-families-pilot/spiral-cap.stl 0.000001
/tmp/pattern-families-validation/mesh_certifier \
  /tmp/pattern-families-pilot/spiral-assembled.stl 0.000001 38.7
uv run python /tmp/pattern-families-validation/mesh_probe.py \
  /tmp/pattern-families-pilot/spiral-body.stl --examples 1355:69245
uv run python /tmp/pattern-families-validation/pair_witness.py \
  /tmp/pattern-families-pilot/spiral-body.stl 1355 69245
```

The three certifier receipt hashes are respectively
`69642175e02aabe35cd50c4a6bd77ed23568ae0c77025f1946af93e2a094e5a5`,
`a7745ccb2296a33e83c89041fea081097319a1c42ef2101f46671ce8d90e293c`
and `80d497664e50e2f379e2a682184c202306e4dda48ce7236d421a5c5c2cea6f40`.
The detailed Body probe and intersection witness hashes are
`e2634bff3a359ffc6f61a4a5785899f881136a7d0b071e1c82acca37b6154b3f`
and `ffc608a0c50818ade0b5a9b44d9c6f33c7cc435f315bd6b1028a5117fa006d64`.
The probe and witness source hashes are
`13588c3860339c1db9a4cb07d2a86907608a30a7085528a95f8bec34a8af2948`
and `97c3cad2cc99571188164aa65366abf47f4d5cf71209ed61f92eca7b0567f6b0`.
All complete evidence and scripts remain under
`/tmp/pattern-families-validation`. Their 23-entry `evidence.sha256` manifest
passes and has SHA-256
`20928d4ed2ef1e9eea87e6f7553b067239b71d8b260e5e68fcc47595c24d7443`.

Per the prescribed stop rule, the validator did not run fresh Smooth/Diamond
parity compilation, protected bores/floors/threads, seven-drain, seam-ring,
no-collar, analytic exterior-error or collision checks. The smallest next step
is a source repair that returns closed, positive-oriented, nondegenerate
Body/Cap meshes without nonadjacent intersections or geometric T-junctions;
rerun this first gate on new frozen artifact hashes before any later pilot work.
