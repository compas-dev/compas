from io import BytesIO
from pathlib import Path

import pytest

from compas.files import GLTFDocument
from compas.files import GLTFEncoder
from compas.files import GLTFWriter
from compas.files import read_gltf
from compas.files import write_gltf
from compas.files.gltf.gltf_node import GLTFNode
from compas.files.gltf.gltf_mesh import GLTFMesh


FIXTURES = Path(__file__).parent / "fixtures" / "gltf"


def test_glb_roundtrip_through_stream():
    content = read_gltf(FIXTURES / "SimpleMeshes.gltf")
    stream = BytesIO()

    write_gltf(stream, content, format="glb")
    stream.seek(0)
    restored = read_gltf(stream)

    assert len(restored.scenes) == len(content.scenes)
    assert len(restored.nodes) == len(content.nodes)
    assert len(restored.meshes) == len(content.meshes)


def test_gltf_roundtrip_writes_external_buffer(tmp_path):
    content = read_gltf(FIXTURES / "SimpleMeshes.gltf")
    target = tmp_path / "result.gltf"

    write_gltf(target, content)
    restored = read_gltf(target)

    assert (tmp_path / "result.bin").is_file()
    assert len(restored.meshes) == len(content.meshes)


def test_encoding_does_not_remove_orphans_from_input():
    content = GLTFDocument()
    content.add_scene()
    GLTFNode(content)
    original_node_count = len(content.nodes)

    GLTFEncoder().encode(content)

    assert len(content.nodes) == original_node_count


def test_external_resources_cannot_be_written_next_to_stream():
    content = read_gltf(FIXTURES / "SimpleMeshes.gltf")
    payload = GLTFEncoder().encode(content)

    with pytest.raises(ValueError, match="filesystem target"):
        GLTFWriter(BytesIO()).write(payload)


def test_encoding_preserves_asset_required_extensions_and_unknown_metadata():
    content = GLTFDocument()
    content.asset = {"version": "2.0", "generator": "test"}
    content.extensions_used = ["EXT_example"]
    content.extensions_required = ["EXT_example"]
    content.unknown = {"vendorProperty": {"value": 1}}

    payload = GLTFEncoder(format="glb").encode(content)

    assert payload.json["asset"]["generator"] == "test"
    assert payload.json["extensionsUsed"] == ["EXT_example"]
    assert payload.json["extensionsRequired"] == ["EXT_example"]
    assert payload.json["vendorProperty"] == {"value": 1}


def test_encoding_uses_unsigned_int_for_large_mesh_indices():
    content = GLTFDocument()
    scene = content.add_scene()
    node = scene.add_child()
    vertices = [[0.0, 0.0, 0.0]] * 65537
    mesh = GLTFMesh.from_vertices_and_faces(content, vertices, [[0, 1, 65536]])
    node.mesh_key = mesh.key

    payload = GLTFEncoder(format="glb").encode(content)

    primitive = payload.json["meshes"][0]["primitives"][0]
    assert payload.json["accessors"][primitive["indices"]]["componentType"] == 5125


def test_repeated_encoding_is_deterministic_and_non_mutating():
    content = read_gltf(FIXTURES / "SpecularTest.glb")

    first = GLTFEncoder(format="glb").encode(content)
    second = GLTFEncoder(format="glb").encode(content)

    assert first.json == second.json
    assert first.binary == second.binary
