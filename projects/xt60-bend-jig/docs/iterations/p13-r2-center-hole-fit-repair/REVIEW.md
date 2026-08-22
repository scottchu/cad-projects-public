# P13 R2 center-hole fit repair review

## Review baseline

- Immutable repository baseline: `b0b79253373c7cf80943e99df8ab799958c50d49`
- Geometry change authorized: enlarge only the exact source-controlled hole responsible for the diagnosed printed stick/hole failure.
- Locked scope: P13 architecture, purchased rods, motion contract, wire preload domain, print orientation, and unrelated fits.

## Independent findings

Critic, review, and validation findings and their dispositions will be recorded here against exact regenerated paths and revisions.

## Current finding

| ID | Severity | Finding | Resolution | Status |
|---|---|---|---|---|
| `P13-R2-REV-001` | high | Latest printed P13 cannot assemble because the user's "middle stick" is too thick for the "center hole"; exact source interface not yet identified. | Diagnose from source, artifacts, and assembly sequence before selecting a parameter. | open |

## Independent critic receipt — `P13R2-C01`

- Owner/role: `/root/independent_critic`, independent mechanical/CAD critic;
  distinct from design, implementation, validation/test, and formal review.
- Candidate fingerprint verified on entry and after this read-only audit:
  `616b951822ed302ef71de8a3ee0752406dd1f84efb1edc99617af403bf8bc6a9`
  over the 53-entry path/content manifest declared in `BRIEF.md`.
- Candidate source, tests, STEP/3MF, provenance, release manifest, snapshots,
  and acceptance records were not changed. This critic wrote only this section.
- Self-approval boundary: this is a critique receipt, not implementation approval,
  validation acceptance, formal review, slicer acceptance, or physical acceptance.

### Scope and mechanical audit

The mate diagnosis is supported by three independent repository traces. The
production 3MF contains one printed stick-like member,
`separate_printed_D_shaft_OD5p60_AF5p15_theta_0p00`, excludes all three
purchased rods, and contains the two matching D-bored cams. The source builds
that shaft at `OD5.60 / AF5.15 mm` and uses only the shared
`cam_d_bore_od`/`cam_d_bore_across_flat` cutter for the centre D bores in
`left_D_bore_cam_OD40p50_theta_0p00` and
`right_D_bore_cam_actuator_OD40p50_theta_0p00`. Finally, the certified service
order removes the keeper, releases both side-entry fixed C guides in `-Z`, and
then extracts this shaft in `+X` through the two stationary cam bores. The
installed `ID4.80` fixed journals are deliberately forbidden axial paths, not
the diagnosed hole. This is therefore one repeated shaft-to-cam-bore interface,
not permission to enlarge rod lanes, fixed journals, keeper, or caps.

The authoritative source diff changes only the controlling amendment hash and
the two dimensions of that one shallow-D hole profile: `5.70 -> 5.75 mm` OD
and `5.25 -> 5.30 mm` AF. The shaft, three purchased `OD4 x 50 mm` rods,
`4.75 mm` lanes, `ID4.80` fixed C journals, `OD4.60` journal lands,
`ID4.80` keeper, caps, motion parameters, and source-authored print rotations
remain unchanged. A before/after imported-BREP comparison found removal only:
`2.003991502 mm^3` from each cam and `0.049700816 mm^3` from each fixed
thrust-land running relief. No material was added, and the other ten production
objects plus both diagnostic coupons had no geometric difference. The fixed
relief is the documented derived consumer of `cam_d_bore_od`; its main C journal
remains `ID4.80`.

At the selected values, both controlling profile allowances are `0.15 mm`
diametral (`0.075 mm` one-sided). The exact one-sided D lash is
`2.9405049698 deg`, leaving `0.0594950302 deg` below the `3 deg` CAD limit.
The controlling hub wall is `2.125 mm`, only `0.050 mm` above its
`2.075 mm` design minimum; the flat-side wall is `2.575 mm`. A conservative
centreline calculation gives `4.10 mm` between the enlarged circular bore
envelope and the nearest cam-lane envelope, so the hub wall, not a lane
ligament, remains controlling. Each cam engagement stays `4.50 mm`; the male
D flat is approximately `3.0447 mm` wide, or `13.701 mm^2` over one engagement.
These are geometry margins, not a PETG torque, wear, or strength certificate.

