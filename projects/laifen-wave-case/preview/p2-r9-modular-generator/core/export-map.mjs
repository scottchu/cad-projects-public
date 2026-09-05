import {deepFreeze, getPath} from "./utils.mjs";
import {FIELD_SCHEMA} from "./schema.mjs";
const key=path=>path.replace(/^container\.outerDiameter$/,"container_outer_diameter").replace(/^container\.height$/,"container_height").replace(/^container\.splitFromTop$/,"container_split_from_top").replaceAll(".","_");
export const OPENSCAD_EXPORT_MAP=deepFreeze(Object.fromEntries(FIELD_SCHEMA.map(field=>[field.path,key(field.path)])));
export function flattenForOpenScad(state){return Object.fromEntries(FIELD_SCHEMA.map(field=>[OPENSCAD_EXPORT_MAP[field.path],getPath(state,field.path)]));}
