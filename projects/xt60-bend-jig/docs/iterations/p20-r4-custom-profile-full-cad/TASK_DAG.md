# P20 R4 full-CAD preview task DAG

Frozen input-manifest SHA-256:
`4286336b7709980f7d9ec4d22bb3f54f262639b88d3b3a7a1dba36b9e48b0691`.
Profile fingerprint:
`7a8013c935c74df865b3bd861ec163a00725e86f0e27415489babd26cd85eeb0`.

The root orchestrator owns scheduling and provenance. One source/artifact
writer at a time; no more than three workers concurrently. Initial attempt
plus at most two focused repair cycles. Any geometry change creates a new
candidate fingerprint and invalidates dependent critique/validation/review.

| ID | owner/role | objective and done gate | deps | exclusive writes / forbidden scope | effort and stop |
|---|---|---|---|---|---|
| `P20R4-DESIGN-01` | `/root/p20_final_design`, design | Freeze brief, math, delta mask, paths and gates | frozen inputs | only this iteration's `BRIEF.md`, `DESIGN.md`, `TASK_DAG.md`; no source/artifacts/indexes | strong/high, one bounded pass; complete |
| `P20R4-IMPL-01` | distinct implementation identity | Implement pure profile authority, focused tests, five STEP targets and sidecar; freeze candidate hash | DESIGN | exclusive R4 source/tests/CAD namespace; no docs outside implementation receipt, no self-approval, no simulator/coupon/P19-P20R3 edits | strong/high; stop on unreproducible profile, invalid solid, or source-scope escape |
| `P20R4-CRIT-01` | distinct mechanical critic | Challenge topology, support, trapping, cap/gap visibility and likely failure modes using exact candidate | IMPL | read-only candidate; write only `CRITIQUE.md`; no repair | strong/high; classify blockers vs known preview warnings |
| `P20R4-VALID-01` | distinct validator | Independently run math, occurrence, BREP collision, constraint, STEP parity and snapshot-readiness gates | IMPL | read-only candidate; write only `VALIDATION.md`; no repair | strong/high; fail closed on stale hash or hidden/omitted parts |
| `P20R4-REPAIR-01` | same implementation identity | Smallest source repair for accepted CRIT/VALID findings; regenerate and refreeze | CRIT + VALID when needed | same R4 implementation namespace only | strong/high; maximum two cycles, then reopen design |
| `P20R4-REVIEW-01` | fourth, distinct formal reviewer | Join current critique and validation; audit traceability, dispositions and exact candidate provenance | CRIT + VALID (+ REPAIR reruns) | write only `REVIEW.md`; no source repair | strong/high; may approve only user-preview delivery |
| `P20R4-PREVIEW-01` | root coordinator | Start Viewer for exact full-motion STEP, verify page + artifact ready, provide OPEN/MID/END/exploded snapshots and ask explicit user pass/fail | REVIEW pass | no geometry or manufacturing change | deterministic; stop after user intent gate |

## Candidate fingerprint rule

Before `P20R4-IMPL-01`, the orchestrator creates a sorted SHA-256 manifest over
the frozen contract files plus the declared authoritative inputs. After
implementation it adds R4 source, focused tests and generated STEP hashes to a
candidate manifest. Critic and validator must quote the identical candidate
manifest hash. Formal review rejects mixed or stale evidence.

## Stop conditions

- Do not substitute the coupon or P20 R3 zero-outer-rail STEP.
- Do not delete the left-Green or any other outer rod rail.
- Do not optimize cap height or plate gap without a new numeric contract.
- Do not proceed to mesh/slicer/print from this DAG.
- Known `1.152 mm` inner-rim and `1.715 mm` left-web warnings remain blockers
  for manufacturing acceptance, but they do not block the explicitly requested
  full-assembly intent preview.
