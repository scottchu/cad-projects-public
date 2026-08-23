"""B2-R3 analysis-witness STEP export."""
from pathlib import Path
from build123d import export_step,import_step
import p3_v3_mvp_drive_b2_r3_exact_involute_output_pinion_geometry as g
from p3_v3_mvp_drive_b2_r3_exact_involute_output_pinion_spec import MODEL_ROOT,NAMESPACE

ASSEMBLED_STEP=MODEL_ROOT/f"{NAMESPACE}_assembled.step"
README=MODEL_ROOT/"README.md"

def export_all():
 MODEL_ROOT.mkdir(parents=True,exist_ok=True);export_step(g.assembled_shape(),ASSEMBLED_STEP);README.write_text("# B2-R3 exact involute output-pinion witness\n\nAnalysis/purchased-witness-only revision. Printed B2-R2 geometry is unchanged.\n");return ASSEMBLED_STEP
def parity_evidence():
 a=g.assembled_shape();b=import_step(ASSEMBLED_STEP);ab=a.bounding_box();bb=b.bounding_box()
 return {"solid_count_equal":len(a.solids())==len(b.solids()),"bounds_error_mm":max(abs(x-y) for x,y in zip((ab.min.X,ab.min.Y,ab.min.Z,ab.max.X,ab.max.Y,ab.max.Z),(bb.min.X,bb.min.Y,bb.min.Z,bb.max.X,bb.max.Y,bb.max.Z))),"volume_error_mm3":abs(sum(s.volume for s in a.solids())-sum(s.volume for s in b.solids())),"written_valid":all(s.is_valid for s in b.solids())}
if __name__=="__main__": print(export_all())
