# CRI-GEN-01 default-candidate critique

Owner `/root/generator_critique`, 2026-09-02. Scope: independent critique of the frozen default delivery only. Read-only on source/artifacts/config; writes limited to this receipt and `scratch/generator-critique/`.

Verified candidate manifest: `projects/laifen-wave-case/docs/iterations/2026-09-01-p1-r3-algorithmic-skin/inputs/geometry-default-candidate.sha256` checked `53/53 OK`, fingerprint `4e1ea38ac083f2f9b708770165bb2281748f129826f1f50bd1782139484a9ffd`. Parameter fingerprint remains `50f1e34681419a81f91b4587b8f1e11a97569b3e99cc530891dfcee32b302677`. Source/artifact hashes and `generated/50f1e34681419a81/manifest.json` were not mutated during this critique.

## Findings

1. **Medium - current acceptance boundary is still the default short preset, not the full editable generator promise.** The frozen implementation receipt already records a mathematically feasible but geometrically rejected nondefault case: `thread_pitch=2.4`, `engagement=7.2`, `cavity_length=82.1`, `cap_height=47` produced an empty female void before the added guard, and the final source now rejects it rather than proving a valid alternate solid. That is the right defensive behavior, but it means the present candidate should still be described as a reviewable default short-coupon generator with guarded controls, not as a generically validated editable screw-cylinder generator across the advertised pitch/engagement space.

2. **Low - the installed snapshot path did not provide a documented longitudinal assembled section control in this bounded critique.** Successful snapshot commands produced a useful rendered print-layout view and a cap-only top view with readable recessed labels. The built-in `section` mode stayed at `XY @ Z=0` even when camera presets changed, and a bounded local search of the installed `cadgen` snapshot source found no documented `sectionAxis`/`sectionPlane` job key. Additional `display.clip` trials rendered ordinary side views rather than a cutaway. This is a tooling limitation in the critique packet, not evidence of a CAD defect, but it means this critique does not independently visualize cavity length, floor stack, or axial thread overlap.

## Visual observations

- The rendered print layout shows broad continuous diamond coverage on the body and all three caps. The candidate clearly preserves smooth functional zones at the thread mouths, shoulder/collar region, and lower floors; it does not regress to the earlier two-row grip treatment.
- The cap-only top snapshot shows the recessed `25`, `30`, and `20` floor marks as visually readable and correctly oriented in print pose after hiding the body and reframing on the caps. This supports the DES03 switch from raised to recessed labels.
- The successful views are strong on skin intent and label usability. They are not print, slicer, or physical evidence.

## Evidence run

Commands executed from repository root with root `uv` Python:

```sh
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-01-p1-r3-algorithmic-skin/inputs/geometry-default-candidate.sha256
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/snapshot --input projects/laifen-wave-case/cad/p1_r3_generator/print_layout.step --output projects/laifen-wave-case/scratch/generator-critique/print-layout-rendered.png --camera iso --display rendered --size-profile assembly --json
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/snapshot --input projects/laifen-wave-case/cad/p1_r3_generator/print_layout.step --output projects/laifen-wave-case/scratch/generator-critique/print-layout-top-caps.png --camera top --display solid --size-profile assembly --hide '#o1.1' --json
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/snapshot --input projects/laifen-wave-case/cad/p1_r3_generator/closed_c25.step --output projects/laifen-wave-case/scratch/generator-critique/closed-c25-section.png --mode section --camera front --display solid --size-profile diagnostic --json
uv run python - <<'PY'
from pathlib import Path
base = Path('.venv/lib/python3.12/site-packages/cadgen')
needles = ['sectionAxis', 'section_axis', 'sectionPlane', 'section_plane', 'clipPlane', 'clip_plane', 'cutLocator', 'cut_locator']
count = 0
for path in sorted(base.rglob('*')):
    if path.suffix not in {'.py', '.md', '.json', '.js', '.ts'}:
        continue
    text = path.read_text(errors='ignore')
    for needle in needles:
        if needle in text:
            count += 1
print('matches', count)
PY
```

Successful retained snapshot files and hashes:

- `projects/laifen-wave-case/scratch/generator-critique/print-layout-rendered_20260902T042508Z.png`
  - SHA-256 `b96237e8f3e15a35108247bdb83e9a6f439c26b7c69f18a7999df36fbc15573f`
  - Observation: broad continuous skin is plainly visible on body plus all three caps.
- `projects/laifen-wave-case/scratch/generator-critique/print-layout-top-caps_20260902T042613Z.png`
  - SHA-256 `9c9b91fb12ca0974e410788bab908e8081b791e38cf4eb4603ab036291ebf275`
  - Observation: recessed `25/30/20` labels read correctly in print pose.

Superseded limitation evidence, not part of the final review packet:

- `projects/laifen-wave-case/scratch/generator-critique/closed-c25-section_20260902T042508Z.png`
  - SHA-256 `5846f5386cc00913bdaef56013b95d201984f3247ec0aacc1e047bf0711e7f48`
  - Observation: `section` mode rendered `XY @ Z=0`, so it did not expose axial stack relationships.
- `projects/laifen-wave-case/scratch/generator-critique/closed-c25-clip-axis-x_20260902T042930Z.png`
  - SHA-256 `7d7b9a41cfd2808d5afce057f93b810ac805d4496a98fb35799938d95c3bcb5f`
  - Observation: bounded `display.clip` retry produced an unclipped side view, not a longitudinal cut.

## Requirement coverage from this critique

- `REQ-SKIN-01`, `REQ-SKIN-02`, `REQ-SKIN-03`: visually supported at the default preset for broad continuous coverage, smooth exclusions, and recessed label treatment.
- `REQ-GEN-02`, `REQ-GEN-03`: still not independently proven across editable nondefault parameter space; current evidence remains default-centered plus rejection guards.
- `REQ-10`, slicer-facing orientation, and all physical acceptance criteria remain outside this critique and still pending.

## Risks and next step

No print acceptance is justified from this critique. The default preset looks consistent with the intended broad diamond grip experiment, but the generator should still be presented as a frozen default CAD candidate pending formal review, slicer checks, and physical testing. The next smallest action is to let root combine this receipt with the independent validator result and keep any further axial-section tooling follow-up separate from default-candidate acceptance.
