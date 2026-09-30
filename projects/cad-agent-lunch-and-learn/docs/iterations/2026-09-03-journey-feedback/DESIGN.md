# J-D/I design contract — journey feedback

Status: implemented initial candidate after root-routed independent design critique. Inputs: BRIEF/INPUTS, four completed audits and their manifests, and the root-verified 99 immutable snapshots in /tmp/cad-journey-evidence/map.json. Prior 16-slide candidate is recoverable at /tmp/cad-journey-feedback-baseline. Latest user brief supersedes preservation-only scope.

Communication job: by the end, curious colleagues should understand how a tinkerer works with agents to turn physical ideas into testable experiments, because shared evidence and human judgment matter more than the number of generated versions.

## Selected sequence and coverage

20 main slides; about 25 minutes including a 90-second Laifen demonstration, then discussion. Plain concrete titles; first-person where the user authorized personal motivation/recollection. No invented quotes, emotions, successful prints, counts, or exact original-screen identity.

| # | Working title / narrative job | Primary visual and evidence | Minutes |
|---|---|---|---|
| 1 | My 3D Printing Journey With AI Agents | Minimal title with actual XT60 cutaway and Laifen case silhouette; objects introduce the journey | .5 |
| 2 | I wanted to make physical things | Idea→object expertise barrier; CAD/materials/slicing/settings/transfer/monitoring drawn as intervening work. Skills remain valuable; I choose where to spend attention | 1 |
| 3 | A jig for bending two wires | H1 cutaway plus H3 exploded view. Explain two insulated wires held at90° during soldering/cooling; rods touch wires, grooves guide motion | 1.5 |
| 4 | The design kept changing | Six-image H1–H6 contact sheet, actual CAD labels. 25 recorded iteration folders, not prints. Three dated observations anchor the changes | 1.5 |
| 5 | The real jig changed the problem | H6 axial view + H8 operation. Actual width/too-tight caps/release springs open observations; distinguish CAD visuals from recorded physical feedback | 1.5 |
| 6 | I kept asking for another rail route | Authentic user recollection; explicitly illustrative full-print loop, not a claim that each historical revision was printed | 1 |
| 7 | Simulation made the relationships visible | Person and agent visibly point to the same actual later P25 clamped study; English cradle/pad explanation, not original breakthrough screen | 1.5 |
| 8 | We could inspect positioning, holding and release | Three genuine P25 state captures in sequence; digital intent evidence only, prescribed poses, not physics. Make the feedback interface before more CAD | 1 |
| 9 | A small print answered one fit question | Existing real read-only Three.js rod/guide cutaway + recorded OD4 PETG coupon outcomes. Modelhole4.15 was best sliding in this test, not universal tolerance | 1.5 |
|10 | Another small experiment isolated a fragile web | Actual H7 toolpath witness; preserve curved slots/web. Prepared-only, 6m12s /1.80g slicer estimates; physical result pending | 1 |
|11 | Different questions need different evidence | Relative hierarchy table: reasoning/calculation, simulation, CAD inspection, partial print, full print, real use. Question, relative cost/speed, what remains unknown | 1.5 |
|12 | The useful loop starts with a specific gap | Observed/desired→gap→hypothesis→evidence→smallest experiment. Separate digital branch into model evidence and physical branch into observations, join at human+agent interpretation | 1.5 |
|13 | A focused loop changes what we ask for | Explicit side-by-side expensive/lossy whole-product loop versus focused/shared question/evidence/decision loop | 1 |
|14 | The execution tools can sit beneath the agent | Demonstrated guided slice/check/authorized send/start/monitor, implemented read-only MCP observation, direction for broader automation. Actual UI synthetic fixture screenshot clearly captioned | 1.5 |
|15 | A finished print still needs a person | One documented PETG pilot printed two cam-plate parts; physical assembly exposed fit and mechanism failures. Human observes fit/use; exact prominent sentence “Agents can remove me from the toolchain without removing me from the loop.” | 1 |
|16 | Laifen: start with the parts I can hold | Actual earlier thread-specimen photo, hand-fit report; R6 layout as separately identified current CAD. Taste/fit/judgment still human; no R6 physical proof | 1.5 |
|17 | Extra length does not hold the brush in place | R6 section and simple bottom/center comparison; open the exact earlier q study in separate in-page overlay. 90-second demonstration: q.5→0, return to section, next acceptance decision | 2 |
|18 | The same approach works for software | Explicitly illustrative stale-reading experiment: uncertainty→small fixture→screen evidence→conditional next action | 1 |
|19 | I want to choose what to learn next | Concrete future load-sensor experiment during jig release; camera/arm as future complementary tools, no deployed integration claim | 1 |
|20 | Keep human judgment in the feedback loop | Final architecture: human intent/judgment + agent continuity; select experiments; distinct digital model evidence and physical tools/observations; update shared model. Personal close: choose fastest, cheapest, strongest useful feedback | 1 |

