# P20 R4 blocked test-print 3MF task DAG

Date: `2026-08-27`

Contract owner: `/root/p20_3mf_design`

Parent candidate fingerprint:
`e90f0f63687118ce9826801335263ea861d546016011c8bb98f31032963f61db`.

All tasks are limited to evidence-only model/mesh preparation. Slicing,
upload, printer control, print start, geometry redesign, and manufacturing
acceptance are forbidden.

| ID | owner/role | objective and done gate | depends on | allowed exclusive writes | forbidden scope | ceiling / stop |
|---|---|---|---|---|---|---|
| `P20R4-3MF-DESIGN-01` | `/root/p20_3mf_design`, contract owner | Freeze exact 13-object census, unchanged-geometry delta mask, layout, export validation, warnings, and DAG | parent P20 R4 manifest, review, validation, P19 layout precedent, P13 lib3mf precedent | this iteration `BRIEF.md`, `TASK_DAG.md` | source/CAD/mesh/test edits; self-approval | balanced/high, one pass; stop if parent fingerprint or source hash differs |
| `P20R4-3MF-IMPL-01` | distinct implementer | Add unchanged-source print-kit composition, STEP generator, model-only lib3mf exporter, tests, provenance, and write STEP/3MF; done when all deterministic implementation checks pass and a candidate manifest pins every output | DESIGN | `p20_r4_custom_profile_full_cad.py` print-kit-only additions; `p20_r4_print_kit.step.py/.step/.3mf`; exporter script; focused test; provenance; implementation receipt/candidate manifest; raw snapshots in new review directory | any geometry parameter or base builder change; parent CAD artifacts; slicer/G-code/upload/start; approval | balanced/medium; initial plus at most two focused repairs; stop on any changed frozen-solid volume or unresolved overlap/manifold failure |
| `P20R4-3MF-CRITIQUE-01` | distinct independent critic | Inspect exact implementation fingerprint, object inclusion/exclusion, labels, bed layout, warnings, STEP/3MF snapshots, and likely user confusion; return prioritized findings | IMPL | `CRITIQUE.md` only | source/artifact/test repair; approval | strong/high, one pass; stop and flag any geometry change or hidden blocker |
| `P20R4-3MF-VALIDATE-01` | distinct independent validator | Recompute 13-object source/STEP/3MF census and names, volume parity, bed separation/contact, STEP parity, lib3mf round trip, metadata/provenance/hashes, and visually inspect both snapshots | IMPL | `VALIDATION.md` only | source/artifact repair; slicer/printer action; acceptance by assertion | strong/high, one pass plus one focused rerun after immutable repair; fail on mismatch, invalid mesh, overlap, or missing warning |
| `P20R4-3MF-REVIEW-01` | distinct formal reviewer | Decide whether the exact model-only 3MF may be handed to the user strictly as a blocked test artifact; confirm warning wording and no downstream action | CRITIQUE, VALIDATE | `REVIEW.md` only | design/implementation/validation work; manufacturing or print approval | strong/high, one pass; fail if provenance chain is mixed or 3MF is described as print-ready |
| `P20R4-3MF-HANDOFF-01` | root orchestrator | Verify receipts/fingerprint, update project continuity files, provide exact 3MF and review links, state blockers and `not sliced/uploaded/printed`, then stop | REVIEW | `PROJECT_STATE.md`, `NEXT_AGENT.md`, iteration `HANDOFF.md` | slicing, upload, start, physical acceptance | concise synthesis; stop after user-facing artifact delivery |

## Frozen task input rules

- The DESIGN task input is the path-and-SHA list in `BRIEF.md`.
- IMPL must record this BRIEF's SHA-256 and the parent candidate fingerprint
  before editing. Its candidate manifest must include every new/modified
  source, generator, test, STEP, 3MF, provenance, receipt, and snapshot.
- CRITIQUE and VALIDATE must use the same exact implementation candidate
  fingerprint; an implementation repair invalidates both downstream gates.
- REVIEW begins only when independent critique and validation address the same
  fingerprint.
- Existing P20 R4 full-assembly artifacts remain parent evidence and must not
  be silently replaced by print-kit artifacts.

## Required receipt fields

Every worker returns: status; verified input and candidate fingerprints;
changed paths; exact commands/results; artifact SHA-256 values; object labels
and counts; layout footprint and overlap count; relevant mesh/STEP metrics;
requirement coverage; explicit blockers; unresolved risks; and next action.

