import scad from '../../../openscad/laifen_case_customizer_v1.scad?raw';
import lockText from '../dependency-lock.json?raw';
import {argv,identity,sha256} from './schema.mjs';
import {DEFAULTS,adapt} from './adapter.mjs';
import {Generation,exactSTLBlob} from './lifecycle.mjs';
import {createViewer} from './viewer.mjs';
const $=id=>document.getElementById(id);
const stable=v=>Array.isArray(v)?`[${v.map(stable)}]`:v&&typeof v==='object'?`{${Object.keys(v).sort().map(k=>`${JSON.stringify(k)}:${stable(v[k])}`)}}`:JSON.stringify(v);
const sourceBytes=new TextEncoder().encode(scad);
let raw={...DEFAULTS},validation=adapt(raw),generated=null,downloadURL=null,viewer=null,busy=false;
try {viewer=createViewer($('viewer'),$('dimensions'),$('dimension-description'));}
catch { $('viewer-note').textContent='WebGL preview is unavailable. Generation and exact STL download still work.'; }
function invalidateDownload(){if(downloadURL)URL.revokeObjectURL(downloadURL);downloadURL=null;$('download').removeAttribute('href');$('download').setAttribute('aria-disabled','true');$('download').tabIndex=-1;}
function refreshFields(){
  validation=adapt(raw);
  for(const key of ['diameter','height','wall','ends','lid','drains','output']){
    const error=validation.errors[key];$(key).setAttribute('aria-invalid',String(Boolean(error)));$(`${key}-error`).hidden=!error;$(`${key}-error`).textContent=error||'';
  }
  $('auto-lid').setAttribute('aria-pressed',String(raw.auto));
  if(raw.auto && Number.isFinite(validation.summary.lid)) $('lid').value=String(Number(validation.summary.lid.toFixed(3)));
  for(const [id,key] of [['outside-diameter','outsideDiameter'],['outside-height','outsideHeight']])$(id).textContent=Number.isFinite(validation.summary[key]) && !Object.keys(validation.errors).length?`${Number(validation.summary[key].toFixed(3))} mm`:'—';
  $('generate').disabled=busy||!validation.values;
}
function state({busy:working,current,message}){
  busy=working;if(!current)invalidateDownload();
  $('status').textContent=message;$('cancel').hidden=!busy;$('cancel').disabled=!busy;$('reset').hidden=false;
  document.querySelector('.actions').dataset.current=String(current);
  $('stale').hidden=!generated||current;
  if(viewer){$('viewer-note').textContent=busy?message:generated?'':message;$('viewer-note').hidden=Boolean(generated)&&!busy;}
  refreshFields();
}
const generation=new Generation({
  prepare:async values=>{
    const [lockFingerprint,sourceHash]=await Promise.all([sha256(new TextEncoder().encode(stable(JSON.parse(lockText)))),sha256(sourceBytes)]);
    const key=await identity(sourceBytes,lockFingerprint,values);
    return {scad,argv:argv(values),identity:key,sourceHash,lockFingerprint};
  },
  createWorker:()=>new Worker(new URL('../workers/openscad.worker.js',import.meta.url),{type:'module'}),onState:state,
  onLog:text=>{$('diagnostics').textContent+=`${text}\n`;},
  onResult:result=>{
    generated=result;invalidateDownload();downloadURL=URL.createObjectURL(exactSTLBlob(result.bytes));
    $('download').href=downloadURL;$('download').download=`container-${result.values.output_mode}-${result.identity.slice(0,12)}.stl`;$('download').setAttribute('aria-disabled','false');$('download').tabIndex=0;
    if(viewer)try{viewer.install(result.bytes,result.values);$('viewer-note').hidden=true;}
    catch {viewer.clear();$('viewer-note').hidden=false;$('viewer-note').textContent='STL compiled, but the preview could not be displayed. The exact download is available.';viewer=null;}
  }
});
function edit(){generation.invalidate('Dimensions changed. Generate to update.');refreshFields();if(!validation.values)$('status').textContent='Check the highlighted dimensions.';}
for(const key of ['diameter','height','wall','ends','lid','drains','output']) {
  $(key).addEventListener('input',()=>{raw={...raw,[key]:$(key).value,...(key==='lid'?{auto:false}:{})};edit();});
  $(key).addEventListener('focus',()=>viewer?.setDimension(key));
}
$('auto-lid').onclick=()=>{raw={...raw,auto:true};edit();};
$('controls').onsubmit=event=>{event.preventDefault();if(!busy&&validation.values)$('generate').click();};
$('generate').onclick=()=>{refreshFields();if(!validation.values)return;$('diagnostics').textContent='';generation.generate(validation.values);};
$('cancel').onclick=()=>generation.invalidate('Cancelled. Generate when you are ready.');
$('reset').onclick=()=>{raw={...DEFAULTS};for(const key of ['diameter','height','wall','ends','lid','drains','output'])$(key).value=raw[key];generated=null;viewer?.clear();generation.invalidate('Dimensions reset. Generate to create the container.');refreshFields();};
$('camera').onclick=()=>viewer?.reset();
for(const mode of ['3d','cutaway'])$(`view-${mode}`).onclick=()=>{viewer?.setMode(mode);$('view-3d').setAttribute('aria-pressed',String(mode==='3d'));$('view-cutaway').setAttribute('aria-pressed',String(mode==='cutaway'));};
$('download').onclick=event=>{if(!downloadURL)event.preventDefault();};
refreshFields();$('generate').click();
