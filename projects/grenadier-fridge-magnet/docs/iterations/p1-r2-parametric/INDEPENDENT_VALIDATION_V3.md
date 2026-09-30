# P2-V3 independent validation — color encoding passes

Owner `/root/parametric_mesh_validation`, 2026-09-06. Read-only export/color validation; source and candidate artifacts untouched. Verified all18 manifest entries before and after checks and independently recomputed fingerprint `1f66199dfbd9b35780aee9cb93af0179277805085e9ac1bc61bbf2c9999b2fc0`.

Flat GLB SHA-256 `bb0b2d54dba75530fbcce067229393cea5534d065251a18a5c6c7c60b8c34e77`; relief `143d67d0365a8b7fd9fc7e2425ee925cf59b24527607b98e8f768880b3966638`.

## Exact allowed delta

Independently decoded each written GLB JSON/BIN chunk. Complete BIN chunks are byte-identical to corresponding connected V2 artifacts. After removing only COLOR_0 primitive bindings, primitive material references and the newly added materials table, complete JSON trees are exactly equal. Thus node transforms, geometry membership, vertex/index buffers, accessors, bufferViews, metadata, mesh names and all remaining attributes are unchanged. Unused historical color buffers remain present but unbound.

V2 geometry evidence therefore carries forward explicitly from fingerprint `2541d21cfbb28d29eede289a3ae978c9d516a91b1e5f07e045f8d6c8286993ce`: connected backing, permitted176-cell addition, no positive-volume collisions, exact accepted face projections and independent XY/Z behavior. No broad geometry rerun was needed.

## Color evidence

Every primitive binds a constant material for its original visible class. Independently calculated piecewise sRGB→linear expected factors and inverse transfer from actual written factors. All RGB factors match a single conversion within1e-15; inverse maximum error across both artifacts is1.1102230246251565e-16. Rounded8-bit inverse values equal every original palette byte. There is no COLOR_0 or baseColorTexture multiplier, so no second conversion or color multiplication occurs. Alpha remains1, alphaMode OPAQUE, single-sided state, metallicFactor1 and roughnessFactor1 preserve the prior absent-material defaults.

| Class | Original sRGB bytes, recovered exactly |
|---|---|
| black | 8,9,11 |
| gray | 155,155,157 |
| white | 255,255,255 |
| deep-blue | 7,95,188 |
| glass-mix | 184,217,236 |

The source-focused command `uv run pytest -q projects/grenadier-fridge-magnet/tests/test_parametric_magnet.py -k color` passed1 test, including0/1 endpoints. Independent written-export command `uv run python /tmp/grenadier-v3-independent.py` passed all assertions. Full independent script and actual output follow.

PASS for export encoding only. Four real material intents and the glass blue+white process placeholder metadata are unchanged. Lighting-dependent front/oblique appearance requires separate critique. Thin connections, STL welding, STEP/BREP, slicing, physical mixing and print performance remain unaccepted. Next: formal review joins this evidence with fresh visual critique for this fingerprint.

## Independent script

```python
import json,struct,copy,hashlib,sys
from pathlib import Path
import numpy as np
P=Path('projects/grenadier-fridge-magnet');sys.path.insert(0,str(P/'src'));from face_vector import PALETTE

def read(path):
 data=path.read_bytes();magic,version,length=struct.unpack_from('<4sII',data);assert magic==b'glTF' and version==2 and length==len(data)
 chunks=[];o=12
 while o<len(data):
  n,t=struct.unpack_from('<II',data,o);chunks.append((t,data[o+8:o+8+n]));o+=8+n
 assert o==len(data) and len(chunks)==2
 return json.loads(chunks[0][1]),chunks[1][1]
result={}
for variant in ('flat','relief'):
 old,oldbin=read(P/'GLB/p1-r2-connected'/f'{variant}.glb');new,newbin=read(P/'GLB/p1-r2-color-corrected'/f'{variant}.glb')
 assert oldbin==newbin
 assert old.keys()|{'materials'}==new.keys()
 colors={};oldnorm=copy.deepcopy(old);newnorm=copy.deepcopy(new)
 for mo,mn in zip(old['meshes'],new['meshes'],strict=True):
  assert mo['name']==mn['name']
  color='black' if mn['name']=='backing-black' else mn['name'].rsplit('-',1)[0]
  source=np.array([int(PALETTE[color][i:i+2],16) for i in (1,3,5)])/255
  for po,pn in zip(mo['primitives'],mn['primitives'],strict=True):
   assert 'COLOR_0' not in pn['attributes'] and pn['attributes']=={k:v for k,v in po['attributes'].items() if k!='COLOR_0'}
   mat=new['materials'][pn['material']];pbr=mat['pbrMetallicRoughness'];f=np.array(pbr['baseColorFactor'])
   expect=np.array([v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in source])
   assert np.max(abs(f[:3]-expect))<1e-15 and f[3]==1
   inverse=np.array([12.92*v if v<=.0031308 else 1.055*v**(1/2.4)-.055 for v in f[:3]])
   assert np.max(abs(inverse-source))<1e-6 and np.array_equal(np.rint(inverse*255),np.rint(source*255))
   assert mat.get('alphaMode','OPAQUE')=='OPAQUE' and not mat.get('doubleSided',False)
   assert 'baseColorTexture' not in pbr and pbr['metallicFactor']==1 and pbr['roughnessFactor']==1
   colors[color]={'source_rgb':np.rint(source*255).astype(int).tolist(),'linear_rgb':f[:3].tolist(),'inverse_max_error':float(np.max(abs(inverse-source))),'alpha':float(f[3])}
 for tree in (oldnorm,newnorm):
  tree.pop('materials',None)
  for mesh in tree['meshes']:
   for prim in mesh['primitives']:
    prim.pop('material',None);prim['attributes'].pop('COLOR_0',None)
 assert oldnorm==newnorm,'JSON changed outside allowed color bindings'
 # Existing export had no explicit material: metallic/roughness/opacity defaults preserved.
 assert not old.get('materials')
 assert len(colors)==5
 result[variant]={'BIN_sha256':hashlib.sha256(newbin).hexdigest(),'BIN_identical':True,'all_noncolor_JSON_identical':True,'palette':colors}
print(json.dumps(result,indent=2));Path('/tmp/grenadier-v3-results.json').write_text(json.dumps(result,indent=2))
```

