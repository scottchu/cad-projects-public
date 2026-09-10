include <BOSL2/std.scad>
include <../../lib/render.scad>
include <../../spec/screw.scad>
use <../screw/adjustable_screw.scad>
use <base.scad>

function adjustable_length(screw_diameter, screw_distance, angle) =
  hyp_ang_to_adj(hyp = (screw_diameter + screw_distance), ang = angle);

module GPS_Adjustable_Mount(
  // Mount
  thickness = 2,
  adjustable_angle = 30,

  // Base
  base_multiplier = 3,
  base_length_offset = 0,
  base_scale = [1,1],
  show_center_point = false,

  // Screw
  screw_diameter,
  screw_distance,
  screw_edge_distance = 2,

  show_screws = true

) {
  _offset = 0.2;

  true_screw_diameter = screw_diameter * SCREW_MM_Multiplier;
  true_screw_radius = true_screw_diameter / 2;
  screw_radius = screw_diameter / 2;

  base_r1 = true_screw_radius * base_multiplier;
  base_r2 = hyp_ang_to_opp(hyp = screw_distance, ang = adjustable_angle * 1.05);
  base_distance = adjustable_length(
    true_screw_diameter,
    screw_distance,
    adjustable_angle / 2) + base_length_offset;

  difference() {
    AdjustableSideMount_Base(
      r1 = base_r1,
      r2 = base_r2,
      distance = base_distance,
      thickness = thickness,
      center_point = show_center_point ? true_screw_radius : 0,
      scale = base_scale
    );

    if (show_screws) {
      alwaysRender() {
        AdjustableScrewHoles(
          diameter = screw_diameter,
          angle = adjustable_angle,
          distance = screw_distance,
          length = thickness * 1.5,
          caps = true,
          show_meta = false
        );
      }
    }
  }
}

GPS_Adjustable_Mount(
  thickness = 2,
  adjustable_angle = 30,
  base_multiplier = 3,
  base_length_offset = 0.1225,
  base_scale = [1.1, 1.2],
  screw_diameter = 1.6,
  screw_distance = 12
);
