# VFR-06: periodic knot lattice and edge-owned clipping

Status: **ARCHITECTURE SELECTED FOR ONE BOUNDED IMPLEMENTATION; browser diamond remains blocked pending executable gates.**

Owner: `/root/openscad_vfr06_arbiter`, independent architecture arbiter. Project: `projects/laifen-wave-case`; iteration: `2026-09-04-openscad-visual-fidelity-recovery`; worktree: `/Users/scottchu/.codex/worktrees/4f8c/design-projects`. This document is the sole write. No source, test, generated artifact, browser, service, or continuity record changed.

Verified input manifest: `inputs/VFR06_ARCH_INPUTS.sha256`, SHA-256 **`18eb004c0d562ec12437e1e29177ac31abd86806c6d9b122099eaaf161d2d412`**; all **13** entries passed. Baseline SCAD: **`4e6ccd68f95d583d0c3b93bc33442d01107af90b5e66267bfe20034732e0d672`**. Read every listed document, source/oracle/test, JSON metric file, and the actual VFR-05A STL. The recorded user B decision is immutable.

## Decision and evidence boundary

Select a **globally conforming nonuniform lattice in `(s,t)`**, periodic under simultaneous integer translation, with a fixed diagonal per rectangle. Own every subsequent axial/trim intersection by its original lattice edge or original triangle. This replaces the patch-union/address-reconciliation architecture; it is not another repair of its H/V/I tables.

The field is affine on every base triangle by construction. Its default conservative radial-error maximum is **0.0133880671 mm** on field facets and **0.0201949975 mm** including the chamfer/field crease, both below 0.025 mm, without the former trapezoid/ramp midpoint subdivision. The conservative default exterior-wall allocations below are 59,400 body and 47,520 cap triangles; direct shell attachments leave both below 67,000 before the unchanged small Boolean operations. A bounded, in-memory mathematical witness closes the exact G2 interval with **3,168 triangles, edge use exactly two, opposite directed uses, one component, Euler 2**, and sampled maximum **0.0128863746 mm**. Separate trim and endpoint-coincidence witnesses also close.

These are sufficient evidence to select one source-feasible architecture. They are **not SCAD execution, Manifold acceptance, actual worker timing, or a body/cap candidate**. No available evidence proves the 60-second browser ceiling will pass. The representation removes the two source-evidenced growth hazards and has an output size comparable to the fast VFR-05A data experiment; performance remains a measured gate. If the bounded implementation cannot pass, the editable browser OpenSCAD diamond path is blocked under the current contracts. Do not renew this budget through another indexing amendment.

## Reconciliation of the preceding results

| Evidence | What it establishes | What it does not establish |
|---|---|---|
| VFR-04R G2: 4,956 triangles; 4.192 s; edge use 2; sampled error 0.007052 mm | The approved field and finite off-lattice band can produce a valid accurate surface. | Full-body speed. Two full-body attempts exceeded 60 s without an artifact; cap was not run. |
| Restored SCAD source | Full raw-key and unique-key scans occur for every vertex/face reference; the solid exterior also participates in envelope/cavity Booleans. | Which stage caused how much of the timeout. No stage-isolated full-body profile exists. |
| VFR-05A data checkpoint: 6.714 s; 18,018 outer points; 35,574 side faces | Bounded template work and approximately this output size are plausible within the front-end checkpoint. | Valid topology, final Boolean cost, or actual browser-worker timing. |
| VFR-05A repaired G2: 0.559 s; 2,838 triangles | Fast generation alone is possible. | A closed manifold surface. Independent exact-XYZ inspection found 252 edges used four times, 25 used six times, eight excess duplicate unoriented triangles, Euler -336, and no boundary edges. |

The last row is overcoverage as well as an edge-connectivity failure. Shared coordinate/index tables alone cannot remove duplicate area or ensure that neighboring polygons use the same edge subdivision. The new base lattice has exactly one owner for each rectangular cell and two prescribed triangles; clipping partitions each triangle's area once. Every crossing has a pre-existing edge/triangle address. No downstream welding or local patch matching creates connectivity.

## Frozen surface and protected geometry

Keep the original named field functions, half-up valley-derived count, parameters, validation/rejection domain and global mapping:

