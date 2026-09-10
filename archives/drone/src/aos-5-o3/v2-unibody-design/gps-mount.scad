include <BOSL2/std.scad>
include <spec.scad>

include <../../spec/gps/bn220.v1.scad>
use <../../common/gps/mount.v1.scad>

module AOS_5_o3_GPS_Mount() {
  gps_mount_v1(
    dimension = GPS_dimension,
    clip_dimension = GPS_clip_dimension,
    cover_length = GPS_cover_length,
    plug_width = GPS_plug_width,
    plug_height = BN220_plug_height + 3,
    thickness = GPS_mount_thickness,
    chamfer = GPS_mount_chamfer,
    offset = GPS_mount_offset,
    hide_side = DEBUG
  );
}
