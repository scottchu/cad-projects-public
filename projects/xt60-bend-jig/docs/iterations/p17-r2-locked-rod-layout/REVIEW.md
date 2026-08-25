# P17-D13 / I13 review

## P17-C13 independent critic

Status: **BLOCK for product acceptance; faithful D13 materialization appears confirmed**.

Reviewer: `/root/p17_critic`  
UTC: `2026-08-25T21:39:34Z`  
Candidate fingerprint / independent gate manifest SHA-256:
`590e05f90e865f499af83c59350039ce20afc9ccd33bcad1975024aa3fba4b8c`.

### Scope and provenance

- Verified
  `projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist/p17-d13-independent-gate-manifest.sha256`
  file SHA-256 exactly matches
  `590e05f90e865f499af83c59350039ce20afc9ccd33bcad1975024aa3fba4b8c`.
- Verified manifest payload with `shasum -a 256 -c`: **21/21 OK** before
  critique.
- Candidate includes the D13 design contract, implementation input manifest,
  source, tests, ten STEP files, two motion sidecars, four PNG snapshots and one
  GIF.
- This review distinguishes two different questions:
  1. whether I13 faithfully materializes frozen user-locked D13 coordinates;
  2. whether that materialized layout is an acceptable product.

The answer is: **yes, it appears faithful; no, it is not product-acceptable**.

### Findings

#### Blocker C13-B01 — OPEN bottom rod intersects the frozen XT60 body

Evidence:

- Frozen D13 design states the bottom OPEN rod center is
  `(-4.7983156216,19.7949747468)` and the frozen XT60 body rectangle is
  `Y=-10.55..-2.45`, `Z=12.25..32.75`
  (`DESIGN.md` lines 102-118).
- Source intentionally computes this as a retained blocker, not an allowlisted
  pass (`p17_r2_direct_counter_twist.py` lines 2170-2221).
- Independent root-uv probe reproduced:
  - `bottomOpenSignedBodyClearanceMm = -2.0`
  - `bottomOpenBodyIntersectionMm3 = 199.8052927683109`
  - `knownInvalidProductInterface = true`

Disposition: blocks product acceptance and any fabrication/physical handoff.
This directly violates the no-XT60-plastic-load intent in `REQ-017`.

#### Blocker C13-B02 — OPEN bottom rod intersects the frozen vertical wire envelope

Evidence:

- Frozen design states the bottom OPEN center is only
  `1.7016843784 mm` from vertical-wire centerline `Y=-6.5`, against required
  rod+wire nonintersection distance `4.15 mm`, for `2.4483156216 mm` overlap
  (`DESIGN.md` lines 120-125).
- Independent root-uv probe reproduced:
  - `bottomOpenWireCenterlineSeparationMm = 1.7016843783999995`
  - `bottomOpenWireRadialOverlapMm = 2.448315621600001`
  - `bottomOpenWireIntersectionMm3 = 53.78737126188056`

Disposition: blocks product acceptance. This is an actual workpiece collision,
not a visual polish issue or force proxy.

#### Blocker C13-B03 — END no longer provides the three-point wire contact/preload

Evidence:

- Frozen design says END bottom/upright straight-feature gaps are
  `8.136965753 mm` and `2.244974747 mm`, and the diagonal rod also moves away
  from bend contact (`DESIGN.md` lines 127-134).
- Independent root-uv probe reproduced finite modeled-wire gaps:
  - bottom `8.136965752599998`
  - diagonal `16.71834015015733`
  - upright `7.877883157765334`
  - `lostEndContact = true`

Disposition: blocks `REQ-029`; the clamped/end-forming interface no longer
exists even though the coordinate transform is mathematically faithful.

#### Major / acceptance-blocking C13-M01 — Severe rail/path asymmetry remains

Evidence:

- Frozen design reports full left/right ratios bottom `1.859285084`, diagonal
  `1.605234636`, upright `3.071372411`; contact-END ratios bottom
  `1.876587387`, diagonal `1.750767749`, upright `4.243331211`; minimum contact
  crossing angle `4.387453 deg` (`DESIGN.md` lines 65-73).
