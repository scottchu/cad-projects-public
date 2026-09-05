# P2 Foundation V1 implementation brief

**Owner:** `DES-GCS-FOUNDATION-01`  
**Status:** frozen implementation contract  
**Accepted gate:** exact user response `Yes pass` on 2026-09-04  
**Gate fingerprint:** `535ec0f9eb5bce77c409c12576ab4b9bdf2b66b930a6a477d22276f46d659dfa`

## Outcome

Build one small, real Three.js preview of the passed Foundation V1. It shows a smooth two-piece container with one common outside diameter, a split within the body, a screw closure, real hollow interiors, independent ends, an optional one-end drain, and assembled/exploded presentation. Pure math owns every derived value and returns the only descriptor accepted by scene construction.

This preview is conceptual, dimensionally proportional intent evidence. It is not CAD and makes no printability, thread-fit, strength, drainage-performance, export, or physical-acceptance claim.

## Requirements

| ID | Required result |
| --- | --- |
| `FV1-DERIVE` | Implement every passed input, equation, default, bound, conditional field, and invalid-state rule in the frozen Foundation V1 `DESIGN.md`. `deriveV1(state)` returns either `{valid:false, errors, descriptor:null}` or a complete finite serializable descriptor. |
| `FV1-BOUNDARY` | UI state is passed only to `deriveV1`; scene and readout modules accept the descriptor and never inspect, import, or rederive raw state. Invalid state clears model geometry. |
| `FV1-BODY` | Lower and upper are actual hollow indexed meshes, coaxial at assembly, split in the body, and equal in maximum outside diameter. Height, OD, wall, floor, split, section, and polygon side count change actual geometry. |
| `FV1-SCREW` | Actual mating helical surfaces visibly respond to pitch, turns, engagement, radial clearance, depth, and profile form while remaining within the common outside envelope. |
| `FV1-END-DRAIN` | Flat, chamfer, and rounded end choices alter their actual end meshes. Drain `none/top/bottom`, count, diameter, and bolt circle produce real through-floor holes only at the selected end. |
| `FV1-VIEW` | Assembled and exploded states are clear. Open-mouth and radial-cutaway inspection views expose cavity, floor/end thickness, thread engagement, and drains without substituting teaching cards or captions for geometry. |
| `FV1-UI` | One responsive desktop/mobile viewport, compact controls, derived-value readout, accessible labels, keyboard-operable view controls, validation errors, orbit, pan, zoom, reset, and camera fit to current bounds. |
| `FV1-SCOPE` | Smooth V1 only. No pattern, fade, label/text geometry, patch, attachment, bayonet, OpenSCAD, CAD, export, MakerWorld, service, or live-route work. |

## Exclusive namespaces

New implementation writes are limited to `preview/p2-foundation-v1/**`, the four prescribed `tests/test_p2_foundation_v1_*` files, `scratch/p2-foundation-v1-implementation/**`, and the implementation receipt/manifests named in `HANDOFF.md`. Existing R10 core is immutable reference input; do not import an old renderer. P2 R3 source and served bytes, P1 R7 CAD, quarantine contents, continuity history, package manifests, and all prior preview/test namespaces are read-only.

## Task DAG

| Task | Role and dependency | Done gate |
| --- | --- | --- |
| `IMP-GCS-FV1-01` | Implementer; starts from this fingerprint | Bounded source/tests complete, prescribed checks pass, candidate and evidence frozen. |
| `VAL-GCS-FV1-01` | Independent validator; after candidate freeze | Reproduce inputs/tests and verify math, mesh evidence, requirements, browser behavior, and namespace isolation; write `VALIDATION.md`. |
| `CRIT-GCS-FV1-01` | Independent visual critic; after candidate freeze | Inspect real desktop/mobile assembled, open, exploded, and cutaway screenshots; write `CRITIQUE.md`. |
| `REV-GCS-FV1-01` | Formal reviewer, distinct from IMP/VAL/CRIT; after both reports | Reconcile one exact candidate and issue PASS/BLOCK in `REVIEW.md`. |
| `DEL-GCS-FV1-01` | Separate delivery owner; after VAL, CRIT, and REV all PASS | An isolated route may be proposed; P2 R3 is never replaced. No promotion is part of this implementation task. |

One initial implementation plus at most two focused repair cycles is the ceiling. A changed frozen input, scope expansion, old-namespace write, descriptor bypass, or third repair stops the task and reopens design.
