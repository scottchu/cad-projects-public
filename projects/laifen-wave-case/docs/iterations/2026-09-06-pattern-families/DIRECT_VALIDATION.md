# PF-DIRECT-VAL — independent direct-pilot validation

## Verdict

**PASS for the repaired Spiral pilot; proceed to the bounded five-family and UI
gates in `VALIDATION_PLAN.md`.** This validates only the frozen direct-pilot
source and three written Spiral artifacts. It does not approve broader family
implementation, browser delivery, STEP/CAD, slicing, printing or physical use.

## Frozen provenance

`/tmp/pattern-families-direct-r1/candidate.sha256` has SHA-256
`6f3772ed60afb47845a41c1af149c89b5e7b302c7cb0ab2b7cbe7638234c4749`;
all 8 entries passed before and after validation. The source SHA-256 is
`d7acb997f128538a58f9905fe5537972202f49be2b0a490f080d95068701631d`.
`DIRECT_IMPLEMENTATION.md` has SHA-256
`548f792ca924e00dbacc28ed285af26d4baf956b9b6bf5625612ba8d2166e824`.
Pinned JS/WASM hashes are `904a47f29e63afb597bedef747da3b457d8ea17cc793c462c6c8b444e918a62e`
and `f72ce246c02c0e501990837102be383326b153fd761774ebfacce5c80c5ecf26`.

## Written-mesh stop gate

I rebuilt the durable C++17 certifier warning-clean, passed its adjacent,
crossing, coplanar and T-junction fixtures, then scanned the original frozen
STLs at `1e-6 mm` without a seam exception.

| Artifact | SHA-256 | Faces | Components | Volume mm³ | Pairs tested | Intersections / T-junctions |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Body | `1689355bf915535456af607ef57f372ac231bcce34e8c87715bc270d0d8ae840` | 84,878 | 1 | 22,039.014485 | 1,795,994 | 0 / 0 |
| Cap | `317f1f85c1901f2ef287c4ed8440077045ba55da4aaa73e8da581586a3d433e5` | 58,954 | 1 | 11,672.350888 | 1,537,976 | 0 / 0 |
| Assembled | `632cc81cdfd7a4416775fad29442f7b6473f0e0b1e4097c86c04bfe728466c36` | 143,464 | 2 | 33,711.365372 | 5,973,967 | 0 / 0 |

Every mesh has positive outward signed volume and zero non-two-use edges,
same-direction two-use edges, degenerate faces and duplicate faces. This closes
the failed pilot's negative-orientation, intersection and T-junction regression.

## Protected and exterior geometry

- The Body and Cap share exactly 192 identical seam XY vertices at global
  `z=40.7 mm`; seam radii span 18.999999998–19.6 mm, proving shared phase.
- First internal radial hits match freshly compiled stress-tuple Smooth controls
  at 240 Body and 624 Cap angle/height samples. Maximum deltas are 0 and
  `1.07e-14 mm`. Samples cover straight bores, male thread and female entry,
  groove, runout and bore regions away from section break planes.
- Measured bores are 15 and 15.5 mm. Off-hole floor intervals are Body 0–3 mm
  and Cap 22.31–25.3 mm, retaining the 0.01 mm Cap overshoot.
- A Body section at `z=1.234567 mm` has one outer loop plus seven drain loops:
  one center at radius 0 and six centers on radius 9 mm.
- Near the seam, Body `z=40.2` and Cap local `z=0.5` have radial excursions
  0.599971 and 0.599818 mm. The pattern reaches both sides; no smooth external
  collar is present.
- The independent exterior classifier selects radial-facing triangles by the
  protected/exterior radius separation, then evaluates vertices, three edge
  midpoints and centroids against the analytic Spiral field and chamfer clip.
  Body covers 63,768 faces/446,376 samples with maximum error 0.0061655 mm;
  Cap covers 40,368/282,576 with maximum 0.0061151 mm. Both pass 0.025 mm,
  including the inherited conical-envelope facet contribution.
