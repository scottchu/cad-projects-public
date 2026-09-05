# P1 R4 uniform fully patterned short cylinder

Original source for the short body and C25 cap. The closed crest envelope is40mm diameter, with0.45mm inward diamond valleys over both complete sidewalls and the female collar. The only outer relief is a textured0.20mm radial by0.30mm axial allowance at each closed bed edge. The default cavity is72.5mm; this is not a full Laifen fit release.

`params.py` isolates the original fitted functional dimensions from the new exterior. Bores30/31, floor3, pitch2, engagement6, root16.8, crest17.4, collar-end10.2 and inner taper-end12.4 remain fixed. Original `thread_profile.py` is copied byte-identically from R3. Clearance can be selected within0.20..0.30; exterior pitch, phase, plateau, diameter, height and short lengths are named inputs with early feasibility guards. Only the default geometry is submitted for acceptance. Feasible scalar combinations and alternative clearances are not broad geometric validation. Full Laifen dimensions and any thread change require a separate design gate.

`skin.py` defines the shared field. `surface.py` clips affine diamond facets, creates rational circle/Bezier patches with canonical shared edges, and closes both ends using their actual noncircular planar wires. No per-diamond Boolean or downloaded geometry is used. `parts.py` adds the unchanged functional threads, recessed25 label, source joints, closed assembly and two-part open-up print transform.

Default artifacts:

- `body.step.py` / `body.step`: one body, assembled Z[-35.1,9].
- `cap_c25.step.py` / `cap_c25.step`: one cap, assembled Z[0,43.4].
- `closed_c25.step.py` / `closed_c25.step`: two source-jointed parts, closed length78.5.
- `print_layout.step.py` / `print_layout.step`: two objects, openings up, centers X±23.5, nominal87x40mm envelope, maximum height44.1.

Run from repository root with the root uv environment:

```sh
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/gen projects/laifen-wave-case/cad/p1_r4_uniform_skin/body.step.py projects/laifen-wave-case/cad/p1_r4_uniform_skin/cap_c25.step.py projects/laifen-wave-case/cad/p1_r4_uniform_skin/closed_c25.step.py projects/laifen-wave-case/cad/p1_r4_uniform_skin/print_layout.step.py --write
uv run pytest projects/laifen-wave-case/tests/test_uniform_skin.py -q
```

Parameter edits belong in a new source candidate. Derived STEP and render caches must be regenerated. The implementation receipt and candidate path/content manifest are in `docs/iterations/2026-09-02-p1-r4-uniform-skin/`; immutable R3 remains beside this namespace. The task assigned `p1_r4_uniform_skin` in place of the brief's provisional `p1_r4_generator` path; this is routing only.

Implementation checks are not independent acceptance. Source/CAD, written STEP, slicer and physical statuses remain separate. No slicing, upload or printing was performed for R4.
