include <BOSL2/std.scad>
include <../../spec/screw.scad>
include <hole.scad>

module AdjustableScrewHole(
  angle = 45,
  distance = 16,
  length = 2,
  diameter = 1.6,
  caps = true
) {
  quality = $preview ? ($fn ? $fn : 10) : 60;
  cap_angle = diameter;
  angle = angle;

  path_extrude2d(
    arc(
      r = distance,
      angle = [0, angle],
      n = quality
    ),
    $fn = quality,
    caps = caps
  )
  trapezoid(
    w1 = diameter,
    w2 = diameter,
    h = length,
    anchor = BOTTOM
  );
}

module AdjustableScrewHoles(
  diameter,
  distance,
  angle,
  length,
  edge_distance,
  caps = true,

  show_meta = false
) {
  true_diameter = diameter * SCREW_MM_Multiplier;
  true_radius = true_diameter / 2;
  true_distance = distance + true_diameter;

  dz = -length / 2;

  union() {
    Screw_M_Hole(
      diameter = diameter,
      length = length
    );

    translate([0, 0, dz])
    AdjustableScrewHole(
      diameter = true_diameter,
      angle = angle,
      distance = true_distance,
      length = length,
      caps = caps
    );
  }

  if ($preview && show_meta) {
    color([0, 0.75, 0.5, 0.75])
    translate([0, 0, dz])
    linear_extrude(
      height = length
    )
    union() {
      zrot(angle, cp=[0, 0, 0])
      stroke(
        path = [
          [0, 0],
          [true_distance, 0]
        ],
        width = true_diameter
      );

      stroke(
        path = [
          [0, 0],
          [true_distance, 0]
        ],
        width = true_diameter
      );
    }

  }
}

AdjustableScrewHoles(
  diameter = 1.6,
  angle = 30,
  distance = 10,
  length = 2,
  caps = true,
  show_meta = true,
  $fn = 30
);