## Actual output

```json
{
  "flat": {
    "BIN_sha256": "ed28a3e72c312f6a217b022f007d7698d280bfbd8e82e0ac926e7ea0c7699252",
    "BIN_identical": true,
    "all_noncolor_JSON_identical": true,
    "palette": {
      "black": {
        "source_rgb": [
          8,
          9,
          11
        ],
        "linear_rgb": [
          0.0024282158683907,
          0.0027317428519395373,
          0.003346535763899161
        ],
        "inverse_max_error": 6.938893903907228e-18,
        "alpha": 1.0
      },
      "gray": {
        "source_rgb": [
          155,
          155,
          157
        ],
        "linear_rgb": [
          0.3277780980565422,
          0.3277780980565422,
          0.33716361504833037
        ],
        "inverse_max_error": 0.0,
        "alpha": 1.0
      },
      "white": {
        "source_rgb": [
          255,
          255,
          255
        ],
        "linear_rgb": [
          1.0,
          1.0,
          1.0
        ],
        "inverse_max_error": 1.1102230246251565e-16,
        "alpha": 1.0
      },
      "deep-blue": {
        "source_rgb": [
          7,
          95,
          188
        ],
        "linear_rgb": [
          0.0021246888848418626,
          0.11443537382697373,
          0.5028864580325687
        ],
        "inverse_max_error": 0.0,
        "alpha": 1.0
      },
      "glass-mix": {
        "source_rgb": [
          184,
          217,
          236
        ],
        "linear_rgb": [
          0.4793201831008268,
          0.6938717612919899,
          0.83879901174074
        ],
        "inverse_max_error": 0.0,
        "alpha": 1.0
      }
    }
  },
  "relief": {
    "BIN_sha256": "85d7de0a39fa11e4deed012138e3fa86f1a7ca837f6ed3993566bdc15e6a66bd",
    "BIN_identical": true,
    "all_noncolor_JSON_identical": true,
    "palette": {
      "black": {
        "source_rgb": [
          8,
          9,
          11
        ],
        "linear_rgb": [
          0.0024282158683907,
          0.0027317428519395373,
          0.003346535763899161
        ],
        "inverse_max_error": 6.938893903907228e-18,
        "alpha": 1.0
      },
      "gray": {
        "source_rgb": [
          155,
          155,
          157
        ],
        "linear_rgb": [
          0.3277780980565422,
          0.3277780980565422,
          0.33716361504833037
        ],
        "inverse_max_error": 0.0,
        "alpha": 1.0
      },
      "white": {
        "source_rgb": [
          255,
          255,
          255
        ],
        "linear_rgb": [
          1.0,
          1.0,
          1.0
        ],
        "inverse_max_error": 1.1102230246251565e-16,
        "alpha": 1.0
      },
      "deep-blue": {
        "source_rgb": [
          7,
          95,
          188
        ],
        "linear_rgb": [
          0.0021246888848418626,
          0.11443537382697373,
          0.5028864580325687
        ],
        "inverse_max_error": 0.0,
        "alpha": 1.0
      },
      "glass-mix": {
        "source_rgb": [
          184,
          217,
          236
        ],
        "linear_rgb": [
          0.4793201831008268,
          0.6938717612919899,
          0.83879901174074
        ],
        "inverse_max_error": 0.0,
        "alpha": 1.0
      }
    }
  }
}
```
