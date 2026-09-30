# P2-R final independent formal review

2026-09-06; owner `/root/parametric_magnet_formal_review`, distinct from design, implementation, critique, validation, and presentation roles. **PASS to present both variants as adjustable, source-first development-mesh previews.** This is not CAD/STEP, slicer, fabrication, or physical acceptance.

## Candidate and provenance

The current authority is `color-corrected-candidate-manifest.json`: 18/18 path/content hashes reverified and sorted path-NUL-hash-LF fingerprint recomputed as `1f66199dfbd9b35780aee9cb93af0179277805085e9ac1bc61bbf2c9999b2fc0` (manifest file SHA-256 `bd3347ec958484d64249ffbc52e56f8ce2ffc09413871b6d1f43d92aec1c85f0`). Current GLBs are `GLB/p1-r2-color-corrected/flat.glb` (`bb0b2d54dba75530fbcce067229393cea5534d065251a18a5c6c7c60b8c34e77`) and `relief.glb` (`143d67d0365a8b7fd9fc7e2425ee925cf59b24527607b98e8f768880b3966638`). Historical disconnected and cyan-rendering candidates remain preserved and rejected only for their recorded defects.

## Join and requirement coverage

P2-V2 independently established one watertight connected backing, exactly 176 permitted addition-only backing cells within the 356-cell/distance/bounds mask, no face-pixel changes, exact accepted SVG projection, no positive-volume overlaps, valid flat/relief heights, and independent XY/Z behavior. P2-V3 proved the final GLBs retain byte-identical complete BIN chunks and normalized non-color JSON geometry against that V2 candidate, while each material performs exactly one reversible sRGB-to-linear conversion. P2-C3 reverified this fingerprint and directly observed both freshly served variants with deep royal-blue plate, distinct pale glass, preserved lettering, and the backing-edge disclosure. Root's final browser reload also showed flat and relief loaded without visible error; this is local-browser evidence, not user-device approval.

This covers GM-R2-01 through GM-R2-07 for the declared mesh-preview scope: accepted face and both variants retained; flat is coplanar; relief order and locally flush plate lettering are preserved; no holes or scale decision were introduced; four physical filament intents plus the unresolved glass-mix placeholder are represented; XY and Z remain independently adjustable; original visible artwork is unchanged. The earlier 179-component backing blocker is resolved by the bounded 176-cell backing-only repair. The cyan-plate blocker is resolved by the exact export encoding correction. No blocking finding remains for showing the development preview.

## Acceptance boundaries and operations

- Development source/GLB mesh evidence: accepted for preview at this fingerprint.
- Visual delivery: Mac Chrome evidence passes; user inspection of both variants remains the intent gate. Live URL: `https://mac-mini.duckbill-ionian.ts.net:8448/grenadier-model`.
- CAD/STEP: not generated; no BREP claim. Installed root `cadgen` 0.4.15, pinned by another project, lacked the applicable mesh snapshot/viewer CLI, so the actual-GLB Three.js page is the recorded fallback.
- STL/3MF and slicer: existing STL is study/interchange evidence only; pinched contacts, thin connectors, nozzle/toolpath survival, orientation, resolved scale, and a slicer-ready package remain open.
- Physical: glass blue/white mixing, filament appearance, magnet retention, strength, printed detail, assembly, and durability remain unverified.

Recorded environment operations are two root runs of `uv sync --all-packages --all-groups`, plus root `npm install`; no project-local environment or lockfile was created. The preview route proxies loopback port 60896; PID 57483 is recorded in `/tmp/grenadier-model-server.pid`, has no autostart, and will not survive reboot. `PREVIEW_DELIVERY.md` owns exact service/rollback details.

Next action: the user inspects flat and relief in the live 3D page. A later iteration should resolve actual slicer/toolpath evidence first, then choose scale and enlarge only logo/text regions that fail; no final width is selected here.
