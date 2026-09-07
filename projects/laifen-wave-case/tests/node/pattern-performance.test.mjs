import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {dirname, resolve} from 'node:path';

const project = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const source = readFileSync(resolve(project, 'openscad/laifen_case_customizer_v1.scad'), 'utf8');
const runner = readFileSync(resolve(project, 'tests/mesh/pattern-performance/benchmark.mjs'), 'utf8');

test('wave no-cut shortcuts use exact cone equality and retain the original cut arithmetic',()=>{
  const edge = source.slice(source.indexOf('function wave_edge_cut'), source.indexOf('function wave_xyz'));
  assert.match(edge,/wave_cone\(zs\[row\],h,role\)==outer_radius && wave_cone\(zs\[row\+\(kind==0\?0:1\)\],h,role\)==outer_radius \? undef/);
  assert.match(edge,/let\(ab=wave_edge_ends\(e,zs,h,role\),a=ab\[0\],b=ab\[1\]\)/);
  assert.match(edge,/v06_sgn\(a\[3\]\)\*v06_sgn\(b\[3\]\)!=-1\?undef/);
  assert.match(edge,/let\(t=-a\[3\]\/\(b\[3\]-a\[3\]\)\)\[for\(k=\[0:3\]\)k==3\?0:a\[k\]\+t\*\(b\[k\]-a\[k\]\)\]/);
  assert.doesNotMatch(edge,/EPS|epsilon/i);

  const face = source.slice(source.indexOf('function wave_face_polys'), source.indexOf('function wave_ring'));
  assert.match(face,/uncut=wave_cone\(zs\[row\],h,role\)==outer_radius && wave_cone\(zs\[row\+1\],h,role\)==outer_radius/);
  assert.match(face,/uncut\?\[\[a,c,b\],\[a,d,c\]\]:\[for\(tri=/);
  assert.match(source,/wave_face_polys\(row,col,zs,slots,h,role\)/);
});

test('exact cone predicate implies every skipped wave sample is uncut',()=>{
  const outerRadius=19.6, depth=.6, spacing=4, bodyThreadZ=58.7;
  const radius=(style,theta,z)=>outerRadius-depth*(1-Math.cos((style==='ribs'?20*theta:style==='rings'?360*(z-bodyThreadZ)/spacing:6*theta-360*(z-bodyThreadZ)/spacing)*Math.PI/180))/2;
  const cone=(z,h,role)=>outerRadius-Math.max(0,1.2-(role==='body'?z:h-z));
  for(const style of ['ribs','rings','spiral'])for(const [h,role] of [[58.7,'body'],[25.3,'cap']]){
    for(const z of [0,1.2,h/2,h-1.2,h])if(cone(z,h,role)===outerRadius){
      for(let col=0;col<=192;col++) assert.ok(radius(style,360*col/192,(role==='body'?bodyThreadZ:0)+z)-cone(z,h,role)<=1e-12,`${style}/${role}/${z}/${col}`);
    }
  }
});

test('benchmark runner requires an explicit source and pins both runtime assets',()=>{
  assert.match(runner,/RUNTIME_DIR SOURCE OUT_DIR LABEL STYLE FORMAT ROLE RUN/);
  assert.match(runner,/904a47f29e63afb597bedef747da3b457d8ea17cc793c462c6c8b444e918a62e/);
  assert.match(runner,/f72ce246c02c0e501990837102be383326b153fd761774ebfacce5c80c5ecf26/);
  for(const field of ['initializeMs','callMainMs','compilerRenderMs','readMs','writeMs'])assert.match(runner,new RegExp(field));
});
