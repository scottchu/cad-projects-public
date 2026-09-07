# PERF-REV — formal independent review

Date: 2026-09-06. Reviewer: `/root/compact_formal_review`, distinct from the implementer,
validator, critic, browser operator, and root delivery owner.

## Verdict
**APPROVE candidate SCAD `497098afa555092a0ed85a3a7213cd270852aa76f9001e1478c209cd8469bc42`
for commit/push to draft PR 19 and the scoped existing private 8453 refresh,
conditional on the post-review delivery checks below.**

No blocking correctness, performance, provenance, or review finding remains.
The two critic findings are low limitations on how future tests may be described
or reused; neither weakens the frozen candidate evidence.

## Verified join and provenance
- Review join SHA-256
  `6a15779d445ed7b276921b885582be5ffd4c2f82b5a81b159893349f275eb77a`:
  7/7 entries verified.
- Candidate-source manifest SHA-256
  `3888018275bfcd05ab1d66a27d5b29a01eaf7268382075f4e2bd2047cc638c4c`:
  43/43 entries verified.
- Validation-artifact manifest SHA-256
  `750689ca62bd88e4a0006d1994b8a9f91f9daa415f14dd69a8285075ad2df7dc`:
  67/67 entries verified.
- Implementation receipt `d0054a55f03272c2f6af29e781390ccaf4b870d68c9995e9a4c712e2a2cc229d`;
  independent validation receipt
  `ace97b4da1cab515c72b32750937055241469fff8eb357a222af8a37e4fed466`;
  independent critique receipt
  `430bd2364a0e7cfd1e80dd84e12e7b276e17ff19afd6a951dd26a2a68b8b5fea`.
- Baseline commit is `7f15b1649a5d83c77512c9ba0864943ac68996b6`; baseline SCAD is
  `3b96cc2d5a5100e2daa2fe5a14c21e510728f108cfbc9afd5ae80bf1ef5dde40`.

The sole implementation owner was `/root/drain_validation`. Independent
validation was owned by `/root/drain_count_validation`; critique by
`/root/compact_validation`; root operated the isolated browser; this reviewer
verified their immutable join and source diff. The critic's source evidence was
root-relayed during OS error 24, while the validator independently verified all
43 candidate paths before and after its gates. The critic directly inspected the
frozen isometric screenshot. This preserves distinct acceptance provenance.

## Findings and requirement coverage
- The 13-line SCAD diff is limited to exact no-cut edge and uncut-face paths plus
  the required `h`/`role` arguments. When both row cones equal `outer_radius`,
  positive `wave_depth` and `1-cos(phi) >= 0` make every corner field nonpositive.
  The old code therefore produced no edge cut and emitted `[a,c,b]`, `[a,d,c]`;
  the shortcuts return those same results. Chamfer-touching rows retain the old
  point, sign, interpolation, slot/rank, quantization, order, and winding work.
- Smooth and Diamond bypass the changed shared-wave path. Sampling density,
  phase, guards, clipping, controls, UI, worker, runtime, dependencies, drains,
  threads, transforms, and output format are unchanged.
- Independent fresh-process medians pass the prescribed targets with exact STL
  bytes: Rings Body 26.631→19.317s (-27.47%), Spiral Body 26.769→19.335s
  (-27.77%), and Spiral Assembled 46.639→33.499s (-28.17%). Every cohort spread
  is below 7%. Single-pair Smooth/Diamond stay within noise; Ribs is 6.12% faster.
- All 38 fresh receipts (19 baseline/candidate pairs) have exact byte parity.
  Seven additional cases cover new-family caps, edited Diamond, Spiral stress
  body/cap, and near-limit Rings. Exact hashes preserve the prior mesh, seam,
  protected-internal, drain, collision, and field-error certificates.
- Validation passes Node 59/59, Python 13/13, isolated build, source/runtime
  binding, and current Blob/download parity. Default Rings Body was 39,958,888
  bytes, SHA
  `d1b73da0bc2a0dfe479cb89b81e51c3fc608cba53e8487d202b2c1e0405fa849`.
- No fresh print-layout candidate compile is claimed. Its transform source is
  unchanged, exact body/cap bytes are established, and the prior certified
  print-layout result remains applicable. This is adequate for this exact-output
  optimization and does not become a fresh all-four-role compile claim.
- Browser completion took minutes and is evidence of current output ownership,
  rendering, and download identity only. Controlled Node pairs establish the
  performance improvement; no browser or phone speedup is claimed.

## Retained low limitations
1. The JS inequality sampler offsets Body/Cap phase oppositely to SCAD. Its
   inequality is phase-independent, and exact WASM byte parity is authoritative.
2. The durable runner records but does not reject an unexpected source hash.
   The validator externally enforced both expected hashes for every frozen pair;
   future reuse must preserve that controller-side check.

## Delivery conditions and boundary
The corrected implementation record discloses that a standard build briefly
wrote live `dist`; the six accepted R2 local files were restored exactly. Because
served HTTPS restoration was not separately proved, delivery must now:

1. run the standard build from this reviewed candidate;
2. prove all six served 8453 HTTPS files byte-identical to that build; and
3. perform one fresh live default Ribs Body generation/current download,
   expecting 7,623,719 bytes and SHA
   `40f29575b0c752ea4f42dff181db02c4eb369a300e384d947509c28cd70c5401`.

Failure of a delivery check reopens that delivery gate; it does not authorize a
source repair without a new frozen candidate. This approval excludes main merge,
public hosting, Tailscale configuration, 8448, printer action, STEP, slicing,
grip, drainage-in-use, cleaning, fit, strength, wear, and physical acceptance.

Review commands: `shasum -a 256` and `shasum -a 256 -c` for the join and both
nested manifests; `git diff --no-ext-diff --unified=80` from the exact baseline;
read-only inspection of all six required records and selected frozen JSON
receipts. No benchmark, build, browser, source, test, service, or status write was
performed. This reviewer changed only `REVIEW.md`.
