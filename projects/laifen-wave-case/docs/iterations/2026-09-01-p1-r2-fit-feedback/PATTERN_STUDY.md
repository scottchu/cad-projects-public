# PAT-01 original faceted grip concept study

Date: 2026-09-01  
Task ID: `PAT-01`  
Owner: `/root/case_knurl_study`  
Model: Codex GPT-5 child agent  
Baseline: `d0aab1ff21a0cd2e5790c9800fcec7cfec2bfc3c`

## Scope and frozen inputs

This study answers the user's September 1, 2026 question about an original grip pattern "like stainless steel" without touching the active width preview, full case CAD, exported solids, slicing, or printer state. The attached Shutterstock PNG was treated as aesthetic reference only and was not copied, edited, or traced.

Frozen input manifest reused from the P1 R1 study:

- manifest path: `projects/laifen-wave-case/docs/iterations/2026-09-01-p1-r1-measurement-gate/inputs/pattern-inputs.sha256`
- manifest file hash: `9a1dcbab6dcb4ceb0b5edcf3c6c05a756d38e90ffdd71fbf6a8bc5c52e62f89e`
- verification before and after local work: `shasum -a 256 -c .../pattern-inputs.sha256` -> all entries `OK`
- reference PNG hash: `cb0eadb30f246c5a35ff03e31be530f6857cefb8a9a0511eef1d59b782619db5`

## Original concept

Selected concept: a shallow raised faceted lattice on the developed cylindrical surface, with truncated diamond or pyramid cells and a flat tip sized for a 0.4 mm nozzle. The study keeps the preserved internal bores unchanged by treating the texture as outward additive geometry. It uses full cells only inside the active band and leaves equal smooth margins at both ends.

Global phase rule for future CAD: define one assembled-space angular datum `theta0` at the seam and one assembled axial datum `Z0` at the future shoulder or parting reference, then generate one larger lattice and clip it to each allowed texture band. This keeps axial pitch constant when body length changes and avoids Z scaling. Smooth exclusions near floors, shoulders, threads, and openings stay separate from the lattice.

## Chosen numeric checkpoint

- preserved bores from DEC-05: lower `ID30`, cap `ID31`
- nominal plain outer diameters at wall `2.4`: lower `34.8`, cap `35.8`
- target circumferential pitch family: about `3.64 mm`
- derived repeat counts:
  - lower body `30` repeats -> actual circumferential pitch `3.644247 mm`
  - cap `31` repeats -> actual circumferential pitch `3.628033 mm`
- chosen study cell top flat: `1.0 mm`
- chosen raised texture height: `0.6 mm`
- study band height: `28.0 mm`
- derived full-row count at main pitch: `6`
- derived textured height: `21.865485 mm`
- derived equal smooth margins: `3.067258 mm` each end
- derived visible study feature count: `180` cells

Overhang bound using a simple axial rise/run section:

- axial run from valley to flat shoulder = `(3.644247 - 1.0) / 2 = 1.322124 mm`
- `atan(0.6 / 1.322124) = 24.409275 deg`
- `atan(0.8 / 1.322124) = 31.177591 deg`

Both stay below the repository's current `45 deg` support-free limit, so a shallow blunt faceted concept is analytically plausible in the intended vertical PLA print orientation. This is slope math only, not slice evidence.

Wall and OD bounds:

- outward-additive `+0.6 mm` texture keeps the preserved bores unchanged
- additive max ODs: lower `36.0`, cap `37.0`
- margin to approximate OD cap `39`: lower `3.0`, cap `2.0`
- if a later subtractive or bidirectional interpretation is attempted, residual wall at `0.6` depth becomes exactly `1.8`; at `0.8` it drops to `1.6`

That means `0.6` is the safe bound for this original study if future CAD needs the option to cut inward anywhere. A raised-only implementation could go deeper analytically, but this study does not recommend it.

## Coupon checkpoint for `/root/case_coupon_design`

The sibling coupon task provided cap-only texture span `z14.4..20.0`, so usable axial texture span is `5.6 mm` on radius `17.9` / OD `35.8`.

- keep the cap circumferential family at `31` repeats -> `3.628033 mm`
- the main axial pitch `3.644247 mm` fits only `1` complete row in `5.6 mm`
- if the coupon must show `2` rows inside the same span, axial pitch must drop to `5.6 / 2 = 2.8 mm`, or the taper or smooth-zone budget must shrink
- at `2.8 mm` pitch with the same `1.0 mm` flat:
  - run = `(2.8 - 1.0) / 2 = 0.9 mm`
  - `atan(0.6 / 0.9) = 33.690068 deg`
  - `atan(0.8 / 0.9) = 41.633539 deg`

Recommendation for the coupon freeze: keep circumferential repeats `31`, keep flat tip `1.0`, keep raised height `0.6`, and choose either one representative row at the main pitch family or two rows at `2.8 mm` axial pitch only if the coupon specifically needs a denser vertical sample. Do not texture the smooth female collar.

## Generated artifacts

- generator: `projects/laifen-wave-case/preview/knurl-study.py`
  - SHA-256 `67144102ea10ae3f0e5042706da18600cb945056695bf1a6a6958c75f9803826`
- SVG concept: `projects/laifen-wave-case/preview/knurl-study.svg`
  - SHA-256 `493630fdcf31e291d213c8c169640a1539b7b02d421fc2faf67bb7eff2031373`
- machine-readable metrics: `projects/laifen-wave-case/scratch/pattern-study/knurl-study-metrics.json`
  - SHA-256 `866eef96f64203d3f8b3ed16dd76fdcece18e75c33fb6534b045ffc8fc5d77c9`
- scratch PNG preview from Quick Look: `projects/laifen-wave-case/scratch/pattern-study/knurl-study.svg.png`
  - SHA-256 `2e29383e44b92957c990c7026f72323a96f2d3f997c08e67b4bb36079f3d87f1`

## Commands run

```bash
uv run python projects/laifen-wave-case/preview/knurl-study.py
qlmanage -t -s 1600 -o projects/laifen-wave-case/scratch/pattern-study projects/laifen-wave-case/preview/knurl-study.svg
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-01-p1-r1-measurement-gate/inputs/pattern-inputs.sha256
```

## What remains unproven

- no actual case solids, no joint geometry, no STEP, no mesh, no slicer evidence
- no proof that the future body and cap can share exact visual phase across different diameters without a final seam rule
- no proof that the chosen facet shape feels good in hand or survives wear
- no proof that the unresolved shoulder or thread band leaves enough uninterrupted texture real estate on the final cap
- no physical validation and no acceptance claim
