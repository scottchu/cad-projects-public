import {DEFAULTS,geometry,height,sectionSamples} from './math.mjs';

const light=(()=>{const v=[-.6,-.8,1],n=Math.hypot(...v);return v.map(x=>x/n);})();
const $=id=>document.getElementById(id);
const format=n=>Number(n.toFixed(3)).toString();
const minus=n=>n===0?'0.00':`−${Math.abs(n).toFixed(2)}`;
let renderedValues=DEFAULTS,resizeFrame=0;

function validate(){
  const raw={size:$('size').value,depth:$('depth').value},errors={};
  for(const [key,lo,hi] of [['size',4.8,8],['depth',.1,.6]]){
    const value=raw[key],number=Number(value);
    if(typeof value!=='string'||value.trim()===''||!Number.isFinite(number))errors[key]='Enter a number in millimetres.';
    else if(number<lo||number>hi)errors[key]=`Use ${lo.toFixed(key==='size'?1:2)}–${hi.toFixed(key==='size'?1:2)} mm.`;
    const input=$(key),message=$(`${key}-error`);input.setAttribute('aria-invalid',String(Boolean(errors[key])));message.hidden=!errors[key];message.textContent=errors[key]||'';
  }
  $('render').disabled=Boolean(Object.keys(errors).length);
  return Object.keys(errors).length?null:{size:Number(raw.size),depth:Number(raw.depth)};
}

function drawPatch(canvas,kind,values){
  const ctx=canvas.getContext('2d'),{width:w,height:h}=canvas,{arc}=geometry(values),P=values.size,d=values.depth;
  ctx.fillStyle='#e7eaee';ctx.fillRect(0,0,w,h);
  const margin=34,scale=Math.min((w-2*margin)/(4*arc),(h-2*margin)/(4*P));
  const pw=4*arc*scale,ph=4*P*scale,x0=(w-pw)/2,y0=(h-ph)/2;
  const image=ctx.createImageData(Math.ceil(pw),Math.ceil(ph)),delta=1e-4;
  for(let py=0;py<image.height;py++)for(let px=0;px<image.width;px++){
    const u=-2+(px+.5)/scale/arc,v=2-(py+.5)/scale/P;
    const dhdx=(height(kind,u+delta,v,d)-height(kind,u-delta,v,d))/(2*delta*arc);
    const dhdy=(height(kind,u,v+delta,d)-height(kind,u,v-delta,d))/(2*delta*P);
    const nn=Math.hypot(dhdx,dhdy,1),dot=(-dhdx/nn)*light[0]+(-dhdy/nn)*light[1]+light[2]/nn;
    const intensity=.35+.65*Math.max(0,dot),tone=Math.round(48+174*intensity),i=4*(py*image.width+px);
    image.data[i]=tone;image.data[i+1]=tone+2;image.data[i+2]=tone+5;image.data[i+3]=255;
  }
  ctx.putImageData(image,Math.round(x0),Math.round(y0));
  ctx.strokeStyle='#5e6b7a';ctx.lineWidth=1;ctx.strokeRect(Math.round(x0)+.5,Math.round(y0)+.5,image.width-1,image.height-1);
  const bar=5*scale,bx=x0+14,by=y0+ph-18;ctx.strokeStyle='#fff';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(bx,by);ctx.lineTo(bx+bar,by);ctx.stroke();
  ctx.strokeStyle='#1e2834';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(bx,by);ctx.lineTo(bx+bar,by);ctx.stroke();
  ctx.fillStyle='#fff';ctx.strokeStyle='#1e2834';ctx.lineWidth=3;ctx.font='700 13px system-ui';ctx.strokeText('5 mm',bx,by-8);ctx.fillText('5 mm',bx,by-8);
}

