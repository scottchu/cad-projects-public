import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {DEFAULT_STATE,FIELD_SCHEMA,MODULE_SCHEMA,visible} from "../preview/p2-r9-modular-generator/core/schema.mjs";
import {deepMerge,clone,getPath,setPath} from "../preview/p2-r9-modular-generator/core/utils.mjs";
import {PRESET_PATCHES,presetState} from "../preview/p2-r9-modular-generator/core/presets.mjs";
import {OPENSCAD_EXPORT_MAP,flattenForOpenScad} from "../preview/p2-r9-modular-generator/core/export-map.mjs";
import {ACCESSORY_REGISTRY} from "../preview/p2-r9-modular-generator/plugins/accessories.mjs";
import {CLOSURE_REGISTRY} from "../preview/p2-r9-modular-generator/plugins/closures.mjs";
import {END_REGISTRY} from "../preview/p2-r9-modular-generator/plugins/ends.mjs";
import {PATTERN_REGISTRY} from "../preview/p2-r9-modular-generator/plugins/patterns.mjs";
import {attachmentBounds,deriveModel,drainHoles,endSamples,labelBoxes,patchWeight,rawPattern,reliefFacts,sectionFrame} from "../preview/p2-r9-modular-generator/core/derive.mjs";
const copy=state=>clone(state),derive=(patch={})=>deriveModel(deepMerge(DEFAULT_STATE,patch));

