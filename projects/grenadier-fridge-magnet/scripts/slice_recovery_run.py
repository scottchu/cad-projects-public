"""P3-D native diagnostic recovery; no geometry, GUI, or printer mutations."""
from pathlib import Path
import hashlib,json,subprocess,time,sys
ROOT=Path(__file__).resolve().parents[3]; P=ROOT/'projects/grenadier-fridge-magnet'; OLD=P/'slicer/p1-r3'; D=P/'slicer/p1-r3-recovery'; I=P/'docs/iterations/p1-r3-slice-probe'; D.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
variant=sys.argv[1]
if not (D/'input-manifest.json').exists():
 machine=json.loads((OLD/'machine.json').read_text()); process=json.loads((OLD/'process.json').read_text());machine['wipe_tower_filament']=process.pop('wipe_tower_filament')
 assert machine['nozzle_diameter']==['0.2']*4
 for name,obj in [('machine',machine),('process',process)]: (D/f'{name}.json').write_text(json.dumps(obj,indent=2)+'\n')
 for i in range(4):(D/f'filament-{i}.json').write_bytes((OLD/f'filament-{i}.json').read_bytes())
 paths=[OLD/'flat-diagnostic.3mf',OLD/'relief-diagnostic.3mf',I/'input-manifest.json',I/'BRIEF.md',P/'docs/REQUIREMENTS.md',Path(__file__).resolve(),*D.glob('*.json')]
 entries=[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in sorted(paths)]
 fp=hashlib.sha256(''.join(e['path']+'\0'+e['sha256']+'\n' for e in entries).encode()).hexdigest()
 (D/'input-manifest.json').write_text(json.dumps({'fingerprint':fp,'parent':'d03289125d33c90026f742f5732acef9c98a58f6c5e87015598d631db4871dcb','method':'SHA256(sorted path + NUL + SHA256(content) + LF)','entries':entries},indent=2)+'\n')
manifest=json.loads((D/'input-manifest.json').read_text());assert all(sha(ROOT/e['path'])==e['sha256'] for e in manifest['entries'])
out=D/(variant+'-run1');out.mkdir(exist_ok=False);(out/'datadir').mkdir()
binary=Path('/Applications/Snapmaker Orca.app/Contents/MacOS/Snapmaker_Orca')
cmd=[str(binary),'--debug','3','--datadir',str(out/'datadir'),'--load-settings',';'.join(str(D/f'{n}.json') for n in ['machine','process']),'--load-filaments',';'.join(str(D/f'filament-{n}.json') for n in range(4)),'--arrange','0','--orient','0','--slice','0','--export-3mf',str(out/f'{variant}-sliced.3mf'),'--outputdir',str(out),str(OLD/f'{variant}-diagnostic.3mf')]
r={'status':'DIAGNOSTIC NON-PRINT-RELEASE','fingerprint':manifest['fingerprint'],'argv':cmd,'executable_sha256':sha(binary),'started':time.time()};(out/'command.json').write_text(json.dumps(r,indent=2)+'\n')
with (out/'slicer.log').open('w') as log:
 child=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT)
 try:rc=child.wait(timeout=210)
 except subprocess.TimeoutExpired:child.kill();rc=child.wait();r['timed_out']=True
r.update(child_exit=rc,elapsed_s=time.time()-r['started'],artifacts={str(p.relative_to(ROOT)):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in out.rglob('*') if p.suffix in ['.gcode','.3mf']})
(out/'receipt.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
