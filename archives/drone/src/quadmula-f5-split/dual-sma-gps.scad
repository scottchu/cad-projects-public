include <BOSL2/std.scad>
include <../spec/gps/bn220.scad>
include <spec.scad>
use <gps-mount.scad>
use <gps-side-panel.scad>
use <sma.scad>

translate([0, 0, 10])
Quadmula_F5_DualSMA_Mount();

translate([0, -30, -4.05])
xrot(30 - 15, cp=[0, -BN220_LENGTH / 2, BN220_HEIGHT / 2])
Quadmula_F5_GPS_Mount();

Quadmula_F5_GPS_SidePanels($fn = 30);
