# P13 R1 monorepo migration validation

## Environment

- Repository root: `design-projects`
- Python: required `>=3.12,<3.13`
- Python workspace: root `.venv` and `uv.lock`
- JavaScript workspace: root npm install and `package-lock.json`
- Legacy project dependency preserved: `cadgen==0.4.15`

## Completed import checks

- The 206-file bulk transfer used checksum-aware `rsync` with explicit exclusions.
- A post-copy checksum dry run reported no file-content differences; directory timestamp differences only.
- The imported legacy handoff, continuation summary, and next-agent prompt match their source bytes after relocation under `docs/legacy/`.
- Key imported release hashes match the migration and release manifests.

## Commands and results

- `uv lock && uv sync --all-packages --all-groups`: passed; the XT60 package is registered in the root Python 3.12 workspace.
- Root repository tests: `6 passed`.
- `npm test --workspace xt60-bend-jig-simulator`: `26 passed`.
- `npm run build --workspace xt60-bend-jig-simulator`: passed; the generated `dist/` bundle remains ignored.
- Initial complete project run: `396 passed, 8 skipped, 14 failed` in 14 minutes 39 seconds. Seven failures were current P13 outputs deliberately excluded from bulk transfer; seven were historical P2–P6 tests that assume generated exports absent from the transfer source.
- Explicit P13 source regeneration: all 24 current STEP outputs, production/coupon 3MF files, and provenance were written from migrated source. The source, brief, and amendment hashes remained unchanged.
- Focused rerun of `test_p13_four_plate_three_rod.py`, `test_p13_motion.py`, and `test_p13_rod_fit_coupon_3p8.py`: `59 passed`.
- `scripts/inspect validate`:
  - P13 print kit: 14 occurrences, pass; all solids valid, closed, and positive volume.
  - P13 motion assembly: 16 occurrences, pass; all solids valid, closed, and positive volume.
  - P13 3.8 mm coupon: 1 occurrence, pass; valid, closed, positive-volume solid including self-intersection check.
- P13 production 3MF export: 12 manifold and oriented objects, lib3mf round-trip valid, zero pairwise bounding-box overlap, `136.269 x 105.05 mm` footprint.
- ISO snapshots were rendered and visually inspected:
  - `docs/review/p13-migration/p13-print-kit_20260822T183044Z.png`
  - `docs/review/p13-migration/p13-motion_20260822T183050Z.png`
- CAD Viewer started successfully and served the project with HTTP 200 on localhost. A Tailscale URL is deliberately required from the next repair worktree so it points at the repaired artifact.
- Browser-controlled simulator review was attempted, but the attached browser list was empty. No visual-browser claim is made.

## Requirement evidence

The source/solid/export requirements for migration are satisfied by the focused results above. Historical slicer evidence remains linked from the release manifest and legacy handoff; it was not silently promoted to current regenerated-artifact evidence.

## Artifact paths and checksums

See `migration-manifest.json` and `releases/p13-petg-test/release-manifest.json`.

## Acceptance state

- CAD/source: pass for migration baseline.
- Written artifact: pass for regenerated STEP/3MF/provenance and static mesh checks. Fresh slicer acceptance remains pending.
- Physical: failed center-hole fit observed on the latest print; repair and remaining complete P13 checks pending.

## Failures, repairs, and reruns

- The physical center-hole defect is recorded for a separate post-migration iteration. No geometry change is permitted in this migration iteration.
- The seven current P13 missing-output failures were repaired only by regenerating from source, then rerunning the 59 focused tests.
- The remaining historical P2–P6 output assumptions are documented, not masked by stale artifact imports.
