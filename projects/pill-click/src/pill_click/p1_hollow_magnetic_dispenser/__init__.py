"""Three-part hollow magnetic dispenser API."""

from .assembly import make_assembly, make_pressed_assembly, make_released_assembly, placed_hollow_keyboard_container
from .diagnostics import make_hopper_cutaway
from .geometry import make_cover_m1_bore_tools, make_cover_m1_pick_bore_tools, make_cover_m2_bore_tools, make_cover_m2_pick_bore_tools, make_cover_magnet_bosses, make_hollow_keyboard_container, make_hopper_void, make_inner_magnet_pick_bore_tools, make_inner_magnet_pocket_tools, make_inner_port_tool, make_magnetic_rear_cover, make_outer_port_tool, make_ported_outer_housing, make_upper_medicine_chamber
from .print_exports import make_print_bundle, print_hollow_keyboard_container, print_magnetic_rear_cover, print_outer_housing
from .spec import P1_HOLLOW_MAGNETIC_DISPENSER, P1HollowMagneticDispenserSpec

__all__ = [name for name in globals() if name.startswith("make_") or name.startswith("placed_") or name.startswith("print_") or name.startswith("P1")]
