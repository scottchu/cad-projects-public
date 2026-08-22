# P13 R2 center-hole fit repair validation

## Environment and baseline

- Repository root: `design-projects`
- Worktree branch: `codex/xt60-p13-center-hole-fit`
- Requested and observed baseline: `b0b79253373c7cf80943e99df8ab799958c50d49`
- Python and JavaScript tooling: root `uv` and npm workspaces only

## Planned commands and evidence

Exact commands and results will be appended as they run. Required categories are focused defect regression, object collision, math, constraints, user requirements, relevant motion/service states, primary STEP topology and actual-solid validation, mandatory snapshots, written STEP/3MF parity, mesh/manifold/orientation, DfAM, and available slicer checks.

## Implementation evidence

### Focused physical-defect regression — failing baseline witness

Command run from repository root before changing the authoritative P13 source:

```bash
uv run --project projects/xt60-bend-jig pytest -q \
  projects/xt60-bend-jig/tests/test_p13_four_plate_three_rod.py::test_printed_D_shaft_cam_bore_fit_regression_p13_r2
```

Result: `1 failed` in `2.5 s`. The baseline `cam_d_bore_od=5.70 mm` and
`shaft_od=5.60 mm` provide only `0.10000000000000053 mm` circular diametral
allowance, below the selected repair contract of at least `0.15 mm`. This is
the required pre-repair witness for the printed D-shaft to shared cam-D-bore
fit defect. The authoritative source had not yet been edited when this command
ran.

## Implementation closeout receipt — `P13R2-I02`

- Owner/role: `/root/implementation_closeout`, implementation closeout only;
  this is not independent validation or approval.
- Input candidate fingerprint: `c41289e18bebe676ca3f11dddc369b6b26a5d112bc359a39714f414f0415ce2b`.
  The frozen source/tests/artifact inputs remained byte-identical during this
  closeout. Only the release manifest and these explicitly labeled
  implementation-evidence sections changed.
- Authoritative source SHA-256:
  `7927bc9bb0d0516faa5410200fc870df408fe16b282c2a226828e712ec801067`.
- Controlling amendment SHA-256:
  `dcf770f5da16d5f71b4d99b69b1fe568adbabce64c37e66ece5250f6cd8f6bda`.
- Production 3MF SHA-256:
  `588f11e47c89a64221e527085e560453d4e7e75a7b6ecc00cf448f7d22bf75a7`.
- `p13-artifact-provenance.json` indexed 23 source artifacts and all 23
  written STEP hashes matched. The separately generated motion STEP matched
  `1501c8b2e75d17a48367fe78871592be3c9999ba056aa706043f6fb069632160`.
  Both written 3MF hashes matched `p13-3mf-provenance.json`.
- The parameter-manifest identifier
  `a4cff853c6b48ed55e50e8316835e83072f13e83d965c14653060aea004fad46`
  is the canonical compact-JSON hash returned by
  `parameter_manifest_sha256()`. The pretty-printed evidence file has a
  different byte hash by design.

Focused repaired-candidate command rerun during closeout:

```bash
uv run --project projects/xt60-bend-jig pytest -q \
  projects/xt60-bend-jig/tests/test_p13_four_plate_three_rod.py::test_printed_D_shaft_cam_bore_fit_regression_p13_r2
```

Result: `1 passed` in the closeout run. Together with the recorded failing
baseline witness above, this establishes the digital failing-before / passing-
after regression only. It does not prove printed fit.

The release manifest now records reproducible source-evidence, all-wrapper
STEP, 3MF, and snapshot commands plus current hashes for all 24 STEP outputs,
both P13 3MFs, both provenance files, and the two implementation snapshots.
The exact prior snapshot invocation/stdout did not survive the interrupted
implementation turn; it is not reconstructed as an observed command. The
independent validator must rerun and record its own exact snapshot commands.

The prior broader P13/motion suite was interrupted before a durable result was
recorded. It remains pending independent validation; no pass is claimed here.

### Required independent audit item

The implementation changed `tests/p13_geometry_case.py` canonical volume
rounding from 7 to 6 decimal places, with the stated rationale that a STEP
round trip can move the final `1e-7 mm^3` digit. The critic, validator, and
formal reviewer must explicitly decide whether that tolerance remains strict
enough to catch a meaningful source/export mismatch. This closeout does not
approve that test change.

## Acceptance boundary

