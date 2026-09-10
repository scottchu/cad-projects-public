include <BOSL2/std.scad>
use <panel.scad>
use <../../adjustable-side-mount/mount.scad>
use <../../standoff/curved-holder.scad>
use <../../../lib/polygon.scad>

module GPS_CurvedSidePanel_v1(
  // general
  thickness = 2,
  length,

  // Arm
  arm_length,
  arm_height,
  arm_shift = 0,

  // Fin
  fin_length,
  fin_height,
  fin_angle,

  // Bottom
  bottom_length = -1,
  bottom_height,
  bottom_angle,

  // Standoff
  standoff_diameter,
  standoff_wall,
  standoff_height,
  standoff_offset = 0,
  standoff_ofn = 10,
  standoff_ifn = -1,
  standoff_zrot = 0,

  // Curve
  standoff_curve_x,
  standoff_curve_y,

  // Connecting Point
  standoff_connect_width,
  standoff_connect_length,

  // Mount
  mount_thickness = 2,
  mount_adjustable_angle = 30,
  mount_base_multiplier = 3,
  mount_base_scale = [1, 1],
  mount_base_length_offset = 0,
  mount_show_center_point = false,

  mount_screw_diameter,
  mount_screw_distance,
  mount_screw_edge_distance = 2,
  mount_offset = [0, 0]
) {
  standoff_outer_radius = (standoff_diameter / 2) + standoff_wall;
  panel_dy = apothem(r = standoff_outer_radius, n = standoff_ofn) - (standoff_ofn/16);

  mount_length = adjustable_length(mount_screw_diameter, mount_screw_edge_distance, mount_screw_distance);
  mount_transition_x = (thickness + mount_thickness) / 2;
  mount_transition_y = -length / 2 + mount_offset[0];
  mount_transition_z = 0 + mount_offset[1];


  standoff_tx = -(standoff_diameter + standoff_curve_x + standoff_offset) + 0.1;
  standoff_tz = standoff_height / 2;

  translate([standoff_tx, 0, standoff_tz])
  Standoff_CurvedHolder(
    diameter = standoff_diameter,
    wall = standoff_wall,
    height = standoff_height,
    offset = standoff_offset,
    ofn = standoff_ofn,
    ifn = standoff_ifn,
    // Curve
    curve_x = standoff_curve_x,
    curve_y = standoff_curve_y,

    // Connecting Point
    connect_width = standoff_connect_width,
    connect_length = standoff_connect_length
  );

  translate([arm_shift, -arm_length - panel_dy, 0])
  union() {
    difference() {
      Panel_v1(
        thickness = thickness,
        length = length,

        arm_length = arm_length,
        arm_height = arm_height,

        fin_height = fin_height,
        fin_length = fin_length,
        fin_angle = fin_angle,

        bottom_height = bottom_height,
        bottom_angle = bottom_angle,
        bottom_length = bottom_length
      );

    //   translate([0, mount_transition_y, mount_transition_z])
    //   zrot(-90)
    //   xrot(90)
    //   mirror([1, 0, 0])
    //   GPS_Adjustable_Mount(
    //     // Mount
    //     thickness = thickness + 0.1,
    //     adjustable_angle = mount_adjustable_angle,

    //     // Base
    //     base_multiplier = mount_base_multiplier,
    //     base_scale = mount_base_scale,
    //     base_length_offset = mount_base_length_offset,
    //     show_center_point = mount_show_center_point,

    //     // Screw
    //     screw_diameter = mount_screw_diameter,
    //     screw_distance = mount_screw_distance,
    //     screw_edge_distance = mount_screw_edge_distance,

    //     show_screws = false
    //   );
    }

    // translate([mount_transition_x, mount_transition_y, mount_transition_z])
    // zrot(-90)
    // xrot(90)
    // mirror([1, 0, 0])
    // GPS_Adjustable_Mount(
    //   // Mount
    //   thickness = mount_thickness,
    //   adjustable_angle = mount_adjustable_angle,

    //   // Base
    //   base_multiplier = mount_base_multiplier,
    //   base_scale = mount_base_scale,
    //   base_length_offset = mount_base_length_offset,
    //   show_center_point = mount_show_center_point,

    //   // Screw
    //   screw_diameter = mount_screw_diameter,
    //   screw_distance = mount_screw_distance,
    //   screw_edge_distance = mount_screw_edge_distance
    // );
  }
}

STANDOFF_DIAMETER = 4.5;
STANDOFF_WALL = 2;
STANDOFF_HEIGHT = 10;
STANDOFF_DISTANCE = 16.5;

ANGLE = 30;

GPS_CurvedSidePanel_v1(
  thickness = 2,
  length = 40,

  arm_length = 15,
  arm_height = 10,
  arm_shift = -1.15,

  fin_height = 2.5,
  fin_length = 8,
  fin_angle = 30,

  bottom_height = 4,
  bottom_angle = 30,
  bottom_length = 35,

  standoff_diameter = STANDOFF_DIAMETER,
  standoff_wall = STANDOFF_WALL,
  standoff_height = STANDOFF_HEIGHT,
  standoff_ofn = 30,
  standoff_ifn = 30,
  standoff_offset = 0.1,
  standoff_curve_x = 2,
  standoff_curve_y = -2,
  standoff_connect_width = 2,
  standoff_connect_length = 14,

  mount_screw_diameter = 1.6,
  mount_screw_distance = 12,
  mount_thickness = 2,
  mount_base_multiplier = 3,
  mount_base_scale = [1.2, 1.2],
  mount_offset = [0, 0],
  mount_adjustable_angle = 25
);