# OSC-03 independent OpenSCAD V1 critique

- Owner / role: `OSC-03`, independent CAD/code critic
- Date: 2026-09-04
- Candidate: `openscad/laifen_case_customizer_v1.scad`
- Source SHA-256: `d43574aad869e8428ca384501f7d6e83f52936275240ae2ee7f8934dd50f1c4d`
- Verdict: **BLOCK**
- Highest severity: `P1` functional geometry defects

## Provenance and checks

The frozen input contract was read from `BRIEF.md`, `DESIGN.md`,
`HANDOFF.md`, `IMPLEMENTATION.md`, and `inputs/MANIFEST.sha256`. The source and
focused test hashes match the implementation receipt. The focused Python suite
passes, but it checks only the separate Python contract layer and textual SCAD
features; it does not execute OpenSCAD CSG or inspect an STL.

```text
uv run pytest projects/laifen-wave-case/tests/test_openscad_customizer.py -q
  3 passed

/usr/bin/shasum -a 256 <source> <contract> <focused test>
  d43574aad869e8428ca384501f7d6e83f52936275240ae2ee7f8934dd50f1c4d  source
  6f9a3b10cb6950e3e1c105d312d6650ba5d9321975b5bbe8285552b60986d6ce  contract
  387c3baad77f80db76ae202d73611922d98b26eed4b7de2145ef2429539aaa10  test

OpenSCAD executable discovery
  /opt/homebrew/bin/openscad exists, but the attempted CLI invocation did not
  return a usable result in this critique session; no STL result is accepted.
```

## Blocking findings

### P1 — female thread void is completely removed by the preceding bore cutter

In `cap_shell()`, the cutter

```scad
translate([0,0,-.1])
  cylinder(r=thread_crest_radius+thread_clearance+thread_depth,
           h=closure_overlap+thread_pitch+.2);
```

has default radius `16.9 + 0.25 + 0.5 = 17.65 mm` and spans the full cap
thread zone. The following `female_thread_void()` occupies only approximately
the radial interval `16.65..17.40 mm`, so it is entirely inside the already
removed `r=17.65` cylinder. The female helical surface therefore contributes no
remaining material/void boundary. The body male ridge reaches radius16.90 mm
and meets a smooth cap bore near radius17.65 mm, so the intended 0.25 mm/side
thread contract is not realized and screw closure is not established.

Smallest repair: make the pre-bore stop at the female thread root boundary,
then subtract the helical female void so its radial profile remains in the cap
wall. Recheck the resulting actual solids and a complete hand-like screw
motion before accepting any STL.

### P1 — the body bottom chamfer Boolean removes the centre of the floor and can disconnect it

The body uses a solid frustum cutter with `r1=18.3` at its lower end and
`r2=19.5` at its upper end, subtracted from a solid cylinder of radius19.05.
Near the upper end of the cutter its radius exceeds the base cylinder radius,
so it removes the entire cross-section through part of the first 1.2 mm. The
remaining bottom annulus is separated from the upper body by that cut. This is
not an outside-edge chamfer on a connected floor; it risks a multi-solid/open
body and violates the bottom thickness/drain and printable-shell contract.

Smallest repair: construct the end profile as a connected revolved/extruded
wall section, or subtract only the outside wedge while preserving the central
floor and its `floor_thickness`. Validate solid count, watertightness, and the
drain holes after the repair.

### P1 — `end_chamfer` is implemented only at the body end

The sole chamfer Boolean is inside `body_shell()`. `cap_shell()` uses the value
only to stop the diamond rows; it does not chamfer the cap's closed end. The
frozen user/design intent calls for the small chamfer on both closed ends.

Smallest repair: add the same connected outer-edge chamfer construction to the
cap closed end, with the floor and optional top drains preserved, then validate
both end profiles.

### P1 — `wall` is exposed but does not drive the generated geometry

`wall` appears only in the OD assertion. The actual body/cap wall radii are
derived from `outer_radius`, `valley_radius`, and the two bores; changing
`wall` within a valid range does not change any solid. A Customizer control that
claims to be wall thickness but has no geometry effect is misleading and cannot
support the requested reusable parameter model.

Smallest repair: either derive/limit the exterior from the requested wall and
classify OD as a derived consequence, or remove the editable wall control and
expose a truthful derived wall readout. Preserve the minimum 1.8 mm textured
wall constraint in the chosen formulation.

### P1 — round and smooth modes silently change the OD from 39 mm to 38.1 mm

The base shell is always `cylinder(r=valley_radius)`, where
`valley_radius = outer_radius - diamond_depth`. The diamond spheres restore the
39 mm crest only in diamond mode. In `round` and `smooth`, no spheres are
created, so the maximum exterior diameter becomes `2*(19.5-0.45)=38.1 mm`.
That violates the envelope's editable `outer_diameter` meaning and makes
surface selection alter the container size unexpectedly.

Smallest repair: use `outer_radius` for round/smooth base shells, retaining
`valley_radius` only for diamond valleys, and add a geometry/bounds regression.

## Additional P2 contract gaps

### Split bounds do not protect the thread interval

The SCAD assertion checks only `cap_height > floor_thickness` and
`cap_height < closed_length-floor_thickness`. It permits cap heights below the
`closure_overlap + floor_thickness` needed by the 8 mm female cutter and cap
floor, producing a degenerate or threadless cap. The Python contract test also
does not bind the thread-specific feasible interval. Derive one shared feasible
split interval from the thread and floor requirements and assert it in SCAD and
the test layer.

### Diamond phase is not the specified seam/end phase law

`diamond_skin()` starts rows at `z0 + (row+.5)*diamond_axial_pitch` and truncates
with `floor()`. It does not use a global `z mod axial_pitch` phase or derive a
phase-matched terminal row at both functional ends. `diamond_phase_deg` changes
angle only. This can leave endpoint phase drift when dimensions or split
parameters change, contrary to the frozen phase continuity requirement.

### `thread_root_wall` and actual wall minima are not guarded consistently

The editable `thread_root_wall` range allows 1.0 mm while the design requires a
minimum 1.8 mm textured wall. No source assertion computes the actual minimum
wall across the thread, diamond valley, chamfer, and drain regions. Add a
derived minimum-wall guard and a geometry/mesh measurement once the CSG is
fixed.

### Required CLI STL and snapshot evidence is still absent

The implementation receipt records that OpenSCAD validation and snapshots were
pending. This critique accepts no printable, manifold, bounds, support-free,
or physical claim until each output selector (`assembled`, `body`, `cap`,
`print_layout`) is rendered and independently inspected, including changed and
reset parameter states.

## Passing observations

The source is self-contained and does not import or copy the downloaded mesh.
The canonical distance/percentage split formula, top/bottom/none drainage
choice, output selectors, named body/cap modules, original helical CSG intent,
and default envelope arithmetic are present. The default formulas derive
`cavity=213`, `engagement=6`, `overlap=9`, `body_height=144`, `cap_height=84`,
and `closed_length=219` as required. These observations do not overcome the
thread and shell-topology defects above.

## Recommendation

Reopen the implementation for the smallest P1 repairs in this order: connected
end profile/chamfers, functional female thread material/void, truthful OD/wall
parameter behavior, then split/phase/minimum-wall assertions. Regenerate every
output through OpenSCAD, inspect actual solid counts and bounds, and run the
independent validation/formal review gates before presenting this as a
customizer or printable design.

