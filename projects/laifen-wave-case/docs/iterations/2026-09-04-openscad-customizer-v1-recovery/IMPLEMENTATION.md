# OSC-06 constructive thread-root recovery implementation

## Frozen inputs

Verified `inputs/MANIFEST.sha256` SHA-256:
`22e3b909bf3a3fbac3d1f85bdd2056ea95c3a3c584d9904a9c9a1bf2b0f9aa3b`.

## Change

`THREAD_EMBED_EPS = .05` is an internal constructive Boolean overlap.  The
male helical polygon now begins 0.05 mm inside the male root cylinder.  The
matching female cutter begins 0.05 mm inside the full-overlap female root
void.  Both profiles retain their `thread_depth` crest coordinate, so the
2 mm pitch, 6 mm active engagement, root-cylinder clearance, and 0.25 mm
radial clearance contract are unchanged.  The epsilon is constrained positive
and below both depth and clearance.

## Bounded diamond compilation change

The pre-recovery diamond body STL did not finish within a 60-second native
OpenSCAD ceiling.  The diamond generator now creates all `groove_count`
starts for one handedness in one 2D child set and extrudes that set once; the
other handedness is a second extrusion.  The derived count, arc-pitch-based
starts, axial twist law, global phase expression, depth, and source parameters
are unchanged.  This replaces 68 separate Boolean cutter extrusions with two
without reducing the repeat field.

## Validation

Commands actually run from the repository root:

```text
uv run pytest projects/laifen-wave-case/tests/test_openscad_customizer.py -q
/Volumes/OpenSCAD/OpenSCAD-2021.01.app/Contents/MacOS/OpenSCAD \
  -D 'surface_style="smooth"' -D 'output_mode="body"' \
  -o /tmp/osc06-smooth-body.stl openscad/laifen_case_customizer_v1.scad
/Volumes/OpenSCAD/OpenSCAD-2021.01.app/Contents/MacOS/OpenSCAD \
  -D 'surface_style="smooth"' -D 'output_mode="cap"' \
  -o /tmp/osc06-smooth-cap.stl openscad/laifen_case_customizer_v1.scad
/Volumes/OpenSCAD/OpenSCAD-2021.01.app/Contents/MacOS/OpenSCAD \
  -D 'surface_style="smooth"' -D 'output_mode="assembled"' \
  -o /tmp/osc06-smooth-assembled.stl openscad/laifen_case_customizer_v1.scad
```

The focused suite passed: `6 passed`.  Native smooth STL render times were
7.14 s (body), 4.01 s (cap), and 15.73 s (assembled).  `trimesh` with processed
STL vertices reported body and cap as watertight, one component each, positive
volumes 68998.710 mm3 and 38033.176 mm3, with bounds respectively
`[-19.5,-19.5,0]..[19.5,19.5,144]` and
`[-19.5,-19.5,0]..[19.5,19.5,84]`.  The assembled temporary STL was watertight
and positive-volume (107031.885 mm3), bounds
`[-19.5,-19.5,0]..[19.5,19.5,219]`, and contained three disconnected shell
components because OpenSCAD exports the intentionally overlapping two moving
parts and their nested cavity boundary as separate shells.  It is an assembly
review artifact, not a printable release mesh.

## Diamond benchmark limit

Using the same native executable, a default diamond body STL was terminated by
an explicit 60-second ceiling before completion both before and after the
two-extrusion consolidation.  The default diamond cap was terminated at its
55-second ceiling.  No further geometry reduction was applied: a third change
would exceed this recovery's repair allowance and must be reopened as a design
decision.  The smooth source is mesh-valid; diamond release/export acceptance
remains blocked on a bounded performance design.

No STL or other release asset was retained; all compiled meshes were temporary
files under `/tmp`.
