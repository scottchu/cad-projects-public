"""P20 test-only Blue-Orange minimum-web print coupon.

The authoritative geometry is the immutable 361-point LEFT-outer local
trajectory contract frozen in ``p20-blue-orange-web-coupon/DESIGN.md``.  This
module intentionally contains no P20 product assembly geometry: only a
rectangular plate patch and the Blue and Orange swept through-cutters.

Source coordinates use X as plate thickness and the simulator's FRONT YZ
plane.  ``build_print_coupon`` applies the one declared rigid transform that
puts a broad YZ face on the printer bed with thickness along build +Z.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from functools import lru_cache
from hashlib import sha256
import json
from math import cos, hypot, radians, sin
from pathlib import Path
from typing import Literal

from build123d import (
    Align,
    Box,
    Face,
    Kind,
    Pos,
    Rot,
    Shape,
    Side,
    Vector,
    Wire,
    extrude,
)


RailName = Literal["blue", "orange"]
PART_LABEL = "P20_test_only_blue_orange_1p72_web_coupon"
SOURCE_SCHEMA = "P20BlueOrangeWebCoupon/v1"

BRIEF_SHA256 = "388c27a9af1c8c6dffe0a809f057428e986d246d099b55617a74de8752ac2081"
DESIGN_SHA256 = "c8920c6014bfbdfe3904ae09975b7446fbc92d2e115a051556279c0d992034f9"
BASELINE_HEAD = "9698cf30e9ddb3e576c08179bfdd067446514c67"


@dataclass(frozen=True, slots=True)
class PointYZ:
    y: float
    z: float

    def as_tuple(self) -> tuple[float, float]:
        return (self.y, self.z)


@dataclass(frozen=True, slots=True)
class RailSpec:
    name: RailName
    start_angle_deg: float
    base_end_y: float
    base_end_z: float


@dataclass(frozen=True, slots=True)
class P20BlueOrangeWebCouponParameters:
    path_steps: int = 360
    blue_start_angle_deg: float = 118.0
    orange_start_angle_deg: float = 45.0
    start_radius_mm: float = 16.0
    inner_arch_mm: float = 0.0
    inner_arch_peak: float = 0.50
    end_offset_y_mm: float = -7.3241343806549555
    end_offset_z_mm: float = -2.77402040577638
    left_end_angle_deg: float = 45.0
    curve_bias: float = 0.0
    rail_cutter_width_mm: float = 4.15
    outer_plate_thickness_mm: float = 3.20
    cutter_overrun_each_face_mm: float = 1.00
    ordinary_min_web_mm: float = 2.20
    coupon_exception_web_mm: float = 1.7150733085690888
    nozzle_diameter_mm: float = 0.40
    material: str = "PETG"

    def __post_init__(self) -> None:
        if self.path_steps != 360:
            raise ValueError("the frozen coupon requires exactly 360 segments / 361 points")
        if self.inner_arch_mm != 0.0 or self.curve_bias != 0.0:
            raise ValueError("the frozen Blue and Orange inner paths are straight")
        if self.rail_cutter_width_mm != 4.15:
            raise ValueError("the frozen sliding cutter width is 4.15 mm")
        if self.outer_plate_thickness_mm != 3.20:
            raise ValueError("the frozen outer-plate thickness is 3.20 mm")

    @property
    def rail_cutter_radius_mm(self) -> float:
        return self.rail_cutter_width_mm / 2.0

    @property
    def cutter_length_x_mm(self) -> float:
        return self.outer_plate_thickness_mm + 2.0 * self.cutter_overrun_each_face_mm


DEFAULTS = P20BlueOrangeWebCouponParameters()

RAIL_SPECS: dict[RailName, RailSpec] = {
    "blue": RailSpec(
        "blue",
        DEFAULTS.blue_start_angle_deg,
        9.552212035894,
        8.022322349948,
    ),
    "orange": RailSpec(
        "orange",
        DEFAULTS.orange_start_angle_deg,
        15.802212035894,
        2.272322349948,
    ),
}

# Frozen source-coordinate blank bounds (X thickness, local FRONT YZ).
BLANK_X_BOUNDS = (-1.6, 1.6)
BLANK_Y_BOUNDS = (-11.786545004574247, 16.308446371474318)
BLANK_Z_BOUNDS = (-10.624660298830026, 18.402161485742834)

BLUE_WITNESS_INDEX = 360
ORANGE_WITNESS_INDEX = 209
WITNESS_CENTER_DISTANCE_MM = 5.8650733085690888
WITNESS_MIDPOINT = PointYZ(7.963860139702033, 0.9389413002297666)


def _rail_spec(rail: RailName) -> RailSpec:
    try:
        return RAIL_SPECS[rail]
    except KeyError as exc:  # fail closed on accidental Green/other geometry
        raise ValueError(f"unsupported coupon rail {rail!r}") from exc


def trajectory_point(
    rail: RailName,
    u: float,
    p: P20BlueOrangeWebCouponParameters = DEFAULTS,
) -> PointYZ:
    """Return the sole deterministic LEFT-outer local centerline authority."""

    if not 0.0 <= u <= 1.0:
        raise ValueError("trajectory progress must stay in 0..1")
    spec = _rail_spec(rail)
    start_angle = radians(spec.start_angle_deg)
    start = PointYZ(
        p.start_radius_mm * cos(start_angle),
        p.start_radius_mm * sin(start_angle),
    )
    end = PointYZ(
        spec.base_end_y + p.end_offset_y_mm,
        spec.base_end_z + p.end_offset_z_mm,
    )
    inner = PointYZ(
        (1.0 - u) * start.y + u * end.y,
        (1.0 - u) * start.z + u * end.z,
    )
    angle = radians(-p.left_end_angle_deg * u)
    return PointYZ(
        inner.y * cos(angle) - inner.z * sin(angle),
        inner.y * sin(angle) + inner.z * cos(angle),
    )


def sampled_trajectory(
    rail: RailName,
    p: P20BlueOrangeWebCouponParameters = DEFAULTS,
) -> tuple[PointYZ, ...]:
    """Return all 361 immutable witnesses, including both endpoints."""

    return tuple(trajectory_point(rail, index / p.path_steps, p) for index in range(p.path_steps + 1))


def sampled_witness_gap_mm(p: P20BlueOrangeWebCouponParameters = DEFAULTS) -> float:
    blue = sampled_trajectory("blue", p)[BLUE_WITNESS_INDEX]
    orange = sampled_trajectory("orange", p)[ORANGE_WITNESS_INDEX]
    return hypot(orange.y - blue.y, orange.z - blue.z) - p.rail_cutter_width_mm


@lru_cache(maxsize=None)
def build_rail_cutter(
    rail: RailName,
    p: P20BlueOrangeWebCouponParameters = DEFAULTS,
) -> Shape:
    """Sweep round 4.15 mm cutter over every straight witness segment.

    The planar wire contains exactly 360 straight edges.  OCC's 2D offset
    constructs the Minkowski sum with a 2.075 mm disk using round joins and
    endpoints.  No spline, resampling, or curve fitting enters the BREP.
    """

    points = sampled_trajectory(rail, p)
    centerline = Wire.make_polygon(
        (Vector(0.0, point.y, point.z) for point in points),
        close=False,
    )
    swept_boundary = centerline.offset_2d(
        p.rail_cutter_radius_mm,
        kind=Kind.ARC,
        side=Side.BOTH,
        closed=True,
    )
    cutter = extrude(
        Face(swept_boundary),
        amount=p.cutter_length_x_mm / 2.0,
        dir=(1.0, 0.0, 0.0),
        both=True,
    )
    cutter.label = f"{rail}_361_point_OD4p15_through_cutter"
    return cutter


@lru_cache(maxsize=None)
def build_coupon(p: P20BlueOrangeWebCouponParameters = DEFAULTS) -> Shape:
    """Build the one source-coordinate coupon solid."""

    y_min, y_max = BLANK_Y_BOUNDS
    z_min, z_max = BLANK_Z_BOUNDS
    blank = Pos(0.0, (y_min + y_max) / 2.0, (z_min + z_max) / 2.0) * Box(
        p.outer_plate_thickness_mm,
        y_max - y_min,
        z_max - z_min,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    coupon = blank - build_rail_cutter("blue", p) - build_rail_cutter("orange", p)
    coupon.label = PART_LABEL
    return coupon


@lru_cache(maxsize=None)
def build_print_coupon(p: P20BlueOrangeWebCouponParameters = DEFAULTS) -> Shape:
    """Rigidly orient the coupon for support-free printing at build Z=0."""

    oriented = Pos(0.0, 0.0, p.outer_plate_thickness_mm / 2.0) * Rot(0.0, -90.0, 0.0) * build_coupon(p)
    oriented.label = PART_LABEL
    return oriented


def actual_solid_evidence(p: P20BlueOrangeWebCouponParameters = DEFAULTS) -> dict[str, object]:
    blue = build_rail_cutter("blue", p)
    orange = build_rail_cutter("orange", p)
    coupon = build_coupon(p)
    bounds = coupon.bounding_box()
    return {
        "blueOrangeCutterDistanceMm": blue.distance_to(orange),
        "blueOrangeIntersectionMm3": float((blue & orange).volume),
        "couponSolidCount": len(coupon.solids()),
        "couponValid": bool(coupon.is_valid),
        "couponVolumeMm3": float(coupon.volume),
        "couponBounds": {
            "min": [bounds.min.X, bounds.min.Y, bounds.min.Z],
            "max": [bounds.max.X, bounds.max.Y, bounds.max.Z],
            "size": [bounds.size.X, bounds.size.Y, bounds.size.Z],
        },
    }


def parameter_manifest(p: P20BlueOrangeWebCouponParameters = DEFAULTS) -> dict[str, object]:
    return {
        "schema": SOURCE_SCHEMA,
        "status": "test_only_non_product_coupon",
        "units": "mm",
        "baselineHead": BASELINE_HEAD,
        "briefSha256": BRIEF_SHA256,
        "designSha256": DESIGN_SHA256,
        "coordinateConvention": "+X thickness; FRONT local +Y right, +Z up",
        "parameters": asdict(p),
        "railSpecs": {name: asdict(spec) for name, spec in RAIL_SPECS.items()},
        "blankBounds": {
            "x": list(BLANK_X_BOUNDS),
            "y": list(BLANK_Y_BOUNDS),
            "z": list(BLANK_Z_BOUNDS),
        },
        "witness": {
            "blueIndex": BLUE_WITNESS_INDEX,
            "orangeIndex": ORANGE_WITNESS_INDEX,
            "centerDistanceMm": WITNESS_CENTER_DISTANCE_MM,
            "sampledBoundaryGapMm": sampled_witness_gap_mm(p),
            "midpointYZ": list(WITNESS_MIDPOINT.as_tuple()),
        },
        "contents": ["blue_cutout", "orange_cutout"],
        "excluded": ["green", "fixed_axle", "other_rails", "assembly"],
        "printTransform": {
            "rotationDegXYZ": [0.0, -90.0, 0.0],
            "translationXYZMm": [0.0, 0.0, p.outer_plate_thickness_mm / 2.0],
            "result": "broad face at build Z=0; thickness along +Z",
        },
        "physicalAcceptanceClaimed": False,
        "productAcceptanceClaimed": False,
    }


def parameter_manifest_sha256(p: P20BlueOrangeWebCouponParameters = DEFAULTS) -> str:
    encoded = json.dumps(parameter_manifest(p), sort_keys=True, separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _welded_triangles(
    shape: Shape,
    *,
    linear_tolerance: float = 0.01,
    angular_tolerance: float = 0.03,
    weld_tolerance: float = 1.0e-6,
) -> tuple[list[tuple[float, float, float]], list[tuple[int, int, int]]]:
    """Tessellate and weld OCC's per-face duplicate boundary vertices."""

    raw_vertices, raw_triangles = shape.tessellate(linear_tolerance, angular_tolerance)
    vertex_by_key: dict[tuple[int, int, int], int] = {}
    vertices: list[tuple[float, float, float]] = []
    remap: list[int] = []
    for vertex in raw_vertices:
        point = (float(vertex.X), float(vertex.Y), float(vertex.Z))
        key = tuple(int(round(value / weld_tolerance)) for value in point)
        if key not in vertex_by_key:
            vertex_by_key[key] = len(vertices)
            vertices.append(point)
        remap.append(vertex_by_key[key])

    triangles: list[tuple[int, int, int]] = []
    for a, b, c in raw_triangles:
        triangle = (remap[a], remap[b], remap[c])
        if len(set(triangle)) == 3:
            triangles.append(triangle)

    undirected: Counter[tuple[int, int]] = Counter()
    directed: Counter[tuple[int, int]] = Counter()
    for a, b, c in triangles:
        for start, end in ((a, b), (b, c), (c, a)):
            undirected[tuple(sorted((start, end)))] += 1
            directed[(start, end)] += 1
    if any(count != 2 for count in undirected.values()):
        raise ValueError("welded coupon mesh has an open or non-manifold edge")
    if any(directed[(a, b)] != 1 or directed[(b, a)] != 1 for a, b in undirected):
        raise ValueError("welded coupon mesh has inconsistent triangle orientation")
    return vertices, triangles


