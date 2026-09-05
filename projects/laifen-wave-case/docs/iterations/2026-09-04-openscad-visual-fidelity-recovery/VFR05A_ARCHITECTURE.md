# VFR-05A: explicit OpenSCAD addresses for clipped boundaries

Status: **INDEXING AMENDMENT SELECTED; executable data, geometry and timing gates pending.**

Owner: `/root/openscad_vfr05_architect`, architecture/design only. Sole write: this document. Worktree `/Users/scottchu/.codex/worktrees/4f8c/design-projects`; project `projects/laifen-wave-case`; active iteration `2026-09-04-openscad-visual-fidelity-recovery`.

Verified `inputs/VFR05A_ARCH_INPUTS.sha256`: **`45d46516969628800e50c20738e5f3c4d2a6ea30e4e556cc18db0e7e871ec238`**; all seven project-relative entries passed. The source is restored to `4e6ccd68f95d583d0c3b93bc33442d01107af90b5e66267bfe20034732e0d672`. This amends only the addressing and clipping representation in `VFR05_ARCHITECTURE.md` at `5d3f83f2f57bca53d95bb26c9a7709a5cfee448a4b40e378f392c598123b6798` and its implementing task. All other VFR-05 architecture, dimensions, B field, direct annular solids, protected operations, thresholds, authority and gates remain in force.

## Checkpoint disposition

`scratch/vfr05-implementation/CHECKPOINT.md` at `634ffc774c29ebf146ad1f0f651573fbd120c099ced419ef40ceff3a36d34647` correctly stops before candidate G2/G3. The1.418-second open-surface experiment is noncandidate. The retained `duplicate-polyhedron.scad` at `402c8b55b6acaf5686bfe0ec8aa6179b845c0eaedcc466f73a295fb4d12ea7dc` uses different indices for coincident positions; it cannot establish the required shared-index topology. Do not use downstream Manifold welding as the indexing algorithm.

The original architecture did not fully specify the ordinals for arbitrary clipped vertices. The correction is **numeric local tables with four explicit global index classes**. It needs only SCAD lists, local comparisons, comprehensions, recursion and arithmetic. No map/dictionary, unavailable library, global string registry or external mesh generator is required.

## 1. Finite row templates

Let N be the unchanged circumferential repeat count. Partition the exterior's global-v interval into ordered boundaries `b[0] .. b[J]`. Include its exact first/last v, all intervening integers, and the required horizontal chamfer/profile break levels from VFR-05. Snap only within the existing1e-10 developed-coordinate equivalence; keep the actual off-lattice endpoint values. Remove equivalent consecutive boundaries and require `0 < b[j+1]-b[j] <= 1`.

Row j contains N rectangular tiles:

```text
tile(j,k): u = k+x, 0 <= x <= 1; v = b[j] .. b[j+1]
k = 0 .. N-1
```

Construct one local polygon template for a row class in `x=[0,1]`. The field is periodic under integer u shifts, and the trim envelope depends on z, so every circumferential sector in this row has the same developed template. Full untrimmed integer rows reuse the same topology shifted in v; partial or trimmed rows get their own finite local template, evaluated once and then reused for all N sectors.

Within that local template retain the R7 cell partition, ramp midpoint split, exact facet/trim clipping, cleanup and conforming n-2 triangulation. An arbitrary trim intersection is an ordinary point in the template's numeric vertex list. Its address comes from a bounded local ordinal below; it need not have an integer lattice formula.

**Per-cell clipping is permitted and necessary for cells that cross a boundary.** The original prohibition meant to prevent redoing the entire full-body clipping/lookup computation for every placed tile. It does not prohibit clipping cells while creating a finite unit template, an off-lattice first/last row, a chamfer/trim interval or the angular template boundary. Test the cell support first, copy wholly inside unchanged patches, and clip only crossing patches. Repeated interior tiles use the completed template; do not rerun its cell clipping for each `(j,k)` instance or scan a component-wide square of irrelevant cells.

## 2. Form shared boundary tables before assigning faces

Template polygons initially retain their closed geometric support, including x0/x1 and both v endpoints. Clean cyclic duplicates using the existing tolerance. Tables contain numeric coordinates, not formatted XYZ strings.

Build these local tables, ordered increasingly by their scalar coordinate:

- `H[j]`: x values strictly inside0..1 on horizontal interface `v=b[j]`. Take the union of all vertices supplied by the row below's upper edge and row above's lower edge; at an exterior endpoint use the existing incident row. Endpoints x0/x1 belong to corners and are excluded from H.
- `V[j]`: v values strictly inside`b[j]..b[j+1]` on a tile's vertical edge. Take the union of the local template's x0 and x1 edge vertices. Periodicity makes this the shared table for both edges and every sector in that row. Its endpoints belong to corners and are excluded from V.
- `I[j]`: distinct numeric pairs `[x,v]` strictly inside the tile, after boundary conformity. These include interior trim intersections and any other permitted interior vertex. Give them deterministic local ordinals, for example lexicographic coordinate order with stable polygon provenance as a tie-breaker.

