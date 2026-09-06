import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js';
import {STLLoader} from 'three/examples/jsm/loaders/STLLoader.js';
import {dimensionAnchor} from './dimensions.mjs';
export function createViewer(canvas,overlay,description) {
  const renderer=new THREE.WebGLRenderer({canvas,antialias:true});
  renderer.setPixelRatio(Math.min(devicePixelRatio,2)); renderer.localClippingEnabled=true;
  const scene=new THREE.Scene();scene.background=new THREE.Color('#fafbfc');
  const camera=new THREE.PerspectiveCamera(34,1,.1,5000);camera.up.set(0,0,1);
  const orbit=new OrbitControls(camera,canvas);orbit.enableDamping=true;
  const light=new THREE.DirectionalLight(0xffffff,3.2);light.position.set(-80,-150,280);scene.add(light);
  scene.add(new THREE.HemisphereLight(0xffffff,0x9ba6b3,2.5));
  const plane=new THREE.Plane(new THREE.Vector3(0,1,0),0);
  let mesh=null,values=null,mode='cutaway',dimension='height',width=0,height=0;
  const context=overlay.getContext('2d');
  function clear() {if(mesh){scene.remove(mesh);mesh.geometry.dispose();mesh.material.dispose();mesh=null;}values=null;description.textContent='';}
  function reset() {
    if(!mesh)return;
    const box=new THREE.Box3().setFromObject(mesh),center=box.getCenter(new THREE.Vector3()),size=box.getSize(new THREE.Vector3());
    const distance=Math.max(size.z,size.x/Math.max(camera.aspect,.1),size.y)*2.05;
    camera.position.set(center.x+distance*.16,center.y-distance,center.z+distance*.18);
    orbit.target.copy(center);orbit.update();
  }
  function setMode(next) {mode=next;if(mesh)mesh.material.clippingPlanes=mode==='cutaway'?[plane]:[];}
  function install(bytes,snapshot) {
    const buffer=bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength);
    const geometry=new STLLoader().parse(buffer);
    if(!geometry.getAttribute('position')?.count) {geometry.dispose();throw Error('Empty preview geometry');}
    geometry.computeVertexNormals();clear();values=snapshot;
    mesh=new THREE.Mesh(geometry,new THREE.MeshStandardMaterial({color:0xb8c4cb,roughness:.65,metalness:.12,side:THREE.DoubleSide,clippingPlanes:mode==='cutaway'?[plane]:[]}));
    scene.add(mesh);reset();
  }
  function drawDimension() {
    context.clearRect(0,0,width,height);
    if(!mesh || values.output_mode!=='assembled' || mode!=='cutaway') {description.textContent='';return;}
    const {a,b,label}=dimensionAnchor(values,dimension);
    description.textContent=label;
    const project=p=>{const v=new THREE.Vector3(...p).project(camera);return [(v.x+1)*width/2,(-v.y+1)*height/2];};
    const p=project(a),q=project(b),angle=Math.atan2(q[1]-p[1],q[0]-p[0]);
    context.strokeStyle='#2563eb';context.fillStyle='#2563eb';context.lineWidth=1.7;
    context.beginPath();context.moveTo(...p);context.lineTo(...q);context.stroke();
    for(const [point,theta] of [[p,angle],[q,angle+Math.PI]]){context.beginPath();context.moveTo(...point);context.lineTo(point[0]+9*Math.cos(theta-.4),point[1]+9*Math.sin(theta-.4));context.moveTo(...point);context.lineTo(point[0]+9*Math.cos(theta+.4),point[1]+9*Math.sin(theta+.4));context.stroke();}
    context.font='500 13px -apple-system, sans-serif';
    const tw=context.measureText(label).width,x=Math.max(12,Math.min(width-tw-16,(p[0]+q[0])/2+14)),y=Math.max(88,Math.min(height-75,(p[1]+q[1])/2));
    context.fillStyle='#fafbfce8';context.fillRect(x-6,y-17,tw+12,25);context.fillStyle='#1859d6';context.fillText(label,x,y);
  }
  function render() {
    const rect=canvas.getBoundingClientRect();
    if(rect.width!==width || rect.height!==height){width=rect.width;height=rect.height;renderer.setSize(width,height,false);camera.aspect=width/Math.max(height,1);camera.updateProjectionMatrix();overlay.width=width*devicePixelRatio;overlay.height=height*devicePixelRatio;context.setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0);}
    orbit.update();renderer.render(scene,camera);drawDimension();requestAnimationFrame(render);
  }
  render();return {install,clear,reset,setMode,setDimension:key=>{dimension=key;}};
}
