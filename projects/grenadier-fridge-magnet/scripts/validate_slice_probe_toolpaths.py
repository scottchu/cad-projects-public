"""Independently read frozen diagnostic Gcode; produce actual extrusion SVG layers/crops."""
from pathlib import Path
import json,hashlib,re,math,collections,zipfile
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parents[1];ROOT=P.parents[1];OUT=P/'slicer/p1-r3-validation';D=P/'slicer/p1-r3-recovery'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected={'flat':'8c25bf304f425ca763839839a030a88856afe7aeea336a925a18b27c7c286259','relief':'dc41c358a0ca015ddc2fae5aa9676e9cdacd13b7dc62a5029aa6db3d20ae54d5'}
files=[Path(__file__).resolve(),OUT/'package-input-manifest.json',D/'input-manifest.json',D/'relief-input-manifest.json']+[D/f'{v}-run1/plate_1.gcode' for v in expected]+[D/'relief-run1/relief-sliced.3mf']+[D/f'{p}.json' for p in ['machine','process','filament-0','filament-1','filament-2','filament-3']]
entries=[{'path':str(f.relative_to(ROOT)),'sha256':sha(f)} for f in sorted(files)]
fp=hashlib.sha256(''.join(e['path']+'\0'+e['sha256']+'\n' for e in entries).encode()).hexdigest()
(OUT/'toolpath-input-manifest.json').write_text(json.dumps({'owner':'/root/slice_artifact_validator','fingerprint':fp,'method':'SHA256(sorted path + NUL + SHA256(content) + LF)','entries':entries},indent=2)+'\n')
colors=['#181818','#808080','#FFFFFF','#1746C5']; summary={}
def region(b):
 u0,v0,u1,v1=b;return (135+(u0-627)*.1,136+(627-v1)*.1,135+(u1-627)*.1,136+(627-v0)*.1)
