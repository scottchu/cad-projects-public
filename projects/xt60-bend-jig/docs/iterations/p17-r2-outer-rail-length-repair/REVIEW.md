# P17-C10 independent critic review

Status: **BLOCKED for candidate evidence**. I found no mechanical blocker in the
inspected D12-R1 rail-length, placement, web, collision, service, or preserved-
architecture evidence, but the frozen motion GIF is visually static despite the
candidate manifest claiming a 72-frame opposed-twist GIF. Regenerate or replace
the motion visual packet before formal acceptance.

Reviewed candidate:

- Candidate/fingerprint manifest:
  `/tmp/p17-i10-r1-independent-gate-manifest.txt`
- Candidate fingerprint:
  `5443e39e3b82bbbc2f6e3ed8dd6c2487a69035c263d44128a47f31ddab509d93`
- Delivery record manifest:
  `/tmp/p17-i10-r1-delivery-record-manifest.txt`
- Delivery record manifest SHA-256:
  `25b12189f6c5b43d8ce224bd66ef63cb12701abaed21917a8379217025cc082d`
- Candidate manifest entries: 24/24 matched before review.
- Delivery manifest entries: 6/6 matched before review.

## Findings

### Blocker: frozen motion GIF does not visibly animate

The file
`cad/p17_r2_direct_counter_twist/snapshots/p17_r2_i10_r1_full_motion_20260825T163402Z.gif`
is present and is encoded as an animated GIF with 72 frames, but decoded RGBA
frames are pixel-identical. A PIL frame-difference check against frame 0 returned
no non-empty bounding boxes for any of the 71 later frames. This contradicts the
candidate/provenance claim that the packet contains a 72-frame opposed-twist GIF
and was visually inspected as motion evidence.

This is an evidence blocker, not a geometry-law blocker. The sidecar source still
contains a correct `open_to_end` control, linear `24.0 * travel`, translated rod
paths, and opposite left/right rotations; focused tests passed those sidecar
checks. But the frozen visual packet itself does not demonstrate motion, so the
candidate should not pass the C10 gate until the GIF is regenerated or a
replacement motion artifact is frozen and hashed.

Disposition: block P17-C10 on motion visual evidence.

### No blocker found: six functional rail lengths and force diagnostics

The exact D12-R1 rail-length correction is implemented as a one-time translated
working set, not old rail solid reuse. Source defines `T=(-16.735,-14.935)` at
`src/xt60_bend_jig/p17_r2_direct_counter_twist.py:196`, derives workpiece
coordinates as properties at
`src/xt60_bend_jig/p17_r2_direct_counter_twist.py:224`, and translates accepted
pre-D12 guides once through `guide_path` at
`src/xt60_bend_jig/p17_r2_direct_counter_twist.py:490`. The dedicated evidence
function checks no-old-rail reuse and fixed axle rails at
`src/xt60_bend_jig/p17_r2_direct_counter_twist.py:2073`.

Independent probe results matched the contract:

- `T=(-16.735,-14.935)`, physical `C=(3,12)`, fixed axle `A=(-29,17)`,
  `C_rel=(19.735,26.935)`.
- `translationAppliedExactlyOnce=True`; maximum rigid-translation residual
  `1.776e-15 mm`.
- Old translated rails are not reused; minimum contact/end residual from naïvely
  translated old rails is `9.109841648 mm`.
- Functional rail ratios:
  - `bottom`: `14.062509916 / 12.380157783`, ratio `1.135891009`;
  - `diagonal`: `9.452391469 / 12.332546705`, ratio `1.304701222`;
  - `upright`: `15.321870406 / 13.793481567`, ratio `1.110805153`.
- Contact-to-END ratios:
  - `bottom`: `1.166307930`;
  - `diagonal`: `1.270524536`;
  - `upright`: `1.137221427`.
- Force-diagnostic multiplier ratios:
  - `bottom`: `1.167052996`;
  - `diagonal`: `1.271610389`;
  - `upright`: `1.137915858`.

These satisfy the D12-R1 `<=1.50` visual/functional balance target. The middle
rod is now the worst numeric ratio, not Rod 1 or Rod 2, which addresses the
original user defect. This remains only a geometric diagnostic; force, friction,
wear, and torque are not physically proven.

### No blocker found: web, support, collision, service, and working-area placement

Independent source evidence returned:

- maximum rail reconstruction residual `8.88e-15 mm`;
- maximum axle reconstruction residual `7.11e-15 mm`;
- minimum web `2.247514207972 mm` against required `2.20 mm`;
- minimum fixed extended-cutter gap `6.103048327205 mm`;
- minimum outer cutter gaps left/right `6.659754405892 / 6.819809099118 mm`;
- conditioning rank `3`, maximum condition `11.634572639008`;
- actual-solid motion `passes=True`, 65 states, exact contact included, minimum
  XT60 clearance `0.75 mm`, unintended intersection `0.0`, precontact wire
  intersection `0.0`, plate guides and fixed hardware clear;
- cap stack `passes=True`, rod length `50.0 mm`, cap count `6`, cap/plate/keeper
  intersection `0.0`;
- service path `passes=True`, minimum clearance `0.933815921231 mm`, BREP
  clearance `1.25 mm`, zero service intersection;
