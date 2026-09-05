import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import vm from 'node:vm';
const source=fs.readFileSync(new URL('../preview/measurement-gate.html',import.meta.url),'utf8'),script=source.match(/<script>([\s\S]*?)<\/script>/)[1];
function app(w=360){class E{constructor(v=''){this.value=v;this.dataset={};this._innerHTML='';this._textContent='';this.attrs={};this.l={}}get innerHTML(){return this._innerHTML}set innerHTML(v){this._innerHTML=v;this._textContent=''}get textContent(){return this._textContent}set textContent(v){this._textContent=v;this._innerHTML=''}addEventListener(n,f){this.l[n]=f}fire(n){this.l[n]?.()}setAttribute(k,v){this.attrs[k]=v}getBoundingClientRect(){return{width:w}}}const f=Object.fromEntries([...source.matchAll(/<input[^>]*data-key="(\w+)"[^>]*value="([^"]+)"/g)].map(([,k,v])=>{let e=new E(v);e.dataset.key=k;return[k,e]})),u=Object.fromEntries([...source.matchAll(/data-role="([^"]+)"/g)].map(([,k])=>[k,new E()])),b=[...source.matchAll(/data-preset="([^"]+)"/g)].map(([,v])=>{let e=new E;e.dataset.preset=v;return e}),r={querySelector:s=>u[s.match(/data-role="([^"]+)"/)[1]],querySelectorAll:s=>s==='input[data-key]'?Object.values(f):b},c={document:{getElementById:()=>r},window:{},ResizeObserver:class{observe(){}}};vm.createContext(c);vm.runInContext(script,c);return{f,u,b,compute:c.window.__laifenMeasurementGate.compute,set(x){for(const[k,v]of Object.entries(x))f[k].value=String(v);f.L.fire('input')}}}
test('fixed bore arithmetic and stepped z references survive D edits',()=>{for(const w of [360,736]){let a=app(w);for(const D of [29,30,31]){a.set({D});let d=a.compute(Object.fromEntries(Object.entries(a.f).map(([k,e])=>[k,Number(e.value)])));assert.equal(d.lowerGap,(30-D)/2);assert.equal(d.upperGap,(31-D)/2);assert.match(a.u.section.innerHTML,/lower-id-span/);assert.match(a.u.section.innerHTML,/upper-id-span/);assert.match(a.u.section.innerHTML,/z137/);assert.match(a.u.section.innerHTML,/z132/);assert.equal(a.u.section.attrs.viewBox.split(' ')[2],String(w))}}});
test('q preserves envelope size and endpoint state',()=>{let a=app(),size;for(const q of [0,.5,1]){a.set({q});let t=a.u.section.innerHTML.match(/<rect[^>]*data-geometry="device"[^>]*>/)[0],s=t.match(/width="([^"]+)".*height="([^"]+)"/);size??=s.slice(1);assert.deepEqual(s.slice(1),size)}a.set({q:0});assert.match(a.u.state.textContent,/底端接觸/);a.set({q:1});assert.match(a.u.state.textContent,/頂端接觸/);a.set({q:0,slack:0});assert.match(a.u.state.textContent,/兩端接觸/)});
test('invalid clears and contact warning clears after restore',()=>{for(const x of [{D:''},{L:'Infinity'},{L:137,slack:0},{L:'1e308',slack:5},{q:2}]){let a=app();a.set(x);assert.match(a.u.error.textContent,/有限數值/);for(const k of ['section','state','gaps','targets','dimensions'])assert.equal(a.u[k].innerHTML,'')}let a=app();a.set({D:31});assert.match(a.u.targets.textContent,/接觸／干涉/);assert.doesNotMatch(a.u.targets.textContent,/<1|未達 1/);a.set({D:29});assert.equal(a.u.targets.textContent,'')});
test('joint labels have separated coordinates and gravity points down',()=>{let a=app(),s=a.u.section.innerHTML;const y=n=>Number(s.match(new RegExp(`data-joint-label="${n}"[^>]*y="([^"]+)"`))[1]);assert.ok(Math.abs(y('neck')-y('mouth'))>=12);assert.ok(Math.abs(y('mouth')-y('band'))>=12);assert.match(s,/data-geometry="neck-leader"/);assert.match(s,/data-geometry="mouth-leader"/);assert.match(s,/data-geometry="band-leader"/);assert.match(s,/data-geometry="gravity"/);assert.match(s,/ v 32 l -4 -6/)});
test('scope excludes radial control and finalized joint claims',()=>{let a=app();assert.deepEqual(Object.keys(a.f),['L','D','slack','q']);assert.match(source,/實際列印內徑及配合仍未知/);assert.match(source,/pending-joint-band/);assert.doesNotMatch(source,/data-key="radial"/);assert.doesNotMatch(source,/fetch\(/)});
test('decimal slack remains renderable at center and both endpoint presets',()=>{
 for(const slack of [.1,5.1])for(const q of [0,.5,1]){
  const a=app();a.set({slack,q});const d=a.compute({L:208,D:29,slack,q});
  assert.ok(d);assert.ok(Math.abs(d.C-(208+slack))<1e-12);assert.ok(Math.abs(d.bottom+d.top-slack)<1e-12);
  assert.equal(d.lowerGap,.5);assert.equal(d.upperGap,1);assert.equal(a.u.error.textContent,'');
  assert.match(a.u.section.innerHTML,/data-geometry="device"/);assert.doesNotMatch(a.u.section.innerHTML,/NaN|Infinity/);
  if(q===0)assert.match(a.u.state.textContent,/底端接觸/);if(q===1)assert.match(a.u.state.textContent,/頂端接觸/);
 }
});
test('lost positive increments clear geometry and stale contact warnings',()=>{
 for(const values of [{L:'1e308',slack:5},{L:'1e17',slack:0},{slack:'5e-324',q:.5},{D:'5e-324'}]){
  const a=app();a.set({D:31});assert.ok(a.u.targets.textContent);a.set(values);
  assert.ok(a.u.error.textContent);for(const k of ['section','state','gaps','targets','dimensions'])assert.equal(a.u[k].innerHTML,'');
 }
});
test('rendered geometry clears on huge finite D and restores at both layouts',()=>{
 for(const w of [360,736]){
  const a=app(w),numbers=svg=>[...svg.matchAll(/\s(?:x|y|width|height|d|data-scale)="([^"]*)"/g)].flatMap(([,v])=>[...v.matchAll(/-?\d+(?:\.\d+)?(?:e[+-]?\d+)?/gi)].map(m=>Number(m[0])));
  assert.match(a.u.section.innerHTML,/data-geometry="device"/);assert.ok(numbers(a.u.section.innerHTML).every(Number.isFinite));assert.ok(a.u.section.attrs.viewBox.split(' ').map(Number).every(Number.isFinite));
  a.set({D:'1.7e308'});assert.ok(a.u.error.textContent);for(const k of ['section','state','gaps','targets','dimensions']){assert.equal(a.u[k].innerHTML,'');assert.equal(a.u[k].textContent,'')}assert.doesNotMatch(a.u.section.innerHTML,/NaN|Infinity/);
  a.set({D:29});assert.equal(a.u.error.textContent,'');assert.match(a.u.section.innerHTML,/data-geometry="device"/);assert.ok(numbers(a.u.section.innerHTML).every(Number.isFinite));assert.ok(a.u.section.attrs.viewBox.split(' ').map(Number).every(Number.isFinite));assert.match(a.u.gaps.innerHTML,/每側 0.5 mm/);
 }
});
test('actual emitted SVG exterior leaders and anchors clear the maximum exterior at both layouts and changed scales',()=>{
 for(const w of [360,736])for(const L of [140,208,400]){
  const a=app(w);a.set({L});const svg=a.u.section.innerHTML,scale=Number(svg.match(/data-scale="([^"]+)"/)[1]);
  const exterior=w*.38+17.9*scale;
  for(const name of ['neck','mouth','band']){
   const path=svg.match(new RegExp(`data-geometry="${name}-leader" d="([^"]+)"`))[1];
   const coords=path.match(/^M ([\d.e+-]+) ([\d.e+-]+) H ([\d.e+-]+) V ([\d.e+-]+)$/).slice(1).map(Number);
   assert.ok(coords.every(Number.isFinite));assert.ok(coords[0]>exterior);assert.ok(coords[2]>exterior);
   const anchor=Number(svg.match(new RegExp(`data-joint-label="${name}" x="([^"]+)"`))[1]);assert.ok(anchor>exterior&&anchor<w);
  }
  const stop=svg.match(/data-geometry="external-stop"><path[^>]*d="M ([\d.e+-]+) ([\d.e+-]+) H ([\d.e+-]+)"/).slice(1).map(Number);
  assert.ok(stop[0]>exterior&&stop[2]>exterior);
 }
});
