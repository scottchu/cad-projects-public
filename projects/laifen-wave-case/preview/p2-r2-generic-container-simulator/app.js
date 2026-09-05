import * as THREE from "three";
import {OrbitControls} from "three/addons/controls/OrbitControls.js";
import {PRESETS,deriveContainer,patternField,percentBounds,percentToSplit,cameraFitForBox,clamp} from "./math.mjs";

const $=id=>document.getElementById(id);
const numberKeys=["H","OD","wall","F","S","p","Lr","formHeight","keepout","clearance","axial","arc","depth","chamfer","drainCount"];
const optional=["lowerBore","upperBore"];
const controlIds=[...numberKeys,...optional,"percent","N","pattern","drains","exploded"];
const unavailable="Unavailable until parameters are valid";
const readoutLabels=["Split / percent","H / OD","Bores / walls","E / P / allowance","Visual thread bands","Split range / feasibility","Thread settings","Pattern","Chamfer / drains"];
let raw={...PRESETS.generic},d=deriveContainer(raw),scene,group,renderer,cam,controls,resizeObserver;
const viewDirection=new THREE.Vector3(1,.72,1).normalize();

function syncControlsFromCanonical(rawState,derivedState){
  for(const k of numberKeys)$(k).value=String(rawState[k]);
  for(const k of optional)$(k).value=rawState[k]??"";
  $("N").value=String(rawState.N);$("pattern").value=rawState.pattern;$("drains").value=String(rawState.drains);$("exploded").value=String(rawState.exploded);
  const bounds=percentBounds(derivedState);
  $("S").min=String(derivedState.Smin);$("S").max=String(derivedState.Smax);$("S").step="0.1";$("S").value=String(rawState.S);
  $("percent").min=String(bounds.min);$("percent").max=String(bounds.max);$("percent").step="any";$("percent").value=String(100*rawState.S/rawState.H);
}

function closedEndInset(z){
  if(d.chamfer<=0)return 0;
  if(z<d.chamfer)return d.chamfer-z;
  if(z>d.H-d.chamfer)return d.chamfer-(d.H-z);
  return 0;
}

function endPatternFade(z){
  if(d.chamfer<=0)return 1;
  return clamp(Math.min(z,d.H-z)/d.chamfer,0,1);
}

function shell(a,b,color,name){
  const seg=112,rows=Math.max(10,Math.ceil((b-a)/1.6)),pos=[],idx=[],R=d.OD/2;
  for(let j=0;j<=rows;j++)for(let i=0;i<=seg;i++){
    const th=i*2*Math.PI/seg,z=a+(b-a)*j/rows;
    const taper=closedEndInset(z),relief=patternField(d.pattern,th,z,d)*endPatternFade(z);
    const r=Math.max(.05,R-taper)+relief;
    pos.push(r*Math.cos(th),z,r*Math.sin(th));
  }
  for(let j=0;j<rows;j++)for(let i=0;i<seg;i++){const x=j*(seg+1)+i,y=x+seg+1;idx.push(x,y,x+1,x+1,y,y+1);}
  const geometry=new THREE.BufferGeometry();geometry.setAttribute("position",new THREE.Float32BufferAttribute(pos,3));geometry.setIndex(idx);geometry.computeVertexNormals();
  const mesh=new THREE.Mesh(geometry,new THREE.MeshStandardMaterial({color,roughness:.36,metalness:.08,flatShading:true,side:THREE.DoubleSide}));mesh.name=name;return mesh;
}

function circleLine(z,r,color,name){
  const pts=[];for(let i=0;i<96;i++){const th=2*Math.PI*i/96;pts.push(new THREE.Vector3(r*Math.cos(th),z,r*Math.sin(th)));}
  const line=new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints(pts),new THREE.LineBasicMaterial({color,transparent:true,opacity:.9}));line.name=name;return line;
}

function endDisc(z,color,name,isTop){
  const r=Math.max(.05,d.OD/2-d.chamfer);
  const mesh=new THREE.Mesh(new THREE.CircleGeometry(r,96),new THREE.MeshStandardMaterial({color,side:THREE.DoubleSide,roughness:.42}));
  mesh.rotation.x=isTop?-Math.PI/2:Math.PI/2;mesh.position.y=z;mesh.name=name;return mesh;
}