```text
N = floor(2*pi*Rvalley/target_arc + 0.5) = 33 at defaults
a = 0.18; Rcrest = 19.5; Rvalley = 19.05; depth = 0.45; P = 4.8
s = u+v; t = u-v
u = (s+t)/2; v = (s-t)/2
theta = phase + 360*u/N
z_global = S + P*v; S = 135 at defaults
body local z = z_global; cap local z = z_global-S
r_field = Rvalley + depth*diamond_field(u,v,a)
```

Body exterior ends at S; cap exterior begins at S. Both roles remain separate, with the same limiting seam ring and texture to both sides. There are no new collars. Preserve OD 39, bores 30/31, body/cap heights 144/84, shoulder, overlap 9, engagement 6, thread profile/placement/embed, all drain cutters/placements, output transforms and smooth/depth-zero branch. Preserve the actual cap bore end `H-floor+0.01`, hence 2.99 mm default floor. Physical fit, drainage and manufacturing remain unaccepted.

For diamond trim use the nominal envelope already selected in VFR-05:

```text
q_body(v) = Rcrest-chamfer + (S+P*v)
q_cap(v)  = Rcrest-chamfer + H-P*v
r_outer  = min(r_field, q_role)
```

No extra `min(Rcrest, q)` or horizontal chamfer-break subdivision is needed: `r_field <= Rcrest` makes this expression identical to the selected capped envelope. Equality with the affine q is sufficient to preserve every actual crease, including the plateau meeting the top of the chamfer. It retains the 45-degree slope, end radius, height and planes. The old 96-sided outer envelope has at most 0.010440545 mm circular chord deviation; retain the inherited <=0.05 mm protected-envelope parity gate and <=0.025 mm `min(field,q)` gate. This does not authorize a new chamfer dimension or tolerance.

## 1. Exact base lattice and triangles

Use positive modulo throughout. Define one knot sequence for both axes:

```text
K(p) = floor(p/3) + [-0.5, -a, +a][p mod 3], p any integer
K(p+3) = K(p)+1
M = 3*N
```

Each integer-centered field square now contains nine rectangular cells, with widths `0.5-a, 2*a, 0.5-a` on each axis. Knots hit both plateau edges and both valley boundaries exactly for any supported a; no rational approximation of a or tiny uniform sampling grid is used.

Cell `(p,d)` has `q=p+d` and these corners in counterclockwise `(s,t)` order:

```text
A = (K(p),   K(q))     = B(p,   d)
B = (K(p+1), K(q))     = B(p+1, d-1)
C = (K(p+1), K(q+1))   = B(p+1, d)
D = (K(p),   K(q+1))   = B(p,   d+1)
```

Use the B-to-D diagonal only if `(p mod 3, q mod 3)` is `(0,2)` or `(2,0)`:

```text
anti diagonal: [A,B,D], [B,C,D]
otherwise:     [A,B,C], [A,C,D]
```

The two opposite outer corner cells need the `s_local=-t_local` breakline. The two equal outer corner cells need `s_local=t_local`, supplied by the other diagonal. Cells with a middle strip have one dominant ramp coordinate; the middle/middle cell is the plateau. Thus no triangle crosses a field breakline. Every cell is owned once and tiled completely. There are **18 triangles per full field square**, equivalently 36 per unit `(u,v)` area.

The listed face order is the same `(s,t)` orientation as the passing baseline's SCAD facets. The `(s,t)->(u,v)` determinant is negative; those lists are inward under the ordinary right-hand XYZ normal convention and are supplied in the baseline's OpenSCAD polyhedron convention. Use one explicit reversal when converting a mathematical outward face list to SCAD, never role-dependent trial-and-error flipping. The exported mesh must independently have outward winding and positive volume.

### Finite axial support without an angular clipping seam

Let `v0 < v1` be the exact requested finite endpoints. Set:

```text
Dlo = floor(-6*v1)-3
Dhi = ceil(-6*v0)+3
R = Dhi-Dlo+1
p = 0..M-1; d = Dlo..Dhi
```

