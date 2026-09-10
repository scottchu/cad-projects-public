include <BOSL2/std.scad>

module AdjustableSideMount_BaseShape(
  r1,
  r2,
  distance
) {
  c2_dy = r2 - r1;

  hull() {
    circle(r = r1);

    translate([distance, c2_dy, 0])
    circle(r = r2);
  }
}

module AdjustableSideMount_Base(
  r1,
  r2,
  distance,
  thickness,
  scale = [1, 1],
  center_point = 0
) {
  quality = $preview ? 30 : 60;
  c2_dy = r2 - r1;
  center_point_h = thickness * 1.5;

  move([0, 0, -thickness / 2])
  linear_extrude(height = thickness, scale = scale)
  AdjustableSideMount_BaseShape(
    r1 = r1,
    r2 = r2,
    distance = distance,
    $fn = quality
  );

  if (center_point > 0) {
    move([0, 0, -center_point_h / 2])
    #linear_extrude(height = center_point_h)
    union() {
      circle(
        r = center_point,
        $fn = quality
      );

      translate([distance, c2_dy, 0])
      circle(
        r = center_point,
        $fn = quality
      );
    }
  }
}

AdjustableSideMount_Base(
  r1 = 0.8 * 2,
  r2 = 0.8 * 4,
  distance = 12,
  thickness = 2,
  center_point = 0.8
);