## Visual and artifact system

White/off-white canvas, charcoal text, restrained blue/orange/teal mechanism accents. Large plain titles, wide evidence images, flat diagrams/tables, varied compositions. No generic stock images, gradients, pill/card grids or scripted slogans. Native SVG for explanation; authentic images remain unchanged and visibly classified. P25 Chinese authored labels retained with adjacent concise English explanation. At least one primary visual on every slide.

Build stays root npm, no dependencies. Presentation-local assets copy exact selected snapshot bytes, with source→snapshot→asset hashes in a provenance JSON. HTML inlines all required images, Three.js and demo fragment. Read-only fit scene preserved; deterministic static fallback stays available in print/no-WebGL. Audience source/notes drawers support details without clutter.

Laifen lives in a modal/overlay within index.html, outside main slide inventory. Sandboxed srcdoc hosts the exact earlier measurement-gate fragment with only host styles; no openai host or submissions. Reset restores initial centered state. Fallback tab shows the two rehearsed captures plus actual R6 section; close returns to slide17. It cannot generate or mutate CAD, R6/R7 or printer state. Existing viewer is optional, not required. PDF remains a separate validator-produced release artifact; avoid circular HTML/PDF hashes.

## Gates and scope

Root-routed design critique completed and the corrections below were adopted before implementation. Initial candidate target10minutes/10k tokens; maximum2 focused repair cycles. Build/check; freeze requirements, brief/design, four audits, exact snapshots/provenance, source/tests/assets/generatedHTML in CANDIDATE.sha256; mutable status/validation records excluded. Validator checks20desktop/mobile/PDF slides, main show-and-tell/no quizzes, Three.js/fallback, offline demo q/reset/close/fallback and source boundaries. Critic/questioner independently check story; formal reviewer separate.

Exclusive writes: presentation build/source/simulator/assets/index, necessary test inventory, README/requirements/experience/decision/source register, PRESENTER_GUIDE, this DESIGN/IMPLEMENTATION/CANDIDATE. Parent owns continuity and PDF generation. No source-project, CAD, device, hosting, lock/dependency or Git edits.

## Adopted independent design corrections

Root authorized implementation after the quick critique. Slide18 replaces optional Kage with an explicitly illustrative software experiment: uncertain stale-state handling → small synthetic fixture → observed UI state → conditional next action. Slide13 directly compares expensive/lossy and focused/shared loops. Slide7 visibly connects person and agent to the same later P25 study. Slide6 full-print loop is illustrative, not a claim every rail iteration was printed. Slide19 uses a concrete future sensor experiment; slide20 retains the final architecture. No other scope expansion.

## Focused repair1 contract

Initial candidate HTML f79f24460dc7aff7cd80455cfb28f3acd93a5120020001379b8f9dc37502497e / manifest ce5303954c8b9db721204ec6ef202b65f32ded7cadcbe83924bc02d8d11f0fd0 preserved at /tmp/cad-journey-repair1-baseline. Root released the source gate after validation. Change only visible bodies3,14,15,17: define XT60; name guided Snapmaker Orca CLI versus read-only U1 Print Studio MCP without registry jargon; narrow acceptance to the documented two-cam-plate PETG pilot; draw identical cavity outlines around the two brush positions with exaggerated gaps. Convert presenter notes into speaking cues and add iframe scroll cue. Title source remains unchanged: validator isolated SwiftShader capture artifact and obtained a clean no-GPU image. No other slide body, geometry, source evidence or runtime changes.

Print repair within the same focused cycle: initial PDF pixels showed mobile stacking and clipped lower content. Both max-width responsive blocks are now explicitly screen-only, so print retains the desktop compositions. Desktop and mobile rules themselves are unchanged; only the media boundary changes. Scoped gap-pair SVG styling supports the new nominal end-contact drawing.
