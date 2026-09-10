# Independent delivery critique

Owner: `/root/merge_inventory`, role `M4` (delivery critic). This role did not
implement the candidate and does not supply formal approval or CAD acceptance.

## Initial candidate and disposition

Initial manifest `CANDIDATE.sha256`, SHA-256
`899f5c4fc57b8ad08cdaae5cce38b8568857c55f9e6e4e51f90aad01452bd7da`,
verified 528/528 files before inspection. Frozen delivery contract is BRIEF
lines 1-24, SHA-256
`af14739aad568286ee5246a40c6f1690ccb4ea578edc7e4511ead0710803f57f`.

Initial disposition: focused continuity/provenance repair required; no source,
geometry, artifact regeneration, or acceptance promotion requested.

| ID | Severity | Finding | Required disposition |
|---|---|---|---|
| M4-01 | P2 | XT60 PROJECT_STATE omitted literal Baseline, Active iteration and Acceptance state headings required by main's structural test. | Restore heading contract while retaining one current P25 preview. |
| M4-02 | P2 | XT60 PROJECT_STATE delivery-record pointer resolved within the project although delivery records are root-owned. | Use `../../docs/iterations/2026-09-10-local-work-delivery/`. |
| M4-03 | P2 | PROVENANCE.tsv marks P25 HANDOFF as exact-import although its intentional delivery addendum changes the destination hash. | Classify this row as reconciled handoff; preserve source and destination hashes. |

The validator separately found historical manifest-bound Pill Click metadata
excluded by an ignore rule. Include only exact hash-matching provenance metadata,
scan it before delivery, and retain its migration-only status.

## Scope and preservation evidence

Read-only Node/SHA-256 checks establish:

- Every one of 109 branch-difference paths (`b69b6ad..a883404`) and all 437
  recovery-snapshot paths has an explicit row in the 546-row provenance table.
- Every declared original source hash and destination hash matches. The one
  initial discrepancy was M4-03's classification, not a content hash failure.
- Modern-main policy, workflow binding, structural tests, Kage and unrelated
  projects are unchanged. Tracked differences are restricted to README,
  XT60 continuity/requirements/experience/profile and uv.lock.
- Fifteen excluded intermediate PNGs remain exactly recoverable in the original
  snapshot. Final and annotated review media, authored HTML gates, and historical
  prepared coupon evidence are intentional preservation artifacts.
- Largest candidate file is a documented coupon STEP of 9,579,761 bytes. No
  candidate path is Git metadata, an environment, cache, log or private-key file.
- A bounded scan for private-key headers and common GitHub, OpenAI and AWS token
  formats reports no matching files; no secret values were printed. This is a
  spot check, not a universal secret-detection claim.
- The preserved `quadmula.zip` contains three historical STL files and small
  macOS resource-fork entries. Preserve its original bytes as archive provenance.

Commands: `git diff --name-only b69b6ad a883404`, `git show` for original branch
and protected main files, read-only Node filesystem/SHA-256/provenance comparisons,
explicit `/opt/homebrew/bin/rg` reads, `git status --short`, and
`unzip -l archives/drone/src/quadmula-f5-split/quadmula.zip`.
One initial Node Git-blob read hit its default output buffer; rerunning with a
32 MiB buffer completed. A `git diff --no-index` returned the expected status 1
for the intentional P25 HANDOFF addendum. No test suite or CAD command ran.

## Acceptance and ancestry boundaries

The reconciled authority correctly keeps P25 as first-CAD preview only; P19 is
the latest accepted digital mechanism baseline. P20 R4's historical manifest
drift and print-kit guard failures remain explicit. Pill Click is a
source-preserving migration with no selected accepted release; drone stays
inactive under archives. Existing STEP/3MF/G-code files do not grant current
fabrication or physical approval.

A later ancestry-only `ours` merge of `a883404` is appropriate only after the
reviewed content commit includes these explicit path dispositions. Root must
verify the merge tree is byte-identical to that reviewed content commit and
record the old branch as merged ancestry. This critique does not itself perform
or approve Git operations; independent formal review remains the join gate.

## Repair recheck

Pending exact repair candidate fingerprint. Implementation and validator retain
their separate roles; this evidence file is the critic's only repository write.

Repair 1 manifest `7394590745e1b606dff1c6900064439a84e58e128d162d0c8b22dcc4dca56b68`
verified 529/529. M4-01, M4-02 and M4-03 were corrected. Added Pill metadata
matches its historical migration-manifest hash and original bytes; JSON is valid
and bounded credential-pattern scan has no match. All 547 provenance source hashes
pass, but two PROJECT_STATE destination hashes remain stale after the heading/link
repair (M4-04, P2). Refresh these two recorded destination hashes and the enclosing
candidate manifest; no further source or acceptance change is requested.

## Final repair 2 disposition

**PASS for source/history-preserving delivery scope.** M4-01 through M4-04 are
resolved. This is delivery critique only; independent formal review still joins
this receipt with validator evidence.

Final `CANDIDATE.sha256` SHA-256:
`97357dfeadd1023c178f27e02b02429bf725053fda3f884ae7aa69714dda0210`.
All **529/529** entries verify at final recheck. The **547** provenance rows
account for 109 branch paths, 437 snapshot paths, and one original ignored file;
all destination hashes pass and exact-import classifications have matching hashes.
All source hashes were independently verified during repair recheck; repair 2
changed only two destination-hash records in PROVENANCE.tsv and the encompassing
manifest. Frozen BRIEF contract remains
`af14739aad568286ee5246a40c6f1690ccb4ea578edc7e4511ead0710803f57f`.

The added ignored `p1_review_job.json` is exactly the original and historical
migration-manifest SHA-256
`02b48475b4922f9f332b1a9a6a9fb0efe653529106fe34931e9adb0e221a1518`.
It is a JSON jobs descriptor, with no detected secret pattern, and preserving it
repairs provenance completeness without adding an accepted design or fabrication
claim. This exception is explicitly represented in PROVENANCE.tsv.

No remaining blocking delivery-critique finding. Retain all stated historical
CAD, artifact, fixture-drift, browser-review and physical boundaries. Root can
proceed to the distinct formal-review join and reviewed PR delivery; no downstream
printer or product acceptance follows from this PASS.
