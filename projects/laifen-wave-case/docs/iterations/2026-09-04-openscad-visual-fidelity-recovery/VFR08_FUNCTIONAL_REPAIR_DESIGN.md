# VFR-08 bounded functional repair design

Status: **DESIGN READY; no implementation or acceptance performed.**

Task VFR-08-D; owner `/root/openscad_vfr08_repair_designer`, independent repair
designer. Worktree `/Users/scottchu/.codex/worktrees/4f8c/design-projects`;
project `projects/laifen-wave-case`; iteration
`2026-09-04-openscad-visual-fidelity-recovery`.

## Frozen inputs and scope

Verified project-relative `inputs/VFR08_FUNCTIONAL_REPAIR_INPUTS.sha256`:
`2bcbf0d5e41914cf1c5103322a42d5fd1ced64e61723bf3e6764311a8b6a4044`,
10/10 entries OK. Nested `candidate/VFR07_C1_CANDIDATE.sha256`:
`c95ca570ada87f7fad216c1beba08c0933764bddeb9fb1be7903075c39526101`,
13/13 entries OK. Source baseline:
`openscad/laifen_case_customizer_v1.scad`, SHA-256
`48b4ac84dc0cf4b8274200e9e2e13f145cfc01a5f721f975c37d1166c91ebd31`.

The task supersedes VFR-07's protected-geometry restriction only for complete
selected-end drain penetration and the cap's print-layout pose. The recorded B
selection and REQ-10 already determine intent. No new spatial choice is needed.
This is a source repair design for the existing OpenSCAD target, not a conversion
to build123d or a change to immutable P1 R7 STEP authority.

Outcome: the same two-piece screw case has seven through holes at the selected
closed end, and both separate pieces stand closed-end-down/open-end-up in
`print_layout`. Units are mm; +Z is up. Assembly use and local datums are unchanged.
The body opens at local Z=144; the cap opens at local Z=0 and closes onto the
body with its existing +135 mm assembly translation.

## Selected exact source delta

### DRAIN-08: one shared cutter convention

In `module drain_pattern(h)`, change **both** cylinder arguments from
`center=true` to explicit `center=false`. Preserve cylinder diameter, h, $fn,
ring coordinates, angle iteration, and all four call sites byte-for-byte.
The module's local axial interval becomes `[0,h]`. There are exactly four
production callers: body/cap in each of the diamond and smooth branches.

Keep their current `h=floor_thickness+.2` and translations:

| Role and condition | Cutter interval for thickness t and cap height H | Default |
|---|---|---|
| Body, `drainage_mode == "bottom"` | `[-0.1, t+0.1]` | `[-0.1,3.1]` |
| Cap, `drainage_mode == "top"` | `[H-t-0.1, H+0.1]` | `[80.9,84.1]` |

The body floor is `[0,t]`, nominally `[0,3]`. The existing cap inner-floor
datum includes the protected +0.01 mm cavity extension: its actual floor is
`[H-t+0.01,H]`, nominally `[81.01,84]`, thickness **2.99 mm**. Preserve that
extension; do not turn this repair into a floor-thickness correction. The cap
cutter consequently overlaps the cavity by 0.11 mm and the exterior by 0.1 mm.
Both intervals strictly cross every floor for valid existing t/H values.

Default center positions remain `(0,0)` and
`(9*cos(a),9*sin(a))`, `a=0,60,120,180,240,300` degrees, with nominal diameter
3 and $fn=96. Default furthest radial extent 10.5 leaves 4.5 mm to the smaller
15 mm bore; no sidewall or chamfer intersection is introduced. Preserve the
existing sidewall assertion and parameter domain without adding a new domain.
`none` cuts neither piece; `bottom` cuts only the body; `top` cuts only the cap.

Reason for this choice: the callers already express a noncentered cutter start
and end. Correcting the shared module fixes all four paths in two argument
edits. Moving four callers to centered mid-floor coordinates would work but
repeat the same axial derivation. Increasing cutter length would remove the
roofs without restoring the intended bounded interval and is rejected.

### POSE-08: rigid transform only in print_layout

Keep the body line unchanged. Replace only the cap line with:

```scad
translate([-outer_diameter/2-3.5,0,cap_height])
  rotate([180,0,0]) color("#77b09a") cap_shell();
```

The exact local-to-print map is
`(x,y,z) -> (-outer_diameter/2-3.5+x, -y, cap_height-z)`.
Rotation acts first, then translation. It is a proper rotation, determinant
+1; no mirroring, scaling, phase edit or geometry rewrite is allowed.
Cap local closed end Z=H maps to bed Z=0; local open rim Z=0 maps to Z=H.
The cap cavity-floor normal reverses from -Z to +Z; the opening direction
reverses from -Z to +Z. Body and cap heights remain 144 and 84 by default.
Default X offsets remain +23 and -23, leaving 7 mm between the 39 mm envelopes.
Body/cap standalone and `closed_assembly()` transforms stay byte-identical.

