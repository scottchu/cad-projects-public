include <spec.scad>
use <../common/GPS/side-panel/mount-panel-with-immortal-t.scad>

module Quadmula_F5_GPS_SidePanel() {
  GPS_SidePanel_with_ImmortalT_v1(
    thickness = PANEL_THICKNESS,
    length = PANEL_LENGTH,

    arm_length = ARM_LENGTH,
    arm_height = ARM_HEIGHT,
    arm_shift = ARM_SHIFT,

    fin_height = FIN_HEIGHT,
    fin_length = FIN_LENGTH,
    fin_angle = FIN_ANGLE,

    bottom_height = BOTTOM_HEIGHT,
    bottom_angle = BOTTOM_ANGLE,
    bottom_length = BOTTOM_LENGTH,

    standoff_diameter = STANDOFF_DIAMETER,
    standoff_wall = STANDOFF_WALL,
    standoff_height = PANEL_STANDOFF_HEIGHT,
    standoff_ofn = STANDOFF_OUTER_SIDES,
    standoff_ifn = STANDOFF_INNER_SIDES,
    standoff_front_flat = STANDOFF_FRONT_FLAT,

    mount_screw_diameter = MOUNT_SCREW_DIAMETER,
    mount_screw_distance = MOUNT_SCREW_DISTANCE,
    mount_thickness = MOUNT_THICKNESS,
    mount_base_multiplier = MOUNT_BASE_MULTIPLIER,
    mount_base_scale = MOUNT_BASE_SCALE,
    mount_offset = MOUNT_OFFSET,
    mount_adjustable_angle = MOUNT_ADJUSTABLE_ANGLE
  );
}

module Quadmula_F5_GPS_SidePanels() {
  distance = (STANDOFF_DISTANCE + STANDOFF_DIAMETER) + STANDOFF_WALL * 2;

  distribute(distance) {
    Quadmula_F5_GPS_SidePanel();

    mirror([1, 0, 0])
    Quadmula_F5_GPS_SidePanel();
  }
}

Quadmula_F5_GPS_SidePanels();

import("../../stl/SF5_Antenna_Tube_4mm_Type2.stl");
// import("../../stl/SF5_Antenna_SMA_Mid_Split.stl");
// import("../../stl/SF5_Antenna_T_915.stl");
