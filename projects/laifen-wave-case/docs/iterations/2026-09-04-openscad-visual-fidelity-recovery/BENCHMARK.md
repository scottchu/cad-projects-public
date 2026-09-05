# VFR-02 read-only diamond benchmark

**Owner/role:** `/root/openscad_diamond_benchmark`, independent geometry investigator.  
**Status:** source/analytic benchmark complete; current-diamond browser/manifold execution remains unresolved.  
**Decision boundary:** this receipt does not approve an implementation, generated artifact, slicer result, or physical result.

## Frozen baseline and provenance

Repository root: `/Users/scottchu/.codex/worktrees/4f8c/design-projects`. Repository `HEAD` was `d0aab1ff21a0cd2e5790c9800fcec7cfec2bfc3c` on branch `codex/laifen-wave-measurement-gate`. The complete `projects/laifen-wave-case/` tree is untracked at this checkout, so that Git commit is not a source revision for this project. The authoritative editable OpenSCAD revision is therefore pinned by content:

- `openscad/laifen_case_customizer_v1.scad`: `b5db326716df1f5cbff7135440cacac3cf0e61a67d9b0229a6e99261fa859f0e`
- `preview/openscad-wasm-simulator/src/schema.mjs`: `fe77d55cc91f9e526559b307a70db3fa03aefe35a84c4c87cf5d4ee42f242f1a`
- VFR-02 read-set/candidate fingerprint: `8c205f72f28d846ecdf94a2d4bd1cb5663c87235c74758bab3e7b96ef4e36e3f`

The VFR-02 fingerprint is SHA-256 of the following UTF-8 manifest, including its final newline, sorted by path and formatted as `<sha256><two spaces><repo-relative-path>`:

```text
c227f85d5de9b28fc5e47794eeeee0741aa1e652bfd800f41020fac2d0dc69e6  projects/laifen-wave-case/cad/p1_r7_end_chamfer/params.py
a579690b9523ea56a0e2daf2ba2854bc330d445088617a56197f82dba90d6e1d  projects/laifen-wave-case/cad/p1_r7_end_chamfer/parts.py
c1d6ad0d853a28eb9a155eabdd3530438ef743626f28996296458e6a1fb671be  projects/laifen-wave-case/cad/p1_r7_end_chamfer/skin.py
0367b4aff210f4638e5f6f0c599ad3e640738de7d09325b551a80344d01aee19  projects/laifen-wave-case/docs/REQUIREMENTS.md
038876c9be60d74d6f659817dbc11e86b2d80802084bd675fe028a07513326bd  projects/laifen-wave-case/docs/iterations/2026-09-03-p1-r7-end-chamfer/REVIEW.md
57b56b93e4ad4abc4b78d7ae1d127ac3ebdd89dc0559e683e806e2fb8764e3eb  projects/laifen-wave-case/docs/iterations/2026-09-03-p1-r7-end-chamfer/VALIDATION.md
de4a28251d182038a987c85d543e3c69e5015a60c4c738128bf5e7e7176f2de7  projects/laifen-wave-case/docs/iterations/2026-09-03-p1-r7-end-chamfer/inputs/BRIEF.contract.md
327852bb47620b54cd67ee80f06414573bc3cca5e117353da028705a81c296db  projects/laifen-wave-case/docs/iterations/2026-09-03-p1-r7-end-chamfer/inputs/DESIGN.contract.md
8d3941772cca549846937dcad6ce4a05e06f5bba104c261668a0cf747c62b6a1  projects/laifen-wave-case/docs/iterations/2026-09-03-p1-r7-end-chamfer/inputs/implementation-candidate.sha256
2d853e2be1e1d3b49646d356d83d47b54bc8901e28cf336d685e3a8a2f51e5ce  projects/laifen-wave-case/docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/BRIEF.md
fcea1f7507083e6932607c1b5473dbccc9648facc8a7ca057def907d4ab57bb5  projects/laifen-wave-case/docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/DESIGN.md
10ab643af3ee973b9593104a76bd51092730f763faa4b275108068d214896b88  projects/laifen-wave-case/docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/HANDOFF.md
2915ea354251e2122215752d95920b94a30c3a583e367220e730d31c39df0ce9  projects/laifen-wave-case/docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/OBSERVATION.md
7e40fa713313aedd0ae6edba6fba8169b07da79631ced6e9cd0d3bf052657c43  projects/laifen-wave-case/openscad/generated_v1/compile-validation.json
9c5003458f8990bf3cc27f54945ab03de2fef063fe6f41baa0eb9541b68d042a  projects/laifen-wave-case/openscad/generated_v1/mesh-validation.json
e0ddf0b4239f4d9b14f02d5deba26705c43e02a0be2cd8f8415cd4aa9106e6fe  projects/laifen-wave-case/openscad/generated_v1_recovery/collision-validation.json
11591be9ffe34f29dbad353cbd2e9a1e4673b1c7c3a70d30019ec19fa62803ad  projects/laifen-wave-case/openscad/generated_v1_recovery/compile-validation.json
b5db326716df1f5cbff7135440cacac3cf0e61a67d9b0229a6e99261fa859f0e  projects/laifen-wave-case/openscad/laifen_case_customizer_v1.scad
fe77d55cc91f9e526559b307a70db3fa03aefe35a84c4c87cf5d4ee42f242f1a  projects/laifen-wave-case/preview/openscad-wasm-simulator/src/schema.mjs
```

