# Requirements

## Intent and invariants

- **REQ-001 — Format:** English, standalone offline HTML lunch-and-learn presentation, 18–22 slides, approximately 40–45 minutes including discussion. Presentation first; no live end-to-end demo implementation.
- **REQ-002 — Narrative:** explain why/how/what, expected versus observed reality, the gap, understanding, decomposition into phases and subsystem responsibilities, composition and feedback.
- **REQ-003 — Real histories:** Kage and XT60 are central. Include actual iteration struggles and how the process changed. Distinguish proposals from completed responses.
- **REQ-004 — Agent workflow:** connect CAD lessons to the concrete slicer pilot and the agent-managed workflow direction. Preserve Preparation and Operations as peers; explain continuity, teaching and consequential authority.
- **REQ-005 — Evidence:** cite exact primary repository sources with stable IDs, dates, paths, hashes and offline readable summaries. Count records only using declared scope; never relabel counts as prints or total attempts.
- **REQ-006 — Acceptance:** separate source/CAD, export/slicer/operational, and physical evidence. Long-term product direction is not a present runtime capability claim.
- **REQ-007 — Visual truth:** use only existing inspected CAD assets; no fabricated physical photos or CAD acceptance. Label conceptual mechanism diagrams explicitly.
- **REQ-008 — Interaction:** two useful teaching interactions: nominal hole-fit prediction versus observed coupon data; completion/evidence/ownership exercise. Accessible keyboard controls, reset and print fallback.
- **REQ-009 — Delivery:** keyboard navigation, overview, presenter notes, embedded source references, responsive layout, printable complete slides, no external runtime resources.
- **REQ-010 — Quality:** restrained editorial composition, readable projected text, one main claim per slide, low audience-copy density and richer speaker notes. Independent factual/visual review and browser validation against an exact candidate.
- **REQ-011 — Development roles:** explain how bounded orchestrator, design, implementation, critique, validation and formal-review responsibilities preserve candidate identity and durable evidence. Distinguish these development roles from the product-facing Manager, Teacher and Engineer/Operator roles.

## Design choices and derived constraints

22 slides; system fonts; embedded image data; authored HTML/SVG for conceptual diagrams; no external runtime resources. Interface calculations must label nominal diametral clearance separately from printed measurement. Interactive fit outcomes are qualitative observations, not probabilities or simulated physical results.

## 2026-09-01 visual/simulator addendum

- **REQ-012 — Explicit visuals:** preserve 22 slides while adding legible connected feedback and agent fork/join flowcharts plus a semantic Kage/XT60 challenge/evidence/response table. Preserve observed versus proposed status.
- **REQ-013 — Useful Three.js model:** upgrade exercise 1 with real bundled Three.js and a rod/hole cutaway. Separate nominal dimensions, adjustable hypothetical hole error and analytic radial/diametral clearance from unchanged observed coupon outcomes. Label exaggerated geometry and teaching-model limits; never infer friction or physical acceptance.
- **REQ-014 — Resilient delivery:** inline exact pinned Three.js with license provenance, root npm workspace only, no runtime network resources; on-demand rendering, keyboard controls/reset, camera alternatives, reduced-motion compatibility, useful no-WebGL section fallback and deterministic printable section. Independent candidate-specific critique, validation and formal review are required.

The active visual-simulator DESIGN.md defines the exact selected parameters and formulas. This addendum intentionally permits an embedded runtime library; the first-deck dependency-free choice remains historical. It does not authorize production CAD, slicing or printer operations.

## Non-goals and unknowns

No CAD modification, new slicing, printer action, upload, publication or deployment. No acceptance of the source projects. Audience composition and actual speaking pace remain working assumptions; user review may refine both. Physical mechanism outcomes retain their source-record limitations.

## 2026-09-02 concrete-opening addendum

- **REQ-015 — Concrete introduction:** slides 1/2 must name 3D printing, CAD and AI agents and tell a first-person why → how → what story grounded in Kage (kinetic shadow clock) and the XT60 wire-bending jig. The user permits creative motivation framing, not invented dated events, measurements or successful outcomes. Preserve slides 3–22 and all simulator/source evidence.

## 2026-09-02 concrete-fit-example addendum

- **REQ-016 — Physical example before framework:** slide 3 must introduce the XT60 metal rod and printed test piece, label what is being inserted into what, explain the CAD-design hole size versus the recorded very-tight physical result in everyday words, and state the lesson after the example. A labeled schematic must not imply measured printed geometry. Preserve the other 21 slide sections, both scripts and simulator. This user-requested revision supersedes only the slide-3 abstract diagram in REQ-012 and the slide-3 preservation boundary in REQ-015.

## 2026-09-02 count-layout addendum

- **REQ-017 — Paired count clarity:** slide 4 must keep each count adjacent to its existing description at wide, narrow, mobile, and print sizes. Preserve the exact two counts, descriptions, caveat, source and speaker-note meaning; preserve the other 21 complete sections and both scripts. This user-requested revision supersedes only the slide-4 preservation boundary in prior addenda.

## 2026-09-02 project-introduction addendum

- **REQ-018 — Introduce each project before its mechanics:** slide 3 must introduce XT60 as the connector for the two insulated wires and explain the intended jig as a small tool/holder for a fixed 90-degree bend during soldering and cooling, before the rod/hole example on slide 4. Slide 10 must introduce Kage as the intended wall-mounted kinetic shadow-clock concept and define its hour, minute and second shadow-fin roles before the relationship challenge. Preserve slide order except slide 3 new, prior slides 3/4 moved to 4/5, and slide 10 revised; preserve all other 18 complete sections and both scripts. This user-requested revision supersedes only the relevant preservation boundaries in REQ-015 through REQ-017.

