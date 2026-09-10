# P17-D12-R1 design handoff

Status: design frozen against the paused D12 I10 source/test checkpoint. D12
`T=(-7,-6.5)` is rejected and superseded. No source, test, CAD artifact,
Viewer or git change was made by D12-R1.

## Implement exactly

1. In the current named working-set translation parameter, replace only
   `T=(-7.00,-6.50)` with `T=(-16.735,-14.935)`.
2. Keep physical `C=(3,12)`, axle `A=(-29,17)`, plate envelopes/hierarchy,
   linear `24u` opposite rotation, `4.15` rail section and all pre-translation
   rod/workpiece dimensions unchanged.
3. Derive all rod, XT60/wire and service coordinates once from `T`; do not add
   scattered replacement literals or translate an already translated solid.
4. Regenerate every dependent OPEN/mid/contact/END/exploded/print-kit STEP,
   sidecar, snapshot and motion-review artifact from source.
5. Replace old-D12 numeric expectations with D12-R1 exact tables while keeping
   all relative-geometry, assembly-count and defect-regression gates.

## Allowed implementation writes

- `projects/xt60-bend-jig/src/xt60_bend_jig/p17_r2_direct_counter_twist.py`;
- `projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py`;
- affected P17 R2 STEP generators and regenerated STEP/sidecar/snapshot/motion
  review artifacts with provenance and checksums;
- this file's implementation receipt section.

No requirements/prior-history rewrite, topology/slot/plate/count change,
unrelated project, slicer/3MF, new part, or physical claim is allowed.

## Required receipt

Return the verified R1 implementation-manifest SHA, exact changed paths and
root-`uv` commands; rail/force tables; rigid-translation and relative-geometry
proof; actual-solid web/support/collision/service/conditioning; STEP parity;
visual packet; and one immutable candidate fingerprint. Stop rather than patch
topology if minimum web `2.20` or occupied-segment `0.30` support fails.

Physical acceptance remains open for cap retention, slot wear/wobble, PETG
compliance, real hand torque and three-rod wire clamping.

## P17-I10 implementation receipt — D12-R1 candidate

Status: implementation complete; independent critique, validation, formal
review and physical acceptance remain pending.

- Frozen input: `IMPLEMENTATION_INPUT_MANIFEST.sha256`
  `76acc0507b283d8ac5b10b5fc9eaa01eb51f8b68c7c60d93019cbad7867a2b86`;
  every declared entry verified before the R1 write.
- Source/test: named one-time working-set translation
  `T=(-16.735,-14.935)` with physical `C=(3,12)`, `A=(-29,17)` unchanged.
  All rods, XT60/wire and service references derive once from `T`; all six
  outer rails are reconstructed from translated rod centers, not reused or
  translated old rail solids. Part topology and the `4.15 mm` slot section are
  unchanged.
- Exact functional rail lengths `(left,right,ratio)` in mm:
  bottom `(14.062509916,12.380157783,1.135891009)`, diagonal
  `(9.452391469,12.332546705,1.304701222)`, upright
  `(15.321870406,13.793481567,1.110805153)`. The maximum ratio is
  `1.304701222`, below `1.50`; rejected D12 ratios were
  `1.516917371/1.379884550/2.012551004`.
- Contact-state force diagnostics `(left,right,ratio)`: bottom
  `(2.30107502,1.97169711,1.167052996)`, diagonal
  `(2.32863800,2.96112028,1.271610389)`, upright
  `(1.81049287,1.59106041,1.137915858)`. These are geometric diagnostics,
  not physical force or self-lock claims.
- Focused root-uv command:
  `uv run --project projects/xt60-bend-jig pytest projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py -q`
  passed `21/21` tests. The gates include exact translated coordinates and six
  rail endpoints, unchanged relative geometry/fixed axle/counts, no old-rail
  reuse, continuous two-sided `0.30 mm` occupied-segment support at 65 states,
  closed caps, actual-solid collision/contact/service, web and conditioning.
