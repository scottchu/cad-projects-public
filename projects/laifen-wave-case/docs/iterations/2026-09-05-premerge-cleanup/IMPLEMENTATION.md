# LC-IMP-01 implementation receipt

## Bound contract

- Baseline: `d0aab1ff`.
- Designer-reported contract bundle: `a70b728a2b70745cde58df995f12b43f38922d59379ca3f740e11ac51fbb8769`.
- Direct frozen files: `DESIGN.md` `ece9e37ba3b10aa787f4e4a40691d6ce68ad28facd23b0ee1d01d0c240dc8ee8`; `KEEP_MANIFEST.txt` `a97021b58d7dcbec26d7e0df185c9b1953efd89a9e1804faeaf8c326894ff7b1`; `QUARANTINE_MANIFEST.txt` `261b58e42931999958f5df7e2b4ed5fcb322b7231bb44e4ba97afb007ab35808`; `INPUT_MANIFEST.sha256` `be46c16f8c3b43ea265600de2f50e31a56aa01a45f7a0ccd999358bea1d7fddd`.
- Deterministic local bundle (`sha256(CONTRACT_FILES.sha256)`): `b2ae46496cb8fcbf6abef69c8a3d5fb47ccac436c618a07e605e7887c70fe7ae`.

## Result

All 27 exact listed paths existed and were moved to the unique quarantine `/Users/scottchu/.Trash/laifen-wave-case-premerge-cleanup-2026-09-05.46d83abc57`. The move covered 617 regular-file or symlink entries, 210 directories, and 1,303,210,296 bytes. No missing path, unlisted path, CAD source, OpenSCAD source, simulator source, current VFR-12 C3 evidence, or live presentation path was moved.

The project-local `.gitignore` now excludes only the named historical P1 R2-R6 STEP fixture namespaces plus runtime/cache namespaces. It does not exclude P1 R7 or `container_generator_v1` STEP releases.

## Recovery evidence

- `PREMOVE.sha256` and `POSTMOVE.sha256` compare byte-for-byte equal.
- `MOVE_MANIFEST.tsv` records all 27 roots, counts, bytes, tree fingerprints, and destinations.
- `projects/laifen-wave-case/openscad/__pycache__` was safely restored, verified, and moved back. Its tree SHA-256 stayed `61303169cd453a6e1b74737847aed5d5811ea94e387ed5bcf8ee488147228933` in all three states.
- All 27 originals are absent and all 27 quarantine roots exist in the final state.
- Trash was not emptied and nothing was permanently deleted.

## Authority and service evidence

Before and after cleanup:

- OpenSCAD source: `ade77d3fcff4d5ba1c659838b4f9d24245584f0570834453b6e8c2b778047841`.
- P1 R7 `print_layout.step`: `80fd95845b51da5266883614f9bf8eff60793a24d5c39b7321c9c6cb16d477a4`.
- Private simulator: `HTTP/2 200`, response SHA-256 `53210be5e3b21a509c449261c69a271619f6ce0475a32a6eff90af70098b30bb`.
- Runtime: PID 2629, `.venv/bin/python3 -m http.server 8972`, serving `/Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case/scratch/presentation`.
- Preserved current runtime/evidence directories: `scratch/presentation`, `scratch/vfr12-mobile-c3-validation`, `scratch/vfr12-mobile-delivery-c3`, and `scratch/vfr12-mobile-implementation`.

`AUTHORITY_BEFORE.sha256`, `AUTHORITY_AFTER.sha256`, and `SERVICE_CHECK.tsv` contain the raw compact receipts.

## Commands

- Created direct contract file hashes with `shasum -a 256` and hashed the resulting ordered list.
- Captured the live route with `curl -fsS -D ... https://mac-mini.duckbill-ionian.ts.net:8448/openscad-simulator/` before and after.
- Enumerated, SHA-256 hashed, moved, and post-verified the exact manifest roots with `/tmp/laifen_lc_imp01.py`.
- Compared pre/post inventories with `cmp -s` and verified every original/destination pair in Python.
- Created the project-local Git boundary in `.gitignore`.

