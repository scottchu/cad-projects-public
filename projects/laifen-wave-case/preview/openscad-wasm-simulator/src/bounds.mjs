import {BROWSER_PRESET,snapshot} from './schema.mjs';
import {DRAIN_DEFAULT_COUNT,feasibility,legalCount,whole} from './drain-layout.mjs';

const k=84/219, tick=.1;
const STATIC=Object.freeze({diameter:[10,69],height:[6,305],wall:[4,35],ends:[2,8],lid:[20,250]});
const PURPOSE=Object.freeze({diameter:'lid is 1 mm wider',height:'space inside with the lid closed',wall:'body sides; lid sides are 0.5 mm thinner',ends:'top and bottom end thickness',lid:'lid height at the seam'});
export const DIMENSIONS=Object.freeze(['diameter','height','wall','ends','lid']);

const decimal=value=>typeof value==='string'&&value.trim()!==''&&/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$/.test(value.trim())&&Number.isFinite(Number(value));
const issue=(id,type,message,fields)=>Object.freeze({id,type,message,fields:Object.freeze(fields)});
const up=value=>Math.ceil((value-1e-9)/tick)*tick;
const down=value=>Math.floor((value+1e-9)/tick)*tick;
const clean=value=>Number(value.toFixed(1));

function directIssue(raw,key) {
  if(!decimal(raw[key])) return issue(`${key}-number`,'direct','Enter a number in millimetres.',[key]);
  const value=Number(raw[key]),[lo,hi]=STATIC[key];
  if(value<lo||value>hi) return issue(`${key}-bounds`,'direct',key==='wall'&&value<lo?'This screw lid needs walls of at least 4 mm.':`Use a value from ${lo} to ${hi} mm.`,[key]);
  return null;
}

function dimensionResult(raw) {
  const active=['diameter','height','wall','ends',...(!raw.auto?['lid']:[])];
  const issues=active.map(key=>directIssue(raw,key)).filter(Boolean);
  const blocked=new Set(issues.flatMap(item=>item.fields));
  const n=Object.fromEntries(DIMENSIONS.map(key=>[key,decimal(raw[key])?Number(raw[key]):NaN]));
  const {diameter:D,height:H,wall:W,ends:T}=n;
  const lid=raw.auto?k*(H+2*T):n.lid;
  if(!blocked.has('diameter')&&!blocked.has('wall')) {
    if(D+2*W<20) issues.push(issue('outside-diameter-min','coupled','Inside diameter and wall thickness must make an outside diameter of at least 20 mm.',['diameter','wall']));
    else if(D+2*W>80) issues.push(issue('outside-diameter-max','coupled','Inside diameter and wall thickness must keep the outside diameter at or below 80 mm.',['diameter','wall']));
  }
  if(!blocked.has('height')&&!blocked.has('ends')) {
    if(H<2*T+9) issues.push(issue('closure-height','coupled','Inside height must be at least twice the end thickness plus 9 mm.',['height','ends']));
    if(raw.auto) {
      if(lid<20||lid>250) issues.push(issue('auto-lid-range','coupled','Auto lid height must be from 20 to 250 mm.',['height','ends']));
      else if(lid<=T+11) issues.push(issue('auto-lid-lower','coupled','Auto lid height must be more than end thickness plus 11 mm.',['height','ends']));
      else if(lid>=H+T-2) issues.push(issue('auto-lid-upper','coupled','Auto lid height must be less than inside height plus end thickness minus 2 mm.',['height','ends']));
    } else if(!blocked.has('lid')) {
      if(lid<=T+11) issues.push(issue('manual-lid-lower','coupled','Lid height must be more than end thickness plus 11 mm.',['height','ends','lid']));
      else if(lid>=H+T-2) issues.push(issue('manual-lid-upper','coupled','Lid height must be less than inside height plus end thickness minus 2 mm.',['height','ends','lid']));
    }
  }
  return {issues,n,summary:{outsideDiameter:D+2*W,outsideHeight:H+2*T,lid}};
}

const feasible=(raw,key,value)=>dimensionResult({...raw,[key]:String(value)}).issues.length===0;
function interval(raw,key,drainCount=null) {
  if(key==='lid'&&raw.auto) {const value=dimensionResult(raw).summary.lid;return {min:value,max:value,step:tick,disabled:true};}
  const [lo,hi]=STATIC[key];let min=null,max=null;
  for(let value=up(lo);value<=down(hi)+1e-8;value=clean(value+tick)) {
    const diameter=key==='diameter'?value:Number(raw.diameter),radius=Math.min(9,diameter/2-2);
    const countFits=drainCount===null||feasibility({count:drainCount,diameter:3,radius,innerRadius:diameter/2}).max>=drainCount;
    if(feasible(raw,key,value)&&countFits) {if(min===null)min=value;max=value;}
  }
  return min===null?{min:null,max:null,step:tick,disabled:true}:{min,max,step:tick,disabled:false};
}
function sourceCount(raw) {return legalCount(raw.drainCount??String(DRAIN_DEFAULT_COUNT))?Number(raw.drainCount??DRAIN_DEFAULT_COUNT):DRAIN_DEFAULT_COUNT;}
function generationValues(raw,n,summary) {
  return snapshot({...BROWSER_PRESET,body_bore:n.diameter,cap_bore:n.diameter+1,device_length:n.height-5,outer_diameter:summary.outsideDiameter,floor_thickness:n.ends,split_distance_from_top:summary.lid,drain_ring_radius:Math.min(9,n.diameter/2-2),drainage_mode:raw.drains,drain_count:sourceCount(raw),output_mode:raw.output});
}
export function dimensionSnapshot(raw) {return Object.freeze({diameter:raw.diameter,height:raw.height,wall:raw.wall,ends:raw.ends,lid:raw.lid,auto:Boolean(raw.auto)});}

