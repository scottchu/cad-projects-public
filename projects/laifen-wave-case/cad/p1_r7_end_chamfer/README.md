# P1 R7 editable smooth end chamfer

Original full-length 39 mm Laifen case, copied from the reviewed R6 parametric source. `Params.end_chamfer_size` is a real source-level CAD parameter: default **1.20 mm**, permitted range **0.80–1.50 mm**. Change it in `params.py` or pass `Params(end_chamfer_size=1.40)` to the part builders, then regenerate. No viewer-only control or automatic sidecar regeneration is claimed.

At each closed end, inward distance `t` gives the exact conical limit `r = 19.50 - end_chamfer_size + t`. Default end radius is 18.30 mm, axial height 1.20 mm and slope 1 (45 degrees). The guaranteed circular smooth band is `end_chamfer_size - skin_height`: 0.75 mm at default and at least 0.35 mm within the selected range. Above that band the cone meets the original unscaled diamonds. This single smooth chamfer replaces the previous textured end bevel; there is no stacked second bevel and no smooth seam collar.

`chamfer.py` forms one annular cutter per part: an overshooting cylinder minus a coaxial cone, extending 0.01 mm beyond each end of its local interval. Cone radii continue the same equation through the extensions, preserving the nominal end and shoulder limits. Body uses inward +Z; cap uses inward -Z before its print rotation. `parts.py` subtracts this one cutter from the raw outer blank before existing bore/thread/drain operations. `body_from_outer` and `cap_from_outer` permit sensitivity checks to reuse a raw diamond blank across chamfer sizes. No downloaded or mesh geometry is used.

The retained full-case dimensions are crest OD39, body/cap bores30/31, cavity213, outside length219, body height144 and cap height84. Approximate device inputs L208/D29 and axial allowance5 remain editable through named inputs; cap cavity81 and two 3 mm floors derive the full axial stack. Device diameter affects reference/readout geometry, not the fixed bores. The original N33, pitch4.8, relief height0.45 diamond field shares phase across the seam without Z scaling. Each closed floor retains seven diameter3 drains: center plus six at R9. Chamfer cutters cannot reach the inner floors, bores, thread, seam or positive stop.

The R6 B thread, native datums and repaired upper female runout are preserved. `runout.py` uses the same isolated native trim/vertex-parameter correction with unchanged curves, surfaces, coordinates and tolerances. The source/written STEP volume gate stays 0.001 mm³. No new motion or fit claim follows from this end treatment.

Primary source/output pairs:

- `body.step.py` / `body.step`: one body, Z[-135,9].
- `cap_c25.step.py` / `cap_c25.step`: one cap, Z[0,84].
- `closed_c25.step.py` / `closed_c25.step`: exactly two case parts, outside length219.
- `print_layout.step.py` / `print_layout.step`: body at(+23,0,135), cap rotated Rx180 then placed at(-23,0,84); openings up, two objects, nominal85×39×144.

`review.py` remains a separate reference-only device-envelope/section helper. Centered nominal gaps are2.5/2.5, without retention; it is excluded from the four fabrication outputs.

Run from the repository root using its uv Python3.12:

```sh
uv run pytest projects/laifen-wave-case/tests/test_end_chamfer.py -q
uv run python projects/laifen-wave-case/cad/p1_r7_end_chamfer/generate.py
```

The generation driver runs exactly these installed commands with owned-process limits of600s per target and1800s total:

```sh
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/gen projects/laifen-wave-case/cad/p1_r7_end_chamfer/body.step.py --write
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/gen projects/laifen-wave-case/cad/p1_r7_end_chamfer/cap_c25.step.py --write
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/gen projects/laifen-wave-case/cad/p1_r7_end_chamfer/closed_c25.step.py --write
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/gen projects/laifen-wave-case/cad/p1_r7_end_chamfer/print_layout.step.py --write
```

Source guards preserve600s stage limits and count raw exterior patches before allocation (16000 per part,26000 combined), with unchanged rational accuracy and sewing tolerance. Implementation/sensitivity evidence and immutable manifests live in `docs/iterations/2026-09-03-p1-r7-end-chamfer/`. Independent validation, critique and formal review establish CAD/source and STEP status. Slicer/process, tall-part adhesion, thread strength/fit, loaded device fit and end contact, drainage under a blocked floor, and physical acceptance remain unproven.

`end_trim.py` repairs tolerance-covered endpoint inconsistencies introduced where the new conical trim meets the diamond field. It selects only the end-local45-degree cone and shortens existing3D/pcurve ranges to the existing vertices, on an isolated topology copy. Curves, surfaces, coordinates and vertex tolerances remain unchanged. This native consistency step keeps the original0.001 mm³ source/STEP parity gate; it is not STEP-roundtrip canonicalization.
