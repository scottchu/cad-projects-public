"""Pure final-results evaluator for the KAGE B0 Q4-R1 physical card v3.

This module reads evidence already recorded by a human.  It does not prompt,
schedule work, mutate result files, inspect photographs, or approve the article.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP
import json
from pathlib import Path
import re
from typing import Any, Iterable

from p3_v3_mvp_base_q4_r1_spec import NAMESPACE, SPEC


INPUT_SCHEMA = "kage.b0.q4-r1.physical-results.v3"
OUTPUT_SCHEMA = "kage.b0.q4-r1.physical-evaluation.v3"


@dataclass(frozen=True)
class B0PhysicalAcceptance:
    card_version: str = "v3"
    card_sha256: str = "cb37c040fcf06f1bc807155044638f25ac359b638dd70b586bffa7b7999a046c"
    od_tolerance_mm: Decimal = Decimal("0.50")
    od_range_max_mm: Decimal = Decimal("0.50")
    od_resolution_max_mm: Decimal = Decimal("0.25")
    seam_gap_min_mm: Decimal = Decimal("0.05")
    seam_gap_max_mm: Decimal = Decimal("0.30")
    seam_step_max_mm: Decimal = Decimal("0.25")
    flatness_max_mm: Decimal = Decimal("0.50")
    reference_plane_feeler_max_mm: Decimal = Decimal("0.25")
    pin_motion_max_mm: Decimal = Decimal("0.00")
    assembly_cycle_count: int = 3
    unconstrained_wait_min: int = 60
    vertical_dwell_min: int = 60
    vertical_down_quadrant: str = "Q1"
    lift_height_min_mm: Decimal = Decimal("50")
    lift_hold_min_seconds: Decimal = Decimal("3")
    lift_sequence: tuple[str, ...] = (
        "Q1", "Q2", "Q3", "Q4", "Q1", "Q2", "Q3", "Q4", "Q1", "Q3"
    )

    @property
    def od_min_mm(self) -> Decimal:
        return Decimal(str(SPEC.base_outer_diameter_mm)) - self.od_tolerance_mm

    @property
    def od_max_mm(self) -> Decimal:
        return Decimal(str(SPEC.base_outer_diameter_mm)) + self.od_tolerance_mm

    @property
    def pin_target_exposure_mm(self) -> Decimal:
        return Decimal(str(SPEC.base_split_slip_engagement_mm))


B0_PHYSICAL_ACCEPTANCE = B0PhysicalAcceptance()

CHECK_IDS = (
    "01_loop_od",
    "02_seam_gap_step",
    "03_free_state_flatness",
    "04_service_cycles",
    "05_vertical_retention",
    "06_lift_place",
)
CHECK_LABELS = {
    "01_loop_od": "01 loop + OD",
    "02_seam_gap_step": "02 seam gap + step",
    "03_free_state_flatness": "03 free-state flatness",
    "04_service_cycles": "04 three service cycles",
    "05_vertical_retention": "05 vertical retention",
    "06_lift_place": "06 ten lift/place cycles",
}
STATUS_RANK = {"pass": 0, "borderline": 1, "incomplete": 2, "fail": 3}
CHECKPOINT_NAMES = ("cycle1_free_state", "after_vertical", "after_lift_place")
DIAMETER_KEYS = ("d0", "d45", "d90", "d135")
SEAMS = tuple(f"S{index}" for index in range(1, SPEC.bridge_count_total + 1))
GAP_POSITIONS = ("inner", "middle", "outer")
STEP_KEYS = tuple(
    f"S{seam}-{side}"
    for seam in range(1, SPEC.bridge_count_total + 1)
    for side in ("A", "B")
)
PIN_IDS = tuple(
    f"S{seam}-R{int(radius)}"
    for seam in range(1, SPEC.bridge_count_total + 1)
    for radius in SPEC.dowel_axis_radii_mm
)
FASTENER_IDS = tuple(
    f"S{seam}-{side}"
    for seam in range(1, SPEC.bridge_count_total + 1)
    for side in ("A", "B")
)
PHOTO_KEYS = (
    "parts_and_hardware",
    "hardware_fit",
    "reference_plane",
    "supported_quadrants_s1_s3",
    "s4_half_inserted",
    "s4_fully_seated",
    "cycle1_front",
    "cycle1_underside",
    "od_measurement_setup",
    "worst_seam_measurement",
    "worst_flatness_measurement",
    "vertical_start_q1_down",
    "vertical_end_q1_down",
    "final_front",
    "final_underside",
)
PHOTO_OWNERS = {
    "parts_and_hardware": "04_service_cycles",
    "hardware_fit": "04_service_cycles",
    "reference_plane": "03_free_state_flatness",
    "supported_quadrants_s1_s3": "01_loop_od",
    "s4_half_inserted": "01_loop_od",
    "s4_fully_seated": "01_loop_od",
    "cycle1_front": "01_loop_od",
    "cycle1_underside": "01_loop_od",
    "od_measurement_setup": "01_loop_od",
    "worst_seam_measurement": "02_seam_gap_step",
    "worst_flatness_measurement": "03_free_state_flatness",
    "vertical_start_q1_down": "05_vertical_retention",
    "vertical_end_q1_down": "05_vertical_retention",
    "final_front": "06_lift_place",
    "final_underside": "06_lift_place",
}
STABLE_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/-]*\Z")


class B0ContractError(ValueError):
    """Unreadable, malformed, identity, type, or value error (CLI exit 2)."""


@dataclass(frozen=True)
class _Reason:
    severity: str
    code: str
    path: str
    expected: Any
    actual: Any

    def public(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "path": self.path,
            "expected": _public(self.expected),
            "actual": _public(self.actual),
        }


class _Context:
    def __init__(self, input_path: Path):
        self.input_path = input_path
        self.reasons: dict[str, list[_Reason]] = {check: [] for check in CHECK_IDS}
        self.missing_fields: list[str] = []
        self.warnings: list[dict[str, str]] = []

    def add(self, check: str, severity: str, code: str, path: str, expected: Any, actual: Any) -> None:
        self.reasons[check].append(_Reason(severity, code, path, expected, actual))

    def missing(self, check: str, path: str) -> None:
        if path not in self.missing_fields:
            self.missing_fields.append(path)
        self.add(check, "incomplete", "missing_field", path, "required", None)

    def warn_unknown(self, obj: dict[str, Any], allowed: Iterable[str], path: str) -> None:
        allowed_set = set(allowed)
        for key in obj:
            if key not in allowed_set:
                field_path = f"{path}.{key}" if path else key
                self.warnings.append({"code": "unknown_field", "path": field_path})


def _public(value: Any) -> Any:
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, tuple):
        return [_public(item) for item in value]
    if isinstance(value, list):
        return [_public(item) for item in value]
    if isinstance(value, dict):
        return {key: _public(item) for key, item in value.items()}
    return value


def _object(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise B0ContractError(f"{path} must be an object")
    return value


def _array(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        raise B0ContractError(f"{path} must be an array")
    return value


def _decimal(value: Any, path: str) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (int, Decimal)):
        raise B0ContractError(f"{path} must be a finite JSON number, not a boolean")
    result = value if isinstance(value, Decimal) else Decimal(value)
    if not result.is_finite():
        raise B0ContractError(f"{path} must be finite")
    return result


def _required_object(parent: dict[str, Any], key: str, path: str, ctx: _Context, owner: str) -> dict[str, Any] | None:
    field = f"{path}.{key}" if path else key
    if key not in parent:
        ctx.missing(owner, field)
        return None
    return _object(parent[key], field)


def _required_array(parent: dict[str, Any], key: str, path: str, ctx: _Context, owner: str) -> list[Any] | None:
    field = f"{path}.{key}" if path else key
    if key not in parent:
        ctx.missing(owner, field)
        return None
    return _array(parent[key], field)


def _required_string(parent: dict[str, Any], key: str, path: str, ctx: _Context, owner: str) -> str | None:
    field = f"{path}.{key}" if path else key
    if key not in parent:
        ctx.missing(owner, field)
        return None
    value = parent[key]
    if not isinstance(value, str):
        raise B0ContractError(f"{field} must be a string")
    if not value.strip():
        ctx.add(owner, "incomplete", "empty_field", field, "nonempty string", value)
        return None
    return value


def _required_bool(parent: dict[str, Any], key: str, path: str, ctx: _Context, owner: str) -> bool | None:
    field = f"{path}.{key}" if path else key
    if key not in parent:
        ctx.missing(owner, field)
        return None
    value = parent[key]
    if not isinstance(value, bool):
        raise B0ContractError(f"{field} must be a boolean")
    return value


def _required_number(parent: dict[str, Any], key: str, path: str, ctx: _Context, owner: str) -> Decimal | None:
    field = f"{path}.{key}" if path else key
    if key not in parent:
        ctx.missing(owner, field)
        return None
    return _decimal(parent[key], field)


def _status(reasons: list[_Reason]) -> str:
    if not reasons:
        return "pass"
    return max((reason.severity for reason in reasons), key=STATUS_RANK.__getitem__)


def _inside_interval(value: Decimal, uncertainty: Decimal, minimum: Decimal, maximum: Decimal) -> str:
    low, high = value - uncertainty, value + uncertainty
    if low > minimum and high < maximum:
        return "pass"
    if high < minimum or low > maximum:
        return "fail"
    return "borderline"


def _maximum_interval(value: Decimal, uncertainty: Decimal, maximum: Decimal) -> str:
    if value + uncertainty < maximum:
        return "pass"
    if value - uncertainty > maximum:
        return "fail"
    return "borderline"


def _unknowns(ctx: _Context, obj: dict[str, Any], allowed: Iterable[str], path: str) -> None:
    ctx.warn_unknown(obj, allowed, path)


def _parse_systems(doc: dict[str, Any], ctx: _Context) -> dict[str, dict[str, Any] | None]:
    owners = {
        "od": "01_loop_od",
        "gap": "02_seam_gap_step",
        "step": "02_seam_gap_step",
        "flatness": "03_free_state_flatness",
        "pin_exposure": "04_service_cycles",
    }
    container = doc.get("measurement_systems")
    if container is None:
        for name, owner in owners.items():
            ctx.missing(owner, f"measurement_systems.{name}")
        return {name: None for name in owners}
    systems_obj = _object(container, "measurement_systems")
    _unknowns(ctx, systems_obj, owners, "measurement_systems")
    result: dict[str, dict[str, Any] | None] = {}
    for name, owner in owners.items():
        path = f"measurement_systems.{name}"
        if name not in systems_obj:
            ctx.missing(owner, path)
            result[name] = None
            continue
        system = _object(systems_obj[name], path)
        flag = "verified" if name == "od" else "calibrated"
        _unknowns(ctx, system, ("name", "resolution_mm", "uncertainty_mm", flag), path)
        instrument_name = _required_string(system, "name", path, ctx, owner)
        resolution = _required_number(system, "resolution_mm", path, ctx, owner)
        uncertainty = _required_number(system, "uncertainty_mm", path, ctx, owner)
        qualified = _required_bool(system, flag, path, ctx, owner)
        if resolution is not None and resolution <= 0:
            raise B0ContractError(f"{path}.resolution_mm must be greater than zero")
        if uncertainty is not None and uncertainty < 0:
            raise B0ContractError(f"{path}.uncertainty_mm must be nonnegative")
        if qualified is False:
            ctx.add(owner, "incomplete", "instrument_unqualified", f"{path}.{flag}", True, False)
        if name == "od" and resolution is not None and resolution > B0_PHYSICAL_ACCEPTANCE.od_resolution_max_mm:
            ctx.add(
                owner,
                "incomplete",
                "instrument_resolution_inadequate",
                f"{path}.resolution_mm",
                f"<= {B0_PHYSICAL_ACCEPTANCE.od_resolution_max_mm}",
                resolution,
            )
        result[name] = {
            "name": instrument_name,
            "resolution_mm": resolution,
            "uncertainty_mm": uncertainty,
            flag: qualified,
        }
    return result


def _parse_print(doc: dict[str, Any], ctx: _Context) -> None:
    owner = "04_service_cycles"
    obj = _required_object(doc, "print", "", ctx, owner)
    if obj is None:
        return
    _unknowns(ctx, obj, ("material", "printer", "profile", "date", "nozzle_mm", "layer_height_mm"), "print")
    for key in ("material", "printer", "profile"):
        _required_string(obj, key, "print", ctx, owner)
    date_value = _required_string(obj, "date", "print", ctx, owner)
    if date_value is not None:
        try:
            date.fromisoformat(date_value)
        except ValueError as exc:
            raise B0ContractError("print.date must be an ISO date") from exc
    for key in ("nozzle_mm", "layer_height_mm"):
        number = _required_number(obj, key, "print", ctx, owner)
        if number is not None and number <= 0:
            raise B0ContractError(f"print.{key} must be greater than zero")


def _parse_reference_plane(doc: dict[str, Any], ctx: _Context) -> str:
    owner = "03_free_state_flatness"
    obj = _required_object(doc, "reference_plane", "", ctx, owner)
    if obj is None:
        return "missing"
    kind = _required_string(obj, "kind", "reference_plane", ctx, owner)
    if kind == "certified":
        _unknowns(ctx, obj, ("kind", "reference"), "reference_plane")
        _required_string(obj, "reference", "reference_plane", ctx, owner)
        return "certified"
    if kind == "verified":
        _unknowns(ctx, obj, ("kind", "verification_feeler_mm", "passed", "worst_location"), "reference_plane")
        feeler = _required_number(obj, "verification_feeler_mm", "reference_plane", ctx, owner)
        passed = _required_bool(obj, "passed", "reference_plane", ctx, owner)
        _required_string(obj, "worst_location", "reference_plane", ctx, owner)
        if feeler is not None and (feeler <= 0 or feeler > B0_PHYSICAL_ACCEPTANCE.reference_plane_feeler_max_mm):
            ctx.add(owner, "incomplete", "reference_plane_unqualified", "reference_plane.verification_feeler_mm", f"0 < x <= {B0_PHYSICAL_ACCEPTANCE.reference_plane_feeler_max_mm}", feeler)
        if passed is False:
            ctx.add(owner, "incomplete", "reference_plane_unqualified", "reference_plane.passed", True, False)
        return "verified"
    if kind is not None:
        ctx.add(owner, "incomplete", "reference_plane_unqualified", "reference_plane.kind", "certified or verified", kind)
    return "invalid"


def _parse_exact_number_map(obj: Any, keys: tuple[str, ...], path: str, ctx: _Context, owner: str) -> tuple[dict[str, Decimal], bool]:
    if not isinstance(obj, dict):
        raise B0ContractError(f"{path} must be an object")
    _unknowns(ctx, obj, keys, path)
    result: dict[str, Decimal] = {}
    complete = True
    for key in keys:
        if key not in obj:
            ctx.missing(owner, f"{path}.{key}")
            complete = False
        else:
            result[key] = _decimal(obj[key], f"{path}.{key}")
    return result, complete


def _parse_gaps(obj: Any, path: str, ctx: _Context, owner: str) -> tuple[dict[str, Decimal], bool]:
    gaps_obj = _object(obj, path)
    _unknowns(ctx, gaps_obj, SEAMS, path)
    result: dict[str, Decimal] = {}
    complete = True
    for seam in SEAMS:
        seam_path = f"{path}.{seam}"
        if seam not in gaps_obj:
            ctx.missing(owner, seam_path)
            complete = False
            continue
        values, row_complete = _parse_exact_number_map(gaps_obj[seam], GAP_POSITIONS, seam_path, ctx, owner)
        complete = complete and row_complete
        result.update({f"{seam}.{position}": value for position, value in values.items()})
    return result, complete


def _parse_rechecks(obj: dict[str, Any], checkpoint_path: str, ctx: _Context) -> dict[str, dict[str, Any]]:
    path = f"{checkpoint_path}.rechecks"
    if "rechecks" not in obj:
        ctx.missing("02_seam_gap_step", path)
        return {}
    rechecks = _object(obj["rechecks"], path)
    forbidden = set(rechecks) - {"od", "seam_gaps", "seam_steps", "flatness"}
    if forbidden:
        raise B0ContractError(f"{path} permits only od, seam_gaps, seam_steps, and flatness; got {sorted(forbidden)}")
    parsed: dict[str, dict[str, Any]] = {}
    if "od" in rechecks:
        if isinstance(rechecks["od"], dict) and "range_mm" in rechecks["od"]:
            raise B0ContractError(f"{path}.od.range_mm is forbidden; provide four diameters")
        values, complete = _parse_exact_number_map(rechecks["od"], DIAMETER_KEYS, f"{path}.od", ctx, "01_loop_od")
        parsed["od"] = {"values": values, "complete": complete}
    if "seam_gaps" in rechecks:
        values, complete = _parse_gaps(rechecks["seam_gaps"], f"{path}.seam_gaps", ctx, "02_seam_gap_step")
        parsed["seam_gaps"] = {"values": values, "complete": complete}
    if "seam_steps" in rechecks:
        values, complete = _parse_exact_number_map(rechecks["seam_steps"], STEP_KEYS, f"{path}.seam_steps", ctx, "02_seam_gap_step")
        parsed["seam_steps"] = {"values": values, "complete": complete}
    if "flatness" in rechecks:
        flat = _object(rechecks["flatness"], f"{path}.flatness")
        _unknowns(ctx, flat, ("rocking", "worst_flatness_gap_mm", "worst_flatness_location"), f"{path}.flatness")
        complete = True
        rocking = _required_bool(flat, "rocking", f"{path}.flatness", ctx, "03_free_state_flatness")
        gap = _required_number(flat, "worst_flatness_gap_mm", f"{path}.flatness", ctx, "03_free_state_flatness")
        location = _required_string(flat, "worst_flatness_location", f"{path}.flatness", ctx, "03_free_state_flatness")
        complete = rocking is not None and gap is not None and location is not None
        parsed["flatness"] = {"rocking": rocking, "gap": gap, "location": location, "complete": complete}
    return parsed


def _parse_checkpoint(name: str, value: Any, ctx: _Context) -> dict[str, Any]:
    owner = "01_loop_od" if name == "cycle1_free_state" else ("05_vertical_retention" if name == "after_vertical" else "06_lift_place")
    path = f"checkpoints.{name}"
    obj = _object(value, path)
    _unknowns(
        ctx,
        obj,
        ("s4_hand_pressure_only", "forced_actions", "seam_overlap", "visible_bow", "diameters_mm", "seam_gaps_mm", "seam_steps_mm", "rocking", "worst_flatness_gap_mm", "worst_flatness_location", "rechecks"),
        path,
    )
    s4_hand = _required_bool(obj, "s4_hand_pressure_only", path, ctx, "01_loop_od")
    forced_actions = _required_array(obj, "forced_actions", path, ctx, "01_loop_od")
    overlap = _required_bool(obj, "seam_overlap", path, ctx, "01_loop_od")
    bow = _required_bool(obj, "visible_bow", path, ctx, "01_loop_od")
    if forced_actions is not None and any(not isinstance(item, str) for item in forced_actions):
        raise B0ContractError(f"{path}.forced_actions must contain strings")
    for field, actual, expected in (
        ("s4_hand_pressure_only", s4_hand, True),
        ("seam_overlap", overlap, False),
        ("visible_bow", bow, False),
    ):
        if actual is not None and actual != expected:
            ctx.add("01_loop_od", "fail", "physical_observation_failed", f"{path}.{field}", expected, actual)
    if forced_actions:
        ctx.add("01_loop_od", "fail", "forced_action_observed", f"{path}.forced_actions", [], forced_actions)

    if "diameters_mm" in obj:
        diameters, diameters_complete = _parse_exact_number_map(obj["diameters_mm"], DIAMETER_KEYS, f"{path}.diameters_mm", ctx, "01_loop_od")
    else:
        ctx.missing("01_loop_od", f"{path}.diameters_mm")
        diameters, diameters_complete = {}, False
    if "seam_gaps_mm" in obj:
        gaps, gaps_complete = _parse_gaps(obj["seam_gaps_mm"], f"{path}.seam_gaps_mm", ctx, "02_seam_gap_step")
    else:
        ctx.missing("02_seam_gap_step", f"{path}.seam_gaps_mm")
        gaps, gaps_complete = {}, False
    if "seam_steps_mm" in obj:
        steps, steps_complete = _parse_exact_number_map(obj["seam_steps_mm"], STEP_KEYS, f"{path}.seam_steps_mm", ctx, "02_seam_gap_step")
    else:
        ctx.missing("02_seam_gap_step", f"{path}.seam_steps_mm")
        steps, steps_complete = {}, False
    rocking = _required_bool(obj, "rocking", path, ctx, "03_free_state_flatness")
    flatness = _required_number(obj, "worst_flatness_gap_mm", path, ctx, "03_free_state_flatness")
    location = _required_string(obj, "worst_flatness_location", path, ctx, "03_free_state_flatness")
    if rocking is True:
        ctx.add("03_free_state_flatness", "fail", "rocking_observed", f"{path}.rocking", False, True)
    rechecks = _parse_rechecks(obj, path, ctx)
    return {
        "name": name,
        "diameters": diameters,
        "diameters_complete": diameters_complete,
        "gaps": gaps,
        "gaps_complete": gaps_complete,
        "steps": steps,
        "steps_complete": steps_complete,
        "rocking": rocking,
        "flatness": flatness,
        "flatness_location": location,
        "rechecks": rechecks,
    }


def _evaluate_bounded_family(
    ctx: _Context,
    check: str,
    checkpoint: dict[str, Any],
    family: str,
    values: dict[str, Decimal],
    uncertainty: Decimal,
    minimum: Decimal | None,
    maximum: Decimal,
    base_path: str,
) -> tuple[dict[str, Decimal], bool]:
    states: list[str] = []
    for key, value in values.items():
        state = _inside_interval(value, uncertainty, minimum, maximum) if minimum is not None else _maximum_interval(value, uncertainty, maximum)
        states.append(state)
        if state == "fail":
            ctx.add(check, "fail", "measurement_outside_limit", f"{base_path}.{key}", {"minimum": minimum, "maximum": maximum}, value)
    needs_recheck = "borderline" in states
    recheck = checkpoint["rechecks"].get(family)
    if needs_recheck and recheck is None:
        ctx.add(check, "borderline", "complete_recheck_required", f"checkpoints.{checkpoint['name']}.rechecks.{family}", "complete second set", None)
        return values, True
    if recheck is None or not recheck["complete"]:
        return values, needs_recheck
    authoritative = recheck["values"]
    for key, value in authoritative.items():
        passed = (minimum is None or value >= minimum) and value <= maximum
        if not passed:
            ctx.add(check, "fail", "recheck_outside_limit", f"checkpoints.{checkpoint['name']}.rechecks.{family}.{key}", {"minimum": minimum, "maximum": maximum}, value)
    return authoritative, needs_recheck


def _recheck_trigger_set(
    checkpoints: dict[str, dict[str, Any]],
    systems: dict[str, dict[str, Any] | None],
) -> set[tuple[str, str]]:
    """Return checkpoint/family pairs with an actual v3 BORDERLINE trigger."""

    triggers: set[tuple[str, str]] = set()
    od_system = systems.get("od")
    gap_system = systems.get("gap")
    step_system = systems.get("step")
    flatness_system = systems.get("flatness")
    for name, checkpoint in checkpoints.items():
        if od_system and od_system["uncertainty_mm"] is not None and checkpoint["diameters_complete"]:
            uncertainty = od_system["uncertainty_mm"]
            values = checkpoint["diameters"]
            states = tuple(
                _inside_interval(
                    value,
                    uncertainty,
                    B0_PHYSICAL_ACCEPTANCE.od_min_mm,
                    B0_PHYSICAL_ACCEPTANCE.od_max_mm,
                )
                for value in values.values()
            )
            observed_range = max(values.values()) - min(values.values())
            range_state = _maximum_interval(
                observed_range,
                2 * uncertainty,
                B0_PHYSICAL_ACCEPTANCE.od_range_max_mm,
            )
            if "borderline" in states or range_state == "borderline":
                triggers.add((name, "od"))
        if gap_system and gap_system["uncertainty_mm"] is not None and checkpoint["gaps_complete"]:
            uncertainty = gap_system["uncertainty_mm"]
            if any(
                _inside_interval(
                    value,
                    uncertainty,
                    B0_PHYSICAL_ACCEPTANCE.seam_gap_min_mm,
                    B0_PHYSICAL_ACCEPTANCE.seam_gap_max_mm,
                )
                == "borderline"
                for value in checkpoint["gaps"].values()
            ):
                triggers.add((name, "seam_gaps"))
        if step_system and step_system["uncertainty_mm"] is not None and checkpoint["steps_complete"]:
            uncertainty = step_system["uncertainty_mm"]
            if any(
                _maximum_interval(
                    value,
                    uncertainty,
                    B0_PHYSICAL_ACCEPTANCE.seam_step_max_mm,
                )
                == "borderline"
                for value in checkpoint["steps"].values()
            ):
                triggers.add((name, "seam_steps"))
        if (
            flatness_system
            and flatness_system["uncertainty_mm"] is not None
            and checkpoint["flatness"] is not None
            and _maximum_interval(
                checkpoint["flatness"],
                flatness_system["uncertainty_mm"],
                B0_PHYSICAL_ACCEPTANCE.flatness_max_mm,
            )
            == "borderline"
        ):
            triggers.add((name, "flatness"))

    pairs = (
        ("cycle1_free_state", "after_vertical"),
        ("after_vertical", "after_lift_place"),
        ("cycle1_free_state", "after_lift_place"),
    )
    for family, key_name, system_name in (
        ("seam_gaps", "gaps", "gap"),
        ("seam_steps", "steps", "step"),
    ):
        system = systems.get(system_name)
        if not system or system["uncertainty_mm"] is None:
            continue
        combined_uncertainty = 2 * system["uncertainty_mm"]
        for before_name, after_name in pairs:
            before = checkpoints.get(before_name)
            after = checkpoints.get(after_name)
            if (
                before is None
                or after is None
                or not before[f"{key_name}_complete"]
                or not after[f"{key_name}_complete"]
            ):
                continue
            if any(
                (after[key_name][key] - before[key_name][key]) > 0
                and (after[key_name][key] - before[key_name][key])
                == combined_uncertainty
                for key in before[key_name]
            ):
                triggers.add((before_name, family))
                triggers.add((after_name, family))
    return triggers


def _validate_recheck_triggers(
    checkpoints: dict[str, dict[str, Any]],
    systems: dict[str, dict[str, Any] | None],
) -> None:
    triggers = _recheck_trigger_set(checkpoints, systems)
    for checkpoint_name, checkpoint in checkpoints.items():
        for family in checkpoint["rechecks"]:
            if (checkpoint_name, family) not in triggers:
                raise B0ContractError(
                    f"checkpoints.{checkpoint_name}.rechecks.{family} was supplied "
                    "without a corresponding BORDERLINE trigger"
                )


def _evaluate_od(ctx: _Context, checkpoint: dict[str, Any], uncertainty: Decimal) -> dict[str, Any]:
    values = checkpoint["diameters"]
    if not checkpoint["diameters_complete"]:
        return {}
    states = [
        _inside_interval(value, uncertainty, B0_PHYSICAL_ACCEPTANCE.od_min_mm, B0_PHYSICAL_ACCEPTANCE.od_max_mm)
        for value in values.values()
    ]
    observed_range = max(values.values()) - min(values.values())
    range_interval = (max(Decimal("0"), observed_range - 2 * uncertainty), observed_range + 2 * uncertainty)
    range_state = _maximum_interval(observed_range, 2 * uncertainty, B0_PHYSICAL_ACCEPTANCE.od_range_max_mm)
    for (key, value), state in zip(values.items(), states):
        if state == "fail":
            ctx.add("01_loop_od", "fail", "od_outside_limit", f"checkpoints.{checkpoint['name']}.diameters_mm.{key}", {"minimum": B0_PHYSICAL_ACCEPTANCE.od_min_mm, "maximum": B0_PHYSICAL_ACCEPTANCE.od_max_mm}, value)
    if range_state == "fail":
        ctx.add("01_loop_od", "fail", "od_range_outside_limit", f"checkpoints.{checkpoint['name']}.diameters_mm", f"range <= {B0_PHYSICAL_ACCEPTANCE.od_range_max_mm}", observed_range)
    needs_recheck = "borderline" in states or range_state == "borderline"
    authoritative = values
    if needs_recheck:
        recheck = checkpoint["rechecks"].get("od")
        if recheck is None:
            ctx.add("01_loop_od", "borderline", "complete_recheck_required", f"checkpoints.{checkpoint['name']}.rechecks.od", "four new diameters", None)
        elif recheck["complete"]:
            authoritative = recheck["values"]
            authoritative_range = max(authoritative.values()) - min(authoritative.values())
            for key, value in authoritative.items():
                if not B0_PHYSICAL_ACCEPTANCE.od_min_mm <= value <= B0_PHYSICAL_ACCEPTANCE.od_max_mm:
                    ctx.add("01_loop_od", "fail", "recheck_outside_limit", f"checkpoints.{checkpoint['name']}.rechecks.od.{key}", {"minimum": B0_PHYSICAL_ACCEPTANCE.od_min_mm, "maximum": B0_PHYSICAL_ACCEPTANCE.od_max_mm}, value)
            if authoritative_range > B0_PHYSICAL_ACCEPTANCE.od_range_max_mm:
                ctx.add("01_loop_od", "fail", "recheck_od_range_outside_limit", f"checkpoints.{checkpoint['name']}.rechecks.od", f"recomputed range <= {B0_PHYSICAL_ACCEPTANCE.od_range_max_mm}", authoritative_range)
    authoritative_range = max(authoritative.values()) - min(authoritative.values())
    return {
        "od_values_mm": tuple(authoritative[key] for key in DIAMETER_KEYS),
        "od_range_mm": authoritative_range,
        "od_range_interval_mm": range_interval if authoritative is values else (authoritative_range, authoritative_range),
    }


def _evaluate_checkpoints(ctx: _Context, checkpoints: dict[str, dict[str, Any]], systems: dict[str, dict[str, Any] | None]) -> dict[str, Any]:
    derived: dict[str, Any] = {}
    od_u = systems["od"]["uncertainty_mm"] if systems.get("od") and systems["od"]["uncertainty_mm"] is not None else None
    gap_u = systems["gap"]["uncertainty_mm"] if systems.get("gap") and systems["gap"]["uncertainty_mm"] is not None else None
    step_u = systems["step"]["uncertainty_mm"] if systems.get("step") and systems["step"]["uncertainty_mm"] is not None else None
    flat_u = systems["flatness"]["uncertainty_mm"] if systems.get("flatness") and systems["flatness"]["uncertainty_mm"] is not None else None
    for name in CHECKPOINT_NAMES:
        checkpoint = checkpoints.get(name)
        if checkpoint is None:
            continue
        row: dict[str, Any] = {}
        if od_u is not None:
            row.update(_evaluate_od(ctx, checkpoint, od_u))
        if gap_u is not None and checkpoint["gaps_complete"]:
            authoritative, _ = _evaluate_bounded_family(
                ctx, "02_seam_gap_step", checkpoint, "seam_gaps", checkpoint["gaps"], gap_u,
                B0_PHYSICAL_ACCEPTANCE.seam_gap_min_mm, B0_PHYSICAL_ACCEPTANCE.seam_gap_max_mm,
                f"checkpoints.{name}.seam_gaps_mm",
            )
            row["worst_gap_mm"] = max(authoritative.values())
        if step_u is not None and checkpoint["steps_complete"]:
            authoritative, _ = _evaluate_bounded_family(
                ctx, "02_seam_gap_step", checkpoint, "seam_steps", checkpoint["steps"], step_u,
                None, B0_PHYSICAL_ACCEPTANCE.seam_step_max_mm,
                f"checkpoints.{name}.seam_steps_mm",
            )
            row["worst_step_mm"] = max(authoritative.values())
        if flat_u is not None and checkpoint["flatness"] is not None:
            state = _maximum_interval(checkpoint["flatness"], flat_u, B0_PHYSICAL_ACCEPTANCE.flatness_max_mm)
            authoritative = checkpoint["flatness"]
            if state == "fail":
                ctx.add("03_free_state_flatness", "fail", "flatness_outside_limit", f"checkpoints.{name}.worst_flatness_gap_mm", f"<= {B0_PHYSICAL_ACCEPTANCE.flatness_max_mm}", authoritative)
            elif state == "borderline":
                recheck = checkpoint["rechecks"].get("flatness")
                if recheck is None:
                    ctx.add("03_free_state_flatness", "borderline", "complete_recheck_required", f"checkpoints.{name}.rechecks.flatness", "rocking, gap, and location", None)
                elif recheck["complete"]:
                    authoritative = recheck["gap"]
                    if recheck["rocking"] or authoritative > B0_PHYSICAL_ACCEPTANCE.flatness_max_mm:
                        ctx.add("03_free_state_flatness", "fail", "recheck_flatness_outside_limit", f"checkpoints.{name}.rechecks.flatness", {"rocking": False, "maximum": B0_PHYSICAL_ACCEPTANCE.flatness_max_mm}, {"rocking": recheck["rocking"], "gap": authoritative})
            row["worst_flatness_mm"] = authoritative
        derived[name] = row
    return derived


def _evaluate_growth_family(ctx: _Context, checkpoints: dict[str, dict[str, Any]], family: str, uncertainty: Decimal) -> dict[str, Any]:
    pairs = (
        ("cycle1_free_state", "after_vertical", "sequential"),
        ("after_vertical", "after_lift_place", "sequential"),
        ("cycle1_free_state", "after_lift_place", "cumulative"),
    )
    key_name = "gaps" if family == "seam_gaps" else "steps"
    field_name = "seam_gaps_mm" if family == "seam_gaps" else "seam_steps_mm"
    all_rows: list[tuple[Decimal, str, str]] = []
    for before_name, after_name, kind in pairs:
        before = checkpoints.get(before_name)
        after = checkpoints.get(after_name)
        if before is None or after is None or not before[f"{key_name}_complete"] or not after[f"{key_name}_complete"]:
            continue
        for key in before[key_name]:
            delta = after[key_name][key] - before[key_name][key]
            path = f"checkpoints.{after_name}.{field_name}.{key} - checkpoints.{before_name}.{field_name}.{key}"
            before_recheck = before["rechecks"].get(family)
            after_recheck = after["rechecks"].get(family)
            pair_has_complete_rechecks = bool(
                before_recheck
                and before_recheck["complete"]
                and after_recheck
                and after_recheck["complete"]
            )
            if delta > 2 * uncertainty:
                ctx.add("02_seam_gap_step", "fail", "measurable_post_handling_growth", path, f"delta <= {2 * uncertainty}", delta)
            elif delta > 0 and delta == 2 * uncertainty:
                if not before_recheck and not after_recheck:
                    ctx.add("02_seam_gap_step", "borderline", "growth_rechecks_required", path, "complete rechecks at both checkpoints", None)
                elif not pair_has_complete_rechecks:
                    ctx.add("02_seam_gap_step", "incomplete", "growth_recheck_pair_incomplete", path, "complete rechecks at both checkpoints", {"before": bool(before_recheck and before_recheck["complete"]), "after": bool(after_recheck and after_recheck["complete"])})
                else:
                    terminal_delta = after_recheck["values"][key] - before_recheck["values"][key]
                    if terminal_delta > 0:
                        ctx.add("02_seam_gap_step", "fail", "recheck_growth_positive", path, "recorded recheck delta <= 0", terminal_delta)
            elif pair_has_complete_rechecks:
                terminal_delta = after_recheck["values"][key] - before_recheck["values"][key]
                if terminal_delta > 0:
                    ctx.add("02_seam_gap_step", "fail", "recheck_growth_positive", path, "recorded recheck delta <= 0", terminal_delta)
            authoritative_before = (
                before_recheck["values"] if pair_has_complete_rechecks else before[key_name]
            )
            authoritative_after = (
                after_recheck["values"] if pair_has_complete_rechecks else after[key_name]
            )
            authoritative_delta = authoritative_after[key] - authoritative_before[key]
            all_rows.append((authoritative_delta, path, kind))
    if not all_rows:
        return {}
    worst = max(all_rows, key=lambda row: row[0])
    sequential_rows = tuple(row for row in all_rows if row[2] == "sequential")
    cumulative_rows = tuple(row for row in all_rows if row[2] == "cumulative")
    sequential = max(sequential_rows, key=lambda row: row[0]) if sequential_rows else None
    cumulative = max(cumulative_rows, key=lambda row: row[0]) if cumulative_rows else None
    prefix = "gap" if family == "seam_gaps" else "step"
    return {
        f"worst_{prefix}_delta_mm": worst[0],
        f"worst_{prefix}_path": worst[1],
        f"worst_sequential_{prefix}_delta_mm": sequential[0] if sequential else None,
        f"worst_sequential_{prefix}_path": sequential[1] if sequential else None,
        f"worst_cumulative_{prefix}_delta_mm": cumulative[0] if cumulative else None,
        f"worst_cumulative_{prefix}_path": cumulative[1] if cumulative else None,
    }


def _parse_hardware(doc: dict[str, Any], ctx: _Context, systems: dict[str, dict[str, Any] | None]) -> None:
    owner = "04_service_cycles"
    hardware = _required_object(doc, "hardware_fit", "", ctx, owner)
    if hardware is None:
        return
    _unknowns(ctx, hardware, ("pins", "nuts", "screws"), "hardware_fit")
    collections = {}
    for name in ("pins", "nuts", "screws"):
        rows = _required_array(hardware, name, "hardware_fit", ctx, owner)
        collections[name] = rows
    pin_system = systems.get("pin_exposure")
    pin_resolution = pin_system["resolution_mm"] if pin_system and pin_system["resolution_mm"] is not None else Decimal("0")
    specs = {
        "pins": (
            PIN_IDS,
            ("id", "before_mm", "after_mm", "steady_nonimpact_pressure", "free_dropped", "impact_used", "released", "visible_movement", "damage"),
        ),
        "nuts": (FASTENER_IDS, ("id", "flat", "below_seat", "spun", "forced")),
        "screws": (FASTENER_IDS, ("id", "hard_before_head_contact", "bridge_moved_when_tight", "paper_remained_at_contact", "cross_threaded")),
    }
    for collection_name, rows in collections.items():
        if rows is None:
            continue
        expected_ids, allowed = specs[collection_name]
        ids: list[str] = []
        parsed_rows: list[tuple[str, dict[str, Any], str]] = []
        for index, raw in enumerate(rows):
            row_path = f"hardware_fit.{collection_name}[{index}]"
            row = _object(raw, row_path)
            _unknowns(ctx, row, allowed, row_path)
            identifier = _required_string(row, "id", row_path, ctx, owner)
            if identifier is not None:
                ids.append(identifier)
                parsed_rows.append((identifier, row, row_path))
        if len(ids) != len(set(ids)):
            raise B0ContractError(f"hardware_fit.{collection_name} contains duplicate IDs")
        if tuple(sorted(ids)) != tuple(sorted(expected_ids)):
            ctx.add(owner, "incomplete", "hardware_id_set_incomplete", f"hardware_fit.{collection_name}", list(expected_ids), ids)
        for identifier, row, row_path in parsed_rows:
            if collection_name == "pins":
                before = _required_number(row, "before_mm", row_path, ctx, owner)
                after = _required_number(row, "after_mm", row_path, ctx, owner)
                if before is not None and before != B0_PHYSICAL_ACCEPTANCE.pin_target_exposure_mm:
                    ctx.add(owner, "fail", "pin_target_failed", f"{row_path}.before_mm", B0_PHYSICAL_ACCEPTANCE.pin_target_exposure_mm, before)
                if before is not None and after is not None and pin_resolution > 0:
                    rounded_before = (before / pin_resolution).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
                    rounded_after = (after / pin_resolution).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
                    if rounded_after - rounded_before != B0_PHYSICAL_ACCEPTANCE.pin_motion_max_mm:
                        ctx.add(owner, "fail", "pin_motion_failed", f"{row_path}.after_mm", "zero change at pin-tool resolution", after - before)
                expectations = {
                    "steady_nonimpact_pressure": True,
                    "free_dropped": False,
                    "impact_used": False,
                    "released": False,
                    "visible_movement": False,
                    "damage": False,
                }
            elif collection_name == "nuts":
                expectations = {"flat": True, "below_seat": True, "spun": False, "forced": False}
            else:
                expectations = {
                    "hard_before_head_contact": False,
                    "bridge_moved_when_tight": False,
                    "paper_remained_at_contact": False,
                    "cross_threaded": False,
                }
            for key, expected in expectations.items():
                actual = _required_bool(row, key, row_path, ctx, owner)
                if actual is not None and actual != expected:
                    ctx.add(owner, "fail", "hardware_fit_failed", f"{row_path}.{key}", expected, actual)


def _parse_assembly(doc: dict[str, Any], ctx: _Context) -> None:
    owner = "01_loop_od"
    obj = _required_object(doc, "assembly_attestations", "", ctx, owner)
    if obj is None:
        return
    expected = {
        "all_quadrants_supported_in_final_xy": True,
        "bridge_insertion_order": ["S1", "S2", "S3", "S4"],
        "s4_inserted_upward_from_below": True,
        "q4_with_s4_lowering_used": False,
        "all_eight_screws_loose_before_tightening": True,
        "tightening_order": ["S1", "S3", "S2", "S4"],
        "finger_snug_only": True,
        "forced_closure_used": False,
        "unconstrained_wait_minutes": B0_PHYSICAL_ACCEPTANCE.unconstrained_wait_min,
        "direct_force_or_damage_observed": False,
    }
    _unknowns(ctx, obj, expected, "assembly_attestations")
    for key, expected_value in expected.items():
        path = f"assembly_attestations.{key}"
        if key not in obj:
            target_owner = "03_free_state_flatness" if key == "unconstrained_wait_minutes" else owner
            ctx.missing(target_owner, path)
            continue
        actual = obj[key]
        if key in ("bridge_insertion_order", "tightening_order"):
            actual = _array(actual, path)
            if any(not isinstance(item, str) for item in actual):
                raise B0ContractError(f"{path} must contain strings")
        elif key == "unconstrained_wait_minutes":
            actual = _decimal(actual, path)
        else:
            if not isinstance(actual, bool):
                raise B0ContractError(f"{path} must be a boolean")
        if key == "unconstrained_wait_minutes":
            if actual < expected_value:
                ctx.add("03_free_state_flatness", "incomplete", "procedure_duration_short", path, f">= {expected_value}", actual)
        elif key in ("forced_closure_used", "direct_force_or_damage_observed") and actual is True:
            ctx.add(owner, "fail", "forced_closure_or_damage", path, expected_value, actual)
        elif actual != expected_value:
            ctx.add(owner, "incomplete", "method_attestation_mismatch", path, expected_value, actual)


def _parse_cycles(doc: dict[str, Any], ctx: _Context) -> tuple[str, ...]:
    owner = "04_service_cycles"
    rows = _required_array(doc, "cycles", "", ctx, owner)
    if rows is None:
        return ()
    parsed: dict[int, str] = {}
    force_order = {"free": 0, "light": 1, "firm": 2, "forced": 3}
    seen: list[int] = []
    for index, raw in enumerate(rows):
        path = f"cycles[{index}]"
        row = _object(raw, path)
        _unknowns(ctx, row, ("cycle", "initial_assembly", "s4_force", "damage"), path)
        if "cycle" not in row:
            ctx.missing(owner, f"{path}.cycle")
            continue
        cycle_value = row["cycle"]
        if isinstance(cycle_value, bool) or not isinstance(cycle_value, int):
            raise B0ContractError(f"{path}.cycle must be an integer")
        seen.append(cycle_value)
        initial = _required_bool(row, "initial_assembly", path, ctx, owner)
        force = _required_string(row, "s4_force", path, ctx, owner)
        damage = _required_array(row, "damage", path, ctx, owner)
        if damage is not None and any(not isinstance(item, str) for item in damage):
            raise B0ContractError(f"{path}.damage must contain strings")
        if force is not None and force not in force_order:
            raise B0ContractError(f"{path}.s4_force must be free, light, firm, or forced")
        if initial is not None and initial != (cycle_value == 1):
            ctx.add(owner, "incomplete", "cycle_method_mismatch", f"{path}.initial_assembly", cycle_value == 1, initial)
        if force == "forced":
            ctx.add(owner, "fail", "forced_cycle", f"{path}.s4_force", "free, light, or firm", force)
        if damage:
            ctx.add(owner, "fail", "cycle_damage", f"{path}.damage", [], damage)
        if force is not None:
            parsed[cycle_value] = force
    if len(seen) != len(set(seen)):
        raise B0ContractError("cycles contains duplicate cycle IDs")
    if tuple(sorted(seen)) != tuple(range(1, B0_PHYSICAL_ACCEPTANCE.assembly_cycle_count + 1)):
        ctx.add(owner, "incomplete", "cycle_set_incomplete", "cycles", [1, 2, 3], seen)
    for previous, current in ((1, 2), (2, 3)):
        if previous in parsed and current in parsed and force_order[parsed[current]] > force_order[parsed[previous]]:
            ctx.add(owner, "fail", "cycle_force_escalation", f"cycles[{current}].s4_force", f"<= cycle {previous} ({parsed[previous]})", parsed[current])
    return tuple(parsed.get(index, "missing") for index in range(1, 4))


def _parse_vertical(doc: dict[str, Any], ctx: _Context) -> Decimal | None:
    owner = "05_vertical_retention"
    obj = _required_object(doc, "vertical", "", ctx, owner)
    if obj is None:
        return None
    allowed = ("down_quadrant", "started_at", "ended_at", "only_down_quadrant_rim_contact", "safety_tether_load_bearing", "movement_or_disengagement")
    _unknowns(ctx, obj, allowed, "vertical")
    down = _required_string(obj, "down_quadrant", "vertical", ctx, owner)
    if down is not None and down != B0_PHYSICAL_ACCEPTANCE.vertical_down_quadrant:
        ctx.add(owner, "incomplete", "vertical_method_mismatch", "vertical.down_quadrant", B0_PHYSICAL_ACCEPTANCE.vertical_down_quadrant, down)
    times: dict[str, datetime] = {}
    for key in ("started_at", "ended_at"):
        value = _required_string(obj, key, "vertical", ctx, owner)
        if value is not None:
            try:
                parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError as exc:
                raise B0ContractError(f"vertical.{key} must be an ISO timestamp") from exc
            if parsed.tzinfo is None or parsed.utcoffset() is None:
                raise B0ContractError(f"vertical.{key} must be timezone-aware")
            times[key] = parsed
    duration = None
    if len(times) == 2:
        seconds = Decimal(str((times["ended_at"] - times["started_at"]).total_seconds()))
        if seconds < 0:
            raise B0ContractError("vertical.ended_at must not precede vertical.started_at")
        duration = seconds / Decimal("60")
        if duration < B0_PHYSICAL_ACCEPTANCE.vertical_dwell_min:
            ctx.add(owner, "incomplete", "procedure_duration_short", "vertical", f">= {B0_PHYSICAL_ACCEPTANCE.vertical_dwell_min} minutes", duration)
    expected = {
        "only_down_quadrant_rim_contact": True,
        "safety_tether_load_bearing": False,
        "movement_or_disengagement": False,
    }
    for key, target in expected.items():
        value = _required_bool(obj, key, "vertical", ctx, owner)
        if value is not None and value != target:
            severity = "fail" if key == "movement_or_disengagement" and value else "incomplete"
            ctx.add(owner, severity, "vertical_observation_failed" if severity == "fail" else "vertical_method_mismatch", f"vertical.{key}", target, value)
    return duration


def _parse_lift(doc: dict[str, Any], ctx: _Context) -> None:
    owner = "06_lift_place"
    obj = _required_object(doc, "lift_place", "", ctx, owner)
    if obj is None:
        return
    allowed = ("sequence", "height_mm", "hold_seconds", "seam_click_or_disengagement", "hardware_moved")
    _unknowns(ctx, obj, allowed, "lift_place")
    sequence = _required_array(obj, "sequence", "lift_place", ctx, owner)
    if sequence is not None:
        if any(not isinstance(item, str) for item in sequence):
            raise B0ContractError("lift_place.sequence must contain strings")
        if tuple(sequence) != B0_PHYSICAL_ACCEPTANCE.lift_sequence:
            ctx.add(owner, "incomplete", "lift_procedure_incomplete", "lift_place.sequence", B0_PHYSICAL_ACCEPTANCE.lift_sequence, sequence)
    for key, limit in (("height_mm", B0_PHYSICAL_ACCEPTANCE.lift_height_min_mm), ("hold_seconds", B0_PHYSICAL_ACCEPTANCE.lift_hold_min_seconds)):
        value = _required_number(obj, key, "lift_place", ctx, owner)
        if value is not None and value < limit:
            ctx.add(owner, "incomplete", "lift_procedure_incomplete", f"lift_place.{key}", f">= {limit}", value)
    for key in ("seam_click_or_disengagement", "hardware_moved"):
        value = _required_bool(obj, key, "lift_place", ctx, owner)
        if value is True:
            ctx.add(owner, "fail", "lift_movement_observed", f"lift_place.{key}", False, True)


def _parse_photos(doc: dict[str, Any], ctx: _Context) -> None:
    value = doc.get("photos")
    if value is None:
        for key in PHOTO_KEYS:
            ctx.missing(PHOTO_OWNERS[key], f"photos.{key}")
        return
    photos = _object(value, "photos")
    _unknowns(ctx, photos, PHOTO_KEYS, "photos")
    for key in PHOTO_KEYS:
        owner = PHOTO_OWNERS[key]
        path = f"photos.{key}"
        if key not in photos:
            ctx.missing(owner, path)
            continue
        evidence = photos[key]
        if not isinstance(evidence, dict):
            ctx.add(owner, "incomplete", "photo_evidence_invalid", path, "exactly one photo object", evidence)
            continue
        _unknowns(ctx, evidence, ("kind", "value"), path)
        if set(evidence) != {"kind", "value"}:
            ctx.add(owner, "incomplete", "photo_evidence_invalid", path, "exactly kind and value", sorted(evidence))
            continue
        kind, photo_value = evidence["kind"], evidence["value"]
        if not isinstance(kind, str) or not isinstance(photo_value, str):
            raise B0ContractError(f"{path}.kind and {path}.value must be strings")
        if kind == "local_path":
            candidate = Path(photo_value)
            resolved = candidate if candidate.is_absolute() else ctx.input_path.parent / candidate
            if candidate.is_absolute() or not resolved.is_file():
                ctx.add(owner, "incomplete", "photo_local_path_invalid", path, "existing regular file relative to input", photo_value)
        elif kind == "stable_id":
            if not STABLE_ID_RE.fullmatch(photo_value):
                ctx.add(owner, "incomplete", "photo_stable_id_invalid", path, STABLE_ID_RE.pattern, photo_value)
        else:
            ctx.add(owner, "incomplete", "photo_kind_invalid", f"{path}.kind", "local_path or stable_id", kind)


def _parse_checkpoints(doc: dict[str, Any], ctx: _Context) -> dict[str, dict[str, Any]]:
    value = doc.get("checkpoints")
    owners = {"cycle1_free_state": "01_loop_od", "after_vertical": "05_vertical_retention", "after_lift_place": "06_lift_place"}
    if value is None:
        for name, owner in owners.items():
            ctx.missing(owner, f"checkpoints.{name}")
        return {}
    obj = _object(value, "checkpoints")
    _unknowns(ctx, obj, CHECKPOINT_NAMES, "checkpoints")
    parsed = {}
    for name in CHECKPOINT_NAMES:
        if name not in obj:
            ctx.missing(owners[name], f"checkpoints.{name}")
        else:
            parsed[name] = _parse_checkpoint(name, obj[name], ctx)
    return parsed


def evaluate_document(document: Any, input_path: Path) -> dict[str, Any]:
    """Validate and evaluate one already-decoded v3 result document."""

    doc = _object(document, "document")
    identity = {
        "schema": INPUT_SCHEMA,
        "article": NAMESPACE,
        "card_version": B0_PHYSICAL_ACCEPTANCE.card_version,
        "card_sha256": B0_PHYSICAL_ACCEPTANCE.card_sha256,
    }
    for key, expected in identity.items():
        if key not in doc or not isinstance(doc[key], str) or doc[key] != expected:
            raise B0ContractError(f"{key} must equal {expected!r}")
    ctx = _Context(input_path.resolve())
    _unknowns(
        ctx,
        doc,
        ("schema", "article", "card_version", "card_sha256", "print", "measurement_systems", "reference_plane", "hardware_fit", "assembly_attestations", "cycles", "checkpoints", "vertical", "lift_place", "photos"),
        "",
    )
    _parse_print(doc, ctx)
    systems = _parse_systems(doc, ctx)
    plane_kind = _parse_reference_plane(doc, ctx)
    _parse_hardware(doc, ctx, systems)
    _parse_assembly(doc, ctx)
    cycle_forces = _parse_cycles(doc, ctx)
    checkpoints = _parse_checkpoints(doc, ctx)
    duration = _parse_vertical(doc, ctx)
    _parse_lift(doc, ctx)
    _parse_photos(doc, ctx)
    _validate_recheck_triggers(checkpoints, systems)
    derived = _evaluate_checkpoints(ctx, checkpoints, systems)
    growth: dict[str, Any] = {}
    gap_system = systems.get("gap")
    if gap_system and gap_system["uncertainty_mm"] is not None:
        growth.update(_evaluate_growth_family(ctx, checkpoints, "seam_gaps", gap_system["uncertainty_mm"]))
    step_system = systems.get("step")
    if step_system and step_system["uncertainty_mm"] is not None:
        growth.update(_evaluate_growth_family(ctx, checkpoints, "seam_steps", step_system["uncertainty_mm"]))
    derived["post_handling_growth"] = growth

    checks = []
    summary = {status: 0 for status in ("pass", "borderline", "fail", "incomplete")}
    for check_id in CHECK_IDS:
        check_status = _status(ctx.reasons[check_id])
        summary[check_status] += 1
        checks.append({
            "id": check_id,
            "status": check_status,
            "reasons": [reason.public() for reason in ctx.reasons[check_id]],
        })
    overall = max((check["status"] for check in checks), key=STATUS_RANK.__getitem__)
    exit_code = {"pass": 0, "fail": 1, "borderline": 3, "incomplete": 4}[overall]
    measurement_payload = {
        name: _public(system) if system is not None else None
        for name, system in systems.items()
    }
    payload = {
        "schema": OUTPUT_SCHEMA,
        "article": NAMESPACE,
        "card_version": B0_PHYSICAL_ACCEPTANCE.card_version,
        "card_sha256": B0_PHYSICAL_ACCEPTANCE.card_sha256,
        "input": str(input_path.resolve()),
        "overall_status": overall,
        "exit_code": exit_code,
        "summary": summary,
        "measurement_systems": measurement_payload,
        "derived": _public(derived),
        "checks": checks,
        "missing_fields": sorted(ctx.missing_fields),
        "warnings": sorted(ctx.warnings, key=lambda warning: warning["path"]),
    }
    payload["_text_context"] = {
        "plane_kind": plane_kind,
        "cycle_forces": cycle_forces,
        "vertical_duration_minutes": duration,
    }
    return payload


def load_and_evaluate(path: str | Path) -> dict[str, Any]:
    """Read one UTF-8 JSON document and return the six-check evaluation."""

    input_path = Path(path).expanduser()
    try:
        text = input_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise B0ContractError(f"cannot read {input_path}: {exc}") from exc

    def reject_constant(value: str) -> None:
        raise B0ContractError(f"non-finite JSON number {value} is forbidden")

    try:
        document = json.loads(text, parse_float=Decimal, parse_constant=reject_constant)
    except B0ContractError:
        raise
    except json.JSONDecodeError as exc:
        raise B0ContractError(f"malformed JSON at line {exc.lineno} column {exc.colno}: {exc.msg}") from exc
    return evaluate_document(document, input_path)


def json_report(payload: dict[str, Any]) -> str:
    public = {key: value for key, value in payload.items() if key != "_text_context"}
    return json.dumps(public, indent=2, ensure_ascii=False) + "\n"


def _fmt(value: Any) -> str:
    if value is None:
        return "missing"
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, float):
        return format(value, ".3f")
    return str(value)


def text_report(payload: dict[str, Any]) -> str:
    status = payload["overall_status"].upper()
    derived = payload["derived"]
    cycle = derived.get("cycle1_free_state", {})
    growth = derived.get("post_handling_growth", {})
    context = payload["_text_context"]
    forces = "/".join(context["cycle_forces"]) if context["cycle_forces"] else "missing"
    details = {
        "01_loop_od": f"D={cycle.get('od_values_mm', 'missing')}; range={_fmt(cycle.get('od_range_mm'))}; uncertainty={payload['measurement_systems'].get('od', {}).get('uncertainty_mm') if payload['measurement_systems'].get('od') else 'missing'}",
        "02_seam_gap_step": f"gaps={_fmt(cycle.get('worst_gap_mm'))}; step={_fmt(cycle.get('worst_step_mm'))}; growth={_fmt(growth.get('worst_gap_delta_mm'))}/{_fmt(growth.get('worst_step_delta_mm'))}",
        "03_free_state_flatness": f"worst={_fmt(cycle.get('worst_flatness_mm'))}; plane={context['plane_kind']}",
        "04_service_cycles": f"pins={SPEC.dowel_count_total}; S4={forces}",
        "05_vertical_retention": f"{B0_PHYSICAL_ACCEPTANCE.vertical_down_quadrant} down; {_fmt(context['vertical_duration_minutes'])} min; post-checks {next(check['status'] for check in payload['checks'] if check['id'] == '05_vertical_retention')}",
        "06_lift_place": f"sequence/count {next(check['status'] for check in payload['checks'] if check['id'] == '06_lift_place')}; post-checks {next(check['status'] for check in payload['checks'] if check['id'] == '06_lift_place')}",
    }
    lines = [f"KAGE B0 Q4-R1: {status}"]
    for check in payload["checks"]:
        lines.append(f"{CHECK_LABELS[check['id']]:<28} {check['status'].upper():<10} {details[check['id']]}")
        if check["status"] != "pass":
            for reason in check["reasons"]:
                lines.append(
                    f"  - {reason['code']} {reason['path']}: expected {reason['expected']}; actual {reason['actual']}"
                )
    lines.append(f"Overall: {status} — evaluator result; independent acceptance still required.")
    return "\n".join(lines) + "\n"
