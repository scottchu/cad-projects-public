//! SMA Mount Hex Screw Recess Module
//!
//! Creates a hexagon-shaped recess (counterbore/socket) for SMA mount bottom.
//! This recess allows the mount to lock onto the hex screw head at the bottom.
//! Based on observation: SMA mounts typically have hex screw recesses with
//! diameter 12mm (flat-to-flat) and depth 1mm.
//!
//! @file screw-hexgon.scad
//! @module SMA_HexScrewRecess

include <BOSL2/std.scad>
include <spec.scad>

//! Creates a hexagon-shaped recess for locking onto hex screw heads
//!
//! Creates a hexagonal recess (counterbore/socket) that fits over hex screw heads.
//! Used in difference() operations to cut out the recess from the mount bottom,
//! allowing the mount to lock onto the screw head for secure attachment.
//!
//! @param diameter Flat-to-flat diameter of hexagon (default: SMA_SCREW_HEX_DIAMETER)
//! @param depth Depth/height of recess (default: SMA_SCREW_HEX_DEPTH)
//! @param anchor BOSL2 anchor position (default: BOTTOM)
//! @param clearance Additional clearance for easier fit (default: 0)
module SMA_HexScrewRecess(
  diameter = SMA_SCREW_HEX_DIAMETER,
  depth = SMA_SCREW_HEX_DEPTH,
  anchor = CENTER,
  clearance = 0
) {
  // Parameter validation
  assert(diameter > 0, "Diameter must be positive");
  assert(depth > 0, "Depth must be positive");
  assert(clearance >= 0, "Clearance must be non-negative");

  // Small value for boolean operation clearance
  EPSILON = 0.01;

  // Add small clearance to ensure clean boolean operation
  translate([0, 0, -EPSILON / 2])
  linear_extrude(height = depth + EPSILON, anchor = anchor) {
    hexagon(d = diameter + clearance);  // d = flat-to-flat distance
  }
}

// Reference STL for comparison
// rotate([-30, -4, 3]) {
//   translate([-98, 102, -15]) {
//     #import("sample/Dual_SMA_Apex_Rear_Mount.stl");
//   }
// }

// Example usage: Creating a recess in a mount
if ($preview) {
  // Example: Mount with hex screw recess
  difference() {
    // Mount bottom plate
    cuboid(size = [30, 30, 2], anchor = BOTTOM);

    // Hex screw recess - allows mount to lock onto screw head
    translate([0, 0, 0])
      SMA_HexScrewRecess();
  }
}
