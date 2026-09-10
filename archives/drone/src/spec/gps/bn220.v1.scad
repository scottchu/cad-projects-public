include <BOSL2/std.scad>

BN220_width = 20;
BN220_length = 22;
BN220_height = 5.8;

BN220_dimension = [
  BN220_width,
  BN220_length,
  BN220_height
];

// Top Layer
BN220_top_width = 18;
BN220_top_length = 18;
BN220_top_height = 2;

// Middle Layer
BN220_middle_width = BN220_width;
BN220_middle_length = BN220_length;
BN220_middle_height = 0.7;

// Bottom Layer
BN220_bottom_width = 18;
BN220_bottom_length = 14.8;
BN220_bottom_height = 2.8;

// Battery
BN220_battery_diameter = 4.6;
BN220_battery_height = 1.7;
BN220_battery_distance_from_edge = 0.7;

// Plug
BN220_plug_width = 6;
BN220_plug_length = 4.3;
BN220_plug_height = 3.1;

module BN220_top_chip() {
  diff()
  cuboid(
    size = [
      BN220_top_width,
      BN220_top_length,
      BN220_top_height
    ],
    anchor = CENTER
  ) {
    edge_mask(FRONT+RIGHT)
    chamfer_edge_mask(l=4, chamfer=2);

    edge_mask(edges=[BACK+RIGHT, FRONT+LEFT, BACK+LEFT])
    rounding_edge_mask(l=4, r=1, $fn = 50);
  };
}

module BN220(
  anchor = CENTER
) {
  tz = anchor == TOP ?
    (BN220_middle_height / 2 + BN220_bottom_height) :
    anchor == BOTTOM ? -(BN220_middle_height / 2 + BN220_top_height) :
    0;

  translate([0, 0, tz]) {
    // MIDDLE
    cuboid(
      size = [
        BN220_middle_width,
        BN220_middle_length,
        BN220_middle_height
      ],
      anchor = CENTER
    );

    // Top
    translate([0, 0, (BN220_top_height + BN220_middle_height) / 2])
    BN220_top_chip();

    // Bottom
    bottom_chip_ty = -(BN220_middle_length - BN220_bottom_length) / 2 + 1;
    bottom_chip_tz = -(BN220_middle_height + BN220_bottom_height) / 2;

    translate([0, bottom_chip_ty, bottom_chip_tz])
    cuboid(
      size = [
        BN220_bottom_width,
        BN220_bottom_length,
        BN220_bottom_height
      ],
      anchor = CENTER
    );

    // Battery
    battery_tx = (BN220_middle_width - BN220_battery_diameter) / 2 - BN220_battery_distance_from_edge;
    battery_ty = (BN220_middle_length - BN220_battery_diameter) / 2 - BN220_battery_distance_from_edge;
    battery_tz = -(BN220_middle_height + BN220_battery_height) / 2;

    translate([
      battery_tx,
      battery_ty,
      battery_tz
    ])
    cylinder(
      r = BN220_battery_diameter / 2,
      h = BN220_battery_height,
      anchor = CENTER,
      $fn = 50
    );

    // Plug
    plug_tx = 0;
    plug_ty = (BN220_middle_length - BN220_plug_length) / 2;
    plug_tz = -(BN220_middle_height + BN220_plug_height) / 2;

    translate([
      plug_tx,
      plug_ty,
      plug_tz
    ])
    cuboid(
      size = [
        BN220_plug_width,
        BN220_plug_length,
        BN220_plug_height
      ],
      anchor = CENTER
    );
  }
}

// BN220(anchor=TOP);