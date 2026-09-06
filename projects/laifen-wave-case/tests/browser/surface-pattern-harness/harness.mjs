import {createCustomizerController} from './src/controller.mjs';
import {Generation} from './src/lifecycle.mjs';
import {argv,identity,sha256} from './src/schema.mjs';

const $=id=>document.getElementById(id);
const stable=v=>Array.isArray(v)?`[${v.map(stable)}]`:v&&typeof v==='object'?`{${Object.keys(v).sort().map(k=>`${JSON.stringify(k)}:${stable(v[k])}`)}}`:JSON.stringify(v);
const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
const log=text=>{$('h-log').textContent+=`${new Date().toISOString().slice(11,23)} ${text}\n`;};
const checks=new Map();
function check(name,status,detail){checks.set(name,{status,detail});$('checks').replaceChildren(...[...checks].flatMap(([label,item])=>{const dt=document.createElement('dt');dt.textContent=label;const dd=document.createElement('dd');dd.className=`h-${item.status}`;dd.textContent=`${item.status.toUpperCase()} — ${item.detail}`;return [dt,dd];}));}
const bytesView=bytes=>bytes instanceof ArrayBuffer?new Uint8Array(bytes):new Uint8Array(bytes.buffer,bytes.byteOffset,bytes.byteLength);
const digest=bytes=>sha256(bytesView(bytes));

const binding=await (await fetch('../../../../../binding.json',{cache:'no-store'})).json();
const controllerPath='projects/laifen-wave-case/preview/openscad-wasm-simulator/src/controller.mjs';
$('binding').textContent=`Manifest ${binding.manifestHash}; controller ${binding.hashes[controllerPath]}; ${binding.entries} frozen paths.`;
check('Candidate binding','pass',`${binding.manifestHash.slice(0,16)}… / controller ${binding.hashes[controllerPath].slice(0,16)}…`);

