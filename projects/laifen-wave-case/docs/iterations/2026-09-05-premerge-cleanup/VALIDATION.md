# LC-VAL-02 independent validation — PASS

Owner: `/root/laifen_premerge_cleanup_validate`, independent of design, implementation and formal review. Date: 2026-09-05. Baseline: `d0aab1ff`. Validated staged candidate manifest `STAGED_FILES.sha256`: `96f5eceea77e8ab95716fc0212b72d85ba577b955825d5eea780d505307fb035` (1009 listed files; 1010 staged files including the manifest). All candidate bytes were rechecked at the start and end before writing this mutable validation receipt. This receipt supersedes LC-VAL-01 HOLD.

## Findings resolved

LC-VAL-01 identified bare `python3` recovery instructions and a customizer math test depending on an excluded scratch runner. The repaired `RECOVERY.md` uses `uv run python`. The test now invokes tracked `openscad/run_math_probe.mjs`; it executes successfully using the pinned WASM package. No remaining blocking cleanup finding.

## Independent results

| Gate | Result and evidence |
| --- | --- |
| Staged content | PASS: every manifest entry matches both Git index bytes (`git show :path`) and working file SHA-256; staged names equal the manifest paths plus the manifest itself. Listed content totals 504,396,146 bytes. |
| Git boundary | PASS: `git check-ignore --no-index --stdin` returns 1 with no ignored staged files. No staged entry reaches 100 MiB; largest is 74,416,394 bytes. Retained historical source stays included while excluded historical STEP fixture paths remain local. |
| Quarantine | PASS: independently traversed and rehashed all 27 mapped Trash roots: 617 regular files, zero symlinks, 210 directories, 1,303,210,296 bytes. Every path/content/type/size and each tree fingerprint matches the recorded inventory. All original roots are absent, all destinations exist, and PREMOVE/POSTMOVE are byte-identical. |
| Recovery | PASS: exact original/destination mappings remain available; restore code rejects an existing destination or missing source. Recorded spot-check pre/restored/final hashes are identical; current quarantined bytes were independently verified. Validator did not perform another restore. |
| Authority | PASS: OpenSCAD source `ade77d3fcff4d5ba1c659838b4f9d24245584f0570834453b6e8c2b778047841`; P1 R7 print layout `80fd95845b51da5266883614f9bf8eff60793a24d5c39b7321c9c6cb16d477a4`. All four retained `container_generator_v1` STEP files match the input manifest. |
| Current C3 evidence | PASS: C3 candidate manifest 9/9, retained build 6/6, delivery evidence 34/34 and C3 validation evidence 33/33 rehashed. Current implementation, validation and live presentation directories exist. |
| Live route | PASS: exact private simulator directory URL and all six built assets return HTTP 200 with matching hashes. Index response is `53210be5e3b21a509c449261c69a271619f6ce0475a32a6eff90af70098b30bb`. PID 2629 still uses this worktree's root `.venv/bin/python3`, port 8972, directory `projects/laifen-wave-case/scratch/presentation`. |
| Workspace locks | PASS: `uv lock --check` exits 0, resolving 72 packages. `npm ls --workspace=laifen-wave-case --depth=0` exits 0 with Three 0.176.0 and Vite 6.4.3. Root npm lock's workspace dependency declarations exactly match the project package. |
| Focused tests | PASS: 55 OpenSCAD/WASM/source/parameter/requirement/preview/frozen-authority tests plus two written STEP equivalence/hash tests, all exit 0. No CAD source or written artifact regenerated. |

`audit.json` and `final-audit.json` retain the ten largest staged files, exact retained STEP hashes, pinned vendor hashes and quarantine totals. `service-evidence.json` binds the preserved evidence manifests and each fetched HTTPS asset. These scratch files are diagnostic evidence, excluded from Git; this report and `VALIDATION_EVIDENCE.sha256` are the durable receipt.

## Commands actually run

All commands below ran from `/Users/scottchu/.codex/worktrees/4f8c/design-projects`. Validation scripts and outputs are under `projects/laifen-wave-case/scratch/laifen-premerge-cleanup-validation/` (abbreviated E below).

