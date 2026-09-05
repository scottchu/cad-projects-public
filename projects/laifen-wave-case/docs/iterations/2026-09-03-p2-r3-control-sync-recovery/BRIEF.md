# P2 R3 control-sync recovery brief

**Iteration:** `2026-09-03-p2-r3-control-sync-recovery`
**Design owner:** DES-GCS-REC-01
**Exact baseline:** P2 R2 repair-2 candidate manifest SHA-256 `32429b0817e918343959be9cfe783a8ae76a2d00e0a35b9903b77c71ef6f34b6`.

## Narrow reason for reopening

Independent repair-2 validation passed all repaired geometry, camera, pattern, accessibility, invalid-state, end-control and marker gates, but found one P1 control discontinuity. A percent edit changes canonical/derived `S` while leaving the editable mm input stale at `60`; an immediate mm keyboard edit overwrites canonical `S` with a value near `60.4`. P2 R2 remains HOLD and is preserved without modification.

This R3 recovery resolves only GCS-02's control-synchronization surface and the stale implementation-receipt pointer. It is not a reopening of the generic-container architecture or any passing repair-2 visual gate.

## Stable recovery requirements

| ID | Requirement | Evidence target |
| --- | --- | --- |
| REC-01 | `raw.S` remains the one canonical split value; mm and percent inputs are projections/adapters, never competing sources. | Browser state trace and pure helper test. |
| REC-02 | Every successful percent edit recomputes and synchronizes raw `S`, derived percent, mm input, percent input, bounds, all readouts and scene in one render transaction. | Exact endpoint regression. |
| REC-03 | Every height edit recomputes dynamic S/percent bounds using the new raw `H` and current raw `S`, then repopulates both controls without reparsing a formatted display string. | H-change regression and raw-value assertion. |
| REC-04 | At H261 sequence endpoints, percent-min maps to S12.4 and percent-max maps to S248.6 in model, readout and mm DOM input. | Real browser assertion, not source-text inference. |
| REC-05 | The S control has derived `min=S_min`, `max=S_max`, `step=0.1`. At exact maximum 248.6, native ArrowUp remains 248.6 because the next 0.1 step exceeds max; canonical raw S and percent remain at max. | Keyboard browser regression. |
| REC-06 | Repair-2 candidate geometry/camera/pattern/accessibility/end controls remain byte-identical except `app.js`, `tests/test_generic_container_simulator.mjs`, and required recovery receipts/manifests. | Candidate parity/delta manifest plus focused reruns. |
| REC-07 | The active receipt pointer names P2 R2 repair 2 and the forthcoming P2 R3 recovery receipt. | Formal-review provenance check. |

## Delta mask and forbidden scope

| Object | Allowed delta | Forbidden change |
| --- | --- | --- |
| `preview/.../app.js` | one canonical-state-to-controls synchronization path; dynamically set `S` min/max/step and canonical values after relevant edits | scene construction, camera fitting, pattern field, marker/end/drain/accessibility behavior, styling, dependency URL and unrelated control semantics. |
| `tests/test_generic_container_simulator.mjs` | exact UI/control regression and focused source assertions | weaken/delete passing repair-2 coverage or change acceptance thresholds. |
| P2 R3 receipts/manifests | recovery provenance only | alter P2 R2 historical receipts/evidence. |
| all other candidate source/test bytes | none | any mutation. |

No route/static service, CAD, mesh, slicer, printer, project index/status, R7, P2 R1, or P2 R2 file may change. Existing `/container-simulator` delivery remains blocked until formal recovery review passes.

## Planned source, test and route target

Implementation changes only existing P2 R2 `preview/p2-r2-generic-container-simulator/app.js` and `tests/test_generic_container_simulator.mjs`, then writes P2 R3 `IMPLEMENTATION_RECOVERY.md` and immutable candidate/evidence manifests. The eventual isolated delivery target remains `https://mac-mini.duckbill-ionian.ts.net:8448/container-simulator`; delivery must not change any existing private/public route or service.

## Recovery DAG

| ID | Role / owner class | Depends on | Exclusive writes | Done gate and ceiling |
| --- | --- | --- | --- | --- |
| DES-GCS-REC-01 | design, Terra/high | repair-2 baseline | this P2 R3 contract/inputs/pointer | 8 min, 6k output, initial + one document repair. |
| IMP-GCS-REC-01 | implementation, Terra/medium | R3 baseline fingerprint | permitted app/test paths plus P2 R3 implementation receipt/manifests | Exact sequence passes under browser control; 12 min, 8k output, initial + one focused repair. |
| VAL-GCS-REC-01 | independent validation, Sol/high | frozen recovery candidate | P2 R3 validation receipt/evidence and scratch only | Reproduce exact keyboard trace; verify byte parity for protected files; 10 min, 7k output, initial + one method repair. |
| CRIT-GCS-REC-01 | independent critique, Terra/medium | same candidate | P2 R3 critique receipt/evidence and scratch only | Check user-facing continuity and no new stale/discontinuous control state; 8 min, 5k output, initial + one focused finding. |
| REV-GCS-REC-01 | formal review, Sol/high | VAL + CRIT exact receipts | P2 R3 review receipt/manifest only | Join scope/parity/provenance, including receipt pointer; 7 min, 5k output, initial + one provenance repair. |
| DEL-GCS-REC-01 | private delivery, fast/low | formal PASS | only isolated route configuration/readiness receipt | Confirm `/container-simulator` local/private response, then require user-device check; 6 min, one retry. |

VAL and CRIT may run in parallel after an implementation candidate is frozen; REV joins them. Stop immediately if a proposed repair changes a protected candidate file, relies on rounding for state, or cannot specify the raw post-event `S`. A candidate change requires the affected independent gates to rerun on its new manifest.
