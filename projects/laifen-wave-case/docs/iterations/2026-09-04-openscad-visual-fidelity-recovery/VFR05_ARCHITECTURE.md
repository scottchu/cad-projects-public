# VFR-05 direct annular-solid architecture

Status: **ARCHITECTURE SELECTED; implementation, timing, mesh acceptance and independent review pending.**

Owner: `/root/openscad_vfr05_architect`, independent architecture/design role after the exhausted VFR-04 and VFR-04R workstreams. This document is the sole write. Root owns the new implementation manifest, task assignments and continuity indexes. No source, tests, artifacts, browser or hosting changed during this task.

Project: `projects/laifen-wave-case`; iteration: `2026-09-04-openscad-visual-fidelity-recovery`; worktree: `/Users/scottchu/.codex/worktrees/4f8c/design-projects`. Verified architecture-input fingerprint: **`9b4dbaf516633a407b13375685ffd546e8f89cb67a91dd63e1e5ba39c314f27e`**, SHA-256 of `inputs/VFR05_ARCH_INPUTS.sha256`; all 16 project-relative path/content entries passed verification. The SCAD baseline is `openscad/laifen_case_customizer_v1.scad` at `4e6ccd68f95d583d0c3b93bc33442d01107af90b5e66267bfe20034732e0d672`.

The recorded user `b` in `VFR03_USER_DECISION.md` remains the intent authority: two roles, valley-derived default N33, plateau half-fraction 0.18, common global phase, texture to both sides of seam S. This changes the representation of the same approved surfaces; it does not reopen or silently amend B. P1 R7 remains the preserved build123d/STEP authority. OpenSCAD remains the authority for this editable browser/STL candidate.

## Diagnosis and decision

The current G2 result proves the field partition can produce a valid short surface: 4,956 triangles, one watertight component, positive volume, maximum analytic bound 0.00725582416 mm and sampled error 0.00705172583 mm. Its final reported wall time is 4.192 seconds. The two G3 body runs exceeded 60 seconds and wrote no body. The receipts contain no stage-isolated full-body timing; **they do not prove that the cavity Boolean is the sole bottleneck**.

Two independent costs are evident in the source:

