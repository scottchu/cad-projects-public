import argparse
from pathlib import Path
parser=argparse.ArgumentParser()
parser.add_argument('--output-dir',type=Path,default=Path('/tmp/surface-pattern-global'))
args=parser.parse_args()
root=args.output_dir
root.mkdir(parents=True,exist_ok=True)
def write(name,tris):
 s='solid x\n'
 for tri in tris:
  s+='facet normal 0 0 0\nouter loop\n'+''.join(f'vertex {x} {y} {z}\n' for x,y,z in tri)+'endloop\nendfacet\n'
 (root/name).write_text(s+'endsolid x\n')
write('adjacent.stl',[[(0,0,0),(1,0,0),(0,1,0)],[(1,0,0),(1,1,0),(0,1,0)]])
write('crossing.stl',[[(0,0,0),(2,0,0),(0,2,0)],[(.5,-.5,-1),(.5,1.5,1),(.5,1.5,-1)]])
write('coplanar.stl',[[(0,0,0),(2,0,0),(0,2,0)],[(.5,.5,0),(2,.5,0),(.5,2,0)]])
write('tjunction.stl',[[(0,0,0),(2,0,0),(0,2,0)],[(1,0,0),(1,-1,0),(2,-1,0)]])
