include <BOSL2/std.scad>

width = 30;
length = 10;
height = 6;

module hole(size = 1.0) {
  cylinder(
    h = length + 1,
    r = size,
    orient = FRONT,
    anchor = CENTER,
    $fn = 60
  );
}

difference() {
  cuboid(
    size = [
      width, length, height
    ]
  );

  translate([-12, 0, 0])
  hole(1.0);

  translate([-8, 0, 0])
  hole(1.2);

  translate([-3.5, 0, 0])
  hole(1.4);

  translate([1.5, 0, 0])
  hole(1.6);

  translate([6.5, 0, 0])
  hole(1.8);

  translate([12, 0, 0])
  hole(2.0);
}
