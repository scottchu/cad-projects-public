# LC-DOC-CRIT-01 — independent documentation/evidence recovery critique — HOLD

Reviewer: `/root/laifen_premerge_docs_recovery_critic`, independent of the recovery designer, implementer, validator and formal reviewer. Date: 2026-09-05. Supplied staged-candidate fingerprint: `ede603baef8ac0302a3ad044f4c32a8495b565dfd74e21293bcb660a1653761b`.

## Read-only checks

- The stated active OpenSCAD source remains `ade77d3fcff4d5ba1c659838b4f9d24245584f0570834453b6e8c2b778047841` and the R7 print-layout STEP remains `80fd95845b51da5266883614f9bf8eff60793a24d5c39b7321c9c6cb16d477a4`.
- The declared Trash recovery directory exists. A read-only request to the exact current 8448 simulator URL returned HTTP 200. No service, Tailscale, runtime, source, test, CAD, export, index or Trash path was changed by this review.
- All paths in `VALIDATION_DELTA_EVIDENCE.sha256` and `CRITIQUE_EVIDENCE.sha256` resolve relative to their manifest directory. The new 8448 header and index captures exist and hash correctly. The route capture records HTTP/2 200.

## Blocking findings

### D1 — the 55/2 classification contradicts the test source

**High.** `test_frozen_p1_r7_remains_hash_clean_and_new_package_is_standalone` does not read the excluded R7 `body.step`, `cap_c25.step` or `closed_c25.step` fixtures. It hashes the twenty retained P1 R7 files named by `docs/iterations/2026-09-04-cad-foundation-v1/inputs/frozen-inputs.sha256` and checks tracked standalone package text. It is therefore not `LOCAL-FIXTURE-ONLY` on the stated Git boundary.

The only selected test that imports the excluded R7 written STEP views is `test_four_written_steps_are_valid_and_baseline_equivalent`. Static collection from the selected files gives 55 tests for the README's first command (including 21 `test_invalid_inputs_stop_at_pure_derivation` parameter cases); adding the source-equivalence test gives 56 fresh-clone-relevant tests, and adding the written-STEP equivalence test gives one local-fixture-only test, 57 total.

Correct the brief/design/implementation/handoff and README to a **56/1** split, or provide an evidence-backed reason that the frozen P1 R7 source files are excluded. Do not label a source-only check as depending on absent STEP fixtures.

### D2 — evidence manifests cannot be replayed as current candidate evidence

**High.** The current `STAGED_FILES.sha256` hashes to the supplied `ede603ba…761b`, contains 1,012 entries, while the staged index has 1,019 entries. The seven entries outside the manifest are mutable cleanup receipts, including the recovery's new `VALIDATION_DELTA*` files. Both evidence manifests still bind predecessor candidate hashes (`515b249a…c624` and `afef13c1…b052`), neither of which matches the present staged manifest.

`shasum -a 256 -c` therefore fails for the unlabelled current block in `VALIDATION_DELTA_EVIDENCE.sha256` and for stale snapshot lines in `CRITIQUE_EVIDENCE.sha256`. The latter has a historical-snapshot comment for its first block, but its superseding recheck block has no equivalent historical label. Historical observations may remain, but must not look like replayable current bindings.

After correcting D1, regenerate one complete staged manifest and create an unambiguous current evidence block that covers every staged path or explicitly names the deliberately mutable receipt policy. Preserve old evidence as clearly labelled historical snapshots. Then run independent validation and formal review against that new fingerprint.

### D3 — no replayable proof of the asserted no-source/test/artifact delta

**Medium, merge-blocking until D2 is repaired.** The 515b predecessor is named only by content digest; its manifest bytes are not retained in the candidate or available as a Git object. This review can verify the current authority hashes and observe that the recovery itself stages only documentation/evidence files, but it cannot prove the requested no-source/test/artifact change relative to 515b from a digest alone. The re-frozen manifest must carry a predecessor comparison or immutable allowlist/delta that makes that claim independently replayable.

## Verdict

**HOLD.** Runtime and named authority survived, and the live capture is accurate. The documentation recovery misclassifies one test and has not re-frozen the changed candidate. Fix D1 and D2, include the D3 delta proof in the new candidate, then send it to a distinct validator and formal reviewer.

## LC-DOC-CRIT-02 method correction — PASS for the supplied recovery scope

The initial D1 finding is withdrawn. Re-opening the exact frozen input manifest
shows that its twenty P1 R7 paths include the excluded `body.step`,
`cap_c25.step`, and `closed_c25.step`. The source-equivalence test reads every
one of those paths, so it is correctly `LOCAL-FIXTURE-ONLY`. The README's
first command selects 55 tests; its two separately named checks are the two
local-fixture-only tests. The 55/2 wording is accurate.

D2 is also withdrawn as a merge blocker. The seven index paths absent from the
1,012-entry immutable manifest are exactly the declared mutable cleanup
receipts: `STAGED_FILES.sha256`, `CRITIQUE.md`, `CRITIQUE_EVIDENCE.sha256`,
`VALIDATION.md`, `VALIDATION_DELTA.md`, `VALIDATION_DELTA_EVIDENCE.sha256`, and
`VALIDATION_EVIDENCE.sha256`. There are no undeclared index-only paths and no
manifest-only paths. `VALIDATION_DELTA_EVIDENCE.sha256` names the predecessor
`515b…` manifest as the specific candidate validated by `VALIDATION_DELTA.md`,
not the current immutable candidate; `CRITIQUE_EVIDENCE.sha256` likewise
records labelled historical LC-CRIT snapshots. These are historical receipt
hashes rather than current replay bindings. No genuinely stale, unlabelled
current-evidence line was found.

D3 remains a documented limit, not a hold: the exact prior 515b manifest bytes
are unavailable for a raw path-by-path diff. LC-VAL-04 records that its final
manifest repair changed only membership and mutable receipts, and the current
OpenSCAD and printable STEP hashes directly match its authority evidence. This
review does not independently extend that historical no-delta assertion beyond
those current hashes.

**Superseding verdict: PASS for the narrow documentation/evidence recovery.**
The 8448 capture is accurate, corrected path resolution works, current authority
and runtime are preserved, and README test classification is now truthful. This
PASS applies only to the supplied immutable candidate and declared mutable
receipt policy. The coordinator must include this critique as a new mutable
receipt or re-freeze as required by the delivery workflow; it does not approve
CAD, slicing, printing, or physical acceptance.
