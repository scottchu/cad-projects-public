# Default generic-cylinder implementation receipt

Owner `/root/generator_core`; 2026-09-02. Status: complete runnable default CAD/export candidate, pending distinct critique, validation and formal review. Source/artifacts held unchanged after freeze. Candidate `geometry-default-candidate.sha256`:53/53 verified, SHA-256 `4e1ea38ac083f2f9b708770165bb2281748f129826f1f50bd1782139484a9ffd`. Parameter fingerprint `50f1e34681419a81f91b4587b8f1e11a97569b3e99cc530891dfcee32b302677`.

## Deliverables and exact reproduction

`cad/p1_r3_generator/` now contains immutable parameters/derivation, shared original normalized thread helpers, exact scalar skin, bounded rational skin surface construction, body/cap/coupon/assembly/print builders, source datums/joints, real CLI, geometric diagnostic helpers and seven named `gen_step()` entrypoints. Inputs are source parameters, not Viewer mesh scaling. All dimensions remain in mm. Laifen provisional preset remains explicitly gated.

The seven canonical STEP files and matching source entries are:

- `body.step` / `body.step.py`;
- `cap_c20.step`, `cap_c25.step`, `cap_c30.step` and corresponding entries;
- `closed_c25.step`, `exploded_c25.step`, `print_layout.step` and corresponding entries.

Each single part has one valid solid; closed/exploded contain two; print layout contains four. Separate original body and cap24mm grip bands are continuous, with smooth exclusions and raised-only skin. The body has a closed floor; cap clearance marks are recessed0.20 into its floor and source-Y mirrored so the Rx180 print pose reads20/25/30 correctly.

Real CLI command executed successfully from repository root:

```sh
uv run python projects/laifen-wave-case/cad/p1_r3_generator/generator.py --preset short-grip --write-step --target all
```

It built the actual solids, wrote all seven STEP targets into `cad/p1_r3_generator/generated/50f1e34681419a81/`, reimported them, verified topology and solid counts, and emitted `manifest.json` with exact parameters, derived dimensions, source hashes and artifact hashes. Canonical targets are byte copies of these generated outputs. `--target body|cap|coupons|closed|exploded|print-layout|all` selects output scope; `--output-dir` selects the parent of the parameter-fingerprinted directory. Every Params field has a CLI override. Existing `--dry-run` continues to calculate constraints without claiming CAD generation.

Generation-manifest provenance is retained honestly: outputs were generated before the final empty-void rejection guard was added. The guard changes only rejection of empty/disconnected Boolean tools and returns unchanged valid default solids. The actual generating thread source25391b...8404 is preserved in `geometry-mouth-stage/thread_profile.py`; final guarded source is bound in the current candidate. No exact whole-solid parity claim is made from this source reasoning alone; independent validation must compare final source and written artifacts.

## Executed checks and observations

- Earlier phase-A derivation/CLI checks: default C72.5/H43.4, 24/24 bands, C60 rejection, +9.6 length gives two extra unchanged-pitch repeats, feasible scalar p2.4/E7.2 and bore24/25 cases, finite/domain/wall/slope/plateau rejection and exact default scalar thread equivalence against frozen R2.
- DES04 final representative patch:116 faces, one valid positive-volume solid, all canonical edges incidence2, no free/multiple sewn edges; actual surface max sampled radial discrepancy0.000231337mm, actual developed plateau-boundary width lower bound1.057794mm, smooth-radius discrepancy3.55e-15mm; separate global error/plateau/slope proofs retained. Full receipt `IMPLEMENTATION_PATCH_RECOVERY.md` distinguishes the earlier98-face checkpoint.
- Default complete cap exterior:2234 faces, valid,4.851s total;2300-scale faces rather than million-face mesh construction. First body generation14.03s,2311 faces, volume13821.6384mm3. First C25 generation16.98s,2277 faces, volume13577.3385mm3. Final C25 was regenerated after the label-orientation correction.
- Main test run `uv run pytest projects/laifen-wave-case/tests/test_generator.py projects/laifen-wave-case/tests/test_generator_geometry.py -q -s`: nine tests PASS as collected before the later guard regression was added. Written STEP checks include single solids, floor material/void placement, all seven segments of the actual recessed20/25/30 glyphs in print pose, assembly counts, all30 full-part screw poses at zero intersection, extraction g9/10/11, and positive negative-stop collisions. Log `scratch/generator-core/final-pytest.txt`.
- Separate final guard regression `uv run pytest projects/laifen-wave-case/tests/test_generator_geometry.py -q -k empty_changed_pitch`: PASS. It prevents the reproduced nondefault empty-void defect from yielding a silently filled cap. This composes ten focused passing tests; it is not a claim that one recorded process collected all ten.
- Actual C20 untextured thread sections:64 classifier sections, max radial discrepancy3.657341e-5mm. Source remains valid after copied-curve inspection.
- C20/C25/C30 diagnostic source AND written mouth checks pass the unchanged1e-4 actual endpoint/p-curve/plane limits. C20 endpoint4.381745e-5mm, C25 endpoint6.837077e-6, C30 endpoint6.880291e-6. Native C20 tolerance metadata0.000134426 is preserved and recorded under DES05, not altered or confused with actual error. Full records `mouth-source-written-cases-results.json`.

