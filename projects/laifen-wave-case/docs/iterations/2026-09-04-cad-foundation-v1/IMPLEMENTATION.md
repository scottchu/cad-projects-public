# P1 R7 parametric-core refactor implementation

**Owner:** `IMP-CAD-CV1-01`  
**Status:** candidate frozen; independent validation, critique, and formal review pending  
**Verified design fingerprint:** `1c233c8c64f0e7cb87919b601435318f6402a96cd3ad19af0fdb7251e908ed83`  
**Candidate fingerprint:** `6d58e564885c317c62f9b2e89652a9d7f9be04b82df797f9ccc70fc33e99a304`  
**Evidence fingerprint:** `0214bd39e094aed9bf84a0cfedde97cb795a2a946ccb7cd25bb84c989f250acc`

## Result

The standalone `cad/container_generator_v1/` package reproduces the frozen P1
R7 default source geometry and all four reviewed assembly/print placements. It
does not import or mutate `cad/p1_r7_end_chamfer/`. The package exposes a
26-row `PARAMETER_SPECS` registry, immutable input and resolved records, one
pure `derive(params)` boundary, builders that consume only the resolved record,
and exactly four primary STEP entrypoints/outputs.

The only preset is `laifen_wave_r7`; `laifen-wave` is a compatibility alias to
the same defaults. `device_diameter` is explicitly reference-only and has no
fabrication-solid effect. Locked thread, wall, floor, taper, drain, and skin
constants remain visible but are not editable aliases.

No P1 R7 file, continuity record, live/simulator route, slicer/printer state,
package environment, STL, 3MF, or GLB was changed or created.

## Candidate contents

`candidate-files.sha256` freezes 27 files: the complete new package, four STEP
artifacts, and the four assigned tests. `evidence-files.sha256` freezes 42
compact command, inspection, measurement, transform, serialization, and PNG
evidence files. Both manifests use repository-relative paths.

Primary STEP hashes:

| Artifact | Candidate SHA-256 | Frozen P1 R7 SHA-256 |
| --- | --- | --- |
| `body.step` | `02bfc1ca52ef97dcba3451c930408f64d0f383293933f6183029e36409e1c05a` | `3c04d417e3f21c5ef0e3b1d12ff1953ac366ef418fc4792d592a0624ad91982b` |
| `cap.step` | `b9561b34b96667d1af6e84d145c03d9aa319694fbf11f2cc3c0b60d6b6f18cf0` | `0dd09cbd99f4ceb78605ee7eef1a74a315c3f95079d97a4628dffffc70afe82a` |
| `closed.step` | `cca2ea627369c3e2b3ee5c962238e134ecb56eeb878f9ebaf270d3a8751e76a2` | `e72ee16eb4315a2eb93619ecfb3fd363ac89dc5253bb6527de9d71c82444d27c` |
| `print_layout.step` | `cfd674cbbc2b1827d06c17a1daa0e61ed130074b0de205d49d6880939d86f90b` | `80fd95845b51da5266883614f9bf8eff60793a24d5c39b7321c9c6cb16d477a4` |

The byte hashes differ only in the permitted serialization records. A
line-for-line comparison found two changed lines in body/layout and three in
cap/closed: `FILE_NAME` timestamps, `cadgen:sourceHash`, and renamed
`cadgen:sourcePath` for cap/closed. Every other serialized STEP line is
identical. The asserted record-level report is
`scratch/container-generator-v1-implementation/serialization-variance.json`.

## Validation

All commands ran from the repository root with root `uv`/Python 3.12. The
complete exact command ledger and observed durations are frozen in
`scratch/container-generator-v1-implementation/command-results.md`.

| Gate | Command | Result |
| --- | --- | --- |
| Frozen inputs | `shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-04-cad-foundation-v1/inputs/frozen-inputs.sha256` | PASS, 57/57; manifest hash matches the design fingerprint |
| Cheap registry/scope | `uv run pytest projects/laifen-wave-case/tests/test_container_generator_v1_parameters.py projects/laifen-wave-case/tests/test_container_generator_v1_requirements.py -q` | PASS, 28 tests, 0.8 s |
| Standalone/hash guard | `uv run pytest projects/laifen-wave-case/tests/test_container_generator_v1_source_equivalence.py::test_frozen_p1_r7_remains_hash_clean_and_new_package_is_standalone -q` | PASS, 1 test, 1.9 s |
| Native equivalence | `uv run pytest projects/laifen-wave-case/tests/test_container_generator_v1_source_equivalence.py -q -s` | PASS, 3 tests, about 318 s |
| Four exports | `uv run python projects/laifen-wave-case/cad/container_generator_v1/generate.py` | PASS, exactly four STEP outputs, 521.383 s |
| Written STEP | `uv run pytest projects/laifen-wave-case/tests/test_container_generator_v1_step_equivalence.py -q -s` | PASS, 4 tests, about 328 s |
| Manifests | `shasum -a 256 -c .../candidate-files.sha256` and `shasum -a 256 -c .../evidence-files.sha256` | PASS, 27/27 and 42/42 |

