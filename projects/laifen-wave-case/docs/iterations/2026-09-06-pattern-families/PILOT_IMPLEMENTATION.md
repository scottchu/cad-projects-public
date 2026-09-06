# PF-PILOT implementation receipt

Status: Spiral source pilot compiled; independent topology, protected-feature,
phase, parity, and visual review remain required.

## Frozen inputs

Baseline: `c181dda780a3b9c407ebe3419702419254266792`.
`inputs/design.sha256` was verified at
`9866b1c43c45ab0e5e7c29883985aa28fcab90bd67cb01228144435b86bc9679`
before editing. The resulting SCAD source SHA-256 is
`b800269748da4e35ebc6a0f2d438e17d776762e824bc05b3fc9f0a2e39fcf90c`.

## Source change

`openscad/laifen_case_customizer_v1.scad` adds the `spiral` dispatch and fixed
Spiral source fields `wave_spacing` and `wave_depth`. It creates a 192-angle,
global-Z six-start cosine valley field, using the same body/cap seam datum.
The raw exterior is intersected with the existing conical body/cap envelopes,
so the chamfer is owned by the existing Boolean clipping surface rather than a
vertex-only radial minimum. Smooth and Diamond functions were not edited.
The generic body shoulder is suppressed for active Spiral.

## Pinned-WASM pilot artifacts

All artifacts are in `/tmp/pattern-families-pilot`; the copied pinned runtime
hashes are `openscad.js` `904a47f29e63afb597bedef747da3b457d8ea17cc793c462c6c8b444e918a62e`
and `openscad.wasm` `f72ce246c02c0e501990837102be383326b153fd761774ebfacce5c80c5ecf26`.

The exact pilot argv sets D30/H60/W4.6/T3/manual lid25.3 through
`device_length=55`, `outer_diameter=39.2`, `body_bore=30`, `cap_bore=31`,
`floor_thickness=3`, `split_distance_from_top=25.3`, Spiral spacing4/depth.6,
Bottom7, and the named output mode.

| Artifact | SHA-256 | Compile ms |
| --- | --- | ---: |
| `spiral-body.stl` | `71914b7d35dd75d0807b41309fb72bf7420e352bdd63eeb0fe2d27aca8be06fc` | 1687.78 |
| `spiral-cap.stl` | `c33e58dab14d5f525a664f1cfb48e470ceb03ef0cd8839d3d69003e5beeab4e9` | 1103.21 |
| `spiral-assembled.stl` | `a7008ef90eb992640ee94398b5ebcfb89abb884955636e2078346d4b02a77428` | 3739.44 |

Command run:

```sh
node /tmp/pattern-families-pilot/compile_spiral.mjs body
node /tmp/pattern-families-pilot/compile_spiral.mjs cap
node /tmp/pattern-families-pilot/compile_spiral.mjs assembled
uv run pytest projects/laifen-wave-case/tests/test_openscad_customizer.py -q
```

The source-contract check passed: 9 tests, 0 failures. The pilot compiler
script and the three JSON receipts are retained beside the artifacts. Its
artifact names and argument vector are suitable inputs for the prescribed mesh
certifier and root-owned local Viewer snapshot.

## Limits and next action

This is not an approval of Spiral geometry. The pilot deliberately stops before
UI/schema work. It has not established the requested explicit shared-edge
chamfer subdivision, v06 inner-profile/96-zipper reuse, source parity of old
Smooth/Diamond STL bytes, mesh certificate, exterior-error bound, seam ring
identity, protected internal geometry, or visual review. The independent
validator must assess those gaps before any continuation; if the CSG envelope
clip is insufficient for the required owned-intersection contract, reopen the
geometry design rather than treating the pilot as a production path.

## PF-PILOT repair 1 disposition

Independent written-mesh certification rejected this pilot's CSG/generic path:
the reported body result had 8,055 unexpected intersections, 151 T-junctions,
39 non-two-use edges, 52 degenerates, and 12 duplicate faces; cap and assembled
results also failed. No source repair was made after that frozen evidence.

The prescribed direct path cannot safely be produced by a local substitution in
`v06`. Its owned trim intersections are indexed in a field-coordinate slot that
is shared across every angular sector. A Spiral radius is a function of both
sector angle and global Z, so each angular sector crosses the chamfer at a
different location. Replacing `v06_xyz` radius or adding a per-vertex minimum
would retain the invalid cusp bridge that the design forbids. A correct repair
needs a new sector-specific clipped-grid ownership model and matching 96-sample
inner zipper, then explicit shared-edge intersection allocation. That is a
geometry redesign, not a bounded repair to the rejected construction.

Stop condition reached: reopen the direct-mesh algorithm before another source
candidate. Preserve `/tmp/pattern-families-pilot` as the failed evidence; do
not use its artifacts for acceptance.
