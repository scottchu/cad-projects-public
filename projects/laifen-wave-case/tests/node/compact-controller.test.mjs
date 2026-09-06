import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createCustomizerController} from '../../preview/openscad-wasm-simulator/src/controller.mjs';
import {adapt,DEFAULTS} from '../../preview/openscad-wasm-simulator/src/adapter.mjs';

class FakeElement {
  constructor(value=''){this.value=value;this.textContent='';this.hidden=false;this.disabled=false;this.checked=false;this.readOnly=false;this.dataset={};this.attributes={};this.listeners={};this.tabIndex=0;}
  setAttribute(name,value){this.attributes[name]=String(value);}
  getAttribute(name){return this.attributes[name];}
  removeAttribute(name){delete this.attributes[name];delete this[name];}
  addEventListener(name,listener){(this.listeners[name]??=[]).push(listener);}
  dispatch(name){for(const listener of this.listeners[name]??[])listener({preventDefault(){}});}
  click(){if(!this.disabled&&!this.hidden)this.onclick?.({preventDefault(){}});}
}
function fakeDocument(){
  const ids=['diameter','height','wall','ends','lid','drains','drains-top','drains-bottom','drain-count','drain-count-range','drain-count-rule','drain-count-error','surface-pattern','surface-smooth','surface-diamond','surface-pattern-rule','surface-pattern-error','output','auto-lid','dimension-form-error','outside-diameter','outside-height','generate','cancel','status','download','diagnostics','stale','viewer-note','reset','camera','view-3d','view-cutaway','controls'];
  for(const key of ['diameter','height','wall','ends','lid'])ids.push(`${key}-range`,`${key}-rule`);
  for(const key of ['diameter','height','wall','ends','lid','drains','output'])ids.push(`${key}-error`);
  const elements=Object.fromEntries(ids.map(id=>[id,new FakeElement()]));
  Object.assign(elements.diameter,{value:'30'});Object.assign(elements.height,{value:'213'});Object.assign(elements.wall,{value:'4.5'});Object.assign(elements.ends,{value:'3'});Object.assign(elements.lid,{value:'84'});Object.assign(elements.output,{value:'assembled'});elements['drains-bottom'].checked=true;elements['surface-smooth'].checked=true;elements['auto-lid'].checked=true;elements.cancel.hidden=true;
  const actions=new FakeElement();return {elements,actions,getElementById:id=>elements[id],querySelector:selector=>selector==='.actions'?actions:null};
}
function setup(defaults=DEFAULTS){
  const document=fakeDocument(),calls={generate:[],invalidate:[]};let callbacks;
  const controller=createCustomizerController({document,defaults,autoGenerate:false,createGeneration:value=>{callbacks=value;return {generate(values){calls.generate.push(values);callbacks.onState({busy:true,current:false,message:'Loading compiler…'});},invalidate(message){calls.invalidate.push(message);callbacks.onState({busy:false,current:false,message});}};}});
  return {document,controller,calls,callbacks};
}
const edit=(document,key,value)=>{document.elements[key].value=value;document.elements[key].dispatch('input');};
const setDrains=(document,{top,bottom})=>{document.elements['drains-top'].checked=top;document.elements['drains-bottom'].checked=bottom;document.elements['drains-top'].dispatch('change');};

test('full controller renders coherent rules, errors, Generate state, and generation values',()=>{
  const {document,controller,calls}=setup(),e=document.elements;
  assert.equal(e['diameter-rule'].textContent,'Allowed now: 11–69 mm · lid is 1 mm wider');assert.equal(e.generate.disabled,false);
  edit(document,'diameter','');
  assert.equal(e.diameter.value,'');assert.equal(e.diameter.getAttribute('aria-invalid'),'true');assert.equal(e.generate.disabled,true);
  for(const key of ['diameter','height','wall','ends','lid']){assert.equal(e[`${key}-range`].disabled,true);assert.match(e[`${key}-rule`].textContent,/Last valid/);}
  e['diameter-range'].value='11';e['diameter-range'].dispatch('input');assert.equal(controller.getState().raw.diameter,'');assert.equal(e.diameter.value,'');
  const frozen=controller.getState().lastValidDimensions,rules=Object.fromEntries(['diameter','height','wall','ends','lid'].map(key=>[key,e[`${key}-rule`].textContent]));setDrains(document,{top:true,bottom:false});edit(document,'output','body');
  assert.deepEqual(controller.getState().lastValidDimensions,frozen);assert.deepEqual(Object.fromEntries(['diameter','height','wall','ends','lid'].map(key=>[key,e[`${key}-rule`].textContent])),rules);assert.equal(e['diameter-error'].textContent,'Enter a number in millimetres.');
  edit(document,'diameter','70');assert.equal(e.diameter.value,'70');assert.equal(e['diameter-error'].textContent,'Use a value from 10 to 69 mm.');
  e.generate.click();assert.equal(calls.generate.length,0);
  edit(document,'diameter','30');assert.equal(e.generate.disabled,false);e.generate.click();assert.equal(calls.generate.length,1);assert.equal(calls.generate[0].body_bore,30);assert.equal(calls.generate[0].drainage_mode,'top');assert.equal(calls.generate[0].output_mode,'body');
});

