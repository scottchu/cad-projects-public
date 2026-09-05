# Design-stage evidence

DES-SKIN-01 `/root/skin_design`, design role only. No independent CAD validation or acceptance is claimed.

- `shasum -a 256 .../p1-r2-fit-feedback/inputs/coupon-fixed-candidate.sha256`: `3da2cac2b8d29b379b3be6309e3b7eb623fc50f6766dd5a573438a49517f6e4d`; corresponding `shasum -a 256 -c` verified all59 entries. Actual full path begins `projects/laifen-wave-case/docs/iterations/2026-09-01-`.
- Read supplied rejection screenshot and original metal-grip reference. Read repository workflow/continuity/FDM policy, project requirements/experience/state/handoff and R2 coupon/recovery contract/receipt. No mutable CAD was read while its owner was active.
- `uv run python projects/laifen-wave-case/preview/p1-r3-skin-study.py`: generated analytic SVG and PNG. Exact numeric results: body/cap arc pitches3.5266911079008/3.6280328064036964; developed plateau minimum widths1.0231383170253368/1.0419453252303599; diamond slope bound0.6463979235288517 (32.878543414254686deg); optional smooth bound0.942477796076938; minimum cavity72.5; five4.8mm periods in each24mm band.
- Initial analytic silhouette had small rendering gaps from independently sampled quad radii. One focused repair made adjacent quads share analytic vertex positions and reduced SVG sampling/output cost. This was a drawing repair, no CAD change.
- Inspected the regenerated PNG: broad24mm textured bands appear on both upright silhouettes; the full unrolled diamond tiling, fades and smooth alternative are visible; captions identify analytic-only status. The view demonstrates design coverage, not physical comfort or CAD geometry. R3 manifest `e63eecf9e47d97d37787e58f92e5b3f394e18abf33a33e2d10f126286501c027` has68 verified entries/zero mismatches; frozen BRIEF/DESIGN snapshots exactly match their live marked sections.

The scalar equations and derivations are design evidence. CAD topology/sections/motion, actual surface normals, written STEP parity, meshes, slicer and physical hand tests are all pending. No STEP exists for R3, so a CAD primary snapshot/viewer handoff does not apply yet; the PNG is explicitly an analytic design study.
