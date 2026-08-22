"""P15 PETG rod-cap fit test.

This diagnostic is intentionally separate from the XT60 mechanism.  It tests
three copies of the *actual removable cap architecture* (blind socket,
retention throat, and radial flex slit) because a rigid plate coupon cannot
predict the compliance of a thin sleeve.

Coordinate convention:
    XY is the printer bed, +Z is cap height.  Each cap stands on its closed
    end at Z=0 with the rod entry facing upward.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path

from build123d import Align, Box, Compound, Cylinder, Pos


@dataclass(frozen=True)
class P15CapFitParameters:
    socket_diameters: tuple[float, ...] = (4.05, 4.10, 4.15)
    cap_outer_diameter: float = 7.00
    cap_height: float = 3.80
    closed_base_thickness: float = 0.80
    throat_diameter: float = 3.60
    throat_depth: float = 0.60
    slit_width: float = 0.60
    station_pitch: float = 12.00
    identification_notch_depth: float = 0.35
    identification_notch_width: float = 0.45
    identification_notch_height: float = 0.80
    identification_notch_pitch: float = 0.75
    boolean_overshoot: float = 0.03
    minimum_radial_wall: float = 1.40


DEFAULTS = P15CapFitParameters()
PART_LABEL = "P15_PETG_actual_slit_cap_fit_test_4p05_4p10_4p15"


def station_x_positions(p: P15CapFitParameters = DEFAULTS) -> tuple[float, ...]:
    half = p.station_pitch * (len(p.socket_diameters) - 1) / 2.0
    return tuple(index * p.station_pitch - half for index in range(len(p.socket_diameters)))


def cavity_depth(p: P15CapFitParameters = DEFAULTS) -> float:
    return p.cap_height - p.closed_base_thickness - p.throat_depth


def minimum_radial_wall(p: P15CapFitParameters = DEFAULTS) -> float:
    return (p.cap_outer_diameter - max(p.socket_diameters)) / 2.0


def throat_radial_interference_for_nominal_rod(
    p: P15CapFitParameters = DEFAULTS,
) -> float:
    return (4.00 - p.throat_diameter) / 2.0


def parameter_manifest(p: P15CapFitParameters = DEFAULTS) -> dict[str, object]:
    return {
        "schema": "P15ActualCapFitTest/v1",
        "units": "mm",
        "coordinateConvention": "XY printer bed; closed cap end Z=0; rod entry +Z",
        "parameters": asdict(p),
        "stationOrderLeftToRight": [f"{diameter:.2f}" for diameter in p.socket_diameters],
        "identification": {
            "4.05": "one exterior notch",
            "4.10": "two exterior notches",
            "4.15": "three exterior notches",
        },
        "priorRigidCouponObservation": {
            "4.05": "extremely tight; coupon needed to push rod back out",
            "4.10": "tight; hand push and pull possible",
            "4.15": "preferred sliding fit with slight friction",
        },
        "testIntent": "verify actual slit-sleeve compliance before mechanism integration",
        "derived": {
            "cavityDepthMm": cavity_depth(p),
            "minimumRadialWallMm": minimum_radial_wall(p),
            "throatRadialInterferenceForNominal4mmRodMm": throat_radial_interference_for_nominal_rod(p),
        },
        "printOrientation": "three caps upright on closed ends; sockets face +Z",
        "physicalValidationRequired": True,
    }


def parameter_manifest_sha256(p: P15CapFitParameters = DEFAULTS) -> str:
    payload = json.dumps(parameter_manifest(p), sort_keys=True, separators=(",", ":"))
    return sha256(payload.encode("utf-8")).hexdigest()


def source_revision_sha256() -> str:
    return sha256(Path(__file__).read_bytes()).hexdigest()


def _validate_parameters(p: P15CapFitParameters) -> None:
    if p.socket_diameters != (4.05, 4.10, 4.15):
        raise ValueError("actual cap test must contain exactly 4.05, 4.10, and 4.15 mm")
    if p.cap_outer_diameter != 7.00 or p.cap_height != 3.80:
        raise ValueError("cap envelope must remain the P13 7.00 x 3.80 mm envelope")
    if p.closed_base_thickness <= 0.0 or p.throat_depth <= 0.0:
        raise ValueError("base and throat depths must be positive")
    if cavity_depth(p) <= 0.0:
        raise ValueError("blind cavity depth must be positive")
    if p.throat_diameter >= min(p.socket_diameters):
        raise ValueError("retention throat must be smaller than every socket")
    if p.slit_width <= 0.0:
        raise ValueError("radial flex slit must be present")
    if minimum_radial_wall(p) < p.minimum_radial_wall:
        raise ValueError("cap radial wall is below the PETG minimum")
    if p.station_pitch <= p.cap_outer_diameter:
        raise ValueError("print stations must not overlap")


def _identification_notches(
    notch_count: int,
    p: P15CapFitParameters,
):
    """Shallow exterior notches opposite the flex slit identify each cap."""

    total_span = (notch_count - 1) * p.identification_notch_pitch
    notch_y0 = -total_span / 2.0
    outer_radius = p.cap_outer_diameter / 2.0
    return [
        Pos(
            -outer_radius + p.identification_notch_depth / 2.0,
            notch_y0 + index * p.identification_notch_pitch,
            p.cap_height - p.identification_notch_height / 2.0,
        )
        * Box(
            p.identification_notch_depth + p.boolean_overshoot,
            p.identification_notch_width,
            p.identification_notch_height + p.boolean_overshoot,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        )
        for index in range(notch_count)
    ]


def build_cap(
    socket_diameter: float,
    notch_count: int,
    p: P15CapFitParameters = DEFAULTS,
):
    """Build one upright blind slit cap with the actual production envelope."""

    _validate_parameters(p)
    if socket_diameter not in p.socket_diameters:
        raise ValueError("socket diameter is not a P15 test station")
    if notch_count != p.socket_diameters.index(socket_diameter) + 1:
        raise ValueError("notch count must encode the left-to-right station")

    over = p.boolean_overshoot
    body = Cylinder(
        p.cap_outer_diameter / 2.0,
        p.cap_height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    cavity = Pos(0.0, 0.0, p.closed_base_thickness) * Cylinder(
        socket_diameter / 2.0,
        cavity_depth(p) + over,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    throat_z = p.cap_height - p.throat_depth
    throat = Pos(0.0, 0.0, throat_z) * Cylinder(
        p.throat_diameter / 2.0,
        p.throat_depth + over,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )

    # The +X slit joins the smaller throat and larger cavity to free space.
    # It begins above the closed base, preserving the full 0.80 mm floor.
    outer_radius = p.cap_outer_diameter / 2.0
    slit_x0 = p.throat_diameter / 2.0 - over
    slit_length = outer_radius - slit_x0 + 2.0 * over
    slit_height = p.cap_height - p.closed_base_thickness + over
    slit = Pos(
        slit_x0 + slit_length / 2.0,
        0.0,
        p.closed_base_thickness + slit_height / 2.0,
    ) * Box(
        slit_length,
        p.slit_width,
        slit_height,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )

    cap = body - [cavity, throat, slit, *_identification_notches(notch_count, p)]
    cap.label = f"actual_slit_cap_socket_D{socket_diameter:.2f}_notches_{notch_count}"
    return cap


def build_caps(p: P15CapFitParameters = DEFAULTS) -> tuple:
    _validate_parameters(p)
    return tuple(
        Pos(x, 0.0, 0.0) * build_cap(diameter, index + 1, p)
        for index, (x, diameter) in enumerate(
            zip(station_x_positions(p), p.socket_diameters, strict=True)
        )
    )


def build_cap_fit_test(p: P15CapFitParameters = DEFAULTS) -> Compound:
    result = Compound(children=list(build_caps(p)), label=PART_LABEL)
    return result


def gen_step():
    return build_cap_fit_test(DEFAULTS)