- Digital minima/maxima: web `2.247514208 mm`; fixed extended-cutter gap
  `6.103048327 mm`; outer cutter gaps left/right
  `6.659754406/6.819809099 mm`; rail reconstruction residual
  `5.4e-15 mm`; normalized condition number `11.634572639`, rank `3`;
  service clearance `0.933815921 mm` with zero unintended intersection.
- Regeneration: root-uv CAD `scripts/gen --write --force --json` built all ten
  explicit STEP targets. `scripts.inspect refs` and `scripts.inspect validate`
  passed `10/10`. Source/imported-STEP parity passed `10/10`; maximum bounds
  delta `6.253e-12 mm`, maximum summed-volume delta `1.118e-8 mm3`.
- Visual evidence: five current PNGs and one 72-frame/18-fps/4-second opposed
  twist GIF under `cad/p17_r2_direct_counter_twist/snapshots/`; render warnings
  were empty and the OPEN/contact/END/opposite/translated-placement packet was
  visually inspected. A stale imported-STEP render cache was isolated
  recoverably at `/tmp/p17-i10-stale-imported-step-render-cache-20260825/`;
  rebuilt cache bounds match D12-R1 STEP content.
- Frozen candidate fingerprint:
  `5443e39e3b82bbbc2f6e3ed8dd6c2487a69035c263d44128a47f31ddab509d93`
  over 24 verified entries in
  `/tmp/p17-i10-r1-independent-gate-manifest.txt`.
- Physical boundary: no PETG print, cap retention, hand torque, friction,
  wear/wobble, wire clamping or self-lock has been physically proven.

## P17-D12-R2 superseding design handoff

Status: `DESIGN FROZEN`; implementation and independent evidence pending. This
supersedes the I10/D12-R1 placement only. No source, test, CAD artifact, Viewer
or git write was made by the R2 designer.

Implement exactly one source parameter change from I10
`T=(-16.735,-14.935)` to `T=(-12.350,-10.550)`. Keep `A=(-29,17)`, physical
`C=(3,12)`, `C_rel=(15.350,22.550)`, linear `beta=24u`, opposite
`-beta/+beta`, every plate envelope, relative rod/workpiece state, straight
inner stroke, OD4 x 50 hardware, six caps and service sequence unchanged.

The implementation must recompute, not translate or reuse, all six rails using
`q=R(-alpha)(r-C)`. Exact world and local endpoint tables are in DESIGN
Section 6. The visible regression is a complete-working-set displacement of
`(+4.385,+4.385) mm` screen-right/up from I10. The OPEN relative box midpoint
must change from `(-10.743,-15.743)` to `(-6.358,-11.358)`.

Expected diagnostic maxima/minima are: full side ratio `1.405803849`,
contact-to-END side ratio `1.514484088`, minimum contact crossing angle
`8.166759353 deg`, minimum web `4.651875693`, minimum fixed-feature gap
`4.947934776`, XT60 clearance `0.750000`, service clearance `0.933815921`,
support material ratio `0.9999999999999982`, condition number `10.200550511`,
and zero unintended intersection. The contact ratio exceeds the preferred
`1.50` by `0.014484088` as an explicit placement-first decision.

Required implementation receipt: verify the updated immutable manifest before
writes; name exact source/test/artifact paths and root-`uv` commands; regenerate
all states, STEP/sidecars, motion and visual placement evidence; prove source/
STEP parity; and obtain independent critique, validation and formal review.
Stop if any actual-solid, web `>=2.20`, continuous support, collision/contact,
service, conditioning or right/up placement regression fails. Do not claim
physical hand force, clamp force, cap fit, wear, retention or self-lock.

## P17-D12-R3 superseding fixed-axle handoff

Status: `DESIGN FROZEN`; implementation and independent evidence pending. No
source, test, CAD artifact, Viewer or git write was made by the R3 designer.

Implement only fixed purple axle datum `A=(19.250,11.000)`, relative to
unchanged `C` as `(16.250,-1.000)`. This replaces I11 `A=(-29,17)`.
Do not change R2 `T=(-12.350,-10.550)`, the six rod rails, rod/workpiece states,
plates, `C`, motion angles, slot widths, axial hardware or architecture.

