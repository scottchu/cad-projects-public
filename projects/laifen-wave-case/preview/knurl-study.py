from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "projects" / "laifen-wave-case"
OUTPUT_SVG = PROJECT / "preview" / "knurl-study.svg"
SCRATCH_DIR = PROJECT / "scratch" / "pattern-study"
OUTPUT_JSON = SCRATCH_DIR / "knurl-study-metrics.json"


def mm(value: float) -> str:
    return f"{value:.3f}".rstrip("0").rstrip(".")


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


@dataclass(frozen=True)
class StudyConfig:
    lower_id: float = 30.0
    cap_id: float = 31.0
    wall: float = 2.4
    min_wall: float = 1.8
    rise: float = 0.6
    max_rise: float = 0.8
    flat_width: float = 1.0
    target_pitch: float = 3.64
    study_band_height: float = 28.0
    min_smooth_zone: float = 2.0
    coupon_texture_span: float = 5.6


@dataclass(frozen=True)
class StudyMetrics:
    lower_plain_od: float
    cap_plain_od: float
    lower_repeats: int
    cap_repeats: int
    lower_circ_pitch: float
    cap_circ_pitch: float
    lower_pitch_error: float
    cap_pitch_error: float
    axial_rows: int
    textured_height: float
    end_smooth_zone: float
    cell_count: int
    axial_run_to_flat: float
    overhang_angle_rise_0_6: float
    overhang_angle_rise_0_8: float
    additive_lower_max_od: float
    additive_cap_max_od: float
    subtractive_wall_at_0_6: float
    subtractive_wall_at_0_8: float
    max_od_margin_lower: float
    max_od_margin_cap: float
    coupon_rows_at_main_pitch: int
    coupon_pitch_for_two_rows: float
    coupon_overhang_angle_rise_0_6: float
    coupon_overhang_angle_rise_0_8: float


def compute_metrics(config: StudyConfig) -> StudyMetrics:
    lower_plain_od = config.lower_id + 2.0 * config.wall
    cap_plain_od = config.cap_id + 2.0 * config.wall
    lower_circumference = math.pi * lower_plain_od
    cap_circumference = math.pi * cap_plain_od

    lower_repeats = round(lower_circumference / config.target_pitch)
    cap_repeats = round(cap_circumference / config.target_pitch)

    lower_circ_pitch = lower_circumference / lower_repeats
    cap_circ_pitch = cap_circumference / cap_repeats

    rows = math.floor(
        (config.study_band_height - 2.0 * config.min_smooth_zone) / lower_circ_pitch
    )
    if rows < 1:
        raise ValueError("Configured band does not admit one complete knurl row.")
    textured_height = rows * lower_circ_pitch
    end_smooth_zone = (config.study_band_height - textured_height) / 2.0

    axial_run_to_flat = (lower_circ_pitch - config.flat_width) / 2.0
    if axial_run_to_flat <= 0:
        raise ValueError("Flat width must remain below the chosen pitch.")

    overhang_angle_rise_0_6 = math.degrees(math.atan(config.rise / axial_run_to_flat))
    overhang_angle_rise_0_8 = math.degrees(
        math.atan(config.max_rise / axial_run_to_flat)
    )

    additive_lower_max_od = lower_plain_od + 2.0 * config.rise
    additive_cap_max_od = cap_plain_od + 2.0 * config.rise
    subtractive_wall_at_0_6 = config.wall - config.rise
    subtractive_wall_at_0_8 = config.wall - config.max_rise

    coupon_rows_at_main_pitch = math.floor(config.coupon_texture_span / lower_circ_pitch)
    coupon_pitch_for_two_rows = config.coupon_texture_span / 2.0
    coupon_run_to_flat = (coupon_pitch_for_two_rows - config.flat_width) / 2.0
    if coupon_run_to_flat <= 0:
        raise ValueError("Coupon pitch leaves no room for a flat top.")
    coupon_overhang_angle_rise_0_6 = math.degrees(
        math.atan(config.rise / coupon_run_to_flat)
    )
    coupon_overhang_angle_rise_0_8 = math.degrees(
        math.atan(config.max_rise / coupon_run_to_flat)
    )

    return StudyMetrics(
        lower_plain_od=lower_plain_od,
        cap_plain_od=cap_plain_od,
        lower_repeats=lower_repeats,
        cap_repeats=cap_repeats,
        lower_circ_pitch=lower_circ_pitch,
        cap_circ_pitch=cap_circ_pitch,
        lower_pitch_error=lower_circ_pitch - config.target_pitch,
        cap_pitch_error=cap_circ_pitch - config.target_pitch,
        axial_rows=rows,
        textured_height=textured_height,
        end_smooth_zone=end_smooth_zone,
        cell_count=rows * lower_repeats,
        axial_run_to_flat=axial_run_to_flat,
        overhang_angle_rise_0_6=overhang_angle_rise_0_6,
        overhang_angle_rise_0_8=overhang_angle_rise_0_8,
        additive_lower_max_od=additive_lower_max_od,
        additive_cap_max_od=additive_cap_max_od,
        subtractive_wall_at_0_6=subtractive_wall_at_0_6,
        subtractive_wall_at_0_8=subtractive_wall_at_0_8,
        max_od_margin_lower=39.0 - additive_lower_max_od,
        max_od_margin_cap=39.0 - additive_cap_max_od,
        coupon_rows_at_main_pitch=coupon_rows_at_main_pitch,
        coupon_pitch_for_two_rows=coupon_pitch_for_two_rows,
        coupon_overhang_angle_rise_0_6=coupon_overhang_angle_rise_0_6,
        coupon_overhang_angle_rise_0_8=coupon_overhang_angle_rise_0_8,
    )


