# Decision index

## Current surface pattern gate

[Surface pattern iteration](../iterations/2026-09-06-surface-pattern/) follows
the delivered drain count at `cf4adb0`. Existing Smooth/Diamond selection is
under review; Diamond must pass the new combined gates before enablement.
The accepted count source SHA is
`517f8546612ffecbc50a732362c9e3a326db03fa2c94e94a68daad472a0b42e2`.

## Preserved drain checkbox follow-up

[Drain checkbox iteration](../iterations/2026-09-06-drain-checkboxes/) extends
the editable SCAD drain mode to both ends and exposes independent Top/Bottom
checkboxes. Current development source SHA `cf0983e84e738be87e31462c903afcf02646915cc1e4a9e8641b8edce05b5393`;
private preview <https://mac-mini.duckbill-ionian.ts.net:8453/>. Bottom-only
default geometry is preserved byte-for-byte. Prior VFR-12/8448 and R7 STEP
records below remain preserved releases, not the current editable source hash.


## Preserved deployed pointer: VFR-12 OpenSCAD customizer

The selected current contract is the [OpenSCAD visual-fidelity recovery](../iterations/2026-09-04-openscad-visual-fidelity-recovery/). Its authoritative source is `openscad/laifen_case_customizer_v1.scad`, SHA-256 `ade77d3fcff4d5ba1c659838b4f9d24245584f0570834453b6e8c2b778047841`, and its preserved live review surface is <https://mac-mini.duckbill-ionian.ts.net:8448/openscad-simulator/>. VFR-12 C3 is the delivered smooth mobile UI; Diamond controls remain disabled pending browser recovery.

P2 R3 is preserved historical user-validation evidence. Its generic two-piece, mid-split control model and receipts remain under [P2 R3](../iterations/2026-09-03-p2-r3-control-sync-recovery/), but it is no longer the current pointer or a claimed live delivery surface.

P2 R19 is rejected prototype history, not a replacement pointer: candidate `566aa6bc8c0aa57f1aeea341805a48db7d54c2078a48cebc4f9204a685e2fc74` failed independent validation (48/84 class-specific rows) and critique. It has no formal-review or delivery decision. Any successor must redesign the semantic validation contract and obtain a small user teaching-gate PASS before renderer implementation.

## Preserved CAD pointer: P1 R7 editable smooth end chamfer

R7 remains the immutable Laifen CAD/STEP baseline: [BRIEF](../iterations/2026-09-03-p1-r7-end-chamfer/BRIEF.md), [DESIGN](../iterations/2026-09-03-p1-r7-end-chamfer/DESIGN.md), and [HANDOFF](../iterations/2026-09-03-p1-r7-end-chamfer/HANDOFF.md). `end_chamfer_size=1.20` mm, range 0.80–1.50, controls the true 45-degree circular end trim. Candidate `8d3941772cca549846937dcad6ce4a05e06f5bba104c261668a0cf747c62b6a1` passed formal CAD/STEP review. Slicing and physical acceptance remain pending.

## Preserved decisions

- DEC-01: measurement-preview contract; historical R1/R2 scope.
- DEC-02: actual dimensions and permitted bottom contact; pending physical evidence.
- DEC-03: thread-junction OD, root ligaments, and engagement; physical fit/strength remains open.
- DEC-04: texture registration; superseded for current R7 geometry by the shared-phase pattern contract.
- DEC-05: [preserve original width](0005-preserve-original-width.md); 30/31 mm bores remain the R7 contract.
- DEC-06: [generic cylinder generator with a full grippable skin](0006-generic-cylinder-continuous-skin.md); preserved early generator/design history, now advanced by the P2 R3 intent gate.
