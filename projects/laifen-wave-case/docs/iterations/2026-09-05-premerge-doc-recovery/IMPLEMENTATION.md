# LC-DOC-IMP-01 — documentation and evidence recovery

Owner: `/root/laifen_premerge_docs_recovery_impl`. Date: 2026-09-05. Frozen input manifest: `3ca27ef088c0b6734dc6fac0b315d0a06a1ee176446a2e8aff8331d5f85278c2`; contract bundle: `cabec1112f62fbd27dc18b56cfe82f2d4188d5098e3a8c7ec0263cc983a3994f`.

## Corrections

- `README.md` now separates the 55 `FRESH-CLONE-RELEVANT` selections from the two explicitly named `LOCAL-FIXTURE-ONLY` checks. Repair cycle 1 places `test_step_hashes_are_recorded_without_relaxing_geometry_or_scope` in the 55 set, and places `test_frozen_p1_r7_remains_hash_clean_and_new_package_is_standalone` plus `test_four_written_steps_are_valid_and_baseline_equivalent` in the local-fixture set. It records LC-VAL-02's existing-worktree result and says that no clean clone or install was executed.
- Cleanup evidence manifests now resolve project-root references with `../../../`; the visual-fidelity handoff resolves through the sibling iteration.
- The exact private simulator URL was captured read-only into `LIVE_8448_HEADERS.txt` and `LIVE_8448_INDEX.html`. The headers record HTTP/2 200. Both files are bound in `VALIDATION_DELTA_EVIDENCE.sha256`; the nonexistent `live-8448-index.html` entry is gone.

## Checks actually run

Before repair cycle 1, I ran the then-written two-test command and it passed (`2 passed`, exit 0); that command included the STEP hash test now correctly classified in the 55 set. The pre-repair 55-selection command produced 54 passes and one environment failure because the intentionally ignored `preview/openscad-wasm-simulator/vendor/openscad.js` dependency is absent after cleanup. Per the repair instruction, I did not rerun either corrected selection. I did not recreate the dependency because this recovery forbids dependency/runtime and Trash changes. These checks do not replace or extend LC-VAL-02's prior passing result after its verified temporary dependency harness.

All paths in the corrected manifests resolve from the cleanup iteration. Current/superseding bindings and the two new capture bindings replay. The first LC-CRIT-01 section remains clearly labelled as historical snapshot observations; its old digests are not current-state claims.

Authority hashes remained unchanged: OpenSCAD `ade77d3fcff4d5ba1c659838b4f9d24245584f0570834453b6e8c2b778047841`; R7 print layout `80fd95845b51da5266883614f9bf8eff60793a24d5c39b7321c9c6cb16d477a4`.
