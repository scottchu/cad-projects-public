# Slide 4 count layout

Replace only slide 4's count presentation in the accepted 22-slide deck. Each existing number and its existing explanation must form one visually adjacent group at desktop (1280 × 800), narrow (about 855 px wide), mobile (390 × 844), and the existing print page. Preserve all count, caveat, source, note, and slide-count meaning. REQ-017 authorizes this sole exception to the prior 21-section preservation boundary.

Baseline HTML: `ebb4113fb57951ba62cfa2760fdec40d918991b265b8c688a07d713c61797ee4`; accepted manifest: `4f79f9740e85eb0e11b16cdd2ff219324a69756b5d444add18b870fa81dedda1`. Full baseline `index.html` and `build.mjs` are retained at `/tmp/cad-slide4-before/` for complete nested-section and inline-script preservation checks.

## Execution DAG

| ID | Owner / role | Dependencies | Done gate | Exclusive writes | Ceiling |
| --- | --- | --- | --- | --- | --- |
| C4 | /root/slide4_writer; implementation | verified baseline and frozen inputs | paired count layout; build/check; frozen candidate; preservation receipt | `build.mjs`, generated `index.html`, this iteration contracts/manifests/IMPLEMENTATION, requirements/experience/decision/CURRENT | balanced/medium; 2 min, 4k; initial + two repairs |
| V4 | /root/slide4_validation; validator | C4 frozen candidate | source preservation plus desktop/narrow/mobile/print rendering evidence | `VALIDATION.md` | strong/high; 2 min, 3k |
| C4C | /root/slide4_critique; critic | C4 frozen candidate | independent novice clarity and factual/visual critique | `CRITIQUE.md` | balanced/medium; 1 min, 2k |
| R4 | /root/slide4_review; formal reviewer | V4 + C4C on the same candidate | provenance join and independent review | `REVIEW.md` | balanced/medium; 1 min, 2k |

Inputs are immutable path-and-content SHA-256 records. V4 and C4C may run in parallel with disjoint writes; root owns `PROJECT_STATE.md`, `NEXT_AGENT.md`, and `HANDOFF.md`. Read only project/root docs, the user screenshot, and temporary tools. C4 may write only the paths named above; all other source, simulator, scripts, tests, dependencies, locks, Git, hosting, CAD, slicer, and printer scope is forbidden. Stop on evidence drift, scope growth, or after two focused repairs. Each receipt states fingerprint, commands, coverage, findings, limits, and next action.
