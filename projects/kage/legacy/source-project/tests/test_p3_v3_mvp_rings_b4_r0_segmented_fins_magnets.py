"""Focused B4-R0 MVP acceptance gates."""

import pytest

import p3_v3_mvp_rings_b4_r0_segmented_fins_magnets_export as export
import p3_v3_mvp_rings_b4_r0_segmented_fins_magnets_validation as v
from p3_v3_mvp_rings_b4_r0_segmented_fins_magnets_spec import SPEC


def test_01_predecessors_immutable(): assert v.immutable_hash_evidence()["all_unchanged"]
def test_02_exact_260_continuous_teeth_and_valley_seams():
 e=v.tooth_and_seam_evidence();assert e["total_teeth"]==260;assert e["span_total_deg"]==pytest.approx(360,abs=1e-6);assert e["pairwise_max_iv_mm3"]<=SPEC.brep_tolerance_mm3;assert e["joinery_inner_radius_mm"]==132.5
def test_03_nine_segments_valid_and_fit_bed():
 e=v.segment_evidence();assert e["count"]==9 and e["all_valid_one_solid"];assert e["maximum_bbox_mm"]<=255
def test_04_lap_contact_split_and_role_clearance():
 e=v.lap_fastener_evidence();assert e["lap_length_mm"]==23;assert e["lap_contact_area_mm2"]==pytest.approx(78.38);assert e["lap_contact_area_mm2"]>=76.8;assert e["lap_split_total_mm"]==4.4;assert e["role_clearances_mm"]==pytest.approx((.9,.9));assert e["boss_tangential_length_mm"]==12;assert e["seam_relief_mm"]==.2;assert e["relief_radii_mm"]==(133.35,138.9)
def test_05_tangential_m3_and_captive_nut_envelopes():
 e=v.lap_fastener_evidence();assert e["screw_axis_radius_mm"]==136.4;assert e["screw_clearance_diameter_mm"]==3.4;assert e["nut_pocket_af_depth_mm"]==(5.7,2.6);assert e["maximum_nut_obstruction_mm3"]<=SPEC.brep_tolerance_mm3;assert e["maximum_bore_obstruction_mm3"]<=SPEC.brep_tolerance_mm3
def test_06_seam_joinery_sweeps_through_all_rollers(): assert v.seam_passage_evidence()["maximum_iv_mm3"]<=SPEC.brep_tolerance_mm3
def test_07_race_and_tooth_clearances_frozen(): assert (SPEC.ring.race_radius_mm,SPEC.ring.tip_radius_mm,SPEC.ring.root_radius_mm)==(131.6,129.0,132.5)
def test_08_all_q_mesh_states_are_enumerated(): assert v.motion_matrix_evidence()["q_states"]==(-.35,0,.1)
def test_09_fins_clear_higher_rings_rollers_and_pinions():
 e=v.fin_clearance_evidence();assert e["max_higher_ring_iv_mm3"]<=SPEC.brep_tolerance_mm3;assert e["higher_ring_radial_clearance_mm"]==pytest.approx(.3);assert e["roller_radial_clearance_mm"]>=1;assert e["pinion_radial_clearance_mm"]>=1
def test_10_independent_one_degree_and_72_coupled_states():
 e=v.motion_matrix_evidence();assert e["independent_step_deg"]==1;assert e["independent_state_count"]==1080;assert e["coupled_state_count"]==72 and e["all_rotations_preserve_clearances"]
def test_11_sealed_magnet_cavities_have_skins_and_walls():
 e=v.magnet_and_com_evidence();assert e["minimum_skin_mm"]==pytest.approx(1.1);assert e["minimum_outer_wall_mm"]>=.6-1e-8;assert all(x["inner_wall_to_root_mm"]>0 for x in e["rows"])
def test_12_density_weighted_com_needs_no_added_weights(): assert v.magnet_and_com_evidence()["maximum_eccentricity_mm"]<=.5
def test_13_fin_envelope_and_replaceable_optics():
 assert v.fin_clearance_evidence()["max_outer_diameter_mm"]==287.4;assert v.optical_evidence()["extensions_mm"]==(35.1,39.4,44.1);assert v.optical_evidence()["replaceable"]
def test_14_artifacts_exact_nine_prints_and_cad_only_boundary():
 m=export.fresh_lib3mf_import_evidence();assert m["object_count"]==m["build_item_count"]==9;assert m["all_manifold_and_oriented"]
 p=export.source_export_parity_evidence();assert p["all_solid_counts_equal"] and p["all_written_valid"] and p["maximum_bounds_error_mm"]<=1e-6 and p["maximum_volume_error_mm3"]<=1e-4
 b=v.physical_boundary();assert b["cad_only"] and not b["later_layers_present"]
