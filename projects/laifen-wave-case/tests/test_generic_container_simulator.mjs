import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {PRESETS,deriveContainer,patternField,percentBounds,percentToSplit,cameraFitForBox} from "../preview/p2-r2-generic-container-simulator/math.mjs";

const laifen=deriveContainer(PRESETS.laifen_wave_reference);
const jar=deriveContainer(PRESETS.wide_short_makeup_jar);
assert.ok(laifen.valid&&jar.valid,"both reference forms remain feasible");
assert.equal(laifen.E,6);assert.equal(laifen.P,9);assert.equal(jar.E,3);assert.equal(jar.P,7.5);
for(const N of[1,2,3]){const q=deriveContainer({...PRESETS.generic,N});assert.equal(q.E,2*N);assert.equal(q.P,2*(N+q.Lr));}
const shortThread=deriveContainer({...PRESETS.wide_short_makeup_jar,p:1.4,N:1,Lr:.5,H:42,S:21,keepout:2,axial:4});assert.ok(shortThread.valid);assert.equal(shortThread.E,1.4);assert.ok(Math.abs(shortThread.P-2.1)<1e-12);
for(const H of[261,311]){
  const q=deriveContainer({...PRESETS.generic,H,S:80}),bounds=percentBounds(q);
  const lower=percentToSplit(Number(bounds.min.toFixed(3)),H,{...bounds,Smin:q.Smin,Smax:q.Smax});
  const upper=percentToSplit(Number(bounds.max.toFixed(3)),H,{...bounds,Smin:q.Smin,Smax:q.Smax});
  assert.ok(Math.abs(lower-q.Smin)<.002);assert.ok(Math.abs(upper-q.Smax)<.002);
  for(const S of[q.Smin,(q.Smin+q.Smax)/2,q.Smax])assert.ok(Math.abs(percentToSplit(100*S/H,H,{...bounds,Smin:q.Smin,Smax:q.Smax})-S)<1e-9);
}
const infeasible=deriveContainer({...PRESETS.wide_short_makeup_jar,H:20});assert.ok(!infeasible.valid&&!infeasible.feasible);assert.ok(infeasible.errors[0].includes("Required H >= 2*(F+P+K)"));assert.ok(infeasible.errors[0].includes("S_min="));assert.ok(infeasible.fieldErrors.some(e=>e.fieldId==="H"));assert.equal(percentBounds(infeasible),null);
for(const [field,value,id] of [["H",0,"H"],["OD",Infinity,"OD"],["wall",-1,"wall"],["F",0,"F"],["p",0,"p"],["formHeight",0,"formHeight"],["Lr",-1,"Lr"],["keepout",-1,"keepout"],["clearance",-1,"clearance"],["axial",0,"axial"],["arc",0,"arc"],["depth",NaN,"depth"],["chamfer",-1,"chamfer"],["drainCount",1.5,"drainCount"],["N",4,"N"],["pattern","bad","pattern"],["drains","true","drains"],["exploded",1,"exploded"],["lowerBore",-2,"lowerBore"],["upperBore",200,"upperBore"]]){
  const q=deriveContainer({...PRESETS.generic,[field]:value});assert.ok(!q.valid,`${field} rejected`);assert.ok(q.fieldErrors.some(e=>e.fieldId===id),`${field} has stable field association`);
}
const badSplit=deriveContainer({...PRESETS.generic,S:2});assert.ok(!badSplit.valid);assert.deepEqual([...new Set(badSplit.fieldErrors.map(e=>e.fieldId))].sort(),["S","percent"]);
const phaseA=patternField("blunt_diamond",1.2,44,laifen),phaseB=patternField("blunt_diamond",1.2,44,{...laifen,S:50});assert.equal(phaseA,phaseB);
for(const pattern of["smooth","blunt_diamond","shallow_helix","wave_flutes"])for(const z of[0,laifen.z0,laifen.H])assert.equal(patternField(pattern,.75,z,laifen),patternField(pattern,.75,z,{...laifen,exploded:true}));

const portrait=cameraFitForBox({x:120,y:88,z:120},.5,34,1.16),landscape=cameraFitForBox({x:120,y:88,z:120},2,34,1.16);
assert.ok(portrait&&landscape);assert.ok(portrait.horizontalDistance>portrait.verticalDistance);assert.ok(landscape.verticalDistance>landscape.horizontalDistance);assert.equal(portrait.distance,portrait.horizontalDistance);assert.equal(landscape.distance,landscape.verticalDistance);assert.ok(portrait.near>0&&portrait.far>portrait.distance);
assert.equal(cameraFitForBox({x:1,y:1,z:1},0),null);

