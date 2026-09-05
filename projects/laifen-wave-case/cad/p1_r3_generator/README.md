# Generic threaded cylinder generator

This original parametric generator builds a closed-bottom cylinder, a screw cap and a continuous mathematical diamond skin. The default short prototype is under independent CAD review. It is not a print release or a verified Laifen case.

Run every command from the repository root through its shared uv environment. Derive dimensions and check constraints without generating CAD:

```sh
uv run python projects/laifen-wave-case/cad/p1_r3_generator/generator.py --preset short-grip --dry-run
uv run python projects/laifen-wave-case/cad/p1_r3_generator/generator.py --cavity-length 82.1 --cap-height 43.4 --dry-run
```

Regenerate real BREP geometry and write STEP:

```sh
uv run python projects/laifen-wave-case/cad/p1_r3_generator/generator.py --preset short-grip --write-step --target all
```

The command writes to `generated/<parameter-fingerprint>/` and records exact parameters, derived dimensions, generating-source hashes and artifact checksums in `manifest.json`. It reimports the files and checks solid validity/counts. Those checks do not replace independent geometric, slicer or physical validation. `--target` accepts `body`, `cap`, `coupons`, `closed`, `exploded`, `print-layout` or `all`; `--output-dir` changes the parent output directory. `--dry-run` and `--write-step` are mutually exclusive.

The seven default review targets are `body.step`, `cap_c20.step`, `cap_c25.step`, `cap_c30.step`, `closed_c25.step`, `exploded_c25.step` and `print_layout.step`. Their matching `.step.py` entries call the same authoritative builders. Viewer rotation or display settings do not regenerate dimensions; change CLI inputs and regenerate STEP to change geometry.

| Parameter group | Default inputs |
| --- | --- |
| Cavity and split | `--cavity-length 72.5`, `--cap-height 43.4` |
| Radial envelope | `--body-bore 30`, `--cap-bore 31`, `--wall 2.4`, `--floor 3`, `--max-od 39` |
| Original thread | `--thread-pitch 2`, `--engagement 6`, `--thread-height 0.6`, `--root-wall 1.8` |
| Thread clearance | `--thread-clearance 0.25`, `--clearance-budget 0.30`; coupon caps use 0.20/0.25/0.30 |
| Diamond skin | `--skin-axial-pitch 4.8`, `--skin-arc-pitch-target 3.63`, `--skin-height 0.45`, `--plateau-half-fraction 0.18` |
| Skin placement | `--skin-phase-theta 0` radians, `--skin-phase-z 0`, `--smooth-margin 2`, `--fade-length 2`, `--min-grip-band 24` |

Lengths are millimetres. Inputs are independent only within their derived constraints: the CLI rejects infeasible grip bands, walls, outside diameters, thread slopes and plateau widths. The short preset locks maximum OD39; `--preset generic` permits another limit inside the supported scalar domain. A feasible scalar result is not evidence that every parameter combination has validated BREP geometry.

At defaults, the nominal closed cavity is72.5, outer end-to-end length78.5, full-form thread engagement6 and total neck penetration9. The two usable skin bands are24 each. Adding9.6 to cavity length with the same cap height adds two body-skin periods; it does not stretch the pattern. The common circumferential count is31. Cap labels20/25/30 are recessed0.20 into the nominal3mm floor, leaving2.8mm beneath the marks, and read upright when viewing into the cap in its opening-up print pose.

`--skin-style diamond` is the implemented STEP route. `smooth_crosswave` is an analytic comparison only and its STEP request rejects explicitly. `--preset laifen-provisional` remains gated by unresolved full-case split/end-contact decisions and physical measurements.

A known nondefault failure remains: pitch2.4/engagement7.2 with cavity82.1/cap-height47 is scalar-feasible, but its female-thread Boolean produced an empty cutter. The current generator rejects empty or disconnected cutters instead of returning a silently filled cap. General editable-pitch CAD and actual smaller-bore cases remain unaccepted; do not infer them from default success.

The default review evidence includes valid written solids, floors, recessed-label identity in print pose,30 zero-intersection screw poses, extraction and positive-stop checks, and an inspected print-layout snapshot. The frozen candidate is `../../docs/iterations/2026-09-01-p1-r3-algorithmic-skin/inputs/geometry-default-candidate.sha256`, fingerprint `4e1ea38ac083f2f9b708770165bb2281748f129826f1f50bd1782139484a9ffd`. Independent continuous mouth-boundary correspondence passed for all three default caps with bounds of approximately0.0002mm. Whole-surface source/export correspondence remains on hold; see `../../docs/iterations/2026-09-01-p1-r3-algorithmic-skin/VALIDATION_DEFAULT.md`. No STL/3MF, slicer or physical-print acceptance is implied.

Before a physical trial, validate the exact fabrication files and chosen process. Record hand grip, comfort, shoulder closure without forcing, preferred clearance and five empty cycles per cap, alternating cap order to expose body wear. This short empty experiment does not establish toothbrush fit, retention, wet grip, durability or strength. No printer operation is part of these commands.