- Independent root-uv probe reproduced `minimumCrossingSine =
  0.000748503000915208`, with rail reconstruction residual
  `7.105427357601002e-15`.

Disposition: this is a strong path/leverage-balance diagnostic and should block
advancement unless explicitly superseded. It is not a hand-force proof.

#### Minor C13-N01 — Static PNG labels are visually weak for review

Evidence:

- Four PNGs load and visually show the candidate states, but the rendered label
  says `ISO` even on files named `*_front` and `*_opposite`. The implementation
  receipt also notes this label issue (`IMPLEMENTATION.md` lines 43-46).
- The OPEN collision is visible through transparency, but not strongly called
  out; a viewer could miss it without the BREP numbers.

Disposition: not a geometry blocker because source/provenance/facts are clear,
but formal review should not rely on these PNG labels as authoritative camera
evidence.

### Faithfulness checks

No contrary evidence found that I13 cheated the D13 contract:

- Source constant `D13_COMMON_ROD_DELTA =
  (16.1869657526,10.2949747468)` is present (`p17_r2_direct_counter_twist.py`
  line 93).
- Source keeps `C=(3,12)` and `A=(-29,12)` (`p17_r2_direct_counter_twist.py`
  lines 182-185).
- Final `GUIDES` are derived by translating explicit I10 guides with the one
  D13 delta (`p17_r2_direct_counter_twist.py` lines 444-447).
- The shared transform authority is documented as
  `p_target = T_target^-1 * T_source * p_source`
  (`p17_r2_direct_counter_twist.py` lines 517-532).
- Focused pytest subset for coordinates, guide translation, rail endpoints and
  retained blocker tests passed: `6 passed`.
- Independent root-uv probe reproduced all rod centers, `A`, `C`, `D`, known
  blockers, rail reconstruction, minimum web `3.6323365469396114 >= 2.2`, and
  `allFixedWorldInvariant = true`.

### Requirement coverage

- `REQ-017`: **failed** by OPEN XT60 body loading/intersection.
- `REQ-029`: **failed** by lost END three-point wire contact/preload.
- `REQ-027`: frame convention appears preserved in source and D13 docs; visual
  PNG labels are weak but not source-authoritative.
- `REQ-028`: rod identities/topology are faithfully common-translated, but the
  translated placement is product-invalid.
- `REQ-009`, `REQ-010`, `REQ-022`: focused evidence supports fixed inner/axle
  and opposite outer transforms; no product acceptance follows from that.
- `REQ-030`: no self-lock/hard-stop claim found; endpoint is review travel only.
- `CON-013`: inverse rail reconstruction is satisfied digitally.

### Commands run

- `shasum -a 256 projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist/p17-d13-independent-gate-manifest.sha256`
  -> matched `590e05f90e865f499af83c59350039ce20afc9ccd33bcad1975024aa3fba4b8c`.
- `shasum -a 256 -c projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist/p17-d13-independent-gate-manifest.sha256`
  -> `21/21 OK`.
- `grep`/`sed`/`nl -ba` over source, tests, D13 docs, implementation receipt,
  manifest/provenance records and sidecars.
- `uv run --project projects/xt60-bend-jig pytest -q ... -p no:cacheprovider`
  on six focused tests -> `6 passed`.
- A broader full test attempt was interrupted after it reached the expensive
  `two_sided_support_evidence()` path in `BRepClass3d_SolidClassifier`; this
  does not affect the disposition because the product blockers above are
  independent and already fatal.
- `uv run --project projects/xt60-bend-jig python -u - <<'PY' ...` independent
  in-memory probe for A/C/D, rod states, blockers, inverse rails, web and fixed
  occurrence invariance.
- `uv run --project projects/xt60-bend-jig python - <<'PY' ... PIL ...` image
  packet check -> four PNGs `1800x1200 RGBA`; GIF `960x720`, `72` frames,
  `71/71` adjacent frame diffs nonempty.

### Unresolved risks

- Actual two-sided support was not independently rerun to completion in this
  critic session due the slow `is_inside` path. The candidate is blocked
  regardless; do not use the support claim to advance it past the known
  workpiece failures.
