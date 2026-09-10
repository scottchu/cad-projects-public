include <BOSL2/std.scad>
use <../screw/hole.scad>
include <../../spec/screw.scad>

module GPS_BottomPlate(
  width,
  length,
  height,
  chamfer = 2,
  edges = [BOTTOM+FRONT, BOTTOM+BACK]
) {
  cuboid(
    size = [width, length, height],
    chamfer = chamfer,
    edges = edges,
    anchor = BOTTOM
  );
}

module GPS_Base(
  width,
  length,
  height,
  chamfer = 2,
  screw_diameter = 1.6,
  screw_distance = 4
) {
  screw_spec = str("M", screw_diameter);
  true_diameter = screw_diameter * SCREW_MM_Multiplier;
  true_radius = true_diameter / 2;

  difference() {
    GPS_BottomPlate(
      width = width,
      length = length,
      height = height,
      chamfer = chamfer
    );

    translate([0, true_radius + screw_distance / 2, height / 2]) {
      translate([0, -true_diameter - screw_distance, 0])
      Screw_Hole(
        spec = screw_spec,
        length = length,
        anchor = CENTER,
        thread = false,
        orient = LEFT
      );

      Screw_Hole(
        spec = screw_spec,
        length = length,
        anchor = CENTER,
        thread = false,
        orient = LEFT
      );
    }
  };
}

GPS_Base(
    width = 20,
    length = 22,
    height = 5,
    screw_distance = 12,
    $fn = 50
  );
