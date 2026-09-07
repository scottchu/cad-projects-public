# REF-ARCH archive receipt

Status: **PASS — frozen 33-image archive**

## Verified input fingerprint

- Baseline commit declared by the brief: `2989aa412911df1fd947df81d056ea3ebfe7c66d`
- Final ordered source metadata: `inputs/sources-v2.json`, SHA-256 `3d81399f55b1bd1d34fe6693fc22b51484c433b95009e98407c08b3a79d62f83`
- Final source-image manifest: `inputs/source-images-v2.sha256`, SHA-256 `7102384c86cfa60ba4136c6551c829045aa73a778e976ec297cd174e047128f7`
- The original 30-image manifests remain preserved unchanged.

## Deliverables

- `docs/references/2026-09-06-container-patterns/images/ref-001.png` through `ref-033.png`
- `README.md`: numbered thumbnail table and provenance links
- `index.html`: responsive numbered gallery with direct relative links to every original PNG
- `catalog.json`: ID, batch, batch position, original source path, archive path, SHA-256, byte count, media type, and pixel dimensions
- `SHA256SUMS`: 36 archive entries, covering README, catalog, gallery, and all 33 images; excludes itself and the independently mutable `PATTERN_PARAMETERS.md`

## Verification

- Source-to-archive parity: **33/33**
- Archived image bytes: **12,262,526**
- Coverage: catalog 33 entries; gallery 33 figures; README 33 reference rows
- Every catalog image path exists; every archived image matches its declared source SHA-256 and byte count.
- Every gallery card has direct relative `href` and `src` links; every README row links its archived image.
- `(cd docs/references/2026-09-06-container-patterns && shasum -a 256 -c SHA256SUMS)`: **36/36 OK**
- Frozen archive manifest SHA-256: `7cdda37eb2ca54c0a2461214b24482b42089df68534c95886c9fd4320c8bcbd5`

No image was deleted, deduplicated, re-encoded, cropped, or semantically renamed. Text, dimensions, branding, and claims visible inside the images remain unverified reference content. Semantic grouping and feasibility judgments are outside this archive receipt.