def line(x1: float, y1: float, x2: float, y2: float, stroke: str, width: float) -> str:
    return (
        f"<line x1='{x1:.2f}' y1='{y1:.2f}' x2='{x2:.2f}' y2='{y2:.2f}' "
        f"stroke='{stroke}' stroke-width='{width:.2f}' />"
    )


def text(
    x: float,
    y: float,
    value: str,
    size: float,
    fill: str = "#1d2428",
    weight: int = 400,
) -> str:
    return (
        f"<text x='{x:.2f}' y='{y:.2f}' fill='{fill}' font-size='{size:.1f}' "
        f"font-family='Helvetica, Arial, sans-serif' font-weight='{weight}'>{esc(value)}</text>"
    )


def polygon(points: list[tuple[float, float]], fill: str, stroke: str = "none") -> str:
    joined = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f"<polygon points='{joined}' fill='{fill}' stroke='{stroke}' />"


def dimension_horizontal(
    x1: float, x2: float, y: float, label: str, guide_top: float, guide_bottom: float
) -> str:
    elements = [
        line(x1, guide_top, x1, guide_bottom, "#70818a", 1.1),
        line(x2, guide_top, x2, guide_bottom, "#70818a", 1.1),
        line(x1, y, x2, y, "#46545c", 1.2),
        line(x1, y, x1 + 10.0, y - 4.0, "#46545c", 1.2),
        line(x1, y, x1 + 10.0, y + 4.0, "#46545c", 1.2),
        line(x2, y, x2 - 10.0, y - 4.0, "#46545c", 1.2),
        line(x2, y, x2 - 10.0, y + 4.0, "#46545c", 1.2),
        text((x1 + x2) / 2.0 - 32.0, y - 8.0, label, 20.0, "#243038", 600),
    ]
    return "".join(elements)


