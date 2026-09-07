# PERF-CRIT — independent performance-candidate critique
## Verdict

**Pass with two low, non-blocking test/provenance limitations.** The shortcut is
numerically safe under the frozen parameter guards, preserves the old point,
slot, prefix-rank, face, winding, and quantization results, and meets the bounded
Node/OpenSCAD performance targets with exact STL bytes. It does not establish
phone speed, absolute optimality, new geometry, printability, or physical
acceptance. Final live HTTPS delivery parity remains a post-review condition.

Candidate authority is `inputs/candidate-source.sha256`
`3888018275bfcd05ab1d66a27d5b29a01eaf7268382075f4e2bd2047cc638c4c`;
SCAD SHA-256 is
`497098afa555092a0ed85a3a7213cd270852aa76f9001e1478c209cd8469bc42`.
The corrected design-source input is
`4a0d35663c572177fcf8c588654651aad7675fabd2c23c436393363bf842711c`.
Independent validation reverified all 43 candidate paths before and after its
gates. Validation receipt SHA-256 is
`ace97b4da1cab515c72b32750937055241469fff8eb357a222af8a37e4fed466`;
the verified 67-entry artifact manifest is
`750689ca62bd88e4a0006d1994b8a9f91f9daa415f14dd69a8285075ad2df7dc`.

## Source and numerical review

The no-cut implication is valid. With frozen `wave_depth` in `[0.1,0.6]`,
finite dimensions, and an exact plateau predicate,
`wave_cone == outer_radius` while
`wave_radius = outer_radius - wave_depth*(1-cos(phi))/2 <= outer_radius`.
Every skipped endpoint is therefore zero or negative in the existing signed
field. Exact equality can miss an optimization at a floating-point boundary,
but cannot create a false shortcut.

For a face whose two row cones equal `outer_radius`, all four corner signs are
non-positive. The former `min(signs)<0 && max(signs)>0` test is false and emits
`[[a,c,b],[a,d,c]]`, exactly the new fast-path order and winding. The edge fast
path likewise returns the same `undef` as the old sign-product branch. Slot
positions, prefix ranks, emitted points, face indices, ring order, and
`1e-8` coordinate quantization are unchanged. Edges touching either chamfer
continue through the original interpolation and clipping arithmetic.

The source diff is appropriately narrow: 13 SCAD lines add the exact edge
predicate, face shortcut, and required `h`/`role` arguments. Smooth, Diamond,
wave density, sampling, phase, guards, drains, thread geometry, clipping, and
allocation limits are unchanged.

## Evidence and performance claim

All 24 primary samples ran in fresh processes with the pinned OpenSCAD JS/WASM
hashes and exact baseline/candidate output bytes. Median `callMain` reductions
were:

- Rings Body: 26.631 s to 19.317 s, **27.47%**, spreads 6.04% / 6.83%.
- Spiral Body: 26.769 s to 19.335 s, **27.77%**, spreads 2.91% / 0.69%.
- Spiral Assembled: 46.639 s to 33.499 s, **28.17%**, spreads 3.74% / 2.88%.

Single paired controls stayed within their regression caps: Smooth 211.554 to
211.231 ms, Diamond 2701.408 to 2701.923 ms, and Ribs 1065.322 to 1000.138 ms.
Seven additional Ribs/Rings/Spiral cap, edited-Diamond, non-round Spiral, and
near-allocation Rings cases matched baseline and prior certified hashes. The
full validation joined 38/38 compile receipts (19 pairs) to expected source and runtime hashes;
Node 59/59, Python 13/13, and build gates passed.

The runner is fit for this prescribed benchmark: each invocation is a fresh
process; it rejects unexpected runtime assets; records absolute source path and
hash, Node path, full argv/messages, separated initialization/render/read/write
timings, artifact bytes, and output hash; and fails on compiler warnings or
errors.

## Findings and residual risks

- **Low — property-test coordinate description.** The JS inequality sampler
  applies `bodyThreadZ` to Body rather than Cap, opposite the SCAD z-global
  mapping. The inequality is phase-independent, so it still proves
  `wave_radius <= outer_radius`; exact WASM byte parity is the stronger gate.
  Describe this as phase-independent sampling, not a literal coordinate oracle.
- **Low — runner source enforcement is external.** `benchmark.mjs` records but
  does not reject an unexpected source hash. The independent controller enforced
  both expected source hashes for every pair, so current evidence is sound.
  Future ad-hoc runner use must retain that join.
- **Process, corrected.** An unisolated build briefly refreshed live `dist`.
  The six approved R2 local files were restored with exact path, size, and hash.
  HTTPS restore was not separately checked; final candidate publication must
  compare every served byte after formal review.

I directly inspected the fresh 1280x900 Rings/Body 3D view at
`/tmp/pattern-performance-validation/browser-preview-isometric.png`. Rings are
continuous across the visible sidewall; there is no diagonal tear, missing
plateau strip, or winding hole; top and bottom chamfer transitions are clean;
and the mouth/thread and bottom rim are intact. The current browser Blob and the
downloaded STL were both 39,958,888 bytes with SHA-256
`d1b73da0bc2a0dfe479cb89b81e51c3fc608cba53e8487d202b2c1e0405fa849`.
Drains were not visible from this angle; exact identity to the prior certified
STL carries the existing drain/mesh evidence.

## Review provenance and next action

The critic inspected root-captured exact frozen bytes because this worker's
shell could not spawn under OS error 24. The independent validator supplied the
43-path before/after verification and executed all measured gates; the critic
did not duplicate timed load. Proceed to formal review, then refresh the approved build and require exact HTTPS byte parity before calling delivery complete.
