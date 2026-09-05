# P2 R1 MakerWorld simulator brief

**Iteration:** `2026-09-03-p2-r1-makerworld-simulator`
**Design owner:** DES-MW-01
**Baseline:** reviewed P1 R7 full case, candidate `8d3941772cca549846937dcad6ce4a05e06f5bba104c261668a0cf747c62b6a1`; no R7 file may change.

## Outcome and boundary

Create a self-contained HTML/Three.js visual intent gate for a future MakerWorld-oriented parametric case generator. It shows an assembled 39 mm cylindrical case as two **mid-split** pieces and lets the user place the split/thread by distance from the closed top or by percentage from the same top.

The simulator is not CAD, mesh, STEP, fabrication geometry, slicer evidence, or physical acceptance. Values describe a visual axial-accounting model derived from R7 defaults. It must state that warning readouts are design prompts, not proof of wall thickness, thread fit, printability, or device retention.

## Stable requirements

| ID | Requirement | Evidence target |
| --- | --- | --- |
| MW-REQ-01 | Show two separately identifiable cylinder pieces whose joint is in the body, not a tiny top lid. | Render/DOM check: `upper-piece`, `lower-piece`, seam and thread-band labels coexist. |
| MW-REQ-02 | `split_from_top_mm` is the sole stored split value; percent edits convert into it and mm edits derive percent. | Pure-math round trip and UI synchronization tests. |
| MW-REQ-03 | The top datum is the closed outer end. Global assembled `Z=0` is the closed lower end and `Z=H` is the closed top end. | Rendered datum labels and invariant tests. |
| MW-REQ-04 | Default values reproduce the R7 axial reference: `H=219`, `C=213`, upper cavity `81`, lower-cavity accounting readout `137`, `P=9`, effective engagement `6`. | Pure-math default test. |
| MW-REQ-05 | Pattern evaluation uses assembled global Z before clipping to the pieces; moving the split must not create independent local phases. | Same `(theta,zGlobal)` field value before/after split edit and seam-neighbour probe. |
| MW-REQ-06 | Offer smooth, current blunt diamond, shallow helix, and wave/flutes. | Pattern-select DOM/render test. |
| MW-REQ-07 | Read out thread band, effective engagement, nominal wall/clearance prompts, and warnings. | Boundary and warning-state tests. |
| MW-REQ-08 | Serve the finished static preview only through the existing private static service, at a new isolated route. | Local/private HTTP and user-surface gate; preserve existing routes. |

R7 requirements REQ-01, REQ-02, REQ-03, REQ-05 through REQ-10, and REQ-13 remain the authority for eventual CAD/physical work. This preview neither supersedes nor satisfies them.

## Topology, use sequence, and non-goals

The user changes either **distance from top** or **top percentage**, observes the single horizontal seam and the thread band move, selects a pattern, then answers this gate: *Does this show the intended two-piece mid split and the desired relative thread location?* Pass means only that topology and placement intent are understood. Fail means correct the contract before any generator work.

The lower piece is fixed in assembled space. The upper piece is fixed at the top datum. The split moves the boundary between them; neither is represented as a small removable top cap. Camera orbit, zoom, and exploded spacing are display-only controls. No displayed part moves as a consequence of a pattern selection.

Excluded: changes to `cad/p1_r7_end_chamfer/`, its four STEP files, `tests/`, present previews, public port 3245, existing private routes, MakerWorld publication, CAD/export/slicer/print work, and claims of fit, strength, drainage, or printability.

## Planned source, output, and delivery paths

Implementation owns only this new namespace:

- `preview/p2-r1-makerworld-simulator/index.html`
- `preview/p2-r1-makerworld-simulator/app.js`
- `preview/p2-r1-makerworld-simulator/style.css`
- `tests/test_makerworld_simulator.mjs`
- iteration-local implementation, validation, critique, and review records/manifests.

The proposed delivery route is `https://mac-mini.duckbill-ionian.ts.net:8448/laifen-makerworld-simulator`, using the already running loopback 8972/private 8448 static service. A future delivery worker may add that one route after local verification; it must not alter `/laifen-chamfer`, `/laifen-full`, `/laifen-full-section`, the CAD Viewer 3249/private 8449 service, or public 3245. A successful HTTP request does not prove the user's browser/phone presentation; the user-visible gate remains required.

## Frozen task DAG

| ID | Role / owner class | Depends on | Exclusive writes | Done gate and ceiling |
| --- | --- | --- | --- | --- |
| DES-MW-01 | design, Terra/high | frozen baseline | this BRIEF/DESIGN/inputs only | Contract and manifest complete; 12 min, 10k output, initial + two doc repairs. |
| IMP-MW-01 | implementation, Terra/medium | DES fingerprint | new simulator source and its test only | Parameter math, semantic DOM, rendering; 20 min, 12k output, initial + two focused repairs. No CAD/static-service mutation. |
| VAL-MW-01 | independent validation, Sol/high | frozen implementation candidate | `scratch/makerworld-simulator-validation/` and iteration `VALIDATION.md`/evidence manifests | Run math/UI/render checks on exact candidate; 12 min, 8k output, initial + two method repairs. Read-only source. |
| CRIT-MW-01 | independent critique, Terra/high | same candidate | `scratch/makerworld-simulator-critique/` and `CRITIQUE.md` | Challenge topology, datum language, phase continuity, mobile clarity and false CAD claims; 10 min, 7k output, initial + two focused findings. Read-only source. |
| REV-MW-01 | formal review, Sol/high | VAL + CRIT exact receipts | `REVIEW.md`, review manifest/receipt only | Verify scope, manifests, requirement traceability and dispositions; 8 min, 6k output, initial + two provenance repairs. |
| DEL-MW-01 | private static delivery, fast/low | formal PASS | route-specific static-service configuration and readiness receipt only | New isolated path returns 200 locally/private; then request/record actual user-surface check. 8 min, one retry. |

At most three workers may run. After implementation freezes a candidate, VAL and CRIT may run in parallel against the same hash; REV is their join. DEL follows only a formal PASS. A candidate-source change invalidates only VAL/CRIT/REV/DEL manifests that include it. Stop and return to design if the model cannot preserve both canonical conversion and global-Z phase; stop and ask the user if they reject the topology gate. Each worker must return the role, status, exact input fingerprint, changed paths, commands/results, requirement coverage, findings, unresolved risks, and next action.
