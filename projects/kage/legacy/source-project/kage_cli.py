"""Command-line interface for the Kage optical and packaging contract."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Sequence

from p3_v3_mvp_base_q4_r1_physical_contract import (
    B0ContractError,
    json_report as b0_json_report,
    load_and_evaluate as load_b0_evaluation,
    text_report as b0_text_report,
)

from optical_spec import (
    body_stack_packaging,
    calculate_scenario,
    central_occlusion_check,
    halo_response,
    penumbra_width,
    projected_blocker,
    projected_offset,
    projected_direct_shaft_disc,
    projected_mask,
    projected_ring_carrier,
    projection_distances,
    stage_presets,
    upright_fin_reference,
    baffle_clear_radius_for_full_angle,
    cone_radius,
    fin_shadow_interval,
    projected_tangential_width,
    required_mask_radius,
    full_angle_to_half_angle_degrees,
    normalize_led_full_angle_degrees,
)


def _hand(value: str) -> tuple[str, str, float, float]:
    try:
        parts = value.split(":")
        if len(parts) == 3:
            name, length, width = parts
            shape = "blade"
        else:
            name, shape, length, width = parts
        return name, shape, float(length), float(width)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("hand must be NAME:SHAPE:LENGTH_MM:WIDTH_MM") from exc


def _hardware(value: str) -> tuple[str, float, float]:
    try:
        name, radius, distance = value.split(":")
        return name, float(radius), float(distance)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("hardware must be NAME:RADIUS_MM:SOURCE_DISTANCE_MM") from exc


def _projection_payload(args: argparse.Namespace) -> dict[str, Any]:
    distances = projection_distances(args.source_hand, args.hand_wall)
    hands = {
        name: projected_blocker(
            name=name,
            shape=shape,
            radial_length_mm=length,
            width_mm=width,
            source_hand_mm=args.source_hand,
            hand_wall_mm=args.hand_wall,
            occluder_radius_mm=args.occluder_radius,
        )
        for name, shape, length, width in args.hand
    }
    return {
        "schema_version": 1,
        "calculation": "projection",
        "angle_semantics": "optical blocker geometry only; no drive mechanism is modeled",
        "distances": distances,
        "aperture_mm": args.aperture,
        "penumbra_mm": penumbra_width(args.aperture, args.source_hand, args.hand_wall),
        "offset": projected_offset(args.offset_x, args.offset_y, args.source_hand, args.hand_wall),
        "hands": hands,
        "projected_sweep_diameter_mm": max(hand["projected_length_mm"] for hand in hands.values()) * 2,
    }


def _ring_carrier_payload(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "calculation": "ring-carrier",
        "carrier": projected_ring_carrier(
            name=args.name,
            carrier_inner_radius_mm=args.inner_radius,
            carrier_outer_radius_mm=args.outer_radius,
            blocker_radial_start_mm=args.blocker_start,
            blocker_radial_end_mm=args.blocker_end,
            blocker_width_mm=args.blocker_width,
            blocker_shape=args.shape,
            axial_plane_offset_mm=args.axial_offset,
            source_hand_mm=args.source_hand,
            hand_wall_mm=args.hand_wall,
            effective_occluder_radius_mm=args.occluder_radius,
            optical_angle_degrees=args.optical_angle,
            effective_aperture_mm=args.aperture,
            carrier_thickness_mm=args.carrier_thickness,
            axial_gap_mm=args.axial_gap,
            exposed_drive_radius_mm=args.drive_radius,
            clear_center_radius_mm=args.clear_center_radius,
            pivot_offset_mm=args.pivot_offset,
        ),
        "architecture_role": "comparison-only hollow-center hypothesis",
        "drive_mechanism": "not modeled",
    }


def _mask_payload(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "calculation": "fixed-mask",
        "result": projected_mask(
            physical_radius_mm=args.radius,
            mask_z_mm=args.mask_z,
            source_z_mm=args.source_z,
            wall_z_mm=args.wall_z,
        ),
        "note": "Only this real between-source-and-wall mask creates central wall occlusion; the room-side cosmetic shell does not.",
    }


def _direct_disc_payload(args: argparse.Namespace) -> dict[str, Any]:
    mask = projected_mask(
        physical_radius_mm=args.mask_radius,
        mask_z_mm=args.mask_z,
        source_z_mm=args.source_z,
        wall_z_mm=args.wall_z,
    )
    return {
        "schema_version": 1,
        "calculation": "direct-shaft-disc",
        "mask": mask,
        "disc": projected_direct_shaft_disc(
            name=args.name,
            plane_z_mm=args.plane_z,
            source_z_mm=args.source_z,
            wall_z_mm=args.wall_z,
            carrier_outer_radius_mm=args.carrier_radius,
            blocker_radial_start_mm=args.blocker_start,
            blocker_radial_end_mm=args.blocker_end,
            blocker_width_mm=args.blocker_width,
            blocker_shape=args.shape,
            projected_mask_radius_mm=mask["projected_radius_mm"],
            effective_aperture_mm=args.aperture,
            required_hide_margin_mm=args.hide_margin,
            optical_angle_degrees=args.optical_angle,
        ),
    }


def _body_payload(args: argparse.Namespace) -> dict[str, Any]:
    packaging = body_stack_packaging(
        front_occluder_diameter_mm=args.front_diameter,
        front_occluder_depth_mm=args.front_depth,
        rear_pod_diameter_mm=args.pod_diameter,
        rear_pod_depth_mm=args.pod_depth,
        pod_front_overlap_mm=args.overlap,
        wall_gap_mm=args.wall_gap,
        hand_plane_to_pod_rear_mm=args.hand_to_rear,
        source_hand_mm=args.source_hand,
        source_recess_mm=args.source_recess,
        movement_allowance_mm=args.movement,
        rear_opening_diameter_mm=args.rear_opening,
        movement_envelope_width_mm=args.movement_width,
        movement_envelope_height_mm=args.movement_height,
    )
    return {
        "schema_version": 1,
        "calculation": "body",
        "inputs": {
            "front_occluder_diameter_mm": args.front_diameter,
            "front_occluder_depth_mm": args.front_depth,
            "rear_pod_diameter_mm": args.pod_diameter,
            "rear_pod_depth_mm": args.pod_depth,
            "pod_front_overlap_mm": args.overlap,
            "wall_gap_mm": args.wall_gap,
            "hand_plane_to_pod_rear_mm": args.hand_to_rear,
            "source_hand_mm": args.source_hand,
            "source_recess_mm": args.source_recess,
            "movement_allowance_mm": args.movement,
            "rear_opening_diameter_mm": args.rear_opening,
            "movement_envelope_width_mm": args.movement_width,
            "movement_envelope_height_mm": args.movement_height,
        },
        "derived": packaging,
    }


def _occlusion_payload(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "calculation": "central-occlusion",
        "result": central_occlusion_check(
            occluder_radius_mm=args.occluder_radius,
            occluder_source_distance_mm=args.occluder_distance,
            hardware={name: (radius, distance) for name, radius, distance in args.hardware},
        ),
    }


def _text(payload: dict[str, Any]) -> str:
    if "scenarios" in payload:
        return "\n".join(f"{item['name']:<18} {item['description']}" for item in payload["scenarios"])
    if payload.get("calculation") == "projection":
        d = payload["distances"]
        lines = [
            f"D = L + W          {d['source_wall_mm']:.2f} mm",
            f"Magnification      {d['magnification']:.4f}x",
            f"Penumbra (approx.) {payload['penumbra_mm']:.2f} mm",
        ]
        lines.extend(
            f"{name.title():<10} [{hand['shape']}] projected {hand['projected_length_mm']:.2f} mm; visible {hand['visible_length_mm']:.2f} mm"
            for name, hand in payload["hands"].items()
        )
        return "\n".join(lines)
    if payload.get("calculation") == "body":
        d = payload["derived"]
        return "\n".join(
            [
                f"Overall depth       {d['overall_depth_mm']:.2f} mm",
                f"Front → wall        {d['total_front_to_wall_mm']:.2f} mm",
                f"Hand plane          {d['hand_plane_from_front_mm']:.2f} mm from front",
                f"Aperture plane      {d['aperture_plane_from_front_mm']:.2f} mm from front",
                f"Hand → wall         {d['hand_wall_mm']:.2f} mm",
                f"Optical allowance   {d['optical_packaging_allowance_mm']:.2f} mm",
                f"Movement allowance  {d['movement_packaging_allowance_mm']:.2f} mm",
                f"Radial shoulder     {d['radial_shoulder_mm']:.2f} mm",
                f"Rear opening        {d['rear_opening_diameter_mm']:.2f} mm",
                f"Pod wall at opening {d['rear_opening_radial_wall_mm']:.2f} mm",
                f"Movement clearance  {d['movement_lateral_clearance_mm']:.2f} mm radial",
                f"Fits axially        {'yes' if d['fits_axially'] else 'NO'}",
            ]
        )
    if payload.get("calculation") == "ring-carrier":
        carrier = payload["carrier"]
        return "\n".join(
            [
                f"Carrier             {carrier['name']} / {carrier['blocker_shape']}",
                f"Ring radii          {carrier['carrier_inner_radius_mm']:.2f} → {carrier['carrier_outer_radius_mm']:.2f} mm",
                f"Blocker span        {carrier['blocker_radial_start_mm']:.2f} → {carrier['blocker_radial_end_mm']:.2f} mm",
                f"Axial offset        {carrier['axial_plane_offset_mm']:.2f} mm",
                f"Li / Wi / Mi        {carrier['effective_source_hand_mm']:.2f} / {carrier['effective_hand_wall_mm']:.2f} mm / {carrier['magnification']:.5f}x",
                f"Penumbra            {carrier['penumbra_mm']:.3f} mm",
                f"Projected span      {carrier['projected_radial_start_mm']:.2f} → {carrier['projected_radial_end_mm']:.2f} mm",
                f"Visible span        {carrier['visible_projected_span_mm']:.2f} mm",
                f"Carrier hide margin {carrier['carrier_hide_margin_mm']:.2f} mm",
                f"Optical angle       {carrier['optical_angle_degrees']:.2f}° (not drive geometry)",
                "Drive mechanism      not modeled",
                "Failure flags        " + (", ".join(flag for flag, failed in carrier["failure_flags"].items() if failed) or "none"),
            ]
        )
    if payload.get("calculation") == "fixed-mask":
        result = payload["result"]
        return "\n".join([
            f"Physical mask       Ø{result['physical_diameter_mm']:.3f} mm at z={result['mask_z_mm']:.2f} mm",
            f"Source / wall z     {result['source_z_mm']:.2f} / {result['wall_z_mm']:.2f} mm",
            f"Mask magnification  {result['magnification']:.6f}x",
            f"Wall shadow         Ø{result['projected_diameter_mm']:.3f} mm",
        ])
    if payload.get("calculation") == "direct-shaft-disc":
        disc = payload["disc"]
        return "\n".join([
            f"Disc                {disc['name']} / {disc['blocker_shape']}",
            f"Plane z / L / W      {disc['plane_z_mm']:.2f} / {disc['source_blocker_mm']:.2f} / {disc['blocker_wall_mm']:.2f} mm",
            f"Magnification       {disc['magnification']:.6f}x",
            f"Penumbra            {disc['penumbra_mm']:.3f} mm",
            f"Projected tip       {disc['projected_tip_mm']:.3f} mm",
            f"Visible beyond mask {disc['visible_length_mm']:.3f} mm",
            f"Carrier hide margin {disc['carrier_hide_margin_mm']:.3f} mm",
            f"Full light field    {disc['required_full_field_angle_degrees']:.3f}°",
            f"Carrier hidden      {'yes' if disc['carrier_hidden'] else 'NO'}",
        ])
    if payload.get("calculation") == "central-occlusion":
        result = payload["result"]
        lines = [
            f"Occluder r/z       {result['occluder_angular_extent']:.6f}",
            f"All hardware hidden {'yes' if result['all_hardware_hidden'] else 'NO'}",
        ]
        lines.extend(
            f"{name:<20} margin {component['angular_hide_margin']:.6f}  {'hidden' if component['hidden'] else 'EXPOSED'}"
            for name, component in result["components"].items()
        )
        return "\n".join(lines)
    if payload.get("calculation") == "upright-fin-optics":
        result = payload["result"]
        lines = [
            f"Architecture         {result['architecture']}",
            f"Wall / source z      {result['wall_z']:.2f} / {result['source_z']:.2f} mm",
            f"Mask                 r{result['mask_physical_radius']:.3f} at z={result['mask_z']:.2f} -> r{result['projected_mask_radius']:.2f}",
        ]
        for name, fin in result["fins"].items():
            lines.append(
                f"{name.title():<10} upright fin r{fin['radius']:.1f}; z {fin['base_z']:.3f}..{fin['tip_z']:.3f}; shadow r{fin['start_radius']:.1f}..{fin['tip_radius']:.1f}"
            )
        custom = payload.get("custom")
        if custom:
            fin = custom["fin"]
            baffle = "unbounded at 180° full field" if custom["baffle_clearance_unbounded"] else f"clear r{custom['baffle_clear_radius']:.3f} mm"
            lines.extend([
                f"Custom fin          shadow r{fin['start_radius']:.3f}..{fin['tip_radius']:.3f}; width at tip {fin['projected_tip_width']:.3f} mm",
                f"Custom mask / cone  r{custom['mask_physical_radius']:.3f} / r{custom['cone_radius']:.3f} mm",
                f"LED field           {custom['led_clear_full_angle_degrees']:.1f}° full / {custom['optical_half_angle_degrees']:.1f}° half",
                f"Custom baffle       {baffle}",
            ])
        return "\n".join(lines)
    if "scenario" in payload:
        o = payload["optics"]
        lines = [
            f"{payload['scenario']} — {payload['description']}",
            f"Provenance: {payload['provenance']}",
            f"L / W / D           {o['source_hand_mm']:.1f} / {o['hand_wall_mm']:.1f} / {o['source_wall_mm']:.1f} mm",
            f"Magnification       {o['magnification']:.4f}x",
            f"Penumbra (approx.)  {o['penumbra_mm']:.2f} mm",
            f"Projected sweep     {o['projected_sweep_diameter_mm']:.2f} mm",
            (
                f"Halo diameter       {payload['halo']['diameter_mm']:.2f} mm"
                if payload["halo"]["enabled"]
                else "Halo                disabled for this stage"
            ),
        ]
        movement = payload["movement"]
        lines.extend(
            [
                f"Movement type       {movement['movement_type']}",
                f"Drive assumption    {movement['drive_mechanism']}",
                f"Drive geometry      {'modeled' if movement['drive_geometry_modeled'] else 'not modeled'}",
                "Angles               optical blocker state, not a gear/drive model",
            ]
        )
        for name, carrier in movement["carriers"].items():
            if carrier["movement_type"] == "quartz-direct-shaft-orbital-disc":
                lines.append(
                    f"{name.title()} disc         z {carrier['plane_z_mm']:.1f}; L {carrier['source_blocker_mm']:.1f} / W {carrier['blocker_wall_mm']:.1f} / M {carrier['magnification']:.5f}; "
                    f"tip {carrier['projected_tip_mm']:.2f}; visible {carrier['visible_length_mm']:.2f}; hide {carrier['carrier_hide_margin_mm']:.2f} mm"
                )
            else:
                lines.append(
                    f"{name.title()} ring         L {carrier['effective_source_hand_mm']:.1f} / W {carrier['effective_hand_wall_mm']:.1f} / M {carrier['magnification']:.5f}; "
                    f"tip {carrier['projected_tip_mm']:.2f}; visible {carrier['visible_length_mm']:.2f}; hide {carrier['carrier_hide_margin_mm']:.2f} mm"
                )
        if movement["failure_flags"]:
            failed = [flag for flag, active in movement["failure_flags"].items() if active]
            lines.append("Orbital failure flags " + (", ".join(failed) if failed else "none"))
        if payload["body"]:
            body = payload["body"]["derived"]
            lines.extend(
                [
                    f"Overall body depth  {body['overall_depth_mm']:.2f} mm",
                    f"Total stand-off     {body['total_front_to_wall_mm']:.2f} mm",
                    f"Packaging allowance {body['optical_packaging_allowance_mm']:.2f} mm",
                    f"Rear opening        {body['rear_opening_diameter_mm']:.2f} mm",
                    f"Movement envelope   {body['movement_envelope_width_mm']:.0f} × {body['movement_envelope_height_mm']:.0f} × 15 mm",
                ]
            )
        lines.extend(
            f"{name.title()} [{hand['shape']}] projected {hand['projected_length_mm']:.2f} mm; visible {hand['visible_length_mm']:.2f} mm"
            for name, hand in o["hands"].items()
        )
        if payload["warnings"]:
            lines.append("Warnings: " + ", ".join(payload["warnings"]))
        return "\n".join(lines)
    return json.dumps(payload, indent=2, sort_keys=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="kage-clock", description="Kage shadow-clock optical and packaging calculator")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON (may appear before or after the command)")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="list named scenarios")
    upright = sub.add_parser("upright-optics", help="calculate the constant-radius upright rim-fin reference")
    upright.add_argument("--source-z", type=float, default=40.0, metavar="MM")
    upright.add_argument("--carrier-pitch", type=float, default=4.75, metavar="MM")
    upright.add_argument("--fin-radius", type=float, default=30.0, metavar="MM")
    upright.add_argument("--base-z", type=float, default=15.0, metavar="MM")
    upright.add_argument("--tip-z", type=float, default=25.882352941, metavar="MM")
    upright.add_argument("--fin-width", type=float, default=3.2, metavar="MM")
    upright.add_argument("--mask-z", type=float, default=6.0, metavar="MM")
    upright.add_argument("--mask-wall-radius", type=float, default=50.0, metavar="MM")
    upright.add_argument("--wall-radius", type=float, default=130.0, metavar="MM")
    upright.add_argument("--cone-plane-z", type=float, default=23.076923077, metavar="MM")
    upright.add_argument("--baffle-distance", type=float, default=3.0, metavar="MM")
    upright.add_argument("--full-angle", type=float, default=None, metavar="DEG")
    upright.add_argument("--half-angle", type=float, default=None, metavar="DEG", help=argparse.SUPPRESS)
    upright.add_argument("--margin", type=float, default=1.0, metavar="MM")
    scenario = sub.add_parser("scenario", help="calculate a named design scenario")
    scenario.add_argument("name", choices=sorted(stage_presets()))

    projection = sub.add_parser("projection", help="calculate pinhole projection and penumbra")
    projection.add_argument("--source-hand", type=float, required=True, metavar="MM")
    projection.add_argument("--hand-wall", type=float, required=True, metavar="MM")
    projection.add_argument("--aperture", type=float, default=0.8, metavar="MM")
    projection.add_argument("--offset-x", type=float, default=0, metavar="MM")
    projection.add_argument("--offset-y", type=float, default=0, metavar="MM")
    projection.add_argument("--occluder-radius", type=float, default=0, metavar="MM")
    projection.add_argument(
        "--hand",
        action="append",
        type=_hand,
        default=None,
        metavar="NAME:SHAPE:LENGTH:WIDTH",
        help="repeat for each hand; defaults to hour, minute, and second reference hands",
    )

    ring = sub.add_parser("ring-carrier", help="comparison only: project one hollow-center ring carrier")
    ring.add_argument("--name", default="hour")
    ring.add_argument("--inner-radius", type=float, required=True, metavar="MM")
    ring.add_argument("--outer-radius", type=float, required=True, metavar="MM")
    ring.add_argument("--blocker-start", type=float, required=True, metavar="MM")
    ring.add_argument("--blocker-end", type=float, required=True, metavar="MM")
    ring.add_argument("--blocker-width", type=float, required=True, metavar="MM")
    ring.add_argument("--shape", required=True)
    ring.add_argument("--axial-offset", type=float, default=0, metavar="MM")
    ring.add_argument("--source-hand", type=float, required=True, metavar="MM")
    ring.add_argument("--hand-wall", type=float, required=True, metavar="MM")
    ring.add_argument("--occluder-radius", type=float, default=0, metavar="MM")
    ring.add_argument("--optical-angle", type=float, default=0, metavar="DEG")
    ring.add_argument("--aperture", type=float, default=0.8, metavar="MM")
    ring.add_argument("--carrier-thickness", type=float, default=1.2, metavar="MM")
    ring.add_argument("--axial-gap", type=float, default=0.4, metavar="MM")
    ring.add_argument("--drive-radius", type=float, default=49.5, metavar="MM")
    ring.add_argument("--clear-center-radius", type=float, default=18, metavar="MM")
    ring.add_argument("--pivot-offset", type=float, default=0, metavar="MM")

    mask = sub.add_parser("mask", help="project the real fixed central mask onto the wall")
    mask.add_argument("--radius", type=float, default=55.5714285714, metavar="MM")
    mask.add_argument("--mask-z", type=float, default=60, metavar="MM")
    mask.add_argument("--source-z", type=float, default=104.8, metavar="MM")
    mask.add_argument("--wall-z", type=float, default=0, metavar="MM")

    disc = sub.add_parser("direct-disc", help="project one stock-quartz direct-shaft blocker disc")
    disc.add_argument("--name", choices=("hour", "minute", "second"), required=True)
    disc.add_argument("--plane-z", type=float, required=True, metavar="MM")
    disc.add_argument("--carrier-radius", type=float, default=47, metavar="MM")
    disc.add_argument("--blocker-start", type=float, default=47, metavar="MM")
    disc.add_argument("--blocker-end", type=float, required=True, metavar="MM")
    disc.add_argument("--blocker-width", type=float, required=True, metavar="MM")
    disc.add_argument("--shape", required=True)
    disc.add_argument("--source-z", type=float, default=104.8, metavar="MM")
    disc.add_argument("--wall-z", type=float, default=0, metavar="MM")
    disc.add_argument("--mask-radius", type=float, default=55.5714285714, metavar="MM")
    disc.add_argument("--mask-z", type=float, default=60, metavar="MM")
    disc.add_argument("--aperture", type=float, default=0.8, metavar="MM")
    disc.add_argument("--hide-margin", type=float, default=5, metavar="MM")
    disc.add_argument("--optical-angle", type=float, default=0, metavar="DEG")

    occlusion = sub.add_parser("occlusion", help="verify that measured central hardware stays inside the occluder shadow")
    occlusion.add_argument("--occluder-radius", type=float, required=True, metavar="MM")
    occlusion.add_argument("--occluder-distance", type=float, required=True, metavar="MM")
    occlusion.add_argument(
        "--hardware", action="append", type=_hardware, required=True,
        metavar="NAME:RADIUS:SOURCE_DISTANCE",
        help="repeat for movement body corners, stand, washer, nut, and hubs",
    )

    body = sub.add_parser("body", help="calculate stepped-body axial and radial packaging")
    body.add_argument("--front-diameter", type=float, default=260)
    body.add_argument("--front-depth", type=float, default=12)
    body.add_argument("--pod-diameter", type=float, default=150)
    body.add_argument("--pod-depth", type=float, default=60)
    body.add_argument("--overlap", type=float, default=2)
    body.add_argument("--wall-gap", type=float, default=45)
    body.add_argument("--hand-to-rear", type=float, default=15)
    body.add_argument("--source-hand", type=float, default=42)
    body.add_argument("--source-recess", type=float, default=13)
    body.add_argument("--movement", type=float, default=15)
    body.add_argument("--rear-opening", type=float, default=120)
    body.add_argument("--movement-width", type=float, default=56)
    body.add_argument("--movement-height", type=float, default=56)
    b0 = sub.add_parser("b0-evaluate", help="evaluate one completed KAGE B0 Q4-R1 physical-results JSON file")
    b0.add_argument("path", metavar="PATH/TO/b0-results.json")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    values = list(sys.argv[1:] if argv is None else argv)
    json_requested = "--json" in values
    values = [value for value in values if value != "--json"]
    parser = build_parser()
    args = parser.parse_args(values)
    args.json = json_requested
    if args.command == "b0-evaluate":
        try:
            payload = load_b0_evaluation(args.path)
        except B0ContractError as exc:
            print(f"kage-clock b0-evaluate: error: {exc}", file=sys.stderr)
            return 2
        sys.stdout.write(b0_json_report(payload) if args.json else b0_text_report(payload))
        return payload["exit_code"]
    try:
        if args.command == "list":
            payload = {
                "schema_version": 1,
                "scenarios": [
                    {"name": name, "description": preset["description"], "provenance": preset["provenance"]}
                    for name, preset in stage_presets().items()
                ],
            }
        elif args.command == "scenario":
            payload = calculate_scenario(args.name)
        elif args.command == "projection":
            args.hand = args.hand or [
                ("hour", "leaf-kite", 60.0, 9.0),
                ("minute", "blade", 70.0, 2.4),
                ("second", "needle", 85.0, 0.8),
            ]
            payload = _projection_payload(args)
        elif args.command == "upright-optics":
            requested_full_angle = args.full_angle if args.full_angle is not None else (args.half_angle * 2.0 if args.half_angle is not None else 150.0)
            normalized_full_angle = normalize_led_full_angle_degrees(requested_full_angle)
            half_angle = full_angle_to_half_angle_degrees(requested_full_angle)
            payload = {
                "schema_version": 1,
                "calculation": "upright-fin-optics",
                "result": upright_fin_reference(args.source_z, args.carrier_pitch),
                "custom": {
                    "fin": {
                        **fin_shadow_interval(args.source_z, args.fin_radius, args.base_z, args.tip_z),
                        "projected_tip_width": projected_tangential_width(args.source_z, args.fin_width, args.tip_z),
                    },
                    "mask_physical_radius": required_mask_radius(args.source_z, args.mask_wall_radius, args.mask_z),
                    "cone_radius": cone_radius(args.source_z, args.wall_radius, args.cone_plane_z),
                    "led_clear_full_angle_degrees": normalized_full_angle,
                    "optical_half_angle_degrees": half_angle,
                    "full_angle_was_clamped": normalized_full_angle != requested_full_angle,
                    "baffle_clear_radius": baffle_clear_radius_for_full_angle(args.baffle_distance, normalized_full_angle, args.margin),
                    "baffle_clearance_unbounded": half_angle == 90.0,
                },
            }
        elif args.command == "ring-carrier":
            payload = _ring_carrier_payload(args)
        elif args.command == "mask":
            payload = _mask_payload(args)
        elif args.command == "direct-disc":
            payload = _direct_disc_payload(args)
        elif args.command == "occlusion":
            payload = _occlusion_payload(args)
        else:
            payload = _body_payload(args)
    except (ValueError, KeyError) as exc:
        parser.error(str(exc))
    print(json.dumps(payload, indent=2, sort_keys=True) if args.json else _text(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