## Limits

This receipt proves reversible filesystem cleanup and preservation of the current authority/service chain. It does not stage, commit, push, merge, regenerate CAD, validate written CAD solids, or claim new physical acceptance. Independent staging, focused tests, validation, and formal review remain downstream gates.

## Repair cycle 1 — stable math-probe dependency

The independent validator found two merge-boundary defects in the initial receipt. The recovery example invoked bare `python3`, and `test_real_pinned_openscad_executes_vfr04_math_witnesses` invoked a script under ignored `scratch/`.

The recovery example now uses `uv run python -` from the repository root. `openscad/run_math_probe.mjs` is a tracked copy of the prior scratch probe. Its executable logic and assertions are byte-for-byte equivalent except for the three import/resource URLs required by its new location: the two WASM vendor paths changed from `../../preview/...` to `../preview/...`, and the SCAD path changed from `../../openscad/laifen_case_customizer_v1.scad` to `./laifen_case_customizer_v1.scad`. The test now points to this stable helper; its assertions and subprocess contract are unchanged.

Repair fingerprints:

- prior scratch probe: `a86d4f2961e503d24fe7ebb5ec4b76ce07ab4b9fb32929785a90d04c1819871f`;
- tracked stable probe: `59c555065196d443f1c110eb1ff2f356be831bc862ae79ad58e3c315f04de58f`;
- updated focused test: `903859b70da4f86308170f846ddecbad688b53bd0a3eba211d988dfc8f98659f`;
- updated recovery note: `64413eccdce545ceb1984b25b142c4c796ca5b63c947d0e562276807c5acec69`.

The focused runtime test was not run in this implementation role because `preview/openscad-wasm-simulator/vendor` is deliberately quarantined by LC-DES-02. Restoring it would violate this repair scope. Its declared setup dependency is `npm --workspace laifen-wave-case run setup:openscad-wasm`; the independent validator may recreate the pinned vendor cache before running only `uv run pytest projects/laifen-wave-case/tests/test_openscad_customizer.py::test_real_pinned_openscad_executes_vfr04_math_witnesses -q`. No setup or test command was claimed as run here.

## LC-IMP-02 repair cycle 2 — continuity and Git payload boundary

This final repair addresses LC-CRIT-01 C1-C3 and the formal current-pointer
finding. It does not stage files or mutate CAD, OpenSCAD, tests, runtime, Trash
or services.

- Added exact ignores for P1 R7 `body.step`, `cap_c25.step` and
  `closed_c25.step`. These redundant releases remain local and reproducible;
  R7 `print_layout.step` remains the Git authority and all four
  `container_generator_v1` releases remain trackable.
- Removed current/ready claims for stale 8449 CAD Viewer links from current
  documentation. The 8448 OpenSCAD simulator is the only live current surface;
  older viewer and P2 R3 material remains historical evidence.
- Aligned `CURRENT` and `CURRENT.md` to
  `2026-09-04-openscad-visual-fidelity-recovery`.
- Rewrote the README around the implemented OpenSCAD source/browser workflow,
  root reproducible setup/build commands and the 57-test validator selection.
- Updated the decision index and continuity records, and added a cleanup
  handoff with recovery, provenance, artifact policy and remaining gaps.

Frozen predecessor hashes are LC-DES-02
`ece9e37ba3b10aa787f4e4a40691d6ce68ad28facd23b0ee1d01d0c240dc8ee8`,
LC-IMP-01 `fb390af434987010e0644a57a75196e8f018197cd0b1a02fab8e6b3c5216fe0e`,
LC-VAL-02 `b3acb4889c877fe18526ee80d5ecfecbafd460b7bf87111fe5eade748d77817c`,
and LC-CRIT-01
`9363b472e33e8308c01a78d508476340f768fdc643d54197d6db0724eac79caf`.
LC-CRIT-01 remains HOLD in its immutable receipt; its three blockers are
repaired here pending re-freeze and independent recheck. No formal PASS is
claimed.
