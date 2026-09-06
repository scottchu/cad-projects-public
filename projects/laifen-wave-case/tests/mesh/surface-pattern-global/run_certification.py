import argparse, hashlib, json, subprocess, time
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--certifier',type=Path,required=True)
parser.add_argument('--fixture-dir',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--body',type=Path,required=True)
parser.add_argument('--cap',type=Path,required=True)
parser.add_argument('--assembled',type=Path,required=True)
parser.add_argument('--print-layout',type=Path,required=True)
parser.add_argument('--wide-print-layout',type=Path,required=True)
args=parser.parse_args()
root=args.fixture_dir
binary=args.certifier
tolerance='0.000001'
cases=[
 ('default-body',args.body,'6789c6b1ade20b205646bcc2e5eb17d22b515e47c6e3fd1fd5688390376f60c8',None),
 ('default-cap',args.cap,'e9629eb47fc215a914d6579c77af945d96d935789a44a5cacb7557bd0dbcd514',None),
 ('default-assembled',args.assembled,'5cfe2f06339bcc3df70dbc7072448789e5078aee9998a6599016298a148260fe','135'),
 ('default-print-layout',args.print_layout,'73dc750bd9bea35d1e65e4cd05ec7a56b1cc5cdd42faf8a1649455694d83062e',None),
 ('wide-print-layout',args.wide_print_layout,'4f42c45b9a847f5de188359cbe710b0d631450901a70173aec4f1e371c7d3041',None),
]
rows=[];started=time.monotonic()
for label,path,expected,seam in cases:
 actual=hashlib.sha256(path.read_bytes()).hexdigest()
 if actual!=expected: raise SystemExit(f'{label} hash drift: {actual}')
 command=[str(binary),str(path),tolerance]+([seam] if seam else [])
 completed=subprocess.run(command,text=True,capture_output=True)
 if completed.returncode: raise SystemExit(f'{label} failed: {completed.stdout}{completed.stderr}')
 row=json.loads(completed.stdout);row['label']=label;row['sha256']=actual;rows.append(row)
fixtures=[]
for label,expected_code in [('adjacent',0),('crossing',1),('coplanar',1),('tjunction',1)]:
 completed=subprocess.run([str(binary),str(root/f'{label}.stl'),tolerance],text=True,capture_output=True)
 if completed.returncode!=expected_code: raise SystemExit(f'fixture {label} returned {completed.returncode}')
 row=json.loads(completed.stdout);row['label']=label;row['expectedExit']=expected_code;fixtures.append(row)
result={'status':'pass','candidateCommit':'8068fbd19b4fd526d6120e7dfd714e9aca217a9b','candidateManifestSha256':'412b5e389a85dbaa7ad730870f496639d8dcd2e2129de733b4da1ba1e031fc63','toleranceMm':float(tolerance),'certifierBinarySha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'runnerSha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'rows':rows,'fixtures':fixtures,'wallSeconds':time.monotonic()-started}
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