function drainApertures(z,isTop){
  const apertures=new THREE.Group();apertures.name=isTop?"upper-drain-apertures":"lower-drain-apertures";
  if(!d.drains||d.drainCount===0)return apertures;
  const endRadius=Math.max(.5,d.OD/2-d.chamfer),holeRadius=Math.max(.45,Math.min(1.25,endRadius*.075));
  const ringRadius=d.drainCount===1?0:Math.max(0,endRadius*.55);
  for(let i=0;i<d.drainCount;i++){
    const th=d.drainCount===1?0:2*Math.PI*i/d.drainCount;
    const aperture=new THREE.Mesh(new THREE.CircleGeometry(holeRadius,24),new THREE.MeshBasicMaterial({color:0x050708,side:THREE.DoubleSide}));
    aperture.rotation.x=isTop?-Math.PI/2:Math.PI/2;aperture.position.set(ringRadius*Math.cos(th),z+(isTop?.055:-.055),ringRadius*Math.sin(th));aperture.name=`${isTop?"upper":"lower"}-drain-aperture-${i+1}`;apertures.add(aperture);
  }
  return apertures;
}

function bracket(a,b,color,name,off){
  const x=d.OD/2+off,t=4.5,pts=[new THREE.Vector3(x,a,0),new THREE.Vector3(x,b,0),new THREE.Vector3(x-t,a,0),new THREE.Vector3(x+t,a,0),new THREE.Vector3(x-t,b,0),new THREE.Vector3(x+t,b,0)];
  const line=new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(pts),new THREE.LineBasicMaterial({color}));line.name=name;return line;
}

function marker(){
  const markerGroup=new THREE.Group();markerGroup.name=d.exploded?"exploded-thread-band-marker":"assembled-thread-band-marker";
  markerGroup.add(bracket(...d.threadBand,0xc39cf2,"full-visual-thread-band-bracket",7),bracket(...d.effectiveBand,0xffffff,"effective-thread-engagement-bracket",14));return markerGroup;
}

function build(){
  group.clear();
  if(!d.valid){window.__containerSimulator={scene,group,derived:d,lastFit:null};renderScale();return;}
  const low=shell(0,d.z0,0x45c5b8,"lower-piece"),up=shell(d.z0,d.H,0xe9a356,"upper-piece");
  low.add(endDisc(0,0x329a91,"lower-closed-end",false));
  up.add(endDisc(d.H,0xc98240,"upper-closed-end",true));
  if(d.drains&&d.drainCount>0){low.add(drainApertures(0,false));up.add(drainApertures(d.H,true));}
  if(d.chamfer>0){low.add(circleLine(d.chamfer,d.OD/2,0x8ce8dc,"lower-chamfer-transition"));up.add(circleLine(d.H-d.chamfer,d.OD/2,0xffc47e,"upper-chamfer-transition"));}
  const mark=marker(),seam=circleLine(d.z0,d.OD/2+.35,0xffd86b,"seam-marker");
  if(d.exploded){const gap=Math.max(5,Math.min(14,d.H*.06));low.position.y=-gap;up.position.y=gap;}
  group.add(low,up,seam,mark);renderScale();
  requestAnimationFrame(()=>fitCamera("geometry-build"));
}

function fitCamera(reason="update"){
  if(!d.valid||!group.children.length)return;
  scene.updateMatrixWorld(true);
  const box=new THREE.Box3().setFromObject(group);if(box.isEmpty())return;
  const size=box.getSize(new THREE.Vector3()),center=box.getCenter(new THREE.Vector3());
  const fit=cameraFitForBox(size,cam.aspect,cam.fov,1.16);if(!fit)return;
  controls.target.copy(center);cam.position.copy(center).addScaledVector(viewDirection,fit.distance);cam.near=fit.near;cam.far=fit.far;cam.updateProjectionMatrix();controls.maxDistance=fit.far*.8;controls.update();
  window.__containerSimulator={scene,group,derived:d,lastFit:{reason,size:{x:size.x,y:size.y,z:size.z},center:{x:center.x,y:center.y,z:center.z},...fit}};
}

