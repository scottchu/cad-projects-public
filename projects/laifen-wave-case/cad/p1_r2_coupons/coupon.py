"""Original CDE-01 short-cap experiment, millimetres, assembly +Z screw axis.

Authoritative functional source. Helix sweeps have an oblique meridian profile
and a Frenet frame: helix's constant torsion rotates that profile about +Z.
Actual radial sections are checked rather than assuming sweep-frame fidelity.
"""
from functools import lru_cache
from math import cos, sin, pi, sqrt

from build123d import (
    Axis, Color, Compound, CylindricalJoint, Face, Helix, Location, Plane,
    RigidJoint, Shell, Solid, Vector, Wire, revolve, sweep,
)

PITCH = 2.0
CLEARANCES = (0.20, 0.25, 0.30)
ROOT, CREST, BORE = 16.8, 17.4, 15.0
COLLAR_R, SHELL_R, MAIN_BORE_R = 19.5, 17.9, 15.5
CAP_HEIGHT, FLOOR_Z, NECK_HEIGHT = 25.0, 22.0, 9.0
FULL_START, FULL_END = 2.0, 8.0
PROFILE_TOLERANCE = 0.01
EMBED = 0.05
CLIP_OVERBUILD = 0.10  # Tool-only ceiling; the infinite thread bounds radius17.4.
GRIP_COUNT, GRIP_PITCH, GRIP_HEIGHT = 31, 2.8, 0.6
GRIP_Z0, GRIP_FLAT = 15.8, 1.0
ALPHA = pi / GRIP_COUNT
A, B = SHELL_R * sin(ALPHA), GRIP_PITCH / 2
K = GRIP_FLAT * sqrt(A*A+B*B) / (2*A*B)
XB = SHELL_R*cos(ALPHA)-0.01
XT = sqrt((SHELL_R+GRIP_HEIGHT)**2-(K*A)**2)


def check_clearance(c):
    if c not in CLEARANCES:
        raise ValueError(f"CDE-01 permits only {CLEARANCES}; received {c}")
    return c


def infinite_radius(theta, z, c=0.0):
    q = (z-PITCH*theta/(2*pi)+PITCH/2) % PITCH-PITCH/2
    a = abs(q)
    return ROOT+c+max(0.0, min(0.6, (0.85-a)*6/7))


def male_radius(theta, z):
    envelope = 0 if z <= 1 else min(0.6, 0.6*(z-1), 0.6*(9-z))
    return min(infinite_radius(theta, z), ROOT+envelope)


def female_radius(theta, z, c):
    check_clearance(c)
    envelope = 0.6 if z <= 1 else max(0.0, 0.6*(2-z), 0.6*(z-8))
    return max(infinite_radius(theta, z, c), ROOT+c+envelope)


def polygon(points):
    return Wire.make_polygon([Vector(*p) for p in points], close=True)


def turned(rz):
    """Revolve an exact linear meridian polygon, no faceted circumference."""
    return revolve(Face(polygon([(r, 0, z) for r,z in rz])), axis=Axis.Z)


def one_shape(result):
    """build123d 0.11 intersections return ShapeList even for one solid."""
    if isinstance(result, list):
        if len(result) != 1:
            raise ValueError(f"Expected one connected shape, received {len(result)}")
        return result[0]
    return result


@lru_cache(maxsize=4)
def infinite_thread(c=0.0):
    """Overbuilt original thread tool, -2..12 plus profile half-width."""
    root = ROOT+c
    z0 = -2.0
    half_base = 0.85+EMBED/(6/7)
    wire = polygon([(root-EMBED,0,z0-half_base),
                    (CREST+c,0,z0-0.15), (CREST+c,0,z0+0.15),
                    (root-EMBED,0,z0+half_base)])
    path = Helix(PITCH, 14.0, root, center=(0,0,z0), lefthand=False)
    ridge = sweep(Face(wire), path=path, is_frenet=True)
    core = turned([(0,-3),(root,-3),(root,13),(0,13)])
    return core.fuse(ridge).clean()


def add_datums(part, cap=False):
    """Part-local named interface/inspection frames, never export-only shifts."""
    datums = {"shoulder": 0.0, "tip": 9.0, "full_thread_start": 2.0,
              "full_thread_end": 8.0, "bed": 25.0 if cap else -8.0,
              "grip_phase": 15.8 if cap else 0.0}
    if cap:
        datums["inner_floor"] = 22.0
    for name,z in datums.items():
        RigidJoint(name, part, Location((0,0,z)))
    CylindricalJoint("screw_axis", part, Axis.Z,
                     linear_range=(-0.1,11), angular_range=(-4,2000))
    return part


