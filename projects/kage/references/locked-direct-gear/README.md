# Locked direct-gear reference

This folder contains the only selected binary frozen reference plus its exact source/test snapshots. `p3_v3_direct_gear_race_assembled.step` has SHA-256 `dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7`.

It is a comparison/restart parent, not a physically accepted product. Do not edit it or reuse its tiny nominal clearances as PETG truth. The original source-label paths and hashes are recorded in `../../manifests/source-authority.sha256`.

## Recovery status

This packet is frozen provenance and is not runnable or generatable in place. Exact recoverable legacy routes are:

- `legacy/source-project/p3_v3_direct_gear_race_guidance_spec.py`
- `legacy/source-project/p3_v3_direct_gear_race_guidance_geometry.py`
- `legacy/source-project/p3_v3_direct_gear_race_guidance_export.py`
- `legacy/source-project/models/p3_v3_direct_gear_race_guidance_locked_pre_radial_visibility_20260818/source_snapshot/`
- `legacy/source-project/models/p3_v3_direct_gear_race_guidance_locked_pre_radial_visibility_20260818/tests_snapshot/`

Do not generate into this reference directory. If a future decision adopts any concept, copy only the required parametric source into a newly named restart namespace, declare the locked parent hash, add focused regressions, and generate new artifacts there.
