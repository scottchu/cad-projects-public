# PR 19 merge readiness — independent receipt
Owner: `/root/merge_readiness`; date: 2026-09-06. Read-only review of source,
tests, references and prior receipts; exclusive write is this record.

Verdict: **APPROVE the frozen candidate for merge.** Final prescribed checks
passed as root-relayed below. No correctness or scope blocker found.
The user's current explicit merge request supersedes historical
draft-only/no-main-merge delivery boundaries; it does not approve new features.

Candidate: `90d73c13355385cc51bc2a17c2b3b2ac0d21cbe1` against fetched main
`6e00ba898d6435614782de2764c6aae0ff131de5`. A subsequent commit may add only this
review and root-owned merge/status coordination; changed decision-bearing
source, tests, contracts or reference artifacts require affected review again.

## Current fingerprint verification

- Performance source manifest `3888018275bfcd05ab1d66a27d5b29a01eaf7268382075f4e2bd2047cc638c4c`: **43/43** current paths match.
- Study candidate `8d71809de30441b9f0c0c62fb5191524f06f125c0d010ff71b33d0b6f9ff5779`: **38/38** current paths match.
- Reference review inputs `52e6cbb4d1009b39946d746a1baf701557bd449b2134596618ac840cdb87a09b`: **6/6** current paths match.
- Archive `7cdda37eb2ca54c0a2461214b24482b42089df68534c95886c9fd4320c8bcbd5`: **36/36** entries match, including all 33 original images.
- SCAD remains `497098afa555092a0ed85a3a7213cd270852aa76f9001e1478c209cd8469bc42`; proposal remains `d4e5f6a9ad0b315b4dbb57187ffa2eee9864fd1c646a01bbdacfd0b17f88f16f`.
- Formal performance review `994847a86d578b29c6949b9de2258f7ed93542f5b670e84d07f6713a7a93afe4`, study review `ce6d08d05591e66b863829f4f1a83f945b85f9e8b7a0afcc8c76cb5e9d29e0ab`, and reference review `4432435b50a28a8b10fd0b31841e244f25f875d2ead78cc73c0a112a63c88b80` match their receipts.

## Evidence, findings and retained limits

Commands: `shasum -a 256 -c` on performance `inputs/candidate-source.sha256`,
study `inputs/candidate.sha256`, reference `inputs/review-inputs.sha256` from
repository root, and archive `SHA256SUMS` from its directory; `shasum -a 256`
on the named manifests and receipts; `git diff --stat`, `--name-only`, and
`--check` over the exact base/head range above. All 228 PR paths are project-local.

Prior distinct implementation, validation, critique and formal-review identities
remain traceable. Performance and study DELIVERY records close their historical
private delivery conditions. This review does not reassert fresh live parity.
Exact-output performance evidence preserves prior bounded geometry certificates;
the analytic study and 10-family reference proposal remain unaccepted proposals.

Low/nonblocking: diff-check reports three preserved Markdown hard-break spaces
in pattern-families FULL_CRITIQUE lines 3/4 and REVIEW line 3. Frozen historical
receipts were preserved. Existing phase-independent sampler/source-hash runner
limitations remain documented; no new benchmark claim follows from this merge.
Native Safari/iPhone, slicer, fit, strength and physical acceptance remain open.

Root-relayed final checks: `node --test projects/laifen-wave-case/tests/node/*.test.mjs`: **66/66**; `PYTHONDONTWRITEBYTECODE=1 uv run pytest projects/laifen-wave-case/tests/test_openscad_customizer.py projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -p no:cacheprovider`: **13 passed**, 0.14s.
`npm run build:openscad-simulator --workspace laifen-wave-case -- --outDir /tmp/container-pr19-merge-check/dist --emptyOutDir`: **exit 0**, 20 modules, 594ms; existing >500kB chunk advisory only. Next: verify only permitted status/review changes, then merge PR 19 as authorized.
