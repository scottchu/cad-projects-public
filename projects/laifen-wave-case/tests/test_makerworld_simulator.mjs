import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { DEFAULTS, deriveSimulator, patternRelief, splitFromPercent, splitPercentBounds } from "../preview/p2-r1-makerworld-simulator/math.mjs";
const d=deriveSimulator();
assert.deepEqual([d.H,d.C,d.U,d.B,d.penetration,d.seamZ],[219,213,81,137,9,135]);
assert.equal(d.percent.toFixed(6),"38.356164");assert.equal(d.upperOuter+d.lowerOuter-d.penetration,d.H);
const fromPercent=deriveSimulator({splitFromTop:219*.5});assert.equal(fromPercent.S,109.5);assert.equal(fromPercent.percent,50);
const H311=311,bounds311=splitPercentBounds(H311);assert.equal(splitFromPercent(bounds311.min,H311),50);assert.equal(splitFromPercent(bounds311.max,H311),169);
for(const pattern of ["smooth","blunt-diamond","shallow-helix","wave-flutes"]){const x=patternRelief(pattern,1.2,137.4,DEFAULTS);assert.ok(x>=0&&x<=.45);assert.equal(x,patternRelief(pattern,1.2,137.4,{...DEFAULTS,splitFromTop:50}));}
assert.ok(deriveSimulator({splitFromTop:49}).errors.length);assert.ok(deriveSimulator({engagement:4.9}).errors.length);
const [html,js]=await Promise.all([readFile(new URL("../preview/p2-r1-makerworld-simulator/index.html",import.meta.url),"utf8"),readFile(new URL("../preview/p2-r1-makerworld-simulator/app.js",import.meta.url),"utf8")]);
for(const token of ["closed top","split-percent","blunt-diamond","shallow-helix","wave-flutes","not CAD, printable geometry","visual-summary","aria-live","for=\"split-mm-number\""]){assert.ok(html.includes(token),token)}
for(const token of ["upper-piece","lower-piece","full-thread-band","effective-thread-band","event.currentTarget","splitPercentBounds","ringGeometry(0,state.seamZ","full.position.y+=lowerOffset","seam.position.y+=upperOffset"]){assert.ok(js.includes(token),token)}
assert.match(html,/three@0\.160\.1/);assert.match(js,/patternRelief\(p\.pattern, theta, zGlobal/);assert.match(js,/new THREE\.BufferGeometry/);
console.log("makerworld simulator math and semantic-source checks passed");