- CAD/source: pending.
- Written artifact/slicer: pending.
- Physical: failed on the latest print; repaired physical fit and complete assembly/use validation remain pending.

## Independent validator receipt — `P13R2-V01`

- Owner/role: `/root/independent_validator`; independent validation/test only,
  distinct from design, implementation, critic, and formal review.
- Candidate fingerprint verified on entry and again before this receipt:
  `616b951822ed302ef71de8a3ee0752406dd1f84efb1edc99617af403bf8bc6a9`.
  The manifest was reproduced with the exact sorted SHA-256 rule in
  `BRIEF.md`; candidate source, tests, release/provenance, STEP, 3MF, and
  indexed snapshot inputs remained byte-identical throughout validation.
- Candidate scope was read-only. Validator outputs were limited to this
  section, `/tmp` snapshot/slicer evidence, and live Viewer process state.
- Gate status: **blocked on one deterministic test-contract defect** described
  below. No CAD, artifact, slicer, or physical acceptance is issued by this
  receipt.

### Concrete defect regression and fit/service facts

Current repaired-source command:

```bash
uv run --project projects/xt60-bend-jig pytest -q \
  projects/xt60-bend-jig/tests/test_p13_four_plate_three_rod.py::test_printed_D_shaft_cam_bore_fit_regression_p13_r2
```

Result: `1 passed`. A separate read-only calculation using the exact regression
formula and baseline values recovered with
`git show b0b79253373c7cf80943e99df8ab799958c50d49:projects/xt60-bend-jig/src/xt60_bend_jig/p13_four_plate_three_rod.py`
quantified the durable failing-before witness:

| Candidate | Circular diametral allowance (mm) | Flat-profile diametral allowance (mm) | `>=0.15 mm` | One-sided lash | Hub wall | Engagement |
|---|---:|---:|---|---:|---:|---:|
| P13 R1 baseline `5.70 / 5.25` | `0.10000000000000053` | `0.09999999999999876` | fail | `1.9325113632825863 deg` | `2.150 mm` | `4.50 mm` |
| P13 R2 repaired `5.75 / 5.30` | `0.15000000000000036` | `0.14999999999999858` | pass | `2.9405049697591217 deg` | `2.125 mm` | `4.50 mm` |

The same source calculation of `shaft_service_extraction_certificate()` found
the intentionally forbidden direct `+X` path through the installed fixed
guides inadmissible, with `7.300469154631463` and
`7.300469154631419 mm^3` actual intersection volumes. The staged path after
fixed-guide radial release had `0.0 mm^3` maximum intersection. This agrees
with the focused test's actual-male/female-solid and complete extraction-
envelope checks and does not confuse the cam D bores with the installed
`ID4.80` fixed journals.

### Relevant automated suites and blocking finding

Command:

```bash
uv run --project projects/xt60-bend-jig pytest -q \
  projects/xt60-bend-jig/tests/test_p13_four_plate_three_rod.py \
  projects/xt60-bend-jig/tests/test_p13_motion.py \
  projects/xt60-bend-jig/tests/test_p13_rod_fit_coupon_3p8.py
```

Result: 60 tests collected; exactly one failed and the other 59 completed
without failure. This run covered object collisions, derived math, constraints,
`REQ-001` through `REQ-008`, `CON-001` through `CON-007`, continuous motion and
removal, staged service, source dependency, all declared STEP parity,
metamorphic export, 3MF packaging/bed contact, and physical-acceptance boundary
checks.

Blocking failure, independently reproduced in isolation:

```bash
uv run --project projects/xt60-bend-jig pytest -q -vv \
  projects/xt60-bend-jig/tests/test_p13_four_plate_three_rod.py::test_domain_a_global_command_is_closed_form_outward_and_not_the_nominal_seed
```

Result: fail at line 812. The numeric command correctly equals `20.88 mm`, but
the test derives `global_command_20p88mm` with `str(command)` while the source's
stable `_tag()` formatting emits
`P13_REMOVE_global_command_20p880mm_full_workpiece_caps_off_rods_left`. This is
a test expectation formatting defect, not a geometric mismatch. It must be
repaired in the test by the implementation role, followed by candidate
refreeze and rerun; the validator did not modify it.

Repository-policy command:

```bash
uv run pytest -q tests/test_repository_structure.py
```

Result: `8 passed`.

### Written STEP inspection, solids, parity, and rounding audit

