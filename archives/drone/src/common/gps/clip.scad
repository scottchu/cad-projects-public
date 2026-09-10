include <BOSL2/std.scad>

module GPS_Clip(
  width,
  arm_thickness,
  height,
  clip_thickness,
  clip_length
) {
  union() {
    difference() {
      cuboid(
        size = [
          width,
          arm_thickness + clip_length,
          height + clip_thickness
        ],
        chamfer = 1,
        edges = [TOP+BACK, TOP+FRONT],
        anchor = BOTTOM
      );

      translate([0, -arm_thickness / 2, -0.01])
      cuboid(
        size= [
          width + 0.2,
          clip_length + 0.1,
          height/2 + 0.02
        ],
        chamfer = 1.5,
        edges = [BOTTOM+BACK],
        anchor = BOTTOM
      );

      translate([0, -arm_thickness / 2, height / 2])
      cuboid(
        size=[
          width + 0.2,
          clip_length + 0.1,
          height / 2
        ],
        chamfer = 0.5,
        edges = [TOP+BACK, TOP+FRONT],
        anchor = BOTTOM
      );
    };
  }
}

GPS_Clip(
  width = 6,
  arm_thickness = 2,
  height = 6,
  clip_thickness = 2,
  clip_length = 4
);