include <BOSL2/std.scad>
use <base.scad>
use <clip.scad>

module GSP_Mount(
  base_width,
  base_length,
  base_height,
  screw_diameter,
  screw_distance,
  clip_width,
  clip_arm_thickness,
  clip_arm_height,
  clip_thickness,
  clip_length,
  clip_distance = -1
) {
  clip_distance = clip_distance < 0 ? (base_width - clip_width) / 2 : clip_distance / 2;
  clip_transform_y = (base_length - clip_length + clip_arm_thickness) / 2;

  union() {
    GPS_Base(
      width = base_width,
      length = base_length + (clip_arm_thickness * 2),
      height = base_height,
      screw_diameter = screw_diameter,
      screw_distance = screw_distance
    );

    translate([
      -clip_distance,
      clip_transform_y,
      base_height
    ])
    GPS_Clip(
      width = clip_width,
      arm_thickness = clip_arm_thickness,
      height = clip_arm_height,
      clip_thickness = clip_thickness,
      clip_length = clip_length
    );

    translate([
      clip_distance,
      clip_transform_y,
      base_height
    ])
    GPS_Clip(
      width = clip_width,
      arm_thickness = clip_arm_thickness,
      height = clip_arm_height,
      clip_thickness = clip_thickness,
      clip_length = clip_length
    );

    translate([
      0,
      -clip_transform_y,
      base_height
    ])
    zrot(180)
    GPS_Clip(
      width = base_width,
      arm_thickness = clip_arm_thickness,
      height = clip_arm_height,
      clip_thickness = clip_thickness,
      clip_length = clip_length
    );
  }
}

GSP_Mount(
  base_width = 22,
  base_length = 20,
  base_height = 6,
  screw_diameter = 1.6,
  screw_distance = 12,
  clip_width = 6,
  clip_arm_thickness = 2,
  clip_arm_height = 6,
  clip_thickness = 2,
  clip_length = 4
);