For each of `p13_print_kit`, `p13_left_cam`, `p13_right_actuator`,
`p13_motion`, and `p13_service_disassembly`, the validator ran:

```bash
CAD_SKILL=/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.21/skills/cad
uv run --project projects/xt60-bend-jig python "$CAD_SKILL/scripts/inspect" \
  refs "projects/xt60-bend-jig/cad/p13_four_plate_three_rod/<name>.step" \
  --facts --planes --positioning
uv run --project projects/xt60-bend-jig python "$CAD_SKILL/scripts/inspect" \
  validate "projects/xt60-bend-jig/cad/p13_four_plate_three_rod/<name>.step"
```

All five written STEP artifacts returned `ok:true` and zero validation
failures. Relevant actual counts were print kit `14`, left cam `1`, right
actuator `1`, motion `16`, and service-disassembly `6` validated occurrences.
Observed STEP hashes matched the release manifest: print kit
`5237fe9bc908781ae5793c9ab004f4fc51d24720244b26846bb1dacba63256b7`,
left cam `1971b2fce46dec45eda93a069a558f6d749d4265a02b79a6a068c4f2a1eef616`,
right actuator `81e04eaa89732e49b9265b84f8ce14ef222519467306dc83abec85b97b77d619`,
motion `1501c8b2e75d17a48367fe78871592be3c9999ba056aa706043f6fb069632160`,
and service-disassembly
`d0edc304e751d0b4c7010b8804b1f5eeed78c51e5f3e8a2074a59aa1863d0862`.

The full relevant suite's all-wrapper/no-skip parity test passed. The validator
also directly audited the `p13_geometry_case.py` change from seven to six
decimal places by comparing source BREP leaves with written STEP leaves:

| Artifact | Maximum absolute leaf-volume delta | 7-decimal mismatches | 6-decimal mismatches |
|---|---:|---:|---:|
| left cam | `5.9526428231e-10 mm^3` | 1 | 0 |
| right actuator | `5.63886715099e-10 mm^3` | 1 | 0 |
| print kit | `5.97992766416e-10 mm^3` | 2 | 0 |

The prior seven-decimal comparison failed only because nearly identical values
straddled a decimal rounding boundary; the actual deltas are below
`6e-10 mm^3`. Six-decimal comparison still retains labels, solid counts,
`2e-6 mm` bounds parity, and an effective volume-resolution scale of
`1e-6 mm^3`, so this relaxation is quantitatively adequate for meaningful
source/export mismatch detection.

### Snapshot evidence and visual review

The two committed implementation snapshots were inspected at original
resolution:

- `docs/review/p13-r2-center-hole-fit-repair/p13-print-kit_20260822T192147Z.png`
- `docs/review/p13-r2-center-hole-fit-repair/p13-motion-locked_20260822T192157Z.png`

Fresh deterministic scratch snapshots were then generated with:

```bash
CAD_SKILL=/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.21/skills/cad
uv run --with playwright --project projects/xt60-bend-jig python \
  "$CAD_SKILL/scripts/snapshot" \
  --input projects/xt60-bend-jig/cad/p13_four_plate_three_rod/p13_print_kit.step \
  --output /tmp/p13-r2-validator-snapshots.UYvx4j/print-kit.png \
  --camera iso --size-profile assembly --view-labels --json
uv run --with playwright --project projects/xt60-bend-jig python \
  "$CAD_SKILL/scripts/snapshot" \
  --input projects/xt60-bend-jig/cad/p13_four_plate_three_rod/p13_motion.step.py \
  --output /tmp/p13-r2-validator-snapshots.UYvx4j/motion-locked.png \
  --camera iso --size-profile assembly --view-labels \
  --params '{"motion":1.0}' --json
```

Results: print kit `14` meshes at `1800x1200`, motion `16` meshes at
`1800x1200`, no warnings. The fresh views matched the committed views and
showed the four plates, separate shallow-D shaft, keeper, caps, calibration
geometry, and locked assembly without a missing, floating, or obviously
misplaced component. This visual check is diagnostic; the solid and parity
checks above remain authoritative.

### Exact production-3MF DfAM and orientation screen

Commands against the exact production artifact SHA-256
`588f11e47c89a64221e527085e560453d4e7e75a7b6ecc00cf448f7d22bf75a7`:

