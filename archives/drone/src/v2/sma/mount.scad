//! SMA Antenna Mount Module
//!
//! This module creates a dual SMA antenna mount with standoff holders for frame attachment.
//! The mount features an angled top surface for optimal antenna positioning.
//!
//! Module Hierarchy:
//!   - SMA_Mount_Dual: Complete assembly (top level)
//!     ├── Standoff_Holder_Pair: Frame attachment points
//!     └── SMA_Mount_Base: Hollow angled mount
//!         └── SMA_Mount_BaseShape: Solid angled shape (base geometry)
//!
//! Key Features:
//!   - Angled top surface (typically 30°) for antenna positioning
//!   - Dual SMA connector holes with configurable spacing
//!   - Standoff holders for frame attachment
//!   - Preview mode optimization for faster rendering
//!   - Comprehensive parameter validation
//!
//! Dependencies:
//!   - BOSL2 library for primitives and chamfering
//!   - right_triangle.scad for geometry calculations
//!   - standoff/holder.scad for frame attachment
//!   - spec.scad for SMA specifications
//!   - hole.scad for SMA_Hole module
//!   - functions.scad for utility functions

include <BOSL2/std.scad>

include <../functions/right_triangle.scad>
use <../standoff/holder.scad>

include <spec.scad>
use <hole.scad>
use <functions.scad>

// Constants
EPSILON = 0.01; // Small value for boolean operation clearance
EPSILON_LARGE = 0.02; // Larger clearance value
DEFAULT_BOTTOM_CHAMFER = 0.5; // Default chamfer for bottom edges

//! Creates a solid angled mount base shape
//! @param width Width of the mount
//! @param length Length of the mount
//! @param height Height of the mount
//! @param top_flat_length Length of flat section at the top (before angle starts)
//! @param angle Angle of the sloped surface in degrees
//! @param chamfer Chamfer size for bottom edges (default: 0)
//! @param top_back_chamfer Chamfer size for top-back edge (default: 0, falls back to chamfer)
//! @param top_back_chamfer_length Length of top-back chamfer (default: 0)
//! @param label Label for error messages (default: "")
module SMA_Mount_BaseShape(
  width,
  length,
  height,
  top_flat_length,
  angle,
  chamfer = 0,
  top_back_chamfer = 0,
  top_back_chamfer_length = 0,
  label = ""
) {
  // Parameter validation
  assert(width > 0, str("Width must be positive for ", label));
  assert(length > 0, str("Length must be positive for ", label));
  assert(height > 0, str("Height must be positive for ", label));
  assert(top_flat_length >= 0 && top_flat_length < length, str("top_flat_length must be between 0 and length for ", label));
  assert(angle > 0 && angle < 90, str("Angle must be between 0 and 90 degrees for ", label));
  assert(chamfer >= 0, str("Chamfer must be non-negative for ", label));
  assert(top_back_chamfer >= 0, str("top_back_chamfer must be non-negative for ", label));

  sloped_section_length = length - top_flat_length;
  sloped_section_height = calc_opposite_from_adjacent(sloped_section_length, angle);
  base_height = height - sloped_section_height;
  max_angle = calc_angle_from_sides(height, sloped_section_length);

  assert(angle <= max_angle, str("Angle for ", label, " is too large, max angle is ", max_angle));

  final_chamfer = top_back_chamfer > 0 ? top_back_chamfer : chamfer;

  difference() {
    diff()
      cuboid(
        size=[width, length, height],
        anchor=BOTTOM
      ) {
        if (top_back_chamfer_length > 0 && final_chamfer > 0) {
          edge_mask(TOP + BACK)
            chamfer_edge_mask(l=top_back_chamfer_length, chamfer=final_chamfer);
        }

        if (chamfer > 0) {
          edge_mask([BOTTOM + FRONT, BOTTOM + LEFT, BOTTOM + RIGHT])
            chamfer_edge_mask(l=width, chamfer=DEFAULT_BOTTOM_CHAMFER);
        }
      }
    ;

    translate([0, -length / 2 - EPSILON, base_height + EPSILON])
      wedge(
        size=[width + EPSILON, sloped_section_length + EPSILON, sloped_section_height + EPSILON_LARGE],
        anchor=TOP + FRONT,
        orient=DOWN
      );
  }
  ;
}

