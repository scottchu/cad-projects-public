# P20 R2 fixed-rod curved-rail handoff

Date: `2026-08-26`

## Status

The user approved the complete P19-based P20 R2 assembly's fixed purple rod
and both curved fixed-rod rails. Those elements are now immutable and may not
be touched by the next wire-only task. The inherited P19 diagonal wire is
separately **USER-REJECTED** and is the only next design subject.

## Provenance

- Branch: `codex/xt60-p20-r1-fixed-rod-reset`.
- Contract-opening clean HEAD:
  `a48c5697f9126dbb6934d764e48f2a01f6a01475`.
- Product baseline: P19 R1
  `b69b6ad12af611644987f026eef4940db9c7bb34`.
- Frozen contract: `TASK_INPUT.md`, `BRIEF.md`, and
  `DESIGN_INPUT_MANIFEST.sha256` in this iteration.
- Repaired design candidate file SHA-256:
  `c3aaa10589408db6d24fcde9b46ed89f8cbd95e41764c4a4db0672cbd3fd2c30`
  (`5/5`).
- Independent focused recheck SHA-256:
  `f737c6c075c726500ae7c251c4dcef84c6726b2b5700dae46939e7778cebcb3b`.
- Implementation input manifest SHA-256:
  `acec208df5f1de3abcc9b245c51c6161f099363517f92616852c146677fcfb26`
  (`36/36`).
- P20 R1 source/docs/artifacts remain untouched rejected history.

## Corrected invariant

Outer plates rotate about P19 virtual center `C=(0,0)`, not about the fixed
axle. The fixed axle remains world-stationary at candidate `A=(-15,-11)` while
the physical left/right outer plates counter-rotate `+45/-45 deg`. Therefore each outer plate needs
a true curved local fixed-axle rail
`q_s(u)=C+R(-alpha_s(u))(A-C)` whose forward reconstruction is always `A`.
The round journal in the rejected P20 R1 scaffold is explicitly forbidden.

Frozen user-approved evidence:

- source SHA-256:
  `1b004ac07fbd3f8ff2f776b3219c5b98e50825b123e1ec3410683d61134baa73`;
- focused fixed-rail STEP SHA-256:
  `07c398b9b01233150dc4ca0805e2a7e2980f60fff302e1442654e0c3fb3f8f2c`;
- complete P19-based assembly STEP SHA-256:
  `715851b434ab2e17a7f6c29be0b21924fb99ed6e28c20be8b276399a5d1d6bca`;
- `C=(0,0)`, `A=(-15,-11)`, physical left/right `+45/-45 deg`;
- `qL(0)=qR(0)=(-15,-11)`;
- `qL(1)=(-18.384776310850235,+2.828427124746188)`;
- `qR(1)=(-2.828427124746192,-18.384776310850235)`;
- two curved fixed-axle rails at `7.90 mm`; and
- zero white-rod outer rails or substitute apertures.

## Exact bounded scope

- Zero white-rod outer rails and zero substitutes.
- All three white-rod inner rails retained in both inner plates.
- Exactly two curved fixed-axle rails, one per outer plate.
- Six rod/solid-outer-plate collisions retained as known non-product evidence.
- No rail sequence choice, next rail, mesh, 3MF, slice, print, or physical
  acceptance.

## Next action

Open a new wire-only correction from the exact source and complete-assembly
hashes above. Replace the inherited diagonal wire reference with the
already-established exact 90-degree topology: exactly vertical leg, tangent
`R6` quarter arc, and tangent horizontal leg. Add a regression against
`REQ-002` and `REQ-017`. Never touch the purple fixed rod, either curved
fixed-rod rail, their paths/cutters, `C`, `A`, motion signs, or zero outer-rail
count. Stop and return if the wire correction would require any such change.

## Acceptance split

- **USER-APPROVED:** fixed purple rod presence and position; both curved
  fixed-rod rail paths and visible apertures; their presence in the complete
  P19-based P20 R2 assembly.
- **USER-REJECTED:** the inherited P19 END-derived diagonal wire reference.
- **NOT CLAIMED:** complete product function, collision-free motion,
  manufacturing, mesh/3MF, slicing, printing, force/torque, fit, or physical
  acceptance.

The wire defect escaped because P19 `build_workpiece_reference()` and its tests
encoded the same END-derived diagonal assumption. That local agreement masked
their contradiction with core `REQ-002` and `REQ-017`, which require a fixed
90-degree bend.

## P20R2-DESIGN-01 receipt

- Status: **PASS analytic design; no implementation authority**.
- Candidate-manifest SHA-256:
  `c3aaa10589408db6d24fcde9b46ed89f8cbd95e41764c4a4db0672cbd3fd2c30`
  (`5/5` entries verified), superseding
  `c38fe2158b150efa946f92a6d110b56be2806a1c4dd7d933f8b50666c2a2860f`.
- Repair input: immutable critique SHA-256
  `43c98d108c1713e2efd54172fe275b3dafb7d74fa17421b1d170244368794b21`.
- Input manifest: `20/20` entries verified; manifest SHA-256
  `07847a8fec788ece8c9f421225ca1301810cf619713904a7da867dfcc6674a55`.
- Geometry: radius `18.601075238 mm`, each 45-degree centerline arc
  `14.609250329 mm`, cutter width `7.90 mm`, 33 samples, maximum segment
  sagitta `0.001400627 mm`.
- Minimum exact rim web: left outer `4.798925 mm`; right outer
  `4.948925 mm`; moved inner AF8.15 hex `3.893520 mm`.
- Interactions: conservative fixed-rail clearance from any white rod
  `>18.469 mm` and any retained inner path `>18.394 mm`; left/right apertures
  are in disjoint outer-plate X intervals.
- Required boundary: white-rod outer rails/apertures remain exactly zero and
  all six expected rod/solid-outer collisions remain.
- Approved sign correction: physical left outer `+45 deg`, physical right
  outer `-45 deg`, and inverse local rails turning in the opposite direction.
- Changed paths: `DESIGN.md`, `DESIGN_CANDIDATE.sha256`, this design section,
  and deterministic SVG/PNG gate under
  `docs/review/p20-r2-fixed-rod-arc-rail/`.
- Unresolved risks: exact BREP validity, true solid collision census, STEP
  parity and physical force/friction remain downstream gates.

## P20R2-CRIT-01 focused design-repair recheck receipt

- Status: **PASS exact repaired analytic design; source implementation may
  begin under the separately frozen implementation manifest**.
- Rechecked design candidate file SHA-256:
  `c3aaa10589408db6d24fcde9b46ed89f8cbd95e41764c4a4db0672cbd3fd2c30`.
- Recheck report SHA-256:
  `f737c6c075c726500ae7c251c4dcef84c6726b2b5700dae46939e7778cebcb3b`.
- Verified: `5/5` repaired design entries and nested `20/20` design-input
  entries; correct side-specific MID coordinates and direction arrows;
  prior sign review is superseded by the approved corrected gate; `3` retained inner rails per plate, `6` total; both
  complete curved fixed-rod rail bodies visible; zero white-rod outer rails.
- Scope: analytic design and phone-gate traceability only. No source, BREP,
  STEP, manufacturing, printing, force, torque, or physical approval.
