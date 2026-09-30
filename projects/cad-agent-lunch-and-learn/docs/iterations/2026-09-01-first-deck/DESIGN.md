# First deck: narrative and evidence contract

## Communication job

By the end, a mixed technical audience should know how to turn a mismatch between a digital prediction and a physical outcome into a smaller, testable next step, because reliable agent workflows depend on preserving intent and earning evidence at each boundary.

The presentation is English, 22 slides, approximately 40 minutes including two embedded discussions plus 5 minutes for audience questions. Timings belong in presenter notes only. Central takeaway: **Make the next uncertainty small enough to test.** This is a reasoning journey through actual project difficulties, not a finished-product showcase or a live demonstration.

## Selected approach and alternatives

- Selected: expected reality → observed reality → gap → understanding → smaller phases and subsystems → composition → feedback. XT60 and Kage supply the evidence, and the slicer pilot extends the same reasoning into agent-managed software and hardware workflows.
- Rejected: chronological version catalogue, because it hides the transferable lesson in names and counts.
- Rejected: a seamless end-to-end success story, because physical acceptance and the integrated product vision remain unproven.
- Rejected: an agent/tool feature inventory, because responsibilities and evidence explain the workflow better than product names.

## Visual and interaction contract

Warm canvas `#F3F0E8`, charcoal `#222623`, rust `#AF492D`, teal `#14665F`, muted grey `#626961`; confirm final contrast. Use system fonts only: a restrained serif for selected oversized claims and a clean system sans for explanation, labels and controls. A 16:9 desktop stage may adapt to available space; mobile must remain readable. Giant type, generous margins, thin rules, flat diagrams, a few large numerical statements, and two real CAD-image moments. Avoid card grids, decorative icons and ornamental gradients. Dark charcoal chapter moments may be used for slides 1, 8, 11 and 22. Do not shrink text to fit: shorten copy or adjust layout.

Use real assets A01/A02 only, embedded as data URLs in the standalone HTML. Both were visually inspected during D1. Preserve aspect ratio; do not crop away a geometry feature used to support a claim. A01 is a digital exploded CAD view with four coloured plates, three grey rods, a purple axle and black caps. A02 is a digital right-side view dominated by a blue plate and slots. Neither is a photograph, a physically accepted assembly or the corrected P20 wire baseline. Do not invent CAD screenshots or physical photographs. Other diagrams are HTML/SVG, clearly labelled conceptual when representing a mechanism.

Every source-derived slide has visible short source IDs in a small footer. IDs open readable embedded source notes with title, date, canonical path, repo-relative path, section/line reference, hash and limitation; the essential evidence must remain usable offline without local repositories. Presenter notes include source IDs and stage boundaries. References supplement the slide count rather than adding a dense bibliography slide. No timing, planning instructions, task IDs or authoring metadata on audience canvas.

Controls: previous/next buttons, arrow keys, Home/End, overview, notes, source references, and fullscreen if supported. Include accessible names and visible focus. Keyboard shortcuts must not hijack interaction controls. Print mode shows one complete slide per page; interactive answers must be revealed in print. Hidden notes and source drawer must not obscure the slide while presenting. Reduced-motion support; no autoplay.

## Slide plan

### 01 — When the model passes and the part doesn’t

**Audience copy:** “What building a jig, a shadow clock, and an agent workflow taught me.” Small footer: “CAD × physical feedback × agents”.

**Visual:** giant editorial title on charcoal; one thin looping line that will recur at the end. No invented product hero.

**Speaker notes (1 minute):** Open with the tension: a model can look plausible, a test suite can be green, and a printer can finish, while the thing still fails its purpose. These are different observations. This talk follows the reasoning process that developed while working on the XT60 jig and Kage, then carries it into a slicer and printer workflow. The useful output is a way to decide the next experiment. The histories contain rejected simulations, missed collisions, physical fit failures and provisional software findings. They are valuable precisely because the gaps are visible.

**Sources:** S01, S02, S03, S06. **Job:** establish the central tension.

### 02 — Start with the outcome you want

**Audience copy:** “WHY — What should become easier?” / “HOW — What has to be true?” / “WHAT — What can we build and test?”

