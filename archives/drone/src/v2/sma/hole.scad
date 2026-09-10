include <BOSL2/std.scad>
include <spec.scad>


module SMA_Hole(
  height = 2,
  $fn = 25,
  show_teeth_disk = false
) {
  cylinder(
    d=SMA_DIAMETER,
    h=height,
    anchor=CENTER + BOTTOM,
    $fn=$fn
  );

  if (show_teeth_disk) {
    // Show the full volume that needs to be removed (including teeth clearance)
    // Using % (background) so it visualizes but doesn't participate in boolean operations
    %cylinder(
      d=SMA_DIAMETER_REQUIRED,
      h=height,
      anchor=CENTER + BOTTOM,
      $fn=$fn
    );
  }
}

SMA_Hole(show_teeth_disk=true, $fn=120);
