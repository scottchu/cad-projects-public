import {test} from 'node:test';
import assert from 'node:assert/strict';
import {adapt,DEFAULTS} from '../../preview/openscad-wasm-simulator/src/adapter.mjs';
import {BROWSER_PRESET,snapshot} from '../../preview/openscad-wasm-simulator/src/schema.mjs';
import {Generation,exactSTLBlob} from '../../preview/openscad-wasm-simulator/src/lifecycle.mjs';
test('adapter preserves every baseline parameter and scales lid without changing the target height',()=>{
 assert.deepEqual(adapt(DEFAULTS).values,BROWSER_PRESET);
 const short=adapt({...DEFAULTS,height:'60'});assert.equal(short.values.device_length,55);assert.equal(short.values.split_distance_from_top,66*(84/219));
 const daily=adapt({...DEFAULTS,diameter:'39',wall:'4',ends:'4'});assert.equal(daily.values.outer_diameter,47);assert.equal(daily.values.cap_bore,40);assert.equal(daily.values.floor_thickness,4);
});
test('rejects impossible and blank dimensions without clamping or coercing to zero',()=>{
 for(const value of ['', ' ', 'NaN','Infinity','0'])assert.ok(adapt({...DEFAULTS,diameter:value}).errors.diameter,value);
 assert.match(adapt({...DEFAULTS,diameter:'39',wall:'3'}).errors.wall,/at least 4 mm/);
 assert.ok(adapt({...DEFAULTS,height:'20'}).errors.height);
 assert.ok(adapt({...DEFAULTS,auto:false,lid:'230'}).errors.lid);
 assert.ok(adapt({...DEFAULTS,diameter:'69',wall:'6'}).errors.wall);
 const tiny=adapt({...DEFAULTS,diameter:'10',wall:'5'});assert.equal(tiny.values.drain_ring_radius,3);
});
test('advertised 4mm minimum avoids unstable source residual boundary',()=>{
 assert.throws(()=>snapshot({...BROWSER_PRESET,body_bore:12.5,cap_bore:13.5,outer_diameter:20.4,drain_ring_radius:4.25}),/thread wall constraint/);
 assert.ok(adapt({...DEFAULTS,diameter:'12.5',wall:'4'}).values);
});
const deferred=()=>{let resolve;const promise=new Promise(r=>resolve=r);return {promise,resolve};};
function harness(prepare=async()=>({identity:'key',sourceHash:'source',lockFingerprint:'lock'})){
 const states=[],results=[],logs=[],workers=[],timers=[];
 const generation=new Generation({prepare,onState:s=>states.push(s),onResult:r=>results.push(r),onLog:l=>logs.push(l),createWorker:()=>{const w={terminate(){this.stopped=true;},postMessage(r){this.request=r;}};workers.push(w);return w;},setTimer:cb=>{timers.push(cb);return timers.length;},clearTimer:()=>{}});
 const result=(worker,extra={})=>worker.onmessage({data:{id:worker.request.id,type:'result',identity:'key',sourceHash:'source',lockFingerprint:'lock',bytes:new Uint8Array([3,1,4]).buffer,...extra}});
 return {generation,states,results,logs,workers,timers,result};
}
for(const reason of ['Cancelled','Dimensions reset','Dimensions changed'])test(`${reason} during identity await cannot create a worker`,async()=>{
 const d=deferred(),h=harness(()=>d.promise),pending=h.generation.generate(BROWSER_PRESET);
 assert.equal(h.states[0].busy,true);h.generation.invalidate(reason);d.resolve({identity:'key'});await pending;
 assert.equal(h.workers.length,0);assert.equal(h.states.at(-1).message,reason);assert.equal(h.results.length,0);
});
test('superseded identity and queued worker events cannot replace current output',async()=>{
 const d=deferred();let calls=0;const h=harness(()=>++calls===1?d.promise:Promise.resolve({identity:'key',sourceHash:'source',lockFingerprint:'lock'}));
 const old=h.generation.generate(BROWSER_PRESET);await h.generation.generate(BROWSER_PRESET);const worker=h.workers[0];
 d.resolve({identity:'old'});await old;assert.equal(h.workers.length,1);
 h.result(worker);assert.equal(h.results.length,1);h.result(worker);worker.onmessage({data:{id:worker.request.id,type:'log',text:'late'}});assert.equal(h.results.length,1);assert.deepEqual(h.logs,[]);
});
test('edit cancels active worker and queued result cannot become downloadable',async()=>{
 const h=harness();await h.generation.generate(BROWSER_PRESET);h.generation.invalidate('edit');h.result(h.workers[0]);assert.equal(h.results.length,0);assert.equal(h.workers[0].stopped,true);
});
test('timeout during identity work invalidates later continuation',async()=>{
 const d=deferred(),h=harness(()=>d.promise),pending=h.generation.generate(BROWSER_PRESET);h.timers[0]();d.resolve({identity:'key'});await pending;
 assert.equal(h.workers.length,0);assert.match(h.states.at(-1).message,/timed out/);
});
test('rejects mismatched result identity/source/lock and empty output',async()=>{
 for(const extra of [{identity:'wrong'},{sourceHash:'wrong'},{lockFingerprint:'wrong'},{bytes:new ArrayBuffer(0)}]){
 const h=harness();await h.generation.generate(BROWSER_PRESET);h.result(h.workers[0],extra);assert.equal(h.results.length,0);assert.equal(h.states.at(-1).current,false);
 }
});
test('download Blob preserves exact bytes including a subarray offset',async()=>{
 const bytes=new Uint8Array([99,2,7,8,99]).subarray(1,4);assert.deepEqual(new Uint8Array(await exactSTLBlob(bytes).arrayBuffer()),new Uint8Array([2,7,8]));
});

