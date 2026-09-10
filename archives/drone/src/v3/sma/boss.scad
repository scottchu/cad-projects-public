include <BOSL2/std.scad>
include <./spec.scad>

// Single SMA mounting boss: raised cylinder with SMA through-hole
// and hex counterbore on the entry face (Z=0) for bulkhead flange / nut.
//
// Oriented with boss rising in +Z:
//   - Bottom (Z=0): connector enters; hex recess opens here
//   - Top: flat (no counterbore)

/* [Part Selection] */
part = "preview"; // ["preview", "test"]

/* [Boss Parameters] */
wall   = 2.5;  // [1.5:0.5:5] Wall thickness around SMA hole (thicker for TPU)
height = 3;    // [2:0.5:8]   Boss total height

$fn = $preview ? 36 : 72;

module SMA_Boss(
    wall   = wall,
    height = height
) {
    outer_d = SMA_HOLE_D + 2 * wall;

    assert(height > SMA_HEX_NUT_DEPTH,
        str("Boss height (", height, ") must exceed hex recess depth (", SMA_HEX_NUT_DEPTH, ")"));
    assert(outer_d > SMA_HEX_D,
        str("Boss OD (", outer_d, ") must exceed hex recess size (", SMA_HEX_D, ")"));

    difference() {
        // Outer boss cylinder
        cylinder(d = outer_d, h = height, anchor = BOTTOM);

        // SMA through-hole
        translate([0, 0, -0.01]) {
            cylinder(d = SMA_HOLE_D, h = height + 0.02, anchor = BOTTOM);
        }

        // Hex counterbore on bottom (entry) face
        // BOSL2: hexagon(d=) is outside diameter at *vertices* (corner–corner), not across flats.
        // Nut wrench size is across flats → use id = inside diameter at mid-side = flat-to-flat.
        translate([0, 0, -0.01])
            linear_extrude(height = SMA_HEX_NUT_DEPTH + 0.01)
                hexagon(id = SMA_HEX_D);
    }
}

if (part == "preview") {
    SMA_Boss();

} else if (part == "test") {
    // Test print: single boss for verifying SMA + hex fit in TPU.
    // Insert connector from below; hex flange should seat in the bottom recess.
    // Adjust SMA_TPU_HOLE_CLEARANCE and SMA_TPU_HEX_CLEARANCE in
    // spec.scad based on results.
    SMA_Boss();
}
