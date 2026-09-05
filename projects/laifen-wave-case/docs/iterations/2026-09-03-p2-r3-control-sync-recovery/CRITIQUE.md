# CRIT-GCS-REC-01 narrow control-sync recovery critique

**Status: PASS.** The actual browser trace keeps the millimetre and percentage
split controls as synchronized projections of one canonical split value. No
reopened P2 R2 visual gate regressed in this narrow recovery review.

## Provenance and scope

Owner: `/root/mw_sim_critic`, independent of implementation and validation.
The P2 R3 recovery input fingerprint is
`cc4c378fe3b398ead900b1bf39a94bf8b1e94f21599c4219bb3f55b6af1fdf61`.
The exact recovery candidate manifest
[`inputs/implementation-recovery-candidate.sha256`](inputs/implementation-recovery-candidate.sha256)
has SHA-256 `15c7c0503e87ec0f0b1a828fb62d471baaefc9a6caecf629d14d4504d0d19224`;
all five declared candidate files verified. Protected index, math and style
parity verified against the R2 repair-2 baseline. The recovery Node suite
passed.

The active continuity pointer correctly names P2 R2
`IMPLEMENTATION_REPAIR2.md` as the upstream candidate narrative and directs
formal review to this recovery’s `IMPLEMENTATION_RECOVERY.md`. The prior P2 R2
repair-2 visual critique PASS remains evidence for the protected visual scope;
this report neither repeats nor broadens that review.

This critic served the exact candidate read-only on loopback, drove Chrome with
the root-venv Playwright runtime, and inspected both saved screenshots. It
wrote only `scratch/generic-container-sync-critique/`, this receipt and the
evidence manifest. Candidate source/test, CAD, route, service, slicer, printer
and prior receipts were not changed.
The critique evidence-manifest SHA-256 is
`dc3af7cd22df37eb25005d52d14c42b21e6bc54c611ad4b13eadcae83eacfe1f`.

## Actual browser trace

At H=261, the page synchronizes S bounds to 12.4–248.6 mm and projects the
existing 60 mm split to 22.988505747126435%. Setting percent to its minimum
immediately produces S input/readout/derived state 12.4. Setting percent to
its maximum immediately produces `S=248.6`, `percent=95.24904214559388`, and
the matching scene seam/bands. At that exact S maximum, native ArrowUp leaves
the DOM value, derived state, readout, percent and scene unchanged at 248.6;
there is no stale 60 or 60.4 overwrite. The visible endpoint is captured in
`01-h261-percent-max-arrowup.png`.

A reverse mm edit to 120.125 produces the direct unrounded percentage
46.024904214559385. A subsequent H=311 edit preserves S=120.125, recomputes
the S maximum to 298.6 and projects percent to 38.62540192926045. The second
capture shows the inputs, status, readout and seam continuing to agree. Named
two-piece scene children remain present throughout valid states.

## Requirement disposition

| Requirement | Result | Evidence |
| --- | --- | --- |
| REC-01 / REC-02 | PASS | Percent min/max updates raw-derived S, both DOM controls, status/readout and scene in one valid update. |
| REC-03 | PASS | H=261→311 retains raw S=120.125 and recomputes both projection bounds directly from new H. |
| REC-04 / REC-05 | PASS | Browser endpoint is exactly 12.4/248.6; ArrowUp at 248.6 leaves all checked state at the maximum. |
| REC-06 | PASS | Protected parity manifest passed for index, math and style; candidate manifest confines the permitted code delta to app/test. |
| REC-07 | PASS | `RECEIPT_POINTER.md` names P2 R2 repair 2 as source and P2 R3 recovery receipt as the formal-review input. |

Labels remain clear (`Split from top S (mm)` and `Split from top (%)`), and the
full-page captures show matching raw-mm and percent readouts. No recovery
finding blocks formal review. This result does not add CAD, actual thread,
fit, drainage, print, slicer or user-device acceptance evidence.

## Commands

```sh
sha256sum -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r3-control-sync-recovery/inputs/implementation-recovery-candidate.sha256
sha256sum -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r3-control-sync-recovery/inputs/implementation-protected-parity.sha256
node projects/laifen-wave-case/tests/test_generic_container_simulator.mjs
/Users/scottchu/.codex/worktrees/4f8c/design-projects/.venv/bin/python3 -m http.server 8996 --directory projects/laifen-wave-case/preview
/Users/scottchu/.codex/worktrees/4f8c/design-projects/.venv/bin/python3 projects/laifen-wave-case/scratch/generic-container-sync-critique/browser_repro.py
sha256sum -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r3-control-sync-recovery/inputs/critique-evidence.sha256
```