Recompute the two fixed-axle guides with
`q_A,s=R[-alpha_s](A-C)`. Their exact OPEN/contact/END endpoints and
`6.819660489 mm` length are in DESIGN Section 7. The axle and both keepers must
remain fixed at `A` in every state; inner hex bores share the same datum.

Implementation must reproduce: minimum web `2.447634348`, exact feature gap
`3.040481243`, outer guide webs `3.117105554/3.774308649`, fixed-guide support
ratio `0.9999999999999987` with continuous `+0.30` material, fixed hardware/
service clearance `1.213238136`, completed-pigtail service clearance
`0.933815921`, zero unintended intersection, fixed-frame invariance and
condition number `9.056843781` at rank `3`.

Visual regression must match `/tmp/p17-d12-r3-fixed-axle-overlay.html`: the
purple axle occupies the marked central-right down-sloping band, above the
tail/wire corridor, not the far-left I11 location and not the upper-right rim.
The nominal `A0=(17,12)` is not an allowed shortcut because its web is
`-0.014196`; `A=(19,11)` is also rejected for only `0.021355` margin.

Required receipt: verify the R3 manifest; name exact changed paths and root-uv
commands; prove only the axle/inner bores/fixed guides/keepers changed; regenerate
all dependent STEP, sidecars, motion and snapshots; prove source/STEP parity;
obtain independent critique, validation and formal review. Physical keeper
press-fit, PETG wear, hand force and self-lock remain open.

## P17-I12 implementation receipt — D12-R3 candidate

Status: implementation and deterministic evidence complete; independent
critique, validation, formal review and physical acceptance remain pending.

- Frozen input manifest SHA-256
  `1a57f155865a834a8c8c24b205f6f1bf52553c0a7bdc5f819697dd03f63de343`
  verified `17/17` before writes. Candidate source/test SHA-256 are
  `60818ab3759a158a6d7e480e4d47be9166e65a40c9ba21045133f14f030facd0`
  and `e39fdec7b062b84241703f1ac27469716365b8295bb391fa26d7a4df95433d70`.
- Implemented only fixed purple axle `A=(19.25,11.00)`, with unchanged
  `C=(3,12)`, so `A-C=(16.25,-1)`. The axle, both inner bores and both keepers
  share that fixed world datum. The two outer guide openings are inverse-frame
  loci; all six stainless-rod rails, `T=(-12.35,-10.55)`, rod/workpiece states,
  four plates, `4.15 mm` slots, three OD4x50 rods and six caps are unchanged.
- Exact guide endpoints `(OPEN,contact,END)` are left
  `(16.25,-1)/(15.307452615,5.544762793)/(15.251850330,5.695924992)` and right
  `(16.25,-1)/(14.512094177,-7.379811827)/(14.438377044,-7.523015908)`;
  analytic length is `6.819660489 mm`.
- Actual-solid gates passed: minimum web `2.447634348 mm`; fixed-feature gap
  `3.040481243 mm`; left/right outer guide web `3.117105554/3.774308649 mm`;
  `132` support probes and continuous `+0.30 mm` material pass; unintended
  intersection `0.0`; fixed-hardware service clearance `1.213238136 mm`;
  completed-pigtail service clearance `0.933815921 mm`; conditioning rank `3`,
  sigma ratio `0.110413741`, condition `9.056843781`.
- Root command
  `uv run --project projects/xt60-bend-jig pytest projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py -q`
  passed `24/24`. All ten explicit generators were rebuilt with root-uv
  `scripts/gen --write --force --json`; `scripts/inspect refs` and
  `scripts/inspect validate` passed `10/10`; source/export parity passed
  `10/10`, with maximum bounds delta `1.322e-12 mm` and maximum summed-volume
  delta `1.246e-8 mm3`.
