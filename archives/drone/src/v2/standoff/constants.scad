//! Standoff Module Constants
//!
//! This file contains shared constants used across standoff modules.
//! File-specific constants should remain in their respective files.

// Boolean Operations
EPSILON = 0.02; // Small value for boolean operation clearance

// Default Dimensions
DEFAULT_WALL_THICKNESS = 1; // Default wall thickness around standoff

// Default Facet Counts
DEFAULT_OUTER_FACETS = 10; // Default number of sides for outer shape
DEFAULT_INNER_FACETS = -1; // Special value: -1 means use outer facets

// Curved Holder Specific Constants
DEFAULT_CURVED_OUTER_FACETS = 6; // Default outer facets for curved holder (lower for performance)
DEFAULT_CURVED_INNER_FACETS = 50; // Default inner facets for curved holder (higher for smooth hole)
DEFAULT_PREVIEW_FACETS = 60; // Default facet count for preview mode

// Tolerance Constants
DEFAULT_OFFSET = 0.02; // Default offset for fit tolerance
