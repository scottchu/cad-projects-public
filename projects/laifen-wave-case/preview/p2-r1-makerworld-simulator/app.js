import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { DEFAULTS, deriveSimulator, patternRelief, splitFromPercent, splitPercentBounds } from "./math.mjs";

const $ = (id) => document.getElementById(id);
let state = deriveSimulator();
let renderer, scene, camera, orbit, caseGroup, bandGroup;
const fmt = (n, digits = 1) => `${Number(n).toFixed(digits)} mm`;
const range = (a) => `${fmt(a[0])}–${fmt(a[1])}`;

function ringGeometry(z0, z1, p, material) {
  const radial = 96, axial = Math.max(8, Math.ceil((z1 - z0) / 2));
  const positions = [], normals = [], indices = [];
  for (let j = 0; j <= axial; j++) for (let i = 0; i <= radial; i++) {
    const theta = 2 * Math.PI * i / radial, zGlobal = z0 + (z1 - z0) * j / axial;
    const relief = patternRelief(p.pattern, theta, zGlobal, p); // global z before piece clipping
    const r = p.outerDiameter / 2 + relief;
    positions.push(r * Math.cos(theta), zGlobal, r * Math.sin(theta)); normals.push(Math.cos(theta), 0, Math.sin(theta));
  }
  for (let j = 0; j < axial; j++) for (let i = 0; i < radial; i++) { const a=j*(radial+1)+i,b=a+radial+1;indices.push(a,b,a+1,a+1,b,b+1); }
  const g = new THREE.BufferGeometry();g.setAttribute("position",new THREE.Float32BufferAttribute(positions,3));g.setAttribute("normal",new THREE.Float32BufferAttribute(normals,3));g.setIndex(indices);g.computeVertexNormals();
  return new THREE.Mesh(g, material);
}
function labelledBand(z0, z1, color, opacity, radius = 19.25) { const g=new THREE.CylinderGeometry(radius,radius,Math.max(.35,z1-z0),64,1,true);const m=new THREE.MeshBasicMaterial({color,transparent:true,opacity,side:THREE.DoubleSide,depthWrite:false});const mesh=new THREE.Mesh(g,m);mesh.position.y=(z0+z1)/2; return mesh; }
function build() {
  caseGroup.clear(); bandGroup.clear();
  const lowerMat=new THREE.MeshStandardMaterial({color:0x3fc2b6,roughness:.34,metalness:.10,flatShading:true});
  const upperMat=new THREE.MeshStandardMaterial({color:0xf0a354,roughness:.34,metalness:.10,flatShading:true});
  // Exterior intervals meet only at the seam. The penetration is visualized inside, never as a second outer shell.
  const lower=ringGeometry(0,state.seamZ,state,lowerMat); lower.name="lower-piece";
  const upper=ringGeometry(...state.upperInterval,state,upperMat); upper.name="upper-piece";
  const exploded=$("display").value === "exploded", lowerOffset=exploded?-7:0, upperOffset=exploded?7:0;
  lower.position.y=lowerOffset; upper.position.y=upperOffset;
  caseGroup.add(lower,upper);
  // Seam follows upper piece; penetration/effective overlays sit inside and follow lower piece in exploded view.
  const seam=labelledBand(state.seamZ-.22,state.seamZ+.22,0xffdb75,.96,20.12); seam.name="seam";seam.position.y+=upperOffset;
  const full=labelledBand(...state.threadBand,0xb384df,.30,19.05); full.name="full-thread-band";full.position.y+=lowerOffset;
  const effective=labelledBand(...state.effectiveBand,0xffffff,.55,18.82); effective.name="effective-thread-band";effective.position.y+=lowerOffset;
  bandGroup.add(seam,full,effective);
}
function readings() {
  const rows=[["Canonical split from top",`${fmt(state.S)} (${state.percent.toFixed(3)}%)`],["Seam global Z",fmt(state.seamZ)],["Upper piece outer / cavity",`${fmt(state.upperOuter)} / ${fmt(state.U)}`],["Lower piece outer / cavity accounting",`${fmt(state.lowerOuter)} / ${fmt(state.B)}`],["Cavity C / closed outer H",`${fmt(state.C)} / ${fmt(state.H)}`],["Full thread band",range(state.threadBand)],["Effective thread band",`${range(state.effectiveBand)} · pitch ${fmt(state.threadPitch)} · engagement ${fmt(state.engagement)}`],["Nominal radial reference gaps",`lower ${fmt(state.lowerGap)} · upper ${fmt(state.upperGap)} (device Ø${fmt(state.deviceDiameter)})`],["Visual residual-wall estimate",fmt(state.residualWall)],["Inherited R7 thread-root assumption","1.4 mm; not a validated minimum wall"],["Inherited clearance reference","0.25 mm per side; not validated by this visual model"]];
  $("readouts").innerHTML=rows.map(([a,b])=>`<dt>${a}</dt><dd>${b}</dd>`).join("");
  $("status").innerHTML=[...state.errors.map(x=>`<p class=\"error\">Red: ${x}</p>`),...state.warnings.map(x=>`<p class=\"warning\">Amber: ${x}</p>`)].join("");
  $("visual-summary").textContent=`Split ${fmt(state.S)} from the closed top; lower exterior spans global z 0 to ${fmt(state.seamZ)}, upper piece spans ${fmt(state.seamZ)} to ${fmt(state.H)}. Pattern ${state.pattern}. Full visual thread band ${range(state.threadBand)}; effective portion ${range(state.effectiveBand)}. Display mode: ${$("display").value}.`;
}
function sync(source, input) {
  const mm=$("split-mm-number"), pct=$("split-percent-number"), len=$("device-length");
  let S=state.S;
  // The emitted element is the only adapter read: sliders and number fields cannot overwrite each other.
  if(source==="percent")S=splitFromPercent(Number(input.value),state.H);if(source==="mm")S=Number(input.value);
  state=deriveSimulator({...state,deviceLength:Number(len.value),splitFromTop:S,pattern:$("pattern").value});
  const bounds=splitPercentBounds(state.H);
  [$("split-percent"),pct].forEach(control=>{control.min=bounds.min;control.max=bounds.max;});
  $("split-mm").value=state.S;mm.value=state.S;$("split-percent").value=state.percent;pct.value=state.percent.toFixed(3);$("split-mm-value").value=fmt(state.S);$("split-percent-value").value=`${state.percent.toFixed(3)}%`;build();readings();
}
function init() {
  renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));$("viewer").append(renderer.domElement);
  scene=new THREE.Scene();scene.background=new THREE.Color(0x101417);camera=new THREE.PerspectiveCamera(34,1,.1,1000);camera.position.set(165,132,195);
  orbit=new OrbitControls(camera,renderer.domElement);orbit.target.set(0,109,0);orbit.enableDamping=true;orbit.minDistance=105;orbit.maxDistance=410;
  scene.add(new THREE.HemisphereLight(0xffffff,0x24313b,2.4));const light=new THREE.DirectionalLight(0xffffff,2);light.position.set(90,190,120);scene.add(light);caseGroup=new THREE.Group();bandGroup=new THREE.Group();scene.add(caseGroup,bandGroup);
  const grid=new THREE.GridHelper(140,14,0x32414d,0x24303a);grid.position.y=0;scene.add(grid);
  const render=()=>{const box=$("viewer").getBoundingClientRect();renderer.setSize(box.width,box.height,false);camera.aspect=box.width/box.height;camera.updateProjectionMatrix();orbit.update();renderer.render(scene,camera);requestAnimationFrame(render)};render();
  ["split-mm","split-mm-number"].forEach(id=>$(id).addEventListener("input",event=>sync("mm",event.currentTarget)));["split-percent","split-percent-number"].forEach(id=>$(id).addEventListener("input",event=>sync("percent",event.currentTarget)));["device-length","pattern","display"].forEach(id=>$(id).addEventListener("input",event=>sync("other",event.currentTarget)));sync("other",$("device-length"));
}
try { init(); } catch (error) { const e=$("load-error");e.hidden=false;e.textContent=`Three.js failed to load: ${error.message}. Check the declared pinned CDN dependency and network access.`;console.error(error); }