## Per-object delta mask and preservation

| Object | Allowed change | Invariants / forbidden changes |
|---|---|---|
| Body solid | Remove existing blind roofs only inside selected bottom drain footprints | Exterior, B lattice, seam at135, bore30, floor outside holes, thread, height144, local datum unchanged |
| Cap solid | Remove selected top floor material only within existing drain footprints | Exterior, B lattice, local seam0, bore31, existing2.99 floor elsewhere, threads, height84, local datum unchanged |
| Print-layout body | None | Original +X placement and opening-up pose |
| Print-layout cap | Above rigid transform only | Same cap solid, same X spacing; no effect on assembled or standalone outputs |
| Other authority | None | OD39, N33, plateau0.18, pitch4.8, phase, depth0.45, 1.2 end chamfers, threads, profiles, shoulder, defaults, existing parameter assertions, P1 R7, browser/schema/worker/vendor, services, prior evidence |

Smooth geometry receives the same intended drain/print-pose correction through
the shared functions. It must otherwise remain identical; old default smooth
body byte identity is intentionally superseded because its blind roof is removed.
Smooth `none` geometry and every unselected standalone end remain preservation
oracles. Depth-zero diamond must remain equivalent to corrected smooth geometry.

## Ordered regression and evidence gates

These are prescribed checks, **not results from this design task**. Implementer
records the failing drain/pose regressions on frozen C1 before edits. Use the
pinned OpenSCAD/Manifold path already in the project; no new compiler, mesh
repair, geometry reconstruction, browser deployment or slicing is authorized.

1. **Cheap math and scope (DRAIN-08/POSE-08, REQ-05/10):** execute the real
   SCAD cutter and transform witnesses, not only string assertions. Check both
   cutter intervals, all seven centers, and all four callers. Check thickness
   2,3,8 with valid cap heights and a nondefault valid split, plus the exact
   default. Prove endpoints/orientation, distance preservation and inverse
   transform for representative non-axis points. Source comparison must allow
   only the two `center` arguments, cap-layout line and explanatory comments;
   preserve all other named geometry/functions/derivations. No duplicated
   production transform helpers are necessary for this single use.

2. **Meaningful actual-solid drain regression:** generate default body/cap
   for both styles (`diamond` depth0.45 and `smooth`) in `none`, `bottom`, and
   `top`: 12 explicit standalone outputs. Inspect actual CSG/Manifold result
   and written mesh. For each selected end, all seven hole axes must have no
   triangle intersection or solid occupancy across the full floor and beyond
   both faces; additionally probe small interior offsets, away from boundaries,
   to catch a partial web. Unselected ends must retain their original floor
   intervals. At default off-hole witnesses `(3,0)` and `(12,0)`, floor material
   must remain, with no axial-datum shift. Verify seven distinct full apertures
   and their $fn96 diameter/ring polygons in sections immediately inside both
   floor faces. A mouth screenshot or one central ray alone is insufficient.

3. **Constraint/topology and containment:** every standalone written mesh must
   be one positive-volume, watertight, consistently wound connected component,
   with each edge used exactly twice, no zero-area or duplicate triangles.
   Seven through apertures change genus: selected pieces should have Euler
   characteristic `2-2*7=-12`; undrained pieces remain Euler2. Do not reuse C1's
   blanket Euler2 expectation. Inspect actual solid difference versus same-mode
   frozen C1: no added solid; all removed material lies within the seven intended
   floor columns. Use temporary CSG intersections/differences from authoritative
   solids or independent mesh Boolean/section evidence, never a bounding-box-only
   assertion. For same-source none versus drained outputs, removed volume must
   equal the seven polygon areas times floor thickness (3 body,2.99 cap), within
   documented mesh numerical tolerance. Preserve thread/sidewall/chamfer geometry
   using scoped surface/profile comparisons outside the drain mask.

4. **Written print-layout pose and object collision (REQ-10):** export two
   layouts, default diamond/bottom and smooth/top. Require exactly two separated
   components, both minZ=0 within1e-6 mm, respective maxZ144/84, openings facing
   +Z and closed end faces at the bed. Default cap internal floor is now Z2.99;
   its mouth is Z84. Compare each component with its corresponding standalone
   solid under the exact prescribed transform (surface/solid parity within1e-6,
   allowing serializer reordering); require zero inter-component intersection
   volume and measured7 mm X-envelope gap. Inspect floor and open-rim sections:
   min/max bounds alone cannot distinguish which end is open.

