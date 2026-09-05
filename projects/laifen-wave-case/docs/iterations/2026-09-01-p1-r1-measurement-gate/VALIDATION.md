# Validation evidence
DES-01 read root AGENTS.md, CAD_WORKFLOW.md, PROJECT_CONTINUITY.md, FDM_DESIGN_RULES.md, CAD skill/brief reference and visualization skill; shell reads succeeded.
`git rev-parse HEAD` -> d0aab1ff21a0cd2e5790c9800fcec7cfec2bfc3c; `git branch --show-current` -> codex/laifen-wave-measurement-gate. Initial `find projects/laifen-wave-case -maxdepth 2 -type f` reported absent project before creation.
Earlier tool-host negotiation failed before execution; no artifacts/measurements resulted. Current docs writing/hash checks are authoring evidence only; independent validation pending.
Contract manifest uses shasum -a256 and LC_ALL=C sort; section snapshots extracted between exact FROZEN-CONTRACT markers. Exact fingerprint in inputs/fingerprint.txt.
No preview runtime, CAD, STEP/mesh, slicing or physical check ran during DES-01.

## Initial preview candidate — rejected
Validator `/root/case_preview_validate` (Sol/high), distinct from implementer and critic; read-only candidate fingerprint `da5a17a87a22675a1b0d04843ec592582085cf0f65cace118c0ced35c4f7adc0`. All 11 manifest entries verified. Disposable evidence only under `scratch/validation/` (not release artifacts).
- `node --test projects/laifen-wave-case/tests/test_measurement_gate.mjs`: 2 passed. These checks missed the displayed-geometry and invalid-input defects below.
- `uv run pytest tests/test_repository_structure.py -q`: 12 passed, 1 failed on pre-existing XT60 `PROJECT_STATE.md` missing the `## Baseline` heading. This project does not change that file.
- `uv run python /Users/scottchu/.codex/plugins/cache/openai-bundled/visualize/1.0.23/skills/visualize/scripts/render.py` and isolated Chrome headless `--dump-dom` exercised actual default, bottom/top, blank, overflow and below-target states; local harness/results in `scratch/validation/dom-harness.html` and `dom.html`.
- Independent diagram failures matched CRI-01: wrong inner-floor datums, unrelated radial geometry, missing gap/engagement labels and target warnings.
- Additional P1: blank radial input became zero through `Number('')`; finite L/slack values `1e308` overflowed derived dimensions without rejecting invalid geometry. P2: 0.25 mm thread clearance displayed as 0.3 mm.
- Initial mobile screenshot was inspected, but Chrome minimum viewport behavior prevented attributing clipping to the product. Repaired candidate needs a true 360 px content-width harness plus 736 px and both themes.
Initial verdict FAIL. These failures must remain recorded after repair; they do not create a new product-design version. No CAD/STEP/slicer/physical check occurred.

## Root provenance and environment checks
`uv sync --all-packages --all-groups` restored root CPython 3.12.13 environment; after scaffold, repeated sync and `uv lock --check` passed. Root `uv.lock` changes only register the new dependency-free workspace member.
Root repeated candidate checksums and confirmed marked BRIEF/DESIGN frozen sections equal their snapshots. Mutable orchestration/evidence changes do not change the candidate inputs.

## Repair cycle 1 — independent checks in progress
Implementer `/root/case_preview_impl` reported corrected preview, focused regression tests and README render command. Revised fingerprint `8611dd9ec2b5e511dc51cfb5d78b1ad00645c24add139bfff327dac564ebbd9f`; root rechecked all 11 hashes and manifest fingerprint. Initial manifest retained for provenance.
Implementer command: `node --test projects/laifen-wave-case/tests/test_measurement_gate.mjs` -> 3 passed; `git diff --check` clean. These are implementation receipts, not independent acceptance; CRI-01 and VAL-01 reruns are pending.

