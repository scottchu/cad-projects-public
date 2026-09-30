# Presenter guide — My 3D Printing Journey With AI Agents

20 main slides; planned 24.5 minutes including the 90-second Laifen demonstration, followed by discussion. Start with downloaded prints and the wish to make personal ideas; let project difficulties introduce the methods. Arrow/Space/Page keys navigate; N notes, S evidence, O overview, Escape close. The HTML embeds images, Three.js and the demo for offline use.

## Slide-by-slide pacing

### 1. My 3D Printing Journey With AI Agents — 0.5 min

Introduce the two things I wanted to make: a wire-bending jig and a toothbrush travel case. Explain that this is a journey through attempts, evidence and changing decisions.

### 2. I started with downloaded models — 1 min

Start at the beginning: buying the printer, downloading models and printing them. Explain the shift from choosing an existing design to wanting a personal solution.

### 3. My own ideas came with a stack of skills — 1 min

Trace the vertical stack between an idea and an object. Explain that the barrier was learning how these decisions fit together, rather than just finding a button in one application.

### 4. The agent was an assistant and a teacher — 1 min

Explain both roles in ordinary language. The agent could help produce work and make its reasoning understandable. Lead into the jig as a real project where these roles were tested.

### 5. A jig for bending two wires — 1.5 min

Point out the XT60 connector, the two wires and the grey forming rods. Trace the intended 90-degree bend, then point to the plates and grooves that guide movement.

### 6. The design kept changing — 1.5 min

Walk across the six historical CAD images. Use the folder count to convey the amount of recorded design work, then move to the physical observations that made revisions necessary.

### 7. The real jig changed the problem — 1.5 min

Name the three changes in the problem: room, fit and holding. Explain how releasing my hand revealed a different requirement from merely reaching a plausible pose.

### 8. I kept asking for another rail route — 1 min

Describe relying on AI to deliver the imagined mechanism. Explain that seeing relationships in simulation changed how I could reason with the agent. The exact original customizer is missing; the next slide uses other recovered studies.

### 9. Different studies answered different questions — 1.5 min

Compare the questions, not competing accepted designs. The earlier study prescribes paths for the rods. P25 keeps rod centers fixed while fixture poses show contact and release. Identify its rear cradle supporting Blue and Green and its front pad holding Orange. These are separate historical hypotheses; neither is the missing original rail customizer or a force solver.

### 10. The fit test became knowledge we could reuse — 1.5 min

Identify the rod, guide and clearance in the cutaway. Follow the observed tight-to-wobbly progression. Explain how the 4.15 mm result was recorded with its material, nozzle and rod context, making it available for later decisions without claiming universal fit.

### 11. We prepared a print around one question — 1 min

Point to the thin web between curved slots. Explain how a smaller experiment can retain the actual uncertainty. This record contains prepared toolpaths and slicer estimates; the physical survival result remains pending.

### 12. I learned to choose the smallest useful test — 1.5 min

Compare the question each evidence type can answer. Emphasize that the cheapest useful experiment is the one that can change the decision, rather than always the smallest or fastest test.

### 13. Tools reduced the work between decisions — 1.5 min

Explain how guided Snapmaker Orca CLI workflows carried preparation and authorized printing, while U1 Print Studio MCP supplied read-only observation. These tool connections reduced execution friction; they did not remove the need to choose and interpret the experiment.

### 14. A finished print still needed me — 1 min

Use the single PETG pilot to separate printing from acceptance. Two cam-plate parts printed, but assembly exposed fit and mechanism-design failures. Read the human-loop sentence and explain what I still need to judge.

### 15. The projects and the working system grew together — 1.5 min

Use the two loops as the payoff of co-evolution. Point back to the saved fit reference, the separate studies and the guided tools. Explain that project pressure supplied the reason for each improvement; this is not a dated claim that every capability appeared in this order.

### 16. Laifen: a case for my electric toothbrush — 1 min

Introduce Laifen as the current example of this way of working. Show the earlier physical thread specimens and their hand-fit feedback, then distinguish the separately reviewed full-size R6 CAD. The physical specimens informed preference, not proof of R6 loaded fit.

### 17. Extra length does not hold the brush in place — 2 min

Connect this to XT60: inspect one relationship before more execution. Compare the two outlined cavities, then open the earlier study and follow the 90-second demonstration below. Ask what evidence would settle whether bottom support is acceptable, without turning the slide into an audience exercise.

### 18. Now we can name what remains to learn — 1 min

Move beyond the clearance observation to the actual acceptance decision. Separate earlier closure feedback, nominal model evidence and the still-needed full-size loaded-case observations. Explain what a useful result would let us decide.

### 19. The same habit can guide other work — 1 min

Compare the same uncertainty, experiment and decision pattern across software and physical work. Keep the software fixture explicitly illustrative and sensor or arm examples future-facing. Leave the full architecture to the next slide.

### 20. Keep human judgment in the feedback loop — 1 min

Return to the shared model at the center. Connect human intent and acceptance, agent reasoning and continuity, digital evidence and physical observations. Close by choosing what to learn next and designing feedback from day one.

## Laifen 90-second runbook

- 0–15 s: introduce the travel case for a Laifen electric toothbrush. Earlier physical thread specimens fitted by hand; reviewed R6 CAD is a separate full-size design, with physical loaded fit still pending.
- 15–30 s: open “Open the clearance study” on slide17. Explain this is an earlier nominal-envelope browser study, not controls for R6 CAD. Keep L208, D29 and total allowance5. The shape/joint details predate R6.
- 30–50 s: click 置中 (centered; q0.5). Point to top/bottom2.5mm and the unrestrained illustrative-position label. Scroll inside the study frame to show the lower section drawing; scroll back up to reach the q buttons.
- 50–65 s: click 靠底 (resting on bottom; q0). Show bottom0/top5. This is a prescribed position, not gravity/contact simulation.
- 65–80 s: return to the actual R6 section alongside. Extra cavity length does not create a restraint.
- 80–90 s: name the decision: whether bottom support is acceptable; verify installed brush envelope and eventual full-size loaded closure/contact. The user chose full-size progression; do not prescribe another compulsory coupon. Close returns to slide17.

Reset centered reloads the exact fragment. “Show fallback” displays the two rehearsed state screenshots plus actual R6 section. Use fallback immediately if browser controls cannot be shown; no server, CAD regeneration, external host integration or printer action is required. The iframe has allow-scripts only, no same-origin/host submission capability.

## Evidence and delivery limits

The original P20 customizer is missing. Later P25 screenshots are real recovered study states, not that original screen and not physical proof. XT60 counts are recorded folders, not prints. Coupon dimensions are contextual observations. U1 UI image is a synthetic fixture; guided Snapmaker Orca CLI demonstrations are distinct from the read-only U1 Print Studio MCP application. The PETG pilot contained two cam-plate parts; its private project identity is not inferred. Current Live reliability was unresolved at the audited snapshot. The prepared web coupon has no physical result.

The standalone HTML is index.html. Validator produces releases/journey-walkthrough.pdf from the frozen candidate; this guide does not claim it already exists. The previous delivered HTML/PDF remain preserved as releases/journey-feedback.html and releases/journey-feedback.pdf. The new PDF cannot reproduce browser controls and uses the static fit cutaway and Laifen section.