## Current OpenSCAD diamond facts

At the default values, `outer_radius = 39 / 2 = 19.50 mm` and `valley_radius = 19.50 - 0.45 = 19.05 mm`. The source computes:

```text
groove_count = max(8, round(2 * PI * outer_radius / diamond_arc_pitch))
             = round(2*pi*19.50/3.63)
             = 34
```

This is an `N34` count derived at the crest/outer radius. The resulting crest-circle arc pitch is `3.603591573 mm`; carrying those same 34 starts at the 19.05 mm valley circle gives `3.520431768 mm` between starts.

The cutter has `groove_tangent_halfwidth = 0.576574652 mm`, hence a `1.153149303 mm` full inner-base width. The current OpenSCAD source has no `plateau_half_fraction` and no literal `0.18`. Its `.32` is a cutter-width multiplier and is not the R7 plateau parameter.

The default closed geometry is 219 mm long. `body_height=144`, `cap_height=84`, and the assembled seam/contact plane is global `z=135`. The texture intervals are:

| Component | Source interval | Global interval | Smooth interval at seam |
|---|---:|---:|---:|
| body | `z=3.2..133` | `z=3.2..133` | `133..135`, 2 mm |
| cap | local `z=11..80.8` | `z=146..215.8` | `135..146`, 11 mm |

The current source therefore creates a 13 mm combined untextured band around the seam. The `global_offset` term does preserve the mathematical helical phase across the missing band; it does not make the diamonds physically continuous across the seam.

Source-level component identity exists: `body_shell()` and `cap_shell()` are separate modules, `print_layout()` places them separately, and `closed_assembly()` assigns separate colors before placing the cap at `z=135`. Existing recovery collision evidence measures only the smooth pair and finds zero-volume contact at exactly `z=135`. STL does not preserve those source colors, and the touching assembled output does not by itself guarantee that a viewer will communicate two-piece identity.

The browser contract currently selects `BROWSER_PRESET.surface_style="smooth"`, rejects every non-smooth job, and removes all `diamond_*` parameters from `JOB_ALLOWLIST`. A plain live browser cylinder is therefore consistent with the currently delivered smooth-only schema; it is not evidence that the diamond source ran and failed visually.

## Preserved R7 relationship

R7 uses the same `Rcrest=19.50 mm`, `skin_height=0.45 mm`, and therefore `Rvalley=19.05 mm`, but derives count at the valley radius:

```text
N = floor(2*pi*Rvalley/skin_arc_pitch_target + 0.5)
  = floor(2*pi*19.05/3.63 + 0.5)
  = 33
```

Its actual valley-circle arc pitch is `3.627111518 mm`. `plateau_half_fraction=0.18` is a dimensionless half-fraction of the crest plateau in the R7 rational field, not 0.18 mm. With R7's 4.8 mm axial pitch, the derived developed plateau width is `1.041776914 mm`.

R7's `body_band=(-135,0)` and `cap_band=(0,84)` meet at their shared seam datum with the same phase. Apart from the narrow closed-end chamfers, the preserved reviewed R7 has textured body and cap up to the seam and explicitly reports no smooth seam collar. `parts.py` also preserves body and cap as distinct children of the closed compound and as two separately placed print objects.

The four currently present reviewed R7 STEP files still match the hashes in its formal review:

- `body.step`: `3c04d417e3f21c5ef0e3b1d12ff1953ac366ef418fc4792d592a0624ad91982b`
- `cap_c25.step`: `0dd09cbd99f4ceb78605ee7eef1a74a315c3f95079d97a4628dffffc70afe82a`
- `closed_c25.step`: `e72ee16eb4315a2eb93619ecfb3fd363ac89dc5253bb6527de9d71c82444d27c`
- `print_layout.step`: `80fd95845b51da5266883614f9bf8eff60793a24d5c39b7321c9c6cb16d477a4`

The full 201-entry R7 candidate manifest is no longer reproducible as a whole in this checkout: `shasum -a 256 -c .../implementation-candidate.sha256` produced `ok=163 failed=38`, with the failures caused by absent temporary remote attachments and removed `scratch/` evidence. This is a provenance limitation, not evidence that the four present STEP bytes or the inspected R7 source facts changed.

## Hypothesis disposition and findings

