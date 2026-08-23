"""B4-R1 STEP and unchanged nine-segment 3MF exports."""
from pathlib import Path
from build123d import export_step,import_step
import p3_v3_mvp_rings_b4_r0_segmented_fins_magnets_export as r0e
import p3_v3_mvp_rings_b4_r1_exact_involute_mesh_geometry as g
from p3_v3_mvp_rings_b4_r1_exact_involute_mesh_spec import MODEL_ROOT,NAMESPACE

ASSEMBLED_STEP=MODEL_ROOT/f"{NAMESPACE}_assembled.step"
EXPLODED_STEP=MODEL_ROOT/f"{NAMESPACE}_assembly_order_exploded.step"
MODEL_ONLY_3MF=MODEL_ROOT/f"{NAMESPACE}_nine_ring_segments_unchanged_model_only.3mf"
README=MODEL_ROOT/"README.md"

def export_all():
 MODEL_ROOT.mkdir(parents=True,exist_ok=True);export_step(g.assembled_shape(),ASSEMBLED_STEP);export_step(g.exploded_shape(),EXPLODED_STEP);write_unchanged_3mf();README.write_text("# B4-R1 exact involute mesh evidence\n\nB4-R0 printed ring segments are unchanged. B2-R3 exact purchased pinions replace analysis witnesses only. No B5 geometry.\n");return (ASSEMBLED_STEP,EXPLODED_STEP,MODEL_ONLY_3MF,README)

def write_unchanged_3mf():
 """Byte-preserve the accepted B4-R0 printed geometry and manifest."""
 MODEL_ROOT.mkdir(parents=True,exist_ok=True)
 MODEL_ONLY_3MF.write_bytes(r0e.MODEL_ONLY_3MF.read_bytes())
 return MODEL_ONLY_3MF
def _sig(s):
 b=s.bounding_box();return len(s.solids()),(b.min.X,b.min.Y,b.min.Z,b.max.X,b.max.Y,b.max.Z),sum(x.volume for x in s.solids()),all(x.is_valid for x in s.solids())
def parity_evidence():
 rows=[]
 for source,path in ((g.assembled_shape(),ASSEMBLED_STEP),(g.exploded_shape(),EXPLODED_STEP)):
  a,b=_sig(source),_sig(import_step(path));rows.append({"solid_count_equal":a[0]==b[0],"bounds_error_mm":max(abs(x-y) for x,y in zip(a[1],b[1])),"volume_error_mm3":abs(a[2]-b[2]),"written_valid":b[3]})
 return {"rows":tuple(rows),"all_solid_counts_equal":all(x["solid_count_equal"] for x in rows),"all_written_valid":all(x["written_valid"] for x in rows),"maximum_bounds_error_mm":max(x["bounds_error_mm"] for x in rows),"maximum_volume_error_mm3":max(x["volume_error_mm3"] for x in rows)}
if __name__=="__main__": print(export_all())