- Physical cap fit, PETG wear, rod wobble, force, heat, insulation marking,
  springback, endpoint retention and self-lock remain unproven.

### Critic disposition

**BLOCK for critic gate.** I13 appears to faithfully materialize the frozen
D13 locked-coordinate contract, but D13 itself is a known invalid product
layout. Next action is not implementation polish; it is explicit design/user
scope reopening to resolve XT60 body collision, wire collision, lost END
contact and rail/path balance.

## P17-R13 formal review

Owner: P17-R13 formal reviewer. Scope was acceptance-boundary arbitration for
the exact D13/I13/C13/V13 candidate only.

Status: **FORMAL BLOCK / REJECT for product, mechanical, physical, PR merge and
release.** The exact candidate is accepted only as a faithful digital
materialization/review artifact of a known-invalid D13 coordinate contract.

### Provenance verified

- Branch at review time: `codex/xt60-p17-r2-locked-rod-layout`;
  `git rev-parse HEAD` = `8adfb20f352e36cede54a3414307ced3de81c2b8`.
- Immutable candidate manifest:
  `projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist/p17-d13-independent-gate-manifest.sha256`
  SHA-256 =
  `590e05f90e865f499af83c59350039ce20afc9ccd33bcad1975024aa3fba4b8c`;
  independent verifier read all `21` entries and reported `ENTRIES_OK`.
- C13 critic REVIEW prefix before this append:
  `eabf464c6b94e58b8a2e51b88a8274ce34307da2c35401fba5428b21d0060fe3`
  over the first `8080` bytes.
- V13 validation record SHA-256 =
  `9a42f397fb3ab4c0f49feba5a9c7027638ae6d929bf5f55a85a336820c92f634`.
- Candidate records all bind to the same manifest/fingerprint boundary:
  `p17-r2-candidate-fingerprint.txt` contains the same `590e05...4b8c`
  fingerprint; the JSON fingerprint record states `entryCount: 21` and limits
  the claim to exact review materialization only.

### Acceptance by boundary

- Implementation fidelity: **ACCEPT for exact materialization only.** D13 fixed
  `A=(-29,12)`, retained `C=(3,12)`, and applied
  `D13_COMMON_ROD_DELTA=(16.1869657526,10.2949747468)`; C13 and V13 both found
  the source/artifacts faithfully match that contract.
- Written CAD/export: **ACCEPT as review artifacts only.** V13 reports 10/10
  written STEP source/export parity and actual-solid checks for this exact
  fingerprint. This does not overcome the known product blockers.
- Static visual/motion packet: **ACCEPT as static review evidence only.** The
  four PNG hashes match the manifest; the GIF hash matches, is `960x720`, has
  `72` frames, and sampled frame hashes differ. The PNG camera labels say `ISO`
  even for files named front/opposite, so filenames and deterministic geometry
  facts remain the authority.
- Viewer transport readiness: **ACCEPT for transport/asset loading only.** Local
  and Tailscale focused URLs returned page HTTP `200`; both
  `/__cad/artifact` requests returned HTTP `200` with `state:"ready"` for
  `p17_r2_full_motion.step.py`. Asset checks returned HTTP `200` for
  `assembly.json` (`schemaVersion: 2`, `packageSchemaVersion: 3`, 10
  components, 18 occurrences), `p17_r2_full_motion.params.js`, and one component
  GLB over both local and Tailscale. The params file has one
  `parameters.open_to_end` control. In-app browser/live slider manipulation was
  unavailable and is **not** accepted here.
- Product/mechanical acceptance: **REJECT/BLOCK.** This candidate fails the
  intended XT60 workpiece interaction and may not be treated as an acceptable
  jig merely because the invalid contract was materialized faithfully.
- Physical acceptance: **NOT ESTABLISHED / BLOCKED.** No print, slicer, DfAM,
  PETG compliance, cap retention, lock force, wear, heat, vibration,
  springback, insulation marking, or assembly-fit claim is made or accepted.
