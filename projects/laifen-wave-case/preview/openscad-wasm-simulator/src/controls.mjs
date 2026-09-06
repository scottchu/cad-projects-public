/** Range rendering never changes exact state. Pattern events use feasible grids. */
export function steppedValue(values,current,key){
 if(!values?.length)return null;
 if(key==='Home')return values[0];if(key==='End')return values.at(-1);
 if(key==='ArrowRight'||key==='ArrowUp')return values.find(v=>v>current+1e-10)??values.at(-1);
 if(key==='ArrowLeft'||key==='ArrowDown')return [...values].reverse().find(v=>v<current-1e-10)??values[0];
 return values.reduce((best,v)=>Math.abs(v-current)<=Math.abs(best-current)+1e-10?v:best,values[0]);
}
export function bindRange({input,range,onChange,onFocus,getSlider}) {
 const commit=value=>{if(onChange(String(value))!==false)input.value=String(value);};
 range.addEventListener('input',()=>{
  if(getSlider){const slider=getSlider();if(slider.disabled)return;const value=steppedValue(slider.values,Number(range.value));if(value!==null)commit(value);}
  else commit(range.value);
 });
 range.addEventListener('keydown',event=>{
  if(!getSlider||!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','Home','End'].includes(event.key))return;
  event.preventDefault();const slider=getSlider();if(slider.disabled)return;
  const value=steppedValue(slider.values,Number(input.value),event.key);if(value!==null)commit(value);
 });
 if(onFocus)range.addEventListener('focus',onFocus);
}
