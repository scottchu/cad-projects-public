include <BOSL2/std.scad>

// Standoff holder for drone frame attachment.
// Hollow cylinder that clips around a frame standoff post.
//
// Designed for TPU: slightly snug bore so the flexible material
// grips the standoff naturally without needing fasteners.
//
// Oriented with standoff axis in +Z:
//   - Bottom (Z=0): sits on the frame
//   - Standoff post slides into the bore from above

/* [Part Selection] */
part = "preview"; // ["preview", "test"]

/* [Standoff Parameters] */
diameter = 4.5;    // [3:0.5:8]   Frame standoff post diameter
wall     = 2.5;    // [1.5:0.5:5] Wall thickness (thicker for TPU rigidity)
height   = 10;     // [5:1:20]    Holder height

/* [Pair Parameters] */
distance = 14.5;   // [8:0.5:25]  Center-to-center standoff spacing

/* [TPU Tuning] */
bore_clearance = -0.2;  // [-0.5:0.1:0.5] Negative = tighter (TPU grip)

$fn = $preview ? 36 : 72;

EPSILON = 0.01;

module Standoff_Holder(
    diameter       = diameter,
    wall           = wall,
    height         = height,
    bore_clearance = bore_clearance
) {
    outer_d = diameter + 2 * wall;
    bore_d  = diameter + bore_clearance;

    assert(bore_d > 0, str("Bore diameter (", bore_d, ") must be positive"));
    assert(outer_d > bore_d, str("Outer (", outer_d, ") must exceed bore (", bore_d, ")"));

    difference() {
        cylinder(d = outer_d, h = height, anchor = BOTTOM);

        translate([0, 0, -EPSILON])
            cylinder(d = bore_d, h = height + 2 * EPSILON, anchor = BOTTOM);
    }
}

module Standoff_Pair(
    diameter       = diameter,
    wall           = wall,
    height         = height,
    distance       = distance,
    bore_clearance = bore_clearance
) {
    assert(distance > 0, "Distance between standoffs must be positive");

    for (sign = [-1, 1])
        translate([sign * distance / 2, 0, 0])
            Standoff_Holder(
                diameter       = diameter,
                wall           = wall,
                height         = height,
                bore_clearance = bore_clearance
            );
}

if (part == "preview") {
    Standoff_Pair();

} else if (part == "test") {
    // Test print: single holder for verifying standoff fit in TPU.
    // Print this (~3min), slide it onto a frame standoff post.
    // If too tight, increase bore_clearance toward 0.
    // If too loose, decrease bore_clearance toward -0.5.
    Standoff_Holder();
}
