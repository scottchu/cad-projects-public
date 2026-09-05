import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const source = fs.readFileSync(new URL('../preview/measurement-gate.html', import.meta.url), 'utf8');
const script = source.match(/<script>([\s\S]*?)<\/script>/)[1];
function setup(width = 360) {
  class Element {
    constructor(value = '') { this.value = value; this.dataset = {}; this.innerHTML = ''; this.textContent = ''; this.attrs = {}; this.listeners = {}; }
    addEventListener(name, handler) { this.listeners[name] = handler; }
    fire(name) { this.listeners[name]?.(); }
    setAttribute(key, value) { this.attrs[key] = value; }
    getBoundingClientRect() { return {width}; }
  }
  const fields = Object.fromEntries([...source.matchAll(/<input[^>]*data-key="(\w+)"[^>]*value="([^"]+)"/g)].map(([,key,value]) => { const el = new Element(value); el.dataset.key = key; return [key,el]; }));
  const ui = Object.fromEntries([...source.matchAll(/data-role="([^"]+)"/g)].map(([,key]) => [key,new Element()]));
  const buttons = [...source.matchAll(/data-preset="([^"]+)"/g)].map(([,preset]) => {const el = new Element(); el.dataset.preset = preset; return el;});
  const root = {querySelector: selector => ui[selector.match(/data-role="([^"]+)"/)[1]], querySelectorAll: selector => selector === 'input[data-key]' ? Object.values(fields) : buttons};
  const context = {document:{getElementById:() => root}, window:{}, ResizeObserver:class{observe(){}}};
  vm.createContext(context); vm.runInContext(script, context);
  const set = changes => {for (const [key,value] of Object.entries(changes)) fields[key].value = String(value); fields.L.fire('input');};
  return {fields,ui,buttons,set,compute:context.window.__laifenMeasurementGate.compute};
}
const close = (a,b) => assert.ok(Math.abs(a-b) < 1e-8, `${a} != ${b}`);
function rect(svg, name) {
  const tag = svg.match(new RegExp(`<rect[^>]*data-geometry="${name}"[^>]*>`))?.[0];
  assert.ok(tag, `missing ${name}`);
  return Object.fromEntries([...tag.matchAll(/(x|y|width|height)="([^"]+)"/g)].map(([,key,value]) => [key,Number(value)]));
}
function finiteGeometry(svg) {
  assert.doesNotMatch(svg, /NaN|Infinity|undefined/);
  for (const [,name,value] of svg.matchAll(/\b(x|y|width|height|data-scale)="([^"]+)"/g)) assert.ok(Number.isFinite(Number(value)), `${name}=${value}`);
  for (const [,path] of svg.matchAll(/ d="([^"]+)"/g)) {
    assert.ok(path.match(/[-+]?\d*\.?\d+(?:e[-+]?\d+)?/gi)?.length, `empty path ${path}`);
    assert.doesNotMatch(path, /[{}$]/);
    for (const number of path.match(/[-+]?\d*\.?\d+(?:e[-+]?\d+)?/gi)) assert.ok(Number.isFinite(Number(number)));
  }
}
test('default/changed dimensions share one physical scale and floors exclude cavity', () => {
  for (const width of [360,736]) for (const changed of [{},{L:220,D:32,slack:8,radial:2}]) {
    const app = setup(width); app.set(changed);
    const p = Object.fromEntries(Object.entries(app.fields).map(([key,el]) => [key,Number(el.value)]));
    const d = app.compute(p), svg = app.ui.section.innerHTML;
    finiteGeometry(svg);
    const lower = rect(svg,'lower-floor'), upper = rect(svg,'upper-floor'), device = rect(svg,'device'), left = rect(svg,'left-wall'), right = rect(svg,'right-wall');
    const scale = device.height/p.L;
    close(device.width/p.D,scale);
    close(lower.height,3*scale); close(upper.height,3*scale);
    close(lower.y-(upper.y+upper.height),(p.L+p.slack)*scale);
    close(right.x-(left.x+left.width),(p.D+2*p.radial)*scale);
    close(lower.width,(p.D+2*p.radial+4.8)*scale);
    close(d.cap,p.L+p.slack-132);
    close(d.top+d.bottom,p.slack);
    const stop = svg.match(/<g data-geometry="external-stop">([\s\S]*?)<\/g>/)[1];
    for (const [,x] of stop.matchAll(/x="([^"]+)"/g)) assert.ok(Number(x)>lower.x+lower.width);
    const stopPath = stop.match(/d="([^"]+)"/)[1];
    for (const [,x] of stopPath.matchAll(/[MH] ([-\d.e+]+)/g)) assert.ok(Number(x)>lower.x+lower.width);
    close(Number(app.ui.section.attrs.viewBox.split(' ')[2]),width);
  }
});
test('presets and q endpoints move the same envelope into exact end contact', () => {
  const app=setup(); let initial;
  for (const q of [0,.5,1]) {
    app.set({q}); const svg=app.ui.section.innerHTML, device=rect(svg,'device'), lower=rect(svg,'lower-floor'), upper=rect(svg,'upper-floor');
    initial ??= device; close(device.width,initial.width); close(device.height,initial.height);
    if(q===0){close(device.y+device.height,lower.y); assert.match(app.ui.state.textContent,/底端接觸/);}
    if(q===.5){close(device.y-upper.y-upper.height,lower.y-device.y-device.height); assert.match(app.ui.state.textContent,/未固定/);}
    if(q===1){close(device.y,upper.y+upper.height); assert.match(app.ui.state.textContent,/頂端接觸/);}
  }
  app.buttons[1].fire('click'); assert.equal(app.fields.q.value,'0');
  app.buttons[0].fire('click'); assert.equal(app.fields.q.value,'0.5');
  for(const q of [0,.5,1]){app.set({q,slack:0});assert.match(app.ui.state.textContent,/兩端接觸/);const svg=app.ui.section.innerHTML,d=rect(svg,'device'),lo=rect(svg,'lower-floor'),hi=rect(svg,'upper-floor');close(d.y,hi.y+hi.height);close(d.y+d.height,lo.y);}
});
test('blank, nonfinite, negative, overflow and impossible cap clear every stale result', () => {
  for(const changes of [{D:''},{L:'Infinity'},{L:0},{radial:-1},{slack:-1},{L:120},{L:'1e308',slack:'1e308'},{D:'1e308'},{q:2}]){
    const app=setup();app.set(changes);assert.match(app.ui.error.textContent,/有限數值/);
    for(const key of ['section','state','gaps','targets','dimensions'])assert.equal(app.ui[key].innerHTML,'');
  }
  const app=setup();app.set({slack:2,radial:.5});assert.match(app.ui.targets.textContent,/軸向餘量未達/);assert.match(app.ui.targets.textContent,/徑向間隙未達/);finiteGeometry(app.ui.section.innerHTML);
});
test('scope remains four dimensions plus position, native controls, pending claims',()=>{
  const app=setup();assert.deepEqual(Object.keys(app.fields),['L','D','slack','radial','q']);
  assert.match(source,/尺寸待實測；此圖不代表已驗證配合/);assert.match(source,/有效咬合5–6目標；尚未定案/);
  assert.doesNotMatch(source,/fetch\(|XMLHttpRequest|WebSocket|<iframe|tabindex=|data-key="(?:thread|pitch)"/);
});
