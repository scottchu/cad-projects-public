# P17 R2 fixed stepped-axle guide validation

Status: `P17-V05` pass for exact candidate fingerprint
`b4ad7e49b198c189c5a32fdeecef7cf231b0306ef26d2404ae662711b22ff5b5`.

## Validator gate `P17-V05`

Owner: `/root/p17_validator`, distinct from design, implementation, critique,
and formal review.

Independent evidence completed:

- frozen fingerprint, provenance, manifest, source, test, and pre-receipt
  HANDOFF hashes matched;
- focused regressions: `8 passed`; full focused file: `31 passed`;
- all ten written STEP exports: `ok:true`, `failureCount:0`;
- all ten STEP hashes, four motion source/sidecar hashes, eleven PNG hashes,
  and two GIF hashes matched provenance;
- source/export topology, occurrence, and bounds parity passed;
- 66 side/state closure rows had rank 3, maximum residual
  `3.43e-15 mm`, and maximum perturbed pose error `7.31e-12`;
- all 33-state axle/outer, keeper/outer, axle/white-rod, keeper/cap, and
  XT60/service unintended-intersection gates were clear;
- fixed purple axle/keepers/inners, opposite outer rotation, all three moving
  white rods, filled `C`, and no added structure were verified in source,
  sidecars, PNGs, and GIF frame extracts;
- focused motion transforms only the outer plates; full motion also shows the
  three rods and caps moving on their frozen paths.

This is digital CAD/export validation only. A sidecar animation, a clean
snapshot, and nominal pin/slot clearance do not prove physical revolute
constraint. Physical fit, friction, force, heat, wear, keeper retention,
self-lock, wire retention, solder ergonomics, slicer/3MF, and durability remain
pending.
