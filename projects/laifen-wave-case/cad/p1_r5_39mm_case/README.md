# P1 R5 original 39 mm short case

This new candidate adapts our R4 rational diamond generator. It has a common39mm crest envelope, N33 repeats,4.8mm axial pitch,0.45mm skin height and shared zero phases. Changing short length changes the field domain, never its proportions. Textured0.30mm radial by0.50mm axial closed-end bevels preserve the full motif amplitude. Each3mm floor has a center hole and six holes on radius9, all diameter3. The previous recessed clearance glyph is omitted because of the center hole; C25 remains in source/artifact labels. The holes permit unobstructed passage; loaded-device and flat-table drainage are unproven.

The selected thread B is intentionally new: male root16.4/crest16.9, pitch2, effective engagement6, radial gap0.25 and budget0.30. The male root wall is1.4, an untested strength assumption. Minimum female wall is1.90 at C25,1.85 at budget C30. New thread flank slope changes nominal axial freedom; R3/R4 fit and strength do not transfer. Bores30/31, shoulderZ0, tip9, collar-end10.2 and taper-end12.4 remain. The2.2mm cap taper is an independent named parameter, avoiding radial-size drift. Guaranteed stop extends to texture-valley radius19.05.

Source modules: `params.py` owns dimensions and early guards; `skin.py` owns the original field; `surface.py` retains rational circle/Bezier patches, canonical shared edges and actual noncircular planar closures; `thread_profile.py` constructs the new profile using our original thread family; `parts.py` builds the floors/drains, native joints, assembly and print poses. No downloaded mesh is used. Short limits remain6000 exterior faces per part and180s each outer and Boolean stage; scalar feasibility is not broad nondefault CAD acceptance.

Default targets and poses:

- `body.step.py` / `body.step`: bodyZ[-35.1,9], one solid.
- `cap_c25.step.py` / `cap_c25.step`: capZ[0,43.4], one solid.
- `closed_c25.step.py` / `closed_c25.step`: two source-jointed parts, cavity72.5 and closed length78.5. Screw gap=pitch*angle/360.
- `print_layout.step.py` / `print_layout.step`: one body at(+23,0,35.1) and one cap at(-23,0,43.4) afterRx180. Both openings up; nominal85x39x44.1 envelope.

Run from repository root, using its uv Python3.12 environment:

```sh
uv run pytest projects/laifen-wave-case/tests/test_case39.py -q -k 'not written'
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/gen projects/laifen-wave-case/cad/p1_r5_39mm_case/body.step.py projects/laifen-wave-case/cad/p1_r5_39mm_case/cap_c25.step.py projects/laifen-wave-case/cad/p1_r5_39mm_case/closed_c25.step.py projects/laifen-wave-case/cad/p1_r5_39mm_case/print_layout.step.py --write
uv run pytest projects/laifen-wave-case/tests/test_case39.py -q
```

Frozen design and implementation receipts/manifests live in `docs/iterations/2026-09-02-p1-r5-39mm-case/`. Source/CAD and written STEP require independent critique, validation and formal review. Slicer/process and physical acceptance remain separate and pending. This short experiment does not establish full Laifen length, end contact, retention or physical thread strength. Full-case construction remains separately gated.