The staged `+X` service envelope is the correct path to recheck after this
repair; direct axial travel through installed fixed guides remains intentionally
inadmissible. The unchanged fixed-guide/keeper side-entry sequence and the
unchanged print transforms preserve the approved P13 architecture. Both
implementation snapshots were inspected at original resolution: the 14-object
STEP layout visibly contains the four plates, D shaft, keeper, six caps, and two
separate diagnostic coupons without a gross placement error; the locked-motion
view shows the expected four-plate/three-rod assembly without an obvious
omission or gross interference. The internal D fit is not visually resolvable,
so neither snapshot is fit evidence.

The production 3MF provenance reports exactly 12 objects, no purchased rods or
proof envelopes, zero pairwise layout-box overlaps, a `136.269 x 105.050 mm`
footprint, positive source/mesh volumes, manifold/oriented meshes, lib3mf
round-trip success, and source-defined principal bed contact. For the repaired
cams, the stored tessellation volume error is about `0.0113%`. A fresh DfAM
measurement could not be performed by this critic because the installed
`dfam_tool.py` stopped at `ModuleNotFoundError: No module named 'trimesh'` in
the root environment; no fresh wall/overhang/support verdict is claimed here.
The source-controlled `2.125 mm` hub wall exceeds the skill's conservative
FDM wall limits (`1.2 mm` supported, `1.6 mm` unsupported), the repaired
`5.75 mm` through bore exceeds its `2.0 mm` minimum-hole reference, and the
cam bore prints vertical in the unchanged plate-flat orientation, but the
independent validator must own any measured DfAM/slicer acceptance.

### Explicit parity-tolerance audit

The `tests/p13_geometry_case.py` change from seven to six decimal places does
not mask a meaningful source/export mismatch in this candidate. Independent
source-versus-written-STEP measurements on `left_cam`, `right_actuator`,
`print_kit`, and `service_disassembly` found a worst affected-cam leaf-volume
difference of only `5.98e-10 mm^3`. That tiny difference straddles a
seven-decimal rounding boundary (`2881.2848331` versus `2881.2848332`) even
though it is about 167 times smaller than one `1e-7 mm^3` rounded unit. Six
decimal places admit less than approximately `1e-6 mm^3` while the intended
`0.05 mm` OD/AF repair removes `2.003991502 mm^3` from each cam—more than two
million times that tolerance. Labels, per-leaf solid counts, and the separate
`2e-6 mm` bounds test remain exact independent guards. The relaxed comparison
is therefore adequate for this repair, but an explicit absolute-volume
tolerance would communicate intent better than decimal rounding.

### Severity-ranked findings

| ID | Severity | Finding | Candidate disposition |
|---|---|---|---|
| `P13R2-C-001` | medium, physical gate | The `0.15 mm` target is inferred from a PETG printed-hole/metal-rod coupon, while this interface is a printed vertical D bore mating with a printed horizontal D shaft. Two printed dimensional errors, elephant foot, seam, and anisotropy may consume the allowance. | Not a CAD/artifact blocker; blocks physical acceptance. Reprint the two cams and unchanged shaft, verify insertion through both cams, then assemble in the certified order. |
| `P13R2-C-002` | medium, physical gate | Lash and wall pass the frozen CAD limits but with small margins (`0.0595 deg` and `0.050 mm`). Actual torque transfer, actuation play, hub cracking, wear, and heat response are unmeasured. | Not a candidate blocker. During reprint acceptance, check dry `0..27 deg` cycling, rotational play under hand load, hub damage, and repeat fit after use/heat. |
| `P13R2-C-003` | low, test clarity | Six-decimal volume canonicalization is quantitatively non-masking here, but its comment describes the rounded-bin change rather than the actual sub-nanocubic-millimetre delta, and rounding is less explicit than an absolute tolerance. | Nonblocking. Retain for this candidate; consider an explicit `abs <= 1e-6 mm^3` comparison in a later test-maintenance change. |
| `P13R2-C-004` | informational, evidence pending | This critic could not run the fact-only DfAM tool because `trimesh` is absent. Stored 3MF integrity/orientation and exact parametric margins are favorable, but support/slicer facts remain the validator's gate. | Independent validation must record the available DfAM and slicer result or an honest tool limitation. |

No blocking source, geometry, scope, or release-artifact defect was found in
the frozen candidate. `P13-R2-REV-001` is digitally diagnosed and represented
by the focused regression, but its physical failure is not closed until the
repaired print is assembled successfully.

