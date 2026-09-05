# REV-R6-01 formal independent review

Status: complete. Owner `/root/uniform_skin_review`, formal independent-review join role, GPT5.4/high. This review joins the repaired implementation, independent repair validation, independent repair critique, and preserved pre-repair evidence for the exact full-case candidate only.

## Frozen provenance

- Repaired join manifest: `inputs/review-repaired-join.sha256`, 234 entries, SHA-256 `be20db1f9bd1e9e5ac2d0967f6102bfe7661dfc76bc8810a4f7563fc9d5ce87e`.
- Reviewed repaired candidate: `inputs/implementation-repaired.sha256`, 145 entries, SHA-256 `a3873490fc7d7742698d9d73aceb6a8a29131fd8b846c76973d7133afb438bdc`.
- Repaired validation receipt: `VALIDATION_REPAIR.md`, inputs158 SHA-256 `3679717b59d3eeca3f3bfbb7cf98967106b304a2557e8e43bb37dfbd8062fab7`, evidence18 SHA-256 `78af5b48e569cd1d427cdd1c67963df30f4a126f58087cfb9d427e6d3feed295`.
- Repaired critique receipt: `CRITIQUE_REPAIR.md`, inputs12 SHA-256 `66b8e44708984b7db90d8896c1a2e3c6990009851760b94d5227e4efb89a7dfd`, evidence11 SHA-256 `494f31477330f5059a9d6a547fac7465dcf5e38079273bd7405bec6495f41908`.
- Archived original production map: `scratch/fullcase-export-repair/production/before-map.json`, exact six preserved originals from candidate135.

## Reviewed repaired artifacts

- Full closed case STEP: `cad/p1_r6_full_case/closed_c25.step`
- Standalone cap STEP: `cad/p1_r6_full_case/cap_c25.step`
- Standalone body STEP: `cad/p1_r6_full_case/body.step`
- Two-part print layout STEP: `cad/p1_r6_full_case/print_layout.step`

Exact current hashes:

- `body.step`: `b5d425acecb35a57264e4267b7958608af289d2975c53c6d94c059083226fbdd`
- `cap_c25.step`: `5b47075e5ee27dc57b8089c7955856e15119b8a7692569c2f0f532d4a21f4afe`
- `closed_c25.step`: `31e4125fcfc6d6c543312491298d8a508f0d2db9a5da247b6a933b6fa7d3efa6`
- `print_layout.step`: `be27b1c7962bcc241babea257aa85b11bc1675b83072f475bf684e865d166410`

## Checks performed

The formal reviewer did not rerun optional geometry or CAD generation. Checks were limited to provenance, repaired-scope audit, and evidence review:

- verified `inputs/review-repaired-join.sha256` at entry;
- read the original implementation, original validation failure, export diagnosis, production repair receipt, repaired validator receipt, repaired critic receipt, review preparation, and preserved before-map;
- audited the candidate delta from original135 to repaired145 to confirm the repair touched only the cap-containing path set plus the narrowly scoped helper and preservation records;
- spot-checked the repaired written-STEP visual evidence:
  - `scratch/fullcase-critique/repair/closed-long-shaded_20260903T033014Z.png`
  - `scratch/fullcase-critique/repair/section-dimensions.png`
  - `scratch/fullcase-critique/repair/print-layout-open-up_20260903T033441Z.png`
- read the runtime presentation receipts proving the current repaired closed STEP and print layout pages are `HTTP 200` and `state=ready`, and the repaired private images match the inspected PNG bytes.

## Repair scope and inherited evidence

The production repair is acceptably narrow. Relative to original candidate135, the authoritative source/artifact delta is:

- changed: `cad/p1_r6_full_case/parts.py`, `cad/p1_r6_full_case/README.md`, `cad/p1_r6_full_case/cap_c25.step`, `cad/p1_r6_full_case/closed_c25.step`, `cad/p1_r6_full_case/print_layout.step`, `tests/test_full_case.py`
- added: `cad/p1_r6_full_case/runout.py`, `inputs/native-repair-contract.sha256`, and the exact six-file preservation archive under `scratch/fullcase-export-repair/production/before/`
- unchanged by hash: `body.step`, all wrapper `.step.py` files, `params.py`, `thread_profile.py`, `skin.py`, `surface.py`, and `review.py`

The preserved before-map proves the original six changed files from candidate135 still exist byte-for-byte in the production archive. Because the repaired validator independently confirmed unchanged body/source hashes, unchanged body placement, unchanged exterior field behavior, and unchanged AST/function regions outside the cap runout call, the earlier body/math/field evidence is inherited for repaired145 where explicitly referenced by the repaired validation receipt. The final join does not inherit the old cap STEP parity failure; it requires the repaired receipts that close it.

