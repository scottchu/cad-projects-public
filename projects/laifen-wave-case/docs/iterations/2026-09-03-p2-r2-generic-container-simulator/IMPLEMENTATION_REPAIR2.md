# IMP-GCS-02 repair 2 implementation receipt

**Status:** repair 2 candidate frozen for new independent validation and critique. This is the final permitted implementation repair; it does not authorize delivery.

## Provenance and preserved evidence

- Verified frozen design-input fingerprint: `aea717d84cc31b67b345ed9367f6c5ae72b2a370291aa55e75ce1662238574df` for `inputs/current-baseline.sha256`.
- Verified incoming repair-1 manifest-file SHA-256: `8e3d7cd62d4c46c80a0d11865bc8fc39a36e1f943920e3051e130f948ec29e81`.
- Preserved that exact manifest at `inputs/implementation-repair1-candidate.sha256` and copied its five declared source/test bytes to `scratch/generic-container-impl/repair1-source/`; the local `manifest.sha256` verifies all five copies.
- New repair-2 candidate manifest-file SHA-256: `32429b0817e918343959be9cfe783a8ae76a2d00e0a35b9903b77c71ef6f34b6`.
- Repair-2 evidence manifest-file SHA-256: `ca38256e85859139902f0aeecdbfc6b6b5ee871e3e063a38c443797ab36bd9a2`.

## Changed candidate

- `preview/p2-r2-generic-container-simulator/index.html` groups controls into semantic collapsible **Size & split**, **Thread**, and **Surface & ends** sections. Preset, assembled/exploded view, and the intent question remain outside the groups. Thread pitch, 1/2/3 turns, lead/runout, form-height reference, per-side clearance, and smooth keepout are editable.
- `math.mjs` replaces `math.js`, preserving the frozen derivation and global-Z pattern field while adding stable `fieldErrors`, guarded percent conversion/bounds, and a pure aspect-aware camera fit derived from vertical and horizontal FOV.
- `app.js` fits an oblique camera to an actual Three.js `Box3` containing both pieces and both line brackets after every valid build and `ResizeObserver` callback. It sets target, distance, near, and far from the fit result.
- Invalid states clear all scene children, clear and mark the detail canvas unavailable, hide the axial scale, set every derived value to exactly “Unavailable until parameters are valid”, remove stale fit state, announce only exact error reasons in a shared alert, and associate each responsible field through `aria-invalid`, `aria-errormessage`, and `aria-describedby`.
- Closed-end side radii now taper linearly by the requested chamfer, pattern relief fades through that band, reduced-radius end faces close both global outer ends, and named dark drain apertures appear at deterministic center/ring positions only while drains are enabled with a positive count. These remain display-only references.
- Non-solid `LineSegments` retain distinct full/effective scene brackets. The responsive DOM global-Z scale labels `P … visual thread band` and `E … effective`, maps both intervals from the assembled global coordinates, and supplies an accessible textual equivalent in assembled and exploded views.
- `tests/test_generic_container_simulator.mjs` changed from repair 1 and covers all prior preset/turn/bounds/round-trip/global-Z checks plus short one-turn configuration, strict domains and field IDs, aspect-aware fit math/calls, ResizeObserver wiring, invalid-state suppression, ARIA associations, end/drain scene variation, marker semantics, and the grouped mobile controls.

## Commands and results

`node projects/laifen-wave-case/tests/test_generic_container_simulator.mjs` — PASS; stdout: “generic container simulator repair2 checks passed”.

`.venv/bin/python3 -m http.server 8997 --bind 127.0.0.1 --directory projects/laifen-wave-case/preview` plus `.venv/bin/python3 projects/laifen-wave-case/scratch/generic-container-impl/repair2/capture.py` — PASS at 1024×900, 390×844, and 412×915; HTTP 200, no console/page errors, no horizontal overflow. Runtime probes show `ResizeObserver` refits at every viewport, distinct assembled/exploded marker names, drain scene objects present/on and absent/off, and empty invalid scene/detail/scale state.

`shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r2-generic-container-simulator/inputs/implementation-candidate.sha256` — PASS for all five exact repair-2 candidate files.

`(cd projects/laifen-wave-case/scratch/generic-container-impl/repair1-source && shasum -a 256 -c manifest.sha256)` — PASS for all five preserved repair-1 files.

## Screenshot inspection

The exact post-test repair-2 source was captured and visually inspected. In the 1024×900, 390×844, and 412×915 Laifen images, teal and orange pieces, the seam, external line brackets, closed upper end, drains, and the labelled global-Z scale are all visible with margin. The H88/OD120 wide form fits fully at every width. The wide-short jar shows a clear 6 mm end taper and five dark apertures when enabled; its paired off-state removes all apertures. Assembled and exploded images retain exactly two exterior pieces and keep marker geometry as lines. Invalid H=20 images show a blank 3D viewer and an unavailable detail surface; the full phone page shows the exact feasibility formula, linked fields, and unavailable derived values.

Evidence is in `scratch/generic-container-impl/repair2/`, including `browser-evidence.json`, full/cropped invalid images, assembled/exploded Laifen images, wide-form images, paired drain images, test output, and the capture method.

## Requirement disposition

- **GCS-01/GCS-03/GCS-06:** implemented and visually evidenced for the supplied tall and wide-short forms plus H88/OD120 at all required viewports; camera fits actual scene bounds and preserves the two-piece mid-split topology.
- **GCS-02/GCS-04/GCS-05/GCS-07/GCS-08:** preserved and expanded with editable thread parameters, strict invalid suppression, and unchanged pure-math/global-Z tests.
- **GCS-09:** implemented with field-level associations, one live valid/warning/error status, named line markers, labelled DOM scale, semantic groups, and textual equivalents.
- **GCS-10:** untouched; no route, service, package, index, CAD, slicer, or printer state changed.

## Remaining boundary and next action

This remains a browser visual-intent simulator. It provides no CAD solid, actual helical thread, tolerance, wall, clearance, fit, drainage, strength, printability, slicer, or physical acceptance evidence. Independent validation and critique must verify the exact new candidate manifest before formal review; private route work remains blocked until that join passes.
