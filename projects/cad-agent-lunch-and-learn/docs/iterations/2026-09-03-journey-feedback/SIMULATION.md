# J-S actual interactive XT60 evidence

Status: complete with original-artifact gap. Owner `/root/journey_simulation`, 2026-09-03. Read-only canonical sources; source fingerprint is `SIMULATION.sha256` (SHA-256 path/content list). Genuine later interactive studies recovered and exercised; exact historical P20 customizer remains unavailable. No source CAD, device, Git or dependencies changed.

## Recommended usable artifact

Canonical `/Users/scottchu/Projects/personal/design-projects/projects/xt60-bend-jig/work/p25-rear-loop-front-pusher-intent-preview.html` is a preserved, runnable interactive SVG concept page, dated by filesystem Aug30 (not claimed creation date). Its inner authored source is sibling `p25-rear-loop-front-pusher-intent.html`. Both currently exist but are not Git tracked; `git log --all` on matching HTML names returned no history. Identify it on slides as **“Later XT60 interactive study — contact and release sequence”**. Do not claim this was the exact first breakthrough screen.

Actual controls, exercised locally:

- `#p25-position`: three-finger positioning; manual arrows visible, front assembly rotated open and translucent.
- `#p25-clamped`: front assembly closes; rear U-frame supports Blue+Green, front pad holds Orange; hand arrows fade. Left hinge and right latch labelled.
- `#p25-released`: front assembly rotates open and rear frame translates down; contact is visually released.

All three buttons update `aria-pressed`, visible subtitle and SVG transforms/opacity. The text explicitly asks whether this contact topology is correct and labels the page “意圖確認圖・尚非列印 CAD”. It is suitable evidence of a small feedback interface that makes intent visible and actionable. Rod centers stay fixed between these three states; these buttons animate prescribed fixture poses. There is no contact solver, force computation, deformation, friction, retention-strength, clearance or fit proof. In particular the words “鬆開彈離” do not establish measured spring action.

Genuine browser screenshots, 1440×1050:

- `/tmp/cad-journey-simulation/p25-position.png`
- `/tmp/cad-journey-simulation/p25-clamped.png` — visually inspected; best single slide image, all controls and labels visible.
- `/tmp/cad-journey-simulation/p25-released.png`

Use 2–3 states or live buttons to show positioning→hold→release; speaker explains the question: which member contacts which rod, and when? Observing agreement closes an intent gap; it does not close physical acceptance. Copy the exact archived preview into presentation-local demo assets if needed; keep the revision/status caption.

## Second actual interface, narrower and potentially contradictory

Canonical `.../work/three-rod-force-gate-preview.html`, inner source `three-rod-force-gate.html`, shows three rods following fixed straight inner-rail lines. Slider `#xt60-force-progress` spans 0–100, integer step1; all three rod centers linearly interpolate. Blue and Green are labelled “pull”, Orange “push”; an independent passive lock fades in during final16% and is fully shown at100%. Tested0/50/100% with coordinates captured in `receipt.json`; mid is Blue(313,130), Orange(313,215), Green(313,300), in SVG coordinates, not mm.

Screenshots `/tmp/cad-journey-simulation/force-{open,mid,locked}.png`; mid visually inspected. PASS/FAIL buttons can call `window.openai.sendFollowUpMessage` only in a compatible host. They were not clicked and no acceptance/message was emitted. Standalone browser has no host integration, so these feedback buttons do not record a decision. Do not present them as a persistent working form.

This force diagram and later P25 wording differ: earlier labels describe outer-rod pulling, while P25 says Blue/Green pushed from rear to front. That is valuable evidence of evolving interpretation but must not be merged into one accepted motion contract. Prefer P25 in the main deck; earlier force page only as a clearly labelled historical alternative, if needed.

## Exact historical customizer gap

Renewed filename search covered scoped visualization directories and current design-projects worktrees, including hidden files, plus Git all-refs history for rail/customizer/P25 HTML names. It found generic `index.html` copies and the canonical work files above, but no `inner-outer-rails-3d.html`. Generic index is the older simulator excluded by prior audit. No broad personal-session content scan was used.

Primary P20R4 `docs/iterations/p20-r4-custom-profile-full-cad/BRIEF.md:12–32,45–77,96–109` records the exact customizer pointer and hash `1f7cae7260871f2ba54e663ebf24aaa01a5bdef69e5c0a40e6524736846558cc`, accepted `GREEN 0 / BLUE→GREEN` profile, fixed inner plates/axle, outer rotations ±45u°, inverse-frame rail paths and prescribed OPEN/MID/END states. That written contract is direct evidence of customizer-informed design; missing HTML means its original UI/controls/pixels cannot be reverified. Rebuilding that scene would be reconstruction, not recovery. Later P25 and force-gate pages are not its substitutes in chronology.

## Capture and command receipt

Searches used `/opt/homebrew/bin/rg` explicitly, scoped to visualization/worktree HTML filenames and canonical XT60 docs. Read source scripts before execution. Ran `git -C /Users/scottchu/Projects/personal/design-projects log --all --oneline -- '*/inner-outer-rails*' '*custom*html' '*p25*html'` and `git ls-files` for exact files; no tracked history returned. `sed`, `cat`, `ls` only read canonical content.

Browser helper `/tmp/cad-agent-visual-validation/cdp.mjs` was inspected; capture script `/tmp/cad-journey-simulation/capture.mjs` launches isolated headless Chrome with HTTP(S) resources blocked. Initial iframe-context access failed because sandboxed srcdoc was out of process. Final successful capture reads the existing preview's srcdoc string and loads those exact inner-document bytes as the top-level document using CDP `Page.setDocumentContent`; it does not change authored source/content/styles. Thus screenshots are genuine inner UI rendering, omitting only outer iframe padding, with controls exercised. Embedded external optional icon/tooltip helpers were blocked; diagrams and interactions rendered using original inline source. DOM state receipts are `/tmp/cad-journey-simulation/receipt.json`. Command: `/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node /tmp/cad-journey-simulation/capture.mjs`, exit0. All six captures made; P25-clamped and force-mid pixel-inspected.

Coverage: actual artifact identity, controls and observations, three genuine states, authored constraints, preserved-vs-original boundary, no physical-success claim. Remaining risk: neither work page has Git provenance or physical acceptance; do not invent exact creation order beyond filenames/content/history evidence. Next: writer copies exact P25 asset and selected captures with caption; validator checks archived identity and demo behavior in final offline package.
