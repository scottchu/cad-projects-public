const esc=value=>String(value).replace(/[&<>"']/g,char=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[char]));
const targetGroup=(id,content="")=>`<g data-target="${esc(id)}" aria-label="${esc(id)}">${content}</g>`;
const profilePath=(path,scale,x,y,top)=>path.map((point,index)=>`${index?"L":"M"}${x+(top?point.r:-point.r)*scale} ${y+(top?-point.z:point.z)*scale}`).join(" ");

export function renderMainSvg(d){
 const h=290,w=220,x=170,y=52,split=y+h*(d.constraints.splitZ/d.constraints.height),upper=h-(split-y),lower=split-y,offset=d.closure.assembled.phaseMatchesPattern?0:18;
 const targetMarks=Object.keys(d.targets).map((id,index)=>targetGroup(id,`<circle class="target-mark" cx="${18+(index%8)*18}" cy="${390+Math.floor(index/8)*8}" r="2"/>`)).join("");
 const fieldPath=d.surface.field.slice(0,42).map((point,index)=>`${index?"L":"M"}${x+(index/41)*w} ${split+38-point.placed*28}`).join(" ");
 const drains=d.drains.masks.map((hole,index)=>`<circle class="drain" cx="${x+w/2+Math.cos(index*2.4)*Math.min(42,hole.r*10+10)}" cy="${hole.end==="top"?y+12:split-12}" r="${Math.max(2,hole.r*1.5)}"/>`).join("");
 const labels=d.labels.map(label=>`<g class="label" transform="translate(${x+w/2} ${label.target==="upper"?y+upper/2:split+lower/2}) rotate(${label.orientation==="vertical"?-90:0})"><rect x="${-label.size*2.5}" y="${-label.size}" width="${label.size*5}" height="${label.size*1.6}" rx="3"/><text text-anchor="middle" y="${label.size*.18}" style="font-family:${esc(label.font)};font-size:${label.size}px;font-weight:${esc(label.weight)}">${esc(label.text)}</text><title>OpenSCAD font disclosure: ${esc(label.openScadFontFamily)}</title></g>`).join("");
 const attachment=d.attachment.mode==="none"?"":`<g class="attachment ${esc(d.attachment.primitive.kind)}" transform="translate(${x+w+24} ${split+12})"><path d="M0 26 Q18 -12 36 26 V42 H0Z"/><circle cx="18" cy="25" r="7"/><text x="0" y="60">${esc(d.attachment.primitive.kind)}</text></g>`;
 return `<svg class="model-svg" viewBox="0 0 560 470" role="img" aria-label="Dimensionally proportional two-piece container visual. Pixels are fit-to-view, not calibrated.">
 <defs><linearGradient id="core-gradient" x1="0" x2="1"><stop stop-color="#90e0d0"/><stop offset=".5" stop-color="#346a75"/><stop offset="1" stop-color="#b3f0de"/></linearGradient></defs>
 <text class="scale-note" x="18" y="28">dimensionally proportional visual · pixels fit-to-view, not calibrated</text>
 <g data-core-piece="upper-piece"><rect class="core" x="${x}" y="${y+offset}" width="${w}" height="${upper}"/><path class="end" d="${profilePath(d.ends.top.path,3.6,x+w/2,y+offset,true)}"/></g>
 <g data-core-piece="lower-piece"><rect class="core" x="${x}" y="${split}" width="${w}" height="${lower}"/><path class="end" d="${profilePath(d.ends.bottom.path,3.6,x+w/2,split+lower,false)}"/></g>
 <line class="seam" x1="${x}" x2="${x+w}" y1="${split}" y2="${split}"/><text x="${x+5}" y="${split-8}">upper-piece</text><text x="${x+5}" y="${split+18}">lower-piece</text>
 <path class="surface-field" d="${fieldPath}"/><text x="${x}" y="${split+56}">${esc(d.annotations.pattern)}</text>
 <g class="closure"><path d="M${x+18} ${split} C${x+66} ${split-18} ${x+154} ${split+18} ${x+w-18} ${split}"/><text x="${x+32}" y="${split-26}">${esc(d.annotations.closure)}</text></g>
 <g class="drains">${drains}</g>${labels}${attachment}
 <rect class="envelope" x="${x-12}" y="${y-8}" width="${w+24}" height="${h+16}"/><text x="${x}" y="${y+h+30}">base Ø${d.envelopes.baseOD.toFixed(1)} · crest Ø${d.envelopes.crestOD.toFixed(1)} · total Ø${d.envelopes.totalOD.toFixed(1)}</text>
 ${targetMarks}</svg>`;
}

export function renderComparison(d){
 const cards=[...d.ends.comparison.map(end=>({id:end.profile,label:end.profile.replaceAll("_"," ")})),{id:d.surface.pattern,label:d.surface.pattern.replaceAll("_"," ")},{id:d.attachment.mode,label:d.attachment.mode.replaceAll("_"," ")}].filter(card=>card.id!=="none");
 return `<section class="comparison-grid" aria-label="Comparison silhouettes">${cards.map(card=>`<figure data-comparison="${esc(card.id)}"><div class="comparison-shape ${esc(card.id)}"></div><figcaption>${esc(card.label)}</figcaption></figure>`).join("")}</section>`;
}

export function renderDetail(d){
 return `<svg class="detail-svg" viewBox="0 0 560 110" role="img" aria-label="Surface relief and drain detail"><path d="M20 70 H185 V${d.surface.relief.outsetHeight>0?38:92} H300 V70 H540"/><text x="20" y="24">relief inset ${d.surface.relief.insetDepth.toFixed(2)} mm · outset ${d.surface.relief.outsetHeight.toFixed(2)} mm</text><text x="20" y="102">${d.drains.masks.length} visual drain mask openings</text></svg>`;
}