### Requirement coverage

- `REQ-001`, `REQ-002`, `REQ-004`–`REQ-007`, `CON-001`–`CON-005`: preserved
  by the source diff and regenerated source-derived state/service artifacts;
  independent deterministic validation remains the acceptance gate.
- `REQ-003`, `CON-006`: the three purchased `OD4 x 50 mm` rods, their lanes,
  and the role-specific `4.15 mm` reference are unchanged; rods remain absent
  from the production 3MF as required.
- `REQ-008`: stored export provenance shows the exact 12-object production
  census; the STEP review kit's two extra objects are explicitly diagnostic
  coupons and are excluded from the production 3MF.
- `CON-007`: satisfied digitally by an exact shaft/two-cam repeated-interface
  diagnosis, a hole-only named-parameter repair, a failing-before/passing-after
  focused regression, and frozen unrelated-fit/orientation assertions.
- `PHYS-001`–`PHYS-006`: not accepted. `PHYS-001` now has a repair candidate;
  all require the repaired PETG print and the documented assembly/use trial.

### Commands and evidence used

- Candidate fingerprint: the exact `awk`/`shasum -a 256` 53-entry manifest
  command declared by the orchestrator; result `616b9518...bf8bc6a9`.
- Source scope: `git diff --unified=3 b0b79253373c7cf80943e99df8ab799958c50d49 --`
  against the P13 source and focused tests.
- Quantitative BREP diff: root-workspace `uv run --project
  projects/xt60-bend-jig python` importing the preserved baseline and current
  `p13_left_cam.step`, `p13_right_actuator.step`, and `p13_print_kit.step`,
  then evaluating per-label subtraction volumes.
- Parity audit: the same root `uv` environment rebuilt source artifacts and
  imported current STEP leaves for `left_cam`, `right_actuator`, `print_kit`,
  and `service_disassembly`; labels/counts matched and the maximum relevant
  absolute volume delta was `5.98e-10 mm^3`.
- Visual review: both PNGs under
  `docs/review/p13-r2-center-hole-fit-repair/` opened at original resolution.
- DfAM attempt: `uv run --project projects/xt60-bend-jig python
  .../dfam-check/scripts/dfam_tool.py measure .../p13_print_kit.3mf
  --angle-limit 45`; stopped before measurement because `trimesh` is absent.

### Affected-gate critic recheck — `P13R2-C01-R1`

- Revised candidate fingerprint verified:
  `9f123ad24f46d60fcb89ae305455ba1a0c3b38d4738f82766ec91d02c1350db9`
  over the same 53-entry manifest. The only candidate delta is
  `tests/test_p13_four_plate_three_rod.py` at SHA-256
  `f0f63a8c35b1cb8100703e5bc0c49fd26eca00b045397154c7fd826dab20654f`;
  source, STEP/3MF, provenance, release manifest, and snapshots are unchanged.
- The changed assertion is stricter, not weaker. It replaces a partial
  substring built from `str(20.88) -> 20p88` with the source's explicit
  three-decimal tag `20p880` and requires the complete exact label
  `P13_REMOVE_global_command_20p880mm_full_workpiece_caps_off_rods_left`.
  This catches suffix, command-format, and role-label drift that the prior
  substring check could miss.
- Focused recheck command:
  `uv run --project projects/xt60-bend-jig pytest -q
  projects/xt60-bend-jig/tests/test_p13_four_plate_three_rod.py::test_domain_a_global_command_is_closed_form_outward_and_not_the_nominal_seed`;
  result: `1 passed`.
- Disposition: no new finding and no prior finding is weakened. The exact mate,
  hole-only scope, BREP/parity analysis, DfAM limitation, and requirement
  coverage carry forward unchanged. `P13R2-C-001` and `P13R2-C-002` remain
  nonblocking CAD/artifact findings that block physical acceptance until the
  repaired PETG reprint, assembly, cycling, play/torque, wear, and heat checks.
  `P13R2-C-003` remains a low test-clarity note on volume comparison only;
  `P13R2-C-004` remains an informational DfAM-evidence boundary.

## Formal independent review receipt — `P13R2-R01`

- Owner/role: `/root/formal_reviewer`, formal independent reviewer; distinct
  from the design, implementation, critic, and validation/test owners.