function resizeAndFit(){
  const rect=$("viewer").getBoundingClientRect(),width=Math.max(1,rect.width),height=Math.max(1,rect.height);
  renderer.setSize(width,height,false);cam.aspect=width/height;cam.updateProjectionMatrix();fitCamera("ResizeObserver");
}

function renderDetail(){
  const canvas=$("detail"),ctx=canvas.getContext("2d");ctx.clearRect(0,0,canvas.width,canvas.height);
  if(!d.valid){canvas.classList.add("unavailable");canvas.setAttribute("aria-label",unavailable);$("detailUnavailable").hidden=false;$("detailText").textContent=unavailable;return;}
  canvas.classList.remove("unavailable");$("detailUnavailable").hidden=true;
  const scale=d.depth>0&&d.depth<.25?4:1,denom=Math.max(d.depth,1e-9);
  for(let i=0;i<canvas.width;i++)for(let j=0;j<canvas.height;j++){
    const relief=patternField(d.pattern,2*Math.PI*i/canvas.width,d.z0+j/canvas.height*d.axial,d)*scale/denom;
    ctx.fillStyle=`hsl(${190+80*relief} 70% ${18+55*relief}%)`;ctx.fillRect(i,j,1,1);
  }
  const text=`Detail magnifier: ${scale}× radial display; requested relief ${d.depth} mm; full model is true scale.`;canvas.setAttribute("aria-label",text);$("detailText").textContent=text;
}

function renderScale(){
  const scale=$("axialScale");
  if(!d.valid){scale.hidden=true;scale.setAttribute("aria-label",unavailable);return;}
  scale.hidden=false;$("scaleTop").textContent=`H ${d.H} mm`;$("scaleBottom").textContent="0 mm";
  $("fullBand").querySelector("b").textContent=`P ${d.P} mm visual thread band`;
  $("effectiveBand").querySelector("b").textContent=`E ${d.E} mm effective`;
  for(const[id,band]of[["fullBand",d.threadBand],["effectiveBand",d.effectiveBand]]){
    const el=$(id),low=band[0],high=band[1];el.style.top=`${100*(d.H-high)/d.H}%`;el.style.height=`${Math.max(1.2,100*(high-low)/d.H)}%`;
  }
  const view=d.exploded?"exploded":"assembled";scale.setAttribute("aria-label",`Global Z scale, ${view} view. Visual thread band ${d.threadBand[0].toFixed(2)} to ${d.threadBand[1].toFixed(2)} mm; effective ${d.effectiveBand[0].toFixed(2)} to ${d.effectiveBand[1].toFixed(2)} mm.`);
}

function applyFieldErrors(){
  for(const id of controlIds){const el=$(id);el.removeAttribute("aria-invalid");el.removeAttribute("aria-errormessage");el.removeAttribute("aria-describedby");}
  for(const {fieldId} of d.fieldErrors){const el=$(fieldId);if(!el)continue;el.setAttribute("aria-invalid","true");el.setAttribute("aria-errormessage","status");el.setAttribute("aria-describedby","status");}
}