/** The single pure owner of draft validity and every UI projection derived from it. */
export function deriveDraftState(raw,lastValidDimensions) {
  const current=dimensionResult(raw);
  if(!current.issues.length)try{generationValues({...raw,drains:'bottom',drainCount:'1',output:'assembled'},current.n,current.summary);}catch{current.issues.push(issue('snapshot-constraint','coupled','These dimensions leave too little room for the screw closure.',['diameter','height','wall','ends',...(!raw.auto?['lid']:[])]));}
  const dimensionsValid=current.issues.length===0;
  const last=dimensionsValid?dimensionSnapshot(raw):dimensionSnapshot(lastValidDimensions);
  if(dimensionResult(last).issues.length) throw new TypeError('lastValidDimensions must be one complete valid dimension snapshot');
  const activeDrains=raw.drains!=='none',rawDrainCount=raw.drainCount??String(DRAIN_DEFAULT_COUNT);
  const countNumber=legalCount(rawDrainCount)?Number(rawDrainCount):null;
  const source=dimensionsValid?dimensionSnapshot(raw):last,sourceName=dimensionsValid?'current':'last-valid',sliders={};
  const drainGeometry=Number.isFinite(current.n.diameter)?feasibility({count:countNumber??1,diameter:3,radius:Math.min(9,current.n.diameter/2-2),innerRadius:current.n.diameter/2}):null;
  const countMax=drainGeometry?.max??null;
  for(const key of DIMENSIONS) {
    const bounds=interval(source,key,key==='diameter'&&dimensionsValid&&activeDrains?countNumber:null),auto=key==='lid'&&source.auto;
    let rule;
    if(!dimensionsValid) rule=auto?`Last valid Auto lid height: ${clean(bounds.min)} mm · correct the highlighted dimensions to use sliders`:bounds.min===null?'Last valid range has no 0.1 mm setting · correct the highlighted dimensions to use sliders':`Last valid range: ${bounds.min}–${bounds.max} mm · correct the highlighted dimensions to use sliders · ${PURPOSE[key]}`;
    else rule=auto?`Auto lid height: ${clean(bounds.min)} mm · turn off Auto to adjust`:bounds.min===null?`No allowed 0.1 mm value with the current dimensions · ${PURPOSE[key]}`:`Allowed now: ${bounds.min}–${bounds.max} mm · ${PURPOSE[key]}`;
    sliders[key]=Object.freeze({...bounds,disabled:!dimensionsValid||bounds.disabled,source:sourceName,rule});
  }
  const issues=[...current.issues];
  if(!['none','top','bottom','both'].includes(raw.drains)) issues.push(issue('drains-choice','direct','Choose drain holes.',['drains']));
  if(activeDrains) {
    if(!whole(rawDrainCount)) issues.push(issue('drain-count-whole','direct','Enter a whole number.',['drainCount']));
    else if(!legalCount(rawDrainCount)) issues.push(issue('drain-count-range','direct','Use a whole number from 1 to 24.',['drainCount']));
    else if(drainGeometry&&(!drainGeometry.center||countNumber>=2&&(!drainGeometry.ring||countNumber>drainGeometry.max))) issues.push(issue('drain-count-spacing','coupled',`At ${current.n.diameter} mm inside diameter, use at most ${countMax} holes to keep 0.4 mm between openings.`,['diameter','drainCount']));
  }
  if(!['assembled','body','cap','print_layout'].includes(raw.output)) issues.push(issue('output-choice','direct','Choose an export shape.',['output']));
  const values=issues.length?null:generationValues(raw,current.n,current.summary);
  const fieldErrors={};for(const item of issues)if(item.type==='direct'&&!fieldErrors[item.fields[0]])fieldErrors[item.fields[0]]=item.message;
  const formError=issues.filter(item=>item.type==='coupled').map(item=>item.message).join(' ');
  const summary=Object.freeze(Object.fromEntries(Object.entries(current.summary).map(([key,value])=>[key,Number.isFinite(value)?value:null])));
  const countInvalid=activeDrains&&!legalCount(rawDrainCount);
  const countDisabled=!activeDrains||!dimensionsValid||countMax===null||countInvalid;
  const countRule=!activeDrains?'Drain holes are off; this value is remembered.':countInvalid?'Correct the hole count to use its slider.':countDisabled?'Correct the inside diameter to set hole count.':countNumber>countMax?`Draft ${countNumber} is too high; choose 1–${countMax} holes at ${current.n.diameter} mm inside diameter.`:`Allowed now: 1–${countMax} holes at ${current.n.diameter} mm inside diameter`;
  return Object.freeze({issues:Object.freeze(issues),fieldErrors:Object.freeze(fieldErrors),formError,sliders:Object.freeze(sliders),summary,generationValues:values,canGenerate:Boolean(values)&&issues.length===0,nextLastValidDimensions:dimensionsValid?dimensionSnapshot(raw):last,drainCount:Object.freeze({active:activeDrains,min:1,max:countMax,step:1,disabled:countDisabled,rule:countRule})});
}
