# P2 Foundation V1 implementation handoff

**Status:** **STOPPED / SUPERSEDED** by user scope change on 2026-09-04  
**User authority:** exact response `Yes pass`  
**Frozen design fingerprint:** `46a37b6d61973c8b3287b67fa5b3c91b9df515e04e7f332c27cda6ab1edcb024`  
**Frozen manifest entries:** 15

The web candidate was frozen and received an independent visual-critique PASS, but independent validation and formal review were not completed. The user then chose to skip simulation and clarified that the existing printed first version is the correct baseline. Candidate manifest SHA-256 `1f4caa5befa635f5a31ee1933b220a02572d6e685183960819e30af0479866a6` remains historical and was never promoted or delivered. Do not resume its VAL/REV/delivery chain unless the user explicitly reopens it.

## Historical implementer scope

`IMP-GCS-FV1-01` may write only:

- `projects/laifen-wave-case/preview/p2-foundation-v1/**`
- `projects/laifen-wave-case/tests/test_p2_foundation_v1_derive.mjs`
- `projects/laifen-wave-case/tests/test_p2_foundation_v1_source_contract.mjs`
- `projects/laifen-wave-case/tests/test_p2_foundation_v1_scene.mjs`
- `projects/laifen-wave-case/tests/test_p2_foundation_v1_browser.py`
- `projects/laifen-wave-case/scratch/p2-foundation-v1-implementation/**`
- this iteration's future `IMPLEMENTATION.md`, `candidate-files.sha256`, and `evidence-files.sha256`

The implementer may read the frozen gate/R10 inputs and root dependency configuration. It may use the already-installed root-workspace Three.js dependency, but may not change package manifests or locks. R10, P2 R3, P1 R7, live services/routes, quarantine, prior previews/tests/scratch, CAD, OpenSCAD, exports, and project continuity files are read-only.

## Implementer done gate

1. Verify every entry in `inputs/frozen-inputs.sha256` before writing.
2. Implement only the accepted smooth V1 through the descriptor boundary and stable IDs in `DESIGN.md`.
3. Run all four prescribed test files from the repository root; every check passes without skip, expected failure, first-fail truncation, or no-op assertion.
4. Freeze exact source/tests into `candidate-files.sha256`; freeze test logs, compact mesh facts, and desktop/mobile screenshots into `evidence-files.sha256`.
5. In `IMPLEMENTATION.md`, report input fingerprint, candidate/evidence hashes, exact commands/results, changed paths, requirement coverage, repair count, and unresolved intent/CAD/physical gaps.
6. Stop after the immutable candidate receipt. The implementer does not validate, critique, review, serve, or promote its own work.

After candidate freeze, assign distinct `VAL-GCS-FV1-01` and `CRIT-GCS-FV1-01` owners. Assign `REV-GCS-FV1-01` only after both reports. Initial implementation plus two focused repairs is the maximum; every source repair creates a new candidate fingerprint and invalidates dependent reports.

P2 R3 remains the live visual authority and P1 R7 remains the CAD authority. Any later preview delivery must use an isolated route and requires VAL, CRIT, and REV PASS for one exact candidate.
