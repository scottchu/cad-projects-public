import {DEFAULTS} from './adapter.mjs';
import {DIMENSIONS,deriveDraftState,dimensionSnapshot} from './bounds.mjs';
import {bindRange} from './controls.mjs';
import {exactSTLBlob} from './lifecycle.mjs';

const FIELDS=['diameter','height','wall','ends','lid','output'];
const rounded=value=>Number(value.toFixed(3));

export function createCustomizerController({document,createGeneration,viewer=null,defaults=DEFAULTS,autoGenerate=true,createObjectURL=blob=>URL.createObjectURL(blob),revokeObjectURL=url=>URL.revokeObjectURL(url)}) {
  const $=id=>document.getElementById(id);
  let raw={...defaults,drainCount:defaults.drainCount??'7'},lastValidDimensions=dimensionSnapshot(defaults),draft=deriveDraftState(raw,lastValidDimensions);
  let generated=null,downloadURL=null,busy=false,draftDirty=false;

  function invalidateDownload(){if(downloadURL)revokeObjectURL(downloadURL);downloadURL=null;$('download').removeAttribute('href');$('download').setAttribute('aria-disabled','true');$('download').tabIndex=-1;}
  function refreshFields(){
    draft=deriveDraftState(raw,lastValidDimensions);lastValidDimensions=draft.nextLastValidDimensions;
    const coupledFields=new Set(draft.issues.filter(item=>item.type==='coupled').flatMap(item=>item.fields));
    for(const key of FIELDS){
      const error=draft.fieldErrors[key]||'';
      $(key).setAttribute('aria-invalid',String(Boolean(error)||coupledFields.has(key)));
      $(`${key}-error`).hidden=!error;$(`${key}-error`).textContent=error;
      const described=[`${key}-rule`,`${key}-error`,...(coupledFields.has(key)?['dimension-form-error']:[])].filter(id=>document.getElementById(id));
      $(key).setAttribute('aria-describedby',described.join(' '));
    }
    $('dimension-form-error').hidden=!draft.formError;$('dimension-form-error').textContent=draft.formError;
    $('auto-lid').checked=raw.auto;$('lid').readOnly=raw.auto;
    $('drains-top').checked=raw.drains==='top'||raw.drains==='both';
    $('drains-bottom').checked=raw.drains==='bottom'||raw.drains==='both';
    const drainError=draft.fieldErrors.drains||'';
    $('drains').setAttribute('aria-invalid',String(Boolean(drainError)));
    $('drains-error').hidden=!drainError;$('drains-error').textContent=drainError;
    const patternError=draft.fieldErrors.pattern||'';
    $('surface-pattern').setAttribute('aria-invalid',String(Boolean(patternError)||coupledFields.has('pattern')));
    $('surface-pattern-error').hidden=!patternError;$('surface-pattern-error').textContent=patternError;
    $('surface-pattern').setAttribute('aria-describedby',`surface-pattern-rule ${patternError?'surface-pattern-error':coupledFields.has('pattern')?'dimension-form-error':'surface-pattern-error'}`);
    for(const pattern of ['smooth','diamond'])$('surface-'+pattern).checked=raw.pattern===pattern;
    const count=draft.drainCount,countError=draft.fieldErrors.drainCount||'';
    $('drain-count').value=raw.drainCount;$('drain-count').disabled=!count.active;$('drain-count').setAttribute('aria-invalid',String(Boolean(countError)||coupledFields.has('drainCount')));
    $('drain-count-error').hidden=!countError;$('drain-count-error').textContent=countError;$('drain-count-rule').textContent=count.rule;
    const countRange=$('drain-count-range');countRange.disabled=count.disabled;
    if(count.max!==null){countRange.min='1';countRange.max=String(count.max);countRange.step='1';const n=Number(raw.drainCount);countRange.value=String(Number.isInteger(n)&&n>=1&&n<=count.max?n:count.max);}
    countRange.setAttribute('aria-invalid',String(Boolean(countError)||coupledFields.has('drainCount')));countRange.setAttribute('aria-describedby','drain-count-rule drain-count-error dimension-form-error');
    $('output').value=raw.output;
    for(const key of DIMENSIONS){
      const input=$(key),range=$(`${key}-range`),slider=draft.sliders[key];
      const autoLid=Number.isFinite(draft.summary.lid)?draft.summary.lid:slider.min;
      input.value=key==='lid'&&raw.auto?String(rounded(autoLid)):raw[key];
      range.disabled=slider.disabled;$(`${key}-rule`).textContent=slider.rule;
      if(slider.min!==null){range.min=String(slider.min);range.max=String(slider.max);range.step=String(slider.step);const sourceValue=key==='lid'&&raw.auto?slider.min:Number((slider.source==='current'?raw:lastValidDimensions)[key]);range.value=String(Number.isFinite(sourceValue)?sourceValue:slider.min);}
      const rangeDescription=[`${key}-rule`,`${key}-error`,...(coupledFields.has(key)?['dimension-form-error']:[])];range.setAttribute('aria-describedby',rangeDescription.join(' '));
      range.setAttribute('aria-invalid',String(coupledFields.has(key)||Boolean(draft.fieldErrors[key])));
    }
    for(const [id,key] of [['outside-diameter','outsideDiameter'],['outside-height','outsideHeight']])$(id).textContent=Number.isFinite(draft.summary[key])?`${rounded(draft.summary[key])} mm`:'—';
    $('generate').disabled=busy||!draft.canGenerate;
  }
  function state({busy:working,current,message}){
    busy=working;if(!current)invalidateDownload();if(current)draftDirty=false;
    $('status').textContent=message;$('generate').hidden=busy;$('cancel').hidden=!busy;$('cancel').disabled=!busy;
    document.querySelector('.actions').dataset.current=String(current);$('stale').hidden=!generated||current;
    if(viewer){$('viewer-note').textContent=busy?message:generated?'':message;$('viewer-note').hidden=Boolean(generated)&&!busy;}
    refreshFields();
  }
  const generation=createGeneration({onState:state,onLog:text=>{$('diagnostics').textContent+=`${text}\n`;},onResult:result=>{
    generated=result;invalidateDownload();downloadURL=createObjectURL(exactSTLBlob(result.bytes));
    $('download').href=downloadURL;$('download').download=`container-${result.values.output_mode}-${result.identity.slice(0,12)}.stl`;$('download').setAttribute('aria-disabled','false');$('download').tabIndex=0;
    if(viewer)try{viewer.install(result.bytes,result.values);$('viewer-note').hidden=true;}catch{viewer.clear();$('viewer-note').hidden=false;$('viewer-note').textContent='STL compiled, but the preview could not be displayed. The exact download is available.';viewer=null;}
  }});
  function edit(){if(busy||!draftDirty){generation.invalidate('Dimensions changed. Generate to update.');draftDirty=true;}refreshFields();$('status').textContent=draft.canGenerate?'Dimensions changed. Generate to update.':'Check the highlighted dimensions.';}

  for(const key of FIELDS){
    $(key).addEventListener('input',()=>{raw={...raw,[key]:$(key).value,...(key==='lid'?{auto:false}:{})};edit();});
    $(key).addEventListener('focus',()=>viewer?.setDimension(key));
  }
  const updateDrains=()=>{
    const top=$('drains-top').checked,bottom=$('drains-bottom').checked;
    raw={...raw,drains:top?(bottom?'both':'top'):(bottom?'bottom':'none')};edit();
  };
  $('drains-top').addEventListener('change',updateDrains);
  $('drains-bottom').addEventListener('change',updateDrains);
  for(const pattern of ['smooth','diamond'])$('surface-'+pattern).addEventListener('change',()=>{if($('surface-'+pattern).checked){raw={...raw,pattern};edit();}});
  $('drain-count').addEventListener('input',()=>{raw={...raw,drainCount:$('drain-count').value};edit();});
  bindRange({input:$('drain-count'),range:$('drain-count-range'),onChange:value=>{const count=draft.drainCount,n=Number(value);if(count.disabled||!Number.isInteger(n)||n<1||n>count.max){refreshFields();return false;}raw={...raw,drainCount:value};edit();return true;}});
  $('auto-lid').onchange=()=>{const auto=$('auto-lid').checked;raw={...raw,auto,...(!auto&&raw.auto?{lid:$('lid').value}:{})};edit();};
  for(const key of DIMENSIONS)bindRange({input:$(key),range:$(`${key}-range`),onChange:value=>{const slider=draft.sliders[key],number=Number(value);if(slider.disabled||!Number.isFinite(number)||number<slider.min||number>slider.max){refreshFields();return false;}raw={...raw,[key]:value};viewer?.setDimension(key);edit();return true;},onFocus:()=>viewer?.setDimension(key)});
  $('controls').onsubmit=event=>{event.preventDefault();if(!busy&&draft.canGenerate)$('generate').click();};
  $('generate').onclick=()=>{refreshFields();if(!draft.generationValues)return;draftDirty=false;$('diagnostics').textContent='';generation.generate(draft.generationValues);};
  $('cancel').onclick=()=>generation.invalidate('Cancelled. Generate when you are ready.');
  $('reset').onclick=()=>{raw={...defaults,drainCount:defaults.drainCount??'7'};lastValidDimensions=dimensionSnapshot(defaults);draftDirty=false;generated=null;viewer?.clear();generation.invalidate('Dimensions reset. Generate to create the container.');refreshFields();};
  $('camera').onclick=()=>viewer?.reset();
  for(const mode of ['3d','cutaway'])$(`view-${mode}`).onclick=()=>{viewer?.setMode(mode);$('view-3d').setAttribute('aria-pressed',String(mode==='3d'));$('view-cutaway').setAttribute('aria-pressed',String(mode==='cutaway'));};
  $('download').onclick=event=>{if(!downloadURL)event.preventDefault();};
  refreshFields();if(autoGenerate)$('generate').click();
  return Object.freeze({refresh:refreshFields,getState:()=>({raw:{...raw},lastValidDimensions:{...lastValidDimensions},draft,busy,generated,downloadURL})});
}
