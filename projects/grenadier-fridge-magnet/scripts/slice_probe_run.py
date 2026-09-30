"""Isolated diagnostic Snapmaker Orca subprocess; no printer contact."""
from pathlib import Path
import subprocess,json,time,hashlib,sys,plistlib
P=Path(__file__).resolve().parents[1];D=P/'slicer/p1-r3';binary=Path('/Applications/Snapmaker Orca.app/Contents/MacOS/Snapmaker_Orca')
variant=sys.argv[1];out=D/(variant+'-02-'+(sys.argv[2] if len(sys.argv)>2 else 'run1'));out.mkdir(exist_ok=False)
(out/'datadir').mkdir()
cmd=[str(binary),'--debug','3','--datadir',str(out/'datadir'),'--load-settings',';'.join(str(D/(n+'.json')) for n in ['machine','process']),'--load-filaments',';'.join(str(D/f'filament-{n}.json') for n in range(4)),'--arrange','0','--orient','0','--slice','0','--export-3mf',str(out/(variant+'-sliced.3mf')),'--outputdir',str(out),str(D/(variant+'-diagnostic.3mf'))]
receipt={'argv':cmd,'status':'DIAGNOSTIC NON-PRINT-RELEASE','bundle_version':plistlib.loads((binary.parents[1]/'Info.plist').read_bytes()).get('CFBundleShortVersionString'),'executable_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'inputs':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in list(D.glob('*.json'))+list(D.glob('*.3mf'))},'started':time.time()}
(out/'command.json').write_text(json.dumps(receipt,indent=2))
with (out/'slicer.log').open('w') as log:
 child=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT)
 try:rc=child.wait(timeout=210)
 except subprocess.TimeoutExpired:child.kill();rc=child.wait();receipt['timed_out']=True
receipt.update(child_exit=rc,elapsed_s=time.time()-receipt['started'],artifacts={str(p):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in out.iterdir() if p.suffix in ['.gcode','.3mf']})
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
