include <spec.scad>
use <../../common/GPS/side-panel/panel.v1.scad>

module AOS_5_o3_GPS_SidePanel() {
  Panel(
    thickness =4,
    length = 35,

    arm_length = 13.5,
    arm_height = 10,

    fin_height = 2.5,
    fin_length = 8,
    fin_angle = FIN_ANGLE,

    bottom_height = 4,
    bottom_length = 35,
    bottom_back_angle = 30,
    bottom_front_angle = 30
  );
}

module AOS_5_o3_GPS_SidePanels() {
  distance = (STANDOFF_DISTANCE + STANDOFF_DIAMETER) + STANDOFF_WALL * 2;

  distribute(distance) {
    AOS_5_o3_GPS_SidePanel();

    mirror([1, 0, 0])
    AOS_5_o3_GPS_SidePanel();
  }
}

AOS_5_o3_GPS_SidePanels();