Keep only positive-area intersections with the axial strip. These are safe finite bounds: `K(p)-p/3` has range width less than 2/3 for `0<a<0.5`, so a cell that intersects the strip must lie within the stated d range. The constant margins include complete incident cells for every retained vertex and boundary edge. They do not grow with N or trigger a square search of irrelevant cells.

`(p,q)` and `(p+M,q+M)` identify one physical point. Reducing p modulo M keeps d unchanged, so no u=0/N clipping, angular seam polygons, endpoint search or XYZ merge is needed. The quotient of this triangulated strip is a cylinder. Keep unwrapped `(s,t)` within each local triangle for clipping and error calculations; canonicalize only its integer address and point evaluation.

## 2. Primitive addresses before clipping

The following formulas use M=3N and demonstrate the global integer identities. Every `p` in a formula is reduced modulo M; the indicated d domains are distinct blocks.

```text
vertex B(p,d) = M*(d-Dlo+1) + (p mod M)
    d = Dlo-1 .. Dhi+1                       # M*(R+2) slots

s-edge Es(p,d) = M*(d-Dlo) + (p mod M)
    d = Dlo .. Dhi+1                         # M*(R+1) slots
t-edge Et(p,d) = M*(R+1) + M*(d-Dlo+1) + (p mod M)
    d = Dlo-1 .. Dhi                         # M*(R+1) slots
diagonal Ed(p,d) = 2*M*(R+1) + M*(d-Dlo) + (p mod M)
    d = Dlo .. Dhi                           # M*R slots

triangle F(p,d,j) = 2*(M*(d-Dlo)+(p mod M))+j, j=0,1
```

Cell edges AB, BC, CD and DA reference `Es(p,d)`, `Et(p+1,d-1)`, `Es(p,d+1)` and `Et(p,d)` respectively. Both triangles reference `Ed(p,d)`. An s-edge connects `B(p,d)` to `B(p+1,d-1)`; a t-edge connects `B(p,d)` to `B(p,d+1)`. A diagonal uses the selected corner pair above. These formulas include all wraps.

### Compact implementation once per circumferential period

For actual SCAD allocation, compute templates with **M=3** in these same formulas and p=0,1,2. Scalar coordinates, clipping decisions and topology repeat under p/q plus three. A reference carrying arbitrary p becomes `r=p mod 3`, `k=floor(p/3)`; a p+1 crossing from r=2 to r=0 carries k+1. This sector carry is part of every vertex/edge/face descriptor and alias.

Let `VB=3*(R+2)`, `E=3*(3*R+2)`, `F=6*R`. Give template point slots these fixed disjoint blocks:

```text
base vertex       slot = B                       [0, VB)
axial cut 0       slot = VB+edge                 [VB, VB+E)
axial cut 1       slot = VB+E+edge
trim on edge      slot = VB+2*E+edge
trim on cut/face  slot = VB+3*E+2*face+cut        cut=0,1
polygon center    slot = VB+3*E+2*F+2*face+branch branch=field,cone
Q = VB+3*E+4*F = 54*R+24
```

An inactive or aliased slot has flag zero; an owned, used point has flag one. Build one exclusive prefix `rank[slot]` over these flags and evaluate each owned template point once. Global address:

```text
point_index(slot, k) = N*rank[slot] + positive_mod(k,N)
point_count = N*sum(flags)
```

Use the VFR-05A divide-and-conquer prefix recurrence once, with logarithmic recursion depth. This is O(Q log Q) bounded template list work; output assembly is O(emitted points+faces). At defaults Q is 9,528 for body and 6,072 for cap. No point or face scans a whole-component registry. Clipped polygon descriptors have bounded size, so local membership/cleanup is constant-bounded. Resolve aliases directly to their owner slot plus sector carry, not through coordinate-key discovery or long alias chains. Do not emit unused slots as points.

## 3. Clip edges once; partition triangle area once

For each original triangle, first intersect with `v>=v0` and `v<=v1`. Its scalar radius is affine. Define `h=r_field-q_role` at its vertices and interpolate that same affine h at crossings. Untrimmed G2 omits h. All clipping uses the existing 1e-10 developed-coordinate equivalence and final 1e-8 mm outer coordinate quantization; do not widen either.