5. **Preservation and requirements:** check unchanged B exterior, seam point-set
   equality, bores, protected profiles and end chamfers on repaired diamond
   meshes. For unchanged radial exterior triangles, retain the existing
   <0.025 mm error and <250000 exterior-triangle budgets. Compare same-mode
   frozen C1 for unselected standalone pieces; smooth none must remain unchanged.
   Execute one corrected depth-zero bottom body and require equality with smooth
   bottom body. Existing focused customizer and WASM simulator tests must pass:
   `uv run pytest projects/laifen-wave-case/tests/test_openscad_customizer.py projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py`
   from the worktree root. Implementer adds only focused regressions needed for
   the two concrete defects; retain root uv environment and no browser edits.

6. **Review artifacts and join:** freeze new source/tests and generated scratch
   output hashes under a new VFR-08 candidate manifest. Independent critic and
   validator inspect that identical candidate; a distinct formal reviewer joins
   their findings. Review selected-end inside/outside views and both open-up
   print pieces after deterministic gates. Bind snapshots to exact artifact
   hashes. Any eventual user-facing visibility claim needs the actual delivery
   surface gate; this task grants no live-browser change.

## Budget, ownership and stop conditions

One initial VFR-08 candidate plus at most two focused repair cycles. Implementation
owner alone writes source/tests and new scratch artifacts; preserve C1 artifacts.
Initial explicit mesh budget is 15 outputs:12 matrix components,2 layouts,1
depth-zero witness. Baseline failing witnesses and scoped Boolean diagnostics
are evidence-only, not extra design candidates. Regenerate only changed/failed
outputs and dependent gates on repair. No parameter grid or full-project build.

Use balanced/medium for prescribed implementation; independent strong/high roles
for critique, validation and formal review. At most three workers concurrently,
one writer. Qualitative implementation timebox20 minutes with a checkpoint at10;
individual mesh jobs cap60 seconds, and a timeout triggers diagnosis before retry.
Exact runtime/token controls unavailable to this designer remain qualitative;
target a compact receipt, not raw logs. This design task permits one concise
design artifact and no subordinate workers.

Stop and route to root if input hashes drift; the repair needs changes outside
the mask; any cheap gate fails; a hole merges with a sidewall/other aperture for
the chosen valid fixture; topology, preserved surface, source/mesh parity or
orientation fails; candidate budget expires; or passing requires browser/slicer
work. A floor-thickness, pattern, thread or parameter-domain redesign needs a new
contract. Never suppress a defect by relaxing a tolerance, mesh cleanup, adding
supports or rotating only in a slicer. Check diagnostics as well as return code:
OpenSCAD echo/assertion errors can accompany return0.

## Evidence receipt and acceptance boundary

Commands actually run for design: `cat`/`sed` of root AGENTS/CAD workflow/FDM
rules, CAD skill/brief reference, project state/next-agent/requirements/experience/
decision index/printing profile, active brief/handoff, task, C1 source/tests and
critic/validation evidence; `/opt/homebrew/bin/rg -n 'drain_pattern\('` found four
call sites. Project-root `shasum -a 256` of the repair input manifest returned
the fingerprint above; `shasum -a 256 -c` verified all10 repair inputs and all13
nested C1 entries. An initial nested-manifest check from the repository root
failed because the path is project-relative; rerun from the project root passed.
Initial experience filename lookup missed `EXPERIENCE_LOG.md`; actual
`docs/EXPERIENCE.md` was read. No geometry generation or tests ran in this role.

Sole changed path is this design document. No snapshot applies because no CAD
or mesh artifact was created or edited. Its SHA-256 is reported in the return
receipt after writing; a self-referential in-file checksum is intentionally not
used. Root owns continuity indexes and downstream scheduling.

Design coverage: the two High findings have exact bounded repairs; all remaining
VFR-06/07 browser-performance, full clipping/ownership, service-path/thread-contact
and acceptance gaps remain open. Native/OpenSCAD mesh evidence, CAD/STEP authority,
written artifact/slicer acceptance and physical acceptance stay separate.
Correct orientation does not establish support-free slicing. Actual drainage,
bed adhesion, elephant foot, fit/torque/cycling, seam appearance and strength still
require bound slicer/print evidence. Intended U1 PLA/0.4 nozzle/0.2 layers/supports
off settings are unchanged. No slicing, printer action, deployment or release is
authorized by this receipt. Next action: root freezes this design into the
implementation input manifest and assigns VFR-08 implementation.
