# P1 R4: uniform outside diameter and full sidewall diamonds

Design owner `/root/uniform_skin_design`, task DES-R4-01, 2026-09-02. Design-only delivery; no new CAD exists at this gate. Applicable CAD skill and repository workflow read. Baseline HEAD `d0aab1ff21a0cd2e5790c9800fcec7cfec2bfc3c`; all58 entries of `inputs/baseline.sha256` verified, fingerprint `fef9b674d14d5fb0469425db28e65cf14f4c8b58b9018cdf9eca8c830dcf8e3f`. R3 source/artifacts remain immutable.

<!-- FROZEN-CONTRACT-BEGIN -->
## Intent and evidence

The user wants a straight assembled cylinder with the same outside diameter from end to end and diamond texture over its entire visible outer sidewall, including the outside of the female thread collar. No bulge, broad smooth ring, or externally untextured collar. A thin cap separation seam is acceptable. The supplied photo was inspected: one body and three caps, pronounced smooth collars and limited textured bands. It supplies appearance evidence, not dimensions. The user reports all three hand closures are good; exact print provenance and measured performance remain unknown. Canonical observation: `docs/observations/2026-09-02-coupon-fit/` and EXPERIENCE OBS-06/07.

This version deliberately supersedes REQ-08/R3's external2mm smooth exclusions, exterior fades and raised-only skin envelope. Internal threads and functional contact faces remain smooth. R4 deliberately changes the approximate REQ-05 OD39 target to40mm: retaining fitted threads,0.45mm texture depth and1.8mm minimum structural wall with clearance budget0.30 requires at least39.90mm. This is a design choice for the new external intent, to be shown explicitly in the small2D gate.

## Requirements

| ID | Contract and classification |
|---|---|
| R4-01 | Invariant: common cylindrical diamond-crest envelope, selected OD40.00; no outward collar or taper, no broad blank sidewall zone. Only0.30mm axial textured relief at each closed bed edge is allowed. |
| R4-02 | Invariant: shared mathematical diamond generator covers assembled body z[-35.1,0] and cap z[0,43.4], including seam and collar. Common phase at z0,theta0; axial pitch4.8 unchanged when length changes. |
| R4-03 | Invariant: bores30/31, original right-hand thread pitch2, engagement6, root16.8/crest17.4, clearance0.25 default and budget0.30; actual male/female internal geometry and positive shoulder stop z0 preserved. |
| R4-04 | Invariant: cavity72.5, floors3, body inner floor z-32.1, cap inner floor40.4, male tip9 and original internal cap transition10.2..12.4. Short experiment remains closed length78.5. |
| R4-05 | Derived: inward valley depth0.45 from crest radius20, valley radius19.55; minimum female ligament1.85 using budget0.30,1.90 at c25; male root wall remains1.8. No wall thinning to save OD. |
| R4-06 | Design choice: blunt diamonds use plateau fraction0.18, axial pitch4.8 and target arc pitch3.63; derive common integer repeat count from valley radius. Default34 repeats, common actual arc pitch about3.613. |
| R4-07 | Deliver one body and one C25 cap, source-defined closed assembly and two-part print layout. Alternate clearances remain parameters; no three-cap print set is required. |
| R4-08 | Invariant: parts print vertically openings up, cap Rx180. U1/PLA/nozzle0.4/layer0.2/supports off are intended settings only. Actual source solids, exported solids, first-layer geometry and surface normals require focused checks. |
| R4-09 | Physical unknown: new textured collar feel, seam registration under real tightening, print quality, torque/wobble/wear and strength. Existing hand report is useful baseline evidence, not R4 physical acceptance. |

Use sequence: empty short body/cap; start original screw by hand; twist to original shoulder; assess straight profile, coverage and grip; reopen. Full Laifen length, installed brush fit, retention and end-contact policy remain outside this task. No p2.4/DES07 repair, broad parameter-domain certification, drainage redesign, slicing/upload/start or printer control. Any full-length request reopens its own fit gate.

Coordinates: mm; common axis Z, shoulder/seam at z0, body below and cap above. Proposed source namespace `cad/p1_r4_generator/`; primary outputs `body.step`, `cap_c25.step`, `closed_c25.step`, `print_layout.step` from named parametric `.step.py` entrypoints. Diagram `preview/p1-r4-profile-study.svg/.png` is formula-based, not a CAD render.
<!-- FROZEN-CONTRACT-END -->

## Execution boundary

DES-R4-01 owns only this brief, DESIGN, numeric notes, contract manifests and profile study source/outputs. Root owns coordination/state/NEXT_AGENT/HANDOFF; physical-evidence writer owns observation records. Strong/high design work, qualitative6minute/7k-token ceiling, initial plus one focused correction, no child agents. Next DAG gates: present the small profile/coverage study as an informative checkpoint under the already clear user intent; distinct implementation; frozen candidate for distinct critic and validator; distinct formal reviewer join. No implementation or engineering acceptance is asserted here.


