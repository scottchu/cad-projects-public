include <BOSL2/std.scad>
// ./ — resolve next to this file (plain <spec.scad> only hits library paths on some setups)
include <./spec.scad>

// Dual-SMA plate: each boss aims along its own axis (antennas in different directions).
//
// All aim angles are user preference — left/right azimuth & elevation, collective_pitch_x,
// and mount_rot for your frame, vtx, and coverage. Customizer values are examples, not a spec.
//
// Axis convention (before mount_rot):
//   - Azimuth 0° = +X, 90° = +Y (in XY, measured from +X)
//   - Elevation 0° = horizontal (in XY), 90° = +Z
//   - Unit axis = (cos(el)cos(az), cos(el)sin(az), sin(el))
//
// Bosses sit on ±X (left at -X, right at +X). For a diverging “V” (antennas open outward,
// not crossing in front of the mount), aim left roughly toward -X and right toward +X:
//
//       \.     ./
//        \   /
//         \ /
//          o o     ← left boss (-X)    right boss (+X)
//
// Defaults below: el 45°, left az 180° (-X), right az 0° (+X) → symmetric outward + up,
// 90° between axes. Using az 90° / 270° instead points both toward ±Y and makes axes
// converge / cross between the bosses — opposite of this sketch.
//
// Boss geometry: hole + hex along local +Z, then rot(from=UP, to=axis).
//
// collective_pitch_x: rotate the whole dual-boss assembly around +X after per-boss aim (both
// SMAs tilt together). If the lean aims the wrong way in your view, negate the value.
//
// mount_rot: optional whole-part [x,y,z] in world space (frame / deck alignment).
// Transform chain (sma_plate_pose): collective_pitch_x → spacing_yaw → mount_rot on children.
//
// Planar trim (optional): removes everything with world Z < trim_below_z after mount_rot.
// Use this for a deliberate flat bed / frame face instead of hoping the hull ends at a plane.
// spacing_yaw: rotates the boss pair around world +Z (moves ±X line onto any horizontal bearing).
//
// Preview vs print: F5 (preview) uses OpenCSG and may draw the plate as a solid slab without
// showing holes/hex cuts. F6 (render) and STL export use CGAL — that mesh matches what you
// slice. If preview looks wrong, hit F6 or export STL and check there.
//
// --- Insertion vs reference quad deck ---
// Aim vector +Z_local = toward the antenna (outward). With SMA_PLATE_HEX_RECESS_TOWARD_ANTENNA
// (spec.scad), the hex pocket is on that outward face and you insert the bulkhead from the
// opposite side (-aim) — frame interior / “back” — matching a slanted rear plate with brass
// nuts visible outside.
//
// You still may not see two round holes on one global plane: each bore is along its own axis,
// so “back” is *along -aim*, not necessarily world -Z. Use part=preview_guides for bore ghosts.
// part=test = vertical bosses, same hex rule, easy flat fit check.

/* [Part Selection] */
part = "preview"; // ["preview", "preview_stl", "preview_guides", "test"]

/* [Plate Parameters] */
thickness = 2;       // [1:0.5:5]   Bridge thickness between bosses
distance  = 12;      // [6:1:30]    Center-to-center SMA spacing
margin    = 1;       // [1:0.5:5]   Extra plate material beyond boss edge

/* [SMA aim — your preference; left boss at -X, right at +X]
   Azimuth: XY angle from +X toward +Y. Elevation: angle above horizontal (0 = in XY, 90 = up). */
left_azimuth    = 180;  // [0:5:360]   outward along -X when boss is on -X (diverging V)
left_elevation  = 45;   // [0:5:90]    tune freely
right_azimuth   = 0;    // [0:5:360]   outward along +X when boss is on +X
right_elevation = 45;   // [0:5:90]

/* [Collective tilt — both SMAs together, around +X, after aim, before mount_rot] */
collective_pitch_x = 45;  // [-90:5:90] e.g. 45 leans the pair “forward”; negate if backward

/* [Whole-part tilt — your preference; applied last, world XYZ degrees] */
mount_rot = [0, 0, 0];  // [0:5:360] each — e.g. pitch whole mount to match frame deck

/* [Layout — boss line in horizontal plane; default ±X] */
spacing_yaw = 0;  // [0:5:360] rotate pair around +Z (e.g. 90 puts bosses on ±Y)

/* [World Z trim — flat cut after mount_rot (printer bed = XY at Z=0)] */
trim_below_z_enable = false;  // true: chop everything below trim_below_z (world mm)
trim_below_z        = 0;      // e.g. 0 = remove z < 0 for a flat bottom on the bed

