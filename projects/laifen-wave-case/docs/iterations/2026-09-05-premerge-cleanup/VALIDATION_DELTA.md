# LC-VAL-04 final delta validation — PASS

Owner: `/root/laifen_premerge_cleanup_validate_delta`, independent of cleanup implementation and critique. Date: 2026-09-05. Baseline: `d0aab1ff`.

## Frozen candidate

The immutable merge-candidate manifest is
`STAGED_FILES.sha256` SHA-256
`515b249a19509e5509d4785a47e41896abc34d4d604494e708a0fe5afe33c624`.
It lists 1,005 immutable paths, totalling 355,808,250 bytes. The manifest is
162,707 bytes, so the frozen content plus manifest totals 355,970,957 bytes.

All 1,005 listed hashes matched both the working tree and Git index. The staged
index contains 1,010 paths: the 1,005 frozen paths plus exactly five deliberate
mutable evidence paths:

- `STAGED_FILES.sha256` itself;
- `CRITIQUE.md` and `CRITIQUE_EVIDENCE.sha256` (LC-CRIT-02 PASS);
- `VALIDATION.md` and `VALIDATION_EVIDENCE.sha256` (LC-VAL-02 PASS).

No immutable path is missing, no other staged path is outside the manifest, no
staged path is ignored, and no staged blob is 100 MiB or larger.

## Independent results

| Gate | Result |
| --- | --- |
| Git release policy | PASS. P1 R7 `print_layout.step` and all four `container_generator_v1` STEP releases are staged. Local redundant P1 R7 `body.step`, `cap_c25.step`, and `closed_c25.step` exist but are excluded. |
| Authority | PASS. OpenSCAD source is `ade77d3fcff4d5ba1c659838b4f9d24245584f0570834453b6e8c2b778047841`; P1 R7 print layout is `80fd95845b51da5266883614f9bf8eff60793a24d5c39b7321c9c6cb16d477a4`. Working tree and index agree. |
| Current continuity | PASS. Both `CURRENT` files select `2026-09-04-openscad-visual-fidelity-recovery`; current README/state/next/handoff URLs name only the 8448 OpenSCAD simulator as live and contain no active 8449/3249 URL. |
| Live service | PASS. `https://mac-mini.duckbill-ionian.ts.net:8448/openscad-simulator/` returned HTTP 200; response SHA-256 is `53210be5e3b21a509c449261c69a271619f6ce0475a32a6eff90af70098b30bb`. PID 2629 uses this worktree's root `.venv/bin/python3`, serves port 8972, and points at `scratch/presentation`. |
| Locks | PASS. `uv lock --check` resolved 72 packages; `npm ls --workspace=laifen-wave-case --depth=0` reported Three 0.176.0 and Vite 6.4.3. |
| Prior focused evidence | Still applicable. This final manifest repair changes only manifest membership and mutable cleanup receipts; it does not alter the retained source, tests, written STEP authority, or served runtime bytes covered by LC-VAL-02's 57 passing focused tests. |

## Commands actually run

```sh
# Rehashed every listed path against both working-tree and index bytes.
/usr/bin/shasum -a 256 ...
/usr/bin/git show :path | /usr/bin/shasum -a 256
/usr/bin/git cat-file -s :path

/usr/bin/git diff --cached --name-only | /usr/bin/git check-ignore --no-index --stdin
/usr/bin/curl -fsS https://mac-mini.duckbill-ionian.ts.net:8448/openscad-simulator/
uv lock --check
npm ls --workspace=laifen-wave-case --depth=0
```

No source, index, service, Trash or CAD artifact was mutated by this validation.
This is a merge-boundary validation only; it does not extend CAD, printed fit,
slicing, drainage, strength, or physical acceptance claims.
