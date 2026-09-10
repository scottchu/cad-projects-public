include <BOSL2/std.scad>

module Standoff(
  diameter,
  height,
  offset = 0,
  anchor = BOTTOM
) {
  cylinder(
    h = height,
    d = diameter + offset,
    anchor = anchor
  );
}

Standoff(4, 20, 1, $fn=6);