## 2026-09-02 audience-rewrite addendum

- **REQ-019 — Whole-deck newcomer clarity:** every slide must identify its object or action, evidence status and lesson in ordinary language. Rewrite all 22 slides where needed, especially the fit exercise, slicer-preview observation, shared 90-degree wire-reference defect, Kage collision/restart, and agent/print workflow. Preserve real source facts, interactive IDs/runtime, 22 slides, offline delivery and explicit acceptance boundaries. This user-requested revision supersedes earlier slide-preservation limits.

## 2026-09-02 story and show-and-tell addendum

- **REQ-020 — Visible causal story:** visible slide content alone must connect each example to the intended object and next action. Explain the XT60 forming rods and their sliding guide relationship before fit evidence; merge repeated fit beats and remove disruptive inventory slides. Use 18–22 slides where useful; no fixed count.
- **REQ-021 — Show-and-tell:** no audience questions, quizzes, prediction/reveal/reset controls, diameter choices, hypothetical sliders or physical tasks. Show actual results directly. Useful read-only Three.js demonstrations explain fit and plate/bed/contact/orientation; navigation remains. Offline execution, accessible labelled fallback and printable explanation remain required. This supersedes REQ-008 and the interaction, fixed-count and preservation obligations of REQ-012–019.

## 2026-09-02 feedback-first addendum

- **REQ-022 — Central argument:** lead with people and agents working side by side across digital and physical tools. Explain why feedback must be designed into the workflow from day one; show observations returning to joint interpretation and the next decision. Case studies serve this argument.
- **REQ-023 — Framing and scope:** camera, sensor and robotic-arm examples are a broader direction, not demonstrated integrations. People help define intent and interpret evidence; agents carry continuity. The floating-plate detail and bed scenes may be removed, slide count may shrink, and useful real read-only Three.js fit evidence remains. This supersedes earlier fixed-count and bed-scene obligations; offline/show-and-tell/source boundaries remain.

## 2026-09-02 collaboration-story addendum

- **REQ-024 — Demonstrate collaboration:** show one sourced physical observation, documented agent contribution and next decision, with named source attribution and pending physical outcomes distinguished. Make task/failure relationships visible; consolidate process frameworks; connect future action/measurement tools in one illustrative return loop; give a portable day-one sentence and concrete fit criterion. Case-specific source facts override assumed actor narratives.

## 2026-09-02 maker-story steering

- **REQ-025 — Personal maker story:** lead with the tinkerer and desired objects, attempts, surprises and observations about working with the agent. Use warm, candid first-person show-and-tell; feedback emerges from the cases and one simple close. This supersedes framework-first opening, formal loop and planning-table requirements where they conflict. Do not invent feelings, dialogue, events, successes or actor work. Keep material pending/proposed/illustrative states visible; detailed IDs and provenance belong in notes/sources.

- **REQ-026 — Personal turning point:** the user’s frustrating rail-route iterations, reliance on AI for an imagined solution and simulation-enabled understanding form the central story. Other cases support it. User recollection permits these personal facts but does not establish an exact iterationcount, first discovered mechanicalfact, particular screenshot or successfulphysicaloutcome. The archived relationship example and accepted2Dprofile must be source-grounded and labelled accurately.

## 2026-09-02 additive balance correction

- **REQ-027 — Add, do not replace:** restore the previous13-slide collaboration talk and its exact visible/browser titles, broader digital/physical argument, feedback loop, planning table and all cases. Add only a compact2–3-slide personal rail anecdote near the jig introduction, with local transitions and necessary clarity corrections. This supersedes the replacement/narrowing instructions in REQ025/026; personal evidence, factual boundaries and show-and-tell remain. No global genre/theme rewrite or case deletion.

## JF — Current journey revision, 2026-09-03

The explicit journey-feedback BRIEF supersedes earlier count, title, palette and additive-only constraints. JF-01:20 main slides,20–30min, light engineering style. JF-02:actual XT60 history and physical observations, counts as recorded folders only. JF-03:shared later P25 interface, exact original missing boundary, digital/physical evidence separated. JF-04:contextual rod observations, prepared web experiment, relative cost hierarchy and experimental planning. JF-05:expensive/lossy versus focused/shared loops; human judgment and agent continuity. JF-06:Orca demonstratedguided/currentread-only/direction layers, syntheticfixture identified. JF-07:Laifen travel-case purpose, actual earlier threadphoto, reviewed R6images, exactearlier sandboxed qstudy, reset/fallback/close; physicalfitpending. JF-08:softwareplanningtransfer and concrete future sensor example. JF-09:offlineHTML, actualread-onlyThreeJS/staticfallback,20-pagePDF viaindependentvalidator, notes/runbook, noaudiencequiz. JF-10:no sourceproject/CAD/device/hosting/dependency/lock mutation.

## J2 — User-approved causal walkthrough, 2026-09-03

J2-01: begin with buying a printer and downloaded models before personal ideas expose the skill stack. J2-02: visibly identify the agent as assistant and teacher. J2-03: project problems motivate recorded fit knowledge, distinct focused studies and tool integration; no invented chronology or results. J2-04: use one earlier rod-path image and one P25 fixture image as separate historical hypotheses, not multiple states counted as simulations. J2-05: prepared-only web title and contextual fit reference. J2-06: make costly versus focused loops the payoff of project/system co-evolution. J2-07: retain Laifen current demo, full-size direction and unresolved loaded-fit decision; software/future chains remain illustrative. J2-08: preserve title, light style, authentic assets, runtime/demo/Three.js and corrected print media boundary; new full PDF requires independent validation. This supersedes only the prior ordering and causal framing.
