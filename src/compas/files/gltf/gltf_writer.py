"""Target writing for encoded glTF payloads."""

import json
import struct
from os import PathLike
from pathlib import Path

from compas import _iotools

from .gltf_payload import GLTFPayload


class GLTFWriter:
    """Write an encoded payload and any adjacent resources."""

    def __init__(self, target: _iotools.IOTarget) -> None:
        self.target = target

    def write(self, payload: GLTFPayload) -> None:
        """Write an encoded payload.

        """
        if payload.format == "glb":
            _iotools.write_bytes(self.target, _glb_bytes(payload))
            return
        data = json.dumps(payload.json, indent=4).encode("utf-8")
        _iotools.write_bytes(self.target, data)
        if not payload.resources:
            return
        if not isinstance(self.target, (str, PathLike)):
            raise ValueError("External glTF resources require a filesystem target.")
        directory = Path(self.target).parent
        for name, resource in payload.resources.items():
            _iotools.write_bytes(directory / name, resource)


def _glb_bytes(payload: GLTFPayload) -> bytes:
    json_data = json.dumps(payload.json, indent=4).encode("utf-8")
    json_data += b" " * (-len(json_data) % 4)
    binary = payload.binary + b"\0" * (-len(payload.binary) % 4)
    length = 12 + 8 + len(json_data) + (8 + len(binary) if binary else 0)
    result = b"glTF" + struct.pack("<II", 2, length)
    result += struct.pack("<I4s", len(json_data), b"JSON") + json_data
    if binary:
        result += struct.pack("<I4s", len(binary), b"BIN\0") + binary
    return result
