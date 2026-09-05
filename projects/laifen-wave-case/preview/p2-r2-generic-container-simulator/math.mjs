export const PRESETS={
  generic:{H:120,OD:60,wall:2.4,F:3,S:60,p:2,N:2,Lr:1.5,formHeight:.5,keepout:2.4,pattern:"blunt_diamond",axial:4.8,arc:3.63,depth:.45,chamfer:1.2,drains:true,drainCount:7,lowerBore:null,upperBore:null,clearance:.25,exploded:false},
  laifen_wave_reference:{H:219,OD:39,wall:2.4,F:3,S:84,p:2,N:3,Lr:1.5,formHeight:.5,keepout:2.4,pattern:"blunt_diamond",axial:4.8,arc:3.63,depth:.45,chamfer:1.2,drains:true,drainCount:7,lowerBore:30,upperBore:31,clearance:.25,exploded:false},
  wide_short_makeup_jar:{H:55,OD:80,wall:3,F:3,S:27.5,p:3,N:1,Lr:1.5,formHeight:.5,keepout:4,pattern:"blunt_diamond",axial:8,arc:6,depth:.35,chamfer:1,drains:false,drainCount:0,lowerBore:null,upperBore:null,clearance:.25,exploded:false}
};

export const clamp=(x,a,b)=>Math.min(b,Math.max(a,x));

export function percentBounds(d){
  if(!d?.feasible||![d.H,d.Smin,d.Smax].every(Number.isFinite)||d.H<=0)return null;
  return {min:100*d.Smin/d.H,max:100*d.Smax/d.H};
}

export function percentToSplit(percent,H,bounds){
  if(!Number.isFinite(percent)||!Number.isFinite(H)||H<=0)return NaN;
  const raw=H*percent/100,t=.002;
  if(bounds&&percent>=bounds.min-.0005&&raw>=bounds.Smin-t&&raw<=bounds.Smin)return bounds.Smin;
  if(bounds&&percent<=bounds.max+.0005&&raw<=bounds.Smax+t&&raw>=bounds.Smax)return bounds.Smax;
  return raw;
}

export function cameraFitForBox(size,aspect,fovDeg=34,margin=1.18){
  const w=Math.max(0,Number(size?.x??size?.width??0));
  const h=Math.max(0,Number(size?.y??size?.height??0));
  const d=Math.max(0,Number(size?.z??size?.depth??0));
  if(![w,h,d,aspect,fovDeg,margin].every(Number.isFinite)||aspect<=0||fovDeg<=0||fovDeg>=179||margin<=0)return null;
  const radius=Math.max(.01,.5*Math.hypot(w,h,d));
  const verticalFov=fovDeg*Math.PI/180;
  const horizontalFov=2*Math.atan(Math.tan(verticalFov/2)*aspect);
  const verticalDistance=margin*radius/Math.sin(verticalFov/2);
  const horizontalDistance=margin*radius/Math.sin(horizontalFov/2);
  const distance=Math.max(verticalDistance,horizontalDistance);
  return {distance,near:Math.max(.01,distance-radius*1.35),far:distance+radius*3,radius,verticalFov,horizontalFov,verticalDistance,horizontalDistance};
}