1. **Original vertex:** keep its B owner if in the closed axial strip. Snap a value within the declared equivalence to the exact boundary. Both incident triangles use that same owner/evaluation.
2. **Axial cut through an original edge:** only a strict crossing creates `A(cut,edge)`. Calculate its interpolation from that edge's one canonically ordered endpoint pair. A cut at an endpoint aliases B. Parallel/coincident edges create no new crossing. Two different cut planes have separate slots, unless the input itself violates `v0<v1` after permitted snapping, which stops.
3. **Trim through an original edge:** only opposite strict h signs create `T(edge)`. Its single root is computed from the same canonical edge endpoints, then retained only inside the axial strip. A root at an original vertex aliases B; a root at an axial intersection aliases that A slot. An edge with h identically zero is an existing crease with its existing vertices, not a new coincident edge.
4. **Trim crossing an axial boundary segment inside one original triangle:** create `U(face,cut)` only for a strict interior crossing of that segment. Its endpoints already have B/A/T owners. A crossing at either endpoint aliases that endpoint, including its sector carry. This segment belongs to one original triangle's finite-strip boundary; no neighboring triangle independently owns an overlapping segment. A segment coincident with an original edge uses the original edge rules instead.
5. Split the clipped triangle into `h<=0` field and `h>=0` cone polygons **only when both strict signs occur**. If all h are zero, own it once as field. If there is one strict sign and some equalities, keep one polygon. Never emit the same positive area in both branches.

The only new intersections possible are original-edge/plane or triangle-interior intersection of the axial plane with the trim line. Parallel axial planes cannot create another class. Thus these fixed slots cover arbitrary off-lattice endpoints, trim/edge/corner coincidences and all remaining boundary events. There is no H/V/internal patch boundary union to reconcile.

Maintain original cyclic ordering and canonical descriptors during clipping. Remove repeated adjacent/cyclic aliases; reject nonconsecutive repeated owners or disagreement outside the declared equivalence. Do not remove a collinear point belonging to an edge subdivision. Keep a positive-area three-vertex polygon as one triangle. For a polygon with at least four distinct boundary vertices, create its one interior arithmetic center C, evaluate the selected affine radius there, and emit `[C, p[j], p[j+1]]`. This preserves every edge segment and cannot create a zero-area fan when the convex polygon has positive area. No polygon has more than six vertices after the three half-plane cuts; there is no unbounded triangulation routine.

Every shared original edge is partitioned by the same ordered B/A/T owners on both incident triangles. Every new trim chord has its two incident branches inside the same original triangle. Every retained axial segment has exactly one side face and exactly one later closure/annulus face. Those local facts prove combinatorial conformity, including the circumferential wrap. They also explain why removing boundary edges alone was an insufficient VFR-05A gate.

Reject collapsed XYZ triangles after quantization, nonpositive Jacobian/area, vertex-link defects, self-intersections or any required merge beyond tolerance. An endpoint is not required to lie on the lattice; parameters that collapse distinct geometry under the existing precision remain unvalidated and stop, rather than silently becoming a coarser grid.

## 4. Endpoint rings and direct role boundaries

Obtain each axial endpoint's directed segments from the original triangles that intersect that plane, including any U split. This is a bounded scan of its constant-width d neighborhood, not a full-point lookup. Reference the exact side point descriptors. Never recompute a separate ring from approximate samples.

Within the M=3 template, gather distinct endpoint owners and normalize each template point's unwrapped u to `f=u-floor(u)` in `[0,1)`. Store its descriptor with sector carry `-floor(u)`. Sort this small scalar list by f once and require a single ordered cycle after N repetition. An equivalent scalar with a different nonalias owner is an error. Ring vertex `(k,t)` references its stored owner at `k+carry[t]`; its actual angle is `phase+360*(k+f[t])/N`. This is a ordering operation for the closure only; it cannot alter side topology.

At the body/cap seam, invoke this same role-independent procedure at **v=0 without trim**. The limiting exterior is untrimmed for both roles. Normalize start/order and require identical final quantized XYZ point sets. Their local array offsets can differ; their coordinates, neighboring side subdivisions and role-independent phase cannot. Do not include either role's finite opposite endpoint when defining this seam table.