//! Creates a hollow mount base with walls (like a box with angled top)
//! @param width Width of the mount
//! @param length Length of the mount
//! @param height Height of the mount
//! @param top_flat_length Length of flat section at top (default: 2)
//! @param angle Angle of sloped surface in degrees (default: 30)
//! @param thickness Wall thickness (default: 1.5)
//! @param wall Side wall thickness (default: 1.5)
//! @param chamfer Chamfer size for bottom edges (default: 0)
//! @param top_back_chamfer Chamfer size for top-back edge (default: 0)
//! @param top_back_chamfer_length Length of top-back chamfer (default: 0)
//! @param enable_side_access If true, removes one side wall for access (default: false)
module SMA_Mount_Base(
  width,
  length,
  height,
  top_flat_length = 2,
  angle = 30,
  thickness = 1.5,
  wall = 1.5,
  chamfer = 0,
  top_back_chamfer = 0,
  top_back_chamfer_length = 0,
  enable_side_access = false
) {
  // Parameter validation
  assert(width > 0, "Width must be positive");
  assert(length > 0, "Length must be positive");
  assert(height > 0, "Height must be positive");
  assert(thickness > 0, "Thickness must be positive");
  assert(wall > 0, "Wall thickness must be positive");
  assert(thickness < width / 2, "Thickness must be less than half the width");
  assert(wall < width / 2, "Wall thickness must be less than half the width");

  final_chamfer = top_back_chamfer > 0 ? top_back_chamfer : chamfer;
  final_chamfer_length = top_back_chamfer_length > 0 ? top_back_chamfer_length : width;

  difference() {
    SMA_Mount_BaseShape(
      width=width,
      length=length,
      height=height,
      top_flat_length=top_flat_length,
      angle=angle,
      chamfer=chamfer,
      top_back_chamfer=final_chamfer,
      top_back_chamfer_length=final_chamfer_length,
      label="outer BaseShape"
    );

    wall_components = calculate_angled_wall_components(thickness, angle);
    wall_horizontal = wall_components[0];
    wall_vertical = wall_components[1];
    wall_diagonal = wall_components[2];

    inner_width = width - wall * 2;
    inner_length = length - wall_diagonal;
    inner_height = height - wall_diagonal;

    translate([0, wall_diagonal / 2 + EPSILON, -EPSILON])
      SMA_Mount_BaseShape(
        width=inner_width,
        length=inner_length,
        height=inner_height,
        top_flat_length=top_flat_length,
        angle=angle,
        label="inner BaseShape"
      );

    if (enable_side_access == true) {
      translate([-(width - wall) / 2, 0, -EPSILON])
        cuboid(size=[wall + EPSILON_LARGE, length + EPSILON_LARGE, height + EPSILON_LARGE], anchor=BOTTOM);
    }
  }
}