**Visual:** three large typographic steps on a single descending line, not separate cards. Tiny example below: “XT60: hold the intended bend → preserve geometry and access → test a jig.”

**Speaker notes (2 minutes):** Why, how and what are questions to keep revisiting. For a jig, the desired outcome is not a collection of printed plates: it is a useful way to hold the intended wire bend with access for the actual operation. That immediately raises constraints about fixed and moving parts, force, removal, fit and heat. The artifact is one proposed answer to those constraints. For Kage, an intended shadow-clock experience depends on mechanical motion, light and packaging working together. Ask the room for a recent task where the output file existed but the intended outcome had not happened yet.

**Sources:** S01, S02, S04. **Job:** connect purpose to testable constraints.

### 03 — Expected reality is a hypothesis

**Audience copy:** “Expected: slides freely. Observed: binds.” / “The gap is the next question.”

**Visual:** two simple aligned lines titled EXPECTED and OBSERVED, separated by a rust bracket marked “gap”; underneath, the loop “Predict → observe → explain → test”. Conceptual, no fabricated measurement curve.

**Speaker notes (1.5 minutes):** A dimension in CAD describes an intention. A prediction about how the printed part behaves adds assumptions about process, orientation, material and use. When observation differs, name the mismatch before changing a parameter. Is the requirement wrong, the geometric model wrong, the exported artifact wrong, the preparation wrong, or the physical assumption wrong? We will see examples at several layers. The loop is a reasoning tool: state the expected observation, collect the actual one, explain the difference, then choose the smallest test that could disprove the explanation.

**Sources:** S01, S06. **Job:** introduce the recurring loop.

### 04 — The record contains many revisions

**Audience copy:** “25 formal XT60 iteration directories” / “11 Kage phase-3 design amendments” / “These count records, not prints or total attempts.”

**Visual:** huge 25 and 11 on a flat split canvas; fine non-proportional trail of revision labels behind them. Add “repository snapshot • 1 Sep 2026”. Do not chart these as comparable productivity metrics.

**Speaker notes (1 minute):** These numbers communicate the breadth of the recorded struggle, not a success rate. The canonical XT60 checkout contains 25 top-level formal iteration directories; the working presentation checkout contains only 12. Kage has 11 amendment files matching one specific phase-3 naming family. Neither count includes every conversation, repair cycle or print. Versions also have different meanings across the projects. We will follow a few decisive failures and responses rather than walk through the entire catalogue.

**Sources:** S08. **Job:** establish iteration depth without overstating counts.

### 05 — A small jig couples many decisions

**Audience copy:** “Fit. Motion. Holding. Access. Removal.” / caption: “XT60 P19 R1 • historical exploded CAD view”.

**Visual:** A01 occupies about two-thirds of the stage. Short words run down one side; no unverified callout arrows assigning exact functions. Caption includes “Digital reference; physical acceptance not established”.

**Speaker notes (2 minutes):** Orient the audience to the four-plate and three-rod assembly in this historical view. A change to plate spacing can affect rod length and cap engagement. A motion that reaches an endpoint can still have poor hand force, friction or access. A part can fit during assembly and obstruct removal afterward. The image helps explain why apparently local changes can propagate. It is P19 reference imagery, not an accepted current baseline or proof that the mechanism works. We now isolate one relationship that was small enough to measure directly: a rod sliding in a printed hole.

**Sources:** A01, S01. **Job:** make coupling concrete.

### 06 — Which hole would you print?

**Audience copy:** “4.00 mm rod · PETG · 0.4 mm nozzle” / “Choose a nominal hole diameter.” Choices: “4.05 / 4.10 / 4.15 / 4.20 / 4.25 mm”. Initial prompt: “Predict first. Then reveal the observation.”

**Visual and interaction 1:** five positions on a horizontal diameter ruler with a selectable native radio/button control. A conceptual rod/hole cross-section may change nominal clearance; label it “Nominal geometry, not a print simulation”. Selection changes the displayed nominal diametral clearance (`hole − 4.00 mm`) and a “Reveal measured fit” button reveals the full qualitative result strip. Exact results: 4.05 “Very tight”; 4.10 “Tight”; 4.15 “Best sliding fit; slight friction”; 4.20 “Looser”; 4.25 “Loose; wobble”. Selected choice stays visible. Reset hides results. All answers revealed in print.

