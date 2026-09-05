export const finite=v=>typeof v==="number"&&Number.isFinite(v);
export const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
export const rad=d=>d*Math.PI/180;
export const wrap=v=>v-Math.floor(v+.5);
export const clone=v=>structuredClone(v);
export function deepFreeze(value){if(value&&typeof value==="object"&&!Object.isFrozen(value)){for(const v of Object.values(value))deepFreeze(v);Object.freeze(value);}return value;}
export function deepMerge(base,patch={}){if(Array.isArray(base)||Array.isArray(patch))return clone(patch??base);if(!base||typeof base!=="object")return patch===undefined?base:clone(patch);const out={};for(const k of new Set([...Object.keys(base),...Object.keys(patch||{})]))out[k]=Object.hasOwn(patch,k)?deepMerge(base[k],patch[k]):clone(base[k]);return out;}
export const getPath=(o,path)=>path.split(".").reduce((v,k)=>v?.[k],o);
export function setPath(o,path,value){const keys=path.split(".");let at=o;for(const k of keys.slice(0,-1))at=at[k];at[keys.at(-1)]=value;return o;}
export const jsonHash=value=>{const text=JSON.stringify(value,Object.keys(value||{}).sort());let h=2166136261;for(let i=0;i<text.length;i++)h=Math.imul(h^text.charCodeAt(i),16777619);return (h>>>0).toString(16).padStart(8,"0");};
