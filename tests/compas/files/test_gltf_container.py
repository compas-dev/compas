import json
import struct

import pytest

from compas.files.gltf.gltf_container import GLTFParseError
from compas.files.gltf.gltf_container import parse_container


def glb(json_document, binary=b""):
    json_data = json.dumps(json_document).encode("utf-8")
    json_data += b" " * (-len(json_data) % 4)
    binary += b"\0" * (-len(binary) % 4)
    length = 20 + len(json_data) + (8 + len(binary) if binary else 0)
    data = b"glTF" + struct.pack("<II", 2, length)
    data += struct.pack("<I4s", len(json_data), b"JSON") + json_data
    if binary:
        data += struct.pack("<I4s", len(binary), b"BIN\0") + binary
    return data


def test_parse_container_decodes_json_and_glb():
    document = {"asset": {"version": "2.0"}}

    assert parse_container(json.dumps(document).encode())[0] == "gltf"
    format, restored, binary = parse_container(glb(document, b"data"))

    assert format == "glb"
    assert restored == document
    assert binary == b"data"


@pytest.mark.parametrize(
    "data",
    [
        b"not json",
        b"[]",
        b'{"asset":{"version":"1.0"}}',
        b"glTF" + struct.pack("<II", 1, 12),
        b"glTF" + struct.pack("<II", 2, 100),
    ],
)
def test_parse_container_rejects_invalid_data(data):
    with pytest.raises(GLTFParseError):
        parse_container(data)
