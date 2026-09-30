# Initial audience reading

## Scope and limit

I read the rendered images only, in order: `/tmp/cad-story-refinement-baseline/slides/slide-1.png` through `/tmp/cad-story-refinement-baseline/slides/slide-13.png`. I did not read speaker notes, sources, the brief, project records, or source files. This is therefore a first-viewer account of what the visible slides communicate, not a factual audit of the examples.

## Main argument, in plain language

The presentation argues that when people use agents and digital tools to make things, they should build a feedback loop from the beginning: agree on success, do a bounded action, observe the real result, and use that evidence together to decide whether to continue, change, or stop. Passing model checks, file checks, or a completed printer job alone does not prove that a physical design works. The cases make the point concrete with a wire-bending jig, a shadow clock, and a 3D-print pilot.

## Cases as understood

| Case | Object/task | Observation | Next decision | Why it is included |
| --- | --- | --- | --- | --- |
| Rod guide | A 4.00 mm metal forming rod sliding through a printed guide for an XT60 wire-bending jig. | A 4.05 mm CAD hole was very tight; the table says 4.15 mm gave the best sliding with slight friction. | Use 4.15 mm as the sliding-fit reference, while checking it again in the real guide. | It shows a small physical test changing a named design reference, with limits on what that result proves. |
| Center shaft | A printed center shaft passing through holes in two plates in the same jig. | A person reported the shaft was too thick for the center hole, despite digital checks passing. | Agents identify only the shaft and matching holes, enlarge those holes, regenerate/check the files, then reprint and test by hand. | It shows a human observation being turned into a narrow agent task and a physical follow-up. |
| Wire path | The jig’s required fixed 90-degree wire bend. | CAD and tests both copied a diagonal reference instead of the required horizontal-leg, 90-degree path. | Return the new check to the original requirement; the slide says a wire-only correction was proposed but not completed. | It shows that multiple agreeing checks can still share the same bad premise. |
| Kage clock | A kinetic shadow-clock concept with a shaft and gear. | A shaft crossed solid gear material; original checks omitted that relationship. | Restart from small joints, one moving ring, and one drive before combining the clock. | It broadens the lesson from a single fit to relationships between assembled/moving parts. |
| PETG print pilot | Two PETG parts requested on printer head 3. | The first file selected head 1 because profiles were incomplete; later, the printer reported 22/22 layers and no errors, but a person’s assembly check did not accept the parts. | Complete profiles produced a corrected pre-print file; afterward, repeat preparation checks with test fixtures before making automation reusable. | It separates requested setup, generated-file checking, machine completion, and physical acceptance. |
| Future tool loop | A future arm making a small insertion, observed by camera and force sensor. | No measured result is shown; the slide explicitly calls it illustrative and does not claim successful robotic insertion. | People interpret whether to continue, adjust, or stop based on camera/force observations. | It extends the same return-path idea to possible future automation without presenting it as demonstrated. |

## Terms, transitions, and visual relationships I cannot explain without guessing

* `P13 R2 repair`, `T2`, `T0`, `U1`, and the footer links such as `S01`/`S13` are unexplained acronyms or references in the visible deck. I can infer that T-values are G-code/tool selections, but not their exact meaning.
* “Complete profiles” is presented as what restored head 3, but the visible slides do not say which profile fields were missing or how the correction was verified beyond the recorded file check.
* The connection between the XT60 jig cases and the Kage clock is thematic (checking physical/part relationships); no common design system is stated.
* The arrowed return paths communicate iteration. I cannot tell whether the arrows specify a formal workflow, a required sequence for every task, or a recommended mental model.
* I cannot identify the exact fit and mechanism failures in the final print pilot; slide 10 explicitly withholds them, and says the center-shaft case is separate.

## What I would do afterward

As a listener, I would apply the visible planning pattern to a pending tool-assisted task: state the success condition, choose the observation that would test it, state what result changes the plan, preserve that result with the exact design/file, then make the continue/adjust/stop decision with the people involved. For a physical build, I would treat a passing digital or printer status check as one piece of evidence and still perform the stated real-world check.
