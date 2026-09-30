import {readFile,writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {build} from 'esbuild';
const here=new URL('.',import.meta.url).pathname;
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const provenance=JSON.parse(await readFile(resolve(here,'assets/journey/provenance.json'),'utf8'));
const media={};for(const a of provenance){if(/\.(png|jpg)$/.test(a.local))media[a.id]=`data:image/${a.local.endsWith('.jpg')?'jpeg':'png'};base64,${(await readFile(resolve(here,a.local))).toString('base64')}`;}
const gate=await readFile(resolve(here,'assets/journey/Lgate.html'),'utf8');
const bundle=(await build({entryPoints:[resolve(here,'simulator.mjs')],bundle:true,format:'iife',write:false,minify:true,legalComments:'inline',target:'es2020'})).outputFiles[0].text.replaceAll('</script','<\\/script');
const fig=(id,caption,cls='')=>`<figure class="${cls}"><img data-asset="${id}" alt="${esc(caption)}"><figcaption>${caption}</figcaption></figure>`;
const split=(a,b,cls='')=>`<div class="split ${cls}">${a}${b}</div>`;
const path=(items,cls='')=>`<div class="path ${cls}">${items.map(t=>`<div>${t}</div>`).join('')}</div>`;
const table=(heads,rows,cls='')=>`<table class="${cls}"><thead><tr>${heads.map(h=>`<th>${h}</th>`).join('')}</tr></thead><tbody>${rows.map(r=>`<tr>${r.map((v,i)=>`<${i?'td':'th'}>${v}</${i?'td':'th'}>`).join('')}</tr>`).join('')}</tbody></table>`;
const note=t=>`<p class="note">${t}</p>`;
const fit=`<figure class="scene" data-scene="fit"><div class="scene-canvas"></div><svg class="scene-annotations" aria-hidden="true"><line data-leader="rod"/><text data-label="rod">Metal rod</text><line data-leader="guide"/><text data-label="guide">Printed guide</text></svg><div class="scene-fallback"><svg viewBox="0 0 500 280" role="img" aria-label="Cutaway of a metal rod inside a printed guide; clearance exaggerated"><path d="M 332 70 A100 100 0 1 0 332 210 L294 185 A55 55 0 1 1 294 95Z" fill="#14665f"/><circle cx="250" cy="140" r="43" fill="#af492d"/><path d="M100 224L230 167M380 40L306 91" stroke="#30363b"/><text x="20" y="247">Metal rod</text><text x="320" y="30">Printed guide</text></svg></div><figcaption>Read-only 3D cutaway · gap exaggerated ×8.<br>Teaching geometry; printed fit comes from the test.</figcaption><p class="scene-status" hidden>Static cutaway shown because WebGL is unavailable.</p></figure>`;
const slides=[
  [
    "title",
    "My 3D Printing Journey<br>With AI Agents",
    "<p class=\"subtitle\">Making physical things, and learning how to work together.</p><div class=\"title-images\"><figure class=\"\"><img data-asset=\"H1\" alt=\"XT60 wire-bending jig · CAD\"><figcaption>XT60 wire-bending jig · CAD</figcaption></figure><figure class=\"\"><img data-asset=\"Lclosed\" alt=\"Laifen toothbrush case · R6 CAD\"><figcaption>Laifen toothbrush case · R6 CAD</figcaption></figure></div>",
    ".5",
    "Introduce the two things I wanted to make: a wire-bending jig and a toothbrush travel case. Explain that this is a journey through attempts, evidence and changing decisions.",
    "HISTORY LAIFEN"
  ],
  [
    "",
    "I started with downloaded models",
    "<p class=\"large\">I bought a printer and started by printing other people’s designs.</p><div class=\"path horizontal\"><div>Buy a printer</div><div>Download a model</div><div>Print it</div><div>Want something of my own</div></div><p class=\"takeaway\">Then I wanted to solve <b>my own problems</b> and make <b>my own ideas</b>.</p><p>The printer made objects accessible. Designing those objects was the next step.</p>",
    "1",
    "Start at the beginning: buying the printer, downloading models and printing them. Explain the shift from choosing an existing design to wanting a personal solution.",
    "BRIEF"
  ],
  [
    "skills-slide",
    "My own ideas came with a stack of skills",
    "<div class=\"barrier\"><div class=\"endpoint\">An idea<br><strong>in my head</strong></div><div class=\"toolchain\"><span>CAD</span><span>Materials</span><span>Orientation & supports</span><span>Slicing & settings</span><span>Transfer & printing</span><span>Monitoring</span></div><div class=\"endpoint\">An object<br><strong>I can use</strong></div></div><p class=\"takeaway\">Making my own design meant climbing this stack.</p><p>I needed help with the work—and help understanding it. The skills still mattered.</p>",
    "1",
    "Trace the vertical stack between an idea and an object. Explain that the barrier was learning how these decisions fit together, rather than just finding a button in one application.",
    "BRIEF"
  ],
  [
    "",
    "The agent was an assistant and a teacher",
    "<div class=\"split \"><div><h2>Assistant</h2><div class=\"path \"><div>Help create a model</div><div>Inspect and revise it</div><div>Carry the tool work</div></div></div><div><h2>Teacher</h2><div class=\"path \"><div>Explain what moves and what stays fixed</div><div>Make tradeoffs understandable</div><div>Explain what a test could tell us</div></div></div></div><div class=\"join\">One shared idea, explained and worked on together.</div><p class=\"takeaway\">My part: define what I want, question the model and judge the result.</p>",
    "1",
    "Explain both roles in ordinary language. The agent could help produce work and make its reasoning understandable. Lead into the jig as a real project where these roles were tested.",
    "BRIEF"
  ],
  [
    "",
    "A jig for bending two wires",
    "<div class=\"split \"><figure class=\"\"><img data-asset=\"H1\" alt=\"P13 contact cutaway · gold wire reference, grey forming rods\"><figcaption>P13 contact cutaway · gold wire reference, grey forming rods</figcaption></figure><figure class=\"\"><img data-asset=\"H3\" alt=\"P18 exploded CAD · plates and grooves guide the rods\"><figcaption>P18 exploded CAD · plates and grooves guide the rods</figcaption></figure></div><p class=\"takeaway\">Hold two insulated wires in a <b>90° bend</b> while soldering and cooling.</p><p class=\"compact\">XT60 is the connector on the two wires. Rods shape them; rails—grooves in the plates—guide movement.</p>",
    "1.5",
    "Point out the XT60 connector, the two wires and the grey forming rods. Trace the intended 90-degree bend, then point to the plates and grooves that guide movement.",
    "HISTORY"
  ],
  [
    "history",
    "The design kept changing",
    "<div class=\"gallery six\"><figure class=\"\"><img data-asset=\"H1\" alt=\"P13 · wire contact · CAD\"><figcaption>P13 · wire contact · CAD</figcaption></figure><figure class=\"\"><img data-asset=\"H2\" alt=\"P13 · printable kit · CAD\"><figcaption>P13 · printable kit · CAD</figcaption></figure><figure class=\"\"><img data-asset=\"H3\" alt=\"P18 · plate arrangement · CAD\"><figcaption>P18 · plate arrangement · CAD</figcaption></figure><figure class=\"\"><img data-asset=\"H4\" alt=\"P19 · shorter rails · CAD\"><figcaption>P19 · shorter rails · CAD</figcaption></figure><figure class=\"\"><img data-asset=\"H5\" alt=\"P20 · revised curves · CAD\"><figcaption>P20 · revised curves · CAD</figcaption></figure><figure class=\"\"><img data-asset=\"H6\" alt=\"P20 · axial stack · CAD\"><figcaption>P20 · axial stack · CAD</figcaption></figure></div><p class=\"takeaway\"><b>25 recorded iteration folders</b> in the audited project snapshot.</p><p class=\"note\">Folders include refinements, experiments and migration work. This is not a count of prints.</p>",
    "1.5",
    "Walk across the six historical CAD images. Use the folder count to convey the amount of recorded design work, then move to the physical observations that made revisions necessary.",
    "HISTORY"
  ],
  [
    "",
    "The real jig changed the problem",
    "<div class=\"split \"><figure class=\"\"><img data-asset=\"H6\" alt=\"Earlier P20 axial CAD · before the width correction\"><figcaption>Earlier P20 axial CAD · before the width correction</figcaption></figure><div class=\"observations\"><div><b>More room</b><p>The reported inner span needed another 10 mm.</p></div><div><b>Different fit</b><p>Caps were too tight. Purchased rods had to stay 50 mm.</p></div><div><b>A different way to hold</b><p>Pushing felt smooth; releasing it sprang the mechanism open.</p></div></div></div><p class=\"takeaway\">The next design let fingers position the rods, then used a clamp to hold them.</p><p class=\"note\">Recorded physical feedback, Aug28; later P24 intent preview still needed physical testing.</p>",
    "1.5",
    "Name the three changes in the problem: room, fit and holding. Explain how releasing my hand revealed a different requirement from merely reaching a plausible pose.",
    "HISTORY"
  ],
  [
    "",
    "I kept asking for another rail route",
    "<div class=\"split \"><div><p class=\"large\">I relied on AI to deliver the mechanism I imagined.</p><p>After many frustrating rail iterations, simulation helped me begin to see the relationships and constraints.</p></div><figure class=\"\"><img data-asset=\"H4\" alt=\"One historical rail design · P19 CAD\"><figcaption>One historical rail design · P19 CAD</figcaption></figure></div><div class=\"loop-label\">An expensive route when the uncertainty stays vague · illustrative</div><div class=\"path horizontal\"><div>Describe the idea</div><div>Generate a model</div><div>Print & assemble</div><div>Explain what went wrong</div><div>Try again</div></div>",
    "1",
    "Describe relying on AI to deliver the imagined mechanism. Explain that seeing relationships in simulation changed how I could reason with the agent. The exact original customizer is missing; the next slide uses other recovered studies.",
    "BRIEF HISTORY"
  ],
  [
    "studies",
    "Different studies answered different questions",
    "<div class=\"shared-heading\"><span><b>Me</b> · intent and observations</span><span>↘ a shared representation ↙</span><span><b>Agent</b> · explanation and revision</span></div><div class=\"split\"><div><h2>Prescribed rod paths</h2><figure class=\"\"><img data-asset=\"Fpath\" alt=\"Earlier path study · a separate motion hypothesis\"><figcaption>Earlier path study · a separate motion hypothesis</figcaption></figure><p class=\"study-caption\">Make each rod’s proposed movement visible.</p></div><div><h2>Fixture contact and release</h2><figure class=\"\"><img data-asset=\"Pclamped\" alt=\"Later P25 study · rear cradle and front pad\"><figcaption>Later P25 study · rear cradle and front pad</figcaption></figure><p class=\"study-caption\">Show which fixture touches which rod, and when.</p></div></div><p class=\"note\">Two separate historical studies. Prescribed motion and intent views; neither proves force, friction or physical holding.</p>",
    "1.5",
    "Compare the questions, not competing accepted designs. The earlier study prescribes paths for the rods. P25 keeps rod centers fixed while fixture poses show contact and release. Identify its rear cradle supporting Blue and Green and its front pad holding Orange. These are separate historical hypotheses; neither is the missing original rail customizer or a force solver.",
    "SIMULATION BRIEF"
  ],
  [
    "fit-slide",
    "The fit test became knowledge we could reuse",
    "<div class=\"split \"><figure class=\"scene\" data-scene=\"fit\"><div class=\"scene-canvas\"></div><svg class=\"scene-annotations\" aria-hidden=\"true\"><line data-leader=\"rod\"/><text data-label=\"rod\">Metal rod</text><line data-leader=\"guide\"/><text data-label=\"guide\">Printed guide</text></svg><div class=\"scene-fallback\"><svg viewBox=\"0 0 500 280\" role=\"img\" aria-label=\"Cutaway of a metal rod inside a printed guide; clearance exaggerated\"><path d=\"M 332 70 A100 100 0 1 0 332 210 L294 185 A55 55 0 1 1 294 95Z\" fill=\"#14665f\"/><circle cx=\"250\" cy=\"140\" r=\"43\" fill=\"#af492d\"/><path d=\"M100 224L230 167M380 40L306 91\" stroke=\"#30363b\"/><text x=\"20\" y=\"247\">Metal rod</text><text x=\"320\" y=\"30\">Printed guide</text></svg></div><figcaption>Read-only 3D cutaway · gap exaggerated ×8.<br>Teaching geometry; printed fit comes from the test.</figcaption><p class=\"scene-status\" hidden>Static cutaway shown because WebGL is unavailable.</p></figure><div><h2>A real 4 mm metal rod</h2><p class=\"compact\">Five model holes, printed in PETG with a 0.4 mm nozzle.</p><table class=\"fit-record\"><thead><tr><th>Model hole</th><th>Recorded hand fit</th></tr></thead><tbody><tr><th>4.05 mm</th><td>Very tight</td></tr><tr><th>4.10 mm</th><td>Push / pull, still tight</td></tr><tr><th>4.15 mm</th><td>Best sliding; slight friction</td></tr><tr><th>4.20 mm</th><td>Looser</td></tr><tr><th>4.25 mm</th><td>Loose; wobble</td></tr></tbody></table></div></div><p class=\"takeaway\">Observation → <b>recorded sliding-fit reference</b> → available for the next design.</p><p class=\"note\">Observed coupon results, Aug21. Not a universal tolerance or whole-jig acceptance; no coupon photograph was recovered.</p>",
    "1.5",
    "Identify the rod, guide and clearance in the cutaway. Follow the observed tight-to-wobbly progression. Explain how the 4.15 mm result was recorded with its material, nozzle and rod context, making it available for later decisions without claiming universal fit.",
    "HISTORY"
  ],
  [
    "",
    "We prepared a print around one question",
    "<p>Keep the real curved slots. Test whether the small bridge between them survives printing and handling.</p><figure class=\"wide\"><img data-asset=\"H7\" alt=\"Actual prepared toolpaths · first, middle and top layers\"><figcaption>Actual prepared toolpaths · first, middle and top layers</figcaption></figure><div class=\"metrics\"><span><b>6m12s</b> slicer estimate</span><span><b>1.80g</b> slicer estimate</span><span><b>Physical result pending</b></span></div>",
    "1",
    "Point to the thin web between curved slots. Explain how a smaller experiment can retain the actual uncertainty. This record contains prepared toolpaths and slicer estimates; the physical survival result remains pending.",
    "HISTORY"
  ],
  [
    "",
    "I learned to choose the smallest useful test",
    "<table class=\"cost-table\"><thead><tr><th>Evidence</th><th>A useful question</th><th>Relative effort / speed</th><th>Still unknown</th></tr></thead><tbody><tr><th>Reasoning / calculation</th><td>Are the numbers consistent?</td><td>Lowest / immediate</td><td>Real behavior</td></tr><tr><th>Simulation</th><td>Do the relationships make sense?</td><td>Low / fast to vary</td><td>Unmodelled physics</td></tr><tr><th>CAD inspection</th><td>Do these solids interfere?</td><td>Low–medium / digital</td><td>Printed fit</td></tr><tr><th>Partial print</th><td>Does this interface work?</td><td>Material + waiting</td><td>Whole assembly</td></tr><tr><th>Full print</th><td>Does it assemble and operate?</td><td>More material + waiting</td><td>Long-term use</td></tr><tr><th>Real use</th><td>Does it work for me?</td><td>Context + time</td><td>Other conditions</td></tr></tbody></table><p class=\"takeaway\">Choose the smallest experiment that can change the decision.</p><p class=\"note\">Relative costs depend on the question. Choosing a test still leaves preparation and execution; digital evidence does not settle physical fit.</p>",
    "1.5",
    "Compare the question each evidence type can answer. Emphasize that the cheapest useful experiment is the one that can change the decision, rather than always the smallest or fastest test.",
    "BRIEF HISTORY"
  ],
  [
    "capabilities",
    "Tools reduced the work between decisions",
    "<div class=\"split wide-copy\"><div><table class=\"\"><thead><tr><th>Layer</th><th>What the evidence supports</th></tr></thead><tbody><tr><th>Snapmaker Orca CLI<br>guided workflows</th><td>Slice → inspect → authorized upload/start → monitor</td></tr><tr><th>U1 Print Studio MCP</th><td>Read-only observation of printer status and views</td></tr><tr><th>Further automation</th><td>Reusable preparation, support/orientation choices and reliable Live remain incomplete or unproven</td></tr></tbody></table><p class=\"compact\">The guided workflows have operated a real slicer and printer. The MCP app currently helps us observe.</p></div><figure class=\"ui-shot\"><img data-asset=\"UI\" alt=\"U1 Print Studio UI · synthetic test fixture\"><figcaption>U1 Print Studio UI · synthetic test fixture</figcaption></figure></div><p class=\"note\">Recorded runs and implementation audit, Sep3 snapshot. Fixture readings are not current printer telemetry.</p>",
    "1.5",
    "Explain how guided Snapmaker Orca CLI workflows carried preparation and authorized printing, while U1 Print Studio MCP supplied read-only observation. These tool connections reduced execution friction; they did not remove the need to choose and interpret the experiment.",
    "CAPABILITIES"
  ],
  [
    "",
    "A finished print still needed me",
    "<p>One recorded PETG pilot: two cam-plate parts.</p><table class=\"\"><thead><tr><th>Execution result</th><th>Physical result</th></tr></thead><tbody><tr><th>The print completed</th><td>Assembly exposed fit and mechanism-design failures</td></tr></tbody></table><p class=\"statement\">Agents can remove me from the toolchain<br><b>without removing me from the loop.</b></p><p class=\"compact\">I still decide what matters, interpret fit and use, and accept the result.</p>",
    "1",
    "Use the single PETG pilot to separate printing from acceptance. Two cam-plate parts printed, but assembly exposed fit and mechanism-design failures. Read the human-loop sentence and explain what I still need to judge.",
    "CAPABILITIES"
  ],
  [
    "coevolution",
    "The projects and the working system grew together",
    "<p>Each project problem gave us a reason to improve how we worked.</p><div class=\"split \"><div><h2>Costly whole revisions</h2><div class=\"path \"><div>A broad idea becomes a whole model</div><div>Full print and assembly</div><div>An unclear failure report</div><div>Another whole revision</div></div></div><div><h2>Shared studies + targeted tests</h2><div class=\"path \"><div>Name one project uncertainty</div><div>Build a shared view or targeted sample</div><div>Record specific evidence and context</div><div>Choose a bounded next action</div></div></div></div><p class=\"takeaway\">We accumulated <b>fit knowledge, feedback interfaces and tool handoffs</b> alongside the designs.</p><p class=\"note\">Illustrative comparison with relative costs; not every historical revision was printed.</p>",
    "1.5",
    "Use the two loops as the payoff of co-evolution. Point back to the saved fit reference, the separate studies and the guided tools. Explain that project pressure supplied the reason for each improvement; this is not a dated claim that every capability appeared in this order.",
    "BRIEF HISTORY SIMULATION CAPABILITIES"
  ],
  [
    "",
    "Laifen: a case for my electric toothbrush",
    "<p>A travel case for my Laifen electric toothbrush.</p><div class=\"split \"><figure class=\"\"><img data-asset=\"Lphoto\" alt=\"Earlier physical thread specimens · actual photo\"><figcaption>Earlier physical thread specimens · actual photo</figcaption></figure><figure class=\"\"><img data-asset=\"Llayout\" alt=\"R6 two-part full case · reviewed CAD\"><figcaption>R6 two-part full case · reviewed CAD</figcaption></figure></div><p class=\"takeaway\">All three printed closures felt good by hand. I wanted a uniform shape and a full-size case.</p><p class=\"note\">Earlier closure feedback does not establish physical fit of this R6 case.</p>",
    "1",
    "Introduce Laifen as the current example of this way of working. Show the earlier physical thread specimens and their hand-fit feedback, then distinguish the separately reviewed full-size R6 CAD. The physical specimens informed preference, not proof of R6 loaded fit.",
    "LAIFEN"
  ],
  [
    "laifen",
    "Extra length does not hold the brush in place",
    "<div class=\"split \"><figure class=\"\"><img data-asset=\"Lsection\" alt=\"R6 section · nominal brush envelope, centered and unretained\"><figcaption>R6 section · nominal brush envelope, centered and unretained</figcaption></figure><div><p>Like XT60, this is a relationship we can inspect before more execution.</p><div class=\"gap-pair\"><div><b>Centered</b><span>2.5 mm above</span><svg viewBox=\"0 0 160 190\" role=\"img\" aria-label=\"Identical cavity, brush centered with space at both ends\"><rect x=\"50\" y=\"15\" width=\"60\" height=\"150\" fill=\"none\" stroke=\"#394b59\" stroke-width=\"2\"/><rect x=\"57\" y=\"35\" width=\"46\" height=\"110\" fill=\"#cfaa48\" stroke=\"#926a05\"/><path d=\"M40 165H120\" stroke=\"#394b59\" stroke-width=\"3\"/></svg><span>2.5 mm below</span></div><div><b>Resting on bottom</b><span>5 mm above</span><svg viewBox=\"0 0 160 190\" role=\"img\" aria-label=\"Identical cavity, same brush touching its bottom end\"><rect x=\"50\" y=\"15\" width=\"60\" height=\"150\" fill=\"none\" stroke=\"#394b59\" stroke-width=\"2\"/><rect x=\"57\" y=\"55\" width=\"46\" height=\"110\" fill=\"#cfaa48\" stroke=\"#926a05\"/><path d=\"M40 165H120\" stroke=\"#394b59\" stroke-width=\"3\"/></svg><span>0 mm below · contact</span></div></div><p class=\"note\">Nominal schematic · gaps exaggerated</p><button class=\"demo-launch\" data-demo-open>Open the clearance study</button><p class=\"note\">Earlier browser study · not R6 CAD controls</p></div></div><p class=\"takeaway\">The next decision: is bottom support acceptable for the real loaded brush.</p>",
    "2",
    "Connect this to XT60: inspect one relationship before more execution. Compare the two outlined cavities, then open the earlier study and follow the 90-second demonstration below. Ask what evidence would settle whether bottom support is acceptable, without turning the slide into an audience exercise.",
    "LAIFEN"
  ],
  [
    "",
    "Now we can name what remains to learn",
    "<p>The next decision is whether bottom support is acceptable for the real loaded brush.</p><table class=\"\"><thead><tr><th>Evidence or gap</th><th>What it means for the next decision</th></tr></thead><tbody><tr><th>Earlier physical observation</th><td>The printed thread specimens felt good by hand.</td></tr><tr><th>Digital model evidence</th><td>The nominal envelope has room; that does not establish restraint.</td></tr><tr><th>Unresolved physical condition</th><td>Installed brush envelope, loaded closure and end contact.</td></tr><tr><th>Useful next evidence</th><td>Check the full-size loaded case against the intended fit and support.</td></tr></tbody></table><p class=\"takeaway\">Use the result to accept the support arrangement or revise it.</p><p class=\"note\">Full-size progression is already chosen. R6 physical fit remains pending; this is not a request for another mandatory coupon.</p>",
    "1",
    "Move beyond the clearance observation to the actual acceptance decision. Separate earlier closure feedback, nominal model evidence and the still-needed full-size loaded-case observations. Explain what a useful result would let us decide.",
    "LAIFEN BRIEF"
  ],
  [
    "",
    "The same habit can guide other work",
    "<div class=\"split \"><div><h2>Software · illustrative experiment</h2><div class=\"path \"><div>Uncertainty: a stale reading may look current</div><div>Experiment: feed a small fixture an old timestamp and failed refresh</div><div>Decision: revise misleading feedback, or test the next failure case</div></div></div><div><h2>Physical tools · future example</h2><div class=\"path \"><div>Uncertainty: holding after my hand releases</div><div>Experiment: record release with a load sensor</div><div>Decision: compare with the agreed holding criterion and revise if needed</div></div></div></div><p class=\"takeaway\">Choose an experiment whose evidence could change the plan.</p><p class=\"note\">A camera could add motion evidence; an arm could repeat an action. These are future examples, not deployed integrations.</p>",
    "1",
    "Compare the same uncertainty, experiment and decision pattern across software and physical work. Keep the software fixture explicitly illustrative and sensor or arm examples future-facing. Leave the full architecture to the next slide.",
    "BRIEF"
  ],
  [
    "closing",
    "Keep human judgment in the feedback loop",
    "<div class=\"architecture\"><div class=\"partners\"><span><b>Person</b><br>Intent · constraints · taste · acceptance</span><span>↔</span><span><b>Agent</b><br>Reasoning · tool use · continuity</span></div><div class=\"shared-model\">Shared model of the problem<br><strong>↓ choose what to learn next</strong></div><div class=\"branches\"><div><b>Digital experiment</b><p>Calculate · simulate · inspect</p><span>↓ model evidence</span></div><div><b>Physical experiment + tools</b><p>Prepare · print · measure · use</p><span>↓ physical observations</span></div></div><div class=\"return\">↑ Interpret together and update the shared model ↺</div></div><p class=\"takeaway\">Design feedback from day one.<br>Choose the fastest, cheapest, strongest useful loop.</p>",
    "1",
    "Return to the shared model at the center. Connect human intent and acceptance, agent reasoning and continuity, digital evidence and physical observations. Close by choosing what to learn next and designing feedback from day one.",
    "BRIEF"
  ]
];
const css=await readFile(resolve(here,'deck.css'),'utf8');
const auditText={};for(const name of ['HISTORY','CAPABILITIES','SIMULATION','LAIFEN','BRIEF'])auditText[name]=await readFile(resolve(here,`docs/iterations/2026-09-03-journey-feedback/${name}.md`),'utf8');
auditText.BRIEF+='\n\n'+await readFile(resolve(here,'docs/iterations/2026-09-03-journey-walkthrough/BRIEF.md'),'utf8');
const gateDoc=`<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><style>:root{--foreground:#202b34;--muted:#65717b;--viz-series-1:#176ac0}body{font:16px system-ui;margin:20px;background:white;color:var(--foreground)}input,button{font:inherit}button{padding:8px 18px;margin:4px;background:#edf5fb;border:1px solid #8ea4b5;border-radius:4px}.viz-controls{display:flex;gap:12px;flex-wrap:wrap}.form-label{display:block}input[type=number]{width:80px}input[type=range]{width:200px}.text-destructive{color:#ac431f}</style>${gate}</html>`;
const nav=`(()=>{'use strict';const images=${JSON.stringify(media)};document.querySelectorAll('[data-asset]').forEach(i=>i.src=images[i.dataset.asset]);const slides=[...document.querySelectorAll('.slide')],notes=${JSON.stringify(slides.map(s=>s[4]))},audits=${JSON.stringify(auditText)},gateDoc=${JSON.stringify(gateDoc)},drawer=document.querySelector('#drawer'),demo=document.querySelector('#laifen-demo'),frame=document.querySelector('#laifen-frame');let current=0;function show(n){current=Math.max(0,Math.min(slides.length-1,n));slides.forEach((s,i)=>s.classList.toggle('active',i===current));history.replaceState(null,'','#slide-'+(current+1));document.querySelector('#counter').textContent=(current+1)+' / '+slides.length;document.querySelector('#overview').classList.remove('open');window.scrollTo(0,0)}window.showSlide=show;function close(){drawer.classList.remove('open');document.querySelector('#overview').classList.remove('open');if(demo.open){demo.close();document.querySelector('[data-demo-open]').focus()}}document.querySelector('#prev').onclick=()=>show(current-1);document.querySelector('#next').onclick=()=>show(current+1);document.querySelector('#notes').onclick=()=>{document.querySelector('#drawer-title').textContent='Presenter notes · '+(current+1);document.querySelector('#drawer-body').textContent=notes[current];drawer.classList.add('open')};document.querySelector('#sources').onclick=()=>{document.querySelector('#drawer-title').textContent='Evidence for slide '+(current+1);document.querySelector('#drawer-body').textContent=slides[current].dataset.sources.split(' ').map(k=>audits[k]).join('\\n\\n');drawer.classList.add('open')};document.querySelector('#close-drawer').onclick=close;document.querySelector('#overview-toggle').onclick=()=>document.querySelector('#overview').classList.toggle('open');document.querySelectorAll('[data-go]').forEach(b=>b.onclick=()=>show(Number(b.dataset.go)));document.querySelectorAll('[data-demo-open]').forEach(b=>b.onclick=()=>{demo.showModal();frame.srcdoc=gateDoc;document.querySelector('#demo-live').hidden=false;document.querySelector('#demo-fallback').hidden=true});document.querySelector('#demo-close').onclick=close;document.querySelector('#demo-reset').onclick=()=>{frame.srcdoc=gateDoc;document.querySelector('#demo-live').hidden=false;document.querySelector('#demo-fallback').hidden=true};document.querySelector('#demo-fallback-toggle').onclick=()=>{document.querySelector('#demo-live').hidden=true;document.querySelector('#demo-fallback').hidden=false};addEventListener('keydown',e=>{if(e.key==='Escape'){close();return}if(demo.open||/INPUT|TEXTAREA|SELECT/.test(e.target.tagName))return;if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();show(current+1)}if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();show(current-1)}if(e.key==='Home')show(0);if(e.key==='End')show(slides.length-1);if(e.key.toLowerCase()==='n')document.querySelector('#notes').click();if(e.key.toLowerCase()==='s')document.querySelector('#sources').click();if(e.key.toLowerCase()==='o')document.querySelector('#overview-toggle').click()});show(Number(location.hash.match(/slide-(\\d+)/)?.[1]||1)-1)})();`;
const html=`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>My 3D Printing Journey With AI Agents</title><style>${css}</style></head><body><main class="deck">${slides.map(([cls,title,body,time,notes,refs],i)=>`<section class="slide ${cls}${i===0?' active':''}" id="slide-${i+1}" data-sources="${refs}"><div class="eyebrow">${i<4?'GETTING STARTED':i<12?'WHAT THE PROJECTS TAUGHT ME':i<18?'HOW WE WORK NOW':'WHAT COMES NEXT'}</div><h1>${title}</h1><div class="body">${body}</div><footer>SCOTT · 3D PRINTING × AI AGENTS</footer><span class="num">${String(i+1).padStart(2,'0')} / ${slides.length}</span></section>`).join('')}</main><nav class="controls" aria-label="Presentation controls"><button id="prev" aria-label="Previous slide">←</button><span id="counter">1 / ${slides.length}</span><button id="next" aria-label="Next slide">→</button><button id="notes">Notes</button><button id="sources">Sources</button><button id="overview-toggle">Overview</button></nav><aside class="drawer" id="drawer"><button id="close-drawer">Close</button><h2 id="drawer-title"></h2><pre id="drawer-body"></pre></aside><div class="overview" id="overview"><h2>Journey overview</h2>${slides.map((s,i)=>`<button data-go="${i}">${i+1}. ${s[1].replaceAll('<br>',' ')}</button>`).join('')}</div><dialog id="laifen-demo"><header><div><h2>Laifen clearance study</h2><p>Earlier nominal-envelope study · browser-only · not R6 CAD controls</p></div><div><button id="demo-reset">Reset centered</button><button id="demo-fallback-toggle">Show fallback</button><button id="demo-close">Close demo</button></div></header><p class="demo-explanation">Use <b>置中</b> (centered): 2.5 mm + 2.5 mm. Then <b>靠底</b> (resting on bottom): 0 mm + 5 mm. Clearance alone does not hold the brush in place.</p><div id="demo-live"><iframe id="laifen-frame" title="Earlier Laifen measurement study" sandbox="allow-scripts"></iframe>${fig('Lsection','Current R6 section · nominal reference is not retained')}</div><div id="demo-fallback" hidden><div class="gallery three">${fig('Lcenter','Earlier study · centered: 2.5 + 2.5 mm')}${fig('Lbottom','Earlier study · bottom contact: 0 + 5 mm')}${fig('Lsection','R6 section · physical loaded fit pending')}</div></div><p class="demo-decision">Next decision: whether bottom support is acceptable. Confirm the installed brush envelope and eventual loaded closure/contact.</p></dialog><script>${nav.replaceAll('</script','<\\/script')}</script><script>${bundle}</script></body></html>`;
await writeFile(resolve(here,'index.html'),html);
await writeFile(resolve(here,'docs/iterations/2026-09-03-journey-walkthrough/SLIDES.json'),JSON.stringify(slides.map((s,i)=>({slide:i+1,title:s[1].replaceAll('<br>',' '),minutes:Number(s[3]),notes:s[4],sources:s[5].split(' ')})),null,2)+'\n');
console.log(`Built ${slides.length} slides; ${(Buffer.byteLength(html)/1048576).toFixed(1)} MiB; embedded ${Object.keys(media).length} actual images and exact Laifen study.`);
