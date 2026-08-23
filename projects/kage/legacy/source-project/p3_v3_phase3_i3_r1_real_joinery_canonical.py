"""I3.12 v3 semantic projection for the real six-plate Orca archive."""

from __future__ import annotations

from hashlib import sha256
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import subprocess
from tempfile import TemporaryDirectory
from urllib.parse import unquote_to_bytes
import xml.etree.ElementTree as ET
from zipfile import ZipFile

from p3_v3_phase3_i3_r1_real_joinery_print_project import (
    MODEL_ROOT,
    ORCA_SOURCE_PROJECT,
    _write_orca_source_project,
)
from p3_v3_phase3_i3_r1_real_joinery_spec import ARTIFACT_CONTRACT, NAMESPACE


ROOT = Path(__file__).resolve().parent
NODE = Path("/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node")
JCS_IMPLEMENTATION = ROOT / "vendor" / "i3_rfc8785" / "canonicalize.js"
PROJECTION_PATH = MODEL_ROOT / "i3_12_parity_projection.jcs.json"

JSON_MEMBERS = (
    "Metadata/project_settings.config",
    "Metadata/model_settings.json",
    "Metadata/plate_data.json",
)
XML_MEMBERS = (
    "[Content_Types].xml",
    "_rels/.rels",
    "3D/3dmodel.model",
    "Metadata/model_settings.config",
)
REQUIRED_MEMBERS = set(JSON_MEMBERS + XML_MEMBERS)


def _jcs(value: object) -> bytes:
    source = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    script = (
        "const c=require(process.argv[1]);"
        "let b='';process.stdin.on('data',d=>b+=d);"
        "process.stdin.on('end',()=>process.stdout.write(c(JSON.parse(b))));"
    )
    completed = subprocess.run(
        [str(NODE), "-e", script, str(JCS_IMPLEMENTATION)],
        input=source,
        check=True,
        capture_output=True,
    )
    return completed.stdout


def _c14n11(data: bytes) -> bytes:
    if b"<!DOCTYPE" in data.upper() or b"<!--" in data:
        raise ValueError("I3.12 XML DTD/comments are not permitted")
    with TemporaryDirectory(prefix="kage-i3-c14n11-") as temporary:
        source = Path(temporary) / "source.xml"
        source.write_bytes(data)
        completed = subprocess.run(
            ["/usr/bin/xmllint", "--nonet", "--c14n11", str(source)],
            check=True,
            capture_output=True,
        )
    return completed.stdout


def _normalized_reference(target: str) -> str:
    if any(ord(ch) > 127 or ord(ch) < 32 for ch in target):
        raise ValueError("non-ASCII/control relationship target")
    if "\\" in target or "?" in target or "#" in target or "://" in target:
        raise ValueError("ambiguous relationship target")
    output = bytearray()
    i = 0
    unreserved = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
    while i < len(target):
        if target[i] != "%":
            output.extend(target[i].encode("ascii"))
            i += 1
            continue
        if i + 2 >= len(target):
            raise ValueError("invalid percent triplet")
        value = int(target[i + 1 : i + 3], 16)
        if value in (0, 47, 92):
            raise ValueError("encoded separator/NUL")
        output.extend(bytes((value,)) if value in unreserved else f"%{value:02X}".encode())
        i += 3
    normalized = output.decode("ascii")
    if any(segment in ("%2E", "%2e") for segment in normalized.split("/")):
        raise ValueError("encoded dot segment")
    return normalized


def _relationships(source_part: str, data: bytes, member_names: set[str]) -> list[dict[str, str]]:
    root = ET.fromstring(data)
    rows = []
    for relationship in list(root):
        raw = relationship.attrib["Target"]
        normalized = _normalized_reference(raw)
        if normalized.startswith("/"):
            resolved = posixpath.normpath(normalized)
        else:
            base = "/" if source_part == "/" else str(PurePosixPath(source_part).parent)
            resolved = posixpath.normpath(posixpath.join(base, normalized))
        if not resolved.startswith("/"):
            resolved = "/" + resolved
        if resolved.lstrip("/") not in member_names:
            raise ValueError(f"unresolved relationship target {resolved}")
        rows.append({
            "source_part": source_part,
            "id": relationship.attrib["Id"],
            "type": relationship.attrib["Type"],
            "target_mode": relationship.attrib.get("TargetMode", "Internal").lower(),
            "normalized_target_reference": normalized,
            "resolved_part_name": resolved,
        })
    return sorted(rows, key=lambda row: tuple(row[key] for key in (
        "source_part", "id", "type", "target_mode",
        "normalized_target_reference", "resolved_part_name",
    )))


def _content_types(data: bytes, member_names: set[str]) -> dict[str, object]:
    root = ET.fromstring(data)
    defaults = sorted(
        ({"extension": node.attrib["Extension"], "content_type": node.attrib["ContentType"]}
         for node in root if node.tag.endswith("Default")),
        key=lambda row: (row["extension"], row["content_type"]),
    )
    overrides = sorted(
        ({"part_name": node.attrib["PartName"], "content_type": node.attrib["ContentType"]}
         for node in root if node.tag.endswith("Override")),
        key=lambda row: (row["part_name"], row["content_type"]),
    )
    default_map = {row["extension"]: row["content_type"] for row in defaults}
    override_map = {row["part_name"].lstrip("/"): row["content_type"] for row in overrides}
    resolved = []
    for name in sorted(member_names):
        if name == "[Content_Types].xml":
            # OPC's content-type declaration part classifies payload parts;
            # it is not itself selected through its own declarations.
            continue
        content_type = override_map.get(name)
        if content_type is None:
            content_type = default_map.get(name.rsplit(".", 1)[-1])
        if content_type is None:
            raise ValueError(f"unresolved content type {name}")
        resolved.append({"part_name": "/" + name, "content_type": content_type})
    return {"defaults": defaults, "overrides": overrides, "resolved": resolved}


