// Phase 4 stub — optional GPS cradle / pocket as a subtractive module for tail integration.
// Dimensions are placeholders until a module + mount style are locked (capability gap otherwise).

include <BOSL2/std.scad>

/* [Part] */
part = "preview"; // ["preview", "cut_only"]

/* [Cradle envelope — measure your GPS + foam] */
gps_pocket_l    = 18;   // [10:1:40]  X extent
gps_pocket_w    = 18;   // [10:1:40]  Y extent
gps_pocket_depth = 3;   // [1:0.5:12] pocket depth (into mounting face, local +Z)

$fn = $preview ? 24 : 48;

// Centered pocket opening on Z=0 face, cut grows in +Z (use inside difference() on parent solid).
module GPS_Cradle_Cut(
    l     = gps_pocket_l,
    w     = gps_pocket_w,
    depth = gps_pocket_depth,
    eps   = 0.02
) {
    assert(l > 0 && w > 0 && depth > 0, "GPS pocket dims must be positive");

    translate([0, 0, -eps])
        cuboid([l + 2 * eps, w + 2 * eps, depth + eps], anchor = BOTTOM);
}

// Optional strap slot across X at pocket rim — stub (zero volume until enabled)
module GPS_Strap_Slots_Stub(slot_w = 3, slot_l = 12, depth = 1) {
    // Placeholder: uncomment when strap geometry is specified
    // translate([0, 0, 0]) cube([slot_l, slot_w, depth], center = true);
}

if (part == "preview") {
    difference() {
        cuboid([gps_pocket_l + 8, gps_pocket_w + 8, gps_pocket_depth + 2], anchor = BOTTOM);
        GPS_Cradle_Cut();
    }

} else if (part == "cut_only") {
    GPS_Cradle_Cut();
}
