import {createHash} from 'node:crypto';
import {cp, mkdir, readFile, rm, writeFile} from 'node:fs/promises';
import {dirname, join, resolve, sep} from 'node:path';

const [repoArg, manifestArg, expectedManifestHash, outputArg] = process.argv.slice(2);
if (!repoArg || !manifestArg || !expectedManifestHash || !outputArg) {
  throw Error('usage: node generate.mjs REPO CANDIDATE.sha256 EXPECTED_MANIFEST_SHA256 /tmp/OUTPUT');
}
const repo=resolve(repoArg), manifestPath=resolve(manifestArg);
const sha=bytes=>createHash('sha256').update(bytes).digest('hex');
const manifestBytes=await readFile(manifestPath);
const manifestHash=sha(manifestBytes);
if(manifestHash!==expectedManifestHash) throw Error(`candidate manifest mismatch: ${manifestHash}`);
const entries=manifestBytes.toString('utf8').trim().split(/\r?\n/).filter(Boolean).map(line=>{
  const match=line.match(/^([0-9a-f]{64})  (.+)$/);
  if(!match) throw Error(`malformed manifest line: ${line}`);
  return {hash:match[1],path:match[2]};
});
const hashes=new Map();
for(const entry of entries){
  const source=resolve(repo,entry.path);
  if(!source.startsWith(`${repo}${sep}`)) throw Error(`path escapes repo: ${entry.path}`);
  const actual=sha(await readFile(source));
  if(actual!==entry.hash) throw Error(`candidate changed: ${entry.path}: ${actual}`);
  hashes.set(entry.path,actual);
}
const exact={
  'projects/laifen-wave-case/docs/iterations/2026-09-06-surface-pattern/DESIGN.md':'176bb99dc05b08b52ae757682b8f70ae1ccdf8a3e470a89476dfad4701e3d924',
  'projects/laifen-wave-case/docs/iterations/2026-09-06-surface-pattern/BRIEF.md':'5df06828d9794d6fd75e0cce4412858f4ded86ef6d3f6241f47090fd77f3d5bd',
  'projects/laifen-wave-case/preview/openscad-wasm-simulator/vendor/openscad.js':'904a47f29e63afb597bedef747da3b457d8ea17cc793c462c6c8b444e918a62e',
  'projects/laifen-wave-case/preview/openscad-wasm-simulator/vendor/openscad.wasm':'f72ce246c02c0e501990837102be383326b153fd761774ebfacce5c80c5ecf26'
};
for(const [path,expected] of Object.entries(exact)){
  const actual=sha(await readFile(join(repo,path)));
  if(actual!==expected) throw Error(`frozen support mismatch: ${path}: ${actual}`);
  hashes.set(path,actual);
}
const mustBeManifested=[
  'projects/laifen-wave-case/openscad/laifen_case_customizer_v1.scad',
  'projects/laifen-wave-case/preview/openscad-wasm-simulator/index.html',
  'projects/laifen-wave-case/preview/openscad-wasm-simulator/src/controller.mjs',
  'projects/laifen-wave-case/preview/openscad-wasm-simulator/src/lifecycle.mjs',
  'projects/laifen-wave-case/preview/openscad-wasm-simulator/src/schema.mjs'
];
for(const path of mustBeManifested) if(!hashes.has(path)) throw Error(`candidate manifest omits ${path}`);
const support=[
  'projects/laifen-wave-case/preview/openscad-wasm-simulator/dependency-lock.json',
  'projects/laifen-wave-case/preview/openscad-wasm-simulator/workers/openscad.worker.js',
  ...Object.keys(exact).filter(path=>path.includes('/vendor/'))
];
for(const path of support){
  if(!hashes.has(path)) hashes.set(path,sha(await readFile(join(repo,path))));
}
const harnessRoot=dirname(new URL(import.meta.url).pathname);
const snapshot=resolve(outputArg);
await rm(snapshot,{recursive:true,force:true});
for(const path of new Set([...entries.map(x=>x.path),...support])){
  const target=join(snapshot,path); await mkdir(dirname(target),{recursive:true}); await cp(join(repo,path),target);
}
const appRel='projects/laifen-wave-case/preview/openscad-wasm-simulator';
const app=join(snapshot,appRel);
let html=await readFile(join(app,'index.html'),'utf8');
if(!html.includes('./src/main.mjs')) throw Error('candidate index has no expected main module');
html=html.replace('./src/main.mjs','./harness.mjs')
  .replace('</head>','<link rel="stylesheet" href="./harness.css"></head>')
  .replace('</body>',`<aside id="harness-panel" aria-label="Independent lifecycle validation harness">
<h1>Surface-pattern lifecycle harness</h1>
<p id="binding">Binding candidate…</p>
<ol>
 <li><button id="h-start-cancel" type="button">Start held Diamond body</button> Wait for “result held”.</li>
 <li><button id="h-cancel" type="button">Cancel job 1</button> then <button id="h-deliver-cancelled" type="button">Deliver cancelled result</button>.</li>
 <li><button id="h-start-race" type="button">Start held job 2</button> Wait, then <button id="h-start-newer" type="button">Start newer job 3</button>.</li>
 <li>Wait for job 3 to be held. <button id="h-deliver-superseded" type="button">Deliver job 2 late</button> then <button id="h-deliver-latest" type="button">Deliver job 3</button>.</li>
</ol>
<dl id="checks"></dl><pre id="h-log" aria-live="polite"></pre>
</aside></body>`);
await writeFile(join(app,'index.html'),html);
for(const file of ['harness.mjs','harness.css']) await cp(join(harnessRoot,file),join(app,file));
await writeFile(join(snapshot,'binding.json'),JSON.stringify({manifestPath,manifestHash,entries:entries.length,hashes:Object.fromEntries([...hashes].sort()),syncedAt:new Date().toISOString()},null,2)+'\n');
console.log(JSON.stringify({status:'READY',manifestHash,entries:entries.length,snapshot,app:`/${appRel}/index.html`},null,2));
