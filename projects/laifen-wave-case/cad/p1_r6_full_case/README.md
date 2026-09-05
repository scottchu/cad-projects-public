# P1 R6 full 39 mm Laifen case

Original full-length body and C25 screw cap, adapted from our frozen R5 parametric source. The approximate device inputs are `device_length=208` and `device_diameter=29`; accepted axial allowance is5 and selected cap cavity81. These derive closed usable cavity213, cap height84, body depth132 and outside length219. They are editable inputs, not hardware measurements. `cavity_length` and `cap_height` are derived properties; no independently editable copies exist. Device diameter changes only the reference envelope and radial-gap readouts, preserving body/cap bores30/31.

The exterior has a common39mm crest envelope, original N33 diamonds at4.8mm axial pitch,0.45mm relief and common zero phase. Additional length adds rows without scaling. Both outer closed ends have the textured0.30radial/0.50axial bevel. Every3mm floor has seven diameter3 holes: one center and six on radius9. The holes permit unobstructed water passage; loaded-device and flat-table drainage remain unproven. No recessed center glyph crosses the drain; C25 is identified by source/artifact labels.

The unchanged R5 B thread has male root16.4/crest16.9, pitch2, effective engagement6, tip9 and radial clearance0.25 with0.30 budget. Its1.4mm male root wall is an untested strength assumption. Female wall is1.90 at C25,1.85 at budget C30. New thread fit/strength are not inherited from old printed coupons. Collar-end10.2 and straight-bore start12.4 use independent taper length2.2. The external positive stop acts atZ0 and the shared textured seam; no device stop or retention is added. Straight texture-valley walls4.05/3.55 are derived from the exterior and fixed bores; the old noncontrolling nominal wall input has been removed.

`params.py` owns inputs and derivation; `skin.py` owns our original field; `surface.py` retains rational circle/Bezier patches, canonical shared edges and noncircular planar closures; `thread_profile.py` retains the original R5 thread construction family; `parts.py` builds the case, native datums, screw relationship and print poses. `runout.py` corrects one tolerance-covered native trim endpoint shared by the female upper helical flank and its runout cone. It projects the existing vertex onto the existing curve and shortens its trim range, preserving surfaces, vertex coordinates and tolerance. The geometric role selector uses the neck-height/crest-radius datum, with no face index. An isolated topology copy prevents mutation of cached thread tools. No downloaded geometry is used. Scalar parameter feasibility is separate from default-only CAD acceptance.

The four primary source/output pairs are:

- `body.step.py` / `body.step`: one body,Z[-135,9], height144.
- `cap_c25.step.py` / `cap_c25.step`: one cap,Z[0,84], height84.
- `closed_c25.step.py` / `closed_c25.step`: exactly two case parts, cavity213 and outside219. Physical overlap9 differs from effective thread engagement6. Screw gap=pitch*angle/360.
- `print_layout.step.py` / `print_layout.step`: exactly one body at(+23,0,135) and one cap at(-23,0,84) afterRx180; both openings up. Nominal layout85x39x144, crest-envelope spacing7.

`review.py` is nonfabrication source. `device_readouts()` supplies dimensions, device-end datums and warnings. `device_envelope()` makes the approximate diameter29/length208 cylinder with named lower/upper joints. Centered nominal endpoints are-129.5/78.5 and gaps2.5/2.5; bottom-resting comparison is-132/76 with gaps0/5. This is nominal placement, not retention. `section_review(case_parts=(body,cap))` can use the exact imported primary solids to produce a diagnostic half-case and labelled envelope. This helper is excluded from all four primary targets and has no fifth fabrication wrapper. A critic can annotate the actual STEP section using the same source readouts.

Run from repository root with its uv Python3.12 environment:

```sh
uv run pytest projects/laifen-wave-case/tests/test_full_case.py -q -k 'not written'
uv run python projects/laifen-wave-case/cad/p1_r6_full_case/generate.py
uv run pytest projects/laifen-wave-case/tests/test_full_case.py -q
```

`generate.py` invokes the installed CAD launcher against exactly these sources, each with `--write`:

```sh
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/gen projects/laifen-wave-case/cad/p1_r6_full_case/body.step.py --write
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/gen projects/laifen-wave-case/cad/p1_r6_full_case/cap_c25.step.py --write
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/gen projects/laifen-wave-case/cad/p1_r6_full_case/closed_c25.step.py --write
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/gen projects/laifen-wave-case/cad/p1_r6_full_case/print_layout.step.py --write
```

Use the wrapper for enforced target/global process timeouts. It allows600s per target and1800s total, logs each target's completion and stops the owned process group on timeout. Source guards allow600s per outer/Boolean stage,16000 exterior faces per part and26000 combined. Both polygon counts are checked before BREP allocation. Sewing tolerance and rational accuracy are unchanged; no per-diamond Boolean or coarse substitute is used.

Frozen contract and implementation evidence are in `docs/iterations/2026-09-02-p1-r6-full-case/`. Independent critic, validator and formal reviewer establish source/CAD and written-STEP status. Slicer/process, physical thread/loaded fit, exact installed dimensions and literal both-end noncontact remain separate open evidence. The user's direct-full instruction supersedes the short-first route; it does not prove physical fit or introduce retention.

For the focused native-runout repair, the bounded scratch production driver invokes only the three cap-containing `gen --write` commands above; `body.step` remains byte-identical to the frozen full candidate. The defect regression uses the actual raw female thread tool, and the cap parity regression compares adaptive source/written volume at `eps=1e-10` against the unchanged `0.001 mm³` gate. Repair provenance and exact regeneration timings are recorded in `IMPLEMENTATION_REPAIR.md` in the active iteration.
