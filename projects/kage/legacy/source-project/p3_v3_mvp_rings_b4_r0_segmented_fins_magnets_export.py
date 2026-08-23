"""STEP-first and printed-only 3MF exports for B4-R0."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from uuid import NAMESPACE_URL,uuid5
from zipfile import ZipFile

from build123d import export_step,import_step
import lib3mf
import trimesh

import p3_v3_mvp_rings_b4_r0_segmented_fins_magnets_geometry as g
from p3_v3_mvp_rings_b4_r0_segmented_fins_magnets_spec import MODEL_ROOT,NAMESPACE,SPEC

ASSEMBLED_STEP=MODEL_ROOT/f"{NAMESPACE}_assembled.step"
EXPLODED_STEP=MODEL_ROOT/f"{NAMESPACE}_assembly_order_exploded.step"
MODEL_ONLY_3MF=MODEL_ROOT/f"{NAMESPACE}_nine_ring_segments_model_only.3mf"
README=MODEL_ROOT/"README.md"


def required_artifact_paths(): return (ASSEMBLED_STEP,EXPLODED_STEP,MODEL_ONLY_3MF,README)


def _mesh(shape):
 vertices,triangles=shape.tessellate(SPEC.mesh_linear_deflection_mm,SPEC.mesh_angular_deflection_rad)
 mesh=trimesh.Trimesh(vertices=[(v.X,v.Y,v.Z) for v in vertices],faces=triangles,process=True,validate=True)
 if not(mesh.is_watertight and mesh.is_winding_consistent and mesh.is_volume): raise RuntimeError("non-manifold printable mesh")
 vv=[]
 for vertex in mesh.vertices:
  p=lib3mf.Position();p.Coordinates[:]=tuple(float(x) for x in vertex);vv.append(p)
 tt=[]
 for a,b,c in mesh.faces:
  t=lib3mf.Triangle();t.Indices[:]=(int(a),int(b),int(c));tt.append(t)
 return vv,tt


def write_model_only_3mf(path=MODEL_ONLY_3MF):
 rows=g.printable_occurrences()
 if len(rows)!=9: raise RuntimeError(f"expected nine segments, got {len(rows)}")
 path.parent.mkdir(parents=True,exist_ok=True)
 w=lib3mf.Wrapper();model=w.CreateModel()
 for row in rows:
  obj=model.AddMeshObject();obj.SetName(row["label"]);obj.SetUUID(str(uuid5(NAMESPACE_URL,f"{NAMESPACE}:{row['label']}")))
  vertices,triangles=_mesh(row["shape"]);obj.SetGeometry(vertices,triangles);model.AddBuildItem(obj,w.GetIdentityTransform())
 with TemporaryDirectory(prefix=f".{NAMESPACE}-",dir=path.parent) as temp:
  candidate=Path(temp)/path.name;model.QueryWriter("3mf").WriteToFile(str(candidate))
  with ZipFile(candidate) as archive:
   if archive.testzip() is not None: raise RuntimeError("3MF CRC failure")
   if any(any(token in name.lower() for token in ("project_settings","model_settings","slice_info")) for name in archive.namelist()): raise RuntimeError("3MF is not model-only")
  path.write_bytes(candidate.read_bytes())
 return path


def fresh_lib3mf_import_evidence(path=MODEL_ONLY_3MF):
 script='''import json,lib3mf,sys\nw=lib3mf.Wrapper();m=w.CreateModel();m.QueryReader("3mf").ReadFromFile(sys.argv[1]);o=[];it=m.GetMeshObjects()\nwhile it.MoveNext():\n x=it.GetCurrentMeshObject();o.append((x.GetName(),x.GetVertexCount(),x.GetTriangleCount(),x.IsManifoldAndOriented()))\nb=[];it=m.GetBuildItems()\nwhile it.MoveNext():b.append(it.GetCurrent().GetObjectResource().GetName())\nprint(json.dumps({"o":o,"b":b}))'''
 result=subprocess.run([sys.executable,"-c",script,str(path)],check=True,capture_output=True,text=True);data=json.loads(result.stdout)
 return {"object_count":len(data["o"]),"build_item_count":len(data["b"]),"all_nonempty":all(x[1] and x[2] for x in data["o"]),"all_manifold_and_oriented":all(x[3] for x in data["o"]),"unique_names":len({x[0] for x in data["o"]})==len(data["o"])}


def _signature(shape):
 b=shape.bounding_box();return len(shape.solids()),(b.min.X,b.min.Y,b.min.Z,b.max.X,b.max.Y,b.max.Z),sum(s.volume for s in shape.solids()),all(s.is_valid for s in shape.solids())


def source_export_parity_evidence():
 rows=[]
 for source,path in ((g.assembled_shape(),ASSEMBLED_STEP),(g.exploded_assembly_order_shape(),EXPLODED_STEP)):
  a,b=_signature(source),_signature(import_step(path));rows.append({"path":str(path),"solid_count_equal":a[0]==b[0],"bounds_error_mm":max(abs(x-y) for x,y in zip(a[1],b[1])),"volume_error_mm3":abs(a[2]-b[2]),"written_valid":b[3]})
 return {"rows":tuple(rows),"all_required_exist":all(p.is_file() and p.stat().st_size for p in required_artifact_paths()),"all_solid_counts_equal":all(x["solid_count_equal"] for x in rows),"all_written_valid":all(x["written_valid"] for x in rows),"maximum_bounds_error_mm":max(x["bounds_error_mm"] for x in rows),"maximum_volume_error_mm3":max(x["volume_error_mm3"] for x in rows)}


def export_all():
 MODEL_ROOT.mkdir(parents=True,exist_ok=True);export_step(g.assembled_shape(),ASSEMBLED_STEP);export_step(g.exploded_assembly_order_shape(),EXPLODED_STEP);write_model_only_3mf()
 README.write_text("# B4-R0 segmented moving rings\n\nCAD-only MVP: nine printed ring segments with integral fins and sealed magnet cavities. Purchased magnets and M3 fasteners are STEP witnesses only. No Hall sensors, electronics, LEDs, or added balance weights.\n")
 return required_artifact_paths()


if __name__=="__main__":
 export_all();print(json.dumps({"3mf":fresh_lib3mf_import_evidence(),"parity":source_export_parity_evidence()},indent=2))