rois={'whole':(71,83,199,187),'plate':region([326,838,584,949]),'wordmark':region([716,537,902,613])}
for i,(cx,cy,rx,ry) in enumerate([(137,720,60,65),(288,732,59,60),(602,736,60,62),(802,727,65,69)],1):rois[f'lamp-{i}']=region([cx-rx,cy-ry,cx+rx,cy+ry])
for variant,h in expected.items():
 p=D/f'{variant}-run1/plate_1.gcode';assert sha(p)==h
 xyze=[0.,0.,0.,0.];relative=False;erel=True;tool=0;width=.22;feature='';layer_z=0.;layers=[];segs=collections.defaultdict(list);counts=collections.Counter();typecounts=collections.Counter();unknown=collections.Counter();meta=[];allbounds=[math.inf,math.inf,-math.inf,-math.inf];objbounds=[math.inf,math.inf,-math.inf,-math.inf];objectactive=False;arcs=0;end=False;changes=0;temps=[]
 selected=[2.02] if variant=='flat' else [1.62,2.02,2.42]
 for line in p.open():
  line=line.strip()
  if line.startswith(';Z:'):layer_z=round(float(line[3:]),3);layers.append(layer_z)
  elif line.startswith(';WIDTH:'):width=float(line[7:])
  elif line.startswith(';TYPE:'):feature=line[6:]
  elif line.startswith('; printing object '):objectactive=True
  elif line.startswith('; stop printing object '):objectactive=False
  elif line=='; EXECUTABLE_BLOCK_END':end=True
  if line.startswith(';'):
   if any(s in line for s in ['filament used','estimated printing time','total filament','total toolchanges']):meta.append(line)
   continue
  code=line.split(';',1)[0].strip()
  if not code:continue
  op=code.split()[0];args={k:float(v) for k,v in re.findall(r'([XYZEFS])(-?\d*\.?\d+)',code)}
  if re.fullmatch(r'T\d+',op):new=int(op[1:]);changes+=new!=tool;tool=new
  elif op=='G90':relative=False
  elif op=='G91':relative=True
  elif op=='M82':erel=False
  elif op=='M83':erel=True
  elif op=='G92':
   for i,k in enumerate('XYZE'):
    if k in args:xyze[i]=args[k]
  elif op in ['G0','G1','G2','G3']:
   old=xyze[:]
   for i,k in enumerate('XYZ'):
    if k in args:xyze[i]=args[k]+(old[i] if relative else 0)
   de=args.get('E',0) if erel else args.get('E',old[3])-old[3]
   if 'E'in args:xyze[3]=old[3]+de
   if de>0 and math.dist(old[:2],xyze[:2])>1e-7:
    assert tool in range(4)
    if op in ['G2','G3']:arcs+=1
    counts[tool]+=1;typecounts[feature]+=1
    for b in [allbounds]+([objbounds] if objectactive and feature!='Prime tower' else []):b[:]=[min(b[0],old[0],xyze[0]),min(b[1],old[1],xyze[1]),max(b[2],old[0],xyze[0]),max(b[3],old[1],xyze[1])]
    if objectactive and feature not in ['Prime tower','Custom'] and layer_z in selected:segs[layer_z].append((old[0],old[1],xyze[0],xyze[1],tool,width,feature))
  elif op in ['M104','M109','M140','M190']:temps.append(code)
  elif not op.startswith(('G','M','SET_')):unknown[op]+=1
 assert end and arcs==0 and set(counts)==set(range(4)) and layers==sorted(set(layers))
 roidata={};media=[]
 for name,b in rois.items():
  zs=selected if name=='whole' else ([2.02] if variant=='flat' or name=='wordmark' else [2.42]);roidata[name]={}
  for z in zs:
   ss=[s for s in segs[z] if max(s[0],s[2])>=b[0] and min(s[0],s[2])<=b[2] and max(s[1],s[3])>=b[1] and min(s[1],s[3])<=b[3]]
   roidata[name][str(z)]={'segments':len(ss),'tool_segment_counts':dict(collections.Counter(s[4] for s in ss)),'width_mm_min_max':[min(s[5] for s in ss),max(s[5] for s in ss)] if ss else None,'source_bounds_mm':b}
   # Gcode +Y is up; invert once in SVG to match accepted source artwork.
   bw=b[2]-b[0];bh=b[3]-b[1];svg=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{b[0]} {-b[3]} {bw} {bh}" width="{max(600,int(bw*8))}"><title>{variant} {name}: actual extrusion paths at Z={z} mm; provisional glass white</title>',f'<rect x="{b[0]}" y="{-b[3]}" width="{bw}" height="{bh}" fill="#ccd5de"/>','<g fill="none" stroke-linecap="round" stroke-linejoin="round">']
   im=Image.new('RGB',(max(1,round(bw*12)),max(1,round(bh*12))),'#ccd5de');draw=ImageDraw.Draw(im)
   for x,y,xx,yy,t,w,f in ss:
    svg.append(f'<path d="M{x:.4f},{-y:.4f}L{xx:.4f},{-yy:.4f}" stroke="{colors[t]}" stroke-width="{w:.6f}"/>')
    draw.line(((x-b[0])*12,(b[3]-y)*12,(xx-b[0])*12,(b[3]-yy)*12),fill=colors[t],width=max(1,round(w*12)))
   svg.append('</g></svg>');stem=f'{variant}-{name}-z{z:.2f}';(OUT/f'{stem}.svg').write_text('\n'.join(svg));im.save(OUT/f'{stem}.png');media.append(stem+'.svg')
 summary[variant]={'gcode_sha256':h,'complete_executable_block':end,'layers':layers,'actual_extrusion_tool_segment_counts':dict(counts),'actual_tool_changes':changes,'extrusion_features':dict(typecounts),'all_extrusion_centerline_bounds_mm':allbounds,'object_extrusion_centerline_bounds_mm':objbounds,'arc_extrusions':arcs,'metadata':meta,'macros_not_resolved':dict(unknown),'rois':roidata,'media':media,'temperatures':sorted(set(temps))}
with zipfile.ZipFile(D/'relief-run1/relief-sliced.3mf') as z:
 assert hashlib.sha256(z.read('Metadata/plate_1.gcode')).hexdigest()==expected['relief']
 summary['relief']['archive_gcode_exact_match']=True;summary['relief']['native_thumbnails']=[n for n in z.namelist() if n.endswith(('.png','.jpg'))]
summary['fingerprint']=fp;summary['limits']=['Selected-layer paths are direct Gcode extrusion strokes, not a simulated final appearance or measured bead size.','PNG inspection copies use rounded display pixels; SVG retains actual declared width.','Native firmware macros not simulated. No printer or physical validation.']
(OUT/'toolpath-validation.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({'fingerprint':fp,'variants':{v:{k:summary[v][k] for k in ['complete_executable_block','actual_tool_changes','object_extrusion_centerline_bounds_mm','rois']} for v in expected}}))
