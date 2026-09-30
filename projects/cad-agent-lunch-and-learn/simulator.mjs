import * as THREE from 'three';

// Read-only teaching geometry; dimensions and fit observations are never predictions.
const scenes = new Map();
const material = (color) => new THREE.MeshStandardMaterial({ color, roughness: .7 });
function mesh(geometry, color, position, scene) {
  const object = new THREE.Mesh(geometry, material(color));
  object.position.set(...position); object.castShadow = true; object.receiveShadow = true; scene.add(object); return object;
}
function fitGeometry(scene) {
  const rod = mesh(new THREE.CylinderGeometry(2, 2, 6, 48), '#af492d', [0, 0, 0], scene); rod.rotation.x = Math.PI / 2;
  const nominalHole = 4.05, rodDiameter = 4, radialClearance = (nominalHole - rodDiameter) / 2;
  const bore = 2 + 8 * radialClearance, outer = 4.4, shape = new THREE.Shape(), end = 1.5 * Math.PI;
  for (let n = 0; n <= 48; n++) { const a = n * end / 48, x = outer * Math.cos(a), y = outer * Math.sin(a); n ? shape.lineTo(x,y) : shape.moveTo(x,y); }
  for (let n = 48; n >= 0; n--) { const a=n*end/48;shape.lineTo(bore*Math.cos(a),bore*Math.sin(a)); }
  shape.closePath(); const guide = new THREE.ExtrudeGeometry(shape, { depth:2.4, bevelEnabled:false }); guide.translate(0,0,-1.2);
  mesh(guide,'#14665f',[0,0,0],scene);
}
function fallback(host) { scenes.set(host,{failed:true}); host.classList.remove('ready');host.querySelector('.scene-status').hidden=false; }
function draw(host) {
  const state=scenes.get(host);if(!state||state.failed||!host.closest('.slide').classList.contains('active'))return;
  const box=host.querySelector('.scene-canvas');if(!box.clientWidth)return;
  state.renderer.setSize(box.clientWidth,box.clientHeight,false);state.camera.aspect=box.clientWidth/box.clientHeight;state.camera.updateProjectionMatrix();state.renderer.render(state.scene,state.camera);
  const annotations=host.querySelector('.scene-annotations');
  if(annotations){annotations.setAttribute('viewBox',`0 0 ${box.clientWidth} ${box.clientHeight}`);for(const [name,point,side,y] of [['rod',new THREE.Vector3(0,0,3),'left',.76],['guide',new THREE.Vector3(2.6,2.5,0),'right',.15]]){const q=point.project(state.camera),label=annotations.querySelector('[data-label="'+name+'"]'),line=annotations.querySelector('[data-leader="'+name+'"]'),x=side==='left'?12:box.clientWidth-12;label.setAttribute('x',x);label.setAttribute('y',box.clientHeight*y);label.setAttribute('text-anchor',side==='left'?'start':'end');line.setAttribute('x1',side==='left'?x+76:x-104);line.setAttribute('y1',box.clientHeight*y-5);line.setAttribute('x2',(q.x+1)*box.clientWidth/2);line.setAttribute('y2',(1-q.y)*box.clientHeight/2);}}

}
function initialize(host) {
  if(scenes.has(host)||!host.closest('.slide').classList.contains('active'))return;
  try {
    const renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
    renderer.domElement.addEventListener('webglcontextlost',event=>{event.preventDefault();fallback(host)});
    const scene=new THREE.Scene();scene.background=new THREE.Color('#ffffff');scene.add(new THREE.HemisphereLight(0xffffff,0x59635b,2.5));
    const light=new THREE.DirectionalLight(0xffffff,3);light.position.set(5,10,7);light.castShadow=true;light.shadow.mapSize.set(1024,1024);Object.assign(light.shadow.camera,{left:-8,right:8,top:8,bottom:-8});scene.add(light);
    const camera=new THREE.PerspectiveCamera(38,1,.1,100);
    fitGeometry(scene);camera.position.set(11,8,13);camera.lookAt(0,0,0);
    host.querySelector('.scene-canvas').replaceChildren(renderer.domElement);scenes.set(host,{renderer,scene,camera});host.classList.add('ready');draw(host);
  }catch{fallback(host)}
}
const hosts=[...document.querySelectorAll('[data-scene]')];
new MutationObserver(()=>hosts.forEach(host=>{initialize(host);draw(host)})).observe(document.querySelector('.deck'),{attributes:true,attributeFilter:['class'],subtree:true});
addEventListener('resize',()=>hosts.forEach(draw));hosts.forEach(initialize);
