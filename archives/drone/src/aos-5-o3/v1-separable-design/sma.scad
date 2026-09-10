use <../../common/SMA/mount.scad>
include <spec.scad>

module AOS_5_o3_DualSMA_Mount() {
  SMA_Mount_Dual(
    width = SMA_MOUNT_WIDTH,
    length = SMA_MOUNT_LENGTH,
    height = SMA_STANDOFF_HEIGHT,
    distance = SMA_DISTANCE,
    angle = SMA_ANGLE,
    thickness = SMA_MOUNT_THICKNESS,
    top_back_chamfer = SMA_TOP_BACK_CHAMFER,
    sma_fn = SMA_FN,
    show_sma_teeth_disk = SHOW_SMA_TEETH_DISK,
    sma_y_offset = SMA_Y_OFFSET,

    standoff_diameter = STANDOFF_DIAMETER,
    standoff_wall = STANDOFF_WALL,
    standoff_height = SMA_STANDOFF_HEIGHT,
    standoff_distance = STANDOFF_DISTANCE,
    standoff_ofn = STANDOFF_OUTER_SIDES,
    standoff_ifn = STANDOFF_INNER_SIDES,
    standoff_front_flat = STANDOFF_FRONT_FLAT
  );
}

AOS_5_o3_DualSMA_Mount();