"""build123d geometry for V0R1 compact representative quartz fixture."""

from __future__ import annotations

from build123d import Align, Axis, Box, Compound, Cone, Cylinder, Location, Sphere

from v0r1_compact_quartz_fixture_spec import CarrierSpec, CompactFixtureSpec, V0R1


def _cylinder(radius,height,z0=0): return Cylinder(radius,height,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,0,z0)))


def make_fake_standard_quartz_body(spec=V0R1):
    body=Box(spec.body_x,spec.body_y,spec.body_depth,align=(Align.CENTER,Align.CENTER,Align.MIN))
    body=body.fillet(spec.body_corner_radius,body.edges().filter_by(Axis.Z))
    o=.02; offset=spec.body_depth
    arbor=_cylinder(6,(5.883333333)+o,offset-o)
    arbor=arbor.fuse(_cylinder(4,1.2+2*o,offset+5.883333333-o))
    arbor=arbor.fuse(_cylinder(3,3.958333334+2*o,offset+7.083333333-o))
    arbor=arbor.fuse(_cylinder(2,5.758333333+o,offset+11.041666667-o))
    arbor=arbor.fuse(Cone(2,1.7,.4+o,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,0,offset+16.8-o))))
    result=body.fuse(arbor); result.label="fake_standard_quartz_body_representative_aa_envelope"
    return result


def _ring(carrier,spec):
    return _cylinder(carrier.radius+spec.ring_radial_width/2,spec.ring_axial_thickness).cut(_cylinder(carrier.radius-spec.ring_radial_width/2,spec.ring_axial_thickness+.4,-.2))


def _spokes(carrier,hub_radius,spec):
    length=carrier.radius+spec.ring_radial_width/2-hub_radius+.05; center=hub_radius-.1+length/2; result=None
    for angle in (0,120,240):
        spoke=Box(length,spec.spoke_tangential_width,spec.ring_axial_thickness,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((center,0,0))).rotate(Axis.Z,angle)
        result=spoke if result is None else result.fuse(spoke)
    return result


def _fin(carrier,spec):
    root=spec.ring_axial_thickness-spec.fin_root_overlap; straight=carrier.local_height-root-spec.fin_tip_radius
    stem=Box(spec.fin_radial_thickness,spec.fin_tangential_width,straight,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((carrier.radius,0,root)))
    cap=Sphere(spec.fin_tip_radius).moved(Location((carrier.radius,0,root+straight)))
    return stem.fuse(cap)


def _lower_hub(carrier):
    hub=_cylinder(carrier.hub_od/2,carrier.hub_height).fuse(_cylinder(carrier.tower_od/2,carrier.tower_height))
    return hub.cut(_cylinder(carrier.bore_diameter/2,carrier.tower_height+.4,-.2))


def _hour_hub(carrier,spec):
    hub=_cylinder(carrier.hub_od/2,carrier.hub_height).cut(_cylinder(spec.hour_bore_diameter/2,carrier.hub_height+.4,-.2))
    pad_r=spec.hour_pad_radial_protrusion+.30; pad_c=spec.hour_bore_diameter/2-spec.hour_pad_radial_protrusion/2+.15
    for angle in (0,120,240):
        pad=Box(pad_r,spec.hour_pad_tangential_width,carrier.hub_height,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((pad_c,0,0))).rotate(Axis.Z,angle)
        hub=hub.fuse(pad)
    slit_l=carrier.hub_od/2-spec.hour_bore_diameter/2+1
    slit=Box(slit_l,spec.hour_slit_width,carrier.hub_height+.4,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((-(spec.hour_bore_diameter/2+slit_l/2-.3),0,-.2)))
    return hub.cut(slit)


def make_carrier_hand(carrier,spec=V0R1):
    hub=_hour_hub(carrier,spec) if carrier.name=="hour" else _lower_hub(carrier)
    result=hub.fuse(_ring(carrier,spec)).fuse(_spokes(carrier,carrier.hub_od/2,spec)).fuse(_fin(carrier,spec))
    result.label=f"{carrier.name}_carrier_hand_upright_fin"; return result


def make_hour_carrier_hand(spec=V0R1): return make_carrier_hand(spec.by_name["hour"],spec)
def make_minute_carrier_hand(spec=V0R1): return make_carrier_hand(spec.by_name["minute"],spec)
def make_second_carrier_hand(spec=V0R1): return make_carrier_hand(spec.by_name["second"],spec)


PART_FACTORIES=(("fake_standard_quartz_body",make_fake_standard_quartz_body),("hour_carrier_hand",make_hour_carrier_hand),("minute_carrier_hand",make_minute_carrier_hand),("second_carrier_hand",make_second_carrier_hand))
def part_factories(): return PART_FACTORIES


def placed_body(spec=V0R1): return make_fake_standard_quartz_body(spec).moved(Location((0,0,-spec.body_depth)))
def placed_carrier(name,angle=0,spec=V0R1):
    c=spec.by_name[name]; return make_carrier_hand(c,spec).rotate(Axis.Z,angle).moved(Location((0,0,c.ring_bottom_z)))


ANGLES={"second":300,"minute":20,"hour":225}
def make_assembly(spec=V0R1): return Compound(children=[placed_body(spec),*(placed_carrier(n,ANGLES[n],spec) for n in ("second","minute","hour"))],label="v0r1_compact_four_part_fixture")
def make_exploded_assembly(spec=V0R1):
    children=[placed_body(spec)]
    for i,n in enumerate(("second","minute","hour"),1): children.append(placed_carrier(n,ANGLES[n],spec).moved(Location((0,0,6*i))))
    return Compound(children=children,label="v0r1_compact_four_part_fixture_exploded")
