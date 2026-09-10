//! Helper Functions for Standoff Modules
//!
//! This file contains utility functions used across standoff modules.

//! Calculate outer diameter of a standoff holder
//! @param standoff_diameter Inner diameter (standoff diameter)
//! @param wall Wall thickness around standoff
//! @param offset Additional offset for fit tolerance
//! @return Outer diameter
function calc_outer_diameter(standoff_diameter, wall, offset) =
  standoff_diameter + (wall * 2) + offset;

//! Calculate inner hole diameter with tolerance
//! @param standoff_diameter Inner diameter (standoff diameter)
//! @param offset Additional offset for fit tolerance
//! @return Inner hole diameter
function calc_inner_hole_diameter(standoff_diameter, offset) =
  standoff_diameter + offset;

//! Calculate radius from diameter
//! @param diameter Diameter
//! @return Radius
function calc_radius(diameter) = diameter / 2;

//! Calculate preview-optimized facet count
//! Reduces facet count by 4x in preview mode, maintains minimum of 6 for visibility
//! @param facets Full quality facet count
//! @param is_preview Whether in preview mode
//! @return Optimized facet count
function calc_preview_facets(facets, is_preview) =
  is_preview ? max(6, facets / 4) : facets;

//! Resolve inner facets value (handles -1 special case)
//! @param inner_facets Inner facets value (-1 means use outer_facets)
//! @param outer_facets Outer facets value to use as fallback
//! @return Resolved inner facets value
function resolve_inner_facets(inner_facets, outer_facets) =
  inner_facets < 0 ? outer_facets : inner_facets;

//! Calculate Y dimension for front flat face
//! @param outer_diameter Outer diameter of holder
//! @param offset Additional offset for fit tolerance
//! @return Y dimension for flat face
function calc_flat_face_y_dimension(outer_diameter, offset) =
  (outer_diameter + offset) / 2;

//! Calculate spacing offset for a pair of standoff holders
//! @param distance Distance between standoff centers
//! @param wall Wall thickness around standoff
//! @param diameter Standoff diameter
//! @return X offset for positioning holders
function calc_holder_spacing(distance, wall, diameter) =
  (distance + wall * 2 + diameter) / 2;
