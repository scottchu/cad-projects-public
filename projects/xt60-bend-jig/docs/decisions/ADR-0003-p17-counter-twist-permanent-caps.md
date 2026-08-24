# ADR-0003: P17 counter-twist permanent-caps simulator architecture

- Status: accepted for simulator-first design contract
- Date: `2026-08-23`
- Supersedes: conflicting P17 portions of `ADR-0001`
- Superseded by:

## Context

The physical P13 assembly and user review exposed architecture-level conflicts, not a manufacturing cut error. Six rod-end caps are now mandatory permanent features. Four printed caps fit nominal rods while two were too tight, so cap fit remains process-variable. The user also requires two fixed grounded inner plates and two larger user-gripped outer plates that rotate in opposite directions. P13's shared D-shaft keys both rotating plates to the same direction and cannot satisfy that requirement.

P13's visible `LOCKED` pose is not proof of a lock. P17 must state a real ground/reaction path and a lock concept while keeping physical force and self-lock proof pending.

## Alternatives considered

1. Preserve P13 four-plate/three-rod same-direction shared-shaft architecture. Rejected for P17 because it contradicts required outer-plate counter-rotation and permanent-cap service assumptions.
2. Keep P13 geometry and reverse the right plate animation sign. Rejected because it does not create complementary tracks or a mechanical relationship that keeps both ends of every rod coincident.
3. Redesign directly in CAD. Rejected for this iteration because simulator motion review is the required next gate.
4. Use a fixed inner guide frame plus two counter-rotating gripped outer plates tied by a 1:1 opposite-rotation relationship. Selected as the smallest falsifiable simulator architecture.

## Decision

P17 uses a simulator-first counter-twist architecture:

- two fixed inner guide plates are grounded and do not rotate;
- two outer plates are user-gripped rotating elements;
- the primary outer plate is slightly larger than the other outer plate, and both are larger than the inner plates;
- one relative twist input drives opposite global rotations, `alpha_left = -theta_rel / 2` and `alpha_right = +theta_rel / 2`;
- left and right outer slot centerlines are complementary paths generated from their own signed rotations;
- all six rod-end caps are permanent;
- the lock concept is a grounded detent/hard stop on the primary outer plate, with the held state transmitted to the secondary outer plate through the required 1:1 opposite-rotation relationship.

## Consequences

P17 supersedes these P13 assumptions for future P17 work:

- one shared same-direction D-shaft as the actuator relationship;
- synchronized cams that rotate together in the same global direction;
- removable right caps or service cap language;
- treating a final pose label as lock proof;
- accepting P13's wide inner span as the current architecture.

P13 remains historical evidence and may remain digitally accepted for its own release state, but it is not the governing architecture for P17. P17 has simulator-only acceptance until implementation, independent validation, independent review, and user motion review occur. CAD, artifact/slicer, and physical acceptance remain pending.

## Evidence

- `docs/iterations/p17-r1-counter-twist-permanent-caps/BRIEF.md`
- `docs/iterations/p17-r1-counter-twist-permanent-caps/DESIGN.md`
- `docs/REQUIREMENTS.md`
- `docs/EXPERIENCE.md`
- Supplied photos:
  - `/tmp/codex-remote-attachments/01a02c54-c344-75f0-a983-e2e2dd8162a7/B931B501-4470-4E89-82E8-BD46F0E51353/1-Photo-1.jpg`
  - `/tmp/codex-remote-attachments/01a02c54-c344-75f0-a983-e2e2dd8162a7/B931B501-4470-4E89-82E8-BD46F0E51353/2-Photo-2.jpg`
  - `/tmp/codex-remote-attachments/01a02c54-c344-75f0-a983-e2e2dd8162a7/B931B501-4470-4E89-82E8-BD46F0E51353/3-Photo-3.jpg`
