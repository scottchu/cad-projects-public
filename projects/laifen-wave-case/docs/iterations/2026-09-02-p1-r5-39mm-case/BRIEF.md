# P1 R5: 39 mm case interface and short experiment

## Frozen brief contract

DES-R5-01, owner `/root/case39_design`, design role, 2026-09-02. This is a new original parametric revision in future `cad/p1_r5_39mm_case/`; R4 source and accepted artifacts remain read-only. Input manifest `inputs/baseline.sha256`, SHA256 `2eb7079c84d83c0734872850e15cfd94e43acdd51a9096c49c75b7e566d85a9b`, binds baseline HEAD plus working source, requirements, contracts, tests, artifacts and supplied photos. R4 candidate80 `e56a117867e2cb0b77e706068636d56fb2adfa5e0eacf34fb2e7cd40897571cb` is accepted only for its scoped short CAD/source and written STEP. R3 user hand closure is encouraging baseline evidence, not acceptance of the new thread.

Outcome: 39 mm maximum crest envelope on both halves, same mathematically generated blunt diamond proportions across seam, small outer chamfers at both closed ends, and water openings. Keep bores30/31 and user-confirmed total axial allowance5. New outside size intentionally reopens our old thread-root1.8 assumption; the user-required texture-zone residual wall1.8 remains binding. Selected new short-test thread root16.4, crest16.9, height0.5, pitch2, effective engagement6, radial clearance0.25 with0.30 budget. Exact geometry and gates are in DESIGN.md.

Use: grip body and cap, screw to external positive shoulder, unscrew, insert/remove device for a later full case. Toothbrush must never be closure stop. Literal prevention of contact with both internal ends is unresolved. Full length remains C=L+5, conditionally213 for approximateL208; no full-case release, silent retention waiver, copied mesh, global scaling, slicing or printer action in this design task. New short cavity72.5 is an experiment independent of unknown full length.

References inspected: three supplied long-case photos show desired common outside envelope, dissimilar diamond proportions across seam, outer end transition and seven visible floor holes. Two ruler photos and preceding short-coupon photo inspected; reference dimensions remain governed by USER_INTAKE and the observation record, not new image measurement. Formula geometry is original; no mesh is imported. PLA/U1/nozzle0.4/layer0.2/openings-up/supports-off are intended settings, not a resolved process.

Evidence distinction: this contract/2D study establishes arithmetic feasibility only. New CAD, written STEP, slicer and physical acceptance remain pending independent gates. The short pair is authorized design work; root records later delivery decisions and project continuity.

## Mutable execution DAG

Common scope: project `projects/laifen-wave-case`, iteration this directory; root baseline above. Each downstream owner verifies its assigned SHA256 manifest before and after work. Exclude only mutable DAG/status/evidence from frozen contract manifests. One writer per namespace, maximum3 workers. Initial attempt plus at most2 focused repairs; stop on changed inputs, topology/geometry limits, unmet done gate or repeated failure. Exact token/runtime enforcement is unavailable; ceilings below are qualitative.

| ID / owner | Role, objective and done gate | Dependencies / immutable inputs | Reads / exclusive writes / forbidden scope | Deliverables and ceilings |
|---|---|---|---|---|
| DES-R5-01 / /root/case39_design | Design; select buildable short contract and dimensioned formula study | frozen baseline manifest above | Project policies, frozen project evidence; write BRIEF/DESIGN/NUMERIC_NOTES, design manifests, preview/p1-r5-39mm-study.*; no CAD/tests/requirements/decisions/Git/services/printer/children | Contract, study, receipt; strong/high, ~8min/9k tokens, 3min checkpoint, one candidate plus2 repairs |
| OBS-R5-01 / /root/case39_observations | Record supplied physical references without inventing measurements | same frozen source photos/intake | Photos/evidence; only observation record and append-only EXPERIENCE; no design/source | observation receipt; bounded inventory/interpretation; root owns exact runtime identity and checkpoint |
| IMP-R5-01 / /root/case39_impl | Implement original39mm short pair and four explicit STEP targets; no self-approval | frozen brief/design/source input manifest | R4 read-only; exclusive new R5 CAD namespace and focused implementation evidence/tests as root assigns | Source, targets, stage timings, exact receipt; balanced/medium if prescribed, initial+2 repairs, checkpoints before skin and export |
| CRIT-R5-01 / unassigned | Independent mechanical/visual critique | frozen implementation candidate | read-only candidate; own CRITIQUE evidence only | concern disposition and snapshots; strong/high, bounded focused review |
| VAL-R5-01 / /root/case39_validate | Independent solid/math/constraint/requirement/export checks | same candidate as critic | read-only candidate; own validation evidence only | exact commands/hashes/results, new thread path and weakened-root evidence; strong/high |
| REV-R5-01 / unassigned | Formal independent acceptance join | critic+validator receipts and same candidate | candidate and evidence read-only; own REVIEW only | separate CAD/STEP/slicer/physical conclusions; strong/high |

Implementation, critic, validator and formal reviewer must be distinct runtime identities. Root binds exact task-specific manifests, exclusive writes and ceilings before scheduling; changes invalidate only gates whose manifests include changed inputs. Full-case work is a future DAG gated by installed envelope/end-contact decision and new-thread physical result, not an automatic continuation of the short release.

Scheduling update: design94 frozen as 64186f7fc3da984878296798305a1189c38d84ae0bedba9356171f95097be2c2; implementation Sol/high active (20min/18k, initial+2 repairs). Validation Sol/high prepares from frozen design only (4min/5k); candidate-dependent execution waits for root handoff (15min/15k). Exact scope and ownership are in HANDOFF.
