import assert from "node:assert/strict";
import {FIELD_SCHEMA} from "../preview/p2-r10-parameter-sensitivity-recovery/core/schema.mjs";
import {PARAMETER_COVERAGE} from "../preview/p2-r10-parameter-sensitivity-recovery/core/parameter-coverage.mjs";
import {derive} from "../preview/p2-r10-parameter-sensitivity-recovery/core/derive.mjs";
import {deepMerge} from "../preview/p2-r10-parameter-sensitivity-recovery/core/utils.mjs";
const deepFrozen=v=>v&&typeof v==="object"&&Object.isFrozen(v)&&Object.values(v).every(x=>typeof x!=="object"||x===null||deepFrozen(x));
assert.equal(PARAMETER_COVERAGE.length,FIELD_SCHEMA.length+1);
let checked=0;for(const c of PARAMETER_COVERAGE){const {a,b}=c.pair();const A=derive(a),B=derive(b);assert.ok(A.valid,`${c.path} A valid: ${JSON.stringify(A.errors)}`);assert.ok(B.valid,`${c.path} B valid: ${JSON.stringify(B.errors)}`);assert.ok(deepFrozen(A.descriptor));assert.equal(JSON.stringify(A.descriptor),JSON.stringify(JSON.parse(JSON.stringify(A.descriptor))),`${c.path} JSON round trip`);if(c.path==="container.splitPercent"){assert.notEqual(A.descriptor.projection.splitPercent,B.descriptor.projection.splitPercent);continue;}const effectA=A.descriptor.effects[c.path],effectB=B.descriptor.effects[c.path],targetA=A.descriptor.targets[c.renderTarget],targetB=B.descriptor.targets[c.renderTarget];assert.ok(effectA&&effectB&&targetA&&targetB,c.path);assert.notEqual(effectA.influence,effectB.influence,`${c.path} changes non-echo descriptor effect`);assert.notEqual(targetA.effect,targetB.effect,`${c.path} changes named SVG target`);checked++;}
const invalid=derive(deepMerge({}, {container:{outerDiameter:3,wall:2.4}}));assert.deepEqual(Object.keys(invalid).sort(),["descriptor","errors","valid"]);assert.equal(invalid.valid,false);assert.equal(invalid.descriptor,null);assert.ok(invalid.errors.length);
const inactive=derive(deepMerge({}, {closure:{mode:"screw",bayonet:{lockAngleDeg:Infinity}}}));assert.equal(inactive.valid,true,"inactive poison must not invalidate");
console.log(`R10 descriptor sensitivity passed: ${checked} active field oracles plus split projection`);
