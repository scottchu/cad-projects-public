# P0 optics fixture physical test plan

Status: CAD implementation frozen for independent review. Physical behavior is not yet approved.

## Print

- Print the pedestal/mask as a closed CAD solid with **8% gyroid infill**, 3 walls, 0.20 mm layers.
- Print all three hands flat, 0.20 mm layers, 4 walls, no support.
- Do not scale any part: the three arbor journals and local hub pads are fit-critical.

## Gate 1 — hub fit

1. Install hour, minute, second in that order on the Ø8/Ø6/Ø4 journals.
2. Each hand must rotate by finger force without splitting or permanent whitening.
3. Turn the fixture vertical and shake gently. No hand may fall off.
4. Cycle every hand 30 full turns. Record looseness, binding, and cracks.
5. If tuning is needed, change only relief-bore or pad protrusion. Do not add a retaining bead/cap.

## Gate 2 — geometry

1. Verify the hand centers sit on the three lands without touching adjacent hands.
2. Confirm axial gaps remain visible through a full rotation.
3. Verify only one tapered rounded blade is present on each hub—no ring, X, star, or spoke shadow.

## Gate 3 — optical bench

1. Put the rear Ø80 face against the wall datum; the Ø111.1429 mask face is 60 mm from the wall.
2. Place the thin-aperture LED source on-axis at z=44.8 mm from the mask.
3. Keep the LED on a metal heatsink and use a compatible constant-current driver.
4. Photograph each hand separately and together. Measure projected tip radius and edge softness.
5. Expected projected radii: hour 144.22 mm, minute 176.35 mm, second 224.95 mm.
6. Reject if the arbor/pedestal casts an unexpected noncentral silhouette or if any hub/slit feature becomes visible outside the central mask shadow.

## Safety boundary

The printed pedestal is not a heatsink. Keep the LED, driver, wiring, and thermal path external and accessible during P0.