### Exact 96-sided internal rings and annular zipper

Append every required internal profile ring once after the outer point block:

```text
I(ring,j) = outerPointCount + 96*ring + j, j=0..95
XYZ = [radius*cos(360*j/96), radius*sin(360*j/96), profile_z]
```

Keep these coordinates in the original unrotated physical datum; diamond phase affects only outer coordinates. Allocate disk centers after the ring block. Each ring is shared by its two neighboring wall/annulus surfaces. No side point or internal ring is duplicated for attachment.

For an annulus, order the outer ring O and inner ring I by physical angle. Start with an outer vertex O0 and the inner vertex whose angle immediately precedes or equals O0. Unwrap both cycles over one revolution. At current i,j compare the next angles:

```text
next outer smaller: emit [Oi, O(i+1), Ij]; advance i
next inner smaller: emit [Oi, I(j+1), Ij]; advance j
equal next angles:  emit [Oi, O(i+1), Ij] and [O(i+1), I(j+1), Ij]; advance both
```

These lists are right-hand +Z; reverse them for -Z, and perform the one declared conversion to the SCAD convention. Once one ring has advanced its full count, treat its next event as positive infinity; stop when both have advanced exactly their vertex counts. The closing bridge is the original bridge with wrapped indices, not a new seam face. There are exactly `len(O)+len(I)` triangles; equality makes a two-triangle quadrilateral with distinct radii, never a collapsed wedge. If every angle matches (e.g. two 96 rings), the same rule gives the ordinary pair of triangles per quad.

Check the generated 2D annulus for crossed bridges and correct containment. The default radii/angle gaps have ample margin: `Rinner_max < Router_min*cos(maximum bridge angle)` is a cheap sufficient margin check for the local radial bridges here. Preserve both original polygons even when their angular samplings differ. Do not rotate internals to make zipper indices easier.

### Body, before retained helix/drain operations

Connect exactly this ordered boundary:

- outer bottom disk at z=0, using the clipped bottom ring;
- patterned/chamfered outer side to S;
- +Z shoulder annulus at S from seam ring to root radius;
- root wall S to body height;
- +Z opening annulus at body height from root ring to bore ring;
- inward bore wall down to `floor_thickness`;
- +Z cavity floor disk.

The outer bottom disk faces -Z. Use two triangles per internal cylinder quad with the required outward/inward orientation. This is one directly closed cup, not solids touching only at S. Union the exact unchanged male helix at `S+thread_transition`; subtract the unchanged selected drain cutters.

### Cap, before retained groove/drain operations

Connect outer side local z=0..H, +Z top disk, -Z open-rim annulus, inward stepped bore profile and -Z cavity floor disk. Let `Rrootc=thread_root_radius+thread_clearance` and `Zc=H-floor+0.01`. The nonhelical void profile is exactly:

```text
0..0.4:     max(Rcap, Rrootc+0.4-z)
0.4..overlap: max(Rcap, Rrootc)
overlap..Zc: Rcap
```

Include `z=0`, `0.4`, `overlap`, `Zc` and any cone/bore equality `z=Rrootc+0.4-Rcap` strictly inside 0..0.4. At an actual step, allocate both radii at the same z and connect by an annulus. Deduplicate only identical `(radius,z)` profile entries and omit zero-area profile segments; this list has fixed small size. Preserve the 96-sided profile at every level. Defaults are `(17.05,0)`, `(16.65,0.4)`, `(16.65,9)`, `(15.5,9)`, `(15.5,81.01)`. Subtract the unchanged female groove at `thread_transition` and unchanged selected cap drains. The actual profile union, not a presumed radius ordering, is the authority for nondefault inputs.

## 5. Accuracy, allocation and cost

Within any field triangle, retain the VFR-04R bound, in radians:

```text
delta = max(theta_i)-min(theta_i); Dr=Rmax-Rmin
L = depth*N/(2*pi*(0.5-a))
E = Rmax*(1-cos(delta/2))
    + L*atan((Dr*delta/4 + Rmax*delta^3/6)/(Rmin*cos(delta)))
    + 0.000002 mm
```

