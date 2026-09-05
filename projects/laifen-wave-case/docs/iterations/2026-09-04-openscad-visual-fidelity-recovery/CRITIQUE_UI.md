# VFR-01U independent UX critique

## Scope and candidate

- Role: independent UX/accessibility critic; this is not formal review or CAD acceptance.
- Candidate: `candidate/UI_CANDIDATE.sha256`, repaired-candidate fingerprint `9f01d5eca03a58263a7716c57f39979128520021a670f59ab960f8a6e2778ebd`.
- Source evidence: `preview/openscad-wasm-simulator/index.html`, `style.css`, `src/main.mjs`, and `VALIDATION_UI.md`; candidate integrity and browser observations are taken from the independent validation receipt.
- Scope: mobile layout and reachability, validation/compiler failure feedback, raw diagnostics, and output identity. Geometry, worker behavior, STL content, deployment, and physical acceptance are out of scope.

## Findings

### UX-UI-01 — Mobile reachability: PASS

The responsive grid orders `preview` before `controls`; at `390x844`, validation measured a sticky result (`top: 0px`), a separately scrollable parameter form (`overflow-y: auto`, computed max-height `454px`), and bottom-sticky actions. The staged-route corroboration also measured the Generate control reachable at the viewport bottom with `44px` height. This meets the requested mobile reachability behavior.

### UX-UI-02 — Validation error does not identify the invalid control: P1 / REPAIRED, PASS WITH LIMIT

The repaired source now promotes the specific `#status` text into the assertive toast and appends `Adjust that value and try again`; the invalid-OD path therefore gives an actionable message instead of the former generic prompt. Focus remains on Dismiss and dismissal restores focus to Generate, as previously validated. The implementation still does not mark the offending input with an error state or `aria-invalid`, so this pass covers actionable toast copy and leaves direct field association as an unresolved accessibility enhancement.

### UX-UI-03 — Raw diagnostic line breaks are encoded literally: P2 / REPAIRED, PASS

The repaired `appendDiagnostic()` now appends `` `${text}\n` `` with a real newline, so expanded raw diagnostics retain separate readable entries. The collapsed `details` behavior and retention of the known localization warning remain passing requirements. No remaining issue was found for this finding in the repaired source.

## Repair-cycle disposition

- Repaired candidate manifest fingerprint: `9f01d5eca03a58263a7716c57f39979128520021a670f59ab960f8a6e2778ebd`.
- UX-UI-02: repaired from P1 partial fail to pass with limit; the toast now carries the specific validation status and recovery instruction. Direct invalid-field semantics remain unverified/unimplemented.
- UX-UI-03: repaired from P2 fail to pass; source now uses a real newline for each raw diagnostic entry.

### UX-UI-04 — Toast failure categories: PASS WITH LIMIT

The implementation separates validation, compiler, result-verification, and timeout paths in status/toast handling, and the browser validation confirmed a visible assertive toast for the invalid-OD case. Compiler and timeout toasts direct the user to diagnostics; mismatched results use a distinct verification message. The copy remains generic within each category and does not expose the underlying validation message in the toast itself (covered by UX-UI-02), but no identity or category conflation was observed.

### UX-UI-05 — Raw warning demotion: PASS

The browser validation confirmed `Could not initialize localization (application path is '/').` remains in the collapsed raw diagnostics and is absent from the primary status/toast surface. The source regex and log path preserve other diagnostics for the details region. The evidence supports the requested demotion of the proven non-fatal warning.

### UX-UI-06 — Output identity regression: PASS

The successful browser result was `Complete 58895df4a50f`, with download enabled. The validation receipt reports matching candidate source, worker, and schema fingerprints, and `src/main.mjs` rejects results whose identity, source hash, or lock fingerprint differs. No source, schema, worker, geometry, or generated STL identity change was found in this UI candidate.

## Unresolved risks and limits

- The supplied browser evidence covers Chromium at `390x844`; keyboard-only traversal, screen-reader announcement timing, zoom/reflow, contrast measurement, and touch behavior were not independently measured here.
- The validation receipt used an isolated local build and explicitly leaves the Tailscale delivery surface for a separate gate. The candidate should not be represented as delivery-surface validated until that exact route is checked.
- The two corrective opportunities above are presentation/diagnostic only; they do not justify changing OpenSCAD geometry or worker protocol.
