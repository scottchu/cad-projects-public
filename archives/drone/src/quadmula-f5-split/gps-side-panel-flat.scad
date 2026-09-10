include <BOSL2/std.scad>
include <spec.scad>
use <gps-side-panel.scad>

module Quadmula_F5_GPS_SidePanels_Flat() {
  distance = (STANDOFF_DISTANCE + STANDOFF_DIAMETER) + STANDOFF_WALL * 2 + BOTTOM_HEIGHT;

  distribute(distance) {
    yrot(90)
    Quadmula_F5_GPS_SidePanel();

    yrot(-90)
    mirror([1, 0, 0])
    Quadmula_F5_GPS_SidePanel();
  }
}

Quadmula_F5_GPS_SidePanels_Flat();