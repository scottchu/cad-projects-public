// Phase 1 stub — frame / standoff sandwich footprint (expand with real carbon + cheek geometry).
// No frame-specific dimensions are asserted as spec; tune from measurements (see v3 README).

include <BOSL2/std.scad>

/* [Part] */
part = "preview"; // ["preview", "stub_holes"]

/* [Standoff pattern — placeholders] */
standoff_spacing = 30;   // [10:1:60]  center-to-center between rear standoffs (example)
standoff_hole_d  = 2.2;  // [1.5:0.1:3] clearance hole for M2 (~2mm) + print margin
shell_width      = 40;   // [20:1:80]   footprint width (X)
shell_length       = 24;  // [12:1:60]   footprint length (Y)
shell_thickness    = 2.5; // [1:0.5:6]  slab thickness (Z)

$fn = $preview ? 24 : 48;

module Frame_Shell_Stub(
    standoff_spacing = standoff_spacing,
    standoff_hole_d  = standoff_hole_d,
    shell_width      = shell_width,
    shell_length     = shell_length,
    shell_thickness  = shell_thickness
) {
    assert(standoff_spacing > standoff_hole_d, "standoff_spacing must exceed hole diameter");
    assert(shell_width > standoff_spacing + standoff_hole_d, "shell too narrow for standoff pattern");

    difference() {
        cuboid([shell_width, shell_length, shell_thickness], anchor = BOTTOM);

        for (sx = [-1, 1])
            translate([sx * standoff_spacing / 2, 0, -0.01])
                cylinder(d = standoff_hole_d, h = shell_thickness + 0.02, anchor = BOTTOM);
    }
}

if (part == "preview" || part == "stub_holes") {
    Frame_Shell_Stub();
}
