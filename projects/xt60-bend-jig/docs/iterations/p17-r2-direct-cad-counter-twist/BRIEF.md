# P17 R2 direct-CAD counter-twist brief

Status: follow-up repair design contract complete for `P17-D05`; implementation,
critic, validation, formal review, and continuity remain pending against this
corrected center-axle/slot/lock contract.

## Baseline and scope

- Project: `projects/xt60-bend-jig`.
- Branch: `codex/xt60-p18-direct-cad` (branch name predates the P17 R2
  version-label correction).
- Baseline commit: `05e0152b045bd82a41ea07a715f2361606c1ec99`.
- Iteration: `p17-r2-direct-cad-counter-twist`.
- Supported predecessor: P13 R2 repaired-print candidate, digitally accepted
  but physically failed/pending.
- Rejected evidence layer: P17 R1 simulator branch at commit `f733f84`; use
  only for the exact rejection and observation provenance. Do not inherit its
  simulator geometry, `18.5 mm` span, `64/60/50 mm` diameters, opposed-bevel
  depiction, detent design, or any animation-sidecar logic.

P17 R2 is a direct STEP-first CAD revision of the P17 counter-twist design, not
a new product-design `P` version. The user explicitly rejected the P17 R1
simulator artifact because holes/slots appeared to move with animation and
directed the project to skip simulation. That rejection invalidates simulator
evidence only; it does not invalidate the P17 design version. Do not create
Three.js, JS sidecars, prescribed animation, or simulator tasks in this
iteration.

Version policy applied here:

- `P` increments only for a core product-design baseline, architecture, or
  interface change.
- `R` increments for same-design geometry, fit, manufacturing, documentation,
  or implementation refinement.
- Simulator, STEP, 3MF, slicer, and physical status are independent evidence
  layers and never alone bump `P`.

## Frozen input manifest

Decision-bearing current-main inputs verified by `P17-D03`:

| Path | SHA-256 |
|---|---|
| `PROJECT_STATE.md` | `24bc2fee0c94508704701ff257ddbbbafab3f9698161491798932d78c9ad137d` |
| `NEXT_AGENT.md` | `795077f38587d80f915d441d0caed8dba17f7de542ff5f54e343d58d5fe7b223` |
| `docs/REQUIREMENTS.md` | `e2330d2f689b116bec1f48f967156bd26f3023673d73e3b126190d4983b29209` |
| `docs/EXPERIENCE.md` | `0d41544bd2a94c9a9d230f9c606e5e311fafa413e02c7421e904e188e6a07f56` |
| `docs/decisions/ADR-0001-p13-four-plate-three-rod.md` | `93cc52a2de04033041273aefca9a1769a186d66ddc2249db1281c1f1b09f95e2` |
| `src/xt60_bend_jig/p13_four_plate_three_rod.py` | `7927bc9bb0d0516faa5410200fc870df408fe16b282c2a226828e712ec801067` |
| `tests/test_p13_four_plate_three_rod.py` | `f0f63a8c35b1cb8100703e5bc0c49fd26eca00b045397154c7fd826dab20654f` |
| `tests/test_p13_motion.py` | `7ea1a0fb470c1ffc7899d2c7f93fc97f8da81ecda2e46b5bc4a47c45b387c28b` |

Supplied physical/photo inputs:

| File | SHA-256 |
|---|---|
| `/tmp/codex-remote-attachments/01a02c54-c344-75f0-a983-e2e2dd8162a7/B931B501-4470-4E89-82E8-BD46F0E51353/1-Photo-1.jpg` | `8604131d1b6ba3e636492a964d0c3d92811041bbf93696afefe0a8a20a976f93` |
| `/tmp/codex-remote-attachments/01a02c54-c344-75f0-a983-e2e2dd8162a7/B931B501-4470-4E89-82E8-BD46F0E51353/2-Photo-2.jpg` | `d740f4e252e0bd1636dd674480c865949c3dbde21c6c6e2522d3a4e602c362ec` |
| `/tmp/codex-remote-attachments/01a02c54-c344-75f0-a983-e2e2dd8162a7/B931B501-4470-4E89-82E8-BD46F0E51353/3-Photo-3.jpg` | `8d12c39427823ff36c4205e70716db6df1f166aab87d113b7a0a767bb7f079fe` |

Rejected-branch provenance:

- `git show f733f84:projects/xt60-bend-jig/docs/EXPERIENCE.md`
  records P13 physical assembly observations and P17 rejection.
- `git show f733f84:projects/xt60-bend-jig/docs/iterations/p17-r1-counter-twist-permanent-caps/HANDOFF.md`
  records final P17 disposition: rejected, simulator phase skipped, PR closed
  without merge, do not inherit simulator geometry or provisional dimensions.