```bash
uv run --with trimesh --with rtree --with networkx --with lxml python \
  /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.21/skills/dfam-check/scripts/dfam_tool.py \
  measure projects/xt60-bend-jig/cad/p13_four_plate_three_rod/p13_print_kit.3mf \
  --angle-limit 45
uv run --with trimesh --with rtree --with networkx --with lxml python \
  /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.21/skills/dfam-check/scripts/dfam_tool.py \
  orientations projects/xt60-bend-jig/cad/p13_four_plate_three_rod/p13_print_kit.3mf \
  --angle-limit 45
```

Measured facts: `136.27 x 105.05 x 7.15 mm`, `12` bodies, `56,946`
triangles, watertight, units consistent with millimetres, `48.13 mm^2` / `0.4%`
down-facing area below the generic FDM 45-degree limit, and coarse support
estimate `16.0 mm^3` / `0.1%` of part volume. The current source-defined
`+Z` orientation is decisively the best axis-aligned candidate; every flip or
90-degree rotation increases support area to `860.77..4871.54 mm^2` and build
height to as much as `136.27 mm`.

Against the DfAM skill's conservative generic FDM supported-wall minimum of
`1.2 mm`, six unchanged cap bodies have `p05=0.8 mm` and the unchanged keeper
has `p05=1.0 mm`, so those are explicit default-rule failures. The shaft and
both repaired cam bodies pass by `p05` (`4.21`, `2.5`, and `2.5 mm`); the
repaired cam D-bore radial wall itself measures/designs at `2.125 mm`. Fixed
guides have `p05=2.8 mm`; isolated smaller minima are sampling outliers under
the skill rule. The cap/keeper findings pre-exist this local hole repair and
the exact file slices, but they remain manufacturing/physical risks rather
than being silently waived. Hole diameter, positive feature, and bridge limits
are not measured by the DfAM tool and remain unchecked there.

### OrcaSlicer check on exact production 3MF

Available slicer: `/Applications/OrcaSlicer.app/Contents/MacOS/OrcaSlicer`,
version `2.4.2`. The installed system profiles supplied Snapmaker U1
`0.4 mm`, U1 `0.20 mm`, and Snapmaker PETG data. Direct leaf-profile loading
does not resolve profile inheritance in Orca CLI and initially produced PLA
defaults; that scratch output was rejected. A scratch-only resolved process
and PETG overlay was therefore used for the accepted check:

```bash
/Applications/OrcaSlicer.app/Contents/MacOS/OrcaSlicer \
  --debug 2 --logfile /tmp/p13-r2-orca-petg-textured-final.log \
  --slice 0 --arrange 1 --orient 0 \
  --load-settings "$HOME/Library/Application Support/OrcaSlicer/system/Snapmaker/machine/Snapmaker U1 (0.4 nozzle).json;/tmp/p13-r2-snapmaker-process-resolved.json" \
  --load-filaments /tmp/p13-r2-snapmaker-petg-resolved.json \
  --outputdir /tmp/p13-r2-orca-petg.01a0ET \
  projects/xt60-bend-jig/cad/p13_four_plate_three_rod/p13_print_kit.3mf
```

Result: exit `0`; scratch G-code
`/tmp/p13-r2-orca-petg.01a0ET/plate_1.gcode`, SHA-256
`f008ae67936c16e69463cb07b822c87d68c2a02a91d1659483f78d8e8852176c`.
The G-code reports Snapmaker U1 / `0.4 mm`, PETG density `1.25`, nozzle
`250/245 C`, Textured PEI Plate `70 C`, first/later layers `0.25/0.20 mm`,
`35` layers, max Z `7.05 mm`, `12.25 g`, `enable_support=0`, and zero support
feature markers. `--orient 0` preserves every source-authored bed face;
`--arrange 1` supplies only the necessary on-bed XY arrangement because the
portable 3MF uses a centered coordinate frame with negative XY values. A
deliberate `--arrange 0` precheck failed closed as “partly inside” the U1 bed,
confirming that translation/arrangement is necessary but no slicer-side flip or
`Lay on face` repair was used.

### Tailscale CAD Viewer verification

Viewer startup command, using the root workspace Python backend and bundled
root npm runtime because `npm` was not otherwise on `PATH`:

```bash
VIEWER_CAD_PYTHON="$PWD/.venv/bin/python" \
PATH=/Applications/ChatGPT.app/Contents/Resources/cua_node/bin:$PATH \
npm --prefix /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.21/skills/cad-viewer/scripts/viewer \
  run start -- --host 0.0.0.0 --json
```

