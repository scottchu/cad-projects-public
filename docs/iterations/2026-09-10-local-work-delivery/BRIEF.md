# Local work delivery

## Frozen delivery contract

User request: merge the existing branch and local work into main. This is source,
history and migration delivery, not a new CAD design or fabrication release.

- Baseline main: `cf8ec46`; source checkout HEAD: `a883404`.
- Source checkout: `/Users/scottchu/Projects/personal/design-projects`.
- Isolated candidate: `/Users/scottchu/Projects/personal/design-projects-delivery-20260910`,
  branch `codex/reconcile-local-work-20260910`.
- Recovery snapshot: `/Users/scottchu/.codex/backups/design-main-20260910T101124`.
  Its `manifest.json` SHA-256 is
  `37c87c541c9bcc8793ea1bc1387c8b1d977ec39d090af962acc98c9cb603cbc1`;
  it preserves 437 changed/untracked files, 96,429,236 bytes, plus tracked patch.
- DEL-1: preserve original checkout and snapshot bytes; deliver intentional source,
  project history and migration assets with exact provenance.
- DEL-2: retain main's workflow separation, other projects and accepted baselines.
- DEL-3: distinguish preserved experiments from CAD/artifact/physical acceptance.
- DEL-4: reconcile current pointers, verify focused local checks, obtain independent
  validation/critique/formal review, then deliver through a PR and merge.
- Exclude caches, logs, redundant screenshots and scratch from trunk; retain them
  in recovery. No new geometry, regeneration, slicing, printing or publishing.

## Mutable delegated execution plan and status

| ID | Owner / role | Dependencies | Inputs | Exclusive writes | Done gate |
|---|---|---|---|---|---|
| M1 | `/root/merge_inventory`, inventory, complete | none | source HEAD, snapshot, main and frozen read manifest | `/tmp/design-main-inventory-20260910` | classified scope and existing evidence |
| M2 | `/root/delivery_implementation`, implementation, repair 2 frozen | M1 | M1 manifest/report, frozen delivery contract, snapshot and main | candidate project/source and implementation records | reconciled source-preserving candidate and manifest |
| M3 | `/root/delivery_validation`, independent validator, PASS with recorded baseline failures | M2 frozen source subset, then final manifest | exact candidate manifest | validation evidence only | prescribed checks and parity verified |
| M4 | `/root/merge_inventory`, distinct critic, PASS | M2 | exact candidate manifest | critique evidence only | scope, exclusions and acceptance assessed |
| M5 | `/root/delivery_formal_review`, distinct formal reviewer, PASS | M3, M4 | candidate manifest and receipts | formal review only | findings resolved, provenance join PASS |
| M6 | `/root`, delivery coordination | M5 | reviewed candidate | Git delivery and concise handoff indexes | PR merged and remote main verified |

Every worker reads project continuity before material changes, returns exact
commands/results and hashes, and verifies its input fingerprint before returning.
Decision-bearing inputs use sorted SHA-256 path/content manifests; mutable
orchestration/status and evidence records are excluded. One candidate writer;
reviewers are read-only apart from exclusive evidence paths. Original checkout,
other worktrees, services, equipment and external repositories are forbidden writes.
At most three active workers. Each role has a ten-minute checkpoint, concise
receipt ceiling of 2,000 words, and an initial attempt plus at most two focused
repair cycles. Stop on input drift, lost preservation, unresolved authority, or
new design decisions. Model/effort and exact manifests are assigned at dispatch.

M1 froze `/tmp/design-main-inventory-20260910/inputs.sha256`, SHA-256
`c7162df2da0885d4dee64f70cd1b2e12d8c4062522f8e53a2c7c7291a15b15aa`,
and verified all 1,825 inputs at return. Its read-only inventory separates the
106 changed XT60 paths, 158 Pill Click paths and 106 Drone archive paths from
newer main-owned policy and Kage records. The P25/P24/P20R3/scaffold candidate
manifests reproduce; P20R4 historical parent/child manifests do not describe all
current derivative bytes. M2 must preserve those distinctions without rewriting
historical manifests. Fifteen redundant intermediate PNGs remain in recovery.
M1 used the inherited strong model/effort; M2 uses gpt-5.6-sol/medium. Root
independently rechecked the 437 original snapshot paths and source HEAD after
dispatch: unchanged. Bound Workbench policy-manifest and governing CAD/continuity
policy hashes were verified directly against revision
`1d7f4fcd65e04136bb6bad24e90015ca36d97f2f`.