## User outcome

The jig must clamp and form only insulated wires, not the XT60 plastic body,
produce a fixed 90-degree bend, allow loading, dry motion, soldering, cooling,
and completed-pigtail removal, and remain a PETG prototype for a `0.4 mm`
nozzle until physical tests supersede that process assumption.

## Observed physical failures and corrections to baseline assumptions

- P13 nominal inner clear span was `26.2 mm` against an XT60 body width of
  `15.9 mm`; photo 3 and user feedback show excessive middle space.
- P13 used nominal `OD4.00 x 50.00 mm` rods, a printed D-shaft total length of
  `45.275 mm`, a principal plate stack of `37.4 mm`, and left-cap `ID3.90` on
  an `OD4.00` rod for `0.10 mm` diametral interference.
- Four physical P13 caps fit; two were too tight to push onto nominal rods.
  That makes rigid `ID3.90` permanent interference unaccepted.
- P13's named `LOCKED` pose did not prove a real lock; P17 R2 must define a
  grounded reaction path and a physical endpoint lock/hard-stop/over-center
  architecture with force, wear, creep, heat, vibration, and self-lock proof
  pending.
- The old `REQ-003` freeze on three uncut `50.00 mm` rods is superseded for
  P17 R2. Rod length must be re-derived from inner span, plate stack, cap
  engagement, and axial running clearances.
- Follow-up user correction for `P17-D02`: do not add three yoke/stability bars
  or yoke socket/tenon requirements. P17 R2 must use the original good
  four-plate plus one center-bar architecture. The center bar is a one-piece
  stepped center axle with a larger central hex spacer, smaller inner-plate hex
  key sections, outer round bearing journals, and thin axial keepers. This is a
  refinement within P17 R2, not a new `P` version.
- Follow-up numeric/assembly correction for `P17-D03`: P17-D02's provisional
  `AF6` fixed-inner hex key/bore with `OD8` outer journal is unassemblable
  because the inner plate cannot slide over the round journal before seating on
  the hex key. P17-D03 supersedes that numeric table inside the same P17 R2 and
  requires `outer_journal_diameter < fixed_inner_hex_bore_af`, coherent
  defaults around `AF10` central spacer, `AF8` inner key, `AF8.15` inner bore,
  `OD7.60` journal, `7.90` outer bearing bore, and an actual retained keeper
  seat/groove.
- Follow-up repair correction for `P17-D04`: P17-I02 candidate
  `cbec2062217dcdbbc8e5e0cc6f278bebc5ecaede8a517f0945c8030299e168de`
  failed validation because the center axle and keepers collide with the
  diagonal rod/caps. User also requires the stepped axle/keeper pivot to sit
  behind the XT60 body, opposite the `+Y` wire-exit/solder side, inside the
  connector body's `XZ` shadow, with positive clearance from XT60 body,
  solder joints, outgoing wires, heat-shrink, and service envelopes.
- Follow-up slot correction for `P17-D04`: current `OD4.00 mm` rods in
  `4.90 mm` fixed slots and `7.55 mm` outer slots are rejected as wobbly and
  visually bulky. P17-D04 requires low-wobble narrow swept slots around the
  actual derived cam centerlines plus a PETG slot-fit coupon ladder; no
  physical slot-fit acceptance is claimed.
- Follow-up repair correction for `P17-D05`: P17-I03 candidate
  `2761adf6154054185bb2cff21e3ef7b923e06682ab760b1acd1e99a22aa370f8`
  failed independent review/validation on four bounded points: lock shoulder
  collision during normal closing, completed-pigtail removal collision with
  fixed inner plates and diagonal rod, ambiguous "body shadow" wording that
  over-constrained the full X-spanning axle, and non-reproducible prose-only
  candidate fingerprinting.
- P17-D05 keeps the P17 R2 architecture and the accepted offset-pivot,
  low-wobble-slot, four-plate, one-stepped-axle, larger-right-outer, permanent
  cap intent. The repair contract is right-inner/right-outer lock pass-in and
  release geometry, a real released-open service removal trajectory/window,
  clarified pivot-behind-body rule, keeper wall/coupon correction, and persisted
  manifest/fingerprint schema.

## Explicit non-goals

- No simulator, animation sidecar, Three.js scene, or JS motion contract.
- No scene-only sign flip and no same-direction shared shaft.
- No removable/service rod-end caps.
- No physical force, heat, creep, wear, vibration, self-lock, cap-retention, or
  printed-fit acceptance from CAD alone.
- No hand-editing generated STEP, STL, 3MF, GLB, DXF, or slicer artifacts.
- No inherited P17 R1 simulator geometry or dimensions.
- No three-bar yoke, stability-bar frame, yoke socket, or yoke tenon
  architecture in P17 R2.

