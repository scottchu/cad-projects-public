"""Diagnostic only: preserve indexed GLB meshes in a multipart Orca 3MF."""
from pathlib import Path
import json, hashlib, zipfile, io
import trimesh
from xml.sax.saxutils import escape
ROOT=Path(__file__).resolve().parents[3]; P=ROOT/'projects/grenadier-fridge-magnet'; D=P/'slicer/p1-r3'; I=P/'docs/iterations/p1-r3-slice-probe'
PROFILES=Path('/Applications/Snapmaker Orca.app/Contents/Resources/profiles/Snapmaker')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
parent=json.loads((P/'docs/iterations/p1-r2-parametric/color-corrected-candidate-manifest.json').read_text())
assert all(sha(ROOT/e['path'])==e['sha256'] for e in parent['entries'])
files={}; chain=[]
for p in PROFILES.rglob('*.json'):
 try:j=json.loads(p.read_text());files[j.get('name',p.stem)]=p
 except:pass
def resolve(name):
 p=files[name];j=json.loads(p.read_text());chain.append(p);out=resolve(j['inherits']) if j.get('inherits') else {};out.update(j);out.pop('inherits',None);return out
machine=resolve('Snapmaker U1 (0.2 nozzle)'); process=resolve('0.08 High Quality @Snapmaker U1 (0.2 nozzle)');fil=resolve('Generic PLA @U1 0.2 nozzle')
process['curr_bed_type']='Textured PEI Plate'
# Diagnostic explicit physical prime tool avoids known 2.3.5 zero sentinel crash.
process['wipe_tower_filament']='1'
process['filament_colour']=['#181818','#808080','#FFFFFF','#1746C5']
for name,j in [('machine',machine),('process',process)]: (D/(name+'.json')).write_text(json.dumps(j,indent=2)+'\n')
for n,color in enumerate(process['filament_colour']):
 j=dict(fil);j['filament_colour']=[color];assert j.get('filament_diameter') and j.get('filament_is_support') is not None
 (D/f'filament-{n}.json').write_text(json.dumps(j,indent=2)+'\n')
inputs=[ROOT/e['path'] for e in parent['entries']]+[I/'BRIEF.md',P/'docs/REQUIREMENTS.md',Path(__file__).resolve(),*set(chain)]
entries=[{'path':str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p),'sha256':sha(p)} for p in sorted(set(inputs))]
fingerprint=hashlib.sha256(''.join(e['path']+'\0'+e['sha256']+'\n' for e in entries).encode()).hexdigest()
(I/'input-manifest.json').write_text(json.dumps({'fingerprint':fingerprint,'method':'SHA256(sorted path + NUL + SHA256(content) + LF)','parent':parent['fingerprint'],'entries':entries},indent=2)+'\n')
records=[]
for variant in ['flat','relief']:
 scene=trimesh.load(P/f'GLB/p1-r2-color-corrected/{variant}.glb',process=False)
 resources=[];components=[];parts=[];meta=[]
 for idx,node in enumerate(sorted(scene.graph.nodes_geometry),1):
  tf,g=scene.graph[node];m=scene.geometry[g].copy();m.apply_transform(tf)
  tool=1 if ('black' in node) else 2 if node.startswith('gray') else 4 if node.startswith('deep-blue') else 3
  verts=''.join(f'<vertex x="{x:.9g}" y="{y:.9g}" z="{z:.9g}"/>' for x,y,z in m.vertices)
  tris=''.join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a,b,c in m.faces)
  resources.append(f'<object id="{idx}" type="model" name="{escape(node)}"><mesh><vertices>{verts}</vertices><triangles>{tris}</triangles></mesh></object>')
  components.append(f'<component objectid="{idx}"/>')
  parts.append(f'<part id="{idx}" subtype="normal_part"><metadata key="name" value="{escape(node)}"/><metadata key="extruder" value="{tool}"/></part>')
  meta.append({'name':node,'object_id':idx,'tool':tool-1,'vertices':len(m.vertices),'triangles':len(m.faces),'bounds':m.bounds.tolist()})
 rootid=len(meta)+1
 resources.append(f'<object id="{rootid}" type="model" name="DIAGNOSTIC-{variant}"><components>{"".join(components)}</components></object>')
 model=f'<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"><metadata name="BambuStudio:3mfVersion">1</metadata><resources>{"".join(resources)}</resources><build><item objectid="{rootid}" transform="1 0 0 0 1 0 0 0 1 135 136 0"/></build></model>'
 config=f'<?xml version="1.0" encoding="UTF-8"?><config><object id="{rootid}"><metadata key="name" value="DIAGNOSTIC-{variant}"/><metadata key="extruder" value="1"/>{"".join(parts)}</object></config>'
 out=D/f'{variant}-diagnostic.3mf'
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
  z.writestr('3D/3dmodel.model',model);z.writestr('Metadata/model_settings.config',config)
  z.writestr('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
  z.writestr('_rels/.rels','<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
 records.append({'variant':variant,'input':str(out),'sha256':sha(out),'parts':meta,'whole_translation':[135,136,0]})
(D/'packaging.json').write_text(json.dumps({'status':'DIAGNOSTIC NON-PRINT-RELEASE','records':records},indent=2)+'\n')
print(json.dumps({'fingerprint':fingerprint,'packaged':[(r['variant'],len(r['parts'])) for r in records]}))