**Speaker notes (3 minutes including interaction):** Ask the audience to predict before revealing. Nominal diametral clearance is easy arithmetic: 4.15 minus 4.00 gives 0.15 mm. It is not a measurement of the printed hole and it is not radial clearance. Reveal the actual coupon observations. The source describes 4.15 mm as the best sliding fit with slight friction in this test. It does not establish a universal PETG hole rule. The role matters: a sliding fit is different from a permanent cap or a retaining interface. This small test separated a physical unknown from the rest of the mechanism and turned a vague fit preference into a usable reference.

**Sources:** S01 lines 5–15. **Job:** let the audience experience prediction, observation and bounded inference.

### 07 — Fix the source of the mismatch

**Audience copy:** “Observed: incomplete or floating first layers.” / “Response: source-defined lands and bed orientations.”

**Visual:** conceptual cross-section of a plate above a bed versus a plate seated on a bed; deliberately exaggerated gap, explicitly “Schematic; not to scale”. A single arrow returns from preview to parametric source. No fabricated slicer screenshot.

**Speaker notes (1.5 minutes):** The early P13 3MF preview showed large plate faces above the bed and incomplete or floating first layers. The experience log records a source repair: different thrust lands, an adjusted face gap, shaft clearance and source-authored bed orientations. The response preserved the desired manufacturing relationship in the parametric source rather than relying on a manual adjustment that the next export could lose. This is an example of an artifact or preparation observation changing source. It is not a claim that every later physical issue was solved. A preview exposes a different category of failure from a solid-model check.

**Sources:** S01 lines 24–29. **Job:** show where a correction belongs.

### 08 — Tests can repeat the same mistake

**Audience copy:** “Source assumption = test assumption” / “Both agreed. The required 90° bend was still wrong.”

**Visual:** giant equals sign between “source” and “test”; below, a rust right-angle outline alongside a diagonal outline labelled “inherited assumption”. These are conceptual topology marks, not exact CAD. Optional A02 only as a small labelled reference; A01 alone is sufficient if layout becomes busy.

**Speaker notes (2 minutes):** The P20 R2 handoff documents a specific escape: the P19 workpiece-reference builder and its tests encoded the same END-derived diagonal-wire assumption. Local agreement masked a contradiction with the fixed 90-degree requirement. That tells us why independence is about where an expectation comes from, not merely running the same logic twice. The handoff proposed a wire-only correction and a regression against the requirements. This slide reports the defect and the planned response in that record; it does not claim the correction was already completed there. Ask what independent observation or requirement could have broken that shared assumption earlier.

**Sources:** S02 lines 64–87. **Job:** expose a shared-assumption failure.

### 09 — Make intent visible before detail

**Audience copy:** “What stays fixed?” / “What moves?” / “What must remain true?” / small line: “A small 2D check can expose a large misunderstanding.”

**Visual:** simple conceptual fixed point and moving point with restrained arrows; no claims about XT60 exact path. Side note: “Intent check → geometry checks → physical checks”.

**Speaker notes (2 minutes):** The user rejected a P17 simulator despite passing deterministic tests because its visible motion did not match the intended behavior. Later the user approved a compact 2D gate and requested P18. The lesson is not that a drawing replaces engineering. A small view can let the human correct fixed/moving identity and topology while the cost of change is low. P18 then passed extensive digital checks, but the record kept real force, friction, backlash, heat and retention open. Intent, geometry and physical evidence each answer a different question. Explain one relationship, ask for a concrete observation, and preserve the answer as a requirement.

**Sources:** S01 lines 69–76 and 262–281. **Job:** show how the process evolved.

### 10 — Kage makes composition unavoidable

**Audience copy:** “A shadow-clock concept needs motion, guidance, light and service access to work together.”

**Visual:** large conceptual system drawing: three concentric rings marked H/M/S, one guide station, one motor/gear station, a light path and a wall/shadow plane. Clearly caption “Conceptual system diagram • not an accepted CAD layout”. Geometry is illustrative, not dimensioned; do not suggest exact optical behavior or an accepted arrangement.

