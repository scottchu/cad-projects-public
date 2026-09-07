import scad from '../../../openscad/laifen_case_customizer_v1.scad?raw';
import lockText from '../dependency-lock.json?raw';
import {argv,identity,sha256} from './schema.mjs';
import {Generation} from './lifecycle.mjs';
import {createViewer} from './viewer.mjs';
import {createCustomizerController} from './controller.mjs';

const $=id=>document.getElementById(id);
const stable=v=>Array.isArray(v)?`[${v.map(stable)}]`:v&&typeof v==='object'?`{${Object.keys(v).sort().map(k=>`${JSON.stringify(k)}:${stable(v[k])}`)}}`:JSON.stringify(v);
const sourceBytes=new TextEncoder().encode(scad);
let viewer=null;
try {viewer=createViewer($('viewer'),$('dimensions'),$('dimension-description'));}
catch {$('viewer-note').textContent='WebGL preview is unavailable. Generation and exact STL download still work.';}

createCustomizerController({document,viewer,createGeneration:callbacks=>new Generation({
  prepare:async values=>{
    const [lockFingerprint,sourceHash]=await Promise.all([sha256(new TextEncoder().encode(stable(JSON.parse(lockText)))),sha256(sourceBytes)]);
    const key=await identity(sourceBytes,lockFingerprint,values);
    return {scad,argv:argv(values),identity:key,sourceHash,lockFingerprint};
  },
  createWorker:()=>new Worker(new URL('../workers/openscad.worker.js',import.meta.url),{type:'module'}),
  ...callbacks
})});