Direct old/new native body and cap checks passed validity, solid/face counts,
bounds, centroid, adaptive volume, surface-type census, full rounded vertex
sets, datum values, and construction-law facts. The written suite repeated
these checks on imported STEP, checked source-to-written parity, tested all
seven drains, walls/slopes, the positive shoulder, six-millimetre full-thread
engagement, an actual-solid Boolean cropped to the only possible 0–9 mm thread
overlap zone, and the openings-up nonoverlapping print layout.

CAD inspection on actual imported STEP passed validation and
facts/planes/positioning for 1/1/2/2 occurrences. Baseline-to-candidate
`inspect diff --planes` reported `geometryChanged=false`,
`topologyChanged=false`, and `bboxChanged=false` for every artifact.
Measurements were 219 mm closed outer length, 213 mm cavity-floor separation,
9 mm thread zone, and 46 mm print-layout center spacing. Shoulder and bed align
checks reported zero translation. Closed frames were identity; print frames
were body `(23,0,135)` along +Z and cap `(-23,0,84)` with Rx180.

Actual-STEP snapshots cover body/cap isometric views, both seven-drain ends,
closed exterior, longitudinal bore/floors/thread/shoulder section and closeup,
and print-layout isometric/top views. Visual inspection found no refactor drift:
the diamond skin is continuous, drains remain open, the closed seam and
thread/shoulder relationship are present, both cavities have floors and open
mouths, and both print objects sit openings-up. The contact sheet is
`scratch/container-generator-v1-implementation/snapshots/contact-sheet.png`.

Viewer review URL (verified HTTP 200):
`http://127.0.0.1:3245/Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case?file=cad/container_generator_v1/closed.step.py`

## Requirement coverage

| Requirement | Evidence |
| --- | --- |
| `CV1-ORIGINAL` | Frozen P1 hash guard and static/runtime standalone-package scan pass. |
| `CV1-PARAMETERS` | Registry metadata/default/domain/classification/geometry-sensitivity tests pass. |
| `CV1-DERIVE` | One pure derivation, immutable complete record, pre-BREP invalid-input tests pass. |
| `CV1-SOLIDS` | Native/imported validity, topology, wall, drain, thread, chamfer, skin, and collision checks pass. |
| `CV1-JOINTS` | Named datums plus shoulder/axis/closed and bed-frame placement checks pass. |
| `CV1-OUTPUTS` | Exactly four matching `.step.py`/`.step` pairs are present. |
| `CV1-EQUIVALENCE` | Old/new native and imported STEP geometry, topology, measurements, and placements pass; permitted byte variance is fully enumerated. |
| `CV1-FDM` | Positive stop, <=45-degree slopes, bounded drains, no internal roof, and openings-up layout pass CAD checks. |
| `CV1-BOUNDARY` | No mesh, simulator/live, slicer, printer, or alternate-family output exists. |

## Repairs and remaining limits

Two focused repair cycles were used. The first corrected the expected frozen P1
manifest-entry count from 17 to 20. The second replaced prohibitively dense
global solid-distance/interference operations with topology, full vertex,
mass-property, exact serialized-geometry equivalence, and a focused
actual-solid thread-zone Boolean. Neither repair changed candidate geometry.
A scratch-only review helper also unwrapped a one-item `ShapeList`; it is not
candidate source.

The full global self-intersection inspection did not complete in a bounded
time on the 10,255-face body and was stopped after about 6.5 minutes. Imported
BREP validity, exact non-metadata STEP identity, old/new native and imported
geometry checks, and the focused actual-solid collision test mitigate that
tool-performance gap. The distinct validator should independently reproduce
the highest-risk equivalence/collision gates against the frozen candidate.

This implementation receipt does not approve its own candidate. Slicer/process
acceptance and physical print/fit acceptance remain HOLD. The next action is
read-only work by distinct `VAL-CAD-CV1-01` and `CRIT-CAD-CV1-01` owners on
candidate fingerprint
`6d58e564885c317c62f9b2e89652a9d7f9be04b82df797f9ccc70fc33e99a304`,
followed by `REV-CAD-CV1-01` only if both complete.
