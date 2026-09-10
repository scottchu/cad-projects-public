"""Small build123d helpers shared by Pill Click parts."""

from build123d import Align, Axis, Box, Location, Part, fillet


def rounded_box(
    size_x: float,
    size_y: float,
    size_z: float,
    radius: float,
    *,
    center: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> Part:
    """Return a centred, edge-rounded box translated to ``center``."""

    body = Box(
        size_x,
        size_y,
        size_z,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    if radius > 0:
        # All Pill Click plates and bodies use Y as depth.  Rounding only the
        # Y-parallel edges preserves the specified depth and avoids fragile
        # all-edge fillets on thin covers/key faces.
        body = fillet(body.edges().filter_by(Axis.Y), radius)
    if center != (0.0, 0.0, 0.0):
        body = body.moved(Location(center))
    return body
