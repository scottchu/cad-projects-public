/** Selected-family raw state and the source-native feasibility contract. */
export const PATTERNS=Object.freeze(['smooth','diamond','ribs','rings','spiral']);
export const TEXTURED=Object.freeze(PATTERNS.slice(1));
export const PATTERN_FIELDS=Object.freeze(['size','depth']);
export const PATTERN_DEFAULTS=Object.freeze(Object.fromEntries(TEXTURED.map(p=>[p,Object.freeze({size:p==='diamond'?'4.8':'6',depth:'0.45'})])));
export const patternMemories=()=>Object.fromEntries(TEXTURED.map(p=>[p,{...PATTERN_DEFAULTS[p]}]));
export const decimal=value=>typeof value==='string'&&value.trim()!==''&&/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$/.test(value.trim())&&Number.isFinite(Number(value));
export const patternRange=(pattern,key)=>key==='depth'?[.1,.6,.05]:pattern==='diamond'?[4.8,8,.1]:[4,16,.1];
export const patternLabel=(pattern,key)=>key==='depth'?'Depth':pattern==='diamond'?'Diamond size':'Spacing';
export const rawPattern=raw=>raw.patterns?.[raw.pattern]??PATTERN_DEFAULTS[raw.pattern];
export function patternFields(raw){
 const defaults={diamond_axial_pitch:4.8,diamond_arc_pitch:3.63,diamond_depth:.45,diamond_phase_deg:0,diamond_plateau_half_fraction:.18,wave_spacing:6,wave_depth:.45};
 if(raw.pattern==='smooth')return defaults;
 const group=rawPattern(raw);if(!group)return defaults;
 const size=Number(group.size),depth=Number(group.depth);
 return raw.pattern==='diamond'?{...defaults,diamond_axial_pitch:size,diamond_arc_pitch:size===4.8?3.63:size*(3.63/4.8),diamond_depth:depth}:{...defaults,wave_spacing:size,wave_depth:depth};
}
export function patternRawErrors(raw){
 if(!PATTERNS.includes(raw.pattern))return [{key:'pattern',message:'Choose a surface pattern.'}];
 if(raw.pattern==='smooth')return [];
 const group=rawPattern(raw);
 return PATTERN_FIELDS.flatMap(key=>{const [lo,hi]=patternRange(raw.pattern,key);return !decimal(group[key])?[{key,message:'Enter a number in millimetres.'}]:Number(group[key])<lo||Number(group[key])>hi?[{key,message:`Use a value from ${lo} to ${hi} mm.`}]:[];});
}
export function waveEstimate(h,n,spacing,chamfer,ribs=false){const m=ribs?1:Math.ceil(h/(spacing/16));return 2*n*(m+2)+4*n*Math.min(m+1,Math.ceil(chamfer*m/h)+2)+2*n;}
export function assertPatternPreflight(v){
 if(v.surface_style==='smooth')return;
 const diamond=v.surface_style==='diamond';
 const d=diamond?v.diamond_depth:v.wave_depth,s=diamond?v.diamond_axial_pitch:v.wave_spacing;
 if(![s,d].every(Number.isFinite)||s<(diamond?4.8:4)||s>(diamond?8:16)||d<.1||d>.6)throw Error('pattern values outside design range');
 const r=v.outer_diameter/2-d,crest=v.body_bore/2+v.thread_root_wall+v.thread_depth;
 if(diamond){
  // Preserve the accepted Diamond guard operation order.
  if(r-(crest+v.thread_clearance)<1.8||r-(v.body_bore/2+v.thread_root_wall+v.thread_clearance+.4)<1.8)throw Error('diamond wall below required thickness');
  if(r-v.body_bore/2<v.minimum_wall||r-v.cap_bore/2<v.minimum_wall)throw Error('pattern source shell constraint failed');
 }else{
  // Compare constructed diameter requirements, avoiding cancellation in an
  // equality residual. SCAD uses this same addition and multiplication order.
  const shell=v.minimum_wall+d+.01;
  const thread=(v.thread_root_wall+v.thread_depth+v.thread_clearance+1.8)+d+.01;
  const entry=(v.thread_root_wall+v.thread_clearance+.4+1.8)+d+.01;
  if(v.outer_diameter<v.body_bore+2*thread||v.outer_diameter<v.body_bore+2*entry)throw Error(`${v.surface_style} wall below required thickness`);
  if(v.outer_diameter<v.body_bore+2*shell||v.outer_diameter<v.cap_bore+2*shell)throw Error('pattern source shell constraint failed');
 }
 const total=v.device_length+v.axial_allowance+2*v.floor_thickness,cap=v.split_mode==='percentage'?total*v.split_percent_from_top/100:v.split_distance_from_top,body=total-cap;
 let estimate;
 if(diamond){
  if(v.diamond_arc_pitch!==(s===4.8?3.63:s*(3.63/4.8))||v.diamond_phase_deg!==0||v.diamond_plateau_half_fraction!==.18)throw Error('diamond derived values changed');
  const count=Math.floor(2*Math.PI*r/v.diamond_arc_pitch+.5),arc=2*Math.PI*r/count;
  if(count<8||count>128||.36*arc*s/Math.sqrt(arc*arc+s*s)<1||d/(s*.32)>1)throw Error('diamond source constraint failed');
  estimate=h=>16*count*(Math.ceil(h/(s/8))+1);
 }else{
  const count=Math.floor(2*Math.PI*r/s+.5),ribs=v.surface_style==='ribs';
  if(ribs&&count<3)throw Error('Ribs needs at least three ridges; reduce spacing.');
  const n=ribs?Math.max(192,32*count):192;
  estimate=h=>waveEstimate(h,n,s,v.end_chamfer,ribs);
 }
 if(estimate(body)>250000||estimate(cap)>250000)throw Error(`${v.surface_style} exterior triangle estimate exceeds cap`);
}

export function patternTriangleFields(pattern,auto){
 if(pattern==='rings'||pattern==='spiral')return ['pattern','pattern-size','height','ends',...(!auto?['lid']:[])];
 if(pattern==='ribs')return ['pattern','pattern-size','pattern-depth','diameter','wall'];
 return ['pattern','pattern-size','pattern-depth','diameter','height','wall','ends',...(!auto?['lid']:[])];
}
export function patternTriangleMessage(pattern){
 const label=pattern[0].toUpperCase()+pattern.slice(1);
 return `${label} is too detailed at this size. ${pattern==='diamond'?'Increase diamond size or reduce the container dimensions.':pattern==='ribs'?'Increase spacing or reduce outside diameter.':'Increase spacing or reduce patterned-part height.'}`;
}