The bound includes radius-dependent angular interpolation; a chord bound alone is insufficient. Axial clipping/trim and polygon centers stay inside their original triangle, so they cannot enlarge its angular span. Default outer/outer ramp span is <=0.32u; mixed ramp span <=0.34u; plateau span <=0.36u. Their conservative bounds are 0.0119977393, **0.0133880671**, and 0.0118502315 mm respectively.

Use the **same full angular-shift bound on cone children near the crease**. Although q depends only on v and z interpolates exactly, the physical `atan2` angle may move across the field/cone boundary; the target there may be field rather than q. The global angular Lipschitz constant of `min(field,q)` is at most L, so the full formula remains valid. With conservative cone values `span<=0.36u`, `Rmin=18.3`, `Rmax=19.5`, `Dr<=1.2`, it gives **0.0201949975 mm**. The cone-only chord value 0.0114528829 mm is insufficient unless remaining inside the cone region is separately proved. This correction closes that accuracy gap without changing geometry or thresholds. Every generated triangle lies within one branch in developed space; the bound covers the subsequent physical-angle shift.

Compute the maximum from actual production triangle data; stop above 0.025 mm. Nondefault a/N/depth combinations retain the old preflight and require this actual bound; this design does not expand the enabled parameter domain. The old midpoint split addressed wide trapezoids. This new exact knot partition has smaller angular spans by construction, so removing that implementation detail does not change B or relax accuracy.

For an interval `[x,y]`, define:

```text
rows(x,y) = ceil(-6*x)+3 - (floor(-6*y)-3) + 1
T(x,y) = 6*N*rows(x,y)
```

`T(v0,v1)` bounds all enumerated base triangles, including rejected support. An axial cut touches at most `T(b,b)` of them. A clipped polygon without trim costs <=5 triangles; two trim branches together cost <=9. The trim can only cross where `q` lies between Rvalley and Rcrest, intersected with the role's domain. If that axial interval is `[c0,c1]`, a conservative exterior-wall bound is:

```text
Twall <= T(v0,v1) + 4*(T(v0,v0)+T(v1,v1)) + 8*T(c0,c1)
```

Use zero for the last term if the trim interval is empty. This deliberately double-counts overlaps. At defaults:

| Role | v interval | Base triangle bound | Trim v interval | Wall bound |
|---|---:|---:|---:|---:|
| Body | -28.125..0 | 34,848 | -27.96875..-27.875 | 59,400 |
| Cap | 0..17.5 | 22,176 | 17.25..17.34375 | 47,520 |

An endpoint ring has at most `2*T(b,b)` vertices, allowing one trim split per original boundary segment. Add its actual disk/zipper counts and the small fixed 96-ring profile counts before allocating. These bounds put default direct body below 66,108 and direct cap below 54,024 triangles. Final helix/drain Booleans may change counts; require the actual final exterior to remain <=250,000. Keep the old rejection estimator as an additional guard unless a separately frozen task explicitly permits its conservative replacement; do not silently enable larger jobs.

The selected data construction has no quadratic component-wide search and no cavity/envelope Boolean. Its template size scales with axial rows and its placement cost with output. That is an algorithmic argument and an allocation bound, **not a wall-clock guarantee**. The VFR-05A 6.714-second checkpoint is useful scale evidence; it is not a benchmark of this algorithm or of the real browser worker.

## 6. Bounded proof actually performed

Ran a read-only `node --input-type=module` stdin calculation of the lattice, primitive identities, clipping ownership, center fans and endpoint closures. It constructed only mathematical short-band arrays in memory, wrote no mesh, imported no production mesh and used no SCAD engine. Canonical B/edge/F identities, not rounded XYZ, keyed shared points. The final outer coordinate calculation used the existing 1e-8 mm quantization. Results:

| Mathematical witness | Vertices | Side / closed triangles | Edge use | Euler / components | Minimum area mm2 |
|---|---:|---:|---|---|---:|
| Exact G2, global 131.93..139.06 | 1,586 | 2,706 / 3,168 | 4,752 edges, all twice | 2 / 1 | 0.000658837826 |
| Same finite band with 1.2 mm bottom trim | 2,048 | 3,630 / 4,092 | 6,138 edges, all twice | 2 / 1 | 0.000658837826 |
| Coincident lattice endpoints v=-0.5..0.5 | 695 | 1,188 / 1,386 | 2,079 edges, all twice | 2 / 1 | 0.497878863310 |