/* [Boss Parameters (passed through)] */
boss_wall   = 2.5;   // [1.5:0.5:5]
boss_height = 3;     // [2:0.5:8]

// true: hex on +aim (outward deck, nut visible); insert bulkhead from -aim (frame back).
// false: hex at boss root (-aim). Default from spec.scad SMA_PLATE_HEX_RECESS_TOWARD_ANTENNA.
hex_on_antenna_side = SMA_PLATE_HEX_RECESS_TOWARD_ANTENNA;

/* [Reference STL — sma-connector.stl, bbox normalized to min @ origin] */
reference_stl_anchor  = [4.619, 24.2, 4];
reference_stl_rotate  = [90, 0, 0];

$fn = $preview ? 36 : 72;

EPSILON = 0.01;

// Half-space subtract: all points with z < z0 (huge XY extent for boolean stability)
module trim_half_space_below_z(z0) {
    translate([-2000, -2000, -2000])
        cube([4000, 4000, 2000 + z0 + EPSILON]);
}

// Unit aim vector: azimuth in XY from +X toward +Y; elevation 0 = horizontal, 90 = +Z.
// OpenSCAD trig uses degrees. ||v|| = 1.
function sma_axis_from_azimuth_elevation(az_deg, el_deg) =
    let(ch = cos(el_deg))
    [
        ch * cos(az_deg),
        ch * sin(az_deg),
        sin(el_deg)
    ];

function boss_axis_for_sign(sign) =
    sign < 0
        ? sma_axis_from_azimuth_elevation(left_azimuth, left_elevation)
        : sma_axis_from_azimuth_elevation(right_azimuth, right_elevation);

// Child coords: after aim (per-boss), then collective_pitch_x, spacing_yaw, mount_rot (world).
// Vertex order: inner rotate applies first to geometry — collective → yaw → mount_rot.
module sma_plate_pose(mount_rot, spacing_yaw, collective_pitch_x) {
    rotate(mount_rot)
        rotate([0, 0, spacing_yaw])
            rotate([collective_pitch_x, 0, 0])
                children();
}

// Translucent bore ghosts only (% = not in STL). Same pose as SMA_Plate body.
module insertion_bore_guides(
    distance,
    total_h,
    mount_rot,
    spacing_yaw,
    collective_pitch_x,
    trim_below_z_enable,
    trim_below_z
) {
    difference() {
        sma_plate_pose(mount_rot, spacing_yaw, collective_pitch_x)
            for (sign = [-1, 1]) {
                ax = boss_axis_for_sign(sign);
                translate([sign * distance / 2, 0, -EPSILON])
                    rot(from = UP, to = ax, a = 0)
                        %cylinder(d = SMA_HOLE_D + 0.3, h = total_h + 4, anchor = BOTTOM);
            }

        if (trim_below_z_enable)
            trim_half_space_below_z(trim_below_z);
    }
}

module SMA_Plate(
    thickness             = thickness,
    distance              = distance,
    margin                = margin,
    left_azimuth          = left_azimuth,
    left_elevation        = left_elevation,
    right_azimuth         = right_azimuth,
    right_elevation       = right_elevation,
    collective_pitch_x    = collective_pitch_x,
    mount_rot             = mount_rot,
    spacing_yaw           = spacing_yaw,
    trim_below_z_enable   = trim_below_z_enable,
    trim_below_z          = trim_below_z,
    boss_wall             = boss_wall,
    boss_height           = boss_height,
    hex_on_antenna_side   = hex_on_antenna_side
) {
    boss_outer_d = SMA_HOLE_D + 2 * boss_wall;
    plate_r = boss_outer_d / 2 + margin;
    total_h = thickness + boss_height;

    assert(distance > 0, "distance must be positive");
    assert(thickness > 0, "thickness must be positive");
    assert(margin >= 0, "margin must be non-negative");
    assert(boss_height > SMA_HEX_NUT_DEPTH, "boss_height must exceed hex recess depth");
    assert(boss_outer_d > SMA_HEX_D, "boss OD must exceed hex pocket flat-to-flat");
    assert(
        !hex_on_antenna_side || SMA_HEX_NUT_DEPTH + 2 * EPSILON <= total_h + EPSILON,
        "total_h too small for hex pocket on antenna side"
    );

    module _boss_at(sign) {
        ax = boss_axis_for_sign(sign);
        translate([sign * distance / 2, 0, 0])
            rot(from = UP, to = ax, a = 0) {
                cylinder(r = plate_r, h = total_h, anchor = BOTTOM);
            }
    }

    module _cuts_at(sign) {
        ax = boss_axis_for_sign(sign);
        hex_z = hex_on_antenna_side
            ? (total_h - SMA_HEX_NUT_DEPTH - 2 * EPSILON)
            : (-EPSILON);
        translate([sign * distance / 2, 0, -EPSILON])
            rot(from = UP, to = ax, a = 0) {
                cylinder(d = SMA_HOLE_D, h = total_h + 2 * EPSILON, anchor = BOTTOM);

                translate([0, 0, hex_z])
                    linear_extrude(height = SMA_HEX_NUT_DEPTH + 2 * EPSILON)
                        hexagon(id = SMA_HEX_D);
            }
    }

    difference() {
        sma_plate_pose(mount_rot, spacing_yaw, collective_pitch_x)
            // convexity helps F5 preview show subtracted SMA holes + hex pockets (still verify with F6/STL)
            difference(convexity = 10) {
                union() {
                    hull()
                        for (sign = [-1, 1])
                            translate([sign * distance / 2, 0, 0])
                                rot(from = UP, to = boss_axis_for_sign(sign), a = 0)
                                    cylinder(r = plate_r, h = thickness, anchor = BOTTOM);

                    for (sign = [-1, 1])
                        _boss_at(sign);
                }

                for (sign = [-1, 1])
                    _cuts_at(sign);
            }

        if (trim_below_z_enable)
            trim_half_space_below_z(trim_below_z);
    }
}