@lru_cache(maxsize=1)
def male():
    # Bed chamfers are constructed in this section, leaving 1.8 mm bed land.
    base = turned([(15.3,-8),(17.1,-8),(17.4,-7.7),(17.4,-4.1),
                   (19.5,-2),(19.5,0),(15,0),(15,-7.7)])
    # Move the redundant crest ceiling off the thread's coincident cylinder.
    # Extend both 0.6 slopes, preserving min(thread, envelope) exactly.
    envelope = turned([(15,0),(16.8,0),(16.8,1),
                       (CREST+CLIP_OVERBUILD,2+CLIP_OVERBUILD/0.6),
                       (CREST+CLIP_OVERBUILD,8-CLIP_OVERBUILD/0.6),
                       (16.8,9),(15,9)])
    neck = one_shape(infinite_thread().intersect(envelope))
    part = base.fuse(neck).clean()
    part.label = "M common male open ring; pitch2 right-hand; 6mm full form"
    part.color = Color(0.35,0.57,0.73)
    return add_datums(part)


def grip_cell():
    base = [(XB,0,-B),(XB,A,0),(XB,0,B),(XB,-A,0)]
    tip = [(XT,0,-K*B),(XT,K*A,0),(XT,0,K*B),(XT,-K*A,0)]
    # Exact planar polygons retain all eight frozen vertices and outward normals.
    faces = [Face(polygon(list(reversed(base)))), Face(polygon(tip))]
    faces += [Face(polygon([base[i],base[(i+1)%4],tip[(i+1)%4],tip[i]]))
              for i in range(4)]
    return Solid(Shell(faces))


def grip_cells():
    cell = grip_cell()
    return [cell.moved(Location((0,0,GRIP_Z0+j*GRIP_PITCH),
                                 (0,0,i*360/GRIP_COUNT+(j%2)*180/GRIP_COUNT)))
            for j in range(2) for i in range(GRIP_COUNT)]


def label_solids(c):
    # Original seven-segment glyphs: 0.6 mm strokes, 3.8 mm high, 0.2 relief.
    segments = {"a":(0,3.2,2.2,.6), "g":(0,1.6,2.2,.6),
                "d":(0,0,2.2,.6), "f":(0,1.9,.6,1.6),
                "b":(1.6,1.9,.6,1.6), "e":(0,.3,.6,1.6),
                "c":(1.6,.3,.6,1.6)}
    glyphs = {"0":"abcdef", "2":"abged", "3":"abgcd", "5":"afgcd"}
    result = []
    for index,char in enumerate(f"{round(c*100):02}"):
        for seg in glyphs[char]:
            x,y,w,h = segments[seg]
            x += index*3.0-2.6
            y -= 1.9
            result.append(Solid.extrude(Face(polygon([(x,y,21.8),(x+w,y,21.8),
                                      (x+w,y+h,21.8),(x,y+h,21.8)])),(0,0,.21)))
    return result


@lru_cache(maxsize=3)
def cap(c=0.25):
    check_clearance(c)
    outer = turned([(0,0),(19.5,0),(19.5,10.2),(17.9,12.4),
                    (17.9,24.7),(17.6,25),(0,25)])
    threaded_void = one_shape(infinite_thread(c).intersect(
        turned([(0,0),(18,0),(18,9),(0,9)])))
    relief = turned([(0,-.1),(17.4+c,-.1),(17.4+c,1),(16.8+c,2),
                     (16.8+c,8),(17.4+c,9),(17.4+c,10.2),
                     (15.5,12.4),(15.5,22),(0,22)])
    body = outer.cut(threaded_void.fuse(relief)).clean()
    part = body.fuse(*grip_cells(), *label_solids(c)).clean()
    part.label = f"C{round(c*100):02} closed grip cap; radial clearance {c:.2f}"
    part.color = Color({.20:"#da9773",.25:"#77b09a",.30:"#b291c8"}[c])
    return add_datums(part, cap=True)


def screw_pose(c, beta_degrees=0.0, gap=None):
    """Male fixed, cap cylindrical joint coupled at 2 mm per revolution."""
    fixed = male().moved(Location())
    moving = cap(c).moved(Location())
    g = PITCH*beta_degrees/360 if gap is None else gap
    fixed.joints["screw_axis"].connect_to(moving.joints["shoulder"],
                                        position=g, angle=beta_degrees)
    return Compound(label=f"C{round(c*100)} M screw pose beta{beta_degrees:g} gap{g:g}",
                    children=[fixed,moving])


def print_part(role):
    if role == "M":
        return male().moved(Location((0,0,8)))
    return cap(int(role)/100).moved(Location((0,0,25),(180,0,0)))


def print_layout():
    children=[]
    for role,xy in zip(("M","20","25","30"),((-23,-23),(23,-23),(-23,23),(23,23))):
        children.append(print_part(role).moved(Location((*xy,0))))
    return Compound(label="Four-part original thread grip coupon print layout",children=children)


def exploded():
    return screw_pose(.25,1620,gap=11)