- A stale imported-STEP snapshot cache, not a dynamic axle transform, caused
  the prior visual discrepancy. It was quarantined recoverably at
  `/tmp/p17-i12-stale-imported-step-cache.i8fUyg`. The sidecar dynamic feature
  maps exclude the axle and keepers, and the fixed occurrence regression holds
  across `65` uniform states plus exact contact.
- Final review packet contains explicitly labeled FRONT and mirrored OPPOSITE
  OPEN/contact/END PNGs, one source-derived placement/rail overlay and a fresh
  72-frame/18-fps/4-second FRONT GIF. FRONT keeps XT60 head up and tail/wires
  right and shows the purple axle center-right at one fixed camera. RGB decode
  found `72` unique frames and `71/71` nonempty adjacent differences.
- Immutable candidate manifest `/tmp/p17-i12-independent-gate-manifest.txt`
  verifies `24/24` entries. Candidate fingerprint SHA-256 is
  `b2069739bf7b27ccd87192834c1555dba250166d3bdba82e2ab2b3bfd1044b03`.
- Physical boundary: no PETG keeper/cap press-fit, wear, hand force, wire
  holding, friction, self-lock or physical acceptance has been proven.

### P17-I12 rejection and restoration checkpoint

The user rejected the I12 visual after the receipt above. The receipt,
candidate fingerprint and provenance are therefore **invalidated and must not
be sent to independent review**. Source was restored to the I11 purple axle
`A=(-29,17)` pending a separately frozen D12-R4 placement contract; only the
full-motion STEP was regenerated for a quick restoration preview.

Read-only audit proves the I12 R3 edit did not move the D12-R2 rods,
workpiece or six stainless-rod rails: their exact OPEN/contact/END coordinates
still match DESIGN Sections 6.2–6.3 and the full-motion parameter sidecar SHA
remained
`4ec9fa235a9ece9d7f4038f32e5ac2c883895e8cb08d3428d898591f20ae796a`.
The apparent shift comes from the old I11 PNG packet having resolved stale
D12-R1/I10 imported-STEP geometry. Plate-normalized OPEN rod centers in the
old PNG match D12-R1 `(-23.985,-2.5)/(2.5,-2.5)/(2.5,-28.985)`, while the
fresh restored-axle preview matches the correct D12-R2
`(-19.6003,1.885)/(6.885,1.885)/(6.885,-24.6003)` local centers. The old and
fresh purple-axle normalized centers are identical, confirming only the axle
restoration.

Restoration hashes: source
`d1e5fa6a95237e9680eee011c299dfb4bd90da487ec9599eb1e94ec6d7f1faa0`,
full-motion STEP
`3e4692c47536592376cbb53a09c91708b27c7173af611dd1caafaec8d51ec526`,
and unchanged full-motion sidecar
`4ec9fa235a9ece9d7f4038f32e5ac2c883895e8cb08d3428d898591f20ae796a`.
Quick preview files are
`/private/tmp/p17_i12_rejected_restore_i11_axle_open_front_20260825T184431Z.png`
and
`/private/tmp/p17_i12_rejected_restore_i11_axle_end_front_20260825T184431Z.png`.

### P17-D12-R4 quick-preview checkpoint — awaiting user visual acceptance

This is a **quick preview only**, not a frozen implementation candidate. The
selected preview datum is purple fixed axle `A=(24.00,20.00)` with unchanged
physical plate center `C=(3,12)`, so `A-C=(21,8)`. Only the axle datum, its two
inner hex bores, the inverse-frame outer fixed-axle guides and both keepers were
regenerated. The D12-R2 rods, XT60/workpiece, wire/service references and all
six stainless-rod rails remain exact: the pre/post working-set digest is
`a13a2cb0deef4c08b20bbd690b8cc74e377cd0f750810c0f86781ed1d09a1e58`.
The full-motion parameter sidecar is likewise unchanged at SHA-256
`4ec9fa235a9ece9d7f4038f32e5ac2c883895e8cb08d3428d898591f20ae796a`.