module Reference_Connector_STL(
    anchor = reference_stl_anchor,
    rot    = reference_stl_rotate
) {
    rotate(rot)
        translate(-anchor)
            import("sma-connector.stl", convexity = 10);
}

module SMA_Plate_With_Reference_STL(
    thickness             = thickness,
    distance              = distance,
    margin                = margin,
    left_azimuth          = left_azimuth,
    left_elevation        = left_elevation,
    right_azimuth         = right_azimuth,
    right_elevation       = right_elevation,
    collective_pitch_x    = collective_pitch_x,
    mount_rot             = mount_rot,
    spacing_yaw           = spacing_yaw,
    trim_below_z_enable   = trim_below_z_enable,
    trim_below_z          = trim_below_z,
    boss_wall             = boss_wall,
    boss_height           = boss_height,
    hex_on_antenna_side   = hex_on_antenna_side
) {
    SMA_Plate(
        thickness             = thickness,
        distance              = distance,
        margin                = margin,
        left_azimuth          = left_azimuth,
        left_elevation        = left_elevation,
        right_azimuth         = right_azimuth,
        right_elevation       = right_elevation,
        collective_pitch_x    = collective_pitch_x,
        mount_rot             = mount_rot,
        spacing_yaw           = spacing_yaw,
        trim_below_z_enable   = trim_below_z_enable,
        trim_below_z          = trim_below_z,
        boss_wall             = boss_wall,
        boss_height           = boss_height,
        hex_on_antenna_side   = hex_on_antenna_side
    );

    _total_h = thickness + boss_height;

    // rotate(mount_rot)
    //     rotate([collective_pitch_x, 0, 0])
    //         for (sign = [-1, 1])
    //             translate([sign * distance / 2, 0, 0])
    //                 rot(from = UP, to = boss_axis_for_sign(sign), a = 0)
    //                     translate([0, 0, -(_total_h - SMA_HEX_NUT_DEPTH)])
    //                         % Reference_Connector_STL();
}

if (part == "preview") {
    SMA_Plate_With_Reference_STL();

} else if (part == "preview_stl") {
    SMA_Plate_With_Reference_STL();

} else if (part == "preview_guides") {
    union() {
        SMA_Plate_With_Reference_STL();
        insertion_bore_guides(
            distance              = distance,
            total_h               = thickness + boss_height,
            mount_rot             = mount_rot,
            spacing_yaw           = spacing_yaw,
            collective_pitch_x    = collective_pitch_x,
            trim_below_z_enable   = trim_below_z_enable,
            trim_below_z          = trim_below_z
        );
    }

} else if (part == "test") {
    // Flat mount: both bores along +Z — two round holes from one flat face (SMA / hex fit test).
    // Not the same aim as angled preview; use for calipers + plug test before trusting angles.
    SMA_Plate(
        left_azimuth       = 90,
        left_elevation     = 90,
        right_azimuth      = 90,
        right_elevation    = 90,
        collective_pitch_x = 0,
        mount_rot          = [0, 0, 0]
    );
}