//! Creates a complete dual SMA antenna mount with standoff holders
//! This is the main module that combines the mount base with standoff holders and SMA connector holes
//! @param width Mount width (use negative for auto-calc from standoffs)
//! @param length Mount length
//! @param height Mount height (use negative to use standoff_height)
//! @param distance Distance between SMA connector centers
//! @param top_flat_length Length of flat section at top (default: 2)
//! @param angle Angle of sloped surface in degrees (default: 30)
//! @param thickness Wall thickness (default: 1.5)
//! @param wall Side wall thickness (default: 1.5)
//! @param chamfer Chamfer size for bottom edges (default: 0)
//! @param top_back_chamfer Chamfer size for top-back edge (default: 0)
//! @param top_back_chamfer_length Length of top-back chamfer (default: 0)
//! @param enable_side_access If true, removes one side wall (default: false)
//! @param standoff_diameter Diameter of frame standoffs
//! @param standoff_wall Wall thickness around standoffs
//! @param standoff_height Height of standoff holders
//! @param standoff_distance Distance between standoff centers
//! @param standoff_offset Additional offset for standoff fit (default: 0)
//! @param standoff_front_flat If true, creates flat front face on standoffs (default: false)
//! @param standoff_front_chamfer Chamfer for standoff front face (default: 0)
//! @param standoff_outer_facets Number of sides for standoff outer shape (default: 10)
//! @param standoff_inner_facets Number of sides for standoff inner hole (default: -1, uses outer_facets)
//! @param sma_fn Number of facets for SMA holes (default: 10, optimized in preview)
//! @param sma_position_y_offset Y-axis offset for SMA hole positioning (default: 0)
//! @param show_sma_clearance If true, shows visualization of required clearance (default: false)
module SMA_Mount_Dual(
  width,
  length,
  height,
  distance,
  top_flat_length = 2,
  angle = 30,
  thickness = 1.5,
  wall = 1.5,
  chamfer = 0,
  top_back_chamfer = 0,
  top_back_chamfer_length = 0,
  enable_side_access = false,
  standoff_diameter,
  standoff_wall,
  standoff_height,
  standoff_distance,
  standoff_offset = 0,
  standoff_front_flat = false,
  standoff_front_chamfer = 0,
  standoff_outer_facets = 10,
  standoff_inner_facets = -1,
  sma_fn = 10,
  sma_position_y_offset = 0,
  show_sma_clearance = false
) {
  // Parameter validation
  assert(has_sufficient_sma_space(width - distance), "Not enough space for SMA");
  assert(width > 0 || width < 0, "Width must be positive or negative (for auto-calc)");
  assert(length > 0, "Length must be positive");
  assert(distance > 0, "Distance between SMA connectors must be positive");
  assert(angle > 0 && angle < 90, "Angle must be between 0 and 90 degrees");
  assert(thickness > 0, "Thickness must be positive");
  assert(wall > 0, "Wall thickness must be positive");
  assert(standoff_diameter > 0, "Standoff diameter must be positive");
  assert(standoff_wall > 0, "Standoff wall thickness must be positive");
  assert(standoff_height > 0, "Standoff height must be positive");
  assert(standoff_distance > 0, "Standoff distance must be positive");
  assert(sma_fn > 0, "SMA $fn must be positive");
  assert(standoff_outer_facets > 0, "Standoff outer facets must be positive");

  // Optimize detail for preview mode (faster preview, full detail for render)
  is_preview_mode = $preview;
  preview_standoff_outer_facets = is_preview_mode ? max(6, standoff_outer_facets / 4) : standoff_outer_facets;
  preview_standoff_inner_facets = is_preview_mode && standoff_inner_facets > 0 ? max(6, standoff_inner_facets / 4) : standoff_inner_facets;
  preview_sma_fn = is_preview_mode ? max(8, sma_fn / 4) : sma_fn;

  actual_height = height < 0 ? standoff_height : height;

  sloped_surface_center_y = get_sloped_surface_center_y(length, top_flat_length, thickness, angle);

  Standoff_Holder_Pair(
    diameter=standoff_diameter,
    wall=standoff_wall,
    height=standoff_height,
    distance=standoff_distance,
    offset=standoff_offset,
    front_flat=standoff_front_flat,
    front_chamfer=standoff_front_chamfer,
    outer_facets=preview_standoff_outer_facets,
    inner_facets=preview_standoff_inner_facets
  );

  // Helper module to create SMA hole cutout on angled surface
  module cut_sma_hole(x_position) {
    rotate([angle, 0, 0])
      translate([x_position, -sloped_surface_center_y + sma_position_y_offset, actual_height - thickness + SMA_HOLE_Z_OFFSET])
        // Make cylinder tall enough to cut through the angled surface
        SMA_Hole(
          height=thickness + SMA_HOLE_HEIGHT_CLEARANCE + 2,
          $fn=preview_sma_fn,
          show_teeth_disk=show_sma_clearance
        );
  }

  difference() {
    translate([0, -(length + standoff_diameter) / 2, 0])
      SMA_Mount_Base(
        width=width,
        length=length,
        height=actual_height,
        top_flat_length=top_flat_length,
        angle=angle,
        thickness=thickness,
        wall=wall,
        chamfer=chamfer,
        top_back_chamfer=top_back_chamfer,
        top_back_chamfer_length=top_back_chamfer_length,
        enable_side_access=enable_side_access
      );

    cut_sma_hole((distance + SMA_SPACING_OFFSET) / 2);
    cut_sma_hole(-(distance + SMA_SPACING_OFFSET) / 2);
  }
}

SMA_Mount_Dual(
  width=30,
  length=15,
  height=10,
  distance=6,
  angle=30,
  thickness=2,
  top_back_chamfer=1,
  standoff_diameter=4.5,
  standoff_wall=2,
  standoff_height=10,
  standoff_distance=14.5,
  sma_fn=50,
  show_sma_clearance=false,
  sma_position_y_offset=-0.2,
  standoff_outer_facets=50
);
