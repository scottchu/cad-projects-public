//! Curved Standoff Holder Module
//!
//! Creates a curved holder that connects two standoffs with a curved path.
//! Useful for non-linear frame designs where standoffs are not in a straight line.
//!
//! @file curved-holder.scad
//! @module Standoff_CurvedHolder

include <BOSL2/std.scad>
include <BOSL2/rounding.scad>

use <standoff.scad>
include <constants.scad>
include <functions.scad>

$fn = DEFAULT_PREVIEW_FACETS;

//! Creates a curved holder connecting two standoffs with a curved path
//!
//! Uses BOSL2's conv_hull() to create a smooth curved transition between
//! two standoffs positioned at different locations.
//!
//! @param diameter Inner diameter (standoff diameter)
//! @param wall Wall thickness around standoff
//! @param height Height of the holder
//! @param offset Additional offset for fit tolerance (default: DEFAULT_OFFSET)
//! @param outer_facets Number of sides for outer shape (default: DEFAULT_CURVED_OUTER_FACETS)
//! @param inner_facets Number of sides for inner hole (default: DEFAULT_CURVED_INNER_FACETS)
//! @param curve_x X offset for curved path
//! @param curve_y Y offset for curved path
//! @param connect_width Width of connecting section
//! @param connect_length Length of connecting section
module Standoff_CurvedHolder(
  diameter,
  wall,
  height,
  offset = DEFAULT_OFFSET,
  outer_facets = DEFAULT_CURVED_OUTER_FACETS,
  inner_facets = DEFAULT_CURVED_INNER_FACETS,

  // Curve
  curve_x,
  curve_y,

  // Connecting Point
  connect_width,
  connect_length
) {
  // Parameter validation
  assert(diameter > 0, "Diameter must be positive");
  assert(wall > 0, "Wall thickness must be positive");
  assert(height > 0, "Height must be positive");
  assert(offset >= -diameter / 2, "Offset too negative - would create negative diameter");
  assert(outer_facets >= 3, "Outer facets must be at least 3");
  assert(inner_facets >= 3, "Inner facets must be at least 3");
  assert(connect_width > 0, "Connect width must be positive");
  assert(connect_length > 0, "Connect length must be positive");

  // Preview mode optimization: reduce facet count for faster preview
  is_preview = $preview;
  preview_outer_facets = calc_preview_facets(outer_facets, is_preview);
  preview_inner_facets = calc_preview_facets(inner_facets, is_preview);

  // Calculate outer diameter and radius using helper functions
  od = calc_outer_diameter(diameter, wall, offset);
  or = calc_radius(od);
  inner_hole_diameter = calc_inner_hole_diameter(diameter, offset);

  // Calculate connection point position
  // Positioned to connect smoothly between main standoff and curved standoff
  connect_point_x = -connect_width / 2 + or + curve_x;
  connect_point_y = -connect_length - or;

  diff()
  conv_hull("remove") {
    cyl(
      d = od,
      h = height,
      $fn = preview_outer_facets);

    translate([curve_x, curve_y, 0])
    cyl(
      d = od,
      h = height,
      $fn = preview_outer_facets);

    tag("remove")
    cyl(
      d = inner_hole_diameter,
      h = height + EPSILON,
      $fn = preview_inner_facets);

    translate([connect_point_x, connect_point_y, 0])
    cuboid(
      size = [
        connect_width,
        connect_length,
        height
      ],
      anchor = FRONT
    );
  }
}

// Test code - only shown in preview mode
if ($preview) {
  Standoff_CurvedHolder(
    // Standoff
    diameter = 5,
    wall = 2,
    height = 10,
    offset = 0.2,
    outer_facets = DEFAULT_CURVED_OUTER_FACETS,
    inner_facets = DEFAULT_CURVED_INNER_FACETS,

    // Curve
    curve_x = 2,
    curve_y = -1,

    // Connecting Point
    connect_width = 2,
    connect_length = 4
  );
}
