# SP-REV-RESUME — resumed formal review

## Verdict

**APPROVED for draft-PR delivery and conditional enablement on the private 8453
validation route. NOT approved for main merge, public release, or final
Safari/iPhone, slicer, print, fit, or physical acceptance.**

The two blockers recorded in `REVIEW.md` are closed on unchanged Candidate 03:
the five named written meshes pass the required global intersection/T-junction
certification, and the Candidate 03 Chromium UI/output/real-worker lifecycle
flow passes. Root may perform one standard build from the reviewed commit and
enable it on 8453 only after all six served files match that build exactly and a
fresh live-route UI check passes. Any mismatch keeps the accepted prior build in
service.

## Frozen review join

- Candidate commit: `8068fbd19b4fd526d6120e7dfd714e9aca217a9b`.
- Candidate manifest SHA-256:
  `412b5e389a85dbaa7ad730870f496639d8dcd2e2129de733b4da1ba1e031fc63`;
  23/23 paths pass.
- Resumed join SHA-256:
  `c58a4ea425b26c1318df25ad8908c64a6b1df4d87bc882142d512426eec63086`;
  7/7 joined paths pass.
- Browser review SHA-256:
  `1785d31de0cfb4c875338b60fffd7cc13a6ccb7a87e7cffc377f52e0cf432da4`;
  its 26-file raw-evidence manifest is
  `3885826d237ae8378dc3d4ab7c4e1a172ec8459e6d30fff653d529ae2ecf6df9`
  and passes 26/26. The mislabeled interim image is excluded.
- Global validation SHA-256:
  `65e5bedfd1ca2d44917c0b6084b1df2bdbca35f1dcf3c7c5a2dab916fd4920e1`.
  Durable certifier manifest
  `da6ea9acc8e9ba2aad38cbffa3ede497a2dd5a4c79085a7cce30f29e5d6ba293`
  passes 5/5.
- Repaired lifecycle-harness manifest
  `e5fd360c1c520d8dd6711e0a4c781f5a790533c43fe835653d7aae147a42fc9e`
  passes 6/6 and remains bound to Candidate 03.

The source implementer, source critic, deterministic/mesh validators, browser
critic, and formal reviewer are independent roles. I verified the joins and
manifests, reviewed the global numerical method and fixtures, inspected the
browser DOM/byte receipts and representative desktop/mobile captures, and
checked the repaired harness observation boundary. I ran no build, browser,
service, broad test, or mesh scan and changed no app source.

## Closure findings

- **Global written-mesh gates: PASS for the five exact STL hashes at `1e-6 mm`.**
  The dependency-free C++17 BVH visits every overlapping nonincident face pair,
  tests noncoplanar and coplanar triangle intersections, and queries every
  canonical vertex against the unique-edge BVH. Crossing, coplanar-overlap, and
  explicit T-junction fixtures fail as expected; an adjacent pair passes. The
  five meshes report zero unexpected intersections and zero geometric
  T-junctions across 17,060,031 tested face pairs. This is numeric evidence for
  those written meshes, not an exact-arithmetic source theorem or coverage of
  every parameter combination.
- **Chromium UI/output: PASS.** At 1280x900 and true 390x844, the fixed preview,
  independent control scrolling, labelled Smooth/Diamond cards, keyboard focus,
  W4.3-to-W4.4 repair, N68 literal 136.8 rejection/136.7 repair, explicit
  generation, stale/download invalidation, Reset, and compact actions behave as
  designed. Body, cap, assembled, and print-layout jobs finish within 11.111 s;
  browser Blob/download hashes equal the independently validated STL hashes.
- **Real-worker ownership: PASS.** Cancelled genuine output changes no status,
  render, Blob, or download. The corrected supersession gate snapshots only
  after the newest genuine result is held; delivering the older genuine result
  changes nothing. The newest result installs once, and held/rendered/Blob hash
  all equal `1799916b0c29b49bc0f7b82221fbd247e4b2d354e0a8bd382f25e6197600d693`.
  The discarded first comparison measured legitimate newest-worker progress,
  not a product failure.

## Delivery and remaining acceptance boundary

Root's final 8453 step must reverify Candidate 03, run the repository-standard
build once, record its six hashes, serve those exact bytes, verify six HTTPS
responses byte-for-byte, and perform a fresh live-route check for Smooth default,
Diamond selection/error recovery, one current generation, and download currency.
Only then may 8453 be reported as the Candidate 03 development preview. Port
8448 configuration was untouched; its pre-existing HTTP 502 was observed and
must not be described as healthy or as changed by this work.

Native Safari remained unavailable after `cgWindowNotFound`. The user's actual
iPhone review is therefore the next visual/touch acceptance gate, especially for
swatch comprehension, scrolling, focus/touch targets, and rule readability. CAD/
STEP authority remains separate, and no slicer, support, grip, drainage-in-use,
thread-strength, fit, wear, or physical result is established.

This reviewer changed only `REVIEW_RESUMED.md`.
