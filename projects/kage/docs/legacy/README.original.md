# Kage upright-fin shadow clock simulator

`index.html` is a local, dependency-free runtime simulation. Its default view
shows the accepted optical architecture: hidden concentric carriers with small
constant-radius upright rim fins between a wall-side mask and one on-axis LED.
The old long flat-hand fixture remains historical only and is not the P1 design.

The page contains one bounded 3D/2D viewport, one consolidated parameter panel,
and a live side-section inset. Five views are available: Assembly, Wall Shadow,
Side Section, Exploded, and Orbital Close-up. `research.html` is the concise
design rationale.

The Three.js r176 runtime is checked in at `vendor/kage-three.bundle.js`; no CDN
or network dependency is used by the page. Rebuild it with the pinned npm lock:

```sh
npm ci
npm run build:three
```

## Executable optical contract

Python and JavaScript expose the same point-source functions for projected
radius, inverse fin sizing, shadow interval, projected width, mask sizing,
optical cone, baffle clearance, radial-envelope clearance, and off-axis point
projection.

```sh
uv sync --dev
uv run pytest
uv run kage-clock upright-optics
uv run kage-clock upright-optics --json
uv run kage-clock upright-optics --source-z 80 --fin-radius 32 \
  --base-z 20 --tip-z 50 --fin-width 3 --mask-z 8 \
  --mask-wall-radius 52 --wall-radius 140 --cone-plane-z 40
```

Frozen starting geometry:

- wall `z=0`, source `z=60`, physical mask `z=6`;
- projected mask radius `50`;
- carrier pitch `4.75`, with radii `r30 / r34.75 / r39.5`;
- hour fin `r30`, `z22.5..38.8235`, shadow `r48..85`;
- minute fin `r34.75`, `z16.5625..41.0455`, shadow `r48..110`;
- second fin `r39.5`, `z10.625..41.7692`, shadow `r48..130`;
- fin section `2.4 mm` tangential × `1.6 mm` radial.

The simulator validates ideal point-source geometry. Real LED die size,
brightness, heat, fin stiffness, carrier runout, quartz torque, and room
visibility remain physical prototype gates.
