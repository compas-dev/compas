"""JSON glTF and binary GLB container decoding."""

import json
import struct
from typing import Optional

from .gltf_types import GLTFFormat
from .gltf_types import GLTFJson


class GLTFParseError(ValueError):
    """Error raised for invalid glTF data."""


def parse_container(data: bytes) -> tuple[GLTFFormat, GLTFJson, Optional[bytes]]:
    """Decode the primary JSON glTF or GLB container.

    Returns
    -------
    tuple[GLTFFormat, GLTFJson, bytes | None]
        Container format, JSON document, and optional GLB binary chunk.

    """
    if data[:4] == b"glTF":
        return _parse_glb(data)
    try:
        document = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise GLTFParseError("Invalid JSON glTF data.") from error
    if not isinstance(document, dict):
        raise GLTFParseError("The glTF JSON root must be an object.")
    _validate_version(document)
    return "gltf", document, None


def _parse_glb(data: bytes) -> tuple[GLTFFormat, GLTFJson, Optional[bytes]]:
    if len(data) < 20:
        raise GLTFParseError("GLB data is incomplete.")
    magic, version, declared_length = struct.unpack_from("<4sII", data)
    if magic != b"glTF" or version != 2:
        raise GLTFParseError("Invalid GLB header.")
    if declared_length != len(data):
        raise GLTFParseError("GLB length does not match its header.")

    offset = 12
    chunks: list[tuple[bytes, bytes]] = []
    while offset < len(data):
        if offset + 8 > len(data):
            raise GLTFParseError("GLB chunk header is incomplete.")
        length, chunk_type = struct.unpack_from("<I4s", data, offset)
        offset += 8
        if offset + length > len(data):
            raise GLTFParseError("GLB chunk data is incomplete.")
        chunks.append((chunk_type, data[offset : offset + length]))
        offset += length
    if not chunks or chunks[0][0] != b"JSON":
        raise GLTFParseError("The first GLB chunk must contain JSON.")
    if len(chunks) > 2 or len(chunks) == 2 and chunks[1][0] != b"BIN\0":
        raise GLTFParseError("GLB contains an unsupported chunk layout.")
    try:
        document = json.loads(chunks[0][1].decode("utf-8").rstrip(" \0"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise GLTFParseError("Invalid JSON in GLB container.") from error
    if not isinstance(document, dict):
        raise GLTFParseError("The glTF JSON root must be an object.")
    _validate_version(document)
    return "glb", document, chunks[1][1] if len(chunks) == 2 else None


def _validate_version(document: GLTFJson) -> None:
    asset = document.get("asset")
    if not isinstance(asset, dict) or asset.get("version") != "2.0":
        raise GLTFParseError("glTF asset version 2.0 is required.")