M2 froze `M2-SOURCE-ARTIFACT-FREEZE.sha256` (702 entries), SHA-256
`a8b81f3a2aa78fba66edd70a664a4a700512ddcba157032f22f291e562884bd1`.
M3 runs prescribed tests against that immutable source/test/artifact/lock subset
while M2 finishes only continuity and delivery records. M3 uses gpt-5.6-sol/high,
owns `VALIDATION.md`, and must verify the final full candidate before returning.

Repair 1 freezes `CANDIDATE.sha256` (529 entries), SHA-256
`7394590745e1b606dff1c6900064439a84e58e128d162d0c8b22dcc4dca56b68`,
and the revised source subset (703 entries), SHA-256
`4afc5f670dacd9625ed4f939e17ad4e16d196f007fef67790df8103093a0583d`.
Changes are limited to XT60 required continuity headings/root link, correct P25
handoff provenance disposition, and the Pill Click ignored review-job metadata
required by its historical migration manifest. That supplementary source file
matches historical SHA-256
`02b48475b4922f9f332b1a9a6a9fb0efe653529106fe34931e9adb0e221a1518`;
it is explicitly force-staged. Other source/tests/artifacts remain unchanged.
M4 reuses the independent inventory identity as critic, never implementer or
formal reviewer. All 109 original branch paths and 437 snapshot paths are
accounted for in the provenance ledger. Exact final validation and critique
receipts are authoritative for gate outcomes.

Repair 2 supersedes the repair 1 full candidate with SHA-256
`97357dfeadd1023c178f27e02b02429bf725053fda3f884ae7aa69714dda0210`
(529 entries). It corrects two provenance destination hashes left stale by the
heading/link repair. `PROVENANCE.tsv` SHA-256 is
`ae4e416eb3b2fbcd692e439b24c724f15bab7c089b4685eb3e31fb677569f6cd`.
The 703-entry source subset remains unchanged. This is the second and final
focused implementation repair; only affected provenance checks are repeated.

M3 and M4 passed the final frozen candidate for bounded preservation/integration.
M3 receipt SHA-256: `e7de67896f4028f1f68ee8037cf6558195b42c57f7f34aec2d09313ab7c4fdf3`.
M4 receipt SHA-256: `66d0760d1a31d474385e81333e569feca459733beb55cd4a2a8afb4e2606907d`.
Both retain known P20 print-guard failures and the unrelated root-structure
failure already present in main's Laifen records. M5 uses gpt-5.6-sol/high,
five-minute checkpoint and the standard two-followup ceiling; its only write
is `REVIEW.md`. No new CAD acceptance is requested or inferred.

M5 formal-review PASS receipt SHA-256:
`a6acc1c7b7300ef36cfc5018cab0b0f3697992cd10e8634c7509d2eebbfb674c`.
It independently joins the final candidate/source manifests, 547 provenance rows,
staged scope, resolved findings and known failures. M6 is authorized to commit,
record `a883404` ancestry with unchanged content tree, and merge through a PR.

M6 committed content as `e0be5a82f4c725f718bf2f96afb9fbde332f22e1`,
then ancestry merge `e293bd9f76926f9de4a08f50569bf94add493067`.
Their trees match exactly (`c14843e28a1ce41cb2d40a56045c5d7a71836fb5`),
and the original source HEAD is an ancestor. The final Git outcome is recorded
by [PR #24](https://github.com/scottchu/design-projects/pull/24); `HANDOFF.md`
contains the candidate-delivery and recovery pointers.