Primary snapshot executed with the installed CAD launcher through root uv:

```sh
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/snapshot --input projects/laifen-wave-case/cad/p1_r3_generator/print_layout.step.py --output projects/laifen-wave-case/scratch/generator-core/print-layout.png --camera isometric --width 1400 --height 1000 --json
```

Saved and visually inspected `scratch/generator-core/print-layout_20260902T041350Z.png`: four parts open upward, threads and broad diamond grip coverage visible. Displayed black construction edges are CAD face boundaries and are not evidence of physical grooves. Numeric glyph checks, not this distant view, establish label identity. Snapshot JSON reports success/no warnings. Root independently manages the private Viewer route and reported exact generator artifact readiness/page200; this worker changed no service configuration.

## Explicit remaining risks

**High, nondefault thread BREP:** the scalar-feasible `Params(thread_pitch=2.4, engagement=7.2, cavity_length=82.1, cap_height=47)` case produces a valid-but-empty female thread/relief union in the frozen pre-guard source. Its volume0/solid count0 leads to a filled cap:6 faces, volume49809.9356053mm3, axis point(0,0,5) IN. Reproduce from immutable old source with `uv run python projects/laifen-wave-case/scratch/generator-core/changed-pitch-failure.py`; exact input/source/stage values are in `changed-pitch-failure.json`. Final `female_void` now rejects this result explicitly before cap generation. Editable-pitch CAD and smaller-bore actual solids are NOT accepted merely because their scalar derivations pass. Root will assign independent diagnosis; no thread-shape redesign was attempted here.

**Pending, continuous source/STEP mouth boundary correspondence:** first helper assumed equal face-edge counts. Source C20 reports12 edges, written9. Read-only orientation diagnostic identifies the three extra source entries as `TopAbs_INTERNAL`; written true boundary entries are FORWARD/REVERSED. These construction-internal edges must not be silently treated as physical boundary changes. This observation is not a completed continuous-boundary proof. Independent validator owns the correct boundary correspondence and unchanged0.001 local limit; current `mouth_correspondence` helper remains diagnostic and is not called by generation or passing tests.

**Pending:** independent actual BOP/surface/whole-export review, complete default source radial evidence beyond scoped tests, nondefault joint geometry, any STL/3MF/slicer validation, physical grip/fit/wear and all Laifen full-case fit/end-contact decisions. No printer action or physical acceptance. The candidate is reviewable CAD, not a print release.

## Scope and environment

Preserved R2 source/artifacts/contracts and prior failed R3 variants. Only authorized R3 source/tests/artifacts/receipts/scratch plus project `cad-preview` dependency group and root uv.lock changed. Playwright1.62.0 uses the existing matching Chromium1234; root uv sync installed its declared dependencies. Existing unrelated cadgen pin and services were preserved. Root owns PROJECT_STATE/NEXT_AGENT/iteration handoff and independent task scheduling.
