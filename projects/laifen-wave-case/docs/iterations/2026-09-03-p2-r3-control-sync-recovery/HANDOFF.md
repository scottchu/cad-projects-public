# P2 R3 final handoff — generic container simulator intent gate

**Status: PASS for exact local/static visual-intent candidate and private tailnet delivery.** User-device comprehension and intent confirmation are still pending. This iteration does not make or approve CAD, OpenSCAD, STEP, mesh, slicer, printer, fit, drainage, physical, or MakerWorld claims.

## Exact candidate and delivery

- Recovery contract fingerprint: `cc4c378fe3b398ead900b1bf39a94bf8b1e94f21599c4219bb3f55b6af1fdf61`.
- Candidate manifest: `inputs/implementation-recovery-candidate.sha256`, SHA-256 `15c7c0503e87ec0f0b1a828fb62d471baaefc9a6caecf629d14d4504d0d19224`.
- Candidate source: `preview/p2-r2-generic-container-simulator/`; served byte-pinned copy: `scratch/presentation/container-simulator/`.
- Private URL: <https://mac-mini.duckbill-ionian.ts.net:8448/container-simulator/>.
- Served `index.html`, `app.js`, `math.mjs`, and `style.css` exactly match the reviewed bytes; their hashes and local/private HTTP 200 checks are in `DELIVERY.md`. Delivery evidence manifest SHA-256: `d9f0c05cffe89abd7bacf8bae44138e46d051d56fa26317ca0a6c6e72fef46ee`.

The page presents exactly two exterior pieces at a mid seam, Laifen and wide-short presets, H/OD/wall/floor/seam controls, original pattern choices, and visual thread accounting. It derives `E=pitch*turns` and `P=pitch*(turns+lead/runout)` for 1/2/3 turns. Those values are not thread-solid, tolerance, or physical-fit evidence.

## Independent evidence

- Implementation recovery receipt: `IMPLEMENTATION_RECOVERY.md`, SHA-256 `8a13b3e6f9724e6b8def5595b7180a5a3e336911115f6aabfc41a5596bd6e659`.
- Independent validation: `VALIDATION.md`, SHA-256 `21348385700605eab0ed0a659190de744f433d2c9295fa507a4bbfe52d758c6e`; evidence manifest `40929b882d69cfac7c9c48c2da842bf20eabff12a58098952c906f622414ffbb`.
- Independent critique: `CRITIQUE.md`, SHA-256 `4b93518dbd20ec5c089f5f9f4c097b65eb2ff89bc1d6c95a62ee94d1634d087a`; evidence manifest `dc3af7cd22df37eb25005d52d14c42b21e6bc54c611ad4b13eadcae83eacfe1f`.
- Formal review: `REVIEW.md`, SHA-256 `57e7a2578387418a3e6c5db850888d9334b563e91e60f56682be37b44bd250fc`; review join `7e89663ea2d341f68b2c5e0f192df00a733481f677e9756bc31544e5f8523c3d`; receipt `bbe955ceb1eb0dd7938119e65f3935f0b2d5b8cee13d1bf6f3fda6d05d78c3e2`.

The repaired trace holds canonical raw S across percentage edits, exact H261 endpoints (12.4 / 248.6), native ArrowUp at maximum, and H311 rebinding. All routes except the new isolated `/container-simulator` remained intact; 8449 CAD Viewer and public 3245 were not altered.

## Preserved R7 baseline and next action

P1 R7 remains the current immutable CAD reference: candidate `8d3941772cca549846937dcad6ce4a05e06f5bba104c261668a0cf747c62b6a1`, print-layout STEP SHA-256 `80fd95845b51da5266883614f9bf8eff60793a24d5c39b7321c9c6cb16d477a4`. Its current physical/slicer gaps are unchanged.

Ask the user to pass or reject the visual relationship on the private URL: a container split in the middle, able to become wide/short, with selectable short thread turns and patterns. If passed, open a new OpenSCAD generator iteration before source changes. Freeze the two-piece topology and named dimensions for split mm/%, pitch, turns 1/2/3, lead/runout, thread form height/clearance, wide-short dimensions, and an original pattern library. Then run separate CAD, STEP/export, slicer, and physical validation. MakerWorld publication is not yet started.
