# VFR-07 C1 independent critique

Status: **HOLD — the C1 lattice/seam construction is digitally credible, but
the exact candidate violates the drain and cap print-orientation requirements.
It may remain scratch evidence; it must not be treated as a fabrication,
browser-enablement, or acceptance candidate.**

Owner role: `/root/openscad_vfr07_critic`, independent C1 critic. This review
is read-only except for this receipt. No candidate source, test, STL, browser,
service, continuity, STEP/slicer, or printer state was changed.

Verified critique-input manifest:
`inputs/VFR07_CRITIQUE_INPUTS.sha256`, SHA-256
`edb551f8622f78ff6609af166c31a7c8670185249a5792efb2d58dacd2e2332b`;
all 9 entries passed. The nested C1 candidate manifest
`candidate/VFR07_C1_CANDIDATE.sha256` also passed all 13 entries. Exact reviewed
source: `48b4ac84dc0cf4b8274200e9e2e13f145cfc01a5f721f975c37d1166c91ebd`.

## Findings

### High — the seven default body drains are blind pockets

`drain_pattern(h)` builds centered cylinders. The default body call places a
3.2 mm-high centered cutter at local `z=-0.1`, so its axial interval is
`-1.7..1.5 mm`. The body floor occupies `z=0..3 mm`; therefore 1.5 mm of solid
floor remains above every nominal drain. The exact default body STL confirms
this construction: the seven downward-facing circular pocket roofs are at
`z=1.5 mm` with combined triangulated area `49.4448 mm^2`, while the cavity
floor is still a full upward-facing disk at `z=3 mm`. There is no water path
through the floor.

The nondefault top-drain branch has the symmetric source defect. Its cutter is
centered at `z=80.9 mm` and spans `79.3..82.5 mm`, while the cap exterior end is
at `z=84 mm`; it also leaves a 1.5 mm outer skin. The supplied cap STL uses the
default bottom-drain mode, so this cap conclusion is source-proven rather than
artifact-proven.

This fails the support-free-drain outcome in REQ-05 and prevents any drain or
water-management acceptance claim. The defect is inherited/protected under
the bounded VFR-07 recovery contract; that provenance does not make the
generated geometry satisfy the requirement. Repair requires a separately
authorized protected-geometry correction and a new candidate fingerprint.

### High — `print_layout` places the cap opening down

The cap's open rim is local `z=0`; its closed exterior end is `z=84`. The
`print_layout()` module only translates the cap in X and does not rotate it, so
the opening is placed on the build plate. In the exact cap STL, the cavity
ceiling is a downward-facing 96-gon disk at `z=81.01 mm` with area
`754.2289 mm^2`. In that pose it is a cavity-wide bridge near the end of the
print. This directly contradicts REQ-10's requirement that both parts print
vertically with openings up, supports off, and intended unsupported overhang
no greater than 45 degrees. It also leaves the support-free part of REQ-13
unmet before slicing.

The standalone cap geometry is not intrinsically invalid: turning the closed
end onto the bed would put the opening up and build the 2.99 mm end floor from
the bed. The defect is the candidate's declared print-layout transform. As
with the drain placement, VFR-07 explicitly protected output transforms, so a
repair must be routed outside this syntax-recovery scope and then reviewed as
a new candidate.

### No additional lattice or seam defect found in the supplied meshes

The supplied G2, body, and cap STLs independently loaded as one positive-volume,
watertight, winding-consistent component each, with Euler characteristic 2,
no zero-area triangles, and every unique edge used exactly twice:

| Artifact | Vertices | Faces | Bounds in mm |
|---|---:|---:|---|
| `g2-short-band.stl` | 1,586 | 3,168 | `39.000 x 38.996536 x 7.130` |
| `body-final.stl` | 27,874 | 55,744 | `39.000 x 38.996536 x 144.000` |
| `cap-final.stl` | 20,257 | 40,510 | `39.000 x 38.996536 x 84.000` |

