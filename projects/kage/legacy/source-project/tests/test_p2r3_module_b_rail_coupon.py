from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import re
import subprocess
from xml.etree import ElementTree as ET
from zipfile import ZipFile

import pytest
import trimesh
from build123d import Axis, Location, import_step

from p2r3_module_b_rail_coupon_export import mesh_data, print_mesh_data
from p2r3_module_b_rail_coupon_geometry import (
    PRINTABLE_FACTORIES,
    make_installed_coupon,
    make_main_rail_coupon,
    make_removable_gate,
    make_second_follower_fin,
    pairwise_intersection_volume,
    placed_follower,
)
from p2r3_module_b_rail_coupon_spec import P2R2_ISOLATION_SHA256, P2R3_MODULE_B


ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "p2r3_module_b_rail_coupon"


def test_frozen_repaired_profile_and_layer_math():
    p = P2R3_MODULE_B
    assert p.radius == 135.0
    assert p.rail_angle_span_deg == 110.0
    assert (p.stationary_inner_radius, p.stationary_outer_radius) == (125.0, 145.0)
    assert (p.rear_web_top_z, p.constant_cavity_top_z, p.throat_z) == (1.2, 5.1, 7.9)
    assert (p.cavity_radial_width, p.throat_radial_width) == (9.6, 4.8)
    assert p.capture_overlap_per_side == pytest.approx(2.1)
    assert p.cavity_clearance_per_side == pytest.approx(0.3)
    assert p.throat_clearance_per_side == pytest.approx(0.3)
    assert (p.axial_rear_clearance, p.axial_front_clearance) == pytest.approx((0.2, 0.2))
    assert p.usable_follower_travel_deg >= 98.0

    widths = [p.cavity_half_width_at_z(5.1 + 0.2 * i) for i in range(15)]
    layer_steps = [abs(a - b) for a, b in zip(widths, widths[1:])]
    assert max(layer_steps) == pytest.approx(0.1714285714)
    assert max(layer_steps) <= p.layer_height


def test_exactly_three_valid_positive_printable_solids_and_bed_footprint():
    assert [name for name, _ in PRINTABLE_FACTORIES] == [
        "main_rail_coupon",
        "second_follower_fin",
        "removable_gate",
    ]
    for _name, factory in PRINTABLE_FACTORIES:
        part = factory()
        assert part.is_valid and len(part.solids()) == 1 and part.volume > 0
        mesh = mesh_data(part)
        assert mesh.is_watertight and mesh.is_volume
        assert mesh.volume == pytest.approx(part.volume, abs=0.10)
    bbox = make_main_rail_coupon().bounding_box()
    assert bbox.size.X <= 77.0
    assert bbox.size.Y <= 238.0
    assert max(bbox.size.X, bbox.size.Y) + 2 * P2R3_MODULE_B.brim <= 248.0


def test_magnet_pocket_membrane_roof_and_single_magnet_depth():
    p = P2R3_MODULE_B
    follower = make_second_follower_fin()
    assert (p.magnet_pocket_diameter, p.magnet_pocket_depth) == (6.15, 3.10)
    assert p.membrane_thickness == 0.20
    assert p.magnet_roof == 0.40
    assert p.pocket_void_depth_before_breakout == pytest.approx(2.90)
    assert p.pocket_void_depth_before_breakout + p.membrane_thickness == pytest.approx(3.10)
    assert follower.is_inside((p.radius, 0.0, 1.50))  # sacrificial membrane
    assert not follower.is_inside((p.radius, 0.0, 2.00))  # pocket void
    assert not follower.is_inside((p.radius, 0.0, p.pocket_front_z - 0.01))
    assert follower.is_inside((p.radius, 0.0, p.pocket_front_z + 0.01))
    assert follower.is_inside((p.radius, 0.0, 4.70))  # exact 0.40 mm roof
    assert not follower.is_inside((p.radius + 3.00, 0.0, 2.00))
    assert follower.is_inside((p.radius + 3.20, 0.0, 2.00))
    assert p.magnet_face_gap == pytest.approx(2.0)
    assert p.physical_gap_shims == (1.7, 2.0, 2.4)

    # The printable mesh must preserve one negative inner shell for the blind
    # pocket rather than flipping it positive and filling the magnet seat.
    mesh = mesh_data(follower)
    shell_volumes = sorted(component.volume for component in mesh.split(only_watertight=True))
    assert len(shell_volumes) == 2
    assert shell_volumes[0] < -80.0 and shell_volumes[1] > 1000.0
    assert sum(shell_volumes) == pytest.approx(follower.volume, abs=0.10)