def dimension_vertical(
    y1: float, y2: float, x: float, label: str, guide_left: float, guide_right: float
) -> str:
    elements = [
        line(guide_left, y1, guide_right, y1, "#70818a", 1.1),
        line(guide_left, y2, guide_right, y2, "#70818a", 1.1),
        line(x, y1, x, y2, "#46545c", 1.2),
        line(x, y1, x - 4.0, y1 + 10.0, "#46545c", 1.2),
        line(x, y1, x + 4.0, y1 + 10.0, "#46545c", 1.2),
        line(x, y2, x - 4.0, y2 - 10.0, "#46545c", 1.2),
        line(x, y2, x + 4.0, y2 - 10.0, "#46545c", 1.2),
        text(x + 12.0, (y1 + y2) / 2.0 + 6.0, label, 20.0, "#243038", 600),
    ]
    return "".join(elements)


def render_svg(config: StudyConfig, metrics: StudyMetrics) -> str:
    patch_scale = 9.0
    patch_x = 70.0
    patch_y = 170.0
    patch_w = metrics.lower_plain_od * 0.0 + math.pi * metrics.lower_plain_od * patch_scale
    patch_h = config.study_band_height * patch_scale
    panel_x = 70.0
    panel_y = patch_y + patch_h + 150.0
    panel_w = 360.0
    canvas_w = max(patch_x + patch_w + 70.0, panel_x + panel_w + 70.0)
    canvas_h = panel_y + 830.0

    peak_half = metrics.lower_circ_pitch * 0.48
    flat_half = config.flat_width / 2.0
    smooth_top = patch_y + metrics.end_smooth_zone * patch_scale
    smooth_bottom = patch_y + patch_h - metrics.end_smooth_zone * patch_scale

    svg: list[str] = [
        (
            f"<svg xmlns='http://www.w3.org/2000/svg' width='{canvas_w:.0f}' height='{canvas_h:.0f}' "
            f"viewBox='0 0 {canvas_w:.0f} {canvas_h:.0f}'>"
        ),
        "<rect width='100%' height='100%' fill='#f3efe6' />",
        text(70, 70, "PAT-01 original faceted-grip concept", 30, "#172127", 700),
        text(
            70,
            106,
            "Developed cylindrical surface only; original vector study, no CAD or print acceptance.",
            20,
            "#43525b",
            400,
        ),
        (
            f"<rect x='{patch_x:.2f}' y='{patch_y:.2f}' width='{patch_w:.2f}' height='{patch_h:.2f}' "
            "rx='18' fill='#fbf8f2' stroke='#314048' stroke-width='2' />"
        ),
        (
            f"<rect x='{patch_x:.2f}' y='{patch_y:.2f}' width='{patch_w:.2f}' "
            f"height='{metrics.end_smooth_zone * patch_scale:.2f}' fill='#e8e2d5' opacity='0.95' />"
        ),
        (
            f"<rect x='{patch_x:.2f}' y='{smooth_bottom:.2f}' width='{patch_w:.2f}' "
            f"height='{metrics.end_smooth_zone * patch_scale:.2f}' fill='#e8e2d5' opacity='0.95' />"
        ),
        text(patch_x, patch_y - 24, "lower-body sample band, ODref 34.8, circumference repeat count 30", 21, "#26333a", 600),
        text(patch_x, patch_y + patch_h + 34, "shared angular datum theta0 at seam; texture band clips from a larger assembled-space lattice", 18, "#43525b", 400),
    ]

    for row in range(metrics.axial_rows):
        center_y_mm = metrics.end_smooth_zone + metrics.lower_circ_pitch / 2.0 + row * metrics.lower_circ_pitch
        center_y = patch_y + center_y_mm * patch_scale
        offset = (row % 2) * metrics.lower_circ_pitch / 2.0
        col = -1
        while True:
            center_x_mm = offset + metrics.lower_circ_pitch / 2.0 + col * metrics.lower_circ_pitch
            if center_x_mm > math.pi * metrics.lower_plain_od + metrics.lower_circ_pitch:
                break
            col += 1
            center_x = patch_x + center_x_mm * patch_scale

            top = (center_x, center_y - peak_half * patch_scale)
            right = (center_x + peak_half * patch_scale, center_y)
            bottom = (center_x, center_y + peak_half * patch_scale)
            left = (center_x - peak_half * patch_scale, center_y)

            ft = (center_x, center_y - flat_half * patch_scale)
            fr = (center_x + flat_half * patch_scale, center_y)
            fb = (center_x, center_y + flat_half * patch_scale)
            fl = (center_x - flat_half * patch_scale, center_y)

            svg.extend(
                [
                    polygon([top, right, fr, ft], "#dce5e8"),
                    polygon([right, bottom, fb, fr], "#8ea0a8"),
                    polygon([bottom, left, fl, fb], "#66757d"),
                    polygon([left, top, ft, fl], "#bac7cc"),
                    polygon([ft, fr, fb, fl], "#f7fbfc", "#d0d9dc"),
                ]
            )

    seam_x = patch_x + patch_w
    svg.extend(
        [
            line(patch_x, patch_y, patch_x, patch_y + patch_h, "#425159", 2.0),
            line(seam_x, patch_y, seam_x, patch_y + patch_h, "#425159", 2.0),
            text(patch_x - 20, patch_y - 8, "theta0", 18, "#425159", 700),
            text(seam_x - 34, patch_y - 8, "wrap", 18, "#425159", 700),
            dimension_horizontal(
                patch_x,
                patch_x + metrics.lower_circ_pitch * patch_scale,
                patch_y + patch_h + 76,
                f"pitch {mm(metrics.lower_circ_pitch)} mm",
                patch_y + patch_h + 8,
                patch_y + patch_h + 64,
            ),
            dimension_vertical(
                patch_y,
                smooth_top,
                patch_x - 48,
                f"smooth {mm(metrics.end_smooth_zone)} mm",
                patch_x - 8,
                patch_x + 22,
            ),
            dimension_vertical(
                smooth_bottom,
                patch_y + patch_h,
                patch_x - 48,
                f"smooth {mm(metrics.end_smooth_zone)} mm",
                patch_x - 8,
                patch_x + 22,
            ),
        ]
    )

    inset_x = panel_x + 26.0
    inset_y = panel_y + 362.0
    inset_w = 290.0
    inset_h = 160.0
    profile_scale = 120.0 / metrics.lower_circ_pitch
    x_left = inset_x + 20.0
    x_right = x_left + metrics.lower_circ_pitch * profile_scale
    x_flat_l = x_left + metrics.axial_run_to_flat * profile_scale
    x_flat_r = x_right - metrics.axial_run_to_flat * profile_scale
    y_base = inset_y + 116.0
    y_top = y_base - config.rise * 120.0
    svg.extend(
        [
            (
                f"<rect x='{panel_x:.2f}' y='{panel_y:.2f}' width='{panel_w:.2f}' height='760' "
                "rx='22' fill='#fffdf8' stroke='#314048' stroke-width='2' />"
            ),
            text(panel_x + 24, panel_y + 38, "Numeric checkpoint", 26, "#172127", 700),
            text(panel_x + 24, panel_y + 82, f"Target pitch {mm(config.target_pitch)} mm", 20, "#26333a", 500),
            text(panel_x + 24, panel_y + 116, f"Lower repeats {metrics.lower_repeats} -> {mm(metrics.lower_circ_pitch)} mm", 19, "#26333a", 400),
            text(panel_x + 24, panel_y + 146, f"Cap repeats {metrics.cap_repeats} -> {mm(metrics.cap_circ_pitch)} mm", 19, "#26333a", 400),
            text(panel_x + 24, panel_y + 192, f"Rise {mm(config.rise)} mm with {mm(config.flat_width)} mm flat top", 19, "#26333a", 400),
            text(panel_x + 24, panel_y + 222, f"Axial run to flat {mm(metrics.axial_run_to_flat)} mm", 19, "#26333a", 400),
            text(panel_x + 24, panel_y + 252, f"Overhang angle {mm(metrics.overhang_angle_rise_0_6)} deg at 0.6 rise", 19, "#26333a", 400),
            text(panel_x + 24, panel_y + 282, f"0.8 rise would be {mm(metrics.overhang_angle_rise_0_8)} deg", 19, "#26333a", 400),
            text(panel_x + 24, panel_y + 328, f"Raised max OD lower/cap {mm(metrics.additive_lower_max_od)} / {mm(metrics.additive_cap_max_od)}", 19, "#26333a", 400),
            text(panel_x + 24, panel_y + 358, f"39 OD margin lower/cap {mm(metrics.max_od_margin_lower)} / {mm(metrics.max_od_margin_cap)}", 19, "#26333a", 400),
            text(panel_x + 24, panel_y + 404, "Facet side profile, developed-surface section", 19, "#26333a", 600),
            (
                f"<rect x='{inset_x:.2f}' y='{inset_y:.2f}' width='{inset_w:.2f}' height='{inset_h:.2f}' "
                "rx='18' fill='#f3efe6' stroke='#cfd6d8' stroke-width='1.5' />"
            ),
            line(x_left, y_base, x_flat_l, y_top, "#48575f", 3.0),
            line(x_flat_l, y_top, x_flat_r, y_top, "#48575f", 3.0),
            line(x_flat_r, y_top, x_right, y_base, "#48575f", 3.0),
            line(x_left, y_base, x_right, y_base, "#88979e", 1.5),
            dimension_horizontal(
                x_left,
                x_right,
                inset_y + 142,
                f"pitch {mm(metrics.lower_circ_pitch)}",
                inset_y + 22,
                inset_y + 132,
            ),
            dimension_horizontal(
                x_flat_l,
                x_flat_r,
                inset_y + 52,
                f"flat {mm(config.flat_width)}",
                inset_y + 28,
                inset_y + 92,
            ),
            dimension_vertical(
                y_top,
                y_base,
                inset_x + inset_w - 28,
                f"rise {mm(config.rise)}",
                inset_x + inset_w - 74,
                inset_x + inset_w - 12,
            ),
            text(panel_x + 24, panel_y + 604, f"Study band rows {metrics.axial_rows}, cells {metrics.cell_count}", 19, "#26333a", 400),
            text(panel_x + 24, panel_y + 634, f"Equal end margins from complete rows: {mm(metrics.end_smooth_zone)} mm", 19, "#26333a", 400),
            text(panel_x + 24, panel_y + 680, "Coupon note: 5.6 mm cap window only fits one row at the main pitch.", 18, "#43525b", 400),
            text(panel_x + 24, panel_y + 708, f"Two rows need {mm(metrics.coupon_pitch_for_two_rows)} mm axial pitch or a shorter transition.", 18, "#43525b", 400),
            text(panel_x + 24, panel_y + 736, f"At 2.8 mm pitch, 0.6 rise is {mm(metrics.coupon_overhang_angle_rise_0_6)} deg.", 18, "#43525b", 400),
            text(panel_x + 24, panel_y + 782, "Global phase rule: keep one assembled Z0 and theta0, then clip full cells to allowed bands.", 18, "#43525b", 400),
        ]
    )

    svg.append("</svg>")
    return "".join(svg)


def main() -> None:
    config = StudyConfig()
    metrics = compute_metrics(config)
    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_SVG.write_text(render_svg(config, metrics), encoding="utf-8")
    OUTPUT_JSON.write_text(
        json.dumps(
            {
                "config": asdict(config),
                "metrics": asdict(metrics),
                "outputs": {
                    "svg": str(OUTPUT_SVG.relative_to(ROOT)),
                    "metrics_json": str(OUTPUT_JSON.relative_to(ROOT)),
                },
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(asdict(metrics), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