function drawSection(canvas,kind,values,magnification){
  const bounds=canvas.getBoundingClientRect(),w=bounds.width,h=bounds.height,dpr=window.devicePixelRatio||1;
  canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr);
  const ctx=canvas.getContext('2d');ctx.setTransform(dpr,0,0,dpr,0,0);
  const {arc}=geometry(values),d=values.depth,g=kind==='current'?.18:.14;
  ctx.clearRect(0,0,w,h);ctx.fillStyle='#f7f8fa';ctx.fillRect(0,0,w,h);
  const left=56,right=14,top=20,bottom=18,datum=top+12,availableWidth=w-left-right;
  const scaleX=Math.min(availableWidth/(2*arc),(h-datum-bottom)/(d*magnification)),scaleY=scaleX*magnification;
  const plotWidth=2*arc*scaleX,x0=left+(availableWidth-plotWidth)/2;
  const toX=u=>x0+(u+1)*arc*scaleX,toY=z=>datum-z*scaleY;
  ctx.strokeStyle='#8a96a4';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(x0,datum+.5);ctx.lineTo(x0+plotWidth,datum+.5);ctx.stroke();
  ctx.fillStyle='#5d6a79';ctx.font='12px system-ui';ctx.fillText('0',12,datum+4);ctx.fillText(`${minus(-d)} mm`,6,toY(-d)+4);
  ctx.fillText(magnification===1?'True proportions':'Depth enlarged ×6',x0,15);
  ctx.strokeStyle='#263847';ctx.lineWidth=2.2;ctx.lineJoin='round';ctx.beginPath();
  sectionSamples(g).forEach((u,i)=>{const x=toX(u),y=toY(height(kind,u,0,d));if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);});ctx.stroke();
  ctx.strokeStyle='#263847';ctx.lineWidth=3;const bar=5*scaleX,by=h-9;ctx.beginPath();ctx.moveTo(x0,by);ctx.lineTo(x0+bar,by);ctx.stroke();
  ctx.fillStyle='#263847';ctx.font='700 12px system-ui';ctx.fillText('5 mm',x0+bar+8,by+4);
}

function renderStudy(values){
  const started=performance.now(),geom=geometry(values);renderedValues={...values};
  for(const kind of ['current','recessed']){
    drawPatch($(`${kind}-patch`),kind,values);drawSection($(`${kind}-true`),kind,values,1);drawSection($(`${kind}-six`),kind,values,6);
    for(const id of [`${kind}-patch`,`${kind}-true`,`${kind}-six`])Object.assign($(id).dataset,{size:String(values.size),depth:String(values.depth),arc:String(geom.arc),count:String(geom.count)});
  }
  $('current-witness').textContent=`Center 0.00 mm · Crossing ${minus(-values.depth)} mm · Pitch ${values.size.toFixed(2)} mm`;
  $('recessed-witness').textContent=`Center ${minus(-values.depth)} mm · Crossing 0.00 mm · Pitch ${values.size.toFixed(2)} mm`;
  const elapsed=performance.now()-started;Object.assign($('study').dataset,{renderedSize:String(values.size),renderedDepth:String(values.depth),drawMs:elapsed.toFixed(2)});
  $('status').dataset.stale='false';$('status').textContent=`Study ready · ${elapsed.toFixed(0)} ms draw`;
}

function redrawSections(){
  for(const kind of ['current','recessed']){
    drawSection($(`${kind}-true`),kind,renderedValues,1);
    drawSection($(`${kind}-six`),kind,renderedValues,6);
  }
}

function edited(){
  const values=validate();$('status').dataset.stale='true';$('status').textContent=values?'Settings changed — render to compare.':'Check the highlighted value.';
}
for(const key of ['size','depth']){
  $(key).addEventListener('input',edited);
  $(`${key}-range`).addEventListener('input',()=>{$(key).value=format(Number($(`${key}-range`).value));edited();});
}
$('controls').addEventListener('submit',event=>{event.preventDefault();const values=validate();if(values){$('size-range').value=String(values.size);$('depth-range').value=String(values.depth);renderStudy(values);}});
$('reset').addEventListener('click',()=>{$('size').value=String(DEFAULTS.size);$('depth').value=String(DEFAULTS.depth);$('size-range').value=String(DEFAULTS.size);$('depth-range').value=String(DEFAULTS.depth);validate();renderStudy(DEFAULTS);});
window.addEventListener('resize',()=>{cancelAnimationFrame(resizeFrame);resizeFrame=requestAnimationFrame(redrawSections);});
validate();renderStudy(DEFAULTS);
