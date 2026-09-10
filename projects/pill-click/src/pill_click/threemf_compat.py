"""Compatibility repair for strict slicers reading otherwise-valid 3MF packages.

Some slicers reject OPC wrapper documents whose default namespaces are emitted
with an arbitrary ``ns0`` prefix.  The XML is standards-valid, but rewriting
the two small wrapper documents with explicit default namespaces makes the
same 3MF package load reliably without touching its model geometry.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import tempfile
import xml.etree.ElementTree as ET
from zipfile import ZIP_DEFLATED, BadZipFile, ZipFile


CONTENT_TYPES_PART = "[Content_Types].xml"
RELATIONSHIPS_PART = "_rels/.rels"
CONTENT_TYPES_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
RELATIONSHIPS_NS = "http://schemas.openxmlformats.org/package/2006/relationships"


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _canonical_default_namespace_xml(data: bytes, namespace: str) -> bytes:
    source = ET.fromstring(data)
    root = ET.Element(_local_name(source.tag), {"xmlns": namespace, **source.attrib})
    for child in source:
        ET.SubElement(root, _local_name(child.tag), child.attrib)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def normalize_3mf_opc_wrappers(path: str | Path) -> Path:
    """Rewrite only the two OPC wrapper XML parts of ``path`` in place."""

    target = Path(path)
    if target.suffix.lower() != ".3mf":
        raise ValueError(f"expected a .3mf file, got {target}")

    try:
        with ZipFile(target, "r") as source:
            names = source.namelist()
            required = {CONTENT_TYPES_PART, RELATIONSHIPS_PART, "3D/3dmodel.model"}
            missing = required.difference(names)
            if missing:
                raise ValueError(f"3MF is missing required package parts: {sorted(missing)}")
            entries = [(info, source.read(info.filename)) for info in source.infolist()]
    except BadZipFile as exc:
        raise ValueError(f"not a readable 3MF ZIP package: {target}") from exc

    package_parts = {info.filename: data for info, data in entries}
    replacements = {
        CONTENT_TYPES_PART: _canonical_default_namespace_xml(
            package_parts[CONTENT_TYPES_PART],
            CONTENT_TYPES_NS,
        ),
        RELATIONSHIPS_PART: _canonical_default_namespace_xml(
            package_parts[RELATIONSHIPS_PART],
            RELATIONSHIPS_NS,
        ),
    }

    with tempfile.NamedTemporaryFile(
        prefix=f".{target.name}.", suffix=".tmp", dir=target.parent, delete=False
    ) as temporary:
        temporary_path = Path(temporary.name)

    try:
        with ZipFile(temporary_path, "w", compression=ZIP_DEFLATED) as destination:
            for info, data in entries:
                destination.writestr(info, replacements.get(info.filename, data))
        with ZipFile(temporary_path, "r") as check:
            if check.testzip() is not None:
                raise ValueError("rewritten 3MF failed its ZIP CRC check")
            ET.fromstring(check.read("3D/3dmodel.model"))
        os.replace(temporary_path, target)
    finally:
        temporary_path.unlink(missing_ok=True)

    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Rewrite 3MF OPC wrappers for strict slicer compatibility."
    )
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args(argv)
    for path in args.paths:
        print(normalize_3mf_opc_wrappers(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