const [html,css,app]=await Promise.all([
  readFile(new URL("../preview/p2-r2-generic-container-simulator/index.html",import.meta.url),"utf8"),
  readFile(new URL("../preview/p2-r2-generic-container-simulator/style.css",import.meta.url),"utf8"),
  readFile(new URL("../preview/p2-r2-generic-container-simulator/app.js",import.meta.url),"utf8")
]);
for(const text of["three@0.160.1","Size &amp; split","Thread","Surface &amp; ends","Lead/runout","Thread form height","Smooth keepout","visual thread band","effective","detailUnavailable"])assert.ok(html.includes(text),`HTML includes ${text}`);
assert.equal((html.match(/<details open>/g)||[]).length,3,"three collapsible semantic groups");
for(const id of["H","OD","wall","F","lowerBore","upperBore","S","percent","p","N","Lr","formHeight","clearance","keepout","pattern","axial","arc","depth","chamfer","drains","drainCount","exploded"])assert.ok(html.includes(`id="${id}"`),`${id} control retained`);
for(const text of["ResizeObserver","cameraFitForBox(size,cam.aspect","new THREE.Box3().setFromObject(group)","fitCamera(\"geometry-build\")","viewDirection","controls.target.copy(center)","cam.near=fit.near","cam.far=fit.far"])assert.ok(app.includes(text),`camera fit behavior includes ${text}`);
assert.ok(!app.includes("cam.position.set(150,130,160)"));assert.ok(!app.includes("controls.target.set(0,60,0)"));
for(const text of["lower-piece","upper-piece","assembled-thread-band-marker","exploded-thread-band-marker","full-visual-thread-band-bracket","effective-thread-engagement-bracket","seam-marker"])assert.ok(app.includes(text),`scene semantics include ${text}`);
for(const text of["closedEndInset","endPatternFade","lower-chamfer-transition","upper-chamfer-transition","lower-closed-end","upper-closed-end","lower-drain-apertures","upper-drain-apertures"])assert.ok(app.includes(text),`end treatment includes ${text}`);
assert.ok(app.includes("if(d.drains&&d.drainCount>0)"),"drain scene objects only added when on and nonzero");
for(const text of["group.clear()","lastFit:null","ctx.clearRect","canvas.classList.add(\"unavailable\")","Unavailable until parameters are valid","status.setAttribute(\"role\",\"alert\")"])assert.ok(app.includes(text),`invalid suppression includes ${text}`);
for(const text of["aria-invalid","aria-errormessage","aria-describedby","d.fieldErrors","Valid: ${summary}","Warning: ${d.warnings.join"])assert.ok(app.includes(text),`field/live semantics include ${text}`);
assert.ok(css.includes("#viewerFrame"));assert.ok(css.includes("@media(max-width:900px)"));

let canonical={...PRESETS.generic,H:261};let canonicalDerived=deriveContainer(canonical),canonicalBounds=percentBounds(canonicalDerived);
canonical.S=percentToSplit(canonicalBounds.min,canonical.H,{...canonicalBounds,Smin:canonicalDerived.Smin,Smax:canonicalDerived.Smax});canonicalDerived=deriveContainer(canonical);assert.equal(canonical.S,12.4);assert.equal(String(canonical.S),"12.4");assert.equal(100*canonical.S/canonical.H,canonicalBounds.min);
canonical.S=percentToSplit(canonicalBounds.max,canonical.H,{...canonicalBounds,Smin:canonicalDerived.Smin,Smax:canonicalDerived.Smax});canonicalDerived=deriveContainer(canonical);assert.equal(canonical.S,248.6);assert.equal(String(canonical.S),"248.6");assert.equal(100*canonical.S/canonical.H,canonicalBounds.max);
canonical.S=137.25;canonicalDerived=deriveContainer(canonical);assert.equal(100*canonical.S/canonical.H,52.58620689655172,"reverse mm edit projects directly to percent");
for(const text of["function syncControlsFromCanonical(rawState,derivedState)","$(\"S\").min=String(derivedState.Smin)","$(\"S\").max=String(derivedState.Smax)","$(\"S\").step=\"0.1\"","$(\"S\").value=String(rawState.S)","$(\"percent\").step=\"any\"","$(\"percent\").value=String(100*rawState.S/rawState.H)","d=deriveContainer(raw);if(d.valid)syncControlsFromCanonical(raw,d);renderAll()"] )assert.ok(app.includes(text),`canonical control transaction includes ${text}`);
const percentWrite=app.indexOf("raw.S=percentToSplit"),deriveAfterPercent=app.indexOf("d=deriveContainer(raw)",percentWrite),syncAfterDerive=app.indexOf("syncControlsFromCanonical(raw,d)",deriveAfterPercent),renderAfterSync=app.indexOf("renderAll()",syncAfterDerive);assert.ok(percentWrite>=0&&percentWrite<deriveAfterPercent&&deriveAfterPercent<syncAfterDerive&&syncAfterDerive<renderAfterSync,"event -> raw -> derive -> sync -> render order is durable");
assert.ok(!app.includes("function syncBounds("));assert.ok(!app.includes("function populateForm("));
console.log("generic container simulator recovery checks passed");