Before triangulation, insert every value of H and V into **both incident polygon boundaries** wherever it lies on an existing edge. Sort inserted vertices along that edge. Index sharing alone cannot repair a long edge that skips the other face's intermediate vertex. Likewise reconcile local internal patch edges: insert an existing template vertex when it lies on a shared edge, including ramp/plateau subdivision and trim intersections. This scan is over one small template, not the whole component. Preserve required collinear boundary vertices and then run the same nondegenerate constrained triangulation.

Use one numerical key/equivalence rule consistently. The existing integer pair `[round(x/eps),round(v/eps)]`, eps1e-10, can identify a local pair; snap declared boundaries before keying and verify that any merged representatives differ by no more than the allowed equivalence. Do not widen the tolerance. Scalar boundary tables use the same snapped scalar rule. Choose one deterministic representative, evaluate its final XYZ once, and reuse that index. If corresponding shared entries disagree outside tolerance, stop instead of averaging them.

For the body/cap seam, use one **role-independent** horizontal table at global v0. It is the union of the untrimmed lower and upper unit-template edge sets at that datum, before either role's endpoint clipping. Both roles reference this table. If its union contributes an extra collinear point, insert it in both endpoint polygons. This preserves identical seam point sets even when the finite body and cap templates are built separately. No extra material or surface is created beyond the endpoint.

All local uniqueness, sorting and lookup may use simple SCAD list scans. They are bounded by one row-class/sector template and its immediate neighbor interfaces. Do not concatenate all sectors or all rows into a lookup table. Record the number of distinct template classes and the maximum raw/local unique/boundary table lengths, and check their conservative finite allocation estimate before constructing full points/faces.

## 3. Exact global point addresses

Set `h[j]=len(H[j])`, `vcount[j]=len(V[j])`, `icount[j]=len(I[j])`. There are J+1 horizontal interfaces and J rows. All indices below are zero-based.

Compute three exclusive-prefix arrays **once**:

```text
HP[j] = N * sum(h[a],      a < j)   for interfaces j=0..J
VP[j] = N * sum(vcount[a], a < j)   for rows j=0..J-1
IP[j] = N * sum(icount[a], a < j)   for rows j=0..J-1

baseC = 0
baseH = N*(J+1)
baseV = baseH + N*sum(h)
baseI = baseV + N*sum(vcount)
outerPointCount = baseI + N*sum(icount)
```

These equations specify the offsets, not repeated per-face summations. A SCAD divide-and-conquer prefix routine can return `[total, exclusive_prefix_list]`: an empty range returns`[0,[]]`; one count c returns`[c,[0]]`; joining L and R returns`[L.total+R.total, concat(L.prefix, [for(p=R.prefix) L.total+p])]`. Build each prefix array once. This uses lists/arithmetic, logarithmic recursion depth and O(J log J) list work; it avoids rescanning prefixes for every generated vertex or face.

Emit the global point array in exactly these four concatenated blocks:

| Class | Global index | Developed coordinate evaluated once |
|---|---|---|
| Corner C | `C(j,k)=j*N+(k%N)` | `[k%N, b[j]]` |
| Horizontal interior H | `HI(j,k,t)=baseH+HP[j]+k*h[j]+t` | `[k+H[j][t], b[j]]` |
| Vertical interior V | `VI(j,k,t)=baseV+VP[j]+(k%N)*vcount[j]+t` | `[k%N, V[j][t]]` |
| Tile interior I | `II(j,k,t)=baseI+IP[j]+k*icount[j]+t` | `[k+I[j][t][0], I[j][t][1]]` |

Here k is0..N-1 except when addressing the right edge; then k+1 may equal N and the `%N` rule closes the angular wrap. Horizontal/vertical tables exclude corners, so point ownership is disjoint. Map the developed coordinate through the unchanged field/global-frame or selected trim function, then apply existing coordinate quantization. Canonical sector0 supplies the actual XYZ for the circumferential wrap.

For every vertex p=`[x,v]` in tile `(j,k)`, select its class in this exact order after snapping:

```text
if v == b[j] or v == b[j+1]:
    q = j or j+1 respectively
    if x == 0: C(q,k)
    else if x == 1: C(q,k+1)
    else: HI(q,k, local_scalar_index(x,H[q]))
else if x == 0:
    VI(j,k,   local_scalar_index(v,V[j]))
else if x == 1:
    VI(j,k+1, local_scalar_index(v,V[j]))
else:
    II(j,k, local_pair_index(p,I[j]))
```

