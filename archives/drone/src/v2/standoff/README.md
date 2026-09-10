# Standoff Module System

## Overview

The standoff module system provides components for creating holders that attach to frame standoffs in drone designs. Standoffs are cylindrical posts on drone frames used for mounting components.

## Module Hierarchy

```
Standoff (standoff.scad)
  └── Basic cylinder representing a standoff post

Standoff_Holder (holder.scad)
  └── Wraps around Standoff, creates hollow holder
      └── Optional flat front face

Standoff_Holder_Pair (holder.scad)
  └── Two Standoff_Holders positioned at specified distance

Standoff_CurvedHolder (curved-holder.scad)
  └── Curved holder connecting two standoffs with a curved path
```

## Files

### `standoff.scad` - Basic Standoff

**Purpose**: Creates a simple cylindrical standoff representation.

**Module**: `Standoff()`

**Parameters**:
- `diameter` - Diameter of the standoff
- `height` - Height of the standoff
- `diameter_offset` - Additional diameter offset (default: 0)
- `anchor` - BOSL2 anchor position (default: BOTTOM)

**Usage**:
```scad
Standoff(diameter=5, height=20, diameter_offset=0.2);
```

**Notes**:
- Simple wrapper around BOSL2 `cylinder()`
- Used as a building block for holders
- Test code creates a hexagonal standoff ($fn=6)

---

### `holder.scad` - Standoff Holders

**Purpose**: Creates holders that wrap around frame standoffs, allowing components to attach to the frame.

#### `Standoff_Holder` Module

Creates a single standoff holder - a hollow cylinder that fits around a standoff post.

**Parameters**:
- `diameter` - Inner diameter (standoff diameter)
- `height` - Height of the holder
- `wall` - Wall thickness around standoff (default: 1)
- `anchor` - BOSL2 anchor position (default: BOTTOM)
- `offset` - Additional offset for fit tolerance (default: 0)
- `front_flat` - If true, creates flat front face (default: false)
- `front_chamfer` - Chamfer size for front face (default: 0)
- `outer_facets` - Number of sides for outer shape (default: 10)
- `inner_facets` - Number of sides for inner hole (default: -1, uses outer_facets)

**Design**:
- Outer cylinder: `diameter + (wall * 2) + offset`
- Inner hole: `diameter + offset` (for standoff clearance)
- Optional flat front face for aesthetic/functional purposes

**Usage**:
```scad
Standoff_Holder(
  diameter=5,
  height=10,
  wall=2,
  offset=0.2,
  front_flat=true,
  front_chamfer=1
);
```

#### `Standoff_Holder_Pair` Module

Creates a pair of standoff holders positioned at a specified distance apart.

**Parameters**:
- `diameter` - Inner diameter (standoff diameter)
- `height` - Height of the holders
- `wall` - Wall thickness around standoffs
- `distance` - Distance between standoff centers (default: 0)
- `anchor` - BOSL2 anchor position (default: BOTTOM)
- `offset` - Additional offset for fit tolerance (default: 0)
- `front_flat` - If true, creates flat front faces (default: false)
- `front_chamfer` - Chamfer size for front faces (default: 0)
- `outer_facets` - Number of sides for outer shape (default: 10)
- `inner_facets` - Number of sides for inner holes (default: -1, uses outer_facets)

**Design**:
- Calculates X offset: `(distance + wall * 2 + diameter) / 2`
- Positions two `Standoff_Holder` modules symmetrically

**Usage**:
```scad
Standoff_Holder_Pair(
  diameter=4.5,
  height=10,
  wall=2,
  distance=14.5,
  offset=0.2
);
```

**Common Use Case**: Frame attachment points for mounts (e.g., SMA mount, GPS mount)

---

### `curved-holder.scad` - Curved Standoff Holder

**Purpose**: Creates a curved holder that connects two standoffs with a curved path, useful for non-linear frame designs.

**Module**: `Standoff_CurvedHolder()`

**Parameters**:
- `diameter` - Inner diameter (standoff diameter)
- `wall` - Wall thickness around standoff
- `height` - Height of the holder
- `offset` - Additional offset for fit tolerance (default: 0.02)
- `outer_facets` - Number of sides for outer shape (default: 6)
- `inner_facets` - Number of sides for inner hole (default: 50)
- `curve_x` - X offset for curved path
- `curve_y` - Y offset for curved path
- `connect_width` - Width of connecting section
- `connect_length` - Length of connecting section

**Design**:
- Uses BOSL2 `conv_hull()` to create a convex hull connecting:
  1. Main standoff cylinder
  2. Curved standoff cylinder (at curve_x, curve_y)
  3. Connecting cuboid
- Subtracts inner hole for standoff clearance
- Creates smooth curved transition between standoffs

**Usage**:
```scad
Standoff_CurvedHolder(
  diameter=5,
  wall=1,
  height=10,
  curve_x=2,
  curve_y=-1,
  connect_width=2,
  connect_length=4
);
```

**Notes**:
- Contains commented-out code for alternative connection methods
- Uses `diff()` and `conv_hull()` from BOSL2 for advanced geometry

---

## Design Patterns

### 1. **Hollow Cylinder Pattern**
Holders use `difference()` to create hollow cylinders:
- Outer cylinder: Standoff diameter + wall thickness
- Inner cylinder: Standoff diameter (for clearance)

### 2. **Optional Features**
- Flat front faces for aesthetic/functional purposes
- Chamfered edges for better appearance
- Configurable polygon count ($fn) for quality vs. performance

### 3. **Tolerance Management**
- `offset` parameter allows fine-tuning fit
- `d = 0.02` epsilon value for clean boolean operations

### 4. **Symmetry**
`Standoff_Holder_Pair` uses symmetric positioning for balanced designs

---

## Dependencies

- **BOSL2**: Required for primitives (`cylinder`, `cuboid`, `conv_hull`, `diff`)
- **standoff.scad**: Required by holder.scad and curved-holder.scad

---

## Usage in Other Modules

The standoff system is used by:
- `sma/mount.scad` - Uses `Standoff_Holder_Pair` for frame attachment
- Other mount modules that need to attach to frame standoffs

---

## Key Concepts

### Standoff vs. Holder
- **Standoff**: The actual post on the drone frame (hardware)
- **Holder**: The 3D printed part that wraps around the standoff

### Wall Thickness
The `wall` parameter determines how thick the holder material is around the standoff. This affects:
- Strength of the holder
- Printability
- Weight

### Offset/Tolerance
The `offset` parameter allows fine-tuning the fit:
- Positive values: Looser fit (easier to slide on)
- Negative values: Tighter fit (more secure)
- Zero: Nominal fit

---

## Example Workflow

1. **Measure frame standoffs**: Get diameter and spacing
2. **Choose holder type**: Single, pair, or curved
3. **Set parameters**: Match frame dimensions
4. **Adjust tolerance**: Fine-tune `offset` for fit
5. **Integrate**: Use in mount designs

---

## Testing

Each file includes test code at the bottom that demonstrates usage:
- `standoff.scad`: Creates a hexagonal standoff
- `holder.scad`: Creates a pair of holders with flat front
- `curved-holder.scad`: Creates a curved holder connecting two standoffs
