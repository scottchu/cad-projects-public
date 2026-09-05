# IMP-R6-03 native runout correction trial

Owner `/root/case39_impl`, implementation role. Status: one focused native correction demonstrated in scratch; independent acceptance and official production patch remain pending. No official source or STEP file changed. Frozen candidate135 remains `4c2750ad632639be5547074173408aa14dfc579faed8d45890ed7233b00c0351`.

Task inputs were frozen before work in `scratch/fullcase-export-repair/r3/inputs.sha256`:145 path/content pairs, SHA256 `f55ec84692bba6be3142c3e6365735f2e06ff71246a82d09a73bf4df34907edc`. They include candidate135, its manifest, EXPORT_REPAIR.md and the exact source/written BREP and relevant diagnostic probes. All145 were verified again after trial verification. Only this receipt and `scratch/fullcase-export-repair/r3/` were written.

## Demonstrated native recipe

The existing runout vertex and underlying3D curve are retained. Project that vertex onto the existing shared helical-flank/conical-runout edge, within its current parameter range. The nearest point has residual5.8723011e-8mm. Set the edge's range in **all**3D/pcurve representations with `BRep_Builder.Range(edge, first, new_last, False)` and update the vertex's stored edge parameter with `BRep_Builder.UpdateVertex(vertex, new_last, edge, original_vertex_tolerance)`.

Observed parameter range `[0,1]` becomes `[0,0.9988497584922102]`. Endpoint-to-vertex residual falls from0.002561321256401561mm to5.872301100285205e-8mm. Vertex coordinates, underlying surface/curve geometry and tolerance0.00256132140603368mm are unchanged. This adjusts an inconsistent trim boundary; it is not a tolerance-metadata reduction or STEP roundtrip canonicalization. No global healing, thread dimension change, skin change or tool-termination alternative was needed.

The corrected scratch source is a valid one-solid cap with6593faces. Default `export_step` settings followed by `import_step` also yield a valid one-solid cap. Pre/post source bounds are identical: nominal39mm outside and84mm height, with normal kernel bound tolerance. The unchanged official parameter/source manifest preserves selected dimensions and laws; independent validation must still verify the production result.

## Unchanged parity gate

All values are mm3. Gate remains absolute source/written delta<=0.001.

| Integration | Source | Written | Absolute delta |
|---|---:|---:|---:|
| Adaptive Gauss eps1e-8 |35022.740705323966|35022.74068204771|0.000023276254069060087|
| Adaptive Gauss eps1e-10 |35022.7406697953|35022.740655030386|0.000014764911611564457|
| Gauss–Kronrod, spans, eps1e-8 |35022.74067843272|35022.74067033321|0.00000809950870461762|
| Gauss–Kronrod, spans, eps1e-10 |35022.740670536296|35022.74065612195|0.000014414348697755486|

The native correction plus scratch export/inspection completed9.201s; verification completed5.175s. Both conventional and GK methods pass the original gate. No repeated failed no-pcurve/GK variant or speculative export sweep was run.

## Production selector and credible regression

`r3/role_selector.py` demonstrates a geometric-role selector without face indices. It considers only edges shared by a conical face and a BSpline helical face, whose existing endpoint vertex is at `neck_height` and radial distance `thread_crest+thread_clearance`. It identifies an endpoint-to-vertex residual above1e-4mm. On the frozen source it finds exactly one defect, residual0.002561321256401561mm; on the corrected native source it finds zero. The trial's direct correction used the already-diagnosed exact face pair to isolate the experiment; production should use the tested geometric selector.

Proposed production guards: require at most one matching default-candidate defect; project only inside the existing curve range; require projection residual<=1e-7mm and a bounded small correction; retain vertex coordinates and all functional datums. Apply to an isolated topology copy if needed to avoid modifying cached female-tool shapes. Recheck actual closed-solid validity after correction. Do not reduce vertex tolerance instead of repairing the trim. A source-level endpoint-consistency regression should fail on the frozen uncorrected source and pass on the repaired cap; conventional source/written volume parity supplies the independent artifact regression.

## Supplemental diagnostic and scope

A supplementary ray comparison initially asserted source/written radius difference<1e-6mm, an unnecessarily strict diagnostic distinct from the frozen0.01mm radial law bound. It failed at theta0,z8.5: before/source radius16.9, written16.90003322150332, delta0.000033221503322522494mm. This is recorded, not hidden. Source before/after values at all five completed sampled stations were identical; largest sampled nominal-law error was0.00003365319218673335mm, within the frozen0.01mm bound. Per root direction, the optional broader ray sequence was stopped after recording this actual diagnostic difference. No acceptance threshold was changed; the unchanged0.001mm3 parity gate passes. Full production interface, motion and visual acceptance belong to the independent validator/critic.

## Commands, evidence and next action

Commands ran from repository root using its uv Python3.12. The native trial ran inside an outer root-Python subprocess timeout300s.

```sh
uv run python projects/laifen-wave-case/scratch/fullcase-export-repair/r3/native_range.py
uv run python projects/laifen-wave-case/scratch/fullcase-export-repair/r3/verify_native.py
```

Exact recipe and results: `r3/native_range.py`, `role_selector.py`, `native-range.json`, `verification.json`; scratch geometry: `native-range.brep` and `cap-native-range.step`. The supplementary first diagnostic assertion is retained in the execution history and described above; final verification JSON includes its actual values and stop reason. These are trial artifacts, not files to hand the user as a fixed release.

One correction attempt succeeded; no geometry repair cycle or alternative construction was used. Root may now authorize the focused production helper/call, source endpoint/parity regression and affected cap/closed/layout regeneration, preserving body bytes. Freeze a new candidate and reopen the cap runout law/parity, affected export occurrences and critic visual gates before formal acceptance. No source/CAD, STEP or physical self-approval is claimed here.
