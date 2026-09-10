include <BOSL2/std.scad>
use <base.scad>

module Standoff_Holder(
  diameter,
  height,
  wall = 1,
  anchor = BOTTOM,
  offset = 0,
  front_flat = false,
  front_chamfer = 0,
  ofn = 10,
  ifn = -1
) {
  ifn = ifn < 0 ? ofn : ifn;
  d = 0.02;

  difference() {
    union() {
      Standoff(
        diameter = diameter,
        height = height,
        offset = (wall * 2 )+ offset,
        anchor = anchor,
        $fn = ofn
      );

      if (front_flat == true) {
         cuboid(
          size=[
            diameter+(wall * 2) + offset,
            diameter / 2 + wall + offset,
            height
          ],
          anchor = anchor+BACK,
          chamfer = front_chamfer,
          edges = [FRONT+LEFT, FRONT+RIGHT]
        );
      }
    }


    translate([0, 0, -d / 2])
    Standoff(
      diameter = diameter + offset,
      height = height + d,
      anchor = anchor,
      $fn = ifn
    );
  };
}

module Standoff_Holder_Pair(
  diameter,
  height,
  wall,
  distance = 0,
  anchor = BOTTOM,
  offset = 0,
  front_flat = false,
  front_chamfer = 0,
  ofn = 10,
  ifn = 1
) {
  dx = (distance + wall * 2 + diameter) / 2;

  translate([-dx, 0, 0])
  Standoff_Holder(
    diameter = diameter,
    wall = wall,
    height = height,
    offset = offset,
    front_flat = front_flat,
    front_chamfer = front_chamfer,
    ofn = ofn,
    ifn = ifn);

  translate([dx, 0, 0])
  Standoff_Holder(
    diameter = diameter,
    wall = wall,
    height = height,
    offset = offset,
    front_flat = front_flat,
    front_chamfer = front_chamfer,
    ofn = ofn,
    ifn = ifn);
}

Standoff_Holder_Pair(
  diameter = 4,
  wall = 1,
  distance = 4,
  height = 20,
  offset = 0.2,
  front_flat = true,
  front_chamfer = 0,
  ofn = 50,
  ifn = 6
);