# REV-GCS-REC-01 formal independent review

**Status: PASS for the exact browser visual-intent simulator candidate and local/static execution.** Owner `/root/gcs_formal_review`, formal independent-review join role, Sol/high. The delivery worker may add only the isolated private `/container-simulator` route and perform its route-specific readiness checks. This verdict does not approve CAD, OpenSCAD, STEP, mesh, slicer, print, physical behavior, or MakerWorld publication.

## Frozen provenance

- Formal review join: `inputs/review-join.sha256`, 217 entries, SHA-256 `7e89663ea2d341f68b2c5e0f192df00a733481f677e9756bc31544e5f8523c3d`; every entry passed before this receipt was written.
- Upstream P2 R2 design fingerprint: `aea717d84cc31b67b345ed9367f6c5ae72b2a370291aa55e75ce1662238574df`.
- Upstream P2 R2 repair-2 candidate manifest: `32429b0817e918343959be9cfe783a8ae76a2d00e0a35b9903b77c71ef6f34b6`.
- P2 R3 recovery design fingerprint: `cc4c378fe3b398ead900b1bf39a94bf8b1e94f21599c4219bb3f55b6af1fdf61`.
- Exact reviewed recovery candidate manifest: `15c7c0503e87ec0f0b1a828fb62d471baaefc9a6caecf629d14d4504d0d19224`; all five declared candidate entries pass.
- Independent validator evidence: `40929b882d69cfac7c9c48c2da842bf20eabff12a58098952c906f622414ffbb`, PASS.
- Independent critic evidence: `dc3af7cd22df37eb25005d52d14c42b21e6bc54c611ad4b13eadcae83eacfe1f`, PASS.
- Protected parity manifest: `d4cdd20ddf527d8f1733724b7f67d897defbdd740831a1705cce953e3bf17e35`, PASS.

The P2 R3 `RECEIPT_POINTER.md` correctly identifies P2 R2 `IMPLEMENTATION_REPAIR2.md` as the incoming source receipt and P2 R3 `IMPLEMENTATION_RECOVERY.md` as the current implementation receipt. The stale P2 R2 `IMPLEMENTATION.md` is preserved only as earlier history and is not used as current-candidate authority.

## Candidate delta and protected scope

Relative to the exact P2 R2 repair-2 candidate, only the two authorized candidate paths changed:

| Path | P2 R2 repair 2 | P2 R3 recovery | Disposition |
| --- | --- | --- | --- |
| `preview/p2-r2-generic-container-simulator/app.js` | `c396b18bae19c44c80582637168fa40f83d1e94225af4d9bb8924fdf42ba6588` | `575f3734f76dd6313ccc9e33b33ffb72008292c20b4dbfc3f5db517d9789affe` | Authorized canonical-control synchronization change. |
| `tests/test_generic_container_simulator.mjs` | `237c1ef273dc1b42b349ea7a52f622f7f8e75811157d94d7b8fc10ba0cb2ef69` | `7b873ff25591fbb9748984bc5345f5eb18e62c75eecd97bb10e6f9defe9be90c` | Authorized focused regression change. |

The other three candidate paths remain byte-identical to repair 2: `index.html` `ace28e8d…`, `math.mjs` `b3e4c734…`, and `style.css` `a19c755c…`. The recovery manifests and receipts are provenance additions outside the candidate source/test set. No route, service, CAD, project index/status, package, slicer, printer, P2 R1, or P2 R2 historical receipt was changed by this recovery.

The manifest audit checked 267 entries across the 13 current/final referenced manifests. Its only old-hash differences were the same authorized app/test replacement repeated by P2 R2 and P2 R3 baseline records; there were no unexpected mismatches. Superseded attempt manifests remain historical snapshots and are not current-candidate manifests.

## Independent evidence and formal spot checks

The independent validator and critic both used the exact recovery candidate read-only and reproduced the real browser trace. At H261, percentage minimum and maximum synchronize canonical `S`, the visible millimetre input, percentage input, readout, status and scene. At `S=248.6`, ArrowUp remains at the exact maximum. A reverse millimetre edit to `120.125` and subsequent H311 edit preserve canonical S while recomputing the direct unrounded percentage and both dynamic bounds.

The earlier P2 R2 repair-2 visual/camera/geometry/accessibility/end/pattern evidence remains applicable only where the protected hashes and current focused smoke support inheritance. `index.html`, `math.mjs`, and `style.css` are byte-identical. The current validator and critic then rechecked the changed `app.js` in real Chrome, retained both named pieces, a non-null camera fit, clean runtime, and matching readout/scene state for Laifen and wide-short presets. This supports the earlier framing, two-piece topology, marker, end, pattern, invalid-state and accessibility conclusions without claiming that the whole current page is pixel-identical to repair 2.

The formal reviewer independently ran a local static server and browser smoke from `scratch/generic-container-formal-review/`. It passed HTTP loading, percent-max synchronization, native ArrowUp behavior, H311 continuity, named two-piece scene structure, and a short/wide H42 × OD80 case at both one and two selected turns. With pitch 1.4 mm and lead/runout 0.5 turn, the actual page reported:

- one turn: effective engagement `E=1.4 mm`, full visual band `P=2.1 mm`;
- two turns: effective engagement `E=2.8 mm`, full visual band `P=3.5 mm`.