- PR/merge eligibility: **BLOCK for product PR merge/release.** It is suitable
  only as rejected evidence or review history if the coordinator chooses to
  preserve it; it is not eligible to merge or ship as an accepted P17 R2
  product candidate.

### Requirement coverage

- `REQ-017`: **failed.** OPEN bottom rod has signed XT60 body clearance
  `-2.000000 mm`; C13 records actual BREP body intersection
  `199.8052927683109 mm3`.
- `REQ-029`: **failed.** END no longer provides the required three-point wire
  contact/preload; V13 records lost END contact with bottom/upright gaps, and
  the design record identifies bottom/upright/diagonal contact loss.
- `REQ-027`: frame convention is preserved in source/provenance; weak PNG
  labels are a minor documentation/camera-label issue, not a source identity
  blocker.
- `REQ-028`: rod identities/topology were faithfully common-translated, but the
  translated layout is product-invalid because it collides with the body/wire
  envelope and loses END contact.
- `REQ-009`, `REQ-010`, `REQ-022`, `CON-013`: fixed inner/axle, opposite outer
  transforms and inverse rail reconstruction are digitally supported for the
  exact candidate; these do not imply product acceptance.
- `REQ-030`: no hard-stop, retention, detent, over-center, self-lock or physical
  lock claim is accepted.

### Formal findings

- **Blocker F13-B01:** OPEN XT60 body collision violates `REQ-017`
  (`-2.000000 mm` signed clearance; C13 body intersection
  `199.8052927683109 mm3`).
- **Blocker F13-B02:** OPEN wire-envelope collision violates the no-load/no-body
  path requirement (centerline separation `1.7016843784 mm`, radial overlap
  `2.4483156216 mm`; C13 wire intersection `53.787371493712925 mm3`).
- **Blocker F13-B03:** END contact/preload is lost, violating `REQ-029`.
- **Major F13-M01:** Severe rail/path asymmetry remains unresolved; it cannot
  be promoted to hand-force or mechanical acceptability evidence.
- **Minor F13-m01:** Static PNG labels read `ISO`; use deterministic source,
  hashes and geometry facts as the authoritative visual-state identity.

### Commands and results

- `git rev-parse --abbrev-ref HEAD` -> `codex/xt60-p17-r2-locked-rod-layout`;
  `git rev-parse HEAD` -> `8adfb20f352e36cede54a3414307ced3de81c2b8`.
- `shasum -a 256
  projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist/p17-d13-independent-gate-manifest.sha256`
  -> `590e05f90e865f499af83c59350039ce20afc9ccd33bcad1975024aa3fba4b8c`.
- `uv run python` manifest verifier -> `ENTRY_COUNT 21`, `ENTRIES_OK`.
- `shasum -a 256` on REVIEW/VALIDATION before append -> C13
  `eabf464c...0060fe3`, V13 `9a42f397...2f634`.
- `curl -k` local and Tailscale page URLs -> HTTP `200`; local and Tailscale
  `/__cad/artifact` -> HTTP `200`, JSON `state:"ready"`.
- `curl -k` local and Tailscale `__cad/asset` for assembly, params and one GLB
  -> all HTTP `200`.
- `uv run python` asset probe -> assembly SHA-256
  `ccb396346004d72e077ea6139b0cdc30f5127631df92274c6b5964a5d726db83`,
  sourceHash `1151a9ba1c7871a977b1ae92f6f55940b0b62ae2315d4f241b0d316f1c5ba7dc`,
  stepHash `522b1a9ff51dd38de40e5866962c5907159e73e3c8cd10fa5313e6a8246eab38`,
  10 components, 18 occurrences.
- `uv run python` PIL probe -> four PNG hashes matched manifest at `1800x1200`;
  GIF hash matched manifest, `960x720`, `72` frames, sampled frame hashes
  changed.

### Next action

Do not print, slice, release, or merge this candidate as accepted product work.
Reopen design/user scope to resolve the XT60 body collision, wire collision,
lost END contact/preload and rail/path asymmetry, then issue a new immutable
candidate fingerprint through independent critique, validation and formal
review.