test('full controller associates one coupled error with all participants and is order independent',()=>{
  const first=setup(),second=setup();
  for(const {document} of [first,second]){document.elements['auto-lid'].checked=false;document.elements['auto-lid'].onchange();}
  for(const [key,value] of [['height','30'],['ends','7'],['lid','35']])edit(first.document,key,value);
  for(const [key,value] of [['lid','35'],['ends','7'],['height','30']])edit(second.document,key,value);
  for(const run of [first,second]){
    const e=run.document.elements,state=run.controller.getState();assert.equal(e['dimension-form-error'].hidden,false);assert.match(e['dimension-form-error'].textContent,/less than inside height/);
    for(const key of ['height','ends','lid']){assert.equal(e[key].getAttribute('aria-invalid'),'true');assert.match(e[key].getAttribute('aria-describedby'),/dimension-form-error/);}
    assert.equal(e.generate.disabled,true);assert.equal(state.draft.sliders.diameter.source,'last-valid');
  }
  assert.deepEqual(first.controller.getState().draft.issues,second.controller.getState().draft.issues);
  edit(first.document,'ends','7.1');assert.equal(first.document.elements['dimension-form-error'].hidden,true);assert.equal(first.document.elements.generate.disabled,false);
});

test('Auto coupled error omits manual lid and keeps the current derived readout',()=>{
  const {document}=setup(),e=document.elements;edit(document,'height','36');edit(document,'ends','7.5');
  assert.match(e['dimension-form-error'].textContent,/Auto lid height/);assert.equal(e.height.getAttribute('aria-invalid'),'true');assert.equal(e.ends.getAttribute('aria-invalid'),'true');assert.equal(e.lid.getAttribute('aria-invalid'),'false');assert.equal(e.lid.readOnly,true);assert.equal(e.lid.value,'19.562');
  edit(document,'height','36.2');edit(document,'ends','8');assert.equal(e['dimension-form-error'].hidden,true);assert.equal(e.generate.disabled,false);
});

test('enabled slider updates exact draft without generation and an edit cancels active generation',()=>{
  const {document,controller,calls}=setup(),e=document.elements,range=e['diameter-range'];
  range.value='11';range.dispatch('input');assert.equal(e.diameter.value,'11');assert.equal(controller.getState().raw.diameter,'11');assert.equal(e['outside-diameter'].textContent,'20 mm');assert.equal(calls.generate.length,0);
  e.generate.click();assert.equal(calls.generate.length,1);assert.equal(e.cancel.hidden,false);
  edit(document,'wall','5');assert.equal(calls.invalidate.at(-1),'Dimensions changed. Generate to update.');assert.equal(e.cancel.hidden,true);assert.equal(controller.getState().busy,false);assert.equal(calls.generate.length,1);
});

