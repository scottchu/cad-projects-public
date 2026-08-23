"""Actual BREP geometry for the B4-R0 three segmented moving rings."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from math import cos, degrees, radians, sin

from build123d import Align, Axis, Box, Compound, Cylinder, Location, Polygon, extrude
import py_gearworks as pgw

import p3_v3_mvp_roller_b3_r1_blind_axle_towers_geometry as b3
from p3_v3_mvp_rings_b4_r0_segmented_fins_magnets_spec import NAMESPACE, SPEC


R, F, M, H = SPEC.ring, SPEC.fin, SPEC.magnets, SPEC.fasteners


def volume_mm3(shape) -> float:
    return 0.0 if shape is None else float(sum(s.volume for s in shape.solids()))


def intersection_volume_mm3(left, right) -> float:
    return volume_mm3(deepcopy(left).intersect(deepcopy(right)))


def _one(shape, label: str):
    solids = list(shape.solids())
    if len(solids) != 1:
        raise RuntimeError(f"{label} must be one solid, got {len(solids)}")
    result = solids[0]
    if not result.is_valid or result.volume <= 0:
        raise RuntimeError(f"{label} must be valid and positive-volume")
    result.label = label
    return result


def polar(radius: float, angle_deg: float) -> tuple[float,float]:
    a = radians(angle_deg)
    return radius*cos(a), radius*sin(a)


def annulus(inner: float, outer: float, z0: float, height: float):
    return Cylinder(outer,height,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,0,z0))).cut(
        Cylinder(inner,height+0.2,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,0,z0-0.1)))
    )


def sector_mask(start_deg: float, span_deg: float, z0: float=-20.0, z1: float=30.0):
    radius = 170.0
    points = [(0.0,0.0)]
    for index in range(65):
        points.append(polar(radius,start_deg+span_deg*index/64.0))
    points.append((0.0,0.0))
    return extrude(Polygon(*points),amount=z1-z0).moved(Location((0,0,z0)))


def tangent_box(angle: float, r0: float, r1: float, t0: float, t1: float, z0: float, z1: float):
    return Box(r1-r0,t1-t0,z1-z0,align=(Align.MIN,Align.MIN,Align.MIN)).moved(
        Location((r0,t0,z0))
    ).rotate(Axis.Z,angle)


def vertical_cylinder(angle: float, radius: float, diameter: float, z0: float, height: float):
    x,y = polar(radius,angle)
    return Cylinder(diameter/2,height,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((x,y,z0)))


def tangential_cylinder(angle: float, radius: float, diameter: float, tangent0: float, length: float, z: float):
    shape = Cylinder(diameter/2,length,align=(Align.CENTER,Align.CENTER,Align.MIN)).rotate(Axis.X,-90)
    return shape.moved(Location((radius,tangent0,z))).rotate(Axis.Z,angle)


def annular_fin_sector(r0: float, r1: float, width: float, z0: float, z1: float):
    half = degrees(width/(2.0*((r0+r1)/2.0)))
    return _one(
        annulus(r0,r1,z0,z1-z0).intersect(sector_mask(-half,2*half,z0-0.1,z1+0.1)),
        f"{NAMESPACE}_fin_sector",
    )


def fin_shape(role_index: int):
    shelf_z = F.shelf_z_mm[role_index]
    blade_z = F.blade_z_mm[role_index]
    width = F.tangential_widths_mm[role_index]
    shelf = annular_fin_sector(*F.shelf_radii_mm,width,*shelf_z)
    blade = annular_fin_sector(*F.blade_radii_mm,width,*blade_z)
    # The specified root radius is represented by a compact integral root
    # bridge; it joins the nominal shelf/blade edge without changing envelopes.
    root_r = F.root_fillet_mm[role_index]
    root = annular_fin_sector(
        F.blade_radii_mm[0]-root_r/2.0,
        F.blade_radii_mm[0]+root_r/2.0,
        width,
        shelf_z[1]-root_r/2.0,
        blade_z[0]+root_r/2.0,
    )
    result = _one(shelf.fuse(root,blade),f"{NAMESPACE}_{R.roles[role_index]}_integral_fin_datum_0")
    return result


def magnet_cavity(role_index: int):
    z0,z1 = R.carrier_z_mm[role_index]
    return vertical_cylinder(
        M.angle_deg,M.center_radius_mm,M.cavity_diameters_mm[role_index],
        (z0+z1-M.cavity_height_mm)/2.0,M.cavity_height_mm,
    )


@lru_cache(maxsize=3)
def full_role_ring(role_index: int):
    z0,z1 = R.carrier_z_mm[role_index]
    tooth_z0,tooth_z1 = R.tooth_z_mm[role_index]
    teeth = pgw.SpurRingGear(
        number_of_teeth=R.teeth,module=R.module_mm,height=tooth_z1-tooth_z0,
        center=[0,0,tooth_z0],backlash=0.10,
    ).build_part().solid().rotate(Axis.Z,R.tooth_phase_deg)
    body = annulus(R.race_radius_mm,R.body_outer_radius_mm,z0,z1-z0)
    ring = teeth.fuse(body,fin_shape(role_index)).cut(magnet_cavity(role_index))
    return _one(ring,f"{NAMESPACE}_{R.roles[role_index]}_complete_260T_validation_ring")


def _lap_roi(angle: float, z0: float, z1: float):
    return tangent_box(angle,R.root_radius_mm,R.body_outer_radius_mm,-H.lap_length_mm/2,H.lap_length_mm/2,z0,z1)


def _boss_half(angle: float, leading: bool, z0: float, z1: float):
    half = H.boss_tangential_length_mm/2.0
    tangent0,tangent1 = ((0.0,half) if leading else (-half,0.0))
    boss_z0 = z0-(H.boss_axial_mm-(z1-z0))/2.0
    return tangent_box(angle,*H.boss_radii_mm,tangent0,tangent1,boss_z0,boss_z0+H.boss_axial_mm)


def _fastener_bore(angle: float, z0: float, z1: float):
    return tangential_cylinder(
        angle,H.screw_axis_radius_mm,H.screw_clearance_diameter_mm,
        -H.screw_length_mm/2,H.screw_length_mm,(z0+z1)/2,
    )


def _nut_envelope(angle: float, z0: float, z1: float):
    # AF envelope of the tangential captive nut; the STEP witness below is hex.
    return tangent_box(
        angle,H.screw_axis_radius_mm-H.nut_pocket_af_mm/2,
        H.screw_axis_radius_mm+H.nut_pocket_af_mm/2,
        H.boss_tangential_length_mm/2-H.nut_pocket_depth_mm,H.boss_tangential_length_mm/2,
        (z0+z1)/2-H.nut_pocket_af_mm/2,(z0+z1)/2+H.nut_pocket_af_mm/2,
    )


def _tongue_relief(angle: float, leading: bool, z0: float, z1: float):
    half = H.boss_tangential_length_mm/2.0
    tangent0,tangent1 = (
        (-half-H.seam_relief_mm,H.seam_relief_mm)
        if leading
        else (-H.seam_relief_mm,half+H.seam_relief_mm)
    )
    return tangent_box(
        angle,*H.seam_relief_radii_mm,tangent0,tangent1,z0,z1
    )


@lru_cache(maxsize=9)
def segment_shape(role_index: int, segment_index: int):
    z0,z1 = R.carrier_z_mm[role_index]
    start = R.seam_angles_deg[segment_index]
    span = R.segment_spans_deg[segment_index]
    end = start+span
    clipped = full_role_ring(role_index).intersect(sector_mask(start,span))
    if not clipped:
        raise RuntimeError("ring sector crop produced no solid")
    segment = max(clipped,key=lambda shape: shape.volume)
    # Leading side owns the upper lap; trailing side owns the lower lap.
    for angle,leading in ((start,True),(end,False)):
        roi = _lap_roi(angle,z0,z1)
        segment = segment.cut(roi)
        lap_z = (z0+H.lap_split_mm[0],z1) if leading else (z0,z0+H.lap_split_mm[0])
        tongue = _lap_roi(angle,*lap_z).cut(
            _tongue_relief(angle,leading,*lap_z)
        )
        segment = segment.fuse(tongue,_boss_half(angle,leading,z0,z1))
        segment = segment.cut(_fastener_bore(angle,z0,z1))
        if leading:
            segment = segment.cut(_nut_envelope(angle,z0,z1))
    label = f"{NAMESPACE}_{R.roles[role_index]}_segment_{R.segment_names[segment_index]}_{R.segment_teeth[segment_index]}T"
    return _one(segment,label)


def magnet_witness(role_index: int):
    z0,z1 = R.carrier_z_mm[role_index]
    shape = vertical_cylinder(
        M.angle_deg,M.center_radius_mm,M.purchased_diameters_mm[role_index],
        (z0+z1-M.purchased_thickness_mm)/2,M.purchased_thickness_mm,
    )
    return _one(shape,f"{NAMESPACE}_{R.roles[role_index]}_purchased_encapsulated_magnet")


def screw_witness(role_index: int, seam_index: int):
    z0,z1 = R.carrier_z_mm[role_index]
    angle = R.seam_angles_deg[seam_index]
    shape = tangential_cylinder(angle,H.screw_axis_radius_mm,H.screw_diameter_mm,-6,12,(z0+z1)/2)
    return _one(shape,f"{NAMESPACE}_{R.roles[role_index]}_seam_{seam_index+1}_purchased_M3x12")


def assembled_shape():
    children=[]
    for child in b3.assembled_shape().children:
        if "nonprint_ring_witness" not in child.label:
            children.append(deepcopy(child))
    for role in range(3):
        children.extend(segment_shape(role,segment) for segment in range(3))
        children.append(magnet_witness(role))
        children.extend(screw_witness(role,seam) for seam in range(3))
    return Compound(children=children,label=f"{NAMESPACE}_assembled")


def exploded_assembly_order_shape():
    children=[]
    for child in b3.assembled_shape().children:
        if "nonprint_ring_witness" not in child.label:
            children.append(deepcopy(child).moved(Location((0,0,-25))))
    for role in range(3):
        for segment in range(3):
            dx,dy=polar(30+120*segment,18+8*role)
            shape=segment_shape(role,segment).moved(Location((dx,dy,30+role*18+segment*4)))
            shape.label=f"{NAMESPACE}_step_0{segment+1}_{R.roles[role]}_segment_{R.segment_names[segment]}"
            children.append(shape)
        magnet=magnet_witness(role).moved(Location((0,0,52+role*18)))
        magnet.label=f"{NAMESPACE}_step_04_{R.roles[role]}_print_pause_insert_magnet_then_seal"
        children.append(magnet)
        for seam in range(3):
            screw=screw_witness(role,seam).moved(Location((0,0,60+role*18+seam*3)))
            screw.label=f"{NAMESPACE}_step_05_{R.roles[role]}_join_seam_{seam+1}_M3x12"
            children.append(screw)
    return Compound(children=children,label=f"{NAMESPACE}_exploded_exact_assembly_order")


def printable_occurrences() -> tuple[dict[str,object],...]:
    rows=[]
    for role in range(3):
        for segment in range(3):
            shape=deepcopy(segment_shape(role,segment))
            shape=shape.moved(Location((0,0,-shape.bounding_box().min.Z)))
            label=f"{NAMESPACE}_{R.roles[role]}_segment_{R.segment_names[segment]}_print_orientation"
            shape.label=label
            rows.append({"name":f"{R.roles[role]}_{R.segment_names[segment]}","label":label,"shape":shape})
    return tuple(rows)
