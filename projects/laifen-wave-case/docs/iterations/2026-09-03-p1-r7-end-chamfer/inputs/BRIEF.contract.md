# R7 end-chamfer brief

**Task:** DES-R7-01 design-only contract. **Frozen baseline:** R7 `inputs/baseline.sha256`, SHA-256 `3faa73950171abe83253c9d521a6b3c037206559072baa354bd3181f012072c7`, which pins reviewed R6 source and STEP. R6 remains immutable.

The user authorizes one real, source-level editable smooth end chamfer in new `cad/p1_r7_end_chamfer/`. It applies at both closed outer ends only. It replaces R6's textured `bed_relief_radial` / `bed_relief_axial`; it is not a viewer-side control and it does not authorize a collar, seam, thread, bore, closure, drain, print, or measurement redesign.

Preserve the full R6 contract: 39 mm crest OD, body/cap bores 30/31, cavity 213 and outside length 219, original N=33/pitch=4.8/shared-phase diamond motif without Z scaling, 3 mm closed floors, seven diameter-3 drains per end, positive stop, native runout repair, datums, closed pose and print transforms. The narrow smooth outer-end treatment is the only skin exception. No new coupon, short version, or physical-measurement gate is required.

Implementation and validation must keep CAD/source, written STEP, slicer, and physical acceptance separate. No STEP, mesh, slicer, printer, service, Git, status-index, or environment work belongs to this design task.
