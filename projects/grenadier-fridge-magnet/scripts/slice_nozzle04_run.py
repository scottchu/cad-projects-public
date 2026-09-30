"""Native 0.4mm diagnostic slice, frozen inputs and isolated outputs only."""
from pathlib import Path
import hashlib,json,subprocess,time,sys,plistlib
ROOT=Path(__file__).resolve().parents[3];P=ROOT/'projects/grenadier-fridge-magnet';D=P/'slicer/p1-r4';I=P/'docs/iterations/p1-r4-nozzle04';OLD=P/'slicer/p1-r3';PROFILES=Path('/Applications/Snapmaker Orca.app/Contents/Resources/profiles/Snapmaker');binary=Path('/Applications/Snapmaker Orca.app/Contents/MacOS/Snapmaker_Orca')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
mode=sys.argv[1]
if mode=='prepare':
 parent=json.loads((P/'docs/iterations/p1-r2-parametric/color-corrected-candidate-manifest.json').read_text());assert all(sha(ROOT/e['path'])==e['sha256'] for e in parent['entries'])
 assert sha(OLD/'flat-diagnostic.3mf')=='ed08511411e7f0f704002794505bf20ef0b883752667413c595f147675295eaf'
 assert sha(OLD/'relief-diagnostic.3mf')=='ebc3caadaff4f41c513a3e4b12e6f328730021358deee32067c55cae5577d774'
 files={};chain=set()
 for p in PROFILES.rglob('*.json'):
  j=json.loads(p.read_text());files[j.get('name',p.stem)]=p
 def resolve(name):
  p=files[name];chain.add(p);j=json.loads(p.read_text());d=resolve(j['inherits']) if j.get('inherits') else {};d.update(j);d.pop('inherits',None);return d
 m=resolve('Snapmaker U1 (0.4 nozzle)');p=resolve('0.08 High Quality @Snapmaker U1 (0.4 nozzle)');f=resolve('Generic PLA');assert m['nozzle_diameter']==['0.4']*4 and p['layer_height']=='0.08'
 m['printer_settings_id']=m['name'];p['print_settings_id']=p['name'];p['curr_bed_type']='Textured PEI Plate';p.pop('wipe_tower_filament',None);m['wipe_tower_filament']='1'
 for n,j in [('machine',m),('process',p)]: (D/f'{n}.json').write_text(json.dumps(j,indent=2)+'\n')
 for n,c in enumerate(['#181818','#808080','#FFFFFF','#1746C5']):
  j=dict(f);j['filament_colour']=[c];assert j.get('filament_diameter') and j.get('filament_is_support') is not None;(D/f'filament-{n}.json').write_text(json.dumps(j,indent=2)+'\n')
 paths=set([ROOT/e['path'] for e in parent['entries']]+[I/'BRIEF.md',P/'docs/REQUIREMENTS.md',Path(__file__).resolve(),binary,OLD/'flat-diagnostic.3mf',OLD/'relief-diagnostic.3mf',*chain,*D.glob('*.json')])
 entries=[{'path':str(q.relative_to(ROOT)) if q.is_relative_to(ROOT) else str(q),'sha256':sha(q)} for q in sorted(paths)];entries.sort(key=lambda e:e['path']);fp=hashlib.sha256(''.join(e['path']+'\0'+e['sha256']+'\n' for e in entries).encode()).hexdigest()
 (D/'input-manifest.json').write_text(json.dumps({'fingerprint':fp,'parent':parent['fingerprint'],'method':'SHA256(sorted path + NUL + SHA256(content) + LF)','entries':entries},indent=2)+'\n');print(fp);sys.exit()
manifest=json.loads((D/'input-manifest.json').read_text());assert all(sha(ROOT/e['path'])==e['sha256'] for e in manifest['entries']);assert mode in ['flat','relief'];out=D/f'{mode}-run1';out.mkdir(exist_ok=False);(out/'datadir').mkdir()
cmd=[str(binary),'--debug','3','--datadir',str(out/'datadir'),'--load-settings',';'.join(str(D/f'{n}.json') for n in ['machine','process']),'--load-filaments',';'.join(str(D/f'filament-{n}.json') for n in range(4)),'--arrange','0','--orient','0','--slice','0','--export-3mf',f'{mode}-sliced.3mf','--outputdir',str(out),str(OLD/f'{mode}-diagnostic.3mf')]
r={'status':'DIAGNOSTIC NON-PRINT-RELEASE','fingerprint':manifest['fingerprint'],'argv':cmd,'bundle_version':plistlib.loads((binary.parents[1]/'Info.plist').read_bytes()).get('CFBundleShortVersionString'),'executable_sha256':sha(binary),'started':time.time()};(out/'command.json').write_text(json.dumps(r,indent=2)+'\n')
with (out/'slicer.log').open('w') as log:
 child=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT)
 try:rc=child.wait(timeout=180)
 except subprocess.TimeoutExpired:child.kill();rc=child.wait();r['timed_out']=True
r.update(child_exit=rc,elapsed_s=time.time()-r['started'],artifacts={str(q.relative_to(ROOT)):{'bytes':q.stat().st_size,'sha256':sha(q)} for q in out.rglob('*') if q.suffix in ['.gcode','.3mf']});(out/'receipt.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