## Material task DAG

Concurrency ceiling: at most three material worker agents active at once. One
writer per project source/artifact namespace. Every material role must return
a receipt with status, verified fingerprint, changed paths/artifacts, exact
commands and results, hashes/manifests, findings with severity, requirement
coverage, unresolved risks, and next action.

| Task | Owner / role | Objective and done gate | Dependencies |
|---|---|---|---|
| `P17-D03` | `/root/p18_design`, design | Correct the P17 R2 center-axle numeric/assembly contract so fixed inner plates can slide over the outer round journals before seating on hex keys, and define retained keeper geometry. Done when docs supersede the D02 impossible defaults without a new P version. | `P17-D02` plus read-only implementation audit |
| `P17-D04` | `/root/p18_design`, mechanism repair designer | Prescribe the smallest repair for P17-I02 collision, slot-wobble, rail-bulk, and REQ-016 lock-proof blockers while preserving P17 R2 identity. Done when DESIGN defines offset pivot, recalculated guide/cam-slot contract, service-envelope gates, low-wobble slot coupon, and falsifiable stop/contact/back-drive tests. | `P17-V02` failure plus user P17-D04 directions |
| `P17-D05` | `/root/p18_design`, independent mechanism repair designer | Prescribe the smallest second/final repair for P17-I03 lock pass-in, completed-pigtail removal, behind-body pivot wording, keeper-wall DfAM, and reproducible fingerprint blockers while preserving P17 R2 identity. Done when DESIGN defines exact states, dimensions, envelopes, tests, and manifest schema for the next implementation owner. | `P17-I03` candidate `2761adf...`, `P17-C03`, `P17-V03`, and user P17-D05 directions |
| `P17-I02` | distinct implementation owner | Repair the P17-I02 CAD source and focused tests against P17-D04; regenerate explicit STEP-first targets and any approved coupon artifacts from source. Done when source, tests, STEP targets, provenance, and snapshots exist and the implementer receipt does not self-approve. | `P17-D04` |
| `P17-C02` | distinct critic owner | Challenge mechanical intent, slide-over assembly, DfAM, center-axle grounding, hex anti-rotation, independent outer rotation, retained keeper strategy, lock path, cap strategy, and likely failure modes against the exact generated candidate. Done when findings are recorded by severity with no implementation edits. | `P17-I02` |
| `P17-V02` | distinct validation/test owner | Run deterministic source, math, actual-solid, assembly-path, motion/service-path, export/parity, snapshot, DfAM, and slicer checks scoped to the candidate. Done when all required evidence is recorded or blockers are explicit. | `P17-I02` |
| `P17-R02` | distinct formal reviewer | Join critic and validator receipts, verify candidate fingerprint, requirement traceability, scope discipline, and finding disposition. Done when acceptance boundaries are explicit. | `P17-C02`, `P17-V02`, and any repair cycles |
| `P17-H02` | continuity/closeout owner | Update `PROJECT_STATE.md`, active iteration `HANDOFF.md`, `NEXT_AGENT.md`, and delivery notes. Done when a new agent can resume from repository files alone. | `P17-R02` |

### Task controls

