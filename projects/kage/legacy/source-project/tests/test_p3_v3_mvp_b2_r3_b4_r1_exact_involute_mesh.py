"""Focused B2-R3/B4-R1 actual-involute acceptance."""
import pytest
import p3_v3_mvp_drive_b2_r3_exact_involute_output_pinion_geometry as p
import p3_v3_mvp_drive_b2_r3_exact_involute_output_pinion_export as pe
import p3_v3_mvp_drive_b2_r3_exact_involute_output_pinion_spec as ps
import p3_v3_mvp_rings_b4_r0_segmented_fins_magnets_export as r0e
import p3_v3_mvp_rings_b4_r1_exact_involute_mesh_export as e
import p3_v3_mvp_rings_b4_r1_exact_involute_mesh_validation as v
from p3_v3_mvp_rings_b4_r1_exact_involute_mesh_spec import SPEC

def test_01_b2_r2_and_b4_r0_immutable(): assert v.immutable_evidence()["all_unchanged"]
def test_02_exact_pinion_contract_and_valid_roles():
 s=ps.SPEC;assert (s.teeth,s.module_mm,s.pressure_angle_deg,s.backlash_mm,s.tip_truncation_mm,s.enable_undercut)==(16,1,20,.1,.1,True);assert s.mesh_backlash_mm==.2
 for role in range(3):
  shape=p.exact_output_pinion(role);assert shape.is_valid and len(shape.solids())==1;assert shape.bounding_box().size.Z==pytest.approx(2.1000002)
def test_03_printed_lower_layer_unchanged():
 x=p.printed_geometry_unchanged_evidence();assert x["before_solids"]==x["after_solids"]==9;assert x["volume_delta_mm3"]<=1e-6
def test_04_compact_actual_brep_mesh_matrix():
 x=v.mesh_probe_evidence();assert x["maximum_iv_mm3"]<=SPEC.brep_tolerance_mm3;assert SPEC.flank_distance_mm[0]<=x["minimum_flank_mm"]<=x["maximum_flank_mm"]<=SPEC.flank_distance_mm[1];assert x["minimum_engagement_mm"]>=1.65 and x["maximum_engagement_mm"]<=2.10
def test_05_required_probe_families_present(): assert set(v.mesh_probe_evidence()["kinds"])=={"compact_coupled_worst","nominal_role","q_theta_representative","qmax_every_seam"}
def test_06_actual_lap_contact_skin_measurement():
 x=v.measured_lap_contact_evidence();assert x["epsilon_mm"]==.02;assert len(x["rows"])==9;assert x["minimum_area_mm2"]>=76.8;assert x["spread_mm2"]<=.5
def test_07_nearest_fin_clearances_actual_brep(): assert v.nearest_fin_evidence()["maximum_iv_mm3"]<=SPEC.brep_tolerance_mm3
def test_08_magnet_sensor_positions_without_sensor_solids():
 x=v.magnet_sensor_position_evidence();assert len(x["rows"])==3 and x["no_sensor_solids_added"];assert all(row["center_xyz_mm"][0]==pytest.approx(-136.2) for row in x["rows"])
def test_09_b2_r3_and_b4_r1_source_export_parity():
 a=pe.parity_evidence();assert a["solid_count_equal"] and a["written_valid"] and a["bounds_error_mm"]<=1e-6 and a["volume_error_mm3"]<=1e-4
 b=e.parity_evidence();assert b["all_solid_counts_equal"] and b["all_written_valid"] and b["maximum_bounds_error_mm"]<=1e-6 and b["maximum_volume_error_mm3"]<=1e-4
def test_10_unchanged_nine_segment_3mf_and_no_b5():
 x=r0e.fresh_lib3mf_import_evidence(e.MODEL_ONLY_3MF);assert x["object_count"]==x["build_item_count"]==9 and x["all_manifold_and_oriented"];b=v.physical_boundary();assert b["cad_only"] and not b["b5_present"]
