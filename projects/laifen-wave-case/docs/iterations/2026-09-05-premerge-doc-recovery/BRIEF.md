# LC-DOC-DES-01 — documentation and evidence recovery brief

## Objective

Repair only the pre-merge documentation/evidence defects identified by the
formal review for staged candidate
`515b249a19509e5509d4785a47e41896abc34d4d604494e708a0fe5afe33c624`.

The corrections are limited to: (1) the README's fresh-clone wording, (2) the
two stale evidence-manifest path sets, and (3) the missing live-route evidence
file named by `VALIDATION_DELTA_EVIDENCE.sha256`.

## Frozen facts

- The selected command contains 57 tests: **55 FRESH-CLONE-RELEVANT** and
  **2 LOCAL-FIXTURE-ONLY**. The latter consume excluded local R7 STEP fixtures;
  neither README nor validation may call all 57 fresh-clone evidence.
- The active OpenSCAD authority is
  `openscad/laifen_case_customizer_v1.scad`, SHA-256
  `ade77d3fcff4d5ba1c659838b4f9d24245584f0570834453b6e8c2b778047841`.
- The immutable R7 print-layout authority is
  `cad/p1_r7_end_chamfer/print_layout.step`, SHA-256
  `80fd95845b51da5266883614f9bf8eff60793a24d5c39b7321c9c6cb16d477a4`.
- Current private route to observe, without restarting or changing it, is
  `https://mac-mini.duckbill-ionian.ts.net:8448/openscad-simulator/`.

## Allowed writes for the recovery implementer

1. `README.md`: replace only the fresh-clone test description and surrounding
   command annotation so it distinguishes the 55 retained-input checks from
   the two explicitly named `LOCAL-FIXTURE-ONLY` checks. It must not claim that
   a clean clone was executed.
2. `docs/iterations/2026-09-05-premerge-cleanup/VALIDATION_DELTA_EVIDENCE.sha256`
   and `CRITIQUE_EVIDENCE.sha256`: correct relative paths using the method in
   `DESIGN.md`; preserve historical observations as observations, not passing
   claims.
3. Add `LIVE_8448_HEADERS.txt` and `LIVE_8448_INDEX.html` in the existing
   premerge-cleanup iteration from one read-only HTTP capture, then bind both
   actual files and hashes in `VALIDATION_DELTA_EVIDENCE.sha256`.
4. Add a concise recovery receipt in this recovery iteration and update the
   three continuity records only after independent review passes.

## Forbidden scope

No CAD/OpenSCAD edits or exports; no test, runtime, dependency, lockfile,
service, Tailscale, Trash/quarantine, staging, commit, push, PR, merge, or
printer changes. Do not regenerate meshes or STEP files.

## Done gates

The next independent roles must verify: every corrected evidence path resolves
from its containing manifest directory; every bound hash matches; the live
capture files exist and record an HTTP 200 response for the exact URL; README
uses the 55/2 split; authority hashes remain unchanged; and the candidate is
re-frozen before any merge decision.
