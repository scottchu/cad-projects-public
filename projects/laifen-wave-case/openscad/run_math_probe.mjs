import {readFileSync} from "node:fs";
import {fileURLToPath} from "node:url";
import factory from "../preview/openscad-wasm-simulator/vendor/openscad.js";

const wasmUrl=new URL("../preview/openscad-wasm-simulator/vendor/openscad.wasm",import.meta.url);
const scadUrl=new URL("./laifen_case_customizer_v1.scad",import.meta.url);
const lines=[];
const mod=await factory({
  noInitialRun:true,
  wasmBinary:readFileSync(fileURLToPath(wasmUrl)),
  print:text=>lines.push(String(text)),
  printErr:text=>lines.push(String(text)),
});
mod.FS.writeFile("/case.scad",readFileSync(fileURLToPath(scadUrl),"utf8"));
const code=mod.callMain(["/case.scad","--backend=Manifold","-D",'VFR04_PROBE_MODE="math"',"-o","/probe.stl"]);
if(code)throw new Error(`OpenSCAD exited ${code}`);
const required=["VFR04_COUNT", "VFR04_HALF_UP", "VFR04_WRAP", "VFR04_FIELD", "VFR04_PATCH", "VFR04_SEAM", "VFR04_WIDTH_SLOPE"];
for(const witness of required)if(!lines.some(line=>line.includes(witness)))throw new Error(`missing ${witness}`);
const fatal=lines.filter(line=>/ERROR:|Parser error|Assertion/.test(line));
if(fatal.length)throw new Error(fatal.join("\n"));
process.stdout.write(lines.filter(line=>line.includes("VFR04_")).join("\n")+"\n");