**Speaker notes (2 minutes):** Kage is a roughly 300 mm wall-mounted kinetic shadow-clock concept. It is a richer composition problem: moving rings need guidance and drive, optical behavior needs suitable light and geometry, and the assembled object needs practical access. The drawing only explains the categories of responsibility; it is not a reconstruction of an accepted mechanism. The migrated repository preserves reference ideas and a restart authority, but it does not establish a physically accepted restart. That distinction becomes important when we look at what a green test result once left outside its scope.

**Sources:** S04, S03. **Job:** introduce Kage’s coupled system.

### 11 — Eleven passing tests missed real overlap

**Audience copy:** “11/11 reported” / “Critical physical pairs were omitted.” / three short labels: “Spool ↔ spool: ~37.107 mm³”; “Spool ↔ boss: ~22.766 mm³”; “Shaft ↔ hub: ~33.301 mm³”.

**Visual:** huge 11/11 crossed by a thin rust rule; three measured text lines alongside a conceptual overlapping-solids sketch. Label “Later actual-solid inspection • rejected Half-Z experiment”. Do not render fictional measured CAD solids.

**Speaker notes (2 minutes):** The Kage restart document rejects the Half-Z namespace. Its reported 11 out of 11 result omitted critical physical pairs. Later actual-solid inspection found overlaps, including approximately 37.107 cubic millimetres between adjacent spools, 22.766 between an hour spool and a chassis boss, and 33.301 between a shaft and a hub without the required bore. These are geometric overlap volumes, not physical measurements from a print. Missing service provisions were also documented. More tests are not automatically more coverage: the question is whether the credible failure and the actual objects were in scope. An omitted interface cannot fail a test that never examines it.

**Sources:** S03 lines 121–152. **Job:** connect coverage to real failure modes.

### 12 — Prove one interface before multiplying it

**Audience copy:** “Seam coupon → one guide + ring coupon → one motor station → compose” / small qualifier: “Proposed Kage restart sequence”.

**Visual:** four stations along one continuous line, each with a simple conceptual silhouette; a physical-evidence gate between stations. No checkmarks or completed-state colour.

**Speaker notes (2 minutes):** The restart plan proposed bottom-up gates. First test a seam, then one guidance station and a ring coupon, then one motor and gear-mesh station. Only after those physical gates should the proven interfaces be applied across the three-ring mechanism. Light and thermal behavior also get separate experiments before packaging. This is a proposed sequence from the restart document, not a report that those experiments passed. The value of decomposition is causal clarity. If a single guide binds, there are fewer plausible causes than when a complete assembly binds. Composition comes after interface evidence, and it still needs its own system checks.

**Sources:** S03 lines 408–474. **Job:** show risk-driven decomposition.

### 13 — Give the gap a name

**Audience copy:** “Intent → geometry → artifact → process → physical behavior” / “Which layer could explain this observation?”

**Visual:** five words along a diagonal path; one rust “?” marker moves only on user click if desired. Below, three grounded examples: “Wrong bend → intent”; “Floating layer → artifact/process”; “Tight rod → physical fit”.

**Speaker notes (1.5 minutes):** This is a synthesis of the examples, not a universal diagnostic taxonomy. A wrong bend can be a requirement or topology misunderstanding even when geometry is valid. A floating first layer can come from how geometry is exported and oriented for manufacture. A tight rod can reveal a process-dependent fit. Naming the layer helps choose a test and the place to make the correction. More than one layer can be involved, so a classification is a hypothesis rather than a verdict. Before asking an agent to redesign everything, ask what observation would distinguish the two most plausible causes.

**Sources:** S01, S02, S03; presenter synthesis. **Job:** convert stories into a diagnostic method.

### 14 — Each phase earns a different claim

**Audience copy:** “Define intent → model → prepare → operate → evaluate” / under each: “Requirement / geometry / job / observed print / accepted outcome”.

**Visual:** broad horizontal flow with distinct boundaries and a long return arrow from evaluate to define. No checkmarks suggesting completed capability.

