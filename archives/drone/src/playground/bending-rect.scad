include <BOSL2/std.scad>
include <BOSL2/rounding.scad>
use <../common/standoff/holder.scad>

// box = square([255,50]);
// rbox = round_corners(box, method="smooth", cut=4, $fn=12);
// thickness = 2;
// difference(){
//   offset_sweep(rbox, height=50, check_valid=false, steps=22,
//                bottom=os_teardrop(r=2), top=os_circle(r=1));
//   up(thickness)
//     offset_sweep(offset(rbox, r=-thickness, closed=true,check_valid=false),
//                  height=48, steps=22, check_valid=false,
//                  bottom=os_circle(r=4), top=os_circle(r=-1,extra=1));

$fn = 30;

conv_hull() {
  diff()
  conv_hull("remove") {
    cyl(r=4.5, h=10);

    translate([4, -4, 0])
    cyl(r=4.5, h=10);

    tag("remove")
    cyl(r=2.5, h=11);
  };

  translate([7.5, -14, 0])
  cuboid(
    size = [2, 5, 10]
  );
}
