include <BOSL2/std.scad>
include <BOSL2/screws.scad>

module Screw_Hole(
  spec = "M1.6",
  length,
  anchor = CENTER,
  thread = true,
  orient = UP,
) {
  screw_hole(
    spec = spec,
    length = length,
    anchor = anchor,
    thread = thread,
    orient = orient
  );
}

module Screw_M_Hole(
  diameter = 1.6,
  length,
  anchor = CENTER,
  thread = false,
  orient = UP,
) {
  thread = thread && $preview;

  spec = str("M", diameter);

  Screw_Hole(
    spec = spec,
    length = length,
    anchor = anchor,
    thread = thread,
    orient = orient
  );
}