**Speaker notes (1.5 minutes):** Decomposition also applies to the workflow. Model work asks whether the source and geometry represent intent. Preparation asks whether the exact model, material, machine and process produce an inspected job. Operations asks what the printer actually did under authorized control. Physical evaluation asks whether the result meets the intended use. Each phase should hand over an identified artifact or observation and a clear statement of what is still unknown. This is the intended lifecycle; the integrated product does not yet claim every stage. The next historical pilot shows why the boundaries matter even in a single print.

**Sources:** S05, S07. **Job:** bridge CAD learning to agent workflow architecture.

### 15 — A successful command can make the wrong job

**Audience copy:** “Requested: physical extruder 3 → T2” / “Early profile resolution: T0” / “Inspect the artifact’s meaning.”

**Visual:** large `3 → T2` and a rust `T0` branch that ends before the print boundary. Tiny caption: “Snapmaker Orca 2.3.5 • U1 pilot • 23 Aug 2026”.

**Speaker notes (2 minutes):** In the recorded PETG pilot, physical extruder 3 maps to logical G-code tool T2. Incomplete inherited filament profiles resolved only one physical extruder and emitted or selected T0 despite the requested assignment. Complete resolved profiles restored the required tool output. The point is semantic validation: a successful process exit would not make the wrong-tool artifact acceptable. The pilot eventually sliced and printed the requested parts under user authorization, but assembly exposed fit and mechanism failures. It also lacked a complete product provenance manifest. Treat the profile findings as one-environment pilot evidence that needs reproduction, not a universally reliable automation recipe.

**Sources:** S06 lines 89–102 and 112–168. **Job:** supply concrete slicer struggle and response.

### 16 — Compose preparation and operations through evidence

**Audience copy:** “Orca Preparation” / “identified model + explicit profiles → inspected job” / “Printer Operations” / “observed job → persistent print session” / joining label: “Versioned handoff”.

**Visual:** two equal-width peer regions connected by one narrow bridge carrying “artifact identity · configuration · checks”. Above both, one simple line labelled “Agent maintains continuity”. Footer: “Target architecture; not a current end-to-end capability claim”.

**Speaker notes (2 minutes):** The product direction keeps Preparation and Printer Operations as peer subsystems. OrcaSlicer is an adapter within Preparation; printer, camera and notification integrations belong inside Operations. Their handoff preserves the prepared job’s identity and evidence when the job becomes an observed printer session. One subsystem is not a wrapper around the other. The agent coordinates across them while maintaining the separate meanings of prepared, uploaded, started and observed. This architecture is a response to the same problem we saw in CAD: if different claims collapse into one green status, a missing interface becomes easy to overlook.

**Sources:** S05 lines 124–143, S07. **Job:** make subsystem responsibilities legible.

### 17 — What does “complete” prove?

**Audience copy:** “The printer reports completion. What can we claim?” / choices: “A. A completion report exists”; “B. The dimensions and fit passed”; “C. The intended mechanism works”.

**Visual and interaction 2:** choose A/B/C, then reveal. All choices remain visible as plain text controls. Correct feedback: “A. Completion is an operational observation. Physical acceptance needs inspection and tests.” Then expand a single evidence ladder: “Inspected G-code → upload → acknowledged start → observed printing → reported completion → physical evaluation”. Beside the last stage: “Pilot: parts obtained; mechanism not accepted.” Use distinct text labels for Preparation, Operations and User + agent evaluation; no colour-only semantics. Reset supported; print includes answer and ladder.

**Speaker notes (3 minutes including interaction):** Let participants commit before revealing. Completion reports tell us something real about the printer session; they cannot establish dimensional fit or mechanism function. The pilot reported all 22 layers and no printer errors, and the user later handled the parts. Yet the mechanism was not accepted. Ask which evidence belongs to Preparation, which belongs to Operations, and which requires physical observation. The agent should carry the same job identity through these boundaries, and carry uncertainty too. This exercise is about evidence ownership, not being pessimistic about automation. Better state distinctions let useful automation advance without inventing later success.

**Sources:** S06 lines 139–157, S05 lines 145–171. **Job:** audience practices boundaries and ownership.

### 18 — The agent owns continuity

