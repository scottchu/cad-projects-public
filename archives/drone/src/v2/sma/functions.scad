include <spec.scad>
include <../functions/right_triangle.scad>

//! Check if there's sufficient space for SMA connector
//! @param available_width Available width for SMA connector placement
//! @returns true if space is sufficient, false otherwise
function has_sufficient_sma_space(available_width) =
  available_width > SMA_DIAMETER_REQUIRED;

//! Calculate wall geometry components accounting for surface angle
//! Returns the horizontal, vertical, and diagonal components of wall thickness
//! @param wall_thickness Horizontal wall thickness
//! @param surface_angle Angle of the sloped surface in degrees
//! @returns [horizontal_component, vertical_component, diagonal_component]
//!   - horizontal_component: Original wall thickness (a)
//!   - vertical_component: Vertical rise due to angle (b)
//!   - diagonal_component: Actual wall thickness along angled surface (c, hypotenuse)
function calculate_angled_wall_components(wall_thickness, surface_angle) =
  [
    wall_thickness, // a: horizontal wall thickness
    calc_opposite_from_adjacent(wall_thickness, surface_angle), // b: vertical component
    calc_hypotenuse(wall_thickness, calc_opposite_from_adjacent(wall_thickness, surface_angle)), // c: diagonal (hypotenuse)
  ];

//! Calculate the Y coordinate of the center point on a sloped surface
//! Used for positioning SMA holes on the angled top surface of the mount
//! @param mount_length Total length of the mount
//! @param top_flat_length Length of flat section at the top (before slope starts)
//! @param wall_thickness Wall thickness
//! @param slope_angle Angle of the sloped surface in degrees
//! @returns Y coordinate of the center point on the sloped surface
function get_sloped_surface_center_y(mount_length, top_flat_length, wall_thickness, slope_angle) =
  let (
    sloped_section_length = mount_length - top_flat_length - wall_thickness,
    sloped_section_height = calc_opposite_from_adjacent(sloped_section_length, slope_angle),
    sloped_section_diagonal = calc_hypotenuse(sloped_section_length, sloped_section_height),
    half_diagonal = sloped_section_diagonal / 2
  ) calc_adjacent_from_hypotenuse(half_diagonal, slope_angle);
