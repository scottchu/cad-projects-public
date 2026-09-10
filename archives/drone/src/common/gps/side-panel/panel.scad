include <BOSL2/std.scad>
use <../../adjustable-side-mount/mount.scad>

module Panel_v1(
  // general
  thickness = 2,
  length,

  // arm
  arm_length,
  arm_height,

  // fin
  fin_length,
  fin_height,
  fin_angle,

  // bottom
  bottom_length = -1,
  bottom_height,
  bottom_angle
) {
  panel_height = fin_height + arm_height;

  fin_y = length - arm_length - fin_length;
  fin_z = adj_ang_to_opp(adj = fin_y, ang = fin_angle);
  fin_translate_y = length - arm_length;
  fin_translate_z = panel_height;

  bottom_length = bottom_length < 0 ? length : bottom_length;
  bottom_z = bottom_height;
  bottom_y = opp_ang_to_adj(opp = bottom_z, ang = bottom_angle);
  union() {

    difference() {
      union() {

        // Arm
        cuboid(
          size = [thickness, arm_length, arm_height],
          anchor = BOTTOM+FRONT
        );

        // Fin
        difference() {
          diff()
          cuboid(
            size = [thickness, length - arm_length, panel_height],
            anchor = BOTTOM+BACK
          ) {
            edge_mask([TOP+BACK])
            chamfer_edge_mask(l = thickness, chamfer = 1, orient = DOWN);
          }

          translate([0, -fin_translate_y - 0.01, fin_translate_z + 0.01])
          wedge(
            size=[thickness + 0.01, fin_y + 0.01, fin_z + 0.01],
            anchor = BOTTOM+FRONT,
            orient = DOWN
          );
        }
      }
    }

    // Bottom
    difference() {
      translate([0, -fin_translate_y, 0])
      diff()
      cuboid(
        size = [thickness, bottom_length, bottom_height],
        anchor = TOP+FRONT
      ) {
        edge_mask([BOTTOM+FRONT])
        chamfer_edge_mask(l = thickness, chamfer = 1, orient = DOWN);
      }

      translate([0, -fin_translate_y + bottom_length + 0.01, 0])
      rot([0, 180, 180])
      wedge(
        size=[thickness + 0.01, bottom_y + 0.01, bottom_z + 0.01],
        anchor = TOP+BACK,
        orient=DOWN
      );
    }
  }
}

Panel_v1(
  thickness = 2,
  length = 40,

  arm_length = 15,
  arm_height = 10,

  fin_height = 2.5,
  fin_length = 8,
  fin_angle = 30,

  bottom_height = 4,
  bottom_angle = 30,
  bottom_length = 35
);