# P2-V independent validation — blocked candidate

Owner: `/root/parametric_mesh_validation`, independent of implementation. Date: 2026-09-06. Read-only candidate examination; no geometry, source, dependencies, or accepted 2D files changed.

Verified all 48 declared path/content SHA-256 entries and recomputed candidate fingerprint `1e5f22bf7437b8cf29b7ae612e04258a2f507aa94908d05ae1cb8631458fcb3d` before testing. Flat GLB SHA-256 `ffd526272b197b9da3a12cfed230e5cce9b99766739998829d4a804f25c74197`; relief `fb606070739dd7532c5de605744b5fcefb4b6dd2eaac4b447a8a34429aca6387`.

## Blocking finding GM-R2-01

The written black backing has **179 disconnected indexed components**, independently confirmed by both mesh splitting and union of written top-cap triangles. The largest polygon has **no holes**; filling its exterior adds zero area and cannot connect any other island.

| Measurement | Actual written geometry, converted to source grid |
|---|---|
| Total footprint | 1,011,482 square source units |
| Main component | 1,011,159; bounds [3,126,1250,1142] |
| Remaining islands | 178; combined area323 (3.23 mm² at working scale) |
| Contained in filled main exterior | 0 |
| Whole footprint bounds | [1,126,1251,1144] |
| Nearest-main distances | 109 islands at1 unit;69 at0 (point contacts) |
| Largest island | area17; bounds [1103,994,1120,995] |

Strictly preserving the existing footprint and producing one positively connected backing are incompatible here. A connector must add currently-background area; merely filling the main exterior is insufficient. This is a design-contract conflict, not authority for this validator to modify the artwork or invent a backing outline. Design must freeze any permitted backing-only delta before implementation resumes.

## Checks completed and limits

Both GLBs load with `process=False`: flat6 named geometries, relief14. Every indexed geometry is watertight, winding-consistent, and has positive signed volume. Both backing STL bytes have the same SHA-256 `1ca3e2eb62abe76cfbfbb34a55f17d33f915573a16429ce5dd847a9db4f70bdf`. Flat total Z is2.0 mm; relief2.400000095 mm. These development values are not product-size acceptance.

Accepted PNG, face source, face tests, SVG and SVG report match their historical face-candidate manifest hashes. The old dependency entry was intentionally outside this baseline-art check.

The root stopped broad acceptance checks when this blocker appeared. Full color-footprint parity, inter-part intersections, semantic-region/plate checks, independent parameter sweeps, and material metadata validation are **not completed** for this candidate. Closed indexed topology does not cure geometric pinched contacts; STL coordinate welding remains nonfabrication evidence. No STEP/BREP, slicer, user-surface or physical acceptance is claimed.

## Reproduction

Commands executed from repository root through the root environment: `uv run python /tmp/grenadier-backing-diagnostic.py` and inline Python SHA-256 / Trimesh checks. The diagnostic's core, sufficient to reproduce the blocking measurement, is:

```python
import trimesh, numpy as np, shapely
from shapely.geometry import Polygon
s = trimesh.load_scene('projects/grenadier-fridge-magnet/GLB/p1-r2/flat.glb', process=False)
m = s.geometry['backing-black']
assert len(m.split(only_watertight=False)) == 179
t = m.triangles
cap = t[np.all(np.isclose(t[:, :, 2], m.bounds[1, 2]), axis=1), :, :2]
uv = cap * [10, -10] + 627
assert np.max(abs(uv - np.rint(uv))) < 3e-5  # actual maximum 1.52587890625e-5
foot = shapely.union_all(shapely.polygons(np.rint(uv)))
parts = sorted(foot.geoms, key=lambda p: -p.area)
filled = Polygon(parts[0].exterior)
print(len(parts), foot.area, parts[0].area, len(parts[0].interiors))
print(sum(filled.covers(p) for p in parts[1:]))
```

Next action: design-owned backing contract correction, implementation-only repair and refreeze, then independent validation on the replacement fingerprint. This receipt remains evidence for the failed candidate above.