## Mutable execution plan and status

Root orchestration ledger, outside the frozen design contract. Full input hashes and receipts are indexed in HANDOFF; inputs below are immutable SHA-256 path/content manifests. All tasks share repository baseline d0aab1ff21a0cd2e5790c9800fcec7cfec2bfc3c and this project/iteration. At most three workers run simultaneously. Root owns coordination/indexes/private presentation only. Worker source scopes are disjoint; no downstream source read occurs before its candidate freeze.

| Task / owner | Role, dependencies and frozen inputs | Exclusive writes / done gate | Model, qualitative ceiling, retries | Status |
|---|---|---|---|---|
| OBS-R3-06 /root/record_print_feedback | Observation; R3 inputs/obs06-inputs.sha256, 10 entries, 4dc93751… | EXPERIENCE append and docs/observations/2026-09-02-coupon-fit; retain photo/user report with physical limits | Luna/low; 2min/2k; initial+1 doc correction | Complete |
| DES-R4-01 /root/uniform_skin_design | Design; inputs/baseline.sha256, 58 entries, fef9b674… | R4 BRIEF/DESIGN/NUMERIC_NOTES/design freeze and preview/p1-r4-profile-study; numeric feasible contract and inspected profile | Sol/high; 6min/7k; initial+1 math/diagram correction | Complete |
| IMP-R4-01 /root/uniform_skin_impl | Implementation after design; inputs/design-contract.sha256, 63 entries, d1413f9b… | cad/p1_r4_uniform_skin, tests/test_uniform_skin.py, scratch/uniform-skin-impl, IMPLEMENTATION and candidate manifest; four valid STEP/source targets with preserved internals, freeze for independence | Sol/high; 20min/18k, 3min checkpoints; initial+2 focused repairs and design stage ceilings | Complete |
| VAL-R4-01 /root/uniform_skin_validate | Independent validation; prep against design63 only, execution after candidate80 e56a1178…; own validation-inputs85 44193194… | scratch/uniform-skin-validation, VALIDATION and validation manifests; actual solids/motion/math/constraints/requirements/STEP evidence | Sol/high; prep5min/5k, execution15min/12k; initial+2 tool repairs | Complete |
| CRI-R4-01 /root/uniform_skin_critique | Independent critic, parallel with validation after candidate80 e56a1178… | scratch/uniform-skin-critique, CRITIQUE; mandatory written-STEP snapshots and intent/manufacturing critique | Terra/high; 10min/9k, 3min checkpoint; initial+2 tool repairs, final2min/1k exact-command receipt correction | Complete |
| CMP-R4-01 /root/download_design_compare | User-requested reference comparison, independent of CAD generation; reference-comparison67 c0acb5cd… | scratch/download-design-compare and REFERENCE_COMPARISON; measured geometry comparison with authoring-method uncertainty | Terra/medium; 6min/6k; initial+1 tool repair | Complete |
| REV-R4-01 /root/uniform_skin_review | Distinct formal join after critic+validator; formal-review111 7e36a21d… | REVIEW, optional review-receipt manifest, scratch/uniform-skin-review; audit exact provenance/coverage/findings and scoped acceptance | GPT5.4/high; 6min/6k; initial+1 report correction | Complete |

Every worker may read the applicable frozen requirements/contracts/source/evidence and repository/skill instructions, but cannot modify another role's scope. R3/downloaded geometry remains read-only; no copying downloaded geometry into new CAD. No printer control, slicing, unrelated routes, Git publication, environment changes or child agents. Critic/validator/formal reviewer never repair the candidate themselves. Retry ceilings include focused tool corrections; stop on changed frozen input, write-ownership conflict, geometry/fit contradiction or exceeded budget and report exact evidence to root. Any source repair invalidates only dependent gates and requires a new candidate fingerprint. Reports include commands/results, hashes, requirement coverage, severity, remaining gaps and next action; formal review alone joins the independent results. Mutable execution records are excluded from design fingerprints.

DOC-R4-01 /root/refresh_project_readme, Luna/low,2min/2k qualitative initial+one doccorrection, updates only project README and scratch/readme-refresh-receipt.md to resolve formal nonblocking stale-entrypoint finding. Frozen5 inputs/readme-refresh.sha256 fingerprint12bf79d079868d397bc62629b34820d35d9b4f32121cd2bc721731c2a96a9dc7. Prior README is preserved in inputs/project-readme-before-r4.md. No candidate/frozen review inputs changed; no new geometry gate.

DOC-R4-01 complete. Final projectREADME SHA256bd324bf04355422e98a4eb1ed1ae7560d31ccb8ca7ac464de6642d1feb14edf6 resolves the nonblocking formal continuity finding; one wording correction clarifies0.25mm radial thread clearance. Source/STEP/review fingerprints unchanged. All DAG tasks complete.
