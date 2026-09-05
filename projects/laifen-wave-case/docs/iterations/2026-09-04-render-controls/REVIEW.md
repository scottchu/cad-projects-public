# RCV-05 formal independent review

**Verdict: PASS for the exact Viewer render-preview candidate and its independently validated private delivery surface.** This verdict joins the frozen design, implementation, independent critique, and independent validation receipts. It does not approve any CAD, STEP, slicer, print, or physical change.

## Frozen provenance

- Design fingerprint: `2ac420ce1eb43f6adb12d39d41416a24167a7ef7a3990a490107f8caed5a80e4`.
- Candidate fingerprint: `8e6ac223dd9e8ff5539120bfb0d8ffcc20dd7d38f801bb0e08a945a5520c3a60`.
- Implementation evidence: `b56b6882497b9ff68cc004dc36bc846e36c49c7121578a0d7f2a6906cc8d6876`.
- Critique evidence: `660ca14b16c051594afc556a571e7326ca177a3c3e7863979ecc8deff274afa4`.
- Validation authority: this iteration's `VALIDATION.md` and `VALIDATION_EVIDENCE_MANIFEST.sha256`, which record PASS against the same candidate fingerprint.
- Independently served `closed.params.js`: SHA-256 `20abaef22b3dbe6c381aa528f5ace3d7b253ed99dcda352d70a5520dd2aa1076`, byte-identical to the reviewed sidecar.

Direct manifest and test re-execution by this formal-review role was unavailable because the host exhausted file descriptors. This review therefore joins the already frozen, independently recorded implementation, critic, and validator fingerprints and receipts. It does not claim an additional formal-review rerun.

## Join decision

The critic's only blocking finding was conditional: the exact private delivery surface had not yet been independently checked. RCV-04 closes that condition for candidate `8e6ac223…` by recording all of the required delivery evidence:

- the exact private page returned HTTP 200;
- the exact artifact endpoint returned HTTP 200 with `state == "ready"`;
- the served sidecar matched the committed sidecar byte-for-byte;
- the generated descriptor identified `closed.step.py`, the accepted closed STEP, two occurrences, and the exact authored body and cap names required by the two sidecar features;
- the focused suite passed seven tests and the independent Node effects mock confirmed 52 rows, zero default effects, correct common scale, one-turn `+360°` and `+2 mm` cap motion, and part-specific style targeting;
- desktop/mobile changed and reset observations showed that scale, screw motion, color, and opacity affect the display while Reset restores the accepted closed pose and source colors;
- native tree visibility remained available; and
- all four accepted STEP files remained byte-identical.

The critique's P2 delivery-surface block is therefore resolved. No source, target-resolution, transform-order, zero-state, reset, disclosure, readout-preservation, native-control, or STEP-parity blocker remains in the joined evidence.

## P3 mobile limitation

At 390 × 844, the right-hand numeric value boxes clip horizontally because the STEP sheet occupies most of the viewport. The disclosure, all ten labels and sliders, and the unchanged read-only snapshot remain visible and usable; exact-value fields remain accessible at a normal viewport. This is a real responsive presentation limitation and should remain recorded for a later Viewer UI refinement. It does not change render-control math, targeting, reset behavior, or STEP parity, so it does not block this candidate.

## Acceptance boundary

This PASS covers only the frozen Viewer-time sidecar effects and the independently observed private delivery presentation for candidate `8e6ac223…`. The controls deform or style the displayed tessellated mesh. They do not edit build123d source, regenerate or rewrite STEP, or prove transformed dimensions, wall thickness, bore size, thread clearance, collision freedom, fit, drainage, strength, printability, slicer behavior, or physical performance.

- Render preview and private delivery surface: **PASS** for the exact candidate.
- CAD/source: inherited accepted state; unchanged by this iteration.
- Written STEP: inherited accepted state; independently recorded byte-identical.
- Slicer/process: **HOLD**.
- Physical acceptance: **PARTIAL / UNBOUND** and unchanged.

No service mutation, CAD generation, STEP generation, slicing, printer action, or physical acceptance is authorized by this formal review.
