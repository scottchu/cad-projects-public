//! Standoff Holder Modules
//!
//! Creates holders that wrap around frame standoffs, allowing components
//! to attach to the frame. Supports single holders and pairs.
//!
//! @file holder.scad
//! @module Standoff_Holder
//! @module Standoff_Holder_Pair

include <BOSL2/std.scad>
use <standoff.scad>
include <constants.scad>
include <functions.scad>

//! Creates a holder that wraps around a frame standoff
//!
//! Creates a hollow cylinder that fits around a standoff post, with optional
//! flat front face for aesthetic or functional purposes.
//!
//! @param diameter Inner diameter (standoff diameter)
//! @param height Height of the holder
//! @param wall Wall thickness around standoff (default: DEFAULT_WALL_THICKNESS)
//! @param anchor BOSL2 anchor position (default: BOTTOM)
//! @param offset Additional offset for fit tolerance (default: 0)
//! @param front_flat If true, creates flat front face (default: false)
//! @param front_chamfer Chamfer size for front face (default: 0)
//! @param outer_facets Number of sides for outer shape (default: DEFAULT_OUTER_FACETS)
//! @param inner_facets Number of sides for inner hole (default: DEFAULT_INNER_FACETS, -1 means use outer_facets)
module Standoff_Holder(
  diameter,
  height,
  wall = DEFAULT_WALL_THICKNESS,
  anchor = BOTTOM,
  offset = 0,
  front_flat = false,
  front_chamfer = 0,
  outer_facets = DEFAULT_OUTER_FACETS,
  inner_facets = DEFAULT_INNER_FACETS
) {
  // Parameter validation
  assert(diameter > 0, "Diameter must be positive");
  assert(height > 0, "Height must be positive");
  assert(wall > 0, "Wall thickness must be positive");
  assert(offset >= -diameter / 2, "Offset too negative - would create negative diameter");
  assert(front_chamfer >= 0, "Front chamfer must be non-negative");
  assert(outer_facets >= 3, "Outer facets must be at least 3");
  assert(inner_facets >= 3 || inner_facets == -1, "Inner facets must be at least 3, or -1 to use outer_facets");

  // Preview mode optimization: reduce facet count for faster preview
  is_preview = $preview;
  final_inner_facets = resolve_inner_facets(inner_facets, outer_facets);
  preview_outer_facets = calc_preview_facets(outer_facets, is_preview);
  preview_inner_facets = calc_preview_facets(final_inner_facets, is_preview);

  // Calculate dimensions using helper functions
  outer_diameter = calc_outer_diameter(diameter, wall, offset);
  inner_hole_diameter = calc_inner_hole_diameter(diameter, offset);
  flat_face_y = calc_flat_face_y_dimension(outer_diameter, offset);

  difference() {
    union() {
      Standoff(
        diameter = diameter,
        height = height,
        diameter_offset = outer_diameter - diameter,
        anchor = anchor,
        $fn = preview_outer_facets
      );

      if (front_flat) {
         cuboid(
          size=[
            outer_diameter,
            flat_face_y,
            height
          ],
          anchor = anchor+BACK,
          chamfer = front_chamfer > 0 ? front_chamfer : 0,
          edges = [FRONT+LEFT, FRONT+RIGHT]
        );
      }
    }


    translate([0, 0, -EPSILON / 2])
    Standoff(
      diameter = inner_hole_diameter,
      height = height + EPSILON,
      diameter_offset = 0,
      anchor = anchor,
      $fn = preview_inner_facets
    );
  };
}

//! Creates a pair of standoff holders positioned at a specified distance apart
//!
//! Creates two Standoff_Holder modules positioned symmetrically at the
//! specified distance. Commonly used for frame attachment points.
//!
//! @param diameter Inner diameter (standoff diameter)
//! @param height Height of the holders
//! @param wall Wall thickness around standoffs
//! @param distance Distance between standoff centers (default: 0)
//! @param anchor BOSL2 anchor position (default: BOTTOM)
//! @param offset Additional offset for fit tolerance (default: 0)
//! @param front_flat If true, creates flat front faces (default: false)
//! @param front_chamfer Chamfer size for front faces (default: 0)
//! @param outer_facets Number of sides for outer shape (default: DEFAULT_OUTER_FACETS)
//! @param inner_facets Number of sides for inner holes (default: DEFAULT_INNER_FACETS)
module Standoff_Holder_Pair(
  diameter,
  height,
  wall,
  distance = 0,
  anchor = BOTTOM,
  offset = 0,
  front_flat = false,
  front_chamfer = 0,
  outer_facets = DEFAULT_OUTER_FACETS,
  inner_facets = DEFAULT_INNER_FACETS
) {
  // Parameter validation
  assert(diameter > 0, "Diameter must be positive");
  assert(height > 0, "Height must be positive");
  assert(wall > 0, "Wall thickness must be positive");
  assert(distance >= 0, "Distance between standoffs must be non-negative");
  assert(offset >= -diameter / 2, "Offset too negative - would create negative diameter");
  assert(front_chamfer >= 0, "Front chamfer must be non-negative");
  assert(outer_facets >= 3, "Outer facets must be at least 3");
  assert(inner_facets >= 3 || inner_facets == -1, "Inner facets must be at least 3, or -1 to use outer_facets");

  // Calculate spacing using helper function
  dx = calc_holder_spacing(distance, wall, diameter);

  translate([-dx, 0, 0])
  Standoff_Holder(
    diameter = diameter,
    wall = wall,
    height = height,
    offset = offset,
    front_flat = front_flat,
    front_chamfer = front_chamfer,
    outer_facets = outer_facets,
    inner_facets = inner_facets);

  translate([dx, 0, 0])
  Standoff_Holder(
    diameter = diameter,
    wall = wall,
    height = height,
    offset = offset,
    front_flat = front_flat,
    front_chamfer = front_chamfer,
    outer_facets = outer_facets,
    inner_facets = inner_facets);
}

// Test code - only shown in preview mode
if ($preview) {
  Standoff_Holder_Pair(
    diameter = 4,
    wall = 1,
    distance = 4,
    height = 20,
    offset = 0.2,
    front_flat = true,
    front_chamfer = 0,
    outer_facets = 50,
    inner_facets = 6
  );
}