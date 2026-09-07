import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import { pathToFileURL } from 'node:url';

const ROOT = new URL('../../', import.meta.url);
const STUDY = new URL('preview/recessed-diamond-study/', ROOT);
const SCAD = new URL('openscad/laifen_case_customizer_v1.scad', ROOT);
const digest = url => crypto.createHash('sha256').update(fs.readFileSync(url)).digest('hex');
const math = await import(pathToFileURL(new URL('math.mjs', STUDY).pathname));
const { R, wrap, field, smoothstep, height, geometry, sectionSamples } = math;

const oracleWrap = t => t - Math.floor(t + 0.5);
const oracleField = (u, v, g) => Math.max(0, Math.min(1,
  (0.5 - Math.max(Math.abs(oracleWrap(u + v)), Math.abs(oracleWrap(u - v)))) / (0.5 - g)));
const oracleHeight = (kind, u, v, d) => kind === 'current'
  ? -d + d * oracleField(u, v, 0.18)
  : -d * (x => x * x * (3 - 2 * x))(oracleField(u, v, 0.14));
const close = (a, b, eps = 1e-12) => assert.ok(Math.abs(a - b) <= eps, `${a} != ${b}`);

test('frozen study and unchanged SCAD fingerprints are exact', () => {
  assert.equal(digest(new URL('index.html', STUDY)), '5edb9e9a561007c8d74b6df4cef77cea8b1c60b50e152fe7fc0452811f4ac8b2');
  assert.equal(digest(new URL('math.mjs', STUDY)), '85148315035fc1b62bab27516d696c4036894b0b06b6896ab378f7a227de9d1a');
  assert.equal(digest(new URL('study.mjs', STUDY)), 'f480e5fdf5e94fd4c3c5c07b682e327d8535cc074c0e0f8715f0781de4fee32e');
  assert.equal(digest(new URL('style.css', STUDY)), 'f6118a474cb454e468135ecaf98658c121160adafd6b285975ff20d26d3507bd');
  assert.equal(digest(SCAD), '497098afa555092a0ed85a3a7213cd270852aa76f9001e1478c209cd8469bc42');
});

test('Current Diamond analytic field is bound to the frozen SCAD algebra', () => {
  const source = fs.readFileSync(SCAD, 'utf8');
  assert.ok(source.includes('function diamond_wrap(t) = t - floor(t + 0.5);'));
  assert.ok(source.includes('max(abs(diamond_wrap(u+v)), abs(diamond_wrap(u-v)))'));
  assert.ok(source.includes('r_valley + depth * diamond_field(u, v, plateau_half_fraction)'));
  assert.ok(source.includes('diamond_plateau_half_fraction = 0.18'));
  for (const [u, v] of [[0,0],[.5,0],[.18,0],[.32,.07],[-.41,.23],[1.17,-.36]]) {
    close(wrap(u), oracleWrap(u));
    close(field(u,v,.18), oracleField(u,v,.18));
    close(height('current',u,v,.45), oracleHeight('current',u,v,.45));
  }
});

test('center and crossing witnesses reverse sign without changing phase', () => {
  const d = 0.45;
  close(height('current',0,0,d), 0);
  close(height('current',.5,0,d), -d);
  close(height('recessed',0,0,d), -d);
  close(height('recessed',.5,0,d), 0);
  close(field(0,0,.18), 1);
  close(field(0,0,.14), 1);
  close(field(.5,0,.18), 0);
  close(field(.5,0,.14), 0);
  close(smoothstep(.25), .15625);
});

test('both fields are bounded and periodic across the displayed four-cell domain', () => {
  for (const d of [.1,.45,.6]) for (const kind of ['current','recessed']) {
    for (let i=0;i<=32;i++) for (let j=0;j<=32;j++) {
      const u=-2+4*i/32, v=-2+4*j/32, h=height(kind,u,v,d);
      assert.ok(h >= -d-1e-12 && h <= 1e-12, `${kind} ${u},${v}: ${h}`);
      close(h,height(kind,u+1,v,d));
      close(h,height(kind,u,v-1,d));
    }
  }
});

test('size and depth change only documented geometry and amplitude', () => {
  const cases=[[4.8,.1],[4.83,.45],[8,.6]];
  for (const [size,depth] of cases) {
    const got=geometry({size,depth});
    const target=size===4.8?3.63:size*(3.63/4.8);
    const count=Math.floor(2*Math.PI*(R-depth)/target+.5);
    close(got.targetArc,target); assert.equal(got.count,count);
    close(got.arc,2*Math.PI*(R-depth)/count);
    close(height('current',.5,0,depth),-depth);
    close(height('recessed',0,0,depth),-depth);
  }
  assert.ok(geometry({size:8,depth:.45}).count < geometry({size:4.8,depth:.45}).count);
});

test('sections contain uniform samples and every center, crossing, and g breakpoint', () => {
  for (const g of [.18,.14]) {
    const samples=sectionSamples(g);
    assert.ok(samples.length>=513);
    assert.deepEqual(samples,[...samples].sort((a,b)=>a-b));
    for(let i=0;i<=512;i++) assert.ok(samples.includes(-1+2*i/512));
    for(let n=-1;n<=1;n++) for(const x of [n,n-.5,n+.5,n-g,n+g])
      if(x>=-1&&x<=1) assert.ok(samples.some(y=>Math.abs(y-x)<1e-12), `missing ${x}`);
  }
});

test('rendered surfaces and sections share one accepted snapshot; invalid edits stay stale', () => {
  const html=fs.readFileSync(new URL('index.html',STUDY),'utf8');
  const source=fs.readFileSync(new URL('study.mjs',STUDY),'utf8');
  assert.match(html,/id="size"[^>]*type="text"[^>]*value="4.8"/);
  assert.match(html,/id="size-range"[^>]*min="4.8"[^>]*max="8"[^>]*step="0.1"/);
  assert.ok(source.includes("value.trim()===''||!Number.isFinite(number)"));
  assert.ok(source.includes('number<lo||number>hi'));
  assert.ok(source.includes("Object.assign($(id).dataset,{size:String(values.size),depth:String(values.depth),arc:String(geom.arc),count:String(geom.count)})"));
  assert.ok(source.includes("dataset.stale='true'"));
  assert.ok(source.includes("if(values){$('size-range').value=String(values.size);$('depth-range').value=String(values.depth);renderStudy(values);}"));
  assert.ok(source.includes('renderStudy(DEFAULTS)'));
  assert.ok(source.includes('renderedValues={...values}'));
  assert.ok(source.includes('drawSection($(`${kind}-true`),kind,renderedValues,1)'));
  assert.ok(source.includes('ctx.setTransform(dpr,0,0,dpr,0,0)'));
  const css=fs.readFileSync(new URL('style.css',STUDY),'utf8');
  assert.ok(css.includes('.number-unit { width: 112px; height: 44px;'));
});
