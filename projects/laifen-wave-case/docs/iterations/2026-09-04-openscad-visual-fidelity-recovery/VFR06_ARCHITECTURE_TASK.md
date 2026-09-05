# VFR-06 architecture arbitration task

Status: ready after `inputs/VFR06_ARCH_INPUTS.sha256` is frozen.

Task ID: VFR-06. Owner role: independent architecture arbiter. Project:
`projects/laifen-wave-case`. Iteration:
`2026-09-04-openscad-visual-fidelity-recovery`. Baseline is the restored
OpenSCAD source named in the input manifest. The recorded user choice B is
immutable.

## Objective and done gate

Decide whether a new source-feasible mathematical representation can preserve
the exact B exterior while producing a conforming manifold short band and full
body/cap within the existing browser OpenSCAD limits. The decision must either:

1. select one complete architecture with explicit numeric indexing,
   triangulation, boundary-conformity, direct-shell connection, and cheap
   preflight proofs sufficient for a separate implementer; or
2. declare the editable browser OpenSCAD diamond path blocked under the current
   0.025 mm exterior-error and 60-second full-part contracts, with a precise
   explanation of which contract cannot presently be met.

Evaluate a globally structured, conforming lattice or equivalent deterministic
representation that avoids both whole-mesh search and dynamically inconsistent
local patch boundaries. Explain how arbitrary finite axial endpoints, the
body/cap seam, circumferential wrap, chamfer intersections, shoulder/rim
connections, and internal 96-sided rings share vertices exactly. Provide
closed-form index formulas and a bounded short-band proof before proposing full
implementation. Reconcile the successful VFR-04R G2 evidence with its full-body
timeout and the fast but nonmanifold VFR-05A evidence.

## Scope and limits

Read only the manifest-listed inputs and repository policy files. The sole
write is `VFR06_ARCHITECTURE_DECISION.md`. Do not edit source, tests, artifacts,
browser/UI files, services, continuity files, or prior receipts. Do not run a
full implementation or generate candidate body/cap files.

Preserve: separate body/cap roles; N33 at valley radius; plateau half-fraction
0.18; shared seam-centered phase; pattern to both sides of seam; OD 39 mm;
bores 30/31 mm; existing thread, drain, chamfer, dimensions and smooth branch;
native OpenSCAD geometry authority; error <=0.025 mm; body/cap browser-worker
generation <=60 seconds each; exterior triangle cap <=250000. Do not relax a
threshold, extend a timeout, import a host-generated mesh, or silently change
the approved B relationship.

Use the least speculative design that closes every known topology and
performance gap. Distinguish a proof from an estimate. Include explicit stop
conditions and a one-attempt plus one-focused-repair ceiling for any subsequent
implementation.
