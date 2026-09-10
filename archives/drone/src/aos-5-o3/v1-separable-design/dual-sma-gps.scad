include <BOSL2/std.scad>
include <../../spec/gps/bn220.scad>
include <spec.scad>
use <gps-mount.scad>
use <gps-side-panel.scad>
use <sma.scad>

translate([0, 0, 10])
AOS_5_o3_DualSMA_Mount();

translate([0, -31.50, -4.05])
xrot(30 - 15, cp=[0, -BN220_LENGTH / 2, BN220_HEIGHT / 2])
AOS_5_o3_GPS_Mount();

AOS_5_o3_GPS_SidePanels($fn = 30);

// translate([-11.75, -18.75, -10])
// zrot(180)
// #import("../../stl/aos_5_gps_pro_2sma_STL.stl");