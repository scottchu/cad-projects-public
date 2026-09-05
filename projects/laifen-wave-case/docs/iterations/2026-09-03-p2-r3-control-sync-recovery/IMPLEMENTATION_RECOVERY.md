# IMP-GCS-REC-01 control-sync recovery implementation receipt

**Status:** recovery candidate frozen for independent validation and critique. Delivery remains blocked.

## Provenance

- Verified P2 R3 frozen recovery fingerprint: `cc4c378fe3b398ead900b1bf39a94bf8b1e94f21599c4219bb3f55b6af1fdf61` for `inputs/current-baseline.sha256`; every declared input passed before implementation.
- Exact upstream source receipt: P2 R2 `IMPLEMENTATION_REPAIR2.md`.
- Exact upstream repair-2 candidate manifest SHA-256: `32429b0817e918343959be9cfe783a8ae76a2d00e0a35b9903b77c71ef6f34b6`.
- Recovery candidate manifest-file SHA-256: `15c7c0503e87ec0f0b1a828fb62d471baaefc9a6caecf629d14d4504d0d19224`.
- Protected-file parity manifest-file SHA-256: `d4cdd20ddf527d8f1733724b7f67d897defbdd740831a1705cce953e3bf17e35`.
- Recovery evidence manifest-file SHA-256: `7e7bff59da4ef96ce4a4f8f421516e5309baebd2bf17fdcbb5676136e8056c2f`.

## Exact permitted delta

`preview/p2-r2-generic-container-simulator/app.js` now has one `syncControlsFromCanonical(rawState, derivedState)` output path. After an event updates canonical `raw` and `deriveContainer(raw)` succeeds, the helper synchronizes every control before scene, detail, readout, and accessibility rendering. It writes unrounded canonical `S`, derived S bounds, `S.step=0.1`, direct percent bounds/value, and `percent.step=any`. Invalid active input remains untouched until it becomes valid.

`tests/test_generic_container_simulator.mjs` retains all repair-2 checks and adds direct endpoint/reverse-projection math plus source-order guards for `event -> raw -> derive -> sync -> render`. It verifies exact control assignments and prevents the removed partial `populateForm`/`syncBounds` paths from returning.

No other candidate behavior was edited. The protected files remain byte-identical to repair 2:

- `index.html`: `ace28e8dd08de7f9ca9bf916887911e0d118c6dd4b0d2e6594f2a88950b878a5`
- `math.mjs`: `b3e4c734b166349251c9b7683aa23d428cb4d2f8f167ff29349def7dc024337b`
- `style.css`: `a19c755ca5c27dbe602283ba2652c5b2ff005c2a59266b078c5930b58ff6ccf3`

No route, service, CAD, index, package, P2 R1, slicer, printer, or unrelated source changed.

## Deterministic evidence

`node projects/laifen-wave-case/tests/test_generic_container_simulator.mjs` — PASS: `generic container simulator recovery checks passed`.

The exact browser reproduction ran through root `.venv/bin/python3` against a local static server at 1024×900:

1. Set H to 261: canonical S remained 60; S bounds became 12.4–248.6; percent bounds became 4.75095785440613–95.24904214559388.
2. Fill percent with its exact minimum: internal S, readout, and visible S input all became exactly 12.4.
3. Fill percent with its exact maximum: internal S, readout, and visible S input all became exactly 248.6.
4. Focus S and press ArrowUp: S stayed 248.6; percent stayed 95.24904214559388; readout and scene stayed at the same maximum.
5. Fill S with 120.125: percent became the direct `100*120.125/261` projection.
6. Change H to 311: S stayed 120.125; S bounds became 12.4–298.6 and both percent bounds/value recomputed from H311 without reparsing formatted output.

All numeric browser comparisons used relative and absolute tolerance `1e-12`. HTTP returned 200 with no console or page errors. Laifen and wide-short jar sanity captures retained both named pieces and valid camera fit. The percent-maximum full screenshot visibly agrees across S input, percent input, status, readout, bands, and scene.

Evidence paths are under `scratch/generic-container-sync-recovery/`: `browser_repro.py`, `browser-repro.json`, exact stdout, Node output, endpoint/ArrowUp full-page captures, and Laifen/jar camera captures.

## Requirement coverage and next action

- **REC-01–REC-05:** PASS in implementation evidence through the single canonical synchronization transaction and exact real-browser trace.
- **REC-06:** PASS for the three protected source hashes and bounded app/test delta.
- **REC-07:** this receipt follows the active pointer and names P2 R2 repair 2 as its source baseline.

This evidence does not independently approve the candidate. VAL-GCS-REC-01 and CRIT-GCS-REC-01 must inspect the exact recovery candidate manifest, then formal review must join their receipts before any private route action. CAD, thread-solid, fit, print, drainage, and user-device comprehension remain outside this recovery.