- Candidate fingerprint verified on entry and exit with the exact 53-entry
  rule declared in `BRIEF.md`:
  `9f123ad24f46d60fcb89ae305455ba1a0c3b38d4738f82766ec91d02c1350db9`.
- The critic affected-gate recheck and validator affected-gate revalidation
  both name that same fingerprint. The only candidate change after their
  first-cycle receipts was the bounded exact-label assertion repair in
  `tests/test_p13_four_plate_three_rod.py`; source, STEP, 3MF, provenance,
  release manifest, and snapshots remained byte-identical.
- Candidate scope was read-only. This reviewer changed only this formal-review
  section and did not modify source, tests, CAD, artifacts, provenance,
  release metadata, snapshots, validation evidence, acceptance state, Viewer
  state, or git state.

### Join-gate audit

| Gate | Formal-review finding | Disposition |
|---|---|---|
| Exact failed mate | The production 3MF contains one printed stick-like part, `separate_printed_D_shaft_OD5p60_AF5p15_theta_0p00`, no purchased rods, and both matching D-bored cam plates. Source and the certified service sequence independently show that the shaft traverses the left and right cam D bores after keeper and fixed-guide release; the installed `ID4.80` fixed journals are deliberately not the axial path. | `P13-R2-REV-001` is resolved digitally as the one repeated printed-shaft/shared-cam-bore interface. Its physical-fit portion remains open until reprint. |
| Smallest source repair | The authoritative source diff changes only the controlling amendment hash and `cam_d_bore_od 5.70 -> 5.75 mm` plus `cam_d_bore_across_flat 5.25 -> 5.30 mm`. The `OD5.60 / AF5.15 mm` shaft, three purchased `OD4 x 50 mm` rods, lanes, fixed journals and lands, keeper, caps, motion, architecture, and authored orientations remain frozen. The fixed thrust-land running relief is the documented derived consumer of `cam_d_bore_od`, not a blanket bore change. | Passes `CON-007` and the explicit non-goals. |
| Fit math and focused regression | Baseline circular and D-flat diametral-equivalent allowances were both `0.10 mm` and failed the new `>=0.15 mm` regression; repaired values are both `0.15 mm` and pass. One-sided D lash is `2.9405049698 deg <= 3 deg`; hub wall is `2.125 mm >= 2.075 mm`; engagement remains `4.50 mm`. Actual male/female solids and the staged `+X` shaft envelope are included in the regression. | Failing-before and passing-after evidence is adequate for the concrete digital defect. It is not physical-fit proof. |
| Deterministic CAD and service validation | After the exact fixed-three-decimal label-test repair, the focused regression passed, the previously failing label gate passed, and the full relevant suite completed `60 passed`. The validator covered actual-solid collision, math, constraints, user requirements, continuous motion/removal, staged service extraction, and repository structure. | Pass. The first-cycle deterministic blocker is resolved on the final fingerprint. |
| STEP and source/export parity | `p13_print_kit`, both repaired cam parts, `p13_motion`, and `p13_service_disassembly` validated as actual written solids. All wrapper parity gates passed. The release manifest SHA-256 is `406325612e34c5c6fce95d96a2fe074591fdf502f592f172c47d016df5a54356`; all 34 indexed artifact hashes and both separately indexed provenance hashes reconcile. | Pass. Primary STEP is `5237fe9bc908781ae5793c9ab004f4fc51d24720244b26846bb1dacba63256b7`; production 3MF is `588f11e47c89a64221e527085e560453d4e7e75a7b6ecc00cf448f7d22bf75a7`. |
| Parity-volume tolerance | The seven-to-six-decimal canonical volume change was audited independently. The largest measured source/STEP leaf delta was below `6e-10 mm^3`, while six-decimal comparison retains an approximately `1e-6 mm^3` scale plus exact labels/counts and the separate `2e-6 mm` bounds gate. The intended cam removal is about `2.004 mm^3` per cam. | Accepted for this candidate; it cannot plausibly mask the intended repair or a meaningful source/export mismatch. An explicit absolute-volume tolerance would be clearer future test maintenance but is not a blocker. |
| Snapshots, mesh, orientation, DfAM, and slicer | Both committed snapshots and fresh validator snapshots show the complete print/review census without gross omission or placement error. The exact 12-body production 3MF is watertight/manifold, has zero layout-box overlaps, and preserves source-defined bed faces. Generic DfAM measurement selects the current orientation and passes the shaft/cams, while flagging unchanged `0.8 mm` cap and `1.0 mm` keeper p05 walls against its conservative `1.2 mm` default. OrcaSlicer 2.4.2 produced Snapmaker U1 / `0.4 mm` / PETG / supports-off G-code with source orientation preserved and XY arrangement only. | Accepted for a repaired test print with the inherited cap/keeper DfAM flags recorded as manufacturing/physical risks, not waived as universal printability proof. |
| Viewer | The exact Tailscale page returned HTTP `200`, the Viewer listens on `*:3245`, and validation obtained `ready` plus the concrete assembly payload (`10` unique components, `14` occurrences). | Pass. Repaired source render URL is recorded below. |

