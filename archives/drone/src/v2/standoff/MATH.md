# Mathematics and Calculations in Standoff Modules

This document explains all mathematical formulas and calculations used in the standoff module system.

---

## 1. Basic Geometry Calculations

### 1.1 Outer Diameter Calculation
**Location:** `functions.scad::calc_outer_diameter()`

**Formula:**
```
outer_diameter = standoff_diameter + (wall × 2) + offset
```

**Explanation:**
- `standoff_diameter`: Inner diameter (the actual standoff post size)
- `wall × 2`: Wall thickness on both sides (left and right)
- `offset`: Additional tolerance/clearance for fit

**Example:**
- Standoff diameter: 5mm
- Wall thickness: 1mm
- Offset: 0.2mm
- **Result:** `5 + (1 × 2) + 0.2 = 7.2mm`

**Usage:**
- Used in `holder.scad` to calculate outer cylinder size
- Used in `curved-holder.scad` to calculate outer cylinder size

---

### 1.2 Radius from Diameter
**Location:** `curved-holder.scad` (line 66)

**Formula:**
```
radius = diameter / 2
```

**Explanation:**
- Standard conversion from diameter to radius
- Used for positioning calculations

**Example:**
- Outer diameter: 7.2mm
- **Result:** `7.2 / 2 = 3.6mm`

---

## 2. Holder Spacing Calculations

### 2.1 Pair Holder Spacing
**Location:** `functions.scad::calc_holder_spacing()`

**Formula:**
```
dx = (distance + wall × 2 + diameter) / 2
```

**Explanation:**
- `distance`: Distance between standoff centers (frame spacing)
- `wall × 2`: Wall thickness on both sides of each holder
- `diameter`: Standoff diameter
- Result is divided by 2 to get offset from center (symmetrical positioning)

**Visual Representation:**
```
     [Holder 1]     [Holder 2]
         |              |
    ─────┴───────┴──────┴──────
    -dx    0    +dx

    Total span = distance + wall×2 + diameter
    Offset from center = total_span / 2
```

**Example:**
- Distance between centers: 14.5mm
- Wall thickness: 2mm
- Standoff diameter: 4.5mm
- **Result:** `(14.5 + 2×2 + 4.5) / 2 = 23 / 2 = 11.5mm`

**Usage:**
- Used in `Standoff_Holder_Pair` to position two holders symmetrically

---

## 3. Preview Mode Optimization

### 3.1 Facet Count Reduction
**Location:** `holder.scad` (lines 51-53), `curved-holder.scad` (lines 61-62)

**Formula:**
```
preview_facets = is_preview ? max(6, facets / 4) : facets
```

**Explanation:**
- In preview mode: Reduce facet count by 4x (divide by 4)
- Minimum: Always keep at least 6 facets for visibility
- In render mode: Use full facet count for quality

**Example:**
- Full quality: 50 facets
- Preview mode: `max(6, 50/4) = max(6, 12.5) = 12.5 → 13 facets`
- Render mode: 50 facets

**Benefits:**
- Faster preview rendering
- Maintains visual quality (still looks circular)
- Full quality in final render

---

### 3.2 Inner Facets Fallback
**Location:** `holder.scad` (line 52)

**Formula:**
```
final_inner_facets = inner_facets < 0 ? outer_facets : inner_facets
```

**Explanation:**
- Special value `-1` means "use outer facets"
- If `inner_facets = -1`, use `outer_facets` instead
- Otherwise, use the specified `inner_facets` value

**Example:**
- `outer_facets = 10`, `inner_facets = -1`
- **Result:** `final_inner_facets = 10`

---

## 4. Boolean Operation Clearance

### 4.1 EPSILON Usage
**Location:** `constants.scad`, used in `holder.scad` (line 83)

**Formula:**
```
translation_z = -EPSILON / 2
hole_height = height + EPSILON
```

**Explanation:**
- `EPSILON = 0.02mm`: Small clearance value for boolean operations
- Subtracting cylinder is translated down by `EPSILON/2` to ensure clean cut
- Height is increased by `EPSILON` to ensure complete penetration

**Visual Representation:**
```
    ┌─────────────┐
    │   Holder    │  height
    └─────────────┘
         ││││││││││  ← Inner hole (subtracted)
    ─────┴┴┴┴┴┴┴┴┴────  ← Extended by EPSILON below
```

**Purpose:**
- Prevents rendering artifacts from floating-point precision
- Ensures clean boolean subtraction
- Standard practice in CAD modeling

---

## 5. Curved Holder Calculations

### 5.1 Connection Point Position
**Location:** `curved-holder.scad` (lines 70-71)

**Formula:**
```
connect_point_x = -connect_width / 2 + or + curve_x
connect_point_y = -connect_length - or
```

**Explanation:**
- `connect_point_x`: X position of connecting cuboid
  - `-connect_width / 2`: Center the cuboid width
  - `+ or`: Offset by outer radius to align with cylinder edge
  - `+ curve_x`: Additional curve offset
- `connect_point_y`: Y position of connecting cuboid
  - `-connect_length`: Position at negative Y (backward)
  - `- or`: Offset by outer radius to align with cylinder edge

**Visual Representation:**
```
         Main Standoff
              │
              ● (0, 0)
              │
              │ connect_point
              │     │
              └─────┼─────┐
                    │     │ Connecting
                    │     │ Cuboid
                    └─────┘

                    ● (curve_x, curve_y)
                    │
              Curved Standoff
```

**Example:**
- Outer radius: 3.6mm
- Connect width: 2mm
- Connect length: 4mm
- Curve X: 2mm
- **Result:**
  - `connect_point_x = -2/2 + 3.6 + 2 = 4.6mm`
  - `connect_point_y = -4 - 3.6 = -7.6mm`

