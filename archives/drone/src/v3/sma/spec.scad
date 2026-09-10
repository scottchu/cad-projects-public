// SMA Connector Physical Specifications
// Source: 1/4-36 UNS standard + physical measurements with calipers
//
// Reference: standard SMA female bulkhead connector
//   Thread: 1/4-36 UNS-2B
//   Hex nut: 5/16" (Hex 8)
//   Panel cutout: 6.5-6.6mm

// --- Physical dimensions (do not change) ---

SMA_THREAD_DIAMETER = 6.35;     // 1/4-36 UNS major diameter
SMA_HOLE_DIAMETER   = 6.5;      // Standard panel cutout (6.5-6.6mm)
SMA_HEX_NUT_SIZE    = 8.0;      // Hex nut flat-to-flat (5/16" = 7.94mm ≈ 8mm)
SMA_HEX_NUT_DEPTH   = 1.0;      // Hex recess depth (starting value, tune with test print)

// Available thread lengths: 6.3 / 7.3 / 8.5 / 11 mm
// Plate thickness + boss height must be less than thread length for nut engagement.

// --- plate.scad only (boss.scad keeps hex on its bottom entry face) ---
// true: hex counterbore on the +aim side — nut visible on the outward slanted face (rear deck);
//       push bulkhead barrel through from the -aim side (frame interior / “back”).
// false: hex at boss root (-aim), legacy orientation.
SMA_PLATE_HEX_RECESS_TOWARD_ANTENNA = true;

// --- Clearance offsets (tune per material + test prints) ---
//
// Names say "TPU" for history, but these apply to whatever you are printing *now*.
// PLA (rigid): often use smaller hex clearance (e.g. 0.1–0.25) so the nut does not
// spin freely; hole can stay at 0 unless the bulkhead binds.
// TPU (flex): extra hex clearance helps the nut seat without ovalizing the pocket;
// widen hole slightly only if a flexy bore grips the barrel too hard.

SMA_TPU_HOLE_CLEARANCE = 0;     // Widen for TPU if barrel fit is too tight
SMA_TPU_HEX_CLEARANCE  = 0.5;   // Reduce for PLA if hex feels too loose (try 0.1–0.25)

// --- Derived values (used by boss.scad and downstream) ---

SMA_HOLE_D = SMA_HOLE_DIAMETER + SMA_TPU_HOLE_CLEARANCE;  // 6.5mm
// Flat-to-flat for hex pocket. Pass to BOSL2 hexagon(id=), NOT hexagon(d=):
//   d/od = corner-to-corner; id = across flats (see BOSL2 shapes2d regular_ngon).
SMA_HEX_D  = SMA_HEX_NUT_SIZE + SMA_TPU_HEX_CLEARANCE;   // e.g. 8.5mm flats + clearance
