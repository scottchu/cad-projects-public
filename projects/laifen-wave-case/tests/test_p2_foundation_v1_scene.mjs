import assert from "node:assert/strict";
import * as THREE from "three";
import {DEFAULT_INPUTS, deriveV1} from "../preview/p2-foundation-v1/core/derive.mjs";
import {buildScene,namedMeshFacts} from "../preview/p2-foundation-v1/scene/build-scene.mjs";
const descriptor=patch=>{const r=deriveV1({...DEFAULT_INPUTS,...patch});assert.ok(r.valid,JSON.stringify(r.errors));return r.descriptor;};
const d=descriptor({}), scene=buildScene(d), facts=namedMeshFacts(scene);
for(const name of ["v1.lower.shell","v1.upper.shell","v1.end.bottom","v1.end.top","v1.closure.maleThread","v1.closure.femaleThread","v1.drains.bottom","v1.seam"]){assert.ok(facts[name],`${name} exists`);assert.ok(facts[name].vertices>0&&facts[name].indices>0,`${name} is an indexed mesh`);}
scene.traverse(o=>{if(o.geometry){const p=o.geometry.getAttribute("position");assert.ok([...p.array].every(Number.isFinite),`${o.name} is finite`);assert.ok(o.geometry.getAttribute("normal"));}});
const lower=scene.getObjectByName("v1.lower.shell"), upper=scene.getObjectByName("v1.upper.shell");lower.geometry.computeBoundingBox();upper.geometry.computeBoundingBox();assert.ok(Math.abs(lower.geometry.boundingBox.max.x-d.R)<.001);assert.ok(Math.abs(upper.geometry.boundingBox.max.x-d.R)<.001,"shells share OD");
assert.throws(()=>buildScene(null),/descriptor/);assert.throws(()=>buildScene({version:"p2-foundation-v1"}),/descriptor/);
const exploded=buildScene(descriptor({presentation:"exploded"}));assert.ok(exploded.getObjectByName("v1.upper.shell").getWorldPosition(new THREE.Vector3()).z>d.pieces.upper.z,"exploded upper moves +Z");
const polygon=buildScene(descriptor({section:"polygon",N:6}));assert.equal(polygon.getObjectByName("v1.lower.shell").geometry.getAttribute("position").count<lower.geometry.getAttribute("position").count,true,"polygon has reduced actual ring topology");
const rounded=buildScene(descriptor({bottomStyle:"rounded",bottomSize:2}));assert.notDeepEqual(namedMeshFacts(rounded)["v1.end.bottom"].bounds,facts["v1.end.bottom"].bounds,"end profile changes end geometry");
const roundedThread=buildScene(descriptor({threadForm:"rounded"}));assert.notDeepEqual(namedMeshFacts(roundedThread)["v1.closure.maleThread"].bounds,facts["v1.closure.maleThread"].bounds,"thread form changes actual helical geometry");
const clearance=buildScene(descriptor({C:.4}));assert.notDeepEqual(namedMeshFacts(clearance)["v1.closure.maleThread"].bounds,facts["v1.closure.maleThread"].bounds,"clearance moves mating surface");
const topDrain=buildScene(descriptor({drainLocation:"top",Q:1,BCD:0}));assert.equal(topDrain.getObjectByName("v1.drains.bottom"),undefined);assert.ok(topDrain.getObjectByName("v1.drains.top").geometry.getAttribute("position").count>0,"selected floor has actual hole geometry");
const none=buildScene(descriptor({drainLocation:"none"}));assert.equal(none.getObjectByName("v1.drains.bottom"),undefined);assert.equal(none.getObjectByName("v1.drains.top"),undefined);
console.log("Foundation V1 scene geometry gates passed");
