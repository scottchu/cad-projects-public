import {patternTriangleMessage,PATTERNS,patternFields,patternRawErrors} from './patterns.mjs';
import {BROWSER_PRESET, snapshot} from './schema.mjs';
import {DRAIN_DEFAULT_COUNT,feasibility,legalCount,whole} from './drain-layout.mjs';
export const DEFAULTS = Object.freeze({diameter:'30',height:'213',wall:'4.5',ends:'3',lid:'84',auto:true,drains:'bottom',pattern:'smooth',output:'assembled'});
// 3.95 may fail the unchanged schema's floating-point residual test. Advertise 4.
export const WALL_MIN = 4;
export function adapt(raw) {
  const errors = {}, n = {};
  for (const [key,lo,hi] of [['diameter',10,69],['height',6,305],['wall',WALL_MIN,35],['ends',2,8],...(!raw.auto ? [['lid',20,250]] : [])]) {
    const value = raw[key];
    if (typeof value !== 'string' || value.trim() === '' || !Number.isFinite(Number(value))) errors[key]='Enter a number in millimetres.';
    else if (Number(value)<lo || Number(value)>hi) errors[key]=key==='wall' && Number(value)<lo ? `This screw lid needs walls of at least ${WALL_MIN} mm.` : `Use a value from ${lo} to ${hi} mm.`;
    n[key]=Number(value);
  }
  const {diameter:D,height:H,wall:W,ends:T}=n;
  const outsideDiameter=D+2*W, outsideHeight=H+2*T;
  const lid=raw.auto ? outsideHeight*(84/219) : n.lid;
  if (!errors.diameter && !errors.wall && (outsideDiameter<20 || outsideDiameter>80)) errors.wall='Choose a wall thickness that keeps the outside diameter between 20 and 80 mm.';
  if (!errors.height && !errors.ends && H<2*T+9) errors.height='Increase the inside height to leave room for the screw lid.';
  if (!errors.height && !errors.ends && (!Number.isFinite(lid) || lid<20 || lid>250 || lid<=T+11 || lid>=H+T-2)) errors[raw.auto?'height':'lid']='The lid needs more room. Increase the inside height or adjust the lid height.';
  if (!['none','top','bottom','both'].includes(raw.drains)) errors.drains='Choose drain holes.';
  if (!PATTERNS.includes(raw.pattern)) errors.pattern='Choose a surface pattern.';
  if (!['assembled','body','cap','print_layout'].includes(raw.output)) errors.output='Choose an export shape.';
  const hasRawCount=Object.hasOwn(raw,'drainCount'),rawCount=raw.drainCount??String(DRAIN_DEFAULT_COUNT),activeDrains=raw.drains!=='none';
  if(activeDrains&&hasRawCount&&!whole(rawCount)) errors.drainCount='Enter a whole number.';
  else if(activeDrains&&hasRawCount&&!legalCount(rawCount)) errors.drainCount='Use a whole number from 1 to 24.';
  const radius=Math.min(9,D/2-2),safeCount=feasibility({count:1,diameter:3,radius,innerRadius:D/2}).max;
  const drainCount=hasRawCount&&legalCount(rawCount)?Number(rawCount):Math.min(DRAIN_DEFAULT_COUNT,safeCount);
  if(!errors.diameter&&!errors.drainCount&&activeDrains){
    const f=feasibility({count:drainCount,diameter:3,radius,innerRadius:D/2});
    if(!f.center||drainCount>=2&&(!f.ring||drainCount>f.max)) {
      const message=`At ${D} mm inside diameter, use at most ${f.max} holes to keep 0.4 mm between openings.`;
      errors.diameter=message;errors.drainCount=message;
    }
  }
  for(const error of patternRawErrors(raw))errors[error.key==='pattern'?'pattern':`pattern-${error.key}`]=error.message;
  if (Object.keys(errors).length) return {errors,summary:{outsideDiameter,outsideHeight,lid}};
  try {
    const values=snapshot({...BROWSER_PRESET,...patternFields(raw),surface_style:raw.pattern,body_bore:D,cap_bore:D+1,device_length:H-5,outer_diameter:outsideDiameter,floor_thickness:T,split_distance_from_top:lid,drain_ring_radius:radius,drain_count:drainCount,drainage_mode:raw.drains,output_mode:raw.output});
    return {errors,values,summary:{outsideDiameter,outsideHeight,lid}};
  } catch(error) {
    if(error.message.includes('wall below')) errors.wall=`${raw.pattern[0].toUpperCase()+raw.pattern.slice(1)} needs wall thickness of at least ${Number((3.95+Number((raw.patterns?.[raw.pattern]??{depth:'.45'}).depth)+(raw.pattern==='diamond'?0:.01)).toFixed(3))} mm. Increase wall thickness or reduce depth.`;
    else if(error.message.includes('triangle estimate')) errors.height=patternTriangleMessage(raw.pattern);
    else errors.wall=error.message==='thread wall constraint failed' ? `This screw lid needs walls of at least ${WALL_MIN} mm.` : 'These dimensions leave too little room for the screw closure. Increase the wall thickness or inside height.';
    return {errors,summary:{outsideDiameter,outsideHeight,lid}};
  }
}