test('Auto/manual transition and reset restore complete defaults without generation',()=>{
  const {document,controller,calls}=setup(),e=document.elements;
  assert.equal(e.lid.value,'84');e['auto-lid'].checked=false;e['auto-lid'].onchange();assert.equal(controller.getState().raw.lid,'84');assert.equal(e.lid.readOnly,false);
  edit(document,'lid','90');setDrains(document,{top:false,bottom:false});edit(document,'output','cap');e.reset.click();
  assert.deepEqual(controller.getState().raw,{diameter:'30',height:'213',wall:'4.5',ends:'3',lid:'84',auto:true,drains:'bottom',drainCount:'7',pattern:'smooth',output:'assembled'});assert.equal(e['auto-lid'].checked,true);assert.equal(e['drains-top'].checked,false);assert.equal(e['drains-bottom'].checked,true);assert.equal(e['surface-smooth'].checked,true);assert.equal(e.output.value,'assembled');assert.equal(calls.generate.length,0);
});
test('surface pattern preserves its raw choice, maps the fixed tuple, and offers a wall repair without pausing it',()=>{
  const {document,controller,calls}=setup(),e=document.elements;
  e['surface-diamond'].checked=true;e['surface-diamond'].dispatch('change');
  assert.equal(controller.getState().raw.pattern,'diamond');assert.equal(e.generate.disabled,false);e.generate.click();assert.equal(calls.generate.at(-1).surface_style,'diamond');assert.equal(calls.generate.at(-1).diamond_axial_pitch,4.8);
  edit(document,'wall','4.3');assert.equal(controller.getState().raw.wall,'4.3');assert.equal(e.generate.disabled,true);assert.equal(e['surface-pattern-error'].hidden,true);assert.equal(e['surface-pattern-error'].textContent,'');assert.match(e['dimension-form-error'].textContent,/at least 4.4/);assert.equal((e['dimension-form-error'].textContent.match(/at least 4\.4/g)||[]).length,1);assert.equal(e['surface-pattern'].getAttribute('aria-describedby'),'surface-pattern-rule dimension-form-error');assert.equal(e['wall-range'].disabled,false);assert.equal(e['wall-range'].min,'4.4');
  e['surface-smooth'].checked=true;e['surface-smooth'].dispatch('change');assert.equal(controller.getState().raw.pattern,'smooth');assert.equal(e.generate.disabled,false);assert.equal(e['wall-range'].min,'4');
});
test('surface-pattern local error is reserved for a direct invalid selection',()=>{
  const {document}=setup({...DEFAULTS,pattern:'unknown'}),e=document.elements;
  assert.equal(e['surface-pattern-error'].hidden,false);assert.equal(e['surface-pattern-error'].textContent,'Choose a surface pattern.');assert.equal(e['surface-pattern'].getAttribute('aria-describedby'),'surface-pattern-rule surface-pattern-error');assert.equal(e['dimension-form-error'].hidden,true);
});

test('drain count preserves raw invalid text while off and enforces dynamic active limits',()=>{
  const {document,controller}=setup(),e=document.elements;
  assert.equal(e['drain-count-range'].max,'17');
  edit(document,'drain-count','18');assert.match(e['dimension-form-error'].textContent,/at most 17/);assert.equal(e.generate.disabled,true);assert.equal(e['drain-count-range'].value,'17');assert.equal(controller.getState().raw.drainCount,'18');
  setDrains(document,{top:false,bottom:false});assert.equal(e['drain-count'].disabled,true);assert.equal(e.generate.disabled,false);assert.equal(controller.getState().raw.drainCount,'18');
  setDrains(document,{top:false,bottom:true});assert.equal(e['drain-count'].disabled,false);assert.match(e['dimension-form-error'].textContent,/at most 17/);
  edit(document,'diameter','11');edit(document,'drain-count','7');assert.equal(e['drain-count-range'].max,'7');assert.equal(e.generate.disabled,false);
  edit(document,'diameter','10');assert.match(e['dimension-form-error'].textContent,/at most 1/);
});

test('malformed count disables its paired range and adapter never substitutes an active raw count',()=>{
  const {document}=setup(),e=document.elements;
  edit(document,'drain-count','x');assert.equal(e['drain-count-range'].disabled,true);assert.equal(e['drain-count'].disabled,false);assert.equal(e['drain-count'].value,'x');assert.equal(e['drain-count-error'].textContent,'Enter a whole number.');
  edit(document,'drain-count','');assert.equal(e['drain-count'].disabled,false);edit(document,'diameter','');assert.equal(e['drain-count'].disabled,false);
  const invalid=adapt({...DEFAULTS,drainCount:'8',diameter:'11'});assert.match(invalid.errors.drainCount,/at most 7/);assert.match(invalid.errors.diameter,/at most 7/);
  const valid=adapt({...DEFAULTS,drainCount:'17'});assert.equal(valid.values.drain_count,17);
  const off=adapt({...DEFAULTS,drains:'none',drainCount:'x'});assert.equal(off.values.drain_count,7);
});

test('independent drain checkboxes map all four modes, preserve invalid drafts, and cancel active work',()=>{
  const {document,controller,calls}=setup(),e=document.elements;
  for(const [top,bottom,mode] of [[false,false,'none'],[true,false,'top'],[false,true,'bottom'],[true,true,'both']]){
    setDrains(document,{top,bottom});assert.equal(controller.getState().raw.drains,mode);assert.equal(e['drains-top'].checked,top);assert.equal(e['drains-bottom'].checked,bottom);assert.equal(calls.generate.length,0);
  }
  edit(document,'diameter','');setDrains(document,{top:true,bottom:true});assert.equal(controller.getState().raw.drains,'both');assert.equal(e['diameter-error'].textContent,'Enter a number in millimetres.');assert.equal(e.generate.disabled,true);
  edit(document,'diameter','30');e.generate.click();assert.equal(calls.generate.length,1);setDrains(document,{top:false,bottom:false});assert.equal(calls.invalidate.at(-1),'Dimensions changed. Generate to update.');assert.equal(controller.getState().busy,false);assert.equal(controller.getState().raw.drains,'none');
});