- Assembled has two components, zero globally detected surface intersections,
  and volume differs from Body+Cap by only `-2.13e-9 mm³`; no positive-volume
  interference is detected.

## Exact Smooth and Diamond parity

I extracted baseline source from commit `c181dda780a3b9c407ebe3419702419254266792`
and freshly compiled baseline and candidate with the same pinned WASM. `cmp`
passed for all eight pairs:

| Style | Body | Cap | Assembled | Print layout |
| --- | --- | --- | --- | --- |
| Smooth | `db78a5eb2a24a16d47ae0e8837003115ee573812016ef443715997aea07474a2` | `646efb49c116b47b49521872c0e35af724053f9fbaa619c412aca40009e0b7d0` | `b1b9db18e21cafed5237afb90e57831b72246c6ac2e4b4c88f736738fd0cf169` | `5b6aac9189e489869982e3786bc681289a3edfffe073fd7f10c93c49f493ff34` |
| Diamond | `6789c6b1ade20b205646bcc2e5eb17d22b515e47c6e3fd1fd5688390376f60c8` | `e9629eb47fc215a914d6579c77af945d96d935789a44a5cacb7557bd0dbcd514` | `5cfe2f06339bcc3df70dbc7072448789e5078aee9998a6599016298a148260fe` | `73dc750bd9bea35d1e65e4cd05ec7a56b1cc5cdd42faf8a1649455694d83062e` |

## Commands and evidence

```sh
shasum -a 256 -c /tmp/pattern-families-direct-r1/candidate.sha256
clang++ -O3 -std=c++17 -Wall -Wextra -pedantic projects/laifen-wave-case/tests/mesh/surface-pattern-global/mesh_certifier.cpp -o /tmp/pattern-families-direct-validation/mesh_certifier
uv run python projects/laifen-wave-case/tests/mesh/surface-pattern-global/selftest.py --output-dir /tmp/pattern-families-direct-validation
for role in body cap assembled; do
  /tmp/pattern-families-direct-validation/mesh_certifier "/tmp/pattern-families-direct-r1/spiral-$role.stl" 0.000001
  uv run python /tmp/pattern-families-validation/mesh_probe.py "/tmp/pattern-families-direct-r1/spiral-$role.stl"
done
uv run python /tmp/pattern-families-direct-validation/feature_probe.py
git show c181dda780a3b9c407ebe3419702419254266792:projects/laifen-wave-case/openscad/laifen_case_customizer_v1.scad > /tmp/pattern-families-direct-validation/parity-baseline/baseline.scad
for style in smooth diamond; do for role in body cap assembled print_layout; do
  node projects/laifen-wave-case/tests/mesh/pattern-families/compile_pilot.mjs /tmp/pattern-families-direct-validation/parity-candidate "$role" "$style" projects/laifen-wave-case/openscad/laifen_case_customizer_v1.scad
  node projects/laifen-wave-case/tests/mesh/pattern-families/compile_pilot.mjs /tmp/pattern-families-direct-validation/parity-baseline "$role" "$style" /tmp/pattern-families-direct-validation/parity-baseline/baseline.scad
  cmp "/tmp/pattern-families-direct-validation/parity-candidate/$style-$role.stl" "/tmp/pattern-families-direct-validation/parity-baseline/$style-$role.stl"
done; done
```

The 57-entry evidence manifest
`/tmp/pattern-families-direct-validation/evidence.sha256` passes and has SHA-256
`6762e16dcc03b0066821d6b0e7de068ef68bbf409cd4dfc707c6af52c931ff91`.
Primary feature receipt SHA-256 is
`47f74d667125e25f34601a39e53cc6e5461d570d9cfdf6877a8c2bf0fd6febaa`.
This validator wrote only this receipt and task scratch evidence; source,
product tests, browser, services and historical receipts were not modified.
