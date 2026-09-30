# J-L Laifen live-demo evidence and handoff

Status: complete, 2026-09-03. Owner `/root/journey_simulation` artifact/demo role. Project root `L=/Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case`. Read applicable AGENTS, current state/next-agent, requirements, R6/R7 handoffs, observation records and actual HTML/parameters. Used cad-viewer skill to identify existing URLs; started no server, generator, slicer or device action. Frozen source/artifact list is LAIFEN.sha256; mutable status/observation copies under `/tmp/cad-journey-laifen/frozen/` capture the audit boundary.

## What exists and what is accepted

R6 repaired full case is the last independently reviewed default CAD/source and written-STEP baseline. Source `L/cad/p1_r6_full_case/`; use `print_layout.step` for two separate parts and `closed_c25.step` for assembly. R6 original procedural diamond texture, OD39, bores30/31, nominal L208/D29, total allowance5, usable cavity213, outside219, body144/cap84, overlap9/effective thread6. `params.py` exposes device_length/device_diameter/axial_allowance, but demo does not edit or regenerate it. Exact source/STEP acceptance does not include slicing, physical fit, support behavior or strength.

User explicitly declined another short-first version and requested full-size delivery. Preserve that choice. R7 is active for an editable smooth end chamfer after the user observed R6's scalloped end; its namespace remains outside demo scope. Do not represent R7 as reviewed or launch its source. Historical root REQUIREMENTS still contains earlier measurement/coupon gate scope; R6's explicit later direction supersedes short-first sequencing.

## Actual observations available

`docs/observations/2026-09-02-coupon-fit/README.md`: user reported all three printed screw closures good by hand. `photo-1.jpg`, visually inspected, shows one male specimen and three cap specimens. Exact print-source revision/profile, measured torque/wobble and five-cycle evidence remain unknown; do not call this R6 physical acceptance. User dislikes the bulged collar and requests uniform diameter/full sidewall pattern.

`docs/observations/2026-09-02-length-and-case-reference/README.md`: ruler view is user-confirmed centimetres, visually near20.8cm but zero datum/perspective prevent exact length. User accepted5mm total allowance and39mm outside diameter. Exact loaded envelope/head cover and whether bottom-resting contact is acceptable remain unresolved. The reference photos are not measured CAD or fit proof.

## Recommended 90-second demonstration

1. Show actual R6 two-part layout and closed-case image. State the current question: does the nominal extra length imply the brush avoids both ends?
2. Open the existing earlier clearance study `L/preview/measurement-gate.html` in a presentation-local HTML host. Label it **“Earlier clearance study — nominal envelope, not R6 CAD controls”**. Keep L208, D29, allowance5. Its geometry predates R6: lower neck137/upper mouth132/pending overlap5, so do not teach those old joint dimensions as current R6.
3. Click **置中** (`data-preset=0.5`): q0.5 yields lower2.5/upper2.5mm and “未固定：僅示意位置” (unrestrained; illustrative position). Click **靠底** (`data-preset=0`): lower0/upper5 and explicit bottom contact. Restore centered if desired. These browser-only controls were rehearsed successfully.
4. Show the actual repaired R6 section. It similarly labels the golden cylinder nominal, centered and unretained. Conclude: a clearance calculation does not create restraint. The shared model has identified an unanswered acceptance condition before another CAD change.
5. Name the next decision and evidence without forcing a test: confirm whether bottom support is acceptable; verify installed envelope and eventual loaded full-case closure/contact. The user has already selected full-size progression. Those physical questions remain pending; this demo does not order another coupon or start a print.

The HTML also exposes L/D/slack fields (step0.1) and q0..1 (step.01). C=L+slack, top=(1−q)slack, bottom=q·slack; bores stay30/31 when D changes, so radial readouts change. No physical dynamics, restraint or CAD generation. Use q only for a short predictable presentation.

## Assets and fallback

All following actual R6 images were viewed:

- `L/scratch/fullcase-critique/repair/print-layout-open-up_20260903T033441Z.png`: best opening visual, two open parts with visible threads.
- `L/scratch/fullcase-critique/repair/closed-long-shaded_20260903T033014Z.png`: complete closed silhouette.
- `L/scratch/fullcase-critique/repair/section-dimensions.png`: actual repaired STEP section with nominal reference and dimensional/acceptance labels.
- `L/docs/observations/2026-09-02-coupon-fit/photo-1.jpg`: actual earlier physical specimens, separately captioned.

Rehearsal captures: `/tmp/cad-journey-laifen/gate-centered.png` and `gate-bottom.png`; bottom visually inspected. Original fragment needs host variables, so capture supplied only foreground/muted/blue CSS variables and page font/padding in the transient browser. Source HTML and calculations were unchanged. Do not call screenshot styling the original chat host. Fallback is these two screenshots followed by the actual R6 section. Writer may wrap the exact fragment in its presentation-local host with explicit historical caption.

## Existing links, checked now

HEAD checks returned200 at11:35:58UTC on2026-09-03:

- https://mac-mini.duckbill-ionian.ts.net:8448/laifen-full
- https://mac-mini.duckbill-ionian.ts.net:8448/laifen-full-section
- https://mac-mini.duckbill-ionian.ts.net:8449/Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case/cad?file=p1_r6_full_case/closed_c25.step

GET copies of the two PNG routes are `/tmp/cad-journey-laifen/full-live.png` and `section-live.png`; byte hashes equal the frozen source images. Viewer page200 alone is not a freshly verified3D-ready state; prior R6 readiness receipt records rendered-ready. Prefer rehearsed local HTML/images for the live sequence; use existing viewer optionally for orbiting the frozen R6. No production-serving/routes changed.

## Receipt and remaining limits

Read/search commands: explicit `/opt/homebrew/bin/rg`, `cat`, `sed`; requests `curl -I --max-time10` and read-only PNG GET. Browser script `/tmp/cad-journey-laifen/capture.mjs` ran using Node26.7.0 and existing inspected CDP helper; exit0, two q states captured in `gate-receipt.json`, external HTTP(S) blocked. SHA256 verified R6 STEP against HANDOFF: closed `31e4125fcfc6d6c543312491298d8a508f0d2db9a5da247b6a933b6fa7d3efa6`, layout `be27b1c7962bcc241babea257aa85b11bc1675b83072f475bf684e865d166410`. Captured sources are evidence, not a new implementation/validation approval. Next writer copies the exact chosen HTML/images into deck assets and final validator checks links/fallback behavior. Physical acceptance and active R7 remain separate.
