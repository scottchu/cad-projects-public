export const R=19.5;
export const DEFAULTS=Object.freeze({size:4.8,depth:.45});
export const clamp=(x,lo=0,hi=1)=>Math.max(lo,Math.min(hi,x));
export const wrap=t=>t-Math.floor(t+.5);
export const field=(u,v,g)=>clamp((.5-Math.max(Math.abs(wrap(u+v)),Math.abs(wrap(u-v))))/(.5-g));
export const smoothstep=t=>t*t*(3-2*t);
export const height=(kind,u,v,d)=>kind==='current'?-d+d*field(u,v,.18):-d*smoothstep(field(u,v,.14));
export const geometry=({size,depth})=>{
  const targetArc=size===4.8?3.63:size*(3.63/4.8),count=Math.floor(2*Math.PI*(R-depth)/targetArc+.5);
  return {targetArc,count,arc:2*Math.PI*(R-depth)/count};
};
export function sectionSamples(g){
  const values=Array.from({length:513},(_,i)=>-1+2*i/512),breaks=[];
  for(let n=-1;n<=1;n++)breaks.push(n,n-.5,n+.5,n-g,n+g);
  return [...new Set(values.concat(breaks.filter(x=>x>=-1&&x<=1)).map(x=>x.toFixed(12)))].map(Number).sort((a,b)=>a-b);
}