VAL-01 independently confirmed those 3 tests and repaired blank/overflow rejection, 0.25 precision, inner-floor/gap placement, radial updates and target warnings. Real Chrome evidence identified two remaining issues on the same fingerprint: P1 texture pitch `1e-20` throws `RangeError: Invalid array length` during unbounded repeat allocation, leaving stale texture content; P2 the external-shoulder label exceeds a 334 px SVG in a true 360 px layout (measured right edge 346.14 px). Final repair must bound visual representation complexity without silently changing pitch and place the label within the available width.

## Reduced candidate after retry escalation
IMP-01 exhausted its ceiling; see REVIEW.md for the malformed SVG and explicit DES-02 scope reduction. IMP-02 owner `/root/case_preview_recovery` rebuilt one essential axial/diameter section from reduced contract fingerprint `8f3a859f5cf183d2abb489ac9d1112d8b50bbeb4965707088ac4e9ee9430da72`.
New candidate fingerprint: `85c04f7de4dce3e6ff4ab092c5f483c8d7449b6f1a3335d6e8197d17e6a1fc73`; 13 entries in `inputs/candidate.sha256` (also `candidate-reduced.sha256`) include root pyproject.toml and uv.lock. Root verified all 13 entries and reduced contract/source-section parity.
Implementer reported `node --test projects/laifen-wave-case/tests/test_measurement_gate.mjs` -> 4 passed: actual scaled SVG floors/dimensions, changed L/D, axial positions and zero slack, finite coordinates, external stop and invalid-state clearing. The previous malformed source is not the current candidate. Independent CRI-02/VAL-02 checks are in progress; no approval inferred from these implementation receipts.

## VAL-02 independent reduced-preview result
Validator `/root/case_preview_validate` (Sol/high), distinct from both implementers and critic. Read-only candidate fingerprint `85c04f7de4dce3e6ff4ab092c5f483c8d7449b6f1a3335d6e8197d17e6a1fc73`; 13/13 entries verified before and after checks. Verdict: PASS for the reduced HTML preview; no blocking findings.
- `node --test projects/laifen-wave-case/tests/test_measurement_gate.mjs`: 4/4 passed independently.
- `shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-01-p1-r1-measurement-gate/inputs/candidate.sha256`: 13/13 passed.
- Official visualization wrapper was generated through `uv run python` with the installed skill's `scripts/render.py`; isolated Chrome used `--headless --virtual-time-budget=1000 --dump-dom` and `--screenshot` against disposable scratch documents.
- Real SVG measurements reproduced default L=208/D=29/ID=32 and changed L=220/D=31/ID=35 with one dimensional scale. Positions q=0/0.5/1 preserved device size and gave bottom/top gaps 0/5, 2.5/2.5 and 5/0. Floor material remained outside usable inner datums.
- Zero slack labeled both-end contact. Blank/overflow inputs cleared geometry and stale results. Below-target values warned. Exercised SVG values were finite and 360 px text bounds fit. Stop path stayed 4 px outside the outer contour, with external labels/leader.
- Four true-content-width screenshots were inspected: `scratch/validation/reduced-360-light.png`, `reduced-360-dark.png`, `reduced-736-light.png`, `reduced-736-dark.png`. Labels, gaps, gravity, fixed references and pending statements were readable in those exercised views.
- Seven native controls were enabled with tabIndex=0; range focus was verified. Physical keyboard navigation was not automated.
- Evidence: `scratch/validation/reduced-dom-evidence.json`, SHA-256 `d72a982e013a9552558003f59448000a4e033488929ee7d3d3e065a9c26254db`; harness/output in `reduced-dom.html`, `reduced-dom-output.html`, `reduced-rendered.html`. Scratch only; browser processes terminated.
This passes the preview-validation gate only. Formal review and user measurement/intent feedback remain pending. CAD, STEP/mesh, slicer and physical acceptance remain NONE; no CAD snapshot applies because no CAD artifact exists.

Final status: REV-01 subsequently passed the formal join on the same fingerprint; see REVIEW.md. User measurement/intent feedback is the remaining gate before full-case design can be frozen. No further source change followed the passing independent checks.
