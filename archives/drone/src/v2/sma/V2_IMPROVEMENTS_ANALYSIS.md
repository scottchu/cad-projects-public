# V2 SMA Mount - Design & Render Efficiency Improvements

## Current Design Analysis

### Strengths
✅ Modular three-level hierarchy
✅ Mathematically precise geometry
✅ Good validation and error checking
✅ Flexible parameter system

### Areas for Improvement

---

## 1. Render Efficiency Issues

### Issue 1: Redundant Calculations
**Current**: Variables `mh` and `ml` are calculated but never used
```scad
mh = RT_calc_a_with_b_alpha(c, angle);
ml = RT_calc_c_with_a_b(c, mh);
```
**Impact**: Unnecessary computation on every render

**Fix**: Remove unused variables

### Issue 2: Multiple `diff()` Operations
**Current**: `SMA_Mount_BaseShape` uses `diff()` for chamfering, then `difference()` for wedge
```scad
diff() cuboid(...) { chamfer edges };
difference() { ... wedge(...) };
```
**Impact**: BOSL2's `diff()` can be slower than native OpenSCAD operations

**Consideration**: `diff()` is cleaner but may be slower. Test performance vs. manual chamfering.

### Issue 3: High `$fn` Values in Preview
**Current**: No preview optimization for `sma_fn` and `standoff_ofn`
```scad
sma_fn = 10;  // Could be 60 in final render
standoff_ofn = 10;  // Could be 50 in final render
```
**Impact**: Slow preview when high detail is set

**Fix**: Add `$preview` checks for automatic detail reduction

### Issue 4: Duplicate SMA Hole Creation
**Current**: Two separate `rotate()` + `translate()` + `SMA_Hole()` calls
```scad
rotate([angle, 0, 0])
translate([(distance + 6) / 2, ...])
SMA_Hole(...);

rotate([angle, 0, 0])
translate([-(distance + 6) / 2, ...])
SMA_Hole(...);
```
**Impact**: Code duplication, harder to maintain

**Fix**: Use a loop or helper module

---

## 2. Design Improvements

### Improvement 1: Pre-calculate Common Values
**Current**: Calculations repeated in multiple places
```scad
// In SMA_Mount_Dual:
a = thickness;
b = RT_calc_a_with_b_alpha(a, angle);
c = RT_calc_c_with_a_b(a, b);
```

**Better**: Create a helper function to calculate wall geometry once
```scad
function calc_wall_geometry(thickness, angle) = [
  thickness,  // a
  RT_calc_a_with_b_alpha(thickness, angle),  // b
  RT_calc_c_with_a_b(thickness, RT_calc_a_with_b_alpha(thickness, angle))  // c
];
```

### Improvement 2: Simplify SMA Hole Positioning
**Current**: Complex 3D midpoint calculation
```scad
ma = length - flat_top - thickness;
mb = RT_calc_a_with_b_alpha(ma, angle);
mc = RT_calc_c_with_a_b(ma, mb);
mid_mc = mc / 2;
mid_mb = RT_calc_b_with_c_alpha(mid_mc, angle);
```

**Better**: Create a helper function
```scad
function calc_angled_surface_midpoint(length, flat_top, thickness, angle) =
  let(
    ma = length - flat_top - thickness,
    mb = RT_calc_a_with_b_alpha(ma, angle),
    mc = RT_calc_c_with_a_b(ma, mb),
    mid_mc = mc / 2
  )
  RT_calc_b_with_c_alpha(mid_mc, angle);
```

### Improvement 3: Extract Magic Numbers
**Current**: Hard-coded values
```scad
distance + 6  // Why 6? (SMA diameter)
height - thickness + 0.5  // Why 0.5?
```

**Better**: Use named constants or parameters
```scad
SMA_DIAMETER = 6;  // From spec
SMA_HOLE_Z_OFFSET = 0.5;  // Clearance
```

### Improvement 4: Better Parameter Validation
**Current**: Only checks `enough_space()`

