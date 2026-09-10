//! Standoff Base Module
//!
//! Creates a basic cylindrical standoff representation.
//! This is a simple wrapper around BOSL2's cylinder() primitive.
//!
//! @file standoff.scad
//! @module Standoff

include <BOSL2/std.scad>

//! Creates a cylindrical standoff
//! @param diameter Diameter of the standoff
//! @param height Height of the standoff
//! @param diameter_offset Additional diameter offset (default: 0)
//! @param anchor BOSL2 anchor position (default: BOTTOM)
module Standoff(
  diameter,
  height,
  diameter_offset = 0,
  anchor = BOTTOM
) {
  // Parameter validation
  assert(diameter > 0, "Diameter must be positive");
  assert(height > 0, "Height must be positive");
  assert(diameter_offset >= -diameter / 2, "Diameter offset too negative - would create negative diameter");

  // Note: $fn is passed from caller, preview optimization handled in calling modules
  cylinder(
    h = height,
    d = diameter + diameter_offset,
    anchor = anchor
  );
}

// Test code - only shown in preview mode
if ($preview) {
  Standoff(4, 20, diameter_offset=1, $fn=6);
}