```sh
PYTHONDONTWRITEBYTECODE=1 uv run --frozen python projects/laifen-wave-case/scratch/laifen-premerge-cleanup-validation/audit.py
uv lock --check
npm ls --workspace=laifen-wave-case --depth=0
curl -fsS -o projects/laifen-wave-case/scratch/laifen-premerge-cleanup-validation/live.html -w '%{http_code}\n' https://mac-mini.duckbill-ionian.ts.net:8448/openscad-simulator/
ps -p 2629 -o pid=,command=
PYTHONDONTWRITEBYTECODE=1 uv run --frozen python projects/laifen-wave-case/scratch/laifen-premerge-cleanup-validation/run_tests.py
PYTHONDONTWRITEBYTECODE=1 uv run --frozen python projects/laifen-wave-case/scratch/laifen-premerge-cleanup-validation/service_evidence.py
PYTHONDONTWRITEBYTECODE=1 uv run --frozen pytest -q -p no:cacheprovider projects/laifen-wave-case/tests/test_container_generator_v1_step_equivalence.py::test_four_written_steps_are_valid_and_baseline_equivalent projects/laifen-wave-case/tests/test_container_generator_v1_step_equivalence.py::test_step_hashes_are_recorded_without_relaxing_geometry_or_scope
```

`run_tests.py` invokes `uv run --frozen pytest -q -p no:cacheprovider` on:

- `tests/test_openscad_customizer.py`
- `tests/test_openscad_wasm_simulator.py`
- `tests/test_vfr08_functional_repair.py`
- `tests/test_container_generator_v1_parameters.py`
- `tests/test_container_generator_v1_requirements.py`
- `tests/test_container_generator_v1_preview_parameters.py`
- `tests/test_container_generator_v1_source_equivalence.py::test_frozen_p1_r7_remains_hash_clean_and_new_package_is_standalone`

Paths are project-relative in this list; E/focused-tests.txt records the exact absolute command and all 55 passing results. E/step-tests.txt records the two passing written STEP cases. The final `audit.py` rerun returned PASS and confirmed the same candidate, original-root absence and all quarantine bytes after the harness was removed.

For the WASM math witness, the coordinator authorized one temporary ignored symlink at `preview/openscad-wasm-simulator/vendor` pointing to its exact matching quarantined vendor directory. Both runtime members first matched `dependency-lock.json`. A `finally` block unlinked only this symlink; the final path is absent. E/vendor-harness.txt records that boundary. No download, vendor copy, source mutation, service change or retained generated CAD resulted.

## Fresh-clone scope and limits

These 57 selected tests consume retained tracked source/current STEP files and declared Python/npm/pinned-WASM dependencies. They are **fresh-clone-relevant**, but no clean clone/install was executed. The pinned runtime was supplied by the verified temporary harness, equivalent in bytes to the declared dependency setup. Tests consuming ignored P1 R2–R6 STEP fixtures or historical scratch evidence remain **LOCAL-FIXTURE-ONLY**; none was counted or run in this pass. This is not a claim that unrestricted project-wide pytest passes on a fresh clone.

Written STEP checks imported the four retained baseline/candidate pairs, checked validity, topology counts, bounds, centers of mass, adaptive volume, face types and sorted vertex coordinates. Full native BREP reconstruction, new solid collision/motion gates, slicing and physical tests were intentionally not repeated for cleanup of unchanged authority bytes.

Actual user Safari/WebKit, browser chrome/safe-area/touch and screen-reader acceptance remain open. Existing Diamond browser HOLD includes the documented cancellation/late-result race and remaining detailed browser/mesh gates; Diamond controls stay disabled. OpenSCAD physical thread fit, drainage, support-free slicing and strength remain unproven. Existing print observations are not promoted to acceptance of the OpenSCAD candidate.

**Next action:** distinct formal reviewer joins this PASS with the bounded cleanup critique and candidate provenance; coordinator may then finish continuity and PR delivery. This validates cleanup and preservation, not new feature or physical acceptance.
