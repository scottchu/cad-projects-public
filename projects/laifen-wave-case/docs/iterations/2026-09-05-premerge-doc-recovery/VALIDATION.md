# LC-DOC-VAL-01 — independent documentation and evidence recovery validation — PASS

**Owner:** `/root/laifen_premerge_docs_recovery_validate`, independent of LC-DOC-DES-01, LC-DOC-IMP-01, critique, and formal review. Date: 2026-09-05.
**Frozen recovery bundle:** `cabec1112f62fbd27dc18b56cfe82f2d4188d5098e3a8c7ec0263cc983a3994f`.
**Supplied staged manifest:** `STAGED_FILES.sha256`, SHA-256 `ede603baef8ac0302a3ad044f4c32a8495b565dfd74e21293bcb660a1653761b` (1,012 immutable entries).

## Independent results

| Gate | Result |
| --- | --- |
| Immutable staged content | PASS. `shasum -a 256 -c STAGED_FILES.sha256` passed all 1,012 paths. Rehashing each `git show :path` blob against the manifest found 0 mismatches. The staged index has 1,019 paths: the 1,012 immutable paths plus seven declared mutable cleanup receipts (`CRITIQUE.md`, `CRITIQUE_EVIDENCE.sha256`, `STAGED_FILES.sha256`, `VALIDATION.md`, `VALIDATION_DELTA.md`, `VALIDATION_DELTA_EVIDENCE.sha256`, and `VALIDATION_EVIDENCE.sha256`). |
| README selection | PASS. The first command selects the six retained-input files plus `test_step_hashes_are_recorded_without_relaxing_geometry_or_scope`: 55 collected cases in the recorded selection. That extra test reads only the four retained `cad/container_generator_v1/*.step` releases and hard-coded R7 digests. The second command selects exactly two local-fixture checks. `test_frozen_p1_r7_remains_hash_clean_and_new_package_is_standalone` iterates all 20 P1 R7 lines in `2026-09-04-cad-foundation-v1/inputs/frozen-inputs.sha256`, including ignored `body.step`, `cap_c25.step`, and `closed_c25.step`; `test_four_written_steps_are_valid_and_baseline_equivalent` imports those same excluded R7 written STEP fixtures. The README therefore correctly calls them `LOCAL-FIXTURE-ONLY`. No test was rerun. |
| Evidence paths and capture | PASS for path resolution and the new capture. Every digest path in `VALIDATION_DELTA_EVIDENCE.sha256` and `CRITIQUE_EVIDENCE.sha256` resolves from the cleanup iteration directory. `LIVE_8448_HEADERS.txt` hashes to `80b16c1551cd22b833c1feacdbf297b0def545cb707758ec5ebfd8db6decd8b4`, records `HTTP/2 200`, and `LIVE_8448_INDEX.html` hashes to `53210be5e3b21a509c449261c69a271619f6ce0475a32a6eff90af70098b30bb`. |
| Authority | PASS. Worktree and index both hash the OpenSCAD authority to `ade77d3fcff4d5ba1c659838b4f9d24245584f0570834453b6e8c2b778047841` and the P1 R7 print layout to `80fd95845b51da5266883614f9bf8eff60793a24d5c39b7321c9c6cb16d477a4`. |

## Provenance limitation

The recovery was defined against predecessor candidate `515b249a19509e5509d4785a47e41896abc34d4d604494e708a0fe5afe33c624`, but its manifest bytes are not retained in this candidate, the repository, or its recorded recovery inputs. The present 1,012-entry manifest is therefore valid on its own. The requested claim that **only** documentation/evidence changed from the predecessor cannot be replayed from the predecessor digest alone; this validation instead confirms the current authority/source/test/artifact hashes match the last independent cleanup receipt and that the recovery's newly added candidate paths are documentation/evidence records.

The two cleanup evidence files correctly retain their named earlier candidate observations: `VALIDATION_DELTA.md` explicitly binds `515b…c624`, and `CRITIQUE_EVIDENCE.sha256` labels its first snapshot as historical. Their old `STAGED_FILES.sha256` digest lines necessarily do not match the current `ede603…761b` manifest and must not be read as current-candidate approvals. The superseding critique block also names its earlier candidate `afef13c1…b052`; it is an earlier observation, not a replay of the present candidate. The new live-capture lines replay successfully.

**Verdict: PASS.** The README's 55/2 split, evidence path resolution, current 8448 capture, manifest/index integrity, and authority hashes all pass. Retain a predecessor manifest or a deterministic predecessor-to-current path/hash delta in a later continuity improvement; it is not needed to reinterpret this completed recovery. The old evidence observations remain historical and do not approve the current candidate. This validation does not reopen CAD, runtime, service, Trash, or physical acceptance gates.

## Commands actually run

```sh
shasum -a 256 projects/laifen-wave-case/docs/iterations/2026-09-05-premerge-cleanup/STAGED_FILES.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-05-premerge-cleanup/STAGED_FILES.sha256
# compared every `git show :path` SHA-256 with each manifest line
git diff --cached --name-only
shasum -a 256 projects/laifen-wave-case/openscad/laifen_case_customizer_v1.scad projects/laifen-wave-case/cad/p1_r7_end_chamfer/print_layout.step
git show :projects/laifen-wave-case/openscad/laifen_case_customizer_v1.scad | shasum -a 256
git show :projects/laifen-wave-case/cad/p1_r7_end_chamfer/print_layout.step | shasum -a 256
```

No tests, CAD/OpenSCAD sources, export artifacts, runtime, service, Tailscale, Trash, index, staging, or quarantine data were changed by this validation.