All three had zero wrong directed edge pairs, zero canonical-ID XYZ disagreement, and no repeated-index/zero-area faces. The maximum affine field centroid discrepancy was 7.11e-15 mm. The untrimmed per-triangle analytic maximum was 0.0133880671 mm. The initial trim witness reported the same maximum using a cone-only chord term; final arbitration identified that term's crease-crossing limitation and superseded it with the conservative **0.0201949975 mm** bound derived and evaluated above. No geometry changed. All edge midpoints and triangle centroids were compared at physical `(atan2,z)` against the independent mathematical field/trim; measured maximum was 0.0128863746 mm. Exact G2 endpoint cycles each had 231 vertices; the coincidence case had 99 each. This supports the indexing/partition argument and catches the preceding multiply-used-edge failure in the small model.

The in-memory witness used a JavaScript map from declared primitive IDs to inspect incidence. **SCAD production must use the numeric slot/prefix formulas above**; the map is not a permitted production substitute. Its proof is bounded to these short cases. Actual SCAD-generated arrays, compaction aliases, annular connections, trim coincidence classes, actual final solids and runtime remain mandatory independent gates below.

Other exact commands run, from the project directory unless stated:

```text
shasum -a 256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/inputs/VFR06_ARCH_INPUTS.sha256
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/inputs/VFR06_ARCH_INPUTS.sha256
```

Both returned the expected fingerprint/all 13 OK. Repository-root `uv run python -B -` read the manifest-listed failed STL, parsed its actual triangles, assigned exact-XYZ vertex indices and counted undirected edges/duplicate faces: 638,468 bytes, 781 vertices, 2,838 triangles, edge histogram `{2:3678,4:252,6:25}`, Euler -336, eight excess duplicate unoriented faces, no repeated-index triangles. No STL cleanup, tolerance weld, serialization or repair was performed. Separate `node --input-type=module` stdin arithmetic evaluations produced the knot/error/row bounds and the corrected cone/crease bound above. No tests, full body/cap mesh construction, Manifold generation or browser action ran in this arbitration.

## 7. Implementation gates and nonrenewable budget

Root must freeze this decision with the restored source, prescribed runtime/harness and protected-region hashes. Assign one implementer, then distinct critic, validator and formal reviewer identities. This decision grants no UI enablement, browser/protocol edit or delivery. One initial implementation attempt plus **one focused repair total**; a timeout or failed candidate gate consumes that attempt. Stop on a second failure, an out-of-contract correction, stale fingerprint or an unbounded algorithm.

