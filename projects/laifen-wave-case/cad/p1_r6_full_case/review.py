"""Nonfabrication review helpers; reference device never enters primary targets."""
from build123d import Color,Compound,Location,Plane,RigidJoint,Solid
from .params import Params,derive,require


def device_readouts(p=Params(),placement='centered'):
    d=derive(p);require(placement in ('centered','bottom-resting'),'unknown reference placement')
    bottom_gap=p.axial_allowance/2 if placement=='centered' else 0.
    z0=-d.body_depth+bottom_gap;z1=z0+p.device_length
    return dict(units='mm',device_length=p.device_length,device_diameter=p.device_diameter,
                placement=placement,reference_only=True,retained=False,
                warning='Approximate installed-device envelope; nominal placement, not retention',
                cavity_length=p.cavity_length,outside_length=d.outer_length,
                body_cavity=d.body_depth+d.neck_height,cap_cavity=p.cap_cavity_length,
                overlap=d.neck_height,full_form_engagement=p.engagement,
                inner_floor_body=-d.body_depth,inner_floor_cap=p.cap_cavity_length,
                device_lower_z=z0,device_upper_z=z1,bottom_gap=bottom_gap,
                top_gap=p.cap_cavity_length-z1,body_radial_gap=d.body_radial_gap,
                cap_radial_gap=d.cap_radial_gap)


def device_envelope(p=Params(),placement='centered'):
    r=device_readouts(p,placement)
    device=Solid.make_cylinder(p.device_diameter/2,p.device_length,
                              Plane(origin=(0,0,r['device_lower_z'])))
    device.label='REFERENCE ONLY: approximate installed device envelope; not a print object; unretained'
    device.color=Color('#e9b54d')
    for name,z in [('device_lower',r['device_lower_z']),('device_upper',r['device_upper_z'])]:
        RigidJoint(name,device,Location((0,0,z)))
    return device


def section_review(p=Params(),placement='centered',case_parts=None):
    """Actual half-case solids with reference cylinder; readouts supply annotations.

    Optional case_parts allows the critic to pass exact written STEP solids.
    This diagnostic is intentionally not a fifth primary STEP wrapper.
    """
    if case_parts is None:
        from .parts import build_body,build_cap
        case_parts=(build_body(p),build_cap(p))
    require(len(case_parts)==2,'section requires exactly body and cap')
    d=derive(p);r=d.outer_crest_radius+1
    keep=Solid.make_box(2*r,r,d.outer_length+2,
                        Plane(origin=(-r,0,d.body_band[0]-1)))
    sections=[]
    for name,part in zip(('body','cap'),case_parts):
        cut=part.intersect(keep);cut.label=f'REVIEW SECTION ONLY: actual {name}'
        sections.append(cut)
    return Compound(label=f'NONFABRICATION SECTION: nominal {placement} device; no retention',
                    children=[*sections,device_envelope(p,placement)])
