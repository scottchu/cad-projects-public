include <BOSL2/std.scad>

width = 18;
length = 21.8;
height = 5;
thickness = 2;

difference() {
  translate([0, 12.45, -5.15])
  xrot(-30)
  zrot(180)
  translate([0, -60, 0])
  #import("../../stl/BN220_Mount.stl");

  translate([0, 0, 2.1])
  #cuboid(
    size = [outer_w, outer_l, 2],
    rounding = 0
  );
}

translate([-4, 4, -2])
color([0, 0.75, 0.25, 1])
cuboid(
  size = [1, 1, 1]
);





// difference() {
//   cuboid(
//     size = [outer_w, outer_l, height],
//     rounding = 0.5
//   ) {

//     #cuboid(
//       size = [width, length, 1],
//       rounding = 0.5,
//       anchor = TOP
//     );
//   };



//   // cuboid(
//   //   size = [width, length, height + 0.01],
//   //   rounding = 0.5
//   // );
// }