The Viewer remains listening on `*:3245` (launcher PID `240`, backend PID
`255` at validation time). The exact Tailscale URL returned HTTP `200` with the
Viewer SPA:

<http://100.70.144.56:3245/Users/scottchu/.codex/worktrees/79caa408-e84c-4bfe-adfd-fa9ba1a1e186/design-projects/projects/xt60-bend-jig?file=cad%2Fp13_four_plate_three_rod%2Fp13_print_kit.step.py>

The Viewer artifact-status endpoint returned `state: ready`; the selected
generator's concrete `assembly.json` render payload returned HTTP `200`, schema
version `2`, `10` unique components, and `14` occurrences. This confirms the
repaired source artifact resolves through the Tailscale-bound Viewer, not only
through localhost.

### Independent acceptance boundary and next action

- CAD/source: the focused repaired-fit, actual-solid, motion/service, STEP
  validity, and source/export checks pass, but the validation gate is blocked
  until the `20.88` versus `20.880` label-format test defect is repaired and the
  dependent gates are rerun against a new frozen fingerprint.
- Written artifact/slicer: exact hashes/provenance, mesh/manifold, source
  orientation, Viewer resolution, and the scratch Snapmaker U1/PETG/supports-
  off slice pass. Generic DfAM still flags the unchanged `0.8 mm` cap walls and
  `1.0 mm` keeper against its conservative `1.2 mm` FDM default; this is a
  documented risk, not evidence of the repaired D-bore failing.
- Physical: the latest printed P13 remains failed at the center-hole fit. The
  repaired D-shaft insertion, play, torque transfer, assembly motion, cycling,
  heat behavior, wear, and complete use sequence remain pending a repaired
  print and user observation.

## Affected-gate revalidation — `P13R2-V01-R1`

- Owner/role: `/root/independent_validator`, continuing only the affected
  validation gate after the implementation role repaired the test-label
  expectation. This is not implementation or formal review.
- New candidate fingerprint verified on entry and exit with the same exact
  sorted manifest command:
  `9f123ad24f46d60fcb89ae305455ba1a0c3b38d4738f82766ec91d02c1350db9`.
- The only candidate input changed from the prior validator fingerprint was
  `tests/test_p13_four_plate_three_rod.py`, now SHA-256
  `f0f63a8c35b1cb8100703e5bc0c49fd26eca00b045397154c7fd826dab20654f`.
  The repaired assertion formats the numeric command to the source's fixed
  three-decimal tag and compares the complete exact label. Authoritative CAD
  source remained
  `7927bc9bb0d0516faa5410200fc870df408fe16b282c2a226828e712ec801067`;
  the release manifest remained
  `406325612e34c5c6fce95d96a2fe074591fdf502f592f172c47d016df5a54356`;
  primary STEP remained
  `5237fe9bc908781ae5793c9ab004f4fc51d24720244b26846bb1dacba63256b7`;
  and production 3MF remained
  `588f11e47c89a64221e527085e560453d4e7e75a7b6ecc00cf448f7d22bf75a7`.
  Both provenance files and the other relevant test modules also retained the
  hashes recorded above. Therefore the prior CAD inspection, actual-solid,
  parity, snapshot, mesh, DfAM, slicer, and orientation evidence remains
  applicable to this candidate.

Formerly failing isolated gate:

```bash
uv run --project projects/xt60-bend-jig pytest -q -vv \
  projects/xt60-bend-jig/tests/test_p13_four_plate_three_rod.py::test_domain_a_global_command_is_closed_form_outward_and_not_the_nominal_seed
```

Result: `1 passed in 10.17 s`. The exact source label
`P13_REMOVE_global_command_20p880mm_full_workpiece_caps_off_rods_left` is now
checked without weakening the numeric `20.88 mm` assertion.

Focused physical-defect regression:

```bash
uv run --project projects/xt60-bend-jig pytest -q \
  projects/xt60-bend-jig/tests/test_p13_four_plate_three_rod.py::test_printed_D_shaft_cam_bore_fit_regression_p13_r2
```

Result: `1 passed`.

Complete relevant suite:

```bash
uv run --project projects/xt60-bend-jig pytest -q \
  projects/xt60-bend-jig/tests/test_p13_four_plate_three_rod.py \
  projects/xt60-bend-jig/tests/test_p13_motion.py \
  projects/xt60-bend-jig/tests/test_p13_rod_fit_coupon_3p8.py
```

