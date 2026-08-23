# KAGE V3 roller-tower frozen architecture

- Three stationary guide towers at 60, 180, and 300 degrees.
- Each tower is one connected bar carrying three independently rotating rollers,
  one each for the hour, minute, and second rings.
- Rollers are direct-running flanged spools on a polished 4 mm pin. POM is the
  preferred prototype material; a low-friction printed spool is the fallback.
- MR84 bearings are intentionally not used in the guide towers because their
  3.0 mm width does not fit the fixed 2.55 mm carrier gaps with axial capture.
- Every tower has symmetric plus/minus 0.6 mm radial setup slots.
- Ring guide land is 1.6 mm total: 0.8 mm neck plus 0.8 mm smooth head.
- Each polished D4 x 24 mm pin is retained by a purchased metal D4 x 10 x
  4 mm set-screw shaft collar. The M2 tapped feature belongs to the purchased
  collar; no printed M2 thread is assumed.
- Each tower base is clamped through its two radial slots with two M3 socket
  head screws, washers, and standard hex nuts. Socket heads are installed from
  the wall side; the nuts remain tool-accessible from the front before the
  rotating ring stack is installed.
- Motor stations at 0, 120, and 240 degrees provide torque only and are not
  locating supports.
- No continuous T-rail, keeper saddle, Hall sensor, or homing geometry belongs
  to this correction.
- Detailed motor-station mounting remains a separate integration work package.

Primary source:

- `p3_v3_roller_tower_spec.py`
- `p3_v3_roller_tower_geometry.py`
- `p3_v3_roller_tower_export.py`