| Task | Immutable manifest / candidate fingerprint | Allowed reads | Exclusive writes | Forbidden scope | Evidence / commands | Model / effort | Time, output, retry, stop |
|---|---|---|---|---|---|---|---|
| `P17-D03` | Baseline table above, P17-D02 docs, read-only implementation audit finding, and user numeric/assembly correction; design-output fingerprint computed after docs are written. | Entire repo/project, photos, CAD workflow/skill docs, `git show f733f84`. | `docs/iterations/p17-r2-direct-cad-counter-twist/{BRIEF.md,DESIGN.md,VALIDATION.md,HANDOFF.md}`, `docs/iterations/CURRENT`, `docs/EXPERIENCE.md`, `docs/REQUIREMENTS.md`, `PROJECT_STATE.md`, `NEXT_AGENT.md`. | CAD/source/tests/artifacts, root config, PR/git delivery, physical acceptance. | `git status`, `rg`, `shasum`, docs diff, repository structure test. | strong/high design. | One design pass plus at most two focused doc repairs; stop if scope needs CAD implementation. |
| `P17-D04` | P17-D03 manifest `18e5b14b5fa01e2b03dcd4aa2a1e8347b5046070049e087508a1959dd46389b1`; P17-I02 candidate fingerprint `cbec2062217dcdbbc8e5e0cc6f278bebc5ecaede8a517f0945c8030299e168de`; current `DESIGN.md`, `BRIEF.md`, `REQUIREMENTS.md`, `REVIEW.md`, `VALIDATION.md`, source geometry facts, and user P17-D04 directions. | Entire repo/project and P17-I02 source/artifact facts read-only. | `docs/iterations/p17-r2-direct-cad-counter-twist/{BRIEF.md,DESIGN.md,HANDOFF.md}` only. | CAD/source/tests/artifacts, requirements, project continuity, review, validation, git/PR, physical acceptance. | `rg`, source read, read-only BREP probes, `shasum`, `git diff --check`. | strong/high mechanism repair design. | One bounded repair pass plus focused consistency repair; stop if repair requires changing P17 architecture or adding new structure. |
| `P17-D05` | P17-I03 candidate fingerprint `2761adf6154054185bb2cff21e3ef7b923e06682ab760b1acd1e99a22aa370f8`; P17-D04 frozen design-doc manifest `72b9319c25fc17c57a27af2102288072fdcf3a6f8adc4cb3d7375fc146eca3aa`; P17-C03/P17-V03 findings; current D04 docs/source/tests/artifact facts; user P17-D05 directions. | Entire repo/project, P17-I03 source/artifact facts, `P17-C03`, `P17-V03`, and current active iteration docs read-only. | `docs/iterations/p17-r2-direct-cad-counter-twist/{BRIEF.md,DESIGN.md,HANDOFF.md}` only. | CAD/source/tests/artifacts, requirements, project continuity, review, validation, git/PR, physical acceptance. | `rg`, source/doc reads, keeper-wall derivation, `shasum`, `git diff --check`. | strong/high independent mechanism repair design. | One bounded repair pass plus focused consistency repair; stop if lock pass-in/release or completed-pigtail removal requires new architecture or extra parts. |
| `P17-I02` | `BRIEF.md` and frozen selected-design section of `DESIGN.md`; P13 source/tests; requirement/ADR docs. Candidate fingerprint must include changed source/tests/generators/STEP/provenance/snapshots. | Project docs/source/tests/artifacts needed for P17 R2. | New P17 R2 source namespace, focused P17 R2 tests, generated P17 R2 STEP/source-derived artifacts/provenance/snapshots only. | Existing P13 artifacts except read-only comparison; simulator JS; yoke/stability-bar geometry; D02 impossible `AF6`/`OD8` center-axle defaults; docs outside P17 R2 except evidence updates requested by root. | `uv run` focused tests; CAD `scripts/gen`; CAD `scripts/inspect refs/validate/measure/frame/align`; snapshot; source/export parity. | balanced/medium, raise to strong/high only for repeated mechanism failure. | Initial attempt plus two repairs; stop if selected axle architecture proves geometrically impossible or requires a different mechanism. |
| `P17-C02` | Exact `P17-I02` candidate fingerprint. | Candidate docs/source/tests/artifacts, photos, requirements, ADRs. | `REVIEW.md` critic section only. | Source/artifact edits, validation approval. | Static review, artifact inspection, photo comparison, DfAM reasoning. | strong/high. | One pass plus one focused follow-up; stop on blocking architecture defect. |
| `P17-V02` | Exact `P17-I02` candidate fingerprint and any repair candidate fingerprint. | Candidate docs/source/tests/artifacts, validation tools. | `VALIDATION.md` validation section only; temporary ignored scratch. | Source edits, critic/formal approval, physical claims. | Focused `uv run` tests; CAD inspect/validate/snapshot; DfAM; slicer only if 3MF/print-ready artifact is produced. | strong/high for mechanism validation. | Initial validation plus two repair reruns; stop if artifact is missing/stale or not source-derived. |
| `P17-R02` | Final candidate fingerprint plus critic/validator record hashes. | All candidate evidence. | `REVIEW.md` formal-review section only. | Source/artifact edits, physical acceptance. | Hash verification, requirement traceability, finding disposition. | strong/high. | One join pass plus one focused follow-up; stop if receipts conflict or candidate changed without invalidating gates. |
| `P17-H02` | Final accepted digital candidate fingerprint and review outcome. | All project docs/evidence. | `PROJECT_STATE.md`, `NEXT_AGENT.md`, `HANDOFF.md`, concise delivery notes. | Design/source/artifact changes unless a formal repair cycle is reopened. | `git status`, path hashes, required local tests if delivery requested. | balanced/medium. | One closeout pass; stop if acceptance state is not resolved. |

## Candidate fingerprint rule

For every material post-design gate, compute a sorted SHA-256 path-and-content
manifest over the task's declared decision-bearing inputs and candidate files.
Mutable orchestration/status records, scratch logs, and ignored build caches are
excluded. If a file in the declared manifest changes, only gates that include
that file are invalidated.
