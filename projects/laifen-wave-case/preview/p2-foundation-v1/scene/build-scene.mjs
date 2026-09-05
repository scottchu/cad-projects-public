import * as THREE from "three";

const material = color => new THREE.MeshStandardMaterial({color, roughness:.48, metalness:.08, side:THREE.DoubleSide, polygonOffset:true, polygonOffsetFactor:1, polygonOffsetUnits:1});
const range = n => Array.from({length:n}, (_, i) => i);
const ring = (d, z, inset=0) => range(d.section.radialSegments).map(i => {
  const a=2*Math.PI*i/d.section.radialSegments;
  const r=(d.section.kind === "round" ? d.R : d.R*Math.cos(Math.PI/d.section.N)/Math.cos(((a+Math.PI/d.section.N)%(2*Math.PI/d.section.N))-Math.PI/d.section.N))-inset;
  return [r*Math.cos(a),r*Math.sin(a),z];
});
function indexed(vertices, indices) {
  const g=new THREE.BufferGeometry(); g.setAttribute("position",new THREE.Float32BufferAttribute(vertices.flat(),3)); g.setIndex(indices); g.computeVertexNormals(); g.computeBoundingBox(); return g;
}
function connect(vertices, indices, a, b, n, reverse=false) {
  for(const i of range(n)){const j=(i+1)%n; const q=reverse?[a+i,b+i,b+j,a+j]:[a+i,a+j,b+j,b+i];indices.push(...q);}
}
function shellGeometry(d, lower) {
  const n=d.section.radialSegments,z0=lower?0:d.splitZ,z1=lower?d.splitZ:d.inputs.H;
  const lowerEnd=lower?d.ends.bottom.size:0, upperEnd=lower?0:d.ends.top.size;
  const outer0=ring(d,z0+lowerEnd),outer1=ring(d,z1-upperEnd),inner0=ring(d,lower?d.inputs.F:d.splitZ,d.inputs.W),inner1=ring(d,lower?d.splitZ:d.inputs.H-d.inputs.F,d.inputs.W);
  const vertices=[...outer0,...outer1,...inner0,...inner1],indices=[];
  connect(vertices,indices,0,n,n); connect(vertices,indices,2*n,3*n,n,true);
  // Seam rim reveals wall thickness, preserving the cavity rather than capping it.
  const seamOuter=lower?n:0,seamInner=lower?3*n:2*n; connect(vertices,indices,seamOuter,seamInner,n,lower);
  return indexed(vertices,indices);
}
function endGeometry(d, bottom) {
  const e=bottom?d.ends.bottom:d.ends.top,n=d.section.radialSegments,base=bottom?0:d.inputs.H,dir=bottom?1:-1;
  const path=e.path,vertices=[],indices=[];
  for(const point of path) vertices.push(...range(n).map(i=>{const a=2*Math.PI*i/n;return [point.r*Math.cos(a),point.r*Math.sin(a),base+point.z];}));
  for(let row=0;row<path.length-1;row++) connect(vertices,indices,row*n,(row+1)*n,n);
  // A small radial cap is an actual end surface for flat and shaped profiles.
  const cap=vertices.length; vertices.push([0,0,base]); for(const i of range(n)) indices.push(cap,i,(i+1)%n);
  return indexed(vertices,indices);
}
function floorGeometry(d, bottom) {
  const R=d.ID/2,n=d.section.radialSegments,z=bottom?0:d.inputs.H-d.inputs.F,depth=d.inputs.F;
  const shape=new THREE.Shape();
  for(const i of range(n+1)){const a=2*Math.PI*i/n;const x=R*Math.cos(a),y=R*Math.sin(a);if(i===0)shape.moveTo(x,y);else shape.lineTo(x,y);}
  const active=d.drains.location === (bottom?"bottom":"top");
  if(active) for(const h of d.drains.positions){const hole=new THREE.Path(); hole.absarc(h.x,h.y,h.r,0,2*Math.PI,true);shape.holes.push(hole);}
  const g=new THREE.ExtrudeGeometry(shape,{depth,bevelEnabled:false,curveSegments:Math.max(12,n)});g.translate(0,0,z);if(!g.getIndex())g.setIndex(range(g.getAttribute("position").count));g.computeVertexNormals();g.computeBoundingBox();return g;
}
function merge(geometries) {
  const vertices=[],indices=[];let offset=0;
  for(const geometry of geometries){const p=geometry.getAttribute("position"),idx=geometry.getIndex();for(let i=0;i<p.count;i++)vertices.push([p.getX(i),p.getY(i),p.getZ(i)]);for(const i of range(idx?idx.count:p.count))indices.push((idx?idx.getX(i):i)+offset);offset+=p.count;}
  return indexed(vertices,indices);
}
function helixGeometry(d, male) {
  const {pitch:P,turns:T,depth:D,radialClearance:C,form}=d.screw, samples=T*48, z0=male?d.splitZ-d.screw.engagement:d.splitZ;
  const vertices=[],indices=[],root=d.R-d.inputs.W;
  for(const i of range(samples+1)){
    const u=i/samples, a=2*Math.PI*T*u+(male?0:Math.PI), z=z0+u*P*T;
    const rounded=form === "rounded" ? .5+.5*Math.cos((u*T%1-.5)*2*Math.PI) : Math.max(0,1-Math.abs((u*T%1-.5)*2)*1.4);
    const crest=male?root-C:root;
    const base=male?crest-D:root-D;
    const r=base+(crest-base)*rounded;
    for(const delta of [-P*.22,P*.22]) vertices.push([r*Math.cos(a),r*Math.sin(a),z+delta]);
  }
  for(const i of range(samples)){const k=2*i;indices.push(k,k+1,k+3,k,k+3,k+2);}
  return indexed(vertices,indices);
}
function seamGeometry(d) { return new THREE.RingGeometry(d.ID/2,d.R, d.section.radialSegments,1,0,Math.PI*2).rotateX(Math.PI/2).translate(0,0,d.splitZ); }
function assertDescriptor(d) { if(!d || d.version!=="p2-foundation-v1" || !Number.isFinite(d.R) || !d.plans) throw new TypeError("buildScene requires a complete valid V1 descriptor."); }

