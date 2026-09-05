# REV-R4-01 formal independent review

Status: complete. Owner `/root/uniform_skin_review`, formal independent-review join role, GPT5.4/high. This review is read-only and joins the frozen R4 implementation, independent validation, and independent critique for the exact default candidate only.

## Frozen provenance

- Join input manifest: `inputs/formal-review.sha256`, 111 entries, SHA-256 `7e36a21d6d364a318d72208c8f8f5b62667d5174c93777a1d4c43575f1b2951e`.
- Reviewed candidate manifest: `inputs/implementation-candidate.sha256`, 80 entries, SHA-256 `e56a117867e2cb0b77e706068636d56fb2adfa5e0eacf34fb2e7cd40897571cb`.
- Frozen design manifest: `inputs/design-contract.sha256`, 63 entries, SHA-256 `d1413f9b17a4e0e7007cebd4e68c07335b11def9805d24d642d25937e391113f`.
- Primary written artifacts:
  - `cad/p1_r4_uniform_skin/body.step`
  - `cad/p1_r4_uniform_skin/cap_c25.step`
  - `cad/p1_r4_uniform_skin/closed_c25.step`
  - `cad/p1_r4_uniform_skin/print_layout.step`

## Checks performed

The reviewer did not rerun CAD generation or validation kernels. Checks were limited to provenance and evidence audit:

- verified `inputs/formal-review.sha256` with `shasum -a 256 -c`;
- read repository policy/state files plus the R4 implementation, validation, critique, handoff, observation, and comparison records;
- spot-checked candidate contents and confirmed `cad/p1_r4_uniform_skin/thread_profile.py` is byte-identical to the preserved R3 thread profile;
- inspected the exact critic-rendered written-STEP evidence:
  - `scratch/uniform-skin-critique/closed-front-shaded_20260903T013939Z.png`
  - `scratch/uniform-skin-critique/closed-longitudinal-collar_20260903T013850Z.png`
  - `scratch/uniform-skin-critique/print-layout-open-up_20260903T013850Z.png`
- spot-checked validator evidence JSON for screw-motion, seam, and plateau results under the frozen candidate.

## Findings and disposition

### Acceptance verdict

- `CAD/source`: PASS for the exact default R4 source namespace `cad/p1_r4_uniform_skin/`. The implementation preserves the fitted bores, pitch, engagement, taper, and thread construction while isolating the new exterior envelope and rejecting unsupported drift.
- `Written STEP`: PASS for the four exact default R4 STEP artifacts listed above. Independent validation covers topology, source-to-written parity, full-coverage exterior checks, seam continuity, first-layer connectedness, layout placement, and prescribed representative screw poses including positive-stop overtravel.
- `Slicer/process`: HOLD. Geometry and first-layer-shape checks passed, but no slicer profile, toolpath, extrusion, or adhesion evidence exists for R4.
- `Physical`: HOLD. The earlier R3 hand-closure report does not prove R4 seam feel, grip, torque, wobble, wear, strength, or printed finish.

### Requirement coverage

- `R4-01` straight common OD40 envelope and no smooth collar: covered by design contract, validator surface checks, and critic written-STEP images. PASS.
- `R4-02` full assembled common-phase diamond field across body, seam, and collar: covered by validator seam/radial evidence and critic seam closeup. PASS.
- `R4-03` preserved bores/thread/shoulder stop and fitted internals: covered by locked source parameters, byte-identical thread profile, functional-mask zero differences, and representative screw-motion checks. PASS.
- `R4-04` preserved short internal geometry and closed length78.5: covered by validator topology/bounds and functional-mask comparisons. PASS.
- `R4-05` wall and ligament budget at OD40/h0.45: covered by design math and validator wall evidence. PASS.
- `R4-06` shared N34 field, plateau, and slope bounds: covered by design math and validator plateau/normal checks. PASS.
- `R4-07` one body plus one C25 cap with closed and print-layout outputs: covered by implementation scope, validator topology/bounds, and critic layout image. PASS.
- `R4-08` intended vertical open-up print orientation and required written-artifact checks: geometry portion PASS; slicer/process portion HOLD.
- `R4-09` physical seam/grip/print behavior: still pending physical evidence. HOLD.

### Review findings

1. Non-blocking continuity finding: `projects/laifen-wave-case/README.md` still describes the old P1 R2 measurement-preview deliverable and says no case CAD or print artifact exists. This conflicts with the active R4 state and should be corrected before iteration closeout. It does not invalidate the reviewed R4 CAD/source or written-STEP evidence.

2. Critic finding `C-01`: resolved for the scoped CAD/source and written-STEP geometry question. The critic flagged scalloped first-layer risk from the textured relief; the validator proved each part has one connected material face and one perimeter wire at print Z0.01 and Z0.20, with no disconnected starting islands. This closes the geometry portion only. Slicer/process evidence remains pending.

3. Critic finding `C-02`: remains open by design. Visual seam continuity does not establish physical tightening angle, tactile feel, torque, wear, or grip. This remains a physical HOLD only and does not block scoped CAD/source or written-STEP acceptance.

4. Historical R3 export HOLD is not inherited as an automatic R4 blocker. The frozen R4 contract intentionally replaced the old broad export method with narrower actual-solid and written-STEP gates, and those gates passed on this exact candidate.

## Evidence summary

- Validator disposition: [VALIDATION.md](./VALIDATION.md) reports PASS for the focused default source/BREP and written STEP gates, including zero functional-mask deltas, adaptive parity within `0.000013981 mm3`, full-coverage collar sampling, seam delta `3.34e-13 mm`, connected first layers, zero prescribed-pose intersections, and positive-stop overlap `24.547567423 mm3`.
- Critic disposition: [CRITIQUE.md](./CRITIQUE.md) reports that the imported written STEP shows a straight OD40 silhouette, full-height diamond coverage including the collar, seam continuity, and the required two-part open-up layout, while leaving slicer/process and physical feel as pending.
- Reviewer visual spot-check agrees with the critic images and does not contradict the validator measurements.

## Final boundary

REV-R4-01 accepts the exact default R4 candidate `e56a117867e2cb0b77e706068636d56fb2adfa5e0eacf34fb2e7cd40897571cb` for scoped `CAD/source` and `written STEP` evidence only. It does not approve nondefault parameter combinations, broad generic-domain behavior, STL/3MF generation, slicer readiness, print readiness, or physical fit/performance.
