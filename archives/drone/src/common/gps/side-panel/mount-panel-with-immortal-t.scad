include <BOSL2/std.scad>
use <../../../lib/polygon.scad>
use <../../standoff/holder.scad>
use <../../adjustable-side-mount/mount.scad>
use <panel.scad>

module GPS_SidePanel_with_ImmortalT_v1(
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
  standoff_offset = 0.1,
  standoff_front_flat = false,
  standoff_front_chamfer = 0,
  standoff_ofn = 10,
  standoff_ifn = -1,
  standoff_zrot = 0,

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
  mount_offset = [0, 0],

  // Immortal-T
  antenna_diameter = 5,
  antenna_offset = [0, 0]
) {
  standoff_outer_radius = (standoff_diameter / 2) + standoff_wall;
  panel_dy = apothem(r = standoff_outer_radius, n = standoff_ofn) - (standoff_ofn/16);

  mount_length = adjustable_length(mount_screw_diameter, mount_screw_edge_distance, mount_screw_distance);
  mount_transition_x = mount_thickness / 2;
  mount_transition_y = -length / 2 + mount_offset[0];
  mount_transition_z = 0 + mount_offset[1];

  antenna_radius = antenna_diameter / 2;
  antenna_tx = 0;
  antenna_ty = -bottom_length / 2 + mount_screw_edge_distance + antenna_radius + antenna_offset[0];
  antenna_tz = -bottom_height + mount_screw_edge_distance + antenna_radius + antenna_offset[1];

  zrot(standoff_zrot)
  Standoff_Holder(
    diameter = standoff_diameter,
    wall = standoff_wall,
    height = standoff_height,
    offset = standoff_offset,
    front_flat = standoff_front_flat,
    front_chamfer = standoff_front_chamfer,
    ofn = standoff_ofn,
    ifn = standoff_ifn
  );

  translate([arm_shift, -arm_length - panel_dy, 0])
  difference() {

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

        translate([0, mount_transition_y, mount_transition_z])
        zrot(-90)
        xrot(90)
        mirror([1, 0, 0])
        GPS_Adjustable_Mount(
          // Mount
          thickness = thickness + 0.01,
          adjustable_angle = mount_adjustable_angle,

          // Base
          base_multiplier = mount_base_multiplier,
          base_scale = mount_base_scale,
          base_length_offset = mount_base_length_offset,
          show_center_point = mount_show_center_point,

          // Screw
          screw_diameter = mount_screw_diameter,
          screw_distance = mount_screw_distance,
          screw_edge_distance = mount_screw_edge_distance,

          show_screws = false
        );
      }

      translate([mount_transition_x, mount_transition_y, mount_transition_z])
      zrot(-90)
      xrot(90)
      mirror([1, 0, 0])
      GPS_Adjustable_Mount(
        // Mount
        thickness = mount_thickness + thickness + 0.01,
        adjustable_angle = mount_adjustable_angle,

        // Base
        base_multiplier = mount_base_multiplier,
        base_scale = mount_base_scale,
        base_length_offset = mount_base_length_offset,
        show_center_point = mount_show_center_point,

        // Screw
        screw_diameter = mount_screw_diameter,
        screw_distance = mount_screw_distance,
        screw_edge_distance = mount_screw_edge_distance
      );
    }
    if (mount_thickness > 0) {
      translate([-(thickness - mount_thickness) / 2 - 0.01, mount_transition_y, mount_transition_z])
      zrot(-90)
      xrot(90)
      mirror([1, 0, 0])
      GPS_Adjustable_Mount(
        // Mount
        thickness = mount_thickness + 0.01,
        adjustable_angle = mount_adjustable_angle,

        // Base
        base_multiplier = mount_base_multiplier,
        base_scale = mount_base_scale,
        base_length_offset = mount_base_length_offset,
        show_center_point = mount_show_center_point,

        // Screw
        screw_diameter = mount_screw_diameter,
        screw_distance = mount_screw_distance,
        screw_edge_distance = mount_screw_edge_distance,

        show_screws = false
      );
    }

    translate([
      antenna_tx,
      antenna_ty,
      antenna_tz
    ])
    cylinder(
      r = antenna_radius,
      h = thickness + 0.1,
      center = true,
      orient = LEFT,
      $fn = $preview ? 30 : 60
    );
  }

  // zrot(standoff_zrot)
  // Standoff_Holder(
  //   diameter = standoff_diameter,
  //   wall = standoff_wall,
  //   height = standoff_height,
  //   offset = standoff_offset,
  //   front_flat = standoff_front_flat,
  //   front_chamfer = standoff_front_chamfer,
  //   ofn = standoff_ofn,
  //   ifn = standoff_ifn
  // );

  // translate([arm_shift, -arm_length - panel_dy, 0])
  // union() {
  //   difference() {
  //     Panel_v1(
  //       thickness = thickness,
  //       length = length,

  //       arm_length = arm_length,
  //       arm_height = arm_height,

  //       fin_height = fin_height,
  //       fin_length = fin_length,
  //       fin_angle = fin_angle,

  //       bottom_height = bottom_height,
  //       bottom_angle = bottom_angle,
  //       bottom_length = bottom_length
  //     );

  //     translate([0, mount_transition_y, mount_transition_z])
  //     zrot(-90)
  //     xrot(90)
  //     mirror([1, 0, 0])
  //     GPS_Adjustable_Mount(
  //       // Mount
  //       thickness = thickness + 0.1,
  //       adjustable_angle = mount_adjustable_angle,

  //       // Base
  //       base_multiplier = mount_base_multiplier,
  //       base_scale = mount_base_scale,
  //       base_length_offset = mount_base_length_offset,
  //       show_center_point = mount_show_center_point,

  //       // Screw
  //       screw_diameter = mount_screw_diameter,
  //       screw_distance = mount_screw_distance,
  //       screw_edge_distance = mount_screw_edge_distance,

  //       show_screws = false
  //     );


  //   }

  //   translate([mount_transition_x, mount_transition_y, mount_transition_z])
  //   zrot(-90)
  //   xrot(90)
  //   mirror([1, 0, 0])
  //   GPS_Adjustable_Mount(
  //     // Mount
  //     thickness = mount_thickness,
  //     adjustable_angle = mount_adjustable_angle,

  //     // Base
  //     base_multiplier = mount_base_multiplier,
  //     base_scale = mount_base_scale,
  //     base_length_offset = mount_base_length_offset,
  //     show_center_point = mount_show_center_point,

  //     // Screw
  //     screw_diameter = mount_screw_diameter,
  //     screw_distance = mount_screw_distance,
  //     screw_edge_distance = mount_screw_edge_distance
  //   );
  // }


}

STANDOFF_DIAMETER = 4.5;
STANDOFF_WALL = 2;
STANDOFF_HEIGHT = 10;
STANDOFF_DISTANCE = 16.5;

ANGLE = 30;

GPS_SidePanel_with_ImmortalT_v1(
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
  standoff_ofn=6,
  standoff_ifn=30,
  standoff_front_flat = false,

  mount_screw_diameter = 1.6,
  mount_screw_distance = 12,
  mount_thickness = 2,
  mount_base_multiplier = 3,
  mount_base_scale = [1.2, 1.2],
  mount_offset = [0, 0],
  mount_adjustable_angle = 25
);