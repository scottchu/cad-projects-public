# P1 R7 parametric-core refactor design

## Frame, identities, and outputs

Use millimetres, XY radial planes, and `+Z` along the screw axis. Preserve the current P1 R7 local geometry: body spans `Z[-135,9]`, cap spans `Z[0,84]`, and the shoulder/seam datum is `Z=0`. `closed.step` contains exactly the body and cap in the reviewed closed placement and measures 219 mm overall. `print_layout.step` contains exactly two occurrences: body translated `(23,0,135)` and cap rotated 180 degrees about X then translated `(-23,0,84)`. Both bed datums are at `Z=0`; object bounding boxes have 7 mm separation.

New source lives only in `cad/container_generator_v1/`. Use these buildable entrypoints and outputs:

- `body.step.py` -> `body.step`
- `cap.step.py` -> `cap.step`
- `closed.step.py` -> `closed.step`
- `print_layout.step.py` -> `print_layout.step`

Recommended internal modules are `parameters.py`, `derive.py`, `surface.py`, `thread.py`, `ends.py`, `parts.py`, `assembly.py`, and `generate.py`. Copying the original P1 R7 algorithms into this package is allowed with source attribution. Importing P1 R7 at runtime or modifying it is forbidden; the new package must stand alone after refactor.

## Parameter contract

`PARAMETER_SPECS` is the only public registry. Each row has stable `id`, group, unit, default, domain, classification, geometry targets, and validation oracle.

### Existing adjustable geometry parameters

| ID | Default | Existing domain/constraint | Geometry effect |
| --- | ---: | --- | --- |
| `device_length` | 208 mm | positive; coupled cavity <=300 | Changes derived cavity and body depth. |
| `axial_allowance` | 5 mm | >=3; coupled cavity <=300 | Adds to cavity/body depth. |
| `cap_cavity_length` | 81 mm | positive; cap/closure feasibility | Changes cap and complementary body lengths. |
| `thread_clearance` | 0.25 mm | 0.20–0.30 | Changes the female thread void only. |
| `outer_diameter` | 39 mm | positive, <=80; wall/skin constraints | Changes common exterior and derived skin count/walls. |
| `skin_axial_pitch` | 4.8 mm | 3–8 | Changes procedural diamond axial period. |
| `skin_arc_pitch_target` | 3.63 mm | positive; derived count 8–128 | Selects the nearest integral circumferential count. |
| `skin_height` | 0.45 mm | >0 and <=0.6; wall/slope constraints | Changes crest-to-valley relief. |
| `plateau_half_fraction` | 0.18 | >0 and <0.5; plateau >=1 mm | Changes the blunt diamond plateau. |
| `skin_phase_theta` | 0 rad | finite/resolvable | Rotates the same procedural skin without seam drift. |
| `skin_phase_z` | 0 mm | finite/resolvable | Translates the same procedural skin phase axially. |
| `end_chamfer_size` | 1.20 mm | 0.80–1.50 and < floor | Changes both existing 45-degree closed-end chamfers. |

`device_diameter=29 mm` is an existing **reference/readout-only** parameter. It derives nominal body/cap radial gaps of 0.5/1.0 mm and never resizes bores or fabrication solids. Its metadata must say `affects_geometry=false`; it cannot satisfy a geometry-sensitivity test.

### Existing locked design constants

Keep these visible in the registry as `locked`, not editable: `body_bore=30`, `cap_bore=31`, `floor=3`, `thread_pitch=2`, `engagement=6`, `clearance_budget=0.30`, `thread_height=0.5`, `root_wall=1.4`, `cap_taper_length=2.2`, `drain_diameter=3`, `drain_ring_radius=9`, `drain_ring_count=6` plus one center hole, and `skin_style="diamond"`. Existing lead/runout laws, thread handedness/form, shoulder geometry, drain placement, end profile, split, and assembly/print poses are also locked. Do not expose them as editable aliases.

The only preset is the exact P1 R7 default, named `laifen_wave_r7`. A compatibility alias may resolve to identical bytes but may not imply a generic or wide-short model.

## Single derivation

`derive(params)` validates finite values and returns one frozen `Resolved` record. Builders accept `Resolved`; calling or reproducing derivation inside surface, thread, end, part, assembly, wrapper, or test code is forbidden.

At the default it computes the existing laws:

- `cavity_length = device_length + axial_allowance = 213`.
- `cap_height = cap_cavity_length + floor = 84`.
- `body_depth = cavity_length - cap_cavity_length = 132`.
- `thread_tool_length T = 1.5*thread_pitch + engagement = 9`; body height is `body_depth + floor + T = 144`.
- `outer_length = cavity_length + 2*floor = 219`.
- `outer_crest_radius=19.5`, `outer_valley_radius=19.05`, body/cap inner radii `15/15.5`.
- `thread_root=16.4`, `thread_crest=16.9`, female minimum wall `1.85`, and overall minimum wall `1.4`.
- `lattice_count=round(2*pi*outer_valley_radius/skin_arc_pitch_target)=33`; derive exact arc pitch, plateau width, slope, bands, and phase from that count.
- `end_chamfer_radius=18.3`, axial height `1.2`, slope `1`, and smooth band `0.75`.
- Drain centers are `(0,0)` plus six positions on radius 9; the cutter spans only its 3 mm floor plus Boolean overshoot.

