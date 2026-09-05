# CRI-04 recovery candidate critique

Owner: `/root/preview_critique`, independent critic. Status: **FAIL — one major finding**. Source, tests, dependencies, runtime and coupon files were read-only. No browser claim is made; VAL-04 owns independent rendered-browser checks.

Verified candidate: `inputs/recovery-candidate.sha256`, SHA-256 `8e2276d24b8c7457a06010af2f489666a190397b22ddd0a64985d4572baf5437`. All 18 declared path/content entries matched before critique. Baseline repository `d0aab1ff21a0cd2e5790c9800fcec7cfec2bfc3c`; preview source hash `bc0655e513aff9cab1efda8701a04ce8ee1f33c2d8d4b7a8fc687326fddc2662`.

## Finding

**C04-01 — major, invalid rendered geometry accepted.** With `L=208, D=1.7e308, slack=5, q=0.5`, at both 360 and 736 px, `compute` accepts the finite inputs, the error readout remains empty, and the actual emitted device SVG has `width="Infinity"`. Its X value is `-1.4748858447488582e+308`, Y is `63.54337899543379`, and height is `360.9132420091324`. Checking finite source parameters and computed physical gaps does not cover overflow of `D*scale` during rendering. This violates DES-04 derived-infinity rejection and DESIGN invalid-state clearing; the section, gaps, dimensions and warnings are retained instead of cleared. This is an input-validation correctness issue, not evidence of real case interference or physical fit.

Smallest correction: validate all essential screen-space geometry before writing SVG/readouts, route unrepresentable values through the existing invalid-state clearing path, and add this focused extreme-D regression at both layouts. Do not introduce an arbitrary physical diameter cap. One affected critique rerun remains available against a newly frozen candidate; no repair was made by this critic.

## Requirement coverage and evidence

- Actual emitted ID-span coordinates divided by actual SVG scale equal 30/31 across widths 360/736, L140/208/400 and D29/30/31. D edits preserve the spans.
- Actual neck/mouth leader Y separation divided by scale is 5; their numeric z137/z132 source datums remain distinct.
- Neck, mouth and pending-band leader start/end X coordinates are strictly beyond `0.38*width+17.9*scale` in all probed cases. Existing tests also check external-stop path and text anchors. Browser font extents remain VAL-04 scope.
- Decimal slack0.1/5.1 renders finite device geometry at q0/0.5/1; the existing suite confirms arithmetic and endpoint state labels.
- L1e308, blank D and C137 reject and clear emitted geometry and derived readouts; the missing extreme-D case above is an additional failure, not a contradiction of those passing cases.
- Persistent text states dimensions are unmeasured and printed-ID/fit unknown. Positive radial gaps do not receive fit acceptance; D30/31 contact/interference warnings and original-width reference intent remain intact. Pending-joint labels do not claim threads, contact, or engagement proof.

Commands, all run from repository root with `login=false`:

```sh
shasum -a 256 projects/laifen-wave-case/docs/iterations/2026-09-01-p1-r2-fit-feedback/inputs/recovery-candidate.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-01-p1-r2-fit-feedback/inputs/recovery-candidate.sha256
node --test projects/laifen-wave-case/tests/test_measurement_gate.mjs
node projects/laifen-wave-case/scratch/width-critique/probe.mjs
```

Results: fingerprint as above; 18/18 manifest entries OK; existing suite 8/8 pass; independent ordinary geometry/decimal/clearing probes pass at both widths and report `hasNonfinite:true`, `error:""` for D1.7e308 at both widths. The scratch probe intentionally reports the adverse case without a nonzero exit; its status is not a passing gate. No EMFILE occurred.

Changed paths: this receipt and `scratch/width-critique/probe.mjs` only. Scratch is reproducible evidence, not a release artifact. Next action: root routes C04-01 to the authorized implementation owner, freezes its new candidate and reruns the affected independent gates before formal review/publication. Full-case CAD, artifact/slicer and physical acceptance remain pending and outside this critique.
