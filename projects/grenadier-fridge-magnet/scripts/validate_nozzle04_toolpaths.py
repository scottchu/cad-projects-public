"""Independently read frozen diagnostic Gcode; produce actual extrusion SVG layers/crops."""
from pathlib import Path
import json,hashlib,re,math,collections,zipfile,sys
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parents[1];ROOT=P.parents[1];OUT=P/'slicer/p1-r4-validation';D=P/'slicer/p1-r4';OUT.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert len(sys.argv)==3, 'Pass frozen flat and relief Gcode SHA256 as two arguments'
expected=dict(zip(['flat','relief'],sys.argv[1:]))
BASE=P/'slicer/p1-r3-validation'
for name in ['package-input-manifest.json','toolpath-input-manifest.json','review-media-manifest.json']:
 manifest=json.loads((BASE/name).read_text())
 assert all(sha(ROOT/e['path'])==e['sha256'] for e in manifest['entries']),f'P3 baseline drift: {name}'
files=[Path(__file__).resolve(),BASE/'package-input-manifest.json',BASE/'toolpath-validation.json',BASE/'toolpath-input-manifest.json',BASE/'review-media-manifest.json',P/'docs/iterations/p1-r4-nozzle04/BRIEF.md']+list(D.glob('*manifest.json'))+[D/f'{v}-run1/plate_1.gcode' for v in expected]+list(D.glob('*-run1/*sliced.3mf'))+[D/f'{p}.json' for p in ['machine','process','filament-0','filament-1','filament-2','filament-3']]
files=sorted(set(files))
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
 xyze=[0.,0.,0.,0.];relative=False;erel=True;tool=0;width=.42;feature='';layer_z=0.;layers=[];segs=collections.defaultdict(list);counts=collections.Counter();typecounts=collections.Counter();unknown=collections.Counter();meta=[];allbounds=[math.inf,math.inf,-math.inf,-math.inf];objbounds=[math.inf,math.inf,-math.inf,-math.inf];objectactive=False;arcs=0;end=False;changes=0;temps=[]
 observed_z=[round(float(m.group(1)),3) for m in re.finditer(r'^;Z:([0-9.]+)$',p.read_text(),re.M)]
 assert observed_z
 offset=round(max(observed_z)-(2.0 if variant=='flat' else 2.4),3)
 selected=[round(2.0+offset,3)] if variant=='flat' else [round(x+offset,3) for x in [1.6,2.0,2.4]]
 assert all(z in observed_z for z in selected), 'Process requires explicit surface-layer selection'
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
  zs=selected if name=='whole' else ([selected[0]] if variant=='flat' else [selected[1]] if name=='wordmark' else [selected[2]]);roidata[name]={}
  for z in zs:
   ss=[s for s in segs[z] if max(s[0],s[2])>=b[0] and min(s[0],s[2])<=b[2] and max(s[1],s[3])>=b[1] and min(s[1],s[3])<=b[3]]
   roidata[name][str(z)]={'segments':len(ss),'tool_segment_counts':dict(collections.Counter(s[4] for s in ss)),'width_mm_min_max':[min(s[5] for s in ss),max(s[5] for s in ss)] if ss else None,'source_bounds_mm':b}
   # Gcode +Y is up; invert once in SVG to match accepted source artwork.
   bw=b[2]-b[0];bh=b[3]-b[1];svg=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{b[0]} {-b[3]} {bw} {bh}" width="{max(600,int(bw*8))}"><title>{variant} {name}: actual extrusion paths at Z={z} mm; provisional glass white</title>',f'<rect x="{b[0]}" y="{-b[3]}" width="{bw}" height="{bh}" fill="#ccd5de"/>','<g fill="none" stroke-linecap="round" stroke-linejoin="round">']
   im=Image.new('RGB',(max(1,round(bw*48)),max(1,round(bh*48))),'#ccd5de');draw=ImageDraw.Draw(im)
   for x,y,xx,yy,t,w,f in ss:
    svg.append(f'<path d="M{x:.4f},{-y:.4f}L{xx:.4f},{-yy:.4f}" stroke="{colors[t]}" stroke-width="{w:.6f}"/>')
    draw.line(((x-b[0])*48,(b[3]-y)*48,(xx-b[0])*48,(b[3]-yy)*48),fill=colors[t],width=max(1,round(w*48)))
   svg.append('</g></svg>');stem=f'{variant}-{name}-z{z:.2f}';(OUT/f'{stem}.svg').write_text('\n'.join(svg));im.resize((max(1,round(bw*12)),max(1,round(bh*12))),Image.Resampling.LANCZOS).save(OUT/f'{stem}.png');media.append(stem+'.svg')
 summary[variant]={'gcode_sha256':h,'complete_executable_block':end,'layers':layers,'actual_extrusion_tool_segment_counts':dict(counts),'actual_tool_changes':changes,'extrusion_features':dict(typecounts),'all_extrusion_centerline_bounds_mm':allbounds,'object_extrusion_centerline_bounds_mm':objbounds,'arc_extrusions':arcs,'metadata':meta,'macros_not_resolved':dict(unknown),'rois':roidata,'media':media,'temperatures':sorted(set(temps))}
for variant in expected:
 archive=D/f'{variant}-run1/{variant}-sliced.3mf'
 if archive.exists():
  with zipfile.ZipFile(archive) as z:
   assert hashlib.sha256(z.read('Metadata/plate_1.gcode')).hexdigest()==expected[variant]
   summary[variant]['archive_gcode_exact_match']=True;summary[variant]['native_thumbnails']=[n for n in z.namelist() if n.endswith(('.png','.jpg'))]
configs={k:json.loads((D/f'{k}.json').read_text()) for k in ['machine','process']}
assert configs['machine']['nozzle_diameter']==['0.4']*4
summary['process_settings']={k:configs['process'].get(k) for k in ['name','layer_height','initial_layer_print_height','line_width','outer_wall_line_width','inner_wall_line_width','wall_generator']}
summary['nozzle_diameter']=configs['machine']['nozzle_diameter']
summary['p3_baseline']={v:{k:json.loads((BASE/'toolpath-validation.json').read_text())[v][k] for k in ['layers','metadata','actual_tool_changes','object_extrusion_centerline_bounds_mm']} for v in expected}
media_entries=[{'path':str(f.relative_to(ROOT)),'sha256':sha(f),'bytes':f.stat().st_size} for f in sorted([*OUT.glob('*.svg'),*OUT.glob('*.png')])]
media_fp=hashlib.sha256(''.join(e['path']+'\0'+e['sha256']+'\n' for e in media_entries).encode()).hexdigest()
(OUT/'review-media-manifest.json').write_text(json.dumps({'fingerprint':media_fp,'method':'SHA256(sorted path + NUL + SHA256(content) + LF)','input_fingerprint':fp,'entries':media_entries},indent=2)+'\n')
summary['media_fingerprint']=media_fp
summary['fingerprint']=fp;summary['limits']=['Selected-layer paths are direct Gcode extrusion strokes, not a simulated final appearance or measured bead size.','PNG inspection copies supersample at48px/mm then downsample to12px/mm; SVG retains actual declared width.','Native firmware macros not simulated. No printer or physical validation.']
(OUT/'toolpath-validation.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({'fingerprint':fp,'variants':{v:{k:summary[v][k] for k in ['complete_executable_block','actual_tool_changes','object_extrusion_centerline_bounds_mm','rois']} for v in expected}}))