def export_print_coupon_3mf(
    output: str | Path,
    p: P20BlueOrangeWebCouponParameters = DEFAULTS,
) -> Path:
    """Write and round-trip validate the one-object print-oriented 3MF."""

    import lib3mf

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    vertices, triangles = _welded_triangles(build_print_coupon(p))
    wrapper = lib3mf.Wrapper()
    model = wrapper.CreateModel()
    mesh = model.AddMeshObject()
    mesh.SetName(PART_LABEL)
    mesh.SetGeometry(
        [lib3mf.Position(vertex) for vertex in vertices],
        [lib3mf.Triangle(triangle) for triangle in triangles],
    )
    if not mesh.IsValid() or not mesh.IsManifoldAndOriented():
        raise ValueError("lib3mf rejected the welded source coupon mesh")
    model.AddBuildItem(mesh, wrapper.GetIdentityTransform())
    model.QueryWriter("3mf").WriteToFile(str(output_path))

    check_model = wrapper.CreateModel()
    check_model.QueryReader("3mf").ReadFromFile(str(output_path))
    iterator = check_model.GetMeshObjects()
    count = 0
    while iterator.MoveNext():
        checked = iterator.GetCurrentMeshObject()
        if not checked.IsValid() or not checked.IsManifoldAndOriented():
            raise ValueError("written 3MF failed round-trip validation")
        count += 1
    if count != 1 or check_model.GetBuildItems().Count() != 1:
        raise ValueError("written 3MF must contain exactly one mesh and build item")
    return output_path
