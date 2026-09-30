"""Independent GLB-buffer versus 3MF-index verification; never repairs geometry."""
from pathlib import Path
import hashlib, json, struct, zipfile, xml.etree.ElementTree as ET
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
P=ROOT/'projects/grenadier-fridge-magnet'; OUT=P/'slicer/p1-r3-validation'; OUT.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected={'flat':('bb0b2d54dba75530fbcce067229393cea5534d065251a18a5c6c7c60b8c34e77','ed08511411e7f0f704002794505bf20ef0b883752667413c595f147675295eaf'),'relief':('143d67d0365a8b7fd9fc7e2425ee925cf59b24527607b98e8f768880b3966638','ebc3caadaff4f41c513a3e4b12e6f328730021358deee32067c55cae5577d774')}
files=[P/'docs/REQUIREMENTS.md',P/'docs/iterations/p1-r2-parametric/DESIGN.md',P/'docs/iterations/p1-r2-parametric/color-corrected-candidate-manifest.json',P/'docs/iterations/p1-r3-slice-probe/input-manifest.json',P/'src/parametric_magnet.py',P/'src/face_vector.py',Path(__file__).resolve()]
for variant in expected: files += [P/f'GLB/p1-r2-color-corrected/{variant}.glb',P/f'slicer/p1-r3/{variant}-diagnostic.3mf']
entries=[{'path':str(f.relative_to(ROOT)),'sha256':sha(f)} for f in sorted(files)]
fingerprint=hashlib.sha256(''.join(e['path']+'\0'+e['sha256']+'\n' for e in entries).encode()).hexdigest()
manifest={'owner':'/root/slice_artifact_validator','task':'P3-V-package','method':'SHA256(sorted path + NUL + SHA256(content) + LF)','fingerprint':fingerprint,'entries':entries,'scope':'GM-R3 diagnostic geometry preservation, four-tool metadata; parent P1-R3 contract frozen by input-manifest; mutable orchestration and receipts excluded'}
(OUT/'package-input-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
parent=json.loads((P/'docs/iterations/p1-r2-parametric/color-corrected-candidate-manifest.json').read_text())
assert all(sha(ROOT/e['path'])==e['sha256'] for e in parent['entries'])
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
results=[]
for variant,(glbhash,mfhash) in expected.items():
 glb=P/f'GLB/p1-r2-color-corrected/{variant}.glb'; mf=P/f'slicer/p1-r3/{variant}-diagnostic.3mf'
 assert sha(glb)==glbhash and sha(mf)==mfhash
 raw=glb.read_bytes(); assert raw[:4]==b'glTF'; off=12; chunks={}
 while off<len(raw):
  length,typ=struct.unpack_from('<II',raw,off); chunks[typ]=raw[off+8:off+8+length];off+=8+length
 j=json.loads(chunks[0x4E4F534A]); buf=chunks[0x004E4942]
 def accessor(i):
  a=j['accessors'][i];v=j['bufferViews'][a['bufferView']]; assert not v.get('byteStride') and not a.get('sparse')
  d={5126:'<f4',5125:'<u4',5123:'<u2'}[a['componentType']];n={'SCALAR':1,'VEC3':3}[a['type']]
  return np.frombuffer(buf,dtype=d,count=a['count']*n,offset=v.get('byteOffset',0)+a.get('byteOffset',0)).reshape(-1,n)
 nodes={n['name']:n for n in j['nodes'] if 'mesh' in n}
 assert all(set(n)<= {'name','mesh'} for n in nodes.values()),'Unexpected source transform'
 with zipfile.ZipFile(mf) as z:
  model=ET.fromstring(z.read('3D/3dmodel.model')); cfg=ET.fromstring(z.read('Metadata/model_settings.config'))
 assert model.attrib['unit']=='millimeter'
 build=model.findall('m:build/m:item',ns);assert len(build)==1
 transform=list(map(float,build[0].attrib['transform'].split()));assert transform==[1,0,0,0,1,0,0,0,1,135,136,0]
 objects={o.attrib['id']:o for o in model.findall('m:resources/m:object',ns)}
 assembly=objects[build[0].attrib['objectid']];components=assembly.findall('m:components/m:component',ns)
 assert len(components)==len(nodes) and all(set(c.attrib)=={'objectid'} for c in components)
 assert len(objects)==len(nodes)+1
 cfgo=cfg.findall('object'); assert len(cfgo)==1 and cfgo[0].attrib['id']==build[0].attrib['objectid']
 metadata={x.attrib['id']:{a.attrib['key']:a.attrib['value'] for a in x.findall('metadata')} for x in cfgo[0].findall('part')}
 parts=[]; bounds=[]
 for c in components:
  oid=c.attrib['objectid'];obj=objects[oid];name=obj.attrib['name'];node=nodes[name]; primitive=j['meshes'][node['mesh']]['primitives'];assert len(primitive)==1 and primitive[0]['mode']==4
  gv=accessor(primitive[0]['attributes']['POSITION']).astype(float);gi=accessor(primitive[0]['indices']).reshape(-1,3)
  mv=np.array([[float(v.attrib[d]) for d in 'xyz'] for v in obj.findall('m:mesh/m:vertices/m:vertex',ns)])
  mi=np.array([[int(v.attrib[d]) for d in ['v1','v2','v3']] for v in obj.findall('m:mesh/m:triangles/m:triangle',ns)])
  assert gv.shape==mv.shape and np.array_equal(gi,mi)
  err=float(np.max(np.abs(gv-mv)));assert err<5e-8
  tool=0 if 'black' in name else 1 if name.startswith('gray') else 3 if name.startswith('deep-blue') else 2
  assert metadata[oid]['name']==name and int(metadata[oid]['extruder'])==tool+1
  # Count indexed edge incidence, independently of any coordinate welding.
  edges=np.sort(np.concatenate([mi[:,[0,1]],mi[:,[1,2]],mi[:,[2,0]]]),axis=1)
  _,counts=np.unique(edges,axis=0,return_counts=True);bad=int(np.count_nonzero(counts!=2));assert bad==0
  bb=np.stack((mv.min(axis=0),mv.max(axis=0)))+np.array([135,136,0]);bounds.append(bb)
  parts.append({'name':name,'vertices':len(mv),'triangles':len(mi),'max_coordinate_serialization_error_mm':err,'exact_indices':True,'indexed_nonmanifold_edges':bad,'tool':tool})
 assert set(metadata)=={c.attrib['objectid'] for c in components}
 bb=np.stack([np.min(np.array(bounds)[:,0],axis=0),np.max(np.array(bounds)[:,1],axis=0)])
 assert bb[0,2]==0 and np.all(bb[0,:2]>=0) and np.all(bb[1,:2]<=270)
 results.append({'variant':variant,'glb_sha256':glbhash,'3mf_sha256':mfhash,'assembled_build_items':1,'whole_translation_mm':[135,136,0],'bounds_mm':bb.tolist(),'dimensions_mm':(bb[1]-bb[0]).tolist(),'parts':parts})
report={'status':'PASS packaging parity only; no print release','fingerprint':fingerprint,'parent_candidate_verified_entries':len(parent['entries']),'variants':results,'limits':['Indexed edge closure does not prove welded-coordinate manifoldness; known point-pinched contacts retained intentionally.','3MF metadata mapping is independently verified; actual tool use awaits successful Gcode.','glass-mix including plate antialias regions maps to T2 white provisionally, so original blue edge color is not preserved or accepted.','No source, mesh, or geometry repaired; no physical acceptance.']}
(OUT/'package-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'fingerprint':fingerprint,'variants':[{'name':r['variant'],'parts':len(r['parts']),'triangles':sum(p['triangles'] for p in r['parts']),'bounds_mm':r['bounds_mm']} for r in results]}))
