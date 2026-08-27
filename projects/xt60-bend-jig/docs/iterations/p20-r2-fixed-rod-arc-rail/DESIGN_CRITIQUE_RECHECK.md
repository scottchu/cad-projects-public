# P20 R2 focused design-repair independent recheck

Status: **SUPERSEDED FOR SIDE SIGNS — the user-approved corrected gate now
controls physical left `+45 deg` / right `-45 deg`; unchanged analytic
magnitudes remain useful evidence.**

Task/role: focused recheck of repair 1 by `P20R2-CRITIC-01`, preserving
`DESIGN_CRITIQUE.md` as the immutable blocked-history receipt. This recheck
does not approve source, BREP, STEP, manufacturing, print, force, torque, or
physical behavior.

## Rechecked fingerprint

- Branch observed: `codex/xt60-p20-r1-fixed-rod-reset`.
- HEAD observed: `a48c5697f9126dbb6934d764e48f2a01f6a01475`.
- Repaired `DESIGN_CANDIDATE.sha256` file SHA-256:
  `c3aaa10589408db6d24fcde9b46ed89f8cbd95e41764c4a4db0672cbd3fd2c30`.
- Repaired candidate manifest: all `5/5` entries independently recomputed and
  matched, including the prior critique SHA-256
  `43c98d108c1713e2efd54172fe275b3dafb7d74fa17421b1d170244368794b21`.
- Nested `DESIGN_INPUT_MANIFEST.sha256` remains
  `07847a8fec788ece8c9f421225ca1301810cf619713904a7da867dfcc6674a55`;
  all `20/20` entries independently recomputed and matched.
- Repaired review-media hashes match the candidate manifest:
  - SVG: `9a451d2f486ab434f034beb0d6beec34254b5d7f203b74ce39dc0a149d584751`;
  - PNG: `6225ec3bb34f22ecbf5ff6dcd683a27b09eed6c0a29165a1e7819b305083e14d`.
- Repaired `DESIGN.md` matches
  `ec2a0df812e43e86dd37363d34f4ac4cc2e35f42df3c56e5ad91c3b73cbc8261`.

Successful manifest verification result:

```text
PASS DESIGN_CANDIDATE.sha256 entries=5
PASS DESIGN_INPUT_MANIFEST.sha256 entries=20
```

## Focused prior-blocker recheck

The PNG was inspected at its original `1200 x 1600` resolution and the SVG
source was independently inspected for exact text, markers, paths, and plotted
coordinates.

### Left/right MID locations — PASS

The repaired gate now has distinct, labeled `LEFT MID u=0.5` and
`RIGHT MID u=0.5` markers. Recomputing the inverse-frame points gives:

| side | exact `q(0.5)=(Y,Z)` mm | expected SVG pixel `(x,y)` | actual SVG marker |
|---|---:|---:|---:|
| left | `(-18.067710743685,-4.422423372148)` | superseded SVG | approved PNG |
| right | `(-9.648675231653,-15.902926343101)` | superseded SVG | approved PNG |

The marker positions therefore encode the correct explicit left/right MID
coordinates within the SVG's declared rounding. Their labels and leader lines
remain legible in the original-resolution PNG.

### Direction and outer rotation labels — PASS

The repaired gate contains and visibly renders:

- `RIGHT local: OPEN -> MID -> END (physical outer -45 deg)`;
- `LEFT local: OPEN -> MID -> END (physical outer +45 deg)`;
- cyan and purple direction overlays with arrowheads; and
- the top-level `LEFT +45 deg / RIGHT -45 deg` physical-motion statement.

The SVG has four marker-ended rail/direction paths. The direction is
unambiguous from the shared OPEN axle toward each side-specific END point.

### Retained inner count — PASS

The gate now states `3 INNER rails / plate · 6 retained total`. This resolves
the prior front-projection ambiguity and agrees with the frozen requirement:
three P19 white-rod paths in each of two inner plates.

### Required visible/absent topology — PASS

At original resolution:

- both complete curved fixed-rod rail bodies are plainly visible as wide black
  apertures with cyan/right and purple/left centrelines;
- the common OPEN point, distinct MID points, and distinct END points remain
  visible;
- `white-rod OUTER rails = 0` and
  `OUTER rails / holes / windows = 0` are explicit;
- the six deliberate rod/solid-outer collisions remain explicit in both text
  and the axial stack; and
- `REJECTED: constant round hole / plate rotating about A` remains present.

No fixed-rod arc is hidden by an opaque plate in this phone gate.

## Analytic regression

The nested 20-entry design input is unchanged. I also recomputed the cheap
motion invariants rather than relying on the repaired prose:

- radius: `sqrt(346) = 18.601075237738 mm`;
- 45-degree arc: `14.609250328937 mm`;
- endpoint chord: `14.236646635318 mm`;
- whole-arc sagitta: `1.415922542889 mm`;
- maximum world reconstruction residual across `1001` states per side:
  `6.405e-15 mm`;
- maximum radius residual: `3.553e-15 mm`;
- 33-sample segment sagitta: `0.001400626755 mm`;
- resulting conservative journal radial clearance: `0.148599373245 mm`;
- left/right outer rim webs: `4.798924762262 / 4.948924762262 mm`;
- moved inner AF8.15 corner web: `3.893520068366 mm`.

These values reproduce the accepted analytic design and show that the focused
repair changed review-media traceability, not the inverse-frame rail geometry,
datum, cutter width, travel, or web conclusion.

## Disposition

**The prior repaired fingerprint is superseded for side signs by approved gate
SHA-256 `e2d05a852889bef2e9c97a2e18878b475aef39b690fa884d6db6a1054d1da8d7`.**

The prior blocker is closed: MID locations, OPEN-to-MID-to-END arrows,
side-specific physical outer `+45/-45 deg` labels, and the six-inner-cut count are now
explicit and legible. The next worker may begin the separately scoped
source/BREP implementation against this exact fingerprint. No white-rod outer
rail sequencing is authorized.
