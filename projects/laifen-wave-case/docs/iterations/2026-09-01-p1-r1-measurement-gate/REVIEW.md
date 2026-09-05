# Independent review
Current result: reduced preview accepted for user measurement/intent feedback by CRI-02, VAL-02 and REV-01. Earlier failures below are historical evidence and remain rejected. No CAD or physical acceptance exists.
Design findings F-01..F-04 in DESIGN.md remain open. Root must record each distinct runtime identity, verified candidate fingerprint, evidence and disposition before advancing.

## Initial candidate critique
Critic: `/root/case_preview_critic`, Sol/high, read-only; implementer `/root/case_preview_impl` is distinct.
Candidate fingerprint: `da5a17a87a22675a1b0d04843ec592582085cf0f65cace118c0ced35c4f7adc0`; all 11 manifest entries verified before and after review.
Command: `shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-01-p1-r1-measurement-gate/inputs/candidate.sha256`.
Findings below refer to the initial `preview/measurement-gate.html`, lines 17–20. Status: repair requested, not accepted.
| ID | Severity | Finding and required correction |
|---|---|---|
| CRI-01-A | P1 | Drawn floors invade usable cavity by 3 mm at each end; move floor material outside inner datums 0 and C. Nominal centered envelope otherwise overlaps each drawn floor by 0.5 mm. |
| CRI-01-B | P1 | Bore/device/outer widths use unrelated scales; derive all radial geometry from the same scale and ID/D/wall parameters. |
| CRI-01-C | P1 | Display both computed end gaps and distinguish overlap 5 from effective engagement target 5–6, pending. |
| CRI-01-D | P2 | Explicitly flag axial slack below 3, radial gap below 1 and inadequate texture base wall; never recommend a negative cut depth. |
| CRI-01-E | P2 | Solid stop line crosses the bore/device; annotate external wall without implying an internal obstruction. |
| CRI-01-F | P2 | Add actual fixed-pitch strip with full-repeat count and expanded smooth margins; current text alone does not demonstrate the relationship. |
Conditional OD assumptions and unretained-position labels were consistent with the contract. These findings concern the preview only, not evaluated CAD.

## Critic rerun after repair cycle 1
Same independent critic and read-only scope; fingerprint `8611dd9ec2b5e511dc51cfb5d78b1ad00645c24add139bfff327dac564ebbd9f`, all 11 hashes checked before/after. CRI-01-A/B/C/D resolved. CRI-01-E partially resolved: fixed 14 px shoulder ticks still extend inward into the bore at narrow widths; draw them outward only. CRI-01-F partially resolved: N complete repeats require N+1 boundaries (default last boundary at 36 mm), not N ticks. Additional P2: restore the frozen contract's illustrative downward gravity cue. Scope remains preview only; final repair requested.

## Retry ceiling and scope reduction
IMP-01 repair cycle 2 failed during a text transformation: the implementer reported invalid SVG coordinates (`x1="-e"` and blank texture boundary attributes) despite passing VM tests. It stopped without freezing or claiming acceptance. This exhausted its initial attempt plus two repair cycles; further repairs under the same plan are prohibited.
Root preserved the failed source under disposable `scratch/failed-repair2/` and reopened design as DES-02. The reduced preview will cover only the essential axial-clearance/device-envelope relationships; optional thread-budget and texture demonstrations are deferred. Original full-case requirements are unchanged. A new bounded implementation role will author the smaller preview from a revised frozen contract; this is an explicit scope reduction, not a reset of the failed candidate's attempt counter.
Lesson: passing formula/VM tests cannot validate malformed SVG attributes. The reduced candidate needs actual DOM coordinate checks and inspected browser screenshots before formal review.

## CRI-02 reduced-candidate receipt
Critic `/root/case_preview_critic` (Sol/high), read-only, distinct from reduced implementer `/root/case_preview_recovery`. Fingerprint `85c04f7de4dce3e6ff4ab092c5f483c8d7449b6f1a3335d6e8197d17e6a1fc73`; all 13 manifest paths checked before and after review.
Verdict: PASS within the reopened measurement-preview contract; no remaining P1/P2 source/intent findings. Verified uniform dimensional scale, inner floors at 0/C and external 3 mm floors, individual/total gaps and zero-slack contact, entirely external stop cue/leader, gravity direction, separate overlap/engagement-pending labels and unmeasured/invalid states. Runtime/layout remain VAL-02's gate.
Old optional thread-budget/texture-strip findings are deferred by explicit DES-02 scope reduction, not claimed fixed or accepted as final case design. Full case, CAD, fabrication and physical requirements remain pending. Formal review awaits same-fingerprint VAL-02 evidence.

## REV-01 formal independent join — PASS
Formal reviewer `/root/case_preview_review`, GPT-5.4/high, read-only; distinct from reduced implementer, critic and validator. Candidate fingerprint `85c04f7de4dce3e6ff4ab092c5f483c8d7449b6f1a3335d6e8197d17e6a1fc73`.
Commands: `shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-01-p1-r1-measurement-gate/inputs/candidate.sha256` -> 13/13 OK; hashing that manifest matched the assigned fingerprint.
No blocking findings. Both independent receipts reference that exact candidate; role separation, explicit retry escalation, scoped requirement coverage and acceptance boundaries are consistent. REQ-02/03/04/12/14 are represented by this teaching gate; full thread/texture/fabrication/source-export/physical requirements remain pending. Root pyproject.toml is included in the manifest but unchanged; root uv.lock registers the new dependency-free project.
Disposition: PASS for preview handoff only. User measurements and the end-contact decision remain open; full CAD/STEP/mesh/slicer/physical work has no acceptance. The pre-existing XT60 repository-structure failure remains documented outside this project's scope.
