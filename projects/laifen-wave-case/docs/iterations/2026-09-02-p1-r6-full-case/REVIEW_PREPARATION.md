# REV-R6-01 formal review preparation

Status: preparation complete for the distinct formal-review join. Owner `/root/uniform_skin_review`, GPT5.4/high. This document does not grant acceptance and does not replace the final immutable `REVIEW.md` join. It records the exact acceptance accounting for the currently frozen full-case candidate while scratch-only export repair work is still outside the candidate.

## Frozen review scope

- Review baseline manifest: `inputs/review-baseline.sha256`, 184 entries, SHA-256 `0925fdfe4b3fcd762ad8370317df2d79cad9d0e265a0b8f887301420d0515835`.
- Current implementation candidate: `inputs/implementation-candidate.sha256`, 135 entries, SHA-256 `4c2750ad632639be5547074173408aa14dfc579faed8d45890ed7233b00c0351`.
- Current design contract: `inputs/design-contract.sha256`, 116 entries, SHA-256 `f72529fe2f5333e80859496453f720635590b11c46a55ec2bb2bc0c942f079b4`.
- Independent validator receipt: `VALIDATION.md`, with inputs144 SHA-256 `36718f6e48a51ab331b832d307126c26e734b5a5a81288a49826270bc25dbcf0` and evidence SHA-256 `1b1cbb84e27e4f610a36820a5f73a5c1fc0e192e8828d5f79a850af750a813ef`.
- Independent critic receipt: `CRITIQUE.md`, with critique-inputs8 SHA-256 `0c9a4485a5eecd40889b153eaa030bcbb35331f737d50eea11fbd1f716148e4a` and critique-evidence11 SHA-256 `8b0e443dcb187502278e7802e01c1b035e411baf8cf72f9b131b9a7860b013e5`.
- Scratch-only diagnosis receipt: `EXPORT_REPAIR.md`. It localizes the cap parity cause but does not mutate the frozen 135-entry candidate.

## Checks performed by the formal reviewer

- verified `inputs/review-baseline.sha256` against live paths with `shasum -a 256 -c`;
- read repository policy, project state, next-agent route, R6 brief/design/implementation/validation/critique/handoff, and export diagnosis;
- confirmed the current `PROJECT_STATE.md` and `NEXT_AGENT.md` both still describe candidate135 as immutable while `IMP-R6-03` remains scratch-only;
- audited the current acceptance boundaries against the independent validator and critic findings, without rerunning CAD generation, export, or geometry kernels.

## Current acceptance accounting

### If the candidate remains `4c2750ad632639be5547074173408aa14dfc579faed8d45890ed7233b00c0351`

- `CAD/source geometry`: ready to PASS in the final join, scoped to the exact default full-case source under `cad/p1_r6_full_case/`. The validator found no blocking geometry or motion defect in the frozen source/BREP candidate.
- `Written STEP`: must remain HOLD in the final join. Validator finding `VAL-R6-01-F01` is still active because the cap source-to-written adaptive volume delta remains about `0.003804650332 mm3`, above the unchanged `0.001 mm3` gate.
- `Slicer/process`: HOLD. The critic and validator bounded first-layer geometry and intended print orientation, but there is still no slicer-profile, toolpath, adhesion, brim, or process evidence for the full 144 mm body and perforated textured floor.
- `Physical`: HOLD. Approximate `L208/D29`, loaded full closure, literal both-end noncontact, new thread fit, `1.4 mm` root strength, wobble, wear, and drainage under real use remain unproven.

### Requirement coverage for the frozen candidate

- `REQ-01/03/05/11/12`: covered for the selected full-case source and two-part STEP outputs. Ready to PASS at scoped CAD/source level.
- `REQ-06/07/08/09/10`: geometry, field continuity, drains, normals, and prescribed motion are covered by independent validation. Ready to PASS for source/CAD geometry only, with slicer/process still HOLD.
- `REQ-02/04/13`: remain evidence gaps. The user explicitly authorized provisional full CAD despite these unresolved physical-fit questions, so they limit claims instead of blocking scoped CAD generation.
- `REQ-14`: intentionally superseded for this full-case CAD route by the user's direct-full instruction; it cannot be used to reopen a short-first prerequisite.

## Blocking finding disposition

1. `VAL-R6-01-F01` is the only measured digital blocker to final written-STEP acceptance for the current candidate. The body passes parity. The cap does not.

2. `EXPORT_REPAIR.md` narrows the cause to the female upper-runout trim/vertex inconsistency near `z9`, and root reports that `IMP-R6-03` is still scratch-only. That diagnosis is useful but does not change the current acceptance outcome. Until a changed official candidate exists and is independently rechecked, the formal review must continue to treat written STEP as HOLD.

3. Critic findings `C-R6-01`, `C-R6-02`, and `C-R6-03` remain acceptance-boundary findings, not reasons to reject scoped full CAD/source geometry. They preserve the slicer/process and physical HOLD lines and prevent overclaiming measured fit or retention.

## Join readiness rules

- If root closes the task on the unchanged candidate135, the final formal review can write `CAD/source geometry PASS`, `written STEP HOLD`, `slicer/process HOLD`, `physical HOLD`.
- If root promotes any official source or STEP change from the scratch repair, candidate135 is no longer the review target. A new candidate fingerprint is required, and at minimum the affected written-STEP parity gate must be rerun independently before final review. Because the change targets a thread runout boundary, the written cap artifact and any assemblies containing it must be considered affected.
- Root's latest scratch checkpoint indicates a minimal cap-only source normalization can likely restore cap parity without changing body geometry, the exterior skin, or the selected laws. If root freezes that repair into an official candidate, the smallest required independent reopen is:
  - source-law and selector preservation on the changed cap runout boundary;
  - written-STEP parity for `cap_c25.step`;
  - affected assembly artifact checks for `closed_c25.step` and `print_layout.step`, since both embed the changed cap occurrence;
  - critic confirmation that the repaired cap leaves the visible seam, profile, section, and layout intent unchanged.
- Body-only geometry, full-length body skin evidence, and unaffected global math need not be rerun if the new candidate explicitly preserves their hashes or independently proves those source laws and artifacts unchanged.
- The user’s request for “only the STEP path after fix” must not be satisfied from the current candidate as if the fix were complete. The current path exists, but the fix and independent revalidation do not.

## Reviewer conclusion at this stage

The current evidence is internally consistent: full-case source geometry is in review-ready shape, the cap written-STEP parity gate is still failing, and the remaining slicer and physical gaps are explicit. Formal review should wait for root’s final immutable join decision after either:

- declaring the unchanged candidate as a scoped geometry PASS plus written-STEP HOLD, or
- freezing a new repaired candidate and routing independent revalidation on the affected written artifacts.
