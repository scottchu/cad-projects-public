# Pre-merge cleanup design

## Contract

LC-DES-02 prepares the existing Laifen worktree for review and merge without changing CAD, OpenSCAD geometry, simulator behavior, Tailscale routes, or physical-acceptance claims. Baseline is `d0aab1ff`; the frozen input fingerprint is `be46c16f8c3b43ea265600de2f50e31a56aa01a45f7a0ccd999358bea1d7fddd`.

Cleanup is reversible. The implementer creates one uniquely named dated directory in macOS Trash, moves only paths named in `QUARANTINE_MANIFEST.txt`, records original-to-quarantine mappings plus file count, byte count and SHA-256 evidence, and never empties Trash. A missing path is recorded and skipped; it must not be replaced by a broader glob.

## Three path classes

`KEEP_MANIFEST.txt` separates:

1. **Filesystem keep + Git include:** project source, documentation, tests, OpenSCAD customizer and simulator source, workspace locks, the immutable P1 R7 STEP authority, and `container_generator_v1` release artifacts required by the active parity/preview chain.
2. **Filesystem keep + Git exclude:** live `scratch/presentation`, current VFR-12 C3 implementation/evidence, and historical generated STEP fixtures used by local regression tests. Those fixtures do not make a fresh clone pass; any consuming test is reported as `LOCAL-FIXTURE-ONLY`.
3. **Reversible quarantine + Git exclude:** only exact duplicate generated trees, superseded VFR-11/VFR-12 C2 evidence, and ignored caches named exactly in `QUARANTINE_MANIFEST.txt`.

The cleanup must not move `scratch/presentation`, `scratch/vfr12-mobile-c3-validation`, `scratch/vfr12-mobile-delivery-c3`, or `scratch/vfr12-mobile-implementation`. It must not reset Tailscale, restart services, change the HTTP server directory, regenerate CAD, or change current OpenSCAD/P1 R7 fingerprints.

## Git boundary

Stage only the Git-include class. Historical P1 R2-R6 `.step` files and the P1 R3 duplicate `generated/` tree stay outside Git. P1 R2-R6 source stays included. Ignored caches, OpenSCAD WASM vendor/dist bundles, `node_modules`, and scratch remain outside Git. `package-lock.json` and `uv.lock` stay included because they carry Laifen workspace dependencies.

The staging audit records exact staged bytes and ten largest files, proves no ignored file is staged, and rejects any staged blob at or above 100 MiB. It also proves:

- P1 R7 `print_layout.step`: `80fd95845b51da5266883614f9bf8eff60793a24d5c39b7321c9c6cb16d477a4`.
- OpenSCAD source: `ade77d3fcff4d5ba1c659838b4f9d24245584f0570834453b6e8c2b778047841`.

## Gates

1. **Recovery:** quarantine directory and recovery manifest record original and quarantined paths, type, counts, bytes, hashes, and restore command; one safe spot-check passes; no permanent deletion occurs.
2. **Service:** before and after, `https://mac-mini.duckbill-ionian.ts.net:8448/openscad-simulator/` serves current VFR-12 C3 from `scratch/presentation`; unrelated Tailscale routes are unchanged.
3. **Authority:** both hashes above match; retained container-generator release files exist and hash-match `INPUT_MANIFEST.sha256`.
4. **Tests:** run focused OpenSCAD/customizer and simulator tests plus CAD/source tests whose inputs are retained. Tests requiring excluded historical STEP fixtures are explicitly `LOCAL-FIXTURE-ONLY`, never fresh-clone evidence.
5. **Size/staging:** the Git boundary and blob limit pass.
6. **Independent review:** a validator checks recovery, authority, service, tests and staging; a distinct formal reviewer approves the same candidate fingerprint.
7. **PR:** update `PROJECT_STATE.md`, active `HANDOFF.md`, and `NEXT_AGENT.md` with exact fingerprints, recovery path, receipts, links and remaining physical gaps, then push the non-main branch, open a concise PR and merge after review passes.

Stop if an authority hash changes, the live route breaks, quarantine is not recoverable, a new path needs removal, a staged blob reaches 100 MiB, or current VFR-12 evidence is threatened. Limit repair to two focused cycles; broader cleanup requires a new frozen contract.