**Audience copy:** “Manager: keep the next step clear.” / “Teacher: explain the tradeoff.” / “Engineer / operator: execute and verify authorized work.” / “The user retains consequential authority.”

**Visual:** three parallel typographic lines under one continuous loop. Footer: “Long-term product direction”. Do not use persona avatars or imply three deployed agents.

**Speaker notes (2 minutes):** The intended relationship changes who carries the process. The user supplies intent and constraints. The agent maintains the plan, remembers the current evidence, follows through and proposes recovery. It also teaches the relevant concept when that helps the user make a meaningful choice. These are roles within one relationship, not a claim that three independent runtime agents are deployed. Workflow responsibility does not confer blanket authority. The user still controls consequential decisions and can pause or stop. This is the accepted direction in the product documents, not a statement that the current integrated product already performs it all.

**Sources:** S05, S07. **Job:** explain the intended agent-managed relationship.

### 19 — Ask the human for one useful observation

**Audience copy:** “Purpose → action → observation → stop condition → evidence” / example: “Try the sliding fit. Describe friction and wobble. Stop if force is needed.”

**Visual:** one large observation prompt, with five small aligned annotations underneath. Label example “Illustrative future task, based on the coupon lesson”.

**Speaker notes (1.5 minutes):** A physical task is more useful when the user knows what uncertainty it resolves. The coupon example becomes a bounded request: identify the specimen and rod, try the intended motion, report friction and wobble, stop instead of forcing a questionable fit, and return the labelled result. This is an illustrative prompt, not a new experiment performed for this talk. The user becomes an active validator and learner without having to resume managing every step. The returned observation must remain separate from the agent’s explanation of it. A photograph can show a failure; it does not by itself specify the right redesign.

**Sources:** S01 lines 5–15, S05, S07. **Job:** connect human feedback and teaching to workflow design.

### 20 — Give each agent a bounded job

**Audience copy:** “Orchestrator: scope + baseline” / “Implementer: one candidate” / “Independent validation + review: evidence” / “Same candidate. Clear ownership. Durable records.”

**Visual:** one left-to-right development flow: scope and frozen design → implementation → parallel “Critique” and “Validation” branches → “Formal review joins findings” → evidence and next action. Render formal review downstream of critique/validation, not as an approval by the implementer. A thin line under the whole flow reads “Exact candidate identity travels with every handoff”. Footer: “Development roles • distinct from product Manager / Teacher / Operator roles”.

**Speaker notes (1.5 minutes):** Repeated errors changed how the work is delegated, not just which tests run. The repository workflow makes the orchestrator responsible for defining the task, freezing its requirements and baseline, scheduling bounded owners, checking provenance and choosing the smallest correction. The implementer owns one candidate and does not approve it. Independent critique and validation inspect that same frozen candidate; formal review checks their findings, requirement coverage and resolutions. A hash identifies the exact inputs and artifacts being discussed, so a passing report cannot silently transfer to changed geometry. Each role returns evidence, limitations and a next action. Decisions and observations live in repository records so a new agent can resume. These development roles are separate from the product-facing roles on slide 18. This organization improves accountability; it does not guarantee independent assumptions or physical success by itself.

**Sources:** S09. **Job:** show how the actual development process responded to repeated mistakes.

### 21 — Let repeated evidence shape automation

**Audience copy:** “Observe → record → repeat → generalize → automate” / “A pilot is a starting point for learning.”

**Visual:** widening line with five named stages; below, small examples “fit reference / regression / profile guard”. No maturity scores or completed-state checks.

**Speaker notes (1.5 minutes):** Feedback has to survive the conversation. Record the exact artifact, settings, observation and limitation, then use that record to choose the next experiment. A measured fit reference may change a parameter; a topology failure may add a requirement-driven regression; a slicer failure may suggest a profile guard. But a one-off pilot does not automatically justify reusable automation. The pilot log explicitly calls for repeated non-user fixtures before promoting the path into product code. The direction is accumulated evidence toward dependable behavior, while keeping the boundary of each finding visible.

**Sources:** S06 lines 159–168, S01; presenter synthesis. **Job:** close the learning loop durably.

### 22 — Make the next uncertainty small enough to test

