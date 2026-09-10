include <BOSL2/std.scad>
include <../../spec/gps/bn220.v1.scad>
include <spec.scad>
use <gps-mount.scad>
use <gps-side-panel.scad>
use <sma.scad>

translate([0, 0, 10])
AOS_5_o3_DualSMA_Mount();

translate([0, -25.0, -3.0])
xrot(15, cp=[0, -BN220_length / 2, BN220_height / 2])
AOS_5_o3_GPS_Mount();

translate([0, -17.5, 0])
AOS_5_o3_GPS_SidePanels($fn = 30);

// translate([-11.75, -18.75, -10])
// zrot(180)
// #import("../../stl/aos_5_gps_pro_2sma_STL.stl");