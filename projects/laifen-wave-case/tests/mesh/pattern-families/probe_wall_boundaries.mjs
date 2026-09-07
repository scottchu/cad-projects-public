// Executes all source-level guards using the tiny existing math output.
// Usage from root: node .../probe_wall_boundaries.mjs SCRATCH_WITH_PINNED_RUNTIME
import {readFile,writeFile} from 'node:fs/promises';
import {resolve,join} from 'node:path';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
const scratch=resolve(process.argv[2]);
const sourcePath=resolve('projects/laifen-wave-case/openscad/laifen_case_customizer_v1.scad');
const source=await readFile(sourcePath),js=await readFile(join(scratch,'openscad.js')),wasm=await readFile(join(scratch,'openscad.wasm'));
const hash=b=>createHash('sha256').update(b).digest('hex');
if(hash(js)!=='904a47f29e63afb597bedef747da3b457d8ea17cc793c462c6c8b444e918a62e'||hash(wasm)!=='f72ce246c02c0e501990837102be383326b153fd761774ebfacce5c80c5ecf26')throw Error('Pinned runtime differs');
const {default:factory}=await import(pathToFileURL(join(scratch,'openscad.js')));
const cases=[];
for(const family of ['ribs','rings','spiral'])for(const wall of [4.55,4.5599999,4.56,4.5600001]){
 const fields=[`surface_style="${family}"`,'wave_spacing=6','wave_depth=.6',`outer_diameter=${30+2*wall}`,'body_bore=30','cap_bore=31','device_length=55','floor_thickness=3','split_distance_from_top=25.3','VFR04_PROBE_MODE="math"'];
 const argv=['/case.scad','--backend=Manifold',...fields.flatMap(x=>['-D',x]),'-o','/probe.stl'],messages=[];
 const mod=await factory({noInitialRun:true,wasmBinary:wasm,print:x=>messages.push(String(x)),printErr:x=>messages.push(String(x))});mod.FS.writeFile('/case.scad',source);
 const code=mod.callMain([...argv]),accepted=!code&&!messages.some(x=>x.includes('ERROR:')),expected=wall>=4.56;
 cases.push({family,wall,argv,accepted,expected,messages});
}
const receipt={sourcePath,sourceSha256:hash(source),runtime:{js:hash(js),wasm:hash(wasm)},cases,pass:cases.every(c=>c.accepted===c.expected)};
await writeFile(join(scratch,'source-wall-boundaries.json'),JSON.stringify(receipt,null,2)+'\n');
console.log(JSON.stringify({sourceSha256:receipt.sourceSha256,pass:receipt.pass,cases:cases.map(({family,wall,accepted,expected})=>({family,wall,accepted,expected}))},null,2));
if(!receipt.pass)process.exitCode=1;