**Audience copy:** “What do you expect?” / “What would you observe?” / “What is the smallest test that could change your mind?”

**Visual:** charcoal canvas, giant closing statement, the opening loop now joined. Three questions beneath. Small footer: “Bring one example from your own work.”

**Speaker notes (2 minutes plus remaining discussion):** Return to the opening: a passing model, command or print is useful evidence with a specific scope. The next move is to identify the missing claim, understand the gap, and design a small experiment. Ask the audience to apply the three questions to a current project. A live end-to-end demo is future work; this presentation establishes the reasoning and evidence boundaries it should demonstrate. Close with discussion about where their workflow currently loses intent, observation or ownership. Do not promise a finished jig, Kage mechanism or fully integrated autonomous product.

**Sources:** synthesis of S01–S07. **Job:** resolve the opening with a usable action.

## Acceptance boundaries and implementation handoff

Requirements in `docs/REQUIREMENTS.md` are binding. Source register `docs/SOURCES.md` preserves exact evidence, hashes, boundaries and count methodology. `DESIGN_INPUTS.sha256` freezes this design, requirements, frozen brief extract and cited source files/assets. Changes to these invalidate affected implementation/review gates. Mutable orchestration/status and later validation reports are excluded.

Implementation may shorten notes or adjust layout without changing claim meaning; material copy, source or interaction changes return to D1. For responsive fit, preserve the one-point composition before adding more text. The page must be fully usable offline and keyboard accessible. The deck’s HTML acceptance has no effect on source-project CAD, slicer or physical acceptance.

## D2 — Bounded provenance, print and responsive implementation contract

Reopened after I1 exhausted its two focused repair cycles. Exact baseline: candidate manifest `8b200517637b42569e8e51e232a51679847bc5e2e6a8476158f400db70b62783`. Independent R1 repair-2 review and V1 repair-2 validation establish that the 22-slide desktop narrative and functional behaviors pass their completed checks, while three material defects remain. This contract changes implementation mechanisms only: preserve every slide, claim, interaction, source fact and feature. `docs/SOURCES.md` remains unchanged.

1. **Derive embedded S08 provenance from the frozen source register.** The builder must read the exact named Kage amendment/hash rows from `docs/SOURCES.md` and generate the standalone S08 article from those values. Do not maintain or patch a second handwritten digest list. Require all 11 distinct named rows and valid 64-character SHA-256 values; fail the build if the declared table cannot be parsed completely. The i3-7 digest must therefore come directly from the frozen register. The resulting HTML must contain every filename and matching digest. This changes how existing evidence is copied, not its meaning or scope.
2. **Separate printed page boxes from inner diagram styling.** The outer `.slide` section owns pagination, full-page dimensions and an explicit zero outer margin in print. Inner sequence/flow layout must use an exclusive component selector or an explicitly scoped descendant selector that cannot style a page section. Remove or override the existing collision where `.sequence` matches both slide 12 and its inner flow. Preserve screen appearance. A DOM-boundary check is insufficient: the written landscape PDF must contain exactly 22 complete pages, one per slide, with no orphan/blank page after slide 12 and with existing revealed answers/captions retained.
3. **Make mobile Kage rules authoritative after desktop rules.** Place the relevant narrow-viewport width and caption-flow overrides after the desktop component declarations, or use equally explicit bounded selectors whose priority is unambiguous. At 390 × 844, the Kage diagram uses the available content width rather than inheriting `48vw`; H/M/S, guide, motor, light/shadow context and the conceptual/not-accepted caption remain distinct and readable. Keep the caption in normal layout flow with reserved space above the source footer and toolbar. Preserve the accepted desktop composition at 1280 × 800.

I2 owns builder/CSS and generated HTML changes, then issues a new candidate manifest. Focused author checks must compare all 11 embedded S08 rows with the frozen register. Independent V1 verifies the actual written PDF page count and relevant print pages plus the mobile/desktop Kage render; independent R1 verifies the source-row agreement and visual findings against that same candidate. Existing desktop/functional evidence remains historical and must not be relabelled as evidence for changed bytes. Limit follow-up to affected gates and the already-prescribed core smoke check; no narrative, style-system or feature expansion. Root retains continuity/status updates.
