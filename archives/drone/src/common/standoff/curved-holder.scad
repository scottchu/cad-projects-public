include <BOSL2/std.scad>
include <BOSL2/rounding.scad>

use <base.scad>

$fn = 60;

module Standoff_CurvedHolder(
  diameter,
  wall,
  height,
  offset = 0.02,
  ofn = 6,
  ifn = 50,

  // Curve
  curve_x,
  curve_y,

  // Connecting Point
  connect_width,
  connect_length
) {
  od = diameter + wall * 2 + offset;
  or = od / 2;

  connect_point_x = -connect_width / 2 + or + curve_x;
  connect_point_y = -connect_length - or;
  // connect_point_y = -or - connect_length / 2;

  diff()
  conv_hull("remove") {
    cyl(
      d = od,
      h = height,
      $fn = ofn);

    translate([curve_x, curve_y, 0])
    cyl(
      d = od,
      h = height);

    tag("remove")
    cyl(
      d = diameter,
      h = height + offset,
      $fn = ifn);

    translate([connect_point_x, connect_point_y, 0])
    cuboid(
      size = [
        connect_width,
        connect_length,
        height
      ],
      anchor = FRONT
    );

    // dx = -(od + curve_x) / 2 + or ;
    // dy = - connect_length - or;

    // tag("remove")
    // translate([dx, dy, 0])
    // cuboid(
    //   size = [od + curve_x, connect_length, height + 0.1],
    //   anchor = FRONT
    // );
  }

  // ang = adj_opp_to_ang(adj = connect_length, opp = od + curve_x);

  // dx = or + curve_x - connect_width;
  // dy = -or + 0.11;
  // translate([dx, dy, 0])
  // zrot(180)
  // teardrop_edge_mask(
  //   l = height,
  //   r = connect_length,
  //   angle = ang,
  //   $fn = 120
  // );
}

Standoff_CurvedHolder(
  // Standoff
  diameter = 5,
  wall = 1,
  height = 10,
  offset = 0.2,
  ofn = 6,
  ifn = 50,

  // Curve
  curve_x = 2,
  curve_y = -1,

  // Connecting Point
  connect_width = 2,
  connect_length = 4
);
