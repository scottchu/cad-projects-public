include <../../spec/gps/bn220.scad>
use <../../common/gps/mount.scad>
include <spec.scad>

module AOS_5_o3_GPS_Mount() {
  GSP_Mount(
    base_width = BN220_WIDTH,
    base_length = BN220_LENGTH,
    base_height = GPS_BASE_HEIGHT,
    screw_diameter = GPS_SCREW_DIAMETER,
    screw_distance = GPS_SCREW_DISTANCE,
    clip_width = CLIP_WIDTH,
    clip_arm_thickness = CLIP_ARM_THICKNESS,
    clip_arm_height = BN220_BACK_HEIGHT,
    clip_thickness = CLIP_THICKNESS,
    clip_length = CLIP_LENGTH,
    $fn = 60
  );
}

AOS_5_o3_GPS_Mount();