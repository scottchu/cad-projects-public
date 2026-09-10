include <BOSL2/std.scad>
include <../../spec/sma.scad>

module SMA_Hole(
  height = 2,
  $fn = 25,
  show_teeth_disk = false
) {
  cylinder(
    d = SMA_DIAMETER,
    h = height,
    anchor = CENTER+BOTTOM,
    $fn = $fn
  );

  if (show_teeth_disk) {
     #circle(
      d = SMA_DIAMETER_REQUIRED,
      $fn = $fn
    );
  }
}

SMA_Hole(show_teeth_disk = true, $fn = 120);