At the assembly seam, the body ring at local `z=135` and cap ring at local
`z=0` each contain 99 exterior vertices. Their XY point sets are exactly equal
after the source's declared `1e-8 mm` quantization, including the `19.05 mm`
valleys and `19.5 mm` crests. This supports relationship B: two separate parts,
N33 from the valley radius, the retained 0.18 plateau relation, one shared
phase, and texture reaching both sides of the middle seam. A printed pair is
still required to decide whether the seam looks continuous after process
variation and screw-clock positioning.

The supplied meshes also retain the protected nominal envelopes: OD 39 mm,
body/cap heights 144/84 mm, body seam at 135 mm, body bore radius 15 mm, cap
bore radius 15.5 mm, a 3.00 mm body floor, and the explicitly preserved
2.99 mm cap floor (`84 - 81.01`). The end rings are radius 18.3 mm and the
outer crest reaches radius 19.5 mm at the 1.2 mm chamfer limit. I found no
mesh evidence of a changed chamfer size, collapsed end, nonmanifold floor, or
seam-coordinate mismatch.

## Requirement and acceptance coverage

| Contract area | Critique result |
|---|---|
| REQ-01 original source-native geometry | Pass for reviewed scope: the SCAD is self-contained and imports no downloaded mesh. |
| Relationship B / REQ-08 count, pitch, phase, seam | Digital pass on source and exact seam point sets. The retained requirements text still mentions smooth zones near openings/shoulders; the later explicit B decision removes the middle seam collars and is the applicable intent for this candidate. |
| REQ-05 dimensions, floor, drains | Envelope and floor dimensions pass the protected digital checks; drains fail because they are blind. |
| REQ-06/07 thread construction | Source retains the 2 mm pitch, 6 mm helix, 0.25 mm nominal radial clearance, root embed, and entry relief. Fit, cycling, elephant foot, torque, and strength remain physical/slicer unknowns. |
| REQ-09 texture depth and residual walls | Default source math retains 0.45 mm depth and the documented nominal valley-wall budgets. No material-strength conclusion follows. |
| REQ-10 print pose/support | Fail: cap opening is down in `print_layout`, with a 754.2289 mm² downward cavity ceiling. No slice was reviewed. |
| REQ-13 physical acceptance | Open. No exact slicer identity, printed C1 parts, fit cycles, loaded clearance, drainage-flow test, or visible-seam observation exists. |
| V06-3B/V06-3C browser worker and protected-geometry gates | Open exactly as the implementation receipt states. Local STL topology does not substitute for the unchanged worker's cold end-to-end timing, final browser bytes, exterior-error proof, or source/artifact parity. |

The implementation receipt's acceptance language is appropriately bounded: it
labels C1 `PARTIAL`, disclaims implementer approval, calls the body/cap files
local probes, and keeps independent accuracy, worker, protected-geometry, and
physical gates pending. The filenames containing `final` must remain understood
as scratch probe names; they are not release or physical-acceptance labels.

## Evidence and disposition

Commands run from the assigned worktree/project roots included:

```text
shasum -a 256 projects/laifen-wave-case/docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/inputs/VFR07_CRITIQUE_INPUTS.sha256
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/inputs/VFR07_CRITIQUE_INPUTS.sha256
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR07_C1_CANDIDATE.sha256
cmp -s projects/laifen-wave-case/openscad/laifen_case_customizer_v1.scad projects/laifen-wave-case/scratch/vfr07-implementation/candidate.scad
uv run python -B -
```

The last command was an in-memory `trimesh`/NumPy inspection of the three exact
manifest-bound STLs. It measured topology, bounds, face areas/normals, endpoint
planes, drain-pocket roofs, and the body/cap seam point-set equality; it wrote
no artifact.

Disposition: retain C1 only as evidence that the selected VFR-06 lattice can
produce valid local G2/body/cap meshes and an exact digital seam. Do not advance
it to browser enablement, fabrication, or formal acceptance. Route the blind
drains and cap print-layout transform as explicit protected-geometry changes,
then freeze a new candidate and rerun the affected mesh, seam, FDM/slicer, and
independent review gates. Worker performance, browser delivery, thread fit,
drain flow, surface feel, and physical seam appearance remain unresolved.
