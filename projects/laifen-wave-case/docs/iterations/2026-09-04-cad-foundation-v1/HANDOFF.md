# P1 R7 parametric-core refactor handoff

**Status:** complete — CAD/source and written STEP PASS; slicer HOLD; physical PARTIAL / UNBOUND  
**Frozen design fingerprint:** `1c233c8c64f0e7cb87919b601435318f6402a96cd3ad19af0fdb7251e908ed83`  
**Frozen manifest entries:** 57

**Candidate:** `6d58e564885c317c62f9b2e89652a9d7f9be04b82df797f9ccc70fc33e99a304`  
**Implementation evidence:** `0214bd39e094aed9bf84a0cfedde97cb795a2a946ccb7cd25bb84c989f250acc`  
**Formal review join:** `scratch/container-generator-v1-formal-review/review-join.sha256`, SHA-256 `2d5715f20a7e211cd98e4d1af0b5ec91046157b980a514a1cd8fc7b6f3a0363c`  
**Private CAD Viewer:** <https://mac-mini.duckbill-ionian.ts.net:8449/Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case?file=cad/container_generator_v1/closed.step.py>

The implementation, independent validation/recovery, critique, and formal join are complete. The grouped package and four STEP outputs are the current refactor authority. The old Foundation V1 web candidate is stopped and superseded. Remaining next work requires a new user-directed slicer or physical validation contract.

## Implementer allowed writes

`IMP-CAD-CV1-01` exclusively owns:

- `projects/laifen-wave-case/cad/container_generator_v1/**`
- `projects/laifen-wave-case/tests/test_container_generator_v1_parameters.py`
- `projects/laifen-wave-case/tests/test_container_generator_v1_source_equivalence.py`
- `projects/laifen-wave-case/tests/test_container_generator_v1_step_equivalence.py`
- `projects/laifen-wave-case/tests/test_container_generator_v1_requirements.py`
- `projects/laifen-wave-case/scratch/container-generator-v1-implementation/**`
- this iteration's future `IMPLEMENTATION.md`, `candidate-files.sha256`, and `evidence-files.sha256`

All P1 R7 files, old tests/artifacts/evidence, P2 preview source, live routes/services, quarantine, requirements, decisions, printing profile, and continuity records are read-only to the implementer. No package/environment changes are authorized. Run Python through root `uv`/Python 3.12.

## Implementer done gate

1. Verify all frozen inputs before writing and report the design fingerprint.
2. Create the standalone new package and four focused tests without altering P1 R7.
3. Pass cheap registry/derive/scope tests, then direct old/new native default-solid equivalence.
4. Generate exactly `body.step`, `cap.step`, `closed.step`, and `print_layout.step`; no STL/3MF/GLB.
5. Pass actual-solid validity/collision/engagement/wall/drain/boundary checks, source-to-STEP parity, P1 R7-to-new STEP equivalence, named datum/placement checks, and print-layout bed/nonoverlap checks.
6. Run CAD inspect validate/refs/facts/planes/positioning plus targeted measure/align/frame, then render and inspect the required actual-STEP snapshot set.
7. Freeze source/tests/STEP in `candidate-files.sha256` and compact commands/results/facts/snapshots in `evidence-files.sha256`. Record any permitted serialization-only variance explicitly.
8. Write `IMPLEMENTATION.md` with exact commands, durations, hashes, baseline deltas, requirement coverage, repair count, and remaining slicer/physical gaps. Stop; do not self-validate or promote.

After candidate freeze, distinct `VAL-CAD-CV1-01` and `CRIT-CAD-CV1-01` owners work read-only against the same candidate. `REV-CAD-CV1-01` joins only after both complete. Initial attempt plus two focused repairs is the limit. A geometry difference, P1 R7 mutation, new feature, third repair, or undocumented STEP-byte variance stops the task.

The user's physical report selects the baseline but is not an exact artifact acceptance receipt. Slicer/process and full physical acceptance remain HOLD after any CAD/STEP PASS.
