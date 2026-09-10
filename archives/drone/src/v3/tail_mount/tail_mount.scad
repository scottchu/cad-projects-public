// Orchestrator stub — phased integration (README “Phased build order”).
// Video: use ../sma/plate.scad in Customizer or instantiate SMA_Plate() from a caller that
// defines all plate globals (use<> does not import plate’s top-level variables).
//
// Intended union order (future):
//   1. Frame_Shell_Stub or real frame from ../frame/frame.scad
//   2. SMA_Plate / video variant
//   3. optional difference() GPS_Cradle_Cut from ../gps/gps.scad
//   4. optional RC tab from ../rx/rx.scad (not created yet)

use <../frame/frame.scad>
use <../gps/gps.scad>

/* [Stub toggles — geometry is illustrative only] */
show_frame_stub = true;
show_gps_preview  = false;  // true: small block with pocket next to origin (not aligned to frame)

module Tail_Mount_Stub_Layout() {
    if (show_frame_stub)
        Frame_Shell_Stub();

    // GPS modules come from use<gps.scad>; pocket defaults live there. Offset is layout-only.
    if (show_gps_preview)
        translate([32, 0, 0]) {
            difference() {
                cuboid([26, 26, 5], anchor = BOTTOM);
                GPS_Cradle_Cut();
            }
        }
}

Tail_Mount_Stub_Layout();