- fixed occurrences remain world-invariant and outer angles are
  `(-12,+12)`, `(-23.433,+23.433)`, and `(-24,+24)` at mid/contact/end.

The implementation receipt and provenance report continuous `+0.30 mm`
two-sided support strips passing at 65 states, with endpoint material ratio
`0.9999999999999983` and maximum boundary recession `0.005098333`. I attempted
to rerun `two_sided_support_evidence()` directly, but interrupted it after the
bounded critic window while it was inside build123d `is_inside` checks. That
interruption is not counted as a pass or failure; the blocker above is independent
of this slow support rerun.

The selected web margin is small: `2.247514 - 2.20 = 0.047514 mm`. Digitally this
meets the gate; physically it remains sensitive to print process, slicing,
material shrink, and wear. Do not treat this as PETG acceptance.

### No blocker found: architecture preservation

Focused tests passed the D12 translation, six rail endpoints/lengths, sidecar,
and no-added-structure checks. The production-count test requires three
`OD4_rod_L50.00` rods, six permanent caps, two inner fixed guides, two outer
guides, two press-fit keepers, and rejects `grip_block`, `stability_bar`, `yoke`,
`linkage`, `gear`, `lock_nose`, and `receiver`
(`tests/test_p17_r2_direct_counter_twist.py:376`). Sidecar tests verify
`open_to_end`, `24.0 * travel`, translated paths, no `smoothstep`, and no
animation transform applied to fixed axle, inner guides, or keepers
(`tests/test_p17_r2_direct_counter_twist.py:404`). Manifest tests retain endpoint
only/no self-lock semantics and physical-boundary wording
(`tests/test_p17_r2_direct_counter_twist.py:450`).

### Minor: still images are adequate for geometry but weak for rail-only visual review

The accepted open/contact/end/opposite/placement PNGs show that Rod 1 and Rod 2
no longer have the rejected visibly long/short rail imbalance, and the working
area has moved inward/back on the outer plate. However, the front views still
occlude parts of the rail centerlines behind rods/caps/plate overlap, and the
placement view is oblique rather than a clean rail-only orthographic overlay.
The numeric rail-length evidence is therefore stronger than the visual evidence.
This is nonblocking once the motion GIF is repaired, but a future packet should
include a rail-only or transparent overlay for all six rails.

## Commands and results

- `shasum -a 256 /tmp/p17-i10-r1-independent-gate-manifest.txt /tmp/p17-i10-r1-delivery-record-manifest.txt`:
  candidate manifest `5443e39e3b82bbbc2f6e3ed8dd6c2487a69035c263d44128a47f31ddab509d93`;
  delivery manifest `25b12189f6c5b43d8ce224bd66ef63cb12701abaed21917a8379217025cc082d`.
- Python manifest verifier:
  independent manifest `24` entries, `0` failures; delivery manifest `6`
  entries, `0` failures.
- Targeted source evidence probe:
  source SHA `0d66dd9b0668c976750036c03bb8b8886a04df2d557ddee4330e933072161060`;
  design SHA `5017d540e83cbdbf6ccc41fc2d7173f2ad4e2b70f1387695b7182bc41863affc`;
  numeric results listed above.
- `uv run --project projects/xt60-bend-jig pytest -q projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py -k 'd12_translation or d12_six_outer_rails or motion_sidecars or exact_production_counts'`:
  `4 passed`.
- GIF inspection with PIL:
  `is_animated=True`, `n_frames=72`, `unique_frame_hashes=72`, but
  `nonempty_diff_count=0 of 71` when comparing decoded RGBA frames to frame 0.
- Visual inspection:
  `p17_r2_i10_r1_open_front_20260825T163146Z.png`,
  `p17_r2_i10_r1_contact_front_20260825T163146Z.png`,
  `p17_r2_i10_r1_end_front_20260825T163146Z.png`,
  `p17_r2_i10_r1_end_opposite_20260825T163206Z.png`, and
  `p17_r2_i10_r1_open_placement_review_20260825T163206Z.png` inspected.

## Requirement coverage

- User defect, all six rails: addressed numerically; Rod 1 and Rod 2 are no
  longer the outliers and all full/contact rail ratios are `<=1.50`.
- Working-area placement: addressed by one named rigid translation with `A`,
  `C`, plate envelopes, and keepers fixed.
- Plate-edge material: digital web and support evidence pass, with small
  `0.047514 mm` web margin remaining as physical risk.
- Preserved architecture: source/tests and visuals show no topology, slot-width,
  part-count, lock, yoke, gear, link, or follower change.
- Motion packet: blocked because the frozen GIF is visually static, despite
  correct sidecar semantics.

## Physical boundary

This review does not accept PETG printability, cap retention, slot wear/wobble,
hand torque, friction, wire clamping, heat behavior, cooled bend angle, or
self-lock. The force numbers remain geometry diagnostics only.

## Disposition

P17-C10 critic gate: **BLOCK** until the motion visual artifact is repaired and
the exact candidate/evidence manifest is re-frozen. After that repair, the
geometry should be rechecked against the same fingerprint discipline; I found no
separate mechanical blocker in the inspected numeric evidence.
