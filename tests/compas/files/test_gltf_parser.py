import json
from io import BytesIO

import pytest

from compas.files import read_gltf
from compas.files.gltf.gltf_container import GLTFParseError
from compas.files.gltf.gltf_accessors import GLTFAccessorDecoder


def test_read_gltf_parses_stream():
    content = read_gltf(BytesIO(json.dumps({"asset": {"version": "2.0"}}).encode()))

    assert content.scenes == {}
    assert content.meshes == {}


def test_read_gltf_stream_requires_loader_for_external_resources():
    document = {
        "asset": {"version": "2.0"},
        "buffers": [{"uri": "data.bin", "byteLength": 4}],
        "bufferViews": [{"buffer": 0, "byteLength": 4}],
        "accessors": [{"bufferView": 0, "componentType": 5126, "count": 1, "type": "SCALAR"}],
    }

    with pytest.raises(GLTFParseError, match="resource loader"):
        read_gltf(BytesIO(json.dumps(document).encode()))


def test_read_gltf_preserves_asset_extension_and_unknown_metadata():
    document = {
        "asset": {"version": "2.0", "generator": "test"},
        "extensionsUsed": ["EXT_example"],
        "extensionsRequired": ["EXT_example"],
        "vendorProperty": {"value": 1},
    }

    content = read_gltf(BytesIO(json.dumps(document).encode()))

    assert content.asset["generator"] == "test"
    assert content.extensions_used == ["EXT_example"]
    assert content.extensions_required == ["EXT_example"]
    assert content.unknown == {"vendorProperty": {"value": 1}}


def test_accessor_decoder_handles_padded_unsigned_byte_matrices():
    binary = bytes([1, 2, 3, 0, 4, 5, 6, 0, 7, 8, 9, 0])
    document = {
        "buffers": [{"byteLength": len(binary)}],
        "bufferViews": [{"buffer": 0, "byteLength": len(binary)}],
        "accessors": [{"bufferView": 0, "componentType": 5121, "count": 1, "type": "MAT3"}],
    }

    values = GLTFAccessorDecoder(document, binary, None).decode_all()

    assert values == [[(1, 2, 3, 4, 5, 6, 7, 8, 9)]]


def test_accessor_decoder_normalizes_non_sparse_accessors():
    document = {
        "buffers": [{"byteLength": 1}],
        "bufferViews": [{"buffer": 0, "byteLength": 1}],
        "accessors": [
            {"bufferView": 0, "componentType": 5121, "count": 1, "type": "SCALAR", "normalized": True}
        ],
    }

    assert GLTFAccessorDecoder(document, b"\xff", None).decode_all() == [[1.0]]


def test_accessor_decoder_rejects_invalid_stride():
    document = {
        "buffers": [{"byteLength": 12}],
        "bufferViews": [{"buffer": 0, "byteLength": 12, "byteStride": 4}],
        "accessors": [{"bufferView": 0, "componentType": 5126, "count": 1, "type": "VEC3"}],
    }

    with pytest.raises(GLTFParseError, match="stride"):
        GLTFAccessorDecoder(document, b"\0" * 12, None).decode_all()