Two focused regressions passed for the exact R4 datum/guide endpoints and the
fixed axle/keeper world invariance across `65` uniform states plus exact
contact. No full suite was run at this preview gate. Actual-solid evidence has
zero axle/outer, keeper/outer, axle/rod, keeper/cap and service intersections;
minimum axle-to-white-rod clearance is `8.281448574 mm`, minimum
keeper-to-cap clearance is `7.082667194 mm`, and the combined hardware
clearance passes the required `>=7.082 mm`. Continuous `+0.30 mm` guide support
and `132` support probes pass.

Only `p17_r2_full_motion.step` was regenerated and validated. Its SHA-256 is
`207c30049bac284331e37fcea6b054d87eb50569fe749783481d958a13ba7f27`;
STEP refs report `19` occurrences / `18` leaves, and validation reports zero
failures. The other nine explicit STEP targets remain from the rejected I12
packet and were intentionally not regenerated for this quick preview.

The fixed-camera labeled evidence packet is:

- `snapshots/p17_r2_d12_r4_preview_open_front_labeled.png`
- `snapshots/p17_r2_d12_r4_preview_contact_front_labeled.png`
- `snapshots/p17_r2_d12_r4_preview_end_front_labeled.png`
- `snapshots/p17_r2_d12_r4_preview_open_opposite_labeled.png`
- `snapshots/p17_r2_d12_r4_preview_contact_opposite_labeled.png`
- `snapshots/p17_r2_d12_r4_preview_end_opposite_labeled.png`

The FRONT packet keeps the XT60 head up and tail/wires right and holds the
purple axle at the same pixel center across OPEN/contact/END; OPPOSITE is
explicitly labeled as mirrored. CAD Viewer page and exact artifact both return
HTTP `200`, with artifact state `ready`, at:
`https://mac-mini.duckbill-ionian.ts.net/Users/scottchu/Projects/personal/design-projects/projects/xt60-bend-jig?file=cad/p17_r2_direct_counter_twist/p17_r2_full_motion.step.py`.

Pending: user visual acceptance. No candidate fingerprint, independent review
or physical acceptance is claimed or requested at this checkpoint.

### P17-D12-R4b quick-preview checkpoint — supersedes R4 preview

The R4 `A=(24,20)` preview above is superseded for visual review by the
recommended true center-right fixed axle `A=(30.00,12.00)`. Physical plate
center remains `C=(3,12)`, hence `A-C=(27,0)`. Only the axle datum, dependent
inner hex bores, inverse-frame outer fixed-axle guides and keepers changed.
The D12-R2 rods, XT60/workpiece, wires/service references and all six
stainless-rod rails remain exact: pre/post working-set digest
`a13a2cb0deef4c08b20bbd690b8cc74e377cd0f750810c0f86781ed1d09a1e58`.
The full-motion parameter sidecar also remains unchanged at SHA-256
`4ec9fa235a9ece9d7f4038f32e5ac2c883895e8cb08d3428d898591f20ae796a`.

Six focused A-dependent tests pass. Actual-solid evidence over `65` states has
zero axle/outer, keeper/outer, axle/rod, keeper/cap and XT60/service
intersections. Minimum fixed-hardware-to-rod/cap clearance is
`11.903129708 mm`; left/right outer boundary webs are `10.05/11.55 mm`;
minimum web is `8.294595306 mm`; minimum service clearance is `2.965 mm`.
The axle and keepers remain fixed in world coordinates for every state.

Only `p17_r2_full_motion.step` was regenerated. Direct BREP import confirms the
axle and keeper centers at `A=(30,12)`; refs and geometry validation pass with
`18` leaf occurrences and zero failures. A stale imported-STEP inspection
cache was quarantined recoverably under
`/tmp/p17-d12-r4b-stale-imported-cache/`; a subsequent frame inspection reports
the left keeper at `(-16.85,30,12)` as required.

The new fixed-camera visual packet is:

