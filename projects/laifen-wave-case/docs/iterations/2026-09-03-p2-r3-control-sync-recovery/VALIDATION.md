# VAL-GCS-REC-01 independent recovery validation

**Owner:** `/root/mw_sim_validate`, independent validator.  
**Status:** **PASS.** The exact recovery candidate fixes the percent/mm discontinuity on the actual page. The protected repair-2 surface remains byte-identical and the focused Laifen/jar camera smoke passes. Formal review may join this receipt with the independent critique; route delivery remains a later gate.

## Frozen provenance and scope

- Verified P2 R3 design fingerprint: `cc4c378fe3b398ead900b1bf39a94bf8b1e94f21599c4219bb3f55b6af1fdf61`.
- Verified recovery candidate manifest-file SHA-256: `15c7c0503e87ec0f0b1a828fb62d471baaefc9a6caecf629d14d4504d0d19224`; all five entries passed before and after execution.
- Validator input manifest SHA-256: `eda373fdb5aaad247e2126dd9fc19a97d55571ef3204d6bc9e928623e9ee1cb3`. It binds the recovery contract/receipt, prior exact HOLD evidence, candidate/parity/evidence manifests, root UV inputs and independent browser helper.
- Runtime: root UV Python 3.12, project Playwright/installed Chromium, Node, and temporary loopback HTTP `127.0.0.1:8998`.
- Candidate source/test and every route, service, CAD, index and prior receipt remained read-only. Writes are limited to this receipt, `inputs/validation*.sha256`, and `scratch/generic-container-sync-validation/`.

## Exact independent browser trace

At H261 the actual inputs expose `S.min=12.4`, `S.max=248.6`, `S.step=0.1`, percent min `4.75095785440613`, percent max `95.24904214559388`, and percent step `any`.

1. Filling percent with its exact minimum produces visible S `12.4`, internal derived S `12.4`, readout `12.400 mm / 4.75096%`, and scene `z0=248.6`.
2. Filling percent with its exact maximum produces visible S `248.6`, internal derived S `248.6`, readout `248.600 mm / 95.24904%`, and scene `z0=12.400000000000006`.
3. Focusing S at that maximum and pressing ArrowUp leaves visible/internal S at `248.6`, percent at its exact maximum, and the readout/scene unchanged. The prior stale-60/60.4 jump does not recur.
4. Filling S with `120.125` updates visible/internal S to `120.125` and percent to the direct unrounded projection `46.024904214559385`.
5. Changing H to 311 preserves visible/internal S `120.125`, recomputes percent to `38.62540192926045`, S bounds to `12.4..298.6`, and percent bounds to `3.987138263665595..96.01286173633441`.

All eight independent assertions pass with `1e-12` relative/absolute numeric tolerance. The page returns HTTP 200 with no console or page errors. `percent-max.png` and `percent-max-arrowup.png` visibly confirm agreement among both controls, status, readout, bands and scene.

## Protected parity and essential smoke

- Protected `index.html`: `ace28e8dd08de7f9ca9bf916887911e0d118c6dd4b0d2e6594f2a88950b878a5`.
- Protected `math.mjs`: `b3e4c734b166349251c9b7683aa23d428cb4d2f8f167ff29349def7dc024337b`.
- Protected `style.css`: `a19c755ca5c27dbe602283ba2652c5b2ff005c2a59266b078c5930b58ff6ccf3`.
- The protected-parity and implementation-recovery-evidence manifests verify fully.
- Candidate Node suite passes: `generic container simulator recovery checks passed`.
- Fresh Laifen and wide-short jar screenshots remain fully framed, show the two named pieces and mid-body seam, and expose a non-null camera fit. This smoke found no regression in the protected visual surface.

## Requirement disposition

| Requirement | Result |
| --- | --- |
| REC-01 canonical raw S | **PASS.** One internal/derived S agrees with both projections. |
| REC-02 percent transaction | **PASS.** DOM, derived state, readout and scene agree at both endpoints. |
| REC-03 height transaction | **PASS.** H311 preserves S and recomputes raw bounds/projection. |
| REC-04 exact H261 endpoints | **PASS.** 12.4 and 248.6 are exact at the control surface. |
| REC-05 native ArrowUp at max | **PASS.** S remains 248.6 and percent remains maximum. |
| REC-06 protected parity | **PASS.** Index/math/style hashes match repair 2. |
| REC-07 receipt provenance | **PASS.** Recovery receipt names repair 2 as source. |

## Commands and remaining boundary

```sh
node projects/laifen-wave-case/tests/test_generic_container_simulator.mjs
uv run --package laifen-wave-case python projects/laifen-wave-case/scratch/generic-container-sync-validation/validate.py
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r3-control-sync-recovery/inputs/implementation-recovery-candidate.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r3-control-sync-recovery/inputs/implementation-protected-parity.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r3-control-sync-recovery/inputs/validation-inputs.sha256
```

No method repair or acceptance-threshold change was required. CDN availability and comprehension on the user's actual device remain external acceptance boundaries. This focused recovery does not add CAD, thread-solid, mesh, slicer, fit, drainage, printing or physical evidence.