export function buildScene(descriptor) {
  assertDescriptor(descriptor); const d=descriptor, root=new THREE.Group(); root.name="v1.scene";
  const lower=new THREE.Group(),upper=new THREE.Group(); upper.position.z=d.pieces.upper.z; root.add(lower,upper);
  const lowerShell=new THREE.Mesh(merge([shellGeometry(d,true),floorGeometry(d,true)]),material(0x356a96)); lowerShell.name="v1.lower.shell"; lower.add(lowerShell);
  const upperShell=new THREE.Mesh(merge([shellGeometry(d,false),floorGeometry(d,false)]),material(0x77a8ca)); upperShell.name="v1.upper.shell"; upper.add(upperShell);
  const bottomEnd=new THREE.Mesh(endGeometry(d,true),material(0x2d5271)); bottomEnd.name="v1.end.bottom"; lower.add(bottomEnd);
  const topEnd=new THREE.Mesh(endGeometry(d,false),material(0x5f8faa)); topEnd.name="v1.end.top"; upper.add(topEnd);
  const male=new THREE.Mesh(helixGeometry(d,true),material(0xd8a83b));male.name="v1.closure.maleThread";lower.add(male);
  const female=new THREE.Mesh(helixGeometry(d,false),material(0xf2cf70));female.name="v1.closure.femaleThread";upper.add(female);
  if(d.drains.location==="bottom"){const drains=new THREE.Mesh(floorGeometry(d,true),material(0x1e425d));drains.name="v1.drains.bottom";lower.add(drains);}
  if(d.drains.location==="top"){const drains=new THREE.Mesh(floorGeometry(d,false),material(0x406b80));drains.name="v1.drains.top";upper.add(drains);}
  const seam=new THREE.Mesh(seamGeometry(d),new THREE.MeshBasicMaterial({color:0xe8eff2,side:THREE.DoubleSide}));seam.name="v1.seam";lower.add(seam);
  root.updateMatrixWorld(true); return root;
}

export const namedMeshFacts = root => {
  const facts={};root.traverse(o=>{if(o.name.startsWith("v1.")){const g=o.geometry;if(g){g.computeBoundingBox();const b=g.boundingBox;facts[o.name]={vertices:g.getAttribute("position")?.count??0,indices:g.getIndex()?.count??0,bounds:b?{min:b.min.toArray(),max:b.max.toArray()}:null};}}});return facts;
};