Preserve all current feasibility checks, including female ligament >=1.8 mm, radial interlock >=0.2 mm, cap taper <=45 degrees, diamond slope <=45 degrees, drain containment, useful shell lengths, and resolvable phase. Invalid input returns errors before any BREP operation.

## Solid and assembly contract

Preserve the P1 R7 construction laws and final trim/runout normalization. Each standalone output is one valid, positive, closed solid. Keep native labels and source-level rigid datums `shoulder`, `tip`, `full_thread_start`, `full_thread_end`, `skin_phase`, `bed`, and `inner_floor`, plus cylindrical `screw_axis`. The body is fixed. Cap axial position for any inspection pose is `thread_pitch*angle_deg/360` about/on the shared axis; default closed placement remains unchanged.

The positive external shoulder defines the closed stop. The approximate device envelope is reference-only, excluded from fabrication outputs, and never participates in joint placement or Boolean geometry. The 5 mm total axial allowance remains mathematical design intent; it does not prove neither-end contact for an unidentified physical print/device.

Preserve openings-up vertical printing. Closed ends sit on the bed and cavities open upward, so the refactor may not introduce an internal roof/ceiling. Actual thread and skin slope checks retain the <=45-degree support assumption. These are CAD/DfAM checks, not slicer or print proof.

## Default equivalence oracle

P1 R7 is immutable and must remain byte-identical. Baseline STEP hashes:

| Artifact | SHA-256 | Required geometry facts |
| --- | --- | --- |
| `body.step` | `3c04d417e3f21c5ef0e3b1d12ff1953ac366ef418fc4792d592a0624ad91982b` | one solid; 10,255 faces; adaptive written volume `65470.38707347599 mm3`; Z[-135,9] |
| `cap_c25.step` | `0dd09cbd99f4ceb78605ee7eef1a74a315c3f95079d97a4628dffffc70afe82a` | one solid; 6,396 faces; adaptive written volume `34973.25082611402 mm3`; Z[0,84] |
| `closed_c25.step` | `e72ee16eb4315a2eb93619ecfb3fd363ac89dc5253bb6527de9d71c82444d27c` | two occurrences/16,651 faces; 219 mm overall; each occurrence equal to standalone |
| `print_layout.step` | `80fd95845b51da5266883614f9bf8eff60793a24d5c39b7321c9c6cb16d477a4` | two occurrences/16,651 faces; bounds `85.0000002 x 38.9965480824 x 144.0000002 mm`; bed delta <=1.1e-7 mm; 7 mm separation |

The new default exports should match those hashes. This contract declares only this narrow fallback serialization variance: a different new-file STEP hash is admissible when generation headers, path metadata, or XCAF label serialization differ, provided the implementation identifies the differing records and all imported geometry checks pass. Geometry variance is forbidden. For each part require identical solid/face counts, bidirectional shape distance <=`1e-6 mm`, bounds/centroid/key datum deltas <=`1e-6 mm`, and adaptive volume delta <=`0.001 mm3` at eps `1e-10`. Closed/layout occurrence transforms and per-occurrence comparisons must meet the same limits. Any other hash difference is a blocker.

Check source-native old versus new body/cap solids directly once at defaults. Also require new source-native to new written-STEP adaptive volume parity <=`0.001 mm3`; do not round-trip STEP as the source oracle.

## Risk-driven tests and evidence order

1. `tests/test_container_generator_v1_parameters.py`: registry completeness/classification; exact defaults/locked values; single-derive equations; invalid/boundary/coupled constraints; reference-only diameter has no solid effect.
2. `tests/test_container_generator_v1_source_equivalence.py`: P1 R7 remains hash-clean; new source contains no downloaded geometry or old-runtime import; default old/new native body and cap satisfy topology, distance, mass-property, datum, thread, drain, chamfer, skin, and collision equivalence.
3. `tests/test_container_generator_v1_step_equivalence.py`: four explicit exports validate; source-to-STEP parity; baseline-to-new STEP equivalence; occurrence labels/placements; same OD/seam, positive shoulder, thread engagement, no unexpected solid intersection, and print-layout nonoverlap/bed orientation.
4. `tests/test_container_generator_v1_requirements.py`: traces `CV1-*`, asserts all deferred features and mesh exports absent, confirms only four STEP outputs, and rejects editable locked/inert parameters.

Run cheap parameter and source guards first. Then generate only the four entrypoints with the installed CAD `scripts/gen ... --write`. For each written STEP run `scripts/inspect validate` and `scripts/inspect refs --facts --planes --positioning`; use targeted `measure`, `align`, and `frame` for the named datums, assembly axis/stop, overall lengths, and print bed. Record actual-solid collision/intersection volumes rather than relying on bounding boxes.

After deterministic PASS, render mandatory snapshots with the installed CAD `scripts/snapshot`: body, cap, closed exterior, closed section showing bore/thread/shoulder/floors, both end/drain closeups, and print layout. Critique the actual new STEP, not source-only previews. Do not produce STL or 3MF until written STEP, independent validation, critique, and formal review all PASS.
