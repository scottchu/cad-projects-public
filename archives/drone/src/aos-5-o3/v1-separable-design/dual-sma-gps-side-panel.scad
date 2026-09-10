include <../../spec/gps/bn220.scad>
use <../../common/GPS/mount.scad>
use <../../common/GPS/side_panel.scad>
use <../../common/SMA/mount.scad>
include <spec.scad>

translate([0, 0, 10])
SMA_Mount_Dual(
  width = SMA_MOUNT_WIDTH,
  length = SMA_MOUNT_LENGTH,
  height = SMA_MOUNT_HEIGHT,
  distance = SMA_DISTANCE,
  angle = SMA_ANGLE,
  thickness = SMA_MOUNT_THICKNESS,
  top_back_chamfer = 1,
  sma_fn = 60,
  show_sma_teeth_disk = true,
  sma_y_offset = SMA_Y_OFFSET,

  standoff_diameter = STANDOFF_DIAMETER,
  standoff_wall = STANDOFF_WALL,
  standoff_height = SMA_STANDOFF_HEIGHT,
  standoff_distance = STANDOFF_DISTANCE,
  standoff_ofn = STANDOFF_OUTER_SIDES,
  standoff_ifn = STANDOFF_INNER_SIDES,
  standoff_front_flat = false
);

translate([-(STANDOFF_DISTANCE + STANDOFF_DIAMETER)/2 - STANDOFF_WALL, 0, 0])
GPS_SidePanel_v1(
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
  standoff_height = STANDOFF_HEIGHT / 2,
  standoff_ofn = 6,
  standoff_ifn = 30,
  standoff_front_flat = false,

  mount_screw_diameter = 1.6,
  mount_screw_distance = 12,
  mount_thickness = 2.5,
  mount_base_multiplier = 3,
  mount_base_scale = [1.2, 1.2],
  mount_offset = [0, 0],
  mount_adjustable_angle = 25
);


translate([(STANDOFF_DISTANCE + STANDOFF_DIAMETER)/2 + STANDOFF_WALL, 0, 0])
mirror([1, 0, 0])
GPS_SidePanel_v1(
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
  standoff_height = STANDOFF_HEIGHT / 2,
  standoff_ofn = 6,
  standoff_ifn = 30,
  standoff_front_flat = false,

  mount_screw_diameter = 1.6,
  mount_screw_distance = 12,
  mount_thickness = 2.5,
  mount_base_multiplier = 3,
  mount_base_scale = [1.2, 1.2],
  mount_offset = [0, 0],
  mount_adjustable_angle = 25
);