def test_gate_has_validated_side_print_orientation_not_tab_cantilevers():
    p = P2R3_MODULE_B
    gate = make_removable_gate()
    printable = print_mesh_data("removable_gate", gate)
    assert printable.bounds[0][2] == pytest.approx(0.0, abs=1e-8)
    # The radial seam plane is on the bed: angular arc becomes build height,
    # while the original 9 mm axial stack becomes the narrow Y footprint.
    assert printable.extents[2] >= 28.0
    assert printable.extents[1] <= 9.01
    assert p.gate_side_print_max_radial_step < 0.05
    assert p.gate_side_print_max_radial_step <= p.layer_height
    assert p.m2_clearance_diameter <= p.maximum_gate_bridge_span


def test_one_degree_installed_sweep_is_collision_free_and_captured():
    p = P2R3_MODULE_B
    main = make_main_rail_coupon()
    gate = make_removable_gate()
    half_travel = p.usable_follower_travel_deg / 2.0
    checked = 0
    for angle in range(-51, 52):
        assert abs(angle) <= half_travel
        follower = placed_follower(float(angle))
        assert pairwise_intersection_volume(main, follower) <= 1e-6
        assert pairwise_intersection_volume(gate, follower) <= 1e-6
        checked += 1
    assert checked == 103

    # At the loading seam the installed gate blocks forward extraction.
    assert pairwise_intersection_volume(gate, placed_follower(0.0, 2.0)) > 1.0
    # With the gate removed, every 1-degree pose whose complete 18 mm shoe is
    # inside the 12-degree loading window lifts freely.
    extraction_half_angle = p.gate_nominal_angle_deg / 2.0 - p.follower_arc_angle_deg / 2.0
    assert extraction_half_angle > 2.0
    for angle in range(-2, 3):
        assert pairwise_intersection_volume(main, placed_follower(float(angle), 5.0)) <= 1e-6


def test_gate_section_clearances_seam_and_m2_interfaces():
    p = P2R3_MODULE_B
    main = make_main_rail_coupon()
    gate = make_removable_gate()
    assert p.gate_nominal_angle_deg == 12.0
    assert p.gate_arc_length == pytest.approx(28.2743339)
    assert p.gate_cut_outer - p.gate_cut_inner == pytest.approx(14.0)
    assert p.gate_radial_inner - p.gate_cut_inner == pytest.approx(0.2)
    assert p.gate_cut_outer - p.gate_radial_outer == pytest.approx(0.2)
    assert p.gate_cut_edge_clearance == pytest.approx(0.2)
    assert p.m2_radii == (123.5, 146.5)
    assert (p.m2_clearance_diameter, p.m2_pilot_diameter, p.m2_pilot_depth) == (2.2, 1.6, 4.0)
    assert pairwise_intersection_volume(main, gate) <= 1e-6
    assert len(make_installed_coupon().solids()) == 3


def test_p2r2_source_and_accepted_artifacts_remain_byte_identical():
    for relative, expected in P2R2_ISOLATION_SHA256.items():
        path = ROOT / relative
        assert path.exists()
        assert sha256(path.read_bytes()).hexdigest() == expected


def test_step_exports_match_live_source_geometry():
    pairs = (
        ("main_rail_coupon.step", make_main_rail_coupon()),
        ("second_follower_fin.step", make_second_follower_fin()),
        ("removable_gate.step", make_removable_gate()),
    )
    for filename, live in pairs:
        path = MODEL_ROOT / filename
        assert path.exists() and path.stat().st_size > 0
        exported = import_step(path)
        assert len(exported.solids()) == len(live.solids()) == 1
        assert exported.volume == pytest.approx(live.volume, rel=1e-7)
        assert exported.bounding_box().size == pytest.approx(live.bounding_box().size, rel=1e-7)


