export const DRAIN_LIGAMENT=.4;
export const DRAIN_DEFAULT_COUNT=7;

export const whole=value=>typeof value==='string'&&/^\d+$/.test(value.trim());
export const legalCount=value=>whole(value)&&Number(value)>=1&&Number(value)<=24;
export function centers(count,radius){return count===1?[[0,0]]:[[0,0],...Array.from({length:count-1},(_,i)=>{const a=2*Math.PI*i/(count-1);return [radius*Math.cos(a),radius*Math.sin(a)];})];}
export function feasibility({count,diameter,radius,innerRadius,ligament=DRAIN_LIGAMENT}){
  const center=innerRadius-diameter/2>=ligament;
  const ring=innerRadius-(radius+diameter/2)>=ligament&&radius-diameter>=ligament;
  const max=center&&ring?Math.min(24,1+Math.floor(Math.PI/Math.asin((diameter+ligament)/(2*radius)))):1;
  return Object.freeze({center,ring,max});
}