Thread pitch, turns, lead/runout, form-height reference, clearance per side, and smooth keepout are editable controls. They remain visual/accounting parameters, not a generated helical thread or printable fit claim.

## Requirement coverage

| Requirement | Formal disposition |
| --- | --- |
| GCS-01 | PASS. Generic, Laifen, wide-short jar and H42 × OD80 cases derive valid, visually distinct two-piece forms. |
| GCS-02 | PASS. P2 R3 closes the stale mm/percent control defect with one canonical unrounded `raw.S`. |
| GCS-03 | PASS for visual/semantic global-Z datums and two closed-end references. |
| GCS-04 | PASS. One, two and three turns derive `E=pitch*turns`; actual browser smoke covers one and two short-thread cases. |
| GCS-05 | PASS. Dynamic bounds, strict domains, exact infeasibility text and invalid-output suppression remain covered. |
| GCS-06 | PASS for visual topology. Exactly two exterior piece groups meet at one seam; line markers are annotations rather than a third tube. |
| GCS-07 | PASS. Four pattern controls, physical pitch derivation, global-Z phase and seam clipping remain protected and tested. |
| GCS-08 | PASS. Main relief remains true scale and the labelled magnifier discloses its scale/depth. |
| GCS-09 | PASS. Text status, accessible field relationships, named markers and grouped responsive controls remain covered. The previously reported one-pixel rotated scale-label residue is accepted as minor presentation residue and is not a source/local-static blocker. |
| GCS-10 | PASS to the delivery gate. No route changed during implementation/review; DEL-GCS-REC-01 may add only `/container-simulator`, then must verify that local and private responses load the exact reviewed bytes. User-device comprehension remains a later explicit gate. |
| REC-01 through REC-07 | PASS. Canonical state, percent/height transactions, exact endpoints, keyboard continuity, protected parity and receipt provenance all match the recovery contract. |

## Prior finding disposition

Every earlier P1/P2-severity finding has an explicit outcome for this candidate:

- P2 R1 `V-MW-01`, `V-MW-02`, `V-MW-03`, and `V-MW-04` were closed by its repair 1 and remain covered by the P2 R2/R3 replacement controls, non-overlapping exterior, dynamic bounds and accessible names. `V-MW-05` was superseded by P2 R2 and is closed for this visual gate through its global-Z labels, four distinct patterns and current camera evidence.
- P2 R1 `R1-MW-01` was superseded and closed by P2 R2's external line brackets and labelled global-Z scale. Critic findings `C-MW-01` through `C-MW-04` are respectively closed by the non-overlapping exterior, exact endpoint-safe adapter, attached line-marker accounting, and protected accessible/distinct pattern presentation. User pattern taste remains a user confirmation question, not a source/local-static defect.
- P2 R2 initial validator findings `GCS-V01` through `GCS-V05` are closed by strict domains, line markers, aspect-aware camera fit, visible closed ends/chamfer/drain indicators, and field-level error relationships in repair 2.
- P2 R2 repair-1 validator findings `GCS-R1-V01` through `GCS-R1-V04` are closed by repair 2's camera fitting, invalid-state suppression, end-control rendering and accessible field associations.
- P2 R2 critic findings `C-GCS-01` through `C-GCS-04` have explicit PASS dispositions in `CRITIQUE_REPAIR2.md`; protected hashes plus the current targeted browser checks preserve their applicability.
- P2 R2 repair-2 `GCS-R2-V01` is closed by the exact P2 R3 percent/mm/ArrowUp browser trace. `GCS-R2-V02` is closed by `RECEIPT_POINTER.md` and the current `IMPLEMENTATION_RECOVERY.md`.

No unresolved P1 or P2 source/local-static finding remains.

## Commands and delivery boundary

Formal checks included:

```sh
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r3-control-sync-recovery/inputs/implementation-recovery-candidate.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r3-control-sync-recovery/inputs/implementation-protected-parity.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r3-control-sync-recovery/inputs/implementation-recovery-evidence.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r3-control-sync-recovery/inputs/validation-inputs.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r3-control-sync-recovery/inputs/validation-evidence.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r3-control-sync-recovery/inputs/critique-evidence.sha256
node projects/laifen-wave-case/tests/test_generic_container_simulator.mjs
uv run --package laifen-wave-case python projects/laifen-wave-case/scratch/generic-container-formal-review/audit_manifests.py
uv run --package laifen-wave-case python projects/laifen-wave-case/scratch/generic-container-formal-review/browser_smoke.py
```

DEL-GCS-REC-01 may now add the isolated private `/container-simulator` route. It must leave `/laifen-chamfer`, `/laifen-full`, `/laifen-full-section`, CAD Viewer private 8449 and unrelated public 3245 untouched, prove local/private HTTP readiness for the exact reviewed bytes, and retain the user-device visibility/comprehension check as pending until the user performs it. CDN availability on the user's device is also outside this source/local-static PASS.

This review does not authorize or imply CAD/OpenSCAD generation, STEP or mesh output, actual thread form or tolerance, wall/clearance validity, drainage, fit, strength, printability, slicing, printer action, physical acceptance, or MakerWorld publication.