| Gate | Required evidence and stop rule |
|---|---|
| V06-0 provenance / cheap regression | Verify inputs and protected byte ranges. Preserve all current field, split, smooth/depth-zero, thread, drainage and rejection checks. Run the existing two-file focused pytest command from the repository root. No geometry on failure. |
| V06-1 executable SCAD data proof | Implement pure mesh-data functions used by both production roles and private probes. Independently inspect their actual emitted point/face arrays for the exact G2 band, its trimmed counterpart, and the v=-0.5..0.5 coincidence case. Verify numeric slot/sector carry aliases; index ranges; no unused/shared duplicate point owners; no repeated faces or indices; all edges twice/oppositely directed after closure; each vertex link one cycle; one connected sphere topology; nonzero areas; no T-junctions/self-intersections. Verify every triangle stays inside one affine field/cone patch and actual analytic error <=0.025. Production code, not a host-language duplicate, must supply the arrays. A cheap failure stops before Manifold. |
| V06-1 boundary/annulus join | Through the same data functions, check h equality at an original vertex, along an original edge, at each axial cut and strictly inside its triangle, plus coincident plateau/trim equality. Check body/cap v=0 ring equality and physical-angle zipper with unequal rings, equal-angle events, wrap, and a nonzero diamond phase while internal 96 rings retain their datum. Check body/cap direct boundary profiles and exact floor/shoulder orientation. Use bounded fixtures/data, not full part exports. |
| V06-1T front-end cost | Force evaluation of production default full-body arrays with compact counts/checksum, no giant log. <=10 s; record template Q, active point/face counts, allocation bound and no-global-search inspection. A failure consumes the attempt and stops before G2. |
| V06-2 real G2 | Same 7.13 mm full-circumference band at global 131.93..139.06, pinned WASM Manifold, <=30 s. New STL: one positive-volume watertight/winding-consistent component, edge use 2, no degenerates; actual field error <=0.025 and analytic bound <=0.025. Reuse seed404, >=3 triangle-interior samples per side triangle, plus midpoints/centroids and wrap/endpoint witnesses. Record max/p99/mean, count, worst triangle/point/provenance, hash and timing. The mathematical witness above cannot pass this gate. |
| V06-3B0 direct body | Only after G2 passes, full direct body before retained helix/drains, <=20 s. Verify actual topology, outer trim, bottom disk, shoulder, root, bore and floor. Record distinguishable front-end/Manifold/export times. Failure stops actual body and cap. |
| V06-3B actual body worker | Exact existing browser worker privately, fresh probe/runtime/compile/byte delivery included, cold end-to-end <=60 s. Require the final mesh after unchanged helix/drains, actual topology, dimensions/walls/protected geometry, exterior error <=0.025, parity <=0.05 and exterior triangles <=250,000. Node smoke-harness time is insufficient. Body failure stops cap. |
| V06-3C direct and actual cap | Only after actual body passes: direct cap <=20 s, then unchanged actual worker <=60 s, with the same final-mesh gates and exact effective bore/entry relief/2.99 mm floor/groove/drain checks. Recheck the actual pair's seam boundary. |
| V06-3P freeze and independent join | Compare smooth/depth-zero against the restored baseline by geometry and protected source; preserve the 0.60-depth rejection. Freeze source/parameters/runtime/artifact hashes. Independent critic and validator inspect this same candidate; a distinct formal reviewer joins coverage and finding dispositions. No implementer self-approval. |

Existing regression command:

```text
uv run pytest projects/laifen-wave-case/tests/test_openscad_customizer.py \
  projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
```

The one repair may address one diagnosed local formula/alias, finite clipping, fan/zipper or avoidable template evaluation defect within this selected architecture. Rerun the failed gate and affected dependent gates on the new fingerprint. It may not replace the lattice, resurrect patch-boundary reconciliation/global searches, add the removed full cavity/envelope Boolean, change B/protected geometry, increase subdivision repeatedly, relax a threshold, extend a timeout, import host geometry or alter the worker. If a second candidate failure occurs, explicitly record **browser OpenSCAD diamond blocked under the 0.025 mm / 60 s contracts**, with its precise failed invariant and preserved evidence.

Later assembly/contact, two-component layout, native/browser parity, exact download bytes, cancellation/stale-state behavior and actual user delivery-surface review remain required as already stated in VFR-05. They are not part of this bounded implementation authorization. CAD/STEP, written artifact/slicer and physical acceptance remain separate and pending.

## Receipt and next action

- **Status:** complete architecture arbitration; one implementable representation selected; no candidate accepted.
- **Verified fingerprint:** `18eb004c0d562ec12437e1e29177ac31abd86806c6d9b122099eaaf161d2d412`, 13/13 files verified.
- **Changed path:** this decision only. No protected source or artifact changed.
- **High finding resolved at design level:** VFR-05A dynamic patch conformity/overcoverage is replaced with a complete nonoverlapping base triangulation and edge-owned cuts; bounded mathematical witnesses pass.
- **High risk still open:** actual SCAD compaction/alias fidelity, final small-Boolean topology and <=60 s actual worker generation are unmeasured.
- **Requirement coverage:** B/count/plateau/shared seam/part identities; finite endpoints/wrap/trim; direct shell/96-ring internals; error/allocation/source authority; preserved protected geometry and smooth branch. Browser, native/export, assembly/contact and physical gates are explicitly pending.
- **Next action:** root freezes this document and the bounded implementation task, then assigns one source owner to V06-0 through V06-3P with the one-attempt/one-repair ceiling. Browser diamond stays disabled until the later independent and delivery gates pass.