---

## 6. Front Flat Face Dimensions
**Location:** `holder.scad` (lines 70-73)

**Formula:**
```
size = [
  outer_diameter,                    // X: Full outer diameter
  diameter / 2 + wall + offset,     // Y: Half diameter + wall + tolerance
  height                             // Z: Full height
]
```

**Explanation:**
- **X dimension:** Full outer diameter (matches cylinder)
- **Y dimension:** Half the inner diameter plus wall and offset
  - Creates a flat face that extends from center to outer edge
  - `diameter / 2` = radius of inner hole
  - `+ wall + offset` = extends to outer edge
- **Z dimension:** Full height (matches cylinder)

**Visual Representation:**
```
    Side View:
    ┌─────────────┐
    │             │
    │      ●      │  ← Standoff hole
    │   ┌───┐     │  ← Flat front face
    │   │   │     │
    └───┴───┴─────┘
```

**Example:**
- Inner diameter: 5mm
- Wall: 1mm
- Offset: 0.2mm
- Outer diameter: 7.2mm
- **Result:**
  - X: `7.2mm`
  - Y: `5/2 + 1 + 0.2 = 3.7mm`
  - Z: `height`

---

## 7. Parameter Validation Math

### 7.1 Offset Validation
**Location:** Multiple modules

**Formula:**
```
assert(offset >= -diameter / 2, "Offset too negative")
```

**Explanation:**
- Prevents offset from making diameter negative
- Minimum allowed: `offset = -diameter / 2`
- At this limit: `diameter + offset = diameter - diameter/2 = diameter/2`

**Example:**
- Diameter: 5mm
- Minimum offset: `-5/2 = -2.5mm`
- At limit: `5 + (-2.5) = 2.5mm` (still positive)

---

## 8. Summary of Key Formulas

| Calculation | Formula | Location |
|------------|---------|----------|
| **Outer Diameter** | `diameter + (wall × 2) + offset` | `functions.scad` |
| **Radius** | `diameter / 2` | `curved-holder.scad` |
| **Holder Spacing** | `(distance + wall×2 + diameter) / 2` | `functions.scad` |
| **Preview Facets** | `max(6, facets / 4)` | `holder.scad`, `curved-holder.scad` |
| **Final Diameter** | `diameter + diameter_offset` | `standoff.scad` |
| **Connection X** | `-width/2 + radius + curve_x` | `curved-holder.scad` |
| **Connection Y** | `-length - radius` | `curved-holder.scad` |
| **Flat Face Y** | `diameter/2 + wall + offset` | `holder.scad` |

---

## 9. Constants Used

| Constant | Value | Purpose |
|----------|-------|---------|
| `EPSILON` | 0.02mm | Boolean operation clearance |
| `DEFAULT_WALL_THICKNESS` | 1mm | Default wall thickness |
| `DEFAULT_OUTER_FACETS` | 10 | Default outer facet count |
| `DEFAULT_INNER_FACETS` | -1 | Special value (use outer) |
| `DEFAULT_CURVED_OUTER_FACETS` | 6 | Curved holder outer facets |
| `DEFAULT_CURVED_INNER_FACETS` | 50 | Curved holder inner facets |
| `DEFAULT_PREVIEW_FACETS` | 60 | Preview mode default |
| `DEFAULT_OFFSET` | 0.02mm | Default fit tolerance |

---

## 10. Design Principles

### 10.1 Tolerance Stacking
All dimensions account for:
1. **Base dimension** (standoff diameter)
2. **Wall thickness** (material thickness)
3. **Fit tolerance** (offset for assembly clearance)

### 10.2 Symmetry
- `Standoff_Holder_Pair` uses symmetric positioning
- Spacing calculation ensures equal distance from center
- Both holders are identical

### 10.3 Preview Optimization
- Facet count reduced by 4x in preview
- Minimum 6 facets maintained for visibility
- Full quality in render mode

### 10.4 Boolean Safety
- EPSILON ensures clean cuts
- Subtracted objects extended beyond boundaries
- Prevents floating-point precision issues

---

## 11. Example Calculations

### Example 1: Standard Holder
**Input:**
- Standoff diameter: 5mm
- Wall: 1mm
- Offset: 0.2mm
- Height: 10mm

**Calculations:**
1. Outer diameter: `5 + (1×2) + 0.2 = 7.2mm`
2. Inner hole diameter: `5 + 0.2 = 5.2mm`
3. Inner hole height: `10 + 0.02 = 10.02mm`

### Example 2: Holder Pair
**Input:**
- Standoff diameter: 4.5mm
- Wall: 2mm
- Distance: 14.5mm

**Calculations:**
1. Spacing offset: `(14.5 + 2×2 + 4.5) / 2 = 11.5mm`
2. Holders positioned at: `-11.5mm` and `+11.5mm` from center

### Example 3: Curved Holder
**Input:**
- Standoff diameter: 5mm
- Wall: 1mm
- Offset: 0.2mm
- Curve: (2mm, -1mm)
- Connect: 2mm × 4mm

**Calculations:**
1. Outer diameter: `5 + (1×2) + 0.2 = 7.2mm`
2. Outer radius: `7.2 / 2 = 3.6mm`
3. Connection X: `-2/2 + 3.6 + 2 = 4.6mm`
4. Connection Y: `-4 - 3.6 = -7.6mm`

---

## 12. Notes

- All calculations use standard geometric formulas
- Dimensions are in millimeters (OpenSCAD default)
- Boolean operations use EPSILON for safety
- Preview optimization balances speed and quality
- Formulas are designed for manufacturability and fit tolerance
