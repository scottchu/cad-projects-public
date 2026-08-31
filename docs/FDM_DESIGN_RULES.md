# FDM printing design rules

Use these checks with each project's `PRINTING_PROFILE.md`. This is a growing
design checklist, not a universal slicer preset or a guarantee of strength.

## Rules to apply during design

| ID | Concern | Design check |
|---|---|---|
| FDM-01 | Layer direction and load | Identify tension, bending, compression and torque at critical sections. A slender bar printed upright may split between layers under sideways bending; printing its length in the bed plane often helps that load case. Horizontal is not always stronger: cross-section, material, bonding, temperature and toolpaths still matter. More infill alone does not remove interlayer weakness. |
| FDM-02 | Assembly pose is not print pose | An upright installed member may be printed lying down and fastened afterward. Record the bed-contact face and source-to-print transform separately from its assembled orientation. Compare support damage, hole quality and footprint before choosing. |
| FDM-03 | Thin features and stress concentrations | Check walls, ligaments, bosses and roots against the selected nozzle, actual extrusion widths and resolved perimeter paths. Nozzle diameter is not a universal minimum wall or clearance. Avoid abrupt thin roots; evaluate a fillet/gusset or a separate part where appropriate. |
| FDM-04 | Real joints and load paths | Every loaded member needs a physical seat, retention and a closed reaction path. Check screw access, assembly order, anti-rotation and tool clearance. M3 specifies a thread, not an insert's outer diameter/length: use the actual heat-set insert specification and coupon, or validate nut capture and access. Check tightening loads, pull-out and layer splitting; do not treat touching/floating CAD as fastening. |
| FDM-05 | Fit and tolerances | Name the fit's role: sliding, rotating, locating, clamping or interference. Use a matching material/orientation/process coupon and record measured fit. Account for elephant foot, shrinkage and warp. Do not transfer one successful bore clearance to every interface. |
| FDM-06 | Bed contact and supports | Inspect first-layer contact, early-layer continuity, bridges/overhangs, support removal and critical supported surfaces. Verify the written plate footprint including brim and spacing against the selected machine. Fix source geometry defects in source, not with an undocumented slicer transform. |
| FDM-07 | Material and service conditions | Record temperature, sustained load, creep, wear and expected cycles where relevant. A printable shape and a short fit test do not prove long-term stiffness, retention or heat resistance. Use the smallest representative physical test. |
| FDM-08 | Traceable process | Bind each verified run to its profile revision, exact source/artifact, printer/head/nozzle, material, slicer/presets and object/plate overrides. Separate intended settings from resolved slice settings and actual print observations. |

Orientation, support and tolerance guidance is informed by Prusa's
[Modeling with 3D printing in mind](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135).
These are qualitative design principles; they supply no validated strength,
temperature, clearance or process settings for this repository's projects.

## Profile and concern workflow

1. Start from the [profile template](templates/project-continuity/PRINTING_PROFILE.md)
   when creating a project. Every project keeps the file; if printing does not
   apply, state N/A with a reason and revisit it if printed parts are introduced.
2. Distinguish **available** inventory, **intended** selections, **verified slice**
   settings and **physical observations**. Use `pending` for unknown fields;
   [workshop inventory](WORKSHOP.md) is not project validation.
3. Add concerns as they arise with a stable ID, affected part, observed evidence
   versus hypothesis, proposed check and status. Close only with linked evidence;
   preserve rejected choices and older run records rather than rewriting history.
4. Before a print handoff, resolve the relevant open concerns and record the exact
   run. Filling a profile never bypasses the [CAD workflow](CAD_WORKFLOW.md) or
   creates printing authority. CAD, written artifact/slicer and physical gates
   remain separate.

Policy provenance: [printing-profile iteration](iterations/2026-08-31-printing-profiles/BRIEF.md).