function renderReadout(){
  const status=$("status");status.setAttribute("aria-atomic","true");
  if(!d.valid){
    $("readout").innerHTML=readoutLabels.map(label=>`<dt>${label}</dt><dd>${unavailable}</dd>`).join("");
    status.setAttribute("role","alert");status.setAttribute("aria-live","assertive");status.textContent=d.errors.join(" ");$("warnings").textContent="";applyFieldErrors();return;
  }
  const turns=d.N===1?"turn":"turns";
  const lines=[
    ["Split / percent",`${d.S.toFixed(3)} mm / ${d.percent.toFixed(5)}%`],
    ["H / OD",`${d.H} / ${d.OD} mm`],
    ["Bores / walls",`${d.lowerBore}/${d.upperBore} mm · ${d.lowerWall.toFixed(2)}/${d.upperWall.toFixed(2)} mm`],
    ["E / P / allowance",`${d.E.toFixed(2)} / ${d.P.toFixed(2)} / ${d.nonEffective.toFixed(2)} mm`],
    ["Visual thread bands",`full ${d.threadBand.map(x=>x.toFixed(2)).join("–")} mm; effective ${d.effectiveBand.map(x=>x.toFixed(2)).join("–")} mm`],
    ["Split range / feasibility",`${d.Smin.toFixed(2)}–${d.Smax.toFixed(2)} mm; H ≥ 2×(F+P+K) = ${(2*(d.F+d.P+d.K)).toFixed(2)} mm; K=${d.K.toFixed(2)}`],
    ["Thread settings",`${d.p} mm pitch · ${d.N} ${turns} · ${d.formHeight} mm form reference · ${d.clearance} mm clearance/side`],
    ["Pattern",`${d.pattern}: count ${d.count}, axial ${d.axial} mm, actual arc ${d.actualArc.toFixed(2)} mm, depth ${d.depth} mm`],
    ["Chamfer / drains",`${d.chamfer} mm / ${d.drains?`on, ${d.drainCount} apertures`:"off"}`]
  ];
  $("readout").innerHTML=lines.map(([label,value])=>`<dt>${label}</dt><dd>${value}</dd>`).join("");
  const summary=`H ${d.H} mm, OD ${d.OD} mm, split S ${d.S} mm, effective E ${d.E} mm, full band P ${d.P} mm, ${d.pattern} pattern, ${d.exploded?"exploded":"assembled"} view.`;
  status.setAttribute("role","status");status.setAttribute("aria-live","polite");status.textContent=d.warnings.length?`Warning: ${d.warnings.join(" ")} ${summary}`:`Valid: ${summary}`;
  $("warnings").textContent="";applyFieldErrors();
}

function renderAll(){build();renderDetail();renderReadout();}

function update(source,element){
  if(source==="percent"){
    const b=percentBounds(d);raw.S=percentToSplit(Number(element.value),raw.H,b?{...b,Smin:d.Smin,Smax:d.Smax}:null);
  }else if(source==="preset"){
    raw={...PRESETS[element.value]};d=deriveContainer(raw);if(d.valid)syncControlsFromCanonical(raw,d);renderAll();return;
  }else{
    const key=element.id;
    raw[key]=optional.includes(key)?(element.value===""?null:Number(element.value)):key==="N"?Number(element.value):key==="drains"?element.value==="true":key==="exploded"?element.value==="true":key==="pattern"?element.value:Number(element.value);
  }
  d=deriveContainer(raw);if(d.valid)syncControlsFromCanonical(raw,d);renderAll();
}

function init(){
  renderer=new THREE.WebGLRenderer({antialias:true,alpha:false});$("viewer").append(renderer.domElement);
  scene=new THREE.Scene();scene.background=new THREE.Color(0x0e1317);cam=new THREE.PerspectiveCamera(34,1,.1,1000);
  controls=new OrbitControls(cam,renderer.domElement);controls.enableDamping=true;controls.dampingFactor=.08;
  scene.add(new THREE.HemisphereLight(0xffffff,0x23333d,2));const light=new THREE.DirectionalLight(0xffffff,2);light.position.set(100,180,80);scene.add(light);
  group=new THREE.Group();group.name="two-piece-container-visual";scene.add(group);
  resizeObserver=new ResizeObserver(resizeAndFit);resizeObserver.observe($("viewer"));
  for(const id of controlIds)$(id).addEventListener("input",event=>update(id,event.currentTarget));
  $("preset").addEventListener("input",event=>update("preset",event.currentTarget));
  syncControlsFromCanonical(raw,d);resizeAndFit();build();renderDetail();renderReadout();
  (function animate(){controls.update();renderer.render(scene,cam);requestAnimationFrame(animate);})();
}

try{init();}catch(error){const status=$("status");status.setAttribute("role","alert");status.setAttribute("aria-live","assertive");status.textContent=`Renderer/CDN error: ${error.message}`;}
