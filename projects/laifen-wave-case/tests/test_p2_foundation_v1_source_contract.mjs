import assert from "node:assert/strict";
import {readFileSync, readdirSync} from "node:fs";
import {join} from "node:path";
const root=new URL("..",import.meta.url).pathname, preview=join(root,"preview/p2-foundation-v1");
const files=[];const walk=dir=>readdirSync(dir,{withFileTypes:true}).forEach(e=>e.isDirectory()?walk(join(dir,e.name)):files.push(join(dir,e.name)));walk(preview);
const all=files.map(path=>[path,readFileSync(path,"utf8")]);const app=all.find(([path])=>path.endsWith("/app.mjs"))[1];
assert.match(app,/deriveV1\(raw\)/,"only UI owns state derivation");
for(const [path,text] of all.filter(([path])=>path.includes("/scene/")||path.includes("readout"))){assert.doesNotMatch(text,/deriveV1\(/,`${path} must consume a descriptor`);assert.doesNotMatch(text,/document\.|raw\b|SVG|<svg|cdn\./i,`${path} bypasses the descriptor or uses a prohibited proxy`);}
for(const [,text] of all){assert.doesNotMatch(text,/p2-r(?:1[3-9]|2[0-2])|p2-r10[^\n]*render|openscad|makerworld|bayonet|attachment|label\/text/i,"excluded or quarantined source leaked into V1");assert.doesNotMatch(text,/https:\/\//,"no CDN dependency");}
assert.ok(all.some(([path])=>path.endsWith("/scene/build-scene.mjs")));assert.ok(all.some(([path])=>path.endsWith("/core/derive.mjs")));
console.log("Foundation V1 source-boundary gates passed");
