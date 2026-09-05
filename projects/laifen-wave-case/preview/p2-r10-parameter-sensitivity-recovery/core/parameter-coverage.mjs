import {DEFAULT_STATE,FIELD_SCHEMA} from "./schema.mjs";
import {clone,deepMerge,getPath,setPath} from "./utils.mjs";

const activate=path=>{
 if(path.startsWith("container.side")||path.startsWith("container.corner")||path.startsWith("container.rotation"))return {container:{crossSection:"regular_polygon"}};
 if(path.startsWith("closure.screw"))return {closure:{mode:"screw"}};
 if(path.startsWith("closure.bayonet"))return {closure:{mode:"bayonet"}};
 if(path.startsWith("ends.top"))return {ends:{linked:false,top:{profile:"chamfer",size:1}}};
 if(path==="ends.bottom.size")return {ends:{bottom:{profile:"chamfer",size:1}}};
 if(path==="surface.coverage")return {surface:{envelope:"fade_from_bottom"}};
 if(path.startsWith("surface.stitch"))return {surface:{pattern:"knit_stitch"}};
 if(path.startsWith("surface.flute"))return {surface:{pattern:"flowing_flutes"}};
 if(path.startsWith("surface.spiral"))return {surface:{pattern:"shallow_helix"}};
 if(path.startsWith("surface.quilt"))return {surface:{pattern:"quilted_diamond"}};
 if(path.startsWith("ventDrain.bottom"))return {ventDrain:{mode:"bottom",bottom:{count:3,diameter:2,ringRadius:8}}};
 if(path.startsWith("ventDrain.top"))return {ventDrain:{mode:"top",linked:false,top:{count:3,diameter:2,ringRadius:8}}};
 if(path==="ventDrain.linked")return {ventDrain:{mode:"both"}};
 if(path.startsWith("label."))return {label:{mode:"outset",text:"WAVE",size:7,relief:.5,axialFromTargetEnd:20}};
 if(path.startsWith("attachment."))return {attachment:{mode:"integrated_lanyard_eyelet"}};
 return {};
};
const alternate=f=>{if(f.path.endsWith(".size")&&f.path.startsWith("ends."))return 1.5;if(f.type==="boolean")return !f.default;if(f.type==="enum")return f.options.find(v=>v!==f.default);if(f.type==="string")return f.default==="WAVE"?"R10":`${f.default} R10`;if(f.type==="integer")return f.default===f.max?f.default-1:f.default+1;const span=(f.max??f.default+1)-(f.min??f.default-1);return Number((f.default+Math.max(f.step??.1,span*.13)).toFixed(6));};
const signedPair=path=>{const a=deepMerge(DEFAULT_STATE,activate(path));setPath(a,path,1);const b=clone(a);setPath(b,path,-1);return {a,b};};
export function pairFor(field){
 if(field.path==="ends.bottom.profile"||field.path==="ends.top.profile"){const end=field.path.split(".")[1],normalized=profile=>{const state=deepMerge(DEFAULT_STATE,activate(field.path));setPath(state,field.path,profile);setPath(state,`ends.${end}.size`,1);if(state.ends.linked)state.ends.top=clone(state.ends.bottom);return state;};return {a:normalized("chamfer"),b:normalized("rounded_fillet")};}
 if(field.path==="surface.flute.waveDirection"||field.path==="surface.spiral.direction")return signedPair(field.path);
 if(field.path==="attachment.mode"){const a=deepMerge(DEFAULT_STATE,{attachment:{mode:"integrated_lanyard_eyelet"}}),b=clone(a);setPath(b,field.path,"captured_loop");return {a,b};}
 const a=deepMerge(DEFAULT_STATE,activate(field.path));if(field.path==="ends.bottom.size")setPath(a,"ends.bottom.size",1);if(field.path==="ends.top.size")setPath(a,"ends.top.size",1);const b=clone(a);setPath(b,field.path,alternate(field));return {a,b};
}
export const PARAMETER_COVERAGE=Object.freeze([...FIELD_SCHEMA.map(field=>Object.freeze({path:field.path,tier:field.tier,visibility:field.visibleWhen,flattenName:field.flattenName,metadata:{label:field.label,help:field.help,unit:field.unit,bounds:field.bounds,default:field.default,type:field.type},descriptorPath:`effects.${field.path}`,oracle:field.oracle,renderTarget:field.renderTarget,pair:()=>pairFor(field)})),Object.freeze({path:"container.splitPercent",tier:"basic",visibility:null,flattenName:"split_percent",metadata:{label:"Split percentage",help:"Projection of canonical upper-piece millimetres.",unit:"percent",bounds:"0–100",default:50,type:"projection"},descriptorPath:"projection.splitPercent",oracle:"oracle:container.splitPercent",renderTarget:"target-container-splitFromTop",pair:()=>({a:clone(DEFAULT_STATE),b:deepMerge(DEFAULT_STATE,{container:{splitFromTop:72}})})})]);
export const coverageByPath=Object.freeze(Object.fromEntries(PARAMETER_COVERAGE.map(x=>[x.path,x])));