test('default timers preserve browser global receiver branding',async()=>{
 const originalSet=globalThis.setTimeout,originalClear=globalThis.clearTimeout;
 let sets=0,clears=0;
 try {
  globalThis.setTimeout=function(){assert.equal(this,globalThis,'setTimeout receiver');sets++;return 1;};
  globalThis.clearTimeout=function(){assert.equal(this,globalThis,'clearTimeout receiver');clears++;};
  const g=new Generation({prepare:async()=>({}),createWorker:()=>({postMessage(){},terminate(){}})});
  await g.generate(BROWSER_PRESET);g.invalidate('cancel');assert.equal(sets,1);assert.ok(clears>=2);
 } finally {globalThis.setTimeout=originalSet;globalThis.clearTimeout=originalClear;}
});

import {dimensionAnchor} from '../../preview/openscad-wasm-simulator/src/dimensions.mjs';
test('section anchors remain in plain body walls and solid ends across valid dimensions/drains',()=>{
 for(const dimensions of [DEFAULTS,{...DEFAULTS,height:'60',ends:'4',auto:false,lid:'60'},{...DEFAULTS,diameter:'10',wall:'5'},{...DEFAULTS,diameter:'69',wall:'4'}]) {
  for(const drains of ['none','top','bottom']) {
   const {values}=adapt({...dimensions,drains});assert.ok(values);
   const T=values.floor_thickness,seam=values.device_length+values.axial_allowance+2*T-values.split_distance_from_top;
   for(const key of ['diameter','wall']) {
    const {a,b}=dimensionAnchor(values,key);assert.ok(a[2]>T && a[2]<seam);assert.equal(a[2],b[2]);assert.ok(a[2]>values.end_chamfer);
   }
   const {a,b}=dimensionAnchor(values,'ends');assert.equal(a[2],0);assert.equal(b[2],T);assert.ok(a[0]<values.body_bore/2);
   assert.ok(a[0]<values.outer_diameter/2-values.end_chamfer);
   const centers=[[0,0],...Array.from({length:6},(_,i)=>[values.drain_ring_radius*Math.cos(i*Math.PI/3),values.drain_ring_radius*Math.sin(i*Math.PI/3)])];
   for(const [x,y] of centers)assert.ok(Math.hypot(a[0]-x,a[1]-y)>values.drain_diameter/2,`${drains}: anchor passes through a drain hole`);
  }
 }
});
