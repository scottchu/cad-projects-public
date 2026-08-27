# P20-SCAFFOLD-REVIEW-01 formal scaffold conformance review

Date: `2026-08-26`

## Formal verdict and boundary

**ACCEPT — the exact focused-repair-1 artifact conforms to the frozen P20
evidence-only, intentionally colliding sequential-scaffold contract.** This
acceptance is limited to scaffold conformance and truthful evidence delivery.
It is not mechanism, product, CAD-candidate, print, manufacturability, force,
fit, or physical acceptance.

The accepted scaffold candidate is exactly the manifest file with SHA-256
`59ad1459f3abcdbb3a8771f3fa10ad461471594d47dbb723781ea3597f9395c9`.
Its nested frozen input-manifest SHA-256 is
`74fe83b49142ff43ce9a356825d8078c27e065bd5123f6cc446f5be00bcbadd6`.
The candidate verified `20/20`, and the nested input verified `18/18`, before
this join. No candidate, source, test, STEP, sidecar, or review-medium file was
changed by the formal reviewer.

## Independent-role and receipt join

- Designer: `/root/p20_mechanism_design`.
- Design critic: `/root/p20_design_critic`.
- Scaffold implementer: `/root/p20_scaffold_implementer`.
- Scaffold critic: `/root/p20_scaffold_critic`.
- Scaffold validator: `/root/p20_scaffold_validator`.
- Formal scaffold reviewer: `/root/p20_scaffold_reviewer`.

These are distinct role owners. The scaffold critic identity is now explicit
in the durable recheck receipt; it was not inferred from implementation or
validation work.

The joined receipts are:

| Receipt | SHA-256 | Disposition |
|---|---|---|
| `SCAFFOLD_IMPLEMENTATION.md` | `b14be60cb9999738168f59f5c80642c36b8cb1ceee6ddcce1e8e1777189b7c36` | Matching replacement candidate; implementation only, not self-approval. |
| `SCAFFOLD_CRITIQUE.md` | `994f38fbfa5c6fc5b27029055c175ce95e56f098e5dec2c4cd08d3c88d40d203` | Preserved blocking critique that opened `SC-01` through `SC-03`; pinned by the replacement candidate. |
| `SCAFFOLD_CRITIQUE_RECHECK.md` | `6531dea20ed5d4d744259f5c6a4c8896d2c0ec929ff47395a5757f0282d10819` | Independent PASS for exact replacement candidate; all three findings resolved. |
| `SCAFFOLD_VALIDATION_RECHECK.md` | `73312ac348745ce6a1a513283e752094bc826f1effcda028961f43d3b23a10b0` | Independent PASS for exact replacement candidate. |

The older `SCAFFOLD_VALIDATION.md` is historical evidence for superseded
candidate-manifest SHA-256 `2f5c68e65a96ee3ef1d32150e283a23b06a3854905883180935f3540af60f903`.
It is deliberately excluded from this formal acceptance basis.

## Frozen-contract traceability

| Contract gate | Formal disposition |
|---|---|
| Start from exact P19 R1 baseline and frozen inputs | **PASS.** Candidate and nested manifests verify exactly; no input drift is reported by either independent recheck. |
| Fixed axle farther lower-left | **PASS.** Source, tests, STEP evidence, sidecar, critic and validator agree on `A=(Y=-15.00,Z=-11.00) mm`. |
| Centered-equivalent fixed guide | **PASS.** `T_s(q,u)=A+R(alpha_s(u))q`; the fixed axle remains local `(0,0)` on both sides at every checked state, and each outer plate has one centered round `OD7.90 mm` journal. |
| Required travel | **PASS.** Left/right endpoints are `-45/+45 deg`, giving exactly `90 deg` relative END travel. |
| Zero outer rod rails and zero substitute apertures | **PASS.** Both outer solids are each one complete P19-diameter disk minus only the centered axle journal. No rod slot, hole, window, pocket, bore, or other rod cutter is present. |
| Preserve three fixed-inner paths per side | **PASS.** Both inner plates retain the delegated P19 three-straight-closed-track geometry. |
| Preserve rods, caps, stack, workpiece and service evidence | **PASS.** Three `OD4 x 50 mm` rods and six caps retain their P19 identities/world paths; static OPEN/mid/END entries each restore the service occurrence and have `19` top-level / `22` leaf occurrences. |
| Truthfully expose expected collisions | **PASS.** All six named OPEN rod/solid-outer-plate intersections remain present at approximately `40.212385966 mm3` each, totaling `241.2743157956962 mm3`; they are not suppressed or treated as valid clearance. |
| No unexpected sampled-state collision | **PASS.** The fail-closed collision authority and independent rechecks report empty unexpected production and service maps at OPEN, mid and END; preserved P19 reference contacts are classified separately. |
| Explicit non-candidate media | **PASS.** Transparent static views and the annotated contact sheet state that rods pass through solid plate volume, the circles are not holes, and the packet is static collision evidence rather than valid motion. |
| Sequential STOP boundary | **PASS.** No outer rail was added, no future rail order was selected, and no 3MF, STL, slicing, printing, clearance feature, optimization, or physical claim appears in the accepted scaffold namespace. |

## Prior-finding disposition

- `SC-01` — **RESOLVED.** The unchanged P19 service-envelope compound is
  restored in each static state, with source/written-STEP occurrence and label
  parity covered by the replacement tests and both independent rechecks.
- `SC-02` — **RESOLVED.** Opaque motion-like delivery media were superseded by
  transparent static collision views and an in-frame annotated contact sheet
  that explicitly denies holes and valid motion.
- `SC-03` — **RESOLVED.** A BREP common-operation failure now raises
  `CollisionEvaluationError` with the original exception chained; unknown
  collision state can no longer become a false `0 mm3` result.

No unresolved material critique or validation finding remains for scaffold
conformance.

## Review method and evidence layers

The formal reviewer independently verified the exact manifest and receipt
hashes, all `20/20` candidate entries, all `18/18` nested frozen inputs, the
distinct durable role ownership, source/test/sidecar wording and topology
gates, candidate artifact inventory, absence of future-order/print artifacts,
and the transparent axial view plus annotated contact sheet. The reviewer did
not regenerate artifacts, rerun validation as a second validator, or modify
the candidate.

Evidence layers remain separate:

- **Scaffold contract/provenance:** accepted for this exact fingerprint.
- **Source and written STEP scaffold evidence:** independently validated for
  the intentionally colliding construction state.
- **Mechanism/product CAD acceptance:** not claimed; the scaffold is not a
  valid movable mechanism.
- **Slicer/print/manufacturing acceptance:** not performed or claimed.
- **Physical fit, torque, force and durability acceptance:** not performed or
  claimed.

## Remaining risks and mandatory STOP

The six rod/solid-outer-plate collisions are deliberate and make this scaffold
non-movable and non-manufacturable as a finished product. Torque, mechanical
advantage, force, fit, friction, backlash, heat, material strength, wear,
retention, service ergonomics and every physical outcome remain unknown.

**STOP here.** Do not add a rail, choose a rail order, add clearance geometry,
optimize, slice, print, or promote this evidence to product acceptance. If the
user separately authorizes the next step, open a new one-factor-at-a-time
contract for exactly one named outer rail with a new immutable input/candidate
fingerprint. That future gate must check the named outer rail against its
corresponding inner path and every already-frozen neighboring outer rail, and
must roll back only that attempted rail if it fails.