`local_*_index` returns the single matching ordinal from the already-deduplicated local table and asserts exactly one match. It may be implemented as a comprehension of matching indices followed by that assertion. Its argument never scales with the number of rows, sectors or total component vertices. A trim point on an arbitrary axial cut therefore uses HI; a trim point at an angular boundary uses VI; a trim point strictly inside the tile uses II. The dynamic real-valued coordinate is stored locally, while its global address is integer arithmetic.

No repeated triangle-local point blocks are emitted. No post-export weld is used to create connectivity. Triangles contain these shared integer indices before `polyhedron` receives them.

## 4. Direct-shell connections and bounded checks

The outer endpoint cycle at interface q is already ordered: for each sector k, traverse `C(q,k)` followed by all `HI(q,k,t)` in increasing t, then advance to the next corner. Use these exact indices for bottom/top fans, shoulder/rim annuli or other direct-shell boundary connections. Append unchanged96-sided bore/root/profile rings and any disk-center points after `outerPointCount`, using their known ring counts and analytic offsets. Their angular datum must remain independent of diamond phase. The annular zipper uses the endpoint-cycle indices; it does not append duplicates of those outer points.

The untrimmed full row can cache both its topology and local address descriptors. Finite boundary/trim rows can cache their descriptors separately. Applying a descriptor to a sector uses only k, prefix bases and local ordinals; local lookup need not be repeated once per sector. This keeps table construction bounded and full point/face emission proportional to the emitted mesh, with small prefix work.

V05-1 must expose production-generated numeric point/face data or exact structural witnesses; verify every index lies in range, every shared edge has two opposite directed uses, no face repeats an index, no zero-area face or T-junction remains, and the closed direct cup has the prescribed connected topology. Include these specific cases in the existing focused gate, without a broad parameter grid:

1. The exact G2 endpoints131.93 and139.06, hence fractional global-v boundaries, including u0/N wrap corners.
2. A trim equality meeting a horizontal boundary, a vertical boundary and an interior patch edge; verify the classes above and both incident faces' subdivisions. Include a coincident trim/corner event if it occurs in the selected fixture.
3. Body/cap seam table equality at global v0, including all indices used by their respective shoulder/open-rim attachments.

Production SCAD must execute these rules; a host-language duplicate alone cannot pass. Keep V05-1T data<=10 seconds, G2<=30 seconds, direct full-body/cap probes<=20 seconds, actual body/cap browser-worker<=60 seconds, exterior error<=0.025 mm, mesh parity<=0.05 mm and exterior triangles<=250000. The first actual body failure still stops cap. These are unchanged gates, not measured results of this amendment.

## Exact amendment delta and budget

Permitted implementation delta is confined to the already authorized SCAD diamond mesh-data/indexing/clipping helpers and focused assertions/evidence in the existing VFR-05 task: numeric boundary-table construction and conformity; the four point classes; prefix offsets; local descriptor-to-global index mapping; boundary-template caching; and corresponding direct-shell endpoint references. The Python oracle and all browser/UI/worker files remain read-only under the implementation task. This amendment creates no new source namespace, public parameter, artifact authority or output mode.

The statement that all dynamic boundaries require an integer lattice address is replaced: their coordinates may be arbitrary finite values, stored in a bounded local table and addressed by an integer local ordinal. The phrase forbidding per-cell clipping is clarified as above: boundary/template clipping is retained; redundant clipping of every placed interior cell is forbidden. The direct role-specific annular solid, n-2 triangulation, B field, trim contract, source-authoritative native/browser path, all protected dimensions/operations and prior stop conditions are unchanged.

**The budget remains one candidate implementation attempt plus one focused repair.** The checkpoint explicitly records that no candidate G2/G3 attempt was consumed; this amendment supplies the missing representation contract and does not renew an exhausted budget. Root must freeze it into the resumed implementation manifest. A failed candidate gate/timeout consumes an attempt exactly as before. Stop on drift, an unbounded/global lookup, unresolved shared boundary, changed geometry/threshold, violated timing or a second candidate failure. Do not replace a failed shared-index gate with the duplicate-polyhedron experiment.

## Architecture receipt

Ran `shasum -a 256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/inputs/VFR05A_ARCH_INPUTS.sha256` and `shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/inputs/VFR05A_ARCH_INPUTS.sha256` from the project directory: expected fingerprint, all7 entries OK. Read the manifest-listed VFR-05 architecture/task, exact checkpoint and duplicate-index SCAD witness. No source, test, artifact or browser changed; no runtime or geometry test was executed by this architecture owner.

Next action: root freezes this amendment with the restored source and prior architecture, then resumes the sole VFR-05 implementer at the executable direct-data/addressing gate. Independent mesh validation and formal acceptance remain separate roles.