assert.deepEqual(Object.keys(DEFAULT_STATE),["container","closure","ends","surface","ventDrain","label","attachment"]);
assert.deepEqual(MODULE_SCHEMA,["Container","Closure","Ends","Surface","Vent & Drain","Label","Attachment"]);
assert.equal(new Set(FIELD_SCHEMA.map(field=>field.path)).size,FIELD_SCHEMA.length,"each canonical leaf has one schema record");
assert.equal(new Set(FIELD_SCHEMA.map(field=>field.exportKey)).size,FIELD_SCHEMA.length,"schema export keys are unique");
for(const field of FIELD_SCHEMA){assert.notEqual(getPath(DEFAULT_STATE,field.path),undefined,field.path);assert.ok(field.label&&field.control&&field.valueType);}
assert.equal(Object.keys(OPENSCAD_EXPORT_MAP).length,FIELD_SCHEMA.length);assert.equal(Object.keys(flattenForOpenScad(DEFAULT_STATE)).length,FIELD_SCHEMA.length);
for(const id of ["generic","laifen_wave_reference","wide_short_makeup_jar"]){const state=presetState(id),again=presetState(id);assert.ok(deriveModel(state).valid,id);assert.deepEqual(state,again,"preset application is idempotent");assert.notEqual(state,again,"preset clone is independent");}
assert.deepEqual(PRESET_PATCHES.generic,{});assert.equal(derive().totalEnvelope,60);assert.equal(derive({surface:{reliefMode:"outset",pattern:"blunt_diamond",depth:1}}).crestOD,62,"outset crest is accounted");
assert.ok(Object.isFrozen(DEFAULT_STATE)&&Object.isFrozen(PRESET_PATCHES)&&Object.isFrozen(ACCESSORY_REGISTRY));
assert.deepEqual(Object.keys(CLOSURE_REGISTRY),["screw","bayonet"]);assert.deepEqual(Object.keys(END_REGISTRY),["flat","chamfer","rounded_fillet","dome"]);assert.ok("quilted_diamond" in PATTERN_REGISTRY);
for(const registry of [CLOSURE_REGISTRY,END_REGISTRY,PATTERN_REGISTRY,ACCESSORY_REGISTRY])for(const plugin of Object.values(registry)){assert.ok(plugin.id&&plugin.visual.mainBuilder&&plugin.visual.comparisonBuilder);}
assert.equal(new Set(Object.values(ACCESSORY_REGISTRY).map(plugin=>plugin.visual.mainBuilder)).size,5,"accessories use unique builders");
for(const profile of Object.keys(END_REGISTRY)){const state=copy(DEFAULT_STATE);state.ends.linked=false;state.ends.bottom.profile=profile;state.ends.bottom.size=profile==="flat"?0:1;assert.ok(deriveModel(state).valid,profile);}
const dome=endSamples("dome",3,30);assert.ok(new Set(dome.map(point=>point.z.toFixed(4))).size>3,"dome is curved, not planar");
for(const patch of [{ends:{bottom:{profile:"flat",size:1}}},{ends:{linked:false,top:{profile:"dome",size:0}}},{attachment:{mountAngleDeg:360}},{attachment:{mountAngleDeg:-1}},{attachment:{mountAngleDeg:Infinity}}])assert.ok(!derive(patch).valid,"invalid active value clears output");
for(const turns of [1,2,3])assert.equal(derive({closure:{mode:"screw",screw:{turns}}}).closure.rotation,2*Math.PI*turns);
const bayonet=derive({closure:{mode:"bayonet",bayonet:{lockAngleDeg:73,lugCount:2,capture:2,rampRise:1}}});assert.ok(bayonet.valid);assert.equal(bayonet.closure.rotation,73*Math.PI/180);
const softA=derive({surface:{pattern:"shallow_helix",spiral:{pitch:35,bandWidth:7,softness:.5,direction:-1}}}),softB=derive({surface:{pattern:"shallow_helix",spiral:{pitch:80,bandWidth:13,softness:.9,direction:1}}});assert.equal(softA.closure.protected,softB.closure.protected,"surface spiral never changes closure accounting");
for(const id of Object.keys(PATTERN_REGISTRY)){const d=derive({surface:{pattern:id}});assert.ok(d.valid,id);assert.ok(Number.isFinite(rawPattern(id,.7,23,d.state)));}
const quilt=derive({surface:{pattern:"quilted_diamond"}});assert.equal(rawPattern("quilted_diamond",.3,18,quilt.state),rawPattern("quilted_diamond",.3+2*Math.PI,18+quilt.state.surface.axialPitch,quilt.state));
for(const mode of ["inset","outset","balanced"]){const r=reliefFacts(derive({surface:{pattern:"quilted_diamond",reliefMode:mode}}).state);assert.ok(r.insetDepth>=0&&r.outsetHeight>=0);}
const both=derive({label:{mode:"outset",target:"both",text:"WAVE",axialFromTargetEnd:20}});assert.equal(both.labels.length,2);assert.equal(patchWeight(Math.PI,both.labels[0].z,both.state,both),0);assert.ok(patchWeight(0,both.labels[0].z,both.state,both)>0);
const frame=sectionFrame(0,DEFAULT_STATE);assert.ok(Math.abs(frame.outwardRight.x)<1e-12&&frame.outwardRight.y===1&&frame.outwardRight.z===0,"outward right is axialUp cross normal");
for(const mode of ["none","bottom","top","both"]){const one={count:1,diameter:2,ringRadius:0},d=derive({ventDrain:{mode,linked:true,bottom:one,top:one}});assert.ok(d.valid,mode);assert.equal(d.drains.bottom.length,mode==="bottom"||mode==="both"?1:0);assert.equal(d.drains.top.length,mode==="top"||mode==="both"?1:0);for(const hole of [...d.drains.bottom,...d.drains.top])assert.ok(hole.throughFloor&&hole.axis);}
assert.ok(!derive({ventDrain:{mode:"bottom",bottom:{count:7,diameter:9,ringRadius:10}}}).valid,"drain web rejects overlap");
for(const id of Object.keys(ACCESSORY_REGISTRY)){const d=derive({attachment:{mode:id,presentation:"separate_visual"}});assert.ok(d.valid,id);assert.ok(attachmentBounds(d.state).radial>0);assert.ok(d.totalEnvelope>=d.crestOD);}
const invalid=derive({container:{outerDiameter:3,wall:2.4}});assert.equal(invalid.valid,false);assert.ok(invalid.errors.length);
const [app,html,css,svg]=await Promise.all(["app.mjs","index.html","style.css","render/svg.mjs"].map(file=>readFile(new URL(`../preview/p2-r9-modular-generator/${file}`,import.meta.url),"utf8")));
assert.ok(app.includes("FIELD_SCHEMA")&&app.includes("deriveModel")&&!app.includes("three"));assert.ok(!html.includes("http")&&!html.includes("cdn"));assert.ok(css.includes("@media(max-width:900px)")&&css.includes("prefers-reduced-motion"));assert.ok(svg.includes("lower-piece")&&svg.includes("upper-piece")&&svg.includes("BAYONET")&&svg.includes("SCREW"));
console.log("R9 modular generator focused pure checks passed");
