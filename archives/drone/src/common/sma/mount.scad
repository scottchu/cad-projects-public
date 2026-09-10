include <BOSL2/std.scad>
use <../../lib/right_triangle.scad>
use <../../spec/sma.scad>
use <../standoff/holder.scad>
use <base.scad>
use <functions.scad>

module SMA_Mount_BaseShape(
  width,
  length,
  height,
  flat_top,
  angle,
  chamfer = 0,
  top_back_chamfer = 0,
  top_back_chamfer_length = 0,
  label = ""
) {
  pl = length - flat_top;
  ph = RT_calc_a_with_b_alpha(pl, angle);
  dz = height - ph;
  max_angle = RT_calc_alpha_with_a_b(height, pl);

  assert(angle <= max_angle, str("Angle for ", label, " is too large, max angle is ", max_angle));

  top_back_chamfer = top_back_chamfer > 0 ? top_back_chamfer : chamfer;

  difference() {
    diff()
    cuboid(
      size=[width, length, height],
      anchor=BOTTOM
    ) {
      if (top_back_chamfer_length > 0 && top_back_chamfer > 0) {
        edge_mask(TOP+BACK)
        chamfer_edge_mask(l=top_back_chamfer_length, chamfer=top_back_chamfer);
      }

      if (chamfer > 0) {
        edge_mask([BOTTOM+FRONT, BOTTOM+LEFT, BOTTOM+RIGHT])
        chamfer_edge_mask(l=width, chamfer=0.5);
      }
    };

    translate([0, -length/2 - 0.01, dz + 0.01])
    wedge(
      size=[width+0.01, pl+0.01, ph+0.02],
      anchor=TOP+FRONT,
      orient=DOWN
    );
  };
}

module SMA_Mount_Base(
  width,
  length,
  height,
  flat_top = 2,
  angle = 30,
  thickness = 1.5,
  wall = 1.5,
  chamfer = 0,
  top_back_chamfer = 0,
  top_back_chamfer_length = 0,
  show_side = false
) {

  top_back_chamfer = top_back_chamfer > 0 ? top_back_chamfer : chamfer;
  top_back_chamfer_length = top_back_chamfer_length > 0 ? top_back_chamfer_length : width;


  difference() {
    SMA_Mount_BaseShape(
      width = width,
      length = length,
      height = height,
      flat_top = flat_top,
      angle = angle,
      chamfer = chamfer,
      top_back_chamfer = top_back_chamfer,
      top_back_chamfer_length = top_back_chamfer_length,
      label="outer BaseShape"
    );

    a = thickness;
    b = RT_calc_a_with_b_alpha(a, angle);
    c = RT_calc_c_with_a_b(a, b);

    iw = width - wall * 2;
    il = length - c;
    ih = height - c;

    translate([0, c/2 + 0.01, -0.01])
    SMA_Mount_BaseShape(
      width = iw,
      length = il,
      height = ih,
      flat_top = flat_top,
      angle = angle,
      label="inner BaseShape"
    );

    if (show_side == true) {
      translate([-(width-wall)/2, 0, -0.01])
      cube([wall+0.02, length+0.02, height+0.02], anchor=BOTTOM);
    }
  }
}

module SMA_Mount_Dual(
  width,
  length,
  height,
  distance,
  flat_top = 2,
  angle = 30,
  thickness = 1.5,
  wall = 1.5,
  chamfer = 0,
  top_back_chamfer = 0,
  top_back_chamfer_length = 0,
  show_side = false,
  standoff_diameter,
  standoff_wall,
  standoff_height,
  standoff_distance,
  standoff_offset = 0,
  standoff_front_flat = false,
  standoff_front_chamfer = 0,
  standoff_ofn = 10,
  standoff_ifn = -1,
  sma_fn = 10,
  sma_y_offset = 0,
  show_sma_teeth_disk = false
) {
  assert(enough_space(width - distance), "Not enough space for SMA");

  height = height < 0 ? standoff_height : height;

  holder_width = width < 0 ? standoff_diameter*2 + standoff_wall*4 + standoff_distance - 4 : width;

  ma = length - flat_top - thickness;
  mb = RT_calc_a_with_b_alpha(ma, angle);
  mc = RT_calc_c_with_a_b(ma, mb);
  mid_mc = mc / 2;
  mid_mb = RT_calc_b_with_c_alpha(mid_mc, angle);

  a = thickness;
  b = RT_calc_a_with_b_alpha(a, angle);
  c = RT_calc_c_with_a_b(a, b);
  mh = RT_calc_a_with_b_alpha(c, angle);
  ml = RT_calc_c_with_a_b(c, mh);

  Standoff_Holder_Pair(
    diameter = standoff_diameter,
    wall = standoff_wall,
    height = standoff_height,
    distance = standoff_distance,
    offset = standoff_offset,
    front_flat = standoff_front_flat,
    front_chamfer = standoff_front_chamfer,
    ofn = standoff_ofn,
    ifn = standoff_ifn
  );

  difference() {
    translate([0,  -(length + standoff_diameter)/2, 0])
    SMA_Mount_Base(
      width  = width,
      length  = length,
      height  = height,
      flat_top = flat_top,
      angle = angle,
      thickness = thickness,
      wall = wall,
      chamfer = chamfer,
      top_back_chamfer = top_back_chamfer,
      top_back_chamfer_length = top_back_chamfer_length,
      show_side = show_side
    );

    rotate([angle, 0, 0])
    translate([(distance + 6) / 2,  -mid_mb + sma_y_offset, height - thickness + 0.5])
    SMA_Hole(
      height = thickness + 1,
      $fn = sma_fn,
      show_teeth_disk = show_sma_teeth_disk
    );

    rotate([angle, 0, 0])
    translate([-(distance + 6) / 2, -mid_mb + sma_y_offset, height - thickness + 0.5])
    SMA_Hole(
      height = thickness + 1,
      $fn = sma_fn,
      show_teeth_disk = show_sma_teeth_disk
    );
  }
}

SMA_Mount_Dual(
  width = 30,
  length = 15,
  height = 10,
  distance = 6,
  angle = 30,
  thickness = 2,
  top_back_chamfer = 1,
  standoff_diameter = 4.5,
  standoff_wall = 2,
  standoff_height = 10,
  standoff_distance = 14.5,
  sma_fn = 50,
  show_sma_teeth_disk = true,
  sma_y_offset = -0.2,
  standoff_ofn = 50
);