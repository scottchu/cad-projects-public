import assert from "node:assert/strict";
import {DEFAULT_STATE,FIELD_SCHEMA,MODULE_SCHEMA,visible} from "../preview/p2-r10-parameter-sensitivity-recovery/core/schema.mjs";
import {PRESET_PATCHES,presetState,R8_PRESET_PARITY} from "../preview/p2-r10-parameter-sensitivity-recovery/core/presets.mjs";
import {PARAMETER_COVERAGE} from "../preview/p2-r10-parameter-sensitivity-recovery/core/parameter-coverage.mjs";
import {derive} from "../preview/p2-r10-parameter-sensitivity-recovery/core/derive.mjs";
import {deepMerge,getPath} from "../preview/p2-r10-parameter-sensitivity-recovery/core/utils.mjs";
assert.equal(FIELD_SCHEMA.length,83,"R10 adds surface.keepout to the 82 R9 fields");assert.deepEqual(MODULE_SCHEMA,["Container","Closure","Ends","Surface","Vent & Drain","Label","Attachment"]);
assert.equal(new Set(FIELD_SCHEMA.map(f=>f.path)).size,83);assert.equal(new Set(FIELD_SCHEMA.map(f=>f.flattenName)).size,83);assert.equal(PARAMETER_COVERAGE.length,84,"83 leaves plus split percent projection");
for(const f of FIELD_SCHEMA){assert.ok(f.label&&f.help&&f.unit&&f.bounds&&f.flattenName&&f.derivation&&f.oracle&&f.renderTarget,f.path);assert.ok(PARAMETER_COVERAGE.some(c=>c.path===f.path),f.path);assert.equal(typeof visible(f,DEFAULT_STATE),"boolean");}
for(const [id,expected] of Object.entries(R8_PRESET_PARITY)){const s=presetState(id);for(const [k,v] of Object.entries(expected))assert.equal(s.container[k],v,`${id}.${k}`);assert.ok(derive(s).valid,id);}
assert.ok(Object.isFrozen(PRESET_PATCHES)&&Object.isFrozen(DEFAULT_STATE));const inactive=deepMerge(DEFAULT_STATE,{closure:{mode:"screw",bayonet:{lockAngleDeg:Infinity}}});assert.equal(derive(inactive).valid,true,"inactive poison is ignored");
console.log("R10 schema coverage passed: 83 fields + canonical split-percent projection");
