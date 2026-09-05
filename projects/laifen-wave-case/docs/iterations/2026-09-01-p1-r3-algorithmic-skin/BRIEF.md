# P1 R3 generic screw-cylinder generator and continuous grip skin

<!-- FROZEN-CONTRACT-BEGIN -->
Design owner DES-SKIN-01 `/root/skin_design`; baseline repository `d0aab1ff21a0cd2e5790c9800fcec7cfec2bfc3c`. R2 implementation candidate is `../2026-09-01-p1-r2-fit-feedback/inputs/coupon-fixed-candidate.sha256`, fingerprint `3da2cac2b8d29b379b3be6309e3b7eb623fc50f6766dd5a573438a49517f6e4d`; all59 entries verified before design freeze. Its repaired thread source evidence is useful; STEP parity remains unresolved and no physical acceptance exists.

User outcome: a generic, mathematically parameterized cylinder with a cap that screws on/off and a procedural surface over its entire grippable area. Laifen is a named provisional preset. The user rejected the R2 two narrow rows as inadequate for hand-grip testing. The new short experiment therefore has a closed body with a substantial countergrip and a matching closed cap, both covered by a continuous diamond tessellation, excluding deliberate functional boundary zones. Three cap clearances share one body. This remains P1 R3: same two-piece threaded-cylinder architecture and user operation; reusable generator factoring and a better grip experiment do not introduce a new product mechanism.

Use: hold the body band, align thread starts, hand-tighten cap to the external shoulder, assess both grip surfaces, release and repeat five empty cycles per clearance. This experiment needs no toothbrush measurement. Laifen full-size production remains behind the existing measured L/D and end-contact gate; provisional L208 plus slack5 means cavity213, not a measured brush or approved full case.

R3 requirement addendum, without mutating the frozen R2 REQUIREMENTS.md:

| ID | Contract |
|---|---|
| REQ-GEN-01 | Invariant: Params -> derived dimensions -> one shared original thread implementation -> body/cap/assembly/coupons/STEP. No Laifen constants hidden in geometry builders. |
| REQ-GEN-02 | Inputs expose cavity length, cap height, both bores, wall/floor, thread pitch/engagement/clearance, skin pitch/depth/phase. Reject infeasible combinations with the failed inequality. |
| REQ-SKIN-01 | Derived: continuous periodic full-surface diamond tessellation across every usable straight grip band; no isolated appliques or a hardcoded two-row count. Pitch never scales with length. |
| REQ-SKIN-02 | Default short experiment has two24mm bands, h0.45, N31, pz4.8, >=2mm smooth boundary zones, blunt tips >=1mm in the analytic developed section, OD<=39 and minimum structural wall1.8. |
| REQ-SKIN-03 | Invariant: keep threads, shoulder and collar smooth; texture is raised only and does not modify the thread profile or clearance. Preserve shared assembled theta/z datums. |
| REQ-SKIN-04 | Physical unknown: comfort, useful friction, skin printing, layer strength, fits and five-cycle wear. Analytic/visual/CAD/export/physical evidence remain separate. |
| REQ-GEN-03 | Invariant: actual solids and written STEP must satisfy the four evidence categories and screw path; parameter cases must catch infeasible grip length, wall/OD and slope budgets. |

Original reference inspected at `/Users/scottchu/.codex/attachments/bcb55926-9802-44b5-8cd4-6c7b5ca61bb9/codex-clipboard-74ccc492-83fe-4c09-91cf-88a06d6bcf0f.png`; raised faceted metal-grip intent only, no traced image or copied mesh. Rejection screenshot inspected at `/tmp/codex-remote-attachments/01a06004-6842-76f1-bf1e-486590d05ac5/09FB4EE1-8AF5-4087-AE3C-204FF04C84FE/1-Pasted-Image-1.jpg`.

Non-goals: copying downloaded case geometry, full Laifen fit/retention approval, printer operation, or promoting the repaired R2 source evidence to artifact acceptance. This task makes analytic review material and a design contract, no CAD solids.
<!-- FROZEN-CONTRACT-END -->

## Execution plan and status (mutable, excluded from contract fingerprint)

| ID / owner | Role and dependency | Exclusive writes / done gate | Ceiling |
|---|---|---|---|
| DES-SKIN-01 `/root/skin_design` | Design; reads frozen R2 candidate and supplied references | This iteration, p1-r3-skin-study.py/.svg, new ADR/experience entry; exact equation/domain/API + teaching visual + frozen manifest | strong/high qualitative; 8min/12k tokens after expanded scope; initial + one focused repair; no children |
| IMP-GEN-01 unassigned | Implementation; requires selected R3 analytic gate and frozen contract | Future cad/p1_r3_generator and focused tests; primary STEP only first | Root assigns owner/ceilings before work |
| CRI-GEN-01 / VAL-GEN-01 unassigned | Distinct critic and validator; frozen generated candidate | Read-only candidate, disjoint evidence records | Root assigns; maximum three workers total |
| REV-GEN-01 unassigned | Distinct formal-review join | Review record only | Requires critic + validator receipts |

Allowed reads are declared frozen inputs, workspace policy and skill references. Forbidden design scope: live CAD edits, R2 tests/artifacts, services, printer, unrelated projects and root continuity indexes. Stop on required changes to functional thread math or a mathematical infeasibility; return the smallest failing constraint. Root owns CURRENT/PROJECT_STATE/NEXT_AGENT and future DAG scheduling.