Result: `60 passed`; no failures. This disposes the sole blocking finding from
`P13R2-V01` and reconfirms the focused fit, object-collision, math, constraint,
requirements, motion/service, source/export parity, 3MF, and acceptance-
boundary coverage against the new fingerprint.

The Viewer remained live on `*:3245`. Both the exact Tailscale page and the
concrete generator `assembly.json` descriptor returned HTTP `200`; the latter
still reports schema version `2`, `10` unique components, and `14`
occurrences:

<http://100.70.144.56:3245/Users/scottchu/.codex/worktrees/79caa408-e84c-4bfe-adfd-fa9ba1a1e186/design-projects/projects/xt60-bend-jig?file=cad%2Fp13_four_plate_three_rod%2Fp13_print_kit.step.py>

Revalidation disposition:

- CAD/source: deterministic validation gates pass for this candidate.
- Written artifact/slicer: prior evidence remains valid because its complete
  input set is byte-identical. The unchanged conservative DfAM cap/keeper wall
  findings remain documented risks, not new failures from the D-bore repair.
- Physical: still failed/pending. Advancement beyond repository CAD/artifact
  validation requires a repaired print and user-observed assembly/use results.

## Implementation repair receipt — `P13R2-I03`

- Owner/role: `/root/implementation_repair`, bounded implementation repair;
  distinct from the validator, critic, and formal reviewer.
- Input candidate: the 53-entry fingerprint frozen in `BRIEF.md` and verified
  by the independent validator,
  `616b951822ed302ef71de8a3ee0752406dd1f84efb1edc99617af403bf8bc6a9`.
  The pre-repair test-file SHA-256 was
  `bf51c82b0ab70c1aa4c5eeecf9dc74a19ed7795dc1416aa08fca4acaefa16799`.
- Scope: changed only
  `tests/test_p13_four_plate_three_rod.py`, then appended this implementation
  receipt and the matching `HANDOFF.md` receipt. Source, STEP, 3MF,
  provenance, release, snapshots, geometry-case tolerance, design/review,
  continuity state, Viewer, and acceptance records were not changed.
- Repair: replaced the float-string-derived partial label assertion with an
  explicit fixed-three-decimal command tag (`f"{command:.3f}"`) and an exact
  full-label equality assertion. This preserves the authoritative
  `global_command_20p880mm` naming contract and strengthens the test from a
  substring check to exact identity; it does not relax a geometry or numeric
  requirement.
- Post-repair test-file SHA-256:
  `f0f63a8c35b1cb8100703e5bc0c49fd26eca00b045397154c7fd826dab20654f`.
- The independently frozen candidate has therefore changed and requires a new
  orchestrator-computed fingerprint plus dependent validation/review reruns.

Exact failing-before command:

```bash
uv run --project projects/xt60-bend-jig pytest -q \
  projects/xt60-bend-jig/tests/test_p13_four_plate_three_rod.py::test_domain_a_global_command_is_closed_form_outward_and_not_the_nominal_seed
```

Pre-repair result: `1 failed`; expected substring
`global_command_20p88mm` was absent from the authoritative full label
`P13_REMOVE_global_command_20p880mm_full_workpiece_caps_off_rods_left`.

Post-repair commands:

```bash
uv run --project projects/xt60-bend-jig pytest -q \
  projects/xt60-bend-jig/tests/test_p13_four_plate_three_rod.py::test_domain_a_global_command_is_closed_form_outward_and_not_the_nominal_seed
uv run --project projects/xt60-bend-jig pytest -q \
  projects/xt60-bend-jig/tests/test_p13_four_plate_three_rod.py::test_printed_D_shaft_cam_bore_fit_regression_p13_r2
```

Post-repair results: `1 passed` and `1 passed`, respectively. These are
implementation checks, not self-approval.

As a byte-identity guard, the 52 non-target entries from the declared
candidate manifest were hashed before and after the edit using the same sorted
path/content set while excluding only the changed test. Both aggregates were
`e039f940a408d87f38b26417405436dd69419d389109fea2a40268c389020108`.
No other candidate input changed during this repair.

Acceptance remains separate: CAD/source and written artifact/slicer approval
await independent reruns against the new fingerprint; physical acceptance
remains failed/pending a repaired print.