- `snapshots/p17_r2_d12_r4b_preview_open_front_labeled.png`
- `snapshots/p17_r2_d12_r4b_preview_contact_front_labeled.png`
- `snapshots/p17_r2_d12_r4b_preview_end_front_labeled.png`
- `snapshots/p17_r2_d12_r4b_preview_open_opposite_labeled.png`
- `snapshots/p17_r2_d12_r4b_preview_contact_opposite_labeled.png`
- `snapshots/p17_r2_d12_r4b_preview_end_opposite_labeled.png`
- `snapshots/p17_r2_d12_r4b_preview_contact_sheet.png`

FRONT preserves XT60 head-up/tail-right. Exact purple pixel bounds are
`(1057,531)-(1264,668)` with `17,545` classified pixels in OPEN, contact and
END, independently confirming the fixed axle does not move. The OPPOSITE row
is explicitly labeled mirrored.

CAD Viewer page and exact artifact both return HTTP `200`, with artifact state
`ready`, at:
`https://mac-mini.duckbill-ionian.ts.net/Users/scottchu/Projects/personal/design-projects/projects/xt60-bend-jig?file=cad/p17_r2_direct_counter_twist/p17_r2_full_motion.step.py`.

This remains a quick-preview gate only. No full suite, candidate fingerprint,
independent review or physical acceptance is claimed pending root/user visual
inspection.

## P17-D12-R4b frozen implementation handoff

Status: `DESIGN FROZEN`; the root visually selected `A=(30,12)` as the true
center-right location that does not occupy the stainless-rod working area.
This final contract supersedes rejected R3 `A=(19.25,11)`, temporary restore
`A=(-29,17)` and upper-right R4 preview `A=(24,20)`.

Implement exactly:

- keep `C=(3,12)` and set fixed purple axle `A=(30,12)`, hence `A-C=(27,0)`;
- change only the axle, two inner hex bores, two inverse-frame fixed-axle outer
  guides and two keepers implied by `A`;
- use guide `OPEN/contact/END` centers left
  `(27,0)/(24.773161951,10.737338915)/(24.665727356,10.981889363)` and right
  `(27,0)/(24.773161951,-10.737338915)/(24.665727356,-10.981889363)`;
- preserve analytic guide length `11.309733553 mm`, `33`-point polyline length
  `11.309652808 mm`, guide width `7.90 mm`, keeper OD/bore `10.00/7.55 mm`
  and radial capture `1.05 mm`;
- keep D12-R2 `T=(-12.350,-10.550)`, XT60 head-up/tail-right geometry, every
  rod state, straight inner track and all six outer rod rails unchanged with
  digest `a13a2cb0deef4c08b20bbd690b8cc74e377cd0f750810c0f86781ed1d09a1e58`;
- keep FRONT as `+Z` up / `+Y` right; label OPPOSITE as mirrored only.

The design evidence to regress is: minimum combined rod/cap clearance
`11.903129708 mm`; web `8.294595306 mm`; outer fixed-guide web left/right
`12.012572604/14.178129708 mm`; exact feature gap `12.012572604 mm`; boundary
web `10.05/11.55 mm`; fixed XT60/wire/service clearance `2.965 mm`; `132`
full support probes and continuous `+0.30 mm` strips; completed-pigtail service
`0.933815921 mm` with zero BREP intersection; conditioning rank `3`, sigma
ratio `0.101441491`, condition `9.857899236`; all unintended actual-solid
intersections zero through `65` states; fixed axle/keepers world-invariant
through those states plus exact contact.

Verify `IMPLEMENTATION_INPUT_MANIFEST.sha256` before editing. Return exact
changed paths and root-uv commands, source and test hashes, regenerated artifact
hashes, source/STEP parity, fixed-camera FRONT/OPPOSITE evidence and the
unchanged working-set digest. Independent critic, validator and formal reviewer
must remain separate from implementation.

Do not alter rods, rod rails, `T`, `C`, plate diameters, slot widths, motion,
architecture, parts or lock claims. Physical keeper/cap fit, PETG wear, rod
wobble, friction, hand force, wire holding, self-lock and physical acceptance
remain unresolved and must not be reported as proven.