| Severity | Hypothesis or finding | Disposition | Evidence |
|---|---|---|---|
| High | Current `groove_count` uses crest radius and yields N34. | **Confirmed.** | SCAD lines 57 and 93; direct calculation above. |
| High | Preserved R7 uses valley radius and yields N33. | **Confirmed.** | R7 `params.py` lines 122-134; direct calculation above. The radius choice alone changes 34 to 33. |
| High | The current OpenSCAD surface retains R7's `0.18` plateau. | **Rejected.** | `0.18` exists as R7 `plateau_half_fraction`; OpenSCAD instead uses `.32` for groove cutter width. They are different parameters and geometries. |
| High | Current texture matches R7 at the seam. | **Rejected at source level.** | OpenSCAD leaves 2 mm body plus 11 mm cap smooth at the seam; R7 carries N33/shared-phase texture to both sides of the seam. |
| Medium | Current source retains body/cap identity. | **Confirmed in source; unresolved in diamond artifact presentation.** | Separate modules/colors/print objects exist, but assembled STL loses color and touches at `z=135`; no current diamond browser result was produced. |
| High | A current valid diamond manifold has been demonstrated. | **Unresolved.** | Recovery benchmark for source hash `b5db...` timed out at 60.0621 s for body and 60.0338 s for cap with no outputs. Older pre-recovery evidence belongs to source hash `7f5aa5...`: body took 429.09 s and was non-watertight with 25 components; cap took 228.73 s and was watertight/one component. Those stale results cannot validate the current source. |
| Medium | The broad collar values are 2 mm body and 11 mm cap. | **Confirmed.** | SCAD texture bounds; 13 mm total blank band around global seam `z=135`. |
| Medium | The VFR records are the checkout's canonical active iteration. | **Unresolved continuity pointer.** | `docs/iterations/CURRENT` points to `openscad-customizer-v1`, `CURRENT.md` points to `openscad-wasm-simulator`, while `PROJECT_STATE.md`/`NEXT_AGENT.md` point to the later smooth-only simulator/error-preview recovery. VFR is task-authoritative here but is not yet the repository pointer. |

No current diamond mesh/artifact hash can be recorded because the recovery benchmark wrote no diamond output and the earlier reported diamond STLs were withheld from the repository. Browser manifold timing beyond the recorded 60-second recovery timeouts was not rerun.

## Commands actually run

All commands ran from the repository root. Searches used the required Homebrew executable.

```sh
/opt/homebrew/bin/rg -n -i 'N33|N34|R7|diamond|groove_count|plateau|collar|crest|valley|seam|component|manifold' projects/laifen-wave-case --glob '*.md' --glob '*.scad' --glob '*.mjs' --glob '*.py' --glob '*.json' --glob '*.sha256'
/opt/homebrew/bin/rg -n -C 3 'N=33|N33|lattice_count|plateau_half_fraction|plateau|outer_crest_radius|outer_valley_radius|skin_height|arc_pitch|seam|collar|component|body_band|cap_band' projects/laifen-wave-case/docs/iterations/2026-09-03-p1-r7-end-chamfer/{BRIEF,DESIGN,IMPLEMENTATION,VALIDATION,CRITIQUE,REVIEW,HANDOFF}.md projects/laifen-wave-case/cad/p1_r7_end_chamfer/{params,skin,parts}.py projects/laifen-wave-case/docs/iterations/2026-09-03-p1-r7-end-chamfer/inputs/{BRIEF.contract,DESIGN.contract}.md
uv run python - <<'PY'
# Read the 19 paths printed in the frozen manifest, emit each SHA-256 and the
# SHA-256 of the sorted manifest, then evaluate the formulas recorded above.
PY
shasum -a 256 projects/laifen-wave-case/cad/p1_r7_end_chamfer/body.step projects/laifen-wave-case/cad/p1_r7_end_chamfer/cap_c25.step projects/laifen-wave-case/cad/p1_r7_end_chamfer/closed_c25.step projects/laifen-wave-case/cad/p1_r7_end_chamfer/print_layout.step
zsh -o pipefail -c 'shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p1-r7-end-chamfer/inputs/implementation-candidate.sha256 | awk '\''BEGIN{ok=0;fail=0} /: OK$/{ok++} /FAILED/{fail++; print} END{printf("ok=%d failed=%d\\n",ok,fail)}'\'''
```

## Smallest VFR-03 2D intent gate

Use one unwrapped, seam-centered strip with an A/B toggle:

- **Fixed:** two named components (`body` below, `cap` above), seam line, OD 39, depth 0.45, axial pitch 4.8, and shared global phase.
- **A — current OpenSCAD:** N34 from crest radius, a 2 mm body blank plus 11 mm cap blank at the seam, and the current cutter profile.
- **B — preserved R7:** N33 from valley radius, `plateau_half_fraction=0.18`, and diamonds meeting the seam on both components.
- **Adjustable:** only the A/B relationship toggle. A seam highlight may be switched on for inspection but must not alter geometry.
- **User action:** toggle A/B, inspect repeat density, diamond crest shape, two-piece identity, and the pattern immediately above and below the seam against the printed/reference case.
- **Explicit pass/fail:** “Should the OpenSCAD recovery use relationship B: two visibly separate pieces, N33 derived at the valley radius, the R7 0.18 crest plateau, and shared-phase diamonds continuing to both sides of the seam without the current 2 mm/11 mm smooth collar?”

Do not begin VFR-04 geometry or UI implementation until that exact relationship is explicitly passed or corrected by the user.