## Findings and disposition

### Acceptance verdict

- `CAD/source`: PASS for the exact default repaired source in `cad/p1_r6_full_case/`.
- `Written STEP`: PASS for the exact repaired default artifacts listed above.
- `Slicer/process`: HOLD.
- `Physical`: HOLD.

### F01 resolution

Original validator finding `VAL-R6-01-F01` is closed for repaired candidate145. Independent repair validation measured the cap source-to-written adaptive volume difference at `0.000023276275897 mm3` for `eps=1e-8` and `0.000014764918888 mm3` for `eps=1e-10`, both below the unchanged `0.001 mm3` gate. Closed and print-layout occurrences were then independently rechecked and matched the repaired standalone parts exactly, so the previous written-STEP HOLD no longer applies to candidate145.

### Requirement coverage

- `REQ-01`: PASS. The repaired candidate remains original source-first CAD, not downloaded mesh reuse.
- `REQ-03`: PASS for scoped CAD/source and written STEP. The repaired case preserves bores `30/31`, nominal radial readouts including `0.5 mm` lower-body radial clearance at `D29`, and derives usable cavity `213` from approximate `L208` plus allowance `5`. These remain nominal source/readout assumptions, not physical proof.
- `REQ-05`: PASS for scoped CAD/source and written STEP. Outside length `219`, OD39 envelope, floors, and drain geometry remain covered.
- `REQ-06` and `REQ-07`: PASS for scoped CAD/source and written STEP. The repaired native runout normalization preserves the selected thread law and positive-stop relationship without relaxing the acceptance threshold.
- `REQ-08` and `REQ-09`: PASS for scoped CAD/source and written STEP. The full-length shared diamond field, seam continuity, and drain-face appearance remain intact after repair.
- `REQ-10`: HOLD for slicer/process. Intended print orientation and first-layer geometry checks exist, but no slicer-profile or toolpath evidence exists.
- `REQ-11`: PASS for the exact repaired full-case source and STEP deliverables. The exact user-facing full STEP path after fix is `projects/laifen-wave-case/cad/p1_r6_full_case/print_layout.step`; the closed assembly review STEP remains `projects/laifen-wave-case/cad/p1_r6_full_case/closed_c25.step`.
- `REQ-12`: PASS for the selected default CAD/source contract. The repaired review still preserves meaningful source parameters and fixed bores under `D` changes.
- `REQ-02`, `REQ-04`, `REQ-13`: HOLD as physical evidence gaps. Approximate `L208/D29`, loaded full closure, literal both-end noncontact, fit, wobble, wear, strength, and drainage under real use are not proven.
- `REQ-14`: superseded for this full-case CAD route by the user's direct-full instruction and must not be reintroduced as a short-first prerequisite.

### Critique boundaries retained

No new critique blocker was introduced by the repair. The following remain explicit non-acceptance boundaries:

1. Tall patterned perforated first layers remain a slicer and adhesion risk until an actual slice or print run exists.
2. The new threaded joint still lacks physical evidence for root strength, clearance, wobble, wear, and loaded closure.
3. The gold `L208/D29` device cylinder in the section is still reference-only, centered, and unretained. It does not prove actual fit, retention, or literal two-end noncontact.

## Evidence summary

- Repaired implementation proves the official fix is a bounded native runout normalization that keeps vertex coordinates and tolerance, archives all six changed originals, and regenerates only the cap-containing STEP set.
- Repaired validation proves the changed cap closes the old parity defect, preserves source/runout laws, preserves unchanged body and exterior evidence where hashes/laws match, and revalidates the affected `cap_c25`, `closed_c25`, and `print_layout` artifacts.
- Repaired critique proves the repaired cap and cap-containing assemblies preserve the visible full-length 39 mm silhouette, seam behavior, section story, seven drains, and two-part opening-up layout.
- Runtime receipts `scratch/r6-fixed-viewer-readiness.json` and `scratch/r6-fixed-presentation-receipt.json` confirm the current repaired closed STEP and print-layout pages are ready and the reviewed images match the served bytes.

## Final boundary

REV-R6-01 accepts repaired candidate `a3873490fc7d7742698d9d73aceb6a8a29131fd8b846c76973d7133afb438bdc` for scoped `CAD/source` and `written STEP` evidence only. It does not approve slicer readiness, print readiness, or physical fit/performance. The user-facing full STEP path after fix is `projects/laifen-wave-case/cad/p1_r6_full_case/print_layout.step`; the closed assembly review STEP remains `projects/laifen-wave-case/cad/p1_r6_full_case/closed_c25.step`.
