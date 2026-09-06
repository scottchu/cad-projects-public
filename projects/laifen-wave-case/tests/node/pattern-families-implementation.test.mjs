import {test} from 'node:test';
import assert from 'node:assert/strict';
import {adapt,DEFAULTS} from '../../preview/openscad-wasm-simulator/src/adapter.mjs';
import {deriveDraftState,dimensionSnapshot} from '../../preview/openscad-wasm-simulator/src/bounds.mjs';
import {canonical,snapshot} from '../../preview/openscad-wasm-simulator/src/schema.mjs';
import {patternMemories,TEXTURED} from '../../preview/openscad-wasm-simulator/src/patterns.mjs';
import {steppedValue} from '../../preview/openscad-wasm-simulator/src/controls.mjs';

test('off-grid slider actions use the next nominal grid and pointer ties upward',()=>{
 const size=[4.8,4.9,5],depth=[.4,.45,.5];
 assert.equal(steppedValue(size,4.83,'ArrowRight'),4.9);assert.equal(steppedValue(size,4.83,'ArrowLeft'),4.8);
 assert.equal(steppedValue(depth,.43,'ArrowRight'),.45);assert.equal(steppedValue(depth,.43,'ArrowLeft'),.4);
 assert.equal(steppedValue(depth,.425),.45);assert.equal(steppedValue(size,4.83,'Home'),4.8);assert.equal(steppedValue(size,4.83,'End'),5);
});
test('full normalized snapshots exclude inactive memories and retain active exact values',()=>{
 const raw={...DEFAULTS,patterns:patternMemories(),pattern:'diamond'};
 raw.patterns.diamond={size:'4.83',depth:'0.43'};
 const job=adapt(raw).values;assert.equal(job.diamond_axial_pitch,4.83);assert.equal(job.diamond_arc_pitch,4.83*(3.63/4.8));
 raw.patterns.ribs={size:'bad',depth:''};assert.equal(canonical(adapt(raw).values),canonical(job));
 assert.equal(canonical(snapshot({...job,wave_spacing:'bad',wave_depth:''})),canonical(job));
 assert.throws(()=>snapshot({...job,diamond_arc_pitch:3.63}),/derived values/);
});
test('each family slider feasible step passes the same adapter and inactive errors cannot disable it',()=>{
 for(const pattern of TEXTURED){
  const raw={...DEFAULTS,patterns:patternMemories(),pattern,wall:'4.6'};
  raw.patterns[pattern==='rings'?'ribs':'rings']={size:'bad',depth:''};
  const state=deriveDraftState(raw,dimensionSnapshot(DEFAULTS));assert.equal(state.canGenerate,true);
  for(const key of ['size','depth'])for(const value of state.patternSliders[key].values){
   const draft={...raw,patterns:{...raw.patterns,[pattern]:{...raw.patterns[pattern],[key]:String(value)}}};
   assert.ok(adapt(draft).values,`${pattern}/${key}/${value}`);
  }
 }
});
test('invalid selected input disables dependent controls while leaving numeric own-field repair',()=>{
 const raw={...DEFAULTS,patterns:patternMemories(),pattern:'spiral'};raw.patterns.spiral.size='3';
 let state=deriveDraftState(raw,dimensionSnapshot(DEFAULTS));assert.equal(state.canGenerate,false);assert.equal(state.patternSliders.size.disabled,false);assert.equal(state.patternSliders.depth.disabled,true);assert.equal(state.sliders.wall.disabled,true);
 raw.patterns.spiral.size='';state=deriveDraftState(raw,dimensionSnapshot(DEFAULTS));assert.equal(state.patternSliders.size.hideThumb,true);assert.equal(state.patternSliders.size.disabled,true);
});

test('wave depth .60 accepts exact wall 4.56 equality and rejects the adjacent lower witness',()=>{
 for(const pattern of ['ribs','rings','spiral'])for(const [wall,valid] of [['4.55',false],['4.5599999',false],['4.56',true],['4.5600001',true]]){
  const raw={...DEFAULTS,patterns:patternMemories(),pattern,wall,height:'60',auto:false,lid:'25.3'};raw.patterns[pattern].depth='.60';
  const adapted=adapt(raw),draft=deriveDraftState(raw,dimensionSnapshot(DEFAULTS));
  assert.equal(Boolean(adapted.values),valid,`${pattern}/${wall} adapter`);assert.equal(draft.canGenerate,valid,`${pattern}/${wall} draft`);
  const candidate={...adapt({...raw,wall:'4.6'}).values,outer_diameter:30+2*Number(wall)};
  if(valid)assert.doesNotThrow(()=>snapshot(candidate));else assert.throws(()=>snapshot(candidate),/wall below/);
 }
});
test('Rings and Spiral allocation errors identify only adjustable participants and their own family',()=>{
 for(const pattern of ['rings','spiral']){
  const raw={...DEFAULTS,patterns:patternMemories(),pattern,height:'305',auto:false,lid:'20'};raw.patterns[pattern].size='4';
  const state=deriveDraftState(raw,dimensionSnapshot(DEFAULTS)),error=state.issues.find(x=>x.id==='pattern-source');
  assert.deepEqual(error.fields,['pattern','pattern-size','height','ends','lid']);
  assert.match(adapt(raw).errors.height,new RegExp(`^${pattern[0].toUpperCase()+pattern.slice(1)} is too detailed`));
  assert.doesNotMatch(error.message,/diameter|depth|wall/);
 }
});