export function deriveContainer(v={}){
  const p={...PRESETS.generic,...v},fieldErrors=[];
  const add=(fieldId,message)=>fieldErrors.push({fieldId,message});
  const positive=[["H","H"],["OD","OD"],["wall","wall"],["F","floor"],["p","thread pitch"],["formHeight","thread form height"],["axial","axial pitch"],["arc","arc pitch"]];
  const nonnegative=[["Lr","lead/runout"],["keepout","keepout"],["clearance","clearance"],["depth","depth"],["chamfer","chamfer"]];
  for(const[id,label]of positive)if(!Number.isFinite(p[id])||p[id]<=0)add(id,`${label} must be finite and > 0.`);
  for(const[id,label]of nonnegative)if(!Number.isFinite(p[id])||p[id]<0)add(id,`${label} must be finite and >= 0.`);
  if(![1,2,3].includes(p.N))add("N","turns must be exactly 1, 2, or 3.");
  if(!["smooth","blunt_diamond","shallow_helix","wave_flutes"].includes(p.pattern))add("pattern","pattern enum is invalid.");
  if(typeof p.drains!=="boolean")add("drains","drains flag must be boolean.");
  if(typeof p.exploded!=="boolean")add("exploded","view flag must be boolean.");
  if(!Number.isInteger(p.drainCount)||p.drainCount<0)add("drainCount","drain count must be an integer >= 0.");
  for(const[id,label]of[["lowerBore","lower bore"],["upperBore","upper bore"]])if(p[id]!==null&&(!Number.isFinite(p[id])||p[id]<=0||!(Number.isFinite(p.OD)&&p[id]<p.OD)))add(id,`${label} override must be null or finite, positive, and below OD.`);
  if(Number.isFinite(p.OD)&&Number.isFinite(p.wall)&&p.OD<=2*p.wall){add("OD","OD must exceed twice wall.");add("wall","OD must exceed twice wall.");}

  const baseValid=fieldErrors.length===0;
  const inner=p.OD-2*p.wall,lowerBore=p.lowerBore??inner,upperBore=p.upperBore??inner;
  const E=p.p*p.N,P=p.p*(p.N+p.Lr),K=Math.max(p.keepout,p.chamfer,.5*p.axial);
  const Smin=p.F+P+K,Smax=p.H-(p.F+P+K);
  const heightFeasible=baseValid&&p.H>=2*(p.F+P+K)&&Smin<=Smax;
  if(baseValid&&!heightFeasible){
    const message=`Required H >= 2*(F+P+K) = ${(2*(p.F+P+K)).toFixed(2)} mm; received H = ${p.H} mm. F=${p.F.toFixed(2)}, P=${P.toFixed(2)}, K=${K.toFixed(2)}, S_min=${Smin.toFixed(2)}, S_max=${Smax.toFixed(2)} mm.`;
    for(const id of["H","F","p","N","Lr","keepout","chamfer","axial"])add(id,message);
  }
  if(heightFeasible&&(!Number.isFinite(p.S)||p.S<Smin||p.S>Smax)){
    const message=`Valid raw split range: ${Smin.toFixed(2)}–${Smax.toFixed(2)} mm; received S = ${p.S}.`;
    add("S",message);add("percent",message);
  }
  const errors=[...new Set(fieldErrors.map(x=>x.message))];
  const valid=errors.length===0;
  const feasible=heightFeasible&&valid;
  const z0=p.H-p.S,Dref=p.OD-2*p.depth;
  const count=baseValid?Math.max(1,Math.round(Math.PI*Math.max(1,Dref)/p.arc)):NaN;
  const warnings=[];
  const lowerWall=(p.OD-lowerBore)/2,upperWall=(p.OD-upperBore)/2;
  if(valid&&p.depth>Math.min(lowerWall,upperWall))warnings.push("Pattern depth exceeds a wall readout; all wall and clearance values are geometric references only.");
  if(valid&&p.depth>0&&p.depth<.25)warnings.push("Detail magnifier is enabled because requested relief is below 0.25 mm; the main model remains true scale.");
  return {...p,inner,lowerBore,upperBore,lowerWall,upperWall,E,P,nonEffective:P-E,K,Smin,Smax,feasible,z0,percent:Number.isFinite(p.H)&&p.H!==0?100*p.S/p.H:NaN,threadBand:[z0,z0+P],effectiveBand:[z0,z0+E],count,actualArc:Number.isFinite(count)?Math.PI*Math.max(1,Dref)/count:NaN,errors,fieldErrors,warnings,valid};
}

const wrap=x=>x-Math.floor(x+.5);
export function patternField(id,theta,z,p){
  if(id==="smooth")return 0;
  const phaseT=p.phaseTheta||0,phaseZ=p.phaseZ||0;
  if(id==="blunt_diamond"){
    const u=p.count*(theta-phaseT)/(2*Math.PI),v=(z-phaseZ)/p.axial;
    return p.depth*clamp((.5-Math.max(Math.abs(wrap(u+v)),Math.abs(wrap(u-v))))/(.5-.18),0,1);
  }
  if(id==="shallow_helix")return p.depth*(.5+.5*Math.sin(10*(theta-phaseT)+2*Math.PI*(z-phaseZ)/(p.axial*5)));
  return p.depth*(.5+.5*Math.cos(12*(theta-phaseT)+.2*Math.sin(2*Math.PI*(z-phaseZ)/(p.axial*5))));
}