### Severity-ranked formal findings and dispositions

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| `P13R2-R-001` | medium, physical gate | The `0.15 mm` profile allowance is informed by same-process rod-hole evidence but mates two differently oriented printed D profiles. Actual insertion, play, torque transfer, hub stress, cycling, wear, and heat response remain unknown; lash and hub-wall CAD margins are small. | Does not block CAD/source or artifact/slicer advancement. It blocks physical acceptance until the repaired cams and unchanged shaft are printed and exercised in the complete assembly. |
| `P13R2-R-002` | medium, manufacturing risk | Generic DfAM flags the six unchanged caps at `0.8 mm` p05 and the unchanged keeper at `1.0 mm` p05 against a conservative `1.2 mm` FDM default. These features were not altered by the D-bore repair, and the exact artifact sliced supports-off. | Nonblocking for this focused repaired test print. Inspect cap/keeper print quality, retention, damage, and wear during the physical gate; reopen source only if that observation fails. |
| `P13R2-R-003` | low, evidence clarity | Six-decimal volume canonicalization is quantitatively strict enough here, but absolute tolerance would communicate the intended threshold more directly. | Accepted and resolved by the independent quantitative audit; defer optional test-style cleanup to a later non-CAD maintenance change. |
| `P13R2-R-004` | informational, release-state provenance | The frozen release manifest conservatively records its build-time status as awaiting independent validation/review. The completed post-generation critic, validator, and formal-review receipts necessarily live outside that candidate manifest so appending them does not invalidate its fingerprint. | No candidate rewrite is required. Final `HANDOFF.md`, `PROJECT_STATE.md`, and `NEXT_AGENT.md` must carry the current post-review acceptance states and this exact manifest/fingerprint. |

No unresolved blocking or high-severity candidate finding remains. The two
medium findings are explicitly physical/manufacturing observation gates and do
not justify broadening this local hole-only repair.

### Requirement and acceptance conclusion

- `REQ-001` through `REQ-008` and `CON-001` through `CON-006` remain traced by
  unchanged architecture/stock/motion/orientation constraints plus the full
  deterministic and written-artifact suite. `CON-007` is satisfied by the
  exact-mate trace, focused failing-before/passing-after regression, and
  hole-only named-parameter source diff.
- The production census remains four principal plates, one printed D shaft,
  one keeper, three permanent left caps, and three removable right caps;
  purchased rods and proof-only geometry remain excluded. The STEP review kit
  intentionally adds two diagnostic coupon objects.
- CAD/source status: **accepted for the P13 R2 repaired-print candidate**.
- Written artifact/slicer status: **accepted for a repaired Snapmaker U1 PETG
  test print**, with the inherited generic cap/keeper DfAM risks above.
- Physical status: **failed/pending**, not accepted. The latest printed P13 did
  not assemble. Reprint the two repaired cam plates with the unchanged shaft,
  verify passage through both cam bores, then check complete assembly, dry
  `0..27 deg` motion, play/torque transfer, cap/keeper behavior, cycling, wire
  handling, solder access, heat response, removal, cooled angle, and springback.

Exact Tailscale CAD Viewer URL, independently rechecked as HTTP `200` during
formal review:

<http://100.70.144.56:3245/Users/scottchu/.codex/worktrees/79caa408-e84c-4bfe-adfd-fa9ba1a1e186/design-projects/projects/xt60-bend-jig?file=cad%2Fp13_four_plate_three_rod%2Fp13_print_kit.step.py>

Formal-review conclusion: this exact fingerprint may advance to orchestration
closeout, commit, and safe fast-forward push. That decision approves the
source-derived CAD and written repair package for reprint; it does not close
physical acceptance.
