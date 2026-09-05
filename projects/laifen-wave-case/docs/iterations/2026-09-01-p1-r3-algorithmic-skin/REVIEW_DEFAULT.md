# REV-GEN-01 formal default review join

Owner `/root/preview_formal_review`, independent formal reviewer; 2026-09-02. Reviewed exact join manifest `inputs/default-review-join.sha256`, fingerprint `8da40d095ce991d4ad4aea8ff1e9fb507d2205e11f37db612c2fe27663874322`. All81 declared entries verified `OK` during this review.

This join is limited to the frozen **default short generator candidate** and the explicit DES06/DES07 evidence status. It does not approve the advertised full editable parameter range, fabrication meshes, slicing, printer action, or physical use.

## Verified provenance

- Default candidate: `inputs/geometry-default-candidate.sha256`, fingerprint `4e1ea38ac083f2f9b708770165bb2281748f129826f1f50bd1782139484a9ffd`.
- Default parameter fingerprint: `50f1e34681419a81f91b4587b8f1e11a97569b3e99cc530891dfcee32b302677`.
- DES06 method package: `inputs/export-evidence-contract.sha256`, fingerprint `111af8062d02c2c515979617d97de788671821d63927f4acfc8267cbfcf0da64`.
- DES07 diagnosis package is frozen as evidence only: `inputs/pitch-recovery-inputs.sha256`, bound through this review join; it is not an implemented or validated candidate.
- Critic receipt reviewed: `CRITIQUE_DEFAULT.md`.
- Validator receipts reviewed: `VALIDATION_DEFAULT.md` and `VALIDATION_EXPORT_DES06.md`.
- Presentation evidence reviewed from the frozen join packet: `cad/p1_r3_generator/README.md`, `scratch/generator-critique/print-layout-rendered_20260902T042508Z.png`, `scratch/generator-critique/print-layout-top-caps_20260902T042613Z.png`, `scratch/generator-presentation/RECEIPT.md`, and `scratch/generator-presentation/longitudinal_20260902T043413Z.png`.

## Findings and disposition

### CAD/source layer: PASS for the frozen default short preset only

- `IMPLEMENTATION_CORE` and `VALIDATION_DEFAULT` support a real reviewable source/BREP candidate for the exact default preset: valid positive solids for body/C20/C25/C30; matching canonical STEP siblings; measured bores30/31; 416 actual thread samples within the unchanged0.01mm gate; 308 actual skin samples; three default mouth-boundary continuous bounds approximately0.0002mm; valid closed/exploded/layout assemblies; and independent zero-intersection screw poses plus positive negative-stop sensitivity.
- `CRITIQUE_DEFAULT` supports the user-intent side of the same default preset: the rendered print layout shows broad continuous grip coverage rather than the rejected two-row treatment, and the cap-top snapshot shows readable recessed `20/25/30` markings.
- The later diagnostic cutaway in `scratch/generator-presentation/longitudinal_20260902T043413Z.png` resolves the critique packet's earlier visualization gap honestly enough for review communication: it is a read-only half-space Boolean on exact `closed_c25.step`, and the image visibly shows the connected cavity, both closed floors, and the neck/thread region. It is a diagnostic view, not new metrology.
- This CAD/source pass is bounded to the exact default preset and current frozen artifacts. It does **not** extend to the general editable pitch/engagement domain, smaller-bore cases, or the still-gated Laifen full-case preset.

### STEP/export layer: HOLD

- `VALIDATION_DEFAULT` explicitly held the STEP layer because whole-surface source/export correspondence was incomplete after the original nonbijective face-matching attempt. That hold was not a measured geometry defect.
- `DES06_EXPORT_EVIDENCE` selected a narrower, coherent continuation method: mass-centroid candidate pairing, exact rational support comparison, ordered true-trim correspondence, explicit analytic-family handling, and a hard stop at the first unsupported class.
- `VALIDATION_EXPORT_DES06` then completed the reopened body branches cleanly: 2311/2311 unique body face matches by actual mass centroid; 2294 one-span rational faces with combined support-plus-trim bound `2.0480750505e-11mm`; three multispan thread faces with combined physical bounds `0.000068503281561mm`, `0.000001699494266mm`, and `0.000051203062990mm`, all below the unchanged0.01mm criterion.
- The reopened validator then stopped exactly where DES06 required: body face123 reaches an unsupported `GeomAbs_Circle` 2D p-curve on the inner wire of the Z0 shoulder plane. The descriptors recorded in `VALIDATION_EXPORT_DES06.md` are precise enough to route the next method addition without implying a defect in the underlying default geometry.
- Because the remaining analytic body faces, cap correspondence branches, cap whole-skin derivative transport, plateau-width transport, seam completion, and exact floor/OD extrema are still unfinished, the written STEP/export layer remains HOLD. No STL/3MF or slicer work should start from this review.

### Fabrication/physical layers: HOLD

- No fabrication meshes are frozen or reviewed here.
- No slicer validation, first-layer path validation, or support-free print evidence exists for this R3 default candidate.
- No physical grip, fit, wear, comfort, five-cycle, strength, or full Laifen installed-brush evidence exists.

## Nondefault and scope boundaries

- The guarded nondefault case `p=2.4`, `E=7.2`, `C=82.1`, `H=47` remains an unresolved separate diagnosis. `DES07_PITCH_RECOVERY.md` describes a plausible partitioned-cutter repair route, but that route is still design-only scratch evidence and has not been implemented, independently validated, or accepted.
- The current candidate therefore must be described as a **default short-preset CAD candidate under review**, not as a generally validated editable screw-cylinder generator.
- The current hold is methodological and scoped: no source redesign is justified by the DES06 unsupported analytic-circle stop alone, and no manufacturing approval is justified by the current CAD/source pass.

## Formal decision

- CAD/source layer: **PASS** for the exact frozen default short preset candidate `4e1ea38ac083f2f9b708770165bb2281748f129826f1f50bd1782139484a9ffd`.
- STEP/export layer: **HOLD** pending completion of the remaining DES06 analytic/cap correspondence work on the same default candidate.
- Fabrication/physical layers: **HOLD** pending mesh, slicer, and real physical evidence.

The current handoff is honest and precise enough to proceed without broad reruns. The smallest next step is the one already named by DES06 and VAL-GEN-02: add explicit analytic circle/frame correspondence, then finish the remaining analytic body families and apply the established method to caps before any STEP-release, mesh, or slicer work.