1. **High: global vertex lookup scales quadratically.** `diamond_first_index` at baseline line 205 searches a list. Lines 224–228 search the full raw key array once for every raw vertex; lines 232–240 search the full unique key array for every face index. These arrays grow with the entire component. A body is 135/7.13 = 18.934 times the G2 band height; quadratic comparisons can grow by about 358.5 times before other costs. This is an order-of-growth explanation, not a measured body-time extrapolation. The current upstream OpenSCAD `builtin_search` implementation also scans the table for each requested vector value; it corroborates the algorithmic concern but does not profile or identify the exact pinned WASM build. [OpenSCAD primary source](https://raw.githubusercontent.com/openscad/openscad/master/src/core/builtin_functions.cc)
2. **High: avoidable whole-part solid work.** The body first creates a solid patterned cylinder, intersects it with a full-height chamfer envelope, unions its neck and helix, then subtracts its full-height bore. The cap repeats a solid outer blank, envelope intersection and overlapping cavity/root/relief subtraction. These operations process a dense exterior to obtain surfaces whose connectivity and inner profile are already known analytically. Their individual timing contribution remains unmeasured.

Select **one directly closed, role-specific annular solid per component, assembled from bounded repeating facet templates and directly indexed boundary surfaces**. Integrate patterned exterior, closed-end trim, smooth bore, floor, shoulder and closure-root profile into that one polyhedron. Retain only the existing male-helix union, female-helix groove subtraction and selected drain subtraction. This removes both full-height cavity Booleans and the outer-envelope Boolean from the positive-depth diamond path. It also removes the global key-search algorithm; changing the Boolean arrangement alone is insufficient.

Keep the existing smooth/depth-zero execution branch intact. Keep the exact rational field and the successful constant-u ramp bisection. Reduce triangulation within those same facets as described below. No per-diamond solid union, uniform resampling grid, host-generated replacement mesh, imported STL, repeated whole-mesh refinement or new runtime is selected.

Alternatives considered:

| Alternative | Disposition |
|---|---|
| Direct shell while retaining the global raw-key registry | Rejected: leaves the strongest source-evidenced growth problem intact. |
| Faster indexing alone, with the existing full solid/cavity Boolean stack | Useful diagnostic, but not the selected full architecture: leaves unnecessary solid work and little timing margin after repeated failures. |
| Remove the ramp split or coarsen field sampling | Rejected: the unsplit recorded candidate exceeded 0.025 mm and the uniform grid exceeded it substantially. |
| More subdivisions or longer timeout | Rejected: worsens the unresolved cost or weakens the frozen gate. |
| Direct body with a generic full-blank cap | Rejected: the cap has a simple known inner profile and can use the same surface primitives without inheriting its Boolean stack. |
| Generate the mesh in Python/JavaScript and import/display it | Rejected: replaces the user-selected SCAD geometry authority. |

## Protected geometry and exact role surfaces

Units remain mm. XY is the circular plane; +Z is the case axis. Body local Z is global Z; cap local Z maps to `S + z`. `S=body_thread_z=cap_close_z`. Existing output transforms, length/split/overlap equations, dimensions and parameter ranges remain unchanged. At defaults: cavity213, closed length219, body height144, cap height84, S135, overlap9, engagement6, floor parameter3, chamfer1.2, OD39, body/cap bores30/31, root radius16.4 and crest radius16.9.

The direct-body boundary is the following connected oriented surface, before existing helix/drain operations:

1. Outer bottom disk at Z0, ending at the inherited trimmed rim.
2. Trimmed patterned outer wall from Z0 to S, ending on the shared seam ring.
3. Positive shoulder annulus at S from the patterned perimeter inward to the unchanged 96-sided male-root perimeter.
4. Male-root outside wall from S to `body_height`, using the same unrotated `$fn=96` polygon as the old cylinder.
5. Open-end annulus at `body_height` from root perimeter to body-bore perimeter.
6. Inward-facing body-bore wall from `body_height` down to `floor_thickness`.
7. Cavity-facing floor disk at `floor_thickness`.

There is no new void, end plug, seam gap or exterior collar. The root surface is directly connected to the shoulder; do not join two solids merely tangent at S. Union the unchanged `body_thread()` at `S+thread_transition`, then apply the unchanged selected body drain cutter. Preserve the male thread profile, winding, pitch, slice count, embed epsilon and radial placement exactly.

The direct-cap boundary contains the exterior wall from local0 to `cap_height`, top disk, open-rim annulus, inward-facing stepped bore/entry-relief surface and cavity-facing floor disk. Its inner void is the exact union implied by the old non-helical cutters:

```text
base bore:       cap_inner_radius, z = 0 .. cap_height-floor_thickness+0.01
thread root:     thread_root_radius+thread_clearance, z = 0 .. closure_overlap
entry relief:    thread_root_radius+thread_clearance+0.4-z, z = 0 .. 0.4
effective bore:  maximum radius of the active intervals above
```

Construct the piecewise profile including endpoints, steps and any cone/base-bore crossing inside 0..0.4; do not assume the default radius ordering for every valid parameter combination. Revolve that profile as the same unrotated 96-sided polygonal surfaces. The helical female groove remains the unchanged `female_thread_groove()` subtraction at `thread_transition`; the selected cap drain cutter is unchanged.

Three easy-to-miss preservation facts come from the frozen source, and override rounded prose when constructing equivalent geometry:

- The actual cap cavity ends at `H-floor+0.01`, giving a 2.99 mm default uncut top floor. Do not normalize it to3.00 or alter the closed-length equation in this recovery.
- Default entry-relief maximum radius is **17.05**, leaving **2.00 mm** from valley19.05 at local Z0. The earlier VFR-04 sentence giving16.65/2.40 describes the root cylinder radius, not the relief maximum. The current source preflight uses the correct relief expression and must remain authoritative.
- `drain_pattern(h)` uses centered cylinders. At defaults the body cutter spans Z-1.7..1.5; the cap cutter spans local79.3..82.5. Preserve these exact cutter placements and intersections. Their names do not establish through-drainage; this source observation grants no separate drain repair or physical-function acceptance.

The bore/root/female-relief polygons keep their original physical angular datum. Changing `diamond_phase_deg` must rotate only the outer field. A ring zipper may reorder the indices of an internal polygon to match angular traversal; it must not rotate, resize or round that polygon's coordinates.

## Exterior trim without a Boolean

Keep the original `body_outer_envelope()` and `cap_outer_envelope()` code for smooth. For diamond, form the same nominal 45-degree circular envelope directly:

```text
q_body(z) = min(Rcrest, Rcrest-end_chamfer+z)
q_cap(z)  = min(Rcrest, Rcrest-end_chamfer+cap_height-z)
r_outer(u,v) = min(diamond_radius(...,u,v,...), q_role(local_z(v)))
```

Do not merely clamp existing vertices and leave triangles crossing an unresolved trim crease. Split the field facets at the axial chamfer break and at the affine equality `r_field=q_role` within each facet. The rational field is affine inside each plateau/ramp and q is affine inside each chamfer interval, so these are straight developed-space clipping lines. Insert their shared-edge intersections in every incident patch. The default transition lies inside the inherited 1.2 mm chamfer; its low end is at0.75 mm for the body, with the cap mirrored. The exact same formula handles other allowed depths, including depth greater than the chamfer without assuming that0.75 interval always exists.

This removes the polygonized-envelope intersection, not the end chamfer. Its defining end planes, radii, chamfer height and 45-degree slope remain unchanged. The old96-sided outer envelope differs from its nominal circle by at most0.010440545 mm at R19.5. Direct diamond tessellation may represent the nominal circular envelope more closely, within the existing <=0.05 mm mesh parity tolerance; it does not promise triangle/byte equality with the old envelope. Independently compare the final trimmed surface with `min(field,q)` and the frozen smooth envelope. If either established tolerance is exceeded, stop; do not alter chamfer dimensions or broaden the tolerance.

Purely conical end patches can use a source-derived angular subdivision sufficient for the same0.025 mm error bound; this is a bounded terminal patch rule, not a public quality parameter. Preserve all pattern/cone intersection breaklines. Large conical patches must satisfy their own chord bound rather than borrowing the field-facet bound. Body and cap seam rings are obtained from the same global-v=0 boundary function, so their limiting outer point sets agree exactly before serializer rounding.

## Bounded templates and direct indexing

Extract a deterministic pure mesh-data construction in SCAD before the solid wrapper. Both role wrappers and private probes must consume it. It returns points and faces; no BREP, I/O or Boolean construction occurs inside the pure functions. Python/JavaScript may independently inspect SCAD-emitted witnesses, but may not construct the production surface.

Use periodicity in both u and v to generate one small developed template for `u=[0,1], v=[0,1]`, with the same plateau/four-ramp partition, ramp midpoint split, cleanup and positive-area ownership. Reuse that template across circumferential sectors and full axial rows. Clip only the finite partial first/last rows and the bounded terminal chamfer intervals; create the few required boundary templates once per source evaluation. A shorter-than-one-row band has one clipped template. Do not clip every interior cell from scratch or scan a broad square of rejected cells.

Classify template vertices as corner, horizontal-edge, vertical-edge or interior. Sort/identify the small local edge lists deterministically, and assign global indices by row/sector offsets and local ordinals. Shared row/sector boundaries have one owner and one point evaluation; circumferential sector N maps to sector0. Boundary-template interfaces use the same ordered interface point list. The existing1e-10 developed-coordinate equivalence and coordinate quantization remain; do not merge merely nearby XYZ points to hide disagreement.

Local lookup within one bounded template is acceptable. No `search`/first-occurrence scan may traverse a list proportional to full body/cap height or total component vertices for every point/face. Any cumulative offsets must be constructed once, not recomputed by repeated prefix scans inside the face loop. Full data construction should scale with emitted vertices/faces, plus bounded local-template work. Record template counts, maximum local registry size and whole-part point/face counts in the cheap probe.

Connect unequal outer/inner ring samplings with an angularly ordered annular triangulation. Keep the field boundary vertices and the96 internal vertices; do not force the96 bore faces onto every outer row. Emit every edge exactly once on each adjacent surface. Handle matching angles and wrap deterministically; no degenerate wedge, missing annular sector or duplicate seam face is permitted. Planar end/floor disks may use one center fan each. Bore/root walls need only their actual profile transition rings, not thousands of axial pattern rows.

## Triangle reduction with the same error threshold

Keep every original field breakline and every successful constant-u ramp bisection. Replace a polygon-center fan by a deterministic constrained triangulation using its existing perimeter vertices. For a cleaned positive-area convex polygon with m boundary vertices, use m-2 nondegenerate triangles. An ear method must skip zero-area ears, retain required collinear boundary subdivisions and reject an ear that skips another perimeter vertex. Do not delete collinear perimeter vertices from only one neighbor. Work on the bounded templates, not on a whole-component polygon.

At default a0.18, each ramp bisection creates one triangle and one pentagon. The current center fans cost3+5=8 triangles per ramp and4 per plateau: **36 per complete diamond cell**. Constrained triangulation costs1+3=4 per ramp and2 per plateau: **18 per complete cell**. This exactly halves the complete-cell contribution while preserving its coordinates and field partition. Clipped boundary/trim/annulus counts are additional and must be counted;18 is not a blanket assertion about every clipped cell.

Before cylindrical embedding, require that every triangle lies within one affine field or cone patch. Retain the VFR-04R per-triangle bound, with radians converted explicitly when evaluated in SCAD:

```text
delta = max(unwrapped theta_i)-min(unwrapped theta_i), 0 <= delta < PI/2
Rmin = min(radius_i) > 0; Rmax = max(radius_i); Dr=Rmax-Rmin
L = depth*N/(2*PI*(0.5-a))
E = Rmax*(1-cos(delta/2))
    + L*atan((Dr*delta/4 + Rmax*delta^3/6)/(Rmin*cos(delta)))
    + 0.000002 mm
require E <= 0.025 mm
```

Using the conservative full-depth radius range, default bisected-ramp span0.25u gives **E<=0.007739064 mm**; plateau span0.36u with Dr0 gives **E<=0.011859618 mm**. Removing polygon centers does not increase those allowed spans. Independently sample the new triangles; the older4,956-triangle STL is evidence for the field, not acceptance of the new triangulation. The trim oracle is `min(field,q)` and includes crease witnesses; field-only error must not be applied inside the intentional chamfer.

A simple area estimate gives about1,856.25 full-cell equivalents for the135 mm body, so its interior field contribution changes from about66,825 to33,412.5 triangles before finite-boundary additions. These are design estimates, not generated integer counts or timing results. Retain the250,000 exterior-triangle cap and existing preflight domain. Compute a conservative template/count bound before full point allocation, then record actual counts including terminal patches. A more efficient estimator must not silently expand the enabled browser domain or remove an existing invalid-job gate.

## Exact delta mask for the implementation task

Root must freeze this document, current permitted write targets, runtime lock and relevant baseline evidence in a new implementation manifest before editing. Paths below are project-relative; this design does not itself authorize any additional worker to write them.

| Object/path | Allowed delta | Protected / forbidden |
|---|---|---|
| `openscad/laifen_case_customizer_v1.scad`: diamond facet helpers/data | Bounded periodic templates; direct indices; conforming m-2 triangulation; trim clipping; finite count estimator; hidden diagnostic probes. | Named field/count/wrap/global-frame formulas and defaults;0.025 bound;1e-10 developed equivalence;250000 cap; no imported or host-generated surface. |
| Same source: positive-depth diamond body | One directly closed boundary with outer wall, trim, shoulder, root neck, inner bore and floor; union original helix; subtract original selected drains. | All analytic internal dimensions,96-sided polygon datums, floor3, shoulder S, helix source/placement, drainage code/placement, body height and role. |
| Same source: positive-depth diamond cap | One directly closed boundary with outer wall/trim and effective piecewise inner void/floor; subtract original female helix and selected drains. | Actual +0.01 cavity endpoint, active interval union, entry-relief cone, root/clearance/profile/engagement, drain code and placement, cap height/local datum. |
| Same source: smooth/depth-zero and output dispatch | A conditional branch may route positive-depth diamond to the new role wrappers; hidden probes select the same pure data. | Exact existing smooth/depth-zero geometry path and four public output transforms; no new public outputs or motion. Preserve existing smooth envelope/cutter modules even when diamond no longer calls them. |
| `tests/test_openscad_customizer.py`; optional focused `tests/test_openscad_direct_shell.py` | Replace obsolete implementation-string assumptions with executable common-caller, profile, topology/index and budget witnesses; add only risks introduced above. | Existing field, smooth, split/thread, rejection and source-authority coverage. Do not make a new wrapper string substitute for actual geometry evidence. |
| `openscad/customizer_contract.py` | Only an independently derived conservative allocation estimate if the old estimate no longer safely bounds the direct construction. Prefer unchanged. | No geometry generation, public parameter/radius/profile/field change, threshold reduction or domain expansion. |
| New `scratch/vfr05-implementation/` and `openscad/generated_vfr05/` | Exact-source private probes, timings, logs, candidate part outputs and compact manifests, assigned to the sole implementation owner. | Preserve old failed/passing evidence and old output namespaces; never edit STL vertices/faces after export. Scratch remains non-release evidence. |
| Every browser/schema/worker/HTML/CSS/vendor/lock, preserved CAD/R7 artifact, hosting/service, unrelated project and continuity namespace | Read only in implementation unless root separately freezes a later task. | Diamond stays disabled in the served UI; smooth preset, job identity, stale/cancel/error/download behavior,180000 ms watchdog, pinned engine and protocols unchanged. No publishing, MakerWorld, printer, slicer, Tailscale or public-Funnel action. |

## Staged gates, checkpoints and retry ceiling

This is a newly frozen implementation task with **one initial attempt plus one focused repair**. A timeout, failed analytic/mesh gate or rejected protected-geometry check consumes the corresponding attempt; moving the output path does not reset the budget. The architect performed no generation or browser timing. Prescribed future gates:

| Gate / checkpoint | Evidence and done condition |
|---|---|
| V05-0: provenance and protected-region freeze | Verify the new input fingerprint, snapshot the current SCAD baseline for smooth/protected-surface comparison, retain original module/parameter hashes and runtime lock hashes. Stop on drift. |
| V05-1: cheap executable math and data | Existing focused pytest command plus exact pinned-SCAD probes. Retain N33, field/phase/split witnesses, all invalid-job gates and depth-zero behavior. Emit compact checksums/counts that force evaluation of the production point/index arrays; inspect SCAD-emitted arrays independently for repeated indices, positive triangle areas, one connected closed boundary, opposite directed edge use exactly2, no unused/duplicate shared seam indices and finite allocation. For an uncut closed cup expect Euler2; later drain topology follows actual cutters. Verify both analytic profiles, trim crossings, shared seam point set and unrotated96-sided internals. No Manifold part generation on failure. |
| V05-1T: front-end cost checkpoint | Time production mesh-data construction separately from solid evaluation, using hidden stats/checksum probes and a trivial witness output. Default full-body data must complete within a10-second diagnostic ceiling; output only compact stats. If not, stop before G2/full-body and use the one repair only for an identified indexing/template cost. This tighter internal checkpoint preserves the existing acceptance budgets. |
| V05-2: changed tessellation G2 | Regenerate the same full-circumference7.13 mm witness at global131.93..139.06 with the pinned Manifold engine, within30 seconds. Require positive volume, one watertight/winding-consistent component, edge use2, no degenerate triangles, analytic maximum<=0.025 and measured maximum<=0.025. Reuse seed404 and at least3 triangle-interior samples per outer triangle; add all edge midpoints/centroids and wrap/split/trim-crease witnesses as applicable. Record worst point, triangle/facet provenance, max/p99/mean, counts and hash. |
| V05-3B0: direct body before small operations | After G2 passes, generate the full direct body without helix/drains through a hidden probe, with a20-second diagnostic ceiling. Check trim, shoulder, bore, floor, root and topology. Record front-end/Manifold/export time when distinguishable. This isolates the new closed-boundary cost; failure stops the actual-body run. |
| V05-3B: default body | Use the unchanged actual browser worker privately with the exact source, diamond parameters and body output. Fresh probe/runtime/result delivery included: cold end-to-end<=60 seconds. Require valid nonempty actual bytes, positive one-component mesh, winding/watertightness, preserved constraints and sampled surfaces. Inspect the result after helix/drain operations. A body failure stops cap. |
| V05-3C: default cap | Only after body passes, apply the same direct-blank<=20-second isolation and actual-worker<=60-second cap gate. Verify effective inner-profile union, +0.01 floor endpoint, relief maximum, thread valley wall, groove, selected drains and seam boundary. |
| V05-3P: protected-surface and scope join | Compare smooth and depth-zero output against the frozen smooth baseline by geometry, not hash alone. Preserve source-defined internal surfaces and selected Boolean cutter intersections. Existing mesh-sampled dimension tolerance remains at most0.05 mm; outer field/trim error remains<=0.025. Body/cap nominal valley walls remain4.05/3.55; female-groove wall1.90; relief wall2.00 at defaults. Measure the actual final meshes and declare serializer/tessellation uncertainty. Require preflight rejection of default-depth0.60 thread-wall violation. Freeze source/parameter/runtime/artifact manifest for independent roles. |

Existing cheap regression command from repository root:

```text
uv run pytest projects/laifen-wave-case/tests/test_openscad_customizer.py \
  projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
```

Add the focused direct-shell test only if created. Freeze exact probe/harness commands with output mode, parameter set, runtime fingerprints and deadlines in the implementation receipt; the existing `run-wasm-export.mjs` is a Node WASM smoke harness, **not the browser worker**: it omits the worker's cube probe, second fresh runtime and byte-message delivery. Its timings are prerequisite evidence only and cannot pass the browser end-to-end gates.

One repair may address a diagnosed local index/interface, triangulation or timing defect within this mask. For example, retain a center fan only for a particular clipped polygon class if it is necessary for conformity and the resulting measured budget still passes; keep the smaller complete-cell triangulation. It may not revert to global searches, add a cavity Boolean, alter field/internal geometry, remove a required operation, raise a timeout or start another speculative algorithm. Rerun the failed gate and only affected dependent gates on the new fingerprint. A second failure or an out-of-mask cause stops the task and returns the exact unresolved invariant to root.

After implementation, independent critic and validator may run against the same frozen candidate with disjoint read-only/evidence scopes; formal reviewer is their distinct-identity join. This architecture author does not approve its own implementation, and the implementer does not approve itself. Root schedules no more than three dependency-ready workers and one source writer. Use one bounded implementation workstream, modest output, a checkpoint after V05-1T/G2/first full-part result, and no broad parameter grid; exact runtime token controls are unavailable, so these are qualitative work/output ceilings in addition to hard geometry deadlines.

G4–G6 from `VFR04_DESIGN.md` remain required later: actual closed-pair intersection target<=1e-6 mm3 with allowed positive shoulder contact, exact assembled union, two-component print layout, native/browser surface parity, actual download-byte identity, controls/error/cancel recovery, and real mobile/delivery visual review. Assembled/print-layout deadlines remain120 seconds; UI watchdog remains180 seconds. This bounded VFR-05 task stops at the frozen body/cap candidate; it grants no G4/G5 run, browser enablement or delivery. No later stage can be waived by the new architecture.

## Authority, acceptance and stop conditions

Native OpenSCAD and browser WASM compile the same self-contained source with canonical parameter values and output transforms. Native/backend and browser/runtime identities are recorded separately. Changing triangulation is a source change and invalidates affected downstream mesh reviews; it does not authorize precomputed caches as replacement geometry. Native/browser serialization may differ; compare topology, bounds, volume and sampled surfaces under the existing tolerances. Three.js displays returned bytes, and the download must be those exact bytes. No independent procedural skin, displacement or artifact repair is allowed.

Stop immediately on input drift, missing executable-source witnesses, global unbounded lookup, unproven mesh allocation, repeated/multiply-used edges, self-intersection, lost floor/shoulder, incorrect bore/profile/phase, restored seam collar, changed smooth behavior, changed protected cutter, failed error/wall/contact/parity threshold, timeout, missing current result identity, required browser/protocol/runtime edits, or consumed repair budget. Do not hide a defect as a display concern or relax the selected B relationship.

Coverage: REQ-03/05 envelope and clearances; REQ-04 positive shoulder; protected REQ-06/07 threads; approved exterior update to REQ-08/09; REQ-12 parameter/source authority; separately pending REQ-10/11/13/14 artifact/process/physical evidence. Remaining physical unknowns include fit, force, wear, grip, strength, actual drainage, support-free slicing and exact identity of the reported printed reference. The inherited cap print-layout orientation gap remains unchanged. No new CAD/STEP, slicer/process or physical acceptance is claimed.

## Architecture receipt

Commands actually run by this owner:

- `shasum -a 256 projects/laifen-wave-case/docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/inputs/VFR05_ARCH_INPUTS.sha256` from the worktree root: expected fingerprint above.
- `shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/inputs/VFR05_ARCH_INPUTS.sha256` from the project directory: all16 entries OK. The first check was attempted from the worktree root; its relative paths were unresolved. Correcting the base directory resolved every entry; no input changed.
- Read the applicable repository instructions/CAD workflow, project state/next-agent/requirements/experience/decision index, active B/design/implementation records, exact source/oracle/tests/worker and the runtime lock. No stale continuity pointer was used over the recorded B decision or newer frozen source.
- Ran a read-only `node --input-type=module` here-document to enumerate the eight default ramp children and evaluate the published bound. Results: child sizes3,5,5,3,5,3,3,5; complete-cell triangulation36 to18; conservative bounds0.007739063046262273 and0.011859617661498782 mm; full-body/band height ratio18.934081346423564. This was an architecture calculation, not executable-SCAD or mesh validation.
- Read the official upstream OpenSCAD `builtin_functions.cc` implementation for list-search semantics. It is supplemental corroboration; the pinned WASM runtime must be measured through the prescribed probes.

The VFR-04 implementation evidence is `scratch/vfr04-implementation/G1.md` at `1bdf96791096a40f9c891644909af50ded378e35e5897ceb0836a42eb53217f2` and `scratch/vfr04-implementation/G2_G3.md` at `8df425e5f2cbdff6fa96e34691673708da07a193705d6daf1334d3f6893b608e`, including its final-cycle appendix. These were read as supplemental failure evidence; the named `VFR04_IMPLEMENTATION.md` delivery path was not produced. VFR-04R's receipt is already in the16-entry architecture manifest. Include the supplemental failure receipts and `preview/openscad-wasm-simulator/dependency-lock.json`/vendor hashes in the next task's immutable inputs.

No tests, full-body timing, mesh generation, browser actions or physical actions were performed by this architecture owner. Next action: root freezes this selected contract and the bounded implementation input manifest, then assigns one source owner to V05-0 through V05-3P under the stated one-attempt/one-repair ceiling.