**Better**: Add more validation
```scad
assert(width > 0 || width < 0, "Width must be positive or negative for auto-calc");
assert(angle > 0 && angle < 90, "Angle must be between 0 and 90 degrees");
assert(thickness > 0, "Thickness must be positive");
```

### Improvement 5: Optimize `diff()` Usage
**Current**: Uses `diff()` for chamfering

**Options**:
1. **Keep `diff()`**: Cleaner code, but potentially slower
2. **Manual chamfering**: Use `minkowski()` or manual geometry (faster but more complex)
3. **Conditional**: Use `diff()` only when chamfers are needed

**Recommendation**: Keep `diff()` but add conditional check
```scad
if (chamfer > 0 || top_back_chamfer > 0) {
  diff() cuboid(...) { chamfer edges };
} else {
  cuboid(...);
}
```

---

## 3. Code Organization Improvements

### Improvement 6: Extract Constants
Create a constants section at the top:
```scad
// Constants
SMA_DIAMETER = 6;
SMA_HOLE_CLEARANCE = 0.5;
EPSILON = 0.01;  // For boolean operations
```

### Improvement 7: Add Documentation
Add module documentation:
```scad
//! Creates an angled mount base shape
//! @param width Width of the mount
//! @param length Length of the mount
//! @param height Height of the mount
//! @param flat_top Length of flat section at top
//! @param angle Angle of the sloped surface (degrees)
module SMA_Mount_BaseShape(...) { ... }
```

### Improvement 8: Use `children()` for Flexibility
Consider making `SMA_Mount_Base` accept children for custom modifications:
```scad
module SMA_Mount_Base(...) {
  difference() {
    SMA_Mount_BaseShape(...);
    // ... existing code ...
    children();  // Allow custom cuts
  }
}
```

---

## 4. Performance Optimizations

### Optimization 1: Preview Mode Detection
```scad
// At module level
_preview = $preview;
_sma_fn = _preview ? max(8, sma_fn / 4) : sma_fn;
_standoff_ofn = _preview ? max(6, standoff_ofn / 4) : standoff_ofn;
```

### Optimization 2: Cache Calculations
For modules called multiple times, consider caching:
```scad
// In SMA_Mount_Base, cache wall geometry
_wall_geom = calc_wall_geometry(thickness, angle);
a = _wall_geom[0];
b = _wall_geom[1];
c = _wall_geom[2];
```

### Optimization 3: Simplify Boolean Operations
**Current**: Nested differences and unions

**Consider**: Flatten boolean tree where possible
- Multiple `difference()` operations can sometimes be combined
- But be careful - order matters for correct geometry

---

## 5. Proposed V2 Structure

```scad
// 1. Constants section
// 2. Helper functions
// 3. Geometry calculation functions
// 4. BaseShape module
// 5. Base module
// 6. Dual module
// 7. Test code
```

---

## Priority Recommendations

### High Priority (Easy wins, big impact)
1. ✅ Remove unused variables (`mh`, `ml`)
2. ✅ Add preview mode optimization for `$fn` values
3. ✅ Extract magic numbers to constants
4. ✅ Create helper function for SMA hole positioning

### Medium Priority (Code quality)
5. ✅ Extract wall geometry calculation to function
6. ✅ Add better parameter validation
7. ✅ Add module documentation
8. ✅ Refactor duplicate SMA hole code

### Low Priority (Performance tuning)
9. ⚠️ Test `diff()` vs manual chamfering performance
10. ⚠️ Consider caching calculations
11. ⚠️ Flatten boolean operations if beneficial

---

## Testing Strategy

1. **Visual Comparison**: Render both versions, compare visually
2. **Render Time**: Time both versions with same parameters
3. **Preview Speed**: Compare preview FPS
4. **STL File Size**: Compare output file sizes
5. **Parameter Sweep**: Test edge cases and various parameters

---

## Next Steps

1. Implement high-priority improvements
2. Test render performance
3. Compare with original
4. Iterate based on results