const [scad,lockText]=await Promise.all([
  fetch('../../openscad/laifen_case_customizer_v1.scad',{cache:'no-store'}).then(r=>{if(!r.ok)throw Error(`SCAD ${r.status}`);return r.text();}),
  fetch('./dependency-lock.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw Error(`lock ${r.status}`);return r.text();})
]);
const sourceBytes=new TextEncoder().encode(scad);
const lockFingerprint=await sha256(new TextEncoder().encode(stable(JSON.parse(lockText))));
const sourceHash=await sha256(sourceBytes);
check('Frozen source and lock','pass',`SCAD ${sourceHash.slice(0,16)}…; lock ${lockFingerprint.slice(0,16)}…`);

const workers=[];
let cancelledWorker=null,raceWorker=null,latestWorker=null,cancelSnapshot=null;
class HoldingWorker {
  constructor(){
    this.number=workers.length+1; this.request=null; this.held=null; this.heldHash=null; this.onmessage=null; this.onerror=null; this.terminated=false;
    this.real=new Worker(new URL('./workers/openscad.worker.js',import.meta.url),{type:'module'}); workers.push(this);
    this.real.onerror=event=>this.onerror?.(event);
    this.real.onmessage=event=>{
      if(event.data?.type!=='result'){this.onmessage?.(event);return;}
      this.held=event.data; this.resultHandler=this.onmessage;
      digest(event.data.bytes).then(hash=>{this.heldHash=hash;const ok=this.request&&event.data.id===this.request.id&&event.data.identity===this.request.identity&&event.data.sourceHash===this.request.sourceHash&&event.data.lockFingerprint===this.request.lockFingerprint&&bytesView(event.data.bytes).byteLength>0;check(`Worker ${this.number} genuine result`,ok?'pass':'fail',`id ${event.data.id}; ${bytesView(event.data.bytes).byteLength} bytes; SHA-256 ${hash}`);log(`worker ${this.number} result held (id ${event.data.id})`);});
    };
  }
  postMessage(request){this.request=request;this.real.postMessage(request);log(`worker ${this.number} posted id ${request.id}, identity ${request.identity.slice(0,12)}…`);}
  terminate(){this.terminated=true;this.real.terminate();log(`worker ${this.number} terminated`);}
  deliver(){if(!this.held||!this.resultHandler)throw Error(`worker ${this.number} has no held result`);log(`delivering held worker ${this.number}`);this.resultHandler({data:this.held});}
}

const viewerState={installCount:0,clearCount:0,lastHash:null,lastValues:null};
const viewer={install(bytes,values){viewerState.installCount++;viewerState.lastValues=values;digest(bytes).then(hash=>{viewerState.lastHash=hash;log(`viewer installed ${hash}`);});},clear(){viewerState.clearCount++;viewerState.lastHash=null;},setDimension(){},setMode(){},reset(){}};
const blobs=[];
const nativeCreateObjectURL=URL.createObjectURL.bind(URL),nativeRevokeObjectURL=URL.revokeObjectURL.bind(URL);
function createObjectURL(blob){const url=nativeCreateObjectURL(blob);const record={url,size:blob.size,type:blob.type,hash:null};blobs.push(record);blob.arrayBuffer().then(bytes=>digest(bytes)).then(hash=>{record.hash=hash;log(`Blob ${blob.size} bytes ${hash}`);});return url;}
function revokeObjectURL(url){nativeRevokeObjectURL(url);const item=blobs.find(x=>x.url===url);if(item)item.revoked=true;}
const snapshot=()=>({status:$('status').textContent,current:document.querySelector('.actions').dataset.current,href:$('download').getAttribute('href'),ariaDisabled:$('download').getAttribute('aria-disabled'),installCount:viewerState.installCount,renderHash:viewerState.lastHash,blobCount:blobs.length,lastBlobHash:blobs.at(-1)?.hash??null});
const equivalent=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
async function waitForNewWorker(previous){for(let i=0;i<100;i++){if(workers.length>previous)return workers.at(-1);await sleep(25);}throw Error('candidate did not create a fresh worker');}

const controller=createCustomizerController({document,viewer,autoGenerate:false,createObjectURL,revokeObjectURL,createGeneration:callbacks=>new Generation({
  prepare:async values=>{
    const vector=argv(values),key=await identity(sourceBytes,lockFingerprint,values);
    const expected={surface_style:'diamond',diamond_axial_pitch:'4.8',diamond_arc_pitch:'3.63',diamond_depth:'0.45',diamond_phase_deg:'0'};
    const assignments=vector.filter((_,i)=>i%2===1);
    const details=[];let ok=true;
    for(const [name,value] of Object.entries(expected)){const hits=assignments.filter(x=>x===`${name}=${name==='surface_style'?JSON.stringify(value):value}`);details.push(`${name}:${hits.length}`);ok&&=hits.length===1;}
    const plateauHits=[...scad.matchAll(/diamond_plateau_half_fraction\s*=\s*0\.18\s*;/g)].length;ok&&=plateauHits===1;details.push(`plateau-source:${plateauHits}`);
    check('Exact fixed pattern tuple',ok?'pass':'fail',details.join(', '));
    return {scad,argv:vector,identity:key,sourceHash,lockFingerprint};
  },createWorker:()=>new HoldingWorker(),...callbacks
})});
check('Actual candidate controller','pass',`initialized; raw pattern=${controller.getState().raw.pattern}`);

function setValue(id,value){const el=$(id);if(!el)throw Error(`missing ${id}`);el.value=value;el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));}
function chooseDiamond(){const radio=$('surface-diamond')||document.querySelector('input[type=radio][value=diamond]');if(!radio)throw Error('candidate Diamond radio absent');radio.click();}
function prepareBody(count='7'){chooseDiamond();setValue('output','body');setValue('drain-count',count);const state=controller.getState();if(state.raw.pattern!=='diamond'||!state.draft.generationValues)throw Error('candidate rejected Diamond body setup');}
function requireHeld(worker,label){if(!worker?.held)throw Error(`${label} is not held yet`);}
async function unchangedAfter(worker,before,name){worker.deliver();await sleep(250);const after=snapshot();check(name,equivalent(before,after)?'pass':'fail',equivalent(before,after)?`status/render/Blob/download unchanged: ${JSON.stringify(after)}`:`before ${JSON.stringify(before)} after ${JSON.stringify(after)}`);}
for(const id of ['h-start-cancel','h-cancel','h-deliver-cancelled','h-start-race','h-start-newer','h-deliver-superseded','h-deliver-latest']) $(id).onclick=async()=>{try{
  if(id==='h-start-cancel'){prepareBody('7');const previous=workers.length;$('generate').click();cancelledWorker=await waitForNewWorker(previous);check('Cancel late-result gate','pending','wait for worker 1 genuine result, then Cancel');}
  if(id==='h-cancel'){requireHeld(cancelledWorker,'job 1');$('cancel').click();cancelSnapshot=snapshot();check('Cancel state','pass',JSON.stringify(cancelSnapshot));}
  if(id==='h-deliver-cancelled'){if(!cancelSnapshot)throw Error('Cancel job 1 first');await unchangedAfter(cancelledWorker,cancelSnapshot,'Cancel late-result gate');}
  if(id==='h-start-race'){prepareBody('7');const previous=workers.length;$('generate').click();raceWorker=await waitForNewWorker(previous);check('Superseded result gate','pending','wait for worker 2 result, then start newer job');}
  if(id==='h-start-newer'){requireHeld(raceWorker,'job 2');setValue('drain-count','6');const previous=workers.length;$('generate').click();latestWorker=await waitForNewWorker(previous);check('Superseded result gate','pending','wait for worker 3 result, then deliver job 2 late');}
  if(id==='h-deliver-superseded'){requireHeld(latestWorker,'job 3');const before=snapshot();await unchangedAfter(raceWorker,before,'Superseded result gate');}
  if(id==='h-deliver-latest'){requireHeld(latestWorker,'job 3');const priorInstalls=viewerState.installCount,priorBlobs=blobs.length;latestWorker.deliver();await sleep(500);const now=snapshot(),same=latestWorker.heldHash&&viewerState.lastHash===latestWorker.heldHash&&blobs.at(-1)?.hash===latestWorker.heldHash;const ok=now.status==='Preview up to date'&&now.current==='true'&&now.ariaDisabled==='false'&&Boolean(now.href)&&viewerState.installCount===priorInstalls+1&&blobs.length===priorBlobs+1&&same;check('Latest result accepted',''+(ok?'pass':'fail'),`${JSON.stringify(now)}; held/view/Blob SHA ${latestWorker.heldHash}/${viewerState.lastHash}/${blobs.at(-1)?.hash}`);}
}catch(error){check(`Action ${id}`,'fail',error.message);log(error.stack||error);}};
log('Harness ready. It will not compile until a visible Start button is clicked.');