def _projection_from_archive(path: Path) -> tuple[dict[str, object], dict[str, object]]:
    with ZipFile(path) as archive:
        if archive.testzip() is not None:
            raise ValueError("CRC failure")
        names = archive.namelist()
        if len(names) != len(set(names)) or set(names) != REQUIRED_MEMBERS:
            raise ValueError(f"I3.12 member grammar mismatch: {sorted(names)}")
        members = {name: archive.read(name) for name in names}

    json_projection = {}
    jcs_verified = True
    parsed_json = {}
    for name in JSON_MEMBERS:
        value = json.loads(members[name])
        canonical = _jcs(value)
        parsed_json[name] = value
        json_projection[name] = {
            "uncompressed_size": len(members[name]),
            "raw_sha256": sha256(members[name]).hexdigest(),
            "jcs_sha256": sha256(canonical).hexdigest(),
        }
        jcs_verified &= _jcs(json.loads(canonical)) == canonical

    xml_projection = {}
    c14n_verified = True
    for name in XML_MEMBERS:
        canonical = _c14n11(members[name])
        xml_projection[name] = {
            "uncompressed_size": len(members[name]),
            "raw_sha256": sha256(members[name]).hexdigest(),
            "c14n11_sha256": sha256(canonical).hexdigest(),
        }
        c14n_verified &= _c14n11(canonical) == canonical

    relationships = _relationships("/", members["_rels/.rels"], set(names))
    content_types = _content_types(members["[Content_Types].xml"], set(names))
    model_root = ET.fromstring(members["3D/3dmodel.model"])
    ns = {
        "m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02",
        "p": "http://schemas.microsoft.com/3dmanufacturing/production/2015/06",
    }
    resources = {
        int(node.attrib["id"]): {
            "resource_id": int(node.attrib["id"]),
            "object_name": node.attrib["name"],
            "object_uuid": node.attrib.get(f"{{{ns['p']}}}UUID", ""),
        }
        for node in model_root.findall("m:resources/m:object", ns)
    }
    build_ids = [int(node.attrib["objectid"]) for node in model_root.findall("m:build/m:item", ns)]
    objects = parsed_json["Metadata/model_settings.json"]["objects"]
    plates = parsed_json["Metadata/plate_data.json"]["plates"]
    if [resources[i]["object_name"] for i in build_ids] != [row["object_name"] for row in objects]:
        raise ValueError("model build/object metadata mismatch")
    if [resources[i]["object_uuid"] for i in build_ids] != [row["object_uuid"] for row in objects]:
        raise ValueError("model UUID/object metadata mismatch")

    projection = {
        "schema": ARTIFACT_CONTRACT.projection_schema,
        "members": {"json": json_projection, "xml": xml_projection, "png": {}, "binary_exact": {}},
        "project": {
            "unit": model_root.attrib["unit"],
            "plates": plates,
            "objects": objects,
            "materials": parsed_json["Metadata/model_settings.json"]["materials"],
            "relationships": relationships,
            "content_types": content_types,
        },
    }
    details = {
        "relationships_stage_correct": all(set(row) == {
            "source_part", "id", "type", "target_mode",
            "normalized_target_reference", "resolved_part_name",
        } for row in relationships),
        "rfc8785_jcs_verified": bool(jcs_verified),
        "c14n11_verified": bool(c14n_verified),
        "jcs_implementation_sha256": sha256(JCS_IMPLEMENTATION.read_bytes()).hexdigest(),
        "xmllint_sha256": sha256(Path("/usr/bin/xmllint").read_bytes()).hexdigest(),
    }
    return projection, details


def projection_evidence(write: bool = False) -> dict[str, object]:
    MODEL_ROOT.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=f".{NAMESPACE}-projection-", dir=MODEL_ROOT.parent) as temporary:
        archive = Path(temporary) / ORCA_SOURCE_PROJECT.name
        _write_orca_source_project(archive)
        first, details = _projection_from_archive(archive)
        second, _ = _projection_from_archive(archive)
        with ZipFile(archive) as package:
            content_types_bytes = package.read("[Content_Types].xml")
            ordinary_members = set(package.namelist()) | {"Metadata/undeclared.payload"}
        undeclared_member_rejected = False
        try:
            _content_types(content_types_bytes, ordinary_members)
        except ValueError as exc:
            undeclared_member_rejected = "unresolved content type" in str(exc)
        if not undeclared_member_rejected:
            raise RuntimeError("ordinary undeclared member negative fixture was accepted")
        first_bytes = _jcs(first)
        second_bytes = _jcs(second)
        if first_bytes != second_bytes:
            raise RuntimeError("I3.12 semantic projection is nondeterministic")
        if write:
            MODEL_ROOT.mkdir(parents=True, exist_ok=True)
            staged = MODEL_ROOT / f".{PROJECTION_PATH.name}.new"
            staged.write_bytes(first_bytes)
            os.replace(staged, PROJECTION_PATH)
    return {
        "schema": first["schema"],
        **details,
        "projection_sha256": sha256(first_bytes).hexdigest(),
        "projection_bytes": len(first_bytes),
        "semantic_repeat_run_equal": first_bytes == second_bytes,
        "relationship_count": len(first["project"]["relationships"]),
        "content_type_resolution_count": len(first["project"]["content_types"]["resolved"]),
        "undeclared_ordinary_member_rejected": undeclared_member_rejected,
        "plate_count": len(first["project"]["plates"]),
        "object_count": len(first["project"]["objects"]),
        "path": str(PROJECTION_PATH) if write else None,
    }