def test_print_artifacts_have_three_named_objects_and_fit_256_bed():
    print_root = MODEL_ROOT / "print"
    stls = sorted(print_root.glob("*.stl"))
    assert [path.stem for path in stls] == [
        "main_rail_coupon",
        "removable_gate",
        "second_follower_fin",
    ]
    printable_factories = dict(PRINTABLE_FACTORIES)
    for path in stls:
        # validate=True flips nested shells positive in trimesh and is exactly
        # the rejected failure mode; preserve authored winding on import.
        mesh = trimesh.load_mesh(path, process=True, validate=False)
        assert mesh.is_watertight and mesh.is_volume
        assert mesh.bounds[0][2] == pytest.approx(0.0, abs=1e-6)
        assert mesh.volume == pytest.approx(
            printable_factories[path.stem]().volume, abs=0.10
        )

    bundle = print_root / "p2r3_module_b_r135_three_part_coupon.3mf"
    assert bundle.exists() and bundle.stat().st_size > 0
    ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    with ZipFile(bundle) as package:
        assert package.testzip() is None
        root = ET.fromstring(package.read("3D/3dmodel.model"))
    objects = root.findall("m:resources/m:object", ns)
    items = root.findall("m:build/m:item", ns)
    assert len(objects) == len(items) == 3
    assert [obj.attrib["name"] for obj in objects] == [
        "main_rail_coupon",
        "second_follower_fin",
        "removable_gate",
    ]
    object_meshes = {}
    for obj, item in zip(objects, items):
        transform = [float(v) for v in item.attrib["transform"].split()]
        tx, ty = transform[9], transform[10]
        vertices = obj.findall("m:mesh/m:vertices/m:vertex", ns)
        xs = [float(v.attrib["x"]) + tx for v in vertices]
        ys = [float(v.attrib["y"]) + ty for v in vertices]
        zs = [float(v.attrib["z"]) for v in vertices]
        triangles = obj.findall("m:mesh/m:triangles/m:triangle", ns)
        faces = [
            (int(t.attrib["v1"]), int(t.attrib["v2"]), int(t.attrib["v3"]))
            for t in triangles
        ]
        object_meshes[obj.attrib["name"]] = trimesh.Trimesh(
            vertices=list(zip(xs, ys, zs)), faces=faces, process=True, validate=False
        )
        assert min(xs) >= 0 and max(xs) <= P2R3_MODULE_B.bed_size
        assert min(ys) >= 0 and max(ys) <= P2R3_MODULE_B.bed_size
        assert min(zs) == pytest.approx(0.0, abs=1e-7)

    follower_mesh = object_meshes["second_follower_fin"]
    follower_brep = make_second_follower_fin()
    assert follower_mesh.volume == pytest.approx(follower_brep.volume, abs=0.10)
    pocket_shells = sorted(
        component.volume for component in follower_mesh.split(only_watertight=True)
    )
    assert len(pocket_shells) == 2 and pocket_shells[0] < 0.0
    # After Z-normalizing the follower, the internal pocket shell begins above
    # the 0.20 mm sacrificial membrane and ends at the 3.10 mm seat depth.
    inner_shell = min(follower_mesh.split(only_watertight=True), key=lambda m: m.volume)
    assert inner_shell.bounds[0][2] == pytest.approx(0.20, abs=0.02)
    assert inner_shell.bounds[1][2] == pytest.approx(3.10, abs=0.02)


def test_orca_loads_bundle_and_preserves_blind_pocket_volume_when_available():
    orca = Path("/Applications/OrcaSlicer.app/Contents/MacOS/OrcaSlicer")
    if not orca.exists():
        pytest.skip("OrcaSlicer is not installed on this host")
    bundle = MODEL_ROOT / "print" / "p2r3_module_b_r135_three_part_coupon.3mf"
    result = subprocess.run(
        [str(orca), "--info", str(bundle)],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.count("manifold = yes") == 3
    volumes = [float(value) for value in re.findall(r"volume = ([0-9.]+)", result.stdout)]
    assert len(volumes) == 3
    assert any(
        volume == pytest.approx(make_second_follower_fin().volume, abs=0.10)
        for volume in volumes
    )
