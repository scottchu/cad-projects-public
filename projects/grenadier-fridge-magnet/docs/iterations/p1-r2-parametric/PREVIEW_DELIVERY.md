# P2-P private 3D review delivery — 2026-09-06

Presentation owner: `/root/parametric_preview_delivery`. Frozen input contract fingerprint verified before work: `2479dacd84b1cc33f54bde6dc7e30c9bfa77a32450827babe3d6361567d0fc7c` (18 entries). This is a custom Three.js fallback for the actual GLBs; it is not CAD Viewer and supplies no CAD, slicer or physical acceptance.

Review URL: https://mac-mini.duckbill-ionian.ts.net:8448/grenadier-model

Direct study downloads:

- https://mac-mini.duckbill-ionian.ts.net:8448/grenadier-model/models/flat.glb
- https://mac-mini.duckbill-ionian.ts.net:8448/grenadier-model/models/relief.glb

The Traditional Chinese page provides flat/relief toggle, orbit rotation, zoom/pan, front/oblique/reset views, continuous-black-backing and relative-height explanations, and a prominent development/not-print-ready notice. It exposes no scale, nozzle or hole controls. The prior accepted `review/p1-r1/face-review.html` is unchanged.

## Current model status

The page serves frozen color-corrected candidate `1f66199dfbd9b35780aee9cb93af0179277805085e9ac1bc61bbf2c9999b2fc0` from `color-corrected-candidate-manifest.json` (18 paths). `flat.glb` SHA-256 is `bb0b2d54dba75530fbcce067229393cea5534d065251a18a5c6c7c60b8c34e77`; `relief.glb` SHA-256 is `143d67d0365a8b7fd9fc7e2425ee925cf59b24527607b98e8f768880b3966638`. Geometry bytes match the connected candidate; corrected linear PBR material factors restore the source sRGB colors. Small black connections at the backing edge make it one connected piece and can add visible pixels at the silhouette. Independent acceptance remains pending; thin bridges, text survival, slicing and physical printing remain unresolved.

## HTTP and browser evidence

The exact served HTML matched local bytes at SHA-256 `dda27ff37252c3967169baa817c236f7468593654976a1e1be25eb9b1754b402`. HTTPS fetches of the page, both color-corrected GLBs, Three.js, `three.core.js`, `GLTFLoader.js`, `OrbitControls.js`, and `BufferGeometryUtils.js` returned HTTP 200. Served GLB hashes matched the frozen candidate files. The color-corrected candidate requires a fresh browser reload by the independent reviewer. This is Mac browser evidence only, not phone or user-device verification.

## Route preservation and lifecycle

Before/after `tailscale serve status --json` snapshots are `/tmp/grenadier-model-serve-before.json` and `/tmp/grenadier-model-serve-after.json`. Removing only the new handler from the after snapshot produced a deep equality match with before. The sole addition is private tailnet handler `/grenadier-model`; after the color-corrected-candidate switch it proxies `http://127.0.0.1:60896/`. Port 443, `AllowFunnel`, all existing routes and `/grenadier-face` remained unchanged; the old face URL was fetched successfully after the addition.

The narrowly allow-listed server is `scripts/parametric-preview-server.mjs`. It serves only the review HTML, two named GLBs and required local Three.js modules; other paths return 404. Detached PID `57483` is recorded in `/tmp/grenadier-model-server.pid`; stdout/stderr are `/tmp/grenadier-model-server.log`. There is no auto-start. The route persists but the process will not survive reboot.

Rollback only this route:

```sh
tailscale serve --https=8448 --set-path=/grenadier-model off
```

Then verify PID 57483 still belongs to `scripts/parametric-preview-server.mjs` before `kill 57483`. Do not disable the whole 8448 port or stop unrelated processes.
