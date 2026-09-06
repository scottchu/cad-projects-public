# PF-DIRECT-01 implementation receipt

Owner `/root/pattern_direct_implementation`, reopened geometry implementation.
Status: **frozen direct Spiral pilot, ready for independent validation**.
No approval, UI exposure, live deployment, slicer or physical claim.

## Inputs and source

Baseline `c181dda780a3b9c407ebe3419702419254266792` on
`codex/container-desktop-customizer`. Verified all31 entries in
`inputs/direct-reopen.sha256`, manifest SHA-256
`e39331da5cfefd282cb3b2a5a7e11c9ffc068b683c6b5b5bb6503e6a607449a4`,
before editing. Read the active BRIEF/DESIGN, design repair and failed pilot
receipts. The earlier failed artifacts remain intact.

Current source `openscad/laifen_case_customizer_v1.scad` SHA-256
`d7acb997f128538a58f9905fe5537972202f49be2b0a490f080d95068701631d`.
New durable compiler: `tests/mesh/pattern-families/compile_pilot.mjs`.
Exclusive changes are that source, compiler script and this receipt. No UI,
schema, dependencies, pinned worker, live dist, services or commits changed.

The new direct exterior has192 angular samples and s/16 maximum axial steps,
plus an explicit chamfer-break row. Canonical per-sector horizontal, vertical
and diagonal edges each own at most one field-minus-cone intersection slot.
Crossing triangles split into shared-index polygons, triangulated with at most
three triangles total. The cone/field radial minimum is applied only after
this explicit subdivision. Periodic endpoints share indices. The resulting
exterior uses the original v06 inward SCAD winding,96-sample internal profile,
zipper, floors, threads, cutters, cap overshoot and output transforms.
Smooth and Diamond geometry functions are unchanged. Only Spiral dispatch is
exposed in this pilot; Ribs/Rings and UI remain gated.

Selected Spiral guards check finite dimensions and fields, nominal s4..16 and
d0.1..0.6, bore/thread/entry residuals including the0.01mm chord reserve, the
prescribed conservative triangle estimate for both roles and actual exterior
allocation. No crest-radius shoulder collar or generic-shell path remains in
Spiral. This is the initial direct candidate; no repair cycle was used.

## Exact artifacts and execution

Scratch: `/tmp/pattern-families-direct-r1`. Candidate source/script/runtime/STL
manifest: `candidate.sha256` (8paths), SHA-256
`6f3772ed60afb47845a41c1af149c89b5e7b302c7cb0ab2b7cbe7638234c4749`.
The original compiler script and complete per-role argv/receipts remain there.
The new durable compiler generates the same stress tuple and records complete
argv, diagnostics and pinned runtime hashes; its separate Smooth/Diamond modes
use original source defaults for the independent parity gate.

Pilot: UI D30/H60/W4.6/T3/manual lid25.3, six-start Spiral s4/d0.6,
Bottom7. Source sets device_length55, OD39.2, body/cap bores30/31,
floor3, distance split25.3; closed height66 and seam40.7.

| Artifact | SHA-256 | Compile seconds |
| --- | --- | ---: |
| spiral-body.stl | 1689355bf915535456af607ef57f372ac231bcce34e8c87715bc270d0d8ae840 | 11.751 |
| spiral-cap.stl | 317f1f85c1901f2ef287c4ed8440077045ba55da4aaa73e8da581586a3d433e5 | 7.298 |
| spiral-assembled.stl | 632cc81cdfd7a4416775fad29442f7b6473f0e0b1e4097c86c04bfe728466c36 | 21.058 |

Commands actually run, sequentially from the root:

```sh
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-06-pattern-families/inputs/direct-reopen.sha256
node /tmp/pattern-families-direct-r1/compile_spiral.mjs body
node /tmp/pattern-families-direct-r1/compile_spiral.mjs cap
node /tmp/pattern-families-direct-r1/compile_spiral.mjs assembled
uv run pytest projects/laifen-wave-case/tests/test_openscad_customizer.py -q
```

For each role `body`, `cap`, `assembled`, also executed:

```sh
uv run python /tmp/pattern-families-validation/mesh_probe.py /tmp/pattern-families-direct-r1/spiral-ROLE.stl
/tmp/pattern-families-validation/mesh_certifier /tmp/pattern-families-direct-r1/spiral-ROLE.stl 0.000001
```

Results are `spiral-ROLE-probe.json` and `spiral-ROLE-global.json` in scratch.
The existing independent tools were reused unchanged for implementation
self-check; the separate validator must own acceptance.

## Self-check findings and remaining gates

All9 source-contract tests passed. All3 original written STLs have positive
volume and zero degenerate faces, duplicates, non-two-use edges or
same-direction two-use edges. Body/cap each have one connected component;
assembled has two. Global certifier at1e-6mm reports zero unexpected
nonadjacent intersections and zero T-junctions for all3, without a seam
exception argument. Body/cap/assembled face counts are84878/58954/143464;
volumes are22039.014485/11672.350888/33711.365372 mm³.

No blocker found in this bounded self-check. PF-05 internals and PF-06 shared
phase/chamfer construction are implemented, but detailed protected-feature,
analytic-error, shared seam, drain-count and collision evidence remain owned by
the independent validator. Default Smooth body was compiled as a compiler
smoke check; original Smooth/Diamond byte parity is still pending. Root asked
to freeze immediately after assembly/source checks before widening the matrix.
Visual seam/end review, UI integration, boundary oracle, default family matrix,
formal review, STEP, slicer and physical evidence are not established here.
Next action: independent pilot validation against the frozen candidate manifest;
no source writes until its disposition.
