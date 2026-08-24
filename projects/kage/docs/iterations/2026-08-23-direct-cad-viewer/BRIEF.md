# Kage direct CAD Viewer brief

## Frozen design contract

- Project and iteration: repository preview-workflow simplification recorded at `projects/kage/docs/iterations/2026-08-23-direct-cad-viewer` (`KAGE-PREVIEW-DIRECT-001`).
- Repository baseline: `9c1ae27b9a856cb19c0dfefd497e5133987e2bd4` on `codex/simplify-cad-preview`.
- User outcome: use the repository's existing CAD workflow and installed `cad-viewer` skill directly, without a custom repository launcher, while preventing a server or URL from being described as good when the requested artifact actually failed to build.
- Runtime authority: the installed `cad-viewer` skill. Repository code must not duplicate its startup, listener, process-management, URL-construction, or plugin-version-selection behavior.
- Exact Kage input: imported historical STEP `projects/kage/references/locked-direct-gear/p3_v3_direct_gear_race_assembled.step`, frozen SHA-256 `dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7`.
- Workspace contract: resolve `projects/kage/references` to an absolute Viewer workspace and select `locked-direct-gear/p3_v3_direct_gear_race_assembled.step` relative to it.
- Readiness contract: before reporting a preview ready, require the exact review page to return HTTP `200` and the exact artifact endpoint to return HTTP `200` with JSON `state == "ready"`. Startup success, a printed URL, or page HTTP `200` alone is insufficient.
- Visual-claim contract: after visually inspecting the loaded page or a snapshot, the general claim is limited to “the requested artifact rendered with no visible error state.” Any feature-specific visual claim must name the inspected features and views. Endpoint readiness may be reported without a visual claim.
- Acceptance boundary: preview readiness is separate from CAD/source, written artifact/slicer, and physical print/assembly acceptance. The locked STEP remains a historical reference, not restart CAD.
- Preserve: all CAD/reference bytes; prior iteration history; `.gitignore`'s `__cadgen__/` exclusion; cleanup/Trash recovery state; branch retention; and all existing CAD, slicer, and physical acceptance boundaries.
- Remove: `bin/preview-cad`, `tests/test_preview_cad_launcher.py`, and `projects/kage/manifests/cad-viewer-runtime-0.4.25.sha256`.

## Done gate

The repository and Kage documentation name only the direct installed Viewer workflow; the obsolete launcher, launcher tests, and runtime pin are absent; the candidate closure is exact; deterministic repository/Kage tests pass; and distinct critic, validator, and formal reviewer roles independently join on one frozen candidate. Only the validator may supply live Viewer evidence for this candidate.

## Delegated task DAG

| ID | Role / owner | Dependency | Exclusive writes | Done gate | Status |
|---|---|---|---|---|---|
| KAGE-PREVIEW-DIRECT-001 | design / `/root/direct_viewer_design` | none | none | direct-workflow contract frozen | complete |
| KAGE-PREVIEW-DIRECT-002 | implementation / `/root/direct_viewer_impl` | 001 | bounded root/Kage docs, launcher removal, integrity test and candidate | deterministic implementation receipt; no live Viewer and no approval | in progress |
| KAGE-PREVIEW-DIRECT-003 | critic / distinct root-assigned identity | 002 | `REVIEW.md` only | adversarial false-positive and stale-instruction audit | pending |
| KAGE-PREVIEW-DIRECT-004 | validator / distinct root-assigned identity | 002 | `VALIDATION.md` only | deterministic gates plus exact live page/artifact/visual evidence | pending |
| KAGE-PREVIEW-DIRECT-005 | formal reviewer / distinct root-assigned identity | 003, 004 | `REVIEW.md` only | provenance and finding-disposition join | pending |
| KAGE-PREVIEW-DIRECT-006 | root delivery / `/root` | 005 | continuity/delivery only | deliver accepted candidate through PR | pending |
