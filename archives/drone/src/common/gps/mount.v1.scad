include <BOSL2/std.scad>
include <../../spec/gps/bn220.v1.scad>
use <mount.scad>

module gps_enclosure(
  outer_dimension,
  inner_dimension,
  hide_side = false
) {
  inner_tz = outer_dimension[2] - inner_dimension[2] + 0.1;

  difference() {
    cuboid(
      size = outer_dimension,
      anchor = BOTTOM
    );

    translate([0, 0, inner_tz])
    cuboid(
      size = inner_dimension,
      anchor = BOTTOM
    );

    if (hide_side) {
      thickness_x = (outer_dimension[0] - inner_dimension[0]) / 2;
      left_side_dx = -outer_dimension[0] / 2 + thickness_x / 2;

      translate([
        left_side_dx,
        0,
        outer_dimension[2] / 2
      ])
      cuboid(
        size = [
          thickness_x + 0.1,
          outer_dimension[1] + 0.1,
          outer_dimension[2] + 0.1
        ]
      );

      translate([
        -left_side_dx,
        0,
        outer_dimension[2] / 2
      ])
      cuboid(
        size = [
          thickness_x + 0.1,
          outer_dimension[1] + 0.1,
          outer_dimension[2] + 0.1
        ]
      );
    }
  }
}

module gps_mount_v1(
  dimension,
  thickness = [4, 4, 4],
  clip_dimension,
  cover_length = 2,
  plug_width,
  plug_height,
  chamfer = 0,
  offset = 0.5,
  hide_side = false
) {

  width = dimension[0];
  length = dimension[1];
  height = dimension[2];

  outer_width = width + (thickness[0] * 2) + offset;
  outer_length = length + (thickness[1] * 2) + offset;
  outer_height = height + thickness[2] + offset;

  inner_width = width + offset;
  inner_length = length + offset;
  inner_height = height + offset + 0.1;

  difference() {
    union() {
      gps_enclosure(
        outer_dimension = [
          outer_width, outer_length, outer_height
        ],
        inner_dimension = [
          inner_width, inner_length, inner_height
        ],
        hide_side = hide_side
      );

      translate([outer_width / 2, -outer_length / 2, outer_height])
      wedge(
        size = [
          clip_dimension[2], // z
          clip_dimension[1], // y
          clip_dimension[0]  // x
        ],
        orient = LEFT
      );

      translate([-outer_width / 2, -outer_length / 2, outer_height + clip_dimension[2]])
      wedge(
        size = [
          clip_dimension[2], // z
          clip_dimension[1], // y
          clip_dimension[0]  // x
        ],
        orient = RIGHT
      );


      translate([-outer_width / 2, outer_length / 2, outer_height])
      zrot(180)
      wedge(
        size = [
          clip_dimension[2], // z
          clip_dimension[1], // y
          clip_dimension[0]  // x
        ],
        orient = LEFT
      );

      translate([outer_width / 2, outer_length / 2, outer_height])
      zrot(90)
      wedge(
        size = [
          clip_dimension[2], // z
          clip_dimension[1], // y
          clip_dimension[0]  // x
        ],
        orient = LEFT
      );

      translate([0, (outer_length - cover_length) / 2, outer_height])
      cuboid(
        size = [
          outer_width,
          cover_length,
          clip_dimension[2]
        ],
        anchor = BOTTOM
      );

      translate([0, -(outer_length - cover_length) / 2, outer_height])
      cuboid(
        size = [
          outer_width,
          cover_length,
          clip_dimension[2]
        ],
        anchor = BOTTOM
      );
    }

    translate([0, outer_length / 2 + 0.1, thickness[2]])
    cuboid(
      size = [plug_width, thickness[1] + 0.2, plug_height],
      anchor = BACK+BOTTOM
    );

    translate([outer_width / 2, outer_length / 2, 0])
    chamfer_edge_mask(
      l = outer_height + clip_dimension[2],
      chamfer = chamfer,
      anchor = BOTTOM
    );

    translate([outer_width / 2, -outer_length / 2, 0])
    chamfer_edge_mask(
      l = outer_height + clip_dimension[2],
      chamfer = chamfer,
      anchor = BOTTOM
    );

    translate([-outer_width / 2, -outer_length / 2, 0])
    chamfer_edge_mask(
      l = outer_height + clip_dimension[2],
      chamfer = chamfer,
      anchor = BOTTOM
    );

    translate([-outer_width / 2, outer_length / 2, 0])
    chamfer_edge_mask(
      l = outer_height + clip_dimension[2],
      chamfer = chamfer,
      anchor = BOTTOM
    );
  }
}

gps_mount_v1(
  dimension = [
    BN220_width,
    BN220_length,
    BN220_middle_height + BN220_bottom_height
  ],
  clip_dimension = [6, 6, 1.5],
  cover_length = 3.5,
  plug_width = 7,
  plug_height = BN220_plug_height + 3,
  thickness = [2, 2, 2],
  chamfer = 1,
  offset = 0.25,
  hide_side = false
);